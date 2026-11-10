#!/usr/bin/env python3
"""
PrivacyFBLite patch applicator for Facebook Lite (com.facebook.lite).

Based on analysis of Facebook Lite 539:
- UI is largely remote Bloks; local surface is modules + network.
- Blocks tracking, ads, News Feed ranking paths, Reels/short-video modules,
  PYMK suggestions, and analytics native plugins.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Downloadable modules to DISABLE (set disabled=true in app_modules.json)
# Keep messaging stack (msys/msysinfra/rtc) intact.
# ---------------------------------------------------------------------------
DISABLE_MODULES = {
    # Tracking / performance phone-home
    "profilo",
    "multisignalanrdetector",
    "shared_fizz_ms_profilo",
    "s_libunwindstack_profilo",
    "s_multisignalanrdetector_profilo",
    # Video / Reels-like playback & streaming
    "heroplayer",
    "mediastreaming",
    "boost",
    "s_heroplayer_rtc",
    "s_mediastreaming_msys_rtc",
    "s_mediastreaming_msysinfra",
    "s_mediastreaming_rtc",
    "s_boost_msys",
    "s_boost_msysinfra",
    "s_blokscamera_heroplayer_idcapture",
    # Optional heavy camera stacks not needed for basic messaging
    "blokscamera",
    "s_blokscamera_boost_idcapture_selfiecapture",
    "s_blokscamera_camera",
    "s_blokscamera_idcapture_rtc_selfiecapture",
    "s_blokscamera_idcapture_selfiecapture",
    "s_idcapture_mediastreaming_rtc_selfiecapture",
    "s_idcapture_rtc_selfiecapture",
    "s_idcapture_selfiecapture",
    "selfiecapture",
    "idcapture",
}

# Modules we explicitly keep enabled (documentation only)
KEEP_MODULES = {
    "msys", "msysinfra", "rtc", "mnshttp", "fizz",
    "camera", "inappbrowser", "uiqr", "libunwindstack",
}

# Network / string fragments to neuter inside smali/xml/json
TELEMETRY_PATHS = [
    # Beacons & pixels
    "/ajax/bz", "/tr/", "/tr?",
    "pixel.facebook.com", "www.facebook.com/tr", "www.facebook.com/ajax/bz",
    "b-www.facebook.com", "snaptu-z.facebook.com", "an.facebook.com",
    "error.facebook.com", "crashlogs.facebook.com", "lookaside.facebook.com",
    # Analytics
    "graph.facebook.com/logging", "/logging_client_events", "/mobile/client_event",
    "client_event", "analytics_logger", "analytics_session_id",
    "analytics_logger_to_file", "analytics_logger_file_session_id",
    "rebound_analytics_session_id", "app_analytics", "e2e/analytics_events",
    "files/mqtt_analytics", "X-FB-Request-Analytics-Tags",
    "LiteAnalyticsPlugin", "mailboxanalyticslogging",
    "pando-graphql-analytics", "pando_consistency_analytics", "xanalyticsadapter",
    # Telemetry / perf
    "app_start_memory_telemetry", "memory_telemetry_state", "unifiedtelemetry",
    "reliability_event_log_upload", "perflogger", "jniperflogger", "perfloggerxplat",
    "BatteryMetrics", "battery_checkin", "periodic_battery", "PERIODIC_BATTERY",
    "AppStateLogger", "APPSTATELOGGER_CRASH",
    "libprofilo", "profilo_mmapbuf", "profilo_multi_buffer_logger",
    "profilo_stacktrace", "fbandroid_libraries_profilo",
    # Ads
    "/ads/", "ads.facebook.com", "an.facebook.com/ads", "/sponsored",
    "adnetwork", "ad_id", "advertising_id",
    # News Feed / ranking
    "newsfeed", "NewsFeed", "news_feed", "/feed/section", "/feed/scroll",
    "/feed/stories", "edge_story", "feed_ranking", "ranked_feed",
    "feed_unit_entries", "feed_unit",
    # Reels / short video
    "reels", "Reels", "short_form_video", "clips_tab", "fb_shorts",
    "video_expression_loader", "heroplayer", "mediastreaming",
    # Suggestions / PYMK / discovery
    "FBLitePYMKQuery", "FBLitePymkSuggestionBlacklistMutation",
    "pymk", "PYMK", "people_you_may_know", "suggested_friends",
    # Experiment / config tracking
    "LiteExperimentsMobileConfig", "MsysExperimentCache", "MCIAppExperiments",
    "mobileconfig_canary", "mobileconfig-jni",
    # Crash / logging plugins
    "bugreporter", "BugReport", "breakpad_write_only_crash_thread",
    "FBLiteFileManagerExceptionLogger", "FbPluginsLogger", "bloks_logging_id",
    "AppNetoworkStateProviderForLogging", "rsysfilelogging",
    "logginginfra", "falco",
]

STRING_NEUTERS = [
    (r'"com\.facebook\.analytics[^"]*"', '"com.privacyfblite.disabled"'),
    (r'"com\.facebook\.logging[^"]*"', '"com.privacyfblite.disabled"'),
    (r'"com\.facebook\.wearable\.system\.analytics[^"]*"', '"com.privacyfblite.disabled"'),
    (r'"com\.facebook\.wearable\.system\.unifiedtelemetry[^"]*"', '"com.privacyfblite.disabled"'),
    (r'"com\.oculus\.telemetry[^"]*"', '"com.privacyfblite.disabled"'),
    (r'"com\.oculus\.unifiedtelemetry[^"]*"', '"com.privacyfblite.disabled"'),
    (r'"LiteAnalyticsPluginjni"', '"DisabledPlugin"'),
    (r'"libLiteAnalyticsPluginjni_so"', '"libdisabled_so"'),
    (r'"libmailboxanalyticsloggingjni_so"', '"libdisabled_so"'),
    (r'"libxanalyticsadapter_jni_so"', '"libdisabled_so"'),
    (r'"libpando_graphql_analytics_so"', '"libdisabled_so"'),
    (r'"libjniperflogger_so"', '"libdisabled_so"'),
    (r'"libperfloggerxplat_init_lite_so"', '"libdisabled_so"'),
    (r'"libperfloggerxplat_cr_bridge_so"', '"libdisabled_so"'),
    (r'"libprofilo[^"]*"', '"libdisabled_so"'),
    (r'"libheroplayer[^"]*"', '"libdisabled_so"'),
    (r'"libmediastreaming[^"]*"', '"libdisabled_so"'),
    (r'"enable_telemetry"', '"false"'),
    (r'"enable_analytics"', '"false"'),
    (r'"analytics_enabled"', '"false"'),
    (r'"telemetry_enabled"', '"false"'),
    (r'"X-FB-Request-Analytics-Tags"', '"X-Privacy-Disabled"'),
    (r'snaptu-z\.facebook\.com', 'privacyfblite.blocked.invalid'),
    (r'b-www\.facebook\.com', 'privacyfblite.blocked.invalid'),
    (r'"FBLitePYMKQuery"', '"PrivacyBlockedQuery"'),
    (r'"FBLitePymkSuggestionBlacklistMutation"', '"PrivacyBlockedMutation"'),
    (r'"FBLiteStoryByIdQuery"', '"PrivacyBlockedQuery"'),
]

MANIFEST_REMOVE_PERMISSIONS = [
    "android.permission.REQUEST_INSTALL_PACKAGES",
    "com.google.android.gms.permission.AD_ID",
    "com.google.android.gms.permission.AD_ID_PERMISSION",
    "android.permission.ACCESS_ADSERVICES_ATTRIBUTION",
    "android.permission.ACCESS_ADSERVICES_AD_ID",
]

MANIFEST_REMOVE_NAME_PATTERNS = [
    r"[Aa]nalytics", r"[Tt]elemetry", r"[Tt]racking",
    r"[Cc]rash[Rr]eporter", r"[Bb]ug[Rr]eport",
    r"[Pp]erflogger", r"[Pp]rofilo",
    r"AppStateLogger", r"BatteryMetrics",
]


def disable_app_modules(apk_root: Path) -> int:
    """Set disabled=true on tracking / Reels / video modules."""
    path = apk_root / "assets" / "app_modules.json"
    if not path.exists():
        print("    app_modules.json not found — skip module disable")
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for mod in data.get("downloadable", []):
        name = mod.get("name", "")
        if name in DISABLE_MODULES and not mod.get("disabled", False):
            mod["disabled"] = True
            changed += 1
            print(f"    disable module: {name}")
    if changed:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return changed


def neutralize_logginginfra(apk_root: Path) -> int:
    """Wipe falco / logginginfra metadata so log pipeline cannot load configs."""
    base = apk_root / "assets" / "com" / "facebook" / "logginginfra"
    if not base.exists():
        return 0
    n = 0
    for path in base.rglob("*"):
        if path.is_file():
            # empty the file — loader gets no usable config
            path.write_bytes(b"")
            n += 1
            print(f"    wiped logginginfra: {path.relative_to(apk_root)}")
    return n


def neutralize_client_ops(apk_root: Path) -> int:
    """Rename suggestion / story GraphQL op ids so client cannot resolve them."""
    path = apk_root / "assets" / "fblite-client_client_persist_ids.json"
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    block_keys = [
        "FBLitePYMKQuery",
        "FBLitePymkSuggestionBlacklistMutation",
        "FBLiteStoryByIdQuery",
        "FBLiteSafetyNoticeImpressionReportMutation",
        "FBLiteGenAINuxConsentStatusQuery",
        "FBLiteGenAIWriteConsentMutation",
    ]
    changed = 0
    for key in block_keys:
        if key in data:
            # poison operation_name so server rejects / client skips
            entry = data[key]
            entry["operation_name"] = "PrivacyBlocked"
            entry["operation_name_hash"] = "0"
            entry["client_doc_id"] = "0"
            changed += 1
            print(f"    poison GraphQL op: {key}")
    if changed:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return changed


def inject_block_helper(apk_root: Path) -> None:
    smali_dirs = list(apk_root.glob("smali*")) or [apk_root / "smali"]
    target = smali_dirs[0] / "com" / "privacyfblite" / "extension"
    target.mkdir(parents=True, exist_ok=True)
    smali = r'''
.class public final Lcom/privacyfblite/extension/Block;
.super Ljava/lang/Object;

.method public static shouldBlock(Ljava/lang/String;)Z
    .locals 3
    if-nez p0, :no
    invoke-virtual {p0}, Ljava/lang/String;->toLowerCase()Ljava/lang/String;
    move-result-object v0
    const-string v1, "telemetry"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "analytics"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "/ads/"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "/tr/"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "/ajax/bz"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "newsfeed"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "reels"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "pymk"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "pixel.facebook"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "snaptu-z.facebook"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "logging_client"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "perflogger"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "profilo"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "heroplayer"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "mediastreaming"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    const-string v1, "feed_unit"
    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z
    move-result v2
    if-eqz v2, :yes
    goto :no
    :yes
    const/4 v0, 0x1
    return v0
    :no
    const/4 v0, 0x0
    return v0
.end method
'''.lstrip()
    (target / "Block.smali").write_text(smali, encoding="utf-8")


def clean_manifest(apk_root: Path) -> int:
    manifest = apk_root / "AndroidManifest.xml"
    if not manifest.exists():
        return 0
    text = manifest.read_text(encoding="utf-8", errors="ignore")
    original = text
    changes = 0
    for perm in MANIFEST_REMOVE_PERMISSIONS:
        new_text, n = re.subn(
            rf'<uses-permission[^>]*android:name="{re.escape(perm)}"[^/]*/>\s*',
            "", text)
        text, changes = new_text, changes + n
        new_text, n = re.subn(
            rf'<uses-permission[^>]*android:name="{re.escape(perm)}"[^>]*>.*?</uses-permission>\s*',
            "", text, flags=re.DOTALL)
        text, changes = new_text, changes + n
    for pattern in MANIFEST_REMOVE_NAME_PATTERNS:
        new_text, n = re.subn(
            rf'<(activity|service|receiver|provider)[^>]*android:name="[^"]*{pattern}[^"]*"[^>]*>.*?</\1>\s*',
            "", text, flags=re.DOTALL | re.IGNORECASE)
        text, changes = new_text, changes + n
        new_text, n = re.subn(
            rf'<(activity|service|receiver|provider)[^>]*android:name="[^"]*{pattern}[^"]*"[^/]*/>\s*',
            "", text, flags=re.IGNORECASE)
        text, changes = new_text, changes + n
    if text != original:
        manifest.write_text(text, encoding="utf-8")
    return changes


def scrub_file(path: Path) -> bool:
    try:
        text = path.read_bytes().decode("utf-8")
    except Exception:
        return False
    original = text
    for frag in TELEMETRY_PATHS:
        if frag in text:
            text = text.replace(frag, "privacyfblite_blocked/" + frag.lstrip("/"))
    for pattern, repl in STRING_NEUTERS:
        text = re.sub(pattern, repl, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def scrub_resources(apk_root: Path) -> int:
    changed = 0
    for root, _, files in os.walk(apk_root):
        for name in files:
            if not name.endswith((".smali", ".xml", ".json", ".txt", ".properties")):
                continue
            if scrub_file(Path(root) / name):
                changed += 1
    return changed


def neutralize_native_deps(apk_root: Path) -> None:
    path = apk_root / "assets" / "native_deps.txt"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    for k in ("profilo", "perflogger", "analytics", "xanalytics",
              "mailboxanalytics", "LiteAnalytics", "jniperflogger",
              "heroplayer", "mediastreaming"):
        text = re.sub(re.escape(k), "disabled", text, flags=re.IGNORECASE)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("    neutralized native_deps.txt")


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: apply_patches.py <decompiled-apk-root> <patches-dir>")
        return 1
    apk_root = Path(sys.argv[1])
    if not apk_root.is_dir():
        print(f"Error: {apk_root} is not a directory")
        return 1

    print("==> [modules] disable Feed/Reels/tracking downloadable modules")
    n_mod = disable_app_modules(apk_root)
    print(f"    modules disabled: {n_mod}")

    print("==> [graphql] poison PYMK / story / impression ops")
    n_ops = neutralize_client_ops(apk_root)
    print(f"    ops poisoned: {n_ops}")

    print("==> [logging] wipe logginginfra/falco configs")
    n_log = neutralize_logginginfra(apk_root)
    print(f"    files wiped: {n_log}")

    print("==> [block] inject Block.smali helper")
    inject_block_helper(apk_root)

    print("==> [manifest] strip AD_ID / analytics components")
    n_man = clean_manifest(apk_root)
    print(f"    manifest edits: {n_man}")

    print("==> [strings] scrub telemetry / feed / reels / ads paths")
    n_scr = scrub_resources(apk_root)
    print(f"    files modified: {n_scr}")

    print("==> [native] neutralize analytics lib names")
    neutralize_native_deps(apk_root)

    print("==> done — tracking + Feed/Reels modules + suggestions blocked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
