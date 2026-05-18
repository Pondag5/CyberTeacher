"""
Tests for features handler.
"""

import unittest
from unittest.mock import MagicMock, patch

from handlers.features import (
    DEFAULT_FEATURES,
    _list_features,
    handle_features,
    is_feature_enabled,
)


class TestFeaturesHandler(unittest.TestCase):
    """Tests for /features command handler."""

    def test_default_features_not_empty(self):
        self.assertGreater(len(DEFAULT_FEATURES), 5)

    def test_default_features_have_required_keys(self):
        for fid, info in DEFAULT_FEATURES.items():
            self.assertIn("enabled", info)
            self.assertIn("description", info)

    @patch("handlers.features.get_context")
    @patch("handlers.features.console")
    def test_list_features(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = {k: v["enabled"] for k, v in DEFAULT_FEATURES.items()}
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_features("/features")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.features.get_context")
    @patch("handlers.features.console")
    def test_enable_feature(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = dict.fromkeys(DEFAULT_FEATURES, False)
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_features("/features enable voice")

        self.assertTrue(success)
        self.assertTrue(mock_state.feature_flags["voice"])
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.features.get_context")
    @patch("handlers.features.console")
    def test_disable_feature(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = dict.fromkeys(DEFAULT_FEATURES, True)
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_features("/features disable hints")

        self.assertTrue(success)
        self.assertFalse(mock_state.feature_flags["hints"])
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.features.get_context")
    @patch("handlers.features.console")
    def test_toggle_feature(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = {"voice": False}
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_features("/features toggle voice")

        self.assertTrue(success)
        self.assertTrue(mock_state.feature_flags["voice"])

    @patch("handlers.features.get_context")
    @patch("handlers.features.console")
    def test_toggle_feature_off(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = {"voice": True}
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_features("/features toggle voice")

        self.assertTrue(success)
        self.assertFalse(mock_state.feature_flags["voice"])

    @patch("handlers.features.get_context")
    @patch("handlers.features.console")
    def test_enable_unknown_feature(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = {}
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_features("/features enable nonexistent")

        self.assertTrue(success)
        mock_ctx.save_state.assert_not_called()

    @patch("handlers.features.get_context")
    @patch("handlers.features.console")
    def test_reset_features(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = dict.fromkeys(DEFAULT_FEATURES, False)
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_features("/features reset")

        self.assertTrue(success)
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.features.get_context")
    @patch("handlers.features.console")
    def test_enable_no_module_specified(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = {}
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_features("/features enable")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.features.get_context")
    def test_is_feature_enabled_default(self, mock_get_context):
        mock_state = MagicMock()
        del mock_state.feature_flags
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        self.assertTrue(is_feature_enabled("hints"))
        self.assertFalse(is_feature_enabled("voice"))

    @patch("handlers.features.get_context")
    def test_is_feature_enabled_from_state(self, mock_get_context):
        mock_state = MagicMock()
        mock_state.feature_flags = {"voice": True, "hints": False}
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        self.assertTrue(is_feature_enabled("voice"))
        self.assertFalse(is_feature_enabled("hints"))


if __name__ == "__main__":
    unittest.main()
