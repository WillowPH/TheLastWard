# The Last Ward — Chapter 1

A multi-file survival horror game set in Blackridge Medical Complex, 1998.
Chapter 1 ends at the service elevator. The hospital layout stays fixed; room
artwork, object states, targets, documents, audio and logic are separate files.

## Play

Extract the entire `The_Last_Ward_Chapter_1_Project.zip` folder. On Windows 10/11,
double-click **START_GAME.exe** or **START_GAME.bat**. No Python or external internet
connection is needed. Keep the launcher open while playing. On macOS/Linux, run
`python3 start_game.py` with Python 3's standard library.

Click objects and drag sideways to see the other authored room facing. Pause stays
below Options in the left menu, including while reading. No keyboard is required.
Hints default to Subtle; strength, motion, flashes and sound are in Options.

Select an item in the right inventory to use, inspect, combine or discard it.
Choose Combine, then a compatible second item. Normal/Story automatically retire
truly spent tools; Nightmare keeps manual discard. Items needed for unfinished
progress remain protected. Save at a Terminal using a Floppy Disk; Storage boxes
share stored equipment. Saving and the optional shotgun are not mandatory.

## Survival and progression

Normal puts pressure on ammunition and route planning across a finite enemy population.
Noise attracts existing infected; cleared enemies stay cleared. A knife can finish
a weakened enemy, but fighting a fresh one at close range is dangerous. Struggling
creates a temporary opening and costs health. Subject X requires a real tactic;
walking back through a door alone does not clear the final transfer route.

The flashlight is collected from the lobby coat. Battery, exposure and encounter
clocks pause while reading records. Wet clothing needs deliberate drying at the
laundry stove or a powered warm room. Close opened windows and leave cold areas.
Death requires loading a save/checkpoint or restarting.

Collected records support physical puzzles: the service pump, transfer supply,
photographs and final interlock. Files groups unfinished Progression objectives
with their collected clues; Story records and All records preserve the rest.
The game does not fill puzzle answers in for the player. System repairs show clear
results, and the elevator only unlocks when all transfer requirements are met.

The active sound design uses room ambience and restrained condition/threat heartbeat
cues. Reading quiets the pulse; Pause stops all playback. Major horror incidents
remain once-only, with bounded later hallucinations and nonlethal imaginary combat.

## Presentation

There are 54 distinct native room paintings across 27 rooms, mostly 1448×1086.
The user chose these sharp front/rear views over limited-resolution continuous 360
artwork. Complete paintings fit without cropping, stretching or fake 4K enlargement.
Mouse turns use a brief optional fade. Real enemies have opaque bodies and grounded
scale; PEEK shows the live room through physical openings. Snow stays outside glass.

The charcoal HUD follows the supplied reference. Narration and Thoughts sit over
artwork without an opaque backing fill. Useful finds and clues occupy rear furniture.
Optional graphical references and Chapter 2 foreshadowing remain in Chapter 1.

## Continued saves

Use the same browser/local port. Recognized v5/v6/v7 saves can continue in v8,
preserving collected items and cleared enemies. Previously earned late clearance
remains valid. A new run gives the entire revised balance and puzzle sequence.

See [v8 changes](docs/REVISION_V8.md), [verified checks](VALIDATION.md) and
[the prior correction pass](docs/REVISION_V7.md).

## Development

Run `python3 start_game.py --no-browser --port 8010`. Author native targets in
`data/room_views.json`, then regenerate with `python3 tools/build_room_views.py`.
Effects use `data/room_view_effects.json`. The late v8 balance, puzzle, survival and
UI modules load before `pause.js`, which remains last. See
[view setup](docs/ROOM_VIEW_SETUP.md) for native geometry and interaction contracts.
