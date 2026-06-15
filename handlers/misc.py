# handlers/misc.py
import json
import os
import re
import time
from typing import Any, Tuple, Optional

from state import get_state

from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from ui import console

from generators import check_open_answer

from utils.common import extract_json_block, parse_json_response

from di import get_context
from courses import list_courses, start_course, get_course_progress
from handlers.types import HandlerResult


# ----------------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ----------------------------------------------------------------------
def _ask_confirm(prompt: str) -> bool:
    """Запросить подтверждение у пользователя."""
    return bool(Confirm.ask(prompt))


def clear_chat_db(conn: Any) -> None:
    """Очистить таблицу сообщений в БД."""
    from memory import clear_chat

    clear_chat(conn)


# ----------------------------------------------------------------------
# ОБРАБОТЧИКИ КОМАНД (используются в core.py)
# ----------------------------------------------------------------------
def handle_adaptive(action: str) -> HandlerResult:
    """Показать слабые темы и рекомендации."""
    from state import get_state

    state = get_state()
    weak = state.get_weak_topics(threshold=70.0)
    if weak:
        console.print(
            Panel(
                "\n".join(
                    [
                        f"• {t['topic']}: {t['success_rate']:.1f}% ({t['attempts']} попыток)"
                        for t in weak
                    ]
                ),
                title="📉 Слабые темы",
                border_style="yellow",
            )
        )
        console.print("[cyan]Совет: повторите эти темы через /quiz или /repeat[/cyan]")
    else:
        console.print("[green]Отлично! Нет слабых тем.[/green]")
    return True, None, None, True


