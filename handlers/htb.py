"""HackTheBox integration handler (API token version)"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import LLM
from di import get_context
from handlers.types import HandlerResult


if TYPE_CHECKING:
    from state import AppState

console = Console()
logger = logging.getLogger(__name__)

_htb_cache: Dict[str, Tuple[float, Any]] = {}
CACHE_TTL = 300

HTB_API_BASE = "https://www.hackthebox.com/api/v4"
HTB_MACHINES_URL = f"{HTB_API_BASE}/machines"
HTB_MACHINE_DETAIL_URL = f"{HTB_API_BASE}/machines/{{machine_id}}"


class HTBAuthError(Exception):
    pass


class HTBAPIError(Exception):
    pass


def _get_headers() -> Dict[str, str]:
    ctx = get_context()
    state = ctx.state
    token = getattr(state, "htb_token", None)
    if not token:
        raise HTBAuthError(
            "HTB API token not set. Use /htb token <your_token> first.\n"
            "Get your token from https://www.hackthebox.com/api/v4/user/token"
        )
    return {"Authorization": f"Bearer {token}"}


def _fetch_htb_machines(machine_type: str = "all") -> List[Dict[str, Any]]:
    cache_key = f"machines_{machine_type}"
    cached = _htb_cache.get(cache_key)
    if cached and (time.time() - cached[0] < CACHE_TTL):
        # Возвращаем копию, чтобы не изменять кэш
        return cached[1][:] if isinstance(cached[1], list) else cached[1]

    params: Dict[str, Any] = {"per_page": 100}
    if machine_type != "all":
        params["type"] = machine_type

    try:
        resp = requests.get(
            HTB_MACHINES_URL, headers=_get_headers(), params=params, timeout=10
        )
        if resp.status_code == 401:
            raise HTBAuthError("Invalid or expired API token")
        if resp.status_code != 200:
            raise HTBAPIError(f"Failed to fetch machines: {resp.status_code}")
        data = resp.json()
        machines = data.get("data", [])
        _htb_cache[cache_key] = (time.time(), machines)
        result: list[dict[str, Any]] = machines
        return result
    except requests.RequestException as e:
        raise HTBAPIError(f"Network error: {e!s}") from e


def _fetch_htb_machine_detail(machine_id: int) -> Optional[Dict[str, Any]]:
    cache_key = f"machine_{machine_id}"
    cached = _htb_cache.get(cache_key)
    if cached and (time.time() - cached[0] < CACHE_TTL):
        result: dict[str, Any] | None = cached[1]
        return result

    try:
        resp = requests.get(
            HTB_MACHINE_DETAIL_URL.format(machine_id=machine_id),
            headers=_get_headers(),
            timeout=10,
        )
        if resp.status_code == 401:
            raise HTBAuthError("Invalid or expired API token")
        if resp.status_code != 200:
            return None
        data = resp.json()
        machine: dict[str, Any] = data.get("data", {})
        if machine:
            _htb_cache[cache_key] = (time.time(), machine)
        return machine
    except requests.RequestException:
        return None


def _get_htb_user_activity() -> Dict[str, Any]:
    try:
        resp = requests.get(
            "https://www.hackthebox.com/api/v4/profile/activity",
            headers=_get_headers(),
            timeout=10,
        )
        if resp.status_code != 200:
            return {}
        data = resp.json().get("data")
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_htb_progress(state: "AppState") -> None:
    try:
        os.makedirs("./memory", exist_ok=True)
        progress = {
            "completed": getattr(state, "htb_completed", []),
            "token_stored": bool(getattr(state, "htb_token", None)),
        }
        with open("./memory/htb_progress.json", "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save HTB progress: {e}")


def _load_htb_progress(state: "AppState") -> None:
    try:
        if os.path.exists("./memory/htb_progress.json"):
            with open("./memory/htb_progress.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if not hasattr(state, "htb_completed"):
                    state.htb_completed = data.get("completed", [])
    except Exception as e:
        logger.error(f"Failed to load HTB progress: {e}")


def handle_htb(action: str) -> HandlerResult:
    """Main HTB command router."""
    parts = action.split()
    if len(parts) < 2:
        console.print("[cyan]HackTheBox команды:[/cyan]")
        console.print("  /htb token <token>    — сохранить API token")
        console.print("  /htb machines         — список машин")
        console.print("  /htb machine <id>     — информация о машине")
        console.print("  /htb walkthrough <id> — walkthrough машины")
        console.print("  /htb submit <id> <flag> — отправить флаг")
        console.print("  /htb sync             — синхронизировать прогресс")
        console.print("  /htb status           — статус прогресса")
        return True, None, None, True

    sub = parts[1].lower()
    if sub == "token":
        return handle_htb_token(action)
    elif sub == "machines":
        return handle_htb_machines(action)
    elif sub == "machine":
        return handle_htb_machine(action)
    elif sub == "walkthrough":
        return handle_htb_walkthrough(action)
    elif sub == "submit":
        return handle_htb_submit(action)
    elif sub == "sync":
        return handle_htb_sync(action)
    elif sub == "status":
        return handle_htb_status(action)
    else:
        console.print(f"[red]Неизвестная HTB команда: {sub}[/red]")
        return True, None, None, True


def handle_htb_token(action: str) -> HandlerResult:
    parts = action.split(maxsplit=2)
    if len(parts) < 3:
        console.print("[cyan]Использование: /htb token <your_api_token>[/cyan]")
        console.print(
            "[dim]Get your token from https://www.hackthebox.com/api/v4/user/token[/dim]"
        )
        return True, None, None, True

    token = parts[2].strip()
    if not token:
        console.print("[red]❌ Токен не может быть пустым[/red]")
        return True, None, None, True

    try:
        resp = requests.get(
            HTB_MACHINES_URL,
            headers={"Authorization": f"Bearer {token}"},
            params={"per_page": 1},
            timeout=10,
        )
        if resp.status_code == 200:
            ctx = get_context()
            state = ctx.state
            state.htb_token = token
            console.print("[green]✅ HTB API token сохранён[/green]")
            return True, None, None, True
        else:
            console.print("[red]❌ Неверный или недействительный API token[/red]")
            return True, None, None, True
    except Exception as e:
        console.print(f"[red]❌ Ошибка проверки токена: {e!s}[/red]")
        return True, None, None, True


def handle_htb_machines(action: str) -> HandlerResult:
    parts = action.split()
    machine_type = "all"
    if len(parts) >= 3:
        machine_type = parts[2].lower()
        if machine_type not in ("all", "free", "pro"):
            console.print("[yellow]Тип должен быть: all, free, pro[/yellow]")
            return True, None, None, True

    try:
        machines = _fetch_htb_machines(machine_type)
        if not machines:
            console.print("[yellow]Машины не найдены[/yellow]")
            return True, None, None, True

        table = Table(title=f"HTB Machines ({machine_type})")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("OS", style="green")
        table.add_column("Diff", style="yellow")
        table.add_column("Points", style="blue")

        for m in machines[:20]:
            table.add_row(
                str(m.get("id", "?")),
                m.get("name", "Unknown"),
                m.get("os", "?"),
                str(m.get("difficulty", "?")),
                str(m.get("points", "?")),
            )
        console.print(table)
        console.print(f"\n[dim]Всего: {len(machines)} машин[/dim]")
        console.print("[dim]Используй /htb machine <id> для деталей[/dim]")
        return True, None, None, True
    except (HTBAuthError, HTBAPIError) as e:
        console.print(f"[red]❌ {e!s}[/red]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]❌ Неожиданная ошибка: {e!s}[/red]")
        return True, None, None, True


def handle_htb_machine(action: str) -> HandlerResult:
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
        machine = _fetch_htb_machine_detail(machine_id)
        if not machine:
            console.print(f"[red]❌ Машина {machine_id} не найдена[/red]")
            return True, None, None, True

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


def handle_htb_submit(action: str) -> HandlerResult:
    parts = action.split(maxsplit=2)
    if len(parts) < 4:
        console.print("[cyan]Использование: /htb submit <machine_id> <flag>[/cyan]")
        return True, None, None, True

    try:
        machine_id = int(parts[2])
        flag = parts[3].strip()
    except (ValueError, IndexError):
        console.print("[red]❌ ID машины должен быть числом[/red]")
        return True, None, None, True

    if not flag:
        console.print("[red]❌ Флаг не может быть пустым[/red]")
        return True, None, None, True

    try:
        resp = requests.post(
            f"{HTB_MACHINES_URL}/{machine_id}/root",
            headers=_get_headers(),
            json={"flag": flag},
            timeout=10,
        )
        if resp.status_code == 401:
            raise HTBAuthError("Invalid or expired API token")
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                console.print("[green]✅ Флаг принят! Машина пройдена![/green]")
                ctx = get_context()
                state = ctx.state
                if not hasattr(state, "htb_completed"):
                    state.htb_completed = []
                if machine_id not in state.htb_completed:
                    state.htb_completed.append(machine_id)
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


def handle_htb_sync(action: str) -> HandlerResult:
    try:
        activity = _get_htb_user_activity()
        if not activity:
            console.print("[yellow]⚠️ Не удалось получить активность[/yellow]")
            return True, None, None, True

        completed = activity.get("machines", [])
        ctx = get_context()
        state = ctx.state
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


def handle_htb_status(action: str) -> HandlerResult:
    ctx = get_context()
    state = ctx.state
    _load_htb_progress(state)

    completed = getattr(state, "htb_completed", [])
    token_set = bool(getattr(state, "htb_token", None))

    out = "[bold]📊 Статус HackTheBox[/bold]\n\n"
    out += f"🔑 API token: {'✅ установлен' if token_set else '❌ не установлен'}\n"
    out += f"✅ Завершено машин: {len(completed)}\n"
    if completed:
        out += f"\n[dim]ID завершённых: {', '.join(map(str, completed[:10]))}"
        if len(completed) > 10:
            out += f" ...и ещё {len(completed) - 10}[/dim]\n"

    console.print(Panel(out, title="HTB Status", border_style="cyan"))
    return True, None, None, True


def handle_htb_walkthrough(action: str) -> HandlerResult:
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
        machine = _fetch_htb_machine_detail(machine_id)
        if not machine:
            console.print(f"[red]❌ Машина {machine_id} не найдена[/red]")
            return True, None, None, True

        ctx = get_context()
        state = ctx.state
        completed = getattr(state, "htb_completed", [])
        if machine_id not in completed:
            console.print(
                "[yellow]⚠️ Рекомендуется сначала пройти машину самостоятельно, "
                "чтобы получить максимальную пользу[/yellow]"
            )
            response = input("Продолжить? (y/N): ").strip().lower()
            if response != "y":
                return True, None, None, True

        console.print("[bold cyan]🔍 Генерация пошагового разбора...[/bold cyan]")

        llm = LLM()
        if llm is None:
            console.print("[red]❌ LLM не доступна[/red]")
            return True, None, None, True

        prompt_lines = [
            "Ты - эксперт по кибербезопасности и преподаватель.",
            "Создай подробный пошаговый разбор (walkthrough) для машины HackTheBox:",
            "",
            f"Название: {machine.get('name')}",
            f"ОС: {machine.get('os')}",
            f"Сложность: {machine.get('difficulty')}",
            f"Описание: {machine.get('description', 'Нет описания')}",
            "",
            "Требования:",
            "1. Разбей на логические шаги (разведка, сканирование, уязвимость, эксплойт, повышение привилегий, флаг)",
            "2. Для каждого шага дай конкретные команды (nmap, gobuster, sqlmap, etc.)",
            "3. Объясни, почему каждая команда используется",
            "4. Укажи возможные ошибки и как их избежать",
            "5. Добавь советы по дебаггингу",
            "",
            "Формат:",
            "## Шаг 1: [Название шага]",
            "**Цель:** ...",
            "**Команды:**",
            "```bash",
            "$ ...",
            "```",
            "**Результат/Пояснение:** ...",
        ]
        prompt = "\n".join(prompt_lines)

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

    except HTBAuthError as e:
        console.print(f"[red]❌ {e!s}[/red]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e!s}[/red]")
        return True, None, None, True
