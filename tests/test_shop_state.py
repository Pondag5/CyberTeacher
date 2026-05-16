"""
Tests for shop_state module.
"""

import unittest
from shop_state import ShopState


class TestShopState(unittest.TestCase):
    
    def setUp(self):
        self.state = ShopState()
    
    def test_default_values(self):
        """Test default values are set correctly."""
        self.assertEqual(self.state.owned_themes, [])
        self.assertEqual(self.state.current_theme, "default")
        self.assertEqual(self.state.unlocked_topics, [])
        self.assertEqual(self.state.hint_credits, 0)
        self.assertEqual(self.state.selected_tools, [])
        self.assertIsNone(self.state.trace_deadline)
        self.assertIsNone(self.state.trace_hint)
    
    def test_apply_theme_item(self):
        """Test applying a theme item."""
        item = {"type": "theme", "value": "dark"}
        result = self.state.apply_item_effect(item)
        
        self.assertEqual(result, "theme")
        self.assertIn("dark", self.state.owned_themes)
        self.assertEqual(len(self.state.owned_themes), 1)
    
    def test_apply_duplicate_theme(self):
        """Test applying duplicate theme does nothing."""
        # Add theme first
        self.state.apply_item_effect({"type": "theme", "value": "dark"})
        initial_count = len(self.state.owned_themes)
        
        # Try to add again
        result = self.state.apply_item_effect({"type": "theme", "value": "dark"})
        
        self.assertIsNone(result)  # Should return None for duplicate
        self.assertEqual(len(self.state.owned_themes), initial_count)
    
    def test_apply_unlock_topic(self):
        """Test applying unlock topic item."""
        item = {"type": "unlock_topic", "value": "web_security"}
        result = self.state.apply_item_effect(item)
        
        self.assertEqual(result, "unlock_topic")
        self.assertIn("web_security", self.state.unlocked_topics)
        self.assertEqual(len(self.state.unlocked_topics), 1)
    
    def test_apply_xp_boost(self):
        """Test applying XP boost item."""
        item = {"type": "xp_boost", "multiplier": 2.0, "duration_hours": 1}
        result = self.state.apply_item_effect(item)
        
        self.assertEqual(result, "xp_boost")
        self.assertEqual(self.state.xp_boost_multiplier, 2.0)
        # expiry should be set to approximately 1 hour from now
        self.assertGreater(self.state.xp_boost_expiry, 0)
    
    def test_apply_hint_credit(self):
        """Test applying hint credit consumable."""
        item = {"type": "consumable", "effect": "hint_credit", "quantity": 3}
        result = self.state.apply_item_effect(item)
        
        self.assertEqual(result, "hint_credit")
        self.assertEqual(self.state.hint_credits, 3)
    
    def test_apply_unknown_item(self):
        """Test applying unknown item type returns None."""
        item = {"type": "unknown", "value": "something"}
        result = self.state.apply_item_effect(item)
        
        self.assertIsNone(result)
    
    def test_apply_item_missing_type(self):
        """Test applying item without type field."""
        item = {"value": "something"}
        result = self.state.apply_item_effect(item)
        
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()