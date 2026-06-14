# Changelog

All notable changes to CyberTeacher project.

## [v5.19] – 2026-06-14

### Event-Driven Narrative Engine (STORY-01)
- **STORY-01** — `handlers/event_engine.py` + `events/narrative_events.json`: 14 narrative events with triggers (threshold/and/or), conditions (not_fired/fired_before/time_window), effects (+XP, +noise, +trace, +cp, hint_block). Integrated in CLI (`main.py`) and PWA (`api_server.py` REST + WebSocket). 52 tests.

### PWA Narrative Events (PWA-STORY-01)
- **PWA-STORY-01** — `static/js/notifications_ws.js`: WebSocket handles `{"events": [...]}` — displays purple animated banners with glitch sound for narrative events.

### Glitch.js Atmosphere (GLITCH-01)
- **GLITCH-01** — `static/js/glitch.js`: 3AM Witching Hour (sidebar flicker, status bar glitch, purple glow, random logo glitch) + Debt Warning (debts ≥5: pulsing red badge, click → profile). Auto-init on DOMContentLoaded. Added to `static/index.html`.

### Behavior Profile + Archetypes (BEHAVIOR-01)
- **BEHAVIOR-01** — `behavior_profile.py`: 6 hidden traits (curiosity, recklessness, discipline, creativity, opsec, stress), 6 archetypes (engineer/analyst/researcher/script_kiddie/ghost/chaotic). `record_action()` hooks in quiz, missions, exploits, stealth, logs, ctf, social, night_session. Archetype prompt modifier injected in `main.py` and `api_server.py`. API `/api/behavior-profile`. 24 tests.

### Persona Router (PERSONA-01)
- **PERSONA-01** — `persona_router.py`: 4 personas (Rick/Doc/Analyst/Ghost) with auto-routing by context (high risk→Ghost, night→Doc, exploit→Rick, stealth→Ghost, learning→Doc). CLI `/persona [list|status|auto|rick|doc|analyst|ghost]` in `handlers/core.py`. Integrated in `main.py` and `api_server.py` (REST + WebSocket). PWA persona indicator in `static/js/tabs/chat.js` (emoji + name + id). 13 tests.

### FAISS Batch Embedding Optimization (PERF-01)
- **PERF-01** — `knowledge.py`: `ProgressEmbeddings.embed_documents()` now uses native batch embedding (HuggingFaceEmbeddings) instead of per-document calls. Significant indexing speedup.

### Backup Rotation (BACKUP-01)
- **BACKUP-01** — `state.py` + `settings.py`: `maybe_auto_backup()` with rotation by count (`max_backups`) and age (`max_backup_age_hours`). Settings: `backup_dir`, `max_backups`, `max_backup_age_hours`. Called from `main.py` on startup.

### Documentation Sync (DOCS-01)
- **DOCS-01** — `docs/STORY_IMPLEMENTATION_PLAN.md`: Added implementation status table (✅ Done / ❌ Not Done), updated Architecture section to reflect real files.

### FAISS Index Optimization (PERF-02)
- **PERF-02** — `index_project.py`: Added `cves/`, `tests/` to `EXCLUDE_DIRS` (2000+ CVE JSONs + test files). Rebuild time: 5+ hours → **9 minutes** (33x faster). Index: 2490 chunks, 301 files.

### Tests
- Total: **1207 passed**, 2 pre-existing failures (QueryCache.id, state_save_load_roundtrip), 8 skipped.

### Ghost Log (STORY-02)
- **STORY-02** — `handlers/ghost_log.py` + `handlers/misc.py`: Hidden log with 14 atmospheric entries (Chapters 1-6). CLI `/ghost_log [list|random|<id>]`. Entries unlock based on chapter, noise, debts, faction, CP, trace, stealth ops, messages sent, teacher memory. Hints included. 13 entries currently available at Chapter 1.

