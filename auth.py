"""Auth system — user registration, login, JWT tokens, roles, 2FA (TOTP).

Multi-user support with:
- Password hashing (bcrypt, backward-compat with SHA-256 salted)
- JWT tokens (HMAC-SHA256)
- Role-based access: admin / teacher / student
- User CRUD operations
- Two-factor authentication (TOTP) with backup codes
"""

import base64
import hashlib
import hmac
import io
import json
import logging
import os
import secrets
import time
from typing import Any, Dict, List, Optional

import bcrypt
import pyotp
import qrcode
from jose import jwt as jose_jwt
from oauthlib.oauth2 import WebApplicationClient
import requests


USERS_FILE = "./memory/users.json"
JWT_SECRET = os.getenv("CYBERTEACHER_JWT_SECRET", "")
if not JWT_SECRET:
    import secrets

    JWT_SECRET = secrets.token_hex(32)
    import logging

    logging.warning(
        "CYBERTEACHER_JWT_SECRET not set — generated random secret. "
        "Tokens will not survive restart. Set CYBERTEACHER_JWT_SECRET in .env."
    )
JWT_EXPIRY = 86400 * 7  # 7 days

ROLES = {"admin", "teacher", "student"}
ROLE_PERMISSIONS = {
    "admin": {
        "manage_users",
        "manage_courses",
        "view_all_stats",
        "manage_config",
        "chat",
        "quiz",
        "labs",
        "settings",
    },
    "teacher": {"manage_courses", "view_all_stats", "chat", "quiz", "labs"},
    "student": {"chat", "quiz", "labs", "profile"},
}


def _hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    h = bcrypt.hashpw(password.encode("utf-8"), salt)
    return h.decode("utf-8")


def _verify_password(password: str, stored: str) -> bool:
    try:
        if stored.startswith("$2"):
            return bcrypt.checkpw(password.encode("utf-8"), stored.encode("utf-8"))
        salt, h = stored.split(":", 1)
        return hmac.compare_digest(
            hashlib.sha256(f"{salt}:{password}".encode()).hexdigest(), h
        )
    except (ValueError, IndexError, KeyError):
        return False


def _load_users() -> Dict[str, Dict[str, Any]]:
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                result: Dict[str, Dict[str, Any]] = json.load(f)
                return result
    except (OSError, IOError, json.JSONDecodeError):
        pass
    return {}


