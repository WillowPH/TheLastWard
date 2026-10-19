# Chapter 1 follow-up — v6, 19 October 2026

Build `last-ward-ch1-chapter-review-6`. Existing v5 saves remain compatible in the
same browser/local port and migrate their build marker after loading. This update
retains separate project files and the Windows launcher without a Python requirement.

## Player-facing changes

- The Night Attendant Journal keeps its short trailing phrase on the same sheet
  when a small, readable type adjustment makes it fit. Narrow screens retain all
  text through real pages; no text is removed or hidden.
- Original calm, caution and danger breathing loops replace repeated hurt grunts.
  Sanity alone does not trigger injured breathing. Longer smooth machine hum and
  exterior wind beds replace the short repeating lobby sound. A restrained original
  pickup cue replaces the bottle/dishes recording; it does not copy another game's audio.
- Pause is available with the mouse in navigation and open dialogs. It freezes audio,
  battery, exposure, world actions, visual motion and remaining real-time deadlines.
  The exact record/puzzle stays open. Returning from a background tab waits for Resume.
- Right-inventory controls appear beside the grid. No dropdown or scrolling submenu
  is needed for use/combine. Ingredient slots remain clickable. Supplies show xN,
  ammunition shows exact quantities, and weapons show loaded/reserve values.
- Story and Normal automatically remove truly spent keys/tools after their final
  matching use. Nightmare retains manual confirmed disposal. Required shared keys,
  unused consumables, firearms, flashlight and lighter remain protected.
- Security's cabinet no longer holds most early supplies. Its access card, lighter,
  fluid, battery cache and Heller note use distinct rear furniture. Rourke's final
  journal contains one record; other pages are scattered into matching furniture.
  Three sparse rooms gained modest optional rear recovery supplies.
- Closed lobby shutters have warm interior reflections rather than visible snow glow.
  Shutters retain their native fitted artwork; plank placement retains confirmation
  and a substantial horizontal board. Exterior snow stays within glass masks.
- East Corridor arrivals from Lobby/Security face toward Patient Wing; returning from
  Patient Wing faces away from that entrance. The map arrow follows authored room
  bearings and the current front/rear view.
- Conscious Daniel Mercer shows pallor, branching veins and a damaged gown. His
  one-time decisions and covered death state remain persistent.
- Sister Mimi is portrayed as helpful and trusted in early notes. Restricted later
  evidence shows her as a victim of experimentation whose condition is deteriorating.
  Her sinister/unstable phase is revealed later, rather than spoiling her first impression.
  Her Chapter 2 encounter sequence is not implemented in this Chapter 1 update.
- PEEK exposes the actual room through the hiding place's physical openings. Closing
  the peek returns to darkness. The old opaque parent layer no longer blocks the view.
- Subject X blocks all casual travel paths while standing in reach. Concentrated
  firearm hits create a temporary knockdown: two handgun rounds or one heavier shot.
  It recovers after a bounded turn/real-time window. Cover, traps and risky escape
  remain alternatives. Existing finite ammunition caches cover the added cost.
- Infected have three distinct visible presentations. Real enemies no longer use a
  transparent fade, and their scale is consistent with room furniture.
- Doors show a latch/hinge opening, frame depth and the destination's lighting.
  Wet/cold hands slow the opening. Input locks during the transition; Pause remains
  usable, and duplicate clicks cannot queue a second trip.
- The Physical Condition trace turns amber/red for Caution/Danger. HUD/dialog fills
  use charcoal and warm neutral colours. Save is a separate navigation item; Options
  contains presentation preferences. Subtle interaction hints are the default.
- Security CRTs show monochrome game-room feeds inside their screens, with limited
  battery standby feeds before generator power. Screen illumination stays local.
  Completed Security pickups leave no persistent green focus/filter layer.
- The optional one-time purge releases a seized linen-return reserve. Its confirmation
  explains both the supplies and the three dangerous windows; all catches must close
  before collection. It is a risk/reward choice, not an obligatory nuisance.

## Verification

See `VALIDATION.md` and `tests/results`. New focused suites cover audio, inventory,
combat, room distribution/art, HUD/PEEK/doors, and Pause/journal behaviour. Earned
Normal and Story routes visit all 27 rooms and reach the elevator using collected
ammunition to stagger Subject X. First-time human pacing and Windows desktop
execution remain outside these Linux browser checks.
