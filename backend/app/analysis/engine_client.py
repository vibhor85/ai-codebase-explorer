import json
import subprocess
from pathlib import Path
from typing import Any


def analyze(repository_root: Path, files: list[Path]) -> list[dict[str, str]]:
    """Send a TypeScript analysis request to the Node engine and return relationships."""
    repository_root = Path(repository_root).resolve()
    engine_entry = (
        Path(__file__).resolve().parents[2].parent
        / "code-analysis-engine"
        / "dist"
        / "index.js"
    )

    if not engine_entry.exists():
        raise FileNotFoundError(
            f"TypeScript analysis engine entry point not found: {engine_entry}"
        )

    request_body = {
        "repositoryRoot": str(repository_root),
        "files": [str(Path(file).resolve()) for file in files],
    }

    result = subprocess.run(
        ["node", str(engine_entry)],
        input=json.dumps(request_body),
        capture_output=True,
        text=True,
        cwd=str(engine_entry.parent),
    )

    if result.returncode != 0:
        raise RuntimeError(
            "TypeScript analysis engine failed"
            f" (exit code={result.returncode})."
            f" stdout={result.stdout!r} stderr={result.stderr!r}"
        )

    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Failed to parse JSON response from TypeScript analysis engine."
        ) from exc

    if not isinstance(response, dict):
        raise RuntimeError(
            "Unexpected response shape from TypeScript analysis engine."
        )

    relationships = response.get("relationships")
    if relationships is None:
        raise RuntimeError("Response missing required 'relationships' field.")
    if not isinstance(relationships, list):
        raise RuntimeError("Response 'relationships' field must be a list.")

    return relationships
