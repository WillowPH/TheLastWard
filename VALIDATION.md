# Validation

Run from this project directory with Python Playwright, Pillow, system Chromium,
FFmpeg and Tesseract installed:

```
python -m http.server 8010
python tests/audit_scenes.py
python tests/test_chapter1.py
python tests/test_regressions.py
python tests/test_scene_corrections.py
python tests/test_visual_review.py
python tests/test_five_room_input.py
python tests/test_refinements.py
python tests/test_inspection_actions.py
python tests/test_state_layers.py
python tests/test_portal_weather.py
python tests/test_art.py
python tools/package_build.py
python tests/test_delivery.py
```

- The geometry audit checks every authored fixture and door for bounds and overlap.
- Two complete Standard seeded routes use actual player actions: opening, phone, keys, map,
  handgun, patient treatment, inventory upgrade, seeded pharmacy code, maintenance
  tools, failed premature generator attempt, regulator repair, fuse installation,
  powered photograph puzzle, Rourke/observation evidence, authorization, theatre,
  shotgun, physical pursuit escape, revelation and elevator completion. Milestone
  flags are not granted by these route tests. A third Story route visits all 27 rooms,
  including optional combat, resident breaker, carrying harness, drainage/winch,
  chapel, specimen, cold store, and isolation branches.
- Regression tests cover 128 seeds for authored-object coverage; all 27 rooms at
  1600×1000, 1000×800 and 390×844; visible controls and hit-tested target centers;
  full-inventory recovery; exhausted-battery recovery and dark inspection; save/load
  and irreversible choices; warned fatal cell and recovery; nonfatal hallucinations;
  separate sprinkler recovery/valve actions, cold and shivering recovery;
  actual pursuer edges/retreat/visibility; locker peeking and waiting; visible infected;
  decoding all 26 bundled recordings.
- Reported-issue regressions reject 1,944 nonadjacent attempts across door, map and
  core travel without state/time changes; verify hide/cancel/confirm, black cover,
  limited peeking, disabled concealed light, unchanged phone scale, full review-room reverse views,
  absence of door masks, and loaded physical object images across all 27 rooms.
- Art audit compares perceptual signatures, including mirrored comparisons, and OCR
  checks for accidental INSPECT/EXAMINE/CLICK HERE/BUTTON prompts. This supports,
  but does not replace, visual inspection of each scene.
- Packaging checks exercise the single-file edition with network disabled after its
  sole document load, and verify hosted offline cache/reload and ZIP integrity.

Current-run results are in tests/results/*.json. Screenshots are supporting evidence,
not a substitute for complete interaction checks. Direct file:// launch is restricted
by the managed test browser; single-file behavior is tested as a single served resource
with all further network access disabled. Other browsers and a human 2–3-hour session
are not claimed tested. Optional live image-provider generation is not configured.

The visual-review suite exercises desktop/mobile anchored panels and Take/Leave,
recorded Clara message without an actor, five review reverse assets, negative removal, file-hotspot cleanup,
patient prerequisites/aftermath, three cover frames, and large-map controls.
These checks verify behavior and supporting layouts; artistic acceptance and
remaining collectible-art conversion are still review work.

## Actual-pointer acceptance checks

`test_five_room_input.py` clicks artwork coordinates rather than invoking travel or
actor actions directly: 12 physical doorway positions, Clara’s recorded message at the monitor bank,
and five reverse views at desktop/mobile sizes. Isolated tests prepare room/lock
states for this input matrix; these do not replace the separate real-progression runs.
It also verifies one cabinet inspection, a multi-item panel remaining open, all ten
focus-room collectible layers, Room 12 save/load, and different drawn canvas pixels
in every focus room with working motion controls. See tests/results/five_room_input.json.

A recorded browser preview is in docs/review/animated-scene.mp4. It shows the actual
layered renderer, not a separately rendered promotional animation.

## Fixed portals and exterior-only rain

The graph has 27 edges / 54 directed transitions. The portal-weather suite clicks
each edge and its return at 1600×1000 and 390×844, requiring the used entrance
to be in the opposite camera view after arrival. It verifies every visible view's
image loads, fixed portal identity, camera migration and retained turned-save view.
All 40 nearby pursuit routes between non-safe rooms also verify that turning
reverses the sound bearing. Safe rooms remain excluded from pursuit. Both lobby views are tested for moving weather pixels, with zero pixels outside
the authored glazing polygons (one pixel antialias tolerance); the other 26 rooms
have no rain canvas in either view. Reduced motion removes both animation canvases.
The same suite runs with networking disabled against the packaged HTML.
Results: `portal_weather.json` and `portal_weather_packaged.json`.

All 27 front and 27 reverse images, plus six state images, were visually inspected
for doorway placement and persistence. Rear target rectangles were fitted to those
images individually. OCR and duplicate checks support this review; they are not
proof of perfect artistic continuity.

## Eight interaction refinement passes

Run `python tests/test_refinements.py` against source, or supply the packaged HTML
URL to repeat the same checks after disabling network access. The eight passes are:

1. Eight focus-panel open/close cycles at three viewports, with fixed bounds and image identity.
2. Trap cancel, advance setup, armed save/load, real-room capture and manual empty release.
3. Every gated edge explains its requirement; legacy key names migrate in inventory/storage.
4. Actual rendered brightness in all 27 rooms, both views and both power states: torch-on cannot darken the image.
5. Clara’s monitor recording and evidence; no floating actor.
6. Every pending fixture has a marker; all active item icons load.
7. Struggle injury, surviving infected on return, and saved remaining enemy health.
8. Knife collection, patient cancellation/confirmation, covered aftermath and saved choice.

Results are `refinements.json` and `refinements_packaged.json`. These are focused
automated browser passes, not eight complete human playthroughs. Three separate
full progression routes still exercise the elevator ending and optional rooms.
