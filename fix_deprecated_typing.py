#!/usr/bin/env python3
import os
import re
from pathlib import Path

deprecated = {"dict": "dict", "list": "list", "tuple": "tuple", "set": "set"}


def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    def filter_import(match):
        names_str = match.group(1)
        names = [n.strip() for n in names_str.split(",")]
        kept = [n for n in names if n not in deprecated]
        if kept:
            return f"from typing import {', '.join(kept)}"
        else:
            return ""  # remove line entirely

    content = re.sub(r"from typing import ([^\n\r]+)", filter_import, content)

    for old, new in deprecated.items():
        content = re.sub(rf"\b{old}\b", new, content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


root = Path(".")
for py_file in root.rglob("*.py"):
    if any(part.startswith(".") or part == "__pycache__" for part in py_file.parts):
        continue
    process_file(py_file)

print("Fixed deprecated typing generics")
