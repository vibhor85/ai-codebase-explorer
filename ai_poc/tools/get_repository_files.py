import json

from langchain.tools import tool
from ai_poc.tools.get_repository_file import get_file
from ai_poc.config.config import REPOSITORY_ROOT


@tool
def get_multiple_files(file_paths):
    """
    Read multiple source files from the repository.

    Use this tool when you need the contents of multiple repository files
    at once. File paths must be relative to the repository root.

    Example:
        [
            "services/AuthService.ts",
            "services/UserService.ts"
        ]

    Returns one result for each requested file. Individual file failures
    are returned as errors rather than failing the entire operation.
    """
    results = []

    for file_path in file_paths:
        result = get_file(REPOSITORY_ROOT, file_path)
        results.append(result)

    print("[TOOL RESULT]", results)

    return json.dumps(results)
