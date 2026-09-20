# Improvement Plan — Teacher Brain & Knowledge Base

*Created: 2026-09-20*
*Status: In Progress*

---

## Goals

1. Make teacher memory reliable and observable
2. Make knowledge base fast and deterministic across restarts
3. Make learning events useful across all learning modes, not just quiz

---

## Tasks

### T1 — Persist BM25 index and verify reload
- Save BM25 to disk during `load_knowledge_base()`
- Load BM25 from disk on startup if FAISS index exists
- Add tests for BM25 persistence/reload
- Files: `knowledge.py`, `tests/test_knowledge.py`

### T2 — CLI /learning_memory command
- Show weak topics
- Show recent breakthroughs
- Show last N learning events
- Files: `handlers/misc.py`, `handlers/core.py`, `handlers/__init__.py`, `ui.py`

### T3 — API endpoints for learning memory
- `GET /api/learning/weak-topics`
- `GET /api/learning/similar-errors?query=...`
- `GET /api/learning/events?limit=...`
- Files: `api_server.py`

### T4 — Extend learning events sources
- Record failures from story submit
- Record lab start/stop/fail if available
- Record exploit failures if available
- Avoid noisy false positives; only record meaningful events
- Files: `handlers/misc.py`, `handlers/practice.py`, `handlers/exploits.py` if exists

### T5 — Personality drift in non-chat responses
- Reuse `apply_personality_drift()` in quiz feedback, story output, hints
- Keep it lightweight; no LLM needed
- Files: `personality.py`, `handlers/quiz.py`, `handlers/misc.py`, `handlers/story_mode.py`

### T6 — Embeddings model warm-up / caching
- Ensure embeddings model is loaded once and reused
- Avoid repeated lazy loads on first real request
- Files: `config.py`, `knowledge.py`

---

## Order

1. T1 — fast, removes a real reliability issue
2. T2 — quick, gives immediate user-facing value
3. T3 — depends on T2 concepts, useful for PWA
4. T4 — high value, low effort
5. T5 — medium effort, improves consistency
6. T6 — quick win if loader path is wrong

---

## Verification

- Run affected tests after each task
- Update `docs/IDEAS_STATUS.md` when complete
