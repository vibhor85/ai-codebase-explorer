from fastapi import APIRouter, HTTPException

from .exception import InvalidRepositoryPathException
from .models import LoadRepositoryRequest
from .scanner import scan_repository


router = APIRouter()


@router.post("/repository/post")
def post_repository(request: LoadRepositoryRequest):
    return scan_repository(request.path)
