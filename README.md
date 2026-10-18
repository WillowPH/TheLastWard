# The Last Ward — Chapter 1: Winter at Blackridge

A playable browser survival horror chapter set in Blackridge Medical Complex, 1998.
This build follows the consolidated design notes in [docs/DESIGN_NOTES.md](docs/DESIGN_NOTES.md).
Chapter 1 ends with the service elevator descending toward Chapter 2. Chapter 2 is not playable yet.

## Download and play

For the player package, extract `The_Last_Ward_Chapter_1_Play.zip` and open the HTML
inside. Alternatively, download this branch using **Code → Download ZIP**, extract it, then open
`downloads/The_Last_Ward_Chapter_1.html` in Chrome, Edge or Firefox. Start a **new game**.
The single HTML contains the artwork, fonts, sound and game code. No installation,
server, image provider or internet connection is required. Press Begin Investigation
to permit sound; check the sound controls in Options if your browser blocks it.

Saves belong to the browser and origin where you play. The winter build uses its own
save namespace and preserves older builds' saves. Export a terminal record before
changing browser or moving the game. Modern desktop browsers are the primary target;
mobile uses a compact layout with horizontal scene looking.

## What changed

- Fixed hospital layout, 27 distinct wide front panoramas and separate reverse views.
  Drag horizontally, use the lower look controls, or turn around. Doors and objects
  move with their room artwork; arriving faces away from the entrance used.
- Explicit object targets, stronger optional hints, contextual examination panels,
  Take/Leave, container interiors, persistent pickups and non-repeating completed reads.
- Inspectable photographs with reverse clues, a high-resolution mug, aged paper records
  and handwritten notes with optional readable transcription. Documents remain in Files.
- Snow outside authored window panes, localized flickering, generator/emergency lighting,
  rare recoverable outages and CRT surveillance using monochrome game-room images.
- Finite flashlight charge and visible percentage. Normal drains faster than Story;
  found cells recharge it. The flashlight never darkens an already lit room.
- One-use window purge hazard, individually closable windows, sprinkler shutoff,
  dropped-flashlight recovery, wet footsteps and local cold recovery. Combine the
  lighter with fluid; use it at the drying stove or chapel candles.
- Seeded items in approved containers, matching puzzle clues, named keys, wiring and
  radio tuning, four distinct chess-shaped elevator interlock plugs and an early clue.
- Finite persistent infected actors, animated walking sprites, costly struggles,
  permanent kills, noise-directed movement and a screaming nurse. Subject X is larger,
  introduced after the midpoint requirements, and follows connected routes.
- Confirmed traps and plank placement; dark hiding and slit/gap peeking. Clara is a
  security recording. Mercer, Kessler and the scientist retain one-time consequences.
- Real playable hallucinated combat uses ammunition but cannot damage real health.
  Other limited episodes alter bodies/CRT messages; recovery prevents constant effects.
- Three once-only payphone calls, Rourke/LULLABY evidence, redacted Mimi foreshadowing,
  optional horror-game/television references and a warned fatal glass encounter.
- Local recorded effects, spatial Subject X boots, footsteps, doors, gunfire,
  breathing, machinery, winter wind, radio static and infected vocalizations.

Animation uses layered effects, sprite frames and transitions over prerendered scenes;
it is not a freely navigable 3D hospital. Some requested more graphic regular-infected
art generations were rejected by the image service; this build uses approved torn,
stained clothing designs. No photographs of real gore are used.

## Develop and verify

Serve this directory with `python -m http.server 8010` and open `http://localhost:8010`.
There are no npm dependencies or required backend services. During browser development,
block/unregister the service worker to avoid testing an old cached build.

```
python tests/test_winter_systems.py
python tests/test_winter_playthrough.py
python tools/package_build.py
```

Tests use Python Playwright and `/usr/bin/chromium`; packaging uses Python's standard
library. See [IMPLEMENTATION.md](IMPLEMENTATION.md) for source ownership and
[VALIDATION.md](VALIDATION.md) for evidence and limits. Optional online artwork is not
needed; approved local room art is authoritative for the hotspot geometry.