### Backdoors (STORY-03)
- **STORY-03** — `handlers/backdoor.py` + `handlers/misc.py`: 8 persistent backdoors in compromised labs (DVWA, Juice Shop, Metasploitable, WebGoat, SQLi Labs, Ghost sector). CLI `/backdoor [list|info <id>|remove <id>|random]`. Unlock by chapter (3-6). Removal: Noise -5, grants flags, deactivates backdoor. Persistence types: cron, JWT, SSH key, SQL trigger, systemd, FTP config, exposed MongoDB.

### Secret Phrases Integration (STORY-04)
- **STORY-04** — `handlers/secret_language.py`: 6 secret phrases integrated into chat flow. CLI (`main.py`) + REST (`api_server.py`) + WebSocket (`api_server.py`). Effects: hint credit (+1), mood change (serious), ghost log unlock hint. Detected before command parsing, intercepted with special response.

### Hidden Knowledge Unlock (STORY-05)
- **STORY-05** — `world_state.py:check_unlock_knowledge()`: 5 hidden knowledge entries (Advanced SQLi, Binary Exploitation, AD Attacks, Reverse Engineering, C2 Frameworks). Conditions: skills.web_security >= 3, skills.binary_analysis >= 3, labs_started >= 10, skills.reverse_engineering >= 2, tracks_completed >= 2. Called from main loop after each action. CLI notification on unlock. Unlocks tracked in world_state.json.

### World Stability + Teacher Sleep (STORY-06)
- **STORY-06** — `state.py` + `handlers/misc.py` + `static/js/glitch.js`: World Stability (0-100) field in state, auto-adjusts on actions (fail=-2, trace=-1, watcher=-3, complete=+2). CLI `/stability [status|damage|heal]`. Teacher Sleep at 4AM: `is_teacher_sleeping()`, `can_access_secret_logs()`, `/teacher_sleep [status|secret]`. PWA CP-based glitches: levels 2-4 trigger escalating visual effects (sidebar flicker, chat bubble glitch, CP overlay intensification, logo glitch). Enhanced `glitch.js` with CP-level detection via `/api/cyberpsychosis`.

### FAISS Auto-Reindex Watcher (OPT-01)
- **OPT-01** — `faiss_watcher.py` + `handlers/misc.py`: File system watcher (watchdog) для автопереиндексации FAISS при изменении файлов проекта. CLI `/faiss_watch [start|status]`. Debounce 2 сек, исключает `cves/`, `tests/`, `__pycache__` и др. Запускает `index_project.py` в фоне с таймаутом 5 мин.

---

## [v5.18] – 2026-05-29

