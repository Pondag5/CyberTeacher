# Общее состояние проекта

Версия: **6.0**
Статус: **Стабильный, все фичи реализованы**
Последнее обновление: 2026-06-08

## Ключевые метрики
| Метрика | Значение |
|---------|----------|
| Python файлов | ~277 |
| Строк Python кода | ~44 000 |
| Handlers | 79 .py |
| API endpoints | ~140 REST + 3 WebSocket |
| PWA табов | 58 зарегистрировано |
| Тестов | ~129 (89 существующих + 40 новых) |
| LLM провайдеров | 6 (ollama, groq, openrouter, huggingface, lmstudio, mock) |
| Launcher кнопок | 34 |
| Docker сервисов | 2 (postgres:16 + pgadmin4) |

## Активные провайдеры
- **LM Studio:** Работает на `http://localhost:1234/v1`, 9 моделей
- **MockLLM:** Офлайн-заглушка, всегда доступен

## Ключевые файлы
- `api_server.py` — 3981 стр., FastAPI сервер
- `launcher.py` — 1109 стр., tkinter GUI + Provider Settings
- `config.py` — LazyLoader, все провайдеры
- `resilient_llm.py` — fallback chain + circuit breaker
- `handlers/` — 79 обработчиков команд

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

## Последние изменения (v6.0)
- Provider Settings окно в лаунчере (API keys + URL + Test Connection + Save)
- LM Studio интеграция (детекция, переключение)
- Чат: WebSocket теперь использует LazyLoader (полный fallback до MockLLM)
- 40 новых тестов для 7 ранее непокрытых хендлеров
- settings.py синхронизирован (добавлены lmstudio, mock)
- Очищена docs/ (удалено 8 мёртвых файлов)
- CI/CD: path filters, lint + test stages
- Исправлен дубль chat_stream(), починена сетка лаунчера
