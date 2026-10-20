# Room-facing views and mouse setup

This is the active presentation. Load `room_views_data.js`, `room_view_renderer.js`
and `room_orbit.js` before `room_view_scene.js`; load `room_view_effects.js` afterward.
Keep reference_theme.css, room_views.css and reading_review.css after the base styles.
Load reading_review.js after inventory_discard.js, then survival_review.js,
combat_pass.js, hud_view_pass.js, then chapter_balance_v8.js, chapter_puzzles_v8.js,
chapter_survival_v8.js and chapter_ui_v8.js. Keep pause.js last. The final wrappers enforce
death, door-transition locking and pause consistently.

- Use one native painting near 1448×1086 per authored facing; retain real source dimensions. Fit the WHOLE image with a uniform
  scale no larger than1. Never use cover-cropping, fake4K resizing or a 360° texture crop.
- Place targets in the same fitted plane. Rectangles are centered percentages `[x,y,w,h]`.
  Edit `data/room_views.json`, then run `python3 tools/build_room_views.py`.
- `WardWinter.orbit.setView('front'|'rear')` changes facing. A55px
  horizontal mouse drag calls this. Input locks during the short optional fade; drag
  release cannot click the object beneath it. Ordinary object clicks never move artwork.
- Do not add view-arrow buttons, bottom labels or a POI picker. Object clicks stay
  separate from the turning gesture. Pause remains in left navigation, not dialogs.
- Mark each door's real view and rectangle. On arrival, choose the opposite facing
  from the door used unless `entryFacing[doorId]` explicitly authors another facing.
  East Corridor looks toward Patient Wing from Lobby/Security. Preserve `roomView` on load.
- Author weather in `data/room_view_effects.json` against actual visible glass cells,
  excluding frames, bars and foreground objects. Interior observation glass has no snow.
  Place CRT scanlines/messages inside actual screens and state patches in their fixtures.
  Native state overlays are composited before lighting, so they cannot bypass darkness.
- Practical blocked actions call `WardWinter.think(text)`; puzzle choices stay in dialogs.
  Discard policy belongs in inventory_discard.js and must protect unfinished item uses.

Historical spherical-camera helpers remain in the repository but are not the active presentation.
The old snap-camera mathematical tests do not validate the current room-view navigation;
use the native presentation, target and full-route suites documented in VALIDATION.md.

V8 captions overlay the fitted native painting with no opaque backing. The UI layer
uses pointer-transparent cards and active caption buttons; preserve target access.
Solid enemy textures and PEEK adaptation are runtime renderer concerns, not
background painting edits. Keep new rear fixtures in authoritative metadata.
