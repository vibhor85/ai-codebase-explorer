from pathlib import Path

from fastapi import APIRouter

from app.analysis.engine_client import analyze
from app.analysis.source_files import collect_source_files
from .models import LoadRepositoryRequest
from .scanner import scan_repository


router = APIRouter()


@router.post("/repository/load")
def post_repository(request: LoadRepositoryRequest):
    repository_path = Path(request.path)
    repository_node = scan_repository(repository_path)
    source_files = collect_source_files(repository_node)
    relationships = analyze(repository_path, source_files)
    return {"relationships": relationships}
