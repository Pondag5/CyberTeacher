# AGENTS.md - Руководство по разработке CyberTeacher

## Описание проекта

CyberTeacher — это CLI-приложение для обучения кибербезопасности со встроенным LLM-учителем. Проект написан на Python и использует:
- **LLM**: Ollama/VL Studio (модели qwen2.5)
- **RAG**: Chroma + sentence-transformers
- **UI**: Rich (форматирование CLI)
- **База данных**: SQLite
- **Тестирование**: unittest

---

## Запуск приложения

```bash
# Главная точка входа
python main.py
```

---

## Тестирование

### Запустить все тесты
```bash
python -m unittest discover -s tests -v
```

### Запустить один тест
```bash
python -m unittest tests.tools-tests.TestTools.test_decode_base64
```

### Запустить конкретный файл тестов
```bash
python -m unittest tests.tools-tests -v
```

---

## Руководство по стилю кода

### Общие принципы

- Пишите код на **английском** для логики и функциональности
- Пишите **документацию и комментарии на русском** (язык проекта)
- Функции должны быть сфокусированы и иметь одну цель (желательно до 80 строк)
- Используйте ранний возврат для уменьшения вложенности

### Соглашения об именовании

| Элемент | Соглашение | Пример |
|---------|------------|--------|
| Функции | snake_case | `get_learning_context()` |
| Переменные | snake_case | `current_mode`, `user_input` |
| Классы | PascalCase | `LazyLoader`, `TeacherPersona` |
| Константы | UPPER_SNAKE | `MODEL_NAME`, `MAX_WORKERS` |
| Файлы-модули | snake_case | `handlers.py`, `tools.py` |

### Аннотации типов

**Всегда используйте аннотации типов в сигнатурах функций:**

```python
# Хорошо
def decode_text(data: str, format_type: str) -> tuple[bool, str]:
def handle_command(action: str, vectordb: Any, conn: Any, ...) -> Tuple[bool, Optional[Any], Optional[Any], bool]:

# Плохо
def decode_text(data, format_type):
```

**Часто используемые импорты типов:**
```python
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
```

### Организация импортов

Импорты располагаются в следующем порядке с пустыми строками между группами:

```python
# 1. Стандартная библиотека
import os
import sys
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

# 2. Сторонние пакеты
from rich.console import Console
from rich.panel import Panel

# 3. Локальные модули приложения
from config import LazyLoader, KNOWLEDGE_DIR
from state import get_state
from ui import console, print_banner
```

### Docstrings

Используйте Google-стиль для docstrings:

```python
def get_learning_context() -> Dict[str, Any]:
    """Получить контекст обучения через state.
    
    Returns:
        Dict с ключами current_course, current_topic, current_lab, action.
    """
    return get_state().get_learning_context()
```

### Обработка ошибок

```python
# Хорошо - конкретная обработка исключений
try:
    from news_fetcher import NewsFetcher
    nf = NewsFetcher()
    nf.fetch_all()
    _news_cache = nf.get_formatted_news()
except Exception as e:
    _news_cache = ""

# Хорошо - грамотная деградация
def fetch_and_summarize(topic: str, LLM: Any) -> Optional[Dict[str, Any]]:
    return None  # Возвращаем None вместо генерации исключения
```

### Логирование

Используйте настроенный логгер:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Загрузка модели LLM...")
logger.warning(f"Путь {path} не существует.")
logger.error(f"Ошибка: {e}")
```

### Dataclasses и Enums

Используйте для структурированных данных:

```python
from dataclasses import dataclass
from enum import Enum

class Mode(Enum):
    TEACHER = "teacher"
    CTF = "ctf"
    EXPERT = "expert"
    CODE_REVIEW = "review"

@dataclass
class Task:
    id: int
    question: str
    answer: str
    hint: str
    category: str
    difficulty: str
```

### Паттерн ленивой загрузки

Для дорогих импортов (LLM, эмбеддинги) используйте паттерн LazyLoader:

```python
def get_llm():
    return LazyLoader.get_llm()

# Использование - загружается только при первом вызове
llm = get_llm()
```

### Использование Rich UI

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# Панели
console.print(Panel(text, title="ЗАГОЛОВОК", border_style="cyan"))

# Цветной вывод
console.print("[red]Ошибка![/red]")
console.print(f"[bold]Ты:[/bold] {user_input}")
```

### Форматирование строк

Используйте f-строки для простых случаев, Panel для структурированного вывода:

```python
# Простой случай
name = "User"
console.print(f"Привет, {name}!")

# Панель с несколькими строками
console.print(Panel(f"""
🔴 СТАТУС: {lab_info['name']}
📊 Состояние: {lab_info['status']}
""", title="ПРОВЕРКА", border_style="cyan"))
```

---

## Структура проекта

```
CyberTeacher/
├── main.py           # Главный цикл, точка входа
├── handlers.py       # Обработка команд
├── state.py          # Глобальное управление состоянием
├── config.py         # Конфигурация, LazyLoader
├── ui.py             # Компоненты UI (Rich)
├── knowledge.py      # RAG база знаний
├── memory.py         # Операции с SQLite БД
├── pedagogy.py       # Персона учителя
├── courses.py        # Управление курсами
├── practice.py       # Docker лаборатории
├── story_mode.py    # Игровой режим
├── tools.py          # Утилиты (кодирование/декодирование)
├── question_generation.py
├── code_review.py
├── news_fetcher.py
├── generators.py
├── terminal_log.py
├── tests/
│   └── tools-tests.py
├── memory/           # SQLite БД, логи
├── embeddings/       # Chroma DB
├── knowledge_base/  # PDF файлы для RAG
└── docs/            # Документация
```

---

## Ключевые паттерны

### Обработка команд
Команды начинаются с `/` и обрабатываются в `handlers.py`:
```python
def handle_command(action: str, ...):
    if action.startswith('/'):
        return handle_commands(action[1:], ...)
```

### Управление состоянием
Используйте синглтон `get_state()`:
```python
from state import get_state
state = get_state()
state.set_course(course_id)
```

### Операции с базой данных
Все операции с БД через `memory.py`:
```python
from memory import init_db, save_message, get_chat_history
conn = init_db()
save_message(conn, "user", user_input, mode.value)
```

---

## Частые задачи

### Добавление новой команды
1. Добавьте функцию-обработчик в `handlers.py`
2. Зарегистрируйте в `handle_commands()` или `handle_extended_commands()`
3. Добавьте в справку в `ui.py`

### Добавление новой темы квиза
Отредактируйте `question_generation.py` — реализуйте вопросы по конкретной теме.

### Изменение персоны учителя
Отредактируйте `pedagogy.py` — содержит TeacherPersona и промпты.

---

## Зависимости

Основные зависимости (см. `requirements.txt`):
- sqlalchemy
- langchain (для LLM)
- langchain-openai (совместимость с VL Studio)
- sentence-transformers (эмбеддинги)
- chromadb (векторное хранилище)
- rich (CLI UI)

Установка: `pip install -r requirements.txt`
