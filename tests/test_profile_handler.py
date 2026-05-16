"""
Tests for profile handler.
"""

import unittest
from unittest.mock import patch, MagicMock

from di import AppContext
from handlers.profile import (
    AVATARS,
    _set_name,
    _set_avatar,
    _list_avatars,
    _show_detailed_stats,
)


class TestProfileHandler(unittest.TestCase):
    """Tests for profile handler functions."""

    @patch("handlers.profile.get_context")
    @patch("handlers.profile.console")
    def test_set_name_valid(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.username = "OldName"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _set_name("NewName")
        self.assertTrue(result[0])
        self.assertEqual(mock_state.username, "NewName")
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.profile.get_context")
    @patch("handlers.profile.console")
    def test_set_name_empty(self, mock_console, mock_get_context):
        mock_ctx = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = _set_name("   ")
        self.assertTrue(result[0])
        mock_console.print.assert_called()

    @patch("handlers.profile.get_context")
    @patch("handlers.profile.console")
    def test_set_name_too_long(self, mock_console, mock_get_context):
        mock_ctx = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = _set_name("A" * 31)
        self.assertTrue(result[0])
        mock_console.print.assert_called()

    @patch("handlers.profile.get_context")
    @patch("handlers.profile.console")
    def test_set_avatar_valid(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _set_avatar("🐱")
        self.assertTrue(result[0])
        self.assertEqual(mock_state.avatar, "🐱")
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.profile.get_context")
    @patch("handlers.profile.console")
    def test_set_avatar_custom(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _set_avatar("🦄")
        self.assertTrue(result[0])
        self.assertEqual(mock_state.avatar, "🦄")

    @patch("handlers.profile.get_context")
    @patch("handlers.profile.console")
    def test_list_avatars(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.avatar = "🧑‍💻"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _list_avatars()
        self.assertTrue(result[0])
        mock_console.print.assert_called()

    @patch("handlers.profile.get_context")
    @patch("handlers.profile.console")
    def test_show_detailed_stats(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.avatar = "🐱"
        mock_state.username = "TestUser"
        mock_state.get_handle.return_value = "Новичок"
        mock_state.reputation = 0
        mock_state.points = 100.0
        mock_state.get_xp_multiplier.return_value = 1.0
        mock_state.quizzes_taken = 5
        mock_state.assignments_completed = 2
        mock_state.total_flags_collected = 10
        mock_state.labs_started = 3
        mock_state.messages_sent = 50
        mock_state.news_checked = 1
        mock_state.get_all_skills.return_value = []
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _show_detailed_stats()
        self.assertTrue(result[0])
        mock_console.print.assert_called()

    def test_avatars_not_empty(self):
        self.assertGreater(len(AVATARS), 10)


if __name__ == "__main__":
    unittest.main()
