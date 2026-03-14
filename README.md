# CyberTeacher

**CLI-приложение для обучения кибербезопасности с встроенным LLM-учителем**

---

## 🎯 О проекте

CyberTeacher — это интерактивный CLI-тренажёр для изучения кибербезопасности. У вас есть персональный AI-учитель (хакер из 90-х), который проводит вас через теорию, практику, CTF-задачи и реальные сценарии атак.

### Технологии
- **LLM провайдеры**: Ollama (локально) / OpenRouter / HuggingFace
- **Модели**: qwen2.5:7b, mistral, llama2 и другие
- **RAG**: ChromaDB + sentence-transformers + cross-encoder реранкинг
- **Интерфейс**: Rich (красивый CLI)
- **Практика**: Docker-лаборатории (DVWA, Juice Shop, Metasploitable и др.)
- **База знаний**: PDF-файлы, автоматическая индексация

---

## 🚀 Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/CyberTeacher.git
cd CyberTeacher

# Установить зависимости
pip install -r requirements.txt

# Скачать модель Ollama (если используете локально)
ollama pull qwen2.5:7b

# Запустить
python main.py
```

---

## 📋 Команды

### Режимы (цифровое меню 1-5)
| Цифра | Режим |
|-------|-------|
| 1 | Учитель (Teacher) — обычный диалог |
| 2 | Эксперт (Expert) — сложные темы |
| 3 | CTF режим — флаги и соревнования |
| 4 | Викторина (Quiz) — тесты по темам |
| 5 | Анализ кода (Code Review) — безопасный код |

### Информация и справка (6-14)
| Цифра | Команда | Описание |
|-------|---------|----------|
| 6 | `/news` | Новости кибербезопасности |
| 7 | `/achievements` | Достижения и XP |
| 8 | `/stats` | Статистика прогресса |
| 9 | `/help` | Справка по командам |
| 10 | `/help detail` | Подробная справка |
| 11 | `/guide` | Гайд по VM (Kali, HTB) |
| 12 | `/version` | Версия приложения |
| 13 | `/menu` | Показать цифровое меню |

### Практика и курсы (15-19)
| Цифра | Команда | Описание |
|-------|---------|----------|
| 14 | `/practice` | Выбор практического задания |
| 15 | `/lab` | Docker лаборатории (21 шт.) |
| 16 | `/courses` | Учебные курсы (6 курсов) |
| 17 | `/story` | Режим истории (21 эпизод) |
| 18 | `/task` | Случайное задание |
| 19 | `/genassignment` | Генератор заданий (в разработке) |

### Управление (20-29)
| Цифра | Команда | Описание |
|-------|---------|----------|
| 20 | `/provider` | Показать/сменить провайдера LLM |
| 21 | `/model` | Показать/сменить модель |
| 22 | `/terminal` | Лог терминала |
| 23 | `/cache stats` | Статистика кэша |
| 24 | `/clearcache` | Очистить кэш |
| 25 | `/check` | Проверить контейнеры Docker |
| 26 | `/history` | История чата |
| 27 | `/writeup` | Шаблон отчёта |
| 28 | `/add_book` | Добавить PDF в базу знаний |
| **29** | **`/social`** | **Тренажёр социальной инженерии** ✨ |

### Разное (30-39)
| Цифра | Команда | Описание |
|-------|---------|----------|
| 30 | `/flag FLAG{...}` | Проверить флаг |
| 31 | `/log <cmd>` | Записать команду в лог |
| 32 | `/set-api-key` | Установить API ключ |
| 33 | `/smart_test` | Умный тест |
| 34 | `/read_url` | Чтение URL |
| **35** | **`/threats`** | **APT досье** (из JSON) ✨ |
| **36** | **`/groups`** | **Группировка APT по странам** ✨ |
| **37** | **`/threat summary`** | **Недельная сводка угроз** ✨ |
| 38 | `/cve` | CVE информация |
| 39 | `/news search` | Поиск новостей |

---

## ✨ Новые возможности (2026-03-14)

### C-02: Социальная инженерия (`/social`)
Интерактивный диалоговый тренажёр, где вы — атакующий, а LLM играет жертву.

**Сценарии:**
- **Фишинг** — убедить перейти по ссылке и ввести пароль
- **Претекстинг** — получить пароль под видом IT-поддержки
- **Тейлгейтинг** — проникнуть в офис, Following someone

После диалога LLM оценивает, достигнута ли цель.

### C-03: Сводка угроз (`/threat summary`)
Еженедельная сводка актуальных угроз (APT, DDoS, ransomware, CVE) с анализом от учителя:
- Забирает свежие новости из RSS (SecurityWeek, CISA)
- Фильтрует по ключевым словам
- LLM составляет обзор, тренды и рекомендации
- Показывает источники

### C-04: APT досье (`/threats`, `/groups`)
7 готовых досье на APT-группы (APT28, APT29, Lazarus, APT41, Sandworm, FIN7, REvil) с:
- Алиасами, страной, активностью
- Тактиками MITRE ATT&CK
- Инструментами и техниками
- Ссылками на MITRE

`/groups` показывает группировку всех групп по странам и топ-10 тактик/инструментов.

### Fix: Кодировка Windows
Проблема `UnicodeEncodeError` при выводе эмодзи и спецсимволов решена автоматически:
- `utils/console_encoding.py` настраивает консоль на UTF-8
- Работает без перезагрузки, не влияет на другие программы

---

## 🐳 Docker лаборатории (21 шт.)

### Web
- DVWA, bWAPP, OWASP Juice Shop, WebGoat, DVNA, Dodgy Ninja, Pickle Rick

### SQLi
- SQLi Labs, SQLMap Demo

### API
- Vulnerable REST API, CRAPI, Holi-Now

### JWT
- JWT Lab

### Linux
- Metasploitable 2, Metasploitable 3 (Linux)

### Windows
- Metasploitable 3 (Windows), VulnServer

### Mobile
- DVMA

### Cloud
- CloudGoat

### CTF
- CTFd, Root The Box

---

## 📚 Учебные курсы

1. Основы веб-безопасности (SQLi, XSS, CSRF)
2. Продвинутая веб-безопасность
3. Сетевая безопасность
4. Безопасность API
5. Privilege Escalation
6. CTF Starter

---

## 🔧 Настройка

### Переключение провайдера LLM
```python
# В config.py
LLM_PROVIDER = "ollama"   # локально
# или
LLM_PROVIDER = "openrouter"  # облако
```

Для **OpenRouter**:
1. Получите ключ на https://openrouter.ai/keys
2. Установите: `export OPENROUTER_API_KEY=sk-...`
3. Выберите модель: `OPENROUTER_MODEL = "mistralai/mixtral-8x7b-instruct"`

---

## 🧪 Тестирование

```bash
# Все тесты
python -m unittest discover -s tests -v

