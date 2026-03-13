# handlers.py
import json
import logging
import os
import re
import shlex
import random
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel

# State Management
from state import get_state

# UI
console = Console()
logger = logging.getLogger(__name__)

# Tools
from code_review import code_review_function

# Knowledge base status
from knowledge import get_knowledge_status
# Assignment generator
try:
    from assignment_generator import generate_assignment, AssignmentGenerator
    ASSIGNMENT_GEN_AVAILABLE = True
except ImportError:
    ASSIGNMENT_GEN_AVAILABLE = False

# Generators (quiz/task)
try:
    from generators import generate_quiz, generate_task
    GENERATORS_AVAILABLE = True
except ImportError:
    GENERATORS_AVAILABLE = False

# Config
from config import KNOWLEDGE_DIR, RESPONSE_CACHE_SIZE, RESPONSE_CACHE_FILE

# DB Operations
from memory import (
    clear_chat as db_clear_chat,
    get_stats,
    get_weak_topics,
    update_topic_progress
)

import json
import os

# LLM Response Cache with LRU eviction
from collections import OrderedDict, deque
class ResponseCache:
    def __init__(self, capacity: int = RESPONSE_CACHE_SIZE):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.access_order = deque(maxlen=capacity)
        self.hit_count = 0
        self.access_count = 0
        self._load()
    
    def _load(self):
        """Загрузить кэш из файла."""
        try:
            if os.path.exists(RESPONSE_CACHE_FILE):
                with open(RESPONSE_CACHE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.cache = OrderedDict(data.get('cache', {}))
                self.access_order = deque(data.get('access_order', []), maxlen=self.capacity)
                self.hit_count = data.get('hit_count', 0)
                self.access_count = data.get('access_count', 0)
                # Ограничиваем размер
                if len(self.cache) > self.capacity:
                    # Удаляем самые старые (первые в access_order)
                    for key in list(self.access_order)[:-self.capacity]:
                        self.cache.pop(key, None)
                    self.access_order = deque(list(self.access_order)[-self.capacity:], maxlen=self.capacity)
        except Exception as e:
            console.print(f"[yellow]⚠️ Не удалось загрузить кэш ответов: {e}[/yellow]")
    
    def _save(self):
        """Сохранить кэш в файл."""
        try:
            os.makedirs(os.path.dirname(RESPONSE_CACHE_FILE), exist_ok=True)
            data = {
                'cache': dict(self.cache),
                'access_order': list(self.access_order),
                'hit_count': self.hit_count,
                'access_count': self.access_count
            }
            with open(RESPONSE_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            console.print(f"[yellow]⚠️ Не удалось сохранить кэш ответов: {e}[/yellow]")
    
    def get(self, key: str) -> Optional[Any]:
        self.access_count += 1
        if key not in self.cache:
            return None
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        self.access_order.remove(key)
        self.access_order.append(key)
        self.hit_count += 1
        return self.cache[key]
    
    def put(self, key: str, value: Any):
        if key in self.cache:
            self.cache.move_to_end(key)
            self.access_order.remove(key)
        self.cache[key] = value
        self.access_order.append(key)
        if len(self.cache) > self.capacity:
            oldest = self.access_order.popleft()
            del self.cache[oldest]
    
    def clear(self):
        self.cache.clear()
        self.access_order.clear()
        self.hit_count = 0
        self.access_count = 0
    
    def stats(self) -> Dict:
        return {
            "size": len(self.cache),
            "capacity": self.capacity,
            "hit_count": self.hit_count,
            "access_count": self.access_count
        }

_response_cache = ResponseCache(RESPONSE_CACHE_SIZE)

def clear_response_cache():
    """Очистить кэш ответов LLM."""
    _response_cache.clear()
    # Сохраняем пустой кэш на диск
    try:
        _response_cache._save()
    except Exception:
        pass

def show_cache_stats():
    """Показать статистику кэша."""
    stats = _response_cache.stats()
    console.print(f"[bold cyan]📊 Статистика кэша ответов:[/bold cyan]")
    console.print(f"  Размер: {stats['size']} / {stats['capacity']}")
    if stats['access_count'] > 0:
        hit_rate = (stats['hit_count'] / stats['access_count']) * 100
        console.print(f"  Hit rate: {stats['hit_count']}/{stats['access_count']} ({hit_rate:.1f}%)")
    console.print(f"  Команды: /clearcache - очистить, /cache stats - показать")




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
    question: str, user_ans: str, key_points: Optional[List[str]] = None
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


def handle_mode(
    action: str,
    conn: Any,
    mode: Optional[Any] = None,
    student_level: Optional[Any] = None,
) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
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
    if action == "clearcache":
        clear_response_cache()
        console.print("[green]✅ Кэш ответов очищен[/green]")
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
            files = status.get("list", [])
            if files:
                files_to_show = files[-15:]
                text += "\n".join([f"• {f}" for f in files_to_show])
                if len(files) > 15:
                    text += f"\n... и еще {len(files) - 15} файлов."
            else:
                text += "[yellow]База пуста[yellow]"
            console.print(Panel(text, title="📚 Состояние Базы Знаний", border_style="cyan"))
        elif action == "check_kb":
            # Простой аудит: покажем статус
            console.print(Panel(str(status), title="🧪 АУДИТ ЗНАНИЙ", border_style="cyan"))
        elif action == "genassignment":
            if not ASSIGNMENT_GEN_AVAILABLE:
                console.print("[yellow]Модуль генератора заданий не доступен. Установите зависимости.[/yellow]")
                return True, mode, student_level, True
            
            # Парсим аргументы: /genassignment <topic> [type] [difficulty]
            parts = action.split()
            if len(parts) < 2:
                console.print("[cyan]Использование: /genassignment <topic> [type] [difficulty][/cyan]")
                console.print("Пример: /genassignment 'SQL Injection' ctf intermediate")
                console.print("Типы: ctf, lab, exercise | Сложность: beginner, intermediate, advanced")
                return True, mode, student_level, True
            
            topic = parts[1]
            a_type = parts[2] if len(parts) > 2 else random.choice(list(AssignmentGenerator.ASSIGNMENT_TYPES.keys()))
            difficulty = parts[3] if len(parts) > 3 else "intermediate"
            
            if a_type not in AssignmentGenerator.ASSIGNMENT_TYPES:
                console.print(f"[yellow]Неизвестный тип '{a_type}'. Доступные: {', '.join(AssignmentGenerator.ASSIGNMENT_TYPES.keys())}[/yellow]")
                return True, mode, student_level, True
            
            console.print(f"[cyan]Генерирую задание по теме '{topic}'...[/cyan]")
            try:
                assignment = generate_assignment(topic, difficulty=difficulty, assignment_type=a_type)
                
                console.print(f"\n[bold green]📝 Задание сгенерировано![/bold green]")
                console.print(f"[bold]ID:[/bold] {assignment['id']}")
                console.print(f"[bold]Тип:[/bold] {AssignmentGenerator.ASSIGNMENT_TYPES[a_type]['name']}")
                console.print(f"[bold]Сложность:[/bold] {difficulty} | [bold]Очки:[/bold] {assignment['points']}")
                console.print(f"[bold]Оценка времени:[/bold] {assignment['time_estimate']}\n")
                
                console.print("[bold]📌 Заголовок:[/bold]")
                console.print(assignment['title'])
                console.print("\n[bold]📋 Описание:[/bold]")
                console.print(assignment['description'])
                console.print("\n[bold]🎯 Сценарий:[/bold]")
                console.print(assignment['scenario'])
                
                if assignment.get('flags'):
                    console.print("\n[bold]🚩 Флаги:[/bold]")
                    for flag in assignment['flags']:
                        console.print(f"  • {flag}")
                
                console.print("\n[bold]💡 Подсказки:[/bold]")
                for i, hint in enumerate(assignment.get('hints', [])[:3], 1):
                    console.print(f"  {i}. {hint}")
                
                console.print("\n[bold]🛠️ Ресурсы:[/bold]")
                for resource in assignment.get('resources', [])[:5]:
                    console.print(f"  • {resource}")
                
                if assignment.get('solution'):
                    console.print("\n[bold]✅ Решение:[/bold]")
                    console.print(assignment['solution'])
                
            except Exception as e:
                console.print(f"[red]Ошибка генерации задания: {e}[/red]")
                import traceback
                traceback.print_exc()
        
        return True, mode, student_level, True
    return True, mode, student_level, True


def handle_commands(
    action: str,
    conn: Any,
    LLM: Any,
    mode: Optional[Any] = None,
    student_level: Optional[Any] = None,
) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    # Если LLM - функция (lazy loading), вызываем для получения объекта
    llm_obj = LLM() if callable(LLM) else LLM
    
    # Parse action parts for subcommands
    parts = action.split() if isinstance(action, str) else []

    if action == "stats":
        stats = get_stats(conn) or {}
        weak_topics = get_weak_topics(conn) if conn else []
        points = stats.get("points", 0) if stats else 0
        quizzes = stats.get("quizzes", 0) if stats else 0
        tasks = stats.get("tasks", 0) if stats else 0
        console.print(f"Очки: {points} | Квизов: {quizzes} | Задач: {tasks}")
        if weak_topics:
            topics_str = ", ".join(
                [f"{t['topic']} ({t['rate']}%)" for t in weak_topics]
            )
            console.print(f"Слабые темы: {topics_str}")
        try:
            from handlers import _response_cache
            cstat = _response_cache.stats()
            if cstat['access_count'] > 0:
                hit_rate = (cstat['hit_count'] / cstat['access_count']) * 100
                console.print(f"Кэш ответов: {cstat['size']}/{cstat['capacity']} (hit rate: {hit_rate:.1f}%)")
            else:
                console.print(f"Кэш ответов: {cstat['size']}/{cstat['capacity']} (hit rate: N/A)")
        except Exception:
            pass
        return True, mode, student_level, True
    elif action == "clear":
        if _ask_confirm("[bold red]Очистить чат?[bold red]"):
            clear_chat_db(conn)
            console.print("[green]✅ Очищено[green]")
        return True, mode, student_level, True
    elif action == "clearcache":
        clear_response_cache()
        console.print("[green]✅ Кэш ответов очищен[/green]")
        return True, mode, student_level, True
    elif parts and parts[0] == "cache":
        if len(parts) > 1 and parts[1] == "stats":
            show_cache_stats()
        else:
            console.print("[cyan]Использование: /cache stats - показать статистику[/cyan]")
        return True, mode, student_level, True
    elif action == "cache":
        if len(parts) > 1 and parts[1] == "stats":
            show_cache_stats()
        else:
            console.print("[cyan]Использование: /cache stats - показать статистику[/cyan]")
        return True, mode, student_level, True
    elif action == "exit":
        console.print("[yellow]👋 Пока![yellow]")
        return False, mode, student_level, True
    elif action in ["smart_test", "read_url"]:
        return handle_quiz_generation(action, conn, llm_obj, mode, student_level)
    elif action in ["quiz_review", "code_review", "review_code"]:
        return handle_code_review(action, conn=conn)
    elif action in [
        "news",
        "cve",
        "security_news",
        "quiz",
        "task",
        "story",
        "practice",
        "help",
        "menu",
        "guide",
        "courses",
        "next",
        "flag",
        "achievements",
        "writeup",
        "check",
        "logs",
        "terminal",
    ]:
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
    elif action == "threats":
        return handle_threats(action)
    elif action == "threat" or action == "threats summary":
        return handle_threat_summary()
    elif action == "groups":
        return handle_groups()
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
    elif action.startswith("add_book"):
        return handle_add_book(action)
    else:
        # Не команда - отправим LLM
        return True, None, None, False


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


# ==================== REAL IMPLEMENTATIONS ====================
# Функции, которые были ранее стабами, но теперь реализованы

def handle_quiz_generation(action: str, conn: Any, LLM: Any, mode=None, student_level=None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
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

def handle_story_mode(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Режим истории (20 эпизодов)"""
    try:
        console.print("[yellow]Режим истории временно недоступен[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_flag_check(flag: str = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Проверка флага /flag <флаг>"""
    try:
        if not flag:
            console.print("[cyan]Использование: /flag <FLAG{...}>[/cyan]")
            return True, None, None, True

        # Простая проверка формата FLAG{...}
        import re
        pattern = r'FLAG\{[^}]+\}'
        if re.fullmatch(pattern, flag.strip()):
            console.print(f"[bold green]✅ Флаг '{flag}' валиден по формату![/bold green]")
            # TODO: Интеграция с базой данных для проверки правильности флага
            console.print("[yellow]Функция проверки корректности флага будет реализована позже.[/yellow]")
        else:
            console.print(f"[bold red]❌ Флаг '{flag}' имеет неверный формат.[/bold red]")
            console.print("[cyan]Ожидается формат: FLAG{...}[/cyan]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_achievements(*args, **kwargs):
    """Управление достижениями: list, earn <id>, help"""
    try:
        action = args[0] if args else "achievements"
        parts = action.split() if isinstance(action, str) else ["achievements"]
        subcmd = parts[1] if len(parts) > 1 else "list"
        
        achievements_file = "data/achievements.json"
        if not os.path.exists(achievements_file):
            console.print("[yellow]Файл достижений не найден[/yellow]")
            return True, None, None, True
        
        with open(achievements_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        achievements = {ach["id"]: ach for ach in data.get("achievements", [])}
        
        # Подкоманда: earn <id> - "получить" достижение (для тестов/демо)
        if subcmd == "earn":
            if len(parts) < 3:
                console.print("[cyan]Использование: /achievements earn <id>[/cyan]")
                console.print("Пример: /achievements earn first_blood")
                return True, None, None, True
            
            ach_id = parts[2]
            if ach_id not in achievements:
                console.print(f"[yellow]Достижение '{ach_id}' не найдено[/yellow]")
                console.print("[cyan]Доступные ID: " + ", ".join(sorted(achievements.keys())) + "[/cyan]")
                return True, None, None, True
            
            # В реальной системе здесь будет логика проверки условий
            # Сейчас просто показываем, что достижение "получено"
            ach = achievements[ach_id]
            console.print(f"[bold green]✅ Достижение получено![/bold green]")
            console.print(f"{ach.get('icon', '🏆')} **{ach.get('name')}** (+{ach.get('xp', 0)} XP)")
            console.print(f"[dim]{ach.get('description', '')}[/dim]")
            console.print("\n[cyan]В будущем это будет интегрировано с системой прогресса.[/cyan]")
            return True, None, None, True
        
        # Подкоманда: help
        elif subcmd == "help":
            console.print("[bold cyan]🏆 Достижения — помощь[/bold cyan]\n")
            console.print("Команды:")
            console.print("  /achievements — показать список всех достижений")
            console.print("  /achievements earn <id> — получить достижение (тестовый режим)")
            console.print("  /achievements help — эта справка")
            return True, None, None, True
        
        # По умолчанию: list
        console.print("[bold cyan]🏆 Все достижения[/bold cyan]\n")
        for ach_id, ach in achievements.items():
            name = ach.get("name", "Без названия")
            description = ach.get("description", "")
            icon = ach.get("icon", "🏆")
            xp = ach.get("xp", 0)
            
            console.print(f"{icon} **{name}** (+{xp} XP)")
            if description:
                console.print(f"   {description}")
            console.print(f"   [dim]ID: {ach_id}[/dim]\n")
            
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback
        traceback.print_exc()
    return True, None, None, True

def handle_threats(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Показать досье на APT-группу"""
    try:
        parts = action.split(maxsplit=1)
        if len(parts) > 1:
            group_name = parts[1].strip().lower()
            threat_file = os.path.join("threats", f"{group_name}.json")
            
            if not os.path.exists(threat_file):
                console.print(f"[yellow]Досье '{group_name}' не найдено[/yellow]")
                # Список доступных
                files = [f[:-5] for f in os.listdir("threats") if f.endswith('.json')] if os.path.exists("threats") else []
                if files:
                    console.print("[cyan]Доступные: " + ", ".join(sorted(files)) + "[/cyan]")
                return True, None, None, True
            
            with open(threat_file, 'r', encoding='utf-8') as f:
                threat = json.load(f)
            
            console.print(f"\n[bold red]📁 Досье: {threat.get('name', 'Unknown')}[/bold red]")
            console.print(f"Алиасы: {', '.join(threat.get('aliases', []))}")
            console.print(f"Страна: {threat.get('country', 'N/A')}")
            console.print(f"Активность: {threat.get('first_seen', 'N/A')}")
            console.print(f"Цели: {', '.join(threat.get('targets', []))}")
            console.print(f"\n[bold]Тактики MITRE:[/bold]")
            for t in threat.get('tactics', []):
                console.print(f"  • {t}")
            console.print(f"\n[bold]Инструменты:[/bold]")
            for tool in threat.get('tools', []):
                console.print(f"  • {tool}")
            console.print(f"\n[bold]Техники:[/bold]")
            for tech in threat.get('techniques', []):
                console.print(f"  • {tech}")
            console.print(f"\n[bold]Недавняя активность:[/bold] {threat.get('recent_activity', 'N/A')}")
            if threat.get('references'):
                console.print(f"[bold]Ссылки:[/bold] {threat['references'][0]}")
            console.print()
            return True, None, None, True
        else:
            console.print("[cyan]Использование: /threats <имя_группы>[/cyan]")
            if os.path.exists("threats"):
                files = [f[:-5] for f in os.listdir("threats") if f.endswith('.json')]
                console.print("[bold]Доступные группы:[/bold]")
                for f in sorted(files):
                    console.print(f"  • {f}")
            return True, None, None, True
            
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

def handle_groups(*args, **kwargs):
    """Группировка APT-групп по странам/тактикам"""
    try:
        if not os.path.exists("threats"):
            console.print("[yellow]Папka threats/ ne najdena[/yellow]")
            return True, None, None, True
        
        # Загружаем все досье
        threats = []
        for f in os.listdir("threats"):
            if f.endswith('.json'):
                with open(os.path.join("threats", f), 'r', encoding='utf-8') as fp:
                    threats.append(json.load(fp))
        
        if not threats:
            console.print("[yellow]Net dannych ob ugrozah[/yellow]")
            return True, None, None, True
        
        console.print("[bold cyan]🌍 APT-gruppy po stranam[/bold cyan]\n")
        
        # Группируем по стране
        by_country = {}
        for t in threats:
            country = t.get('country', 'Unknown')
            by_country.setdefault(country, []).append(t.get('name', 'Unknown'))
        
        for country in sorted(by_country.keys()):
            console.print(f"[bold]{country}[/bold]:")
            for name in sorted(by_country[country]):
                console.print(f"  • {name}")
            console.print()
        
        console.print("[bold]📊 Statistika:[/bold]")
        console.print(f"Vsego grupp: {len(threats)}")
        console.print(f"Stran: {len(by_country)}")
        
        # Populyarnye taktiki
        tactic_counts = {}
        for t in threats:
            for tactic in t.get('tactics', []):
                tactic_counts[tactic] = tactic_counts.get(tactic, 0) + 1
        
        if tactic_counts:
            console.print("\n[bold]TOP-5 tactics:[/bold]")
            sorted_tactics = sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for tactic, count in sorted_tactics:
                console.print(f"  • {tactic}: {count} grupp")
        
        console.print()
        
    except Exception as e:
        console.print(f"[red]Oshibka: {e}[/red]")
    return True, None, None, True

def handle_threat_summary(*args, **kwargs):
    """Kratkaya svodka po vseug ugrozam"""
    try:
        if not os.path.exists("threats"):
            console.print("[yellow]Papka threats/ ne najdena[/yellow]")
            return True, None, None, True
        
        # Zagruzhaem vse dos'e
        threats = []
        for f in os.listdir("threats"):
            if f.endswith('.json'):
                with open(os.path.join("threats", f), 'r', encoding='utf-8') as fp:
                    threats.append(json.load(fp))
        
        if not threats:
            console.print("[yellow]Net dannih ob ugrozah[/yellow]")
            return True, None, None, True
        
        console.print("[bold red]📊 Svodka po threat intelligence[/bold red]\n")
        
        # Statistika po stranam
        by_country = {}
        for t in threats:
            country = t.get('country', 'Unknown')
            by_country[country] = by_country.get(country, 0) + 1
        
        console.print("[bold]🌍 Raspredelenie po stranam:[/bold]")
        for country in sorted(by_country.keys()):
            console.print(f"  {country}: {by_country[country]} grupp")
        
        console.print()
        
        # Top taktiki
        tactic_counts = {}
        for t in threats:
            for tactic in t.get('tactics', []):
                tactic_counts[tactic] = tactic_counts.get(tactic, 0) + 1
        
        console.print("[bold]🎯 Top-10 taktik MITRE ATT&CK:[/bold]")
        for tactic, count in sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {tactic}: {count}")
        
        console.print()
        
        # Instrumenty
        tool_counts = {}
        for t in threats:
            for tool in t.get('tools', []):
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        console.print("[bold]🔧 Top-10 instrumentov:[/bold]")
        for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {tool}: {count}")
        
        console.print()
        
        # Celovye sektory
        target_counts = {}
        for t in threats:
            for target in t.get('targets', []):
                target_counts[target] = target_counts.get(target, 0) + 1
        
        console.print("[bold]🎯 Celovye sektory:[/bold]")
        for target, count in sorted(target_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {target}: {count}")
        
        console.print()
        
        # Issledovanie
        console.print(f"[bold]📈 Vsego doss'e: {len(threats)}[/bold]")
        console.print(f"[bold]🆕 Pervie zametki:[/bold]")
        for t in threats:
            first = t.get('first_seen', 'N/A')
            name = t.get('name', 'Unknown')
            console.print(f"  {name}: {first}")
        
        console.print("\n[cyan]Ispol'zujte '/threats <name>' dla podrobnostej[/cyan]")
        console.print()
        
    except Exception as e:
        console.print(f"[red]Oshibka: {e}[/red]")
    return True, None, None, True


def handle_achievements(*args, **kwargs):
    """Управление достижениями: list, earn <id>, help"""
    try:
        action = args[0] if args else "achievements"
        parts = action.split() if isinstance(action, str) else ["achievements"]
        subcmd = parts[1] if len(parts) > 1 else "list"
        
        achievements_file = "data/achievements.json"
        if not os.path.exists(achievements_file):
            console.print("[yellow]Файл достижений не найден[/yellow]")
            return True, None, None, True
        
        with open(achievements_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        achievements = {ach["id"]: ach for ach in data.get("achievements", [])}
        
        # Подкоманда: earn <id> - "получить" достижение (для тестов/демо)
        if subcmd == "earn":
            if len(parts) < 3:
                console.print("[cyan]Использование: /achievements earn <id>[/cyan]")
                console.print("Пример: /achievements earn first_blood")
                return True, None, None, True
            
            ach_id = parts[2]
            if ach_id not in achievements:
                console.print(f"[yellow]Достижение '{ach_id}' не найдено[/yellow]")
                console.print("[cyan]Доступные ID: " + ", ".join(sorted(achievements.keys())) + "[/cyan]")
                return True, None, None, True
            
            # В реальной системе здесь будет логика проверки условий
            # Сейчас просто показываем, что достижение "получено"
            ach = achievements[ach_id]
            console.print(f"[bold green]✅ Достижение получено![/bold green]")
            console.print(f"{ach.get('icon', '🏆')} **{ach.get('name')}** (+{ach.get('xp', 0)} XP)")
            console.print(f"[dim]{ach.get('description', '')}[/dim]")
            console.print("\n[cyan]В будущем это будет интегрировано с системой прогресса.[/cyan]")
            return True, None, None, True
        
        # Подкоманда: help
        elif subcmd == "help":
            console.print("[bold cyan]🏆 Достижения — помощь[/bold cyan]\n")
            console.print("Команды:")
            console.print("  /achievements — показать список всех достижений")
            console.print("  /achievements earn <id> — получить достижение (тестовый режим)")
            console.print("  /achievements help — эта справка")
            return True, None, None, True
        
        # По умолчанию: list
        console.print("[bold cyan]🏆 Все достижения[/bold cyan]\n")
        for ach_id, ach in achievements.items():
            name = ach.get("name", "Без названия")
            description = ach.get("description", "")
            icon = ach.get("icon", "🏆")
            xp = ach.get("xp", 0)
            
            console.print(f"{icon} **{name}** (+{xp} XP)")
            if description:
                console.print(f"   {description}")
            console.print(f"   [dim]ID: {ach_id}[/dim]\n")
            
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback
        traceback.print_exc()
    return True, None, None, True

def handle_threats(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Показать досье на APT-группу"""
    try:
        parts = action.split(maxsplit=1)
        if len(parts) > 1:
            group_name = parts[1].strip().lower()
            threat_file = os.path.join("threats", f"{group_name}.json")
            
            if not os.path.exists(threat_file):
                console.print(f"[yellow]Досье '{group_name}' не найдено[/yellow]")
                # Список доступных
                files = [f[:-5] for f in os.listdir("threats") if f.endswith('.json')] if os.path.exists("threats") else []
                if files:
                    console.print("[cyan]Доступные: " + ", ".join(sorted(files)) + "[/cyan]")
                return True, None, None, True
            
            with open(threat_file, 'r', encoding='utf-8') as f:
                threat = json.load(f)
            
            console.print(f"\n[bold red]📁 Досье: {threat.get('name', 'Unknown')}[/bold red]")
            console.print(f"Алиасы: {', '.join(threat.get('aliases', []))}")
            console.print(f"Страна: {threat.get('country', 'N/A')}")
            console.print(f"Активность: {threat.get('first_seen', 'N/A')}")
            console.print(f"Цели: {', '.join(threat.get('targets', []))}")
            console.print(f"\n[bold]Тактики MITRE:[/bold]")
            for t in threat.get('tactics', []):
                console.print(f"  • {t}")
            console.print(f"\n[bold]Инструменты:[/bold]")
            for tool in threat.get('tools', []):
                console.print(f"  • {tool}")
            console.print(f"\n[bold]Техники:[/bold]")
            for tech in threat.get('techniques', []):
                console.print(f"  • {tech}")
            console.print(f"\n[bold]Недавняя активность:[/bold] {threat.get('recent_activity', 'N/A')}")
            if threat.get('references'):
                console.print(f"[bold]Ссылки:[/bold] {threat['references'][0]}")
            console.print()
            return True, None, None, True
        else:
            console.print("[cyan]Использование: /threats <имя_группы>[/cyan]")
            if os.path.exists("threats"):
                files = [f[:-5] for f in os.listdir("threats") if f.endswith('.json')]
                console.print("[bold]Доступные группы:[/bold]")
                for f in sorted(files):
                    console.print(f"  • {f}")
            return True, None, None, True
            
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

def handle_groups(*args, **kwargs):
    """Группировка APT-групп по странам/тактикам"""
    try:
        if not os.path.exists("threats"):
            console.print("[yellow]Папka threats/ ne najdena[/yellow]")
            return True, None, None, True
        
        # Загружаем все досье
        threats = []
        for f in os.listdir("threats"):
            if f.endswith('.json'):
                with open(os.path.join("threats", f), 'r', encoding='utf-8') as fp:
                    threats.append(json.load(fp))
        
        if not threats:
            console.print("[yellow]Net dannych ob ugrozah[/yellow]")
            return True, None, None, True
        
        console.print("[bold cyan]🌍 APT-gruppy po stranam[/bold cyan]\n")
        
        # Группируем по стране
        by_country = {}
        for t in threats:
            country = t.get('country', 'Unknown')
            by_country.setdefault(country, []).append(t.get('name', 'Unknown'))
        
        for country in sorted(by_country.keys()):
            console.print(f"[bold]{country}[/bold]:")
            for name in sorted(by_country[country]):
                console.print(f"  • {name}")
            console.print()
        
        console.print("[bold]📊 Statistika:[/bold]")
        console.print(f"Vsego grupp: {len(threats)}")
        console.print(f"Stran: {len(by_country)}")
        
        # Populyarnye taktiki
        tactic_counts = {}
        for t in threats:
            for tactic in t.get('tactics', []):
                tactic_counts[tactic] = tactic_counts.get(tactic, 0) + 1
        
        if tactic_counts:
            console.print("\n[bold]TOP-5 tactics:[/bold]")
            sorted_tactics = sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for tactic, count in sorted_tactics:
                console.print(f"  • {tactic}: {count} grupp")
        
        console.print()
        
    except Exception as e:
        console.print(f"[red]Oshibka: {e}[/red]")
    return True, None, None, True

def handle_threat_summary(*args, **kwargs):
    """Kratkaya svodka po vseug ugrozam"""
    try:
        if not os.path.exists("threats"):
            console.print("[yellow]Papka threats/ ne najdena[/yellow]")
            return True, None, None, True
        
        # Zagruzhaem vse dos'e
        threats = []
        for f in os.listdir("threats"):
            if f.endswith('.json'):
                with open(os.path.join("threats", f), 'r', encoding='utf-8') as fp:
                    threats.append(json.load(fp))
        
        if not threats:
            console.print("[yellow]Net dannih ob ugrozah[/yellow]")
            return True, None, None, True
        
        console.print("[bold red]📊 Svodka po threat intelligence[/bold red]\n")
        
        # Statistika po stranam
        by_country = {}
        for t in threats:
            country = t.get('country', 'Unknown')
            by_country[country] = by_country.get(country, 0) + 1
        
        console.print("[bold]🌍 Raspredelenie po stranam:[/bold]")
        for country in sorted(by_country.keys()):
            console.print(f"  {country}: {by_country[country]} grupp")
        
        console.print()
        
        # Top taktiki
        tactic_counts = {}
        for t in threats:
            for tactic in t.get('tactics', []):
                tactic_counts[tactic] = tactic_counts.get(tactic, 0) + 1
        
        console.print("[bold]🎯 Top-10 taktik MITRE ATT&CK:[/bold]")
        for tactic, count in sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {tactic}: {count}")
        
        console.print()
        
        # Instrumenty
        tool_counts = {}
        for t in threats:
            for tool in t.get('tools', []):
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        console.print("[bold]🔧 Top-10 instrumentov:[/bold]")
        for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {tool}: {count}")
        
        console.print()
        
        # Celovye sektory
        target_counts = {}
        for t in threats:
            for target in t.get('targets', []):
                target_counts[target] = target_counts.get(target, 0) + 1
        
        console.print("[bold]🎯 Celovye sektory:[/bold]")
        for target, count in sorted(target_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {target}: {count}")
        
        console.print()
        
        # Issledovanie
        console.print(f"[bold]📈 Vsego doss'e: {len(threats)}[/bold]")
        console.print(f"[bold]🆕 Pervie zametki:[/bold]")
        for t in threats:
            first = t.get('first_seen', 'N/A')
            name = t.get('name', 'Unknown')
            console.print(f"  {name}: {first}")
        
        console.print("\n[cyan]Ispol'zujte '/threats <name>' dla podrobnostej[/cyan]")
        console.print()
        
    except Exception as e:
        console.print(f"[red]Oshibka: {e}[/red]")
    return True, None, None, True
    """Показать досье на APT-группу"""
    try:
        parts = action.split(maxsplit=1)
        if len(parts) > 1:
            group_name = parts[1].strip().lower()
            threat_file = os.path.join("threats", f"{group_name}.json")
            
            if not os.path.exists(threat_file):
                console.print(f"[yellow]Досье '{group_name}' не найдено[/yellow]")
                # Список доступных
                files = [f[:-5] for f in os.listdir("threats") if f.endswith('.json')] if os.path.exists("threats") else []
                if files:
                    console.print("[cyan]Доступные: " + ", ".join(sorted(files)) + "[/cyan]")
                return True, None, None, True
            
            with open(threat_file, 'r', encoding='utf-8') as f:
                threat = json.load(f)
            
            console.print(f"\n[bold red]📁 Досье: {threat.get('name', 'Unknown')}[/bold red]")
            console.print(f"Алиасы: {', '.join(threat.get('aliases', []))}")
            console.print(f"Страна: {threat.get('country', 'N/A')}")
            console.print(f"Активность: {threat.get('first_seen', 'N/A')}")
            console.print(f"Цели: {', '.join(threat.get('targets', []))}")
            console.print(f"\n[bold]Тактики MITRE:[/bold]")
            for t in threat.get('tactics', []):
                console.print(f"  • {t}")
            console.print(f"\n[bold]Инструменты:[/bold]")
            for tool in threat.get('tools', []):
                console.print(f"  • {tool}")
            console.print(f"\n[bold]Техники:[/bold]")
            for tech in threat.get('techniques', []):
                console.print(f"  • {tech}")
            console.print(f"\n[bold]Недавняя активность:[/bold] {threat.get('recent_activity', 'N/A')}")
            if threat.get('references'):
                console.print(f"[bold]Ссылки:[/bold] {threat['references'][0]}")
            console.print()
            return True, None, None, True
        else:
            console.print("[cyan]Использование: /threats <имя_группы>[/cyan]")
            if os.path.exists("threats"):
                files = [f[:-5] for f in os.listdir("threats") if f.endswith('.json')]
                console.print("[bold]Доступные группы:[/bold]")
                for f in sorted(files):
                    console.print(f"  • {f}")
            return True, None, None, True
            
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

def handle_practice(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Обработка команд /practice и /lab"""
    try:
        from practice import list_labs, start_lab, stop_lab, get_all_running_labs, HTB_MACHINES, get_htb_recommendation

        parts = action.split()

        if action == "practice" or action == "lab":
            # Показать список доступных лаб
            console.print(list_labs())
            return True, None, None, True

        elif parts[0] in ["lab", "practice"] and len(parts) >= 3 and parts[1] == "start":
            lab_name = parts[2]
            result = start_lab(lab_name)
            console.print(result)
            return True, None, None, True

        elif parts[0] in ["lab", "practice"] and len(parts) >= 3 and parts[1] == "stop":
            lab_name = parts[2]
            result = stop_lab(lab_name)
            console.print(result)
            return True, None, None, True

        elif parts[0] in ["lab", "practice"] and len(parts) >= 2 and parts[1] == "status":
            running = get_all_running_labs()
            if running:
                console.print("[bold cyan]🟢 Запущенные лаборатории:[/bold cyan]\n")
                for key, info in running.items():
                    console.print(f"  • {info['name']}: {info['status']}")
            else:
                console.print("[yellow]Нет запущенных лабораторий[/yellow]")
            return True, None, None, True

        elif action == "htb":
            # Рекомендации HTB машин
            console.print(get_htb_recommendation())
            return True, None, None, True

        else:
            console.print("[cyan]Использование:[/cyan]")
            console.print("  /lab          - показать список всех лаб")
            console.print("  /lab start <name> - запустить лабораторию")
            console.print("  /lab stop <name>  - остановить лабораторию")
            console.print("  /lab status      - статус запущенных")
            console.print("  /htb             - рекомендации HTB машин")
            return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback
        traceback.print_exc()
        return True, None, None, True


def handle_container_check(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Проверка статуса контейнеров"""
    try:
        from practice import get_all_running_labs

        running = get_all_running_labs()
        if running:
            console.print("[bold cyan]🐳 Статус контейнеров:[/bold cyan]\n")
            for key, info in running.items():
                console.print(f"  🟢 {info['name']}: {info['status']}")
        else:
            console.print("[yellow]Нет запущенных контейнеров[/yellow]")

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_terminal_log(action: str = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Показать лог терминала"""
    try:
        from terminal_log import get_terminal_log, log_command

        if action and action.startswith("log "):
            # Записать команду в лог: /log <команда>
            cmd = action[4:].strip()
            log_command(cmd, is_input=False)
            console.print(f"[green]✅ Команда записана в лог[/green]")
            return True, None, None, True

        # Показать последние записи
        log_text = get_terminal_log(last_n=20)
        console.print(Panel(log_text, title="📟 Терминал (последние 20 строк)", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_history(*args, **kwargs):
    console.print("[yellow]История временно недоступна[/yellow]")
    return True, None, None, True

def handle_course(*args, **kwargs):
    console.print("[yellow]Курс временно недоступен[/yellow]")
    return True, None, None, True
# =========================================================


# ===== MISSING HANDLERS =====
def handle_flag_check(flag: str = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Проверка флага"""
    if not flag:
        console.print("[cyan]Использование: /flag <FLAG{...}>[/cyan]")
        return True, None, None, True
    import re
    pattern = r'FLAG\{[^}]+\}'
    if not re.fullmatch(pattern, flag.strip()):
        console.print(f"[bold red]❌ Флаг '{flag}' неверного формата.[/bold red]")
        return True, None, None, True
    try:
        flags_file = "data/flags.json"
        if not os.path.exists(flags_file):
            console.print("[yellow]База флагов не найдена. Создайте data/flags.json[/yellow]")
            return True, None, None, True
        with open(flags_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for fdata in data.get("flags", []):
            if fdata["flag"] == flag:
                pts = fdata.get('points', 10)
                console.print(f"[bold green]✅ Флаг верный! +{pts} очков[/bold green]")
                from memory import init_db, update_stats
                conn2 = init_db()
                update_stats(conn2, pts)
                return True, None, None, True
        console.print(f"[bold red]❌ Флаг '{flag}' неверный.[/bold red]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_practice(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        from practice import list_labs, start_lab, stop_lab, get_all_running_labs
        parts = action.split()
        if action == "practice" or action == "lab":
            console.print(list_labs())
        elif len(parts) >= 3 and parts[1] == "start":
            lab_name = parts[2]
            console.print(start_lab(lab_name))
        elif len(parts) >= 3 and parts[1] == "stop":
            lab_name = parts[2]
            console.print(stop_lab(lab_name))
        elif parts[0] in ["lab", "practice"] and len(parts) >= 2 and parts[1] == "status":
            running = get_all_running_labs()
            if running:
                console.print("[bold cyan]🟢 Запущенные лаборатории:[/bold cyan]\n")
                for key, info in running.items():
                    console.print(f"  • {info['name']}: {info['status']}")
            else:
                console.print("[yellow]Нет запущенных лабораторий[/yellow]")
        else:
            console.print("[cyan]Использование: /lab [start|stop|status] <name>[/cyan]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

def handle_container_check(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        from practice import get_all_running_labs
        running = get_all_running_labs()
        if running:
            console.print("[bold cyan]🐳 Статус контейнеров:[/bold cyan]\n")
            for key, info in running.items():
                console.print(f"  🟢 {info['name']}: {info['status']}")
        else:
            console.print("[yellow]Нет запущенных контейнеров[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_terminal_log(action: str = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
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
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_course(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    console.print("[yellow]Курсы временно недоступны[/yellow]")
    return True, None, None, True

def handle_quiz_action() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        from knowledge import get_current_vectordb
        vectordb = get_current_vectordb()
        if GENERATORS_AVAILABLE:
            from generators import generate_quiz
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
            from generators import generate_task
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

def handle_quiz_generation(action: str, conn, llm_obj, mode=None, student_level=None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    # For /smart_test and /read_url - just reuse handle_quiz_action
    return handle_quiz_action()

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

def __main__run_demo():
    conn = None
    LLM = None
    handle_commands("stats", conn, LLM)


if __name__ == "__main__":
    __main__run_demo()
