# Pre-build defect audit — 18 October 2026

Status: **Historical pre-build findings for the commit below.** The follow-up multi-file correction is documented in `VALIDATION.md` at the project root; these screenshots preserve the original defects.

Reviewed build: `0cf0790208deec0820b64a1ae2be4d73f8efec0c` on `build/chapter1-cinematic`.
The user supplied the UI reference again and requested checking before another version.
This folder contains browser observations and annotated artwork, not a new game build.
Gameplay source and download archives were not changed during that original audit.

## Confirmed defects and required corrections

| Report | Evidence | Required correction / acceptance check |
| --- | --- | --- |
| Project delivered as one HTML | The linked player ZIP has exactly two entries: HTML and START_HERE.txt. The separately available source ZIP has 306 files, including assets/audio/css/js/data/docs/tools/tests. | Deliver the complete source project folder as the primary project deliverable. Label the optional standalone player separately. Verify every referenced runtime file exists after extraction. HTML remains the web game's entry point; it must not be mistaken for the complete source project. |
| Panorama / Turn Around | Renderer clamps two independent camera offsets to -1…1 and swaps front/rear scenes. A Turn Around button is present. These are limited pans, not a continuous 360 room. | Genuine continuous horizontal rotation requires wraparound room artwork and a camera with continuous yaw. Keep doors, objects, weather and light regions attached to the same room coordinates. Do not claim 360 by hiding the button or crossfading unrelated pictures. Replace the front/rear presentation once a complete room rotation is verified. |
| Clicking items moves camera | An actual click on the Security diary changed its camera offset from unset to -0.62479. `focusin` unconditionally calls `WardWinter.reveal`. The listener is also added again on every render, retaining older room fixture closures. The camera can move between pointer-down and click, causing a missed action. | Pointer inspection must leave camera yaw/offset unchanged. Use one delegated event handler; reveal an offscreen target only for deliberate keyboard navigation. Test normal pointer clicks without first invoking the reveal helper. |
| Huge yellow paper icon / white text overlap | Reproduced in note-card-open.png. The document image is 276×276 px inside a 276×80 px icon container; text begins only 89 px below the image's top. The image overflows into both title and description. | Give the icon an explicit bounded size and clipped, independent layout cell. Separate image, text and actions. Assert rendered image/text rectangles never overlap; visually check long titles, multi-item containers and every card context. |
| Gun/item icons obscure text | Pickup cards use the same overflowing image container. The inventory list is a different older renderer. | Use a single bounded icon/copy/action component across pickup, inventory, storage and inspection contexts. Verify actual rendered bounds; checking only that an icon path exists is insufficient. |
| Staff portraits repeat | Even after setting the real solved/read state and rendering, the portraits target remains. The local completion predicate handles documents/look/eggs but not the portrait action's read state. | Completed portrait puzzle: no scene target or repeated prompt. Unsolved puzzle: retain a clearly named Arrange portraits action so inspection does not make Chapter 1 unsolvable. Individual photo examination and puzzle completion need separate states. |
| Telephone feedback at bottom | With a dead line, `answerPayphone` writes “The line is dead. It will not ring.” into #interactionText and opens no local panel. | Keep this response beside the telephone/in its interaction panel. Successful calls already have their own modal; completed calls should not leave a repetitive actionable target. Do not overwrite room narration with routine phone feedback. |
| North Patient Corridor door masks | wardnorth-authored-geometry.png: the left wr target extends past the actual door onto the right wall/floor; the right servicePassage target also includes wall area. Central door alignment is better. | Re-author target boundaries against visible frames; use polygons where perspective needs them. Verify both ends of each connection at normal view and while rotating. Collision tests between fixtures and doors alone do not prove a target matches a door. |
| Daniel Mercer mask | isoward-authored-geometry.png: patient target covers the foot of the bed/monitor/cabinet instead of his upper body. Treatment trolley target covers the patient; chart target sits beside the actual chart. | Re-author all three together against the patient, actual trolley and actual chart. Repeat for the covered-body state. A patient target must not block unrelated equipment. |
| Map takes more clicks | `wardMapSelect` selects an adjacent room and then inserts a separate Use connecting door button. Area selection introduces another step. | One click on an available adjacent room should use its connecting door; other rooms show information only. Keep visible lock/key labels and fixed adjacency. Sidebar should clearly show current room and immediate exits; full map remains available without obligatory tab changes. |
| Photographic Negative has no menu icon | The negative asset and ITEM_ART mapping exist. The inventory modal renders ICON text/glyphs instead of itemIconMarkup, so an existing art file does not establish a visible menu icon. | Use the actual film icon in every menu/context, with an accessible item name and bounded display size. Test inventory, combination selection, pickup and storage separately. |
| Children's Ward door leads nowhere | children-authored-geometry.png: front artwork contains a clear door at the left, but views.front.doors is empty. Its only real return connection, rc12 to Room 12, is defined on the rear image. | Each visible plausible exit must match exactly one physical route or be visibly and explicitly blocked. The artwork currently offers a false exit. Correct room art/orientation together rather than adding a shortcut that bypasses the fixed layout. |
| UI differs from supplied screenshot | Current scene begins at y=73 at the reference 1672×941 viewport, while the supplied reference scene reaches the top. It adds a stage heading, Hints/Motion toolbar, lower turn strip, duplicate status rows, bottom quick controls and an objective block. Navigation has no reference-style icons and Save/Load/Options order differs. | Rebuild the presentation around the supplied reference: left brand/nav/map; full-height central scene with floating narration/thought cards; right Physical/Mental/Flashlight/Ammo/Inventory. Keep text and images in separate bounded cells. Put motion/hint options in Options. Compare a screenshot at the same viewport, not just whether three columns exist. |
| Snow visible but not falling | Weather polygons exist only for Lobby, Security and North Patient Corridor. East Corridor, Isolation Treatment, Residence, Children's Ward and other artwork visibly show snowy exterior windows without matching weather definitions. | Audit every front/rear/rotating view with outdoor glazing; author exterior-only masks for all of them. Do not draw weather across interior walls, doors or desks. Verify motion with frame differences at normal settings and check reduced-motion behavior separately. |
| Lights do not visibly flicker | Current effect briefly adds a faint radial glow for 1.2 seconds out of a 29-second phase. It does not visibly switch/modulate an actual room fitting. Reduced-motion preferences also disable it. | Author fitting/light-pool regions with visible but occasional brightness failure/restoration, respecting the light setting. Test the event over its full cycle. Generator/emergency/outage artwork and illumination must remain story-consistent. |
| Lobby still advertises the exterior exit | Lobby artwork still exposes the entrance doors. An explanatory look interaction does not visually block them. | Revise the environment art to show a substantial, believable furniture barricade or remove that opening from the playable composition. Keep Security/East Corridor routes distinct. Verify the barrier is part of the environment, without baked interface labels. |

