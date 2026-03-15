# handlers/quiz.py
import os
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

def handle_quiz_action() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        state_obj = get_state()
        from knowledge import get_current_vectordb
        vectordb = get_current_vectordb()
        if GENERATORS_AVAILABLE:
            quiz = generate_quiz(vectordb)
            console.print("[bold green]📝 Квиз сгенерирован![/bold green]")
            qs = quiz.get('questions', [])
            console.print(f"Количество вопросов: {len(qs)}\n")
            for i, q in enumerate(qs[:5], 1):
                console.print(f"{i}. {q.get('question', '?')}")
                if 'options' in q:
                    for opt in q['options']:
                        console.print(f"   - {opt}")
            if len(qs) > 5:
                console.print(f"... и еще {len(qs) - 5} вопросов")
            # Отмечаем прохождение квиза
            state_obj.take_quiz()
            newly_earned = state_obj.check_achievements()
            if newly_earned:
                for ach in newly_earned:
                    console.print(f"[bold magenta]🏆 Достижение: {ach['name']} ({ach['icon']}) +{ach.get('points',0)} XP[/bold magenta]")
        else:
            console.print("[yellow]Генератор квизов недоступен[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_task_action() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        from knowledge import get_current_vectordb
        vectordb = get_current_vectordb()
        if GENERATORS_AVAILABLE:
            task = generate_task(vectordb)
            if task:
                console.print("[bold green]🎯 Задание сгенерировано![/bold green]")
                console.print(f"**Вопрос:** {task.question}")
                if hasattr(task, 'hint') and task.hint:
                    console.print(f"💡 Подсказка: {task.hint}")
            else:
                console.print("[yellow]Не удалось сгенерировать задание[/yellow]")
        else:
            console.print("[yellow]Генератор заданий недоступен[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_quiz_generation(action: str, conn: Any, llm_obj: Any = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Генерация квиза через /smart_test или /read_url"""
    try:
        if GENERATORS_AVAILABLE:
            # generate_quiz возвращает dict с вопросами
            quiz = generate_quiz()
            console.print(f"[bold green]📝 Квиз сгенерирован: {len(quiz.get('questions', []))} вопросов[/bold green]")
            # TODO: Реализовать интерактивный режим прохождения квиза
            console.print("[yellow]Режим прохождения квиза в разработке. Показываю вопросы:[/yellow]")
            for i, q in enumerate(quiz.get('questions', [])[:5], 1):
                console.print(f"{i}. {q.get('question', '?')}")
                if 'options' in q:
                    for opt in q['options']:
                        console.print(f"   - {opt}")
            if len(quiz.get('questions', [])) > 5:
                console.print(f"... и еще {len(quiz['questions']) - 5} вопросов")
        else:
            console.print("[yellow]Генератор квизов недоступен[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка генерации квиза: {e}[/red]")
    return True, None, None, True


def handle_code_review(action: str, conn: Any = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Анализ кода через /code_review"""
    try:
        console.print("[yellow]Отправьте код для анализа (в разработке)[/yellow]")
        # TODO: Реализовать интерактивный ввод кода или чтение из файла
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True
