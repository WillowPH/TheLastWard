> Historical spherical-view controller. The current user-approved build uses native
> room-facing views; see [ROOM_VIEW_SETUP.md](ROOM_VIEW_SETUP.md).

# Click-to-snap camera setup

The project uses JavaScript/WebGL. The optimized controller is
[`js/snap_camera.js`](../js/snap_camera.js); spherical rendering is in
[`js/panorama_renderer.js`](../js/panorama_renderer.js), and game/HUD integration is
[`js/room_orbit.js`](../js/room_orbit.js).

```js
let yaw = 350;
const camera = WardSnapCamera.create({
  getAngle: () => yaw,
  onUpdate: (angle, pitch) => {
    yaw = angle;
    viewer.look(angle, pitch); // your WardPanoramaRenderer instance
  },
  onState: busy => { scene.inert = busy; },
  snapSpeed: 10
});
deskButton.onclick = () => camera.snapTo(10);
```

- Load `snap_camera.js` before the integration script. Create one controller per viewer.
- Connect HUD buttons to `snapTo(0)`, `snapTo(90)`, `snapTo(180)` and `snapTo(270)`,
  or use a room POI's actual authored yaw. Optional `{pitch: 12}` centers low objects.
- `snapSpeed` is responsiveness per second, not degrees per second. Higher is faster.
  The game's Options exposes 6, 10 and 16; reduced motion can use `{immediate:true}`.
- Use `onState` to lock scene and game input; also guard delegated mouse/key handlers.
  The shipped integration captures game clicks, wheel and keys during glides, disables
  the HUD and rejects retargeting. Escape completes the current glide safely.
- Keep object inspection separate from navigation. An ordinary object click does not
  call `snapTo`, change field of view, replace the viewer or zoom the background.
- Store room targets as UV rectangles in `data/panorama360_world.json`. Their yaw is
  `(u / 100 - 0.5) * 360`; author each door against the actual artwork. Regenerate
  runtime metadata with `python3 tools/build_panorama_world.py`.
- Dispose/cancel when changing rooms; restore the saved yaw/pitch on loading a save.

The wrap delta is `((to - from + 540) % 360) - 180` after normalization.
350°→10° therefore travels forward 20°, internally to 370°, then normalizes to 10°.
Each frame uses `target + (current - target) * exp(-snapSpeed * deltaSeconds)`.
This is independent of frame rate, never overshoots, and snaps exactly once within
0.02° of the target. It stops requesting frames after arrival.

Verification: `node tests/test_snap_camera.js` checks both wrap directions, exact
stop, no idle jitter, no overshoot, 30/60/144 FPS equivalence, long frames, pitch,
retarget rejection and instant reduced-motion arrival. The browser review separately
checks real input blocking/unlocking and pixel equality at 0°/360° in all 27 rooms.
