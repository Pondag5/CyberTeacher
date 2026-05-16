# handlers/theme.py — Смена цветовой схемы (M-29)
"""Темы оформления для CLI интерфейса."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()

THEMES = {
    "default": {
        "name": "Default",
        "description": "Стандартная тема (cyan/green)",
        "border": "cyan",
        "primary": "cyan",
        "success": "green",
        "warning": "yellow",
        "error": "red",
    },
    "dark": {
        "name": "Dark Matrix",
        "description": "Тёмная тема в стиле Matrix (green/black)",
        "border": "green",
        "primary": "green",
        "success": "bright_green",
        "warning": "yellow",
        "error": "red",
    },
    "ocean": {
        "name": "Ocean",
        "description": "Морская тема (blue/teal)",
        "border": "blue",
        "primary": "bright_cyan",
        "success": "green",
        "warning": "yellow",
        "error": "red",
    },
    "sunset": {
        "name": "Sunset",
        "description": "Тёплая тема (orange/purple)",
        "border": "magenta",
        "primary": "bright_magenta",
        "success": "green",
        "warning": "yellow",
        "error": "red",
    },
    "colorblind": {
        "name": "Colorblind Friendly",
        "description": "Доступная тема для дальтоников",
        "border": "white",
        "primary": "bright_white",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
    },
    "hacker": {
        "name": "Hacker Terminal",
        "description": "Стиль терминала хакера (bright green on black)",
        "border": "bright_green",
        "primary": "bright_green",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
    },
}


def handle_theme(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление темами оформления."""
    state = get_state()

    # Инициализируем current_theme если нет
    if not hasattr(state, "current_theme"):
        state.current_theme = "default"
        state.save_to_file()

    parts = action.split(maxsplit=1)

    if len(parts) == 1:
        # Показать список тем
        current = state.current_theme
        console.print(Panel(
            "[bold cyan]🎨 Доступные темы оформления[/bold cyan]\n",
            title="ТЕМЫ",
            border_style="cyan",
        ))

        for theme_id, theme in THEMES.items():
            marker = " [bold green]← текущая[/bold green]" if theme_id == current else ""
            console.print(f"  [cyan]{theme_id:<12}[/cyan] — {theme['name']}{marker}")
            console.print(f"  [dim]{' ' * 14}{theme['description']}[/dim]")
            console.print()

        console.print("[yellow]Использование: /theme <имя>[/yellow]")
        console.print("[dim]Доступные: " + ", ".join(THEMES.keys()) + "[/dim]")
        return True, None, None, True

    theme_name = parts[1].strip().lower()

    if theme_name not in THEMES:
        console.print(f"[red]❌ Тема '{theme_name}' не найдена[/red]")
        console.print("[dim]Доступные: " + ", ".join(THEMES.keys()) + "[/dim]")
        return True, None, None, True

    state.current_theme = theme_name
    state.save_to_file()

    theme = THEMES[theme_name]
    console.print(Panel(
        f"[bold green]✅ Тема изменена![/bold green]\n\n"
        f"Название: [cyan]{theme['name']}[/cyan]\n"
        f"Описание: {theme['description']}\n\n"
        "[dim]Изменения применены к новым панелям.[/dim]",
        title="ТЕМА",
        border_style=theme["border"],
    ))

    return True, None, None, True


def get_theme_colors() -> dict[str, str]:
    """Получить цвета текущей темы."""
    state = get_state()
    theme_name = getattr(state, "current_theme", "default")
    return THEMES.get(theme_name, THEMES["default"])
