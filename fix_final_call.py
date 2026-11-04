#!/usr/bin/env python3
"""
Fix the final LLM call to use prompt_context.build()
"""
import os

ROOT = r'M:\Cyber_Teacher\Cyber_Teacher'

def fix_final_call():
    main_path = os.path.join(ROOT, 'src', 'cli', 'main.py')
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the f-string with system_prompt in the LLM call
    old = 'for chunk in llm.stream(f"{system_prompt}\\n\\nВопрос: {user_input}"):'
    new = 'for chunk in llm.stream(f"{prompt_context.build()}\\n\\nВопрос: {user_input}"):'
    
    content = content.replace(old, new)

    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Fixed final LLM call')

if __name__ == '__main__':
    fix_final_call()
    print('Done')