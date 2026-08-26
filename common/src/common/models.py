from enum import Enum
from pathlib import Path

from pydantic import BaseModel


class NodeType(str, Enum):
    FILE = "file"
    DIRECTORY = "directory"


class RepositoryMetadata(BaseModel):
    name: str
    path: Path


class FileMetadata(BaseModel):
    name: str
    path: Path
    type: NodeType


class DependencyRelationship(BaseModel):
    source: str
    target: str | None


class RepositoryKnowledge(BaseModel):
    repository: RepositoryMetadata
    files: list[FileMetadata]
    relationships: list[DependencyRelationship]
