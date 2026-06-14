# handlers/core.py
# isort: skip_file
import contextlib
import json
import logging
import os
from collections import OrderedDict, deque
from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context
from state import get_state
from ui import Mode, show_help_detail

from .achievements import handle_achievements
from .code_review_v2 import handle_code_review_v2
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
    handle_exploits_log,
    handle_heatmap,
    handle_history,
    handle_model,
    handle_provider,
    handle_repeat,
    handle_risk,
    handle_set_api_key,
    handle_state,
    handle_story_mode,
    handle_final_choice,
    handle_terminal_log,
    handle_topics,
    handle_usage,
    handle_version,
    handle_writeup,
    handle_writeups,
    handle_noise,
    handle_trace,
    handle_check_logs,
    handle_wipe_logs,
    handle_stealth,
    handle_debts,
    handle_faction,
    handle_echo,
    handle_memory,
    handle_ghost_log,
    handle_backdoor,
)
from .missions import handle_missions
from .network import handle_network
from .news import get_last_news, handle_security_news
from .offline import handle_offline
from .mood import handle_mood

# ----------------------------------------------------------------------
# Статические импорты (все хендлеры, которые были динамическими)
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
from .skills import (
    handle_depth,
    handle_reputation,
    handle_skills,
    handle_skills_list,
    handle_certificates,
)
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
from .tryhackme import handle_thm_action
from .pcap_analyzer import handle_pcap_action
from .metasploit import handle_msf_action
from .theme import handle_theme
from .lang import handle_lang
from .writeup_auto import handle_auto_writeup

from .ctf_flags import handle_ctf_flags
from .daily import handle_daily
from .osint import handle_osint
from .history import handle_timeline
from .exploit_trainer import handle_exploits
from .shodan_censys import handle_shodan, handle_censys
from .malware_analysis import handle_malware
from .investigation import handle_investigation
from .jupyter import handle_jupyter
from .media import handle_media
from .timeloop import handle_timeloop
from .sync import handle_sync
from .api_handler import handle_api
from .pwa import handle_pwa
from .versus import handle_versus
from .assignment_templates import handle_assignment_templates
from handlers.types import HandlerResult


