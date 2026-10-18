# Chapter 1 implementation

Build: `last-ward-ch1-panorama360-3`. The latest user authorization replaces artwork
with genuine continuous panoramic rooms. This is a multi-file JavaScript/WebGL game.

| Responsibility | Authoritative implementation |
| --- | --- |
| Room art/UV data | `data/panorama360_world.json`, `assets/panoramic360/`, emitted `js/panorama360_world.js` |
| Spherical rendering | `js/panorama_renderer.js`: one texture, yaw/pitch ray projection, stable FOV, light cone |
| Snap camera/input | `js/snap_camera.js`, `js/room_orbit.js`: elapsed-time exponential glide, shortest wrap, input lock |
| Targets/states | `js/panorama_scene.js`: measured fixtures/doors, spherical projection, arrival orientation, persistent object layers |
| Atmosphere | `js/panorama_effects.js`: UV-clipped snow, local state art, CRT feeds/scanlines, lamp dips, fire and sprinkler |
| HUD | `js/review_ui.js`, `css/review_ui.css`, `js/caption_ui.js`: three columns, stable flashlight button, fixed text pages |
| Floor plan | `data/floorplan.json`, `js/floorplan_ui.js`: room-cell architecture and shared door gaps, adjacent-only travel |
| Findings/inspection | `js/finding_icons.js`, `js/winter_examination.js`: icons, physical items, photos/backs, completed reads |
| Chapter mechanics | `winter_content.js`, `winter_gameplay.js`, `winter_threats.js`, `winter_story.js` |
| Sound | `js/chapter1_audio.js`, `audio/SOURCES.json`: local recordings and WebAudio |
| Delivery | `start_game.py`, platform launchers, `tools/package_build.py`, local service-worker cache |

Legacy artwork/modules remain as baseline references and mechanics dependencies.
`panorama_scene.js` is the active scene renderer; it does not use the old four-view strip.
No remote artwork backend is required or enabled by default.

Run `python3 tools/build_panorama_world.py` after metadata edits. It validates every
room target and graph door, unique artwork, state masks and physical floor-plan adjacency.