## Additional visual mismatches found

The reported masks are not isolated mistakes. In the reviewed Children's Ward image,
the drawing target lies on the curtain beside the drawing, and the rabbit target is
shifted to the right of the toy. In the treatment room, the chart and trolley are also
misplaced. See the annotated images in this directory. These findings require a
room-by-room visual pass, not another universal coordinate adjustment.

## Why the previous green tests were insufficient

The earned routes establish a graph that can be completed, but use a reveal helper
before clicking target rectangles. That hides the ordinary-click camera defect. The
icon audit verifies file existence, not legibility or overlap. Geometry collision
checks do not verify correspondence with visible objects. Earlier motion tests often
use reduced motion, so they cannot establish that snowfall/flicker is visible during
normal play. A valid route through every room does not detect an unconnected doorway
painted into an image.

The earlier completion claims exceeded that evidence. A replacement must pass visual
and ordinary-input checks in addition to progression tests.

## Checks required before packaging

1. Approve a complete continuous room rotation with stable angular targets and no Turn Around button; use it as the camera/art contract for the room conversion.
2. At the supplied reference resolution, compare UI placement, icon/text separation and scene framing with the screenshot. Check smaller viewports separately.
3. Click every authored object and door with ordinary mouse/touch input; no target-reveal helper. Camera must stay fixed during item examination.
4. Visually match every door/object target against its actual artwork, including covered, collected, open, powered and trap states. Every visible door gets a destination or a physical blocker.
5. Inspect/read/leave/take each object class; completed non-puzzle examinations disappear, and unresolved puzzle controls remain usable.
6. Check phone responses near the handset, one-click adjacent map travel, and every item icon in each menu context.
7. Observe snow/flicker through complete normal-motion cycles, clipped to actual exterior panes/fittings; verify power transitions and accessibility settings.
8. Repeat earned Chapter 1 routes after the visual changes. Validate the extracted multi-file source project and optional standalone separately, including offline asset/audio behavior.

## Audit artifacts

- audit.json: observed state, current geometry, camera movement, package inventory and weather coverage.
- note-card-open.png: reproduced overflowing document icons and obscured text.
- lobby-ui.png: current UI at the supplied reference viewport.
- wardnorth-authored-geometry.png: current targets over actual corridor art.
- isoward-authored-geometry.png: patient/trolley/chart mismatches.
- children-authored-geometry.png: false visible door and shifted object targets.

This is a defect audit, not a claim that the listed corrections have already been made.
No replacement player ZIP, version change, commit or push was performed.
