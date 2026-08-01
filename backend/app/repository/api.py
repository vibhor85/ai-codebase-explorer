from pathlib import Path

from fastapi import APIRouter, HTTPException

from .exception import InvalidRepositoryPathException
from .models import LoadRepositoryRequest
from .scanner import scan_repository


router = APIRouter()


@router.post("/repository/load")
def post_repository(request: LoadRepositoryRequest):
    path = Path(request.path)
    return scan_repository(path)
