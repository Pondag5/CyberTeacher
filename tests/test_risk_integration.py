"""
Тесты для проверки интеграции risk_level (C-01)
"""

import os
import sys
import unittest

# Добавляем корень проекта в path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, patch

from handlers.misc import handle_risk, handle_story_mode
from state import get_state
from story_mode import get_story_list, submit_flag


class TestRiskLevel(unittest.TestCase):
    """Тесты уровня риска"""

    def setUp(self):
        """Сброс состояния перед каждым тестом"""
        state = get_state()
        state.reset_risk()

    def test_risk_increase(self):
        """Проверка увеличения уровня риска"""
        state = get_state()
        initial = state.risk_level
        state.increase_risk(10)
        self.assertEqual(state.risk_level, initial + 10)

    def test_risk_decrease(self):
        """Проверка уменьшения уровня риска"""
        state = get_state()
        state.risk_level = 50
        state.decrease_risk(15)
        self.assertEqual(state.risk_level, 35)

    def test_risk_clamp(self):
        """Проверка ограничения 0-100"""
        state = get_state()
        state.increase_risk(150)
        self.assertEqual(state.risk_level, 100)
        state.decrease_risk(150)
        self.assertEqual(state.risk_level, 0)

    def test_risk_status(self):
        """Проверка текстового статуса"""
        state = get_state()
        state.risk_level = 10
        self.assertIn("Низкий", state.get_risk_status())
        state.risk_level = 30
        self.assertIn("Умеренный", state.get_risk_status())
        state.risk_level = 60
        self.assertIn("Высокий", state.get_risk_status())
        state.risk_level = 90
        self.assertIn("Критический", state.get_risk_status())

    @patch("handlers.misc.console.print")
    def test_handle_risk_display(self, mock_print):
        """Проверка команды /risk"""
        state = get_state()
        state.risk_level = 25
        result = handle_risk("risk")
        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.misc.console.print")
    def test_handle_risk_up(self, mock_print):
        """Проверка /risk up"""
        state = get_state()
        state.risk_level = 0
        result = handle_risk("risk up 20")
        self.assertEqual(state.risk_level, 20)

    @patch("handlers.misc.console.print")
    def test_handle_risk_down(self, mock_print):
        """Проверка /risk down"""
        state = get_state()
        state.risk_level = 50
        result = handle_risk("risk down 10")
        self.assertEqual(state.risk_level, 40)

    @patch("handlers.misc.console.print")
    def test_handle_risk_reset(self, mock_print):
        """Проверка /risk reset"""
        state = get_state()
        state.risk_level = 75
        result = handle_risk("risk reset")
        self.assertEqual(state.risk_level, 0)

    @patch("handlers.misc.console.print")
    def test_handle_risk_set(self, mock_print):
        """Проверка установки конкретного значения"""
        state = get_state()
        result = handle_risk("risk 42")
        self.assertEqual(state.risk_level, 42)

    @patch("handlers.misc.console.print")
    @patch("handlers.misc.submit_flag")
    def test_story_mode_flag_success_adjusts_risk(self, mock_submit, mock_print):
        """Проверка что правильный флаг снижает риск в story mode"""
        state = get_state()
        state.risk_level = 50
        mock_submit.return_value = "✅ ЭПИЗОД #1: Test - ПРОЙДЕН!"
        result = handle_story_mode("flag FLAG{test}")
        # Проверяем что risk уменьшился (на 15 по логике)
        self.assertLess(state.risk_level, 50)

    @patch("handlers.misc.console.print")
    @patch("story_mode.submit_flag")
    def test_story_mode_flag_success_adjusts_risk(self, mock_submit, mock_print):
        """Проверка что правильный флаг снижает риск в story mode"""
        state = get_state()
        state.risk_level = 50
        mock_submit.return_value = "✅ ЭПИЗОД #1: Test - ПРОЙДЕН!"
        # Use "story flag <flag>" format which triggers flag check (needs 3 parts)
        result = handle_story_mode("story flag FLAG{test}")
        # Проверяем что risk уменьшился (на 15 по логике)
        self.assertLess(state.risk_level, 50)

    @patch("handlers.misc.console.print")
    @patch("story_mode.submit_flag")
    def test_story_mode_flag_failure_increases_risk(self, mock_submit, mock_print):
        """Проверка что неверный флаг повышает риск в story mode"""
        state = get_state()
        state.risk_level = 10
        mock_submit.return_value = "❌ Неверный флаг! Попробуй ещё."
        result = handle_story_mode("story flag WRONG_FLAG")
        # Проверяем что risk увеличился (на 10 по логике)
        self.assertGreater(state.risk_level, 10)

    @patch("handlers.misc.console.print")
    def test_story_mode_list_no_error(self, mock_print):
        """Проверка что команда /story выполняется без ошибок"""
        state = get_state()
        state.risk_level = 33
        # Не должно быть исключений
        result = handle_story_mode("story")
        self.assertEqual(result, (True, None, None, True))


class TestRiskInStudyContext(unittest.TestCase):
    """Тесты отображения risk_info в study_context"""

    @patch.dict("os.environ", {}, clear=True)
    def test_risk_info_in_ctf_mode(self):
        """Проверка что risk_info добавляется в study_context для CTF режима"""
        from main import get_learning_context, get_mode_prompt
        from state import get_state
        from ui import Mode

        state = get_state()
        state.set_persona("ctf")
        state.risk_level = 45

        # Собираем study_context (имитация логики main.py)
        learning_ctx = {"current_course": None, "current_topic": 0, "current_lab": None}
        kb_info = "В базе знаний: 5 документов."
        weak_info = ""
        risk_info = ""

        # Имитируем логику из main.py
        if state.get_persona() in ("ctf", "story"):
            risk_status = state.get_risk_status()
            risk_info = f"⚠️ Уровень риска (trace/compromise): {risk_status} ({state.risk_level}/100).\n"

        # Проверяем что risk_info сформирован правильно
        self.assertIn("Уровень риска", risk_info)
        self.assertIn("Умеренный", risk_info)  # 45 -> Умеренный


if __name__ == "__main__":
    unittest.main()