def handle_add_book(action: str) -> HandlerResult:
    """Добавить PDF в базу знаний."""
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print("[red]Укажите путь к PDF: /add_book path/to/file.pdf[/red]")
        return True, None, None, True
    path = parts[1].strip()
    if not os.path.exists(path):
        console.print(f"[red]Файл не найден: {path}[/red]")
        return True, None, None, True
    if not path.lower().endswith(".pdf"):
        console.print("[red]Только PDF файлы поддерживаются[/red]")
        return True, None, None, True
    try:
        from knowledge import add_pdf_to_knowledge_base

        add_pdf_to_knowledge_base(path)
        console.print(f"[green]✅ Книга добавлена: {os.path.basename(path)}[/green]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_backup(action: str) -> HandlerResult:
    """Создать бэкап состояния."""
    from state import get_state

    state = get_state()
    state.maybe_auto_backup()  # без аргументов
    console.print("[green]✅ Бэкап создан в папке backups/[/green]")
    return True, None, None, True


def handle_export(action: str) -> tuple[bool, Any | None, Any | None, True]:
    """Экспорт истории чата или SCORM-пакета курса."""
    if "scorm" in action:
        parts = action.split()
        course_id = parts[2] if len(parts) > 2 else ""
        if not course_id:
            from scorm_export import list_exportable_courses

            courses = list_exportable_courses()
            console.print("[bold]Доступные курсы для SCORM экспорта:[/bold]")
            for c in courses:
                console.print(
                    f"  • {c['id']}: {c['name']} ({c['topics_count']} topics)"
                )
            console.print("[dim]Использование: /export scorm <course_id>[/dim]")
            return True, None, None, True
        try:
            from scorm_export import export_scorm_package

            path = export_scorm_package(course_id, ".")
            console.print(f"[green]✅ SCORM пакет создан: {path}[/green]")
            return True, path, None, True
        except ValueError as e:
            console.print(f"[red]Ошибка: {e}[/red]")
            return False, str(e), None, True

    from memory import get_chat_history, init_db

    conn = init_db()
    history = get_chat_history(conn, limit=1000)
    if not history:
        console.print("[yellow]История пуста[/yellow]")
        return True, None, None, True
    console.print("[bold]=== История чата ===[/bold]")
    for msg in history[-50:]:
        console.print(f"[{msg['mode']}] {msg['role']}: {msg['content'][:200]}")
    console.print("[dim]Полная история сохранена в memory/chat_history.db[/dim]")
    return True, None, None, True


def handle_exploits_log(action: str) -> HandlerResult:
    """Показать лог эксплойтов."""
    from state import get_state

    state = get_state()
    logs = getattr(state, "exploit_success", [])
    if not logs:
        console.print("[yellow]Лог эксплойтов пуст[/yellow]")
        return True, None, None, True
    console.print(
        Panel(
            "\n".join(
                [
                    f"• {log.get('date', '?')} - {log.get('exploit', '')} - {'✅' if log.get('success') else '❌'}"
                    for log in logs[-10:]
                ]
            ),
            title="📜 История эксплойтов",
            border_style="cyan",
        )
    )
    return True, None, None, True


def handle_heatmap(action: str) -> HandlerResult:
    """Показать тепловую карту активности."""
    from state import get_state

    state = get_state()
    daily = getattr(state, "daily_command_counts", {})
    if not daily:
        console.print("[yellow]Нет данных об активности[/yellow]")
        return True, None, None, True
    last7 = list(daily.items())[-7:]
    lines = []
    for date, counts in last7:
        total = sum(counts.values()) if isinstance(counts, dict) else counts
        lines.append(f"{date}: {total} действий")
    console.print(
        Panel(
            "\n".join(lines),
            title="🔥 Активность (последние 7 дней)",
            border_style="yellow",
        )
    )
    return True, None, None, True


def handle_history(conn: Any) -> HandlerResult:
    """Показать историю чата (из БД)."""
    from memory import get_chat_history

    history = get_chat_history(conn, limit=20)
    if not history:
        console.print("[yellow]История пуста[/yellow]")
        return True, None, None, True
    for msg in history:
        console.print(f"[dim]{msg['role']}: {msg['content'][:100]}[/dim]")
    return True, None, None, True


def handle_model(action: str) -> HandlerResult:
    """Сменить модель Ollama (только для ollama)."""
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        from config import OLLAMA_MODEL

        console.print(f"[cyan]Текущая модель Ollama: {OLLAMA_MODEL}[/cyan]")
        console.print("[dim]Используйте: /model <имя_модели>[/dim]")
        return True, None, None, True
    new_model = parts[1].strip()
    import config

    config.OLLAMA_MODEL = new_model
    from config import LazyLoader

    LazyLoader._llm = None
    console.print(
        f"[green]Модель изменена на {new_model}. Следующий запрос загрузит её.[/green]"
    )
    return True, None, None, True


def handle_provider(action: str) -> HandlerResult:
    """Показать/сменить/протестировать провайдера LLM."""
    import config as _cfg
    from config import LazyLoader, PROVIDER_KNOWN_MODELS, FALLBACK_ORDER

    # action = "provider [subcmd [args]]"
    parts = action.strip().split(maxsplit=2)
    subcmd = parts[1].strip().lower() if len(parts) > 1 else ""

    if not subcmd:
        # Show current provider info
        llm = LazyLoader._llm
        status_info = ""
        if llm is not None:
            try:
                from resilient_llm import ResilientLLM

                if isinstance(llm, ResilientLLM):
                    st = llm.get_status()
                    for p in st.get("providers", []):
                        icon = "🟢" if p["circuit_state"] == "closed" else "🔴"
                        if p["is_current"]:
                            icon = "⭐"
                        status_info += f"\n  {icon} {p['model']} ({p['role']}) — {p['circuit_state']}, failures: {p['failures']}"
                else:
                    model = getattr(llm, "model", "?")
                    status_info = f"\n  {model} (single, без fallback)"
            except (ValueError, RuntimeError, AttributeError):
                pass

        chain = " → ".join(FALLBACK_ORDER)
        console.print(
            Panel(
                f"[bold]Текущий провайдер:[/bold] [cyan]{_cfg.LLM_PROVIDER}[/cyan]\n"
                f"[bold]Модель:[/bold] [cyan]{_cfg.OLLAMA_MODEL if _cfg.LLM_PROVIDER == 'ollama' else (_cfg.GROQ_MODEL if _cfg.LLM_PROVIDER == 'groq' else _cfg.OPENROUTER_MODEL)}[/cyan]\n"
                f"[bold]Fallback цепочка:[/bold] [dim]{chain}[/dim]"
                f"{status_info}",
                title="⚙️ Провайдер",
                border_style="cyan",
            )
        )
        console.print(
            "[dim]Команды: /provider list, /provider set <name>, /provider test, /provider models[/dim]"
        )
        return True, None, None, True

    if subcmd == "list":
        table = Table(title="Доступные провайдеры", border_style="cyan")
        table.add_column("Провайдер", style="bold")
        table.add_column("Статус", justify="center")
        table.add_column("Модель")
        table.add_column("Описание")

        for p in FALLBACK_ORDER:
            info = PROVIDER_KNOWN_MODELS.get(p, {})
            desc = info.get("description", "")
            model = ""
            status = "[dim]?[/dim]"

            if p == "ollama":
                model = _cfg.OLLAMA_MODEL
                import subprocess

                try:
                    r = subprocess.run(
                        ["ollama", "list"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,
                    )
                    status = (
                        "[green]✅[/green]" if r.returncode == 0 else "[red]❌[/red]"
                    )
                except FileNotFoundError:
                    status = "[red]❌[/red]"
            elif p == "groq":
                model = _cfg.GROQ_MODEL
                status = "[green]✅[/green]" if _cfg.GROQ_API_KEY else "[red]❌[/red]"
            elif p == "openrouter":
                model = _cfg.OPENROUTER_MODEL
                status = (
                    "[green]✅[/green]" if _cfg.OPENROUTER_API_KEY else "[red]❌[/red]"
                )
            elif p == "huggingface":
                model = _cfg.HUGGINGFACE_MODEL
                status = (
                    "[green]✅[/green]" if _cfg.HUGGINGFACE_API_KEY else "[dim]—[/dim]"
                )
            elif p == "lmstudio":
                model = _cfg.LMSTUDIO_MODEL
                import urllib.request
                import json as _json

                try:
                    req = urllib.request.Request(
                        f"{_cfg.LMSTUDIO_BASE_URL}/models", method="GET"
                    )
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        data = _json.loads(resp.read())
                        models = data.get("data", [])
                        if models:
                            model = models[0].get("id", _cfg.LMSTUDIO_MODEL)
                        status = "[green]✅[/green]"
                except (OSError, ValueError):
                    status = "[red]❌[/red]"
            elif p == "mock":
                status = "[green]✅[/green]"
                model = "mock-llm"

            is_current = " ←" if p == _cfg.LLM_PROVIDER else ""
            table.add_row(f"{p}{is_current}", status, model, desc)

        console.print(table)
        console.print(
            "[dim]Используйте /provider set <name> для смены провайдера[/dim]"
        )
        return True, None, None, True

    if subcmd == "models":
        provider_filter = parts[2].strip().lower() if len(parts) > 2 else ""
        table = Table(title="Поддерживаемые модели", border_style="cyan")
        table.add_column("Провайдер", style="bold")
        table.add_column("Модели (рекомендуемые)")

        for p, info in PROVIDER_KNOWN_MODELS.items():
            if provider_filter and p != provider_filter:
                continue
            models = ", ".join(info.get("suggested", []))
            docs = info.get("docs_url", "")
            name = p
            if p == _cfg.LLM_PROVIDER:
                name = f"{p} ← активный"
            table.add_row(name, models)
            if docs:
                table.add_row("", f"[dim]📚 {docs}[/dim]")

        # If we have a filter, show more details
        if provider_filter and provider_filter in PROVIDER_KNOWN_MODELS:
            info = PROVIDER_KNOWN_MODELS[provider_filter]
            console.print(
                Panel(
                    f"[bold]{provider_filter}[/bold]\n"
                    f"{info['description']}\n\n"
                    f"[bold]Модель по умолчанию:[/bold] {info['default']}\n"
                    f"[bold]Рекомендуемые:[/bold]\n"
                    + "\n".join(f"  • {m}" for m in info["suggested"])
                    + "\n\n"
                    f"[dim]📚 {info['docs_url']}[/dim]",
                    title=f"📦 {provider_filter}",
                    border_style="green",
                )
            )
            return True, None, None, True

        console.print(table)
        console.print("[dim]Подробнее: /provider models <provider>[/dim]")
        return True, None, None, True

    if subcmd == "test":
        console.print("[bold]🧪 Тестирование провайдеров...[/bold]")
        from resilient_llm import ResilientLLM
        from config import get_llm as _get_single_llm

        results_table = Table(title="Результаты тестирования", border_style="cyan")
        results_table.add_column("Провайдер", style="bold")
        results_table.add_column("Модель")
        results_table.add_column("Результат")
        results_table.add_column("Детали")

        for p in FALLBACK_ORDER:
            if p == "mock":
                results_table.add_row(
                    "mock", "mock-llm", "[green]✅[/green]", "Всегда доступен"
                )
                continue
            if p == _cfg.LLM_PROVIDER:
                continue  # skip primary, tested separately

            original = _cfg.LLM_PROVIDER
            _cfg.LLM_PROVIDER = p
            llm_instance = _get_single_llm()
            _cfg.LLM_PROVIDER = original

            if llm_instance is None:
                model = (
                    _cfg.GROQ_MODEL
                    if p == "groq"
                    else (
                        _cfg.OPENROUTER_MODEL
                        if p == "openrouter"
                        else _cfg.HUGGINGFACE_MODEL
                        if p == "huggingface"
                        else _cfg.OLLAMA_MODEL
                    )
                )
                results_table.add_row(
                    p, model, "[red]❌[/red]", "Не удалось инициализировать"
                )
                continue

            model = getattr(llm_instance, "model", "?")
            success, msg = ResilientLLM.test_provider(p, llm_instance, timeout=15)
            if success:
                results_table.add_row(p, model, "[green]✅[/green]", msg)
            else:
                results_table.add_row(p, model, "[red]❌[/red]", msg[:60])

        # Test current primary
        primary_llm = _get_single_llm()
        if primary_llm:
            model = getattr(primary_llm, "model", "?")
            success, msg = ResilientLLM.test_provider(
                _cfg.LLM_PROVIDER, primary_llm, timeout=15
            )
            icon = "[green]✅[/green]" if success else "[red]❌[/red]"
            results_table.add_row(
                f"{_cfg.LLM_PROVIDER} (primary)", model, icon, msg[:60]
            )

        console.print(results_table)
        console.print(
            "[dim]Тест отправляет 'ping' каждому провайдеру с таймаутом 15с[/dim]"
        )
        return True, None, None, True

    if subcmd.startswith("set") or subcmd.startswith("switch"):
        # /provider set ollama or /provider switch ollama
        arg_parts = subcmd.split(maxsplit=1)
        provider_name = arg_parts[1].strip().lower() if len(arg_parts) > 1 else ""
        if not provider_name:
            console.print("[red]Укажите имя провайдера: /provider set ollama[/red]")
            return True, None, None, True
        if provider_name not in FALLBACK_ORDER:
            valid = ", ".join(FALLBACK_ORDER)
            console.print(
                f"[red]Неизвестный провайдер '{provider_name}'. Доступны: {valid}[/red]"
            )
            return True, None, None, True
        _cfg.LLM_PROVIDER = provider_name
        LazyLoader.invalidate()
        console.print(
            f"[green]✅ Провайдер изменён на {provider_name}.[/green]\n"
            f"[dim]Следующий запрос загрузит {PROVIDER_KNOWN_MODELS.get(provider_name, {}).get('description', provider_name)}.[/dim]"
        )
        return True, None, None, True

    # Direct provider name as subcmd (backward compat): /provider ollama
    if subcmd in FALLBACK_ORDER or subcmd == "mock":
        _cfg.LLM_PROVIDER = subcmd
        LazyLoader.invalidate()
        console.print(
            f"[green]✅ Провайдер изменён на {subcmd}.[/green]\n"
            f"[dim]Следующий запрос загрузит {PROVIDER_KNOWN_MODELS.get(subcmd, {}).get('description', subcmd)}.[/dim]"
        )
        return True, None, None, True

    if subcmd in ("status", "info"):
        # Reuse the no-arg display
        return handle_provider("provider")

    console.print(f"[red]Неизвестная команда: /provider {subcmd}[/red]")
    console.print(
        "[dim]Доступно: /provider, /provider list, /provider set <name>, /provider test, /provider models [name][/dim]"
    )
    return True, None, None, True


def handle_repeat(action: str) -> HandlerResult:
    """Интерактивное повторение по расписанию SM-2."""
    from state import get_state

    state = get_state()
    due = state.get_due_reviews()
    if not due:
        console.print("[green]Нет тем, готовых к повторению[/green]")
        return True, None, None, True
    console.print(f"[cyan]Доступно для повторения: {len(due)} тем[/cyan]")
    for idx, item in enumerate(due[:5], 1):
        interval = item.get("interval", 0)
        reps = item.get("repetitions", 0)
        console.print(
            f"  {idx}. {item['topic']} (интервал: {interval}д, повторений: {reps})"
        )
    console.print("[dim]Используйте /quiz для прохождения квиза по слабым темам[/dim]")
    return True, None, None, True


def handle_risk(action: str) -> HandlerResult:
    """Показать уровень риска."""
    from state import get_state

    state = get_state()
    console.print(
        f"⚠️ Текущий уровень риска: {state.risk_level}/100 - {state.get_risk_status()}"
    )
    return True, None, None, True


def handle_noise(action: str) -> HandlerResult:
    """Показать уровень шумности."""
    from handlers.noise import get_noise_level

    info = get_noise_level()
    bar = _make_bar(info["level"], 100, 20)
    stealth = "✅" if info["stealth"] else "❌"
    console.print(
        Panel(
            f"Шум: {info['level']}/100 {bar}\n"
            f"Статус: {info['status']}\n"
            f"Stealth mode: {stealth}\n"
            f"Используй /stealth для снижения шума.",
            title="📊 Noise Level",
            border_style="yellow",
        )
    )
    return True, None, None, True


def handle_trace(action: str) -> HandlerResult:
    """Показать статус трассировки."""
    from handlers.trace import get_trace_status

    info = get_trace_status()
    if not info["active"]:
        console.print(
            Panel("Нет активной трассировки.", title="🔍 Trace", border_style="green")
        )
    elif info["expired"]:
        console.print(
            Panel(
                f"⚠️ Трассировка истекла! {info['target']} засёк вторжение.",
                title="🔍 Trace",
                border_style="red",
            )
        )
    else:
        bar = _make_bar(info["remaining_seconds"], 180, 20)
        console.print(
            Panel(
                f"Цель: {info['target']}\n"
                f"Осталось: {info['remaining_minutes']} мин {bar}\n"
                f"Срочно заверши лабу!",
                title="🔍 Trace Timer",
                border_style="red",
            )
        )
    return True, None, None, True


def handle_check_logs(action: str) -> HandlerResult:
    """Показать грязные логи."""
    from handlers.logs import check_logs

    info = check_logs()
    if info["count"] == 0:
        console.print(
            Panel(
                "Логи чисты. Watchers ничего не увидят.",
                title="🧹 Dirty Logs",
                border_style="green",
            )
        )
    else:
        lines = [f"Всего записей: {info['count']}"]
        for log in info["logs"]:
            lines.append(f"  • {log['source']}: {log['detail']} ({log['time_ago']})")
        lines.append("\nИспользуй /wipe_logs для очистки.")
        console.print(
            Panel("\n".join(lines), title="🧹 Dirty Logs", border_style="yellow")
        )
    return True, None, None, True


def handle_wipe_logs(action: str) -> HandlerResult:
    """Очистить грязные логи."""
    from handlers.logs import wipe_logs

    result = wipe_logs()
    console.print(Panel(result, title="🧹 Wipe Logs", border_style="green"))
    return True, None, None, True


def handle_stealth(action: str) -> HandlerResult:
    """Включить/выключить stealth mode."""
    from handlers.noise import toggle_stealth

    result = toggle_stealth()
    status = "✅" if result["active"] else "❌"
    console.print(
        Panel(
            f"Stealth: {status}\n{result['message']}",
            title="🥷 Stealth Mode",
            border_style="blue",
        )
    )
    return True, None, None, True


def handle_debts(action: str) -> HandlerResult:
    """Показать цифровые долги."""
    from handlers.debt import get_debts

    info = get_debts()
    status_icons = {"clean": "✅", "light": "⚠️", "warning": "⚠️⚠️", "critical": "🚨"}
    icon = status_icons.get(info["status"], "❓")
    lines = [f"Всего долгов: {info['total']} {icon}"]
    for d in info["details"]:
        lines.append(f"  • {d}")
    if info["total"] >= 5:
        lines.append("\n🚨 Учитель расстроен. Подсказки отключены до погашения долгов.")
    elif info["total"] >= 3:
        lines.append("\n⚠️ Учитель начинает нервничать. Закрывай долги.")
    console.print(
        Panel("\n".join(lines), title="💳 Digital Debts", border_style="magenta")
    )
    return True, None, None, True


def handle_faction(action: str) -> HandlerResult:
    """Показать/выбрать фракцию."""
    from handlers.faction import get_factions, choose_faction

    FACTION_NAMES = {"rick": "Rick", "ghost": "Ghost", "archive": "Archive"}
    parts = action.strip().split()
    if len(parts) > 1 and parts[0] == "faction":
        sub = parts[1].lower()
        if sub in FACTION_NAMES:
            result = choose_faction(sub)
            console.print(Panel(result, title="🏴 Faction", border_style="cyan"))
        elif sub == "info":
            info = get_factions()
            dom = FACTION_NAMES.get(info["dominant"], "—")
            console.print(
                Panel(
                    f"Rick: {info['rick']} rep\nGhost: {info['ghost']} rep\nArchive: {info['archive']} rep\n"
                    f"Доминирует: {dom}\nВыбрана: {info['chosen'] or '—'}\n\n"
                    f"Используй /faction rick, ghost или archive для выбора.",
                    title="🏴 Factions",
                    border_style="cyan",
                )
            )
        else:
            choices = ", ".join(f"/faction {k}" for k in FACTION_NAMES)
            console.print(f"[yellow]Используй: /faction info, {choices}[/yellow]")
    else:
        info = get_factions()
        rep_line = f"Rick: {info['rick']} | Ghost: {info['ghost']} | Archive: {info['archive']}"
        console.print(Panel(rep_line, title="🏴 Factions", border_style="cyan"))
    return True, None, None, True


def handle_echo(action: str) -> HandlerResult:
    """Показать случайное echo-сообщение."""
    from handlers.echo import get_echo_message

    msg = get_echo_message(force=True)
    console.print(
        Panel(f"[dim][Echo][/dim] {msg}", title="👻 Echo", border_style="blue")
    )
    return True, None, None, True


def handle_memory(action: str) -> HandlerResult:
    """Показать воспоминания учителя."""
    from handlers.memory import get_random_memory
    from state import get_state

    state = get_state()
    memories = getattr(state, "student_memories", [])
    if not memories:
        console.print("[yellow]У учителя пока нет воспоминаний о тебе.[/yellow]")
    else:
        lines = [f"  {i + 1}. {m}" for i, m in enumerate(memories[-10:])]
        random_mem = get_random_memory()
        if random_mem:
            lines.insert(0, f"\n📝 Случайное: {random_mem}\n")
        console.print(
            Panel("\n".join(lines), title="🧠 Память учителя", border_style="magenta")
        )
    return True, None, None, True


def _make_bar(value: int, max_val: int, width: int = 20) -> str:
    """Создать ASCII progress bar."""
    filled = min(int(value / max_val * width), width)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}]"


