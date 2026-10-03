import json
from common.models import RepositoryKnowledge


def build_context_selection_prompt(
    question: str,
    repository: RepositoryKnowledge,
) -> str:

    repository_json = json.dumps(
        repository.model_dump(mode='json'),
        indent=2,
    )

    return f"""
You are a context selector for a repository analysis system.

User question:
{question}

Repository knowledge:
{repository_json}

Select the repository files that should be retrieved to help answer
the user's question.

Rules:

- Only select files that exist in the provided repository knowledge.
- Use only the information provided in the repository knowledge.
- Do not assume what a file contains or what it does.
- Do not invent files or relationships.
- Do not provide an explanation or answer to the user's question.
- Return only the files that are relevant to investigating the question.
- If the repository knowledge does not provide evidence that the
  requested functionality exists, return an empty list.
"""
