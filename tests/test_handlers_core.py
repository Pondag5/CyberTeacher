"""Тесты для диспетчера команд в handlers/core.py"""

import unittest
from unittest.mock import ANY, MagicMock, patch

from handlers.core import handle_extended_commands


@patch("handlers.core.console.print")  # suppress all console output globally
class TestHandlersCore(unittest.TestCase):
    """Проверка маршрутизации команд в handle_extended_commands"""

    def setUp(self):
        # Общие моки
        self.mock_conn = MagicMock()
        self.mock_llm = MagicMock()

    # --- Simple commands ---
    @patch("handlers.core.show_help")
    def test_command_help(self, mock_show_help, mock_print):
        result = handle_extended_commands("help", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_show_help.assert_called_once()

    @patch("handlers.core.show_menu")
    def test_command_menu(self, mock_show_menu, mock_print):
        result = handle_extended_commands("menu", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_show_menu.assert_called_once()

    def test_command_guide(self, mock_print):
        result = handle_extended_commands("guide", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])

    @patch("handlers.core.handle_version")
    def test_command_version(self, mock_handle_version, mock_print):
        result = handle_extended_commands("version", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_handle_version.assert_called_once()

    def test_command_exit(self, mock_print):
        result = handle_extended_commands("exit", self.mock_llm, self.mock_conn)
        self.assertFalse(result[0])  # возвращает False для выхода

    @patch("handlers.core._ask_confirm", return_value=True)
    @patch("handlers.core.clear_chat_db")
    def test_command_clear_confirmed(self, mock_clear, mock_ask, mock_print):
        result = handle_extended_commands("clear", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_clear.assert_called_once_with(self.mock_conn)

    @patch("handlers.core._ask_confirm", return_value=False)
    @patch("handlers.core.clear_chat_db")
    def test_command_clear_cancelled(self, mock_clear, mock_ask, mock_print):
        result = handle_extended_commands("clear", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_clear.assert_not_called()

    @patch("handlers.core.clear_response_cache")
    def test_command_clearcache(self, mock_clear_cache, mock_print):
        result = handle_extended_commands("clearcache", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_clear_cache.assert_called_once()

    @patch("knowledge.get_knowledge_status", return_value={"files_on_disk": 1})
    def test_command_kb_status(self, mock_status, mock_print):
        result = handle_extended_commands("kb_status", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])

    @patch("knowledge.get_knowledge_status", return_value={"files_in_db": 1})
    def test_command_check_kb(self, mock_status, mock_print):
        result = handle_extended_commands("check_kb", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])

    def test_command_genassignment_stub(self, mock_print):
        result = handle_extended_commands(
            "genassignment", self.mock_llm, self.mock_conn
        )
        self.assertTrue(result[0])

    @patch("handlers.core.show_cache_stats")
    def test_command_cache_stats(self, mock_show, mock_print):
        result = handle_extended_commands("cache stats", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_show.assert_called_once()

    @patch("handlers.core.handle_stats")
    def test_command_stats(self, mock_stats, mock_print):
        result = handle_extended_commands("stats", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_stats.assert_called_once_with(self.mock_conn)

    # --- Mode switches ---
    @patch("handlers.core.get_context")
    def test_mode_teacher(self, mock_get_context, mock_print):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        result = handle_extended_commands("teacher", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_state.set_persona.assert_called_with("teacher")

    @patch("handlers.core.get_context")
    def test_mode_expert(self, mock_get_context, mock_print):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        result = handle_extended_commands("expert", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_state.set_persona.assert_called_with("expert")

    @patch("handlers.core.get_context")
    def test_mode_ctf(self, mock_get_context, mock_print):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        result = handle_extended_commands("ctf", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_state.set_persona.assert_called_with("ctf")

    @patch("handlers.core.get_context")
    def test_mode_review(self, mock_get_context, mock_print):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        result = handle_extended_commands("review", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_state.set_persona.assert_called_with("review")

    # --- News & threats ---
    @patch("handlers.core.handle_security_news")
    def test_news_commands(self, mock_news, mock_print):
        for action in ("news", "cve", "security_news"):
            result = handle_extended_commands(action, self.mock_llm, self.mock_conn)
            self.assertTrue(result[0])
            mock_news.assert_called_with(action, ANY)

    @patch("handlers.core.handle_threats")
    def test_command_threats(self, mock_threats, mock_print):
        result = handle_extended_commands("threats", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_threats.assert_called_once_with("threats")

    @patch("handlers.core.handle_threat_summary")
    def test_command_threat_summary(self, mock_summary, mock_print):
        result = handle_extended_commands(
            "threat summary", self.mock_llm, self.mock_conn
        )
        self.assertTrue(result[0])
        mock_summary.assert_called_once_with("threat summary")

    # --- Groups ---
    @patch("handlers.core.handle_groups")
    def test_command_groups(self, mock_groups, mock_print):
        result = handle_extended_commands("groups", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_groups.assert_called_once()

    # --- Practice & labs ---
    @patch("handlers.core.handle_practice")
    def test_command_practice(self, mock_practice, mock_print):
        result = handle_extended_commands("practice", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_practice.assert_called_once_with("practice")

    @patch("handlers.core.handle_practice")
    def test_command_lab_start(self, mock_practice, mock_print):
        result = handle_extended_commands(
            "lab start nginx", self.mock_llm, self.mock_conn
        )
        self.assertTrue(result[0])
        mock_practice.assert_called_once_with("lab start nginx")

    @patch("handlers.core.handle_htb")
    def test_command_htb(self, mock_htb, mock_print):
        result = handle_extended_commands("htb", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_htb.assert_called_once_with("htb")

    # --- Courses & story ---
    @patch("handlers.core.handle_course")
    def test_command_next(self, mock_course, mock_print):
        result = handle_extended_commands("next", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_course.assert_called_once_with("next")

    @patch("handlers.core.handle_course")
    def test_command_course(self, mock_course, mock_print):
        result = handle_extended_commands("courses", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_course.assert_called_once_with("courses")

    @patch("handlers.core.handle_story_mode")
    def test_command_story_episode_quest(self, mock_story, mock_print):
        for action in ("story", "episode", "quest"):
            result = handle_extended_commands(action, self.mock_llm, self.mock_conn)
            self.assertTrue(result[0])
            mock_story.assert_called_with(action)

    # --- Quiz & tasks ---
    @patch("handlers.core.handle_quiz_action")
    def test_command_quiz(self, mock_quiz, mock_print):
        result = handle_extended_commands("quiz", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_quiz.assert_called_once()

    @patch("handlers.core.handle_task_action")
    def test_command_task(self, mock_task, mock_print):
        result = handle_extended_commands("task", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_task.assert_called_once()

    # --- Flag & achievements ---
    @patch("handlers.core.handle_flag_check")
    def test_command_flag_with_value(self, mock_flag, mock_print):
        result = handle_extended_commands(
            "flag CTF{test}", self.mock_llm, self.mock_conn
        )
        self.assertTrue(result[0])
        mock_flag.assert_called_once_with("CTF{test}")

    @patch("handlers.core.handle_flag_check")
    def test_command_flag_no_value(self, mock_flag, mock_print):
        result = handle_extended_commands("flag", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_flag.assert_called_once_with(None)

    @patch("handlers.core.handle_achievements")
    def test_command_achievements(self, mock_ach, mock_print):
        result = handle_extended_commands("achievements", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_ach.assert_called_once()

    # --- Miscellaneous ---
    @patch("handlers.core.handle_writeup")
    def test_command_writeup(self, mock_writeup, mock_print):
        result = handle_extended_commands("writeup", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_writeup.assert_called_once()

    @patch("handlers.core.handle_add_book")
    def test_command_add_book(self, mock_add, mock_print):
        result = handle_extended_commands(
            "add_book test.pdf", self.mock_llm, self.mock_conn
        )
        self.assertTrue(result[0])
        mock_add.assert_called_once_with("add_book test.pdf")

    @patch("handlers.core.handle_terminal_log")
    def test_command_terminal_short(self, mock_term, mock_print):
        result = handle_extended_commands("terminal", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_term.assert_called_once_with()  # called with no args (default None)

    @patch("handlers.core.handle_terminal_log")
    def test_command_log_prefix(self, mock_term, mock_print):
        result = handle_extended_commands("log ls -la", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_term.assert_called_once_with("ls -la")

    @patch("handlers.core.handle_terminal_log")
    def test_command_term(self, mock_term, mock_print):
        result = handle_extended_commands("term", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_term.assert_called_once_with()

    @patch("handlers.core.handle_history")
    def test_command_history(self, mock_hist, mock_print):
        result = handle_extended_commands("history", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_hist.assert_called_once_with(self.mock_conn)

    @patch("handlers.core.handle_container_check")
    def test_command_check(self, mock_check, mock_print):
        result = handle_extended_commands("check", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_check.assert_called_once_with("check")

    @patch("handlers.core.handle_container_check")
    def test_command_logs(self, mock_check, mock_print):
        result = handle_extended_commands("logs", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_check.assert_called_once_with("logs")

    @patch("handlers.core.handle_provider")
    def test_command_provider_with_arg(self, mock_provider, mock_print):
        result = handle_extended_commands(
            "provider ollama", self.mock_llm, self.mock_conn
        )
        self.assertTrue(result[0])
        mock_provider.assert_called_once_with("provider ollama")

    @patch("handlers.core.handle_provider")
    def test_command_provider_no_arg(self, mock_provider, mock_print):
        result = handle_extended_commands("provider", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_provider.assert_called_once_with("provider")

    @patch("handlers.core.handle_model")
    def test_command_model_with_arg(self, mock_model, mock_print):
        result = handle_extended_commands("model llama2", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_model.assert_called_once_with("model llama2")

    @patch("handlers.core.handle_model")
    def test_command_model_no_arg(self, mock_model, mock_print):
        result = handle_extended_commands("model", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_model.assert_called_once_with("model")

    @patch("handlers.core.handle_set_api_key")
    def test_command_set_api_key(self, mock_set, mock_print):
        result = handle_extended_commands(
            "set-api-key openrouter key123", self.mock_llm, self.mock_conn
        )
        self.assertTrue(result[0])
        mock_set.assert_called_once_with("set-api-key openrouter key123")

    @patch("handlers.core.handle_quiz_generation")
    def test_command_smart_test(self, mock_gen, mock_print):
        result = handle_extended_commands("smart_test", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_gen.assert_called_once_with("smart_test", None)

    @patch("handlers.core.handle_quiz_generation")
    def test_command_read_url(self, mock_gen, mock_print):
        result = handle_extended_commands("read_url", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_gen.assert_called_once_with("read_url", None)

    # --- Social engineering trainer ---
    @patch("handlers.core.handle_social")
    def test_command_social(self, mock_social, mock_print):
        result = handle_extended_commands("social", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_social.assert_called_once_with("social")

    @patch("handlers.core.handle_social")
    def test_command_social_with_arg(self, mock_social, mock_print):
        result = handle_extended_commands("social start", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_social.assert_called_once_with("social start")

    # --- Sandbox ---
    @patch("handlers.core.handle_sandbox")
    def test_command_sandbox(self, mock_sandbox, mock_print):
        result = handle_extended_commands(
            "sandbox echo hi", self.mock_llm, self.mock_conn
        )
        self.assertTrue(result[0])
        mock_sandbox.assert_called_once_with("sandbox echo hi")

    # --- Risk level ---
    @patch("handlers.core.handle_risk")
    def test_command_risk_short(self, mock_risk, mock_print):
        result = handle_extended_commands("risk", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_risk.assert_called_once_with("risk")

    @patch("handlers.core.handle_risk")
    def test_command_risk_with_arg(self, mock_risk, mock_print):
        result = handle_extended_commands("risk up 5", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_risk.assert_called_once_with("risk up 5")

    # --- Adaptive learning ---
    @patch("handlers.core.handle_adaptive")
    def test_command_adaptive(self, mock_adaptive, mock_print):
        result = handle_extended_commands("adaptive", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_adaptive.assert_called_once_with("adaptive")

    @patch("handlers.core.handle_adaptive")
    def test_command_weaknesses(self, mock_adaptive, mock_print):
        result = handle_extended_commands("weaknesses", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_adaptive.assert_called_once_with("weaknesses")

    # --- Spaced Repetition ---
    @patch("handlers.core.handle_repeat")
    def test_command_repeat(self, mock_repeat, mock_print):
        result = handle_extended_commands("repeat", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_repeat.assert_called_once_with("repeat")

    # --- Summary generation ---
    @patch("handlers.core.handle_summary")
    def test_command_summary(self, mock_summary, mock_print):
        result = handle_extended_commands("summary", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_summary.assert_called_once_with("summary")

    # --- Auto Writeup ---
    @patch("handlers.core.handle_auto_writeup")
    def test_command_auto_writeup(self, mock_auto, mock_print):
        result = handle_extended_commands("auto_writeup", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])
        mock_auto.assert_called_once_with("auto_writeup")

    # --- Unknown command ---
    def test_unknown_command(self, mock_print):
        result = handle_extended_commands("unknown123", self.mock_llm, self.mock_conn)
        self.assertTrue(result[0])  # returns True but prints unknown message
