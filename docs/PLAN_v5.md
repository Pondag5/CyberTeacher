# CyberTeacher v5.0 — План развития

*Цель: PWA = CLI по функционалу. Развернуть БД. Добавить медиа-контент.*
*Последнее обновление: 2026-05-18*

---

## 📊 Текущее состояние

| Метрика | CLI | PWA | Статус |
|---------|-----|-----|--------|
| Команд / Фич | 95+ | 18 вкладок | ✅ Parity достигнут |
| API эндпоинтов | — | 40+ | ✅ Все используются |
| Вкладок | — | 18 | ✅ Полное покрытие |
| Тестов | 985 | — | ✅ 0 ошибок |
| Темы | 3 (CLI) | 3 (PWA) | ✅ Синхронизированы |

---

## ✅ Шаг 1: PostgreSQL — ВЫПОЛНЕН

| Задача | Файлы | Статус |
|--------|-------|--------|
| SQLAlchemy abstraction layer | `db.py`, `memory.py` | ✅ |
| Миграции (Alembic) | `migrations/` | ✅ |
| Session management | `api_server.py`, `state.py` | ✅ |
| Docker compose (PostgreSQL + pgAdmin) | `docker-compose.yml` | ✅ |
| .env конфигурация | `.env.example` | ✅ |

**Как переключиться на PostgreSQL:**
```bash
docker compose up -d
# В .env: DATABASE_URL=postgresql://cyberteacher:pass@localhost:5432/cyber_teacher
alembic upgrade head
```

---

## ✅ Шаг 2: PWA = CLI — ВЫПОЛНЕН

### Реализовано (18 вкладок):

| # | Вкладка | Статус | API Endpoints |
|---|---------|--------|---------------|
| 1 | 🎭 Modes | ✅ | `GET /api/modes`, `POST /api/mode/set` |
| 2 | 💬 Chat | ✅ | `POST /api/chat` (Rick persona) |
| 3 | 📊 Progress | ✅ | `GET /api/progress` |
| 4 | 📝 Quiz | ✅ | `POST /api/quiz/generate`, `POST /api/quiz/result` |
| 5 | 🎯 Daily | ✅ | `GET /api/daily`, `POST /api/daily/submit` |
| 6 | 👤 Profile | ✅ | `GET /api/profile`, `POST /api/profile/update` |
| 7 | 📚 Courses | ✅ | `GET /api/courses`, `POST /api/courses/{id}/select` |
| 8 | 📖 Story | ✅ | `GET /api/story`, `POST /api/story/start`, `POST /api/story/submit` |
| 9 | 🛤️ Tracks | ✅ | `GET /api/tracks`, `POST /api/tracks/start`, `POST /api/tracks/progress` |
| 10 | 🚩 CTF | ✅ | `GET /api/ctf/status`, `POST /api/flags/submit` |
| 11 | 🐳 Labs | ✅ | `GET /api/labs`, `POST /api/docker/*` (5 endpoints) |
| 12 | 🔍 OSINT | ✅ | `GET /api/threats`, `GET /api/news`, `GET /api/cve/{id}` |
| 13 | 💻 Scanner | ✅ | `POST /api/scan`, `POST /api/scanv2`, `GET /api/scanv2/rules` |
| 14 | 🛒 Shop | ✅ | `GET /api/shop`, `POST /api/shop/purchase` |
| 15 | 🦠 Malware | ✅ | `POST /api/malware` |
| 16 | 🏆 Achievements | ✅ | `GET /api/achievements` |
| 17 | 🥊 Versus | ✅ | `GET/POST /api/versus/*` (4 endpoints) |
| 18 | 📈 Stats | ✅ | `GET /api/stats` |
| 19 | ⚙️ Settings | ✅ | `GET/POST /api/offline`, `GET /api/config` |

### Дизайн-система:
- ✅ 3 темы: Ocean 🌊, Sunset 🌅, Matrix 💻
- ✅ Персонаж: Рик Санчез + Док Браун
- ✅ Шрифты: Fira Code + Inter
- ✅ Neon glow эффекты
- ✅ Launcher GUI (`python launcher.py`)

---

## 📚 Шаг 3: Контент — В ПРОЦЕССЕ

### Книги (PDF для RAG базы)
Нужны книги по кибербезопасности для `knowledge_base/`:

