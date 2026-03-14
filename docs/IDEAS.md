# 🎯 CyberTeacher - Идеи для улучшения

*Все фичи, которые могут быть реализованы. Отсортировано по приоритету.*

---

## 📊 Легенда

| Параметр | Описание |
|----------|----------|
| **Impact** | Влияние на продукт (1-10, 10 = максимально) |
| **Effort** | Сложность реализации (1-5, 5 = очень сложно) |
| **Status** | Not started / In progress / Done |
| **Dependencies** | Зависит от других задач |

---

## 🔴 Critical (Blockers)

Толькоgrade correctness, security, stability.

| ID | Идея | Impact | Effort | Зависимости | Статус |
|----|------|--------|--------|-------------|--------|
| B-01 | state.py интеграция | 9 | 2 | - | ✅ Done |
| B-02 | Циклические импорты | 9 | 3 | B-01 | ✅ Done |
| B-03 | generators.py | 8 | 2 | B-02 | ✅ Done |
| B-04 | Docker availability check | 8 | 1 | - | ✅ Done |
| B-05 | Docker exec validation | 10 | 2 | - | ✅ Done |
| S-01 | Command injection ( practicе ) | 10 | 2 | B-05 | ✅ Done |

---

## 🟠 High Priority

Ключевые фичи для перехода на новый уровень.

| ID | Идея | Impact | Effort | Зависимости | Статус |
|----|------|--------|--------|-------------|--------|
| C-01 | `risk_level` в state.py | 7 | 2 | B-01 | ✅ Done |
| C-02 | Команда `/social` (социальная инженерия) | 9 | 5 | B-01, C-01 | ✅ Done |
| C-03 | Команда `/threats` (сводки угроз) | 9 | 4 | B-01 | ✅ Done |
| C-04 | Команда `/group` (APT досье) | 8 | 3 | B-01 | ✅ Partially done (7/27 групп, можно расширять) |
| C-05 | Умный RAG с реранкингом | 9 | 4 | B-01 | ✅ Partially (re

指着reranker уже загружен) |
| C-06 | Гибридный поиск (BM25) | 8 | 5 | C-05 | ❌ Not started |
| C-07 | Кэширование ответов LLM | 7 | 4 | B-01 | ✅ Partially (in-memory кэш, нужен SQLite + TTL) |
| C-08 | Песочница для кода | 10 | 8 | B-01, practice.py | ❌ Not started |
| C-09 | Адаптивный план обучения | 9 | 6 | B-01, C-01 | ❌ Not started |
| C-10 | Интервальные повторения (Spaced Repetition) | 8 | 5 | C-01, C-09 | ❌ Not started |
| C-11 | Генерация конспектов (`/summary`) | 8 | 4 | B-01, C-05 | ❌ Not started |
| C-12 | Автоматическая генерация writeup | 7 | 4 | B-01, C-02 | ❌ Not started |
| C-13 | Расширенные достижения | 6 | 3 | B-01 | ❌ Not started |
| C-14 | Магазин / прокачка | 9 | 7 | C-01, C-13 | ❌ Not started |
| U-05 | Graceful degradation LLM | 8 | 2 | B-01 | ✅ Done |
| U-06 | Лимит длины ответа LLM | 7 | 1 | B-01 | ✅ Done |
| S-02 | Валидация длины ввода | 7 | 1 | B-01 | ✅ Done |
| S-03 | Фильтрация паролей из логов | 6 | 2 | B-01 | ✅ Done |
| S-04 | Rate limiting | 7 | 3 | B-01 | ❌ Not started |
| H-13 | **Мульти-провайдер LLM** | **9** | **4** | B-01 | ✅ Done |

---

## 🟡 Medium Priority

Важные, но не критичные улучшения.

