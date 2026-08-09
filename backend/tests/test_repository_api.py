from pathlib import Path
import unittest
from unittest.mock import patch

from app.repository.api import post_repository
from app.repository.models import LoadRepositoryRequest


class RepositoryApiTest(unittest.TestCase):
    @patch("app.repository.api.analyze", return_value=[{"source": "a", "target": "b"}])
    @patch("app.repository.api.collect_source_files", return_value=[Path("/tmp/example.ts")])
    @patch("app.repository.api.scan_repository")
    def test_post_repository_wires_components_together(self, scan_repository_mock, collect_source_files_mock, analyze_mock):
        repository_node = object()
        scan_repository_mock.return_value = repository_node

        request = LoadRepositoryRequest(path="/tmp/repo")

        response = post_repository(request)

        scan_repository_mock.assert_called_once_with(Path("/tmp/repo"))
        collect_source_files_mock.assert_called_once_with(repository_node)
        analyze_mock.assert_called_once_with(
            Path("/tmp/repo"), [Path("/tmp/example.ts")])
        self.assertEqual(response, {"relationships": [
                         {"source": "a", "target": "b"}]})


if __name__ == "__main__":
    unittest.main()
