# Current visual review

Use the complete Project ZIP and its Python launcher. The old embedded HTML and
four-card room strip are superseded by the continuous panorama renderer.

All 27 room rear views were inspected. Corrected exports include Morgue (extra false
door removed), Service Crossroads (opaque hatch instead of an outside view) and
Surgery (usable route no longer barred). Actual rendered Security feeds were checked
against the CRT glass after UV adjustment. Shutters, stove, spent hoist, Mercer cover
and Kessler aftermath were inspected as local state overlays in the live viewer.

The fixed scene/HUD was reviewed at the supplied screenshot's 1672×941 proportions;
automated bounds checks also cover tablet and phone widths. This follows the reference
layout while using the new room art. It does not reproduce the reference painting.

World effects and targets share the panorama's projection. Snow is limited to authored
exterior panes, lamp dips exclude outside glass, and CRT scanlines stay inside screens.
The floor plan uses room polygons and actual shared doorways. Its unexplored/locked
state is intentional until the player finds the map.

For measured checks and limits, see ../VALIDATION.md.
