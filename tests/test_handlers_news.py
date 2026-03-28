"""Unit tests for handlers/news.py"""

import unittest
from unittest.mock import MagicMock, patch


class MockState:
    def __init__(self):
        self.last_news = None
        self.news_checked = 0
        self.earned_achievements = []

    def check_news(self):
        self.news_checked += 1

    def check_achievements(self):
        return []


class TestHandlersNews(unittest.TestCase):
    """Tests for handlers/news module"""

    @patch("handlers.news.get_state")
    @patch("handlers.news.console.print")
    @patch("news_fetcher.fetch_news")
    def test_handle_security_news_no_news(self, mock_fetch, mock_print, mock_get_state):
        """Test when fetch_news returns empty list"""
        from handlers import news

        mock_state = MockState()
        mock_get_state.return_value = mock_state
        mock_fetch.return_value = []

        result = news.handle_security_news("", lambda: None)

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Новостей нет.[/yellow]")

    @patch("handlers.news.get_state")
    @patch("handlers.news.console.print")
    @patch("news_fetcher.fetch_news")
    def test_handle_security_news_without_llm(
        self, mock_fetch, mock_print, mock_get_state
    ):
        """Test news fetched but LLM is None -> raw display"""
        from handlers import news

        mock_state = MockState()
        mock_get_state.return_value = mock_state
        mock_fetch.return_value = [
            {"title": "Vuln 1"},
            {"title": "Vuln 2"},
            {"title": "Vuln 3"},
        ]

        result = news.handle_security_news("", None)

        self.assertEqual(result, (True, None, None, True))
        # Should have printed panel with raw news
        # We can check that last_news is set to raw format
        self.assertEqual(mock_state.last_news, "- Vuln 1\n- Vuln 2\n- Vuln 3")
        self.assertEqual(mock_state.news_checked, 1)

    @patch("handlers.news.get_state")
    @patch("handlers.news.console.print")
    @patch("news_fetcher.fetch_news")
    def test_handle_security_news_with_llm_success(
        self, mock_fetch, mock_print, mock_get_state
    ):
        """Test news processed by LLM (get_llm callable returns LLM instance)"""
        from handlers import news

        mock_state = MockState()
        mock_get_state.return_value = mock_state
        mock_fetch.return_value = [{"title": "News A"}, {"title": "News B"}]

        # Create mock LLM instance and a callable that returns it
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = "1. News A - Desc A\n2. News B - Desc B"
        get_llm_callable = lambda: mock_llm_instance

        result = news.handle_security_news("", get_llm_callable)

        self.assertEqual(result, (True, None, None, True))
        mock_llm_instance.invoke.assert_called_once()
        self.assertEqual(mock_state.last_news, "1. News A - Desc A\n2. News B - Desc B")
        mock_print.assert_any_call("[cyan]Обрабатываю новости...[/cyan]")

    @patch("handlers.news.get_state")
    @patch("handlers.news.console.print")
    @patch("news_fetcher.fetch_news")
    def test_handle_security_news_llm_exception_fallback(
        self, mock_fetch, mock_print, mock_get_state
    ):
        """Test LLM raises exception, fallback to raw"""
        from handlers import news

        mock_state = MockState()
        mock_get_state.return_value = mock_state
        mock_fetch.return_value = [{"title": "X"}, {"title": "Y"}]

        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.side_effect = Exception("LLM error")
        get_llm_callable = lambda: mock_llm_instance

        result = news.handle_security_news("", get_llm_callable)

        self.assertEqual(result, (True, None, None, True))
        self.assertEqual(mock_state.last_news, "- X\n- Y")

    @patch("handlers.news.get_state")
    @patch("handlers.news.console.print")
    @patch("news_fetcher.fetch_news")
    def test_handle_security_news_achievements_checked(
        self, mock_fetch, mock_print, mock_get_state
    ):
        """Test that achievements are checked after news"""
        from handlers import news

        mock_state = MockState()
        mock_state.check_news = MagicMock()
        mock_state.check_achievements = MagicMock(return_value=[{"name": "Test Ach"}])
        mock_get_state.return_value = mock_state
        mock_fetch.return_value = [{"title": "News"}]

        result = news.handle_security_news("", None)

        self.assertEqual(result, (True, None, None, True))
        mock_state.check_news.assert_called_once()
        mock_state.check_achievements.assert_called_once()

    @patch("handlers.news.get_state")
    @patch("news_fetcher.fetch_news")
    def test_get_last_news(self, mock_fetch, mock_get_state):
        """Test get_last_news returns state.last_news"""
        from handlers import news

        mock_state = MockState()
        mock_state.last_news = "Some news text"
        mock_get_state.return_value = mock_state

        result = news.get_last_news()

        self.assertEqual(result, "Some news text")


if __name__ == "__main__":
    unittest.main()
