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
    elif action.startswith("log "):
        # log <команда> - записать команду в лог
        return handle_terminal_log(action[4:])
    elif action == "writeup":
        return handle_writeup()
    else:
        # Не команда - отправим LLM
        return True, None, None, False

def handle_container_check(action: str):
    """Проверить контейнер - логи, статус"""
    try:
        from practice import get_all_running_labs, get_container_logs, DOCKER_LABS
        from main import get_learning_context
        
        running_labs = get_all_running_labs()
        
        if not running_labs:
            console.print("[yellow]Нет запущенных контейнеров[/yellow]")
            return True, None, None, True
        
        # Получаем текущую лабу из контекста
        learning_ctx = get_learning_context()
        current_lab = learning_ctx.get("current_lab", None)
        
        # Если есть текущая лаба - показываем её
        if current_lab and current_lab in running_labs:
            lab_info = running_labs[current_lab]
            web_name = f"{current_lab}-web"
            logs = get_container_logs(web_name, lines=30)
            
            console.print(Panel(f"""
🔴 СТАТУС: {lab_info['name']}
📊 Состояние: {lab_info['status']}

📝 ПОСЛЕДНИЕ ЛОГИ:
{logs}
            """, title="🔍 ПРОВЕРКА КОНТЕЙНЕРА", border_style="cyan"))
        else:
            # Показываем все запущенные
            text = "🔴 ЗАПУЩЕННЫЕ ЛАБЫ:\n\n"
            for lab_key, lab_info in running_labs.items():
                text += f"• {lab_info['name']}: {lab_info['status']}\n"
                ports = ", ".join([f"localhost:{p}" for p in lab_info.get('ports', {}).keys()])
                text += f"  Доступ: {ports}\n\n"
            console.print(Panel(text, title="🔍 КОНТЕЙНЕРЫ", border_style="cyan"))
            
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_terminal_log(command: str = None):
    """Обработка /terminal - показать лог команд ученика"""
    try:
        from terminal_log import get_terminal_log, log_command
        
        if command:
            # Записать команду
            log_command(command, is_input=True)
            console.print(f"[green]✓ Записано: {command}[/green]")
        else:
            # Показать лог
            log = get_terminal_log(last_n=15)
            console.print(Panel(log[:2000], title="📟 ТЕРМИНАЛ УЧЕНИКА", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_quiz_action():
    """Обработка /quiz"""
    try:
        from question_generation import generate_open_quiz, check_open_answer
        topic = console.input("[cyan]Тема (sql/xss/network/crypto/linux или Enter - случайно): [/cyan]")
        q = generate_open_quiz(topic=topic or "")
        
        console.print(Panel(f"[bold]{q['question']}[/bold]", title="ВИКТОРИНА"))
        answer = console.input("[yellow]Твой ответ: [/yellow]")
        
        result = check_open_answer(q['question'], answer, q.get('key_points', []))
        
        score = result.get('score', 0)
        color = "green" if score >= 7 else "yellow" if score >= 4 else "red"
        console.print(f"[{color}]Оценка: {score}/10[/{color}]")
        console.print(f"[cyan]Отзыв: {result.get('feedback', '')}[/cyan]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_task_action():
    """Обработка /task"""
    try:
        from practice import PracticeHub
        lab = PracticeHub.get_lab()
        console.print(Panel(f"""
[b]Задание:[/b] {lab.name}
[b]Категория:[/b] {lab.category}
[b]Сложность:[/b] {lab.difficulty}
[b]Описание:[/b] {lab.description}
[b]Техника:[/b] {lab.technique}
[b]Инструменты:[/b] {', '.join(lab.tools)}
        """, title="ЗАДАНИЕ"))
    except:
        console.print("[yellow]Задание: Найди и изучи уязвимость SQL-инъекция в DVWA[/yellow]")
    return True, None, None, True

def handle_story_mode(action: str):
    try:
        from story_mode import start_story_mode, get_story_list, get_achievements_list
        if action == "story":
            text = start_story_mode()
        elif action == "story list":
            text = get_story_list()
        else:
            text = get_story_list()
        console.print(Panel(text, title="🎮 STORY MODE", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    return True, None, None, True

def handle_flag_check(flag: str = None):
    """Проверить флаг"""
    if not flag:
        console.print("[yellow]Введи флаг: /flag FLAG{...}[/yellow]")
        return True, None, None, True
    
    try:
        from story_mode import submit_flag
        result = submit_flag(flag)
        console.print(Panel(result, title="🏴 ФЛАГ", border_style="green"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_achievements():
    """Показать достижения"""
    try:
        from story_mode import get_achievements_list, get_player
        player = get_player()
        text = get_achievements_list()
        text += f"\n\n📊 Твой XP: {player.xp} | Уровень: {player.level}"
        console.print(Panel(text, title="🏆 ДОСТИЖЕНИЯ", border_style="gold"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_writeup():
    """Обработка /writeup - шаблон writeup"""
    try:
        from main import get_learning_context
        
        ctx = get_learning_context()
        course = ctx.get("current_course", "не выбран")
        topic = ctx.get("current_topic", "не выбрана")
        lab = ctx.get("current_lab", "не запущена")
        
        writeup_template = f"""
╔══════════════════════════════════════════════════════╗
║              📝 ШАБЛОН WRITEUP                      ║
╚══════════════════════════════════════════════════════╝

🎯 ЦЕЛЬ: {lab}

📚 КУРС: {course}
📖 ТЕМА: {topic}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔍 РАЗВЕДКА (Recon)
Опиши здесь:
- Собранная информация
- Найденные сервисы/порты
- Сканирование директорий

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚠️ ЭКСПЛУАТАЦИЯ (Exploitation)
Опиши здесь:
- Найденные уязвимости
- Использованные техники
- Пейлоады

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📊 ПОСТЭКСПЛУАТАЦИЯ (Post-Exploitation)
Опиши здесь:
- Полученный доступ
- Собранные данные/флаги
- Повышение привилегий

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 💡 ВЫВОДЫ
Что было изучено:
- 

Использованные инструменты:
-

"""
        console.print(Panel(writeup_template, title="📝 WRITEUP", border_style="green"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_course(action: str):
    """Обработка курсов"""
    # Если это не команда курса - отправить LLM
    if not action.startswith("course") and action != "courses" and action != "next":
        return True, None, None, False
    
    try:
        from courses import list_courses, start_course, get_course_progress, COURSES, COURSE_MAP
        from main import set_learning_context
        
        state = get_state()
        
        if action == "courses" or action == "courses 1":
            text = list_courses()
        elif action.startswith("course ") or action == "course" or action.startswith("courses "):
            if action.startswith("course "):
                course_input = action.split(" ", 1)[1].strip()
            elif action.startswith("courses "):
                course_input = action.split(" ", 1)[1].strip()
            else:
                course_input = None
            
            if course_input:
                # Проверяем - номер это или ID (используем модульный COURSE_MAP)
                if course_input in COURSE_MAP:
                    course_id = COURSE_MAP[course_input]
                else:
                    course_id = course_input  # если это буквенный ID
                
                state.set_course(course_id)
                text = start_course(course_id)
                
                # Обновляем контекст обучения - передаем НАЗВАНИЕ темы!
                course = COURSES.get(course_id, {})
                if course.get("topics"):
                    first_topic = course["topics"][0]
                    set_learning_context(course=course.get("name", course_id), topic=first_topic.name, lab=first_topic.labs[0] if first_topic.labs else None)
            else:
                text = list_courses()
        elif action == "next":
            if state.current_course:
                state.next_topic()
                text = get_course_progress(state.current_course, state.current_topic)
                # Обновляем контекст - передаем тему
                course = COURSES.get(state.current_course, {})
                topics = course.get("topics", [])
                if state.current_topic < len(topics):
                    next_topic = topics[state.current_topic]
                    set_learning_context(topic=next_topic.name)
            else:
                text = "Сначала выбери курс: /course <номер>"
        else:
            text = list_courses()
        
        console.print(Panel(text, title="📚 КУРСЫ", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_practice(action: str):
    """Обработка практики"""
    try:
        from practice import (
            start_practice, list_practices, get_htb_recommendation,
            list_labs, start_lab, stop_lab, DOCKER_LABS
        )
        from main import set_learning_context
        
        if action == "practice":
            practice_text = start_practice()
        elif action == "htb":
            practice_text = get_htb_recommendation()
        elif action == "lab":
            practice_text = list_labs()
        elif action.startswith("lab "):
            parts = action.split()
            if len(parts) >= 2:
                cmd = parts[1]
                lab_name = parts[2] if len(parts) > 2 else None
                if cmd == "start" and lab_name:
                    practice_text = start_lab(lab_name)
                    # Обновляем контекст - какая лаба запущена
                    lab_info = DOCKER_LABS.get(lab_name, {})
                    set_learning_context(lab=lab_info.get("name", lab_name))
                elif cmd == "stop" and lab_name:
                    practice_text = stop_lab(lab_name)
                else:
                    practice_text = list_labs()
            else:
                practice_text = list_labs()
        else:
            practice_text = list_practices()
        
        console.print(Panel(practice_text, title="🔬 PRACTICE HUB", border_style="green"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_quiz_generation(action: str, conn: Any, LLM: Any, mode: Optional[Any] = None, student_level: Optional[Any] = None):
    if action in ["smart_test", "read_url"]:
        topic = input("Тема (или Enter для общей): ")
        if action == "smart_test":
            try:
                q_data = generate_open_quiz(conn, topic)
            except Exception:
                q_data = None
        else:
            q_data = fetch_and_summarize(topic, LLM)
        if not q_data:
            console.print("[red]Не удалось сгенерировать вопрос.[red]")
            return True, mode, student_level, True
        user_ans = input("\n[bold yellow]Твой ответ:[bold yellow]: ")
        if action == "smart_test":
            result = check_open_answer(q_data.get('question'), user_ans, q_data.get('key_points', []))
            score = result.get('score', 0)
            feedback = result.get('feedback', '')
            color = "green" if score >= 7 else "yellow" if score >= 4 else "red"
            console.print(f"\n[bold {color}]Оценка: {score}10[bold {color}]")
            console.print(f"[cyan]📚 Отзыв:[cyan] {feedback}")
            console.print(f"[dim]Ожидаемые моменты: {', '.join(q_data.get('key_points', []))}[dim]")
        else:
            console.print("[blue]Чтение URL не реализовано в демо-версии.[blue]")
        return True, mode, student_level, True
    return True, mode, student_level, True

def handle_code_review(action: str, conn: Any = None, code_text: Optional[str] = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    if action in ["review", "code_review", "quiz_review"]:
        if code_text is None:
            console.print("[cyan]🔍 Код-ревью[cyan]")
            lines = []
            while True:
                line = input("Введите код (в конце напиши end):")
                if line.strip() == "end":
                    break
                lines.append(line)
            code_text = "\n".join(lines)
        if not code_text:
            console.print("[yellow]Нет кода для анализа.[yellow]")
            return True, None, None, True
        result = code_review_function(code_text)
        if isinstance(result, dict) and result.get("vulnerabilities"):
            for v in result["vulnerabilities"]:
                sev = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(v.get("severity", "low"), "⚪")
                console.print(f"\n[bold]{sev} {v.get('type')} (строка {v.get('line')})[bold]")
                console.print(f"  {v.get('description')}")
                console.print(f"  [green]Исправление:[green] {v.get('fix')}")
            console.print(f"[bold]{result.get('overall_score', 'NA')}\n{result.get('summary', '')}", title="📊", border="green")
            if result.get("fixed_code"):
                console.print(f"[bold green]🛠️ Исправленный код:[bold green]\\n\\n{result.get('fixed_code')}", title="✅ Patch", border="green")
        else:
            console.print("[green]Уязвимостей не найдено![green]")
        return True, None, None, True
    return True, None, None, True

def handle_mode_ctf(action: str):
    if action == "mode_ctf":
        return True, None, None, True
    return True, None, None, True

def classify_intent(text: str, LLM: Any) -> Optional[str]:
    """
    Классифицирует ввод пользователя: команда или вопрос.
    Возвращает имя команды (без /) или None.
    """
    if not text or len(text) > 40: # Слишком длинный для команды
        return None
        
    prompt = f"""
    Анализируй ввод пользователя и определи, хочет ли он вызвать команду.
    Команды: stats (очки, прогресс), news (новости, CVE), quiz (тест, викторина), task (задание), story (история), guide (гайд), exit (выход).
    Ввод: "{text}"
    Ответь ТОЛЬКО одним словом: имя команды или None.
    """
    try:
        # Используем LLM напрямую (без стриминга)
        response = LLM.invoke(prompt).strip().lower()
        if any(cmd in response for cmd in ["stats", "news", "quiz", "task", "story", "guide", "exit"]):
             # Находим первое совпадение
             for cmd in ["stats", "news", "quiz", "task", "story", "guide", "exit"]:
                 if cmd in response: return cmd
    except:
        pass
    return None

def handle_command(
    action: str,
    vectordb: Any,
    conn: Any,
    mode: Optional[Any] = None,
    student_level: Optional[Any] = None,
    LLM: Optional[Any] = None
) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    # Убираем / в начале команды
    if action.startswith('/'):
        return handle_commands(action[1:], conn, LLM, mode=mode, student_level=student_level)
    
    # Пытаемся классифицировать через LLM
    llm_obj = LLM() if callable(LLM) else LLM
    intent = classify_intent(action, llm_obj)
    
    if intent:
        # Это команда!
        return handle_commands(intent, conn, LLM, mode=mode, student_level=student_level)
    
    # Это не команда - вернём False чтобы main.py отправил вопрос LLM
    return True, mode, student_level, False

def __main__run_demo():
    conn = None
    LLM = None
    handle_commands("stats", conn, LLM)

if __name__ == "__main__":
    __main__run_demo()
