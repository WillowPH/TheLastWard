# Implementation map

The uploaded Cinematic Project is the baseline. The rejected five-room pilot is not
merged into it. The complete agreed scope is retained in docs/MASTER_REQUIREMENTS.md.

| Area | Implementation |
| --- | --- |
| Chapter boundary and gates | js/chapter1_complete.js; 27 rooms, 27 graph edges, one elevator entrance; no B2/Chapter 3 map nodes |
| Art and targets | data/chapter1_scenes.json, js/scene_manifest.js, tools/author_scenes.py; 155 fixtures and explicit door rectangles |
| Scene/state/inspection | js/chapter1_scene.js; art and targets resize on one uncropped plane; no arbitrary coordinate fallback |
| Threats and conditions | js/chapter1_survival.js; traversal, encounters, injury aim/movement effects, hiding, rare hallucination, sprinkler recovery and cold/wet recovery |
| People and evidence | js/chapter1_people.js; named NPCs, coherent aftermath, missing-nurse evidence, non-repeating consequences |
| Recorded sound | js/chapter1_audio.js; local playback, spatial cues from graph distance, volume buses and sound captions |
| Accessibility/layout | css/chapter1_scene.css; hints, motion/flash controls, keyboard focus, responsive survival controls |
| Save and delivery | distinct build keys/schema, terminal exports, completion record, tools/package_build.py, offline service worker |

## Artwork rules

All 27 active backgrounds were newly generated for this build and inspected against
room connectivity. Original JPG backgrounds and unused later-chapter backgrounds are
removed from the runtime asset directory. Styles are shared; compositions are distinct.
No random object-placement search or generic door-slot fallback is used by the active
renderer. Seeded supply pouches and phones have authored locations and physical layers.

Only real graph connections receive travel targets. Other pictured doors are sealed
props or decoration. The elevator's rear doors are operated by its controls; they are
not an invisible doorway into an unfinished Chapter 2. Its side cage returns upstairs.

A changed scene can have changed geometry: Kessler's aftermath uses a separate image
and the inspection target moves to the visible fallen sleeve. Other state effects use
separate overlays and the established save flags. Documents remain physical papers
after reading; inventory pickups leave their item layer after collection.

## Audio rules

No browser oscillator, synthetic fallback bleep, or remote sound stream is used. The
phone sound is an edited mechanical-bell recording in a telephone cadence, not a newly
recorded vintage telephone. Heavy steps use recorded metal footfalls with pitch/EQ
processing. Sources, exact original paths, commit and file hashes are in audio/SOURCES.json.
Listening approval and long-session mix tuning remain human playtest work.

## Scope boundary

Chapter 2/3 content is not accessible or mapped. Source baseline functions relating to
later chapters remain in inherited modules where harmless, but their locations and
routes are removed from the active graph. No Chapter 2 completion is claimed.
The desired 2–3-hour runtime and final human acceptance of pacing remain unverified.
