# Chapter 1 panoramic validation — 18 October 2026

Python Playwright with system Chromium and software WebGL. Service workers blocked
for browser checks to prevent stale caches. Reports live in `tests/results/`.

| Command | Evidence |
| --- | --- |
| `python tools/build_panorama_world.py` | 27 unique images, complete reviewed fixture/door targets, valid state masks and physical floor-plan adjacency |
| `node tests/test_snap_camera.js` | Both wrap directions, 350→10 forward 20°, exact stop, no overshoot/idle jitter, equal elapsed-time results at 30/60/144 FPS, long frames, pitch, retarget lock, reduced motion |
| `python tests/test_panorama_targets.py` | 204 available object/door centers receive the expected ordinary mouse hit |
| `python tests/test_panorama_review.py` | 14 focused input, persistence, pixel and responsive presentation checks; no JS errors or failed resources |
| `python tests/test_winter_systems.py` | 17 mechanics checks; all 54 directed arrivals face away from the entrance, 128 seeded placements, all 27 rooms at desktop/tablet/mobile |
| `python tests/test_winter_playthrough.py` | Normal and Story earned routes visit all 27 rooms and reach the explicit four-interlock elevator ending using native POI controls and mouse clicks |
| `python tests/test_winter_package.py` | Extracted ZIP, byte-identical runtime, local launcher, all 27 panoramas, icons/font and measured audio with external internet blocked |

The presentation suite verifies unpowered/powered portraits, photo backs, removal on
completion, single catch prompts, exterior snow pixels, shutter art, stove firebox,
fixed paginated captions preserving all text, the 27-room shared-wall floor plan,
one-click adjacent travel, phone completion and camera pose through save/reload,
actual atmosphere frames/lamp dips respecting Options, 28 obtainable item icons,
0°/360° GPU pixel comparisons in every room and 1672/1000/390px HUD bounds.

The systems suite exercises recorded audio energy, Normal/Story battery drain,
lighting, confirmed hoist states, dark hiding/peek slots, no inspection zoom,
once-only cold/sprinkler incidents, dropped flashlight recovery, lighter/fluid and
warming, plank confirmation, Mercer outcomes, finite noise enemies, knockdown/re-entry,
nonlethal hallucinated combat, payphone progression and fair fatal-encounter warning.

Manual visual review covered all 27 rear views plus shutter, stove, hoist aftermath,
Mercer cover, Kessler aftermath, corrected service hatch, Morgue and Security CRTs.
Three stale corrected exports were found and re-exported before the final archive.
This validates implemented behavior and observed art; it is not a promise of perfect
first-time puzzle pacing, seamless painting at every pole, or identical performance
on every browser/GPU. The game uses painted 2K spherical scenes, not walkable 3D.
