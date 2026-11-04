import os
import subprocess
import sys

ROOT = r'M:\Cyber_Teacher\Cyber_Teacher'
os.chdir(ROOT)

# Run move_services
r = subprocess.run([sys.executable, 'move_services.py'], capture_output=True, text=True)
print('=== move_services ===')
print(r.stdout)
if r.stderr:
    print('ERR:', r.stderr[-500:])

# Now move models
models_src = os.path.join(ROOT, 'models')
models_dst = os.path.join(ROOT, 'src', 'models')
os.makedirs(models_dst, exist_ok=True)
with open(os.path.join(models_dst, '__init__.py'), 'w', encoding='utf-8') as f:
    f.write('')

for fname in os.listdir(models_src):
    if fname == '__init__.py':
        continue
    src_path = os.path.join(models_src, fname)
    if os.path.isfile(src_path):
        dst_path = os.path.join(models_dst, fname)
        shutil.copy2(src_path, dst_path)
        print(f'Copied models: {fname}')

# Create shims
for fname in os.listdir(models_dst):
    if fname == '__init__.py':
        continue
    shim_path = os.path.join(models_src, fname)
    if not os.path.exists(shim_path):
        with open(shim_path, 'w', encoding='utf-8') as f:
            f.write(f'from src.models.{fname.replace(".py","")} import *\n')
        print(f'Shim models: {fname}')

print('Done')