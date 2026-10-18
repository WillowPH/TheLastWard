# The Last Ward — Chapter 1

A multi-file browser survival horror game set in Blackridge Medical Complex, 1998.
Chapter 1 ends at the service elevator; Chapter 2 is not playable.

## Play

Download `downloads/The_Last_Ward_Chapter_1_Project.zip` and extract the entire folder.
Windows 10/11: double-click **`START_GAME.exe`** (or `START_GAME.bat`). No Python
installation is needed. Keep the EXE beside the extracted game files.
macOS/Linux: `python3 start_game.py` (Python 3 standard library).
A modern browser with WebGL enabled is required. Do not open `index.html` directly.
Keep the launcher terminal open. No external internet connection is required.
Start a new game: this build has a new save namespace, preserving earlier saves.

Use the lower **Look At** direction buttons, named points or object/door selector.
A/D and arrow keys turn 90°. Clicking an object examines it without moving the camera.
Hints (Subtle/Strong), smooth glides, speed, motion and flashes are in **Options**.
Map travel is adjacent only. Door labels name required keys or clearance.

## This correction pass

- 27 replacement continuous equirectangular room images, each projected on a spherical
  WebGL view. No four-image strip or Turn Around button. These are painted 2048×1024
  panoramas, not walkable modeled 3D rooms or native 4K artwork.
- Shortest-path, frame-independent click-to-snap camera; exact arrival and input lock
  while moving. Ordinary inspection keeps the same canvas and camera pose.
- Hand-authored room targets, real return-door orientation, persistent item removal,
  usable portraits, single window prompts, completed phone/read state and item icons.
- Exterior snow clipped to actual glazing; enclosed corridors have no outdoor weather.
  Real shutter and stove artwork replaces schematic lines. Local CRT feeds and scanlines
  remain within the glass. Interior light flicker respects the flashes option.
- Three-column reference layout, fixed paginated narration/thought cards, architectural
  floor plan with physical shared doors, right-side status and icon inventory.

Gameplay includes finite noise-responsive enemies, Subject X in the later chapter,
confirmed traps, once-only story incidents and cold/sprinkler hazards, lighter/fluid,
handwritten files, generator power/outages and four named elevator interlocks.
See [design notes](docs/DESIGN_NOTES.md) for the retained story requirements.

## Development

Run `python3 start_game.py --no-browser --port 8010`.
Run `python3 tools/build_panorama_world.py` after editing authored room metadata.
See [camera setup](docs/SNAP_CAMERA_SETUP.md), [implementation](IMPLEMENTATION.md),
[art rules](docs/PANORAMA_ART_RULES.md), and [validation](VALIDATION.md).
The delivery preserves separate code, assets, audio, fonts, data and documentation.
