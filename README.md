# CyberTeacher — Документация

*Последнее обновление: 2026-09-18*

## Навигация

### Активные документы
| Файл | Описание |
|------|----------|
| [FEATURES_EXISTING.md](FEATURES_EXISTING.md) | **Все реализованные фичи** — полный список того, что работает сейчас |
| [FEATURES_PLANNED.md](FEATURES_PLANNED.md) | **Запланированные фичи** — приоритезированный бэклог |
| [ROADMAP.md](ROADMAP.md) | **Дорожная карта** — спринты, RICE, таймлайн |
| [ARCHITECTURE.md](architecture/ARCHITECTURE.md) | **Архитектура** — компоненты, data flow, безопасность |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | **Развёртывание** — Docker, сеть, бэкапы, мониторинг |
| [CURRENT_TASK.md](CURRENT_TASK.md) | **Текущая задача** — спринт, статус, следующие шаги |
| [PROJECT_STATE.md](PROJECT_STATE.md) | **Состояние проекта** — метрики, статус спринтов |
| [CHANGELOG.md](CHANGELOG.md) | **Журнал изменений** — v5.0 → v6.0 |
| [DONE.md](DONE.md) | **Реализованные фичи** — детально по спринтам |
| [KNOWN_ISSUES.md](KNOWN_ISSUES.md) | **Известные проблемы** — решенные и открытые |
| [MEMORY_SUMMARY.md](MEMORY_SUMMARY.md) | **Краткая память** — ADR, паттерны, метрики |

---

## Гайды
| Файл | Описание |
|------|----------|
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Развёртывание: Docker, PostgreSQL, env |
| [ГАЙД_VM.md](ГАЙД_VM.md) | Настройка виртуальной машины |

### Видение
| Файл | Описание |
|------|----------|
| [cyberteacher_vision_ideas_masterfile.md](cyberteacher_vision_ideas_masterfile.md) | Long-term vision: личности, мир, фичи |
| [IDEAS_FOR_NETBUK.md](IDEAS_FOR_NETBUK.md) | 8 планов для нетбука как полигона |

### ADR (Architectural Decision Records)
| Файл | Описание |
|------|----------|
| [adr/0001-lazy-loader.md](adr/0001-lazy-loader.md) | Lazy loading LLM/embeddings |
| [adr/0002-hybrid-rag.md](adr/0002-hybrid-rag.md) | Hybrid RAG: ChromaDB + BM25 |
| [adr/0003-llm-caching.md](adr/0003-llm-caching.md) | LLM response caching |
| [adr/0004-singleton-state.md](adr/0004-singleton-state.md) | Singleton AppState |
| [adr/0005-rate-limiting.md](adr/0005-rate-limiting.md) | Rate limiting |

---

## Новое: память учителя об ошибках

- **LearningMemoryService** — локальная долгосрочная память в SQLite (`learning_events`)
- Хранит: тему, тип события, `user_belief`, `correct_model`, `root_cause`, `resolution`
- Семантический retrieval через embeddings + cosine similarity
- Подключается к чату: учитель получает `[PAST SIMILAR MISTAKES]` и `[LEARNING INSIGHTS]`
- Personality drift теперь реагирует на слабые темы, частые ошибки и breakthrough'ы

См.: `services/learning_memory_service.py`, `db.py`, `personality.py`, `handlers/quiz.py`, `api_server.py`

---

## Быстрый старт

```bash
python launcher.py          # GUI панель управления
python -m uvicorn api_server:app --host 127.0.0.1 --port 8000  # API сервер
python main.py              # CLI интерфейс
```

**PWA:** `http://localhost:8000` — 58 табов, WebSocket чат, LM Studio / Ollama

---

## Ключевые метрики (v6.0)
- **Тесты:** 1268 passed, 0 fail, 8 skip
- **Handlers:** 79
- **PWA Tabs:** 58
- **Story Mechanics:** 15/15 ✅
- **Risk Mechanics:** Noise/Trace/Debt/Stealth ✅
- **Factions:** Rick/Ghost/Archive ✅
- **Cyberpsychosis:** 4 levels, PWA glitches ✅
- **Teacher Memory:** learning events + semantic retrieval ✅

---

*CyberTeacher v6.0 — 2026-09-18*