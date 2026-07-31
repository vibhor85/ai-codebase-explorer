from fastapi import APIRouter

from .scanner import scan_repository
from .models import LoadRepositoryRequest


router = APIRouter()


@router.post("/repository/post")
def post_repository(request: LoadRepositoryRequest):
    return scan_repository(request.path)
