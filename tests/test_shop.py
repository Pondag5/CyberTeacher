"""Тесты для системы магазина (C-14)"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from handlers import shop as shop_handler
from state import AppState


class TestShopHandler(unittest.TestCase):
    """Тесты обработчика магазина"""

    def setUp(self):
        """Подготовка тестового окружения"""
        self.state = AppState()
        self.state.points = 200
        self.state.owned_themes = []
        self.state.current_theme = "default"
        self.state.unlocked_topics = []
        self.state.hint_credits = 0
        self.state.xp_boost_multiplier = 1.0
        self.state.xp_boost_expiry = 0.0

        # Временный shop_items.json
        self.test_shop_items = {
            "items": [
                {
                    "id": "theme_test",
                    "name": "Test Theme",
                    "description": "Test",
                    "cost": 50,
                    "type": "theme",
                    "value": "test",
                },
                {
                    "id": "hint_1",
                    "name": "One Hint",
                    "description": "1 hint",
                    "cost": 20,
                    "type": "consumable",
                    "effect": "hint_credit",
                    "quantity": 1,
                },
                {
                    "id": "xp_2x_1h",
                    "name": "2x XP 1h",
                    "description": "Double XP for 1 hour",
                    "cost": 100,
                    "type": "xp_boost",
                    "multiplier": 2.0,
                    "duration_hours": 1,
                },
            ]
        }
        self.temp_dir = tempfile.TemporaryDirectory()
        self.shop_file = Path(self.temp_dir.name) / "shop_items.json"
        import json

        with open(self.shop_file, "w", encoding="utf-8") as f:
            json.dump(self.test_shop_items, f)

        self.original_shop_file = shop_handler.SHOP_ITEMS_FILE
        shop_handler.SHOP_ITEMS_FILE = str(self.shop_file)

        # Патчим консоль
        self.console_patcher = patch.object(shop_handler, "console", MagicMock())
        self.mock_console = self.console_patcher.start()

    def tearDown(self):
        """Очистка"""
        shop_handler.SHOP_ITEMS_FILE = self.original_shop_file
        self.console_patcher.stop()
        self.temp_dir.cleanup()

    @patch("handlers.shop.get_context")
    def test_shop_list_items(self, mock_get_context):
        """Тест отображения списка товаров"""
        mock_ctx = MagicMock()
        mock_ctx.state = self.state
        mock_get_context.return_value = mock_ctx
        result = shop_handler.handle_shop("")
        self.assertTrue(result[0])
        self.assertEqual(self.state.points, 200)

    @patch("handlers.shop.get_context")
    def test_handle_shop_show_with_no_items(self, mock_get_context):
        """Тест пустого магазина"""
        empty_shop = {"items": []}
        with open(self.shop_file, "w", encoding="utf-8") as f:
            import json

            json.dump(empty_shop, f)
        mock_ctx = MagicMock()
        mock_ctx.state = self.state
        mock_get_context.return_value = mock_ctx
        result = shop_handler.handle_shop("")
        self.assertTrue(result[0])

    @patch("handlers.shop.get_context")
    def test_purchase_theme(self, mock_get_context):
        """Тест покупки темы"""
        self.state.points = 200
        mock_ctx = MagicMock()
        mock_ctx.state = self.state
        mock_get_context.return_value = mock_ctx
        result = shop_handler.handle_shop("shop theme_test")
        self.assertTrue(result[0])
        self.assertEqual(self.state.points, 150)
        self.assertIn("test", self.state.owned_themes)

    @patch("handlers.shop.get_context")
    def test_purchase_insufficient_funds(self, mock_get_context):
        """Тест покупки без достаточного XP"""
        self.state.points = 10
        mock_ctx = MagicMock()
        mock_ctx.state = self.state
        mock_get_context.return_value = mock_ctx
        result = shop_handler.handle_shop("shop theme_test")
        self.assertTrue(result[0])
        self.assertEqual(self.state.points, 10)
        self.assertNotIn("test", self.state.owned_themes)

    @patch("handlers.shop.get_context")
    def test_purchase_duplicate_theme(self, mock_get_context):
        """Тест повторной покупки темы"""
        self.state.points = 200
        self.state.owned_themes = ["test"]
        mock_ctx = MagicMock()
        mock_ctx.state = self.state
        mock_get_context.return_value = mock_ctx
        result = shop_handler.handle_shop("shop theme_test")
        self.assertTrue(result[0])
        self.assertEqual(self.state.points, 200)
        self.assertEqual(self.state.owned_themes.count("test"), 1)

    @patch("handlers.shop.get_context")
    def test_purchase_consumable(self, mock_get_context):
        """Тест покупки расходника"""
        self.state.points = 100
        mock_ctx = MagicMock()
        mock_ctx.state = self.state
        mock_get_context.return_value = mock_ctx
        result = shop_handler.handle_shop("shop hint_1")
        self.assertTrue(result[0])
        self.assertEqual(self.state.points, 80)
        self.assertEqual(self.state.hint_credits, 1)

    @patch("handlers.shop.get_context")
    def test_purchase_xp_boost(self, mock_get_context):
        """Тест покупки XP буста"""
        self.state.points = 200
        import time

        before = time.time()
        mock_ctx = MagicMock()
        mock_ctx.state = self.state
        mock_get_context.return_value = mock_ctx
        result = shop_handler.handle_shop("shop xp_2x_1h")
        self.assertTrue(result[0])
        self.assertEqual(self.state.points, 100)
        self.assertEqual(self.state.xp_boost_multiplier, 2.0)
        self.assertGreater(self.state.xp_boost_expiry, before)

    @patch("handlers.shop.get_context")
    def test_purchase_unknown_item(self, mock_get_context):
        """Тест покупки несуществующего товара"""
        self.state.points = 200
        mock_ctx = MagicMock()
        mock_ctx.state = self.state
        mock_get_context.return_value = mock_ctx
        result = shop_handler.handle_shop("shop unknown_item")
        self.assertTrue(result[0])
        self.assertEqual(self.state.points, 200)

    def test_apply_item_effect_theme(self):
        """Тест применения эффекта темы"""
        self.state.owned_themes = []
        item = {"type": "theme", "value": "matrix"}
        self.state.apply_item_effect(item)
        self.assertIn("matrix", self.state.owned_themes)

    def test_apply_item_effect_topic(self):
        """Тест разблокировки темы"""
        self.state.unlocked_topics = []
        item = {"type": "unlock_topic", "value": "cloud"}
        self.state.apply_item_effect(item)
        self.assertIn("cloud", self.state.unlocked_topics)

    def test_apply_item_effect_consumable(self):
        """Тест добавления расходника"""
        self.state.hint_credits = 0
        item = {"type": "consumable", "effect": "hint_credit", "quantity": 3}
        self.state.apply_item_effect(item)
        self.assertEqual(self.state.hint_credits, 3)

    def test_apply_item_effect_xp_boost(self):
        """Тест применения XP буста"""
        self.state.xp_boost_multiplier = 1.0
        self.state.xp_boost_expiry = 0.0
        item = {"type": "xp_boost", "multiplier": 2.0, "duration_hours": 2}
        self.state.apply_item_effect(item)
        self.assertEqual(self.state.xp_boost_multiplier, 2.0)
        import time

        expected_expiry = time.time() + 2 * 3600
        self.assertAlmostEqual(self.state.xp_boost_expiry, expected_expiry, delta=5)


class TestShopIntegration(unittest.TestCase):
    """Интеграционные тесты магазина"""

    def test_xp_multiplier_in_achievements(self):
        """XP умножается при активном бусте"""
        state = AppState()
        state.points = 0
        state.xp_boost_multiplier = 2.0
        import time

        state.xp_boost_expiry = time.time() + 3600

        xp_gained = 0
        for ach_points in [50]:
            xp_gained += ach_points * state.get_xp_multiplier()
        state.points += xp_gained

        self.assertEqual(state.points, 100)

    def test_expired_boost_resets(self):
        """Истекший буст сбрасывается"""
        state = AppState()
        state.xp_boost_multiplier = 2.0
        state.xp_boost_expiry = 0.0
        mult = state.get_xp_multiplier()
        self.assertEqual(mult, 1.0)
        self.assertEqual(state.xp_boost_multiplier, 1.0)
        self.assertEqual(state.xp_boost_expiry, 0.0)


if __name__ == "__main__":
    unittest.main()
