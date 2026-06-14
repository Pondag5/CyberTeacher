"""
User profile and reputation management.
"""

from typing import Any

from pydantic import BaseModel, Field

from utils.security import decrypt_value as _decrypt
from utils.security import encrypt_value as _encrypt


class UserState(BaseModel):
    """User profile and reputation data."""

    username: str = Field(default="Аноним")
    avatar: str = Field(default="🧑‍💻")
    reputation: int = Field(default=0, ge=0)
    handle: str = Field(default="Новичок")

    HANDLES: list[tuple[int, str]] = Field(
        default_factory=lambda: [
            (0, "Новичок"),
            (50, "Script Kiddie"),
            (150, "Хакер"),
            (300, "Пентестер"),
            (500, "Эксперт"),
            (800, "Призрак"),
            (1200, "Легенда"),
            (2000, "Фантом"),
        ]
    )

    # HackTheBox (M-25)
    htb_token: str | None = None
    htb_email: str | None = None
    htb_password: str | None = None
    htb_completed: list[int] = Field(default_factory=list)

    # TryHackMe (G-01)
    thm_username: str | None = None
    thm_rooms_cache: dict[str, Any] = Field(default_factory=dict)
    thm_completed: list[int] = Field(default_factory=list)
    thm_points: int = Field(default=0, ge=0)
    thm_level: int = Field(default=1, ge=1)
    thm_rank: str = Field(default="Новичок")

    # Versus mode (NEW-01)
    versus_active: bool = False
    versus_scenario: str | None = None
    versus_attempts: int = Field(default=0, ge=0)
    versus_history: list[dict[str, str]] = Field(default_factory=list)

    # Sync (M-20)
    sync_id: str | None = None

    # Theme (dup, but let it be)
    current_theme: str = Field(default="default")

    def _update_handle(self) -> None:
        handle = "Новичок"
        for threshold, name in self.HANDLES:
            if self.reputation >= threshold:
                handle = name
        self.handle = handle

    def add_reputation(self, amount: int) -> None:
        self.reputation = max(0, self.reputation + amount)
        self._update_handle()

    def get_handle(self) -> str:
        self._update_handle()
        return self.handle

    def get_htb_password_encrypted(self) -> str | None:
        if self.htb_password:
            return _encrypt(self.htb_password)
        return None

    def set_htb_password_from_encrypted(self, encrypted: str | None) -> None:
        if encrypted:
            self.htb_password = _decrypt(encrypted)
        else:
            self.htb_password = None

    model_config = {"validate_assignment": True}