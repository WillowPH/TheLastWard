# Chapter 1 validation — v6, 19 October 2026

Build `last-ward-ch1-chapter-review-6`. Browser checks use Chromium and Python
Playwright with service workers blocked. Passing reports live in `tests/results`.

| Executed check | Result |
| --- | --- |
| `python tools/build_room_views.py` | 54 unique native views, 27 rooms, 54 directed doors and 169 authored fixtures |
| `python tests/test_audio_pass.py` | 6 groups: eight original OGG files decode without clipping, measured output, distinct HP breathing tiers, no duplicate loops, frozen/resumed playheads, original pickup and once-only impact |
| `python tests/test_combat_pass.py` | 7 groups: all travel bypasses blocked, earned firearm stagger/recovery, finite ammunition, three opaque enemy identities and paused boundaries |
| `python tests/test_inventory_pass.py` | Actual use/combine/quantity/auto-discard and popover-hit tests at 1672, 1000 and 390 widths |
| `python tests/test_hud_view_pass.py` | 8 groups: health colours, Save/Options, map bearing, live PEEK, emissive CRTs, wet/cold hinged doors, pickup overlay cleanup and rapid-click/Pause travel locking |
| `python tests/test_scene_story_pass.py` | 6 groups including 64 seeded distributions, real rear mouse pickups, scattered records, gradual Sister Mimi evidence, infected/covered Mercer states and closed-shutter reflection pixels |
| `python tests/test_pause_journal.py` | 5 groups: real mouse Pause freezes game/audio, exact record survives, deadlines preserve time, camera fade defers, journal fits desktop/laptop and remains readable on mobile |
| `python tests/test_revision_regressions.py` | 13 groups: initial flashlight, nurse evidence, individual findings, readable complete paper pages, collected clues, rear pickups, damaging hazards and terminal death/checkpoint mouse recovery |
| `python tests/test_survival_revision.py` | 7 groups including three difficulties, fatal save migration, finite exposure/enemies, retreat arrival costs and bounded hallucinations |
| `python tests/test_inventory_discard.py` | 9 manual Nightmare groups; actual Terminal save/reload also verifies a v5 record migrates to v6 without restoring discarded items |
| `python tests/test_story_review.py` | Early physical flashlight, naming/save migration, nurse records, simplified clues, purge reward, chargers and shared Storage boxes |
| `python tests/test_winter_systems.py` | 17 groups, all 54 directed arrivals with authored East Corridor facing, 128 seeds, sound/light, persistent state and 54 views at three sizes |
| `python tests/test_winter_playthrough.py` | Earned Normal and Story routes visit all 27 rooms and complete the elevator, shooting Subject X with collected ammunition |
| `python tests/test_room_view_review.py` | 7 native mouse/view/inspection/photo/save-facing/hint checks |
| `python tests/test_reference_theme.py` | 4 layout, charcoal surface and paper contrast groups at desktop/tablet/mobile sizes |
| `python tests/test_panorama_targets.py` | Compatibility-named native test: 210 live door/object centres receive their expected mouse hit |
| `python tests/test_exterior_weather.py` | All 54 views, eight exterior views, 71 strict glass cells, no snow beyond masks and independent window states |
| `python tests/test_local_lighting.py` | Actual local power/beam pixels and native shutter state lighting |
| `python tests/test_winter_package.py downloads/The_Last_Ward_Chapter_1_Project.zip /tmp/ward-launcher` | Extract, compare every runtime byte, launch native local server, load all views/font and measure audio with external internet blocked |
| `python tests/test_visual_update.py` | Apply the patch to the earlier complete delivery, compare every runtime byte and launch it offline |

The final Normal run ended at 32.59 HP with seven handgun rounds remaining and
three successful Subject X staggers. Story ended at 67.92 HP with twelve rounds
remaining and two staggers. Both earned every gate and the elevator ending; no
health, supplies or progress flags were injected in these full-route runs. Focused
scenario tests isolate setup and do not claim to be a complete playthrough.

v5 saves use the same browser-storage namespace and are explicitly accepted and
stamped as v6 on load. Older incompatible build formats remain separate. New games
continue to work. Pause is not serialized into a save as an active state.

The renderer fits complete native paintings without enlargement or fake 4K. Most
are 1448×1086; North Corridor rear and Mercer use native 1447×1087 variants. The
new infected orderly is a separate native 1024×1536 transparent game-art asset.

First-time human puzzle pacing and every Windows desktop/GPU configuration remain
unmeasured. The Windows x64 launcher is included and its PE header checked; the same
standard-library server is exercised on Linux. Windows desktop opening has not been
executed here. Package hashes are recorded outside their own ZIPs in
`tests/results/winter_package.json` and `visual_update.json`.