def _save_users(users: Dict[str, Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def create_user(
    username: str, password: str, display_name: str = "", role: str = ""
) -> Dict[str, Any]:
    """Register a new user. First user ever gets admin role."""
    users = _load_users()
    username_lower = username.lower().strip()

    if username_lower in users:
        return {"error": "User already exists"}
    if len(username_lower) < 3:
        return {"error": "Username must be at least 3 characters"}
    if len(password) < 8:
        return {"error": "Password must be at least 8 characters"}
    # First user is admin, rest are student
    if not role or role not in ROLES:
        role = "admin" if not users else "student"

    user = {
        "username": username_lower,
        "display_name": display_name or username,
        "password_hash": _hash_password(password),
        "avatar": "🧑‍💻",
        "created_at": time.time(),
        "role": role,
        "user_id": f"user_{username_lower}",
        "totp_enabled": False,
        "totp_secret": None,
        "backup_codes": [],
        "oauth_links": [],
    }
    users[username_lower] = user
    _save_users(users)
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "role": user["role"],
    }


def authenticate(
    username: str, password: str, totp_code: Optional[str] = None
) -> Dict[str, Any]:
    """Authenticate user. Returns token or 2fa_required flag."""
    users = _load_users()
    user = users.get(username.lower().strip())

    if not user:
        return {"error": "User not found"}
    if not _verify_password(password, user["password_hash"]):
        return {"error": "Invalid password"}

    # If TOTP is enabled, require a valid TOTP/backup code
    if user.get("totp_enabled"):
        if not totp_code:
            return {
                "2fa_required": True,
                "user_id": user["user_id"],
                "username": user["username"],
                "display_name": user.get("display_name", user["username"]),
                "avatar": user.get("avatar", "🧑‍💻"),
                "role": user.get("role", "student"),
            }
        if not verify_totp_or_backup(username, totp_code):
            return {"error": "Invalid 2FA code"}

    token = _create_token(
        user["user_id"], user["username"], user.get("role", "student")
    )
    return {
        "token": token,
        "user_id": user["user_id"],
        "username": user["username"],
        "display_name": user.get("display_name", user["username"]),
        "avatar": user.get("avatar", "🧑‍💻"),
        "role": user.get("role", "student"),
    }


def _create_token(user_id: str, username: str, role: str = "student") -> str:
    header = json.dumps({"alg": "HS256", "typ": "JWT"})
    payload = json.dumps(
        {
            "user_id": user_id,
            "username": username,
            "role": role,
            "exp": int(time.time()) + JWT_EXPIRY,
            "iat": int(time.time()),
        }
    )
    import base64

    h = base64.urlsafe_b64encode(header.encode()).decode().rstrip("=")
    p = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    sig = hmac.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).hexdigest()
    return f"{h}.{p}.{sig}"


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode JWT token."""
    try:
        import base64

        parts = token.split(".")
        if len(parts) != 3:
            return None
        h, p, sig = parts

        expected_sig = hmac.new(
            JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None

        padding = 4 - len(p) % 4
        if padding != 4:
            p += "=" * padding
        payload = json.loads(base64.urlsafe_b64decode(p))

        if payload.get("exp", 0) < time.time():
            return None

        result: Optional[Dict[str, Any]] = payload
        return result
    except (ValueError, KeyError, json.JSONDecodeError, IndexError, TypeError):
        return None


def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    users = _load_users()
    for user in users.values():
        if user.get("user_id") == user_id:
            return {
                k: v
                for k, v in user.items()
                if k not in ("password_hash", "totp_secret", "oauth_links")
            }
    return None


def update_user(user_id: str, **kwargs: Any) -> bool:
    users = _load_users()
    for user in users.values():
        if user.get("user_id") == user_id:
            for k, v in kwargs.items():
                if k not in ("user_id", "password_hash", "created_at"):
                    user[k] = v
            _save_users(users)
            return True
    return False


def set_role(user_id: str, role: str) -> bool:
    """Set user role. Only admin can do this."""
    if role not in ROLES:
        return False
    return update_user(user_id, role=role)


def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
    """Get user info from JWT token."""
    payload = verify_token(token)
    if not payload:
        return None
    return get_user(payload.get("user_id", ""))


def list_users() -> List[Dict[str, Any]]:
    """List all users (without password hashes, TOTP secrets, or OAuth links)."""
    users = _load_users()
    return [
        {k: v for k, v in u.items() if k not in ("password_hash", "totp_secret", "oauth_links")}
        for u in users.values()
    ]


def has_permission(token: str, permission: str) -> bool:
    """Check if a token has a specific permission."""
    payload = verify_token(token)
    if not payload:
        return False
    role = payload.get("role", "student")
    perms = ROLE_PERMISSIONS.get(role, set())
    return permission in perms


def get_user_role(token: str) -> str:
    """Get user role from token."""
    payload = verify_token(token)
    return payload.get("role", "student") if payload else "guest"


# =============================================================================
# Two-Factor Authentication (TOTP)
# =============================================================================

TOTP_ISSUER = "CyberTeacher"


def generate_totp_secret() -> str:
    """Generate a new random TOTP secret (base32)."""
    return pyotp.random_base32()


def get_totp_provisioning_url(username: str, secret: str) -> str:
    """Build otpauth:// provisioning URL for QR code."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=TOTP_ISSUER)


def generate_totp_qr_code(provisioning_url: str) -> str:
    """Generate QR code PNG as base64 data URL."""
    img = qrcode.make(provisioning_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def verify_totp_code(secret: str, code: str) -> bool:
    """Verify a TOTP code against the secret."""
    try:
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)
    except Exception:
        return False


def generate_backup_codes(count: int = 8) -> List[str]:
    """Generate single-use backup codes."""
    return [secrets.token_hex(4).upper() for _ in range(count)]


