# Changelog

## 0.3.0 — module + menu/surface blocking (FB Lite 539)

- Disable downloadable modules: profilo, heroplayer, mediastreaming, boost, blokscamera, ANR detector
- Keep messaging modules: msys, msysinfra, rtc
- Poison GraphQL client ops: PYMK, StoryById, impression, GenAI consent
- Wipe assets/com/facebook/logginginfra/falco/*
- Expanded path scrub + Block.smali for feed_unit / pymk / heroplayer / mediastreaming
- Manifest AD_ID + analytics component cleanup

## 0.2.0 — strengthened tracking strings from classes.dex

## 0.1.0 — initial pipeline
