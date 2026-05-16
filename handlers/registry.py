"""Registry pattern для команд (рефакторинг core.py).

Централизованная регистрация обработчиков команд.
"""

from typing import Any, Callable, Dict, Tuple

CommandHandler = Callable[[str, Any, Any], Tuple[bool, Any, Any, bool]]


class CommandRegistry:
    """Реестр команд с поддержкой префиксов и точных совпадений."""

    def __init__(self):
        self._exact: Dict[str, CommandHandler] = {}
        self._prefix: Dict[str, CommandHandler] = {}

    def register_exact(self, command: str):
        """Декоратор для регистрации точной команды."""
        def decorator(func: CommandHandler):
            self._exact[command] = func
            return func
        return decorator

    def register_prefix(self, prefix: str):
        """Декоратор для регистрации команды с префиксом."""
        def decorator(func: CommandHandler):
            self._prefix[prefix] = func
            return func
        return decorator

    def get_handler(self, action: str) -> Tuple[CommandHandler, str]:
        """Найти обработчик для действия.

        Returns:
            Tuple[handler, remaining_args] или (None, action) если не найдено.
        """
        # Точное совпадение
        if action in self._exact:
            return self._exact[action], ""

        # Префиксное совпадение
        for prefix, handler in self._prefix.items():
            if action.startswith(prefix):
                remaining = action[len(prefix):].strip()
                return handler, remaining

        return None, action

    def list_commands(self) -> Dict[str, str]:
        """Список всех зарегистрированных команд."""
        commands = {}
        for cmd in self._exact:
            commands[cmd] = "exact"
        for prefix in self._prefix:
            commands[prefix] = "prefix"
        return commands


# Глобальный экземпляр
registry = CommandRegistry()


# Регистрация новых команд (L-03, L-14, H-16)
@registry.register_prefix("mindmap")
def _mindmap_handler(action: str, llm: Any, conn: Any) -> Tuple[bool, Any, Any, bool]:
    from handlers.mindmap import handle_mindmap
    response, should_continue = handle_mindmap(action)
    # handle_mindmap returns (response_string, bool) -> convert to (bool, None, None, bool)
    return True, None, None, should_continue


@registry.register_prefix("export extended")
def _export_extended_handler(action: str, llm: Any, conn: Any) -> Tuple[bool, Any, Any, bool]:
    from handlers.export_extended import handle_export_extended
    response, should_continue = handle_export_extended(action)
    return True, None, None, should_continue


@registry.register_prefix("async")
def _async_handler(action: str, llm: Any, conn: Any) -> Tuple[bool, Any, Any, bool]:
    from handlers.async_handler import run_async_query
    # The async handler is designed to be called from main.py, but we can still run it here.
    # It returns (response_string, bool) but we ignore response as it's handled elsewhere.
    run_async_query(action)
    return True, None, None, True
