# handlers/profile.py — User profile management (G-09)
"""Profile settings: name, avatar, stats."""

import os
from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context
from handlers.types import HandlerResult


console = Console()

AVATARS = [
    "🐱",
    "🐶",
    "🦊",
    "🐼",
    "🐨",
    "🦁",
    "🐯",
    "🐸",
    "🤖",
    "👾",
    "🎃",
    "👻",
    "💀",
    "🤠",
    "🥷",
    "🧙",
    "🦹",
    "🧑‍💻",
    "🕵️",
    "👨‍🚀",
    "🧑‍🔬",
    "🦸",
    "🥷",
    "🧛",
]


def handle_profile(action: str) -> HandlerResult:
    """Handle profile management commands."""
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

    console.print(
        "[yellow]Usage: /profile name <name> | avatar <emoji> | stats | reset[/yellow]"
    )
    return True, None, None, True


def _show_profile() -> HandlerResult:
    """Show user profile."""
    ctx = get_context()
    state = ctx.state
    username = getattr(state, "username", "Anonymous")
    avatar = getattr(state, "avatar", "🧑‍💻")
    handle = state.get_handle()
    rep = state.reputation

    console.print(
        Panel(
            f"[bold]{avatar} {username}[/bold]\n\n"
            f"Handle: {handle}\n"
            f"Reputation: {rep}\n"
            f"XP: {state.points:.0f}\n"
            f"Flags: {state.total_flags_collected}\n"
            f"Quizzes: {state.quizzes_taken}\n"
            f"Labs: {state.labs_started}\n\n"
            f"[dim]/profile name <name> — change name[/dim]\n"
            f"[dim]/profile avatar — choose avatar[/dim]\n"
            f"[dim]/profile stats — detailed stats[/dim]",
            title="PROFILE",
            border_style="cyan",
        )
    )
    return True, None, None, True


def _set_name(name: str) -> HandlerResult:
    """Set user name."""
    ctx = get_context()
    state = ctx.state
    name = name.strip()
    if not name:
        console.print("[red]❌ Name cannot be empty[/red]")
        return True, None, None, True
    if len(name) > 30:
        console.print("[red]❌ Name too long (max 30 characters)[/red]")
        return True, None, None, True

    old_name = getattr(state, "username", "Anonymous")
    state.username = name
    ctx.save_state()

    console.print(f"[green]✅ Name changed: {old_name} → {name}[/green]")
    return True, None, None, True


def _set_avatar(avatar: str) -> HandlerResult:
    """Set user avatar."""
    ctx = get_context()
    state = ctx.state
    avatar = avatar.strip()
    if avatar not in AVATARS:
        console.print(
            f"[yellow]⚠️ '{avatar}' not in list. /profile avatar for list.[/yellow]"
        )
        # Still allow custom emoji
        state.avatar = avatar
        ctx.save_state()
        console.print(f"[green]✅ Avatar set: {avatar}[/green]")
        return True, None, None, True

    state.avatar = avatar
    ctx.save_state()
    console.print(f"[green]✅ Avatar set: {avatar}[/green]")
    return True, None, None, True


def _list_avatars() -> HandlerResult:
    """Show available avatars."""
    ctx = get_context()
    state = ctx.state
    current = getattr(state, "avatar", "🧑‍💻")

    lines = []
    for a in AVATARS:
        marker = " ←" if a == current else ""
        lines.append(f"  {a}{marker}")

    console.print(
        Panel(
            " ".join(lines[:12]) + "\n" + " ".join(lines[12:]),
            title="AVATARS",
            border_style="cyan",
        )
    )
    console.print("[dim]Usage: /profile avatar <emoji>[/dim]")
    return True, None, None, True


def _reset_profile() -> HandlerResult:
    """Reset profile."""
    ctx = get_context()
    state = ctx.state
    console.print(
        "[bold red]⚠️ Reset profile? Name and avatar will be deleted.[/bold red]"
    )
    confirm = input("Type 'yes': ").strip().lower()
    if confirm == "yes":
        state.username = "Anonymous"
        state.avatar = "🧑‍💻"
        ctx.save_state()
        console.print("[green]✅ Profile reset[/green]")
    else:
        console.print("[yellow]Cancelled[/yellow]")
    return True, None, None, True


def _show_detailed_stats() -> HandlerResult:
    """Show detailed stats."""
    ctx = get_context()
    state = ctx.state
    skills = state.get_all_skills()

    lines = [
        f"[bold]👤 {getattr(state, 'avatar', '🧑‍💻')} {getattr(state, 'username', 'Anonymous')}[/bold]",
        f"Handle: {state.get_handle()} | Reputation: {state.reputation}",
        f"XP: {state.points:.0f} | Multiplier: x{state.get_xp_multiplier():.1f}",
        "",
        f"[bold]📊 Activity:[/bold]",
        f"  Quizzes: {state.quizzes_taken} | Assignments: {state.assignments_completed}",
        f"  Flags: {state.total_flags_collected} | Labs: {state.labs_started}",
        f"  Messages: {state.messages_sent} | News: {state.news_checked}",
    ]

    if skills:
        lines.append(f"\n[bold]🎯 Skills:[/bold]")
        skills_list: list[dict[str, Any]] = [
            {"name": k, **v}
            if isinstance(v, dict)
            else {"name": k, "level": 0, "success_rate": 0}
            for k, v in list(skills.items())[:5]
        ]
        for s in skills_list:
            bar = "█" * s["level"] + "░" * (5 - s["level"])
            lines.append(
                f"  {s['name']:<20} [{bar}] L{s['level']} ({s['success_rate']}%)"
            )

    console.print(Panel("\n".join(lines), title="DETAILED STATS", border_style="cyan"))
    return True, None, None, True