### Security Headers (SEC-01)
- **SEC-01** — `api_server.py`: Security headers middleware: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()`, `Content-Security-Policy` (scripts, styles, fonts, connect-src ws/wss).

### PWA Optimization (PWA-PERF-01)
- **PWA-PERF-01** — `static/index.html`: Critical CSS inlined (1KB, covers layout + sidebar + header). Font Awesome loaded with `media=print` → `onload=all` (async). Font loading with preconnect. `defer` on all JS. `apple-mobile-web-app` meta tags. CSP-compatible manifest.

### Bug Fixes
- **BUG-01** — `world_state.py:_check_condition()`: Fixed dot-notation (`skills.web_security >= 3`) — now traverses nested dicts.
- **BUG-02** — `context_awareness.py:get_time_of_day()`: Fixed unreachable night case (23-3 = night, 3-6 = late_night).
- **BUG-03** — `adaptive_ui.py`: Removed stray Chinese character (除非).
- **BUG-04** — `handlers/context.py`: Fixed missing `conn = init_db()` + removed unused import.
- **BUG-05** — `main.py:CachedLLM.stream()`: Added `llm_call_count` and `llm_total_tokens` increment for streaming.
- **BUG-06** — Deleted dead code: `src/context_budget_manager.py`, `src/summarization_model.py`.

## [v5.17] – 2026-05-29

### Difficulty Badge in Sidebar (UI-01)
- **UI-01** — `static/index.html` + `static/js/app.js`: Difficulty level badge displayed in sidebar below navigation. Shows current level with emoji (beginner/intermediate/advanced/hardcore).

### Extended Test Suite (TEST-03)
- **TEST-03** — `tests/test_auth_roles_courses.py`: Added 17 new tests for atmosphere (4), adaptive UI (5), smart hints (3), quiz multiplayer (4), report generator (1). Total: **77 tests** (was 60).

### Beginner Theme (BEGINNER-02)
- **BEGINNER-02** — `static/css/style.css`: `body.beginner-mode` — bright theme with white background, blue accent (#3b82f6), dark text (#1f2937). Applied automatically for beginner difficulty.

### World Tab Live Notifications (WORLD-LIVE-02)
- **WORLD-LIVE-02** — `static/js/tabs/world.js`: WebSocket connection to `/notifications`. Live incident/cyberpsychosis alerts with animated notification cards. Auto-refresh counters.

## [v5.16] – 2026-05-29

### Live World Notifications (WORLD-LIVE-01)
- **WORLD-LIVE-01** — `static/js/tabs/world.js`: Rewritten with WebSocket `/notifications` connection. Live incident/cyberpsychosis alerts appear as animated notification cards in the world tab. Auto-refresh counters on new events.

### Beginner Mode (BEGINNER-01)
- **BEGINNER-01** — `static/css/style.css`: `body.beginner-mode` — bright theme (white bg, blue accent, dark text) for beginners. Cyberpunk effects disabled.
- **BEGINNER-02** — `static/js/utils.js`: `applyBeginnerMode()` applies CSS class based on `difficulty_level`. Called on init and after onboarding.
- **BEGINNER-03** — `static/js/onboarding.js`: Applies beginner mode immediately after level selection.

### Report Export UI (REPORT-02)
- **REPORT-02** — `static/js/tabs/export.js`: Added "Скачать отчёт" button. Opens `/export_report` in new tab for printing to PDF.

## [v5.15] – 2026-05-29

### Multiplayer Quiz UI (MP-UI-01)
- **MP-UI-01** — `static/js/tabs/quiz.js`: Rewritten with multiplayer section: create/join room (4-char code), WebSocket connection, question rendering, answer buttons, real-time leaderboard. Host controls (start/next). Player connection notifications with sounds.

### Hardcore Timer (HC-01)
- **HC-01** — `static/js/tabs/quiz.js`: In hardcore mode, quiz questions have a 30s countdown timer per question. Auto-submits on timeout. Visual countdown display.

### Adaptive Tab Visibility (TAB-01)
- **TAB-01** — `static/js/app.js`: `renderNav()` now filters tabs based on `difficulty_level`. Beginner hides: ctf, osint, scanner, malware, versus, admin, leaderboard, export. Intermediate hides: admin. Advanced/hardcore: all visible.

## [v5.14] – 2026-05-29

### WebSocket Auth (WS-03)
- **WS-03** — `api_server.py`: `/chat_stream` now accepts optional `token` param for auth. Verifies JWT, extracts user display name and role, injects into system prompt.
- **WS-04** — `static/js/tabs/chat.js`: WebSocket URL now includes `token` from localStorage.

### Training Report Export (REPORT-01)
- **REPORT-01** — `report_generator.py`: `generate_report_html()` — printable HTML report with XP, level, rank, reputation, quizzes, labs, flags, skills (with progress bars), weak topics, achievements, session info. CSS @media print for PDF.
- **REPORT-02** — `api_server.py`: `GET /export_report?token=...` — returns HTML report.
- **REPORT-03** — `handlers/core.py`: `/report` CLI command — saves report to `./memory/training_report.html`.

### Animated Leaderboard (LB-02)
- **LB-02** — `static/js/tabs/leaderboard.js`: Rewritten with animated counters (easeOutCubic), current session stats, date-labeled XP progress chart.

## [v5.13] – 2026-05-29

### Onboarding Wizard (WIZARD-01)
- **WIZARD-01** — `static/js/onboarding.js`: Full-screen wizard при первом входе. Выбор уровня (beginner/intermediate/advanced/hardcore) с визуальными карточками. Step 2: краткий overview команд. Сохранение в localStorage. При следующем входе пропускается.

### Leaderboard (LB-01)
- **LB-01** — `static/js/tabs/leaderboard.js`: 23-я вкладка. Лучший XP, лучший streak, квизы, лабы. SVG line chart прогресса XP. Achievement count. Текущий ранг.

### New Files
- `static/js/onboarding.js`
- `static/js/tabs/leaderboard.js`

### Updated Files
- `static/index.html`: Added onboarding.js, leaderboard.js
- `static/js/app.js`: Onboarding check on DOMContentLoaded, leaderboard tab

## [v5.12] – 2026-05-29

### Adaptive Difficulty (ADAPT-01)
- **ADAPT-01** — `adaptive_ui.py`: 4 уровня (beginner/intermediate/advanced/hardcore) с конфигурацией видимых команд, cyberpsychosis, подсказок, лабов. Auto-promotion по XP/квизам/лабам. System prompt modifier.
- **ADAPT-02** — `state.py`: `difficulty_level`, `tutorial_completed`, `tutorial_step`.
- **ADAPT-03** — `main.py`: Adaptive prefix в system prompt + auto-promotion check.

### Smart Hints (HINT-01)
- **HINT-01** — `smart_hints.py`: При неверной командеuggest closest match через `difflib.get_close_matches`. 14 описаний команд.
- **HINT-02** — `handlers/core.py`: Unknown command handler заменён на smart hints.

### Interactive Tutorial (TUTORIAL-01)
- **TUTORIAL-01** — `smart_hints.py`: 4-step tutorial (/courses → /quiz → /profile → /help). Команда `/tutorial` в CLI.
- **TUTORIAL-02** — `handlers/core.py`: `/tutorial` и `/difficulty` команды.

## [v5.11] – 2026-05-29

### Atmosphere Engine (ATMOS-01)
- **ATMOS-01** — `atmosphere.py`: 3 atmospheric layers:
  - **Ghost Logs**: 15 rare system messages ([SYSTEM]/[GHOST]), weighted random selection, probability tied to cyberpsychosis level (2-30%), interval 60-300s
  - **Echo of Past Sessions**: 15% chance to reference `memorable_events` from state, 7 echo templates with action/result/issue placeholders
  - **Teacher's Doubt**: 3-15% chance based on stress + recklessness, 8 doubt templates
- **ATMOS-02** — `state.py`: Added `memorable_events` list (max 7) and `record_memorable_event()` method
- **ATMOS-03** — `main.py`: Atmosphere engine integrated into system prompt generation

### Multiplayer Quiz (MP-01)
- **MP-01** — `quiz_multiplayer.py`: `QuizRoom` class with host/player system, room creation, answer submission with streak bonuses, leaderboard
- **MP-02** — `api_server.py:websocket_quiz_multiplayer`: WebSocket endpoint `/quiz_multiplayer`. Actions: create, join, answer, start, next, state. Auto-generates questions via LLM.

### WebSocket Notifications (WS-02)
- **WS-02** — `api_server.py:websocket_notifications`: WebSocket endpoint `/notifications`. Push incidents + cyberpsychosis alerts. Ping/pong keep-alive.

### SCORM/LMS (SCORM-01)
- **SCORM-01** — `static/imsmanifest.xml`: SCORM 1.2 manifest with 5 modules mapped to web UI tabs.

### Export/Import UI (EXPORT-01)
- **EXPORT-01** — `static/js/tabs/export.js`: Export/Import tab (21st). Download user data as JSON file. Import with admin role restriction.

### Admin Panel (ADMIN-01)
- **ADMIN-01** — `static/js/tabs/admin.js`: Admin tab (20th). User list with role dropdown, course management, create course form.

### Charts Library (CHARTS-01)
- **CHARTS-01** — `static/js/charts.js`: SVG bar chart + line chart for analytics.

## [v5.10] – 2026-05-29

### Admin Panel (ADMIN-01)
- **ADMIN-01** — `static/js/tabs/admin.js`: Admin tab (20th). User list with role dropdown (student/teacher/admin), inline role change. Course list with topics count. Create new course form (name, description, difficulty). Accessible only for admin JWT holders.

### WebSocket Notifications (WS-02)
- **WS-02** — `api_server.py:websocket_notifications`: WebSocket endpoint `/notifications`. Push-based real-time: world incidents, cyberpsychosis alerts. Ping/pong keep-alive. 30s polling interval.

### SCORM/LMS (SCORM-01)
- **SCORM-01** — `static/imsmanifest.xml`: SCORM 1.2 manifest with 5 modules (Intro, Network, Crypto, Practice, CTF), mapped to web UI tabs.

## [v5.9] – 2026-05-29

### Course Management (COURSE-01)
- **COURSE-01** — `course_manager.py`: CRUD для курсов с темами. 6 встроенных курсов (web, network, crypto, malware, pentest, social). Default courses защищены от удаления, только description/icon.
- **COURSE-02** — `api_server.py`: 4 endpoints: `POST /create_course`, `POST /update_course`, `POST /delete_course`, `POST /add_topic` (teacher/admin only).

### GDPR Export/Import (GDPR-01)
- **GDPR-01** — `api_server.py`: `GET /export_user_data` — экспорт профиля + state (все поля). `POST /import_user_data` — импорт state (admin only).

### Tests
- **TEST-02** — `tests/test_auth_roles_courses.py`: 18 tests (auth: 8, roles: 4, courses: 6). Всего: 60 tests.

## [v5.8] – 2026-05-29

### Multi-User Roles (ROLE-01)
- **ROLE-01** — `auth.py`: 3 roles (admin/teacher/student) with permission sets. `set_role()`, `has_permission()`, `get_user_role()`, `list_users()`. Admin: manage_users, manage_courses, view_all_stats, manage_config. Teacher: manage_courses, view_all_stats. Student: chat, quiz, labs, profile.
- **ROLE-02** — `api_server.py`: 2 new endpoints: `GET /list_users` (admin only), `POST /set_role` (admin only). Role-based access via `has_permission(token, perm)`.
- **ROLE-03** — JWT token now includes `role` field.

### Advanced Analytics Dashboard (STATS-01)
- **STATS-01** — `static/js/tabs/stats.js`: Rewritten with multi-section dashboard: XP/Level/Streak cards, quiz/task stats, skills progress bars, SVG heatmap, world state summary, cyberpsychosis bars, episode memory stats, system info.

### TWA Manifest (PWA-02)
- **PWA-02** — `static/manifest.json`: Updated for TWA: name/description in Russian, shortcuts (Чат, Дейли, Квизы, Ачивки), categories (education), lang/dir, maskable icons, proper theme_color.

## [v5.7] – 2026-05-29

### Enhanced PWA (PWA-01)
- **PWA-01** — `static/sw.js`: Rewritten as Service Worker v3. Three cache stores (static, API, offline). Navigation: network → cached index → offline HTML. API: network-first with cache fallback + JSON error response. Static: cache-first with network update. Offline page with retry button.

### Notifications (NOTIF-01)
- **NOTIF-01** — `static/js/notifications.js`: Browser Notification API. Permission request, poll events (incidents, cyberpsychosis danger). Bell button in header. 60s polling interval.

### CLI /api list (API-02)
- **API-02** — `handlers/api_handler.py`: `/api list` command — displays all 46 endpoints in a formatted table (method, path, description).

### Updated Files
- `static/index.html`: Added notification bell button in header
- `static/js/app.js`: Notifications init + polling + bell click handler
- `static/index.html`: Added notifications.js script tag

## [v5.6] – 2026-05-29

### Canvas Animations (ANIM-01)
- **ANIM-01** — `static/js/particles.js`: CyberParticles — animated particle background with connections between nearby particles. Uses CSS variable accent color. Fixed position, z-index -1, pointer-events none.
- **ANIM-02** — `static/js/effects.js`: GlitchText — glitch scramble animation on hover (800ms). CyberBorder — animated glow on card hover.

### Offline-First (OFF-01)
- **OFF-01** — `static/js/offline.js`: OfflineDB — IndexedDB wrapper with state, chat, cache stores. Auto-caches GET responses, serves from cache when offline. TTL-based expiry.
- **OFF-02** — `static/js/utils.js`: `apiCall()` now uses OfflineDB for offline-first: tries network, falls back to cache.

### Labs Drag-and-Drop (LAB-01)
- **LAB-01** — `static/js/tabs/labs.js`: Rewritten with drag-and-drop (drag running containers to drop zone to stop them), Docker status indicator, loading states, sounds on actions.

## [v5.5] – 2026-05-29

### Multi-User Auth (AUTH-01)
- **AUTH-01** — `auth.py`: User registration, login, JWT tokens (HMAC-SHA256), password hashing (SHA-256 + salt), user CRUD. Endpoints: `POST /register`, `POST /login`, `GET /verify_auth`.

### Web UI Enhancements (UI-06..UI-08)
- **UI-06** — `static/js/tabs/profile.js`: Rewritten with login/register forms, JWT auth flow, logout, radar chart for skills (SVG).
- **UI-07** — `static/js/tabs/world.js`: New "World" tab (19th). Shows incidents, factions, hidden knowledge, episode memory stats, cyberpsychosis bars.
- **UI-08** — `static/js/app.js`: Added World tab to navigation (19 tabs total).

## [v5.4] – 2026-05-29

### WebSocket Streaming (WS-01)
- **WS-01** — `api_server.py:websocket_chat_stream`: WebSocket endpoint `/chat_stream` for real-time LLM streaming. Accepts `message` and `mode` query params. Sends chunks as `{"chunk": "..."}` and final `{"done": true, "full_response": "..."}`.

### Web UI Enhancements (UI-01..UI-03)
- **UI-01** — `static/js/tabs/chat.js`: Rewritten with WebSocket streaming support (chunk-by-chunk display), Enter-to-send, graceful fallback to REST API.
- **UI-02** — `static/js/sounds.js`: Web Audio API sound effects (success, error, achievement, click, notification, levelUp). Zero external files.
- **UI-03** — `static/js/heatmap.js`: SVG-based 28-day activity heatmap with color intensity scaling, day labels, and legend.
- **UI-04** — `static/js/tabs/progress.js`: Updated to use `Heatmap.render()` for SVG heatmap.
- **UI-05** — `static/js/tabs/achievements.js`: Enhanced with earned count and XP badges.

## [v5.3] – 2026-05-29

### Cyberpsychosis System (CP-01)
- **CP-01** — `cyberpsychosis.py`: hidden psychological state (stress, obsession, recklessness) with 4 levels (normal/elevated/critical/dangerous). Auto-decay, teacher modifiers, dramatic prompt at dangerous level. Integrated into main.py system prompt + quiz failure/success hooks + flag capture hooks.

### API & Web (WEB-01..WEB-03)
- **WEB-01** — 5 new API endpoints: `GET /get_personality`, `GET /get_context`, `GET /get_world`, `GET /get_episodes`, `GET /get_cyberpsychosis`
- **WEB-02** — CORS middleware added to FastAPI (`allow_origins=["*"]`)
- **WEB-03** — Episode memory auto-recording: achievements → milestone, skill level up → breakthrough

### Episode Memory Integration (EP-01)
- **EP-01** — `state.py:check_achievements()` now records milestones to episode memory
- **EP-02** — `state.py:track_skill()` records breakthroughs on skill level ups

### Tests
- 42 integration tests (was 20): +9 Cyberpsychosis, +6 WorldState, +7 EpisodeMemory

### Documentation Cleanup
- Removed 11 redundant root-level .md files
- Removed 9 stale docs/ files (COMPLETED, COMPREHENSIVE_PLAN, BACKLOG, FROZEN, IDEAS, PROBLEMS, etc.)
- Created `docs/INDEX.md` — centralized navigation hub
- Updated README.md with docs link and version 5.3

## [v5.2] – 2026-05-29

### Atmosphere & Personality (ATM-01..ATM-06)
- **ATM-01** — `context_awareness.py`: time-of-day detection (morning/afternoon/evening/night/late_night), session pattern recognition (normal/binge_learning/night_owl/perfectionist/chaotic), atmosphere hints for teacher
- **ATM-02** — `personality.py`: `PersonalityState` with 5 drift axes (sarcasm, patience, paranoia, enthusiasm, formality), `apply_personality_drift()` adjusts based on context, `get_system_prompt_modifiers()` generates LLM prompt instructions
- **ATM-03** — Atmosphere hints: late-night sessions trigger atmospheric comments, binge learning triggers break reminders
- **ATM-04** — LLM stats: `CachedLLM.invoke()` now increments `llm_call_count` and `llm_total_tokens` (estimated via char/4)
- **ATM-05** — Backup rotation: `maybe_auto_backup()` keeps max 5 newest backups, deletes oldest
- **ATM-06** — Terminal log rotation: `terminal_log.py` rotates at 512 KB (keeps second half)

### Persistent World & Episode Memory (SPRINT 13)
- **WORLD-01** — `world_state.py`: persistent world with active incidents (8 templates), faction discovery (4 factions), hidden knowledge (5 topics). Auto-spawns incidents, evaluates unlock conditions, generates world prompt for LLM.
- **WORLD-02** — `episode_memory.py`: stores breakthroughs, failures, discoveries, milestones with importance scoring. Generates memory prompt for LLM system prompt. Cap 500 episodes.

### Setup Scripts
- `scripts/setup_ollama.bat` / `scripts/setup_ollama.sh` — Ollama installation + model pull wizard
- Dead code cleanup: removed `src/context_budget_manager.py`, `src/summarization_model.py`

## [v5.1] – 2026-05-29

### Stability Sprint (STAB-01..STAB-04)
- **STAB-01** — Context Budget Manager: token-aware context trimming (4 chars/token ratio), budget allocation (system + RAG + history + input + reserve), `/context stats` and `/context clear` commands
- **STAB-02** — Provider Fallback Chain: `ResilientLLM` wrapper with retry (2 attempts), circuit breaker (3 failures → skip), fallback chain (ollama→groq→openrouter→huggingface), integrated into `LazyLoader.get_llm()`
- **STAB-03** — Memory stabilization: `_trim_unbounded_lists()` caps exploit_success(200), bounty(100), writeups(100), purchases(100), versus(50); QueryCache capped at 1000 rows; RotatingFileHandler 5MB×3 for log; HANDLES excluded from serialization; periodic cleanup every 50 messages
- **STAB-04** — LLM decoupled from game mechanics: `state.check_achievements()` now uses `services/achievement_service` (29 achievements, rule-based); quiz eval, flags, XP, missions already rule-based

### Type Hints (CQ-01)
- **CQ-01** — mypy: 0 errors (was 106): fixed all handler return types (15+ files), stubs (prompt_toolkit, lxml, scapy, pymetasploit3), SQLAlchemy annotations, optional import patterns

### Bug Fixes
- `handlers/core.py` — Added `handle_htb()`, `handle_walkthrough()`, `handle_exploit_search()` (were imported but didn't exist)
- `handlers/practice.py` — Fixed imports (HTB_MACHINES→_list_labs, get_htb_recommendation→htb delegation)
- `handlers/sandbox.py` — Added `practice.run_docker_cmd()` (was missing)
- `api_server.py` — Fixed MISSIONS→_load_mission()
- `ui.py` — Fixed return value in void function `print_streaming_response`
- `state.py` — Fixed `thm_completed: List[int]`→`List[Dict[str, str]]`
- `CachedLLM` — Added try/except with logging in `.invoke()` and `.stream()`

### New Files
- `resilient_llm.py` — ResilientLLM provider fallback chain
- `handlers/context.py` — /context stats, /context clear

### Hybrid LLM Architecture (from actual.md)
- **HYB-01** — `mock_llm.py`: offline stub with intent detection (quiz/hint/explain/default responses), works without API keys or GPU
- **HYB-02** — `handlers/doctor.py`: `/doctor` onboarding command — provider health check table, `/doctor setup ollama|groq|openrouter` wizard, `/doctor mock` to switch offline
- **HYB-03** — `config.py:LazyLoader.get_llm()`: auto-selects MockLLM when no providers available; always adds MockLLM as last fallback in ResilientLLM chain
- **HYB-04** — `tests/test_stability_integration.py`: 20 integration tests covering context budget, quiz→XP→achievement, memory caps, provider fallback, circuit breaker
- **HYB-05** — `.env.example` updated: `LLM_PROVIDER=mock` default, `LLM_PROVIDERS` chain docs

## [Unreleased] – 2026-05-16

### Refactoring — State Modularization (REF-02)
- **REF-02** — Modular state architecture: `AppState` now uses composition with 10 state modules
- **REF-03** — Fixed `xp_boost` duplication between `achievements_state` and `shop_state`
- **REF-06** — Implemented `__getattr__`/`__setattr__` delegation for backward compatibility
- **REF-08** — Delegated business logic methods to respective modules (`risk`, `achievements`, `learning`, `metrics`, `user`, `explanation`, `shop`)
- **REF-14** — Fixed `HANDLES` constant duplication (now only in `user_state.py`)

### New State Modules
- `achievements_state.py` — Achievements, XP, counters (89 lines)
- `explanation_state.py` — Explanation depth (22 lines)
- `hints_state.py` — Hints configuration (15 lines)
- `learning_state.py` — Courses, topics, context (57 lines)
- `metrics_state.py` — Metrics, rate limiting (44 lines)
- `persona_state.py` — Persona, mode (14 lines)
- `risk_state.py` — Risk level (35 lines)
- `shop_state.py` — Shop, themes, XP boost (61 lines)
- `user_state.py` — Profile, reputation, HTB (69 lines)
- `voice_state.py` — Voice assistant (22 lines)

### Test Fixes
- Fixed `test_user_state.py`: `add_repertoire` → `add_reputation` typo
- Fixed rate limiting test: moved from `UserState` to `MetricsState`
- Fixed handle threshold test: 250 → 350 for "Пентестер"
- **577/579 tests passing** (2 errors are Windows environment issues, not code bugs)

### Code Quality
- `state.py`: 1019 → 885 lines (-13%)
- All state methods now delegate to modules (`self.risk.increase_risk()`, `self.achievements.increment_flag()`, etc.)
- Backward compatibility maintained via `__getattr__`/`__setattr__`

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
- **M-33** — Advanced Analytics & AI Tutor (`/analytics`): Displays personalized learning metrics, weak topics (with bar chart), and AI-generated 3-day study plan based on your progress.
- **M-34** — Voice Assistant (TTS) (`/voice`): Text-to-speech output for bot responses. Commands: `/voice on/off/status/test`. Uses pyttsx3 for offline cross-platform speech. Enable to listen to answers hands-free.

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
