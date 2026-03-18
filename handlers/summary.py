# handlers/summary.py
import os
import time
from typing import Any, Dict, Optional, Tuple

from rich.console import Console
from rich.panel import Panel

console = Console()


def handle_summary(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Генерация структурированного конспекта в Markdown по заданной теме."""
    try:
        parts = action.split(maxsplit=1)
        if len(parts) < 2:
            console.print("[cyan]Введите тему для конспекта:[/cyan]")
            topic = input("> ").strip()
            if not topic:
                console.print("[yellow]Отменено[/yellow]")
                return True, None, None, True
        else:
            topic = parts[1].strip()

        console.print(f"[cyan]Генерация конспекта по теме: {topic}[/cyan]")

        try:
            from config import RERANK_TOP_K, LazyLoader
            from knowledge import get_current_vectordb, get_relevant_docs

            vectordb = get_current_vectordb()
            if not vectordb:
                console.print("[red]База знаний не доступна[/red]")
                return True, None, None, True

            docs = get_relevant_docs(vectordb, topic, k=RERANK_TOP_K * 2)

            if not docs:
                console.print("[yellow]Не найдено документов по этой теме[/yellow]")
                console.print("[dim]Добавьте PDF в knowledge_base/[/dim]")
                return True, None, None, True

            context = "\n\n".join(
                [
                    f"Источник {i + 1}:\n{doc.page_content[:2000]}"
                    for i, doc in enumerate(docs[:5])
                ]
            )

            prompt = f"""Ты — эксперт по кибербезопасности. Создай структурированный конспект в Markdown по теме: "{topic}".

Контекст из учебных материалов:

{context}

Конспект должен включать:
1. **Определение** — кратко что это такое
2. **Ключевые концепции** — основные идеи, механизмы
3. **Примеры** — реальные или гипотетические примеры
4. **Техники/Инструменты** — если применимо
5. **Ссылки на источники** — укажи, какие источники использовались (из контекста)

Формат: Markdown с заголовками ##, списками, код-блоками где уместно.
Не добавляй введение или заключение — сразу приступай к делу.
"""

            llm = LazyLoader.get_llm()
            console.print("[dim]Генерация конспекта...[/dim]")
            response = llm.invoke(prompt)
            summary = (
                response.content if hasattr(response, "content") else str(response)
            )

            console.print("\n[bold green]Конспект сгенерирован:[/bold green]\n")
            console.print(
                Panel(
                    summary,
                    title=f"Конспект: {topic}",
                    border_style="cyan",
                    expand=True,
                )
            )

            console.print("\n[yellow]Сохранить конспект в файл? (y/n)[/yellow]")
            try:
                save = input("> ").strip().lower()
                if save in ("y", "yes", "д", "да"):
                    filename = (
                        f"summary_{topic.replace(' ', '_')}_{int(time.time())}.md"
                    )
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"# Конспект: {topic}\n\n")
                        f.write(summary)
                    console.print(f"[green]Конспект сохранён: {filename}[/green]")
            except KeyboardInterrupt:
                console.print("\n[yellow]Отмена сохранения[/yellow]")

            return True, None, None, True

        except Exception as e:
            console.print(f"[red]Ошибка при генерации: {e}[/red]")
            import traceback

            traceback.print_exc()
            return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback

        traceback.print_exc()
        return True, None, None, True
