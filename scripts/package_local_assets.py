#!/usr/bin/env python3
import argparse
import fnmatch
import sys
import tarfile
from pathlib import Path

INCLUDE = ['faiss_index.bin', 'chunks_metadata.json', 'cves/**']
EXCLUDE = ['backups/**', 'logs/**', 'tmp/**', 'static_cache/**', '*.tmp', '*.bak', '.gitkeep']

def match(p, pat):
    return fnmatch.fnmatch(p, pat) or fnmatch.fnmatch(p, pat.replace('**', '*'))
def should_inc(path, root):
    r = str(path.relative_to(root)).replace('\\', '/')
    return not any(match(r, e) for e in EXCLUDE) and any(match(r, i) for i in INCLUDE)

def package(src, dst, verbose=True):
    src, dst = Path(src).resolve(), Path(dst).resolve()
    if not src.exists():
        print(f'Not found: {src}')
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    files = [f for p in INCLUDE for f in src.rglob(p.replace('**', '')) if f.is_file() and should_inc(f, src)]
    if not files:
        print('Nothing to package')
        return False
    if verbose:
        print(f'Packaging {len(files)} files')
        for f in files: print(f'  {f.relative_to(src)} ({f.stat().st_size:,} bytes)')
    try:
        with tarfile.open(dst, 'w:gz') as tar:
            for f in files:
                tar.add(f, arcname=str(f.relative_to(src)))
        sz = dst.stat().st_size
        if verbose:
            print(f'Created: {dst} ({sz/1024/1024:.1f} MB)')
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, default='./local')
    ap.add_argument('--output', type=Path, default='./dist/cyberteacher-assets-full.tar.gz')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    if a.list:
        s = Path(a.source).resolve()
        for p in INCLUDE:
            for f in s.rglob(p.replace('**', '')):
                if f.is_file() and should_inc(f, s): print(f'  {f.relative_to(s)} ({f.stat().st_size:,} bytes)')
    else: sys.exit(0 if package(a.source, a.output, not a.quiet) else 1)
