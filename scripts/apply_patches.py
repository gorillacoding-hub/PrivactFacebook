#!/usr/bin/env python3
"""PrivacyFBLite patches for Facebook Lite — runtime Block hook + Settings UI."""
from __future__ import annotations
import json, os, re, shutil, sys
from pathlib import Path

DISABLE_MODULES = {
    "profilo", "multisignalanrdetector", "shared_fizz_ms_profilo",
    "s_libunwindstack_profilo", "s_multisignalanrdetector_profilo",
    "heroplayer", "mediastreaming", "boost",
    "s_heroplayer_rtc", "s_mediastreaming_msys_rtc", "s_mediastreaming_msysinfra",
    "s_mediastreaming_rtc", "s_boost_msys", "s_boost_msysinfra",
    "s_blokscamera_heroplayer_idcapture",
}

GRAPHQL_POISON = [
    "FBLitePYMKQuery", "FBLitePymkSuggestionBlacklistMutation",
    "FBLiteStoryByIdQuery", "FBLiteSafetyNoticeImpressionReportMutation",
    "FBLiteGenAINuxConsentStatusQuery", "FBLiteGenAIWriteConsentMutation",
]


def copy_extension_smali(apk_root: Path, ext_src: Path) -> None:
    dest = apk_root / "smali" / "com" / "privacyfblite" / "extension"
    dest.mkdir(parents=True, exist_ok=True)
    src = ext_src / "com" / "privacyfblite" / "extension"
    if not src.exists():
        # fallback relative to script
        print("    ERROR: extension_smali not found")
        return
    for f in src.glob("*.smali"):
        shutil.copy2(f, dest / f.name)
        print(f"    + {f.name}")


def patch_application_oncreate(apk_root: Path) -> bool:
    path = apk_root / "smali" / "com" / "facebook" / "lite" / "ClientApplicationSplittedShell.smali"
    if not path.exists():
        print("    Application class not found")
        return False
    text = path.read_text(encoding="utf-8")
    if "PrivacyInit" in text:
        print("    Application already patched")
        return True
    needle = """.method public final onCreate()V
    .locals 5

    .line 0
    invoke-super {p0}, Landroid/app/Application;->onCreate()V
"""
    inject = """.method public final onCreate()V
    .locals 5

    .line 0
    invoke-super {p0}, Landroid/app/Application;->onCreate()V

    # PrivacyFBLite init
    invoke-static {p0}, Lcom/privacyfblite/extension/PrivacyInit;->init(Landroid/content/Context;)V
"""
    if needle not in text:
        # try without .line
        needle2 = "invoke-super {p0}, Landroid/app/Application;->onCreate()V"
        if needle2 in text and "PrivacyInit" not in text:
            text = text.replace(
                needle2,
                needle2 + "\n\n    invoke-static {p0}, Lcom/privacyfblite/extension/PrivacyInit;->init(Landroid/content/Context;)V",
                1,
            )
            path.write_text(text, encoding="utf-8")
            print("    Application.onCreate hooked (fallback)")
            return True
        print("    could not find onCreate inject point")
        return False
    text = text.replace(needle, inject, 1)
    path.write_text(text, encoding="utf-8")
    print("    Application.onCreate -> PrivacyInit.init")
    return True


def patch_http_url_connection(apk_root: Path) -> bool:
    """Inject Block.shouldBlock into LX/03z.AE6(URL)."""
    path = apk_root / "smali" / "X" / "03z.smali"
    if not path.exists():
        print("    LX/03z.smali not found — network hook skipped")
        return False
    text = path.read_text(encoding="utf-8")
    if "PrivacyFBLite" in text or "shouldBlock" in text:
        print("    network hook already present")
        return True
    old = """.method public final AE6(Ljava/net/URL;)Ljava/net/HttpURLConnection;
    .locals 6

    .line 0
    invoke-virtual {p1}, Ljava/net/URL;->openConnection()Ljava/net/URLConnection;
"""
    new = """.method public final AE6(Ljava/net/URL;)Ljava/net/HttpURLConnection;
    .locals 6

    .line 0
    # PrivacyFBLite network block
    invoke-virtual {p1}, Ljava/net/URL;->toString()Ljava/lang/String;
    move-result-object v0
    invoke-static {v0}, Lcom/privacyfblite/extension/Block;->shouldBlock(Ljava/lang/String;)Z
    move-result v0
    if-eqz v0, :pfl_ok
    new-instance v0, Ljava/io/IOException;
    const-string v1, "blocked by PrivacyFBLite"
    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V
    throw v0
    :pfl_ok

    invoke-virtual {p1}, Ljava/net/URL;->openConnection()Ljava/net/URLConnection;
"""
    if old not in text:
        # looser match
        old2 = "invoke-virtual {p1}, Ljava/net/URL;->openConnection()Ljava/net/URLConnection;"
        if old2 not in text:
            print("    AE6 openConnection not found")
            return False
        insert = """invoke-virtual {p1}, Ljava/net/URL;->toString()Ljava/lang/String;
    move-result-object v0
    invoke-static {v0}, Lcom/privacyfblite/extension/Block;->shouldBlock(Ljava/lang/String;)Z
    move-result v0
    if-eqz v0, :pfl_ok
    new-instance v0, Ljava/io/IOException;
    const-string v1, "blocked by PrivacyFBLite"
    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V
    throw v0
    :pfl_ok

    invoke-virtual {p1}, Ljava/net/URL;->openConnection()Ljava/net/URLConnection;"""
        text = text.replace(old2, insert, 1)
    else:
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    print("    LX/03z.AE6 network hook installed")
    return True


