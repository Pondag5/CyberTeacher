# CyberTeacher v3.2

**CLI для обучения кибербезопасности с LLM-учителем внутри**

---

## 🎯 О ПРОЕКТЕ

- **Модель:** Ollama (qwen2.5:7b)
- **RAG:** Chroma + sentence-transformers
- **Учитель:** Хакер из 90-х (IRC, BBS, Zaxelon)
- **Язык:** Русский

---

## ✅ РАБОТАЮЩИЕ КОМАНДЫ

| Команда | Описание |
|---------|----------|
| `/stats` | Статистика пользователя |
| `/news` | Новости с переводом (SecurityWeek RSS) |
| `/story` | 20 эпизодов обучения с флагами |
| `/flag FLAG{...}` | Проверить флаг |
| `/achievements` | Достижения |
| `/writeup` | Шаблон writeup |
| `/practice`, `/lab` | Docker лаборатории |
| `/quiz` | Викторина (sql/xss/network/crypto/linux) |
| `/task` | Случайные задания |
| `/guide` | Гайд по VM |
| `/courses` | Список курсов |
| `/course <номер>` | Начать курс (1-6) |
| `/next` | Следующая тема в курсе |
| `/check`, `/logs` | Проверить контейнеры |
| `/terminal` | Лог команд ученика |
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
- [x] Интеграция state.py
- [x] Story Mode с флагами
- [x] Учитель из 90-х
- [x] Русификация
- [ ] Удалить llm.py

### Средний приоритет
- [ ] Telegram бот
- [ ] FastAPI сервер (для Android/Telegram)
- [ ] Улучшить CTF режим

### Низкий приоритет
- [ ] Docker Compose для проекта
- [ ] Web UI
- [ ] HackNet-стиль игра

---

## 💡 ИДЕИ РАЗВИТИЯ

1. **Android клиент** - обращается к FastAPI на ПК
2. **Telegram бот** - уже в планах
3. **Docker Compose** - упаковка всего проекта
4. **GitHub** - CI/CD для автосборок
5. **Gamification** - больше ачивок, уровней

---

*Обновлено: 2026-03-04*