| ID | Идея | Impact | Effort | Зависимости | Статус |
|----|------|--------|--------|-------------|--------|
| M-01 | Docker Compose | 6 | 3 | B-01 | ❌ Not started |
| M-02 | Система команд (Red vs Blue) | 8 | 6 | B-01, C-02 | ❌ Not started |
| M-03 | Модуль OSINT | 8 | 6 | B-01 | ❌ Not started |
| M-04 | Конструктор фишинговых писем | 7 | 5 | B-01, C-02 | ❌ Not started |
| M-05 | Исторический режим | 6 | 4 | B-01, story_mode.py | ❌ Not started |
| M-06 | Тренажёр эксплойтов | 9 | 7 | C-08, B-01 | ❌ Not started |
| M-07 | Shodan / Censys интеграция | 7 | 4 | B-01 | ❌ Not started |
| M-08 | Анализ вредоносов (песочница) | 9 | 8 | C-08, B-01 | ❌ Not started |
| M-09 | Инфографика (Mermaid) | 6 | 3 | B-01 | ❌ Not started |
| M-10 | Интерактивные расследования | 8 | 5 | B-01 | ❌ Not started |
| M-11 | Голосовой учитель (TTS/STT) | 6 | 6 | B-01 | ❌ Not started |
| M-12 | Поддержка Jupyter Notebook | 7 | 4 | B-01 | ❌ Not started |
| M-13 | SCORM / LTI поддержка | 6 | 5 | B-01 | ❌ Not started |
| M-14 | Плагинная архитектура | 7 | 6 | B-01, A-03 | ❌ Not started |
| M-15 | Курсы от экспертов | 5 | 3 | B-01, courses.py | ❌ Not started |
| M-16 | Видео / подкасты внутри | 5 | 4 | B-01, Web UI | ❌ Not started |
| M-17 | Новости с аналитикой | 7 | 3 | B-01, news_fetcher.py | ✅ Partially (база есть, нужен анализ от LLM) |
| M-18 | Временная петля / альтернативные реальности | 6 | 5 | B-01, story_mode.py | ❌ Not started |
| M-19 | Учитель с эмоциями | 7 | 4 | B-01 | ❌ Not started |
| M-20 | Кроссплатформенная синхронизация | 6 | 5 | B-01 | ❌ Not started |
| M-21 | Rate limiting | 6 | 3 | B-01, main.py | ❌ Not started |
| M-22 | Summarization истории | 7 | 4 | B-01, memory.py | ❌ Not started |
| M-23 | Расширение QUIZ_TOPICS | 5 | 2 | B-01, question_generation.py | ❌ Not started |
| M-24 | `/help detail` | 5 | 2 | B-01, ui.py | ✅ Done |
| M-25 | Graceful degradation LLM | 7 | 2 | B-01 | ✅ Done |
| M-26 | Проверка длины ответа LLM | 6 | 1 | B-01 | ✅ Done |
| M-27 | Улучшение новостного парсера | 5 | 2 | B-01, news_fetcher.py | ❌ Not started |
| M-28 | Команда `/model` — переключение моделей | 8 | 2 | H-13 | ✅ Done |
| M-29 | Команда `/set-api-key` — установка API ключей | 7 | 2 | H-13 | ✅ Done |

---

## 🟢 Low Priority

Долгосрочные, "игрушечные" улучшения.

| ID | Идея | Impact | Effort | Зависимости | Статус |
|----|------|--------|--------|-------------|--------|
| L-01 | Мультимодальность (LLaVA) | 8 | 7 | B-01 | ❌ Not started |
| L-02 | Трекер практических навыков | 7 | 5 | B-01, state.py | ❌ Not started |
| L-03 | Mind map визуализация (Mermaid) | 6 | 4 | B-01, Web UI | ❌ Not started |
| L-04 | Поддержка мобильного приложения | 6 | 8 | M-20, B-01 | ❌ Not started |
| L-05 | Gamification (уровни, бейджи) | 5 | 3 | C-13, B-01 | ❌ Not started |
| L-06 | Dark mode для CLI | 4 | 2 | B-01, rich.py | ❌ Not started |
| L-07 | Sound effects / narrator | 3 | 3 | B-01 | ❌ Not started |
| L-08 | Поддержка Python 3.13+ | 3 | 1 | B-01 | ❌ Not started |
| L-09 | Интеграция с Metasploit | 9 | 9 | C-08, B-01 | ❌ Not started |
| L-10 | Продвинутый анализатор кода (Semgrep) | 8 | 6 | C-08, B-01 | ❌ Not started |