def handle_set_api_key(action: str) -> HandlerResult:
    """Установить API ключ для провайдера."""
    parts = action.split(maxsplit=2)
    if len(parts) < 3:
        console.print("[red]Использование: /set-api-key <provider> <key>[/red]")
        console.print("[dim]Пример: /set-api-key openrouter sk-xxx[/dim]")
        return True, None, None, True
    provider = parts[1].lower()
    key = parts[2].strip()
    if provider == "openrouter":
        os.environ["OPENROUTER_API_KEY"] = key
        console.print("[green]Ключ OpenRouter установлен (временно)[/green]")
    elif provider == "groq":
        os.environ["GROQ_API_KEY"] = key
        console.print("[green]Ключ Groq установлен (временно)[/green]")
    elif provider == "huggingface":
        os.environ["HF_TOKEN"] = key
        console.print("[green]Токен HuggingFace установлен (временно)[/green]")
    else:
        console.print(
            f"[red]Провайдер {provider} не поддерживается для установки ключа[/red]"
        )
    from config import LazyLoader

    LazyLoader._llm = None
    return True, None, None, True


def handle_state(action: str) -> HandlerResult:
    """Управление состоянием (экспорт/импорт)."""
    from state import get_state

    parts = action.split(maxsplit=1)
    subcmd = parts[1].strip() if len(parts) > 1 else ""
    if subcmd == "save":
        get_state().save_to_file()
        console.print("[green]Состояние сохранено[/green]")
    elif subcmd == "load":
        get_state().load_from_file()
        console.print("[green]Состояние загружено[/green]")
    elif subcmd == "migrate":
        console.print(
            "[yellow]Миграция состояния в БД: используйте /state migrate to-db[/yellow]"
        )
    else:
        console.print("[yellow]Доступно: /state save, /state load[/yellow]")
    return True, None, None, True


