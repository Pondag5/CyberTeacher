# Известные проблемы (KNOWN_ISSUES.md)

Последнее обновление: 2026-05-29

## Статус: Все критичные и высокоприоритетные проблемы решены ✅

### Решённые проблемы (все 11)
| # | Проблема | Решение |
|---|----------|---------|
| 1 | Context Budget не работал | `context_budget.py` — token-aware |
| 2 | Нет Provider Fallback | `resilient_llm.py` + MockLLM |
| 3 | Auto-summarize не подключён | Подключён в main loop |
| 4 | QueryCache неограничен | Capped 1000 + eviction |
| 5 | Unbounded lists в AppState | `_trim_unbounded_lists()` |
| 6 | Лог без ротации | RotatingFileHandler 5MB × 3 |
| 7 | LLM для оценки ответов | achievement_service (rule-based) |
| 8 | HANDLES сериализация | Исключён из JSON |
| 9 | Hidden knowledge unlock (dot-notation) | `_check_condition()` поддерживает `skills.web_security >= 3` |
| 10 | Dead code (src/) | Удалены `context_budget_manager.py`, `summarization_model.py` |
| 11 | context_awareness unreachable night | Исправлено: night 23-3, late_night 3-6 |

## Оставшиеся (декоративные / низкий приоритет)

| # | Проблема | Влияние | Статус |
|---|----------|---------|--------|
| 12 | FAISS embed_one_by_one — нет батчинга | Медленная индексация | ⏳ Не критично |
| 13 | Backup rotation не удаляет старые | Рост backups/ | ⏳ Не критично |
| 14 | `llm_total_tokens`/`llm_call_count` декоративные | Нулевое | ⏳ Косметика |
