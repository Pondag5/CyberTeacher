"""
Tests for CVE lookup handler.
"""

import unittest
from unittest.mock import patch, MagicMock

from handlers.cve import handle_cve, _cve_cache


class TestCVEHandler(unittest.TestCase):
    """Tests for /cve command handler."""

    def setUp(self):
        _cve_cache.clear()

    @patch("handlers.cve.console")
    def test_cve_no_id_provided(self, mock_console):
        success, _, _, continue_loop = handle_cve("/cve")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.cve._fetch_cve")
    @patch("handlers.cve.get_state")
    @patch("handlers.cve.console")
    def test_cve_found(self, mock_console, mock_get_state, mock_fetch):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_fetch.return_value = {
            "descriptions": [{"value": "Test CVE description"}],
            "metrics": {
                "cvssMetricV31": [{"cvssData": {"baseScore": 7.5}}]
            },
            "references": [{"url": "https://example.com"}],
        }

        success, _, _, continue_loop = handle_cve("/cve CVE-2024-1234")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.cve._fetch_cve")
    @patch("handlers.cve.get_state")
    @patch("handlers.cve.console")
    def test_cve_not_found(self, mock_console, mock_get_state, mock_fetch):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_fetch.return_value = None

        success, _, _, continue_loop = handle_cve("/cve CVE-2024-9999")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.cve.console")
    def test_cve_cache_hit(self, mock_console):
        # Populate cache manually
        import time
        _cve_cache["CVE-2024-1234"] = (time.time(), {
            "descriptions": [{"value": "Cached CVE"}],
            "metrics": {"cvssMetricV31": [{"cvssData": {"baseScore": 5.0}}]},
            "references": [],
        })

        with patch("handlers.cve._fetch_cve") as mock_fetch:
            with patch("handlers.cve.get_state") as mock_get_state:
                mock_get_state.return_value = MagicMock()

                handle_cve("/cve CVE-2024-1234")

                # Should use cache, not fetch
                mock_fetch.assert_not_called()

    @patch("handlers.cve._fetch_cve")
    @patch("handlers.cve.get_state")
    @patch("handlers.cve.console")
    def test_cve_missing_metrics(self, mock_console, mock_get_state, mock_fetch):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state
        mock_fetch.return_value = {
            "descriptions": [{"value": "CVE without metrics"}],
            "metrics": {},
            "references": [],
        }

        success, _, _, continue_loop = handle_cve("/cve CVE-2024-5678")

        self.assertTrue(success)
        mock_console.print.assert_called()


if __name__ == "__main__":
    unittest.main()
