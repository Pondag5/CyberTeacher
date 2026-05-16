"""Тесты для L-08, L-01, H-08, L-13."""

import unittest
from unittest.mock import patch

from handlers.kb_manager import handle_kb, _get_kb_status
from handlers.vision import handle_vision, VISION_ANALYSIS
from handlers.telegram_bot import handle_telegram
from handlers.subscribe import (
    handle_subscribe,
    _add_subscription,
    _remove_subscription,
    _load_subscriptions,
    THREAT_TYPES,
)


class TestKBManager(unittest.TestCase):
    """Тесты управления базой знаний (L-08)."""

    def test_kb_status(self):
        """Статус базы знаний."""
        with patch("handlers.kb_manager.console.print"):
            result, action_taken = handle_kb("status")
            self.assertTrue(action_taken)

    def test_kb_optimize(self):
        """Оптимизация индекса."""
        with patch("handlers.kb_manager.console.print"):
            result, action_taken = handle_kb("optimize")
            self.assertTrue(action_taken)

    def test_kb_reindex(self):
        """Переиндексация."""
        with patch("handlers.kb_manager.console.print"):
            result, action_taken = handle_kb("reindex")
            self.assertTrue(action_taken)

    def test_kb_help(self):
        """Справка."""
        with patch("handlers.kb_manager.console.print"):
            result, action_taken = handle_kb("help")
            self.assertTrue(action_taken)

    def test_get_kb_status(self):
        """Функция получения статуса."""
        status = _get_kb_status()
        self.assertIn("status", status)
        self.assertIn("files", status)


class TestVision(unittest.TestCase):
    """Тесты мультимодальности (L-01)."""

    def test_vision_help(self):
        """Справка."""
        with patch("handlers.vision.console.print"):
            result, action_taken = handle_vision("help")
            self.assertTrue(action_taken)

    def test_vision_analyze_nonexistent(self):
        """Анализ несуществующего файла."""
        with patch("handlers.vision.console.print"):
            result, action_taken = handle_vision("analyze nonexistent.png")
            self.assertFalse(action_taken)

    def test_vision_unknown(self):
        """Неизвестная подкоманда."""
        with patch("handlers.vision.console.print"):
            result, action_taken = handle_vision("unknown")
            self.assertTrue(action_taken)

    def test_vision_analysis_data(self):
        """Проверка данных анализа."""
        self.assertGreater(len(VISION_ANALYSIS), 0)
        for key, findings in VISION_ANALYSIS.items():
            self.assertIsInstance(findings, list)
            self.assertGreater(len(findings), 0)


class TestTelegramBot(unittest.TestCase):
    """Тесты Telegram бота (H-08)."""

    def test_telegram_help(self):
        """Справка."""
        with patch("handlers.telegram_bot.console.print"):
            result, action_taken = handle_telegram("help")
            self.assertTrue(action_taken)

    def test_telegram_status(self):
        """Статус бота."""
        with patch("handlers.telegram_bot.console.print"):
            result, action_taken = handle_telegram("status")
            self.assertTrue(action_taken)

    def test_telegram_start_no_token(self):
        """Запуск без токена."""
        with patch("handlers.telegram_bot.console.print"):
            with patch("handlers.telegram_bot.os.getenv", return_value=None):
                result, action_taken = handle_telegram("start")
                self.assertFalse(action_taken)

    def test_telegram_stop(self):
        """Остановка бота."""
        with patch("handlers.telegram_bot.console.print"):
            with patch("handlers.telegram_bot._bot_running", False):
                result, action_taken = handle_telegram("stop")
                self.assertTrue(action_taken)


class TestSubscribe(unittest.TestCase):
    """Тесты подписки на угрозы (L-13)."""

    def test_subscribe_help(self):
        """Справка."""
        with patch("handlers.subscribe.console.print"):
            result, action_taken = handle_subscribe("help")
            self.assertTrue(action_taken)

    def test_subscribe_list(self):
        """Список подписок."""
        with patch("handlers.subscribe.console.print"):
            result, action_taken = handle_subscribe("list")
            self.assertTrue(action_taken)

    def test_subscribe_add_valid(self):
        """Добавление валидной подписки."""
        with patch("handlers.subscribe.console.print"):
            with patch("handlers.subscribe._save_subscriptions"):
                with patch("handlers.subscribe._load_subscriptions", return_value={"types": [], "notifications": []}):
                    success = _add_subscription("apt")
                    self.assertTrue(success)

    def test_subscribe_add_invalid(self):
        """Добавление невалидной подписки."""
        with patch("handlers.subscribe.console.print"):
            with patch("handlers.subscribe._load_subscriptions", return_value={"types": []}):
                success = _add_subscription("nonexistent")
                self.assertFalse(success)

    def test_subscribe_remove_valid(self):
        """Удаление валидной подписки."""
        with patch("handlers.subscribe.console.print"):
            with patch("handlers.subscribe._save_subscriptions"):
                with patch("handlers.subscribe._load_subscriptions", return_value={"types": ["apt"]}):
                    success = _remove_subscription("apt")
                    self.assertTrue(success)

    def test_subscribe_notify(self):
        """Проверка уведомлений."""
        with patch("handlers.subscribe.console.print"):
            with patch("handlers.subscribe._load_subscriptions", return_value={"types": ["apt"]}):
                result, action_taken = handle_subscribe("notify")
                self.assertTrue(action_taken)

    def test_threat_types_exist(self):
        """Типы угроз определены."""
        self.assertGreater(len(THREAT_TYPES), 0)
        for t, desc in THREAT_TYPES.items():
            self.assertIsInstance(t, str)
            self.assertIsInstance(desc, str)


if __name__ == "__main__":
    unittest.main()