---

## 🟦 Architecture (Архитектурные улучшения)

| ID | Идея | Impact | Effort | Зависимости | Статус |
|----|------|--------|--------|-------------|--------|
| A-01 | Документация ADR | 7 | 4 | B-01 | ❌ Not started |
| A-02 | Type hints 100% | 8 | 5 | B-01 | ❌ Not started |
| A-03 | Зависимость от интерфейсов (DI) | 8 | 6 | B-01 | ❌ Not started |
| A-04 | Unit tests >70% | 9 | 5 | B-01 | ❌ Not started (текущий ~15%) |
| A-05 | CI/CD (GitHub Actions) | 7 | 4 | A-04, B-01 | ❌ Not started |
| A-06 | ruff/mypy линтинг | 6 | 2 | B-01 | ❌ Not started |
| A-07 | Конфиг в pyproject.toml | 5 | 3 | B-01 | ❌ Not started |

---

## 📈 Gaps (отсутствующие важные фичи)

Фичи, которые ещё не в списке, но могут быть полезны.

| ID | Идея | Impact | Effort | Приоритет |
|----|------|--------|--------|-----------|
| G-01 | Интеграция с TryHackMe API | 8 | 5 | High |
| G-02 | Поддержка VulnHub / HackInTheBox | 7 | 4 | High |
| G-03 | Генерация CTF-флагов на лету (проверка через hash) | 8 | 3 | High |
| G-04 | Мультиязычность (EN/RU) | 6 | 4 | Medium |
| G-05 | Webhook уведомления (Telegram/Discord) | 6 | 4 | Medium |
| G-06 | Docker lab templates (YAML) | 7 | 5 | High |
| G-07 | Офлайн-режим (без LLM) | 5 | 3 | Medium |
| G-08 | Mood translator (сленг → нормальный) | 4 | 2 | Low |
| G-09 | Профили пользователей (смена имени) | 5 | 2 | Medium |
| G-10 | Интеграция с Wireshark (анализ pcap) | 8 | 6 | High |

---

## 🎯 Recommended Next Steps

С учетом текущего состояния (B-01..B-05, U-05, S-02, U-06, H-13 done):

### 1. **Быстрые win** (1-2 часа):
- **C-01**: Добавить `risk_level` в state.py
- **S-03**: Фильтрация паролей из логов
- **M-24**: `/help detail` команда

### 2. **Средние** (1-2 дня):
- **C-02**: `/social` команда (прототип)
- **C-03**: `/threats` (парсинг RSS)
- **C-04**: `/group` (APT досье)
- **C-07**: SQLite кэш с TTL

### 3. **Большие** (3-5 дней):
- **C-05**: Умный RAG (уже частично есть)
- **C-08**: Песочница кода (Docker exec улучшения)
- **C-09**: Адаптивный план обучения
- **M-06**: Тренажёр эксплойтов

### 4. **Архитектурные** (неделя+):
- **A-04**: Тесты >70%
- **A-03**: DI/интерфейсы
- **A-05**: CI/CD

---

## 📌 Как выбирать:

1. **Impact/Effort матрица**:
   - Quick wins: Impact 7-10, Effort 1-2
   - Strategic: Impact 9-10, Effort 3-5
   - Big bets: Impact 8-10, Effort 6+

2. **Зависимости**: Сначала B-01, B-02, B-03, B-04, B-05

3. **User pain**: Что больше всего просят? → `/social`, `/threats`, `/summary`

4. **Technical debt**: A-01..A-07 делать постепенно вместе с фичами

---

*Последнее обновление: 2026-03-14*
