#!/usr/bin/env python3
"""
Fix the final LLM call in main.py
"""
import os

ROOT = r'M:\Cyber_Teacher\Cyber_Teacher'

def fix_final_call():
    main_path = os.path.join(ROOT, 'src', 'cli', 'main.py')
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The actual pattern
    old = 'llm.stream(f"{system_prompt}\\n\\n\xd0\xa0\xe2\x80\x99\xd0\xa0\xd1\x95\xd0\xa0\xd1\x97\xd0\xa1\xd0\x82\xd0\xa0\xd1\x95\xd0\xa1\xd0\x83: {user_input}")'
    new = 'llm.stream(f"{prompt_context.build()}\\n\\n\xd0\xa0\xe2\x80\x99\xd0\xa0\xd1\x95\xd0\xa0\xd1\x97\xd0\xa1\xd0\x82\xd0\xa0\xd1\x95\xd0\xa1\xd0\x83: {user_input}")'
    
    content = content.replace(old, new)

    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Fixed final LLM call')

if __name__ == '__main__':
    main_path = os.path.join(r'M:\Cyber_Teacher\Cyber_Teacher', 'src', 'cli', 'main.py')
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old = 'llm.stream(f"{system_prompt}\\n\\n\xd0\xa0\xe2\x80\x99\xd0\xa0\xd1\x95\xd0\xa0\xd1\x97\xd0\xa1\xd0\x82\xd0\xa0\xd1\x95\xd0\xa1\xd0\x83: {user_input}")'
    new = 'llm.stream(f"{prompt_context.build()}\\n\\n\xd0\xa0\xe2\x80\x99\xd0\xa0\xd1\x95\xd0\xa0\xd1\x97\xd0\xa1\xd0\x82\xd0\xa0\xd1\x95\xd0\xa1\xd0\x83: {user_input}")'
    
    if old in content:
        content = content.replace(old, new)
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Fixed')
    else:
        print('Pattern not found - trying alternative')
        # Try without the unicode
        import re
        content = re.sub(r'llm\.stream\(f"\{system_prompt\}', r'llm.stream(f"{prompt_context.build()}', content)
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Used regex fix')