"""
Тесты для реального Docker в PWA (KB-02).
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDockerStatus(unittest.TestCase):
    """Тесты проверки статуса Docker."""

    @patch("handlers.pcap_analyzer.console")
    @patch("api_server.subprocess.run")
    @patch("api_server.get_state")
    def test_docker_available(self, mock_state, mock_run, mock_console):
        mock_run.return_value = MagicMock(returncode=0)
        from api_server import docker_status
        result = docker_status()
        self.assertTrue(result["available"])

    @patch("api_server.subprocess.run")
    def test_docker_not_available(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        from api_server import docker_status
        result = docker_status()
        self.assertFalse(result["available"])

    @patch("api_server.subprocess.run")
    def test_docker_not_installed(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        from api_server import docker_status
        result = docker_status()
        self.assertFalse(result["available"])


class TestDockerContainers(unittest.TestCase):
    """Тесты списка контейнеров."""

    @patch("api_server.subprocess.run")
    def test_list_containers(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="cyberteacher-dvwa\tUp 2 hours\t0.0.0.0:8080->80/tcp\n"
        )
        from api_server import docker_containers
        result = docker_containers()
        self.assertEqual(len(result["containers"]), 1)
        self.assertEqual(result["containers"][0]["name"], "cyberteacher-dvwa")

    @patch("api_server.subprocess.run")
    def test_no_containers(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        from api_server import docker_containers
        result = docker_containers()
        self.assertEqual(len(result["containers"]), 0)


if __name__ == "__main__":
    unittest.main()
