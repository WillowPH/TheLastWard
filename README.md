# The Last Ward — Chapter 1: Blackridge

A Chapter 1 rebuild based on the supplied Cinematic Project and master requirements.
The playable chapter ends inside the restricted service elevator, after the revelation
and an explicit choice to descend. Chapter 2 exploration is not included.

## Download and play

Download this branch with **Code → Download ZIP**, extract it, and open
`downloads/The_Last_Ward_Chapter_1.html` in a modern browser. The single HTML contains
all room artwork, character cutouts, recorded audio, item art, Roboto, and game code.
No server, installation, image provider, or internet connection is required to play.
Allow audio after pressing Begin Investigation. Start a new game for this build.

For source development, run `python -m http.server 8000` in the repository directory
and open the served `index.html`. The hosted edition caches its required files for
offline return visits. Saves are local to the browser/origin; export a terminal record
before moving to another browser. Older builds' saves are kept under their old keys
and are not silently loaded into this different room topology.

## This build

- 27 unique room backgrounds; no mirrored substitutes or legacy room-image fallback.
- 155 explicitly authored fixtures, separate doors, fixed art coordinates, subtle glints,
  focus/hover labels, stronger hints, and responsive controls.
- Separate object, pickup, lighting, actor, and persistent aftermath layers. The surgical
  aftermath has its own image and matching changed inspection region.
- Subject X and infected are visible in rooms and central encounter views. Pursuit uses
  traversable room edges, with positional heavy boot recordings, cover and locker peeking.
- Clara Whitmore, Evelyn Shaw, Judith Price, Daniel Mercer and Kessler interactions;
  consistent Rourke evidence and the Monolith/LULLABY story.
- Actual maintenance tools plus fuse/regulator repair, matching seeded puzzle clues,
  final clearance, real pursuit escape, and gated elevator completion.
- Inventory, storage, stacking, optional upgrades and crafting, ribbon saves, checkpoint
  recovery, irreversible patient choices, one-time incidents, optional warned fatal
  glass encounter, nonfatal hallucinations, and recoverable environmental conditions.
- 26 local recorded effects/loops. Distinct footsteps, wet steps, mechanical bell foley,
  doors, gunfire, reload handling, breathing, water, machinery and room ambience.
- Exportable Chapter 1 completion record for later Chapter 2 work.

## Interaction corrections

- World props use transparent object artwork; inventory thumbnails stay in UI.
- Inspecting the phone or furniture opens actions without zooming the background.
- Hiding asks first, switches the light off, and blacks out the view. Peek reveals
  only a narrow gap; the flashlight and room travel stay blocked while concealed.
- The return route is marked **Behind you**. **Turn around** shows its closed door;
  forward targets omit that entry. Doorway shading follows the destination circuit.
- Every travel entry point checks physical adjacency before any time/state change.
  Briefly disabled travel buttons prevent a rapid click from crossing a second room.

The room art uses fixed camera compositions; the turn-around view is a separate
closed-door view, not a freely rotating 3D camera.

## Verification and limits

See [VALIDATION.md](VALIDATION.md) for exact automated coverage and commands,
[IMPLEMENTATION.md](IMPLEMENTATION.md) for the implementation map, and
[audio/README.md](audio/README.md) for recording sources and processing.

Three progression runs—two Standard seeds and a Story route visiting all 27 rooms—
have been exercised automatically through the actual inventory, puzzles, gates and
elevator ending. This is not a completed human playtest
or proof of the requested 2–3-hour playtime. Long-session pacing, difficulty balance,
and listening quality still need human evaluation. Automated coverage is Chromium;
other browser engines have not been claimed verified.

Optional online artwork is limited to a noninteractive atmospheric texture above the
room. It cannot replace the background or move targets. No paid/live provider is
configured; the complete offline game is the default reliable path.
