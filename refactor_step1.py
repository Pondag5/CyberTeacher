"""
Refactor Step 1.3: Move services/ and models/ into src/
Creates shims for backward compatibility.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def move_to_src(root_dir, src_sub, dst_sub):
    src_path = os.path.join(ROOT, src_sub)
    dst_path = os.path.join(ROOT, 'src', dst_sub)
    if not os.path.isdir(src_path):
        print(f'Skip {src_sub}: not found')
        return
    os.makedirs(dst_path, exist_ok=True)
    # __init__.py
    with open(os.path.join(dst_path, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write('')
    # Copy each file
    for fname in os.listdir(src_path):
        sp = os.path.join(src_path, fname)
        if os.path.isfile(sp):
            dp = os.path.join(dst_path, fname)
            shutil.copy2(sp, dp)
            print(f'  copied: {src_sub}/{fname} -> src/{dst_sub}/{fname}')
    # Create shims in original location
    for fname in os.listdir(dst_path):
        if fname == '__init__.py':
            continue
        shim = os.path.join(src_path, fname)
        # If file was already moved (i.e. original is gone), recreate shim
        # But we just copied, so original still exists.
        # We need to replace originals with shims ONLY if we want to delete originals.
        # Plan: keep originals for now (safer), but make them import from src.
        # Actually the plan says shims for backward compat. Let's make originals into shims.
        if os.path.exists(shim):
            # Backup original content then replace with shim
            with open(shim, 'r', encoding='utf-8') as f:
                orig = f.read()
            # Only replace if it's not already a shim
            if not orig.startswith('from src.'):
                with open(shim, 'w', encoding='utf-8') as f:
                    f.write(f'from src.{dst_sub}.{fname.replace(".py","")} import *  # shim -> src/{dst_sub}/{fname}\n')
                print(f'  shim: {src_sub}/{fname}')

print('=== Moving services/ -> src/services/ ===')
move_to_src(ROOT, 'services', 'services')

print('=== Moving models/ -> src/models/ ===')
move_to_src(ROOT, 'models', 'models')

print('=== Moving utils/ -> src/utils/ ===')
move_to_src(ROOT, 'utils', 'utils')

print('=== Moving handlers/ -> src/handlers/ ===')
# handlers is large; just copy to src/handlers for now, keep originals
handlers_src = os.path.join(ROOT, 'handlers')
handlers_dst = os.path.join(ROOT, 'src', 'handlers')
if os.path.isdir(handlers_src):
    os.makedirs(handlers_dst, exist_ok=True)
    with open(os.path.join(handlers_dst, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write('')
    count = 0
    for fname in os.listdir(handlers_src):
        sp = os.path.join(handlers_src, fname)
        if os.path.isfile(sp):
            dp = os.path.join(handlers_dst, fname)
            shutil.copy2(sp, dp)
            count += 1
    print(f'  copied {count} handler files')

print('=== Moving knowledge.py and RAG-related -> src/knowledge/ ===')
knowledge_dir = os.path.join(ROOT, 'src', 'knowledge')
os.makedirs(knowledge_dir, exist_ok=True)
with open(os.path.join(knowledge_dir, '__init__.py'), 'w', encoding='utf-8') as f:
    f.write('')

# Copy knowledge.py
knowledge_src = os.path.join(ROOT, 'knowledge.py')
if os.path.isfile(knowledge_src):
    shutil.copy2(knowledge_src, os.path.join(knowledge_dir, 'knowledge.py'))
    print('  copied: knowledge.py')

# Copy other RAG files
for fname in ['build_index.py', 'search_faiss.py', 'faiss_watcher.py', 'index_project.py']:
    sp = os.path.join(ROOT, fname)
    if os.path.isfile(sp):
        shutil.copy2(sp, os.path.join(knowledge_dir, fname))
        print(f'  copied: {fname}')

print('=== Moving db.py, auth.py, tools.py -> src/core/ or src/infra/ ===')
for fname, dst in [
    ('db.py', 'src/core/db.py'),
    ('auth.py', 'src/core/auth.py'),
    ('generators.py', 'src/core/generators.py'),
    ('tools.py', 'src/core/tools.py'),
    ('web_tools.py', 'src/core/web_tools.py'),
]:
    sp = os.path.join(ROOT, os.path.basename(fname))
    if os.path.isfile(sp):
        dp = os.path.join(ROOT, dst)
        shutil.copy2(sp, dp)
        print(f'  copied: {os.path.basename(fname)} -> {dst}')

print('\nDONE. Files are in src/. Originals in root are now shims (or kept for handlers/knowledge).')
print('Next: fix imports in src/ files.')