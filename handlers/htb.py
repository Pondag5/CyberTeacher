"""HackTheBox integration handler"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Any

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import LLM
from di import get_context

console = Console()
logger = logging.getLogger(__name__)

# Cache for HTB data
_htb_cache: dict[str, tuple[float, Any]] = {}
CACHE_TTL = 300  # 5 minutes

# HTB API endpoints
HTB_API_BASE = "https://www.hackthebox.com/api/v4"
HTB_LOGIN_URL = "https://www.hackthebox.com/api/v4/login"
HTB_MACHINES_URL = f"{HTB_API_BASE}/machines"
HTB_MACHINE_DETAIL_URL = f"{HTB_API_BASE}/machines/{{machine_id}}"


class HTBAuthError(Exception):
    """Raised when HTB authentication fails"""


class HTBAPIError(Exception):
    """Raised when HTB API returns an error"""


def _get_htb_session() -> requests.Session:
    """Get or create authenticated HTB session."""
    ctx = get_context()
    state = ctx.state
    session = requests.Session()

    # Check if we have stored credentials
    email = state.htb_email
    password = state.htb_password

    if not email or not password:
        raise HTBAuthError(
            "HTB credentials not set. Use /htb login <email> <password> first."
        )

    # Try to login
    try:
        resp = session.post(
            HTB_LOGIN_URL,
            json={"email": email, "password": password},
            timeout=10,
        )
        if resp.status_code != 200:
            raise HTBAuthError(f"Login failed: {resp.status_code}")
        data = resp.json()
        if not data.get("success"):
            raise HTBAuthError(f"Login error: {data.get('message', 'Unknown')}")
        return session
    except Exception as e:
        raise HTBAuthError(f"Authentication error: {e!s}") from e


def _fetch_htb_machines(
    session: requests.Session, machine_type: str = "all"
) -> list[dict]:
    """Fetch machines from HTB API."""
    cache_key = f"machines_{machine_type}"
    cached = _htb_cache.get(cache_key)
    if cached and (time.time() - cached[0] < CACHE_TTL):
        return cached[1]

    params = {"per_page": 100, "type": machine_type}
    if machine_type == "all":
        params.pop("type")

    try:
        resp = session.get(HTB_MACHINES_URL, params=params, timeout=10)
        if resp.status_code != 200:
            raise HTBAPIError(f"Failed to fetch machines: {resp.status_code}")
        data = resp.json()
        machines = data.get("data", [])
        _htb_cache[cache_key] = (time.time(), machines)
        return machines
    except Exception as e:
        raise HTBAPIError(f"Error fetching machines: {e!s}") from e


def _fetch_htb_machine_detail(
    session: requests.Session, machine_id: int
) -> dict | None:
    """Fetch detailed info about a specific machine."""
    cache_key = f"machine_{machine_id}"
    cached = _htb_cache.get(cache_key)
    if cached and (time.time() - cached[0] < CACHE_TTL):
        return cached[1]

    try:
        resp = session.get(
            HTB_MACHINE_DETAIL_URL.format(machine_id=machine_id), timeout=10
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        machine = data.get("data", {})
        _htb_cache[cache_key] = (time.time(), machine)
        return machine
    except Exception:
        return None


def _get_htb_user_activity(session: requests.Session) -> dict | None:
    """Get user's activity (completed machines)."""
    try:
        resp = session.get(
            "https://www.hackthebox.com/api/v4/profile/activity", timeout=10
        )
        if resp.status_code != 200:
            return None
        return resp.json().get("data", {})
    except Exception:
        return None


def handle_htb_login(action: str) -> tuple[bool, None, None, bool]:
    """Handle /htb login <email> <password>"""
    parts = action.split()
    if len(parts) != 4:
        console.print("[cyan]Использование: /htb login <email> <password>[/cyan]")
        console.print("[dim]Пример: /htb login user@example.com mypassword[/dim]")
        return True, None, None, True

    email = parts[2]
    password = parts[3]

    # Test credentials
    try:
        session = requests.Session()
        resp = session.post(
            HTB_LOGIN_URL, json={"email": email, "password": password}, timeout=10
        )
        if resp.status_code == 200 and resp.json().get("success"):
            ctx = get_context()
            state = ctx.state
            state.htb_email = email
            state.htb_password = password
            console.print("[green]✅ Учётные данные HTB сохранены[/green]")
            return True, None, None, True
        else:
            console.print("[red]❌ Неверные учётные данные HTB[/red]")
            return True, None, None, True
    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e!s}[/red]")
        return True, None, None, True


