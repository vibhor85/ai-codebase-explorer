import json


def build_dependency_analysis_prompt(
    question: str,
    relationships: list[dict[str, str]],
) -> str:

    relationships_json = json.dumps(
        relationships,
        indent=2,
    )

    return f"""
        {question}
    
        The repository analysis engine has already identified the dependency
        relationships for the target file. These relationships are authoritative
        for dependency discovery.
    
        Dependency relationships:
        {relationships_json}
    
        Before answering, retrieve the source code of:
    
        1. The target file: Login.tsx
        2. All relevant internal repository dependencies identified above.
    
        Do not skip the target file. You need the target file's source code to
        verify how it actually uses its dependencies.
    
        When two or more repository files need to be retrieved, use the
        get_multiple_files tool instead of calling get_repository_file multiple
        times.
    
        The get_multiple_files tool accepts a maximum of 3 files per call.
        If more than 3 files are required, split the retrieval into multiple
        calls of at most 3 files each.
    
        Do not attempt to retrieve external packages such as "react" using
        repository file tools.
    
        IMPORTANT RULES:
    
        - Do not rediscover imports or dependencies yourself.
        - Treat the provided dependency relationships as authoritative for
        dependency discovery.
        - Retrieve the target file before making claims about how it uses its
        dependencies.
        - Retrieve the source code of relevant internal dependencies before
        making claims about their implementation.
        - Do not assume the implementation of a dependency without inspecting
        its source code.
        - Do not rely on typical or hypothetical behavior when repository
        evidence is available.
        - Before making a claim about a file, verify that the file was actually
        retrieved.
        - If required information was not retrieved, say:
        "Cannot determine from the retrieved repository files."
    
        For each important claim, clearly distinguish:
    
        - EVIDENCE: directly supported by retrieved source code.
        - INFERENCE: a reasonable conclusion based on retrieved source code.
        - UNKNOWN: cannot be determined from the retrieved repository files.
        """
