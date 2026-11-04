# CyberTeacher: Audit Report

Generated: 2026-11-04

## Root .py Files (66 total)

### Entry Points (3)
- main.py - CLI entry point
- api_server.py - FastAPI REST/WebSocket server
- web_ui.py - Streamlit UI
- launcher.py - GUI launcher

### Business Logic (40)
adaptive_ui.py, assignment_generator.py, atmosphere.py, auth.py, behavior_profile.py, code_review.py, context_awareness.py, context_budget.py, course_manager.py, courses.py, cyberpsychosis.py, daily_challenge.py, db.py, di.py, episode_memory.py, generators.py, knowledge.py, labs.py, memory.py, news_fetcher.py, pedagogy.py, personality.py, persona_router.py, practice.py, question_generation.py, quiz_generator.py, quiz_multiplayer.py, report_generator.py, resilient_llm.py, scorm_export.py, smart_hints.py, state.py, story_mode.py, track_engine.py, web_tools.py, world_state.py

### Utilities (10)
confirm.py, i18n.py, logging_config.py, mock_llm.py, shared_types.py, terminal_log.py, tools.py, tools_ram.py, ui.py, precheck.py

### Tools (12)
build_index.py, export_project.py, faiss_watcher.py, fix_resilient.py, fix_resilient2.py, fix_syntax.py, generate_state_properties.py, generate_stete.py, index_project.py, mcp_server_faiss.py, mcp_server.py, rag_mcp_server.py, run_all_tests.py, search_faiss.py

### Config (2)
config.py, settings.py

## Subpackages (have __init__.py)
- utils/
- routes/
- models/
- services/
- handlers/

No src/ directory exists.

## Silent Failure Patterns (try/except ImportError: pass)
83 matches across ~30 files. Key offenders:
- api_server.py: 10+ locations
- main.py: 18+ locations
- handlers/*: multiple
- config.py: 1 location

## Global State
- get_state() defined in state.py:845 (canonical) and generate_stete.py:366 (legacy)
- ~200+ call sites in production code
- api_server.py: ~47 calls
- main.py: ~12 calls
- Multiple module-level singletons: world_state, personality, cyberpsychosis

## DI Infrastructure
di.py exists (125 lines):
- AppContext dataclass
- get_context(), set_context(), reset_context()
- @inject decorator
- Currently partially adopted

## Dependency Graph (acyclic)
- Leaf modules (import nothing): state, cyberpsychosis, personality, atmosphere, behavior_profile, context_awareness, world_state, config, settings, db, track_engine, pedagogy
- Hub modules: state (5 importers), config (4), knowledge (3)
- main.py imports: config, knowledge, pedagogy, state, context_budget, ui, code_review, generators
- api_server.py imports: 25+ root modules
- No circular imports detected