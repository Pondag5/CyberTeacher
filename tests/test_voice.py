"""Tests for Voice Assistant (M-34)"""

import unittest
from unittest.mock import MagicMock, patch

from handlers.voice import _speak, handle_voice
from state import AppState


class TestVoice(unittest.TestCase):
    """Test voice handler"""

    @patch("handlers.voice.get_context")
    def test_voice_on(self, mock_get_context):
        """Enabling voice output"""
        mock_state = MagicMock(spec=AppState)
        mock_state.voice_enabled = False
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, msg, _ = handle_voice("voice on")
        self.assertTrue(success)
        self.assertTrue(mock_state.voice_enabled)
        self.assertIn("enabled", msg.lower())

    @patch("handlers.voice.get_context")
    def test_voice_off(self, mock_get_context):
        """Disabling voice output"""
        mock_state = MagicMock(spec=AppState)
        mock_state.voice_enabled = True
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, msg, _ = handle_voice("voice off")
        self.assertTrue(success)
        self.assertFalse(mock_state.voice_enabled)
        self.assertIn("disabled", msg.lower())

    @patch("handlers.voice.get_context")
    def test_voice_status(self, mock_get_context):
        """Status shows current settings"""
        mock_state = MagicMock(spec=AppState)
        mock_state.voice_enabled = True
        mock_state.voice_engine = "pyttsx3"
        mock_state.voice_rate = 200
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, msg, _ = handle_voice("voice status")
        self.assertTrue(success)
        self.assertIn("enabled", msg.lower())
        self.assertIn("pyttsx3", msg)
        self.assertIn("200", msg)

    @patch("handlers.voice._speak")
    @patch("handlers.voice.get_context")
    def test_voice_test(self, mock_get_context, mock_speak):
        """Voice test speaks a message"""
        mock_state = MagicMock(spec=AppState)
        mock_state.voice_enabled = True
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_speak.return_value = True

        success, msg, _ = handle_voice("voice test")
        self.assertTrue(success)
        self.assertIn("test", msg.lower())
        mock_speak.assert_called_once()

    @patch("handlers.voice._speak")
    @patch("handlers.voice.get_context")
    def test_voice_test_fails_when_tts_unavailable(self, mock_get_context, mock_speak):
        """Voice test returns error if TTS fails"""
        mock_state = MagicMock(spec=AppState)
        mock_state.voice_enabled = True
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_speak.return_value = False

        success, msg, _ = handle_voice("voice test")
        self.assertFalse(success)
        self.assertIn("❌", msg)

    @patch("handlers.voice.get_context")
    def test_handle_voice_invalid(self, mock_get_context):
        """Invalid voice command shows usage"""
        mock_state = MagicMock(spec=AppState)
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, msg, _ = handle_voice("voice invalid")
        self.assertFalse(success)
        self.assertIn("Usage", msg)


if __name__ == "__main__":
    unittest.main()
