# CyberTeacher — Документация

*Последнее обновление: 2026-06-08*

## Навигация

### Активные документы
| Файл | Описание |
|------|----------|
| [PROJECT_STATE.md](PROJECT_STATE.md) | Текущее состояние: метрики, статус, архитектура |
| [CHANGELOG.md](CHANGELOG.md) | Журнал изменений (v5.0 → v6.0) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Архитектура проекта: компоненты, data flow |
| [KNOWN_ISSUES.md](KNOWN_ISSUES.md) | Известные проблемы |
| [MEMORY_SUMMARY.md](MEMORY_SUMMARY.md) | Краткая память: ADR, структура, метрики |

### Гайды
| Файл | Описание |
|------|----------|
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Развёртывание: Docker, PostgreSQL, env |
| [ГАЙД_VM.md](ГАЙД_VM.md) | Настройка виртуальной машины |

### Видение
| Файл | Описание |
|------|----------|
| [cyberteacher_vision_ideas_masterfile.md](cyberteacher_vision_ideas_masterfile.md) | Long-term vision: личности, мир, фичи |

### ADR (Architectural Decision Records)
| Файл | Описание |
|------|----------|
| [adr/0001-lazy-loader.md](adr/0001-lazy-loader.md) | Lazy loading LLM/embeddings |
| [adr/0002-hybrid-rag.md](adr/0002-hybrid-rag.md) | Hybrid RAG: ChromaDB + BM25 |
| [adr/0003-llm-caching.md](adr/0003-llm-caching.md) | LLM response caching |
| [adr/0004-singleton-state.md](adr/0004-singleton-state.md) | Singleton AppState |
| [adr/0005-rate-limiting.md](adr/0005-rate-limiting.md) | Rate limiting |

---

## Быстрый старт

```bash
python launcher.py          # GUI панель управления
python -m uvicorn api_server:app --host 127.0.0.1 --port 8000  # API сервер
python main.py              # CLI интерфейс
```

**PWA:** `http://localhost:8000` — 58 табов, WebSocket чат, LM Studio / Ollama

*CyberTeacher v6.0 — 2026-06-08*
