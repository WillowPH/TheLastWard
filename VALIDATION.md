# Winter build validation

Validated in system Chromium through Python Playwright, 18 October 2026.
Source tests block service workers so results cannot come from a stale cache.

## Earned progression

`python tests/test_winter_playthrough.py`

Two seeds/difficulties (Normal and Story), exercised against both source and the
packaged standalone with resource requests blocked, each reaching all 27 rooms and the explicit
Chapter 1 elevator ending. Tests click actual scene doors and object action controls;
keys, tools, fuse, weapons, clues and clearance are earned. Test helpers reveal the
camera region containing a target and use seeded puzzle values as an oracle. They do
not grant progression flags. The routes exercise regulator wiring, generator restoration,
patient treatment, Kessler, Rourke, the scientist, portraits, photograph development,
all four interlocks, Subject X introduction/escape and final descent. The required
sprinkler is stopped and its dropped light retrieved through separate actual controls.

Machine-readable results: `tests/results/winter_progression.json`.

## Focused systems

`python tests/test_winter_systems.py`

Isolated state fixtures test sound decoding/playback and nonzero WebAudio output;
battery drain by difficulty, lit-room behavior and exhausted beam removal; confirmed
hoist states; hiding/peeking; stable examination image identity; window confirmation,
three catches, health/sanity exposure and warming; lighter combination/use; one-time
sprinkler recovery; confirmed substantial plank; knife patient choice, covered art and
save/reload; finite actor population, costly knockdown, return and permanent death;
nonlethal imaginary combat with real ammunition; all three phone transcripts; fatal
glass warning/retreat/checkpoint; high-resolution photograph backs; 128 seeded worlds
with authored targets; every pickup icon file and 27 distinct panorama hashes; all-room
front/rear controls and horizontal overflow at 1600×1000, 1000×800 and 390×844.

Machine-readable results: `tests/results/winter_systems.json`.

These scenarios deliberately arrange state to isolate behavior; they are separate from
the earned progression routes. Sound output is measured, not subjectively mixed by a
human listener. Geometry collision review found and corrected chapel candles overlapping
the return door. East Corridor's window/valve and Residence's door were moved to the
actual panorama features. Current authored fixture/door overlap audit has no fixture
covering more than 35% of its area with an unrelated doorway.

## Package

`python tools/package_build.py` creates the source archive, standalone HTML and versioned
cache, plus a separate player ZIP containing the standalone and launch instructions. The final standalone is tested with networking disabled; embedded artwork,
fonts and sound must load without fetching external files. See
`tests/results/winter_package.json` for actual packaged-file checks. The environment’s
Chromium policy blocks direct file:// navigation, so the exact standalone bytes are
served as the only permitted request from a loopback HTTP origin; networking is then
disabled for gameplay. All other resource requests are blocked from the start. Direct file
opening in an unmanaged desktop browser is not certified here.

Historical tests from the preceding build remain in the tree as reference. Some assert
its old artwork paths/renderer selectors and are not represented as passing this
redesign. Use the winter suites above for the active presentation and systems.

## Practical limits

Automated playthroughs prove the tested routes are solvable; they do not replace a
human first-play pacing, difficulty and art review. Nightmare and every possible seed
are not full-run certified. Browser autoplay/output-device settings can still mute
sound until a user gesture. Mobile layouts were checked in Chromium emulation; physical
phone browsers and Firefox/Safari were not run in this environment.

All 30 local recorded clips were also decoded with FFmpeg and checked against their
processed-output SHA-256 values in audio/SOURCES.json. The third-party Caveat license
is retained verbatim, including its original whitespace.
