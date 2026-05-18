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
    @patch("handlers.htb.requests.Session")
    @patch("handlers.htb.get_context")
    def test_successful_login(self, mock_ctx, mock_session_cls, mock_console):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_session.post.return_value = mock_response

        mock_state = MagicMock()
        mock_ctx.return_value.state = mock_state

        from handlers.htb import handle_htb_login
        result = handle_htb_login("htb login user@test.com password123")
        self.assertTrue(result[0])
        self.assertEqual(mock_state.htb_email, "user@test.com")
        self.assertEqual(mock_state.htb_password, "password123")

    @patch("handlers.htb.console")
    def test_login_wrong_args(self, mock_console):
        from handlers.htb import handle_htb_login
        result = handle_htb_login("htb login")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_login_missing_password(self, mock_console):
        from handlers.htb import handle_htb_login
        result = handle_htb_login("htb login user@test.com")
        self.assertTrue(result[0])


class TestHTBMachines(unittest.TestCase):
    """Тесты списка машин."""

    @patch("handlers.htb.console")
    @patch("handlers.htb._get_htb_session")
    @patch("handlers.htb._fetch_htb_machines")
    def test_list_machines(self, mock_fetch, mock_session, mock_console):
        mock_fetch.return_value = [
            {"id": 1, "name": "Machine1", "os": "Linux", "difficulty": "Easy", "points": 20},
            {"id": 2, "name": "Machine2", "os": "Windows", "difficulty": "Medium", "points": 30},
        ]

        from handlers.htb import handle_htb_machines
        result = handle_htb_machines("htb machines")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    @patch("handlers.htb._get_htb_session")
    def test_machines_auth_error(self, mock_session, mock_console):
        from handlers.htb import HTBAuthError, handle_htb_machines
        mock_session.side_effect = HTBAuthError("Not authenticated")
        result = handle_htb_machines("htb machines")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_machines_invalid_type(self, mock_console):
        from handlers.htb import handle_htb_machines
        result = handle_htb_machines("htb machines invalid")
        self.assertTrue(result[0])


class TestHTBMachineDetail(unittest.TestCase):
    """Тесты деталей машины."""

    @patch("handlers.htb.console")
    @patch("handlers.htb._get_htb_session")
    @patch("handlers.htb._fetch_htb_machine_detail")
    def test_machine_detail(self, mock_detail, mock_session, mock_console):
        mock_detail.return_value = {
            "name": "TestMachine",
            "os": "Linux",
            "difficulty": "Easy",
            "points": 20,
            "rating": {"average": 4.5},
            "status": "active",
            "release": "2024-01-01",
            "description": "Test machine",
            "hints": [{"text": "Hint 1"}],
        }

        from handlers.htb import handle_htb_machine
        result = handle_htb_machine("htb machine 1")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_machine_missing_id(self, mock_console):
        from handlers.htb import handle_htb_machine
        result = handle_htb_machine("htb machine")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_machine_invalid_id(self, mock_console):
        from handlers.htb import handle_htb_machine
        result = handle_htb_machine("htb machine abc")
        self.assertTrue(result[0])


class TestHTBSubmit(unittest.TestCase):
    """Тесты отправки флага."""

    @patch("handlers.htb.console")
    @patch("handlers.htb._get_htb_session")
    @patch("handlers.htb.get_context")
    def test_successful_submit(self, mock_ctx, mock_session, mock_console):
        mock_session_obj = MagicMock()
        mock_session.return_value = mock_session_obj
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_session_obj.post.return_value = mock_response

        mock_state = MagicMock()
        mock_state.htb_completed = []
        mock_ctx.return_value.state = mock_state

        from handlers.htb import handle_htb_submit
        result = handle_htb_submit("htb submit 123 FLAG{test}")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_submit_missing_args(self, mock_console):
        from handlers.htb import handle_htb_submit
        result = handle_htb_submit("htb submit")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    def test_submit_invalid_id(self, mock_console):
        from handlers.htb import handle_htb_submit
        result = handle_htb_submit("htb submit abc FLAG{test}")
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

        from handlers.htb import handle_htb_status
        result = handle_htb_status("htb status")
        self.assertTrue(result[0])

    @patch("handlers.htb.console")
    @patch("handlers.htb.get_context")
    def test_status_with_progress(self, mock_ctx, mock_console):
        mock_state = MagicMock()
        mock_state.htb_email = "user@test.com"
        mock_state.htb_completed = [1, 2, 3, 4, 5]
        mock_ctx.return_value.state = mock_state

        from handlers.htb import handle_htb_status
        result = handle_htb_status("htb status")
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

    @patch("handlers.htb.console")
    @patch("handlers.htb.handle_htb_login")
    def test_htb_dispatches_login(self, mock_login, mock_console):
        mock_login.return_value = (True, None, None, True)
        from handlers.htb import handle_htb
        handle_htb("htb login user@test.com pass")
        mock_login.assert_called_once()


if __name__ == "__main__":
    unittest.main()
