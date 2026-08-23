from backend.app.analysis.engine_client import analyze
from config.config import REPOSITORY_ROOT
from ai_service import answer

target_file = REPOSITORY_ROOT / "Login.tsx"

relationships = analyze(
    REPOSITORY_ROOT,
    [target_file],
)

question = "Explain the dependencies of Login.tsx."

result = answer(question, relationships)

print(result)