# Только новые
python -m unittest tests.test_social tests.test_threat_summary tests.test_threats_groups -v
```

---

## 📊 План разработки

См. `docs/IMPLEMENTATION_PLAN.md` — полный план с приоритетами.

**Выполнено (28 задач):**
- Blocker: B-01..B-05 (интеграция state.py, циклические импорты, generators, Docker check, Docker exec validation)
- Critical: C-01 (risk_level), C-02 (social engineering), C-03 (threat summary)
- High: H-13..H-15 (мульти-провайдер, `/model`, `/set-api-key`)
- Medium: M-24..M-29 (help detail, graceful degradation, LLM length check, model switching, API key)
- Encoding fix для Windows

**В работе (4 задачи):**
- C-04: APT досье (7/27 групп)
- C-05: Умный RAG с реранкингом
- C-07: SQLite кэш с TTL
- M-17: Анализ новостей учителем

---

## 🤝 Вклад

PR приветствуются! См. `docs/IMPLEMENTATION_PLAN.md` для задач.

---

## 📄 Лицензия

MIT

---

## 🔗 Полезные ссылки

- [План реализации](docs/IMPLEMENTATION_PLAN.md)
- [Идеи и приоритеты](docs/IDEAS.md)
- [Отслеживание проблем](docs/PROBLEMS.md)
- [Гайд по VM](docs/ГАЙД_VM.md)

---

**CyberTeacher v3.2** — учитесь кибербезопасности в интерактивном режиме! 🛡️💻
