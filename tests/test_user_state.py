"""
Tests for user_state module.
"""

import unittest
from unittest.mock import patch

from models.metrics_state import MetricsState
from models.user_state import UserState
from utils.security import encrypt_value


class TestUserState(unittest.TestCase):
    def setUp(self):
        self.state = UserState()

    def test_default_values(self):
        """Test default values are set correctly."""
        self.assertEqual(self.state.username, "Аноним")
        self.assertEqual(self.state.avatar, "🧑‍💻")
        self.assertEqual(self.state.reputation, 0)
        self.assertEqual(self.state.handle, "Новичок")
        self.assertIsNone(self.state.htb_email)
        self.assertIsNone(self.state.htb_password)
        self.assertEqual(self.state.htb_completed, [])

    def test_handle_update(self):
        """Test that handle updates correctly with reputation."""
        # Test initial handle
        self.assertEqual(self.state.get_handle(), "Новичок")

        # Test Script Kiddie threshold
        self.state.add_reputation(50)
        self.assertEqual(self.state.get_handle(), "Script Kiddie")

        # Test Хакер threshold
        self.state.add_reputation(100)  # Total 150
        self.assertEqual(self.state.get_handle(), "Хакер")

        # Test exceeding highest threshold
        self.state.add_reputation(2000)  # Much higher than Фантом threshold
        self.assertEqual(self.state.get_handle(), "Фантом")

    def test_handle_property(self):
        """Test that handle property stays updated."""
        self.state.reputation = 75
        self.assertEqual(self.state.get_handle(), "Script Kiddie")

        self.state.reputation = 350
        self.assertEqual(self.state.get_handle(), "Пентестер")

    @patch.dict("os.environ", {"CYBERTEACHER_ENC_KEY": "test_fixed_key_12345"})
    def test_htb_password_encryption(self):
        """Test HTB password encryption/decryption."""
        test_password = "my_secret_password"
        self.state.htb_password = test_password

        encrypted = self.state.get_htb_password_encrypted()
        self.assertIsNotNone(encrypted)
        self.assertNotEqual(encrypted, test_password)

        # Test setting from encrypted
        new_state = UserState()
        new_state.set_htb_password_from_encrypted(encrypted)
        self.assertEqual(new_state.htb_password, test_password)

    def test_htb_password_none(self):
        """Test handling of None password."""
        self.state.htb_password = None
        encrypted = self.state.get_htb_password_encrypted()
        self.assertIsNone(encrypted)

        new_state = UserState()
        new_state.set_htb_password_from_encrypted(None)
        self.assertIsNone(new_state.htb_password)

    @patch("models.metrics_state.time.time")
    def test_rate_limiting(self, mock_time):
        """Test rate limiting functionality."""
        state = MetricsState()
        # Mock time to return increasing values
        mock_time.side_effect = [0, 30, 59, 60, 61, 119]

        # Should allow requests under limit
        self.assertTrue(state.can_make_request())
        state.record_request()

        self.assertTrue(state.can_make_request())
        state.record_request()

        # Should still allow (2 requests so far, limit is 10)
        self.assertTrue(state.can_make_request())

        # Advance time past window
        mock_time.return_value = 121  # 61 seconds after first request
        self.assertTrue(state.can_make_request())  # Old requests expired


if __name__ == "__main__":
    unittest.main()
