#!/usr/bin/env python3
"""
Download large assets from GitHub Releases.
Usage: python scripts/download_assets.py [--profile minimal|full|research]
"""

import os
import sys
import argparse
import subprocess
import tarfile
import shutil
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import json

REPO = "Pondag5/CyberTeacher"
RELEASES_API = f"https://api.github.com/repos/{REPO}/releases/latest"
RELEASES_DOWNLOAD = f"https://github.com/{REPO}/releases/latest/download"

# Asset mapping per profile
ASSETS = {
    "minimal": [],  # No extra assets needed
    "full": [
        "faiss_index.bin",
        "chunks_metadata.json",
        "cves.tar.gz",
    ],
    "research": [
        "faiss_index.bin",
        "chunks_metadata.json",
        "cves.tar.gz",
        "threat_feeds.tar.gz",
    ],
}

REPO_OWNER = "Pondag5"
REPO_NAME = "CyberTeacher"
RELEASES_URL = f"https://github.com/Pondag5/CyberTeacher/releases/latest/download"

CHUNK_SIZE = 8192


def download_file(url: str, dest: Path, progress: bool = True) -> bool:
    """Download a file with progress bar."""
    try:
        req = Request(url, headers={"User-Agent": "CyberTeacher-Asset-Downloader"})
        with urlopen(req, timeout=30) as response:
            total = response.headers.get("Content-Length")
            total = int(total) if total else None

            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                downloaded = 0
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress and total:
                        pct = downloaded * 100 / total
                        print(f"\r  {dest.name}: {pct:.1f}% ({downloaded:,}/{total:,} bytes)", end="", flush=True)
            if progress:
                print()
            return True
    except HTTPError as e:
        print(f"\n❌ HTTP {e.code}: {url}")
        return False
    except URLError as e:
        print(f"\n❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def extract_archive(archive_path: Path, dest_dir: Path) -> bool:
    """Extract tar.gz archive."""
    try:
        print(f"  Extracting {archive_path.name}...")
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(dest_dir)
        return True
    except Exception as e:
        print(f"❌ Failed to extract {archive_path}: {e}")
        return False


def get_latest_release_info():
    """Get latest release info from GitHub API."""
    try:
        req = Request(RELEASES_API, headers={"User-Agent": "CyberTeacher-Asset-Downloader"})
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"⚠️ Could not fetch release info: {e}")
        return None


def download_profile_assets(profile: str, base_dir: Path, force: bool = False) -> bool:
    """Download all assets for a given profile."""
    if profile not in ASSETS:
        print(f"❌ Unknown profile: {profile}. Available: {list(ASSETS.keys())}")
        return False

    assets = ASSETS[profile]
    if not assets:
        print(f"✅ Profile '{profile}' requires no extra assets.")
        return True

    print(f"\n📦 Downloading assets for profile: {profile}")
    print(f"   Target: {base_dir}")
    print(f"   Assets: {', '.join(assets)}")

    # Ensure base directory exists
    base_dir.mkdir(parents=True, exist_ok=True)

    success = True
    for asset in assets:
        url = f"{RELEASES_URL}/{asset}"
        dest = base_dir / asset

        if dest.exists() and not force:
            print(f"⏭️  {asset} already exists, skipping (use --force to re-download)")
            continue

        print(f"⬇️  Downloading {asset}...")
        if not download_file(url, base_dir / asset):
            print(f"❌ Failed to download {asset}")
            success = False
            continue

        # Extract if tar.gz
        if asset.endswith(".tar.gz"):
            if not extract_archive(base_dir / asset, base_dir):
                success = False
            else:
                # Remove archive after extraction
                (base_dir / asset).unlink()

    return success


def main():
    parser = argparse.ArgumentParser(description="Download CyberTeacher assets from GitHub Releases")
    parser.add_argument("--profile", choices=["minimal", "full", "research"], default="full",
                        help="Installation profile (default: full)")
    parser.add_argument("--dir", type=Path, default=Path("./local"),
                        help="Target directory for assets (default: ./local)")
    parser.add_argument("--force", action="store_true", help="Re-download existing files")
    parser.add_argument("--list", action="store_true", help="List available profiles and assets")
    args = parser.parse_args()

    if args.list:
        print("Available profiles:")
        for profile, assets in ASSETS.items():
            print(f"  {profile}: {', '.join(assets) if assets else '(no extra assets)'}")
        return 0

    print(f"🔧 CyberTeacher Asset Downloader")
    print(f"   Profile: {args.profile}")
    print(f"   Target dir: {args.dir}")

    # Check if release exists
    release_info = get_latest_release_info()
    if release_info:
        print(f"📦 Latest release: {release_info.get('tag_name', 'unknown')}")
    else:
        print("⚠️ Could not fetch release info, using default download URLs")

    success = download_profile_assets(args.profile, args.dir, args.force)

    if success:
        print(f"\n✅ All assets downloaded successfully to {args.dir}")
        return 0
    else:
        print(f"\n❌ Some assets failed to download")
        return 1


if __name__ == "__main__":
    from urllib.request import urlopen, Request
    import json
    from urllib.error import URLError, HTTPError

    sys.exit(main())