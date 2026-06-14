# Bugs and Fixes

## 2026-06-05
- **NUMERIC_MENU** — config.py содержал маппинг только 1-13, хотя меню показывало до 72. Добавлены все цифры 0-72.
- **OSINT /api/threats** — импортировал несуществующую константу APT_GROUPS. Исправлен на загрузку из threats/*.json.

## 2026-05-29 (Sprint 11-16)
- STAB-01: Context overflow — Session too large to compact. Решение: Context Budget Manager.
- STAB-02: Нет fallback при лимитах Groq/OpenRouter. Решение: ResilientLLM.
- STAB-03: Дублирование памяти, утечки истории. Решение: _trim_unbounded_lists(), periodic cleanup.
- STAB-04: LLM нужен для ачивок/прогресса. Решение: achievement_service rule-based + MockLLM.
- BUG-01: world_state.py _check_condition() не работала dot-notation (skills.web_security >= 3). Fix: рекурсивный обход.
- BUG-02: context_awareness.py night (23-3), late_night (3-6) были недостижимы. Fix: исправлены условия.
- BUG-03: adaptive_ui.py — stray китайский символ 除非. Fix: удалён.
- BUG-04: handlers/context.py — missing conn = init_db(). Fix: добавлен.
- BUG-05: CachedLLM.stream() — не инкрементировал llm_call_count. Fix: добавлен.
- BUG-06: Dead code (src/context_budget_manager.py, src/summarization_model.py). Fix: удалены.
## 2026-06-09T21:53:57.536Z

Bullet list of bugs fixed, each with one-line root cause (write "None" if no bugs were fixed).

---

