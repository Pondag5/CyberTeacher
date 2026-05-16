# 📌 AGENT SESSION CONTEXT — CyberTeacher

> **Updated:** 2026-05-17  
> **Purpose:** Compressed session state for agent continuity.

---

## 🚀 PROJECT OVERVIEW

**CyberTeacher** — Python CLI for cybersecurity education with LLM teacher.
- **LLM:** Ollama/VL Studio (qwen2.5)
- **RAG:** Chroma + sentence-transformers
- **UI:** Rich (CLI) + Streamlit (Web)
- **DB:** SQLite
- **Tests:** unittest (851 tests, 850 passing)
- **Coverage:** ~95%+ (all handlers covered)

---

## ✅ COMPLETED (ALL PUSHED TO `main`)

### Refactoring (REF-05 — REF-15, REF-04 phase 1)
| ID | Task | Status |
|----|------|--------|
| REF-05 | Mode enum → `shared_types.py` | ✅ |
| REF-06 | `__getattr__` → explicit `@property` | ✅ |
| REF-07 | 10 state modules → Pydantic v2 | ✅ |
| REF-08 | `check_achievements` → `services/` | ✅ |
| REF-09 | JSON validation via Pydantic | ✅ |
| REF-10 | Secrets → `.env` | ✅ |
| REF-12 | Paths → `.env` | ✅ |
| REF-13 | 10 state modules → 4 consolidated | ✅ |
| REF-14 | Pydantic Settings | ✅ |
| REF-15 | Business logic → services | ✅ |
| REF-04 | Dependency Injection (phase 1) | ✅ Container created |

### i18n Localization
- `locales/ru.json`, `locales/en.json` — UI translations
- `i18n.py` — Localization engine with `t(lang, 'ui.key')`
- `handlers/lang.py` — `/lang` command
- `config/teacher_prompts.json` — ru + en prompts
- `settings_state.py` — `language` field

### Web UI (M-28)
- `web_ui.py` — Enhanced Streamlit dashboard (6 tabs)
- XP over time chart, activity heatmap, skill bars
- Settings management (language, mode)
- `tests/test_web_ui.py` — 7 tests

### Dependency Injection (REF-04)
- `di.py` — AppContext container with state, settings, db_conn, llm, kb
- `@inject` decorator for handler injection
- `get_context()/set_context()/reset_context()` for lifecycle
- `handlers/core.py` — Context initialized in `handle_commands()`

### REF-04 Phase 2 — DI Migration (IN PROGRESS)
Мигрировано 12 обработчиков с `get_state()` → `get_context().state`:
- `health.py`, `theme.py`, `profile.py`
- `lang.py`, `daily.py`, `news.py`
- `quiz.py`, `skills.py`, `config.py`
- `features.py`, `ctf_flags.py`, `emotions.py`

Осталось мигрировать ~41 обработчик:
`analytics`, `bug_bounty`, `dashboard`, `equipment`, `hints`, `htb`, `missions`, `network`, `phishing`, `shop`, `social`, `voice`, `writeup_auto`, `sync`, `media`, `jupyter`, `investigation`, `malware_analysis`, `exploit_trainer`, `history`, `osint`, `misc`, `mermaid`, `summarize`, `tracks`, `practice`, `exploit_submit`, `code_scan`, `cve`, `flags`, `achievements`, `threats`, `assignment_templates`, `export_extended`, `timeloop`, `voice_stt`, `shodan_censys`, `subscribe`, `core` (частично)

### Tests (851 total)
- Все 60+ обработчиков покрыты (100% handler coverage)
- Services, settings, DI, web_ui протестированы
- ~95%+ общее покрытие
- 850 passing, 1 env error, 4 skipped

---

## 🎯 REMAINING TASKS

| Priority | ID | Task | Notes |
|----------|----|------|-------|
| 🟡 Medium | REF-04 | DI Phase 2 | ~41 handlers: `get_state()` → `ctx.state` |
| 🟢 Low | L-07 | Translate comments | English for open-source |

---

## 🔑 KEY PATTERNS

1. **State:** `get_state()` → singleton `AppState` with 4 Pydantic modules
2. **Config:** `get_settings()` → singleton `Settings` (pydantic-settings)
3. **DI:** `get_context()` → `AppContext` with state, settings, db_conn, llm, kb
4. **Services:** Pure functions, no state mutation
5. **Tests:** `unittest.mock` for `get_context()` and `console`
6. **i18n:** `t(lang, 'ui.key')` for translations
7. **Language:** Code in English, docs/comments in Russian

---

## 📁 CRITICAL FILES

| File | Purpose |
|------|---------|
| `state.py` | Core state orchestration |
| `settings.py` | Typed configuration |
| `di.py` | Dependency injection container |
| `i18n.py` | Localization engine |
| `handlers/core.py` | Command dispatcher (DI initialized) |
| `handlers/lang.py` | Language switching |
| `web_ui.py` | Streamlit dashboard |
| `services/` | Business logic |
| `locales/` | Translation files |

---

## ⚠️ KNOWN ISSUES

1. **Ollama not running** — 1 test error (environment)
2. **Windows UnicodeEncodeError** — Console encoding issue
3. **Pydantic v1 warning** — Python 3.14 + langchain-core (harmless)

---

## 🔄 NEXT STEPS

1. REF-04 Phase 2: Migrate remaining ~41 handlers to use `ctx.state` instead of `get_state()`
2. L-07: Translate comments to English

---

*Update this file after each major session.*