def handle_story_mode(action: str) -> HandlerResult:
    """Обработчик команды /story (исправленный)."""
    parts = action.strip().split()
    if not parts:
        console.print(
            Panel(
                "[yellow]Используйте: /story list, /story start <id>, /story submit <flag>, /story achievements[/yellow]"
            )
        )
        return True, None, None, True

    cmd = parts[0].lower()

    if cmd in ("list", "episodes", "chapters"):
        try:
            from story_mode import get_story_list

            console.print(
                Panel(get_story_list(), title="📖 Story Mode", border_style="cyan")
            )
        except Exception as e:
            console.print(f"[red]Ошибка загрузки story mode: {e}[/red]")
        return True, None, None, True

    if cmd in ("start", "chapter"):
        if len(parts) < 2 or not parts[1].isdigit():
            console.print("[red]Укажите номер: /story chapter 1[/red]")
            return True, None, None, True
        target_id = int(parts[1])
        if cmd == "chapter":
            from story_mode import start_chapter

            result = start_chapter(target_id)
            title = "📖 Начало главы"
        else:
            from story_mode import start_story_mode

            result = start_story_mode(target_id)
            title = "🎬 Начало эпизода"
        try:
            console.print(Panel(result, title=title, border_style="green"))
        except Exception as e:
            console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

    if cmd == "submit":
        if len(parts) < 2:
            console.print("[red]Укажите флаг: /story submit FLAG{...}[/red]")
            return True, None, None, True
        flag = " ".join(parts[1:])
        try:
            from story_mode import submit_flag

            console.print(
                Panel(submit_flag(flag), title="🏆 Результат", border_style="yellow")
            )
        except Exception as e:
            console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

    if cmd == "achievements":
        try:
            from story_mode import get_achievements_list

            console.print(
                Panel(
                    get_achievements_list(),
                    title="🏅 Достижения",
                    border_style="magenta",
                )
            )
        except Exception as e:
            console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

    console.print(
        "[red]Неизвестная подкоманда. Доступные: list, chapter <n>, start <id>, submit <flag>, achievements[/red]"
    )
    return True, None, None, True


