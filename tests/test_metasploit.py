"""
Тесты для Metasploit интеграции (L-09).
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMetasploitAction(unittest.TestCase):
    """Тесты команд Metasploit."""

    @patch("handlers.metasploit.console")
    def test_msf_no_args_shows_help(self, mock_console):
        from handlers.metasploit import handle_msf_action
        result = handle_msf_action("msf")
        self.assertTrue(result[0])

    @patch("handlers.metasploit.console")
    def test_msf_unknown_command(self, mock_console):
        from handlers.metasploit import handle_msf_action
        result = handle_msf_action("msf unknown")
        self.assertTrue(result[0])

    @patch("handlers.metasploit.get_msf_client")
    @patch("handlers.metasploit.console")
    def test_msf_search_no_client(self, mock_console, mock_client):
        mock_client.return_value = None
        from handlers.metasploit import handle_msf_search
        result = handle_msf_search("windows")
        self.assertTrue(result[0])

    @patch("handlers.metasploit.get_msf_client")
    @patch("handlers.metasploit.console")
    def test_msf_info_no_client(self, mock_console, mock_client):
        mock_client.return_value = None
        from handlers.metasploit import handle_msf_info
        result = handle_msf_info("exploit/windows/smb/ms08_067_netapi")
        self.assertTrue(result[0])

    @patch("handlers.metasploit.get_msf_client")
    @patch("handlers.metasploit.console")
    def test_msf_sessions_no_client(self, mock_console, mock_client):
        mock_client.return_value = None
        from handlers.metasploit import handle_msf_sessions
        result = handle_msf_sessions()
        self.assertTrue(result[0])


class TestMetasploitClient(unittest.TestCase):
    """Тесты подключения к Metasploit."""

    @patch("handlers.metasploit.HAS_METASPLOIT", False)
    @patch("handlers.metasploit.console")
    def test_client_not_installed(self, mock_console):
        from handlers.metasploit import get_msf_client
        result = get_msf_client()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
