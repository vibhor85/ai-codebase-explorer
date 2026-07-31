from pydantic import BaseModel


class LoadRepositoryRequest(BaseModel):
    path: str
