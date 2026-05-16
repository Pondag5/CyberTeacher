# handlers/core.py
# isort: skip_file
import contextlib
import json
import logging
import os
from collections import OrderedDict, deque
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel

from state import get_state
from ui import Mode, show_help, show_help_detail, show_menu

from .registry import registry

from .achievements import handle_achievements
from .code_scan import handle_code_scan
from .config import handle_config
from .cve import handle_cve
from .docker_gen import handle_docker_gen
from .equipment import handle_equip, handle_tools
from .emotions import handle_emotions
from .features import handle_features
from .flags import handle_flag_check
from .health import handle_health
from .misc import (
    _ask_confirm,
    check_open_answer,
    clear_chat_db,
    extract_json_block,
    handle_adaptive,
    handle_add_book,
    handle_backup,
    handle_course,
    handle_export,
    handle_history,
    handle_model,
    handle_provider,
    handle_repeat,
    handle_risk,
    handle_set_api_key,
    handle_story_mode,
    handle_terminal_log,
    handle_usage,
    handle_version,
    handle_writeup,
)
from .missions import handle_missions
from .network import handle_network
from .news import get_last_news, handle_security_news

# ----------------------------------------------------------------------
# Импорты модулей handlers
# ----------------------------------------------------------------------
from .practice import handle_container_check, handle_practice
from .htb import handle_htb
from .walkthroughs import handle_walkthrough, handle_exploit_search
from .bug_bounty import handle_bounty
from .dashboard import handle_dashboard
from .exploit_submit import handle_exploit_submit
from .hints import handle_hint
from .tracks import handle_tracks
from .analytics import handle_analytics
from .phishing import handle_phishing
from .profile import handle_profile
from .mermaid import handle_mermaid
from .skills import handle_depth, handle_reputation, handle_skills, handle_skills_list
from .quiz import (
    handle_code_review,
    handle_quiz_action,
    handle_quiz_generation,
    handle_task_action,
)
from .sandbox import handle_sandbox
from .shop import handle_shop
from .social import handle_social
from .summary import handle_summary
from .summarize import handle_summarize
from .threats import handle_groups, handle_threat_summary, handle_threats
from .theme import handle_theme
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
        self.access_order = deque()
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
                self.access_order = deque(data.get("access_order", []))
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
    with contextlib.suppress(Exception):
        _response_cache._save()


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


def handle_stats(conn):
    """Показать статистику пользователя."""
    from memory import get_stats

    stats = get_stats(conn)
    console.print(f"[bold cyan]📈 Статистика:[/bold cyan]")
    console.print(f"  Очков: {stats.get('points', 0)}")
    console.print(f"  Квизов пройдено: {stats.get('quizzes', 0)}")
    console.print(f"  Задач решено: {stats.get('tasks', 0)}")
    console.print(f"  Кэш ответов: {_response_cache.stats()['size']} записей")
    return True, None, None, True


