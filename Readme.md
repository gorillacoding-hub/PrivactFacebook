# PrivacyFBLite

Privacy-focused **patch toolkit** for the official Facebook Lite Android app (`com.facebook.lite`).

**Open-source patch layer only** — does not ship Facebook’s proprietary code.

## Goals

1. Block tracking / telemetry / analytics
2. Disable News Feed ranking paths and suggestion surfaces (PYMK)
3. Disable Reels / short-video modules (heroplayer, mediastreaming, boost)
4. Strip ad-related permissions and paths
5. Keep messaging stack (msys / msysinfra / rtc) working
6. Local-only build — no remote code download, no auto-updater

## What is blocked (Facebook Lite 539 analysis)

| Category | Action |
|----------|--------|
| **Modules disabled** | profilo, multisignalanrdetector, heroplayer, mediastreaming, boost, blokscamera (+ related composites) |
| **Modules kept** | msys, msysinfra, rtc, mnshttp, fizz, camera, inappbrowser |
| **GraphQL ops poisoned** | FBLitePYMKQuery, PYMK blacklist, StoryById, impression report, GenAI consent |
| **logginginfra/falco** | Config files wiped |
| **Network strings** | /tr/, /ajax/bz, pixel.*, snaptu-z, newsfeed, reels, feed_unit, ads, analytics, telemetry |
| **Manifest** | AD_ID / AdServices permissions removed; analytics-named components stripped |

## Build

Requirements: JDK 17+, `apktool`, Python 3, optional `zipalign` / `apksigner`.

```bash
./build.sh path/to/facebook-lite.apk
./build.sh --url "https://trusted.example/facebook-lite.apk"
./build.sh path/to/facebook-lite.apk --clone --install
```

Output: `privacyfblite.apk`

## Honest limitations

- Facebook Lite draws most UI via **remote Bloks**. Disabling local modules and poisoning paths reduces Feed/Reels/tracking; it does not guarantee every server-driven screen disappears.
- After major app updates, re-run analysis and refresh `DISABLE_MODULES` / path lists.
- Do **not** redistribute the patched APK unless you have a legal basis.

## License

GPL-3.0 — see `LICENSE`. Not affiliated with Meta.