def hash_backup_code(code: str) -> str:
    """Hash a backup code for storage (bcrypt)."""
    return bcrypt.hashpw(code.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_backup_code(stored_hash: str, code: str) -> bool:
    """Verify a backup code against its stored hash."""
    try:
        return bcrypt.checkpw(code.encode("utf-8"), stored_hash.encode("utf-8"))
    except Exception:
        return False


def enable_totp_for_user(username: str, secret: str, backup_codes: List[str]) -> Dict[str, Any]:
    """Enable TOTP for a user. Stores secret and hashed backup codes."""
    users = _load_users()
    user = users.get(username.lower().strip())
    if not user:
        return {"error": "User not found"}

    user["totp_secret"] = secret
    user["totp_enabled"] = True
    user["backup_codes"] = [
        {"code": code, "hash": hash_backup_code(code), "used": False}
        for code in backup_codes
    ]
    _save_users(users)
    return {
        "username": user["username"],
        "totp_enabled": True,
        "backup_codes": [c["code"] for c in user["backup_codes"]],
    }


def disable_totp_for_user(username: str) -> bool:
    """Disable TOTP for a user."""
    users = _load_users()
    user = users.get(username.lower().strip())
    if not user:
        return False
    user.pop("totp_secret", None)
    user["totp_enabled"] = False
    user.pop("backup_codes", None)
    _save_users(users)
    return True


def get_totp_status(username: str) -> Dict[str, Any]:
    """Get TOTP status for a user (without exposing secret)."""
    users = _load_users()
    user = users.get(username.lower().strip())
    if not user:
        return {"error": "User not found"}
    return {
        "username": user["username"],
        "totp_enabled": bool(user.get("totp_enabled", False)),
        "backup_codes_remaining": sum(
            1 for c in user.get("backup_codes", []) if not c.get("used", False)
        ),
    }


def consume_backup_code(username: str, code: str) -> bool:
    """Verify and mark a backup code as used. Returns True if valid and unused."""
    users = _load_users()
    user = users.get(username.lower().strip())
    if not user:
        return False

    for bc in user.get("backup_codes", []):
        if not bc.get("used", False) and verify_backup_code(bc["hash"], code):
            bc["used"] = True
            _save_users(users)
            return True
    return False


def verify_totp_or_backup(username: str, code: str) -> bool:
    """Verify a TOTP code or a backup code for a user."""
    users = _load_users()
    user = users.get(username.lower().strip())
    if not user:
        return False

    secret = user.get("totp_secret")
    if secret and verify_totp_code(secret, code):
        return True

    return consume_backup_code(username, code)


# =============================================================================
# OAuth2 (Google, GitHub)
# =============================================================================

OAUTH_PROVIDERS: Dict[str, Dict[str, str]] = {
    "google": {
        "client_id": os.getenv("GOOGLE_OAUTH_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", ""),
        "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
        "scope": "openid email profile",
    },
    "github": {
        "client_id": os.getenv("GITHUB_OAUTH_CLIENT_ID", ""),
        "client_secret": os.getenv("GITHUB_OAUTH_CLIENT_SECRET", ""),
        "authorize_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo_url": "https://api.github.com/user",
        "scope": "read:user user:email",
    },
}


def get_oauth_provider(provider: str) -> Optional[Dict[str, str]]:
    """Return OAuth provider config or None if not configured."""
    cfg = OAUTH_PROVIDERS.get(provider.lower())
    if not cfg:
        return None
    if not cfg["client_id"] or not cfg["client_secret"]:
        return None
    return cfg


def oauth_authorize_url(provider: str, redirect_uri: str, state: str) -> Optional[str]:
    """Build OAuth authorization URL for the given provider."""
    cfg = get_oauth_provider(provider)
    if not cfg:
        return None
    client = WebApplicationClient(cfg["client_id"])
    url = client.prepare_request_uri(
        cfg["authorize_url"],
        redirect_uri=redirect_uri,
        scope=cfg["scope"],
        state=state,
        access_type="offline",
        prompt="consent",
    )
    return url


def oauth_exchange_code(
    provider: str, code: str, redirect_uri: str
) -> Optional[Dict[str, Any]]:
    """Exchange authorization code for access token."""
    cfg = get_oauth_provider(provider)
    if not cfg:
        return None
    client = WebApplicationClient(cfg["client_id"])
    token_url, headers, body = client.prepare_token_request(
        cfg["token_url"],
        authorization_response="",
        redirect_url=redirect_uri,
        code=code,
    )
    try:
        resp = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(cfg["client_id"], cfg["client_secret"]),
            timeout=10,
        )
        resp.raise_for_status()
        token_data = client.parse_request_body_response(resp.text)
        return token_data
    except Exception:
        return None


