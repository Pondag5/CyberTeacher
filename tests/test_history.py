"""Тесты для модуля Historical Mode (M-05)."""

import unittest
from unittest.mock import patch

from handlers.history import (
    handle_timeline,
    _display_era_details,
    _run_history_quiz,
    ERAS,
    QUIZ_QUESTIONS,
)


class TestTimelineDisplay(unittest.TestCase):
    """Тесты отображения хронологии."""

    def test_display_timeline(self):
        """Отображение полной хронологии."""
        with patch("handlers.history.console.print"):
            result, action_taken = handle_timeline("")
            self.assertTrue(action_taken)

    def test_display_timeline_help(self):
        """Отображение справки /timeline help."""
        with patch("handlers.history.console.print"):
            result, action_taken = handle_timeline("help")
            self.assertTrue(action_taken)

    def test_display_unknown_era(self):
        """Запрос несуществующей эпохи."""
        with patch("handlers.history.console.print"):
            result, action_taken = handle_timeline("era nonexistent")
            self.assertFalse(action_taken)

    def test_display_valid_era(self):
        """Запрос существующей эпохи."""
        with patch("handlers.history.console.print"):
            result, action_taken = handle_timeline("era 1980")
            self.assertTrue(action_taken)


class TestEraDetails(unittest.TestCase):
    """Тесты деталей эпох."""

    def test_era_1980s(self):
        """Детали 1980-х."""
        with patch("handlers.history.console.print"):
            success = _display_era_details("1980")
            self.assertTrue(success)

    def test_era_1990s(self):
        """Детали 1990-х."""
        with patch("handlers.history.console.print"):
            success = _display_era_details("1990")
            self.assertTrue(success)

    def test_era_2000s(self):
        """Детали 2000-х."""
        with patch("handlers.history.console.print"):
            success = _display_era_details("2000")
            self.assertTrue(success)

    def test_era_2010s(self):
        """Детали 2010-х."""
        with patch("handlers.history.console.print"):
            success = _display_era_details("2010")
            self.assertTrue(success)

    def test_era_2020s(self):
        """Детали 2020-х."""
        with patch("handlers.history.console.print"):
            success = _display_era_details("2020")
            self.assertTrue(success)


class TestHistoryQuiz(unittest.TestCase):
    """Тесты викторины по истории."""

    def test_quiz_runs(self):
        """Викторина запускается без ошибок."""
        with patch("handlers.history.console.print"):
            _run_history_quiz()
            # Если не упало — тест пройден

    def test_quiz_questions_exist(self):
        """Вопросы викторины существуют."""
        self.assertGreater(len(QUIZ_QUESTIONS), 0)
        for q in QUIZ_QUESTIONS:
            self.assertIn("q", q)
            self.assertIn("a", q)
            self.assertIn("hint", q)

    def test_eras_exist(self):
        """Эпохи определены."""
        self.assertGreater(len(ERAS), 0)
        for era in ERAS:
            self.assertIn("name", era)
            self.assertIn("period", era)
            self.assertIn("events", era)
            self.assertIn("tools", era)
            self.assertIn("vulnerabilities", era)


if __name__ == "__main__":
    unittest.main()
