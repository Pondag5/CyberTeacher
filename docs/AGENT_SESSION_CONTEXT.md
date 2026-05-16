# 📌 AGENT SESSION CONTEXT — CyberTeacher

> **Updated:** 2026-05-16  
> **Purpose:** Compressed session state for agent continuity.

---

## 🚀 PROJECT OVERVIEW

**CyberTeacher** — Python CLI for cybersecurity education with LLM teacher.
- **LLM:** Ollama/VL Studio (qwen2.5)
- **RAG:** Chroma + sentence-transformers
- **UI:** Rich (CLI)
- **DB:** SQLite
- **Tests:** unittest (830 tests, 825 passing)
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
| REF-04 | Dependency Injection (phase 1) | ✅ Container created, phase 2 pending |

### i18n Localization
| Feature | Files |
|---------|-------|
| Russian/English UI | `locales/ru.json`, `locales/en.json` |
| Localization engine | `i18n.py` |
| `/lang` command | `handlers/lang.py` |
| Teacher prompts | `config/teacher_prompts.json` (ru + en) |
| Language field | `settings_state.py` |

### Dependency Injection (REF-04)
| Component | Status |
|-----------|--------|
| `di.py` — AppContext container | ✅ Created |
| `@inject` decorator | ✅ Created |
| `get_context()/set_context()` | ✅ Created |
| `handlers/core.py` — Context initialization | ✅ Migrated |
| Handler migration (phase 2) | ⏳ Pending |

### New Tests (64 total this session)
| File | Tests | Coverage |
|------|-------|----------|
| `test_services.py` | 23 | Services (weak topics, spaced repetition, skills, achievements) |
| `test_settings.py` | 8 | Pydantic Settings validation |
| `test_profile_handler.py` | 8 | Profile handler |
| `test_health_handler.py` | 3 | Health metrics |
| `test_theme_handler.py` | 10 | Theme switching |
| `test_hints_handler.py` | 12 | Hints system |
| `test_i18n.py` | 10 | Localization engine |
| `test_lang_handler.py` | 4 | `/lang` command |
| `test_ctf_flags.py` | 12 | CTF flag generation/verification |
| `test_cve_handler.py` | 5 | CVE lookup with caching |
| `test_skills_handler.py` | 11 | Skills, reputation, depth |

---

## 📊 TEST STATUS

- **Total:** 851 tests
- **Passing:** 846
- **Failing:** 1 (Ollama not running — environment)
- **Skipped:** 4 (external services)
- **Coverage:** ~95%+ (all handlers covered)

### Recent Test Additions (7 tests)
| File | Tests | Coverage |
|------|-------|----------|
| `test_web_ui.py` | 7 | Web UI helper functions (XP history, heatmap) |

---

## 🎯 REMAINING TASKS

| Priority | ID | Task | Notes |
|----------|----|------|-------|
| 🟡 Medium | REF-04 | Dependency Injection (phase 2) | Migrate handlers to use ctx.state instead of get_state() |
| 🟢 Low | L-07 | Translate comments to English | Open-source readiness |
| 🟡 Medium | Q-02 | Coverage >90% | ✅ DONE — ~95% reached, all handlers covered |
| ✅ Done | M-28 | Web UI: XP graphs, heatmap | ✅ DONE — Enhanced dashboard with 6 tabs |

---

## 🔑 KEY PATTERNS

1. **State:** `get_state()` → singleton `AppState` with 4 Pydantic modules
2. **Config:** `get_settings()` → singleton `Settings` (pydantic-settings)
3. **DI:** `get_context()` → `AppContext` with state, settings, db_conn, llm, kb
4. **Services:** Pure functions, no state mutation
5. **Tests:** `unittest.mock` for `get_state()` and `console`
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
| `services/` | Business logic |
| `locales/` | Translation files |

---

## ⚠️ KNOWN ISSUES

1. **Ollama not running** — 1 test error (environment)
2. **Windows UnicodeEncodeError** — Console encoding issue
3. **Pydantic v1 warning** — Python 3.14 + langchain-core (harmless)

---

## 🔄 NEXT STEPS

1. REF-04 phase 2: Migrate handlers to use `ctx.state` instead of `get_state()`
2. M-28: Web UI enhancements (XP graphs, heatmap)
3. L-07: Translate comments to English

---

*Update this file after each major session.*
