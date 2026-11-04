#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open(r"M:\Cyber_Teacher\Cyber_Teacher\src\api\api_server.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines(keepends=True)
for i, line in enumerate(lines):
    if 'weak_topics' in line and 'Слабые темы' in line:
        print(f"Found at line {i+1}: {repr(line)}")
        indent = ' ' * 12
        # Build without escaping issues
        replacement = (
            indent
            + 'f"Слабые темы: {'
            + "'"
            + ', '
            + "'"
            + '.join(str(t.get(\\"topic\\", t)) if isinstance(t, dict) else str(t) for t in getattr(state, \\"weak_topics\\", [])[-5:]) or '
            + '"нет"'
            + '}"'
            + '\\n"\n'
        )
        lines[i] = replacement
        print(f"Replaced with: {repr(lines[i])}")
        break

with open(r"M:\Cyber_Teacher\Cyber_Teacher\src\api\api_server.py", "w", encoding="utf-8") as f:
    f.write(''.join(lines))
print("Fixed")