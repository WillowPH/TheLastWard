# Room-facing views and mouse setup

This is the active presentation. Load `room_views_data.js`, `room_view_renderer.js`
and `room_orbit.js` before `room_view_scene.js`; load `room_view_effects.js` afterward.
Keep reference_theme.css and room_views.css after the base styles.

- Use one 1448×1086 painting per authored facing. Fit the WHOLE image with a uniform
  scale no larger than1. Never use cover-cropping, fake4K resizing or a 360° texture crop.
- Place targets in the same fitted plane. Rectangles are centered percentages `[x,y,w,h]`.
  Edit `data/room_views.json`, then run `python3 tools/build_room_views.py`.
- `WardWinter.orbit.setView('front'|'rear')` changes facing. Side arrows and a55px
  horizontal mouse drag call this. Input locks during the short optional fade; drag
  release cannot click the object beneath it. Ordinary object clicks never move artwork.
- Keep navigation arrows in the side matte, outside the paintings, so edge objects
  remain clickable. No bottom labels or POI picker is rendered.
- Mark each door's real view and rectangle. On arrival, choose the opposite facing
  from the door used; preserve `roomView` when restoring a saved game.
- Author weather in `data/room_view_effects.json` against actual visible glass cells,
  excluding frames, bars and foreground objects. Interior observation glass has no snow.
  Place CRT scanlines/messages inside actual screens and state patches in their fixtures.
- Practical blocked actions call `WardWinter.think(text)`; puzzle choices stay in dialogs.
  Discard policy belongs in inventory_discard.js and must protect unfinished item uses.

Historical spherical-camera code remains in the repository but is not loaded by index.
The old snap-camera mathematical tests do not validate the current room-view navigation;
use the native presentation, target and full-route suites documented in VALIDATION.md.
