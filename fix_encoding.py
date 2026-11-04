#!/usr/bin/env python3
"""
Fix encoding issue in startup_checks.py
"""
import os

p = r'M:\Cyber_Teacher\Cyber_Teacher\src\core\startup_checks.py'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Unicode warning characters with ASCII
content = content.replace('⚠️', '[WARN]')
content = content.replace('✅', '[OK]')

with open(p, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed encoding in startup_checks.py')