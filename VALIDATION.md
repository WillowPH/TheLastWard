# Chapter 1 validation — v8, 20 October 2026

Build `last-ward-ch1-chapter-review-8`. Checks run in Chromium using Python
Playwright, with service workers blocked. Current reports are in `tests/results`.
Focused scenarios isolate their setup; the earned route test does not grant health,
resources or progression flags.

| Executed check | Scope |
| --- | --- |
| `tools/build_room_views.py` | 54 distinct native views, 54 directed door mappings, 182 authored fixtures across 27 rooms |
| `tests/test_balance_v8.py` | 8 groups: finite difficulty populations/ammo, costly knife and struggle, deliberate aim, all firearm knockdown thresholds, migration and real final pursuit opening |
| `tests/test_puzzles_v8.py` | 9 groups: physical crank, prime/drain stages, generator result, load isolation, uniquely deducible numbered fuse pattern, truthful unlock, service shortcut, late photo, optional shotgun and responsive mouse controls |
| `tests/test_survival_v8.py` | 5 groups: actual earned trauma events and deferred hallucinations, real ammunition/nonlethal imaginary combat, finite episodes and Pause, meaningful hazard costs/recovery on three difficulties, once-only windows |
| `tests/test_visual_solid_peek_v8.py` | 5 groups: rendered actor opacity over contrasting backgrounds, useful dark-room PEEK for three covers, coherent Kessler aftermath and retired target, current-facing visions and live aperture resize |
| `tests/test_clues_rear_v8.py` | 7 groups: real rear shotgun authorization/pickup, ammunition/drive collection, collected clue links, completed records, Story separation, three responsive Files layouts and actual spent-lighter ignition states |
| `tests/test_audio_pass.py` | 9 groups: eleven assets decode/provenance, quiet healthy exploration, paced heartbeat condition/threat cues, reading, Pause/fades, no duplicate loops or repeated hurt sounds |
| `tests/test_caption_v8.py` | Transparent caption fills, native art overlay/fit, readable text and remaining-ammo brackets at desktop/tablet/mobile sizes |
| `tests/test_mouse_refresh_v8.py` | 3 groups: real drags survive repeated scene refreshes; short drags and focus loss replay pending rendering safely |
| `tests/test_checkpoint_v8.py` | Actual finale and glass checkpoint loading for all three compatible legacy build IDs, preserving earned clearance/resources/cleared actors |
| `tests/test_pause_journal.py` | 5 groups: frozen world/audio/deadlines, preserved reader, journal fit, exact nav-button position and actual unobstructed Close control |
| `tests/test_reference_theme.py` | 4 groups: responsive whole-art layout, complete readable captions, mouse turning and document/menu contrast |
| `tests/test_actor_scale.py` | 108 room/identity renders, 18 responsive cases, floor contact, larger Subject X, darkness and real struggle/re-entry |
| `tests/test_exterior_weather.py` | All 54 views; eight exterior views and 71 glass cells, with zero snow outside masks |
| `tests/test_local_lighting.py` | Dark versus locally powered circuits, actual flashlight effect and shutter lighting |
| Retained interaction suites | 17 system groups, 13 revision groups, 7 survival groups, 5 story groups, 7 combat groups, 10 HUD groups, 7 room-view groups and 3 direct inventory groups; zero JavaScript errors |
| Native target checks | 212 actual active target centers, with 54 directed room arrivals; retired or gated objects do not leave active targets |

The earned Normal route visited all 27 rooms and completed Chapter 1 without the
optional shotgun. It defeated nine infected, spent 36 firearm rounds, used four
medical supplies and created three actual Subject X knockdowns/escapes. It ended
with 29.65 HP and 24 reserve rounds. Two visible visions and one imaginary fight
occurred; the latter was resolved by observation. The crank, supply and interlock
gates were earned, and the route read its collected progression clues.

The earned Story route also completed all 27 rooms and those progression gates
without the shotgun. It defeated five infected, spent 20 firearm rounds, used one
medical supply and created three Subject X knockdowns/escapes. It ended at 67.12 HP
with four loaded and 28 carried reserve rounds, plus 24 rounds deliberately stored
through the real Storage box interface. Both visions and the imaginary fight
occurred. These routes were executed separately; the report identifies its source
for the preserved Normal trace rather than claiming a single uninterrupted test.

The full-route and archive reports document final integration outcomes.
The project and update archives are tested by extracting them, comparing
shipped bytes and playing through the local native server with external requests
blocked. The update is also applied over an earlier delivered complete project.

Recognized v5/v6/v7 records migrate to v8. New encounters are not spawned into
visited old-save rooms; cleared enemies and pickups remain cleared. Previously
earned late transfer requirements are preserved. A new run exposes the complete
new encounter and puzzle progression.

Native room paintings fit without enlargement or fake 4K. Heartbeats are original
generated game sound design, not human recordings; no human listening review is
claimed. First-time human puzzle pacing and every Windows/GPU configuration remain
unmeasured. The Windows x64 launcher is included and its PE header checked; the
same server is exercised on Linux. Windows desktop execution is not claimed here.
Package hash reports remain outside their own ZIPs.
