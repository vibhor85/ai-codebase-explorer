from pathlib import Path
from enum import Enum

from pydantic import BaseModel, Field


class LoadRepositoryRequest(BaseModel):
    path: str


class NodeType(str, Enum):
    FILE = "file"
    DIRECTORY = "directory"


class RepositoryNode(BaseModel):
    name: str
    path: Path
    type: NodeType
    children: list[RepositoryNode] = Field(default_factory=list)
