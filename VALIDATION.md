# Chapter 1 validation — v9, 21 October 2026

Build `last-ward-ch1-chapter-review-9`. Browser checks use Chromium and Python
Playwright with service workers blocked. Reports are in `tests/results`.
Focused scenarios isolate setup. The two earned routes do not grant health,
ammunition or progression flags.

| Executed check | Scope |
| --- | --- |
| Native compiler | 54 distinct native views, 54 directed door mappings, 186 authored fixtures across 27 rooms |
| `test_actor_poses_v9.py` | 4 groups: separate standing/kneeling/recovery sources, grounded proportions, actual shot-triggered knockdown, Pause, responsive sizes |
| `test_actor_scale.py` | 5 groups: room/identity sizing, responsive floor contact, Subject X proportions, struggle/re-entry |
| `test_patient_outcomes_v9.py` | 9 groups: actual bedside choices and return-door transitions, saved chronology, irreversible mercy, four distinct loaded paintings, identical frame geometry, bounded injury on three difficulties, no repeated enemy |
| `test_doctor_motion_v9.py` | 3 groups: local infected head/shoulder movement, saved response intensity, Pause, Motion Off and incomplete-event suppression; rerun after final facial-art refinement |
| `test_supplies_v9.py` | 8 groups: 384 seed/difficulty budgets, idempotent configuration, actual cells, reliable disk pickup/save/cancel, one charging reserve, early/later healing, rear records, continued saves and full-pack pickup atomicity |
| `test_inventory_v9.py` | 8 groups: all-item local discard/recovery, unused progression equipment, loaded rounds and flashlight state, save/reload, two real ignitions, legacy fuel, Pause and death guards |
| Retained inventory suites | 9 discard groups, 3 responsive direct inventory groups, 12 revision groups; no protected-item prohibition or permanent-deletion assumptions retained |
| `test_weather_v9.py` | 10 groups, 24 fitted exterior view cases: visible real snowfall, motion restart, Pause, shutter panes, moon-free exterior plates, fire/spray/CRT/light changes |
| `test_exterior_weather.py` | All 54 views; 75 reviewed glass cells across eight exterior views; zero snow pixels outside masks |
| `test_online_art_v9.py` | 6 groups: real default/preference controls, truthful native fallback, mocked host image decode and clipping, request reuse, Offline cancellation, stale-room and delayed capability responses, safe service failure |
| `server/test_ward_art_server.py` | 4 stdlib tests using temporary roots and a localhost mock gateway: capabilities, concurrent one-call caching, atomic complete file publication, safe failure/cleanup |
| `test_reading_clock_v9.py` | 4 groups: actual reading preserves pursuit/vision/blackout clocks, overlapping Pause without double-counting, false-combat deadline, new-run checkpoint lifecycle |
| `test_checkpoint_v8.py` | 10 actual loader cases: v5–v7 plus Terminal-serialized v8 earned and unfinished records through both checkpoint loaders |
| Retained survival/presentation | 6 survival-v8 groups, 7 survival-revision groups, 5 opaque/PEEK groups, 5 effects groups; preserve current-facing actual render, 15-second expiry/fade, Pause/cooldowns, and high-sanity/no-trauma suppression |

Six retained suites also pass 59 checks: Winter systems 17 (54 arrivals, 128 seeds and responsive real drags), revision 13, combat 7, HUD 11, room-view 7 and reference theme 4. All report zero JavaScript errors.

The earned Normal and Story routes each visited all 27 rooms and completed the
winch, transfer supply, interlock and pursuit requirements without the shotgun.
Normal finished at 12.975 HP after 40 firearm rounds, five medical uses and four
Subject X knockdowns. Story finished at 59.0384 HP after 22 rounds, one medical use
and three knockdowns. Both retained stabilized Mercer and Kessler's spoken outcome.
The report preserves each actual run's provenance and intermediate checkpoints.
Hallucination eligibility is tested directly; composure recovery need not force
all episodes on every route. Story used real Storage controls for surplus supplies.

The full project and update are checked after extraction: shipped bytes, native
server launch, local audio/font and all 54 room views, with external requests
blocked. The update is applied over an earlier delivered complete project. Final
package hashes remain outside their own ZIPs.

Recognized v5–v8 saves remain loadable. Pickup/charger state and earned progress are
preserved; a new run gives the full revised distribution and choice consequences.

No live paid artwork provider is configured. Hosted artwork behavior is verified
with explicit local mocks; the native download honestly uses bundled art. Original
generated heartbeats are game sound design, not human recordings. Human listening
review, first-time human puzzle pacing and every Windows/GPU configuration remain
unmeasured. The Windows x64 launcher is included and its PE header checked; the
same server is exercised on Linux. Windows desktop execution is not claimed here.
