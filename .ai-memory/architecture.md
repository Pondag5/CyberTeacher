# Architecture

**Data Flow:** CLI/PWA → handle_extended_commands() / API → handlers/*.py → state.py (AppState singleton) → services/ → db.py (SQLAlchemy)

**LLM Layer:** LazyLoader → ResilientLLM (retry 2 + circuit breaker 3) → fallback chain (ollama→groq→openrouter→hf→mock). MockLLM — offline stub.

**Storage:** JSON files (state) + SQLite/PostgreSQL (messages, cache, achievements) + ChromaDB (RAG)

**Key modules:** context_budget.py (token-aware), personality.py (5 drift axes), cyberpsychosis.py (stress/obsession/recklessness), world_state.py (incidents/factions), episode_memory.py

**PWA:** 22 tabs, lazy-loaded, Service Worker v4, OfflineDB (IndexedDB), WebSocket streaming (/chat_stream, /notifications, /quiz_multiplayer)
