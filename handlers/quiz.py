# handlers/quiz.py
import os
import time
from typing import Any

from rich.console import Console

from di import get_context
from utils.common import check_open_answer_heuristic as check_open_answer
from handlers.types import HandlerResult


console = Console()

# Generators (quiz/task) - optional import
try:
    from quiz_generator import generate_quiz, generate_task

    GENERATORS_AVAILABLE = True
except ImportError:
    GENERATORS_AVAILABLE = False


def handle_quiz_action() -> HandlerResult:
    """Interactive quiz with answer evaluation and adaptive learning."""
    if not GENERATORS_AVAILABLE:
        console.print("[yellow]Генератор квизов недоступен[/yellow]")
        return True, None, None, True

    ctx = get_context()
    state_obj = ctx.state
    from knowledge import get_current_vectordb

    vectordb = get_current_vectordb()

    # Определить тему: сначала смотрим слабые темы
    topic = None
    weak_topic = state_obj.get_next_weak_topic(threshold=70.0)
    if weak_topic:
        console.print(f"[cyan]🎯 Фокус на слабой теме: {weak_topic}[/cyan]")
        topic = weak_topic

    # Генерировать квиз
    quiz = generate_quiz(vectordb, topic=topic)
    questions = quiz.get("questions", [])
    quiz_topic = quiz.get("topic", topic or "general")

    if not questions:
        console.print("[yellow]Не удалось сгенерировать вопросы[/yellow]")
        return True, None, None, True

    console.print(
        f"[bold green]📝 Квиз: {len(questions)} вопросов по теме '{quiz_topic}'[/bold green]"
    )
    console.print(
        "[yellow]Напишите ответ на каждый вопрос. Введите /skip чтобы пропустить, /exit для выхода.[/yellow]\n"
    )

    scores = []  # list of (score, max_score) for each question
    responses = []  # Detailed responses for writeup
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
                scores.append((0, 10))
                responses.append(
                    {
                        "question": q.get("question", ""),
                        "user_answer": "<пропущено>",
                        "correct_answer": q.get("correct", ""),
                        "score": 0,
                        "feedback": "Пропущено",
                    }
                )
                continue
            if not user_ans:
                console.print("[dim]Пустой ответ[/dim]\n")
                scores.append((0, 10))
                responses.append(
                    {
                        "question": q.get("question", ""),
                        "user_answer": "",
                        "correct_answer": q.get("correct", ""),
                        "score": 0,
                        "feedback": "Пустой ответ",
                    }
                )
                continue
        except KeyboardInterrupt:
            console.print("\n[yellow]Прервано[/yellow]")
            break

        # Оценить ответ
        correct = q.get("correct", "")
        explanation = q.get("explanation", "")
        if "options" in q:
            # Для вопросов с вариантами - просто проверяем совпадение
            if user_ans.upper() == correct.upper():
                score = 10
                feedback = "✅ Верно!"
            else:
                score = 0
                feedback = f"❌ Неверно. Правильный ответ: {correct}"
            if explanation:
                feedback += f"\n[dim]{explanation}[/dim]"
        else:
            # Для открытых вопросов используем check_open_answer
            result = check_open_answer(q.get("question", ""), user_ans, None)
            score = result["score"]
            feedback = result["feedback"]

        console.print(f"[bold]Результат:[/bold] {score}/10 - {feedback}\n")
        scores.append((score, 10))
        total_score += score
        max_total += 10

        responses.append(
            {
                "question": q.get("question", ""),
                "user_answer": user_ans,
                "correct_answer": correct if "options" in q else None,
                "score": score,
                "feedback": feedback,
            }
        )

    # Показать итоги и обновить weak_topics
    if scores:
        success_rate = (total_score / max_total * 100) if max_total > 0 else 0
        console.print(
            f"[bold]📊 Итог:[/bold] {total_score}/{max_total} ({success_rate:.1f}%)"
        )

        # Record behavioral profile
        try:
            from behavior_profile import record_action

            if success_rate >= 60:
                record_action(state_obj, "quiz_pass")
            else:
                record_action(state_obj, "quiz_fail")
        except ImportError:
            pass

        # Изменение уровня риска
        if success_rate < 50:
            state_obj.increase_risk(10)
            try:
                from cyberpsychosis import get_cyberpsychosis

                get_cyberpsychosis().on_failure(15)
            except (ImportError, RuntimeError):
                pass
        else:
            state_obj.decrease_risk(5)
            try:
                from cyberpsychosis import get_cyberpsychosis

                get_cyberpsychosis().on_success(success_rate * 0.1)
            except (ImportError, RuntimeError):
                pass
        if state_obj.risk_level < 20:
            state_obj.increment_stealth_ops()

        state_obj.complete_assignment()
        # Сохранить активность для writeup
        state_obj.last_writeup_activity = {
            "type": "quiz",
            "topic": quiz_topic,
            "total_score": total_score,
            "max_total": max_total,
            "success_rate": success_rate,
            "timestamp": time.time(),
            "questions_count": len(questions),
            "responses": responses,
        }

        # Обновляем слабые темы (только два аргумента)
        state_obj.update_weak_topic(quiz_topic, success_rate)
        state_obj.schedule_review(quiz_topic, success_rate)

        # Auto-track skill from quiz topic
        try:
            from handlers.skills import guess_skill_from_topic

            skill = guess_skill_from_topic(quiz_topic)
            if skill:
                state_obj.track_skill(skill, success_rate >= 60, xp=int(total_score))
        except (ImportError, AttributeError):
            pass

        # Дать рекомендации
        if success_rate < 50:
            console.print("[red]Рекомендую повторить эту тему![/red]")
        elif success_rate < 70:
            console.print("[yellow]Есть пробелы - стоит потренировать[/yellow]")
        else:
            console.print("[green]Отлично! Тема усвоена[/green]")

        # Показать слабые темы если есть
        weak = state_obj.get_weak_topics(threshold=70.0)
        if weak:
            console.print(f"\n[bold cyan]Слабые темы (нужно повторить):[/bold cyan]")
            for w in weak[:5]:
                console.print(
                    f"  • {w['topic']}: {w['success_rate']:.1f}% ({w['attempts']} попыток)"
                )
    else:
        console.print("[dim]Нет результатов для анализа[/dim]")

    # Отмечаем прохождение квиза
    state_obj.take_quiz()
    newly_earned = state_obj.check_achievements()
    if newly_earned:
        for ach in newly_earned:
            console.print(f"[bold magenta]🏆 Достижение: {ach} [/bold magenta]")

    ctx.save_state()
    return True, None, None, True


