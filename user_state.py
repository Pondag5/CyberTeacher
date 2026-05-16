"""
User profile and reputation management.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from utils.security import decrypt_value as _decrypt, encrypt_value as _encrypt


@dataclass
class UserState:
    """User profile and reputation data."""
    
    # Профиль пользователя (G-09)
    username: str = "Аноним"
    avatar: str = "🧑‍💻"

    # Репутация / хэндлы (L-10)
    reputation: int = 0  # Очки репутации (отдельно от XP)
    handle: str = "Новичок"  # Хэндл/титул
    
    # HANDLES threshold definitions
    HANDLES: List[tuple] = field(default_factory=lambda: [
        (0, "Новичок"),
        (50, "Script Kiddie"),
        (150, "Хакер"),
        (300, "Пентестер"),
        (500, "Эксперт"),
        (800, "Призрак"),
        (1200, "Легенда"),
        (2000, "Фантом"),
    ])

    def _update_handle(self) -> None:
        """Обновить хэндл на основе репутации."""
        handle = "Новичок"
        for threshold, name in self.HANDLES:
            if self.reputation >= threshold:
                handle = name
        self.handle = handle

    def add_reputation(self, amount: int) -> None:
        """Добавить очки репутации и обновить хэндл."""
        self.reputation += amount
        self._update_handle()

    def get_handle(self) -> str:
        """Получить текущий хэндл."""
        self._update_handle()
        return self.handle

    # HackTheBox (M-25) integration
    htb_email: str | None = None
    htb_password: str | None = None
    htb_completed: List[int] = field(default_factory=list)  # список ID завершённых машин

    def get_htb_password_encrypted(self) -> str | None:
        """Get encrypted HTB password for storage."""
        if self.htb_password:
            return _encrypt(self.htb_password)
        return None

    def set_htb_password_from_encrypted(self, encrypted: str | None) -> None:
        """Set HTB password from encrypted value."""
        if encrypted:
            self.htb_password = _decrypt(encrypted)
        else:
            self.htb_password = None