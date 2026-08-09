import subprocess
from app.repository.scanner import scan_repository
from pathlib import Path

repository_path = Path("../code-analysis-engine/samples")

repository_node = scan_repository(repository_path)

input = repository_node.model_dump_json()

result = subprocess.run(
    ["node", "../code-analysis-engine/dist/index.js"],
    input=input,
    capture_output=True,
    text=True,
)

print(result.stdout)
