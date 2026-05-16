"""Тесты для модуля Interactive Investigations (M-10)."""

import unittest
from unittest.mock import patch

from handlers.investigation import (
    handle_investigation,
    _start_case,
    _examine_evidence,
    _conclude,
    CASES,
)


class TestInvestigation(unittest.TestCase):
    """Тесты интерактивных расследований."""

    def test_display_cases(self):
        """Отображение списка кейсов."""
        with patch("handlers.investigation.console.print"):
            result, action_taken = handle_investigation("")
            self.assertTrue(action_taken)

    def test_start_valid_case(self):
        """Начало существующего кейса."""
        with patch("handlers.investigation.console.print"):
            success = _start_case("corp_espionage")
            self.assertTrue(success)

    def test_start_invalid_case(self):
        """Начало несуществующего кейса."""
        with patch("handlers.investigation.console.print"):
            success = _start_case("nonexistent")
            self.assertFalse(success)

    def test_examine_evidence(self):
        """Изучение улики."""
        with patch("handlers.investigation.console.print"):
            with patch("handlers.investigation.get_state") as mock_state:
                mock_state.return_value.current_case = "corp_espionage"
                mock_state.return_value.found_evidence = []
                mock_state.return_value.xp = 0
                success = _examine_evidence("email_logs")
                self.assertTrue(success)

    def test_examine_invalid_evidence(self):
        """Изучение несуществующей улики."""
        with patch("handlers.investigation.console.print"):
            with patch("handlers.investigation.get_state") as mock_state:
                mock_state.return_value.current_case = "corp_espionage"
                success = _examine_evidence("nonexistent")
                self.assertFalse(success)

    def test_conclude_correct(self):
        """Правильное обвинение."""
        with patch("handlers.investigation.console.print"):
            with patch("handlers.investigation.get_state") as mock_state:
                mock_state.return_value.current_case = "corp_espionage"
                mock_state.return_value.found_evidence = ["email_logs"]
                mock_state.return_value.xp = 0
                success = _conclude("Петрова (Инженер)")
                self.assertTrue(success)

    def test_conclude_wrong(self):
        """Неправильное обвинение."""
        with patch("handlers.investigation.console.print"):
            with patch("handlers.investigation.get_state") as mock_state:
                mock_state.return_value.current_case = "corp_espionage"
                mock_state.return_value.found_evidence = []
                success = _conclude("Иванов (Бухгалтер)")
                self.assertFalse(success)

    def test_conclude_without_case(self):
        """Обвинение без начатого кейса."""
        with patch("handlers.investigation.console.print"):
            with patch("handlers.investigation.get_state") as mock_state:
                del mock_state.return_value.current_case
                success = _conclude("Test")
                self.assertFalse(success)

    def test_help_command(self):
        """Вызов справки /investigation help."""
        with patch("handlers.investigation.console.print"):
            result, action_taken = handle_investigation("help")
            self.assertTrue(action_taken)

    def test_unknown_subcommand(self):
        """Неизвестная подкоманда."""
        with patch("handlers.investigation.console.print"):
            result, action_taken = handle_investigation("unknown")
            self.assertTrue(action_taken)

    def test_cases_structure(self):
        """Проверка структуры кейсов."""
        self.assertGreater(len(CASES), 0)
        for cid, case in CASES.items():
            self.assertIn("title", case)
            self.assertIn("description", case)
            self.assertIn("suspects", case)
            self.assertIn("culprit", case)
            self.assertIn("evidence", case)
            self.assertIn("red_herrings", case)
            self.assertIn("xp", case)


if __name__ == "__main__":
    unittest.main()
