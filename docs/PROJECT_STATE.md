# Общее состояние проекта

Версия: **6.0**
Статус: **Стабильный, все фичи реализованы**
Последнее обновление: 2026-09-18

## Ключевые метрики
| Метрика | Значение |
|---------|----------|
| Python файлов | ~277 |
| Строк Python кода | ~44 000 |
| Handlers | 79 .py |
| API endpoints | ~140 REST + 3 WebSocket |
| PWA табов | 58 зарегистрировано |
| Тестов | 105+ passed в ключевых модулях; 85 test файлов |
| LLM провайдеров | 6 (ollama, groq, openrouter, huggingface, lmstudio, mock) |
| Launcher кнопок | 34 |
| Docker сервисов | 2 (postgres:16 + pgadmin4) |
| DB таблиц | 16 |
| Story chapters | 8 (Signal → Convergence) |
| Story mechanics | 15/15 ✅ |
| Achievements | 29 |
| Shop items | 17 |

## Активные провайдеры
- **LM Studio:** Работает на `http://localhost:1234/v1`, 9 моделей
- **MockLLM:** Офлайн-заглушка, всегда доступен

## Ключевые файлы
- `api_server.py` — 3981 стр., FastAPI сервер
- `launcher.py` — 1109 стр., tkinter GUI + Provider Settings
- `config.py` — LazyLoader, все провайдеры
- `resilient_llm.py` — fallback chain + circuit breaker
- `handlers/` — 79 обработчиков команд
- `services/learning_memory_service.py` — память учителя об ошибках
- `knowledge.py` — FAISS + BM25 + RRF + query expansion

## Статус спринтов
| Спринт | Фокус | Статус |
|--------|-------|--------|
| 1–8 | Quick Wins, Analytics, PWA, Инфра | ✅ |
| 9 | State Migration | ✅ |
| 10 | Type Hints (mypy 0) | ✅ |
| 11 | Стабильность + Гибридная LLM | ✅ |
| 12 | Атмосфера и UX | ✅ |
| 13 | Persistent World + Cyberpsychosis | ✅ |
| 14–16 | WebSocket, Auth, Animations, Offline | ✅ |
| P1 | Security + Rate Limiting | ✅ |
| PWA | 58 табов, lazy-load | ✅ |
| **6.0** | **LM Studio, Provider Settings, launcher v6** | **✅** |
| **6.1** | **Learning Memory System, Knowledge Base Optimization** | **✅** |

## Последние изменения (v6.1)
- Learning Memory System: SQLite `learning_events`, semantic retrieval, personality insights
- Knowledge Base Optimization: категоризация, BM25 full-corpus, RRF fusion, query expansion
- Personality drift расширен параметрами из learning events
- GitHub repo description и topics обновлены
- Alembic миграция `cb007d8d52d1` применена