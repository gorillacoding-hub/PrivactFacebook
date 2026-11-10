#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$DIR/privacyfblite.apk"
WORKDIR="$DIR/build/work"
CLONE=0; INSTALL=0; APK=""; URL=""
usage(){ echo "Usage: $0 <facebook-lite.apk>|--url URL [--clone] [--install]"; exit 1; }
while [[ $# -gt 0 ]]; do
  case "$1" in
    --url) URL="$2"; shift 2;;
    --clone) CLONE=1; shift;;
    --install) INSTALL=1; shift;;
    -h|--help) usage;;
    *) [[ -z "$APK" && -f "$1" ]] && APK="$1" || usage; shift;;
  esac
done
if [[ -n "$URL" ]]; then
  mkdir -p "$DIR/build"; APK="$DIR/build/original.apk"
  curl -L --fail -o "$APK" "$URL" || wget -O "$APK" "$URL"
fi
[[ -n "$APK" && -f "$APK" ]] || usage

APKTOOL_JAR="$DIR/tools/apktool.jar"
if [[ -f "$APKTOOL_JAR" ]]; then
  APKTOOL=(java -jar "$APKTOOL_JAR")
elif command -v apktool >/dev/null; then
  APKTOOL=(apktool)
else
  echo "Need apktool or tools/apktool.jar"; exit 1
fi

rm -rf "$WORKDIR"; mkdir -p "$WORKDIR"
echo "==> [1/5] Decompile"
"${APKTOOL[@]}" d -f -o "$WORKDIR/apk" "$APK"
echo "==> [2/5] Patch"
python3 "$DIR/scripts/apply_patches.py" "$WORKDIR/apk" "$DIR/extension_smali"
[[ "$CLONE" -eq 1 ]] && python3 "$DIR/scripts/clone_package.py" "$WORKDIR/apk"
echo "==> [3/5] Rebuild"
"${APKTOOL[@]}" b -f -o "$WORKDIR/unsigned.apk" "$WORKDIR/apk"
echo "==> [4/5] Align/sign"
ALIGNED="$WORKDIR/aligned.apk"
if command -v zipalign >/dev/null; then zipalign -f 4 "$WORKDIR/unsigned.apk" "$ALIGNED"; else cp "$WORKDIR/unsigned.apk" "$ALIGNED"; fi
KEYSTORE="$DIR/build/debug.keystore"
[[ -f "$KEYSTORE" ]] || keytool -genkeypair -v -keystore "$KEYSTORE" -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=PrivacyFBLite" >/dev/null 2>&1 || true
if command -v apksigner >/dev/null; then
  apksigner sign --ks "$KEYSTORE" --ks-pass pass:android --key-pass pass:android --out "$OUT" "$ALIGNED"
else
  jarsigner -keystore "$KEYSTORE" -storepass android -keypass android "$ALIGNED" androiddebugkey 2>/dev/null || true
  cp "$ALIGNED" "$OUT"
fi
echo "==> [5/5] $OUT"; ls -lh "$OUT"
[[ "$INSTALL" -eq 1 ]] && command -v adb >/dev/null && adb install -r "$OUT" || true
echo "Open settings: second launcher icon «PrivacyFBLite Settings»"