def handle_final_choice(action: str) -> HandlerResult:
    """Обработчик команды /final."""
    parts = action.strip().split()
    if len(parts) < 2:
        console.print(
            Panel(
                "Выбери путь:\n  /final memory — Сохранить учителя как архив\n"
                "  /final merge — Слияние с учителем\n"
                "  /final rewrite — Переписать учителя (нужно 6 артефактов)",
                title="⚡ Финальный выбор",
                border_style="red",
            )
        )
        return True, None, None, True
    from story_mode import final_choice

    path = parts[1].lower()
    result = final_choice(path)
    console.print(Panel(result, title="⚡ Финальный выбор", border_style="red"))
    return True, None, None, True


def handle_timeline_action(action: str) -> HandlerResult:
    """Обработчик команды /timeline."""
    parts = action.strip().split()
    if len(parts) > 1:
        era = parts[1].lower()
        eras = {
            "1980s": "• 1983: Первый фильм с хакерами 'WarGames'\n• 1988: Червяк Морриса заразил 10% интернета",
            "1990s": "• 1994: SSL 1.0\n• 1999: Вирус Melissa, основание Honeynet Project",
            "2000s": "• 2000: Mafiaboy атакует Yahoo\n• 2007: Кибератаки на Эстонию",
            "2010s": "• 2013: Утечка Target (40 млн карт)\n• 2017: WannaCry, NotPetya",
            "2020s": "• 2020: SolarWinds\n• 2021: Colonial Pipeline",
        }
        if era in eras:
            console.print(
                Panel(eras[era], title=f"📅 Эпоха {era}", border_style="green")
            )
        else:
            console.print(
                "[red]Неизвестная эпоха. Доступны: 1980s, 1990s, 2000s, 2010s, 2020s[/red]"
            )
    else:
        timeline = """[bold cyan]📅 Хронология кибербезопасности[/bold cyan]

[bold]1980-е[/bold] — Зарождение вирусов (Brain, Morris worm)
[bold]1990-е[/bold] — Эра хакерских атак, появление антивирусов
[bold]2000-е[/bold] — Киберпреступность, черви (Code Red, SQL Slammer)
[bold]2010-е[/bold] — APT-группы, утечки данных, ransomware
[bold]2020-е[/bold] — Supply chain attacks, AI в кибербезопасности

Подробнее: /timeline 1990s"""
        console.print(Panel(timeline, title="Timeline", border_style="cyan"))
    return True, None, None, True


