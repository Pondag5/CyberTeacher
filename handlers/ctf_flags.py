# handlers/ctf_flags.py — Dynamic CTF flags (G-03)
"""On-the-fly CTF flag generation with hash-based verification."""

import hashlib
import random
import time
from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context

console = Console()

FLAG_PREFIX = "CTF"
FLAG_TTL = 3600  # 1 час жизни флага


def generate_flag(challenge_id: str, user_id: str = "default") -> str:
    """Сгенерировать уникальный флаг для пользователя."""
    seed = f"{challenge_id}:{user_id}:{int(time.time() // FLAG_TTL)}"
    h = hashlib.sha256(seed.encode()).hexdigest()[:12]
    return f"{FLAG_PREFIX}{{{challenge_id}_{h}}}"


def verify_flag(submitted: str, challenge_id: str, user_id: str = "default") -> bool:
    """Проверить флаг (действителен в течение TTL)."""
    if not submitted.startswith(f"{FLAG_PREFIX}{{{challenge_id}_"):
        return False

    # Проверить текущий и предыдущий временной слот (для edge cases)
    for offset in [0, -1]:
        seed = f"{challenge_id}:{user_id}:{int(time.time() // FLAG_TTL) + offset}"
        h = hashlib.sha256(seed.encode()).hexdigest()[:12]
        valid = f"{FLAG_PREFIX}{{{challenge_id}_{h}}}"
        if submitted == valid:
            return True
    return False


def handle_ctf_flags(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление динамическими CTF-флагами."""
    parts = action.split(maxsplit=2)

    if len(parts) == 1:
        console.print(Panel(
            "[bold cyan]🚩 Динамические CTF-флаги[/bold cyan]\n\n"
            "Использование:\n"
            "  /ctf generate <challenge>  — сгенерировать флаг\n"
            "  /ctf submit <флаг>         — отправить флаг\n"
            "  /ctf list                  — доступные челленджи\n"
            "  /ctf verify <флаг> <id>    — проверить вручную\n\n"
            "Флаги уникальны для каждого пользователя и меняются каждый час.",
            title="CTF FLAGS",
            border_style="cyan",
        ))
        return True, None, None, True

    subcommand = parts[1].lower()

    if subcommand == "generate" and len(parts) >= 3:
        return _generate(parts[2])

    if subcommand == "submit" and len(parts) >= 3:
        return _submit(parts[2])

    if subcommand == "list":
        return _list_challenges()

    if subcommand == "verify" and len(parts) >= 4:
        flag = parts[2]
        cid = parts[3]
        valid = verify_flag(flag, cid)
        status = "[green]✅ Валидный[/green]" if valid else "[red]❌ Невалидный[/red]"
        console.print(f"Флаг: {flag}\nЧеллендж: {cid}\nРезультат: {status}")
        return True, None, None, True

    console.print("[yellow]Неизвестная подкоманда. /ctf для справки.[/yellow]")
    return True, None, None, True


def _generate(challenge_id: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Generate a flag for a challenge."""
    ctx = get_context()
    state = ctx.state
    user_id = getattr(state, "username", "default")
    flag = generate_flag(challenge_id, user_id)

    remaining = FLAG_TTL - (int(time.time()) % FLAG_TTL)
    mins = remaining // 60

    console.print(Panel(
        f"[bold]Челлендж:[/bold] {challenge_id}\n"
        f"[bold]Флаг:[/bold] [green]{flag}[/green]\n\n"
        f"[dim]Действителен ещё {mins} мин[/dim]\n"
        f"[dim]Уникален для пользователя: {user_id}[/dim]",
        title="🚩 ФЛАГ СГЕНЕРИРОВАН",
        border_style="green",
    ))

    state.ctf_flags_generated = getattr(state, "ctf_flags_generated", 0) + 1
    ctx.save_state()

    return True, None, None, True


def _submit(submitted_flag: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Submit a flag for verification."""
    # Extract challenge_id from flag: CTF{challenge_id_hash}
    if not submitted_flag.startswith(f"{FLAG_PREFIX}{") or not submitted_flag.endswith("}"):
        console.print("[red]❌ Неверный формат флага. Ожидается: CTF{...}[/red]")
        return True, None, None, True

    inner = submitted_flag[4:-1]
    if "_" not in inner:
        console.print("[red]❌ Неверный формат флага[/red]")
        return True, None, None, True

    challenge_id = inner.split("_", 1)[0]
    ctx = get_context()
    state = ctx.state
    user_id = getattr(state, "username", "default")

    if verify_flag(submitted_flag, challenge_id, user_id):
        xp = random.randint(50, 150)
        console.print(Panel(
            f"[bold green]✅ Флаг принят![/bold green]\n\n"
            f"Челлендж: {challenge_id}\n"
            f"XP: +{xp}\n"
            f"Всего флагов: {state.total_flags_collected + 1}",
            title="🚩 УСПЕХ",
            border_style="green",
        ))
        state.total_flags_collected += 1
        state.points += xp
        state.add_reputation(xp // 2)
        state.track_skill("ctf", True, xp)
        state.check_achievements()
        ctx.save_state()
    else:
        console.print(Panel(
            f"[bold red]❌ Флаг неверный или истёк[/bold red]\n\n"
            f"[dim]Флаги действительны 1 час и уникальны для вашего пользователя.[/dim]",
            title="🚩 ОТКАЗ",
            border_style="red",
        ))

    return True, None, None, True


def _list_challenges() -> tuple[bool, Any | None, Any | None, bool]:
    """Показать доступные челленджи."""
    challenges = [
        ("web_basic", "Web Basics", "easy", 50),
        ("sqli_union", "SQLi UNION", "medium", 100),
        ("xss_reflected", "Reflected XSS", "easy", 50),
        ("crypto_caesar", "Caesar Cipher", "easy", 40),
        ("forensics_pcap", "PCAP Analysis", "medium", 100),
        ("priv_esc_linux", "Linux PrivEsc", "hard", 150),
        ("reverse_basic", "Reverse Engineering", "hard", 150),
    ]

    lines = []
    for cid, name, diff, xp in challenges:
        diff_color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(diff, "white")
        lines.append(f"  [cyan]{cid:<20}[/cyan] [{diff_color}]{diff:<8}[/] {name} [dim]({xp} XP)[/dim]")

    console.print(Panel("\n".join(lines), title="🚩 ЧЕЛЛЕНДЖИ", border_style="cyan"))
    return True, None, None, True
