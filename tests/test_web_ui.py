"""
Tests for web_ui.py helper functions.
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock


class TestWebUIHelpers(unittest.TestCase):
    """Tests for web_ui.py helper functions."""

    def setUp(self):
        """Clear module cache to force re-import."""
        if "web_ui" in sys.modules:
            del sys.modules["web_ui"]

    def test_generate_xp_history_from_state(self):
        """Test XP history generation from state."""
        state = {
            "points": 1000,
            "xp_history": [
                {"date": "2024-01-01", "xp": 100},
                {"date": "2024-01-02", "xp": 200},
            ],
        }

        from web_ui import generate_xp_history
        result = generate_xp_history(state)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["xp"], 100)

    def test_generate_xp_history_synthetic(self):
        """Test synthetic XP history generation."""
        state = {"points": 500}

        from web_ui import generate_xp_history
        result = generate_xp_history(state)
        self.assertEqual(len(result), 30)
        self.assertGreater(result[-1]["xp"], 0)

    def test_generate_xp_history_empty(self):
        """Test empty XP history."""
        state = {"points": 0}

        from web_ui import generate_xp_history
        result = generate_xp_history(state)
        self.assertEqual(len(result), 0)

    def test_generate_activity_heatmap(self):
        """Test activity heatmap generation."""
        state = {
            "activity_log": {
                "2024-01-01": 5,
                "2024-01-02": 3,
            }
        }

        from web_ui import generate_activity_heatmap
        result = generate_activity_heatmap(state)
        self.assertEqual(len(result), 4)  # 4 weeks
        self.assertEqual(len(result[0]), 7)  # 7 days per week

    def test_generate_activity_heatmap_empty(self):
        """Test empty activity heatmap."""
        state = {}

        from web_ui import generate_activity_heatmap
        result = generate_activity_heatmap(state)
        self.assertEqual(len(result), 4)
        for week in result:
            for day in week:
                self.assertEqual(day, 0)


class TestWebUIStateLoading(unittest.TestCase):
    """Tests for state loading functions."""

    def setUp(self):
        """Clear module cache."""
        if "web_ui" in sys.modules:
            del sys.modules["web_ui"]

    def test_load_state_missing_file(self):
        """Test loading state from missing file."""
        with patch("web_ui.STATE_PATH") as mock_path:
            mock_path.exists.return_value = False
            from web_ui import load_state
            result = load_state()
            self.assertEqual(result, {})

    def test_load_state_existing_file(self):
        """Test loading state from existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = os.path.join(tmpdir, "app_state.json")
            test_state = {"username": "TestUser", "points": 100}
            with open(state_path, "w") as f:
                json.dump(test_state, f)

            # Directly test the function logic without import issues
            from pathlib import Path
            from web_ui import load_state

            # Temporarily replace STATE_PATH
            import web_ui
            original_path = web_ui.STATE_PATH
            web_ui.STATE_PATH = Path(state_path)
            try:
                result = load_state()
                self.assertEqual(result["username"], "TestUser")
            finally:
                web_ui.STATE_PATH = original_path


if __name__ == "__main__":
    unittest.main()
