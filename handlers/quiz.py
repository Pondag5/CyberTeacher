# handlers/quiz.py
import os
import time
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console

from state import get_state

console = Console()

# Generators (quiz/task) - optional import
try:
    from generators import generate_quiz, generate_task

    GENERATORS_AVAILABLE = True
except ImportError:
    GENERATORS_AVAILABLE = False

# Import check_open_answer for evaluating open-ended responses
try:
    from .misc import check_open_answer
except ImportError:
    # Fallback: define locally if misc not available
    def check_open_answer(question, user_ans, key_points=None):
        score = 0
        feedback = "Спасибо за ответ."
        if user_ans and len(user_ans.strip()) > 0:
            score = 6
        return {"score": score, "feedback": feedback}


def handle_quiz_action() -> tuple[bool, Any | None, Any | None, bool]:
    """Интерактивный квиз с оценкой ответов и адаптивным обучением"""
    try:
        state_obj = get_state()
        from knowledge import get_current_vectordb

        vectordb = get_current_vectordb()

        if not GENERATORS_AVAILABLE:
            console.print("[yellow]Генератор квизов недоступен[/yellow]")
            return True, None, None, True

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

        scores = []  # List of (score, max_score) for each question
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
            key_points = None
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
                result = check_open_answer(q.get("question", ""), user_ans, key_points)
                score = result["score"]
                feedback = result["feedback"]

            console.print(f"[bold]Результат:[/bold] {score}/10 - {feedback}\n")
            scores.append((score, 10))
            total_score += score
            max_total += 10

            # Record response for writeup
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

            # === C-13: Изменение уровня риска и отслеживание стелс-операций ===
            if success_rate < 50:
                state_obj.increase_risk(10)
            else:
                state_obj.decrease_risk(5)
            if state_obj.risk_level < 20:
                state_obj.increment_stealth_ops()
            # Отметить завершение задания
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

            # Обновить weak_topics
            state_obj.update_weak_topic(quiz_topic, total_score, max_total)

            # Запланировать следующее повторение (Spaced Repetition)
            state_obj.schedule_review(quiz_topic, total_score, max_total)

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
                console.print(
                    f"\n[bold cyan]Слабые темы (нужно повторить):[/bold cyan]"
                )
                for w in weak[:5]:
                    console.print(
                        f"  • {w['topic']}: {w['success_rate']:.1f}% ({w['attempts']} попыток)"
                    )
        else:
            console.print("[dim]Нет результатов для анализа[/dim]")
        if scores:
            success_rate = (total_score / max_total * 100) if max_total > 0 else 0
            console.print(
                f"[bold]📊 Итог:[/bold] {total_score}/{max_total} ({success_rate:.1f}%)"
            )

            # Обновить weak_topics
            state_obj.update_weak_topic(quiz_topic, total_score, max_total)

            # Запланировать следующее повторение (Spaced Repetition)
            state_obj.schedule_review(quiz_topic, total_score, max_total)

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
                console.print(
                    f"\n[bold cyan]Слабые темы (нужно повторить):[/bold cyan]"
                )
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
                console.print(
                    f"[bold magenta]🏆 Достижение: {ach['name']} ({ach['icon']}) +{ach.get('points', 0)} XP[/bold magenta]"
                )

        # Сохранить состояние
        state_obj.save_to_file()

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback

        traceback.print_exc()
    return True, None, None, True


def handle_task_action() -> tuple[bool, Any | None, Any | None, bool]:
    """Интерактивное практическое задание с оценкой ответа"""
    try:
        state_obj = get_state()
        from knowledge import get_current_vectordb

        vectordb = get_current_vectordb()

        if not GENERATORS_AVAILABLE:
            console.print("[yellow]Генератор заданий недоступен[/yellow]")
            return True, None, None, True

        # Определить тему: сначала смотрим слабые темы
        category = None
        weak_topic = state_obj.get_next_weak_topic(threshold=70.0)
        if weak_topic:
            # Маппинг weak_topic в category для generate_task
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
            "[yellow]Ведите ваш ответ или команду. /skip - пропустить, /exit - выйти[/yellow]\n"
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
                # Простая проверка: если answer содержит ключевые слова
                answer_lower = task.answer.lower()
                user_lower = user_ans.lower()
                # Проверяем пересечение ключевых слов (разбиваем на слова)
                ans_words = set(answer_lower.split())
                user_words = set(user_lower.split())
                common = ans_words.intersection(user_words)
                # Если overlap >= 50% слов из ответа - засчитываем
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

        # Обновить weak_topics по категории задачи
        state_obj.update_weak_topic(task.category, score, 10)

        # Запланировать следующее повторение (Spaced Repetition)
        state_obj.schedule_review(task.category, score, 10)

        # Показать слабые темы
        weak = state_obj.get_weak_topics(threshold=70.0)
        if weak:
            console.print(f"\n[bold cyan]Слабые темы:[/bold cyan]")
            for w in weak[:5]:
                console.print(
                    f"  • {w['topic']}: {w['success_rate']:.1f}% ({w['attempts']} попыток)"
                )

        state_obj.save_to_file()

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback

        traceback.print_exc()
    return True, None, None, True


def handle_quiz_generation(
    action: str, conn: Any, llm_obj: Any = None
) -> tuple[bool, Any | None, Any | None, bool]:
    """Генерация квиза через /smart_test или /read_url"""
    try:
        if GENERATORS_AVAILABLE:
            # generate_quiz возвращает dict с вопросами
            quiz = generate_quiz()
            console.print(
                f"[bold green]📝 Квиз сгенерирован: {len(quiz.get('questions', []))} вопросов[/bold green]"
            )
            # TODO: Реализовать интерактивный режим прохождения квиза
            console.print(
                "[yellow]Режим прохождения квиза в разработке. Показываю вопросы:[/yellow]"
            )
            for i, q in enumerate(quiz.get("questions", [])[:5], 1):
                console.print(f"{i}. {q.get('question', '?')}")
                if "options" in q:
                    for opt in q["options"]:
                        console.print(f"   - {opt}")
            if len(quiz.get("questions", [])) > 5:
                console.print(f"... и еще {len(quiz['questions']) - 5} вопросов")
        else:
            console.print("[yellow]Генератор квизов недоступен[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка генерации квиза: {e}[/red]")
    return True, None, None, True


def handle_code_review(
    action: str, conn: Any = None
) -> tuple[bool, Any | None, Any | None, bool]:
    """Анализ кода через /code_review"""
    try:
        console.print("[yellow]Отправьте код для анализа (в разработке)[/yellow]")
        # TODO: Реализовать интерактивный ввод кода или чтение из файла
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True
