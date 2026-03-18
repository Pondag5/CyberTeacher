#!/usr/bin/env python3
import json
import os
import random
import sys

# Force UTF-8 on Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["PYTHONUTF8"] = "1"

# Настройка консоли для корректного вывода UTF-8 (эмодзи, спецсимволы)
from utils.console_encoding import setup_utf8_console

setup_utf8_console()

import atexit
import hashlib
import logging

# ===== НАСТРОЙКА ЛОГИРОВАНИЯ ЧТОБЫ УБРАТЬ ШУМ =====
import os
import sqlite3
from dataclasses import dataclass
from enum import Enum

from config import NUMERIC_MENU
from handlers.core import _response_cache, handle_commands
from memory import cache_response, cleanup_expired_cache, get_cached_response

# Отключаем прогресс-бары и лишние логи от библиотек
os.environ["TQDM_DISABLE"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

# Подавляем логи от сторонних библиотек (huggingface, transformers, httpx и т.д.)
_noisy_prefixes = [
    "sentence_transformers",
    "transformers",
    "huggingface_hub",
    "httpx",
    "httpcore",
    "urllib3",
    "filelock",
    "torch",
]
for _p in _noisy_prefixes:
    logging.getLogger(_p).setLevel(logging.WARNING)

# Также подавляем специфические предупреждения transformers о непредвиденных весах
try:
    from transformers import logging as hf_logging

    hf_logging.set_verbosity_error()
except Exception:
    pass  # Если transformers не установлен, игнорируем

# Конфигурация корневого логгера (our own logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ===== НАСТРОЙКА ЛОГИРОВАНИЯ ЧТОБЫ УБРАТЬ ШУМ =====
import logging

# Подавляем INFO-логи от сторонних библиотек (huggingface, transformers, httpx и т.д.)
_noisy_loggers = [
    "sentence_transformers",
    "transformers",
    "huggingface_hub",
    "httpx",
    "httpcore",
    "urllib3",
    "filelock",
    "torch",
    "tqdm",
]
for _ln in _noisy_loggers:
    logging.getLogger(_ln).setLevel(logging.WARNING)


class CachedLLM:
    """Обёртка для LLM с кэшированием ответов в SQLite"""

    def __init__(self, llm, conn):
        self.llm = llm
        self.conn = conn

    def invoke(self, prompt):
        import hashlib

        # Хешируем запрос + модель (разные модели — разные ответы)
        model_id = getattr(self.llm, "model", "default")
        query_string = f"{prompt}|{model_id}"
        query_hash = hashlib.sha256(query_string.encode()).hexdigest()

        # Проверяем кэш
        cached = get_cached_response(self.conn, query_hash)
        if cached:
            # Возвращаем объект с атрибутом content для совместимости
            class CachedResponse:
                def __init__(self, content):
                    self.content = content

            return CachedResponse(cached)

        # Кэша нет — вызываем реальный LLM
        response = self.llm.invoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)

        # Сохраняем в кэш с TTL 1 день (актуальные данные)
        cache_response(self.conn, query_hash, text, ttl_seconds=86400)

    def stream(self, prompt):
        """Стриминг с кэшированием полного ответа в SQLite."""
        model_id = getattr(self.llm, "model", "default")
        query_string = f"{prompt}|{model_id}"
        query_hash = hashlib.sha256(query_string.encode()).hexdigest()

        cached = get_cached_response(self.conn, query_hash)
        if cached:
            # Возвращаем кэшированный ответ как один чанк
            yield cached
            return

        # Кэша нет — стримим от реального LLM и накапливаем
        full_chunks = []
        for chunk in self.llm.stream(prompt):
            full_chunks.append(chunk)
            yield chunk

        # После завершения стрима собираем полный текст и кэшируем
        full_text = "".join(
            str(ch.content) if hasattr(ch, "content") else str(ch) for ch in full_chunks
        )
        if full_text:
            cache_response(self.conn, query_hash, full_text, ttl_seconds=86400)


