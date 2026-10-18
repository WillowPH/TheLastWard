# Native room-view implementation

Build: `last-ward-ch1-roomviews-4`. The user explicitly selected sharper room-facing
views after the 1774px-wide 360° source limitation was measured. The spherical renderer
and joined-strip renderer are inactive. Their sources remain as historical references.

| Area | Active implementation |
| --- | --- |
| Room art/geometry | `data/room_views.json`, `js/room_views_data.js`, `assets/rooms/`, `assets/reverse/`, `assets/room_views/`: 54 distinct native 1448×1086 views and centered-percent targets |
| Rendering | `js/room_view_renderer.js`: 2D canvas, whole-image fit capped at native source size, no crop or zoom; flashlight only adds light in dark rooms |
| Scene | `js/room_view_scene.js`: one fitted art/target plane, state assets, entrance-facing logic, saved view, click priority, persistent items and hiding slots |
| Mouse | `js/room_orbit.js`: click arrows outside the art or drag sideways to change view; 8px click/drag threshold, 55px turn threshold, no click-through, no bottom POIs |
| Atmosphere | `data/room_view_effects.json`, `js/room_view_effects.js`: 71 protected glass cells across 8 exterior views, fitted shutter material, CRT feeds/messages, stove fire and independent open-window patches |
| HUD | `css/review_ui.css`, `css/reference_theme.css`, `css/room_views.css`, `js/review_ui.js`, `js/caption_ui.js`: charcoal/brass reference layout, fixed paginated text cards, responsive Thoughts |
| Inventory/requirements | `js/inventory_discard.js`: protected progression equipment, shared-key last-use checks, confirmation, capacity/persistence and practical Thoughts |
| Game systems | `winter_content.js`, `winter_gameplay.js`, `winter_threats.js`, `winter_story.js`: progression, hazards, sanity, finite enemies and one-time incidents |
| Delivery | `START_GAME.exe`, `launcher/`, platform launchers and `start_game.py`: local-only standard-library servers, separate source/assets/audio/data |

Regenerate metadata with `python3 tools/build_room_views.py`. It checks unique image
hashes and dimensions, all 162 fixture IDs and 54 directed graph-door assignments.
The original generated image edits are preserved in the development workspace;
`data/room_view_art_edits.json` records the three native asset edits and provenance.
Historical review screenshots are omitted from the ZIP; every game asset is retained.
