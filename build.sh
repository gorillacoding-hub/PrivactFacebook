#!/usr/bin/env bash
#
# PrivacyFBLite — patch Facebook Lite for privacy.
#
#   ./build.sh <facebook-lite.apk> [--clone] [--install]
#   ./build.sh --url <download-url> [--clone] [--install]
#
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$DIR/privacyfblite.apk"
WORKDIR="$DIR/build/work"

CLONE=0
INSTALL=0
APK=""
URL=""

usage() {
    echo "Usage: $0 <facebook-lite.apk> [--clone] [--install]"
    echo "       $0 --url <apk-download-url> [--clone] [--install]"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --url) URL="$2"; shift 2 ;;
        --clone) CLONE=1; shift ;;
        --install) INSTALL=1; shift ;;
        -h|--help) usage ;;
        *)
            if [[ -z "$APK" && -f "$1" ]]; then APK="$1"
            else echo "Unknown: $1" >&2; usage; fi
            shift ;;
    esac
done

if [[ -n "$URL" ]]; then
    echo "==> [0/5] Downloading APK"
    mkdir -p "$DIR/build"
    APK="$DIR/build/original.apk"
    if command -v curl >/dev/null 2>&1; then
        curl -L --fail -o "$APK" "$URL"
    elif command -v wget >/dev/null 2>&1; then
        wget -O "$APK" "$URL"
    else
        echo "Error: need curl or wget for --url" >&2; exit 1
    fi
fi

if [[ -z "$APK" || ! -f "$APK" ]]; then
    echo "Error: provide Facebook Lite APK path or --url" >&2
    usage
fi

APKTOOL="$(command -v apktool || true)"
ZIPALIGN="$(command -v zipalign || true)"
APKSIGNER="$(command -v apksigner || true)"

if [[ -z "$APKTOOL" ]]; then
    echo "Error: apktool not found in PATH" >&2
    exit 1
fi

rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"

echo "==> [1/5] Decompiling $(basename "$APK")"
"$APKTOOL" d -f -o "$WORKDIR/apk" "$APK"

echo "==> [2/5] Applying privacy patches (modules + tracking + feed/reels)"
python3 "$DIR/scripts/apply_patches.py" "$WORKDIR/apk" "$DIR/patches"

if [[ "$CLONE" -eq 1 ]]; then
    echo "    clone package id"
    python3 "$DIR/scripts/clone_package.py" "$WORKDIR/apk"
fi

echo "==> [3/5] Rebuilding"
"$APKTOOL" b -f -o "$WORKDIR/unsigned.apk" "$WORKDIR/apk"

echo "==> [4/5] Align + sign"
ALIGNED="$WORKDIR/aligned.apk"
if [[ -n "$ZIPALIGN" ]]; then
    "$ZIPALIGN" -f 4 "$WORKDIR/unsigned.apk" "$ALIGNED"
else
    cp "$WORKDIR/unsigned.apk" "$ALIGNED"
fi

KEYSTORE="$DIR/build/debug.keystore"
if [[ ! -f "$KEYSTORE" ]]; then
    keytool -genkeypair -v -keystore "$KEYSTORE" -storepass android \
        -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 \
        -validity 10000 -dname "CN=PrivacyFBLite, OU=Local, O=Local, L=Local, S=Local, C=US" \
        >/dev/null 2>&1 || true
fi

if [[ -n "$APKSIGNER" && -f "$KEYSTORE" ]]; then
    "$APKSIGNER" sign --ks "$KEYSTORE" --ks-pass pass:android \
        --key-pass pass:android --out "$OUT" "$ALIGNED"
else
    jarsigner -keystore "$KEYSTORE" -storepass android -keypass android \
        "$ALIGNED" androiddebugkey 2>/dev/null || true
    cp "$ALIGNED" "$OUT"
fi

echo "==> [5/5] Output: $OUT"
ls -lh "$OUT"

if [[ "$INSTALL" -eq 1 ]] && command -v adb >/dev/null 2>&1; then
    adb install -r "$OUT" || true
fi

echo ""
echo "Do not redistribute the APK if it still contains proprietary Facebook code."
