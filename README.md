# The Last Ward — Phase 1 Room Art Fix

The five-room art/hotspot pilot is implemented. See [ROOM_ART_PASS.md](ROOM_ART_PASS.md)
for changes, checks, and the remaining Phase 2 scope. Run the editable site with
`python -m http.server 8000`, or open the packaged `The_Last_Ward_Phase_1_Fixed.html`
for standalone offline play.

---

## Original build reference

# The Last Ward — Chapter 1 Approved Cinematic Build

## Playing

* Standalone offline game: download `The_Last_Ward_Chapter_1_Approved.html` and open it locally in a modern browser. It embeds the packaged room artwork, item icons, gameplay code, and existing WAV effects.
* Editable site: extract this project and open `index.html` (or serve the project with HTTP(S)). When the site is hosted via HTTPS or localhost, the service worker precaches baseline assets for offline return visits.
* Start a **new game** because Chapter 1 progression keys, lighting and event flags have changed substantially since older builds.

## Exact UI direction

This uses the previously approved Blackridge lobby screenshot as the art/layout reference: left navigation with a findable partial map, large photorealistic central room stage containing the narration and amber THOUGHTS, and right physical/mental status, flashlight, ammunition, inventory and quick actions. There is **no second room-view pane or bottom interaction list**. Inspectable items use subtle hotspots embedded in the illustrated room; inspection close-ups occupy the same stage. Doors use the shared travel graph and transparent targets instead of floating sprite doors.

## Core Chapter 1 systems included

* An opening with flashlight OFF and no weapon, findable partial map, chained exterior exits, staff-card and maintenance-item gates, required generator repair, and power-dependent room exploration.
* Three different, seeded physical telephones; used story calls do not repeat.
* Later Subject X chase/roaming logic, places to hide, one-use environmental trap, rare reinforced-glass first-warning/second-fatal encounter, sanity-dependent hallucination beats, irreversible patient decisions, scripted horror incidents, photograph puzzle, and the Chapter 1 revelation / elevator gate.
* Health and mental condition cues, item slot limitations and medical supplies, Ink Ribbon saves, and **portable save-record export/import** from the Save / Load screen.

## Online / offline environment art

**Offline always works:** all required backgrounds, item icons, scripts and bundled sound effects are local. Select **Offline** on the start screen to make no online artwork requests; choose **Automatic** or **Online enhanced** to permit requests only when launched from a compatible website. The local environment loads immediately regardless of network conditions.

The project includes an optional same-origin server endpoint (`server/ward_art_server.py`) which can proxy a separately configured image-generation provider. It uses room/seed/state prompts and caches generated images server-side, while the browser caches successful same-origin assets. It does not determine geometry, doors, puzzles, or items, and runtime failure has no gameplay consequences. **A live paid AI provider is not configured in this deliverable.** See `ONLINE_ART.md` and `server/README.md`.

## Important limitations

* Only the lobby and some areas have polished photorealistic art derived from the approved concept. The other first-floor room backgrounds are **distinct local photographic compositions derived from a limited common base**, rather than independently art-directed complete scenes. They require further artwork for truly unique cinematic interiors.
* Existing WAV files were retained; many natural recordings requested (phone rings, hospital ambience, footsteps, generator startup) are not yet produced. The game intentionally remains silent when a sound file is absent.
* The current Chapter 1 is a **playable development build**; the aspirational 2–3-hour runtime has not been validated through manual playtesting. Some Chapter 2/3 legacy content is present in source as carryover, but Chapter 1 is the priority.
* Browser testing covered targeted functions and routes but not a completed human playthrough of every branch.