def handle_htb_machines(action: str) -> tuple[bool, None, None, bool]:
    """Handle /htb machines [type]"""
    parts = action.split()
    machine_type = "all"
    if len(parts) >= 3:
        machine_type = parts[2].lower()
        if machine_type not in ("all", "free", "pro"):
            console.print("[yellow]Тип должен быть: all, free, pro[/yellow]")
            return True, None, None, True

    try:
        session = _get_htb_session()
        machines = _fetch_htb_machines(session, machine_type)

        if not machines:
            console.print("[yellow]Машины не найдены[/yellow]")
            return True, None, None, True

        # Build table
        table = Table(title=f"HTB Machines ({machine_type})")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("OS", style="green")
        table.add_column("Diff", style="yellow")
        table.add_column("Points", style="blue")

        for m in machines[:20]:  # Limit to 20
            table.add_row(
                str(m.get("id", "?")),
                m.get("name", "Unknown"),
                m.get("os", "?"),
                m.get("difficulty", "?"),
                str(m.get("points", "?")),
            )

        console.print(table)
        console.print(f"\n[dim]Всего: {len(machines)} машин[/dim]")
        console.print("[dim]Используй /htb machine <id> для деталей[/dim]")
        return True, None, None, True

    except HTBAuthError as e:
        console.print(f"[red]❌ {e!s}[/red]")
        return True, None, None, True
    except HTBAPIError as e:
        console.print(f"[red]❌ {e!s}[/red]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]❌ Неожиданная ошибка: {e!s}[/red]")
        return True, None, None, True


def handle_htb_machine(action: str) -> tuple[bool, None, None, bool]:
    """Handle /htb machine <id>"""
    parts = action.split()
    if len(parts) < 3:
        console.print("[cyan]Использование: /htb machine <id>[/cyan]")
        return True, None, None, True

    try:
        machine_id = int(parts[2])
    except ValueError:
        console.print("[red]❌ ID должен быть числом[/red]")
        return True, None, None, True

    try:
        session = _get_htb_session()
        machine = _fetch_htb_machine_detail(session, machine_id)

        if not machine:
            console.print(f"[red]❌ Машина {machine_id} не найдена[/red]")
            return True, None, None, True

        # Build detailed output
        out = f"""[bold]🖥️  {machine.get("name", "Unknown")}[/bold] (ID: {machine_id})

[cyan]OS:[/cyan] {machine.get("os", "N/A")}
[yellow]Сложность:[/yellow] {machine.get("difficulty", "N/A")}
[green]Очки:[/green] {machine.get("points", "N/A")}
[blue]Рейтинг:[/blue] {machine.get("rating", {}).get("average", "N/A")}

[bold]🏆 Статус:[/bold] {machine.get("status", "N/A")}
[bold]📅 Релиз:[/bold] {machine.get("release", "N/A")}

[bold]📝 Описание:[/bold]
{machine.get("description", "Нет описания")}

[bold]🔥 Подсказки:[/bold]
"""

        hints = machine.get("hints", [])
        if hints:
            for i, hint in enumerate(hints, 1):
                out += f"{i}. {hint.get('text', '')}\n"
        else:
            out += "Нет подсказок\n"

        console.print(Panel(out, title="Machine Details", border_style="cyan"))
        return True, None, None, True

    except HTBAuthError as e:
        console.print(f"[red]❌ {e!s}[/red]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e!s}[/red]")
        return True, None, None, True


