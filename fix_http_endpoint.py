#!/usr/bin/env python3
"""
Fix HTTP endpoint in api_server.py to use PromptContext
"""
import os

ROOT = r'M:\Cyber_Teacher\Cyber_Teacher'

def fix_http_endpoint():
    api_path = os.path.join(ROOT, 'src', 'api', 'api_server.py')
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the HTTP endpoint section and add PromptContext initialization
    old = '''        system_prompt = TeacherPersona.get_system_prompt(
            style=mode,
            language=language,
        )

        mood_modifier = get_mood_prompt_modifier()
        if mood_modifier:
            prompt_context.add_modifier(f"\\n\\nStyle: {mood_modifier}")'''

    new = '''        # Use PromptBuilder for unified prompt construction
        from src.prompt_engine.builder import PromptContext

        prompt_context = PromptContext(mode)
        
        mood_modifier = get_mood_prompt_modifier()
        if mood_modifier:
            prompt_context.add_modifier(f"\\n\\nStyle: {mood_modifier}")'''

    content = content.replace(old, new)

    # Also need to remove the old system_prompt = TeacherPersona... line since we're using PromptContext
    # But the old code still has system_prompt = TeacherPersona.get_system_prompt() 
    # Let's check if there's a conflict

    with open(api_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Fixed HTTP endpoint')

if __name__ == '__main__':
    fix_http_endpoint()
    print('Done')