# Action Plan — High-Impact Improvements

*Created: 2026-09-20*
*Status: In Progress*

---

## P1 — Quick Wins (1-2 days each)

### A1 — Personality drift in all LLM responses
- Add `get_personality_prompt_modifiers()` to quiz feedback, hints, story narration
- Files: `personality.py`, `handlers/quiz.py`, `handlers/hints.py`, `handlers/misc.py`
- Status: partial helper exists, needs wiring

### A2 — PWA risk indicators
- Complete `static/js/components/risk_indicators.js`
- Show noise bar, trace progress, debt counter in PWA UI
- Files: `static/js/components/risk_indicators.js`, `static/js/tabs/*.js`

### A3 — Memory importance scoring
- Add `importance` field to `LearningEvent` (0.0-1.0)
- Weight retrieval by importance + recency
- Files: `services/learning_memory_service.py`, `db.py`

---

## P2 — Hardware Integration (1-3 days)

### B1 — ASUS 1001PX as target machine
- Install Debian 12 32-bit minimal + SSH
- Configure vulnerable services: FTP, Telnet, Samba, old PHP
- Static IP, isolated VLAN/guest network
- Integration: CyberTeacher task references fixed target IP
- Docs: update `IDEAS_FOR_NETBUK.md` with actual config

### B2 — Redmi 9A portable target (optional)
- Ubuntu Touch + OpenSSH
- One lightweight service at a time
- Use as "pocket target" for demos

---

## P3 — Polish (ongoing)

### C1 — Local LLM as primary (when GPU-ready)
- Switch LM Studio/Ollama from fallback to primary
- Keep cloud as fallback
- Files: `config.py`, `resilient_llm.py`

### C2 — Fake OS integration
- Daemon messages, hidden logs as atmospheric elements
- Files: `static/js/notifications_ws.js`, `handlers/ghost_log.py`

### C3 — Memory layer separation
- Split `memorable_events` into episodic/personality/story stores
- Files: `handlers/memory.py`, `services/learning_memory_service.py`

---

## Order

1. A1 — quick, improves all LLM responses
2. A3 — quick, improves retrieval quality
3. A2 — medium, visible to students
4. B1 — hardware, weekend project
5. B2 — optional, if B1 succeeds
6. C1-C3 — long-term, when GPU/deps ready

---

## Verification

- Run `pytest` after each task
- Update `docs/IDEAS_STATUS.md`
- Commit per feature
