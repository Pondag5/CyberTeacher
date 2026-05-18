"""
Тесты для TryHackMe API интеграции (G-01).
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handlers.tryhackme import (
    _load_thm_key,
    _save_thm_key,
)


class TestTHMKeyManagement(unittest.TestCase):
    """Тесты управления API ключом."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_key_file = os.path.join(self.temp_dir, "thm_api_key.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_and_load_key(self):
        original_file = "handlers.tryhackme.THM_KEY_FILE"
        with patch(original_file, self.test_key_file):
            _save_thm_key("test_api_key_123")
            self.assertTrue(os.path.exists(self.test_key_file))

            loaded = _load_thm_key()
            self.assertEqual(loaded, "test_api_key_123")

    def test_load_nonexistent_key(self):
        nonexistent = os.path.join(self.temp_dir, "nonexistent.json")
        with patch("handlers.tryhackme.THM_KEY_FILE", nonexistent):
            self.assertIsNone(_load_thm_key())

    def test_save_key_creates_directory(self):
        nested = os.path.join(self.temp_dir, "nested", "dir", "thm_key.json")
        with patch("handlers.tryhackme.THM_KEY_FILE", nested):
            _save_thm_key("test_key")
            self.assertTrue(os.path.exists(nested))


class TestTHMRequest(unittest.TestCase):
    """Тесты API запросов."""

    @patch("handlers.tryhackme._load_thm_key")
    @patch("handlers.tryhackme.requests.get")
    def test_successful_request(self, mock_get, mock_key):
        mock_key.return_value = "test_key"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": []}
        mock_get.return_value = mock_response

        from handlers.tryhackme import _thm_request
        result = _thm_request("/v2/rooms")
        self.assertIsNotNone(result)
        self.assertTrue(result["success"])

    @patch("handlers.tryhackme._load_thm_key")
    def test_no_api_key(self, mock_key):
        mock_key.return_value = None

        from handlers.tryhackme import _thm_request
        result = _thm_request("/v2/rooms")
        self.assertIsNone(result)

    @patch("handlers.tryhackme._load_thm_key")
    @patch("handlers.tryhackme.requests.get")
    def test_failed_request(self, mock_get, mock_key):
        mock_key.return_value = "test_key"
        mock_get.side_effect = Exception("Network error")

        from handlers.tryhackme import _thm_request
        result = _thm_request("/v2/rooms")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
