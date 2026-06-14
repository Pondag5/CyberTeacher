"""
Tests for emotions handler.
"""

import unittest
from unittest.mock import MagicMock, patch


# ── Emotions Handler ──────────────────────────────────────────
class TestEmotionsHandler(unittest.TestCase):
    """Tests for /emotions command and sentiment analysis."""

    def test_analyze_sentiment_positive(self):
        from handlers.emotions import analyze_sentiment

        result = analyze_sentiment("спасибо, понял, отлично!")
        self.assertEqual(result, "excited")

    def test_analyze_sentiment_happy(self):
        from handlers.emotions import analyze_sentiment

        result = analyze_sentiment("спасибо")
        self.assertEqual(result, "happy")

    def test_analyze_sentiment_negative(self):
        from handlers.emotions import analyze_sentiment

        result = analyze_sentiment("не понимаю, сложно")
        self.assertEqual(result, "confused")

    def test_analyze_sentiment_frustrated(self):
        from handlers.emotions import analyze_sentiment

        result = analyze_sentiment("бесишь, тупой")
        self.assertEqual(result, "frustrated")

    def test_analyze_sentiment_neutral(self):
        from handlers.emotions import analyze_sentiment

        result = analyze_sentiment("расскажи про sql injection")
        self.assertEqual(result, "neutral")

    @patch("handlers.emotions.get_context")
    @patch("handlers.emotions.console")
    def test_emotions_no_args(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.emotion_mode = "neutral"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers.emotions import handle_emotions

        success, _, _, continue_loop = handle_emotions("/emotions")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.emotions.get_context")
    @patch("handlers.emotions.console")
    def test_emotions_auto(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers.emotions import handle_emotions

        success, _, _, continue_loop = handle_emotions("/emotions auto")

        self.assertTrue(success)
        self.assertEqual(mock_state.emotion_mode, "auto")

    @patch("handlers.emotions.get_context")
    @patch("handlers.emotions.console")
    def test_emotions_set_happy(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers.emotions import handle_emotions

        success, _, _, continue_loop = handle_emotions("/emotions set happy")

        self.assertTrue(success)
        self.assertEqual(mock_state.emotion_mode, "happy")

    @patch("handlers.emotions.get_context")
    @patch("handlers.emotions.console")
    def test_emotions_set_invalid(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers.emotions import handle_emotions

        success, _, _, continue_loop = handle_emotions("/emotions set invalid_state")

        self.assertTrue(success)
        mock_ctx.save_state.assert_not_called()

    @patch("handlers.emotions.get_context")
    @patch("handlers.emotions.console")
    def test_emotions_show(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.emotion_mode = "neutral"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers.emotions import handle_emotions

        success, _, _, continue_loop = handle_emotions("/emotions show")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.emotions.get_context")
    def test_get_emotion_status(self, mock_get_context):
        mock_state = MagicMock()
        mock_state.emotion_mode = "happy"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers.emotions import get_emotion_status

        status = get_emotion_status()
        self.assertEqual(status["name"], "Радостный")

    @patch("handlers.emotions.get_context")
    def test_get_emotion_prompt_modifier_auto(self, mock_get_context):
        mock_state = MagicMock()
        mock_state.emotion_mode = "auto"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers.emotions import get_emotion_prompt_modifier

        modifier = get_emotion_prompt_modifier("спасибо, понял")


if __name__ == "__main__":
    unittest.main()
