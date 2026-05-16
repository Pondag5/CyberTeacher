"""
Tests for daily, network, equipment, mermaid, and mindmap handlers.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# ── Daily Handler ──────────────────────────────────────────────
class TestDailyHandler(unittest.TestCase):
    """Tests for /daily command handler."""

    @patch("handlers.daily.get_context")
    @patch("handlers.daily.console")
    @patch("handlers.daily.generate_daily_challenge")
    @patch("handlers.daily.get_daily_status")
    def test_daily_show_challenge(self, mock_status, mock_gen, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_gen.return_value = {"desc": "Test challenge", "difficulty": "easy"}
        mock_status.return_value = "Status info"

        from handlers.daily import handle_daily
        success, _, _, continue_loop = handle_daily("/daily")

        self.assertTrue(success)
        self.assertTrue(continue_loop)

    @patch("handlers.daily.get_context")
    @patch("handlers.daily.console")
    @patch("handlers.daily.get_hint")
    def test_daily_hint(self, mock_hint, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_hint.return_value = "This is a hint"

        from handlers.daily import handle_daily
        success, _, _, continue_loop = handle_daily("/daily hint")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.daily.get_context")
    @patch("handlers.daily.console")
    @patch("handlers.daily.get_daily_status")
    def test_daily_status(self, mock_status, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_status.return_value = "Status info"

        from handlers.daily import handle_daily
        success, _, _, continue_loop = handle_daily("/daily status")

        self.assertTrue(success)


# ── Network Handler ───────────────────────────────────────────
class TestNetworkHandler(unittest.TestCase):
    """Tests for /network command handler."""

    @patch("handlers.network.get_state")
    @patch("handlers.network.console")
    def test_network_display(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state

        mock_docker_labs = {"dvwa": {"name": "DVWA", "ports": ["8080:80"]}}
        mock_container_status = {"running": False}

        with patch.dict("sys.modules", {"practice": MagicMock()}):
            import sys
            sys.modules["practice"].DOCKER_LABS = mock_docker_labs
            sys.modules["practice"].get_container_status = MagicMock(return_value=mock_container_status)

            # Re-import to get patched version
            import importlib
            import handlers.network
            importlib.reload(handlers.network)

            from handlers.network import handle_network
            success, _, _, continue_loop = handle_network("/network")

            self.assertTrue(success)


# ── Equipment Handler ─────────────────────────────────────────
class TestEquipmentHandler(unittest.TestCase):
    """Tests for /tools and /equip commands."""

    @patch("handlers.equipment.get_state")
    @patch("handlers.equipment.console")
    def test_tools_list(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.selected_tools = []
        mock_get_state.return_value = mock_state

        with patch("handlers.equipment.TOOL_RAM_COSTS", {"nmap": 2, "sqlmap": 3}):
            with patch("handlers.equipment.MAX_RAM", 10):
                from handlers.equipment import handle_tools
                success, _, _, continue_loop = handle_tools("/tools")

                self.assertTrue(success)
                mock_console.print.assert_called()

    @patch("handlers.equipment.get_state")
    @patch("handlers.equipment.console")
    def test_equip_tool(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.selected_tools = []
        mock_get_state.return_value = mock_state

        with patch("handlers.equipment.TOOL_RAM_COSTS", {"nmap": 2, "sqlmap": 3}):
            with patch("handlers.equipment.MAX_RAM", 10):
                from handlers.equipment import handle_equip
                success, _, _, continue_loop = handle_equip("/equip nmap")

                self.assertTrue(success)
                self.assertIn("nmap", mock_state.selected_tools)
                mock_state.save_to_file.assert_called_once()

    @patch("handlers.equipment.get_state")
    @patch("handlers.equipment.console")
    def test_equip_unknown_tool(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.selected_tools = []
        mock_get_state.return_value = mock_state

        with patch("handlers.equipment.TOOL_RAM_COSTS", {"nmap": 2}):
            with patch("handlers.equipment.MAX_RAM", 10):
                from handlers.equipment import handle_equip
                success, _, _, continue_loop = handle_equip("/equip unknown")

                self.assertTrue(success)
                mock_state.save_to_file.assert_not_called()

    @patch("handlers.equipment.get_state")
    @patch("handlers.equipment.console")
    def test_equip_exceeds_ram(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.selected_tools = ["nmap"]
        mock_get_state.return_value = mock_state

        with patch("handlers.equipment.TOOL_RAM_COSTS", {"nmap": 5, "sqlmap": 6}):
            with patch("handlers.equipment.MAX_RAM", 10):
                from handlers.equipment import handle_equip
                success, _, _, continue_loop = handle_equip("/equip sqlmap")

                self.assertTrue(success)
                self.assertNotIn("sqlmap", mock_state.selected_tools)

    @patch("handlers.equipment.get_state")
    @patch("handlers.equipment.console")
    def test_equip_toggle_off(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.selected_tools = ["nmap"]
        mock_get_state.return_value = mock_state

        with patch("handlers.equipment.TOOL_RAM_COSTS", {"nmap": 2}):
            with patch("handlers.equipment.MAX_RAM", 10):
                from handlers.equipment import handle_equip
                success, _, _, continue_loop = handle_equip("/equip nmap")

                self.assertTrue(success)
                self.assertNotIn("nmap", mock_state.selected_tools)


# ── Mermaid Handler ───────────────────────────────────────────
class TestMermaidHandler(unittest.TestCase):
    """Tests for /mermaid command handler."""

    @patch("handlers.mermaid.console")
    def test_mermaid_no_args(self, mock_console):
        from handlers.mermaid import handle_mermaid
        success, _, _, continue_loop = handle_mermaid("/mermaid")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.mermaid.console")
    def test_mermaid_list(self, mock_console):
        from handlers.mermaid import handle_mermaid
        success, _, _, continue_loop = handle_mermaid("/mermaid list")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.mermaid.get_state")
    @patch("handlers.mermaid.console")
    def test_mermaid_show_valid(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.mermaid_views = 0
        mock_get_state.return_value = mock_state

        from handlers.mermaid import handle_mermaid
        success, _, _, continue_loop = handle_mermaid("/mermaid show sqli")

        self.assertTrue(success)
        self.assertEqual(mock_state.mermaid_views, 1)

    @patch("handlers.mermaid.get_state")
    @patch("handlers.mermaid.console")
    def test_mermaid_show_invalid(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state

        from handlers.mermaid import handle_mermaid
        success, _, _, continue_loop = handle_mermaid("/mermaid show nonexistent")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.mermaid.console")
    def test_mermaid_show_no_topic(self, mock_console):
        from handlers.mermaid import handle_mermaid
        success, _, _, continue_loop = handle_mermaid("/mermaid show")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.mermaid.console")
    def test_mermaid_generate_no_topic(self, mock_console):
        from handlers.mermaid import handle_mermaid
        success, _, _, continue_loop = handle_mermaid("/mermaid generate")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.mermaid.console")
    def test_mermaid_unknown_subcommand(self, mock_console):
        from handlers.mermaid import handle_mermaid
        success, _, _, continue_loop = handle_mermaid("/mermaid unknown")

        self.assertTrue(success)
        mock_console.print.assert_called()


# ── Mindmap Handler ───────────────────────────────────────────
class TestMindmapHandler(unittest.TestCase):
    """Tests for /mindmap command handler."""

    @patch("handlers.mindmap.console")
    def test_mindmap_full_tree(self, mock_console):
        from handlers.mindmap import handle_mindmap
        response, should_continue = handle_mindmap("/mindmap")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.mindmap.console")
    def test_mindmap_specific_topic(self, mock_console):
        from handlers.mindmap import handle_mindmap
        response, should_continue = handle_mindmap("/mindmap Web Security")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.mindmap.console")
    def test_mindmap_help(self, mock_console):
        from handlers.mindmap import handle_mindmap
        response, should_continue = handle_mindmap("/mindmap help")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    def test_build_ascii_tree_no_cycles(self):
        from handlers.mindmap import _build_ascii_tree
        tree = _build_ascii_tree("CyberSecurity")
        self.assertIn("Network Security", tree)
        self.assertIn("Web Security", tree)


if __name__ == "__main__":
    unittest.main()
