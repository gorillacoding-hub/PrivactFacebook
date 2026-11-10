#!/usr/bin/env python3
"""Rename package id for side-by-side install (com.facebook.lite.privacy)."""
from __future__ import annotations
import re, sys
from pathlib import Path

ORIGINAL = "com.facebook.lite"
CLONE = "com.facebook.lite.privacy"

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: clone_package.py <decompiled-apk-root>")
        return 1
    root = Path(sys.argv[1])
    manifest = root / "AndroidManifest.xml"
    if not manifest.exists():
        print("AndroidManifest.xml not found")
        return 1
    text = manifest.read_text(encoding="utf-8", errors="ignore")
    text = text.replace(f'package="{ORIGINAL}"', f'package="{CLONE}"')
    text = text.replace(f'android:name="{ORIGINAL}"', f'android:name="{CLONE}"')
    text = re.sub(
        rf'android:authorities="([^"]*){re.escape(ORIGINAL)}([^"]*)"',
        rf'android:authorities="\1{CLONE}\2"',
        text,
    )
    manifest.write_text(text, encoding="utf-8")
    print(f"    package renamed to {CLONE}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
