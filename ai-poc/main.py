from backend.app.analysis.engine_client import analyze
from backend.app.analysis.source_files import collect_source_files
from backend.app.repository.scanner import scan_repository
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


repository_path = Path(
    "/Users/vibhorkumar/AI/AI-Codebase-Explorer/code-analysis-engine/samples")

repository_node = scan_repository(repository_path)

source_files = collect_source_files(repository_node)

relationships = analyze(repository_path, source_files)

print("relationships: ", relationships)

login_source = Path(
    "/Users/vibhorkumar/AI/AI-Codebase-Explorer/code-analysis-engine/samples/Login.tsx"
).read_text()

auth_service_source = Path(
    "/Users/vibhorkumar/AI/AI-Codebase-Explorer/code-analysis-engine/samples/services/AuthService.ts"
).read_text()

user_service_source = Path(
    "/Users/vibhorkumar/AI/AI-Codebase-Explorer/code-analysis-engine/samples/services/UserService.ts"
).read_text()

model = init_chat_model(
    "gemini-3.6-flash",
    model_provider="google_genai",
)

prompt = f"""
Analyze Login.tsx using ONLY the provided source code and dependency relationships.

For each dependency:

1. Explain how Login.tsx actually uses it.
2. Identify the specific function, hook, type, or component being used.
3. Explain its role based only on evidence in the provided code.
4. Clearly distinguish:
   - EVIDENCE: directly supported by the provided code.
   - INFERENCE: a reasonable conclusion derived from the provided code.
   - UNKNOWN: cannot be determined from the provided information.
5. Do not assume the internal implementation of an imported module unless its source code is provided.
6. Do not add typical or hypothetical behavior.
7. If something cannot be determined, explicitly say:
   "Cannot determine from the provided information."

For each important claim, provide the relevant evidence from the source.

Source code: Login.tsx
{login_source}

Source code: AuthService.ts
{auth_service_source}

Source code: UserService.ts
{user_service_source}

Dependency relationships:
{relationships}
"""

response = model.invoke(prompt)

print(response.content)

# agent = create_agent(
#     model=model,
#     tools=[],  # explicit, even if empty — see note below
# )

# response = agent.invoke({
#     "messages": [
#         {"role": "user", "content": """
# Here is some source code...

# Here are the dependency relationships...

# Explain the architecture.
# """}
#     ]
# })

# print(response["messages"][-1].content)