def oauth_get_userinfo(
    provider: str, token_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Fetch user info from OAuth provider using access token."""
    cfg = get_oauth_provider(provider)
    if not cfg:
        return None
    access_token = token_data.get("access_token")
    if not access_token:
        return None
    try:
        resp = requests.get(
            cfg["userinfo_url"],
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        if provider.lower() == "google":
            return {
                "provider_user_id": data.get("id", ""),
                "email": data.get("email", ""),
                "name": data.get("name", ""),
                "picture": data.get("picture", ""),
                "verified_email": data.get("verified_email", False),
            }
        elif provider.lower() == "github":
            emails = []
            try:
                eresp = requests.get(
                    "https://api.github.com/user/emails",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=10,
                )
                if eresp.ok:
                    emails = eresp.json()
            except Exception:
                pass
            primary_email = ""
            for e in emails:
                if e.get("primary"):
                    primary_email = e.get("email", "")
                    break
            return {
                "provider_user_id": str(data.get("id", "")),
                "email": primary_email or data.get("email", ""),
                "name": data.get("name") or data.get("login", ""),
                "picture": data.get("avatar_url", ""),
                "verified_email": bool(primary_email),
            }
        return None
    except Exception:
        return None


def get_or_create_oauth_user(
    provider: str, provider_user_id: str, email: str, name: str, picture: str = ""
) -> Dict[str, Any]:
    """Find existing user by OAuth link or email, or create new user."""
    users = _load_users()
    username_lower = email.split("@")[0].lower().strip() if email else ""

    # 1. Look for existing OAuth link
    for user in users.values():
        oauth_links = user.get("oauth_links", [])
        for link in oauth_links:
            if (
                link.get("provider") == provider.lower()
                and link.get("provider_user_id") == provider_user_id
            ):
                return {
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "display_name": user.get("display_name", user["username"]),
                    "avatar": user.get("avatar", "🧑‍💻"),
                    "role": user.get("role", "student"),
                    "linked": True,
                }

    # 2. Look for existing user by email
    for user in users.values():
        if user.get("email", "").lower() == email.lower():
            if "oauth_links" not in user:
                user["oauth_links"] = []
            user["oauth_links"].append(
                {
                    "provider": provider.lower(),
                    "provider_user_id": provider_user_id,
                    "email": email,
                    "linked_at": time.time(),
                }
            )
            _save_users(users)
            return {
                "user_id": user["user_id"],
                "username": user["username"],
                "display_name": user.get("display_name", user["username"]),
                "avatar": user.get("avatar", "🧑‍💻"),
                "role": user.get("role", "student"),
                "linked": True,
            }

    # 3. Create new user
    if not username_lower or len(username_lower) < 3:
        username_lower = f"oauth_{provider}_{provider_user_id}"[:20]
    base = username_lower
    counter = 1
    while username_lower in users:
        username_lower = f"{base}{counter}"
        counter += 1

    user = {
        "username": username_lower,
        "display_name": name or username_lower,
        "password_hash": "",
        "email": email,
        "avatar": picture or "🧑‍💻",
        "created_at": time.time(),
        "role": "admin" if not users else "student",
        "user_id": f"user_{username_lower}",
        "totp_enabled": False,
        "totp_secret": None,
        "backup_codes": [],
        "oauth_links": [
            {
                "provider": provider.lower(),
                "provider_user_id": provider_user_id,
                "email": email,
                "linked_at": time.time(),
            }
        ],
    }
    users[username_lower] = user
    _save_users(users)
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "avatar": user["avatar"],
        "role": user["role"],
        "linked": False,
    }


def link_oauth_to_user(
    username: str, provider: str, provider_user_id: str, email: str
) -> bool:
    """Link an OAuth account to an existing user."""
    users = _load_users()
    user = users.get(username.lower().strip())
    if not user:
        return False
    if "oauth_links" not in user:
        user["oauth_links"] = []
    for link in user["oauth_links"]:
        if link.get("provider") == provider.lower():
            return False
    user["oauth_links"].append(
        {
            "provider": provider.lower(),
            "provider_user_id": provider_user_id,
            "email": email,
            "linked_at": time.time(),
        }
    )
    _save_users(users)
    return True


def unlink_oauth_from_user(username: str, provider: str) -> bool:
    """Unlink an OAuth account from a user."""
    users = _load_users()
    user = users.get(username.lower().strip())
    if not user:
        return False
    oauth_links = user.get("oauth_links", [])
    user["oauth_links"] = [
        l for l in oauth_links if l.get("provider") != provider.lower()
    ]
    _save_users(users)
    return True


def get_oauth_links(username: str) -> List[Dict[str, Any]]:
    """List OAuth links for a user (without sensitive data)."""
    users = _load_users()
    user = users.get(username.lower().strip())
    if not user:
        return []
    links = user.get("oauth_links", [])
    return [
        {
            "provider": l.get("provider"),
            "email": l.get("email"),
            "linked_at": l.get("linked_at"),
        }
        for l in links
    ]


def oauth_create_token(user_id: str, username: str, role: str = "student") -> str:
    """Create JWT token (reuses HS256 signing)."""
    return _create_token(user_id, username, role)

