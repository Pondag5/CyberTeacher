#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import tarfile
from pathlib import Path
from urllib.request import Request, urlopen

REPO = 'Pondag5/CyberTeacher'
DEFAULT_URL = 'https://github.com/' + REPO + '/releases/latest/download/cyberteacher-assets-full.tar.gz'
LOCAL = Path('./local')
REQUIRED = {'full': ['faiss_index.bin', 'chunks_metadata.json', 'cves'], 'minimal': []}
MANIFEST = LOCAL / '.assets_manifest.json'

def log(m): print('[launcher] ' + m)
def load_man(): return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
def save_man(d):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(d, indent=2))
def fhash(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(8192), b''): h.update(c)
    return h.hexdigest()

def check(p):
    miss = []
    for item in REQUIRED.get(p, []):
        path = LOCAL / item
        if not path.exists(): miss.append(item)
        elif path.is_dir() and not any(path.iterdir()): miss.append(item + ' (empty)')
    return miss

def download(url, dest):
    log('Downloading from ' + url)
    try:
        with urlopen(Request(url, headers={'User-Agent': 'CyberTeacher-Launcher'}), timeout=30) as r, open(dest, 'wb') as f:
            tot = r.headers.get('Content-Length')
            tot = int(tot) if tot else None
            dl = 0
            while True:
                chunk = r.read(8192)
                if not chunk: break
                f.write(chunk)
                dl += len(chunk)
                if tot:
                    sys.stdout.write(f'\r  {dl/1024/1024:.1f}/{tot/1024/1024:.1f} MB')
                    sys.stdout.flush()
        print()
        return True
    except Exception as e:
        log('Download failed: ' + str(e))
        return False

def extract(arch, dest):
    log('Extracting to ' + str(dest))
    try:
        with tarfile.open(arch, 'r:gz') as tar:
            tar.extractall(dest)
        return True
    except Exception as e:
        log('Extract failed: ' + str(e))
        return False

def verify(p):
    man = load_man()
    for item in REQUIRED.get(p, []):
        path = LOCAL / item
        if not path.exists(): return False
        if path.is_file() and man.get(str(path)) != fhash(path): return False
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--profile', choices=['full', 'minimal'], default='full')
    ap.add_argument('--assets-url', default=DEFAULT_URL)
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()

    LOCAL.mkdir(parents=True, exist_ok=True)
    miss = check(a.profile)

    if miss and not a.force:
        log('Missing assets for ' + a.profile + ': ' + str(miss))
        if not download(a.assets_url, LOCAL / 'assets.tar.gz'): return 1
        if not extract(LOCAL / 'assets.tar.gz', LOCAL): return 1
        (LOCAL / 'assets.tar.gz').unlink(missing_ok=True)
        log('Assets ready')
    elif a.force:
        log('Force re-download')
        if not download(a.assets_url, LOCAL / 'assets.tar.gz'): return 1
        if not extract(LOCAL / 'assets.tar.gz', LOCAL): return 1
        (LOCAL / 'assets.tar.gz').unlink(missing_ok=True)

    if a.check_only:
        ok = verify(a.profile)
        log('Verification: ' + ('OK' if ok else 'FAILED'))
        return 0 if ok else 1

    log('Starting CyberTeacher...')
    os.execv(sys.executable, [sys.executable, 'main.py', *sys.argv[1:]])

if __name__ == '__main__': sys.exit(main())
