# handlers.py
import os
import re
import json
import logging
import shlex
from typing import Any, Dict, List, Optional, Tuple
from rich.console import Console
from rich.panel import Panel

# State Management
from state import get_state

# UI
console = Console()
logger = logging.getLogger(__name__)

# DB Operations (merged logic)
from memory import (
    clear_chat as db_clear_chat,
    get_stats,
    get_weak_topics,
    update_topic_progress
)
from knowledge import get_knowledge_status

# Tools
from code_review import code_review_function
try:
    from question_generation import generate_open_quiz
except:
    generate_open_quiz = lambda *args: None

def show_help():
    from ui import show_help as ui_help
    ui_help()

def show_menu():
    from ui import show_menu as ui_menu
    ui_menu()


def _ask_confirm(message: str) -> bool:
    try:
        from rich.prompt import Confirm
        return Confirm.ask(message)
    except Exception:
        resp = input(f"{message} (yn): ").strip().lower()
        return resp in ("y", "yes", "true", "1")

def clear_chat_db(conn: Any) -> None:
    try:
        db_clear_chat(conn)
    except Exception:
        pass

def extract_json_block(text: str) -> Optional[str]:
    if not text:
        return None
    stack = []
    start = None
    for i, ch in enumerate(text):
        if ch == '{':
            if start is None:
                start = i
            stack.append(ch)
        elif ch == '}':
            if stack:
                stack.pop()
                if not stack:
                    end = i + 1
                    return text[start:end]
    return None

def get_weak_topics(conn: Any) -> List[Dict[str, Any]]:
    try:
        from db_operations import get_weak_topics as _gt
        return _gt(conn)
    except Exception:
        return []

def fetch_and_summarize(topic: str, LLM: Any) -> Optional[Dict[str, Any]]:
    return None

