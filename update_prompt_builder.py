#!/usr/bin/env python3
"""
Replace manual system_prompt concatenation with PromptBuilder in main.py and api_server.py
"""
import os
import re

ROOT = r'M:\Cyber_Teacher\Cyber_Teacher'

def update_main_py():
    main_path = os.path.join(ROOT, 'src', 'cli', 'main.py')
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the system_prompt building section
    # Find the section from "system_prompt = get_mode_prompt" to before the next major section
    old_pattern = r'''system_prompt = get_mode_prompt\(
            current_mode, context_str, docs_context, study_context
        \)

        # === Context Awareness \+ Personality Drift ===
        try:
            from context_awareness import get_context_info, get_atmosphere_hint
            from personality import apply_personality_drift

            ctx_info = get_context_info\(
                session_start=state\.metrics\.get\("start_time", 0\),
                messages_this_session=len\(trimmed_history\),
            \)
            atmosphere = get_atmosphere_hint\(ctx_info\)
            personality_mod = apply_personality_drift\(ctx_info\)

            if atmosphere:
                system_prompt \+= f"\\n\\n\{atmosphere\}"
            if personality_mod:
                system_prompt \+= f"\\n\\n\{personality_mod\}"
        except ImportError:
            pass

        # === Behavioral Archetype ===
        try:
            from behavior_profile import get_archetype_prompt_modifier

            archetype_mod = get_archetype_prompt_modifier\(state\)
            if archetype_mod:
                system_prompt \+= archetype_mod
        except ImportError:
            pass

        # === Persona Router \(dynamic\) ===
        try:
            from persona_router import select_persona, get_persona_prompt

            user_msg = user_input if "user_input" in locals\(\) else ""
            persona_id = select_persona\(state, user_msg\)
            persona_mod = get_persona_prompt\(persona_id\)
            if persona_mod:
                system_prompt \+= persona_mod
        except ImportError:
            pass

        # === Persistent World State \+ Episode Memory ===
        try:
            from world_state import get_world_state
            from episode_memory import get_episode_memory

            world = get_world_state\(\)
            world\.check_spawn_incident\(state\)
            world_prompt = world\.get_world_prompt\(\)
            if world_prompt:'''

    new_code = '''system_prompt = get_mode_prompt(
            current_mode, context_str, docs_context, study_context
        )

        # Use PromptBuilder for unified prompt construction
        from src.prompt_engine.builder import PromptContext

        prompt_context = PromptContext(current_mode)
        prompt_context.with_study_context(study_context)
        prompt_context.with_docs_context(docs_context)

        # === Context Awareness + Personality Drift ===
        try:
            from src.personas.context_awareness import get_context_info, get_atmosphere_hint
            from src.personas.personality import apply_personality_drift

            ctx_info = get_context_info(
                session_start=state.metrics.get("start_time", 0),
                messages_this_session=len(trimmed_history),
            )
            atmosphere = get_atmosphere_hint(ctx_info)
            personality_mod = apply_personality_drift(ctx_info)

            if atmosphere:
                prompt_context.with_atmosphere(atmosphere)
            if personality_mod:
                prompt_context.with_personality_drift(personality_mod)
        except ImportError:
            pass

        # === Behavioral Archetype ===
        try:
            from src.personas.behavior_profile import get_archetype_prompt_modifier

            archetype_mod = get_archetype_prompt_modifier(state)
            if archetype_mod:
                prompt_context.with_archetype(archetype_mod)
        except ImportError:
            pass

        # === Persona Router (dynamic) ===
        try:
            from src.personas.persona_router import select_persona, get_persona_prompt

            user_msg = user_input if "user_input" in locals() else ""
            persona_id = select_persona(state, user_msg)
            persona_mod = get_persona_prompt(persona_id)
            if persona_mod:
                prompt_context.with_persona(persona_mod)
        except ImportError:
            pass

        # === Persistent World State + Episode Memory ===
        try:
            from src.gamification.world_state import get_world_state
            from episode_memory import get_episode_memory

            world = get_world_state()
            world.check_spawn_incident(state)
            world_prompt = world.get_world_prompt()
            if world_prompt:'''

    content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

    # Replace the world_prompt addition
    old_world = '''if world_prompt:
                system_prompt += world_prompt'''
    new_world = '''if world_prompt:
                prompt_context.with_cyberpsychosis(world_prompt)'''

    content = content.replace(old_world, new_world)

    # Replace the cyberpsychosis addition
    old_cp = '''# === Cyberpsychosis ===
        try:
            from cyberpsychosis import get_cyberpsychosis_prompt_modifier

            cp_prompt = get_cyberpsychosis_prompt_modifier(state)
            if cp_prompt:
                system_prompt += cp_prompt
        except ImportError:
            pass

        # === Atmosphere Message ===
        try:
            from atmosphere import get_atmosphere_message

            atm_msg = get_atmosphere_message(state)
            if atm_msg:
                system_prompt += atm_msg
        except ImportError:
            pass

        # === Difficulty Adaptation ===
        try:
            from adaptive_ui import get_difficulty_prefix

            diff_prefix = get_difficulty_prefix(state)
            if diff_prefix:
                system_prompt += diff_prefix
        except ImportError:
            pass'''

    new_cp = '''# === Cyberpsychosis ===
        try:
            from src.personas.cyberpsychosis import get_cyberpsychosis_prompt_modifier

            cp_prompt = get_cyberpsychosis_prompt_modifier(state)
            if cp_prompt:
                prompt_context.with_cyberpsychosis(cp_prompt)
        except ImportError:
            pass

        # === Atmosphere Message ===
        try:
            from src.personas.atmosphere import get_atmosphere_message

            atm_msg = get_atmosphere_message(state)
            if atm_msg:
                prompt_context.with_atmosphere(atm_msg)
        except ImportError:
            pass

        # === Difficulty Adaptation ===
        try:
            from adaptive_ui import get_difficulty_prefix

            diff_prefix = get_difficulty_prefix(state)
            if diff_prefix:
                prompt_context.with_difficulty(diff_prefix)
        except ImportError:
            pass'''

    content = content.replace(old_cp, new_cp)

    # Replace the final build
    old_final = 'system_prompt += memory_prompt'
    new_final = 'prompt_context.add_modifier(memory_prompt)'

    content = content.replace(old_final, new_final)

    # Find where system_prompt is used (e.g., in LLM call) and replace with prompt_context.build()
    # This needs careful handling - find the place where system_prompt is passed to LLM
    old_pass = 'system_prompt=system_prompt'
    new_pass = 'system_prompt=prompt_context.build()'
    content = content.replace(old_pass, new_pass)

    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Updated main.py')


