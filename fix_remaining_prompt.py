#!/usr/bin/env python3
"""
Fix remaining system_prompt usage in main.py and api_server.py
"""
import os

ROOT = r'M:\Cyber_Teacher\Cyber_Teacher'

def fix_main_py():
    main_path = os.path.join(ROOT, 'src', 'cli', 'main.py')
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace remaining system_prompt += with prompt_context methods
    # World prompt
    content = content.replace(
        'if world_prompt:\n                system_prompt += f"\\n\\n{world_prompt}"',
        'if world_prompt:\n                prompt_context.with_cyberpsychosis(world_prompt)'
    )

    # Memory prompt
    content = content.replace(
        'if memory_prompt:\n                system_prompt += f"\\n\\n{memory_prompt}"',
        'if memory_prompt:\n                prompt_context.add_modifier(memory_prompt)'
    )

    # Cyberpsychosis - check both patterns
    content = content.replace(
        'if cp_prompt:\n                system_prompt += f"\\n\\n{cp_prompt}"',
        'if cp_prompt:\n                prompt_context.with_cyberpsychosis(cp_prompt)'
    )

    # Atmosphere
    content = content.replace(
        'if atm_msg:\n                system_prompt += f"\\n\\n{atm_msg}"',
        'if atm_msg:\n                prompt_context.with_atmosphere(atm_msg)'
    )

    # Difficulty
    content = content.replace(
        'if diff_prefix:\n                system_prompt += diff_prefix',
        'if diff_prefix:\n                prompt_context.with_difficulty(diff_prefix)'
    )

    # Versus prompts
    content = content.replace(
        'system_prompt = versus_prompt',
        'prompt_context.add_modifier(versus_prompt)'
    )

    # Final LLM call - replace system_prompt in f-string
    # Find: f"... {system_prompt} ..."
    # This is tricky - need to find the actual LLM call
    pass

    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Fixed main.py partial')


def fix_main_final_call():
    """Find and replace the final LLM call"""
    main_path = os.path.join(ROOT, 'src', 'cli', 'main.py')
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the f-string that uses system_prompt at the end
    # Pattern: f"... {system_prompt} ..."
    import re
    # Find the last occurrence of system_prompt in an f-string before LLM call
    # Look for: f"{system_prompt}"
    pattern = r'f"\{system_prompt\}"'
    match = re.search(pattern, content)
    if match:
        print(f'Found at {match.start()}')
    
    # More specific: look for system_prompt in f-string near end of processing
    # Search around position 32972
    idx = content.find('{system_prompt}')
    if idx >= 0:
        print(f'Found {{system_prompt}} at {idx}')
        # Check context
        print(content[max(0,idx-200):idx+200])

    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    fix_main_py()
    fix_main_final_call()
    print('Done partial fix')