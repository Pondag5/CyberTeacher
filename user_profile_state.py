"""
User profile and persona state management.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from utils.security import decrypt_value as _decrypt, encrypt_value as _encrypt


class UserProfileState(BaseModel):
    """User profile, reputation, and persona configuration."""
    
    # Профиль пользователя (G-09)
    username: str = Field(default="Аноним")
    avatar: str = Field(default="🧑‍💻")

    # Репутация / хэндлы (L-10)
    reputation: int = Field(default=0, ge=0)
    handle: str = Field(default="Новичок")
    
    HANDLES: List[tuple] = Field(default_factory=lambda: [
        (0, "Новичок"), (50, "Script Kiddie"), (150, "Хакер"),
        (300, "Пентестер"), (500, "Эксперт"), (800, "Призрак"),
        (1200, "Легенда"), (2000, "Фантом"),
    ])

    # HackTheBox (M-25)
    htb_email: Optional[str] = None
    htb_password: Optional[str] = None
    htb_completed: List[int] = Field(default_factory=list)

    # Persona
    current_persona: str = Field(default="teacher")
    current_mode: str = Field(default="teacher")

    def _update_handle(self) -> None:
        """Обновить хэндл на основе репутации."""
        handle = "Новичок"
        for threshold, name in self.HANDLES:
            if self.reputation >= threshold:
                handle = name
        self.handle = handle

    def add_reputation(self, amount: int) -> None:
        """Добавить очки репутации и обновить хэндл."""
        self.reputation = max(0, self.reputation + amount)
        self._update_handle()

    def get_handle(self) -> str:
        """Получить текущий хэндл."""
        self._update_handle()
        return self.handle

    def get_htb_password_encrypted(self) -> Optional[str]:
        """Get encrypted HTB password for storage."""
        if self.htb_password:
            return _encrypt(self.htb_password)
        return None

    def set_htb_password_from_encrypted(self, encrypted: Optional[str]) -> None:
        """Set HTB password from encrypted value."""
        if encrypted:
            self.htb_password = _decrypt(encrypted)
        else:
            self.htb_password = None

    model_config = {"validate_assignment": True}