| Тема | Примеры | Формат |
|------|---------|--------|
| Web Security | OWASP Testing Guide, Web Hacking 101 | PDF |
| Network Security | Network Security Assessment, Nmap Book | PDF |
| Malware Analysis | Practical Malware Analysis, Malware Analyst's Cookbook | PDF |
| Cryptography | Cryptography Engineering, Serious Cryptography | PDF |
| CTF | The CTF Field Guide, Pwnable.kr writeups | PDF |
| Linux/PrivEsc | Linux Privilege Escalation, HackTricks | PDF |
| OSINT | Open Source Intelligence Techniques | PDF |
| Reverse Engineering | Practical Reverse Engineering, RE for Beginners | PDF |

### Видео (для `/media` вкладки)
Нужны ссылки на обучающие видео (YouTube, локальные файлы):

| Тема | Примеры | Формат |
|------|---------|--------|
| SQL Injection | PortSwigger Web Security Academy | YouTube URL |
| XSS | OWASP XSS Prevention | YouTube URL |
| Buffer Overflow | LiveOverflow, John Hammond | YouTube URL |
| Networking | NetworkChuck, Professor Messer | YouTube URL |
| Linux | NetworkChuck, The Cyber Mentor | YouTube URL |
| CTF Walkthroughs | IppSec, 0xdf | YouTube URL |

### Изображения (для курсов, ачивок, UI)
| Тип | Где используется | Формат |
|-----|------------------|--------|
| Иконки курсов | PWA Courses tab | SVG/PNG 64x64 |
| Иконки навыков | PWA Skills tab | SVG/PNG 48x48 |
| Баннеры ачивок | PWA Achievements | PNG 128x128 |
| Схемы сетей | Обучение networking | PNG/SVG |
| Скриншоты инструментов | OSINT, Nmap, Burp | PNG |
| ASCII-арт альтернативы | PWA вместо ASCII | PNG/SVG |

### Звуки (для геймификации)
| Событие | Где | Формат |
|---------|-----|--------|
| Терминал: ввод команды | PWA + CLI | MP3/WAV 0:01 |
| Успех: операция выполнена | PWA + CLI | MP3/WAV 0:02 |
| Ошибка: доступ запрещён | PWA + CLI | MP3/WAV 0:01 |
| Level Up: новый уровень | Progress | MP3/WAV 0:03 |
| Уведомление: новое сообщение | Chat | MP3/WAV 0:01 |

### Данные (для симуляций)
| Тип | Описание | Формат |
|-----|----------|--------|
| CVE база | 1000+ реальных CVE | JSON/CSV |
| APT группы | Расширенные досье | JSON |
| Malware samples | Хэши, поведенческий анализ | JSON |
| CTF задачи | 100+ задач с решениями | YAML |
| Сценарии OSINT | Реальные кейсы | YAML |
| Эксплойты | PoC коды для обучения | Python/Bash |

---

## 🎯 Рекомендуемый порядок

1. ~~**Неделя 1:** PostgreSQL + миграции (Шаг 1)~~ ✅
2. ~~**Неделя 2-3:** PWA HIGH вкладки (6 вкладок, Шаг 2)~~ ✅
3. ~~**Неделя 4:** PWA MEDIUM вкладки (4 вкладки, Шаг 2)~~ ✅
4. **Неделя 5:** Контент (Шаг 3) + PWA LOW вкладки
5. **Неделя 6:** Тестирование, полировка, релиз v5.0

---

## ✅ Что уже готово

- [x] Multi-user удалён из BACKLOG → `FROZEN.md`
- [x] ROADMAP обновлён (8 задач осталось)
- [x] DONE.md обновлён (100+ фич)
- [x] Тесты: 985/985 passing
- [x] PostgreSQL миграция (SQLAlchemy + Alembic)
- [x] PWA = CLI (18 вкладок, 40+ API endpoints)
- [x] Дизайн-система (3 темы, Rick persona, Fira Code)
- [x] Launcher GUI

## ⏳ Что нужно от тебя

- [ ] **Книги PDF:** 8+ книг по кибербезопасности → `knowledge_base/`
- [ ] **Видео:** Ссылки на YouTube или локальные MP4 → `media/videos/`
- [ ] **Звуки:** 5 MP3/WAV файлов → `media/sounds/`
- [ ] **Изображения:** Иконки, баннеры, схемы → `static/icons/`
- [ ] **Данные:** CVE, APT, CTF задачи (если есть) → `data/`

---

*CyberTeacher v5.0 Plan — 2026-05-18*
