#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты для C-03: threat summary"""

import unittest
from unittest.mock import patch, MagicMock
from handlers.threats import handle_threat_summary


class TestThreatSummary(unittest.TestCase):
    """Проверка еженедельной сводки угроз"""

    @patch('news_fetcher.fetch_news')
    @patch('handlers.threats.LazyLoader.get_llm')
    @patch('handlers.threats.console')
    def test_threat_summary_with_news(self, mock_console, mock_llm, mock_fetch):
        """Сводка с новостями и LLM анализом"""
        mock_fetch.return_value = [
            {
                "title": "APT42 атаковали энергосистему",
                "desc": "Новая кампанияAPT группы",
                "source": "SecurityWeek",
                "link": "https://example.com"
            },
            {
                "title": "Критический CVE в Apache",
                "desc": "Zero-day уязвимость",
                "source": "CISA",
                "link": ""
            }
        ]
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value.content = "Анализ: угрозы серьёзные"
        mock_llm.return_value = mock_llm_instance

        result = handle_threat_summary("threat summary")

        self.assertEqual(result, (True, None, None, True))
        mock_fetch.assert_called_once_with(force=True)
        mock_llm_instance.invoke.assert_called_once()

    @patch('news_fetcher.fetch_news')
    @patch('handlers.threats.LazyLoader.get_llm')
    @patch('handlers.threats.console')
    def test_threat_summary_no_llm(self, mock_console, mock_llm, mock_fetch):
        """Сводка без LLM — сырые новости"""
        mock_fetch.return_value = [
            {"title": "DDoS атака", "desc": "massive", "source": "Test", "link": ""}
        ]
        mock_llm.return_value = None

        result = handle_threat_summary("threat summary")
        self.assertEqual(result, (True, None, None, True))

    @patch('news_fetcher.fetch_news')
    @patch('handlers.threats.console')
    def test_threat_summary_no_news(self, mock_console, mock_fetch):
        """Нет новостей — inform user"""
        mock_fetch.return_value = []

        result = handle_threat_summary("threat summary")
        self.assertEqual(result, (True, None, None, True))

    @patch('news_fetcher.fetch_news')
    @patch('handlers.threats.LazyLoader.get_llm')
    @patch('handlers.threats.console')
    def test_threat_summary_llm_error(self, mock_console, mock_llm, mock_fetch):
        """Ошибка LLM — fallback на сырые новости"""
        mock_fetch.return_value = [
            {"title": "Ransomware outbreak", "desc": "new variant", "source": "Test", "link": ""}
        ]
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.side_effect = Exception("LLM error")
        mock_llm.return_value = mock_llm_instance

        result = handle_threat_summary("threat summary")
        self.assertEqual(result, (True, None, None, True))


if __name__ == "__main__":
    unittest.main()
