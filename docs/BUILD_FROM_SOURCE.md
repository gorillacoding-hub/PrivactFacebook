# Build from source

1. Install `apktool`, JDK 17+, Python 3.
2. Obtain a trusted Facebook Lite APK (e.g. APKMirror, arm64).
3. Run:

```bash
chmod +x build.sh
./build.sh /path/to/facebook-lite.apk
```

Or download during build:

```bash
./build.sh --url "https://..."
```

Flags: `--clone` (side-by-side package), `--install` (adb).
