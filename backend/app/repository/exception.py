class InvalidRepositoryPathException(Exception):

    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Invalid repository path: {path}")
