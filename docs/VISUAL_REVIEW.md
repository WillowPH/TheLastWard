# Doorway and weather correction build

Extract the new ZIP and open `downloads/The_Last_Ward_Chapter_1.html`.
The doorway/camera correction covers every Chapter 1 room.
All 27 rooms remain playable. No extra rooms were needed to repair these inputs.

## Verified interactions

- On arrival, the entry door is behind you. Turn around to see it and click to return.
  Each door keeps its destination regardless of the route used. Locked doors explain what is needed.
- Click Clara's visible body to talk; her mask follows her silhouette.
- Turn around, click the rear door, use Face the room, or press Escape. Flashlight changes
  keep the reverse view open.
- Inspect Equipment cabinet once. The former two empty-case actions are one inspection.
- Inspect Room 12's supply shelf. After taking the dressing, the remaining action stays open.
- Take/Leave works per item. Nine focus-room collectibles have separate artwork and
  disappear after collection, including through save/load. Empty containers stay in place.
- Files remain in Files, without repeated scene hotspots after reading.
- Motion on/off controls visible animated rain, screen scans, lighting and dust.

## Animation preview

[Play the actual recorded browser preview](review/animated-scene.mp4).
The preview is captured from gameplay. Scene animation uses frame-driven canvas
layers, not fully animated video backgrounds or animated character performances.

## Scope

All 27 rooms have fixed reverse artwork and individually fitted rear door targets.
The five original focus rooms have nine authored removable pickups; the negative
in Children's Ward also uses a clean base and separate collectible layer. Other
rooms still need the full collectible-art conversion. Fixed scene views are
not a freely rotating 3D camera. Art has no baked interface labels.

Rain is clipped to the glass panes in both lobby views; indoor surfaces only have
soft reflected-light animation. The duplicate CSS rain layer is gone. Check the
window frames and the floor when comparing the two views.

![Lobby glass, front](review/weather-front.png)

![Lobby glass, reverse](review/weather-rear.png)

## Captures

![Security and Clara](review/clara.png)

![Object-side actions](review/object-actions.png)

![Floor plan](review/floor-plan.png)

![Locker openings](review/locker-peek.png)

## Pickup example

The handgun is separate from the open case; collecting the handgun leaves an empty case.

![Before taking handgun](review/pickup-before.png)

![After taking handgun](review/pickup-after.png)