# Конфигурация корневого логгера (our own logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# === МОДУЛИ ===
from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DB_FILE,
    KNOWLEDGE_DIR,
    MAX_WORKERS,
    METADATA_FILE,
    PERSIST_DIR,
    SOCRATIC_ENABLED,
    THINKING_ENABLED,
    LazyLoader,
)
from state import get_state


# Функции для lazy loading
def get_llm():
    return LazyLoader.get_llm()


def get_cached_llm(conn):
    llm = get_llm()
    if llm is None:
        return None
    return CachedLLM(llm, conn)


# Новости (lazy)
_news_cache = None


def set_learning_context(course=None, topic=None, lab=None, action=None):
    """Установить контекст обучения через state"""
    state = get_state()
    state.set_learning_context(course, topic, lab, action)


def get_learning_context():
    """Получить контекст обучения через state"""
    return get_state().get_learning_context()


def get_news_context():
    global _news_cache
    if _news_cache is None:
        try:
            try:
                from news_fetcher import NewsFetcher

                nf = NewsFetcher()
                nf.fetch_all()
                _news_cache = nf.get_formatted_news()
            except ImportError:
                _news_cache = ""
        except Exception:
            _news_cache = ""
    return _news_cache


def get_embeddings():
    return LazyLoader.get_embeddings()


from code_review import code_review_function as code_review
from generators import generate_quiz, generate_task
from knowledge import get_relevant_docs, load_knowledge_base
from memory import (
    get_chat_history,
    get_stats,
    get_weak_topics,
    init_db,
    save_message,
    update_stats,
)
from pedagogy import TeacherPersona, ThinkingVisualizer
from terminal_log import get_terminal_log, init_terminal_log, log_command
from ui import (
    Mode,
    Panel,
    console,
    print_banner,
    print_panel,
    print_response,
    print_streaming_response,
    print_thinking,
    show_help,
    show_menu,
)


def is_cybersecurity_related(query: str) -> bool:
    return True  # Всегда пропускаем


# === КОНСТАНТЫ ===
MODEL_NAME = "qwen2.5:3b"


@dataclass
class Task:
    id: int
    question: str
    answer: str
    hint: str
    category: str
    difficulty: str


# === ПРОМПТЫ ===
PROMPT_FILE = "./teacher_prompt.txt"
STORIES_FILE = "./stories.json"


