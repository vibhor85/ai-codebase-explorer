class ImportExtractor:
    """
    Responsibility:
        Extract raw import relationships from an AST.

    Input:
        file_path
        ast

    Output:
        List[Relationship]

    Notes:
        - No path resolution.
        - Uses DFS.
    """
