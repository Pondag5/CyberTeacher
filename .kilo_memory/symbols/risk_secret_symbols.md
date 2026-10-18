# Symbol Index — Risk/Secret/Rewind/Phantom Handlers
# Source: /workspace/app/handlers/

## handlers/noise.py
- get_noise_level() -> dict (19) — уровень шума (0-100)
- _get_noise_status(level) -> str (29)
- add_noise(amount=5) -> str (41)
- _decay_noise(state) (66)
- toggle_stealth() -> dict (79) — включение/выключение скрытности

## handlers/trace.py
- get_trace_status() -> dict (16) — статус таймера трассировки
- start_trace(target, duration=TRACE_DURATION) -> str (30)
- stop_trace() -> str (41)
- check_trace_expired() -> Optional[str] (51)

## handlers/debt.py
- get_debts() -> dict (19) — долги
- _get_debt_status(count) -> str (29)
- _recalc_debts(state) (39)
- add_debt(reason, count=1) -> str (74)
- clear_debt(reason, count=1, prefix="") -> str (87)

## handlers/watchers.py
- get_watchers_status() -> dict (28)
- _can_trigger() -> bool (47) — watchers counterattack (noise>=70 + dirty logs>=3 + risk>=50)
- trigger_counterattack() -> Optional[str] (63)
- handle_watchers(action) -> tuple (77)

## handlers/secret_room.py
- check_unlock(state) -> bool (34) — разблокировка секретной комнаты (8 глав + faction + watchers)
- get_secret_room_status() -> dict (41)
- enter_secret_room() -> Optional[str] (63)
- handle_secret(action) -> tuple (104)

## handlers/rewind.py
- handle_rewind(action) -> HandlerResult (15) — машина времени /rewind N

## handlers/phantom_lab.py
- _get_cyberpsychosis_level() -> float (60)
- _spawn_chance(cp_level) -> float (70)
- _pick_phantom() -> Dict (76)
- _cleanup_expired(state) (91)
- _maybe_spawn(state) (104)
- get_phantom_labs() -> List[Dict] (114) — Phantom Labs (timed, исчезают навсегда, CP>=30)
- complete_phantom_lab(lab_id) -> Optional[str] (134)
- force_spawn() -> Optional[str] (145)
- handle_phantom(action) -> tuple (154)

## handlers/core.py (1230 lines)
- handle_commands(action, conn, llm_factory) (line 346) — главный диспетчер CLI команд
- Handles: /reindex_knowledge (line 905-907, delegates to handlers.misc.handle_reindex_knowledge)
- Plus handlers from: achievements, code_review_v2, code_scan, config, cve, docker_gen,
  equipment, emotions, features, flags, health, misc, missions, network, news, offline,
  mood, practice, htb, walkthroughs, bug_bounty, dashboard, exploit_submit, hints, tracks,
  analytics, phishing, profile, mermaid, skills, ctf_flags, cve, daily, dashboard, debt,
  echo, faction, ghost_log, memory, backdoor, etc.
