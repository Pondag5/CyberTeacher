# Task Tracker — Alpha Readiness
# Source: /workspace/app/.kilo_memory/tasks/

## Completed
- [x] Add force_reindex() to knowledge.py (clears persist dir + rebuilds from source)
- [x] Update /reindex_knowledge CLI handler to use force_reindex()
- [x] Add POST /api/knowledge/reindex API endpoint
- [x] Wire up PWA risk_indicators component in dashboard (render + auto-update)
- [x] Create indexed memory storage (.kilo_memory/) with project index, symbols, endpoints, tests, decisions

## In Progress
- [ ] Project exploration & memory indexing (this session)

## Backlog (from AGENTS.md Next Actions)
- [ ] PWA: rewind UI
- [ ] PWA: secret room status
- [ ] P3 Long-term: Mobile, OAuth2, 2FA
- [ ] Knowledge Base: CLI/API команда принудительной переиндексации (DONE via force_reindex + endpoint)

## Validation
- [x] Python 3.13 installed via apt
- [x] pytest installed, 30/30 tests/test_knowledge.py pass
- [x] 46/50 tests in test_knowledge.py + test_api_integration.py pass
  (4 pre-existing failures: handlers/core.py:131 imports missing push_notifications)
- [x] ruff installed, no new lint errors in modified files
- [x] All modified Python files compile (py_compile OK)
- [ ] Run ruff . (full project lint)
- [ ] Run mypy . (typecheck)

## Notes
- Python and pytest now available in container.
- Memory storage located at /workspace/app/.kilo_memory/
- My changes are uncommitted (working tree only) — need `git add` + `commit` before alpha.
