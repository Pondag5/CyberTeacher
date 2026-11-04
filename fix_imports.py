#!/usr/bin/env python3
"""
Fix imports in src/handlers/*.py to use src/ package paths.
"""
import re
from pathlib import Path

# Mapping from root-level module names to their new src/ locations
MODULE_MAP = {
    # src.core
    "config": "src.core.config",
    "state": "src.core.state",
    "db": "src.core.db",
    "di": "src.core.di",
    "settings": "src.core.settings",
    "generators": "src.core.generators",
    "i18n": "src.core.i18n",
    "logging_config": "src.core.logging_config",
    "shared_types": "src.core.shared_types",
    "tools": "src.core.tools",
    "web_tools": "src.core.web_tools",
    "auth": "src.core.auth",
    # src.knowledge
    "knowledge": "src.knowledge.knowledge",
    "faiss_watcher": "src.knowledge.faiss_watcher",
    "build_index": "src.knowledge.build_index",
    "index_project": "src.knowledge.index_project",
    "search_faiss": "src.knowledge.search_faiss",
    # src.utils
    "utils.common": "src.utils.common",
    "utils.console_encoding": "src.utils.console_encoding",
    "utils.security": "src.utils.security",
    # src.services
    "services.learning_memory_service": "src.services.learning_memory_service",
    "services.skill_tracker_service": "src.services.skill_tracker_service",
    "services.achievement_service": "src.services.achievement_service",
    "services.spaced_repetition_service": "src.services.spaced_repetition_service",
    "services.weak_topics_service": "src.services.weak_topics_service",
    # src.gamification
    "story_mode": "src.gamification.story_mode",
    "track_engine": "src.gamification.track_engine",
    "world_state": "src.gamification.world_state",
    "courses": "src.gamification.courses",
    "course_manager": "src.gamification.course_manager",
    "daily_challenge": "src.gamification.daily_challenge",
    # src.personas
    "persona_router": "src.personas.persona_router",
    "personality": "src.personas.personality",
    "atmosphere": "src.personas.atmosphere",
    "behavior_profile": "src.personas.behavior_profile",
    "context_awareness": "src.personas.context_awareness",
    "cyberpsychosis": "src.personas.cyberpsychosis",
    "pedagogy": "src.personas.pedagogy",
    # src.prompt_engine
    "context_budget": "src.prompt_engine.context_budget",
    # src.cli
    "ui": "src.cli.ui",
    "web_ui": "src.cli.web_ui",
    "launcher": "src.cli.launcher",
    "main": "src.cli.main",
    # src.api
    "api_server": "src.api.api_server",
    # src.models (these are imported as models.xxx)
    "models.achievements_state": "src.models.achievements_state",
    "models.explanation_state": "src.models.explanation_state",
    "models.hints_state": "src.models.hints_state",
    "models.learning_state": "src.models.learning_state",
    "models.metrics_state": "src.models.metrics_state",
    "models.persona_state": "src.models.persona_state",
    "models.progress_state": "src.models.progress_state",
    "models.risk_state": "src.models.risk_state",
    "models.settings_state": "src.models.settings_state",
    "models.shop_state": "src.models.shop_state",
    "models.state_models": "src.models.state_models",
    "models.user_profile_state": "src.models.user_profile_state",
    "models.user_state": "src.models.user_state",
}

# Modules that remain at root (NOT moved to src/) - DO NOT REPLACE
ROOT_MODULES = {
    "adaptive_ui", "code_review", "memory", "news_fetcher", "practice",
    "quiz_generator", "report_generator", "resilient_llm", "smart_hints",
    "terminal_log", "tools_ram", "scorm_export", "question_generation",
    "quiz_multiplayer", "rag_mcp_server", "mcp_server", "mcp_server_faiss",
    "mock_llm", "labs", "confirm", "generate_state_properties", "export_project",
    "run_all_tests", "run_move", "refactor_step1", "fix_resilient", "fix_resilient2",
    "fix_syntax", "move_services", "bubblewrap_build",
}

# Third-party libraries (do not replace)
THIRD_PARTY = {
    "apscheduler", "base64", "censys", "collections", "contextlib", "cryptography",
    "datetime", "glob", "hashlib", "json", "logging", "os", "pathlib", "pymetasploit3",
    "pywebpush", "random", "re", "requests", "rich", "scapy", "secrets", "shodan",
    "shutil", "socket", "sqlalchemy", "struct", "subprocess", "tempfile", "time",
    "traceback", "typing", "urllib", "uuid", "yaml",
    "functools", "itertools", "dataclasses", "enum", "math", "textwrap", "string",
    "html", "http", "email", "ssl", "asyncio", "concurrent", "multiprocessing",
    "threading", "queue", "weakref", "copy", "pickle", "csv", "xml", "argparse",
    "getopt", "getpass", "sys", "platform", "inspect", "importlib", "pkgutil",
    "warnings", "numbers", "fractions", "decimal", "statistics", "zoneinfo",
    "collections.abc", "contextvars", "types", "operator", "builtins",
}