def load_teacher_prompt() -> str:
    """Загрузить промпт учителя из файла и добавить случайную байку"""
    persona = ""
    if os.path.exists(PROMPT_FILE):
        try:
            with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                persona = f.read()
        except:
            persona = "Ты - хакер-ветеран из 90-х, учитель кибербезопасности."
    else:
        persona = "Ты - хакер-ветеран из 90-х, учитель кибербезопасности."

    # Добавляем случайную байку из файла
    story = ""
    if os.path.exists(STORIES_FILE):
        try:
            with open(STORIES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                stories = data.get("stories", [])
                if stories:
                    story = random.choice(stories)
        except:
            pass

    if story:
        return f"{persona}\n\nВОТ ТВОЯ ИСТОРИЯ ДЛЯ ЭТОГО ОТВЕТА (используй её если уместно): {story}"
    return persona


def get_mode_prompt(
    mode: Mode, context_str: str, docs_context: str, study_context: str = ""
) -> str:
    """Строит промпт на основе выбранной персоны из state."""
    state = get_state()
    persona = state.get_persona()

    # Загружаем промпты из JSON
    prompts_path = os.path.join("config", "teacher_prompts.json")
    try:
        with open(prompts_path, "r", encoding="utf-8") as f:
            prompts_data = json.load(f)
    except Exception as e:
        console.print(
            f"[yellow]⚠️ Не удалось загрузить teacher_prompts.json: {e}[/yellow]"
        )
        prompts_data = {}

    base_prompt = prompts_data.get("system_prompt", "Ты - учитель кибербезопасности.")

    # Получаем инструкции для текущей персоны
    personas = prompts_data.get("personas", {})
    persona_instructions = personas.get(persona, {}).get("instructions", [])

    if persona_instructions:
        base_prompt += "\n\nИнструкции для режима:\n" + "\n".join(
            [f"- {p}" for p in persona_instructions]
        )

    # Добавляем контекст
    context = f"""{base_prompt}

КОНТЕКСТ УЧЕНИКА:
{study_context}

ДАННЫЕ ИЗ БАЗЫ ЗНАНИЙ:
{docs_context}
"""
    return context


# === ГЛАВНЫЙ ЦИКЛ ===
def main():
    print_banner()
    console.print("[bold green]Loading...[/bold green]\n")

    # Загружаем сохранённое состояние
    state = get_state()
    state.load_from_file()

    # Инициализируем лог терминала
    init_terminal_log()

    # === PROMPT_TOOLKIT (история команд) ===
    session = None
    have_prompt_toolkit = False
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import FileHistory

        have_prompt_toolkit = True
        history_path = os.path.join(".", "memory", "command_history.txt")
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        session = PromptSession(history=FileHistory(history_path))
    except ImportError:
        have_prompt_toolkit = False
    except Exception as e:
        console.print(
            f"[yellow]⚠️ Не удалось инициализировать prompt_toolkit: {e}[/yellow]"
        )
        have_prompt_toolkit = False

    conn = init_db()
    cleanup_expired_cache(conn)  # Очистка просроченных записей кэша
    vectordb = load_knowledge_base()

    # === АДАПТИВНЫЙ СОВЕТ ПРИ СТАРТЕ ===
    weak_topics = get_state().get_weak_topics(threshold=70.0)
    if weak_topics:
        rec = weak_topics[0]  # Берем самую слабую
        console.print(
            f"[bold yellow]Совет:[/bold yellow] Твоя слабая тема - [cyan]{rec['topic']}[/cyan] (Успешность: {rec['success_rate']:.1f}%). Попробуй /quiz!"
        )

    # === SPACED REPETITION НАПОМИНАНИЕ ===
    due_reviews = get_state().get_due_reviews()
    if due_reviews:
        console.print(
            f"[bold magenta]⏰ Напоминание:[/bold magenta] У тебя {len(due_reviews)} тем готовы для повторения (Spaced Repetition). Введи /repeat или 42 чтобы начать."
        )

    current_mode = Mode.TEACHER

    show_help()
    show_menu()

    # Показываем текущую статистику
    stats = get_stats(conn)
    console.print(
        f"[bold]Режим:[/bold] {current_mode.value} | [bold]Очки:[/bold] {stats['points']}"
    )

    while True:
        try:
            if have_prompt_toolkit and session:
                user_input = session.prompt("\nТы: ").strip()
            else:
                user_input = console.input(f"\n[bold]Ты:[/bold] ").strip()
        except KeyboardInterrupt:
            console.print("\n[yellow]Пока![/yellow]")
            break

        if not user_input.strip():
            continue
        user_input = user_input.strip()

        # Валидация длины ввода (S-02)
        if len(user_input) > 2000:
            console.print("[red]❌ Слишком длинный ввод (максимум 2000 символов)[/red]")
            continue

        # Отмечаем отправку сообщения в state (для статистики)
        try:
            get_state().send_message()
        except Exception:
            pass

        # Автозапись ввода в терминал
        try:
            from terminal_log import log_command

            log_command(user_input, is_input=True)
        except Exception:  # ✅ Более-specific исключение
            pass

        # Нормализуем ввод: если цифра -> команда, иначе убираем /
        if user_input.isdigit() and user_input in NUMERIC_MENU:
            action = NUMERIC_MENU[user_input]
        else:
            action = user_input[1:] if user_input.startswith("/") else user_input

        continue_loop, new_mode, _, action_taken = handle_commands(
            action, conn, lambda: get_cached_llm(conn)
        )

        if action_taken:
            if not continue_loop:
                break
            if new_mode:
                current_mode = new_mode
                # Сохраняем персону в state
                get_state().set_persona(
                    current_mode.value
                    if hasattr(current_mode, "value")
                    else str(current_mode)
                )
            # Обновляем отображение режима
            mode_display = current_mode.value if current_mode else "Учитель"
            console.print(f"\n[bold]Режим:[/bold] {mode_display}")
            continue

        # Если не команда - отправляем LLM (вопрос)
        history = get_chat_history(conn)
        context_str = "\n".join(
            [f"{m['role']}: {m['content'][:200]}..." for m in history]
        )

        # === RAG + ИСТОЧНИКИ ===
        relevant_docs = get_relevant_docs(vectordb, user_input) if vectordb else []
        docs_context = ""
        sources = set()
        if relevant_docs:
            docs_context = "\n📖 Контекст:\n" + "\n".join(
                [f"- {d.page_content}" for d in relevant_docs]
            )
            for doc in relevant_docs:
                src = doc.metadata.get("source", None)
                if src:
                    sources.add(os.path.basename(src))

        # === КОНТЕКСТ ОБУЧЕНИЯ + КОНТЕЙНЕРЫ ===
        learning_ctx = get_learning_context()
        container_info = ""
        terminal_info = ""
        kb_info = ""
        weak_info = ""
        risk_info = ""

        try:
            # Данные о базе знаний
            from knowledge import get_knowledge_status

            status = get_knowledge_status()
            kb_info = f"В базе знаний: {status.get('files_in_db', 0)} документов."

            # Данные о слабых темах
            weak_topics = get_weak_topics(conn)
            if weak_topics:
                topics_str = ", ".join(
                    [f"{t['topic']} ({t['rate']}% успеха)" for t in weak_topics]
                )
                weak_info = f"Слабые темы ученика: {topics_str}."

            # ДОБАВЛЕНО: Информация об уровне риска для CTF/Story режимов
            state = get_state()
            if state.get_persona() in ("ctf", "story"):
                risk_status = state.get_risk_status()
                risk_info = f"⚠️ Уровень риска (trace/compromise): {risk_status} ({state.risk_level}/100).\n"

            from practice import get_all_running_labs, get_container_logs
            from terminal_log import get_terminal_log

            terminal_log = get_terminal_log(last_n=10)
            if terminal_log and terminal_log != "Лог пуст":
                terminal_info = f"\n--- ТЕРМИНАЛ УЧЕНИКА ---\n{terminal_log}\n"

            running_labs = get_all_running_labs()
            if running_labs:
                container_info = "\n--- ЗАПУЩЕННЫЕ КОНТЕЙНЕРЫ ---\n"
                for lab_key, lab_info in running_labs.items():
                    container_info += f"  - {lab_info['name']}: {lab_info['status']}\n"
                    web_name = f"{lab_key}-web"
                    logs = get_container_logs(web_name, lines=10)
                    if logs and logs != "Логов нет":
                        container_info += f"    Логи: {logs[:200]}...\n"
        except Exception as e:
            container_info = f"\n(Контейнеры недоступны: {e})"

        if learning_ctx["current_course"] or learning_ctx["current_lab"]:
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

        # Мысли (только для CTF)
        if THINKING_ENABLED and current_mode == Mode.CTF:
            thinking = ThinkingVisualizer.generate_thinking(
                context_str, user_input, "socratic"
            )
            print_thinking(thinking)

        full_response = ""
        try:
            llm = get_cached_llm(conn)
            if llm is None:
                console.print(
                    "[red]❌ LLM недоступна. Проверьте настройки провайдера (OpenRouter API ключ или Ollama).[/red]"
                )
            else:
                console.print(
                    f"[bold green]БОТ ({current_mode.value}):[/bold green] ", end=""
                )
                for chunk in llm.stream(f"{system_prompt}\n\nВопрос: {user_input}"):
                    chunk_text = (
                        str(chunk.content) if hasattr(chunk, "content") else str(chunk)
                    )
                    full_response += chunk_text
                    console.print(chunk_text, end="")
                console.print()
        except Exception as e:
            console.print(f"[red]Ошибка: {e}[/red]")

        if full_response:
            save_message(conn, "user", user_input, current_mode.value)
            save_message(conn, "assistant", full_response, current_mode.value)
            update_stats(conn, 1)


if __name__ == "__main__":
    # Save cache and state on exit
    atexit.register(_response_cache._save)
    atexit.register(lambda: get_state().save_to_file())
    main()
