# Changelog

All notable changes to CyberTeacher project.

## [Unreleased] – 2026-03-28/29

### Added (High Priority Features H-01..H-10)
- **H-01** — ASCII network topology via `/network` command (Rich tree visualization)
- **H-02** — RAM equipment system: `/tools` list, `/equip <tool>` to toggle tools with RAM costs (max 100)
- **H-03** — Trace timer for labs: `time_limit_minutes` in DOCKER_LABS, deadline + hint display in main loop
- **H-04** — Unified story campaign: sequential episodes, progress tracking, rewards
- **H-05** — Missions editor: JSON-based custom scenarios (`/missions`, `/mission start`, `/mission submit`)
- **H-06** — CVE lookup: `/cve <CVE-ID>` fetches from NVD API with 1h caching
- **H-07** — GitHub/GitLab secret scanner: `/scan <repo_url> [branch]` clones and scans for hardcoded secrets
- **H-08** — Metrics & health: `/health` shows uptime, LLM stats, cache hit rate, rate limiting usage
- **H-09** — Web UI (Streamlit): `web_ui.py` dashboard with tabs for system, network, labs, CVE, missions
- **H-10** — Documentation: full README update, ADRs (5), implementation plan

### Added (Subsequent Features M-25..M-30)
- **M-25** — HackTheBox integration: `/htb` commands (login, machines, machine details, submit flags, sync, status, walkthrough)
- **M-26** — Exploit walkthrough system: `/walkthrough <topic>` generates step-by-step exploitation guide; `/exploit <CVE>` searches for exploits
- **M-27** — PoC Verification: `/exploit_submit <mission_id> <step_order> <script>` validate exploit script in sandbox; mission steps require `accepts_exploit: true` and define `exploit_validation`. Success recorded in `state.exploit_success`.
- **M-28** — Learner Dashboard: `/dashboard` shows personal analytics (XP, stats, weak topics, track progress, activity counters) in a formatted overview.
- **M-29** — Path-based Adaptive Learning Tracks: `/tracks` commands (list, start, progress, next, complete, recommend, reset, status). YAML-defined tracks with topics, prerequisites, labs, quizzes. Adaptive selection based on weak_topics. Progress tracking with bonus XP. Includes 4 example tracks (web-fundamentals, network-security, privesc-master, ctf-prep).
- **M-30** — Real-time Hints: `/hint` (on/off/status/get/clear) with automatic pattern-based detection during input. Configurable patterns in `hints/patterns.json`. Credits (default 3), 10% XP penalty, cooldown 30s, per-session limit 3. Resets on mission/lab start.
- **M-31** — Bug Bounty Simulation (`/bounty`): Interactive report writing for simulated vulnerabilities. LLM acts as triage reviewer, scores report (0-100), provides feedback, awards XP (base 50 + score*2). Includes 5 scenarios (SQLi, XSS, CSRF, File Upload, IDOR). Learn responsible disclosure and report structure.

### Added (Infrastructure & Quality Q-01..Q-08)
- **Q-01** — Unit tests coverage >70% (359 tests passing, ~73% coverage)
- **Q-02** — CI/CD (GitHub Actions) with tests, coverage, lint, typecheck
- **Q-03** — Ruff + mypy integrated, lint fixes (deprecated typing, DTZ005, and more)
- **Q-04** — LLM instrumentation (time, tokens), cache hits/misses, `/health` metrics
- **Q-05** — Rate limiting: 10 requests per minute via sliding window in state
- **Q-06** — Automatic backups at startup + `/backup` command (app_state.json, news_cache.json)
- **Q-07** — Architecture Decision Records (5): LazyLoader, Hybrid RAG, LLM Caching, Singleton State, Rate Limiting
- **Q-08** — Dependency vulnerability scanning in CI (`pip-audit`)

### Improved
- Type hints: PEP 604 unions (`str | None`) across codebase
- Time handling: `datetime.now(UTC)` instead of naive datetime
- Bare excepts replaced with `except Exception` or `contextlib.suppress`
- Import sorting with `isort`
- Subprocess calls explicitly `check=False`
- Numerous lint warnings cleaned (RUF012, ARG004, PLW0603, PLR0913, E731, RUF034, B009, SIM117, RUF059, etc.)

### Fixed
- Test isolation issues for CI stability
- Indentation in `state.py` after multiple edits
- `get_cached_response` to properly increment cache hits/misses

## [Previous] – 2026-03-17
Initial public release (base functionality: CLI, LLM integration, RAG, Docker labs, story mode, etc.)
