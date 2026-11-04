#!/usr/bin/env python3
"""
Add add_modifier to PromptContext class
"""
import os

p = r'M:\Cyber_Teacher\Cyber_Teacher\src\prompt_engine\builder.py'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the PromptContext class and add add_modifier method after __init__
old = '''    def __init__(self, mode: str):
        self.builder = PromptBuilder(mode)
    
    def with_study_context'''

new = '''    def __init__(self, mode: str):
        self.builder = PromptBuilder(mode)
    
    def add_modifier(self, modifier: str) -> "PromptContext":
        """Add a modifier to the prompt"""
        self.builder.add_modifier(modifier)
        return self
    
    def with_study_context'''

content = content.replace(old, new)

with open(p, 'w', encoding='utf-8') as f:
    f.write(content)

print('Added add_modifier to PromptContext')