def check_open_answer(question: str, user_ans: str, key_points: Optional[List[str]] = None) -> Dict[str, Any]:
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
        if found >= max(1, len(key_points)//2):
            score = min(10, score + 2)
            feedback = "Частично на ключевых моментах."
    return {"score": score, "feedback": feedback}

def handle_mode(action: str, conn: Any, mode: Optional[Any] = None, student_level: Optional[Any] = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    if action == "help":
        show_help()
        return True, mode, student_level, True
    if action == "menu":
        show_menu()
        return True, mode, student_level, True
    if action == "exit":
        console.print("[yellow]👋 Пока![yellow]")
        return False, mode, student_level, True
    if action == "clear":
        if _ask_confirm("[bold red]Очистить чат?[bold red]"):
            clear_chat_db(conn)
            console.print("[green]✅ Очищено[green]")
        return True, mode, student_level, True
    if action in ["kb_status", "check_kb"]:
        status = get_knowledge_status()
        if action == "kb_status":
            text = f"""
                [bold]📂 Файлов на диске:[bold] {status.get('files_on_disk', '?')}
                [bold]💾 Файлов в базе:[bold] {status.get('files_in_db', '?')}
                [bold]🧠 Всего чанков (фрагментов):[bold] {status.get('total_chunks', '?')}

                [bold]Список загруженных файлов:[bold]
            """
            files = status.get('list', [])
            if files:
                files_to_show = files[-15:]
                text += "\n".join([f"• {f}" for f in files_to_show])
                if len(files) > 15:
                    text += f"\n... и еще {len(files) - 15} файлов."
            else:
                text += "[yellow]База пуста[yellow]"
            console.print(text, title="📚 Состояние Базы Знаний", border="cyan")
        elif action == "check_kb":
            report = audit_knowledge_base()
            console.print(report, title="🧪 АУДИТ ЗНАНИЙ", border="cyan")
        return True, mode, student_level, True
    return True, mode, student_level, True

def handle_commands(action: str, conn: Any, LLM: Any, mode: Optional[Any] = None, student_level: Optional[Any] = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    # Если LLM - функция (lazy loading), вызываем для получения объекта
    llm_obj = LLM() if callable(LLM) else LLM
    
    if action == "stats":
        stats = get_stats(conn) or {}
        weak_topics = get_weak_topics(conn) if conn else []
        points = stats.get('points', 0) if stats else 0
        quizzes = stats.get('quizzes', 0) if stats else 0
        tasks = stats.get('tasks', 0) if stats else 0
        console.print(f"Очки: {points} | Квизов: {quizzes} | Задач: {tasks}")
        if weak_topics:
            topics_str = ", ".join([f"{t['topic']} ({t['rate']}%)" for t in weak_topics])
            console.print(f"Слабые темы: {topics_str}")
        return True, mode, student_level, True
    elif action == "clear":
        if _ask_confirm("[bold red]Очистить чат?[bold red]"):
            clear_chat_db(conn)
            console.print("[green]✅ Очищено[green]")
        return True, mode, student_level, True
    elif action == "exit":
        console.print("[yellow]👋 Пока![yellow]")
        return False, mode, student_level, True
    elif action in ["smart_test", "read_url"]:
        return handle_quiz_generation(action, conn, llm_obj, mode, student_level)
    elif action in ["quiz_review", "code_review", "review_code"]:
        return handle_code_review(action, conn=conn)
    elif action in ["news", "cve", "security_news", "quiz", "task", "story", "practice", "help", "menu", "guide", "courses", "next", "flag", "achievements", "writeup", "check", "logs", "terminal"]:
        return handle_extended_commands(action, llm_obj)
    elif action == "ctf":
        from ui import Mode
        return True, Mode.CTF, student_level, True
    elif action == "teacher":
        from ui import Mode
        return True, Mode.TEACHER, student_level, True
    elif action == "expert":
        from ui import Mode
        return True, Mode.EXPERT, student_level, True
    elif action == "review":
        from ui import Mode
        return True, Mode.CODE_REVIEW, student_level, True
    elif action.startswith("course") or action.startswith("lab") or action == "htb":
        return handle_extended_commands(action, llm_obj)
    else:
        # Это не команда - вернём False чтобы main.py отправил вопрос LLM
        return True, mode, student_level, False

def handle_security_news(action: str, LLM: Any):
    """Обработка команды /news"""
    console.print("[cyan]Загружаю новости...[/cyan]")
    try:
        from news_fetcher import fetch_news
        news = fetch_news(force=(action == "cve"))
        
        if not news:
            console.print("[yellow]Новостей нет.[/yellow]")
            return True, None, None, True
        
        # Формируем для LLM
        news_for_llm = "\n".join([f"- {n.get('title','')}" for n in news[:5]])
        
        # Если LLM доступен - обрабатываем
        llm_obj = LLM() if callable(LLM) else LLM
        if llm_obj:
            console.print("[cyan]Обрабатываю новости...[/cyan]")
            prompt = f"""Кратко переведи на русский и опиши каждую новость в 1-2 предложениях:

{news_for_llm}

Формат:
1. [Название] - Краткое описание"""
            try:
                processed = llm_obj.invoke(prompt)
                news_text = processed
            except:
                news_text = news_for_llm
        else:
            news_text = news_for_llm
        
        # Сохраняем в state
        get_state().last_news = news_text
        console.print(Panel(news_text[:800], title="НОВОСТИ"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def get_last_news():
    """Получить последние новости для промта"""
    return get_state().last_news

def handle_extended_commands(action: str, LLM: Any):
    """Расширенные команды"""
    if action in ["news", "cve", "security_news"]:
        return handle_security_news(action, LLM)
    elif action in ["story", "episode", "quest"]:
        return handle_story_mode(action)
    elif action.startswith("flag"):
        # /flag <флаж>
        flag = action.split(" ", 1)[1] if " " in action else None
        return handle_flag_check(flag)
    elif action == "achievements" or action == "achievement":
        return handle_achievements()
    elif action == "practice":
        return handle_practice(action)
    elif action.startswith("lab") or action == "htb":
        return handle_practice(action)
    elif action == "next":
        return handle_course("next")
    elif action.startswith("course") or action == "courses":
        return handle_course(action)
    elif action == "quiz":
        return handle_quiz_action()
    elif action == "task":
        return handle_task_action()
    elif action == "help":
        from ui import show_help
        show_help()
        return True, None, None, True
    elif action == "menu":
        from ui import show_menu
        show_menu()
        return True, None, None, True
    elif action == "guide":
        try:
            with open("docs/ГАЙД_VM.md", "r", encoding="utf-8") as f:
                guide = f.read()
            console.print(Panel(guide[:1000], title="ГАЙД ПО LAB"))
        except:
            console.print("[yellow]Гайд не найден[/yellow]")
        return True, None, None, True
    elif action == "check" or action == "logs":
        return handle_container_check(action)
    elif action == "terminal" or action == "term":
        return handle_terminal_log()
    elif action == "history":
        return handle_history(conn)
    elif action == "version":
        return handle_version()
    elif action.startswith("log "):
        # log <команда> - записать команду в лог
        return handle_terminal_log(action[4:])
    elif action == "writeup":
        return handle_writeup()
    else:
        # Не команда - отправим LLM
        return True, None, None, False


def handle_history(conn):
    """Показать последние сообщения чата"""
    try:
        from memory import get_chat_history
        history = get_chat_history(conn, limit=10)
        if not history:
            console.print("[yellow]История чата пуста[/yellow]")
        else:
            console.print(Panel("\n".join([f"[bold]{m['role']}:[/bold] {m['content'][:100]}" for m in history[::-1]]), title="📜 История (последние 10)"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_version():
    """Показать версию проекта"""
    try:
        import subprocess
        result = subprocess.run(['git', 'log', '-1', '--pretty=format:%h %s'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            commit = result.stdout.strip()
            console.print(Panel(f"CyberTeacher v3.2\n[cyan]{commit}[/cyan]", title="Версия"))
        else:
            console.print(Panel("CyberTeacher v3.2\nGit недоступен", title="Версия"))
    except:
        console.print(Panel("CyberTeacher v3.2", title="Версия"))
    return True, None, None, True


def __main__run_demo():
    conn = None
    LLM = None
    handle_commands("stats", conn, LLM)

if __name__ == "__main__":
    __main__run_demo()
