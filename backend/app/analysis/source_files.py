from pathlib import Path

from app.repository.models import NodeType, RepositoryNode


def collect_source_files(repository_node: RepositoryNode) -> list[Path]:
    """Collect .ts and .tsx files from an existing RepositoryNode tree."""
    if repository_node.type == NodeType.FILE:
        if repository_node.path.suffix in {".ts", ".tsx"}:
            return [repository_node.path]
        return []

    source_files: list[Path] = []
    for child in repository_node.children:
        source_files.extend(collect_source_files(child))
    return source_files