# Handlers internal (relative imports) - these should become relative
HANDLERS_MODULES = {
    "handlers.achievements", "handlers.analytics", "handlers.api_handler",
    "handlers.assignment_templates", "handlers.backdoor", "handlers.bug_bounty",
    "handlers.code_review_v2", "handlers.code_scan", "handlers.config",
    "handlers.context", "handlers.core", "handlers.ctf_flags", "handlers.cve",
    "handlers.daily", "handlers.dashboard", "handlers.debt", "handlers.docker_gen",
    "handlers.doctor", "handlers.echo", "handlers.emotions", "handlers.equipment",
    "handlers.event_engine", "handlers.exploit_submit", "handlers.exploit_trainer",
    "handlers.faction", "handlers.features", "handlers.flags", "handlers.ghost_log",
    "handlers.health", "handlers.hints", "handlers.history", "handlers.htb",
    "handlers.investigation", "handlers.jupyter", "handlers.lang", "handlers.logs",
    "handlers.malware_analysis", "handlers.media", "handlers.memory", "handlers.mermaid",
    "handlers.metasploit", "handlers.misc", "handlers.missions", "handlers.mood",
    "handlers.network", "handlers.news", "handlers.noise", "handlers.offline",
    "handlers.osint", "handlers.pcap_analyzer", "handlers.phantom_lab",
    "handlers.phantom_messages", "handlers.phishing", "handlers.practice",
    "handlers.profile", "handlers.push_notifications", "handlers.pwa", "handlers.quiz",
    "handlers.rewind", "handlers.sandbox", "handlers.secret_language",
    "handlers.secret_room", "handlers.shodan_censys", "handlers.shop", "handlers.skills",
    "handlers.social", "handlers.summarize", "handlers.summary", "handlers.sync",
    "handlers.theme", "handlers.threats", "handlers.timeloop", "handlers.trace",
    "handlers.tracks", "handlers.tryhackme", "handlers.types", "handlers.versus",
    "handlers.walkthroughs", "handlers.watchers", "handlers.writeup_auto",
}

def resolve_module(module: str) -> str | None:
    """Resolve a module name to its new src/ path, or return None if no change needed."""
    # Handlers internal - convert to relative
    if module in HANDLERS_MODULES or module.startswith("handlers."):
        if module == "handlers.types":
            return ".types"
        elif module.startswith("handlers."):
            return "." + module[len("handlers."):]
        else:
            return "." + module
    
    # Direct mapping
    if module in MODULE_MAP:
        return MODULE_MAP[module]
    
    # First part mapping (e.g., utils.common -> src.utils.common)
    parts = module.split(".")
    if parts[0] in MODULE_MAP:
        return MODULE_MAP[parts[0]] + "." + ".".join(parts[1:])
    
    # Skip root modules
    if parts[0] in ROOT_MODULES:
        return None
    
    # Skip third-party
    if parts[0] in THIRD_PARTY:
        return None
    
    return None

def fix_imports_in_file(filepath: Path) -> tuple[int, list[str]]:
    """Fix imports in a single file. Returns (changes_made, list_of_changes)."""
    content = filepath.read_text(encoding="utf-8")
    
    # Detect line ending style
    if "\r\n" in content:
        line_ending = "\r\n"
    else:
        line_ending = "\n"
    
    # Split WITHOUT keeping line endings
    lines = content.splitlines()
    changes = []
    
    # Regex patterns (without line ending)
    from_pattern = re.compile(r'^(\s*)from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import\s+(.+)$')
    # import X or import X as Y
    import_pattern = re.compile(r'^(\s*)import\s+([a-zA-Z_][a-zA-Z0-9_.]*)(?:\s+as\s+\w+)?\s*$')
    
    for i, line in enumerate(lines):
        # Skip comments
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        
        # Match: from X import Y
        m = from_pattern.match(line)
        if m:
            indent = m.group(1)
            module = m.group(2)
            rest = m.group(3)
            
            new_module = resolve_module(module)
            if new_module:
                lines[i] = f"{indent}from {new_module} import {rest}"
                changes.append(f"Line {i+1}: from {module} import -> from {new_module} import")
                continue
        
        # Match: import X (single import, possibly with alias)
        m = import_pattern.match(line)
        if m:
            indent = m.group(1)
            module = m.group(2)
            
            new_module = resolve_module(module)
            if new_module:
                lines[i] = f"{indent}import {new_module}"
                changes.append(f"Line {i+1}: import {module} -> import {new_module}")
                continue
    
    new_content = line_ending.join(lines)
    if not new_content.endswith(line_ending):
        new_content += line_ending
    
    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        return len(changes), changes
    return 0, []

def main():
    handlers_dir = Path("src/handlers")
    py_files = list(handlers_dir.glob("*.py"))
    print(f"Found {len(py_files)} handler files")
    
    total_changes = 0
    for f in py_files:
        changes_count, changes = fix_imports_in_file(f)
        if changes_count > 0:
            print(f"\n{f.name}: {changes_count} changes")
            for c in changes:
                print(f"  {c}")
            total_changes += changes_count
    
    print(f"\nTotal changes: {total_changes}")

if __name__ == "__main__":
    main()