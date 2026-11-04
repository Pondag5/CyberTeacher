# ️ CyberTeacher: Полный План Рефакторинга и Аудит (v6.x → v7.0)

**Дата:** 2026-11-04  
**Статус:** Критический технический долг требует вмешательства  
**Цель:** Превратить проект из «гениального хаоса» в масштабируемую, поддерживаемую систему без потери уникальных фич.

---

## 📊 1.Executive Summary (Краткий вердикт)

Проект **CyberTeacher** обладает уникальным функционалом (Learning Memory, Киберпсихоз, Гибридный RAG), который ставит его выше 99% аналогов. Однако архитектурные решения («плоская» структура файлов, глобальное состояние, игнорирование ошибок импорта) создают огромный риск для будущего развития.

*   **Функционал:** ⭐⭐⭐⭐⭐ (5/5) — Блестяще.
*   **Архитектура:** ⭐⭐☆☆☆ (2/5) — Требует полной перестройки.
*   **Срочность действий:** 🔴 Высокая (до добавления новых фич).

---

## 🚨 2. Критические Проблемы (Что ломается прямо сейчас)

### Проблема №1: «Плоская свалка» файлов (Flat Directory Hell)
**Симптом:** В корне лежат 60+ `.py` файлов (`cyberpsychosis.py`, `atmosphere.py`, `behavior_profile.py` и т.д.).
**Последствие:** Невозможно найти код, сложно навигация, высокий риск конфликтов при слиянии веток.
**Решение:** Группировка по доменам в пакеты (`src/personas/`, `src/gamification/`).

### Проблема №2: «Тихий провал» (Silent Failure)
**Симптом:** Повсюду конструкции `try... except ImportError: pass`.
**Последствие:** Если зависимость отсутствует или файл удален, фича просто исчезает без предупреждения. Отладка невозможна.
**Решение:** Явная проверка зависимостей при старте с выводом четких ошибок.

### Проблема №3: Глобальный Синглтон (`get_state()`)
**Симптом:** Весь код дергает глобальную функцию для получения состояния.
**Последствие:** Тесты влияют друг на друга, невозможно масштабировать на многопользовательский режим, трудно отследить, кто изменил данные.
**Решение:** Постепенный переход к Dependency Injection (передача контекста явно).

### Проблема №4: Дублирование логики (DRY Violation)
**Симптом:** Логика сборки промпта дублируется в `main.py` (CLI) и `api_server.py` (PWA).
**Последствие:** Рассинхрон поведения бота в разных интерфейсах.
**Решение:** Выделение единого класса `PromptBuilder`.

---

## ️ 3. Пошаговый План Действий (Roadmap)

### Этап 1: Структурная реорганизация (Sprint 1)
*Цель: Навести порядок в файловой системе.*

#### Шаг 1.1: Создание новой структуры папок
Создай следующую структуру внутри корня (или перемести всё в `src/`):
```text
src/
── core/               # Базовые утилиты, конфиги, DI контейнер
│   ├── config.py
│   ├── state.py        # Определение классов состояния (без синглтона!)
│   ── startup_checks.py
├── personas/           # Вся логика поведения ИИ
│   ├── __init__.py
│   ├── cyberpsychosis.py
│   ├── personality.py
│   ├── behavior_profile.py
│   ├── context_awareness.py
│   ├── persona_router.py
│   └── atmosphere.py
├── prompt_engine/      # Сборка промптов
│   ├── __init__.py
│   └── builder.py
├── gamification/       # Игровые механики
│   ├── __init__.py
│   ├── world_state.py
│   ├── factions.py
│   ── achievements.py
├── api/                # FastAPI роуты и сервер
│   ├── main.py         # Точка входа API
│   └── routes/         # Вынесенные роуты
└── cli/                # CLI интерфейс
    └── main.py         # Точка входа CLI
```

#### Шаг 1.2: Миграция файлов
Перемести файлы из корня в соответствующие папки.
*Важно:* Не меняй логику внутри файлов, только пути импортов. Используй поиск/замену в IDE.

---

### Этап 2: Устранение «Тихого провала» (Sprint 1)
*Цель: Сделать ошибки видимыми.*

#### Шаг 2.1: Реализация `startup_checks.py`
Создай файл `src/core/startup_checks.py`:

