# Implementation map

The uploaded Cinematic Project is the baseline. The rejected five-room pilot is not
merged into it. The complete agreed scope is retained in docs/MASTER_REQUIREMENTS.md.

| Area | Implementation |
| --- | --- |
| Chapter boundary and gates | js/chapter1_complete.js; 27 rooms, 27 graph edges, one elevator entrance; no B2/Chapter 3 map nodes |
| Travel and orientation | js/chapter1_navigation.js; shared adjacency guard, click cooldown, fixed front/rear portal identities, arrival orientation, 27 reverse backgrounds; black doorway-shading patches removed |
| Art and targets | data/chapter1_views.json, data/chapter1_scenes.json, js/scene_manifest.js, tools/author_scenes.py; 155 fixtures and explicit door rectangles |
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
and the inspection target moves to the visible fallen sleeve. Each room's portal IDs are partitioned into fixed front/rear views. The rear
portal ID never depends on S.prev. Camera schema 2 chooses the opposite facing on
arrival and migrates older saves once; manual camera state then persists. The
front plane is hidden and inert while rear is active. Every physical travel door
has one target in its own view, with measured per-room geometry. All 27 front
backgrounds remove the relocated door; all 27 reverse backgrounds show one fixed
closed doorway. These are two scene views, not a freely rotating 3D camera.
Contextual inspection keeps the original scene scale.
Hiding requires confirmation and reveals the room only through a narrow peek gap.
Other state effects use
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

## Visual review scope

See docs/VISUAL_REVIEW.md for the full camera pass and remaining collectible-art conversion.
js/chapter1_review.js provides the enlarged physical-connection map and visible
patient-action prerequisites. The actual graph is unchanged: North Corridor branches
to Room 12 and Isolation separately; Children’s Ward connects to Room 12.

## Input and object-layer repair

Clara uses an explicitly authored silhouette hit area. Reverse door buttons are
absolutely positioned inside the art plane and cannot cover footer controls.
Door targets belong to their fixed view, matching the revised artwork; the entry is behind arrival.
Door-lock failures are modal, and scene view survives flashlight updates.

The authoring script defines nine explicit collectible image rectangles for the
five focus rooms. The renderer removes each by its own saved object state. Base
artwork is cleared separately using authored edits. Containers can remain open for
multiple actions without resetting focus. The security cabinet's two empty-case
inspections are merged into one. `js/chapter1_motion.js` paints frame-driven layers
on the current front/reverse art plane; targets remain stationary and unobstructed.

## Exterior weather

`js/chapter1_motion.js` owns one independent transparent weather canvas. Hand-authored
front/rear glazing polygons exclude frames and interior objects. Ambient reflected
light is a separate canvas; the duplicate rectangular CSS rain and its keyframes
are removed. Reduced motion disables both. `tests/test_portal_weather.py` checks
actual doorway clicks and arrival/return facing across all 54 directed edges at
desktop/mobile sizes, save migration, asset loading, and every rain pixel outside
the permitted glass areas. It also runs against the packaged HTML offline.

Pursuer panning and sound captions use the fixed portal geometry and current camera
facing, including ahead/behind cues. Turning reverses the horizontal bearing.
