"""Тесты для модуля OSINT (M-03)."""

import unittest
from unittest.mock import patch

from handlers.osint import (
    handle_osint,
    handle_osint_email,
    handle_osint_metadata,
    handle_osint_phone,
    handle_osint_search,
    _simulate_breaches,
    _simulate_social_media,
)


class TestOSINTSearch(unittest.TestCase):
    """Тесты поиска по никнейму."""

    def test_valid_username(self):
        """Поиск с валидным никнеймом."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_search("testuser")
            self.assertTrue(action_taken)

    def test_short_username(self):
        """Поиск с коротким никнеймом (<3 символов)."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_search("ab")
            self.assertTrue(action_taken)

    def test_empty_username(self):
        """Поиск с пустым никнеймом."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_search("")
            self.assertTrue(action_taken)

    def test_simulate_social_media(self):
        """Симуляция поиска в соцсетях возвращает список."""
        results = _simulate_social_media("testuser")
        self.assertIsInstance(results, list)
        if results:
            self.assertIn("name", results[0])
            self.assertIn("url", results[0])


class TestOSINTEmail(unittest.TestCase):
    """Тесты проверки email."""

    def test_valid_email(self):
        """Проверка валидного email."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_email("test@example.com")
            self.assertTrue(action_taken)

    def test_invalid_email(self):
        """Проверка невалидного email."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_email("invalid-email")
            self.assertTrue(action_taken)

    def test_simulate_breaches(self):
        """Симуляция утечек возвращает список."""
        results = _simulate_breaches("test@example.com")
        self.assertIsInstance(results, list)
        if results:
            self.assertIn("name", results[0])
            self.assertIn("data", results[0])


class TestOSINTPhone(unittest.TestCase):
    """Тесты поиска по телефону."""

    def test_valid_phone(self):
        """Поиск по валидному номеру."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_phone("+79991234567")
            self.assertTrue(action_taken)

    def test_short_phone(self):
        """Поиск по короткому номеру."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_phone("123")
            self.assertTrue(action_taken)


class TestOSINTMetadata(unittest.TestCase):
    """Тесты анализа метаданных."""

    def test_valid_file(self):
        """Анализ метаданных файла."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_metadata("test.jpg")
            self.assertTrue(action_taken)

    def test_empty_file(self):
        """Анализ без указания файла."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint_metadata("")
            self.assertTrue(action_taken)


class TestOSINTMainHandler(unittest.TestCase):
    """Тесты главного обработчика /osint."""

    def test_osint_help(self):
        """Вызов справки /osint help."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint("help")
            self.assertTrue(action_taken)

    def test_osint_search(self):
        """Вызов /osint search username."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint("search testuser")
            self.assertTrue(action_taken)

    def test_osint_email(self):
        """Вызов /osint email test@example.com."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint("email test@example.com")
            self.assertTrue(action_taken)

    def test_osint_phone(self):
        """Вызов /osint phone +79991234567."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint("phone +79991234567")
            self.assertTrue(action_taken)

    def test_osint_metadata(self):
        """Вызов /osint metadata file.jpg."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint("metadata file.jpg")
            self.assertTrue(action_taken)

    def test_osint_no_args(self):
        """Вызов /osint без аргументов показывает справку."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint("")
            self.assertTrue(action_taken)

    def test_osint_unknown_subcommand(self):
        """Вызов неизвестной подкоманды."""
        with patch("handlers.osint.console.print"):
            result, action_taken = handle_osint("unknown arg")
            self.assertTrue(action_taken)


if __name__ == "__main__":
    unittest.main()
