"""Тесты для модуля Shodan/Censys (M-07)."""

import unittest
from unittest.mock import patch

from handlers.shodan_censys import (
    handle_shodan,
    handle_censys,
    _simulate_shodan_search,
    _simulate_shodan_host,
    _simulate_censys_search,
)


class TestShodan(unittest.TestCase):
    """Тесты Shodan."""

    def test_shodan_help(self):
        """Вызов справки /shodan."""
        with patch("handlers.shodan_censys.console.print"):
            result, action_taken = handle_shodan("")
            self.assertTrue(action_taken)

    def test_shodan_search(self):
        """Поиск в Shodan."""
        with patch("handlers.shodan_censys.console.print"):
            result, action_taken = handle_shodan("search apache")
            self.assertTrue(action_taken)

    def test_shodan_host(self):
        """Информация о хосте Shodan."""
        with patch("handlers.shodan_censys.console.print"):
            result, action_taken = handle_shodan("host 8.8.8.8")
            self.assertTrue(action_taken)

    def test_shodan_search_empty(self):
        """Поиск без запроса."""
        with patch("handlers.shodan_censys.console.print"):
            result, action_taken = handle_shodan("search")
            self.assertFalse(action_taken)

    def test_simulate_shodan_search(self):
        """Симуляция поиска возвращает данные."""
        results = _simulate_shodan_search("test")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIn("ip", results[0])

    def test_simulate_shodan_host(self):
        """Симуляция хоста возвращает данные."""
        data = _simulate_shodan_host("1.2.3.4")
        self.assertIn("ip", data)
        self.assertIn("ports", data)
        self.assertIn("os", data)


class TestCensys(unittest.TestCase):
    """Тесты Censys."""

    def test_censys_help(self):
        """Вызов справки /censys."""
        with patch("handlers.shodan_censys.console.print"):
            result, action_taken = handle_censys("")
            self.assertTrue(action_taken)

    def test_censys_search(self):
        """Поиск в Censys."""
        with patch("handlers.shodan_censys.console.print"):
            result, action_taken = handle_censys("search nginx")
            self.assertTrue(action_taken)

    def test_censys_host(self):
        """Информация о хосте Censys."""
        with patch("handlers.shodan_censys.console.print"):
            result, action_taken = handle_censys("host 8.8.4.4")
            self.assertTrue(action_taken)

    def test_censys_search_empty(self):
        """Поиск без запроса."""
        with patch("handlers.shodan_censys.console.print"):
            result, action_taken = handle_censys("search")
            self.assertFalse(action_taken)

    def test_simulate_censys_search(self):
        """Симуляция поиска Censys возвращает данные."""
        results = _simulate_censys_search("test")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIn("ip", results[0])


if __name__ == "__main__":
    unittest.main()
