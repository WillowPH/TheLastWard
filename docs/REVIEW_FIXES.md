# Chapter 1 correction pass

## Delivery

The primary download is the complete multi-file project. Its index loads separate
JavaScript and CSS; artwork, fonts, audio and data remain in their own directories.
The old embedded HTML and player/source split are removed from current downloads.
Python 3 starts a local server; play requires no external internet.

## Interface and interaction

- Reference three-column layout: navigation and local map, full-height scene,
  physical/mental condition, flashlight percentage, ammunition and inventory.
- Restrained corner brackets replace orb markers. Strong mode adds larger brackets
  and contextual symbols. Subtle/Strong selection is exclusively in Options.
- Item clicks preserve yaw. Only deliberate look input or keyboard target focus
  changes the camera. Examinations do not zoom the background.
- Item icons have bounded cells separate from text and controls, including the
  photographic negative and gun. Note thumbnails cannot cover their titles.
- Answered phones remain completed through save/reload. Inactive-phone feedback
  appears beside the phone and its target is then disabled. A later genuine story
  call can reactivate that phone. Transcripts remain in Files.
- Completed staff-portrait puzzle loses its scene target; unresolved puzzle access
  remains available so inspecting once cannot lock progression.
- Mini-map focuses on the present room and its neighbors; adjacent destinations
  can be entered directly. Full-map adjacent travel also takes one click.
- Flashlight is directly switchable from the right HUD.

## Rooms and motion

- Continuous horizontal rotation replaces the Turn Around UI. Front, rear, left
  and right are connected views; targets and effects move with their own art plane.
- All 27 rooms have independent side-view atlases. It is a fixed-position panorama,
  not a fully modeled room. Joins can be visible between painted views.
- North corridor door targets and Mercer/trolley/chart geometry are corrected.
- Room 12 now depicts both real front routes. Service/generator targets are aligned.
- Children's unused front door is blocked by furniture; the actual return is behind.
  Unused Staff Lounge, Isolation and Surgery doors are visibly barred.
- Lobby exterior exit is blocked with furniture, rather than suggesting an escape.
- All 27 front window sets have authored snow masks. Indoor particles are not used
  to simulate exterior snow. Security scan effects stay within the CRT screens.
- Brief irregular lamp dips darken the interior while excluding exterior glazing.
  Motion and light flashes can be disabled in Options.

## Verification

See VALIDATION.md and tests/results JSON reports for browser evidence. Full routes
and focused interaction checks establish functional behavior; they do not replace
human artwork review or first-time-player pacing assessment. Start a new game for
the corrected build. Earlier save namespaces are preserved separately.
