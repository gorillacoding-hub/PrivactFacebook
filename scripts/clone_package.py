#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
ORIGINAL, CLONE = "com.facebook.lite", "com.facebook.lite.privacy"
def main():
    root = Path(sys.argv[1])
    m = root / "AndroidManifest.xml"
    t = m.read_text(encoding="utf-8", errors="ignore")
    t = t.replace(f'package="{ORIGINAL}"', f'package="{CLONE}"')
    t = re.sub(rf'android:authorities="([^"]*){re.escape(ORIGINAL)}([^"]*)"', rf'android:authorities="\1{CLONE}\2"', t)
    m.write_text(t, encoding="utf-8")
    print(f"    package -> {CLONE}")
if __name__ == "__main__":
    main()
