from pathlib import Path
import unittest

from app.analysis.source_files import collect_source_files
from app.repository.models import NodeType, RepositoryNode


class CollectSourceFilesTest(unittest.TestCase):
    def test_collects_typescript_files_from_repository_node_tree(self):
        root = RepositoryNode(
            name="samples",
            path=Path("../code-analysis-engine/samples"),
            type=NodeType.DIRECTORY,
            children=[
                RepositoryNode(
                    name="Login.tsx",
                    path=Path("../code-analysis-engine/samples/Login.tsx"),
                    type=NodeType.FILE,
                ),
                RepositoryNode(
                    name="services",
                    path=Path("../code-analysis-engine/samples/services"),
                    type=NodeType.DIRECTORY,
                    children=[
                        RepositoryNode(
                            name="AuthService.ts",
                            path=Path(
                                "../code-analysis-engine/samples/services/AuthService.ts"),
                            type=NodeType.FILE,
                        ),
                        RepositoryNode(
                            name="README.md",
                            path=Path(
                                "../code-analysis-engine/samples/services/README.md"),
                            type=NodeType.FILE,
                        ),
                    ],
                ),
            ],
        )

        expected = [
            Path("../code-analysis-engine/samples/Login.tsx"),
            Path("../code-analysis-engine/samples/services/AuthService.ts"),
        ]
        self.assertEqual(collect_source_files(root), expected)


if __name__ == "__main__":
    unittest.main()