```python
import logging
import sys
from typing import List, Tuple

logger = logging.getLogger(__name__)

OPTIONAL_MODULES = [
    ("faiss", "faiss-cpu", "pip install faiss-cpu"),
    ("chromadb", "chromadb", "pip install chromadb"),
    ("sentence_transformers", "sentence-transformers", "pip install sentence-transformers"),
    # Добавь сюда все опциональные модули
]

def check_dependencies() -> bool:
    """Проверяет наличие зависимостей. Возвращает False, если есть критические ошибки."""
    missing = []
    
    for module_name, package_name, install_cmd in OPTIONAL_MODULES:
        try:
            __import__(module_name)
            logger.info(f"✅ Found: {module_name}")
        except ImportError:
            logger.warning(f"⚠️ Missing: {module_name}. Install with: {install_cmd}")
            missing.append((module_name, install_cmd))

    if missing:
        print("\n" + "="*50)
        print("⚠️  WARNING: Some features will be disabled due to missing dependencies.")
        for name, cmd in missing:
            print(f"   - {name}: {cmd}")
        print("="*50 + "\n")
        # Можно добавить флаг --force-run, если нужно запустить несмотря на ошибки
        return False
    
    return True
```

#### Шаг 2.2: Интеграция в точки входа
В `main.py` (CLI) и `api/main.py` (API) в самом начале добавь:
```python
from src.core.startup_checks import check_dependencies

if not check_dependencies():
    # Опционально: выход с ошибкой или продолжение с предупреждением
    # sys.exit(1) 
    pass
```
Удали все блоки `try... except ImportError: pass` из основного кода.

---

### Этап 3: Централизация промптов (Sprint 2)
*Цель: Убрать дублирование логики сборки промпта.*

#### Шаг 3.1: Создание `PromptBuilder`
Создай файл `src/prompt_engine/builder.py`:

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class PromptContext:
    chat_history: str
    rag_context: str
    study_context: str
    persona_instructions: str
    atmosphere_hint: Optional[str] = None
    world_state_prompt: Optional[str] = None
    cyberpsychosis_prompt: Optional[str] = None

class PromptBuilder:
    def __init__(self, base_system_prompt: str):
        self.base_system_prompt = base_system_prompt

    def build(self, ctx: PromptContext) -> str:
        parts = [self.base_system_prompt]
        
        if ctx.persona_instructions:
            parts.append(f"\n\nИнструкции для режима:\n{ctx.persona_instructions}")
            
        if ctx.study_context:
            parts.append(f"\n\nКОНТЕКСТ УЧЕНИКА:\n{ctx.study_context}")
            
        if ctx.rag_context:
            parts.append(f"\n\nДАННЫЕ ИЗ БАЗЫ ЗНАНИЙ:\n{ctx.rag_context}")
            
        if ctx.chat_history:
            parts.append(f"\n\nИСТОРИЯ ДИАЛОГА:\n{ctx.chat_history}")

        # Опциональные блоки
        for hint in [ctx.atmosphere_hint, ctx.world_state_prompt, ctx.cyberpsychosis_prompt]:
            if hint:
                parts.append(f"\n\n{hint}")

        return "\n".join(parts)
```

#### Шаг 3.2: Рефакторинг `main.py` и `api_server.py`
Замени всю логику конкатенации строк (`system_prompt += ...`) на вызов `builder.build(context)`. Это гарантирует идентичное поведение в CLI и PWA.

---

### Этап 4: Работа с состоянием (Sprint 3+)
*Цель: Отказ от глобального синглтона.*

Это самый сложный этап. Не пытайся переписать всё сразу.
1.  Создай класс `AppContext` в `src/core/state.py`, который инкапсулирует состояние.
2.  Начни с новых функций: вместо `state = get_state()` передавай `context: AppContext` как аргумент.
3.  Постепенно рефактори старые модули при их изменении.

---

## ✅ 4. Чек-лист проверки (Definition of Done)

Перед тем как считать рефакторинг завершенным, проверь:
- [ ] В корне проекта нет бизнес-логики (только точки входа и конфиги).
- [ ] Все файлы сгруппированы в логические пакеты (`personas`, `gamification`, etc.).
- [ ] При отсутствии зависимости приложение выдает понятное сообщение об ошибке, а не молчит.
- [ ] Логика сборки промпта находится в одном месте (`PromptBuilder`).
- [ ] Тесты проходят успешно после рефакторинга.
- [ ] Документация (`README.md`, `ARCHITECTURE.md`) обновлена в соответствии с новой структурой.

---

## 💡 Советы по реализации

1.  **Делай маленькие коммиты.** Не пытайся сделать всё за один раз. Сначала создай структуру папок и закоммить пустые `__init__.py`. Потом переноси по одному модулю.
2.  **Запускай тесты после каждого шага.** Если сломалось — откатывай последний коммит.
3.  **Используй алиасы импортов.** При перемещении файлов используй `import src.personas.cyberpsychosis as cp`, чтобы минимизировать правки в коде.
4.  **Не бойся ломать.** Лучше потратить день на починку, чем месяц на поддержку спагетти-кода.

---

*Этот документ создан AI-ассистентом на основе аудита проекта CyberTeacher v6.1.*