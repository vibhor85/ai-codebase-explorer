from pathlib import Path

from fastapi import APIRouter

from app.analysis.engine_client import analyze
from app.analysis.source_files import collect_source_files
from ai_poc.ai_service import answer
from app.repository.knowledge import build_repository_knowledge
from .models import LoadRepositoryRequest
from .scanner import scan_repository


router = APIRouter()


@router.post("/repository/query")
def post_repository(request: LoadRepositoryRequest):
    repository_path = Path(request.path)
    repository_node = scan_repository(repository_path)
    source_files = collect_source_files(repository_node)
    relationships = analyze(repository_path, source_files)
    repository_knowledge = build_repository_knowledge(
        repository_node,
        relationships,
    )
    ai_answer = answer(request.question, repository_knowledge)
    return {
        "relationships": relationships,
        "answer": ai_answer,
    }