def handle_terminal_log(action: str = "") -> HandlerResult:
    """Показать лог терминала."""
    from terminal_log import get_terminal_log

    log = get_terminal_log(last_n=30)
    console.print(
        Panel(log if log else "Лог пуст", title="💻 Терминал", border_style="yellow")
    )
    return True, None, None, True


def handle_topics(action: str) -> HandlerResult:
    """Показать темы текущего курса."""
    from state import get_state

    state = get_state()
    course = state.current_course
    if not course:
        console.print("[yellow]Курс не выбран. Используйте /courses[/yellow]")
        return True, None, None, True
    from courses import COURSES

    course_data = COURSES.get(course)
    if not course_data:
        console.print("[red]Курс не найден[/red]")
        return True, None, None, True
    topics = course_data.get("topics", [])
    console.print(f"[bold]Темы курса '{course_data.get('name', course)}':[/bold]")
    for idx, topic in enumerate(topics, 1):
        status = "✅" if topic.get("completed") else "⬜"
        console.print(f"{status} {idx}. {topic.get('name')}")
    return True, None, None, True


def handle_usage(action: str) -> HandlerResult:
    """Статистика использования команд."""
    from state import get_state

    state = get_state()
    usage = getattr(state, "command_usage", {})
    if not usage:
        console.print("[yellow]Нет данных об использовании команд[/yellow]")
        return True, None, None, True
    sorted_cmds = sorted(usage.items(), key=lambda x: x[1], reverse=True)[:15]
    lines = [f"{cmd}: {count}" for cmd, count in sorted_cmds]
    console.print(
        Panel("\n".join(lines), title="📊 Использование команд", border_style="cyan")
    )
    return True, None, None, True