def handle_fixcode(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Генерация безопасной версии кода (L-09)."""
    from code_review import generate_secure_code

    parts = action.split(maxsplit=2)

    if len(parts) < 3:
        console.print(Panel(
            "[bold cyan]🔒 Генерация безопасного кода[/bold cyan]\n\n"
            "Использование:\n"
            "  /fixcode <язык> <код>  — сгенерировать безопасную версию\n\n"
            "Языки: python, javascript, php, java, bash\n\n"
            "Пример: /fixcode python query = f\"SELECT * FROM users WHERE id={user_id}\"",
            title="FIXCODE",
            border_style="cyan",
        ))
        return True, None, None, True

    language = parts[1].lower()
    code = parts[2]

    console.print(f"[cyan]🔍 Анализирую код ({language})...[/cyan]")
    secure = generate_secure_code(code, language)

    if secure:
        console.print(Panel(secure[:1500], title="🔒 БЕЗОПАСНАЯ ВЕРСИЯ", border_style="green"))
        state = get_state()
        state.track_skill("secure_coding", True, 20)
    else:
        console.print("[red]❌ Не удалось сгенерировать безопасный код[/red]")

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

    # Track command usage (M-31)
    state.track_command_usage(action.split()[0] if action else "unknown")

    # Try registry first for extensible commands
    handler, remaining_args = registry.get_handler(action)
    if handler is not None:
        return handler(remaining_args, llm, conn)

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
        from generators import generate_task

        parts = action.split(maxsplit=1)
        category = parts[1].strip() if len(parts) > 1 else None
        console.print("[cyan]🎯 Генерирую задание...[/cyan]")
        task = generate_task(vectordb=None, category=category)
        if task:
            console.print(Panel(
                f"[bold]Категория:[/bold] {task.category}\n"
                f"[bold]Сложность:[/bold] {task.difficulty}\n\n"
                f"[bold]Задача:[/bold]\n{task.question}\n\n"
                f"[bold]Подсказка:[/bold] {task.hint}",
                title="ЗАДАНИЕ",
                border_style="yellow",
            ))
        else:
            console.print("[red]❌ Не удалось сгенерировать задание[/red]")
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
    if action.startswith("lab"):
        return handle_practice(action)
    if action == "htb" or action.startswith("htb "):
        return handle_htb(action)

    # ----- Courses & story -----
    if action == "next":
        return handle_course("next")
    if action.startswith("course") or action == "courses":
        return handle_course(action)
    if action in ("story", "episode", "quest"):
        return handle_story_mode(action)

    # ----- Tracks (M-29) -----
    if action == "tracks" or action.startswith("tracks "):
        return handle_tracks(action)

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
    if action in {"adaptive", "weaknesses"}:
        return handle_adaptive(action)

    # ----- Learner Dashboard (M-28) -----
    if action == "dashboard":
        return handle_dashboard(action)

    # ----- Advanced Analytics (M-33) -----
    if action == "analytics":
        return handle_analytics(action)

    # ----- Voice Assistant (M-34) -----
    if action.startswith("voice") or action == "voice":
        from handlers.voice import handle_voice

        return handle_voice(action, "")

    # ----- Spaced Repetition -----
    if action == "repeat":
        return handle_repeat(action)

    # ----- Walkthroughs & Exploits (M-26) -----
    if action == "walkthrough" or action.startswith("walkthrough "):
        return handle_walkthrough(action)
    if action == "exploit" or action.startswith("exploit "):
        return handle_exploit_search(action)

    # ----- Summary generation -----
    if action.startswith("summary"):
        return handle_summary(action)

    # ----- Auto Writeup -----
    if action == "auto_writeup":
        return handle_auto_writeup(action)
    if action == "health":
        return handle_health(action)
    if action == "backup":
        return handle_backup(action)
    if action == "network":
        return handle_network(action)
    if action == "tools":
        return handle_tools(action)
    if action.startswith("equip "):
        return handle_equip(action)
    if action == "missions" or action.startswith("mission "):
        return handle_missions(action)
    if action == "exploit_submit" or action.startswith("exploit_submit "):
        return handle_exploit_submit(action)
    if action == "hint" or action.startswith("hint "):
        return handle_hint(action)
    if action.startswith("cve "):
        return handle_cve(action)
    if action.startswith("scan "):
        return handle_code_scan(action)

    # ----- Bug Bounty Simulation (M-31) -----
    if action == "bounty":
        return handle_bounty(action)

    # ----- Export chat history (M-30) -----
    if action == "export" or action.startswith("export "):
        return handle_export(action)

    # ----- Command usage statistics (M-31) -----
    if action == "usage":
        return handle_usage(action)

    # ----- Config wizard (M-28) -----
    if action == "config" or action.startswith("config "):
        return handle_config(action)

    # ----- Theme (M-29) -----
    if action == "theme" or action.startswith("theme "):
        return handle_theme(action)

    # ----- Feature flags (M-32) -----
    if action == "features" or action.startswith("features "):
        return handle_features(action)

    # ----- Chat summarization (M-22) -----
    if action == "summarize":
        return handle_summarize(action)

    # ----- Phishing constructor (M-04) -----
    if action == "phishing" or action.startswith("phishing "):
        return handle_phishing(action)

    # ----- Mermaid diagrams (M-09) -----
    if action == "mermaid" or action.startswith("mermaid "):
        return handle_mermaid(action)

    # ----- Skills tracker (L-02) -----
    if action == "skills" or action.startswith("skills "):
        if action == "skills":
            return handle_skills_list(action)
        return handle_skills(action)

    # ----- Reputation (L-10) -----
    if action == "reputation" or action.startswith("reputation "):
        return handle_reputation(action)

    # ----- Explanation depth (L-05) -----
    if action == "depth" or action.startswith("depth "):
        return handle_depth(action)

    # ----- Secure code generation (L-09) -----
    if action == "fixcode" or action.startswith("fixcode "):
        return handle_fixcode(action)

    # ----- Assignment templates (L-17) -----
    if action == "templates" or action.startswith("templates "):
        from handlers.assignment_templates import handle_assignment_templates
        return handle_assignment_templates(action)

    # ----- Emotions (M-19) -----
    if action == "emotions" or action.startswith("emotions "):
        return handle_emotions(action)

    # ----- Docker Compose generator (L-06) -----
    if action == "dockergen" or action.startswith("dockergen "):
        return handle_docker_gen(action)

    # ----- CTF dynamic flags (G-03) -----
    if action == "ctf" or action.startswith("ctf "):
        from handlers.ctf_flags import handle_ctf_flags
        return handle_ctf_flags(action)

    # ----- User profile (G-09) -----
    if action == "profile" or action.startswith("profile "):
        return handle_profile(action)

    # ----- Daily Challenge -----
    if action == "daily" or action.startswith("daily "):
        from handlers.daily import handle_daily
        return handle_daily(action)

    # ----- OSINT Module (M-03) -----
    if action == "osint" or action.startswith("osint "):
        from handlers.osint import handle_osint
        return handle_osint(action)

    # ----- Historical Mode (M-05) -----
    if action == "timeline" or action.startswith("timeline "):
        from handlers.history import handle_timeline
        return handle_timeline(action)

    # ----- Exploit Trainer (M-06) -----
    if action == "exploits" or action.startswith("exploits "):
        from handlers.exploit_trainer import handle_exploits
        return handle_exploits(action)

    # ----- Shodan / Censys Integration (M-07) -----
    if action == "shodan" or action.startswith("shodan "):
        from handlers.shodan_censys import handle_shodan
        return handle_shodan(action)
    if action == "censys" or action.startswith("censys "):
        from handlers.shodan_censys import handle_censys
        return handle_censys(action)

    # ----- Malware Analysis Sandbox (M-08) -----
    if action == "malware" or action.startswith("malware "):
        from handlers.malware_analysis import handle_malware
        return handle_malware(action)

    # ----- Interactive Investigations (M-10) -----
    if action == "investigation" or action.startswith("investigation "):
        from handlers.investigation import handle_investigation
        return handle_investigation(action)

    # ----- Jupyter Notebook Support (M-12) -----
    if action == "jupyter" or action.startswith("jupyter "):
        from handlers.jupyter import handle_jupyter
        return handle_jupyter(action)

    # ----- Video/Podcasts Player (M-16) -----
    if action == "media" or action.startswith("media "):
        from handlers.media import handle_media
        return handle_media(action)

    # ----- Time Loop / Alternate Realities (M-18) -----
    if action == "timeloop" or action.startswith("timeloop "):
        from handlers.timeloop import handle_timeloop
        return handle_timeloop(action)

    # ----- Cross-platform Sync (M-20) -----
    if action == "sync" or action.startswith("sync "):
        from handlers.sync import handle_sync
        return handle_sync(action)

    # ----- Mobile Companion App PWA (M-32) -----
    if action == "pwa" or action.startswith("pwa "):
        from handlers.pwa import handle_pwa
        return handle_pwa(action)

    # ----- Unknown command -----
    console.print("[bold red]Неизвестная команда или ввод.[/bold red]")
    console.print(
        "[yellow]Используй цифровое меню (0-44) или команды со /. Не трать время — я не библиотечный червь.[/yellow]"
    )
    console.print("[dim]Подсказка: введи /help или 9 для справки.[/dim]")
    return True, None, None, True
