"""
User profile and persona state management.
"""

from typing import Any

from pydantic import BaseModel, Field

from utils.security import decrypt_value as _decrypt
from utils.security import encrypt_value as _encrypt


class UserProfileState(BaseModel):
    """User profile, reputation, and persona configuration."""
    
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
    htb_email: str | None = None
    htb_password: str | None = None
    htb_completed: list[int] = Field(default_factory=list)

    # Persona
    current_persona: str = Field(default="teacher")
    current_mode: str = Field(default="teacher")

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