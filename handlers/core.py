# handlers/core.py
import json
import os
import logging
from collections import OrderedDict, deque
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from state import get_state

# ----------------------------------------------------------------------
# Импорты модулей handlers (все функции уже в их файлах)
# ----------------------------------------------------------------------
from .practice import handle_practice, handle_container_check
from .quiz import handle_quiz_action, handle_task_action, handle_quiz_generation, handle_code_review
from .flags import handle_flag_check
from .achievements import handle_achievements
from .threats import handle_threats, handle_groups, handle_threat_summary
from .news import handle_security_news, get_last_news
from .misc import (
    _ask_confirm,
    clear_chat_db,
    extract_json_block,
    check_open_answer,
    handle_story_mode,
    handle_course,
    handle_terminal_log,
    handle_history,
    handle_version,
    handle_writeup,
    handle_add_book,
)
from ui import Mode, show_help, show_menu

console = Console()
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# RESPONSE CACHE
# ----------------------------------------------------------------------
class ResponseCache:
    def __init__(self, capacity: int = 100):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.access_order = deque(maxlen=capacity)
        self.hit_count = 0
        self.access_count = 0
        self._load()

    def _load(self):
        try:
            cache_file = "./memory/response_cache.json"
            if os.path.exists(cache_file):
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.cache = OrderedDict(data.get("cache", {}))
                self.access_order = deque(data.get("access_order", []), maxlen=self.capacity)
                self.hit_count = data.get("hit_count", 0)
                self.access_count = data.get("access_count", 0)
                if len(self.cache) > self.capacity:
                    for key in list(self.access_order)[:-self.capacity]:
                        self.cache.pop(key, None)
                    self.access_order = deque(list(self.access_order)[-self.capacity:], maxlen=self.capacity)
        except Exception as e:
            logger.error(f"[ResponseCache] load error: {e}")

    def _save(self):
        try:
            os.makedirs("./memory", exist_ok=True)
            data = {
                "cache": dict(self.cache),
                "access_order": list(self.access_order),
                "hit_count": self.hit_count,
                "access_count": self.access_count,
            }
            with open("./memory/response_cache.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[ResponseCache] save error: {e}")

    def get(self, key: str) -> Optional[Any]:
        self.access_count += 1
        if key not in self.cache:
            return None
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
            "access_count": self.access_count,
        }

_response_cache = ResponseCache()

def clear_response_cache():
    _response_cache.clear()
    try:
        _response_cache._save()
    except Exception:
        pass

def show_cache_stats():
    stats = _response_cache.stats()
    console.print(f"[bold cyan]📊 Статистика кэша ответов:[/bold cyan]")
    console.print(f"  Размер: {stats['size']} / {stats['capacity']}")
    if stats["access_count"] > 0:
        hit_rate = (stats["hit_count"] / stats["access_count"]) * 100
        console.print(f"  Hit rate: {stats['hit_count']}/{stats['access_count']} ({hit_rate:.1f}%)")
    console.print(f"  Команды: /clearcache - очистить, /cache stats - показать")

# ----------------------------------------------------------------------
# ПОМОГОТЕЛЬНЫЕ ФУНКЦИИ
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# COMMAND DISPATCHERS
# ----------------------------------------------------------------------
def handle_commands(
    action: str,
    conn: Any,
    llm: Any,
    mode: Optional[Any] = None,
    student_level: Optional[Any] = None,
) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Главный диспетчер, вызываемый из main.py."""
    extended = action in {
        "news", "cve", "security_news", "flag", "achievements", "quiz",
        "task", "practice", "lab", "htb", "next", "course", "genassignment",
        "writeup", "add_book", "log", "terminal", "history", "threats",
        "threat summary", "groups", "review", "code_review", "smart_test",
        "read_url", "story", "episode", "quest", "check", "logs", "help", "menu", "guide",
    }
    if extended:
        return handle_extended_commands(action, llm, conn)
    return True, mode, student_level, False

def handle_extended_commands(action: str, llm: Any, conn: Any) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    if action in ("news", "cve", "security_news"):
        return handle_security_news(action, llm)
    elif action in ("story", "episode", "quest"):
        return handle_story_mode(action)
    elif action.startswith("flag"):
        flag = action.split(" ", 1)[1] if " " in action else None
        return handle_flag_check(flag)
    elif action in ("achievements", "achievement"):
        return handle_achievements()
    elif action == "threats":
        return handle_threats(action)
    elif action in ("threat", "threats summary"):
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
        show_help()
        return True, None, None, True
    elif action == "menu":
        show_menu()
        return True, None, None, True
    elif action == "guide":
        try:
            with open("docs/ГАЙД_VM.md", "r", encoding="utf-8") as f:
                guide = f.read()
            console.print(Panel(guide[:1000], title="ГАЙД ПО LAB", border_style="cyan"))
        except Exception:
            console.print("[yellow]Гайд не найден[/yellow]")
        return True, None, None, True
    elif action in ("check", "logs"):
        return handle_container_check(action)
    elif action in ("terminal", "term"):
        return handle_terminal_log()
    elif action == "history":
        return handle_history(conn)
    elif action == "version":
        return handle_version()
    elif action.startswith("log "):
        return handle_terminal_log(action[4:])
    elif action == "writeup":
        return handle_writeup()
    elif action.startswith("add_book"):
        return handle_add_book(action)
    else:
        return True, None, None, False

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
        console.print("[yellow]👋 Пока![/yellow]")
        return False, mode, student_level, True
    if action == "clear":
        if _ask_confirm("[bold red]Очистить чат?[/bold red]"):
            clear_chat_db(conn)
            console.print("[green]✅ Очищено[/green]")
        return True, mode, student_level, True
    if action == "clearcache":
        clear_response_cache()
        console.print("[green]✅ Кэш ответов очищен[/green]")
        return True, mode, student_level, True
    if action in ["kb_status", "check_kb"]:
        from knowledge import get_knowledge_status
        status = get_knowledge_status()
        if action == "kb_status":
            text = f"""
                [bold]📂 Файлов на диске:[/bold] {status.get('files_on_disk', '?')}
                [bold]💾 Файлов в базе:[/bold] {status.get('files_in_db', '?')}
                [bold]🧠 Всего чанков (фрагментов):[/bold] {status.get('total_chunks', '?')}
                [bold]Список загруженных файлов:[/bold]
            """
            files = status.get("list", [])
            if files:
                files_to_show = files[-15:]
                text += "\n".join([f"• {f}" for f in files_to_show])
                if len(files) > 15:
                    text += f"\n... и еще {len(files) - 15} файлов."
            else:
                text += "[yellow]База пуста[/yellow]"
            console.print(Panel(text, title="📚 Состояние Базы Знаний", border_style="cyan"))
        elif action == "check_kb":
            console.print(Panel(str(status), title="🧪 АУДИТ ЗНАНИЙ", border_style="cyan"))
        return True, mode, student_level, True
    if action == "genassignment":
        console.print("[yellow]Модуль генератора заданий временно отключён для рефакторинга[/yellow]")
        return True, mode, student_level, True
    if action == "ctf":
        return True, Mode.CTF, student_level, True
    if action == "teacher":
        return True, Mode.TEACHER, student_level, True
    if action == "expert":
        return True, Mode.EXPERT, student_level, True
    if action == "review":
        return True, Mode.CODE_REVIEW, student_level, True
    if action.startswith("lab") or action == "htb":
        return handle_practice(action)
    if action in {"smart_test", "read_url"}:
        return handle_quiz_generation(action, None, None, mode, student_level)
    return True, mode, student_level, False