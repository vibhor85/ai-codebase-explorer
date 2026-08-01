from pathlib import Path

from .exception import InvalidRepositoryPathException
from .models import NodeType, RepositoryNode


def scan_repository(path: str) -> RepositoryNode:
    repository_path = Path(path)
    if not repository_path.exists() or not repository_path.is_dir():
        raise InvalidRepositoryPathException(path)

    node = RepositoryNode(
        name=repository_path.name,
        path=repository_path,
        type=NodeType.DIRECTORY,
    )
    return node
