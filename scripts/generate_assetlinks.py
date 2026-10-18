#!/usr/bin/env python3
"""
Generate SHA256 certificate fingerprint for TWA assetlinks.json

Usage:
    python scripts/generate_assetlinks.py --keystore debug.keystore --alias androiddebugkey
    python scripts/generate_assetlinks.py --apk app-release.apk

Outputs the fingerprint to add to static/.well-known/assetlinks.json
"""

import argparse
import hashlib
import subprocess
import sys
import os


def get_fingerprint_from_keystore(keystore_path: str, alias: str, storepass: str = "android", keypass: str = "android") -> str:
    """Extract SHA256 fingerprint from keystore."""
    try:
        result = subprocess.run([
            "keytool", "-list", "-v",
            "-keystore", keystore_path,
            "-alias", alias,
            "-storepass", storepass,
            "-keypass", keypass
        ], capture_output=True, text=True, check=True)
        
        for line in result.stdout.split('\n'):
            if "SHA256:" in line:
                return line.split("SHA256:")[1].strip()
    except subprocess.CalledProcessError as e:
        print(f"Error extracting from keystore: {e.stderr}", file=sys.stderr)
    return None


def get_fingerprint_from_apk(apk_path: str) -> str:
    """Extract SHA256 fingerprint from APK (requires apksigner)."""
    try:
        result = subprocess.run([
            "apksigner", "verify", "--print-certs", apk_path
        ], capture_output=True, text=True, check=True)
        
        for line in result.stdout.split('\n'):
            if "SHA-256 digest:" in line:
                return line.split("SHA-256 digest:")[1].strip().replace(" ", ":").upper()
    except subprocess.CalledProcessError as e:
        print(f"Error extracting from APK: {e.stderr}", file=sys.stderr)
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate SHA256 fingerprint for TWA assetlinks.json")
    parser.add_argument("--keystore", help="Path to keystore file (e.g., debug.keystore)")
    parser.add_argument("--alias", default="androiddebugkey", help="Key alias (default: androiddebugkey)")
    parser.add_argument("--storepass", default="android", help="Keystore password (default: android)")
    parser.add_argument("--keypass", default="android", help="Key password (default: android)")
    parser.add_argument("--apk", help="Path to signed APK file")
    parser.add_argument("--package", default="com.cyberteacher.app", help="Android package name")
    parser.add_argument("--output", help="Output assetlinks.json path")
    
    args = parser.parse_args()
    
    fingerprint = None
    if args.keystore:
        fingerprint = get_fingerprint_from_keystore(args.keystore, args.alias, args.storepass, args.keypass)
    elif args.apk:
        fingerprint = get_fingerprint_from_apk(args.apk)
    else:
        parser.error("Either --keystore or --apk is required")
    
    if not fingerprint:
        print("Failed to extract fingerprint", file=sys.stderr)
        sys.exit(1)
    
    print(f"SHA256 Fingerprint: {fingerprint}")
    
    assetlinks = [{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": args.package,
            "sha256_cert_fingerprints": [fingerprint]
        }
    }]
    
    import json
    output_json = json.dumps(assetlinks, indent=2)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Written to {args.output}")
    else:
        print("\nAdd this to static/.well-known/assetlinks.json:")
        print(output_json)


if __name__ == "__main__":
    main()