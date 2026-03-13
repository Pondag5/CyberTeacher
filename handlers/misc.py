# handlers/misc.py (дополнительные функции, которые не warranted отдельного файла)
import os
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from state import get_state

console = Console()

def _ask_confirm(message: str) -> bool:
    try:
        from rich.prompt import Confirm
        return Confirm.ask(message)
    except Exception:
        resp = input(f"{message} (yn): ").strip().lower()
        return resp in ("y", "yes", "true", "1")

def clear_chat_db(conn: Any) -> None:
    try:
        from memory import clear_chat as db_clear_chat
        db_clear_chat(conn)
    except Exception:
        pass

def extract_json_block(text: str) -> Optional[str]:
    if not text:
        return None
    stack = []
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if start is None:
                start = i
            stack.append(ch)
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack:
                    end = i + 1
                    return text[start:end]
    return None

def check_open_answer(
    question: str,
    user_ans: str,
    key_points: Optional[List[str]] = None,
) -> Dict[str, Any]:
    score = 0
    feedback = "Спасибо за ответ."
    if user_ans and len(user_ans.strip()) > 0:
        score = 6
        if "правильно" in user_ans.lower() or "верно" in user_ans.lower():
            score = 9
            feedback = "Отлично!"
    if key_points:
        found = 0
        upp = user_ans.lower() if user_ans else ""
        for kp in key_points:
            if kp.lower() in upp:
                found += 1
        if found >= max(1, len(key_points) // 2):
            score = min(10, score + 2)
            feedback = "Частично на ключевых моментах."
    return {"score": score, "feedback": feedback}

def handle_story_mode(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Режим истории (20 эпизодов)"""
    try:
        console.print("[yellow]Режим истории временно недоступен[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_history(conn) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        from memory import get_chat_history
        history = get_chat_history(conn, limit=20)
        if history:
            console.print("[bold cyan]📜 История чата:[/bold cyan]")
            for msg in history:
                role = msg.get('role', '?')
                content = msg.get('content', '')[:150]
                console.print(f"[{role}] {content}")
        else:
            console.print("[yellow]История пуста[/yellow]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

def handle_course(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    console.print("[yellow]Курсы временно недоступны[/yellow]")
    return True, None, None, True

def handle_terminal_log(action: Optional[str] = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        from terminal_log import get_terminal_log, log_command
        if action and action.startswith("log "):
            cmd = action[4:].strip()
            log_command(cmd, is_input=False)
            console.print(f"[green]✅ Команда записана в лог[/green]")
            return True, None, None, True
        log_text = get_terminal_log(last_n=20)
        console.print(Panel(log_text, title="📟 Терминал (последние 20 строк)", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_version() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    console.print("[bold cyan]CyberTeacher v3.2[/bold cyan]")
    console.print("Обучение кибербезопасности с LLM")
    console.print("Основано на: Ollama/OpenRouter, ChromaDB, Rich")
    console.print("© 2025 CyberTeacher Project")
    return True, None, None, True

def handle_writeup() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
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

def handle_add_book(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
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
            console.print("[red]❌ Запрещенный путь. Файл должен находиться в knowledge_base/[/red]")
            return True, None, None, True

        if not src_path.lower().endswith('.pdf'):
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
        console.print("[cyan]Перезапустите приложение или запустите переиндексацию чтобы обновить базу.[/cyan]")

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True