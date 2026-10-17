# Action Plan — High-Impact Improvements

*Created: 2026-09-20*
*Status: In Progress*

---

## Goals

1. Make teacher personality visible in every response, not only chat
2. Make risk state visible across all relevant PWA tabs
3. Prepare hardware target docs/setup for ASUS and Redmi
4. Keep learning memory reliable, observable, and weighted by importance
5. Close remaining P1/P2 platform gaps from docs/ROADMAP.md

---

## Completed

- A1 — Personality drift wiring: helper, code review, quiz, hints, story mode
- A2 — Risk indicators: API endpoints + world/labs/missions/progress tabs
- B1/B2 — Netbuk docs: ASUS + Redmi plans in `docs/IDEAS_FOR_NETBUK.md`
- B3 — Target API: `/api/targets`, `/api/targets/{target_id}/status`
- C1 — Service Worker stale-while-revalidate
- C2 — DB connection pooling verification: `QueuePool` already in `db.py`
- C3 — LLM caching verification: `ResponseCache` already in `memory.py` + `handlers/core.py`
- D1 — API key rotation: programmatic `.env` update + rotation tests in `tests/test_handlers_core.py`
- D2 — JWT/ENC hardening docs: section added to `docs/DEPLOYMENT_GUIDE.md`
- D3 — PWA achievements/dashboard risk integration: risk indicators in `achievements.js`, `dashboard.js` already had them

---

## Next

### P1/P2 — Remaining platform gaps from `docs/ROADMAP.md`
- Review `docs/ROADMAP.md` for remaining P1/P2 items
- Prioritize based on project needs

---

## Order

1. C1 — quick PWA win
2. C2/C3 — quick verification/docs
3. D1/D2 — security hygiene
4. D3 — optional polish

---

## Verification

- Run `pytest` after each task
- Update `docs/IDEAS_STATUS.md`
- Commit per feature

## Current Status

- All action plan items (C1-D3) completed
- 1163 tests passing (4 pre-existing fastapi import errors unrelated to changes)
- D1: `/keys rotate` now performs programmatic rotation with `.env` persistence
- D2: JWT/ENC hardening documented in `docs/DEPLOYMENT_GUIDE.md`
- D3: Risk indicators added to `achievements.js`; `dashboard.js` already had them