def handle_htb_submit(action: str) -> tuple[bool, None, None, bool]:
    """Handle /htb submit <machine_id> <flag>"""
    parts = action.split(maxsplit=2)
    if len(parts) < 4:
        console.print("[cyan]Использование: /htb submit <machine_id> <flag>[/cyan]")
        console.print("[dim]Пример: /htb submit 123 abcdef...[/dim]")
        return True, None, None, True

    try:
        machine_id = int(parts[2])
        flag = parts[3].strip()
    except ValueError:
        console.print("[red]❌ ID машины должен быть числом[/red]")
        return True, None, None, True

    if not flag:
        console.print("[red]❌ Флаг не может быть пустым[/red]")
        return True, None, None, True

    try:
        session = _get_htb_session()

        # Submit flag
        resp = session.post(
            f"{HTB_MACHINES_URL}/{machine_id}/root",
            json={"flag": flag},
            timeout=10,
        )

        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                console.print("[green]✅ Флаг принят! Машина пройдена![/green]")

                # Update state to mark machine as completed
                ctx = get_context()
                state = ctx.state
                if not hasattr(state, "htb_completed"):
                    state.htb_completed = []
                if machine_id not in state.htb_completed:
                    state.htb_completed.append(machine_id)

                # Save progress
                _save_htb_progress(state)
                return True, None, None, True
            else:
                console.print(f"[red]❌ Флаг неверен: {data.get('message', '')}[/red]")
                return True, None, None, True
        else:
            console.print(f"[red]❌ Ошибка отправки: {resp.status_code}[/red]")
            return True, None, None, True

    except HTBAuthError as e:
        console.print(f"[red]❌ {e!s}[/red]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e!s}[/red]")
        return True, None, None, True


def _save_htb_progress(state):
    """Save HTB progress to file."""
    try:
        os.makedirs("./memory", exist_ok=True)
        progress = {
            "completed": state.htb_completed if hasattr(state, "htb_completed") else [],
            "email": state.htb_email if hasattr(state, "htb_email") else None,
        }
        with open("./memory/htb_progress.json", "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save HTB progress: {e}")


