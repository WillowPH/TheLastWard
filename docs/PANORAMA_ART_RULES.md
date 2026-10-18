> Historical360 artwork rules. The active native-view pipeline is documented in
> [ROOM_VIEW_SETUP.md](ROOM_VIEW_SETUP.md).

# Room artwork and spatial rules

Each room uses one coherent 2:1 equirectangular painting from one fixed eye position.
Do not concatenate unrelated front/rear pictures. Keep level eye height, compatible
left/right boundary geometry and consistent ceiling/floor perspective.

Before generation, define the room's left-to-right longitude layout, exact number
of route doors and each wall's purpose. Route doors connect only to the fixed graph.
Put exterior glazing on a separate exterior wall. Interior observation glass shows
another enclosed hospital space. Enclosed service corridors have no snowy landscape.

Exclusions: no exterior windows directly next to interior doors; no transparency
between indoor rooms and the outside world through interior walls; no UI, EXAMINE,
INSPECT, cursors, button labels, schematic green lines, extra exits or blocked usable
routes. Environmental signs may exist, but interaction labels are rendered by the game.

Review every rendered direction and the rear boundary. Measure UV targets against
visible objects, not generic room templates. Check every route in both directions;
arrivals face away from the door just used. Check hit priority at overlapping related
containers and objects. Window masks stay inside glass, and CRT masks inside screens.
State changes use painted local overlays in the same UV space, never black rectangles.

Authoritative metadata: `data/panorama360_world.json`. Original generation references:
`data/panorama360_art.json`. Runtime art: `assets/panoramic360/` (2048×1024 WebP);
seven local state images live in its `states/` folder. Generated originals were retained
in the development workspace; the delivery includes the actual runtime artwork.
