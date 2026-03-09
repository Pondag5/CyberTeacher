import os
import sqlite3
from enum import Enum
from dataclasses import dataclass
from handlers import handle_commands

# === МОДУЛИ ===
from config import (
    LazyLoader, KNOWLEDGE_DIR, PERSIST_DIR, DB_FILE,
    METADATA_FILE, MAX_WORKERS, CHUNK_SIZE, CHUNK_OVERLAP,
    SOCRATIC_ENABLED, THINKING_ENABLED
)
from state import get_state

# Функции для lazy loading
def get_llm():
    return LazyLoader.get_llm()

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
            from news_fetcher import NewsFetcher
            nf = NewsFetcher()
            nf.fetch_all()
            _news_cache = nf.get_formatted_news()
        except Exception as e:
            _news_cache = ""
    return _news_cache

def get_embeddings():
    return LazyLoader.get_embeddings()

from ui import console, print_banner, show_menu, show_help, print_response, print_thinking, print_panel, print_streaming_response, Panel
from ui import Mode

from knowledge import load_knowledge_base, get_relevant_docs
from memory import init_db, save_message, get_chat_history, update_stats, get_stats, get_weak_topics
from generators import generate_task, generate_quiz
from code_review import code_review_function as code_review
from terminal_log import get_terminal_log, log_command, init_terminal_log
from pedagogy import TeacherPersona, ThinkingVisualizer

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
import os
import random
import json

PROMPT_FILE = "./config/teacher_prompt.txt"
STORIES_FILE = "./config/stories.json"

def load_teacher_prompt() -> str:
    """Загрузить промпт учителя из файла и добавить случайную байку"""
    persona = ""
    if os.path.exists(PROMPT_FILE):
        try:
            with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
                persona = f.read()
        except:
            persona = "Ты - хакер-ветеран из 90-х, учитель кибербезопасности."
    else:
        persona = "Ты - хакер-ветеран из 90-х, учитель кибербезопасности."
    
    # Добавляем случайную байку из файла
    story = ""
    if os.path.exists(STORIES_FILE):
        try:
            with open(STORIES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stories = data.get("stories", [])
                if stories:
                    story = random.choice(stories)
        except:
            pass
    
    if story:
        return f"{persona}\n\nВОТ ТВОЯ ИСТОРИЯ ДЛЯ ЭТОГО ОТВЕТА (используй её если уместно): {story}"
    return persona

def get_mode_prompt(mode: Mode, context_str: str, docs_context: str, study_context: str = "") -> str:
    # Генерируем динамический промпт со случайной байкой при каждом запросе
    dynamic_prompt = load_teacher_prompt()
    context = f"""{dynamic_prompt}

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
    
    # Инициализируем лог терминала
    init_terminal_log()
    
    conn = init_db()
    vectordb = load_knowledge_base()

    # === АДАПТИВНЫЙ СОВЕТ ПРИ СТАРТЕ ===
    weak_topics = get_weak_topics(conn)
    if weak_topics:
        rec = weak_topics[0] # Берем самую слабую
        console.print(f"[bold yellow]Совет:[/bold yellow] Твоя слабая тема - [cyan]{rec['topic']}[/cyan] (Успех: {rec['rate']}%). Попробуй /quiz!")
    
    current_mode = Mode.TEACHER
    student_level = None

    show_help()
    show_menu()
    
    # Показываем текущую статистику
    stats = get_stats(conn)
    console.print(f"[bold]Режим:[/bold] {current_mode.value} | [bold]Очки:[/bold] {stats['points']}")

    while True:
        try:
            user_input = console.input(f"\n[bold]Ты:[/bold] ")
        except KeyboardInterrupt:
            console.print("\n[yellow]Пока![/yellow]")
            break

        if not user_input.strip():
            continue
        user_input = user_input.strip()
        
        # Автозапись ввода в терминал
        try:
            from terminal_log import log_command
            log_command(user_input, is_input=True)
        except:
            pass

        # Обработка команд
        continue_loop, new_mode, new_level, action_taken = handle_commands(
            user_input, conn, get_llm, current_mode, student_level
        )

        if action_taken:
            if not continue_loop:
                break
            current_mode = new_mode if new_mode else current_mode
            student_level = new_level if new_level else student_level
            # Обновляем отображение режима
            mode_display = current_mode.value if current_mode else "Учитель"
            console.print(f"\n[bold]Режим:[/bold] {mode_display}")
            continue

        # Если не команда - отправляем LLM (вопрос)
        history = get_chat_history(conn)
        context_str = "\n".join([f"{m['role']}: {m['content'][:200]}..." for m in history])

        # === RAG + ИСТОЧНИКИ ===
        relevant_docs = get_relevant_docs(vectordb, user_input) if vectordb else []
        docs_context = ""
        sources = set()
        if relevant_docs:
            docs_context = "\n📖 Контекст:\n" + "\n".join([f"- {d.page_content}" for d in relevant_docs])
            for doc in relevant_docs:
                src = doc.metadata.get('source', None)
                if src:
                    sources.add(os.path.basename(src))

        # === КОНТЕКСТ ОБУЧЕНИЯ + КОНТЕЙНЕРЫ ===
        learning_ctx = get_learning_context()
        container_info = ""
        terminal_info = ""
        kb_info = ""
        weak_info = ""
        
        try:
            # Данные о базе знаний
            from knowledge import get_knowledge_status
            status = get_knowledge_status()
            kb_info = f"В базе знаний: {status.get('files_in_db', 0)} документов."

            # Данные о слабых темах
            weak_topics = get_weak_topics(conn)
            if weak_topics:
                topics_str = ", ".join([f"{t['topic']} ({t['rate']}% успеха)" for t in weak_topics])
                weak_info = f"Слабые темы ученика: {topics_str}."
            
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
- Курс: {learning_ctx.get('current_course', 'не выбран')}
- Тема: {learning_ctx.get('current_topic', 'не выбрана')}
- Лаба: {learning_ctx.get('current_lab', 'не запущена')}

{kb_info}
{weak_info}
{container_info}
{terminal_info}
"""
        else:
            study_context = f"=== КОНТЕКСТ: Ученик ===\n{kb_info}\n{weak_info}\n{container_info}\n{terminal_info}"
        
        system_prompt = get_mode_prompt(current_mode, context_str, docs_context, study_context)

        # Мысли (только для CTF)
        if THINKING_ENABLED and current_mode == Mode.CTF:
            thinking = ThinkingVisualizer.generate_thinking(context_str, user_input, "socratic")
            print_thinking(thinking)

        # === STREAMING ===
        full_response = ""
        try:
            llm = get_llm()
            console.print(f"[bold green]БОТ ({current_mode.value}):[/bold green] ", end="")
            for chunk in llm.stream(f"{system_prompt}\n\nВопрос: {user_input}"):
                # VL Studio через ChatOpenAI возвращает AIMessageChunk
                chunk_text = str(chunk.content) if hasattr(chunk, 'content') else str(chunk)
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
    main()
