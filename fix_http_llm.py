#!/usr/bin/env python3
"""
Fix HTTP endpoint to use prompt_context.build()
"""
import os

p = r'M:\Cyber_Teacher\Cyber_Teacher\src\api\api_server.py'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the system_prompt usage in HTTP endpoint
old = 'messages = [{"role": "system", "content": system_prompt}]'
new = 'messages = [{"role": "system", "content": prompt_context.build()}]'

content = content.replace(old, new)

with open(p, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed HTTP endpoint LLM call')