def patch_manifest(apk_root: Path) -> None:
    manifest = apk_root / "AndroidManifest.xml"
    text = manifest.read_text(encoding="utf-8")
    if "privacyfblite.extension.SettingsActivity" in text:
        print("    SettingsActivity already in manifest")
        return
    activity = '''
        <activity android:exported="true" android:label="PrivacyFBLite Settings" android:name="com.privacyfblite.extension.SettingsActivity" android:theme="@android:style/Theme.DeviceDefault.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
            <intent-filter>
                <action android:name="com.privacyfblite.SETTINGS"/>
                <category android:name="android.intent.category.DEFAULT"/>
            </intent-filter>
        </activity>
'''
    # insert before </application>
    if "</application>" not in text:
        print("    manifest: no </application>")
        return
    text = text.replace("</application>", activity + "    </application>", 1)
    # strip AD_ID perms
    for perm in (
        "com.google.android.gms.permission.AD_ID",
        "android.permission.ACCESS_ADSERVICES_AD_ID",
        "android.permission.ACCESS_ADSERVICES_ATTRIBUTION",
        "android.permission.REQUEST_INSTALL_PACKAGES",
    ):
        text = re.sub(
            rf'<uses-permission[^>]*android:name="{re.escape(perm)}"[^/]*/>\s*',
            "",
            text,
        )
    manifest.write_text(text, encoding="utf-8")
    print("    SettingsActivity + LAUNCHER added; AD_ID perms removed")


def disable_modules(apk_root: Path) -> int:
    path = apk_root / "assets" / "app_modules.json"
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for mod in data.get("downloadable", []):
        name = mod.get("name", "")
        if name in DISABLE_MODULES and not mod.get("disabled"):
            mod["disabled"] = True
            n += 1
            print(f"    disable module: {name}")
    if n:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return n


def poison_graphql(apk_root: Path) -> int:
    path = apk_root / "assets" / "fblite-client_client_persist_ids.json"
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for key in GRAPHQL_POISON:
        if key in data:
            data[key]["operation_name"] = "PrivacyBlocked"
            data[key]["operation_name_hash"] = "0"
            data[key]["client_doc_id"] = "0"
            n += 1
            print(f"    poison op: {key}")
    if n:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return n


def wipe_falco(apk_root: Path) -> int:
    base = apk_root / "assets" / "com" / "facebook" / "logginginfra"
    n = 0
    if not base.exists():
        return 0
    for p in base.rglob("*"):
        if p.is_file():
            p.write_bytes(b"")
            n += 1
    if n:
        print(f"    wiped {n} logginginfra files")
    return n


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: apply_patches.py <decompiled-apk-root> [extension_smali_root]")
        return 1
    apk_root = Path(sys.argv[1])
    script_dir = Path(__file__).resolve().parent
    project = script_dir.parent
    ext_src = Path(sys.argv[2]) if len(sys.argv) > 2 else project / "extension_smali"

    print("==> extension smali")
    copy_extension_smali(apk_root, ext_src)

    print("==> Application.onCreate")
    patch_application_oncreate(apk_root)

    print("==> network hook LX/03z")
    patch_http_url_connection(apk_root)

    print("==> AndroidManifest")
    patch_manifest(apk_root)

    print("==> modules")
    disable_modules(apk_root)

    print("==> GraphQL ops")
    poison_graphql(apk_root)

    print("==> logginginfra")
    wipe_falco(apk_root)

    print("==> patches applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