def handle_version() -> HandlerResult:
    """Показать версию."""
    console.print("[bold]CyberTeacher v5.0 (2026-05-23)[/bold]")
    return True, None, None, True


def handle_writeup() -> HandlerResult:
    """Показать шаблон writeup."""
    template = """# Write-up

## Информация
- **Дата:**
- **Категория:**
- **Сложность:**

## Описание

## Решение

### 1. Разведка

### 2. Эксплуатация

### 3. Получение доступа

## Выводы
"""
    console.print(Panel(template, title="📝 Шаблон writeup", border_style="green"))
    return True, None, None, True


def handle_course(action: str) -> HandlerResult:
    """Обработчик команд /courses и /course."""
    parts = action.strip().split()
    if not parts or parts[0] in ("courses", "list"):
        course_list = list_courses()
        console.print(
            Panel(course_list, title="📚 Доступные курсы", border_style="cyan")
        )
        return True, None, None, True

    subcmd = parts[0].lower()
    if subcmd == "start" and len(parts) > 1:
        course_id = parts[1]
        result = start_course(course_id)
        console.print(Panel(result, title="🚀 Запуск курса", border_style="green"))
        return True, None, None, True

    if subcmd == "progress" and len(parts) > 1:
        course_id = parts[1]
        state = get_state()
        current_topic = state.course_progress.get(course_id, 0)
        result = get_course_progress(course_id, current_topic)
        console.print(Panel(result, title="📈 Прогресс курса", border_style="blue"))
        return True, None, None, True

    console.print("[yellow]Использование:[/yellow]")
    console.print("  /courses или /course list - показать список курсов")
    console.print("  /course start <id> - начать курс")
    console.print("  /course progress <id> - показать прогресс")
    return True, None, None, True


