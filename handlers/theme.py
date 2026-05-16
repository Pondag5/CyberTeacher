# handlers/theme.py — Theme switching (M-29)
"""UI theme management."""

from typing import Any

from di import get_context
from rich.console import Console
from rich.panel import Panel

console = Console()

THEMES = {
    "default": {
        "name": "Default",
        "description": "Standard theme (cyan/green)",
        "border": "cyan",
        "primary": "cyan",
        "success": "green",
        "warning": "yellow",
        "error": "red",
    },
    "dark": {
        "name": "Dark Matrix",
        "description": "Dark Matrix-style theme (green/black)",
        "border": "green",
        "primary": "green",
        "success": "bright_green",
        "warning": "yellow",
        "error": "red",
    },
    "ocean": {
        "name": "Ocean",
        "description": "Ocean theme (blue/teal)",
        "border": "blue",
        "primary": "bright_cyan",
        "success": "green",
        "warning": "yellow",
        "error": "red",
    },
    "sunset": {
        "name": "Sunset",
        "description": "Warm theme (orange/purple)",
        "border": "magenta",
        "primary": "bright_magenta",
        "success": "green",
        "warning": "yellow",
        "error": "red",
    },
    "colorblind": {
        "name": "Colorblind Friendly",
        "description": "Accessible theme for colorblind users",
        "border": "white",
        "primary": "bright_white",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
    },
    "hacker": {
        "name": "Hacker Terminal",
        "description": "Hacker terminal style (bright green on black)",
        "border": "bright_green",
        "primary": "bright_green",
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
        state.current_theme = "default"
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
    theme_name = getattr(state, "current_theme", "default")
    return THEMES.get(theme_name, THEMES["default"])