console = Console()
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# RESPONSE CACHE
# ----------------------------------------------------------------------
class ResponseCache:
    def __init__(
        self, capacity: int = 100, cache_file: str = "./memory/response_cache.json"
    ) -> None:
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self.capacity: int = capacity
        self.cache_file: str = cache_file
        self.access_order: deque[str] = deque()
        self.hit_count: int = 0
        self.access_count: int = 0
        self._load()

    def _load(self) -> None:
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, "r", encoding="utf-8") as f:
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

    def _save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            data = {
                "cache": dict(self.cache),
                "access_order": list(self.access_order),
                "hit_count": self.hit_count,
                "access_count": self.access_count,
            }
            with open(self.cache_file, "w", encoding="utf-8") as f:
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

    def put(self, key: str, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
            self.access_order.remove(key)
        self.cache[key] = value
        self.access_order.append(key)
        if len(self.cache) > self.capacity:
            oldest = self.access_order.popleft()
            del self.cache[oldest]

    def clear(self) -> None:
        self.cache.clear()
        self.access_order.clear()
        self.hit_count = 0
        self.access_count = 0

    def stats(self) -> dict[str, Any]:
        return {
            "size": len(self.cache),
            "capacity": self.capacity,
            "hit_count": self.hit_count,
            "access_count": self.access_count,
        }


_response_cache = ResponseCache()


def clear_response_cache() -> None:
    _response_cache.clear()
    with contextlib.suppress(Exception):
        _response_cache._save()


def show_cache_stats() -> None:
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
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ----------------------------------------------------------------------
def show_help() -> None:
    from ui import show_help as ui_help

    ui_help()


def show_menu() -> None:
    from ui import show_menu as ui_menu

    ui_menu()


def handle_stats(conn: Any) -> HandlerResult:
    """Показать статистику пользователя."""
    import time

    from memory import get_stats

    state = get_context().state
    stats = get_stats(conn)

    # ANA-01: Session duration
    start_ts: float = state.metrics.get("start_time", 0)
    if start_ts > 0:
        elapsed = time.time() - start_ts
        hours = int(elapsed // 3600)
        mins = int((elapsed % 3600) // 60)
        session_dur = f"{hours}ч {mins}мин" if hours > 0 else f"{mins}мин"
    else:
        session_dur = "N/A"

    weak_count = len(state.get_weak_topics(threshold=70.0))
    due_reviews = len(state.get_due_reviews())
    streak = state.daily_streak
    session_count = (
        state.metrics.session_count if hasattr(state.metrics, "session_count") else 0
    )
    cache_stats = _response_cache.stats()
    access_count = cache_stats.get("access_count", 0)
    hit_count = cache_stats.get("hit_count", 0)
    hit_rate = (
        (hit_count / access_count * 100)
        if isinstance(access_count, (int, float)) and access_count > 0
        else 0
    )
    cache_size = cache_stats.get("size", 0)

    console.print(f"[bold cyan]📈 Статистика:[/bold cyan]")
    console.print(f"  Очки: {stats.get('points', 0):.0f}")
    console.print(f"  Квизов пройдено: {stats.get('quizzes', 0)}")
    console.print(f"  Задач решено: {stats.get('tasks', 0)}")
    console.print(f"  Сессия: {session_dur}")
    console.print(f"  Всего сессий: {session_count}")
    console.print(f"  Стрик: {streak} дней")
    console.print(f"  Слабые темы: {weak_count}")
    console.print(f"  Повторения готовы: {due_reviews}")
    console.print(f"  Кэш ответов: {cache_size} записей (hit rate: {hit_rate:.1f}%)")
    return True, None, None, True


def handle_fixcode(action: str) -> HandlerResult:
    """Генерация безопасной версии кода (L-09)."""
    from code_review import generate_secure_code

    parts = action.split(maxsplit=2)

    if len(parts) < 3:
        console.print(
            Panel(
                "[bold cyan]🔒 Генерация безопасного кода[/bold cyan]\n\n"
                "Использование:\n"
                "  /fixcode <язык> <код>  — сгенерировать безопасную версию\n\n"
                "Языки: python, javascript, php, java, bash\n\n"
                'Пример: /fixcode python query = f"SELECT * FROM users WHERE id={user_id}"',
                title="FIXCODE",
                border_style="cyan",
            )
        )
        return True, None, None, True

    language = parts[1].lower()
    code = parts[2]

    console.print(f"[cyan]🔍 Анализирую код ({language})...[/cyan]")
    secure = generate_secure_code(code, language)

    if secure:
        console.print(
            Panel(secure[:1500], title="🔒 БЕЗОПАСНАЯ ВЕРСИЯ", border_style="green")
        )
        state = get_context().state
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
) -> HandlerResult:
    """Главный диспетчер. Все команды (включая numeric menu) передаются в handle_extended_commands."""
    from di import AppContext, set_context

    ctx = AppContext(state=get_state(), db_conn=conn, _llm=llm)
    set_context(ctx)

    return handle_extended_commands(action, llm, conn)


def handle_extended_commands(action: str, llm: Any, conn: Any) -> HandlerResult:
    """Обработка всех команд. Если команда неизвестна — блокируем передачу в LLM."""
    state = get_context().state

    # Track command usage (M-31)
    state.track_command_usage(action.split(maxsplit=1)[0] if action else "unknown")

    # ----- Simple commands -----
    if action in ("help", "menu", "help detail"):
        if action == "menu":
            show_menu()
        elif action == "help detail":
            show_help_detail()
        else:
            show_help()
        return True, None, None, True

    if action == "guide":
        try:
            with open("docs/ГАЙД_VM.md", "r", encoding="utf-8") as f:
                guide = f.read()
            console.print(Panel(guide[:1000], title="ГАЙД ПО LAB", border_style="cyan"))
        except (OSError, IOError):
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

    if action == "genassignment" or action.startswith("genassignment "):
        from generators import generate_task

        parts = action.split(maxsplit=1)
        category = parts[1].strip() if len(parts) > 1 else None
        console.print("[cyan]🎯 Генерирую задание...[/cyan]")
        task = generate_task(vectordb=None, category=category)
        if task:
            console.print(
                Panel(
                    f"[bold]Категория:[/bold] {task.category}\n"
                    f"[bold]Сложность:[/bold] {task.difficulty}\n\n"
                    f"[bold]Задача:[/bold]\n{task.question}\n\n"
                    f"[bold]Подсказка:[/bold] {task.hint}",
                    title="ЗАДАНИЕ",
                    border_style="yellow",
                )
            )
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
    if action == "hybrid":
        state.set_persona("hybrid")
        return True, Mode.HYBRID, None, True

    # ----- Persona router (dynamic) -----
    if action == "persona" or action.startswith("persona "):
        return handle_persona(action)

    # ----- Offline mode (G-07) -----
    if action == "offline" or action.startswith("offline "):
        return handle_offline(action)

    # ----- Mood translator (G-08) -----
    if action == "mood" or action.startswith("mood "):
        return handle_mood(action)

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
    if action == "thm" or action.startswith("thm "):
        return handle_thm_action(action)
    if action == "pcap" or action.startswith("pcap "):
        return handle_pcap_action(action)
    if action == "msf" or action.startswith("msf "):
        return handle_msf_action(action)

    # ----- Courses & story -----
    if action == "next":
        return handle_course("next")
    if action.startswith("course") or action == "courses":
        return handle_course(action)
    if action == "topics" or action.startswith("topics "):
        return handle_topics(action)
    if action in ("story", "episode", "quest"):
        return handle_story_mode(action)
    if action == "final" or action.startswith("final "):
        return handle_final_choice(action)
    if action == "timeline" or action.startswith("timeline "):
        from handlers.misc import handle_timeline_action

        return handle_timeline_action(action)

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
    if action == "writeups" or action.startswith("writeups "):
        return handle_writeups(action)
    if action == "exploits_log":
        return handle_exploits_log(action)
    if action == "heatmap":
        return handle_heatmap(action)
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

    # ----- Noise / Stealth / Trace -----
    if action == "noise":
        return handle_noise(action)
    if action == "stealth":
        return handle_stealth(action)
    if action == "trace":
        return handle_trace(action)

    # ----- Dirty logs -----
    if action == "check_logs":
        return handle_check_logs(action)
    if action == "wipe_logs":
        return handle_wipe_logs(action)

    # ----- Debts -----
    if action == "debts":
        return handle_debts(action)

    # ----- Factions -----
    if action == "faction" or action.startswith("faction "):
        return handle_faction(action)

    # ----- Echo -----
    if action == "echo":
        return handle_echo(action)

    # ----- Memory -----
    if action in ("memory", "memories"):
        return handle_memory(action)

    # ----- Watchers -----
    if action == "watchers":
        from handlers.watchers import handle_watchers

        return handle_watchers(action)

    # ----- Phantom labs -----
    if action == "phantom" or action.startswith("phantom "):
        from handlers.phantom_lab import handle_phantom

        return handle_phantom(action)

    # ----- Secret room -----
    if action == "secret" or action.startswith("secret "):
        from handlers.secret_room import handle_secret

        return handle_secret(action)

    # ----- Rewind (time machine) -----
    if action == "rewind" or action.startswith("rewind "):
        from handlers.rewind import handle_rewind

        return handle_rewind(action)

    # ----- Adaptive learning -----
    if action in {"adaptive", "weaknesses"}:
        return handle_adaptive(action)

    # ----- Learner Dashboard (M-28) -----
    if action == "dashboard":
        return handle_dashboard(action)

    # ----- Advanced Analytics (M-33) -----
    if action == "analytics":
        return handle_analytics(action)

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
    if action == "doctor" or action.startswith("doctor "):
        from handlers.doctor import handle_doctor

        return handle_doctor(action)
    if action == "context" or action.startswith("context "):
        from handlers.context import handle_context

        return handle_context(action)
    if action == "backup":
        return handle_backup(action)
    if action == "state" or action.startswith("state "):
        return handle_state(action)
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
    if action == "scanv2" or action.startswith("scanv2 "):
        return handle_code_review_v2(action)

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

    # ----- Language (i18n) -----
    if action == "lang" or action.startswith("lang "):
        return handle_lang(action)

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

    # ----- Skill Certificates (SKL-03) -----
    if action == "certificates" or action.startswith("certificates "):
        return handle_certificates(action)

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
        return handle_assignment_templates(action)

    # ----- Emotions (M-19) -----
    if action == "emotions" or action.startswith("emotions "):
        return handle_emotions(action)

    # ----- Docker Compose generator (L-06) -----
    if action == "dockergen" or action.startswith("dockergen "):
        return handle_docker_gen(action)

    # ----- CTF dynamic flags (G-03) -----
    if action == "ctf" or action.startswith("ctf "):
        return handle_ctf_flags(action)

    # ----- User profile (G-09) -----
    if action == "profile" or action.startswith("profile "):
        return handle_profile(action)

    # ----- Daily Challenge -----
    if action == "daily" or action.startswith("daily "):
        return handle_daily(action)

    # ----- OSINT Module (M-03) -----
    if action == "osint" or action.startswith("osint "):
        return handle_osint(action)

    # ----- Historical Mode (M-05) -----
    if action == "timeline" or action.startswith("timeline "):
        return handle_timeline(action)

    # ----- Exploit Trainer (M-06) -----
    if action == "exploits" or action.startswith("exploits "):
        return handle_exploits(action)

    # ----- Shodan / Censys Integration (M-07) -----
    if action == "shodan" or action.startswith("shodan "):
        return handle_shodan(action)
    if action == "censys" or action.startswith("censys "):
        return handle_censys(action)

    # ----- Malware Analysis Sandbox (M-08) -----
    if action == "malware" or action.startswith("malware "):
        return handle_malware(action)

    # ----- Interactive Investigations (M-10) -----
    if action == "investigation" or action.startswith("investigation "):
        return handle_investigation(action)

    # ----- Jupyter Notebook Support (M-12) -----
    if action == "jupyter" or action.startswith("jupyter "):
        return handle_jupyter(action)

    # ----- Video/Podcasts Player (M-16) -----
    if action == "media" or action.startswith("media "):
        return handle_media(action)

    # ----- Time Loop / Alternate Realities (M-18) -----
    if action == "timeloop" or action.startswith("timeloop "):
        return handle_timeloop(action)

    # ----- Cross-platform Sync (M-20) -----
    if action == "sync" or action.startswith("sync "):
        return handle_sync(action)

    # ----- REST API Server (M-31) -----
    if action == "api" or action.startswith("api "):
        return handle_api(action)

    # ----- Mobile Companion App PWA (M-32) -----
    if action == "pwa" or action.startswith("pwa "):
        return handle_pwa(action)

    # ----- LLM Versus Mode (NEW-01) -----
    if action == "versus" or action.startswith("versus "):
        return handle_versus(action)

    # ----- World Stability + Teacher Sleep (Chapter 7) -----
    if action == "stability" or action.startswith("stability "):
        from handlers.misc import handle_stability
        return handle_stability(action)

    if action == "teacher_sleep" or action.startswith("teacher_sleep "):
        from handlers.misc import handle_teacher_sleep
        return handle_teacher_sleep(action)

    # ----- FAISS Watcher (Optimization) -----
    if action == "faiss_watch" or action.startswith("faiss_watch "):
        from handlers.misc import handle_faiss_watch
        return handle_faiss_watch(action)

    # ----- Ghost Log (Chapter 1) -----
    if action == "ghost_log" or action.startswith("ghost_log "):
        from handlers.misc import handle_ghost_log

        return handle_ghost_log(action)

    # ----- Backdoors (Chapter 5) -----
    if action == "backdoor" or action.startswith("backdoor "):
        from handlers.misc import handle_backdoor

        return handle_backdoor(action)

    # ----- Tutorial -----
    if action == "tutorial":
        from smart_hints import get_tutorial_step, get_total_tutorial_steps

        step = getattr(state, "tutorial_step", 0)
        total = get_total_tutorial_steps()
        if step >= total:
            console.print(
                "[green]\u2705 \u0422\u0443\u0442\u043e\u0440\u0438\u0430\u043b \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d![/green]"
            )
            return True, None, None, True
        data = get_tutorial_step(step)
        if data:
            console.print(
                Panel(
                    f"{data['message']}\n\n"
                    f"[cyan]\u0412\u0432\u0435\u0434\u0438\u0442\u0435:[/cyan] {data['command']}\n"
                    f"[dim]{data['hint']}[/dim]",
                    title=f"\ud83c\udfaf \u0422\u0443\u0442\u043e\u0440\u0438\u0430\u043b ({step + 1}/{total})",
                    border_style="cyan",
                )
            )
            state.tutorial_step = step + 1
        return True, None, None, True

    # ----- Difficulty level -----
    if action.startswith("difficulty"):
        parts = action.split()
        if len(parts) < 2:
            from adaptive_ui import (
                DIFFICULTY_CONFIG,
                DIFFICULTY_LEVELS,
                get_progress_hint,
            )

            level = getattr(state, "difficulty_level", "beginner")
            config = DIFFICULTY_CONFIG.get(level, {})
            lines = [
                f"\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c: {config.get('difficulty_label', level)}"
            ]
            for l in DIFFICULTY_LEVELS:
                c = DIFFICULTY_CONFIG.get(l, {})
                marker = "\u2705" if l == level else "  "
                lines.append(
                    f"  {marker} {c.get('difficulty_label', l)} — {c.get('description', '')}"
                )
            hint = get_progress_hint(level, state)
            if hint:
                lines.append(f"\n[dim]{hint}[/dim]")
            console.print(
                Panel(
                    "\n".join(lines),
                    title="\ud83d\udccb \u0423\u0440\u043e\u0432\u0435\u043d\u044c \u0441\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u0438",
                    border_style="cyan",
                )
            )
            return True, None, None, True

    # ----- Report -----
    if action == "report":
        try:
            from report_generator import generate_report_from_state
            from config import sanitize_log

            html = generate_report_from_state(state)
            report_path = "./memory/training_report.html"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(html)
            console.print(
                f"[green]\u2705 \u041e\u0442\u0447\u0451\u0442 \u0441\u043e\u0445\u0440\u0430\u043d\u0451\u043d: {report_path}[/green]"
            )
        except Exception as e:
            console.print(
                f"[red]\u2717 \u041e\u0448\u0438\u0431\u043a\u0430: {e}[/red]"
            )
        return True, None, None, True

    # ----- Persona handler -----
    if action == "persona" or action.startswith("persona "):
        return handle_persona(action)

    # ----- Unknown command -----
    from smart_hints import suggest_command

    suggestion = suggest_command(action)
    if suggestion:
        console.print(f"[yellow]{suggestion}[/yellow]")
    else:
        console.print("[bold red]Неизвестная команда или ввод.[/bold red]")
        console.print("[dim]Подсказка: введи /help или 9 для справки.[/dim]")
    return True, None, None, True


def handle_persona(action: str) -> tuple:
    """Обработка /persona [list|auto|rick|doc|analyst|ghost]."""
    from persona_router import (
        list_personas,
        get_preferred_persona,
        set_preferred_persona,
        get_persona_info,
    )
    from ui import console, Panel

    state = get_context().state
    parts = action.split()
    sub = parts[1].lower() if len(parts) > 1 else "status"

    if sub == "list":
        personas = list_personas()
        lines = []
        current = get_preferred_persona()
        for p in personas:
            marker = " ← ТЕКУЩАЯ" if p["id"] == current else ""
            lines.append(f"  {p['emoji']} {p['name']} ({p['id']}){marker}")
        console.print(
            Panel("\n".join(lines), title="🎭 Персоны учителя", border_style="magenta")
        )
        return True, None, None, True

    if sub == "status":
        current = get_preferred_persona()
        info = get_persona_info(current)
        console.print(
            Panel(
                f"{info['emoji']} Текущая персона: {info['name']} ({info['id']})\n\n"
                f"Доступные: {', '.join(p['id'] for p in list_personas())}\n\n"
                f"Использование: /persona <id> или /persona auto",
                title="🎭 Персона",
                border_style="cyan",
            )
        )
        return True, None, None, True

    if sub in ("auto", "rick", "doc", "analyst", "ghost"):
        if set_preferred_persona(sub):
            info = get_persona_info(sub)
            console.print(
                Panel(
                    f"{info['emoji']} Персона изменена на: {info['name']}",
                    title="🎭 Персона",
                    border_style="green",
                )
            )
        else:
            console.print("[red]Неизвестная персона[/red]")
        return True, None, None, True

    console.print(
        "[yellow]Использование: /persona [list|status|auto|rick|doc|analyst|ghost][/yellow]"
    )
    return True, None, None, True


