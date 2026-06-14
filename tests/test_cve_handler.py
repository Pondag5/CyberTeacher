"""
Tests for CVE lookup handler.
"""

import unittest
from unittest.mock import MagicMock, patch

from handlers.cve import CVE_CACHE, handle_cve


class TestCVEHandler(unittest.TestCase):
    """Tests for /cve command handler."""

    def setUp(self):
        CVE_CACHE.clear()

    @patch("handlers.cve.console")
    def test_cve_no_id_provided(self, mock_console):
        success, _, _, continue_loop = handle_cve("/cve")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.cve._fetch_cve")
    @patch("handlers.cve.console")
    def test_cve_found(self, mock_console, mock_fetch):
        mock_fetch.return_value = {
            "id": "CVE-2024-1234",
            "description": "Test CVE description",
            "published": "2024-01-01",
            "severity": "HIGH",
            "score": 7.5,
            "references": [{"url": "https://example.com"}],
        }

        success, _, _, continue_loop = handle_cve("/cve CVE-2024-1234")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.cve._fetch_cve")
    @patch("handlers.cve.console")
    def test_cve_not_found(self, mock_console, mock_fetch):
        mock_fetch.return_value = None

        success, _, _, continue_loop = handle_cve("/cve CVE-2024-9999")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.cve.console")
    def test_cve_cache_hit(self, mock_console):
        import time

        CVE_CACHE["CVE-2024-1234"] = (
            time.time(),
            {
                "id": "CVE-2024-1234",
                "description": "Cached CVE",
                "published": "2024-01-01",
                "severity": "MEDIUM",
                "score": 5.0,
                "references": [],
            },
        )

        with patch("handlers.cve._fetch_cve") as mock_fetch:
            handle_cve("/cve CVE-2024-1234")
            mock_fetch.assert_not_called()

    @patch("handlers.cve._fetch_cve")
    @patch("handlers.cve.console")
    def test_cve_missing_metrics(self, mock_console, mock_fetch):
        mock_fetch.return_value = {
            "id": "CVE-2024-5678",
            "description": "CVE without metrics",
            "published": "2024-01-01",
            "severity": "UNKNOWN",
            "score": 0,
            "references": [],
        }

        success, _, _, continue_loop = handle_cve("/cve CVE-2024-5678")

        self.assertTrue(success)
        mock_console.print.assert_called()


if __name__ == "__main__":
    unittest.main()
