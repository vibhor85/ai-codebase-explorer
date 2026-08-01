from pathlib import Path

from .exception import InvalidRepositoryPathException
from .models import NodeType, RepositoryNode


def scan_repository(repository_path: Path) -> RepositoryNode:
    if not repository_path.exists() or not repository_path.is_dir():
        raise InvalidRepositoryPathException(str(repository_path))

    node = RepositoryNode(
        name=repository_path.name,
        path=repository_path,
        type=NodeType.DIRECTORY,
    )

    for child in repository_path.iterdir():
        if child.is_dir():
            child_node = scan_repository(path=child)
        else:
            child_node = RepositoryNode(
                name=child.name, path=child, type=NodeType.FILE)
        node.children.append(child_node)
    return node
