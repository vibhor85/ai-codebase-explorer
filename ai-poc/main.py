from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langfuse.langchain import CallbackHandler
from langchain_groq import ChatGroq
from backend.app.analysis.engine_client import analyze
from config.config import REPOSITORY_ROOT
from tools.get_repository_file import get_repository_file
from tools.get_repository_files import get_multiple_files
import json


load_dotenv()
langfuse_handler = CallbackHandler()

target_file = REPOSITORY_ROOT / "Login.tsx"

relationships = analyze(
    REPOSITORY_ROOT,
    [target_file],
)

print(relationships)


# model = init_chat_model(
#     "gemini-3.6-flash",
#     model_provider="google_genai",
# )
model = ChatGroq(
    model="openai/gpt-oss-120b",
)


agent = create_agent(
    model=model,
    tools=[get_multiple_files],
)


relationships_json = json.dumps(
    relationships,
    indent=2,
)

prompt = f"""
Explain the dependencies of Login.tsx.

The repository analysis engine has already identified the dependency
relationships for the target file. These relationships are authoritative
for dependency discovery.

Dependency relationships:
{relationships_json}

Before answering, retrieve the source code of:

1. The target file: Login.tsx
2. All relevant internal repository dependencies identified above.

Do not skip the target file. You need the target file's source code to
verify how it actually uses its dependencies.

When two or more repository files need to be retrieved, use the
get_multiple_files tool instead of calling get_repository_file multiple
times.

The get_multiple_files tool accepts a maximum of 3 files per call.
If more than 3 files are required, split the retrieval into multiple
calls of at most 3 files each.

Do not attempt to retrieve external packages such as "react" using
repository file tools.

IMPORTANT RULES:

- Do not rediscover imports or dependencies yourself.
- Treat the provided dependency relationships as authoritative for
  dependency discovery.
- Retrieve the target file before making claims about how it uses its
  dependencies.
- Retrieve the source code of relevant internal dependencies before
  making claims about their implementation.
- Do not assume the implementation of a dependency without inspecting
  its source code.
- Do not rely on typical or hypothetical behavior when repository
  evidence is available.
- Before making a claim about a file, verify that the file was actually
  retrieved.
- If required information was not retrieved, say:
  "Cannot determine from the retrieved repository files."

For each important claim, clearly distinguish:

- EVIDENCE: directly supported by retrieved source code.
- INFERENCE: a reasonable conclusion based on retrieved source code.
- UNKNOWN: cannot be determined from the retrieved repository files.
"""

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    },
    config={
        "callbacks": [langfuse_handler]
    }
)


print(response["messages"][-1].content)
