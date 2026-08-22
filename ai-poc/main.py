from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langfuse.langchain import CallbackHandler

from tools.get_file import get_file


load_dotenv()
langfuse_handler = CallbackHandler()

REPOSITORY_ROOT = Path(
    "/Users/vibhorkumar/AI/AI-Codebase-Explorer/code-analysis-engine/samples"
).resolve()


@tool
def get_repository_file(file_path: str) -> dict:
    """
    Read a source file from the repository using a path relative to the
    repository root.

    Example:
        Login.tsx
        services/AuthService.ts
    """
    print(f"\n[TOOL CALL] get_repository_file({file_path})")

    result = get_file(
        str(REPOSITORY_ROOT),
        file_path,
    )

    print(f"[TOOL RESULT] Path: {result['path']}, Status: {result['status']}")
    return result


model = init_chat_model(
    "gemini-3.6-flash",
    model_provider="google_genai",
)


agent = create_agent(
    model=model,
    tools=[get_repository_file],
)


prompt = """
Explain the dependencies of Login.tsx.

You have access to the repository through the get_repository_file tool.

IMPORTANT RULES:

- Use the repository tool to inspect the files you need.
- Treat every successful tool result as direct evidence that the requested file
  exists and that its returned content is the actual file content.
- Never claim that a file does not exist if the tool successfully returned its
  contents.
- Do not contradict information returned by the tool.
- Before making a claim about a file, verify that the file was actually
  retrieved.
- Do not assume the implementation of a dependency without inspecting its
  source code.
- Do not rely on typical or hypothetical behavior when repository evidence
  is available.
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
