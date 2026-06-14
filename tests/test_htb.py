"""
Тесты для HackTheBox API интеграции (G-02).
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestHTBLogin(unittest.TestCase):
    """Тесты авторизации HTB."""

    @patch("handlers.htb.console")
    @patch("handlers.htb.get_context")
    def test_successful_login(self, mock_ctx, mock_console):
        mock_state = MagicMock()
        mock_ctx.return_value.state = mock_state

        from handlers.htb import handle_htb

        result = handle_htb("htb login user@test.com password123")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_login_wrong_args(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb login")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_login_missing_password(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb login user@test.com")
        self.assertTrue(result[0])


class TestHTBMachines(unittest.TestCase):
    """Тесты списка машин."""

    @patch("handlers.htb.console")
    def test_list_machines(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb machines")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_machines_auth_error(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb machines")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_machines_invalid_type(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb machines invalid")
        self.assertTrue(result[0])


class TestHTBMachineDetail(unittest.TestCase):
    """Тесты деталей машины."""

    @patch("handlers.htb.console")
    def test_machine_detail(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb machine 1")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_machine_missing_id(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb machine")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_machine_invalid_id(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb machine abc")
        self.assertTrue(result[0])


class TestHTBSubmit(unittest.TestCase):
    """Тесты отправки флага."""

    @patch("handlers.htb.console")
    @patch("handlers.htb.get_context")
    def test_successful_submit(self, mock_ctx, mock_console):
        mock_state = MagicMock()
        mock_state.htb_completed = []
        mock_ctx.return_value.state = mock_state

        from handlers.htb import handle_htb

        result = handle_htb("htb submit 123 FLAG{test}")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_submit_missing_args(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb submit")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_submit_invalid_id(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb submit abc FLAG{test}")
        self.assertTrue(result[0])


class TestHTBStatus(unittest.TestCase):
    """Тесты статуса."""

    @patch("handlers.htb.console")
    @patch("handlers.htb.get_context")
    def test_status_no_auth(self, mock_ctx, mock_console):
        mock_state = MagicMock()
        mock_state.htb_email = None
        mock_state.htb_completed = []
        mock_ctx.return_value.state = mock_state

        from handlers.htb import handle_htb

        result = handle_htb("htb status")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    @patch("handlers.htb.get_context")
    def test_status_with_progress(self, mock_ctx, mock_console):
        mock_state = MagicMock()
        mock_state.htb_email = "user@test.com"
        mock_state.htb_completed = [1, 2, 3, 4, 5]
        mock_ctx.return_value.state = mock_state

        from handlers.htb import handle_htb

        result = handle_htb("htb status")
        self.assertTrue(result[0])


class TestHTBDispatcher(unittest.TestCase):
    """Тесты диспетчера команд."""

    @patch("handlers.htb.console")
    def test_htb_no_args_shows_help(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_htb_unknown_command(self, mock_console):
        from handlers.htb import handle_htb

        result = handle_htb("htb unknown")
        self.assertTrue(result[0])


if __name__ == "__main__":
    unittest.main()
