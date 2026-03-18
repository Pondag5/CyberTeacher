# CyberTeacher v3.2

**CLI для обучения кибербезопасности с LLM-учителем внутри**

---

## 🎯 О ПРОЕКТЕ

- **LLM провайдер:** Ollama (локально) или OpenRouter (облако)
- **Модель:** qwen2.5:7b (Ollama) или mistral-7b (OpenRouter)
- **RAG:** Chroma + sentence-transformers
- **Учитель:** Хакер из 90-х (IRC, BBS, Zaxelon)
- **Язык:** Русский

---

## 🔄 СМЕНА ПРОВАЙДЕРА LLM

В `config.py` установи:

```python
LLM_PROVIDER = "ollama"   # локально (нужен Ollama)
# или
LLM_PROVIDER = "openrouter"   # облако (нужен API ключ)
```

Для **OpenRouter**:
1. Получи ключ на https://openrouter.ai/keys
2. Заполни `OPENROUTER_API_KEY` в `config.py` или через переменную окружения
3. Выбери модель: `OPENROUTER_MODEL = "mistralai/mixtral-8x7b-instruct"` (бесплатно) или другую

---

## ✅ РАБОТАЮЩИЕ КОМАНДЫ

| Команда | Описание |
|---------|----------|
| `/stats` | Статистика пользователя |
| `/news` | Новости с переводом (SecurityWeek RSS) |
| `/cve` | Информация об уязвимости CVE |
| `/threats [name]` | Досье на APT-группу (APT28, APT29, Lazarus и др.) |
| `/groups` | Группировка APT по странам, топ-тактик |
| `/threat` | Сводка угроз (недельная) |
| `/story` | 20 эпизодов обучения с флагами |
| `/flag FLAG{...}` | Проверить флаг |
| `/achievements` | Достижения |
| `/writeup` | Шаблон writeup |
| `/practice`, `/lab` | Docker лаборатории |
| `/quiz` | Викторина (адаптивная, фокус на слабых темах) |
| `/adaptive` | Показать слабые темы |
| `/repeat` | Интервальные повторения (SM-2) |
| `/task` | Случайные задания |
| `/genassignment` | Генератор заданий (в разработке) |
| `/guide` | Гайд по VM |
| `/courses` | Список курсов |
| `/course <номер>` | Начать курс (1-6) |
| `/next` | Следующая тема в курсе |
| `/summary <topic>` | Генерация конспекта (Markdown) |
| `/auto_writeup` | Автоматический writeup |
| `/check`, `/logs` | Проверить контейнеры |
| `/terminal` | Лог команд ученика |
| `/log <cmd>` | Записать команду в лог |
| `/sandbox <lang> <code>` | Песочница для кода (Docker) |
| `/social [scenario]` | **Тренажёр социальной инженерии** (интерактивный диалог с ботом-жертвой, оценка успеха) |
| `/risk [up\|down\|set N\|reset]` | **Уровень риска** (механика компрометации, влияет на story mode) |
| `/model` | Показать/переключить модель LLM |
| `/set-api-key` | Установить API ключ (OpenRouter/HuggingFace) |
| `/provider` | Показать текущий провайдер LLM |
| `/help detail` | Подробная справка по командам |
| Обычный текст | → LLM (учитель) |

---

## 🐳 DOCKER LABS

| Категория | Лабы |
|-----------|------|
| Web | DVWA, bWAPP, Juice Shop, WebGoat |
| SQLi | SQLi Labs, SQLMap Demo |
| API | Vulnerable REST API, CRAPI |
| Linux | Metasploitable 2/3 |
| Windows | Metasploitable 3, VulnServer |
| CTF | CTFd, Root The Box |

---

## 📚 УЧЕБНЫЕ КУРСЫ

1. Основы веб-безопасности (SQLi, XSS, CSRF)
2. Продвинутая веб-безопасность
3. Сетевая безопасность
4. Безопасность API
5. Privilege Escalation
6. CTF Starter

---

## 🎮 STORY MODE

- **20 эпизодов** с флагами
- **XP система:** Script Kiddie → Legend
- **Достижения:** First Blood, Web Hacker, Network Ninja, etc.
- **Интеграция** с Docker лабами

---

## 🛠️ ХАРАКТЕР УЧИТЕЛЯ

Хакер из 90-х - никогда не сознаётся напрямую, но "случайно" упоминает:
- "Это напоминает мне случай, когда мы с пацанами в 95-м..."
- "Помнится мне один чел в чате в 97-м..."
- "Да это всё фигня, я ещё в 93-м на Zaxelon такое вытворял..."

---

## 📁 СТРУКТУРА ПРОЕКТА

```
CyberTeacher/
├── main.py                    # Главный цикл
├── handlers.py                # Обработка команд
├── state.py                  # Глобальное состояние
├── pedagogy.py               # Характер учителя
├── config.py                 # Конфигурация
├── ui.py                    # Интерфейс (Rich)
├── courses.py                # Учебные курсы
├── practice.py               # Docker лабы
├── story_mode.py             # Игровой режим
├── knowledge.py              # RAG база
├── memory.py                 # SQLite БД
├── terminal_log.py           # Логирование
├── news_fetcher.py          # RSS новости
├── question_generation.py    # Квизы
├── code_review.py           # Анализ кода
├── generators.py             # Генерация задач
├── memory/                   # chat_history.db, terminal_log.txt
├── embeddings/               # Chroma DB
├── knowledge_base/           # PDF по кибербезопасности
└── docs/                    # Документация
```

---

## 🚀 ЗАПУСК

```bash
python main.py
```

---

## ⏳ ОСТАВШАЯСЯ РАБОТА

### Высокий приоритет
- [ ] CVE информация (парсинг NVD/Exploit-DB)
- [ ] Умный RAG с реранкингом (интеграция cross-encoder)
- [ ] LLM анализ новостей (учитель комментирует свежие атаки)
- [ ] Увеличить coverage тестов >50%
- [ ] Улучшить news_fetcher (lxml, обработка ошибок)

### Средний приоритет
- [ ] Завершить BM25 (отладка)
- [ ] ASCII визуальная карта сети
- [ ] GitHub/GitLab интеграция (анализ кода по URL, поиск секретов)
- [ ] Docker Compose для всего стека

### Низкий приоритет
- [ ] Web UI (Streamlit/Gradio)
- [ ] Голосовой учитель (TTS/STT)
- [ ] Мультиплатформенная синхронизация
- [ ] Плагинная архитектура

---

## 💡 ИДЕИ РАЗВИТИЯ

1. **Android клиент** - обращается к FastAPI на ПК
2. **Telegram бот** - уже в планах
3. **Docker Compose** - упаковка всего проекта
4. **GitHub** - CI/CD для автосборок
5. **Gamification** - больше ачивок, уровней

---

*Обновлено: 2026-03-04*
