# CyberTeacher v6.0 — Technical Architecture

*Last updated: 2026-06-10 | Version: 6.0*

---

## 🏗️ System Overview

CyberTeacher is a hybrid CLI/PWA cybersecurity education platform with an AI mentor persona. The architecture follows a **modular monolith** pattern with clear separation of concerns, dependency injection, and explicit data flow.

---

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            USER INTERFACES                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌──────────────────┐    ┌──────────────────────┐   │
│  │   CLI (Rich)    │    │  PWA (Vanilla JS) │    │  REST API (FastAPI)  │   │
│  │  main.py        │    │  static/ (58 tabs) │    │  api_server.py       │   │
│  │ handlers/ (79)  │    │  WebSocket (WS)   │    │  140+ endpoints      │   │
│  └────────┬────────┘    └────────┬─────────┘    └──────────┬───────────┘   │
└───────────┼──────────────────────┼──────────────────────────┼───────────────┘
            │                      │                          │
            ▼                      ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION CORE (DI Container)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  AppContext (di.py) ──→ state.py (AppState)  db.py (SQLAlchemy)  config.py │
│       │                                              │         (LazyLoader) │
│       ▼                                              ▼                      │
│  handlers/ (79) ←── Registry Pattern ──────→ resilient_llm.py (fallback)   │
│       │                                              │                      │
│       ▼                                              ▼                      │
│  services/ (achievement, weak_topics, etc.) ←──→ knowledge.py (RAG)         │
└─────────────────────────────────────────────────────────────────────────────┘
            │                                              │
            ▼                                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  SQLite (chat_history.db)     PostgreSQL (Docker)     FAISS (126 MB)       │
│  Alembic migrations                                    sentence-transformers│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Details

### 1. Backend Core

| File | Lines | Responsibility |
|------|-------|----------------|
| `main.py` | ~800 | CLI entry point, CachedLLM, main loop, signal handling |
| `api_server.py` | ~4000 | FastAPI app, 140+ REST endpoints, 3 WebSocket endpoints |
| `config.py` | ~600 | LazyLoader, get_llm(), providers, .env parsing |
| `di.py` | ~200 | AppContext container, @inject decorator |
| `state.py` | ~800 | AppState singleton (150+ attrs, 4 Pydantic modules) |
| `resilient_llm.py` | ~380 | Fallback chain, circuit breaker, retry, token tracking |

### 2. Handlers (79 modules)

```
handlers/
├── core.py              # Main dispatcher (1023 lines)
├── story_mode.py        # Story chapters, episodes, final choice
├── noise.py             # Noise level + stealth mechanics
├── trace.py             # Trace timer system
├── logs.py              # Dirty log management
├── debt.py              # Digital debt system
├── faction.py           # Faction reputation (Rick/Ghost/Archive)
├── echo.py              # Ghost student messages
├── memory.py            # Teacher memories
├── event_engine.py      # Narrative events (14 events)
├── ghost_log.py         # Ghost log (14 entries)
├── backdoor.py          # Backdoors (8 persistent)
├── secret_language.py   # Secret phrases (6 phrases)
├── persona_router.py    # Dynamic personas (4)
├── behavior_profile.py  # Hidden traits + archetypes
├── cyberpsychosis.py    # CP escalation (4 levels)
├── mood.py              # 5 communication styles
├── watchers.py          # Watchers counterattack
├── ghost_log.py         # Ghost log
├── ...                  # 50+ more handlers
```

**Pattern**: Registry-based dispatch (exact/prefix matching), `HandlerResult(success, data, error, continue_loop)`

### 3. LLM Providers & Resilient Chain

```
Fallback Chain: ollama → groq → openrouter → huggingface → lmstudio → mock
                    ↓              ↓           ↓            ↓            ↓
            Circuit Breaker: 3 failures → skip for 60s
            Retry: 2 attempts per provider with exponential backoff
            Timeout: 30s (Unix SIGALRM / Windows threading)
            MockLLM: Always available offline fallback
```

