# handlers/features.py — Feature flags system (M-32)
"""Enable/disable modules via config."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context

console = Console()

DEFAULT_FEATURES = {
    "voice": {"enabled": False, "description": "Голосовой помощник (TTS)"},
    "hints": {"enabled": True, "description": "Подсказки в реальном времени"},
    "news": {"enabled": True, "description": "Новости кибербезопасности"},
    "social": {"enabled": True, "description": "Тренажёр социальной инженерии"},
    "sandbox": {"enabled": True, "description": "Песочница для кода"},
    "bounty": {"enabled": True, "description": "Bug Bounty симуляция"},
    "htb": {"enabled": True, "description": "HackTheBox интеграция"},
    "analytics": {"enabled": True, "description": "Продвинутая аналитика"},
    "tracks": {"enabled": True, "description": "Учебные траектории"},
    "missions": {"enabled": True, "description": "Система миссий"},
    "dashboard": {"enabled": True, "description": "Личный дашборд"},
    "auto_writeup": {"enabled": True, "description": "Автоматический writeup"},
    "spaced_repetition": {"enabled": True, "description": "Интервальные повторения"},
    "risk": {"enabled": True, "description": "Механика уровня риска"},
    "shop": {"enabled": True, "description": "Магазин за XP"},
    "equipment": {"enabled": True, "description": "Система экипировки"},
}


def handle_features(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Manage feature flags."""
    ctx = get_context()
    state = ctx.state

    # Initialize feature_flags if not present
    if not hasattr(state, "feature_flags"):
        state.feature_flags = {k: v["enabled"] for k, v in DEFAULT_FEATURES.items()}
        ctx.save_state()

    parts = action.split(maxsplit=2)

    if len(parts) == 1:
        # Показать список модулей
        _list_features(state)
        return True, None, None, True

    subcommand = parts[1].lower()

    if subcommand == "list":
        _list_features(state)
        return True, None, None, True

    if subcommand in ("enable", "disable", "toggle"):
        if len(parts) < 3:
            console.print("[yellow]Укажите модуль: /features enable <модуль>[/yellow]")
            return True, None, None, True

        feature = parts[2].lower()
        if feature not in DEFAULT_FEATURES:
            console.print(f"[red]❌ Модуль '{feature}' не найден[/red]")
            console.print("[dim]Доступные: " + ", ".join(DEFAULT_FEATURES.keys()) + "[/dim]")
            return True, None, None, True

        if subcommand == "enable":
            state.feature_flags[feature] = True
            console.print(f"[green]✅ Модуль '{feature}' включён[/green]")
        elif subcommand == "disable":
            state.feature_flags[feature] = False
            console.print(f"[yellow]⚠️ Модуль '{feature}' отключён[/yellow]")
        elif subcommand == "toggle":
            state.feature_flags[feature] = not state.feature_flags.get(feature, True)
            status = "включён" if state.feature_flags[feature] else "отключён"
            console.print(f"[cyan]🔄 Модуль '{feature}' {status}[/cyan]")

        ctx.save_state()
        return True, None, None, True

    if subcommand == "reset":
        state.feature_flags = {k: v["enabled"] for k, v in DEFAULT_FEATURES.items()}
        ctx.save_state()
        console.print("[green]✅ Feature flags сброшены к дефолтным[/green]")
        return True, None, None, True

    console.print("[yellow]Использование:[/yellow]")
    console.print("  /features list              — показать все модули")
    console.print("  /features enable <модуль>   — включить модуль")
    console.print("  /features disable <модуль>  — отключить модуль")
    console.print("  /features toggle <модуль>   — переключить модуль")
    console.print("  /features reset             — сбросить к дефолтным")

    return True, None, None, True


def _list_features(state) -> None:
    """Показать список всех модулей с статусом."""
    console.print(Panel(
        "[bold cyan]🔧 Управление модулями[/bold cyan]\n",
        title="FEATURE FLAGS",
        border_style="cyan",
    ))

    for feature_id, info in DEFAULT_FEATURES.items():
        enabled = state.feature_flags.get(feature_id, info["enabled"])
        status = "[green]✓ ВКЛ[/green]" if enabled else "[red]✕ ВЫКЛ[/red]"
        console.print(f"  {status} [cyan]{feature_id:<20}[/cyan] — {info['description']}")

    console.print()
    console.print("[dim]Управление: /features enable|disable|toggle <модуль>[/dim]")


def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled."""
    ctx = get_context()
    state = ctx.state
    if not hasattr(state, "feature_flags"):
        return DEFAULT_FEATURES.get(feature, {}).get("enabled", True)
    return state.feature_flags.get(feature, DEFAULT_FEATURES.get(feature, {}).get("enabled", True))
