#!/usr/bin/env python3
"""Тесты для /social command (C-02)"""

import unittest
from unittest.mock import MagicMock, patch

from handlers.social import SCENARIOS, handle_social


class TestSocialCommand(unittest.TestCase):
    """Проверка социального инженера"""

    def test_scenarios_exist(self):
        """Все обязательные сценарии присутствуют"""
        required = ["phishing", "pretexting", "tailgating"]
        for key in required:
            self.assertIn(key, SCENARIOS)
            self.assertIn("victim_prompt", SCENARIOS[key])
            self.assertIn("goal", SCENARIOS[key])

    def test_scenario_keys_unique(self):
        """Ключи сценариев уникальны"""
        keys = list(SCENARIOS.keys())
        self.assertEqual(len(keys), len(set(keys)))

    def test_invalid_scenario_shows_list(self):
        """Неверный сценарий -> вывод списка доступных"""
        with patch("handlers.social.console") as mock_console:
            # Имитируем отсутствие LLM
            with patch("handlers.social.LazyLoader.get_llm", return_value=None):
                # handle_social с несуществующим сценарием
                result = handle_social("/social invalid")
                # Должен вернуть (True, None, None, True)
                self.assertEqual(result, (True, None, None, True))
                # Проверяем, что был вывод списка доступных
                printed = " ".join(
                    str(call) for call in mock_console.print.call_args_list
                )
                self.assertIn("Доступные", printed)

    def test_success_structure(self):
        """handle_social возвращает правильную структуру tuple"""
        with patch("handlers.social.LazyLoader.get_llm", return_value=None):
            result = handle_social("/social phishing")
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 4)
            self.assertEqual(result[0], True)  # should_continue
            self.assertIsNone(result[1])  # response
            self.assertIsNone(result[2])  # extra_data
            self.assertEqual(result[3], True)  # is_json

    def test_scenario_defaults_to_phishing(self):
        """Если не указан сценарий - используется phishing"""
        with patch("handlers.social.LazyLoader.get_llm", return_value=None):
            # Вызов без параметра
            result = handle_social("social")
            self.assertEqual(result, (True, None, None, True))

    def test_scenario_with_parameter(self):
        """Сценарий передаётся корректно"""
        with patch("handlers.social.LazyLoader.get_llm", return_value=None):
            result = handle_social("social pretexting")
            self.assertEqual(result, (True, None, None, True))

    def test_phishing_scenario_content(self):
        """Фишинг-сценарий содержит ожидаемые элементы"""
        phishing = SCENARIOS["phishing"]
        self.assertIn("Анна", phishing["victim_prompt"])
        self.assertIn("email", phishing["victim_prompt"].lower())
        self.assertIn("пароль", phishing["goal"].lower())

    def test_pretexting_scenario_content(self):
        """Претекстинг-сценарий содержит ожидаемые элементы"""
        pretext = SCENARIOS["pretexting"]
        self.assertIn("IT-поддержки", pretext["victim_prompt"])
        self.assertIn("пароль", pretext["goal"].lower())

    def test_tailgating_scenario_content(self):
        """Тейлгейтинг-сценарий содержит ожидаемые элементы"""
        tailgate = SCENARIOS["tailgating"]
        self.assertIn("пропуск", tailgate["victim_prompt"])
        self.assertIn("дверь", tailgate["goal"].lower())


if __name__ == "__main__":
    unittest.main()
