# PrivacyFBLite

Privacy patch toolkit for **Facebook Lite** (`com.facebook.lite`) with:

- **Runtime network blocking** (hook on `LX/03z.AE6` → `HttpURLConnection`)
- **In-app Settings** (second launcher icon: *PrivacyFBLite Settings*)
- **Apply & Restart** from settings
- Module disable (Profilo, heroplayer, mediastreaming, boost, …)
- GraphQL op poisoning (PYMK, impressions, …)
- logginginfra/falco wipe

## Build

```bash
# needs Java 17+, Python 3; apktool.jar is under tools/
./build.sh /path/to/facebook-lite.apk
# or
./build.sh --url "https://…/facebook-lite.apk"
```

Optional: `--clone` · `--install`

Output: `privacyfblite.apk`

## Open settings

After install you get **two icons**:

1. Facebook Lite (main app)
2. **PrivacyFBLite Settings** — toggles:

| Toggle | Default |
|--------|---------|
| Block telemetry / analytics | ON |
| Block ads | ON |
| Block News Feed ranking paths | ON |
| Block Reels / short video paths | ON |
| Block PYMK / suggestions | ON |

Tap **Apply & Restart App**.

## How blocking works

1. `ClientApplicationSplittedShell.onCreate` → `PrivacyInit.init` → loads `SharedPreferences`
2. Every `HttpURLConnection` via `LX/03z.AE6` calls `Block.shouldBlock(url)`
3. If the matching toggle is ON and the URL matches, an `IOException` is thrown (request fails)

## Limitations

- Secondary superpack dex is not fully rewritten; some code paths may bypass `LX/03z`
- Server-driven Bloks UI can still show empty shells
- Re-verify hooks after major Lite version bumps

## License

GPL-3.0. Not affiliated with Meta.