def update_api_server_py():
    api_path = os.path.join(ROOT, 'src', 'api', 'api_server.py')
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # First location: websocket handler (around line 717-843)
    old_pattern1 = r'''# Build system prompt
            from main import get_mode_prompt

            system_prompt = get_mode_prompt\(mode, "", "", ""\)
            if user_context:
                system_prompt \+= user_context

            try:
                from context_awareness import get_context_info, get_atmosphere_hint
                from personality import apply_personality_drift

                ctx_info = get_context_info\(
                    session_start=state\.metrics\.get\("start_time", 0\),
                    messages_this_session=state\.messages_sent,
                \)
                atm = get_atmosphere_hint\(ctx_info\)
                pmod = apply_personality_drift\(ctx_info\)
                if atm:
                    system_prompt \+= f"\\n\\n\{atm\}"
                if pmod:
                    system_prompt \+= f"\\n\\n\{pmod\}"
            except ImportError:
                pass

            # Persona Router \(dynamic\)
            try:
                from persona_router import \(
                    select_persona,
                    get_persona_prompt,
                    get_persona_info,
                \)

                persona_id = select_persona\(state, message\)
                persona_mod = get_persona_prompt\(persona_id\)
                if persona_mod:
                    system_prompt \+= persona_mod
                # Send persona info at start
                persona_info = get_persona_info\(persona_id\)
                await websocket\.send_json\(\{"persona": persona_info\}\)
            except ImportError:
                pass

            from memory import get_chat_history, init_db

            conn = init_db\(\)
            raw_history = get_chat_history\(conn, limit=100\)

            # Inject summary if available
            if BUDGET_AVAILABLE and api_budget_manager is not None:
                summary_text = api_budget_manager\.extract_summary\(raw_history\)
                if summary_text:
                    system_prompt \+= f"\\n\\n\[Context summary: \{summary_text\}\]"'''

    new_code1 = '''# Build system prompt using PromptBuilder
            from src.prompt_engine.builder import PromptContext

            prompt_context = PromptContext(mode)
            if user_context:
                prompt_context.add_modifier(user_context)

            try:
                from src.personas.context_awareness import get_context_info, get_atmosphere_hint
                from src.personas.personality import apply_personality_drift

                ctx_info = get_context_info(
                    session_start=state.metrics.get("start_time", 0),
                    messages_this_session=state.messages_sent,
                )
                atm = get_atmosphere_hint(ctx_info)
                pmod = apply_personality_drift(ctx_info)
                if atm:
                    prompt_context.with_atmosphere(atm)
                if pmod:
                    prompt_context.with_personality_drift(pmod)
            except ImportError:
                pass

            # Persona Router (dynamic)
            try:
                from src.personas.persona_router import (
                    select_persona,
                    get_persona_prompt,
                    get_persona_info,
                )

                persona_id = select_persona(state, message)
                persona_mod = get_persona_prompt(persona_id)
                if persona_mod:
                    prompt_context.with_persona(persona_mod)
                # Send persona info at start
                persona_info = get_persona_info(persona_id)
                await websocket.send_json({"persona": persona_info})
            except ImportError:
                pass

            from memory import get_chat_history, init_db

            conn = init_db()
            raw_history = get_chat_history(conn, limit=100)

            # Inject summary if available
            if BUDGET_AVAILABLE and api_budget_manager is not None:
                summary_text = api_budget_manager.extract_summary(raw_history)
                if summary_text:
                    prompt_context.add_modifier(f"[Context summary: {summary_text}]")'''

    content = re.sub(old_pattern1, new_code1, content, flags=re.DOTALL)

    # Second location: around line 4251-4313 (HTTP endpoint)
    old_pattern2 = r'''system_prompt = get_mode_prompt\(mode, study_context, docs_context, errors_context\)
            if user_context:
                system_prompt \+= user_context

            # Mood/persona modifier
            try:
                from mood import get_mood_modifier
                mood_mod = get_mood_modifier\(state\)
                if mood_mod:
                    system_prompt \+= mood_mod
            except ImportError:
                pass

            # Behavioral Archetype
            try:
                from behavior_profile import get_archetype_prompt_modifier
                archetype_mod = get_archetype_prompt_modifier\(state\)
                if archetype_mod:
                    system_prompt \+= archetype_mod
            except ImportError:
                pass

            # Persona Router
            try:
                from persona_router import select_persona, get_persona_prompt
                persona_id = select_persona\(state, message\)
                persona_mod = get_persona_prompt\(persona_id\)
                if persona_mod:
                    system_prompt \+= persona_mod
            except ImportError:
                pass

            # Context summary from insights
            try:
                from insights import get_insights_context
                insights_context = get_insights_context\(state\)
                if insights_context:
                    system_prompt \+= insights_context
            except ImportError:
                pass

            # Personality drift
            try:
                from personality import apply_personality_drift
                from context_awareness import get_context_info
                ctx_info = get_context_info\(session_start=state\.metrics\.get\("start_time", 0\), messages_this_session=len\(trimmed_history\)\)
                pmod = apply_personality_drift\(ctx_info\)
                if pmod:
                    system_prompt \+= pmod
            except ImportError:
                pass'''

    new_code2 = '''# Use PromptBuilder for unified prompt construction
            from src.prompt_engine.builder import PromptContext

            prompt_context = PromptContext(mode)
            prompt_context.with_study_context(study_context)
            prompt_context.with_docs_context(docs_context)
            prompt_context.add_modifier(errors_context)
            if user_context:
                prompt_context.add_modifier(user_context)

            # Mood/persona modifier
            try:
                from mood import get_mood_modifier
                mood_mod = get_mood_modifier(state)
                if mood_mod:
                    prompt_context.add_modifier(mood_mod)
            except ImportError:
                pass

            # Behavioral Archetype
            try:
                from src.personas.behavior_profile import get_archetype_prompt_modifier
                archetype_mod = get_archetype_prompt_modifier(state)
                if archetype_mod:
                    prompt_context.with_archetype(archetype_mod)
            except ImportError:
                pass

            # Persona Router
            try:
                from src.personas.persona_router import select_persona, get_persona_prompt
                persona_id = select_persona(state, message)
                persona_mod = get_persona_prompt(persona_id)
                if persona_mod:
                    prompt_context.with_persona(persona_mod)
            except ImportError:
                pass

            # Context summary from insights
            try:
                from insights import get_insights_context
                insights_context = get_insights_context(state)
                if insights_context:
                    prompt_context.add_modifier(insights_context)
            except ImportError:
                pass

            # Personality drift
            try:
                from src.personas.personality import apply_personality_drift
                from src.personas.context_awareness import get_context_info
                ctx_info = get_context_info(session_start=state.metrics.get("start_time", 0), messages_this_session=len(trimmed_history))
                pmod = apply_personality_drift(ctx_info)
                if pmod:
                    prompt_context.with_personality_drift(pmod)
            except ImportError:
                pass'''

    content = re.sub(old_pattern2, new_code2, content, flags=re.DOTALL)

    # Replace usage of system_prompt with prompt_context.build() in both locations
    content = content.replace('system_prompt=system_prompt', 'system_prompt=prompt_context.build()')

    with open(api_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Updated api_server.py')


if __name__ == '__main__':
    update_main_py()
    update_api_server_py()
    print('Done')