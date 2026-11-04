#!/usr/bin/env python3
"""
Fix PromptBuilder.add_modifier to not reference self.builder
"""
import os

p = r'M:\Cyber_Teacher\Cyber_Teacher\src\prompt_engine\builder.py'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    def add_modifier(self, modifier: str):
        """Add a modifier to the prompt"""
        self.builder.add_modifier(modifier)
        return self'''

new = '''    def add_modifier(self, modifier: str):
        """Add a modifier to the prompt"""
        if modifier:
            self.modifiers.append(modifier)
        return self'''

content = content.replace(old, new)

with open(p, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed PromptBuilder.add_modifier')