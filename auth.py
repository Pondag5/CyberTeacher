"""Auth system — user registration, login, JWT tokens, roles.

Multi-user support with:
- Password hashing (bcrypt, backward-compat with SHA-256 salted)
- JWT tokens (HMAC-SHA256)
- Role-based access: admin / teacher / student
- User CRUD operations
"""

import base64
import hashlib
import hmac
import json
import logging
import os
import secrets
import time
from typing import Any, Dict, List, Optional

import bcrypt


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
    }
    users[username_lower] = user
    _save_users(users)
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "role": user["role"],
    }


def authenticate(username: str, password: str) -> Dict[str, Any]:
    """Authenticate user. Returns token or error."""
    users = _load_users()
    user = users.get(username.lower().strip())

    if not user:
        return {"error": "User not found"}
    if not _verify_password(password, user["password_hash"]):
        return {"error": "Invalid password"}

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
            return {k: v for k, v in user.items() if k != "password_hash"}
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
    """List all users (without password hashes)."""
    users = _load_users()
    return [
        {k: v for k, v in u.items() if k != "password_hash"} for u in users.values()
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
