# Phase 1: room art and object layers

This pass converts Emergency Lobby, Security Office, East Corridor, Patient Wing,
and Room 12. Other rooms retain the previous renderer and artwork pending Phase 2.

## Implemented

- Five newly generated, independently composed local PNG backgrounds. No interaction
  text, cursor, hover label, button or mask is baked into these backgrounds.
- Explicit room/fixture/door rectangles in `js/room_layers.js`, authored against the
  final artwork. Related contents share their physical fixture. Seeded phones and
  supply caches have explicit locations; caches have their own rendered crate layer.
- The uncropped 4:3 art plane and targets resize together. The narration area is
  reserved so it cannot intercept targets on small screens.
- Important fixtures shimmer gently. Hover/focus adds a faint highlight and object
  name, inspect/travel cursors differ, and a persistent Hints toggle shows stronger
  target outlines. Reduced-motion preferences disable animation.
- Background, off-screen passage controls, item overlays, saved object-state cues,
  targets, lighting, and UI remain separate layers. Inventory pickups disappear
  from the object layer, inspected drawers show an opened cue, completed fixtures
  show a small game-rendered check. Existing object/inspection flags survive saves.
- Optional runtime AI cannot replace pilot art and invalidate the authored geometry.
- Service-worker cache revision includes the new art and scripts.

The lobby's two later unlocked return connections are explicitly off-screen side
passages, rendered as navigation above the art when their progression gates open.
They do not introduce door targets over the windows, floor or ceiling.
The original JPG assets remain for compatibility/reference; the pilot renderer uses
only the new PNGs.

## Run and validate

From this project directory: `python -m http.server 8000` and open the site in a
browser. The offline edition is produced by
`python tools/package_build.py /absolute/output/directory`.

Regression command: `python tests/room_layers_smoke.py`. Requires Python Playwright
and system Chromium at `/usr/bin/chromium`. The game itself has no package install,
backend, API-key or build dependency.

Verified in Chromium: 20 browser checks covering 40 seeded worlds, every pilot
fixture and connection, no intersecting target rectangles, all target centers
reachable at desktop/tablet/mobile sizes, loaded local backgrounds, inspection,
collection, hint toggle, real save/load persistence, and travel. Screenshots in
`tests/*-pilot.png` show the desktop result.

Not claimed: a full Chapter 1 playthrough, validation in other browser engines,
or conversion of the remaining rooms. Phase 2 must author each remaining room's
art and fixture map; do not copy, mirror or auto-place pilot targets there.
