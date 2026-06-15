#!/usr/bin/env python3
"""
CyberTeacher v5.21 - Main entry point with Context Budget Manager + auto cleanup
"""

import json
import os
import random
import sys
import time

# Force UTF-8 on Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["PYTHONUTF8"] = "1"

from utils.console_encoding import setup_utf8_console

setup_utf8_console()

import atexit
import contextlib
import logging
import logging.handlers
from typing import Optional, Callable

# Подавление шумных логов
os.environ["TQDM_DISABLE"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

_noisy_prefixes = [
    "sentence_transformers",
    "transformers",
    "huggingface_hub",
    "httpx",
    "httpcore",
    "urllib3",
    "filelock",
    "torch",
    "tqdm",
    "asyncio",
    "uvicorn.access",
    "starlette",
]
for _p in _noisy_prefixes:
    logging.getLogger(_p).setLevel(logging.WARNING)

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

# Structured file logging with 7-day rotation
try:
    from logging_config import setup_logging

    setup_logging()
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ],
)

# Импорты проекта
logger = logging.getLogger(__name__)
from config import NUMERIC_MENU, LazyLoader, THINKING_ENABLED, SOCRATIC_ENABLED
from context_budget import ContextBudgetManager
from handlers.core import _response_cache, handle_commands
from memory import init_db, cleanup_expired_cache, get_cached_response, cache_response
from memory import (
    get_chat_history,
    get_stats,
    get_weak_topics,
    save_message,
    update_stats,
)
from memory import cleanup_old_messages  # <-- НОВЫЙ ИМПОРТ
from knowledge import get_relevant_docs, load_knowledge_base
from ui import Mode, console, print_banner, show_help, show_menu, print_thinking
from pedagogy import ThinkingVisualizer
from terminal_log import init_terminal_log, log_command
from state import get_state
from code_review import code_review_function as code_review
from generators import generate_quiz, generate_task

# ===== ПРОМПТЫ =====
PROMPT_FILE = "./teacher_prompt.txt"
STORIES_FILE = "./stories.json"


def load_teacher_prompt() -> str:
    persona = ""
    if os.path.exists(PROMPT_FILE):
        try:
            with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                persona = f.read()
        except (OSError, IOError):
            persona = "Ты - хакер-ветеран из 90-х, учитель кибербезопасности."
    else:
        persona = "Ты - хакер-ветеран из 90-х, учитель кибербезопасности."

    story = ""
    if os.path.exists(STORIES_FILE):
        try:
            with open(STORIES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                stories = data.get("stories", [])
                if stories:
                    story = random.choice(stories)
        except (OSError, IOError, json.JSONDecodeError):
            pass
    if story:
        return f"{persona}\n\nВОТ ТВОЯ ИСТОРИЯ ДЛЯ ЭТОГО ОТВЕТА: {story}"
    return persona


def get_mode_prompt(
    mode: Mode, context_str: str, docs_context: str, study_context: str = ""
) -> str:
    state = get_state()
    persona = state.get_persona()
    prompts_path = os.path.join("config", "teacher_prompts.json")
    try:
        with open(prompts_path, "r", encoding="utf-8") as f:
            prompts_data = json.load(f)
    except (OSError, IOError, json.JSONDecodeError):
        prompts_data = {}
    base_prompt = prompts_data.get("system_prompt", "Ты - учитель кибербезопасности.")
    personas = prompts_data.get("personas", {})
    persona_instructions = personas.get(persona, {}).get("instructions", [])
    if persona_instructions:
        base_prompt += "\n\nИнструкции для режима:\n" + "\n".join(
            [f"- {p}" for p in persona_instructions]
        )
    comm_mood = getattr(state, "communication_mood", "normal")
    if comm_mood != "normal":
        from handlers.mood import MOODS

        mood_modifier = MOODS.get(comm_mood, {}).get("prompt_modifier", "")
        if mood_modifier:
            base_prompt += f"\n\nСТИЛЬ ОБЩЕНИЯ: {mood_modifier}"
    return f"""{base_prompt}

КОНТЕКСТ УЧЕНИКА:
{study_context}

ДАННЫЕ ИЗ БАЗЫ ЗНАНИЙ:
{docs_context}
"""


# ===== ОБЁРТКА LLM С КЭШИРОВАНИЕМ =====
class CachedLLM:
    def __init__(self, llm, conn):
        self.llm = llm
        self.conn = conn

    def invoke(self, prompt: str):
        import hashlib

        model_id = getattr(self.llm, "model", "default")
        query_string = f"{prompt}|{model_id}"
        query_hash = hashlib.sha256(query_string.encode()).hexdigest()
        cached = get_cached_response(self.conn, query_hash)
        if cached:

            class CachedResponse:
                def __init__(self, content):
                    self.content = content

            return CachedResponse(cached)
        try:
            response = self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"LLM invoke failed: {e}")
            raise
        text = response.content if hasattr(response, "content") else str(response)
        cache_response(self.conn, query_hash, text, ttl_seconds=86400)
        # Track LLM stats
        from state import get_state as _gs

        _s = _gs()
        _s.llm_call_count += 1
        _s.llm_total_tokens += len(text) // 4
        return response

    def stream(self, prompt: str):
        import hashlib

        model_id = getattr(self.llm, "model", "default")
        query_string = f"{prompt}|{model_id}"
        query_hash = hashlib.sha256(query_string.encode()).hexdigest()
        cached = get_cached_response(self.conn, query_hash)
        if cached:
            yield cached
            return
        full_chunks = []
        for chunk in self.llm.stream(prompt):
            full_chunks.append(chunk)
            yield chunk
        full_text = "".join(
            str(ch.content) if hasattr(ch, "content") else str(ch) for ch in full_chunks
        )
        if full_text:
            cache_response(self.conn, query_hash, full_text, ttl_seconds=86400)
            # Track LLM stats for streaming
            try:
                from state import get_state as _gs

                _s = _gs()
                _s.llm_call_count += 1
                _s.llm_total_tokens += len(full_text) // 4
            except (ValueError, RuntimeError):
                pass