def _load_htb_progress(state):
    """Load HTB progress from file."""
    try:
        if os.path.exists("./memory/htb_progress.json"):
            with open("./memory/htb_progress.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if not hasattr(state, "htb_completed"):
                    state.htb_completed = data.get("completed", [])
                # Don't load credentials from file for security
    except Exception as e:
        logger.error(f"Failed to load HTB progress: {e}")


def handle_htb_sync(action: str) -> tuple[bool, None, None, bool]:
    """Handle /htb sync - sync progress with server."""
    try:
        session = _get_htb_session()
        activity = _get_htb_user_activity(session)

        if not activity:
            console.print("[yellow]⚠️ Не удалось получить активность[/yellow]")
            return True, None, None, True

        completed = activity.get("machines", [])
        ctx = get_context()
        state = ctx.state

        # Update local progress
        if not hasattr(state, "htb_completed"):
            state.htb_completed = []

        for m in completed:
            mid = m.get("machine_id")
            if mid and mid not in state.htb_completed:
                state.htb_completed.append(mid)

        _save_htb_progress(state)

        console.print(
            f"[green]✅ Синхронизировано: {len(completed)} завершённых машин[/green]"
        )
        return True, None, None, True

    except HTBAuthError as e:
        console.print(f"[red]❌ {e!s}[/red]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]❌ {e!s}[/red]")
        return True, None, None, True


def handle_htb_status(action: str) -> tuple[bool, None, None, bool]:
    """Handle /htb status - show HTB progress."""
    ctx = get_context()
    state = ctx.state

    # Load progress if not loaded
    _load_htb_progress(state)

    completed = getattr(state, "htb_completed", [])
    email = getattr(state, "htb_email", None)

    out = "[bold]📊 Статус HackTheBox[/bold]\n\n"
    out += f"📧 Аккаунт: {email or 'Не авторизован'}\n"
    out += f"✅ Завершено машин: {len(completed)}\n"

    if completed:
        out += f"\n[dim]ID завершённых: {', '.join(map(str, completed[:10]))}"
        if len(completed) > 10:
            out += f" ...и ещё {len(completed) - 10}[/dim]\n"

    console.print(Panel(out, title="HTB Status", border_style="cyan"))
    return True, None, None, True


def handle_htb_walkthrough(action: str) -> tuple[bool, None, None, bool]:
    """Handle /htb walkthrough <machine_id> - get step-by-step exploit guide."""
    parts = action.split()
    if len(parts) < 3:
        console.print("[cyan]Использование: /htb walkthrough <machine_id>[/cyan]")
        return True, None, None, True

    try:
        machine_id = int(parts[2])
    except ValueError:
        console.print("[red]❌ ID должен быть числом[/red]")
        return True, None, None, True

    try:
        session = _get_htb_session()
        machine = _fetch_htb_machine_detail(session, machine_id)

        if not machine:
            console.print(f"[red]❌ Машина {machine_id} не найдена[/red]")
            return True, None, None, True

        # Check if user has completed this machine
        ctx = get_context()
        state = ctx.state
        completed = getattr(state, "htb_completed", [])
        if machine_id not in completed:
            console.print(
                "[yellow]⚠️ Рекомендуется сначала пройти машину самостоятельно, "
                "чтобы получить максимальную пользу[/yellow]"
            )
            if not console.input("[bold]Продолжить? (y/N): [/bold]"):
                return True, None, None, True

        # Generate walkthrough using LLM
        console.print("[bold cyan]🔍 Генерация пошагового разбора...[/bold cyan]")

        llm = LLM()
        prompt = f"""
Ты - эксперт по кибербезопасности и преподаватель.
Создай подробный пошаговый разбор (walkthrough) для машины HackTheBox:

Название: {machine.get("name")}
ОС: {machine.get("os")}
Сложность: {machine.get("difficulty")}
Описание: {machine.get("description", "Нет описания")}

Требования:
1. Разбей на логические шаги (разведка, сканирование, уязвимость, эксплойт, повышение привилегий, флаг)
2. Для каждого шага дай конкретные команды (nmap, gobuster, sqlmap, etc.)
3. Объясни, почему каждая команда используется
4. Укажи возможные ошибки и как их избежать
5. Добавь советы по дебаггингу

Формат:
## Шаг 1: [Название шага]
**Цель:** ...
**Команды:**
```bash
$ ...
```
**Результат/Пояснение:**
...
"""

        try:
            resp = llm.invoke(prompt)
            walkthrough = resp.content if hasattr(resp, "content") else str(resp)

            console.print(
                Panel(
                    walkthrough,
                    title=f"Walkthrough: {machine.get('name')}",
                    border_style="green",
                )
            )
            return True, None, None, True
        except Exception as e:
            console.print(f"[red]❌ Ошибка генерации walkthrough: {e!s}[/red]")
            return True, None, None, True

    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e!s}[/red]")
        return True, None, None, True


def handle_htb(action: str) -> tuple[bool, None, None, bool]:
    """Main HTB handler - dispatches subcommands."""
    parts = action.split()

    if len(parts) < 2:
        console.print(
            Panel(
                """[bold]HackTheBox Integration[/bold]

[cyan]Команды:[/cyan]
  /htb login <email> <password>  - авторизоваться
  /htb machines [type]          - список машин (all/free/pro)
  /htb machine <id>             - детали машины
  /htb walkthrough <id>         - пошаговый разбор
  /htb submit <id> <flag>       - отправить флаг
  /htb sync                     - синхронизировать прогресс
  /htb status                   - статус аккаунта
""",
                title="HTB Help",
                border_style="cyan",
            )
        )
        return True, None, None, True

    subcmd = parts[1].lower()

    if subcmd == "login":
        return handle_htb_login(action)
    elif subcmd == "machines":
        return handle_htb_machines(action)
    elif subcmd == "machine":
        return handle_htb_machine(action)
    elif subcmd == "walkthrough":
        return handle_htb_walkthrough(action)
    elif subcmd == "submit":
        return handle_htb_submit(action)
    elif subcmd == "sync":
        return handle_htb_sync(action)
    elif subcmd == "status":
        return handle_htb_status(action)
    else:
        console.print(f"[red]❌ Неизвестная команда: /htb {subcmd}[/red]")
        console.print("[dim]Используй /htb для справки[/dim]")
        return True, None, None, True