def handle_task_action() -> HandlerResult:
    """Interactive practical task with answer evaluation."""
    if not GENERATORS_AVAILABLE:
        console.print("[yellow]Генератор заданий недоступен[/yellow]")
        return True, None, None, True

    ctx = get_context()
    state_obj = ctx.state
    from knowledge import get_current_vectordb

    vectordb = get_current_vectordb()

    # Определить тему: сначала смотрим слабые темы
    category = None
    weak_topic = state_obj.get_next_weak_topic(threshold=70.0)
    if weak_topic:
        category = weak_topic
        console.print(f"[cyan]🎯 Фокус на слабой теме: {weak_topic}[/cyan]")

    task = generate_task(vectordb, category=category)
    if not task:
        console.print("[yellow]Не удалось сгенерировать задание[/yellow]")
        return True, None, None, True

    console.print("[bold green]🎯 Практическое задание:[/bold green]")
    console.print(f"\n{task.question}\n")
    if task.hint:
        console.print(f"[dim]💡 Подсказка: {task.hint}[/dim]")
    console.print(
        "[yellow]Введите ваш ответ или команду. /skip - пропустить, /exit - выйти[/yellow]\n"
    )

    try:
        user_ans = input("Ваш ответ: ").strip()
        if user_ans.lower() in ["/exit", "/quit"]:
            console.print("[yellow]Задание прервано[/yellow]")
            return True, None, None, True
        if user_ans.lower() == "/skip":
            console.print("[dim]Пропущено[/dim]")
            score = 0
            feedback = "Пропущено"
        elif not user_ans:
            console.print("[dim]Пустой ответ[/dim]")
            score = 0
            feedback = "Пустой ответ"
        else:
            answer_lower = task.answer.lower()
            user_lower = user_ans.lower()
            ans_words = set(answer_lower.split())
            user_words = set(user_lower.split())
            common = ans_words.intersection(user_words)
            if len(common) >= max(1, len(ans_words) * 0.5):
                score = 10
                feedback = "✅ Верно! (по ключевым словам)"
            else:
                score = 0
                feedback = f"❌ Не совсем. Ожидались ключевые слова: {', '.join(list(ans_words)[:5])}"
    except KeyboardInterrupt:
        console.print("\n[yellow]Прервано[/yellow]")
        return True, None, None, True

    console.print(f"\n[bold]Результат:[/bold] {score}/10 - {feedback}")

    # Сохранить активность для writeup
    state_obj.last_writeup_activity = {
        "type": "task",
        "category": task.category,
        "question": task.question,
        "correct_answer": task.answer,
        "hint": task.hint,
        "user_answer": user_ans,
        "score": score,
        "feedback": feedback,
        "timestamp": time.time(),
    }

    # Обновить weak_topics (два аргумента)
    state_obj.update_weak_topic(task.category, score)
    state_obj.schedule_review(task.category, score)

    # Показать слабые темы
    weak = state_obj.get_weak_topics(threshold=70.0)
    if weak:
        console.print(f"\n[bold cyan]Слабые темы:[/bold cyan]")
        for w in weak[:5]:
            console.print(
                f"  • {w['topic']}: {w['success_rate']:.1f}% ({w['attempts']} попыток)"
            )

    ctx.save_state()
    return True, None, None, True


