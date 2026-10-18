# Decision Log — CyberTeacher Alpha Readiness
# Source: /workspace/app/.kilo_memory/decisions/

## Decision 1 (2026-10-16) — FORCE_REINDEX for knowledge base
Problem: CLI /reindex_knowledge called load_knowledge_base() which only rebuilds if no
persistent index exists (load_knowledge_base checks os.path.exists(PERSIST_DIR) and loads
it without re-reading source files). No way to force a full rebuild from source files.
Solution: Added force_reindex() in knowledge.py (line 256) that deletes PERSIST_DIR,
resets _INDEX_TIMESTAMP/_current_vectordb/_bm25_index/_all_docs_store, clears KB cache,
and calls load_knowledge_base() to rebuild from knowledge_base/ + docs/.
Updated CLI handler handlers/misc.py:1184 to use force_reindex().
Added API endpoint POST /api/knowledge/reindex (api_server.py:3488).
Files changed: knowledge.py, handlers/misc.py, api_server.py

## Decision 2 (2026-10-16) — PWA risk indicators via shared component
Problem: renderRiskIndicators() component (static/js/components/risk_indicators.js) was
loaded in index.html but never called. Dashboard tab (dashboard.js:43-83) had inline
duplicated rendering for noise/trace/debt.
Solution: Dashboard now calls renderRiskIndicators(riskInner) + updateRiskIndicators()
instead of inline HTML. Component provides auto-update every 10s via setInterval.
Files changed: static/js/tabs/dashboard.js

## Pending decisions
- My changes (force_reindex, KB API endpoint, dashboard component) are in working tree
  but NOT committed. Need to commit before alpha release.
- Python 3.13 installed via apt, pytest/ruff available. Tests: 30/30 knowledge pass,
  46/50 knowledge+api_integration pass (4 pre-existing failures from missing
  push_notifications module in handlers/core.py:131).
- Next Actions from AGENTS.md: PWA rewind UI, secret room status; KB forced reindex CLI/API
  (DONE); P3: Mobile, OAuth2, 2FA.
