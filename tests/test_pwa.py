"""Тесты для модуля Mobile Companion App PWA (M-32)."""

import unittest
from unittest.mock import patch

from handlers.pwa import handle_pwa


class TestPWA(unittest.TestCase):
    """Тесты PWA."""

    def test_pwa_info(self):
        """Информация о PWA."""
        with patch("handlers.pwa.console.print"):
            result, action_taken = handle_pwa("")
            self.assertTrue(action_taken)

    def test_pwa_setup(self):
        """Инструкция по установке."""
        with patch("handlers.pwa.console.print"):
            result, action_taken = handle_pwa("setup")
            self.assertTrue(action_taken)

    def test_pwa_help(self):
        """Справка."""
        with patch("handlers.pwa.console.print"):
            result, action_taken = handle_pwa("help")
            self.assertTrue(action_taken)

    def test_pwa_unknown(self):
        """Неизвестная подкоманда."""
        with patch("handlers.pwa.console.print"):
            result, action_taken = handle_pwa("unknown")
            self.assertTrue(action_taken)


if __name__ == "__main__":
    unittest.main()
