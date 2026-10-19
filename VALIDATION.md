# Chapter 1 correction validation — 19 October 2026

Build `last-ward-ch1-survival-review-5`. Chromium and Python Playwright, service
workers blocked. Reports are in `tests/results`; each listed suite executed.

| Check | Verified result |
| --- | --- |
| `python tools/build_room_views.py` | 27 rooms, 54 unique native views, 54 directed doors, 162 authored fixtures; source dimensions recorded without resizing |
| `python tests/test_revision_regressions.py` | 13 groups: real initial flashlight pickup, no living named nurses/invisible doctor, single-finding panels, desktop/mobile complete readable pages, Files and collected clues, rear pickups, charger availability, damaging hazards and mouse recovery after fatal death |
| `python tests/test_survival_revision.py` | 7 groups: three difficulty balances, reading pause, fatal-command/migration guards, once-only retreat arrivals, finite Subject X recovery, earned nonlethal combat and bounded visible body visions |
| `python tests/test_inventory_revision.py` | 12 groups: direct HUD recipes/refill/reload/upgrade, incompatible/full-capacity rollback, protected/spent discard, death guards, Wire guidance, three shared Storage boxes and responsive controls |
| `python tests/test_inventory_discard.py` | 9 existing protection, confirmation, stale-request, save/load and practical-Thought groups |
| `python tests/test_story_review.py` | 5 groups: physical flashlight, Floppy Disk migration and actual Terminal save, nurse records, simplified clues, purge reward and charger/storage state |
| `python tests/test_winter_systems.py` | 17 groups, all 54 directed arrivals, 128 seeds and 54 native views at three viewport sizes; lighting, sound, persistent objects and story systems |
| `python tests/test_winter_playthrough.py` | Normal and Story earn every gate, visit all 27 rooms, use the right HUD to combine and complete the elevator ending |
| `python tests/test_room_view_review.py` | 7 mouse/presentation checks, including stable art during reading, photographs and saved facing |
| `python tests/test_reference_theme.py` | 4 layout/colour/paper groups at 1672/1000/390 widths |
| `python tests/test_panorama_targets.py` | Compatibility-named native test: 202 available door/object centres receive the expected ordinary mouse hit; unavailable chargers are excluded |
| `python tests/test_exterior_weather.py` | All 54 views, 8 exterior views, 71 glass cells; no snow pixels beyond masks; four independent North Corridor closure states |
| `python tests/test_local_lighting.py` | Actual canvas pixels: local unpowered circuit stays dark after generator repair; powered room spends no flashlight charge; both native shutter overlays obey room lighting |
| Integrated visual audit | Seven new art states and seven rear fixture centres; no old shutter mesh or material request; Kessler and barricade continuity reviewed |
| `node tests/test_launch_guard.js` | Direct-file instructions and local-server launch |
| `go test ./launcher` | Complete-folder checks, audio ranges, local binding and occupied-port fallback |
| `python tests/test_winter_package.py downloads/The_Last_Ward_Chapter_1_Project.zip /tmp/ward-launcher` | Extract and compare all runtime bytes; native local server, all 54 views, font and measured audio with external internet blocked |
| `python tests/test_visual_update.py` | Apply the update to the previously delivered complete project; compare all runtime bytes and launch native mouse views offline |

Fresh earned Normal and Story runs both completed every requirement. Normal ended
at 41.6 HP, Story at 72.0 HP. No progression flags, health or resources were injected
in these full-route runs. Focused scenario tests use isolated setup and do not claim
to represent a full playthrough. Zero JavaScript errors occurred in passing runs.

Source paintings remain native resolution: mostly 1448×1086, with the North Corridor
rear/window state at 1447×1087. No 4K or seamless-360 claim is made. The user chose
sharp room-facing views. First-time human puzzle pacing remains unmeasured.

The Windows x64 executable is included and its PE header is checked. The same Go
server source is exercised on Linux; Windows desktop/browser opening has not been
executed in this environment. Package hashes are recorded outside their own ZIPs
in `tests/results/winter_package.json` and `visual_update.json`.
