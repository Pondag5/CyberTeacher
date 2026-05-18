"""
Offline Mode Handler (G-07)

Переключение режима работы без LLM.
В офлайн-режиме доступны: квизы, курсы, лаборатории, прогресс.
Чат с LLM отключён.
"""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context

console = Console()


def handle_offline(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка /offline [on|off|status]."""
    ctx = get_context()
    state = ctx.state

    parts = action.split()
    subcmd = parts[1] if len(parts) > 1 else "status"

    if subcmd == "on":
        state.offline_mode = True
        console.print(Panel(
            "[OFF] Офлайн-режим включён\n\n"
            "[green]Доступно:[/green] квизы, курсы, лаборатории, прогресс\n"
            "[red]Отключено:[/red] чат с LLM, генерация квизов через LLM\n\n"
            "Для отключения: /offline off",
            title="ОФЛАЙН",
            border_style="yellow",
        ))
        return True, None, None, True

    elif subcmd == "off":
        state.offline_mode = False
        console.print(Panel(
            "[ON] Онлайн-режим включён\n\n"
            "Все функции доступны, включая чат с LLM.",
            title="ОНЛАЙН",
            border_style="green",
        ))
        return True, None, None, True

    else:
        status = "[OFF] ВКЛЮЧЁН" if state.offline_mode else "[ON] ВЫКЛЮЧЕН"
        console.print(Panel(
            f"Статус: {status}\n\n"
            "Использование:\n"
            "  /offline on   — включить офлайн-режим\n"
            "  /offline off  — выключить офлайн-режим\n"
            "  /offline      — показать статус",
            title="ОФЛАЙН-РЕЖИМ",
            border_style="cyan",
        ))
        return True, None, None, True
