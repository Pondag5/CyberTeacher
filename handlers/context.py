"""Context Budget Manager CLI handler — /context command."""

from typing import Any, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from di import get_context
from handlers.types import HandlerResult


console = Console()


def handle_context(action: str) -> HandlerResult:
    """Handle /context command.

    Commands:
        /context stats  — show context budget stats
        /context clear  — clear chat history
    """
    parts = action.split(maxsplit=1)
    subcmd = parts[1].strip() if len(parts) > 1 else "stats"

    if subcmd == "stats":
        return _show_stats()
    elif subcmd == "clear":
        return _clear_context()
    else:
        console.print("[cyan]Использование:[/cyan]")
        console.print("  /context stats — статистика контекстного бюджета")
        console.print("  /context clear — очистить историю чата")
        return True, None, None, True


def _show_stats() -> HandlerResult:
    """Show context budget statistics."""
    ctx = get_context()
    state = ctx.state

    from memory import get_chat_history
    from db import init_db

    conn = init_db()
    history = get_chat_history(conn, limit=100)

    msg_count = len(history)
    total_chars = sum(len(m.get("content", "")) for m in history)
    avg_chars = total_chars // max(1, msg_count)

    table = Table(title="Context Budget Stats", border_style="cyan")
    table.add_column("Параметр", style="bold")
    table.add_column("Значение", style="green")

    table.add_row("Сообщений в истории", str(msg_count))
    table.add_row("Всего символов", f"{total_chars:,}")
    table.add_row("Средний размер сообщения", f"{avg_chars:,} символов")
    table.add_row("Лимит сообщений (cleanup)", "500")
    table.add_row("Auto-summarize интервал", "20 сообщений")

    summary_count = getattr(state, "_msg_count_since_summary", 0)
    table.add_row("Сообщений до auto-summary", str(summary_count))

    console.print(table)

    # Budget estimation
    from context_budget import CHARS_PER_TOKEN

    est_tokens = total_chars // CHARS_PER_TOKEN
    console.print(
        f"\n[dim]~{est_tokens:,} токенов в истории "
        f"(~{total_chars:,} символов / {CHARS_PER_TOKEN})[/dim]"
    )
    console.print(
        "[dim]Budget manager автоматически обрезает историю, "
        "если она превышает лимит контекстного окна.[/dim]"
    )

    return True, None, None, True


def _clear_context() -> HandlerResult:
    """Clear chat history."""
    from db import init_db
    from sqlalchemy import text

    conn = init_db()
    conn.execute(text("DELETE FROM messages"))
    conn.commit()

    console.print("[green]✅ История чата очищена.[/green]")
    return True, None, None, True
