from ui import Prompt, console, print_panel
from pedagogy import MermaidGenerator
from config import LazyLoader
from knowledge import get_relevant_docs
import random
import json
import re
from datetime import datetime

LLM = LazyLoader.get_llm

def extract_json_block(text: str) -> dict:
    """Извлечь JSON из текста"""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {}

ALLOWED_TOPICS = ["sql", "xss", "network", "crypto", "linux", "web", "reverse", "osint", "pwn"]

class Task:
    def __init__(self, id, question, answer, hint, category, difficulty):
        self.id = id
        self.question = question
        self.answer = answer
        self.hint = hint
        self.category = category
        self.difficulty = difficulty

def generate_task(vectordb, category=None):
    """Генерация практической задачи"""
    categories = {
        "network": "Сетевая безопасность (Network Security)",
        "web": "Веб-безопасность (Web Security)",
        "crypto": "Криптография (Cryptography)",
        "osint": "OSINT",
        "reverse": "Reverse Engineering"
    }

    if category is None:
        category = random.choice(list(categories.keys()))

    topic_name = categories.get(category, category)
    relevant_docs = get_relevant_docs(vectordb, f"{topic_name} практическая задача", k=3)
    docs_context = "\n\n📖 Контекст:\n" + "\n".join([f"- {d.page_content[:500]}..." for d in relevant_docs]) if relevant_docs else ""

    prompt = f"""Создай практическую задачу по кибербезопасности.
Тема: {topic_name}

Примеры:
1. Log Analysis: Дай фрагмент лога Apache с попыткой SQL-инъекции.
2. Crypto: Зашифруй текст простым шифром (ЦезарьBase64) и попроси расшифровать.
3. Scripting: Попроси написать однострочник на Bash для поиска файлов.

Верни JSON:
{{
    "question": "Текст задачи и данные (например, лог или шифр)",
    "answer": "Правильный ответ",
    "hint": "Подсказка",
    "category": "{category}",
    "difficulty": "easy|medium|hard"
}}
{docs_context}

Только JSON."""  # двойные фигурные скобки используются для экранирования в f-строке

    try:
        llm = LazyLoader.get_llm()
        response = llm.invoke(prompt)
        json_block = extract_json_block(response)
        if isinstance(json_block, dict):
            return Task(
                id=int(datetime.now().timestamp()),
                question=json_block.get("question", ""),
                answer=json_block.get("answer", ""),
                hint=json_block.get("hint", ""),
                category=json_block.get("category", category),
                difficulty=json_block.get("difficulty", "medium")
            )
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")

    return None

def generate_quiz(vectordb, topic=None, count=5):
    """Генерация квиза с фильтрацией тем"""

    # Если тема не указана или слишком общая, выбираем случайную из разрешенных
    if not topic or topic.lower() in ["all", "general", "все", "общее"]:
        topic = random.choice(ALLOWED_TOPICS)
        console.print(f"[dim]Выбрана тема: {topic}[dim]")

    relevant_docs = get_relevant_docs(vectordb, topic, k=3)
    docs_context = "\n\n📖 Контекст:\n" + "\n".join([d.page_content[:300] for d in relevant_docs]) if relevant_docs else ""

    prompt = f"""Ты — эксперт по кибербезопасности. Создай квиз из {count} вопросов.
Тема строго: {topic}.

Примеры:
1. Вопрос: Что такое XSS?
   Опции: A) SQL-инъекция, B) Кросс-сайт scripting, C) ДDoS атака, D) Фишинг
   Ответ: B

Верни JSON массив с вопросами и вариантами ответов:
[
    {{
        "question": "Вопрос?",
        "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
        "correct": "A",
        "explanation": "Краткое объяснение"
    }}
]

{docs_context}

Только JSON."""  # двойные фигурные скобки экранированы

    try:
        response = LLM.invoke(prompt)
        json_block = extract_json_block(response)
        if isinstance(json_block, list):
            return json_block
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[red]")

    return []

def generate_mermaid(vectordb):
    """Генерация Mermaid схемы"""
    from ui import Prompt

    console.print("[cyan]🗺️ Генерация схемы[cyan]")
    topic = Prompt.ask("О чём?", default="аутентификация")

    relevant_docs = get_relevant_docs(vectordb, topic, k=3)

    prompt = f"""Создай структуру для Mermaid на тему: {topic}

JSON:
{{
    "type": "mindmap|flowchart",
    "root": "Главное",
    "nodes": ["А", "Б"],
    "steps": ["Шаг 1"]
}}

Контекст: {' '.join([d.page_content[:200] for d in relevant_docs]) if relevant_docs else '-'}

Только JSON."""  # экранирование фигурных скобок в f-строке
    try:
        response = LLM.invoke(prompt)
        json_block = extract_json_block(response)
        if isinstance(json_block, dict):
            from pedagogy import MermaidGenerator

            data = json_block
            diagram_type = data.get("type", "flowchart")

            if diagram_type == "mindmap":
                diagram = MermaidGenerator.generate_concept_map(
                    data.get("root", topic),
                    data.get("nodes", [])
                )
            else:
                diagram = MermaidGenerator.generate_flowchart(
                    data.get("steps", [topic])[:6]
                )

            print_panel(
                f"[bold]{topic}[bold]\n\n{diagram}",
                title="🗺️ MEREAD",
                border="cyan"
            )
            console.print("\n💡 https:mermaid.live")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[red]")

def generate_open_quiz(vectordb, topic=None):
    """Генерация вопросов со свободным ответом"""
    topic = topic or "кибербезопасность"
    relevant_docs = get_relevant_docs(vectordb, topic, k=3)
    docs_context = "\n".join([d.page_content[:300] for d in relevant_docs]) if relevant_docs else ""

    prompt = f"""Ты — эксперт по кибербезопасности. Сгенерируй вопрос со свободным ответом на тему {topic}.

Пример:
Вопрос: Какие методы шифрования используются для защиты данных в сеть?
Ответ: AES, RSA, TLS

Только JSON:
{{
    "question": "Вопрос?",
    "answer": "Ответ"
}}

{docs_context}

Только JSON."""  # экранирование фигурных скобок
    try:
        response = LLM.invoke(prompt)
        json_block = extract_json_block(response)
        if isinstance(json_block, dict):
            return json_block
    except Exception as e:
        console.print(f"[red]Ошибка генерации: {e}[red]")

    return None

def check_open_answer(question, user_answer, key_points):
    """Проверка ответа через LLM на соответствие ключевым моментам"""
    prompt = f"""Ты — экзаменатор.
Вопрос: {question}
Ответ ученика: {user_answer}
Ключевые моменты, которые должны быть в ответе: {key_points}

Оцени ответ по шкале от 0 до 10.
Напиши краткий отзыв (1 предложение): что упущено или что хорошо.
Верни JSON:
{{
    "score": 8,
    "feedback": "Ты верно описал процесс, но забыл упомянуть шифрование."
}}

Только JSON."""  # экранирование фигурных скобок
    try:
        response = LLM.invoke(prompt)
        json_block = extract_json_block(response)
        if isinstance(json_block, dict):
            return json_block
    except Exception as e:
        pass
    return {"score": 0, "feedback": "Не удалось проверить ответ."}
