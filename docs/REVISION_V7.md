# Chapter 1 correction pass — v7, 20 October 2026

Build: `last-ward-ch1-chapter-review-7`. The project retains separate source,
artwork and audio files. Existing v5 and v6 saves remain compatible in the same
browser and local port.

## Water, surveillance and character presentation

- The cold-status effect no longer casts a blue-green wash across the scene and
  HUD after the East Corridor sprinkler valve closes. A neutral, faint frost edge
  stays local to the room image; wet/cold damage and deliberate recovery remain.
- All six Security CRTs show distinct monochrome images of actual game rooms.
  Their separate surveillance battery bank keeps them active before generator
  power and during outages. Screen effects remain inside the painted CRT faces;
  camera images follow room-state artwork, including closed lobby shutters.
- The brief hanging figure is an earned sanity vision, with its existing bounded
  occurrence count. It is suppressed during active sprinklers and retains its
  elapsed fade when the scene redraws.
- Daniel Mercer has a restrained chest/gown breathing animation and a bedside ECG.
  The room, bed and interaction target stay still. Breathing stops on Pause,
  reduced motion or his death; the covered-body aftermath remains persistent.
- Enemies use native source proportions and visible-body scale rather than the
  transparent file rectangle. Per-room floor anchors keep their feet on usable
  floor; Subject X remains larger and broader than ordinary infected. Actor input
  areas follow their silhouettes rather than a large transparent rectangle.

## Mouse controls and reference HUD

- Horizontal mouse dragging turns between the sharp authored room facings. The
  left/right arrow buttons are removed. Clicking an item still preserves facing.
- Pause remains below Options in the left navigation. Findings, examinations,
  records and inventory dialogs contain no additional Pause buttons. The same
  navigation button stays at its menu position above a full-screen reader, and
  Resume preserves that exact open reader or dialog.
- Narration and Thoughts remain two neutral caption cards. Legacy feedback
  containers are held in an inert hidden source area, where they cannot create
  extra green panels below the captions.
- Surveillance findings use an actual room thumbnail; Clara's recording uses a
  recorder image instead of a supply-pouch/document icon.
- The first payphone response questions who is calling and why they want an
  answer. It no longer claims the hard-wired telephone has no wires.

## Sound, rear-view finds and optional references

- Three replacement synthesized air-foley beds use twelve varied breath cycles,
  asymmetric inhalation/exhalation, different airflow colours and irregular rests.
  Healthy breathing is quieter. Changes between condition tiers fade the outgoing
  breath rather than chopping it off; Pause freezes that transition too. The
  machine, wind, pickup and other effects retain their existing files.
- Nine authored rear-view furniture targets spread existing ammunition, useful
  tools, charging equipment, records and an optional prop across the chapter.
  Existing pickup IDs, resource totals and progression gates are preserved. The
  early lighter and fluid remain available before the hazard.
- Optional high-resolution game-art inspections show the red/white Umbrella
  design, Sweet Tooth's clown-headed ice-cream truck, a Mortal Kombat dragon
  medallion/arcade flyer and an Overwatch-emblem mug. They have matching finding
  previews, are read once, and are not required to finish Chapter 1.
- The active metadata contains 54 native room paintings, 54 directed door
  mappings and 178 authored fixtures across 27 rooms. No continuous 360 panorama
  or fake high-resolution enlargement is introduced.

See [VALIDATION.md](../VALIDATION.md) for executed checks and remaining test limits.