def handle_quiz_generation(
    action: str, conn: Any, llm_obj: Any = None
) -> HandlerResult:
    """Генерация квиза через /smart_test или /read_url"""
    if not GENERATORS_AVAILABLE:
        console.print("[yellow]Генератор квизов недоступен[/yellow]")
        return True, None, None, True

    from knowledge import get_current_vectordb

    vectordb = get_current_vectordb()
    quiz = generate_quiz(vectordb)
    console.print(
        f"[bold green]📝 Квиз сгенерирован: {len(quiz.get('questions', []))} вопросов[/bold green]"
    )
    questions = quiz.get("questions", [])
    quiz_topic = quiz.get("topic", "general")

    if not questions:
        console.print("[yellow]Не удалось сгенерировать вопросы[/yellow]")
        return True, None, None, True

    console.print(
        f"[bold green]📝 Интерактивный квиз: {len(questions)} вопросов по теме '{quiz_topic}'[/bold green]"
    )
    console.print(
        "[yellow]Напишите ответ на каждый вопрос. Введите /skip чтобы пропустить, /exit для выхода.[/yellow]\n"
    )

    scores = []
    responses = []
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
                scores.append((0, 10))
                responses.append(
                    {
                        "question": q.get("question", ""),
                        "user_answer": "<пропущено>",
                        "correct_answer": q.get("correct", ""),
                        "score": 0,
                        "feedback": "Пропущено",
                    }
                )
                continue
            if not user_ans:
                console.print("[dim]Пустой ответ[/dim]\n")
                scores.append((0, 10))
                responses.append(
                    {
                        "question": q.get("question", ""),
                        "user_answer": "",
                        "correct_answer": q.get("correct", ""),
                        "score": 0,
                        "feedback": "Пустой ответ",
                    }
                )
                continue
        except KeyboardInterrupt:
            console.print("\n[yellow]Прервано[/yellow]")
            break

        correct = q.get("correct", "")
        explanation = q.get("explanation", "")
        if "options" in q:
            if user_ans.upper() == correct.upper():
                score = 10
                feedback = "✅ Верно!"
            else:
                score = 0
                feedback = f"❌ Неверно. Правильный ответ: {correct}"
            if explanation:
                feedback += f"\n[dim]{explanation}[/dim]"
        else:
            result = check_open_answer(q.get("question", ""), user_ans, None)
            score = result["score"]
            feedback = result["feedback"]

        console.print(f"[bold]Результат:[/bold] {score}/10 - {feedback}\n")
        scores.append((score, 10))
        total_score += score
        max_total += 10

        responses.append(
            {
                "question": q.get("question", ""),
                "user_answer": user_ans,
                "correct_answer": correct if "options" in q else None,
                "score": score,
                "feedback": feedback,
            }
        )

    if scores:
        success_rate = (total_score / max_total * 100) if max_total > 0 else 0
        console.print(
            f"[bold]📊 Итог:[/bold] {total_score}/{max_total} ({success_rate:.1f}%)"
        )

        ctx = get_context()
        state_obj = ctx.state
        state_obj.update_weak_topic(quiz_topic, success_rate)
        state_obj.schedule_review(quiz_topic, success_rate)

        if success_rate < 50:
            console.print("[red]Рекомендую повторить эту тему![/red]")
        elif success_rate < 70:
            console.print("[yellow]Есть пробелы - стоит потренировать[/yellow]")
        else:
            console.print("[green]Отлично! Тема усвоена[/green]")

        weak = state_obj.get_weak_topics(threshold=70.0)
        if weak:
            console.print(f"\n[bold cyan]Слабые темы (нужно повторить):[/bold cyan]")
            for w in weak[:5]:
                console.print(
                    f"  • {w['topic']}: {w['success_rate']:.1f}% ({w['attempts']} попыток)"
                )
    else:
        console.print("[dim]Нет результатов для анализа[/dim]")

    return True, None, None, True


def handle_code_review(action: str, conn: Any = None) -> HandlerResult:
    """Анализ кода через /code_review"""
    console.print("[yellow]Отправьте код для анализа (в разработке)[/yellow]")
    # TODO: Реализовать интерактивный ввод кода или чтение из файла
    return True, None, None, True
