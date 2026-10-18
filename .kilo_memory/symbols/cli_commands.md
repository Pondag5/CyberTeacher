# Symbol Index — All CLI Commands (handlers/core.py:360+)
# Source: /workspace/app/handlers/core.py

## Simple commands
help, menu, "help detail", guide, version, exit, clear, clearcache, kb_status, check_kb,
genassignment, "cache stats", stats

## Mode switches
teacher, expert, ctf, review, hybrid

## Persona / offline / mood
persona, offline, mood

## Story / tracks / quiz / practice
threats, groups, practice, htb, thm, pcap, msf, next, topics, final, timeline, tracks,
quiz, task, writeup, writeups, exploits_log, heatmap, history, social, risk, noise, stealth,
trace, check_logs, wipe_logs, debts, faction, echo, watchers, phantom, phantom_msg, secret,
rewind, dashboard, analytics, repeat, walkthrough, exploit, auto_writeup, health, doctor,
context, backup, state, network, tools, missions, exploit_submit, hint, scanv2, code_review,
bounty, export, usage, config, keys, theme, lang

## Knowledge / memory (lines 900-915)
faiss_watch, reindex_knowledge, knowledge, learning_memory

## Stability / sleep / ghost log / backdoor (lines 891-927)
stability, teacher_sleep, ghost_log, backdoor

## Delegation targets (handlers/misc.py)
handle_reindex_knowledge (1178) — force_reindex + get_knowledge_status
handle_knowledge_search (1286) — /knowledge <query> [category]
handle_learning_memory (1202) — weak|events|breakthroughs
handle_ghost_log, handle_backdoor, handle_stability, handle_teacher_sleep,
handle_faiss_watch, handle_risk, handle_noise, handle_trace, handle_debts,
handle_faction, handle_echo, handle_memory, handle_wipe_logs, handle_check_logs,
handle_stealth, handle_backup, handle_state, handle_adaptive, handle_export,
handle_history, handle_model, handle_provider, handle_repeat, handle_terminal_log,
handle_topics, handle_usage, handle_version, handle_writeup, handle_writeups,
handle_course, handle_add_book, handle_heatmap, handle_config, handle_set_api_key

## Numeric menu (main.py:69, from config import NUMERIC_MENU)
Mapped in main.py:439-440: if user_input.isdigit() and user_input in NUMERIC_MENU
