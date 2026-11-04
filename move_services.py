"""Перенос services/ в src/services/ с shim-файлами в корне."""
import os
import shutil

ROOT = r'M:\Cyber_Teacher\Cyber_Teacher'
SRC = os.path.join(ROOT, 'src', 'services')
DST = os.path.join(ROOT, 'services')  # source dir in root

os.makedirs(SRC, exist_ok=True)

# Create __init__.py
with open(os.path.join(SRC, '__init__.py'), 'w', encoding='utf-8') as f:
    f.write('')

# Move files
for fname in os.listdir(DST):
    if fname == '__init__.py':
        continue
    src_path = os.path.join(DST, fname)
    if os.path.isfile(src_path):
        dst_path = os.path.join(SRC, fname)
        shutil.copy2(src_path, dst_path)
        print(f'Copied: {fname}')

# Create shim files in root services/
for fname in os.listdir(SRC):
    if fname == '__init__.py':
        continue
    shim_path = os.path.join(DST, fname)
    if not os.path.exists(shim_path):
        with open(shim_path, 'w', encoding='utf-8') as f:
            f.write(f'from src.services.{fname.replace(".py","")} import *\n')
        print(f'Shim: {fname}')

print('Done services')