# handlers/lang.py — Language switching (i18n)
"""Interface language selection and switching."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context
from i18n import get_available_languages, t

console = Console()


def handle_lang(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Handle /lang command for switching interface language."""
    ctx = get_context()
    state = ctx.state
    parts = action.split(maxsplit=1)

    if len(parts) == 1:
        return _show_languages()

    lang_code = parts[1].strip().lower()
    available = get_available_languages()
    codes = [lang["code"] for lang in available]

    if lang_code not in codes:
        console.print(
            f"[red]{t(state.language, 'ui.lang.not_found', lang_code=lang_code)}[/red]"
        )
        console.print(f"[dim]{t(state.language, 'ui.lang.available')}: {', '.join(codes)}[/dim]")
        return True, None, None, True

    old_lang = state.language
    state.language = lang_code
    ctx.save_state()

    lang_name = get_available_languages()[codes.index(lang_code)]["name"]
    console.print(
        f"[green]{t(lang_code, 'ui.lang.changed', lang_name=lang_name)}[/green]"
    )
    return True, None, None, True


def _show_languages() -> tuple[bool, Any | None, Any | None, bool]:
    """Show available languages."""
    ctx = get_context()
    state = ctx.state
    available = get_available_languages()
    current = state.language

    lines = []
    for lang in available:
        marker = f" [bold green]{t(current, 'ui.theme.current')}[/bold green]" if lang["code"] == current else ""
        lines.append(f"  [cyan]{lang['code']:<6}[/cyan] — {lang['name']}{marker}")

    console.print(Panel(
        "\n".join(lines),
        title=t(current, "ui.lang.title"),
        border_style="cyan",
    ))
    console.print(f"[dim]{t(current, 'ui.lang.usage')}[/dim]")
    return True, None, None, True
