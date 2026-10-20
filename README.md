# The Last Ward — Chapter 1

A multi-file survival horror game set in Blackridge Medical Complex, 1998.
Chapter 1 ends at the service elevator; Chapter 2 is not playable.

## Play

Extract the entire `The_Last_Ward_Chapter_1_Project.zip` folder.
Windows 10/11: double-click **START_GAME.exe** or **START_GAME.bat**. No Python
installation or external internet connection is needed. Keep the launcher window open.
macOS/Linux: `python3 start_game.py` (Python 3 standard library only).
Use the same local port/browser for saved games. Existing v5 and v6 saves can continue in
this v7 update; a new game also works. Older incompatible builds remain separate.

**Click objects to examine them. Drag sideways to see the
other side of the room. No keyboard is needed.** Hints (Subtle/Strong), motion and
flashes are in Options. The right-side flashlight button shows its battery percentage.
Select an item in the right inventory to use, inspect or discard it. Select Combine,
then a second item to craft, refill the lighter or load a compatible weapon. Discard
requires confirmation; items needed for unfinished progression remain protected.

## Visual correction

The user chose sharper room-facing artwork over the limited-resolution 360° format.
The active renderer uses **54 distinct native room paintings** across 27 rooms,
mostly 1448×1086 (the North Corridor rear and Mercer view are 1447×1087).
Each complete painting fits inside the scene without cropping, stretching or digital
zoom. Mouse turns use a brief fade between authored views; no images are joined into
a pretend continuous panorama. This is game artwork, not native 4K or walkable 3D.

- Neutral charcoal HUD, warm grey text, brass rules and amber Thoughts follow the
  supplied three-column reference. Green is reserved for physical health feedback.
- No bottom navigation/hint strip or required keyboard controls. Ordinary inspection
  preserves the same image and scale. There are no view-arrow buttons.
- Corrected lobby furniture barricade, integrated laundry stove and actual 1998 CRT.
  Shutters fit real glass, with local snow beyond windows and scanlines inside screens.
- Practical light, power, key and supply requirements appear in Thoughts. Story and
  puzzle dialogs retain their own presentation. Documents use readable pages; Files
  group collected evidence by subject and unfinished leads. Locks can reopen related
  collected records without filling in the answer. Thoughts stay concise.

## Gameplay correction — 19 October

The flashlight is collected from the lobby coat. It runs only where local lighting
requires it; reading records pauses battery and exposure. Death is terminal until
loading or restarting. Sprinklers injure, cold causes exposure damage, and wet clothes
need deliberate recovery at a powered warm shelter or lit laundry stove.

Judith and Evelyn Shaw appear through records rather than living nurse sprites.
Kessler has a visible full-body encounter and persistent aftermath. Rear views now
hold useful supplies, including the Archives elevator fuse. Native shutter artwork
and the rear barricade match the lobby; snow remains outside the reviewed glass.

Existing finite ammunition caches provide more rounds. Subject X evasion gives a
limited recovery interval. Earned sanity episodes are bounded, persistent across
saves and nonlethal in imaginary combat. The optional one-time window purge releases
supplies after all three catches are closed. Save at a **Terminal** using a **Floppy
Disk**; additional **Storage boxes** share equipment along the route.

## Gameplay and audio follow-up

Pause from the left navigation, including while a dialog is open. Resume preserves the record,
world time, battery, exposure and encounter deadlines. Normal, caution and danger
use distinct quiet air-breath loops; longer machine/wind beds and an original pickup
cue replace the repeated hurt and bottle sounds.

Inventory actions stay beside the grid, with quantity badges and direct pairing.
Story/Normal remove truly spent keys/tools automatically; Nightmare keeps manual
discard. Supplies are spread across rear furniture, including Security's early tools.

Subject X blocks casual exits. Two handgun rounds or a heavier shot create a short
knockdown opening; it recovers. Finite ammunition is balanced for this use. Infected
have distinct opaque appearances. PEEK shows the live room through physical gaps.
Door openings use hinged animations, slow with wet/cold hands and respect Pause.

Security CRTs show local monochrome room feeds, ECG colour follows condition, and
the map arrow follows the current facing. Closed shutters remove snowy reflections.
Sister Mimi's early notes portray someone helpful; experimentation and instability
are revealed later. Chapter 2 encounters remain deferred.

The latest pass removes view-arrow and dialog Pause buttons, keeps Pause below
Options, removes the cold-status colour wash and extra caption panels, and runs
all six surveillance feeds on their own backup supply. Mercer has local breathing
motion; enemy scale and floor placement follow each room. Rear furniture carries
more useful finds. Four optional graphic references and longer varied breath beds
are included. See the correction notes for their exact scope.

See [the v7 correction notes](docs/REVISION_V7.md), [v6 notes](docs/REVISION_V6.md) and [the prior pass](docs/REVISION_2026-10-19.md).

Finite noise-responsive enemies, later Subject X pursuit, confirmed traps, once-only
story/cold/sprinkler incidents, handwritten records, generator outages, lighter/fluid,
shared access keys and four elevator interlocks remain in Chapter 1.

## Development

Run `python3 start_game.py --no-browser --port 8010`.
Author native targets in `data/room_views.json`, then run
`python3 tools/build_room_views.py`. Effects use `data/room_view_effects.json`.
See [view setup](docs/ROOM_VIEW_SETUP.md), [implementation](IMPLEMENTATION.md),
[design notes](docs/DESIGN_NOTES.md) and [verified checks](VALIDATION.md).
