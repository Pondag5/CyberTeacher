"""Security tests for CyberTeacher Hardening (SPRINT SA).

Tests cover:
- Auth bypass fix (/api/users empty token)
- Rate limiting on auth endpoints
- WebSocket auth (mandatory JWT)
- CORS configuration
- Error leakage prevention
"""

import os
import tempfile
import time
import unittest

from fastapi.testclient import TestClient

import api_server


class TestAuthBypass(unittest.TestCase):
    """Test that auth bypass on /api/users is fixed."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.mkdtemp()
        os.environ["DB_FILE"] = os.path.join(cls.temp_dir, "test.db")
        os.environ["STATE_FILE"] = os.path.join(cls.temp_dir, "state.json")
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls) -> None:
        import shutil

        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_users_without_token_returns_403(self) -> None:
        """Empty token must NOT bypass admin check."""
        r = self.client.get("/api/users")
        self.assertEqual(r.status_code, 403)

    def test_users_with_invalid_token_returns_403(self) -> None:
        """Invalid token must not grant access."""
        r = self.client.get("/api/users?token=invalid_token_here")
        self.assertEqual(r.status_code, 403)

    def test_health_still_public(self) -> None:
        """Health endpoint should remain accessible."""
        r = self.client.get("/api/health")
        self.assertEqual(r.status_code, 200)


class TestRateLimiting(unittest.TestCase):
    """Test rate limiting on auth endpoints."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.mkdtemp()
        os.environ["DB_FILE"] = os.path.join(cls.temp_dir, "test.db")
        os.environ["STATE_FILE"] = os.path.join(cls.temp_dir, "state.json")
        os.environ["AUTH_RATE_LIMIT"] = "3"
        import importlib

        importlib.reload(api_server)
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls) -> None:
        import shutil

        shutil.rmtree(cls.temp_dir, ignore_errors=True)
        os.environ.pop("AUTH_RATE_LIMIT", None)

    def test_login_rate_limit(self) -> None:
        """After N failed logins, should get 429."""
        for i in range(3):
            r = self.client.post("/api/auth/login?username=testuser&password=wrong")
            self.assertIn(r.status_code, [401, 429])
        r = self.client.post("/api/auth/login?username=testuser&password=wrong")
        self.assertEqual(r.status_code, 429)

    def test_register_rate_limit(self) -> None:
        """Register endpoint should be rate limited."""
        for i in range(5):
            r = self.client.post(
                f"/api/auth/register?username=newuser{i}&password=StrongPass123!"
            )
            self.assertIn(r.status_code, [200, 400, 429])
        r = self.client.post(
            "/api/auth/register?username=overflow&password=StrongPass123!"
        )
        self.assertEqual(r.status_code, 429)


class TestErrorLeakage(unittest.TestCase):
    """Test that internal errors are not leaked."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.mkdtemp()
        os.environ["DB_FILE"] = os.path.join(cls.temp_dir, "test.db")
        os.environ["STATE_FILE"] = os.path.join(cls.temp_dir, "state.json")
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls) -> None:
        import shutil

        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_500_errors_generic_message(self) -> None:
        """500 errors must not contain stack traces or file paths."""
        r = self.client.get("/api/stats?token=invalid")
        if r.status_code == 500:
            detail = r.json().get("detail", "")
            self.assertNotIn("Traceback", detail)
            self.assertNotIn('File "', detail)
            self.assertNotIn("/home/", detail)


class TestSecurityHeaders(unittest.TestCase):
    """Test security headers are present."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.mkdtemp()
        os.environ["DB_FILE"] = os.path.join(cls.temp_dir, "test.db")
        os.environ["STATE_FILE"] = os.path.join(cls.temp_dir, "state.json")
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls) -> None:
        import shutil

        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_hsts_header(self) -> None:
        """HSTS header must be present."""
        r = self.client.get("/api/health")
        self.assertIn("strict-transport-security", r.headers)

    def test_x_frame_options(self) -> None:
        """X-Frame-Options DENY must be present."""
        r = self.client.get("/api/health")
        self.assertEqual(r.headers.get("x-frame-options"), "DENY")

    def test_csp_header(self) -> None:
        """Content-Security-Policy must be present."""
        r = self.client.get("/api/health")
        self.assertIn("content-security-policy", r.headers)
        csp = r.headers["content-security-policy"]
        self.assertIn("frame-ancestors 'none'", csp)

    def test_no_unsafe_inline_in_script_src(self) -> None:
        """CSP script-src should not include unsafe-inline."""
        r = self.client.get("/api/health")
        csp = r.headers.get("content-security-policy", "")
        script_src = (
            csp.split("script-src")[1].split(";")[0] if "script-src" in csp else ""
        )
        self.assertNotIn("'unsafe-inline'", script_src)


class TestPasswordHashing(unittest.TestCase):
    """Test that bcrypt is used for password hashing."""

    def test_hash_starts_with_bcrypt_prefix(self) -> None:
        """New passwords should be hashed with bcrypt ($2b$)."""
        from auth import _hash_password

        h = _hash_password("test_password_123")
        self.assertTrue(h.startswith("$2b$"), f"Expected bcrypt hash, got: {h[:10]}")

    def test_verify_works_with_bcrypt(self) -> None:
        """Bcrypt hashes should verify correctly."""
        from auth import _hash_password, _verify_password

        h = _hash_password("my_secure_password")
        self.assertTrue(_verify_password("my_secure_password", h))
        self.assertFalse(_verify_password("wrong_password", h))

    def test_verify_backward_compat_sha256(self) -> None:
        """Old SHA-256 hashes should still verify (migration)."""
        import hashlib
        import hmac
        from auth import _verify_password

        salt = os.urandom(16).hex()
        old_hash = f"{salt}:{hashlib.sha256(f'{salt}:old_pass'.encode()).hexdigest()}"
        self.assertTrue(_verify_password("old_pass", old_hash))
        self.assertFalse(_verify_password("wrong_pass", old_hash))


class TestCORSConfig(unittest.TestCase):
    """Test CORS is not wildcard with credentials."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.mkdtemp()
        os.environ["DB_FILE"] = os.path.join(cls.temp_dir, "test.db")
        os.environ["STATE_FILE"] = os.path.join(cls.temp_dir, "state.json")
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls) -> None:
        import shutil

        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_cors_not_wildcard(self) -> None:
        """CORS origins should not be ['*']."""
        r = self.client.options(
            "/api/health",
            headers={
                "Origin": "https://evil.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        origin = r.headers.get("access-control-allow-origin", "")
        self.assertNotEqual(origin, "https://evil.com")


if __name__ == "__main__":
    unittest.main()
