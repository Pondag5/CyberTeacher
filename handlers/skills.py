# handlers/skills.py — Трекер навыков + репутация + глубина (L-02, L-10, L-05)
"""Трекер практических навыков, система репутации, глубина объяснений."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()

SKILL_CATEGORIES = [
    "sql_injection", "xss", "network_scanning", "privilege_escalation",
    "cryptography", "social_engineering", "forensics", "reverse_engineering",
    "web_exploitation", "malware_analysis", "osint", "cloud_security",
]


def handle_skills(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление навыками, репутацией, глубиной."""
    parts = action.split(maxsplit=2)

    if len(parts) == 1:
        console.print(Panel(
            "[bold cyan]🎯 Навыки, репутация, глубина[/bold cyan]\n\n"
            "Использование:\n"
            "  /skills                     — показать все навыки\n"
            "  /skills track <навык> <ok/fail> — записать практику\n"
            "  /reputation                 — показать репутацию\n"
            "  /depth [beginner|normal|expert] — глубина объяснений",
            title="НАВЫКИ",
            border_style="cyan",
        ))
        return True, None, None, True

    subcommand = parts[1].lower()

    if subcommand == "track" and len(parts) >= 4:
        return _track_skill(parts[2], parts[3])

    if subcommand == "track":
        console.print("[yellow]/skills track <навык> <ok|fail>[/yellow]")
        return True, None, None, True

    return True, None, None, True


def handle_reputation(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Показать репутацию и хэндл."""
    state = get_state()
    handle = state.get_handle()
    rep = state.reputation

    # Найти следующий хэндл
    next_handle = None
    next_threshold = None
    for threshold, name in state.HANDLES:
        if rep < threshold:
            next_handle = name
            next_threshold = threshold
            break

    progress = ""
    if next_threshold:
        pct = (rep / next_threshold) * 100
        bar_len = int(pct / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        progress = f"\n  Прогресс: [{bar}] {pct:.0f}% до '{next_handle}'"

    console.print(Panel(
        f"[bold]🏆 Репутация: {rep}[/bold]\n"
        f"[bold]Хэндл: {handle}[/bold]"
        f"{progress}",
        title="РЕПУТАЦИЯ",
        border_style="yellow",
    ))
    return True, None, None, True


def handle_depth(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление глубиной объяснений."""
    state = get_state()
    parts = action.split(maxsplit=1)

    if len(parts) == 1:
        current = state.get_explanation_depth()
        depth_names = {
            "beginner": "🟢 Новичок — простые объяснения, аналогии, пошагово",
            "normal": "🟡 Стандарт — баланс деталей и краткости",
            "expert": "🔴 Эксперт — технически точно, без воды",
        }
        console.print(Panel(
            f"Текущая: [bold]{depth_names.get(current, current)}[/bold]\n\n"
            "Доступные:\n"
            f"  /depth beginner  — {depth_names['beginner']}\n"
            f"  /depth normal    — {depth_names['normal']}\n"
            f"  /depth expert    — {depth_names['expert']}",
            title="ГЛУБИНА ОБЪЯСНЕНИЙ",
            border_style="cyan",
        ))
        return True, None, None, True

    depth = parts[1].strip().lower()
    if depth not in ("beginner", "normal", "expert"):
        console.print("[red]❌ Доступные: beginner, normal, expert[/red]")
        return True, None, None, True

    state.set_explanation_depth(depth)
    state.save_to_file()
    console.print(f"[green]✅ Глубина установлена: {depth}[/green]")
    return True, None, None, True


def _track_skill(skill: str, result: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Записать практику навыка."""
    state = get_state()
    success = result.lower() in ("ok", "yes", "true", "1", "success")
    xp = 15 if success else 5

    state.track_skill(skill, success, xp)
    level = state.get_skill_level(skill)

    status = "✅ успех" if success else "❌ попытка"
    console.print(f"[green]📈 {skill}: {status} (+{xp} XP, уровень {level})[/green]")
    return True, None, None, True


def handle_skills_list(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Показать все навыки."""
    state = get_state()
    skills = state.get_all_skills()

    if not skills:
        console.print("[yellow]Нет записанных навыков. Используйте /skills track <навык> <ok/fail>[/yellow]")
        return True, None, None, True

    lines = []
    for s in skills:
        bar = "█" * s["level"] + "░" * (5 - s["level"])
        lines.append(
            f"  [cyan]{s['name']:<25}[/cyan] [{bar}] L{s['level']} "
            f"({s['xp']} XP, {s['success_rate']}% success, {s['attempts']} attempts)"
        )

    console.print(Panel(
        "\n".join(lines),
        title="🎯 ПРАКТИЧЕСКИЕ НАВЫКИ",
        border_style="cyan",
    ))
    return True, None, None, True
