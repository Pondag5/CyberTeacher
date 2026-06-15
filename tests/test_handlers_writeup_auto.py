"""Unit tests for handlers/writeup_auto.py"""

import time
import unittest
from unittest.mock import MagicMock, mock_open, patch


class MockState:
    def __init__(self):
        self.last_writeup_activity = None
        self.writeup_history = []
        self.save_called = False

    def save_to_file(self):
        self.save_called = True


class TestHandlersWriteupAuto(unittest.TestCase):
    """Tests for handlers/writeup_auto module"""

    @patch("handlers.writeup_auto.get_context")
    @patch("handlers.writeup_auto.console.print")
    def test_handle_auto_writeup_no_activity(self, mock_print, mock_get_context):
        """Test when there is no last_writeup_activity"""
        from handlers import writeup_auto

        mock_state = MockState()
        mock_state.last_writeup_activity = None
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = writeup_auto.handle_auto_writeup("")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[yellow]Нет данных для генерации writeup. Сначала пройдите квиз или задание.[/yellow]"
        )

    @patch("handlers.writeup_auto.get_context")
    @patch("handlers.writeup_auto.console.print")
    def test_handle_auto_writeup_activity_without_topic(
        self, mock_print, mock_get_context
    ):
        """Test activity missing topic/category"""
        from handlers import writeup_auto

        mock_state = MockState()
        mock_state.last_writeup_activity = {"type": "quiz"}  # no topic
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = writeup_auto.handle_auto_writeup("")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[red]Не указана тема в активности[/red]")

    @patch("handlers.writeup_auto.get_context")
    @patch("handlers.writeup_auto.console.print")
    @patch("handlers.writeup_auto.get_current_vectordb")
    @patch("handlers.writeup_auto.get_relevant_docs")
    @patch("handlers.writeup_auto.LazyLoader")
    @patch("builtins.input", return_value="n")
    def test_handle_auto_writeup_quiz_success(
        self,
        mock_input,
        mock_lazy,
        mock_get_docs,
        mock_vectordb,
        mock_print,
        mock_get_context,
    ):
        """Test writeup generation for quiz activity with LLM"""
        from handlers import writeup_auto

        mock_state = MockState()
        activity = {
            "type": "quiz",
            "topic": "xss",
            "total_score": 8,
            "max_total": 10,
            "success_rate": 80.0,
            "responses": [
                {
                    "question": "Q1?",
                    "user_answer": "A",
                    "correct_answer": "A",
                    "score": 10,
                    "feedback": "OK",
                }
            ],
        }
        mock_state.last_writeup_activity = activity
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        # Mock vectordb and docs
        mock_vectordb.return_value = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "Relevant content about XSS"
        mock_get_docs.return_value = [mock_doc]

        # Mock LLM
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = "# Writeup\n\nGenerated content."
        mock_lazy.get_llm.return_value = mock_llm

        result = writeup_auto.handle_auto_writeup("")

        self.assertEqual(result, (True, None, None, True))
        mock_lazy.get_llm.assert_called_once()
        mock_llm.invoke.assert_called_once()
        self.assertEqual(len(mock_state.writeup_history), 1)
        self.assertEqual(mock_state.writeup_history[0]["topic"], "xss")

    @patch("handlers.writeup_auto.get_context")
    @patch("handlers.writeup_auto.console.print")
    @patch("handlers.writeup_auto.get_current_vectordb")
    @patch("handlers.writeup_auto.get_relevant_docs")
    @patch("handlers.writeup_auto.LazyLoader")
    @patch("builtins.input", return_value="y")
    @patch("builtins.open", new_callable=mock_open)
    def test_handle_auto_writeup_saves_to_file(
        self,
        mock_file_open,
        mock_input,
        mock_lazy,
        mock_get_docs,
        mock_vectordb,
        mock_print,
        mock_get_context,
    ):
        """Test writeup is saved to file when user confirms"""
        from handlers import writeup_auto

        mock_state = MockState()
        activity = {
            "type": "task",
            "category": "crypto",
            "question": "Decrypt this",
            "user_answer": "flag",
            "correct_answer": "flag",
            "score": 10,
            "feedback": "Good",
        }
        mock_state.last_writeup_activity = activity
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_vectordb.return_value = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "Crypto context"
        mock_get_docs.return_value = [mock_doc]

        mock_llm = MagicMock()
        mock_llm.invoke.return_value = "# Writeup content"
        mock_lazy.get_llm.return_value = mock_llm

        result = writeup_auto.handle_auto_writeup("")

        self.assertEqual(result, (True, None, None, True))
        # Should have called open for writing
        mock_file_open.assert_called_once()
        # Verify state saved
        self.assertTrue(mock_state.save_called)

    @patch("handlers.writeup_auto.get_context")
    @patch("handlers.writeup_auto.console.print")
    @patch("handlers.writeup_auto.get_current_vectordb")
    @patch("handlers.writeup_auto.get_relevant_docs")
    @patch("handlers.writeup_auto.LazyLoader")
    def test_handle_auto_writeup_llm_exception(
        self, mock_lazy, mock_get_docs, mock_vectordb, mock_print, mock_get_context
    ):
        """Test writeup generation when LLM raises exception"""
        from handlers import writeup_auto

        mock_state = MockState()
        activity = {
            "type": "quiz",
            "topic": "test",
            "total_score": 5,
            "max_total": 10,
            "success_rate": 50.0,
            "responses": [],
        }
        mock_state.last_writeup_activity = activity
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_vectordb.return_value = MagicMock()
        mock_get_docs.return_value = []
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("LLM error")
        mock_lazy.get_llm.return_value = mock_llm

        result = writeup_auto.handle_auto_writeup("")

        self.assertEqual(result, (True, None, None, True))
        # Should print error message
        self.assertTrue(
            any("Ошибка" in str(call) for call in mock_print.call_args_list)
        )

    @patch("handlers.writeup_auto.get_context")
    @patch("handlers.writeup_auto.console.print")
    @patch("handlers.writeup_auto.get_current_vectordb")
    @patch("handlers.writeup_auto.LazyLoader")
    @patch("builtins.input", return_value="n")
    def test_handle_auto_writeup_no_vectordb(
        self, mock_input, mock_lazy, mock_vectordb, mock_print, mock_get_context
    ):
        """Test writeup when vectordb is None (context unavailable)"""
        from handlers import writeup_auto

        mock_state = MockState()
        activity = {
            "type": "task",
            "category": "web",
            "question": "What is XSS?",
            "user_answer": "Cross-site scripting",
            "correct_answer": "Cross-site scripting",
            "score": 10,
            "feedback": "Good",
        }
        mock_state.last_writeup_activity = activity
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        mock_vectordb.return_value = None
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = "Writeup without context"
        mock_lazy.get_llm.return_value = mock_llm

        result = writeup_auto.handle_auto_writeup("")

        self.assertEqual(result, (True, None, None, True))
        # LLM still invoked with context note
        mock_llm.invoke.assert_called_once()
        # Check that context mentions unavailable
        prompt = mock_llm.invoke.call_args[0][0]
        self.assertIn("База знаний недоступна", prompt)


if __name__ == "__main__":
    unittest.main()
