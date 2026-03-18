# handlers/writeup_auto.py
import os
import time
from typing import Any, Dict, Optional, Tuple

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()


def handle_auto_writeup(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Автоматическая генерация writeup на основе последней завершённой активности (квиз/задание/эпизод)."""
    try:
        state = get_state()
        activity = state.last_writeup_activity

        if not activity:
            console.print(
                "[yellow]Нет данных для генерации writeup. Сначала пройдите квиз или задание.[/yellow]"
            )
            return True, None, None, True

        console.print(
            f"[cyan]Генерация writeup для активности: {activity['type']} ({activity.get('topic', activity.get('category', 'unknown'))})[/cyan]"
        )

        # Подготовить контекст из базы знаний по теме
        try:
            from config import RERANK_TOP_K, LazyLoader
            from knowledge import get_current_vectordb, get_relevant_docs

            topic = activity.get("topic") or activity.get("category")
            if not topic:
                console.print("[red]Не указана тема в активности[/red]")
                return True, None, None, True

            vectordb = get_current_vectordb()
            if vectordb:
                docs = get_relevant_docs(vectordb, topic, k=RERANK_TOP_K)
                context = "\n\n".join(
                    [
                        f"Источник {i + 1}:\n{doc.page_content[:1500]}"
                        for i, doc in enumerate(docs[:3])
                    ]
                )
            else:
                context = "База знаний недоступна."

            # Сформировать промпт для writeup
            act_type = activity["type"]
            if act_type == "quiz":
                summary_intro = f"Квиз по теме '{topic}'. Общий балл: {activity['total_score']}/{activity['max_total']} ({activity['success_rate']:.1f}%)."
                questions_text = "\n".join(
                    [
                        f"Вопрос {idx + 1}: {resp['question']}\n  Ваш ответ: {resp['user_answer']}\n  Верный ответ: {resp['correct_answer']}\n  Результат: {resp['score']}/10 - {resp['feedback']}"
                        for idx, resp in enumerate(activity.get("responses", []))
                    ]
                )
            elif act_type == "task":
                summary_intro = (
                    f"Практическое задание по категории '{activity['category']}'."
                )
                questions_text = f"Вопрос: {activity['question']}\nВаш ответ: {activity['user_answer']}\nВерный ответ: {activity['correct_answer']}\nРезультат: {activity['score']}/10 - {activity['feedback']}"
            else:
                summary_intro = f"Активность типа: {act_type}"
                questions_text = str(activity)

            prompt = f"""Ты — эксперт по кибербезопасности. На основе данных учебной сессии создай структурированный writeup в Markdown.

Данные сессии:
{summary_intro}

Подробности:
{questions_text}

Дополнительный контекст из учебных материалов (если есть):
{context}

Структура writeup:
1. **Цель** — что было нужно сделать/изучить
2. **Действия** — шаги, которые предпринял ученик (основано на ответах)
3. **Результат** — итоги, оценка, что получилось
4. **Анализ** — почему ответы верные/неверные, объяснение с точки зрения теории
5. **Рекомендации** — что повторить, изучить дополнительно
6. **Ссылки** — какие источники из контекста relevante (если есть)

Формат: Markdown, с заголовками ##, списками, код-блоками где уместно.
"""

            llm = LazyLoader.get_llm()
            console.print("[dim]Генерация writeup...[/dim]")
            response = llm.invoke(prompt)
            writeup = (
                response.content if hasattr(response, "content") else str(response)
            )

            console.print("\n[bold green]Writeup сгенерирован:[/bold green]\n")
            console.print(
                Panel(
                    writeup, title=f"Writeup: {topic}", border_style="cyan", expand=True
                )
            )

            # Сохранить в историю
            writeup_entry = {
                "timestamp": time.time(),
                "type": act_type,
                "topic": topic,
                "writeup": writeup,
                "activity_id": id(activity),  # для связи
            }
            state.writeup_history.append(writeup_entry)
            state.last_writeup_activity = (
                activity  # оставляем для повторного использования
            )

            # Предложить сохранить в файл
            console.print("\n[yellow]Сохранить writeup в файл? (y/n)[/yellow]")
            try:
                save = input("> ").strip().lower()
                if save in ("y", "yes", "д", "да"):
                    filename = (
                        f"writeup_{topic.replace(' ', '_')}_{int(time.time())}.md"
                    )
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"# Writeup: {topic}\n\n")
                        f.write(writeup)
                    console.print(f"[green]Writeup сохранён: {filename}[/green]")
            except KeyboardInterrupt:
                console.print("\n[yellow]Отмена сохранения[/yellow]")

            state.save_to_file()
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
