# handlers/core.py
import json
import logging
import os
from collections import OrderedDict, deque
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel

from state import get_state
from ui import Mode, show_help, show_help_detail, show_menu

from .achievements import handle_achievements
from .flags import handle_flag_check
from .misc import (
    _ask_confirm,
    check_open_answer,
    clear_chat_db,
    extract_json_block,
    handle_adaptive,
    handle_add_book,
    handle_course,
    handle_history,
    handle_model,
    handle_provider,
    handle_repeat,
    handle_risk,
    handle_set_api_key,
    handle_story_mode,
    handle_terminal_log,
    handle_version,
    handle_writeup,
)
from .news import get_last_news, handle_security_news

# ----------------------------------------------------------------------
# Импорты модулей handlers
# ----------------------------------------------------------------------
from .practice import handle_container_check, handle_practice
from .quiz import (
    handle_code_review,
    handle_quiz_action,
    handle_quiz_generation,
    handle_task_action,
)
from .sandbox import handle_sandbox
from .social import handle_social
from .summary import handle_summary
from .threats import handle_groups, handle_threat_summary, handle_threats
from .writeup_auto import handle_auto_writeup

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
                self.access_order = deque(
                    data.get("access_order", []), maxlen=self.capacity
                )
                self.hit_count = data.get("hit_count", 0)
                self.access_count = data.get("access_count", 0)
                if len(self.cache) > self.capacity:
                    for key in list(self.access_order)[: -self.capacity]:
                        self.cache.pop(key, None)
                    self.access_order = deque(
                        list(self.access_order)[-self.capacity :], maxlen=self.capacity
                    )
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

    def get(self, key: str) -> Any | None:
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

    def stats(self) -> dict:
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
        console.print(
            f"  Hit rate: {stats['hit_count']}/{stats['access_count']} ({hit_rate:.1f}%)"
        )
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


def extract_json_block(text: str) -> str | None:
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
    key_points: list[str] | None = None,
) -> dict[str, Any]:
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


def handle_stats(conn):
    """Показать статистику пользователя."""
    from memory import get_stats

    stats = get_stats(conn)
    console.print(f"[bold cyan]📈 Статистика:[/bold cyan]")
    console.print(f"  Сообщений: {stats.get('messages', 0)}")
    console.print(f"  Очков: {stats.get('points', 0)}")
    console.print(f"  Флагов: {stats.get('flags', 0)}")
    console.print(f"  Лабораторий: {stats.get('labs', 0)}")
    console.print(f"  Курсов: {stats.get('courses', 0)}")
    console.print(f"  Кэш ответов: {_response_cache.stats()['size']} записей")
    return True, None, None, True


# ----------------------------------------------------------------------
# COMMAND DISPATCHERS
# ----------------------------------------------------------------------
def handle_commands(
    action: str,
    conn: Any,
    llm: Any,
) -> tuple[bool, Any | None, Any | None, bool]:
    """Главный диспетчер. Все команды (включая numeric menu) передаются в handle_extended_commands."""
    return handle_extended_commands(action, llm, conn)


def handle_extended_commands(
    action: str, llm: Any, conn: Any
) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка всех команд. Если команда неизвестна — блокируем передачу в LLM."""
    state = get_state()

    # ----- Simple commands -----
    if action in ("help", "menu"):
        show_help() if action == "help" else show_menu()
        return True, None, None, True

    if action == "guide":
        try:
            with open("docs/ГАЙД_VM.md", "r", encoding="utf-8") as f:
                guide = f.read()
            console.print(Panel(guide[:1000], title="ГАЙД ПО LAB", border_style="cyan"))
        except Exception:
            console.print("[yellow]Гайд не найден[/yellow]")
        return True, None, None, True

    if action == "version":
        handle_version()
        return True, None, None, True

    if action == "exit":
        console.print("[yellow]👋 Пока![/yellow]")
        return False, None, None, True

    if action == "clear":
        if _ask_confirm("[bold red]Очистить чат?[/bold red]"):
            clear_chat_db(conn)
            console.print("[green]✅ Очищено[/green]")
        return True, None, None, True

    if action == "clearcache":
        clear_response_cache()
        console.print("[green]✅ Кэш ответов очищен[/green]")
        return True, None, None, True

    if action == "kb_status":
        from knowledge import get_knowledge_status

        status = get_knowledge_status()
        text = f"""[bold]📂 Файлов на диске:[/bold] {status.get("files_on_disk", "?")}
