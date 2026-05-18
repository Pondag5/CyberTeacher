# handlers/misc.py (дополнительные функции, которые не warranted отдельного файла)
import json
import os
import shutil
import time
from datetime import datetime
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel

from di import get_context
from utils.common import ask_confirm as _ask_confirm
from utils.common import check_open_answer_heuristic as check_open_answer
from utils.common import clear_chat_db, extract_json_block

console = Console()


def handle_backup(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Создать бэкап state и news cache."""
    state = get_context().state
    state.maybe_auto_backup()
    console.print("[green]✅ Бэкап создан (или актуальный уже существует).[/green]")
    return True, None, None, True


def handle_story_mode(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Режим истории (20 эпизодов) с интеграцией risk_level"""
    try:
        from story_mode import (
            get_achievements_list,
            get_player,
            get_story_list,
            start_story_mode,
            submit_flag,
        )

        state = get_context().state
        parts = action.split()

        if action in {"story", "episode", "quest"}:
            # Показать список эпизодов
            console.print(get_story_list())
            return True, None, None, True

        elif len(parts) >= 2 and parts[0] == "story" and parts[1] == "start":
            # Начать конкретный эпизод
            try:
                if len(parts) >= 3:
                    episode_id = int(parts[2])
                    console.print(start_story_mode(episode_id))
                else:
                    console.print(start_story_mode())
            except ValueError:
                console.print("[red]Неверный номер эпизода[/red]")
            return True, None, None, True

        elif len(parts) >= 2 and parts[0] in ("story", "flag"):
            # Проверить флаг
            if len(parts) >= 3:
                flag = parts[2] if parts[0] == "flag" else " ".join(parts[2:])
                result = submit_flag(flag)
                console.print(result)

                # Обновляем риск уровень на основе успеха
                if "✅" in result or "ПРОЙДЕН" in result:
                    state.decrease_risk(15)  # Успех снижает риск
                    console.print(
                        f"[green]🛡️ Уровень риска снижен! Текущий: {state.get_risk_status()} ({state.risk_level}/100)[/green]"
                    )
                else:
                    state.increase_risk(10)  # Ошибка повышает риск
                    console.print(
                        f"[red]⚠️  Уровень риска повышен! Текущий: {state.get_risk_status()} ({state.risk_level}/100)[/red]"
                    )
            else:
                console.print(
                    "[yellow]Использование: /flag <флаг>  или  /story flag <флаг>[/yellow]"
                )
            return True, None, None, True

        elif len(parts) >= 2 and parts[0] == "achievements":
            # Показать достижения
            console.print(get_achievements_list())
            return True, None, None, True

        else:
            console.print("[cyan]Использование Story Mode:[/cyan]")
            console.print("  /story            - список эпизодов")
            console.print("  /story start [N]  - начать эпизод N (или следующий)")
            console.print("  /flag <флаг>      - отправить флаг")
            console.print("  /achievements     - список достижений")
            return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback

        traceback.print_exc()
        return True, None, None, True


def handle_risk(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление и просмотр уровня риска"""
    try:
        state = get_context().state
        parts = action.split()

        if len(parts) == 1:
            # Показать текущий статус
            status = state.get_risk_status()
            console.print(
                f"[bold cyan]⚡ Уровень риска: {status} ({state.risk_level}/100)[/bold cyan]"
            )
            console.print(
                "[dim]Уровень риска повышается при ошибках и снижается при успехах в CTF/Story режимах.[/dim]"
            )
            return True, None, None, True

        # Изменить уровень вручную (для отладки/админа)
        if len(parts) >= 2:
            try:
                if parts[1] == "reset":
                    state.reset_risk()
                    console.print(f"[green]✅ Уровень риска сброшен[/green]")
                elif parts[1] == "up":
                    amount = int(parts[2]) if len(parts) >= 3 else 10
                    state.increase_risk(amount)
                    console.print(
                        f"[yellow]⚠️  Уровень риска увеличен на {amount}[/yellow]"
                    )
                elif parts[1] == "down":
                    amount = int(parts[2]) if len(parts) >= 3 else 5
                    state.decrease_risk(amount)
                    console.print(
                        f"[green]🛡️ Уровень риска уменьшен на {amount}[/green]"
                    )
                else:
                    amount = int(parts[1])
                    state.risk_level = max(0, min(100, amount))
                    console.print(
                        f"[cyan]Уровень риска установлен: {state.risk_level}/100[/cyan]"
                    )

                console.print(
                    f"[bold]Текущий статус: {state.get_risk_status()} ({state.risk_level}/100)[/bold]"
                )
            except ValueError:
                console.print(
                    "[red]Использование: /risk [reset|up|down <колво>|число 0-100][/red]"
                )

            return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_history(conn) -> tuple[bool, Any | None, Any | None, bool]:
    try:
        from memory import get_chat_history

        history = get_chat_history(conn, limit=20)
        if history:
            console.print("[bold cyan]📜 История чата:[/bold cyan]")
            for msg in history:
                role = msg.get("role", "?")
                content = msg.get("content", "")[:150]
                console.print(f"[{role}] {content}")
        else:
            console.print("[yellow]История пуста[/yellow]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_course(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    console.print("[yellow]Курсы временно недоступны[/yellow]")
    return True, None, None, True


def handle_terminal_log(
    action: str | None = None,
) -> tuple[bool, Any | None, Any | None, bool]:
    try:
        from terminal_log import get_terminal_log, log_command

        if action and action.startswith("log "):
            cmd = action[4:].strip()
            log_command(cmd, is_input=False)
            console.print(f"[green]✅ Команда записана в лог[/green]")
            return True, None, None, True
        log_text = get_terminal_log(last_n=20)
        console.print(
            Panel(
                log_text, title="📟 Терминал (последние 20 строк)", border_style="cyan"
            )
        )
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_version() -> tuple[bool, Any | None, Any | None, bool]:
    console.print("[bold cyan]CyberTeacher v3.2[/bold cyan]")
    console.print("Обучение кибербезопасности с LLM")
    console.print("Основано на: Ollama/OpenRouter, ChromaDB, Rich")
    console.print("© 2025 CyberTeacher Project")
    return True, None, None, True


def handle_writeup() -> tuple[bool, Any | None, Any | None, bool]:
    template = """
# Write-up: [Название задачи]

## Информация
- **Категория:** [web|crypto|pwn|forensics|reversing|misc]
- **Сложность:** [★☆☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆]
- **Инструменты:** инструмент1, инструмент2, ...

## Описание
[Краткое описание задачи и цели]

## Решение

### 1. Разведка (Reconnaissance)
[Описание шагов разведки: сканирование, анализ, ...]

### 2. Эксплуатация (Exploitation)
[Как использовал уязвимость, команды, эксплойт]

### 3. Получение флага/доступа
[Что получилось в итоге, флаг]

## Выводы
- **Чему научился:** ...
- **Что было сложно:** ...
- **Что можно улучшить:** ...
"""
    console.print(Panel(template, title="📝 Шаблон Write-up", border_style="magenta"))
    return True, None, None, True


def handle_provider(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление провайдером LLM"""
    import config
    from config import LLM_PROVIDER, LazyLoader

    # Показать текущий провайдер
    if not action or action == "provider":
        console.print(f"[cyan]📡 Текущий провайдер: {LLM_PROVIDER}[/cyan]")
        console.print("[cyan]Доступные провайдеры:[/cyan]")
        console.print("  • ollama      - локально, бесплатно (рекомендуется)")
        console.print("  • openrouter  - облако, требуется API ключ")
        console.print("  • huggingface - HF Inference API, требуется HF_TOKEN")
        console.print("\nИспользование: /provider <имя>")
        return True, None, None, True

    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print(
            "[yellow]Использование: /provider <ollama|openrouter|huggingface>[/yellow]"
        )
        return True, None, None, True

    provider = parts[1].strip()

    if provider not in ("ollama", "openrouter", "huggingface"):
        console.print(
            "[red]❌ Неизвестный провайдер. Доступные: ollama, openrouter, huggingface[/red]"
        )
        return True, None, None, True

    # Меняем провайдер
    old_provider = LLM_PROVIDER
    config.LLM_PROVIDER = provider
    # Сбрасываем кэш LLM для перезагрузки
    LazyLoader._llm = None

    console.print(f"[green]✅ Провайдер изменён: {old_provider} → {provider}[/green]")
    console.print(
        "[yellow]Следующий запрос загрузит модель нового провайдера.[/yellow]"
    )

    # Показываем настройки для нового провайдера
    if provider == "ollama":
        console.print(f"[dim]Модель: {config.OLLAMA_MODEL}[/dim]")
        console.print(
            "[dim]Запустите 'ollama serve' и 'ollama pull <модель>' если ещё не[/dim]"
        )
    elif provider == "openrouter":
        console.print(f"[dim]Модель: {config.OPENROUTER_MODEL}[/dim]")
        console.print("[dim]Убедитесь, что OPENROUTER_API_KEY установлен в .env[/dim]")
    elif provider == "huggingface":
        console.print(f"[dim]Модель: {config.HF_MODEL}[/dim]")
        console.print("[dim]Убедитесь, что HF_TOKEN установлен в .env[/dim]")

    return True, None, None, True


def handle_model(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление моделями LLM для текущего провайдера"""
    import config

    provider = config.LLM_PROVIDER

    # Показать текущую модель
    if not action or action == "model":
        console.print(f"[cyan]🤖 Текущий провайдер: {provider}[/cyan]")
        if provider == "ollama":
            console.print(f"[cyan]Модель: {config.OLLAMA_MODEL}[/cyan]")
            console.print(
                "[cyan]Доступные модели: qwen2.5:7b, mistral:7b, llama2:7b и другие[/cyan]"
            )
        elif provider == "openrouter":
            console.print(f"[cyan]Модель: {config.OPENROUTER_MODEL}[/cyan]")
            console.print(
                "[cyan]Примеры: meta-llama/llama-3.3-70b-instruct:free, google/gemma-3-27b-it:free[/cyan]"
            )
        elif provider == "huggingface":
            console.print(f"[cyan]Модель: {config.HF_MODEL}[/cyan]")
            console.print(
                "[cyan]Примеры: mistralai/Mixtral-8x7B-Instruct-v0.1, meta-llama/Llama-2-70b-chat-hf[/cyan]"
            )
        console.print("\nИспользование: /model <имя_модели>")
        return True, None, None, True

    # Изменить модель
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print("[yellow]Использование: /model <имя_модели>[/yellow]")
        return True, None, None, True

    model_name = parts[1].strip()

    # Устанавливаем модель в зависимости от провайдера
    if provider == "ollama":
        config.OLLAMA_MODEL = model_name
        console.print(f"[green]✅ Модель Ollama изменена: {model_name}[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    elif provider == "openrouter":
        config.OPENROUTER_MODEL = model_name
        console.print(f"[green]✅ Модель OpenRouter изменена: {model_name}[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    elif provider == "huggingface":
        config.HF_MODEL = model_name
        console.print(f"[green]✅ Модель HuggingFace изменена: {model_name}[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    else:
        console.print("[red]❌ Неизвестный провайдер[/red]")
        return True, None, None, True

    console.print("[dim]Следующий запрос загрузит новую модель.[/dim]")
    return True, None, None, True


def handle_set_api_key(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Установка API ключа для провайдера"""
    import os

    import config

    if not action or action == "set-api-key":
        console.print("[cyan]Установка API ключа[/cyan]")
        console.print("Использование:")
        console.print("  /set-api-key openrouter <ключ>")
        console.print("  /set-api-key huggingface <ключ>")
        console.print("\nПримечание: Ключ будет сохранён только в текущей сессии.")
        return True, None, None, True

    parts = action.split(maxsplit=2)
    if len(parts) < 3:
        console.print(
            "[yellow]Использование: /set-api-key <openrouter|huggingface> <api_key>[/yellow]"
        )
        return True, None, None, True

    provider = parts[1].strip().lower()
    api_key = parts[2].strip()

    if provider == "openrouter":
        os.environ["OPENROUTER_API_KEY"] = api_key
        console.print(
            "[green]✅ OPENROUTER_API_KEY установлен для текущей сессии[/green]"
        )
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    elif provider == "huggingface":
        os.environ["HF_TOKEN"] = api_key
        console.print("[green]✅ HF_TOKEN установлен для текущей сессии[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    else:
        console.print("[red]❌ Поддерживаются только: openrouter, huggingface[/red]")

    return True, None, None, True


def handle_add_book(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Добавить PDF книгу в базу знаний"""
    try:
        parts = action.split(maxsplit=1)
        if len(parts) < 2:
            console.print("[yellow]Использование: /add_book <путь_к_PDF>[/yellow]")
            return True, None, None, True

        src_path = parts[1].strip()
        if not os.path.exists(src_path):
            console.print(f"[red]Файл не найден: {src_path}[/red]")
            return True, None, None, True

        # ✅ Path traversal защита
        from config import KNOWLEDGE_DIR

        src_path_abs = os.path.abspath(src_path)
        knowledge_dir_abs = os.path.abspath(KNOWLEDGE_DIR)
        if not src_path_abs.startswith(knowledge_dir_abs):
            console.print(
                "[red]❌ Запрещенный путь. Файл должен находиться в knowledge_base/[/red]"
            )
            return True, None, None, True

        if not src_path.lower().endswith(".pdf"):
            console.print("[yellow]Поддерживаются только PDF файлы[/yellow]")
            return True, None, None, True

        import shutil

        filename = os.path.basename(src_path)
        dst_path = os.path.join(KNOWLEDGE_DIR, filename)

        if os.path.exists(dst_path):
            console.print(f"[yellow]Файл уже существует: {filename}[/yellow]")
            return True, None, None, True

        shutil.copy2(src_path, dst_path)
        console.print(f"[green]✓ Книга добавлена: {filename}[/green]")
        console.print(
            "[cyan]Перезапустите приложение или запустите переиндексацию чтобы обновить базу.[/cyan]"
        )

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_adaptive(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Показать слабые темы и адаптивный план обучения"""
    try:
        state = get_context().state
        weak = state.get_weak_topics(threshold=70.0)
        if not weak:
            console.print(
                "[green]Поздравляю! Нет слабых тем (все темы с успешностью >=70%)[/green]"
            )
        else:
            console.print("[bold cyan]Адаптивное обучение: слабые темы[/bold cyan]")
            console.print(
                f"[dim]Порог: 70%. Темы с успешностью ниже порога приоритетны для повторения.[/dim]\n"
            )
            for w in weak:
                console.print(
                    f"  • {w['topic']}: {w['success_rate']:.1f}% (попыток: {w['attempts']})"
                )
            # Recommend next focus
            next_topic = state.get_next_weak_topic()
            if next_topic:
                console.print(
                    f"\n[yellow]Следующая тема для фокуса: {next_topic}[/yellow]"
                )
                console.print("[dim]Запустите /quiz чтобы потренировать эту тему[/dim]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_repeat(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Интервальные повторения (Spaced Repetition) - повторение тем, готовых к проверке."""
    try:
        state = get_context().state

        # SR-01: Review statistics
        parts = action.split()
        if len(parts) > 1 and parts[1] == "stats":
            schedule = state.review_schedule
            if not schedule:
                console.print("[yellow]Нет тем в расписании повторений[/yellow]")
                return True, None, None, True

            total = len(schedule)
            due = len(state.get_due_reviews())
            total_reps = sum(d.get("repetitions", 0) for d in schedule.values())
            avg_ef = sum(d.get("ef", 2.5) for d in schedule.values()) / total if total else 0
            longest_interval = max((d.get("interval", 0) for d in schedule.values()), default=0)

            # Most reviewed topic
            most_reviewed = max(schedule.items(), key=lambda x: x[1].get("repetitions", 0))

            console.print(Panel(
                f"[bold]Всего тем:[/bold] {total}\n"
                f"[bold]Готовы к повторению:[/bold] {due}\n"
                f"[bold]Всего повторений:[/bold] {total_reps}\n"
                f"[bold]Средний ease factor:[/bold] {avg_ef:.2f}\n"
                f"[bold]Максимальный интервал:[/bold] {longest_interval} дней\n"
                f"[bold]Самая повторяемая:[/bold] {most_reviewed[0]} ({most_reviewed[1].get('repetitions', 0)} раз)",
                title="📊 СТАТИСТИКА ПОВТОРЕНИЙ",
                border_style="cyan",
            ))
            return True, None, None, True

        # SR-02: Review Calendar
        if len(parts) > 1 and parts[1] == "calendar":
            from datetime import datetime, timedelta

            schedule = state.review_schedule
            if not schedule:
                console.print("[yellow]Нет тем в расписании повторений[/yellow]")
                return True, None, None, True

            today = datetime.now()
            console.print("[bold cyan]📅 Календарь повторений (14 дней)[/bold cyan]\n")

            for i in range(14):
                day = today + timedelta(days=i)
                day_str = day.strftime("%Y-%m-%d")
                day_label = day.strftime("%d.%m (%a)")

                # Find topics due on or before this day
                due_topics = []
                for topic, data in schedule.items():
                    next_review = data.get("next_review", 0)
                    if next_review <= day.timestamp():
                        due_topics.append(topic)

                if due_topics:
                    blocks = "█" * min(len(due_topics), 5)
                    console.print(f"  {day_label} [green]{blocks}[/green] {', '.join(due_topics[:3])}{'...' if len(due_topics) > 3 else ''}")
                else:
                    console.print(f"  {day_label} [dim]—[/dim]")

            return True, None, None, True

        due = state.get_due_reviews()

        if not due:
            console.print(
                "[green]🎉 Нет тем для повторения! Все темы в актуальном состоянии.[/green]"
            )
            return True, None, None, True

        console.print("[bold cyan]📚 Темы для повторения:[/bold cyan]")
        console.print(f"[dim]Всего: {len(due)}[/dim]\n")
        for idx, item in enumerate(due, 1):
            console.print(
                f"  {idx}. {item['topic']} (интервал: {item['interval']} дней, попыток: {item['repetitions']})"
            )

        console.print(
            "\n[yellow]Выберите тему для повторения (номер) или /cancel для отмены[/yellow]"
        )
        choice = input("Номер: ").strip()
        if choice.lower() in ["/cancel", "/exit"]:
            console.print("[yellow]Отмена[/yellow]")
            return True, None, None, True

        try:
            idx = int(choice) - 1
        except ValueError:
            console.print("[red]Неверный ввод[/red]")
            return True, None, None, True

        if idx < 0 or idx >= len(due):
            console.print("[red]Неверный номер[/red]")
            return True, None, None, True

        topic = due[idx]["topic"]
        console.print(f"[cyan]Запускаю квиз по теме: {topic}[/cyan]")

        try:
            from generators import generate_quiz
            from knowledge import get_current_vectordb

            vectordb = get_current_vectordb()
            quiz = generate_quiz(vectordb, topic=topic)
            questions = quiz.get("questions", [])
            if not questions:
                console.print(
                    "[yellow]Не удалось сгенерировать вопросы для этой темы[/yellow]"
                )
                return True, None, None, True
        except Exception as e:
            console.print(f"[red]Ошибка генерации квиза: {e}[/red]")
            return True, None, None, True

        console.print(f"[bold green]📝 Квиз: {len(questions)} вопросов[/bold green]\n")
        total_score = 0
        max_total = 0

        for i, q in enumerate(questions, 1):
            console.print(f"[bold cyan]Вопрос {i}/{len(questions)}:[/bold cyan]")
            console.print(q.get("question", "?"))
            if "options" in q:
                for opt_key, opt_val in q["options"].items():
                    console.print(f"  {opt_key}) {opt_val}")
            try:
                user_ans = input("\nВаш ответ: ").strip()
                if user_ans.lower() in ["/exit", "/quit"]:
                    console.print("[yellow]Квиз прерван[/yellow]")
                    break
                if user_ans.lower() == "/skip":
                    console.print("[dim]Пропущено[/dim]\n")
                    continue
                if not user_ans:
                    console.print("[dim]Пустой ответ[/dim]\n")
                    continue
            except KeyboardInterrupt:
                console.print("\n[yellow]Прервано[/yellow]")
                break

            # Evaluate
            if "options" in q:
                correct = q.get("correct", "")
                if user_ans.upper() == correct.upper():
                    score = 10
                    feedback = "✅ Верно!"
                else:
                    score = 0
                    feedback = f"❌ Неверно. Правильный ответ: {correct}"
            else:
                result = check_open_answer(q.get("question", ""), user_ans, None)
                score = result["score"]
                feedback = result["feedback"]
            console.print(f"[bold]Результат:[/bold] {score}/10 - {feedback}\n")
            total_score += score
            max_total += 10

        if max_total > 0:
            success_rate = total_score / max_total * 100
            console.print(
                f"[bold]📊 Итог:[/bold] {total_score}/{max_total} ({success_rate:.1f}%)"
            )

            state.update_weak_topic(topic, total_score, max_total)
            state.mark_reviewed(topic, total_score, max_total)

            entry = state.review_schedule.get(topic, {})
            if entry:
                import time

                next_date = time.strftime(
                    "%Y-%m-%d", time.localtime(entry["next_review"])
                )
                console.print(
                    f"[cyan]Следующее повторение: {next_date} (интервал: {entry['interval']} дней)[/cyan]"
                )

            state.save_to_file()
        else:
            console.print("[dim]Нет результатов[/dim]")

        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback

        traceback.print_exc()
        return True, None, None, True

def handle_export(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    from datetime import datetime

    from memory import get_chat_history
    try:
        ctx = get_context()
        parts = action.split(maxsplit=1)
        filename = parts[1].strip() if len(parts) >= 2 else None
        if not filename:
            filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        history = get_chat_history(conn=ctx.db_conn, limit=1000)
        if not history:
            console.print("[yellow]История пуста[/yellow]")
            return True, None, None, True
        if filename.endswith(".json"):
            import json
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        else:
            md = "# CyberTeacher - Экспорт чата\n\n"
            md += f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nСообщений: {len(history)}\n\n---\n\n"
            for msg in history:
                role = msg.get("role", "?")
                content = msg.get("content", "")
                mode = msg.get("mode", "")
                md += f"### {'👤' if role == 'user' else '🤖'} {role.capitalize()}"
                if mode: md += f" ({mode})"
                md += f"\n\n{content}\n\n---\n\n"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(md)
        console.print(f"[green]✅ Экспортирован: {filename}[/green]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_usage(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    try:
        cmd_stats = get_context().state.command_usage
        if not cmd_stats:
            console.print("[yellow]Статистика пуста[/yellow]")
            return True, None, None, True
        sorted_cmds = sorted(cmd_stats.items(), key=lambda x: x[1], reverse=True)
        total = sum(cmd_stats.values())
        console.print("[bold cyan]📊 Статистика команд[/bold cyan]")
        console.print(f"[dim]Всего: {total}[/dim]\n")
        top_15 = sorted_cmds[:15]
        for cmd, count in top_15:
            bar_len = int((count / top_15[0][1]) * 20) if top_15[0][1] > 0 else 0
            pct = (count / total * 100) if total > 0 else 0
            console.print(f"  [cyan]{cmd:<20}[/cyan] {count:>4} ({pct:.1f}%) [dim]{'█' * bar_len}[/dim]")
        if len(sorted_cmds) > 15:
            console.print(f"\n[dim]... и ещё {len(sorted_cmds) - 15} команд[/dim]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_writeups(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """ANA-04: Browse and search past writeups."""
    from datetime import datetime

    state = get_context().state
    history = state.writeup_history

    if not history:
        console.print("[yellow]Нет сохранённых writeups[/yellow]")
        return True, None, None, True

    parts = action.split()
    subcmd = parts[1] if len(parts) > 1 else "list"

    if subcmd == "list":
        console.print("[bold cyan]📝 История writeups[/bold cyan]")
        console.print(f"[dim]Всего: {len(history)}[/dim]\n")
        for idx, entry in enumerate(history[-15:], 1):
            ts = entry.get("timestamp", 0)
            dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
            topic = entry.get("topic", "?")
            wtype = entry.get("type", "?")
            preview = entry.get("writeup", "")[:80]
            console.print(f"  {idx}. [{dt}] {topic} ({wtype})")
            console.print(f"     [dim]{preview}...[/dim]")
        if len(history) > 15:
            console.print(f"\n[dim]... и ещё {len(history) - 15} записей[/dim]")
        console.print("\n[yellow]Просмотр: /writeups <номер> | Поиск: /writeups search <тема>[/yellow]")

    elif subcmd == "search" and len(parts) > 2:
        query = " ".join(parts[2:]).lower()
        matches = [e for e in history if query in e.get("topic", "").lower() or query in e.get("writeup", "").lower()]
        if not matches:
            console.print(f"[yellow]Ничего не найдено по запросу: {query}[/yellow]")
        else:
            console.print(f"[bold cyan]🔍 Найдено: {len(matches)} writeups[/bold cyan]\n")
            for idx, entry in enumerate(matches[-10:], 1):
                ts = entry.get("timestamp", 0)
                dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
                topic = entry.get("topic", "?")
                console.print(f"  {idx}. [{dt}] {topic}")
            console.print("\n[yellow]Просмотр: /writeups <номер>[/yellow]")

    elif subcmd.isdigit():
        idx = int(subcmd) - 1
        if 0 <= idx < len(history):
            entry = history[idx]
            console.print(Panel(
                entry.get("writeup", ""),
                title=f"Writeup: {entry.get('topic', '?')}",
                border_style="cyan",
                expand=True,
            ))
        else:
            console.print("[red]Неверный номер[/red]")

    else:
        console.print("[yellow]Использование: /writeups [list|search <тема>|<номер>][/yellow]")

    return True, None, None, True


def handle_exploits_log(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """ANA-05: Browse past exploit submission results."""
    state = get_context().state
    log = state.exploit_success

    if not log:
        console.print("[yellow]Нет записей об эксплойтах[/yellow]")
        return True, None, None, True

    console.print("[bold cyan]🔓 История эксплойтов[/bold cyan]")
    console.print(f"[dim]Всего успешных: {len(log)}[/dim]\n")

    # Group by mission
    missions: dict[str, list] = {}
    for entry in log:
        mid = entry.get("mission_id", "?")
        if mid not in missions:
            missions[mid] = []
        missions[mid].append(entry.get("step_order", "?"))

    for mid, steps in missions.items():
        steps.sort()
        console.print(f"  [cyan]{mid}[/cyan] — шаги: {', '.join(str(s) for s in steps)}")

    console.print(f"\n[dim]Успешных попыток: {len(log)}[/dim]")
    return True, None, None, True


def handle_heatmap(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """ANA-02: Command usage heatmap (GitHub contributions style)."""
    from datetime import datetime, timedelta

    state = get_context().state
    daily = state.daily_command_counts

    if not daily:
        console.print("[yellow]Нет данных для heatmap. Используйте команды, чтобы начать[/yellow]")
        return True, None, None, True

    # Get last 28 days
    today = datetime.now()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(27, -1, -1)]

    # Calculate max commands per day for scaling
    max_cmds = max((sum(daily.get(d, {}).values(), 0) for d in days), default=0)
    if max_cmds == 0:
        max_cmds = 1

    console.print("[bold cyan]📊 Активность команд (28 дней)[/bold cyan]\n")

    # Display heatmap
    for day in days:
        dt = datetime.strptime(day, "%Y-%m-%d")
        total = sum(daily.get(day, {}).values(), 0)
        intensity = int((total / max_cmds) * 4)
        blocks = [" ", "░", "▒", "▓", "█"]
        block = blocks[min(intensity, 4)]
        day_label = dt.strftime("%d")
        console.print(f"  {day_label} {block} ({total} команд)")

    console.print(f"\n[dim]Легенда: ░ мало  ▒ средне  ▓ много  █ очень много[/dim]")

    # Top commands overall
    all_cmds: dict[str, int] = {}
    for day_cmds in daily.values():
        for cmd, count in day_cmds.items():
            all_cmds[cmd] = all_cmds.get(cmd, 0) + count
    if all_cmds:
        top = sorted(all_cmds.items(), key=lambda x: x[1], reverse=True)[:5]
        console.print("\n[bold]Топ команд:[/bold]")
        for cmd, count in top:
            console.print(f"  [cyan]{cmd:<20}[/cyan] {count}")

    return True, None, None, True


def handle_state(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """CLI-05: Export/Import full app state as JSON."""
    from config import STATE_FILE

    state = get_context().state
    parts = action.split(maxsplit=2)
    subcmd = parts[1] if len(parts) > 1 else "help"

    if subcmd == "export":
        os.makedirs("backups", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backups/app_state_{ts}.json"

        try:
            state.save_to_file(filename)
            size = os.path.getsize(filename) / 1024
            console.print(Panel(
                f"[bold]Файл:[/bold] {filename}\n"
                f"[bold]Размер:[/bold] {size:.1f} KB\n"
                f"[bold]Очки:[/bold] {state.points:.0f}\n"
                f"[bold]Стрик:[/bold] {state.daily_streak} дней\n"
                f"[bold]Навыков:[/bold] {len(state.skill_tracker)}\n"
                f"[bold]Тем в расписании:[/bold] {len(state.review_schedule)}",
                title="✅ ЭКСПОРТ СОСТОЯНИЯ",
                border_style="green",
            ))
        except Exception as e:
            console.print(f"[red]Ошибка экспорта: {e}[/red]")

    elif subcmd == "import" and len(parts) > 2:
        filename = parts[2].strip()
        if not os.path.exists(filename):
            console.print(f"[red]Файл не найден: {filename}[/red]")
            return True, None, None, True

        try:
            if os.path.exists(STATE_FILE):
                backup = f"{STATE_FILE}.backup"
                shutil.copy2(STATE_FILE, backup)
                console.print(f"[dim]Бэкап текущего состояния: {backup}[/dim]")

            state.load_from_file(filename)
            state.save_to_file()
            console.print(Panel(
                f"[bold]Загружено из:[/bold] {filename}\n"
                f"[bold]Очки:[/bold] {state.points:.0f}\n"
                f"[bold]Стрик:[/bold] {state.daily_streak} дней\n\n"
                "[yellow]Перезапустите приложение для полного применения[/yellow]",
                title="✅ ИМПОРТ СОСТОЯНИЯ",
                border_style="green",
            ))
        except Exception as e:
            console.print(f"[red]Ошибка импорта: {e}[/red]")

    elif subcmd == "list":
        os.makedirs("backups", exist_ok=True)
        backups = sorted([
            f for f in os.listdir("backups")
            if f.startswith("app_state_") and f.endswith(".json")
        ], reverse=True)

        if not backups:
            console.print("[yellow]Нет сохранённых бэкапов[/yellow]")
        else:
            console.print("[bold cyan]📦 Доступные бэкапы[/bold cyan]")
            console.print(f"[dim]Всего: {len(backups)}[/dim]\n")
            for f in backups[:10]:
                path = os.path.join("backups", f)
                size = os.path.getsize(path) / 1024
                console.print(f"  {f} ({size:.1f} KB)")
            if len(backups) > 10:
                console.print(f"\n[dim]... и ещё {len(backups) - 10}[/dim]")
            console.print("\n[yellow]Импорт: /state import backups/<файл>[/yellow]")

    else:
        console.print(Panel(
            "[bold]Управление состоянием[/bold]\n\n"
            "  /state export        — экспортировать в backups/\n"
            "  /state import <файл> — импортировать из файла\n"
            "  /state list          — список бэкапов",
            title="STATE",
            border_style="cyan",
        ))

    return True, None, None, True


def handle_topics(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """CNT-03: Browse all course topics with progress."""
    from courses import list_all_topics

    state = get_context().state
    parts = action.split(maxsplit=2)
    subcmd = parts[1] if len(parts) > 1 else "all"

    all_topics = list_all_topics(state.course_progress)

    if subcmd == "all":
        courses: dict[str, list] = {}
        for t in all_topics:
            if t["course"] not in courses:
                courses[t["course"]] = []
            courses[t["course"]].append(t)

        console.print("[bold cyan]📚 Все темы курсов[/bold cyan]")
        total = len(all_topics)
        completed = sum(1 for t in all_topics if t["status"] == "completed")
        console.print(f"[dim]Всего: {total} тем | Пройдено: {completed}[/dim]\n")

        status_emoji = {"completed": "✅", "in_progress": "📍", "not_started": "⬜"}
        for course_name, topics in courses.items():
            console.print(f"[bold]{course_name}[/bold]")
            for t in topics[:10]:
                emoji = status_emoji.get(t["status"], "⬜")
                console.print(f"  {emoji} {t['topic']}")
            if len(topics) > 10:
                console.print(f"  [dim]... и ещё {len(topics) - 10}[/dim]")
            console.print()

    elif subcmd.isdigit():
        idx = int(subcmd) - 1
        if 0 <= idx < len(all_topics):
            t = all_topics[idx]
            status_names = {"completed": "✅ Пройдена", "in_progress": "📍 В процессе", "not_started": "⬜ Не начата"}
            console.print(Panel(
                f"[bold]Курс:[/bold] {t['course']}\n"
                f"[bold]Тема:[/bold] {t['topic']}\n"
                f"[bold]Статус:[/bold] {status_names.get(t['status'], '?')}\n\n"
                f"[bold]Описание:[/bold] {t['description']}\n\n"
                f"[bold]Лаборатории:[/bold] {', '.join(t['labs']) if t['labs'] else 'нет'}\n"
                f"[bold]Квизы:[/bold] {', '.join(t['quiz_topics']) if t['quiz_topics'] else 'нет'}",
                title="ТЕМА КУРСА",
                border_style="cyan",
            ))
        else:
            console.print("[red]Неверный номер[/red]")

    else:
        query = " ".join(parts[1:]).lower()
        matches = [t for t in all_topics if query in t["topic"].lower() or query in t["description"].lower()]
        if not matches:
            console.print(f"[yellow]Ничего не найдено по запросу: {query}[/yellow]")
        else:
            console.print(f"[bold cyan]🔍 Найдено: {len(matches)} тем[/bold cyan]\n")
            status_emoji = {"completed": "✅", "in_progress": "📍", "not_started": "⬜"}
            for t in matches[:10]:
                emoji = status_emoji.get(t["status"], "⬜")
                console.print(f"  {emoji} [{t['course']}] {t['topic']}")

    return True, None, None, True
