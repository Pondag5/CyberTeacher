"""
Tests for CTF flags handler.
"""

import unittest
from unittest.mock import patch, MagicMock

from handlers.ctf_flags import (
    FLAG_PREFIX,
    FLAG_TTL,
    generate_flag,
    verify_flag,
    handle_ctf_flags,
    _list_challenges,
)


class TestCTFFlags(unittest.TestCase):
    """Tests for CTF flag generation and verification."""

    def test_generate_flag_format(self):
        flag = generate_flag("test_challenge", "user1")
        self.assertTrue(flag.startswith(f"{FLAG_PREFIX}{{test_challenge_"))
        self.assertTrue(flag.endswith("}"))

    def test_generate_flag_unique_per_user(self):
        flag1 = generate_flag("test_challenge", "user1")
        flag2 = generate_flag("test_challenge", "user2")
        self.assertNotEqual(flag1, flag2)

    def test_generate_flag_same_user_same_slot(self):
        flag1 = generate_flag("test_challenge", "user1")
        flag2 = generate_flag("test_challenge", "user1")
        self.assertEqual(flag1, flag2)

    def test_verify_flag_valid(self):
        flag = generate_flag("test_challenge", "user1")
        self.assertTrue(verify_flag(flag, "test_challenge", "user1"))

    def test_verify_flag_invalid_prefix(self):
        self.assertFalse(verify_flag("INVALID{test_abc123}", "test_challenge", "user1"))

    def test_verify_flag_wrong_user(self):
        flag = generate_flag("test_challenge", "user1")
        self.assertFalse(verify_flag(flag, "test_challenge", "user2"))

    def test_verify_flag_wrong_challenge(self):
        flag = generate_flag("test_challenge", "user1")
        self.assertFalse(verify_flag(flag, "wrong_challenge", "user1"))

    @patch("handlers.ctf_flags.get_context")
    @patch("handlers.ctf_flags.console")
    def test_handle_ctf_flags_list(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_ctf_flags("/ctf")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.ctf_flags.get_context")
    @patch("handlers.ctf_flags.console")
    def test_handle_ctf_flags_generate(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.username = "testuser"
        mock_state.ctf_flags_generated = 0
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_ctf_flags("/ctf generate web_basic")

        self.assertTrue(success)
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.ctf_flags.get_context")
    @patch("handlers.ctf_flags.console")
    def test_handle_ctf_flags_submit_invalid_format(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_ctf_flags("/ctf submit invalid_flag")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.ctf_flags.get_context")
    @patch("handlers.ctf_flags.console")
    def test_handle_ctf_flags_verify(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        flag = generate_flag("test_challenge", "default")
        success, _, _, continue_loop = handle_ctf_flags(f"/ctf verify {flag} test_challenge")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.ctf_flags.console")
    def test_list_challenges(self, mock_console):
        success, _, _, continue_loop = _list_challenges()

        self.assertTrue(success)
        mock_console.print.assert_called()


if __name__ == "__main__":
    unittest.main()
