# handlers/theme.py — Theme switching (M-29)
"""UI theme management."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context

console = Console()

THEMES = {
    "ocean": {
        "name": "Ocean",
        "description": "Океан (Blue/Teal) — #00B4D8",
        "border": "cyan",
        "primary": "#00B4D8",
        "success": "#48CAE4",
        "warning": "yellow",
        "error": "red",
    },
    "sunset": {
        "name": "Sunset",
        "description": "Закат (Orange/Purple) — #FF6A00",
        "border": "magenta",
        "primary": "#FF6A00",
        "success": "#9D4EDD",
        "warning": "yellow",
        "error": "red",
    },
    "matrix": {
        "name": "Matrix",
        "description": "Матрица (Neon Green) — #00FF41",
        "border": "bright_green",
        "primary": "#00FF41",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
    },
}


def handle_theme(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Handle /theme command for theme switching."""
    ctx = get_context()
    state = ctx.state

    # Initialize current_theme if not present
    if not hasattr(state, "current_theme"):
        state.current_theme = "ocean"
        ctx.save_state()

    parts = action.split(maxsplit=1)

    if len(parts) == 1:
        # Show available themes
        current = state.current_theme
        console.print(Panel(
            "[bold cyan]🎨 Available Themes[/bold cyan]\n",
            title="THEMES",
            border_style="cyan",
        ))

        for theme_id, theme in THEMES.items():
            marker = " [bold green]← current[/bold green]" if theme_id == current else ""
            console.print(f"  [cyan]{theme_id:<12}[/cyan] — {theme['name']}{marker}")
            console.print(f"  [dim]{' ' * 14}{theme['description']}[/dim]")
            console.print()

        console.print("[yellow]Usage: /theme <name>[/yellow]")
        console.print("[dim]Available: " + ", ".join(THEMES.keys()) + "[/dim]")
        return True, None, None, True

    theme_name = parts[1].strip().lower()

    if theme_name not in THEMES:
        console.print(f"[red]❌ Theme '{theme_name}' not found[/red]")
        console.print("[dim]Available: " + ", ".join(THEMES.keys()) + "[/dim]")
        return True, None, None, True

    state.current_theme = theme_name
    ctx.save_state()

    theme = THEMES[theme_name]
    console.print(Panel(
        f"[bold green]✅ Theme changed![/bold green]\n\n"
        f"Name: [cyan]{theme['name']}[/cyan]\n"
        f"Description: {theme['description']}\n\n"
        "[dim]Changes applied to new panels.[/dim]",
        title="THEME",
        border_style=theme["border"],
    ))

    return True, None, None, True


def get_theme_colors() -> dict[str, str]:
    """Get colors of current theme."""
    ctx = get_context()
    state = ctx.state
    theme_name = getattr(state, "current_theme", "ocean")
    return THEMES.get(theme_name, THEMES["ocean"])
