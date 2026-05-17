"""
Tests for htb, walkthroughs, exploit_submit, code_scan, and docker_gen handlers.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# ── HTB Handler ───────────────────────────────────────────────
class TestHTBHandler(unittest.TestCase):
    """Tests for /htb command handler."""

    @patch("handlers.htb.console")
    def test_htb_no_args_shows_help(self, mock_console):
        from handlers.htb import handle_htb
        success, _, _, continue_loop = handle_htb("/htb")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.htb.console")
    def test_htb_unknown_subcommand(self, mock_console):
        from handlers.htb import handle_htb
        success, _, _, continue_loop = handle_htb("/htb unknown")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.htb.console")
    def test_htb_login_no_args(self, mock_console):
        from handlers.htb import handle_htb_login
        success, _, _, continue_loop = handle_htb_login("/htb login")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.htb.console")
    @patch("handlers.htb.requests.Session")
    def test_htb_login_success(self, mock_session_cls, mock_console):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"success": True}
        mock_session = MagicMock()
        mock_session.post.return_value = mock_resp
        mock_session_cls.return_value = mock_session

        from handlers.htb import handle_htb_login
        with patch("handlers.htb.get_context") as mock_get_context:
            mock_state = MagicMock()
            mock_ctx = MagicMock()
            mock_ctx.state = mock_state
            mock_get_context.return_value = mock_ctx

            success, _, _, continue_loop = handle_htb_login("/htb login test@test.com pass123")

            self.assertTrue(success)
            self.assertEqual(mock_state.htb_email, "test@test.com")

    @patch("handlers.htb.console")
    def test_htb_machines_no_type(self, mock_console):
        from handlers.htb import handle_htb_machines
        with patch("handlers.htb._get_htb_session") as mock_session:
            mock_session.side_effect = Exception("No credentials")
            success, _, _, continue_loop = handle_htb_machines("/htb machines")

            self.assertTrue(success)

    @patch("handlers.htb.console")
    def test_htb_machine_no_id(self, mock_console):
        from handlers.htb import handle_htb_machine
        success, _, _, continue_loop = handle_htb_machine("/htb machine")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.htb.console")
    def test_htb_machine_invalid_id(self, mock_console):
        from handlers.htb import handle_htb_machine
        success, _, _, continue_loop = handle_htb_machine("/htb machine abc")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.htb.console")
    def test_htb_submit_no_args(self, mock_console):
        from handlers.htb import handle_htb_submit
        success, _, _, continue_loop = handle_htb_submit("/htb submit")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.htb.console")
    def test_htb_submit_invalid_id(self, mock_console):
        from handlers.htb import handle_htb_submit
        success, _, _, continue_loop = handle_htb_submit("/htb submit abc flag123")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.htb.console")
    @patch("handlers.htb.get_context")
    def test_htb_status(self, mock_get_context, mock_console):
        mock_state = MagicMock()
        mock_state.htb_completed = [1, 2, 3]
        mock_state.htb_email = "test@test.com"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers.htb import handle_htb_status
        success, _, _, continue_loop = handle_htb_status("/htb status")

        self.assertTrue(success)
        mock_console.print.assert_called()


# ── Walkthroughs Handler ──────────────────────────────────────
class TestWalkthroughsHandler(unittest.TestCase):
    """Tests for /walkthrough and /exploit commands."""

    @patch("handlers.walkthroughs.console")
    def test_walkthrough_no_topic(self, mock_console):
        from handlers.walkthroughs import handle_walkthrough
        success, _, _, continue_loop = handle_walkthrough("/walkthrough")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.walkthroughs.console")
    def test_exploit_no_query(self, mock_console):
        from handlers.walkthroughs import handle_exploit_search
        success, _, _, continue_loop = handle_exploit_search("/exploit")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.walkthroughs.console")
    @patch("handlers.walkthroughs._fetch_cve")
    @patch("handlers.walkthroughs._cve_cache")
    def test_exploit_cve_not_found(self, mock_cache, mock_fetch, mock_console):
        mock_cache.get.return_value = None
        mock_fetch.return_value = None

        from handlers.walkthroughs import handle_exploit_search
        success, _, _, continue_loop = handle_exploit_search("/exploit CVE-2024-9999")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.walkthroughs.console")
    def test_exploit_non_cve_query(self, mock_console):
        from handlers.walkthroughs import handle_exploit_search
        success, _, _, continue_loop = handle_exploit_search("/exploit buffer overflow")

        self.assertTrue(success)
        mock_console.print.assert_called()


# ── Exploit Submit Handler ────────────────────────────────────
class TestExploitSubmitHandler(unittest.TestCase):
    """Tests for /exploit_submit command."""

    @patch("handlers.exploit_submit.console")
    def test_exploit_submit_no_args(self, mock_console):
        from handlers.exploit_submit import handle_exploit_submit
        success, _, _, continue_loop = handle_exploit_submit("/exploit_submit")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.exploit_submit.console")
    def test_exploit_submit_invalid_step(self, mock_console):
        from handlers.exploit_submit import handle_exploit_submit
        success, _, _, continue_loop = handle_exploit_submit("/exploit_submit mission abc script.py")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.exploit_submit.console")
    def test_exploit_submit_file_not_found(self, mock_console):
        from handlers.exploit_submit import handle_exploit_submit
        success, _, _, continue_loop = handle_exploit_submit("/exploit_submit mission 1 nonexistent.py")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.exploit_submit.console")
    def test_exploit_submit_unsupported_ext(self, mock_console):
        import tempfile
        tmpdir = tempfile.mkdtemp()
        filepath = os.path.join(tmpdir, "test.cpp")
        with open(filepath, "w") as f:
            f.write("test")

        from handlers.exploit_submit import handle_exploit_submit
        success, _, _, continue_loop = handle_exploit_submit(f"/exploit_submit mission 1 {filepath}")

        self.assertTrue(success)
        mock_console.print.assert_called()
        os.unlink(filepath)
        os.rmdir(tmpdir)


# ── Code Scan Handler ─────────────────────────────────────────
class TestCodeScanHandler(unittest.TestCase):
    """Tests for /scan command."""

    @patch("handlers.code_scan.console")
    def test_code_scan_no_args(self, mock_console):
        from handlers.code_scan import handle_code_scan
        success, _, _, continue_loop = handle_code_scan("/scan")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    def test_scan_directory_no_secrets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "clean.py"), "w") as f:
                f.write("print('hello')\n")
            from handlers.code_scan import _scan_directory
            matches = _scan_directory(tmpdir)
            self.assertEqual(len(matches), 0)

    def test_scan_directory_finds_secret(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "config.py"), "w") as f:
                f.write("api_key = 'sk-abcdefghijklmnopqrstuvwxyz0123456789ABCDEF'\n")
            from handlers.code_scan import _scan_directory
            matches = _scan_directory(tmpdir)
            self.assertGreater(len(matches), 0)


# ── Docker Gen Handler ────────────────────────────────────────
class TestDockerGenHandler(unittest.TestCase):
    """Tests for /dockergen command."""

    @patch("handlers.docker_gen.console")
    def test_dockergen_no_args(self, mock_console):
        from handlers.docker_gen import handle_docker_gen
        success, _, _, continue_loop = handle_docker_gen("/dockergen")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.docker_gen.console")
    def test_dockergen_list(self, mock_console):
        from handlers.docker_gen import handle_docker_gen
        success, _, _, continue_loop = handle_docker_gen("/dockergen list")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.docker_gen.console")
    def test_dockergen_create_sqli(self, mock_console):
        from handlers.docker_gen import handle_docker_gen
        success, _, _, continue_loop = handle_docker_gen("/dockergen sqli")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.docker_gen.console")
    def test_dockergen_create_web(self, mock_console):
        from handlers.docker_gen import handle_docker_gen
        success, _, _, continue_loop = handle_docker_gen("/dockergen web")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.docker_gen.console")
    def test_dockergen_create_invalid(self, mock_console):
        from handlers.docker_gen import handle_docker_gen
        success, _, _, continue_loop = handle_docker_gen("/dockergen create nonexistent_lab")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.docker_gen.console")
    def test_dockergen_custom(self, mock_console):
        from handlers.docker_gen import handle_docker_gen
        success, _, _, continue_loop = handle_docker_gen("/dockergen custom mylab nginx:latest 8080:80")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.docker_gen.console")
    def test_dockergen_unknown_subcommand(self, mock_console):
        from handlers.docker_gen import handle_docker_gen
        success, _, _, continue_loop = handle_docker_gen("/dockergen unknown")

        self.assertTrue(success)
        mock_console.print.assert_called()


if __name__ == "__main__":
    unittest.main()
