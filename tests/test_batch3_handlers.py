"""
Tests for emotions, subscribe, telegram_bot, vision, and kb_manager handlers.
"""

import json
import os
import tempfile
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
        self.assertNotEqual(modifier, "")


# ── Subscribe Handler ─────────────────────────────────────────
class TestSubscribeHandler(unittest.TestCase):
    """Tests for /subscribe command."""

    @patch("handlers.subscribe.console")
    def test_subscribe_help(self, mock_console):
        from handlers.subscribe import handle_subscribe
        response, should_continue = handle_subscribe("/subscribe help")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.subscribe.console")
    def test_subscribe_add_valid(self, mock_console):
        from handlers.subscribe import SUBSCRIPTIONS_FILE, handle_subscribe
        if os.path.exists(SUBSCRIPTIONS_FILE):
            os.remove(SUBSCRIPTIONS_FILE)

        response, should_continue = handle_subscribe("/subscribe add apt")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

        if os.path.exists(SUBSCRIPTIONS_FILE):
            os.remove(SUBSCRIPTIONS_FILE)

    @patch("handlers.subscribe.console")
    def test_subscribe_add_invalid(self, mock_console):
        from handlers.subscribe import handle_subscribe
        response, should_continue = handle_subscribe("/subscribe add invalid_type")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.subscribe.console")
    def test_subscribe_list_empty(self, mock_console):
        from handlers.subscribe import (
            SUBSCRIPTIONS_FILE,
            _load_subscriptions,
            handle_subscribe,
        )
        if os.path.exists(SUBSCRIPTIONS_FILE):
            os.remove(SUBSCRIPTIONS_FILE)

        response, should_continue = handle_subscribe("/subscribe list")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

        if os.path.exists(SUBSCRIPTIONS_FILE):
            os.remove(SUBSCRIPTIONS_FILE)

    @patch("handlers.subscribe.console")
    def test_subscribe_notify_empty(self, mock_console):
        from handlers.subscribe import SUBSCRIPTIONS_FILE, handle_subscribe
        if os.path.exists(SUBSCRIPTIONS_FILE):
            os.remove(SUBSCRIPTIONS_FILE)

        response, should_continue = handle_subscribe("/subscribe notify")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

        if os.path.exists(SUBSCRIPTIONS_FILE):
            os.remove(SUBSCRIPTIONS_FILE)

    @patch("handlers.subscribe.console")
    def test_subscribe_unknown_subcommand(self, mock_console):
        from handlers.subscribe import handle_subscribe
        response, should_continue = handle_subscribe("/subscribe unknown")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()


# ── Telegram Bot Handler ──────────────────────────────────────
class TestTelegramBotHandler(unittest.TestCase):
    """Tests for /telegram command."""

    @patch("handlers.telegram_bot.console")
    def test_telegram_status(self, mock_console):
        from handlers.telegram_bot import handle_telegram
        response, should_continue = handle_telegram("/telegram status")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.telegram_bot.console")
    def test_telegram_help(self, mock_console):
        from handlers.telegram_bot import handle_telegram
        response, should_continue = handle_telegram("/telegram help")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.telegram_bot.console")
    def test_telegram_start_no_token(self, mock_console):
        from handlers.telegram_bot import handle_telegram
        with patch("handlers.telegram_bot.TELEGRAM_AVAILABLE", True):
            with patch.dict(os.environ, {}, clear=True):
                response, should_continue = handle_telegram("/telegram start")

                self.assertTrue(should_continue)
                mock_console.print.assert_called()

    @patch("handlers.telegram_bot.console")
    def test_telegram_stop_not_running(self, mock_console):
        from handlers.telegram_bot import handle_telegram
        response, should_continue = handle_telegram("/telegram stop")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.telegram_bot.console")
    def test_telegram_unknown_subcommand(self, mock_console):
        from handlers.telegram_bot import handle_telegram
        response, should_continue = handle_telegram("/telegram unknown")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()


# ── Vision Handler ────────────────────────────────────────────
class TestVisionHandler(unittest.TestCase):
    """Tests for /vision command."""

    @patch("handlers.vision.console")
    def test_vision_help(self, mock_console):
        from handlers.vision import handle_vision
        response, should_continue = handle_vision("/vision help")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.vision.console")
    def test_vision_analyze_file_not_found(self, mock_console):
        from handlers.vision import handle_vision
        response, should_continue = handle_vision("/vision analyze nonexistent.png")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.vision.console")
    def test_vision_ocr_file_not_found(self, mock_console):
        from handlers.vision import handle_vision
        response, should_continue = handle_vision("/vision ocr nonexistent.png")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.vision.console")
    def test_vision_unknown_subcommand(self, mock_console):
        from handlers.vision import handle_vision
        response, should_continue = handle_vision("/vision unknown")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    def test_vision_analysis_dict_not_empty(self):
        from handlers.vision import VISION_ANALYSIS
        self.assertGreater(len(VISION_ANALYSIS), 2)


# ── KB Manager Handler ────────────────────────────────────────
class TestKBManagerHandler(unittest.TestCase):
    """Tests for /kb command."""

    @patch("handlers.kb_manager.console")
    def test_kb_status(self, mock_console):
        from handlers.kb_manager import handle_kb
        response, should_continue = handle_kb("/kb status")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.kb_manager.console")
    def test_kb_help(self, mock_console):
        from handlers.kb_manager import handle_kb
        response, should_continue = handle_kb("/kb help")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.kb_manager.console")
    def test_kb_unknown_subcommand(self, mock_console):
        from handlers.kb_manager import handle_kb
        response, should_continue = handle_kb("/kb unknown")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    def test_get_kb_status_empty(self):
        from handlers.kb_manager import _get_kb_status
        with patch("handlers.kb_manager.KNOWLEDGE_DIR", "/nonexistent/path"):
            status = _get_kb_status()
            self.assertEqual(status["status"], "empty")


if __name__ == "__main__":
    unittest.main()