| Provider | Type | Config |
|----------|------|--------|
| Ollama | Local | `http://localhost:11434` |
| LM Studio | Local (OpenAI API) | `http://localhost:1234/v1` |
| Groq | Cloud (free) | `GROQ_API_KEY` |
| OpenRouter | Cloud (100+ models) | `OPENROUTER_API_KEY` |
| HuggingFace | Cloud | `HUGGINGFACE_API_KEY` |
| Mock | Offline stub | Always available |

**Circuit Breaker**: 3 failures → OPEN (skip 60s) → HALF_OPEN (test) → CLOSED

### 4. PWA Frontend (58 tabs, Vanilla JS)

```
static/
├── index.html                 # SPA shell
├── app.js                     # Tab registry + router (lazy-load)
├── manifest.json              # PWA manifest v3 (TWA ready)
├── sw.js                      # Service Worker v3 (Network First)
├── js/
│   ├── app.js                 # Tab registry + router
│   ├── components/
│   │   ├── risk_indicators.js  # Noise bar, Trace progress, Debt counter
│   │   ├── glitch.js           # 3AM Witching Hour + Debt Warning
│   │   ├── charts.js           # SVG charts (bar/line/radar)
│   │   └── heatmap.js          # 28-day activity heatmap
│   ├── tabs/                  # 58 tabs (chat.js, dashboard.js, etc.)
│   │   ├── chat.js            # WebSocket streaming chat
│   │   ├── dashboard.js       # XP, streak, skills
│   │   ├── story.js           # Story chapters
│   │   ├── labs.js            # Docker labs drag-drop
│   │   └── ...
│   ├── tabs/                  # 58 tabs
│   └── utils.js               # apiCall, OfflineDB, utils
```

**Service Worker v3**: Three cache stores (static, API, offline). Navigation: network → cached index → offline HTML. API: network-first with cache fallback. Static: cache-first with network update.

### 5. Launcher (tkinter GUI)

| Section | Buttons | Purpose |
|---------|---------|---------|
| **SERVER** | 5 | Start/Stop/Restart API, MCP, CLI |
| **DATABASE** | 5 | PostgreSQL, pgAdmin, Migrations, SQLite |
| **DOCKER** | 6 | Labs, Prune, Info |
| **PWA LINKS** | 6 | Open PWA, Dashboard, CTF, Labs, Writeups, Recon |
| **TOOLS** | 8 | Tests, KB, Logs, System Info, Env Config, Provider Settings |
| **SERVICES** | 4 | MCP Test, Dependencies, Memory Cleanup |

---

## 🗄️ Data Layer

### SQLAlchemy Models (16 tables)

| Model | Table | Purpose |
|-------|-------|---------|
| `Message` | `messages` | Chat history |
| `Stat` | `stats` | XP, quizzes, tasks |
| `TopicProgress` | `progress` | Topic mastery |
| `QueryCache` | `query_cache` | RAG query cache (1000 cap) |
| `AppStateRecord` | `app_state` | State persistence (JSON) |
| `Achievement` | `achievements` | 29 achievements |
| `Skill` | `skills` | Skill tracker |
| `Flag` | `flags` | CTF flags |
| `Purchase` | `purchases` | Shop history |
| `HTBMachine` | `htb_machines` | HTB sync |
| `THMRoom` | `thm_rooms` | TryHackMe sync |

### Vector Store (FAISS)

| Metric | Value |
|--------|-------|
| Index size | ~126 MB |
| Chunks | ~2500 |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Hybrid search | FAISS + BM25 + Cross-encoder rerank |

---

## 🔄 Data Flows

### 1. User Request (CLI/PWA)
```
User Input → Registry → Handler → DI (LLM, Knowledge, State) → Result
                                    ↓
                            LLM Request → ResilientLLM (fallback chain)
                                    ↓
                            Response → Cache (SQLite TTL) → Handler → User
```

