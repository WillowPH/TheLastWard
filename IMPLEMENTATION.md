# Winter Chapter 1 implementation

Build identifier: `last-ward-ch1-winter-1`. The uploaded Cinematic Project is the baseline;
latest decisions are preserved in `docs/DESIGN_NOTES.md`. Implementation was authorized
by “lets fire this up and build it.” Older notes-only instructions are historical.

| Area | Active implementation |
| --- | --- |
| Chapter boundary | `chapter1_complete.js`, `winter_content.js`: 27 rooms, fixed graph, clearance/pursuit/fuse gates, elevator ending and transfer record |
| Panoramas | `panorama_assets.js`, `data/panorama_assets.json`: 27 distinct 2:1 front images; rear art remains independently authored |
| Geometry | `data/winter_geometry.json`, `winter_geometry.js`, base `scene_manifest.js`: explicit room coordinates, no runtime wall-placement fallback; regenerate embedded coordinates with `tools/build_winter_geometry.py` |
| Content/seeds | `winter_content.js`: early winter journal, lighter/fluid, batteries, redacted Mimi documents, eggs, four named interlocks and saved item/container placements |
| Scene/UI | `winter_scene.js`, `css/winter.css`: shared art/target planes, camera rotation, local focus panels, Take/Leave, container imagery, item removal, reverse interaction, continuous circular four-view camera controls, transitions |
| Object inspection | `winter_examination.js`: physical object close-ups, photo reverses, seeded appointment dates, damaged/handwritten documents and literal transcription, radio tuning |
| Power/hazards | `winter_gameplay.js`: authoritative clock, Normal/Story battery drain, two limited automatic-reset outages, window catches, exposure, sprinkler, separate flashlight recovery, warming, lighter, wiring and four socket plugs |
| Threats | `winter_threats.js`: finite saved actor identities, damage/death, knockdown/re-entry, graph-based noise response, screams, shared in-room combat presentation, nonlethal imaginary encounter |
| Story/map | `winter_story.js`: Kessler choices, mandatory one-time suppression event on the return route after Room 12, phone transcripts, zone-based floor map and adjacent-only travel |
| Effects | `winter_fx.js`: snow clipped to pane polygons; optional localized light flicker; individual CRT clips and room feeds; sprinkler particles; stove glow. Effects are children of the same moving art plane |
| Audio | `chapter1_audio.js`, `audio/SOURCES.json`: local CC0 recordings, WebAudio spatial routing with HTMLAudio fallback, resumed playback after user gesture, measured output, winter ambience and creature voices |
| Persistence | `bootstrap.js`, `save.js`: new winter save namespace, saved placement/enemy/hazard/story state, checkpoints and completion export |
| Packaging | `tools/package_build.py`: complete multi-file project ZIP, Python stdlib launcher and optional deterministic cache |

The previous engine modules remain as underlying narrative/combat/inventory code; the
winter modules load last in the order declared in index.html. Their final overrides
are authoritative. The previous rain canvas mount is replaced, not run alongside snow.
The scene renderer does not use optional provider-generated backgrounds that could
invalidate the explicit target coordinates.

## State rules

- `S.placements`: saved seed plus approved object/container selections. Load/visits do not reroll.
- `S.enemyActors`: finite identities with health, room/home, alert expiry and knockdown.
  Noise redirects existing survivors through unlocked edges. A reserved window-breach
  actor is included in the initial finite registry; it is not an endless spawn source.
- `S.windows`: triggered, three closed flags, resolved and local exposure. The lever is
  irreversible once used; closing all catches resolves it for the run.
- Sprinkler trigger/stopped/recovered flags are independent. Its one-time required route
  event drops the torch; closing the valve does not retrieve it.
- Cold exposure is local and recoverable. Wetness expires or dries in warm rooms. No
  permanent stack of hunger/cold meters is added. Windows give a grace warning first.
- Major incident choices and aftermath flags persist. Hallucinations can refer to them
  without replaying them. False combat is one saved episode; visual episodes are capped.
- Hallucinated attacks have no real-health damage path. Shots consume real loaded rounds;
  waiting, retreat, damage or timeout resolves the encounter. Active unresolved cold/
  sprinkler hazards are excluded from beginning this episode.
- Normal infected killed in combat stay dead. Struggle costs health and leaves a living
  knockdown; that survivor can return on room re-entry with its health retained.
- Subject X remains a distinct pursuer, gated behind power, executive authorization,
  observation/Rourke evidence and at least 14 visited rooms. Ordinary fire delays it.
- Both real and imaginary combat keep room actors visible behind a compact control panel.
- One-off items disappear; completed documents remain available in Files. Within a
  container that still has contents, read papers can remain as noninteractive decoration.
- Opening an examination does not scale the room. Pure examinations retain the existing
  image node unless power, room, view, temperature or light state genuinely changes.

## Art and remaining limits

Room/environment artwork is fictional game art. Runtime labels, hints, dates, map text,
surveillance readouts and menus are game-rendered. The new front panoramas are not
mirrored copies. Persistent front-state variants retain the wide aspect ratio to avoid
camera jumps. Sprite sheets provide four walking frames; ambient layers provide motion
rather than full video for every background prop.

The image service rejected some bloodier regular-infected variants. Approved clothed,
torn/stained designs are used. Their presentation and frame-based animation can still
benefit from human art review. Automated route tests establish solvability, not ideal
first-time player pacing or a measured human completion time.

Mimi is Chapter 1 foreshadowing only. Her friendly introduction, surveillance revelation,
knife betrayal, stalking and containment ending remain Chapter 2 work. Her legal name
stays redacted. The existing Marian Vale evidence is a separate mystery thread.

## Review corrections (18 October 2026)

`room_orbit.js` moves four natural-aspect art/target planes on a circular strip.
`orbit_assets.js` supplies independent left/right artwork for all 27 rooms.
It is a fixed-position horizontal panorama; view joins can remain visible.
Pointer focus never invokes camera reveal. Keyboard focus deliberately reveals targets.
`review_ui.js` and `review_ui.css` apply the reference three-column HUD.
Subtle and Strong corner markers are configured only in Options. Inventory/inspection
art is bounded separately from copy. Dead-phone feedback stays beside the handset;
completed phones lose their targets unless a genuine later call activates one.
Exterior glazing is hand-authored in data/exterior_glazing.json; lamp dips exclude
windows. Marked unused doors are visibly barred; Room 12 has two actual door images.
The distributable preserves code/art/audio as separate files and starts a loopback
server with Python 3. No browser service worker is automatically registered.
