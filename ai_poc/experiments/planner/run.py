import json
from pathlib import Path
from common.models import RepositoryKnowledge
from ai_poc.ai_service import select_context


CASE_FILE = Path(__file__).parent / "cases" / "login_flow.json"


with CASE_FILE.open() as file:
    cases = json.load(file)


case = cases[1]

repository = RepositoryKnowledge.model_validate(case["repository"])

retrieval_plan = select_context(
    case["question"],
    repository,
)

print(retrieval_plan)