### 2. LLM Request Flow
```
Prompt → ResilientLLM.invoke()
  → Try primary (ollama) with retry (2) + timeout (30s)
  → On failure: circuit breaker check → fallback to next provider
  → On success: circuit.record_success()
  → On failure: circuit.record_failure() → fallback
  → MockLLM as ultimate fallback
```

### 3. State Persistence
```
AppState (singleton) → save_to_file() / load_from_file()
  → JSON (default) or PostgreSQL (STATE_BACKEND=db)
  → Debounced save (2s throttle)
  → _trim_unbounded_lists() caps all lists
```

### 4. LLM Request/Response Caching
```
Query → SHA256 hash → SQLite cache (TTL 24h, max 1000 entries)
  → Hit: return cached response
  → Miss: call LLM → store in cache → return
```

---

## 🔐 Security

| Layer | Implementation |
|-------|----------------|
| **Auth** | JWT (HMAC-SHA256), bcrypt passwords |
| **API** | Rate limiting (10 req/min sliding window) |
| **Headers** | CSP, HSTS, X-Content-Type-Options, X-Frame-Options |
| **CORS** | Configurable origins (default: all for dev) |
| **Secrets** | `.env` only, pydantic-settings, no hardcoded secrets |
| **Containers** | Non-root user, read-only FS, no network (sandbox) |

---

## 📦 Deployment

### Docker Compose (Production)
```yaml
services:
  cyberteacher:
    build: .
    ports: ["8501:8501"]
    volumes:
      - ./memory:/app/memory
      - ./knowledge_base:/app/knowledge_base
    environment:
      - LLM_PROVIDER=ollama
      - OLLAMA_BASE_URL=http://ollama:11434

  ollama:
    image: ollama/ollama
    ports: ["11434:11434"]
    volumes: [ollama_data:/root/.ollama]

  postgres:  # optional
    image: postgres:16
    environment:
      POSTGRES_DB: cyberteacher
      POSTGRES_PASSWORD: ${DB_PASSWORD}
```

### Resource Requirements

| Profile | CPU | RAM | SSD | GPU |
|---------|-----|-----|-----|-----|
| Minimal | 4 cores | 8 GB | 50 GB | — |
| Recommended | 8 cores | 16 GB | 100 GB | NVIDIA 8+ GB VRAM |
| Classroom (20 students) | 16 cores | 32 GB | 200 GB | NVIDIA 16+ GB VRAM |

---

## 🧪 Testing & Quality

| Tool | Command | Target |
|------|---------|--------|
| Tests | `python -m unittest discover -s tests` | 1268 passed |
| Lint | `ruff check .` | 0 errors |
| Types | `mypy . --ignore-missing-imports` | 0 errors |
| Coverage | `coverage run -m unittest` | ~95% |

---

## 🔌 Extension Points

| Extension | How |
|-----------|-----|
| **New Handler** | Create `handlers/xxx.py`, register in `handlers/__init__.py` |
| **New LLM Provider** | Implement `invoke()`/`stream()`, add to `config.py` fallback chain |
| **New PWA Tab** | Add `static/js/tabs/xxx.js`, register in `app.js:TABS` |
| **New Story Event** | Add JSON to `events/narrative_events.json` |
| **New Track** | Add YAML to `tracks/` |
| **New Achievement** | Add to `data/achievements.json` |

---

## 📊 Monitoring & Observability

| Metric | Endpoint |
|--------|----------|
| Health | `GET /health` |
| LLM Stats | `GET /api/llm/stats` |
| Cache Stats | `GET /api/cache/stats` |
| DB Stats | `GET /api/db/stats` |
| Metrics | `GET /metrics` (Prometheus format) |

---

*Last updated: 2026-06-10 | CyberTeacher v6.0*