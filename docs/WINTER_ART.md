> Current presentation:54 native room-facing paintings; see [ROOM_VIEW_SETUP.md](ROOM_VIEW_SETUP.md)
> and `data/room_view_art_edits.json`. The outpainted/spherical notes below are historical.

# Winter artwork provenance and presentation

All newly generated visuals are fictional game artwork produced for this project;
no photographs of real injuries, blood or gore are used. Environment requests exclude
interface text. Object names, prompts, dates, messages and captions are rendered by
JavaScript/HTML rather than painted into backgrounds.

- `data/panorama_assets.json` maps all 27 independent wide room fronts.
- `data/winter_state_assets.json` records generated state/prop source paths retained in
  the development workspace, and state-image destinations. Wide state variants cover
  Mercer's covered bed, Kessler's aftermath, armed/spent laundry hoist and drained tunnel.
- `assets/reverse/lobby.webp` and `wardnorth.webp` were revised for exterior snow;
  `assets/states/wardnorth_windows_open.webp` raises all three lower sashes. Individual
  clipped overlays restore each closed window as its catch is secured.
- `assets/characters/patient_walk.webp`, `nurse_walk.webp`, `subject_walk.webp` contain
  four equal-width walking frames. `shrouded_figure.webp` supports transient visual
  episodes. Transparent sprites have ground shadows and floor-based placement.
- New physical props include a brass lighter/fluid tin, substantial wooden plank,
  wooden drawer and metal container interiors, chipped coffee mug, opening-day photograph
  and a three-portrait sheet. Inventory and inspection use these local assets.
- Small authored SVG props cover the drying stove, candles, CRT shell, purge handle,
  toy truck and individually shaped interlock contacts. They are separate object layers.
- The Caveat handwriting font is distributed under its SIL Open Font License in
  `assets/fonts/Caveat-OFL.txt`, embedded alongside the existing font/audio licenses in
  the standalone HTML.

Some requested bloodier regular-infected renders were rejected by the image service.
The delivered regular enemies use approved fully clothed, torn/stained designs. Subject
X has a distinct broad silhouette, coat and opaque shield. These are prerendered sprites,
not skeletal 3D characters. Background motion is layered weather, flicker, screen feeds,
prop glow and transitions; it is not continuous video of every room object.

Source audio details and processed-output hashes are in `audio/SOURCES.json`. The winter
wind removes silent padding from a CC0 recorded air sample, normalizes and loops it;
no oscillator fallback generates gunshots, footsteps or creature voices.
