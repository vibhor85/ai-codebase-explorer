from langchain.tools import tool
from pathlib import Path
from config.config import REPOSITORY_ROOT


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


def get_file(repository_root: str, file_path: str) -> dict:
    """
    Read a single file from a repository, by path relative to the repo root.

    Args:
        repository_root: Root directory of the repository being analyzed.
        file_path: Path to the requested file, relative to repository_root
                    (e.g. "Login.tsx" or "services/AuthService.ts").

    Returns:
        On success: {"path": file_path, "content": "<file contents>"}
        On failure: {"path": file_path, "error": "<reason>"}
    """
    root = Path(repository_root).resolve()
    requested = (root / file_path).resolve()

    # Security: the resolved path must stay inside repository_root.
    # This blocks path traversal like "../../.env".
    if root not in requested.parents and requested != root:
        return {"status": "error", "path": file_path, "error": "Path is outside repository_root"}

    if not requested.exists():
        return {"status": "error", "path": file_path, "error": "File not found"}

    if not requested.is_file():
        return {"status": "error", "path": file_path, "error": "Path is not a file"}

    try:
        content = requested.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"status": "error", "path": file_path, "error": "File is not valid UTF-8 text"}

    return {
        "status": "success",
        "path": file_path,
        "content": content,
    }
