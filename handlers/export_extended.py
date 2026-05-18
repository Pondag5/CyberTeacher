"""Модуль расширенного экспорта диалога (PDF/HTML).

Команды:
    /export extended <format> [file] — Экспорт в PDF/HTML/Markdown
"""

import os
from datetime import datetime
from typing import Tuple

from rich.panel import Panel

from di import get_context
from memory import get_chat_history
from ui import console


def _export_html(conn, filepath: str = None) -> bool:
    """Экспорт истории чата в HTML."""
    if not filepath:
        filepath = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    try:
        history = get_chat_history(conn)
        html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberTeacher - Chat Export</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #00ff88; text-align: center; }
        .message { margin: 10px 0; padding: 10px 15px; border-radius: 8px; }
        .user { background: #16213e; border-left: 3px solid #00ff88; }
        .assistant { background: #0f3460; border-left: 3px solid #e94560; }
        .timestamp { color: #888; font-size: 0.8em; }
        .meta { text-align: center; color: #666; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 CyberTeacher - История диалога</h1>
"""
        for msg in history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            ts = msg.get("timestamp", "")
            css_class = "user" if role == "user" else "assistant"
            html_content += f'<div class="message {css_class}"><div class="timestamp">{ts}</div><p>{content}</p></div>\n'

        html_content += f"""
        <div class="meta">Экспортировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>
</body>
</html>"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        console.print(Panel(
            f"[green]✅ Экспорт в HTML завершён:[/green] {filepath}\n"
            f"[bold]Сообщений:[/bold] {len(history)}",
            border_style="green",
        ))
        return True
    except Exception as e:
        console.print(f"[red]Ошибка экспорта HTML: {e}[/red]")
        return False


def _export_pdf(conn, filepath: str = None) -> bool:
    """Экспорт истории чата в PDF (через HTML + weasyprint или fpdf2)."""
    if not filepath:
        filepath = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    try:
        # Попытка использовать fpdf2
        from fpdf import FPDF

        history = get_chat_history(conn)

        class PDF(FPDF):
            def header(self):
                self.set_font("Helvetica", "B", 12)
                self.cell(0, 10, "CyberTeacher - Chat Export", new_x="LMARGIN", new_y="NEXT", align="C")

            def footer(self):
                self.set_y(-15)
                self.set_font("Helvetica", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        for msg in history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:500]  # Лимит длины
            label = "User" if role == "user" else "Assistant"
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(0, 128, 0) if role == "user" else pdf.set_text_color(128, 0, 0)
            pdf.cell(0, 8, label, new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 9)
            pdf.multi_cell(0, 5, content)
            pdf.ln(3)

        pdf.output(filepath)

        console.print(Panel(
            f"[green]✅ Экспорт в PDF завершён:[/green] {filepath}\n"
            f"[bold]Сообщений:[/bold] {len(history)}",
            border_style="green",
        ))
        return True
    except ImportError:
        console.print("[yellow]fpdf2 не установлен. Установите: pip install fpdf2[/yellow]")
        console.print("[dim]Попробуйте /export extended html вместо PDF.[/dim]")
        return False
    except Exception as e:
        console.print(f"[red]Ошибка экспорта PDF: {e}[/red]")
        return False


def handle_export_extended(args: str) -> tuple[str, bool]:
    """Обработчик расширенного экспорта."""
    parts = args.strip().split(maxsplit=2)
    if len(parts) < 2:
        console.print(Panel(
            "[bold]Расширенный экспорт:[/bold]\n"
            "/export extended html [file]  — Экспорт в HTML\n"
            "/export extended pdf [file]   — Экспорт в PDF (требуется fpdf2)",
            border_style="yellow",
        ))
        return "", True

    fmt = parts[1].lower()
    filepath = parts[2] if len(parts) > 2 else None

    ctx = get_context()
    conn = ctx.db_conn

    if fmt == "html":
        success = _export_html(conn, filepath)
        return "", success
    elif fmt == "pdf":
        success = _export_pdf(conn, filepath)
        return "", success
    else:
        console.print(f"[red]Неизвестный формат: {fmt}. Доступны: html, pdf[/red]")
        return "", True
