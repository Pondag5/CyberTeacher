#!/usr/bin/env python
"""Test script to check registry commands."""

from handlers.registry import registry

print("Registered commands:")
for cmd, type_ in registry.list_commands().items():
    print(f"  {cmd} ({type_})")

print("\nTesting mindmap command:")
handler, remaining = registry.get_handler("mindmap")
print(f"Handler: {handler}")
print(f"Remaining: '{remaining}'")

print("\nTesting mindmap help command:")
handler, remaining = registry.get_handler("mindmap help")
print(f"Handler: {handler}")
print(f"Remaining: '{remaining}'")

print("\nTesting export extended command:")
handler, remaining = registry.get_handler("export extended")
print(f"Handler: {handler}")
print(f"Remaining: '{remaining}'")