def handle_writeups(action: str) -> HandlerResult:
    """Показать список сохранённых writeup'ов."""
    writeup_dir = "./writeups"
    if not os.path.exists(writeup_dir):
        os.makedirs(writeup_dir, exist_ok=True)
        console.print("[yellow]Нет сохранённых writeup'ов[/yellow]")
        return True, None, None, True
    files = [f for f in os.listdir(writeup_dir) if f.endswith(".md")]
    if not files:
        console.print("[yellow]Нет сохранённых writeup'ов[/yellow]")
        return True, None, None, True
    console.print("[bold]Сохранённые writeup'ы:[/bold]")
    for f in sorted(files, reverse=True):
        console.print(f"  • {f}")
    return True, None, None, True


def handle_ghost_log(action: str) -> HandlerResult:
    """Обработчик /ghost_log [list|random|<id>] — скрытый лог (Глава 1)."""
    from handlers.ghost_log import handle_ghost_log as ghost_log_handler

    args = action.strip()
    if args == "ghost_log":
        args = ""
    else:
        args = args[len("ghost_log"):].strip()

    result = ghost_log_handler(args)
    console.print(result)
    return True, None, None, True


def handle_backdoor(action: str) -> HandlerResult:
    """Обработчик /backdoor [list|info <id>|remove <id>|random] — бэкдоры (Глава 5)."""
    from handlers.backdoor import handle_backdoor as backdoor_handler

    args = action.strip()
    if args == "backdoor":
        args = ""
    else:
        args = args[len("backdoor"):].strip()

    result = backdoor_handler(args)
    console.print(result)
    return True, None, None, True


def handle_stability(action: str) -> HandlerResult:
    """Обработчик /stability [status|damage <amount>|heal <amount>] — World Stability (Глава 7)."""
    from state import get_state

    state = get_state()
    parts = action.strip().split()
    sub = parts[1].lower() if len(parts) > 1 else "status"

    if sub == "status":
        status = state.get_world_stability_status()
        console.print(f"[bold]World Stability:[/bold] {state.world_stability}/100 — {status}")
        return True, None, None, True

    if sub == "damage" and len(parts) > 2:
        try:
            amount = int(parts[2])
            state.adjust_world_stability(-abs(amount))
            console.print(f"[red]World Stability damaged by {amount}. Current: {state.world_stability}[/red]")
        except ValueError:
            console.print("[red]Invalid amount[/red]")
        return True, None, None, True

    if sub == "heal" and len(parts) > 2:
        try:
            amount = int(parts[2])
            state.adjust_world_stability(abs(amount))
            console.print(f"[green]World Stability healed by {amount}. Current: {state.world_stability}[/green]")
        except ValueError:
            console.print("[red]Invalid amount[/red]")
        return True, None, None, True

    console.print("[yellow]Usage: /stability [status|damage <amount>|heal <amount>][/yellow]")
    return True, None, None, True


def handle_teacher_sleep(action: str) -> HandlerResult:
    """Обработчик /teacher_sleep [status|secret] — Teacher Sleep 4AM (Глава 7)."""
    from state import get_state

    state = get_state()
    parts = action.strip().split()
    sub = parts[1].lower() if len(parts) > 1 else "status"

    if sub == "status":
        status = state.get_teacher_sleep_status()
        console.print(f"[bold]Teacher Sleep:[/bold] {status}")
        if state.is_teacher_sleeping():
            console.print("[dim]Доступен /teacher_sleep secret для скрытых логов[/dim]")
        return True, None, None, True

    if sub == "secret":
        if state.can_access_secret_logs():
            console.print("[bold cyan]🌙 SECRET LOGS (4:00 AM):[/bold cyan]")
            console.print("  [REDACTED] — Учитель не видит. Это твоё окно.")
            console.print("  Логи учителя за сегодня: ...")
            console.print("  [dim]Доступно только в 4:00 AM[/dim]")
        else:
            console.print("[red]Учитель не спит. Попробуй в 4:00 AM.[/red]")
        return True, None, None, True

    console.print("[yellow]Usage: /teacher_sleep [status|secret][/yellow]")
    return True, None, None, True


def handle_faiss_watch(action: str) -> HandlerResult:
    """Обработчик /faiss_watch [start|stop|status] — автопереиндексация FAISS."""
    parts = action.strip().split()
    sub = parts[1].lower() if len(parts) > 1 else "status"

    if sub == "start":
        console.print("[bold cyan]🔄 Запуск FAISS Watcher...[/bold cyan]")
        console.print("[dim]Наблюдение за изменениями в проекте. Ctrl+C для остановки.[/dim]")
        try:
            from faiss_watcher import run_watcher
            run_watcher()
        except KeyboardInterrupt:
            console.print("[yellow]Watcher остановлен[/yellow]")
        except ImportError:
            console.print("[red]watchdog не установлен: pip install watchdog[/red]")
        except Exception as e:
            console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

    if sub == "status":
        console.print("[dim]FAISS Watcher: не запущен (команда /faiss_watch start для запуска)[/dim]")
        return True, None, None, True

    console.print("[yellow]Usage: /faiss_watch [start|status][/yellow]")
    return True, None, None, True