def get_llm():
    return LazyLoader.get_llm()


def get_cached_llm(conn):
    llm = get_llm()
    return CachedLLM(llm, conn) if llm else None


def set_learning_context(course=None, topic=None, lab=None, action=None):
    get_state().set_learning_context(course, topic, lab, action)


def get_learning_context():
    return get_state().get_learning_context()


_news_cache = None


def get_news_context():
    global _news_cache
    if _news_cache is None:
        try:
            from news_fetcher import NewsFetcher

            nf = NewsFetcher()
            nf.fetch_all()
            _news_cache = nf.get_formatted_news()
        except (ImportError, OSError):
            _news_cache = ""
    return _news_cache


def get_embeddings():
    return LazyLoader.get_embeddings()


def _save_session_summary():
    state = get_state()
    start_time: float = state.metrics.get("start_time", 0)
    if start_time > 0:
        elapsed = time.time() - start_time
        hours = int(elapsed // 3600)
        mins = int((elapsed % 3600) // 60)
        state.last_session_summary = {
            "duration": f"{hours}ч {mins}мин" if hours > 0 else f"{mins}мин",
            "duration_seconds": int(elapsed),
            "points": state.points,
            "streak": state.daily_streak,
            "timestamp": time.time(),
        }


# ===== ГЛАВНЫЙ ЦИКЛ =====
def main():
    print_banner()
    console.print("[bold green]Loading...[/bold green]\n")

    state = get_state()
    from settings import get_settings

    state.load_from_file(str(get_settings().state_file))
    init_terminal_log()
    settings = get_settings()
    state.maybe_auto_backup(
        backup_dir=str(settings.backup_dir),
        max_age_hours=settings.max_backup_age_hours,
        max_backups=settings.max_backups,
    )

    # Инициализация менеджера контекста (восстанавливаем из сохранённого состояния)
    budget_manager = ContextBudgetManager.from_dict(
        getattr(state, "context_budget", None)
    )

    # Prompt Toolkit
    have_prompt_toolkit = False
    session_hist = None
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import FileHistory

        have_prompt_toolkit = True
        history_path = os.path.join(".", "memory", "command_history.txt")
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        session_hist = PromptSession(history=FileHistory(history_path))
    except ImportError:
        pass
    except Exception as e:
        console.print(f"[yellow]⚠️ prompt_toolkit: {e}[/yellow]")

    conn = init_db()
    cleanup_expired_cache(conn)
    # ===== НОВОЕ: очистка старых сообщений (оставляем 500 последних) =====
    cleanup_old_messages(conn, keep_last=500)
    # ===================================================================
    vectordb = load_knowledge_base()

    # Советы при старте
    weak_topics = state.get_weak_topics(threshold=70.0)
    if weak_topics:
        rec = weak_topics[0]
        console.print(
            f"[bold yellow]Совет:[/bold yellow] Слабая тема - [cyan]{rec['topic']}[/cyan] (успешность {rec['success_rate']:.1f}%). /quiz"
        )
    due_reviews = state.get_due_reviews()
    if due_reviews:
        console.print(
            f"[bold magenta]⏰ Напоминание:[/bold magenta] {len(due_reviews)} тем для повторения. /repeat"
        )

    # Прошлая сессия
    last = state.last_session_summary
    if last and last.get("timestamp", 0) > 0:
        from datetime import datetime

        dt = datetime.fromtimestamp(last["timestamp"])
        time_ago = datetime.now() - dt
        if time_ago.days == 0:
            when = f"сегодня в {dt.strftime('%H:%M')}"
        elif time_ago.days == 1:
            when = "вчера"
        else:
            when = f"{time_ago.days} дн. назад"
        console.print(
            f"[dim]📋 Прошлая сессия ({when}): {last.get('duration', '?')}, "
            f"очки: {last.get('points', 0):.0f}, стрик: {last.get('streak', 0)}д[/dim]"
        )

    current_mode = Mode.TEACHER
    show_help()
    show_menu()

    stats = get_stats(conn)
    weak_count = len(state.get_weak_topics(threshold=70.0))
    due_count = len(state.get_due_reviews())
    console.print(
        f"[bold]Режим:[/bold] {current_mode.value} | "
        f"[bold]Очки:[/bold] {stats['points']:.0f} | "
        f"[bold]Уровень:[/bold] {stats.get('level', 1)} | "
        f"[bold]Стрик:[/bold] {state.daily_streak}д | "
        f"[bold]Слабые темы:[/bold] {weak_count} | "
        f"[bold]Повторения:[/bold] {due_count} готовы"
    )

    while True:
        try:
            if have_prompt_toolkit and session_hist:
                user_input = session_hist.prompt("\nТы: ").strip()
            else:
                user_input = console.input("\n[bold]Ты:[/bold] ").strip()
        except KeyboardInterrupt:
            console.print("\n[yellow]Пока![/yellow]")
            break
        if not user_input:
            continue
        if len(user_input) > 2000:
            console.print("[red]❌ Слишком длинный ввод (максимум 2000 символов)[/red]")
            continue

        # Secret phrase detection
        try:
            from secret_language import detect_secret_phrase
            secret = detect_secret_phrase(user_input)
            if secret:
                console.print(f"[bold magenta]🔐 Секретная фраза:[/bold magenta] {secret['phrase']}")
                console.print(f"[magenta]{secret['response']}[/magenta]")
                # Apply effect
                if secret["effect"] == "hint":
                    state.hint_credits = min(10, state.hint_credits + 1)
                    console.print("[green]💡 Получен кредит подсказки![/green]")
                elif secret["effect"] == "mood_serious":
                    state.current_mood = "serious"
                    console.print("[yellow]🎭 Настроение учителя: серьёзное[/yellow]")
                elif secret["effect"] == "unlock_ghost_log":
                    console.print("[green]📜 Ghost Log разблокирован![/green]")
                # Don't process further - secret phrase handled
                continue
        except ImportError:
            pass

        state = get_state()
        if not state.can_make_request():
            console.print("[red]❌ Слишком много запросов. Подождите минуту.[/red]")
            continue
        state.record_request()

        if state.trace_deadline and time.time() > state.trace_deadline:
            console.print("[red]⏰ Время на лабораторию истекло![/red]")
            if state.trace_hint:
                console.print(f"[yellow]💡 Подсказка: {state.trace_hint}[/yellow]")
            state.trace_deadline = None
            state.trace_hint = None

        # Автоматическая подсказка (без LLM)
        if (
            not user_input.startswith("/")
            and not user_input.isdigit()
            and state.hint_enabled
            and state.hints_used < 3
            and state.hint_credits > 0
            and time.time() - state.last_hint_time > state.hint_cooldown
        ):
            from handlers.hints import generate_contextual_hint

            hint = generate_contextual_hint(user_input, state.get_learning_context())
            if hint:
                console.print(f"[yellow]💡 Подсказка: {hint}[/yellow]")
                state.hints_used += 1
                state.last_hint_time = time.time()
                state.points = max(0, state.points * 0.9)
                console.print(
                    f"[dim]Использовано подсказок: {state.hints_used}/3[/dim]"
                )

        state.send_message()
        log_command(user_input, is_input=True)

        if user_input.isdigit() and user_input in NUMERIC_MENU:
            action = NUMERIC_MENU[user_input]
        else:
            action = user_input[1:] if user_input.startswith("/") else user_input

        cli_log = logging.getLogger("cyberteacher.cli")
        cli_log.info(f"COMMAND: {action}")
        try:
            continue_loop, new_mode, _, action_taken = handle_commands(
                action, conn, lambda: get_cached_llm(conn)
            )
            cli_log.info(
                f"RESULT: action={action}, taken={action_taken}, continue={continue_loop}"
            )
        except Exception as e:
            cli_log.exception(f"COMMAND FAILED: {action}")
            raise

        # Check narrative events after any state change
        try:
            from handlers.event_engine import check_events

            fired_events = check_events()
            for evt in fired_events:
                console.print(
                    f"[bold magenta]⚡ {evt['title']}:[/bold magenta] {evt['message']}"
                )
                if evt["effects"]:
                    console.print(f"[dim]{', '.join(evt['effects'])}[/dim]")
        except ImportError:
            pass

        # Check hidden knowledge unlocks
        try:
            from world_state import get_world_state

            world = get_world_state()
            unlocked = world.check_unlock_knowledge(state)
            if unlocked:
                console.print(
                    f"[bold cyan]🔓 Скрытые знания разблокированы:[/bold cyan] {unlocked['title']}"
                )
                console.print(f"[cyan]{unlocked['desc']}[/cyan]")
        except ImportError:
            pass

        # World Stability auto-adjustments based on action
        if action_taken:
            try:
                # Negative impacts
                if "fail" in action.lower() or "fail" in str(action).lower():
                    state.adjust_world_stability(-2)
                if state.trace_active:
                    state.adjust_world_stability(-1)
                if state.watcher_attack_active:
                    state.adjust_world_stability(-3)
                # Positive impacts
                if "complete" in action.lower() and ("mission" in action.lower() or "track" in action.lower()):
                    state.adjust_world_stability(2)
                if "achievement" in action.lower() or "earned" in str(action).lower():
                    state.adjust_world_stability(1)
            except Exception:
                pass

        if action_taken:
            if not continue_loop:
                break
            if new_mode:
                current_mode = new_mode
                get_state().set_persona(
                    current_mode.value
                    if hasattr(current_mode, "value")
                    else str(current_mode)
                )
            console.print(
                f"\n[bold]Режим:[/bold] {current_mode.value if current_mode else 'Учитель'}"
            )
            continue

        # === ОБРАБОТКА ВОПРОСА К LLM ===
        history = get_chat_history(conn)
        # Управление контекстом — токен-осознанное обрезание
        trimmed_history, warn_msg = budget_manager.prepare_context(
            history,
            max_messages=30,
            user_input=user_input,
        )
        if warn_msg:
            console.print(warn_msg)
        context_str = "\n".join(
            [f"{m['role']}: {m['content']}" for m in trimmed_history]
        )

        # RAG
        relevant_docs = get_relevant_docs(vectordb, user_input) if vectordb else []
        docs_context = ""
        if relevant_docs:
            docs_context = "\n📖 Контекст:\n" + "\n".join(
                [f"- {d.page_content}" for d in relevant_docs]
            )

        # Контекст обучения
        learning_ctx = get_learning_context()
        container_info = ""
        terminal_info = ""
        kb_info = ""
        weak_info = ""
        risk_info = ""
        try:
            from knowledge import get_knowledge_status

            status = get_knowledge_status()
            kb_info = f"В базе знаний: {status.get('files_in_db', 0)} документов."
            weak_topics = get_weak_topics(conn)
            if weak_topics:
                topics_str = ", ".join(
                    [f"{t['topic']} ({t['rate']}% успеха)" for t in weak_topics]
                )
                weak_info = f"Слабые темы ученика: {topics_str}."
            if state.get_persona() in ("ctf", "story"):
                risk_status = state.get_risk_status()
                risk_info = (
                    f"⚠️ Уровень риска: {risk_status} ({state.risk_level}/100).\n"
                )
            from practice import get_all_running_labs, get_container_logs, get_terminal_log

            terminal_log = get_terminal_log(last_n=10)
            if terminal_log and terminal_log != "Лог пуст":
                terminal_info = f"\n--- ТЕРМИНАЛ УЧЕНИКА ---\n{terminal_log}\n"
            running_labs = get_all_running_labs()
            if running_labs:
                container_info = "\n--- ЗАПУЩЕННЫЕ КОНТЕЙНЕРЫ ---\n"
                for lab_key, lab_info in running_labs.items():
                    container_info += f"  - {lab_info['name']}: {lab_info['status']}\n"
                    logs = get_container_logs(f"{lab_key}-web", lines=10)
                    if logs and logs != "Логов нет":
                        container_info += f"    Логи: {logs[:200]}...\n"
        except Exception as e:
            container_info = f"\n(Контейнеры недоступны: {e})"

        if learning_ctx.get("current_course") or learning_ctx.get("current_lab"):
            study_context = f"""
=== ТЕКУЩИЙ КОНТЕКСТ ===
- Курс: {learning_ctx.get("current_course", "не выбран")}
- Тема: {learning_ctx.get("current_topic", "не выбрана")}
- Лаба: {learning_ctx.get("current_lab", "не запущена")}

{kb_info}
{weak_info}
{risk_info}
{container_info}
{terminal_info}
"""
        else:
            study_context = f"=== КОНТЕКСТ: Ученик ===\n{kb_info}\n{weak_info}\n{risk_info}\n{container_info}\n{terminal_info}"

        system_prompt = get_mode_prompt(
            current_mode, context_str, docs_context, study_context
        )

        # === Context Awareness + Personality Drift ===
        try:
            from context_awareness import get_context_info, get_atmosphere_hint
            from personality import apply_personality_drift

            ctx_info = get_context_info(
                session_start=state.metrics.get("start_time", 0),
                messages_this_session=len(trimmed_history),
            )
            atmosphere = get_atmosphere_hint(ctx_info)
            personality_mod = apply_personality_drift(ctx_info)

            if atmosphere:
                system_prompt += f"\n\n{atmosphere}"
            if personality_mod:
                system_prompt += f"\n\n{personality_mod}"
        except ImportError:
            pass

        # === Behavioral Archetype ===
        try:
            from behavior_profile import get_archetype_prompt_modifier

            archetype_mod = get_archetype_prompt_modifier(state)
            if archetype_mod:
                system_prompt += archetype_mod
        except ImportError:
            pass

        # === Persona Router (dynamic) ===
        try:
            from persona_router import select_persona, get_persona_prompt

            user_msg = user_input if "user_input" in locals() else ""
            persona_id = select_persona(state, user_msg)
            persona_mod = get_persona_prompt(persona_id)
            if persona_mod:
                system_prompt += persona_mod
        except ImportError:
            pass

        # === Persistent World State + Episode Memory ===
        try:
            from world_state import get_world_state
            from episode_memory import get_episode_memory

            world = get_world_state()
            world.check_spawn_incident(state)
            world_prompt = world.get_world_prompt()
            if world_prompt:
                system_prompt += f"\n\n{world_prompt}"

            memory = get_episode_memory()
            memory_prompt = memory.get_memory_prompt()
            if memory_prompt:
                system_prompt += f"\n\n{memory_prompt}"
        except ImportError:
            pass

        # === Cyberpsychosis ===
        try:
            from cyberpsychosis import get_cyberpsychosis

            cp = get_cyberpsychosis()
            cp.decay(0.5)
            cp_prompt = cp.get_system_prompt_addition()
            if cp_prompt:
                system_prompt += f"\n\n{cp_prompt}"
        except ImportError:
            pass

        # === Atmosphere (ghost logs, echo, doubt) ===
        try:
            from atmosphere import maybe_get_atmospheric_message
            from cyberpsychosis import get_cyberpsychosis as _cp

            _cp_state = _cp()
            atm_msg = maybe_get_atmospheric_message(
                cyberpsychosis_level=_cp_state.get_level(),
                stress=_cp_state.stress,
                recklessness=_cp_state.recklessness,
                memorable_events=getattr(state, "memorable_events", []),
            )
            if atm_msg:
                system_prompt += f"\n\n{atm_msg}"
        except ImportError:
            pass

        # === Adaptive UI difficulty prompt ===
        try:
            from adaptive_ui import (
                get_system_prompt_prefix,
                check_auto_promotion,
                get_progress_hint,
            )

            level = getattr(state, "difficulty_level", "beginner")
            diff_prefix = get_system_prompt_prefix(level)
            if diff_prefix:
                system_prompt += diff_prefix
            # Auto-promotion check
            new_level = check_auto_promotion(state)
            if new_level:
                state.difficulty_level = new_level
                try:
                    from episode_memory import get_episode_memory

                    get_episode_memory().record(
                        "milestone",
                        f"Difficulty promoted to {new_level}",
                        f"XP: {state.xp}, Quizzes: {state.quizzes_taken}",
                        importance=8,
                    )
                except (ImportError, RuntimeError):
                    pass
                console.print(
                    f"[bold cyan]\ud83d\udd25 \u0412\u044b \u043f\u0435\u0440\u0435\u0448\u043b\u0438 \u043d\u0430 \u0443\u0440\u043e\u0432\u0435\u043d\u044c {new_level.upper()}![/bold cyan]"
                )
        except ImportError:
            pass

        # Versus override
        from handlers.versus import get_versus_system_prompt, increment_versus_attempts

        versus_prompt = get_versus_system_prompt()
        if versus_prompt:
            system_prompt = versus_prompt

        if THINKING_ENABLED and current_mode == Mode.CTF:
            thinking = ThinkingVisualizer.generate_thinking(
                context_str, user_input, "socratic"
            )
            print_thinking(thinking)

        full_response = ""
        try:
            if state.offline_mode:
                console.print(
                    "[yellow]📴 Офлайн-режим: чат с LLM отключён. /offline off для включения.[/yellow]"
                )
            else:
                llm = get_cached_llm(conn)
                if llm is None:
                    console.print(
                        "[red]❌ LLM недоступна. Проверьте настройки провайдера (OpenRouter API ключ или Ollama).[/red]"
                    )
                else:
                    if versus_prompt:
                        console.print(f"[bold cyan]Ты:[/bold cyan] {user_input}")
                        increment_versus_attempts()
                    console.print(
                        f"[bold green]БОТ ({current_mode.value}):[/bold green] ", end=""
                    )
                    for chunk in llm.stream(f"{system_prompt}\n\nВопрос: {user_input}"):
                        chunk_text = (
                            str(chunk.content)
                            if hasattr(chunk, "content")
                            else str(chunk)
                        )
                        full_response += chunk_text
                        console.print(chunk_text, end="")
                    console.print()

        except (ValueError, RuntimeError, KeyError, OSError) as e:
            console.print(f"[red]Ошибка: {e}[/red]")

        if full_response:
            save_message(conn, "user", user_input, current_mode.value)
            save_message(conn, "assistant", full_response, current_mode.value)
            update_stats(conn, 1)
            # Track context budget usage
            budget_manager.record_usage(len(user_input) + len(full_response))
            # Auto-summarize periodically (every 20 messages)
            try:
                from handlers.summarize import check_auto_summarize

                check_auto_summarize(conn)
            except ImportError:
                pass
            # Periodic memory cleanup (every 50 messages)
            msg_count = getattr(state, "_msg_count_since_summary", 0)
            if msg_count > 0 and msg_count % 50 == 0:
                cleanup_old_messages(conn, keep_last=500)
    # Save context budget on exit
    try:
        setattr(get_state(), "context_budget", budget_manager.to_dict())
        get_state().save_to_file()
    except Exception:
        pass


if __name__ == "__main__":
    atexit.register(_response_cache._save)
    atexit.register(_save_session_summary)
    main()
