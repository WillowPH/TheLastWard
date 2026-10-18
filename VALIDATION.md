# Native room-view validation — 18 October 2026

Chromium and Python Playwright with service workers blocked. The active renderer uses
2D canvas and native room views; it does not depend on WebGL. Reports are in tests/results.

| Check | Result |
| --- | --- |
| `python tools/build_room_views.py` | 54 unique native 1448×1086 paintings, 27 rooms, 54 directed doors, 162 fixture definitions |
| `python tests/test_room_view_review.py` | 7 focused checks: no toolbar/keyboard dependency, whole-image fit, drag versus click, portraits/backs/completion, stable inspection, saved facing and Options-only hints |
| `python tests/test_reference_theme.py` | 4 groups: neutral HUD, native mouse turns, readable typed/handwritten paper, full art and Thoughts at 1672/1000/390 widths |
| `python tests/test_inventory_discard.py` | 9 groups: safe/spent inventory policy, shared-key/tool guards, confirmation, stale-request protection, capacity, actual save/reload and practical Thoughts |
| `python tests/test_exterior_weather.py` | All 54 views; 8 confirmed exterior views and 71 glass cells; zero weather pixels outside protected glass; four independent window states |
| `python tests/test_panorama_targets.py` | Compatibility-named native test: 206–207 actionable target centers (seeded phone placement varies) receive the expected mouse hit, including active catches |
| `python tests/test_winter_systems.py` | 17 groups including all 54 directed entrances, 128 seeds and pixel-level lighting/object-state checks |
| `python tests/test_winter_playthrough.py` | Normal and Story routes visit all 27 rooms, earn progression and reach the four-interlock elevator ending through ordinary mouse controls |
| `python tests/test_winter_package.py <zip> /tmp/ward-launcher` | Required delivery check: extract, compare every runtime file/asset hash, native local server, all 54 views and measured audio with external internet blocked |

The mechanics checks cover actual audio, Normal/Story battery drain, illuminated rooms
unchanged by the flashlight, battery exhaustion, confirmed hoist states, hiding/peek gaps,
no inspection zoom, once-only cold/sprinkler incidents, dropped flashlight, lighter/fluid,
plank confirmation, covered Mercer, finite enemies, imaginary combat, phones and fair
fatal warnings. All directed arrivals face away from the entry and can return correctly.

The earned routes collect the Archives fuse before later Subject X occupation; the
pursuit/escape still occurs and is required. Enemies can physically obstruct objects.
Normal ended at 70 HP and Story at 92 HP; both completed every progression requirement.

Manual review covered all 54 source views and actual integrated shutters, CRTs, stove,
window states and the reference HUD. Native paintings remain 1448×1086; no native4K claim
is made. First-time puzzle pacing and every Windows/GPU configuration are not guaranteed.
The Windows x64 executable is built and its PE headers checked; its standard-library
server is tested from the same source on Linux. Windows desktop browser opening has
not been executed in this Linux environment. `go test ./launcher` covers complete-folder
validation, audio ranges, local binding and occupied-port fallback.
