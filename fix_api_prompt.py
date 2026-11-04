#!/usr/bin/env python3
"""
Fix remaining system_prompt usage in api_server.py
"""
import os
import re

ROOT = r'M:\Cyber_Teacher\Cyber_Teacher'

def fix_api_server():
    api_path = os.path.join(ROOT, 'src', 'api', 'api_server.py')
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Location 1: websocket handler - already partially done, check if system_prompt=prompt_context.build()
    # Find the websocket LLM call
    old1 = 'system_prompt=system_prompt'
    new1 = 'system_prompt=prompt_context.build()'
    content = content.replace(old1, new1)

    # Location 2: HTTP endpoint (around line 28145 onwards) - replace remaining system_prompt +=
    replacements = [
        # Mood modifier
        ('system_prompt += f"\\n\\nStyle: {mood_modifier}"', 
         'prompt_context.add_modifier(f"\\n\\nStyle: {mood_modifier}")'),
        
        # Archetype
        ('system_prompt += archetype_mod', 
         'prompt_context.with_archetype(archetype_mod)'),
        
        # Persona
        ('system_prompt += persona_mod', 
         'prompt_context.with_persona(persona_mod)'),
        
        # Study context
        ('system_prompt += study_context', 
         'prompt_context.with_study_context(study_context)'),
        
        # Docs context
        ('system_prompt += docs_context', 
         'prompt_context.with_docs_context(docs_context)'),
        
        # Errors context
        ('system_prompt += errors_context', 
         'prompt_context.add_modifier(errors_context)'),
        
        # Insights context
        ('system_prompt += insights_context', 
         'prompt_context.add_modifier(insights_context)'),
        
        # Personality drift
        ('system_prompt += f"\\n\\n{pmod}"', 
         'prompt_context.with_personality_drift(pmod)'),
        
        # Summary
        ('system_prompt += f"\\n\\n[Context summary: {summary_text}]"', 
         'prompt_context.add_modifier(f"[Context summary: {summary_text}]")'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    # Find and replace the LLM calls
    # Location 1: websocket - system_prompt=system_prompt
    content = content.replace('system_prompt=system_prompt', 'system_prompt=prompt_context.build()')

    # Location 2: HTTP endpoint - find the LLM call
    # The HTTP endpoint is around line 166687
    # Look for: f"{system_prompt}\n\n---\n{context_str}\n\n..."
    old_llm = 'f"{system_prompt}\\n\\n---\\n{context_str}\\n\\n'
    new_llm = 'f"{prompt_context.build()}\\n\\n---\\n{context_str}\\n\\n'
    content = content.replace(old_llm, new_llm)

    # Also check for other LLM calls with system_prompt
    content = content.replace('f"{system_prompt}', 'f"{prompt_context.build()}')

    # Fix the websocket section - it should use prompt_context.build()
    # Look for: await websocket.send_json({"role": "assistant", "content": await llm.ainvoke(...})
    # or similar
    content = content.replace(
        'f"{system_prompt}\\n\\n',
        'f"{prompt_context.build()}\\n\\n'
    )

    # Fix the versus endpoint - it has its own system_prompt logic, leave as is unless it uses the shared system_prompt
    # The versus endpoint at 73593+ is separate, leave it

    with open(os.path.join(ROOT, 'src', 'api', 'api_server.py'), 'w', encoding='utf-8') as f:
        f.write(content)

    print('Fixed api_server.py')

if __name__ == '__main__':
    fix_api_server()
    print('Done')