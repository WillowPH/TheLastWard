# The Last Ward — Chapter 1

A multi-file survival horror game set in Blackridge Medical Complex, 1998.
Chapter 1 ends at the service elevator; Chapter 2 is not playable.

## Play

Extract the entire `The_Last_Ward_Chapter_1_Project.zip` folder.
Windows 10/11: double-click **START_GAME.exe** or **START_GAME.bat**. No Python
installation or external internet connection is needed. Keep the launcher window open.
macOS/Linux: `python3 start_game.py` (Python 3 standard library only).
Use the same local port/browser for saved games. Start a new game for this build;
older builds' saves are preserved in their own namespaces.

**Click objects to examine them. Drag sideways or click a side arrow to see the
other side of the room. No keyboard is needed.** Hints (Subtle/Strong), motion and
flashes are in Options. The right-side flashlight button shows its battery percentage.
Inventory → Manage → Inspect exposes confirmed Discard for supplies, keepsakes and
spent keys/tools. Items needed for unfinished progression remain protected.

## Visual correction

The user chose sharper room-facing artwork over the limited-resolution 360° format.
The active renderer uses **54 distinct 1448×1086 native room paintings** across 27 rooms.
Each complete painting fits inside the scene without cropping, stretching or digital
zoom. Mouse turns use a brief fade between authored views; no images are joined into
a pretend continuous panorama. This is game artwork, not native 4K or walkable 3D.

- Neutral charcoal HUD, warm grey text, brass rules and amber Thoughts follow the
  supplied three-column reference. Green is reserved for physical health feedback.
- No bottom navigation/hint strip or required keyboard controls. Ordinary inspection
  preserves the same image and scale. Side arrows sit outside the artwork and targets.
- Corrected lobby furniture barricade, integrated laundry stove and actual 1998 CRT.
  Shutters fit real glass, with local snow beyond windows and scanlines inside screens.
- Practical light, power, key and supply requirements appear in Thoughts. Story and
  puzzle dialogs retain their own presentation. Long narration uses pages, not scrollbars.

Finite noise-responsive enemies, later Subject X pursuit, confirmed traps, once-only
story/cold/sprinkler incidents, handwritten records, generator outages, lighter/fluid,
shared access keys and four elevator interlocks remain in Chapter 1.

## Development

Run `python3 start_game.py --no-browser --port 8010`.
Author native targets in `data/room_views.json`, then run
`python3 tools/build_room_views.py`. Effects use `data/room_view_effects.json`.
See [view setup](docs/ROOM_VIEW_SETUP.md), [implementation](IMPLEMENTATION.md),
[design notes](docs/DESIGN_NOTES.md) and [verified checks](VALIDATION.md).
