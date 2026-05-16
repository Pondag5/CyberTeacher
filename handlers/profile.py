# handlers/profile.py — Профили пользователей (G-09)
"""Смена имени, аватар, настройки профиля."""

import os
from typing import Any

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()

AVATARS = [
    "🐱", "🐶", "🦊", "🐼", "🐨", "🦁", "🐯", "🐸",
    "🤖", "👾", "🎃", "👻", "💀", "🤠", "🥷", "🧙",
    "🦹", "🧑‍💻", "🕵️", "👨‍🚀", "🧑‍🔬", "🦸", "🥷", "🧛",
]


def handle_profile(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление профилем пользователя."""
    parts = action.split(maxsplit=2)

    if len(parts) == 1:
        return _show_profile()

    subcommand = parts[1].lower()

    if subcommand == "name" and len(parts) >= 3:
        return _set_name(parts[2])

    if subcommand == "avatar" and len(parts) >= 3:
        return _set_avatar(parts[2])

    if subcommand == "avatar":
        return _list_avatars()

    if subcommand == "reset":
        return _reset_profile()

    if subcommand == "stats":
        return _show_detailed_stats()

    console.print("[yellow]Использование: /profile name <имя> | avatar <эмодзи> | stats | reset[/yellow]")
    return True, None, None, True


def _show_profile() -> tuple[bool, Any | None, Any | None, bool]:
    """Показать профиль."""
    state = get_state()
    username = getattr(state, "username", "Аноним")
    avatar = getattr(state, "avatar", "🧑‍💻")
    handle = state.get_handle()
    rep = state.reputation

    console.print(Panel(
        f"[bold]{avatar} {username}[/bold]\n\n"
        f"Хэндл: {handle}\n"
        f"Репутация: {rep}\n"
        f"XP: {state.points:.0f}\n"
        f"Флагов: {state.total_flags_collected}\n"
        f"Квизов: {state.quizzes_taken}\n"
        f"Лабораторий: {state.labs_started}\n\n"
        f"[dim]/profile name <имя> — сменить имя[/dim]\n"
        f"[dim]/profile avatar — выбрать аватар[/dim]\n"
        f"[dim]/profile stats — подробная статистика[/dim]",
        title="ПРОФИЛЬ",
        border_style="cyan",
    ))
    return True, None, None, True


def _set_name(name: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Установить имя."""
    name = name.strip()
    if not name:
        console.print("[red]❌ Имя не может быть пустым[/red]")
        return True, None, None, True
    if len(name) > 30:
        console.print("[red]❌ Имя слишком длинное (макс 30 символов)[/red]")
        return True, None, None, True

    state = get_state()
    old_name = getattr(state, "username", "Аноним")
    state.username = name
    state.save_to_file()

    console.print(f"[green]✅ Имя изменено: {old_name} → {name}[/green]")
    return True, None, None, True


def _set_avatar(avatar: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Установить аватар."""
    avatar = avatar.strip()
    if avatar not in AVATARS:
        console.print(f"[yellow]⚠️ '{avatar}' нет в списке. /profile avatar для списка.[/yellow]")
        # Всё равно установить — вдруг пользователь хочет свой эмодзи
        state = get_state()
        state.avatar = avatar
        state.save_to_file()
        console.print(f"[green]✅ Аватар установлен: {avatar}[/green]")
        return True, None, None, True

    state = get_state()
    state.avatar = avatar
    state.save_to_file()
    console.print(f"[green]✅ Аватар установлен: {avatar}[/green]")
    return True, None, None, True


def _list_avatars() -> tuple[bool, Any | None, Any | None, bool]:
    """Показать доступные аватары."""
    state = get_state()
    current = getattr(state, "avatar", "🧑‍💻")

    lines = []
    for a in AVATARS:
        marker = " ←" if a == current else ""
        lines.append(f"  {a}{marker}")

    console.print(Panel(
        " ".join(lines[:12]) + "\n" + " ".join(lines[12:]),
        title="АВАТАРЫ",
        border_style="cyan",
    ))
    console.print("[dim]Использование: /profile avatar <эмодзи>[/dim]")
    return True, None, None, True


def _reset_profile() -> tuple[bool, Any | None, Any | None, bool]:
    """Сбросить профиль."""
    console.print("[bold red]⚠️ Сбросить профиль? Имя и аватар будут удалены.[/bold red]")
    confirm = input("Введите 'yes': ").strip().lower()
    if confirm == "yes":
        state = get_state()
        state.username = "Аноним"
        state.avatar = "🧑‍💻"
        state.save_to_file()
        console.print("[green]✅ Профиль сброшен[/green]")
    else:
        console.print("[yellow]Отмена[/yellow]")
    return True, None, None, True


def _show_detailed_stats() -> tuple[bool, Any | None, Any | None, bool]:
    """Подробная статистика."""
    state = get_state()
    skills = state.get_all_skills()

    lines = [
        f"[bold]👤 {getattr(state, 'avatar', '🧑‍💻')} {getattr(state, 'username', 'Аноним')}[/bold]",
        f"Хэндл: {state.get_handle()} | Репутация: {state.reputation}",
        f"XP: {state.points:.0f} | Множитель: x{state.get_xp_multiplier():.1f}",
        "",
        f"[bold]📊 Активность:[/bold]",
        f"  Квизов: {state.quizzes_taken} | Заданий: {state.assignments_completed}",
        f"  Флагов: {state.total_flags_collected} | Лаб: {state.labs_started}",
        f"  Сообщений: {state.messages_sent} | Новостей: {state.news_checked}",
    ]

    if skills:
        lines.append(f"\n[bold]🎯 Навыки:[/bold]")
        for s in skills[:5]:
            bar = "█" * s["level"] + "░" * (5 - s["level"])
            lines.append(f"  {s['name']:<20} [{bar}] L{s['level']} ({s['success_rate']}%)")

    console.print(Panel("\n".join(lines), title="ПОДРОБНАЯ СТАТИСТИКА", border_style="cyan"))
    return True, None, None, True
