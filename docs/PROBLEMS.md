# CyberTeacher - Текущие проблемы и решения

*Последнее обновление: 2026-05-16*

---

## 📋 Оглавление

1. [Критические проблемы (оставшиеся)](#critical)
2. [Архитектурные недостатки](#architecture)
3. [Качество кода](#code-quality)
4. [Тестирование](#testing)
5. [Производительность](#performance)
6. [Документация](#documentation)
7. [Пользовательский опыт](#ux)

---

## ✅ Решено 2026-05-16

### BUG-01: CachedLLM.invoke() возвращал None
**Проблема:** При cache hit функция не возвращала ответ — кэш не работал.
**Решение:** Добавлен `return response` в `main.py:116`.

### BUG-02: Dead code в knowledge.py
**Проблема:** 70 строк unreachable кода после `return` в `load_knowledge_base()` и дубликат в `get_relevant_docs()`.
**Решение:** Удалены unreachable блоки.

### BUG-03: handle_stats() читал несуществующие ключи
**Проблема:** `stats.get('messages')`, `stats.get('flags')` и т.д. — `get_stats()` возвращает только `points/quizzes/tasks`.
**Решение:** Исправлены ключи в `handlers/core.py`.

### BUG-04: /courses — "временно недоступны"
**Проблема:** Заглушка вместо реальной функциональности.
**Решение:** Подключено к `courses.py` — показывает список курсов и детали.

### BUG-05: /genassignment — отключён
**Проблема:** Команда показывала "временно отключён".
**Решение:** Восстановлен через `generators.generate_task()`.

### SEC-01: HTB пароль в plaintext
**Проблема:** `state.htb_password` хранился в JSON файле без шифрования.
**Решение:** XOR-based шифрование в `utils/security.py`. Поле `htb_password_enc` в state, автоматическая миграция старых plaintext паролей.

### DEDUP-01: Дубликаты кода
**Проблема:** `extract_json_block` (4 копии), `check_open_answer` (5 копий), `_ask_confirm` (2), `clear_chat_db` (2).
**Решение:** Вынесены в `utils/common.py`. Все копии заменены на импорты.

### DEAD-01: Мёртвый код
**Удалено:**
- `StudentLevel`, `AssessmentResult`, `ASSESSMENT_TOPICS`, `LevelAssessor` из `pedagogy.py` (~130 строк)
- `is_cybersecurity_related()`, `Task` dataclass из `main.py` (~12 строк)
- `downloader.py` — неиспользуемый файл

### NEW-01: Daily Challenge
**Добавлено:** `/daily` — ежедневные челленджи со стрик-системой, 14 задач, 3 уровня сложности, XP бонусы за стрик.

---

## Critical (Требуют внимания в ближайшее время)

### PC-01: UnicodeEncodeError на Windows (ПОЛНОСТЬЮ РЕШЕНО)
**Было:** При выводе эмодзи и спецсимволов в консоли Windows возникало `UnicodeEncodeError` из-за кодировки cp1251.

**Решение:** Создан модуль `utils/console_encoding.py`, который при запуске:
- Переключает консоль на UTF-8 (`chcp 65001`)
- Обёртывает `sys.stdout/stderr` с `errors='replace'`

**Файлы:** `utils/console_encoding.py`, `main.py` (импорт и вызов)

**Статус:** ✅ Done (2026-03-14)

---

## Architecture Issues (Архитектурные недостатки)

### A-01: Неполное использование state.py (РЕШЕНО)
**Описание:** `handlers/` частично используют `get_state()`, но некоторые функции всё ещё принимают `mode` и `level` как параметры. Нужно полный переход на state-синхронизацию.

**Файлы:** `handlers/*.py`, `main.py`

**Приоритет:** Medium

**Статус:** ✅ Done (2026-03-17) - Убран `new_level` из возвратов, полностью используется `get_state()`.

### A-02: Отсутствие DI (Dependency Injection)
**Описание:** Файлы импортируют глобальные объекты (LLM, кэш), что затрудняет тестирование и замену реализаций.

**Решение:** Внедрить простой DI-контейнер или фабрики.

**Файлы:** `config.py`, `handlers/*.py`

**Приоритет:** Low

**Статус:** ❌ Not started

---

## Code Quality

### CQ-01: Низкое покрытие тестами (~15%)
**Описание:** Только базовые тесты. Нет покрытия для большинства handlers, knowledge, memory.

**Решение:** Добавить unit-тесты для:
- `handlers/social.py` ✅ (сделано)
- `handlers/risk` ✅ (сделано)
- `memory.py`
- `knowledge.py`
- `practice.py`

**Приоритет:** High (H-11)

**Статус:** ⚠️ In progress (15% → цель 70%)

### CQ-02: LSP/Type hints нарушения
**Описание:** Множество ошибок типов в `config.py` (ChatOllama параметры), `handlers/social.py` (response types).

**Решение:** Добавить `# type: ignore` там, где типы неизвестны, или явно аннотировать.

**Приоритет:** Medium

**Статус:** ⚠️ In progress (базовые исправления есть)

---

## Testing

### T-01: Нет интеграционных тестов
**Описание:** Только unit-тесты с моками. Нет end-to-end сценариев.

**Решение:** Добавить e2e тесты через `subprocess` запуска `python main.py` с симулированным вводом.

**Приоритет:** Medium

**Статус:** ❌ Not started

---

## Performance

### P-01: Большой размер embeddings
**Описание:** Chroma DB хранит все чанки без очистки старых версий при обновлении PDF.

**Решение:** Реализован `incremental_update` — добавляет только новые/changed файлы. Нужно тестирование.

**Файлы:** `knowledge.py`

**Статус:** ✅ Done (2026-03-09)

---

## Documentation

### D-01: Устаревший README.md
**Описание:** В README не хватает новых команд: `/social`, `/risk`, `/model`, `/set-api-key`.

**Решение:** Обновить README.md с полным списком команд и примерами.

**Приоритет:** High

**Статус:** ⚠️ In progress (частично обновлён)

---

## User Experience

### UX-01: Нет справки по новым командам (РЕШЕНО)
**Описание:** `/help` не показывает `/social`, `/risk` и другие новые команды.

**Решение:** Обновить `ui.py` show_help() с полным списком команд и добавить `/help detail`.

**Файлы:** `ui.py`

**Приоритет:** Medium

**Статус:** ✅ Done (2026-03-17) - Добавлены все новые команды в `/help` и реализован `/help detail`.

---

## ✅ Недавно решённые проблемы (2026-03-14)

- **UnicodeEncodeError** на Windows — создан `utils/console_encoding.py`
- **Циклические импорты** — вынесены общие функции, устранены зависимости
- **Проверка Docker** — добавлена `docker_available()`
- **Валидация Docker exec** — shlex.split + white-list
- **Генераторы** — исправлены импорты и `extract_json_block`
- **Кэширование** — in-memory LRU кэш + планирование SQLite

---

*Последнее обновление: 2026-03-17*
