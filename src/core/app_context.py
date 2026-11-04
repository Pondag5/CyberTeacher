"""
Контекст приложения (AppContext).
Инкапсулирует состояние, настройки и сервисы для реализации Dependency Injection.
"""

from typing import Any, Optional
from src.core.state import AppState, get_state
from src.core.settings import get_settings

class AppContext:
    """
    Класс-контейнер для всех основных подсистем CyberTeacher.
    Вместо обращения к глобальным get_state() / get_settings(),
    компоненты должны получать этот контекст.
    """
    def __init__(self, state: AppState, settings: Any):
        self.state = state
        self.settings = settings
        # Здесь в будущем можно инициализировать БД, LLM клиент и др.
        self.db = None
        self.services = {}

    @classmethod
    def create(cls) -> "AppContext":
        """Фабричный метод для создания контекста по умолчанию."""
        return cls(state=get_state(), settings=get_settings())

_context: Optional[AppContext] = None

def get_app_context() -> AppContext:
    """Получить глобальный синглтон контекста (для переходного периода)."""
    global _context
    if _context is None:
        _context = AppContext.create()
    return _context
