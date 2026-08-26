from pathlib import Path
from common.models import NodeType
from pydantic import BaseModel, Field


class LoadRepositoryRequest(BaseModel):
    question: str
    path: str


class RepositoryNode(BaseModel):
    name: str
    path: Path
    type: NodeType
    children: list[RepositoryNode] = Field(default_factory=list)
