from .models import (
    DependencyRelationship,
    FileMetadata,
    NodeType,
    RepositoryKnowledge,
    RepositoryMetadata,
    RepositoryNode,
)


def _collect_files(node: RepositoryNode) -> list[FileMetadata]:
    files = []

    if node.type == NodeType.FILE:
        files.append(
            FileMetadata(
                name=node.name,
                path=node.path,
                type=node.type,
            )
        )
        return files

    for child in node.children:
        files.extend(_collect_files(child))

    return files


def build_repository_knowledge(
    repository_node: RepositoryNode,
    relationships: list[dict[str, str | None]],
) -> RepositoryKnowledge:

    files = _collect_files(repository_node)

    dependency_relationships = [
        DependencyRelationship(**relationship)
        for relationship in relationships
    ]

    return RepositoryKnowledge(
        repository=RepositoryMetadata(
            name=repository_node.name,
            path=repository_node.path,
        ),
        files=files,
        relationships=dependency_relationships,
    )