[bold]💾 Файлов в базе:[/bold] {status.get("files_in_db", "?")}
[bold]🧠 Всего чанков:[/bold] {status.get("total_chunks", "?")}
[bold]Список файлов:[/bold]"""
        files = status.get("list", [])
        if files:
            files_to_show = files[-15:]
            text += "\n" + "\n".join([f"• {f}" for f in files_to_show])
            if len(files) > 15:
                text += f"\n... ещё {len(files) - 15}"
        else:
            text += "\n[yellow]База пуста[/yellow]"
        console.print(Panel(text, title="📚 База знаний", border_style="cyan"))
        return True, None, None, True

    if action == "check_kb":
        from knowledge import get_knowledge_status

        status = get_knowledge_status()
        console.print(Panel(str(status), title="🧪 Аудит базы", border_style="cyan"))
        return True, None, None, True

    if action == "genassignment":
        console.print("[yellow]Генератор заданий временно отключён[/yellow]")
        return True, None, None, True

    if action == "cache stats":
        show_cache_stats()
        return True, None, None, True

    if action == "stats":
        handle_stats(conn)
        return True, None, None, True

    # ----- Mode switches -----
    if action == "teacher":
        state.set_persona("teacher")
        return True, Mode.TEACHER, None, True
    if action == "expert":
        state.set_persona("expert")
        return True, Mode.EXPERT, None, True
    if action == "ctf":
        state.set_persona("ctf")
        return True, Mode.CTF, None, True
    if action == "review":
        state.set_persona("review")
        return True, Mode.CODE_REVIEW, None, True

    # ----- News & threats -----
    if action in ("news", "cve", "security_news"):
        return handle_security_news(action, llm)
    if action == "threats":
        return handle_threats(action)
    if action in ("threat", "threat summary"):
        return handle_threat_summary(action)

    # ----- Groups -----
    if action == "groups":
        return handle_groups()

    # ----- Practice & labs -----
    if action == "practice":
        return handle_practice(action)
    if action.startswith("lab") or action == "htb":
        return handle_practice(action)

    # ----- Courses & story -----
    if action == "next":
        return handle_course("next")
    if action.startswith("course") or action == "courses":
        return handle_course(action)
    if action in ("story", "episode", "quest"):
        return handle_story_mode(action)

    # ----- Quiz & tasks -----
    if action == "quiz":
        return handle_quiz_action()
    if action == "task":
        return handle_task_action()

    # ----- Flag & achievements -----
    if action.startswith("flag"):
        flag = action.split(" ", 1)[1] if " " in action else None
        return handle_flag_check(flag)
    if action in ("achievements", "achievement"):
        return handle_achievements()

    # ----- Miscellaneous -----
    if action == "writeup":
        return handle_writeup()
    if action.startswith("add_book"):
        return handle_add_book(action)
    if action.startswith("log "):
        return handle_terminal_log(action[4:])
    if action in ("terminal", "term"):
        return handle_terminal_log()
    if action == "history":
        return handle_history(conn)
    if action in ("check", "logs"):
        return handle_container_check(action)
    if action.startswith("provider"):
        return handle_provider(action)
    if action.startswith("model"):
        return handle_model(action)
    if action.startswith("set-api-key"):
        return handle_set_api_key(action)
    if action in {"smart_test", "read_url"}:
        return handle_quiz_generation(action, None)

    # ----- Social engineering trainer -----
    if action == "social" or action.startswith("social "):
        return handle_social(action)

    # ----- Sandbox -----
    if action.startswith("sandbox"):
        return handle_sandbox(action)

    # ----- Risk level -----
    if action == "risk":
        return handle_risk(action)
    if action.startswith("risk "):
        return handle_risk(action)

    # ----- Adaptive learning -----
    if action == "adaptive" or action == "weaknesses":
        return handle_adaptive(action)

    # ----- Spaced Repetition -----
    if action == "repeat":
        return handle_repeat(action)

    # ----- Summary generation -----
    if action.startswith("summary"):
        return handle_summary(action)

    # ----- Auto Writeup -----
    if action == "auto_writeup":
        return handle_auto_writeup(action)

    # ----- Unknown command -----
    console.print("[bold red]Неизвестная команда или ввод.[/bold red]")
    console.print(
        "[yellow]Используй цифровое меню (0-44) или команды со /. Не трать время — я не библиотечный червь.[/yellow]"
    )
    console.print("[dim]Подсказка: введи /help или 9 для справки.[/dim]")
    return True, None, None, True
