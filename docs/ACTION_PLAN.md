# Action Plan — High-Impact Improvements

*Created: 2026-09-20*
*Status: In Progress*

---

## Goals

1. Make teacher personality visible in every response, not only chat
2. Make risk state visible across all relevant PWA tabs
3. Prepare hardware target docs/setup for ASUS and Redmi
4. Keep learning memory reliable, observable, and weighted by importance

---

## Tasks

### A1 — Personality drift in all LLM responses
- Add `get_personality_prompt_modifiers()` to quiz feedback, hints, story narration
- Files: `personality.py`, `handlers/quiz.py`, `handlers/hints.py`, `handlers/misc.py`, `handlers/story_mode.py`
- Status: partial helper exists, needs wiring

### A2 — Risk indicators across PWA tabs
- Reuse `/api/noise`, `/api/trace`, `/api/debts`, `/api/stealth/toggle` in `labs.js`, `missions.js`, `progress.js`
- Keep `world.js` as reference implementation
- Files: `static/js/tabs/labs.js`, `static/js/tabs/missions.js`, `static/js/tabs/progress.js`

### B1 — ASUS 1001PX target machine docs/setup
- Document exact setup in `docs/IDEAS_FOR_NETBUK.md`
- Base image, SSH, vulnerable services, fixed IP
- No code changes required; docs + optional setup script

### B2 — Redmi 9A portable target
- Document lightweight service approach
- Optional SSH + one-container workflow
- Files: `docs/IDEAS_FOR_NETBUK.md`

### B3 — Hardware API references (optional)
- Optional API endpoints for target status if needed later
- Files: `api_server.py`

---

## Order

1. A1 — quick, improves all LLM responses
2. A2 — medium, visible to students
3. B1/B2 — docs first, hardware later
4. B3 — optional, only if needed

---

## Verification

- Run `pytest` after each task
- Update `docs/IDEAS_STATUS.md`
- Commit per feature
