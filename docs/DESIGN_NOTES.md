# The Last Ward — consolidated design and correction notes

Recorded: 18 October 2026, Europe/Warsaw.

**Implementation authorized on 18 October 2026: “lets fire this up and build it.”**

The notes-phase restrictions below are historical. The current build implements Chapter 1; see IMPLEMENTATION.md and VALIDATION.md for scope and verified behavior.

## 1. Status, authority and scope

- This is a design record, not a release or a claim that the listed work is already implemented.
- During this notes phase, do not modify gameplay, generate production assets, package, publish or create another version until the user explicitly authorizes implementation.
- This document is stored separately from the game checkout. Creating these requested notes does not authorize changing the game.
- Some requirements preserve existing behavior; others correct reported bugs or add features. The existing build must be checked against the target behavior before implementation claims are made.
- The user's latest decisions supersede older suggestions and documents. Attached documents are project reference material, not instructions that override the user.
- Finish Chapter 1 before developing Chapter 2. Mimi's Chapter 2 outline is recorded here so Chapter 1 can foreshadow her correctly.
- Preserve the Blackridge Medical Complex setting, Monolith Pharmaceuticals, Project LULLABY and the year 1998. Keep their established identities and story roles consistent.
- The final Chapter 1 destination is the elevator leading into Chapter 2. Do not accidentally expose playable Chapter 2 routes early.
- Additional connecting rooms are permitted when they improve believable navigation. Original room-number conventions are not mandatory.

## 2. Decisions that replace earlier alternatives

- **Hospital layout stays fixed.** Do not shuffle room identities, floor plans or connections between runs.
- **Use controlled seed-based variation inside that layout.** Items and selected encounters may use approved alternative locations.
- **Snow replaces the exterior rainstorm.** This applies to effects, relevant art, descriptions and ambience. It does not remove water from the separate sprinkler incident.
- **Both cold-window events and the sprinkler incident are required.** The earlier suggestion that sprinklers were merely an optional alternative was superseded when the user explicitly restored the original sprinkler requirements.
- **Panoramic viewing is the intended camera direction:** horizontal looking around from a fixed player position. Exact turning range and presentation still need to be chosen. Full 360 degrees, vertical looking and free walking are unnecessary.
- With panoramic viewing, separate front/back item placement is absorbed into placement throughout the viewable panorama.
- **Subject X's full introduction is in the second half of Chapter 1.** Earlier content foreshadows him.
- **Mimi first appears in Chapter 2.** Chapter 1 introduces references to her, not her full encounter sequence.

## 3. Interface and scene composition

Use the user's supplied screenshot as the interface reference:

- Left: title/chapter information, navigation, Map, Files, Journal, Save/Load and Options.
- Centre: the room scene with contextual interaction controls.
- Right: physical condition, mental condition, flashlight status and battery percentage, ammunition and inventory.
- Lower scene area: narration and thoughts, composed so they do not cover required interactions.
- Move Turn Around into the lower GUI/action controls instead of leaving an isolated button at the top.
- Correct the reported regression where the scene sits too far down.
- Keep scene placement stable when narration, tooltips and inspection panels open or close.
- Keep core controls usable at supported desktop and narrow/mobile sizes.
- Turning around must produce an interactive view. It must not require toggling the flashlight to recover the normal scene.

Opening-scene alternative:

- Consider replacing the original opening view with clean artwork based on the supplied screenshot, or removing inappropriate doors from the original image.
- Remove the baked EXAMINE cursor/label from any screenshot-derived art.
- Do not remove a necessary route merely for visual composition. Match visible doors to the actual map.

## 4. Visual identity and room artwork

- Every room must have its own recognizable environment. No Laundry/Security Office reuse, Isolation/Patient Wing reuse or flipped Patient Wing standing in for Room 12.
- Preserve a coherent cinematic survival-horror game style across rooms, characters, objects, documents and effects.
- All blood, injuries, corpses, hanged bodies and body parts must be fictional game graphics. Never use photographs of real deaths, injuries or gore.
- Room artwork contains environmental information and believable in-world signage. Interface labels, cursors, buttons and hover text are rendered by the game.
- Remove old masks, black squares, placeholder objects and unintended leftovers.
- Maintain correct scale, perspective, floor contact and lighting for characters and props.
- Create appropriate changed-state art for opened containers, removed pickups, covered bodies, power changes, traps and real environmental destruction.
- Add suitable ambient motion: localized light changes, screen noise, outdoor snow and selected environmental movement. Avoid constant distracting motion.

## 5. Panoramic room presentation

- Let the player look left/right from a fixed position over a designed horizontal range.
- Create suitable wide/panoramic room art. Existing front and rear pictures alone do not contain the missing side walls and cannot simply be stretched into a complete panorama.
- Give objects, characters, hotspots, hint markers, windows and screens consistent room positions.
- When the view turns, their visual layers and interaction areas move together.
- Place props only where their perspective, scale and lighting fit the room.
- Limit outdoor snow, window illumination and screen effects to their actual surfaces/openings as the view moves.
- Preserve orientation and the identity of entrances/exits. Viewing changes must not alter the floor plan.
- Existing reverse views must remain functional until a panoramic replacement is complete.
- Suggested first validation: prove the full camera/object/effect interaction in one representative room before converting all rooms. This is a future implementation suggestion, not authorization for a build.

## 6. Doors, routes and transition animation

Navigation corrections:

- Repair broken doors, misleading destinations and connections that skip intermediate rooms.
- Rooms shown as connected on the map must have usable matching routes. Review the previously reported Room 12 / Isolation Treatment Room / Children's Ward connections and corridor dead ends.
- The door the player just used must be behind them on arrival, with a coherent default facing direction.
- A doorway into a dark room must not inexplicably glow as though that room were brightly lit.
- Doors shown in the artwork, authored hotspots, the map and enemy routes must describe the same hospital.
- Avoid cutout-only reverse-door views and noninteractive static reverse scenes.

Requested transition feature:

- Add short first-person door-opening transitions inspired by classic Resident Evil.
- Show an appropriate approach/handle/opening action, door sound and entry into the destination panorama.
- Match the actual door type, appearance and destination lighting.
- Locked doors give appropriate feedback and name the required access item or condition.
- Exact duration, replay speed and skip behavior remain design choices; quicker repeat transitions were suggested.
- Pursuit and sound logic must remain coherent across transitions.

## 7. Hotspots, layers and discoverability

- One visible object should have one coherent interaction entry. Do not attach window controls or unrelated objects to a payphone or directory.
- Hand-author precise hotspots for doors, drawers, desks, files, phones, switches, lockers, terminals and puzzle objects.
- No hotspots on empty walls, black door masks or overlaps with unrelated objects.
- Separate the base environment from collectible objects and changed-state overlays.
- Make important interaction hints more visible than the current faint dots.
- Retain Hints options, contextual cursors, object names and restrained hover/focus highlights.
- Use visual cues appropriate to the object: a paper corner, slightly open drawer, glint or carefully placed marker.
- Important objects should be discoverable without mouse-sweeping every surface.
- World objects must resemble actual props rather than generic blocks containing tiny icons.

## 8. Examination and object close-ups

- Remove the reported unwanted zoom-in/zoom-out effect during examination, including the phone interaction.
- Put contextual Examine controls near the selected object instead of forcing every action to the bottom of the screen.
- Selected small/story objects open in detailed, high-resolution central inspection views.
- Examples include mugs, portraits, photographs, keepsakes and personal belongings.
- Appropriate objects can be flipped or viewed from another prepared side, such as handwriting on the back of a photograph.
- The close-up must match the object placed in the scene.
- Not every object is needed for progression. Optional objects should add believable history, personality and atmosphere.
- Doors, phones and large fixtures can keep contextual interactions without a dedicated collectible-style close-up.
- After all relevant details are discovered, completed one-time inspections such as Staff Portraits stop offering redundant examination.
- Do not mark an object fully examined before a relevant reverse-side clue has been discovered.
- A genuine state change may make an object inspectable again. Unresolved containers and puzzles remain usable.
- Preserve necessary discoveries in Files/Journal so completing an inspection does not erase useful information.

## 9. Containers, pickups and icons

- Searching a drawer opens artwork of its interior, containing individually selectable objects.
- Distinguish collectible objects, readable documents that remain in place and decorative clutter.
- Offer Take / Leave for pickups. Leave must preserve the item for later.
- Remove duplicate Explore actions, especially on the equipment cabinet.
- Keep the container open while the player examines or collects multiple contents.
- Collected objects disappear from both the room and any container interior. They remain gone on revisits and after save/load.
- Separate collectible art from the base image so removal does not require black masks or leave a baked copy behind.
- Audit inventory, pickups, container views and inspection panels for missing icons.
- Supply clear, matching icons for every item that needs one, including the lighter and lighter fluid.
- Use appropriate transparent PNG prop/icon assets where requested, rather than generic square placeholders.

## 10. Documents, handwriting and legibility

- Mix typed clinical/corporate records with handwritten diaries, warnings, letters and maintenance notes.
- Give different writers recognizable pen/pencil styles, annotations, crossings-out and signatures where appropriate.
- Show documents as physical scene objects and detailed readable images when opened.
- Add torn edges, stains, blood drops, folds and damaged pages while keeping the actual writing readable.
- Include reverse-side writing where it serves a clue or story purpose.
- Preserve the document artwork in Files, with an optional readable transcription.
- A transcription reproduces the document's content; it does not interpret clues or disclose a puzzle solution.
- Essential information cannot depend on unreadable handwriting, a barely visible stain or a single subliminal frame.
- Once read, avoid repetitive scene inspections while keeping the record accessible.

## 11. Fixed layout and seed-based variation

- Generate the run seed automatically. Do not require the player to enter it.
- Keep the lobby/tutorial arrangement stable and the hospital floor plan fixed.
- Author approved placement slots in each room: suitable drawers, shelves, lockers, containers and surfaces.
- Let the seed select among valid locations; do not scatter items at arbitrary coordinates.
- The object's artwork, hotspot, hint and container association must all use the chosen placement.
- Save the chosen arrangement and subsequent object states. Re-entry and loading must never reroll them.
- Suitable variation includes supplies, selected key locations, optional documents, Easter eggs, matching puzzle codes/clues, eligible later phones and some finite enemy starting locations.
- Restrict progression items to smaller pools of sensible locations.
- Never place a key behind its own lock or create circular dependencies.
- Keep the lighter and fluid obtainable before the relevant hazard. Preserve access to all required elevator components and clues.
- Generate randomized solutions and their displayed written clues together.
- Major narrative order remains stable, including Subject X's second-half introduction and once-per-run story incidents.
- Suggested implementation order: establish safe supply variation, then extend to progression items once dependencies are validated.

## 12. Puzzles, access items and the final elevator

- Aim for Resident Evil-style reasoning and exploration, with short hands-on tasks also inspired by wiring/tuning interactions.
- Candidate tasks include connecting electrical wires, tuning a radio/stereo, adjusting equipment and examining records or photographs.
- Provide understandable rules, environmental feedback and discoverable clues.
- Hints suggest where to investigate or what evidence matters, without showing solutions.
- Length comes from meaningful exploration, discoveries, encounters and changing rooms, not hours looking for a tiny key.
- Clearly name keys/cards and show matching requirements at doors and in useful map/journal records.
- One key or card can open multiple related doors. Do not consume it after the first door if it has further uses.
- Record when an access item is no longer needed, or otherwise keep its remaining purpose understandable.
- Final elevator proposal: four themed fuse pieces restore its controls.
- A journal encountered within roughly the first 30 minutes introduces that objective and provides direction without listing solutions.
- The suggested chess-piece form originated from interpreting the user's phrase 'cheese pieces'; the exact visual theme is not finally specified.
- Complete required Chapter 1 milestones before the elevator ending. No accidental Chapter 2 bypass.

## 13. Electricity, lighting, blackouts and flashlight

- Before generator restoration, most rooms are dark. Any working lights need an understandable emergency/backup source.
- After restoration, room lighting, lamp states, reflections and light through doors must visibly match the powered condition.
- A suitable fuse or power component can restore a wing circuit once generator power is available.
- Flickering should affect actual fixtures and their illuminated surfaces, not unrelated areas of the image.
- Occasional temporary blackouts after restoration can renew flashlight usefulness. Power restores after some time; blackouts must not be constant.
- Leave substantial calmer periods between power events.
- Fix the flashlight making already lit rooms darker.
- Normal difficulty needs faster, meaningful battery consumption so the flashlight is not effectively limitless.
- Drain while switched on, preserve charge while off, and stop illumination at empty charge.
- Battery pickups replenish charge. Show remaining percentage next to the flashlight status, matching the reference UI.
- Balance battery availability, required dark exploration and blackouts so resource management matters without a progression softlock.
- Review existing charging methods against this intended balance rather than assuming their current behavior is acceptable.

## 14. Snow, windows and shutters

- Replace the exterior rain effect with snow and update related art, reflections, descriptions and ambience where necessary.
- Keep snow outside window glazing; any entering flurries are localized to actual open windows.
- Do not cover whole indoor rooms with weather particles.
- Open/closed window and shutter states need matching visual layers, lighting and sound.
- Add closable shutters with clear controls and persistent positioning.
- Screen, window and weather effects remain aligned during panoramic turning.

## 15. One-time cold-window hazard

- A window-control lever opens multiple windows.
- The player closes them individually to resolve the event.
- Use appropriate closeable windows; a genuinely broken opening may require barricading instead.
- Provide a clear warning period through wind, shivering, thoughts and visual/audio feedback before serious consequences.
- Prolonged exposure can reduce movement/escape effectiveness, affect aim steadiness, cause an occasional handling problem, and eventually affect health and sanity.
- Leaving the cold area reduces exposure. Closing the openings stops the source; reaching a warm powered room supports recovery.
- Once resolved, the scripted hazard cannot be reactivated endlessly in that run. Save its completion.
- Do not use it to force perpetual insanity or constant hallucinations.
- Cold remains a local, recoverable condition rather than a permanent collection of HUD meters.
- Exact timing, rates and exposure limits are balancing decisions still to be specified.

## 16. Required sprinkler incident

- A malfunctioning fire-suppression system activates once per run.
- Freezing water drenches the protagonist; he may recoil or slip.
- During the scripted event, he drops the flashlight.
- The flashlight becomes a real recoverable scene object; the player must pick it up again.
- A valve or related mechanism stops the water.
- Wet clothing persists temporarily. Wet footsteps and cold hands influence subsequent interactions.
- Create the visual sequence: localized sprinkler spray, wet environment, dropped flashlight, operating valve and water-off aftermath.
- Use appropriate water, impact, breathing and wet-footstep audio. This indoor water does not reinstate the replaced rainstorm.
- Provide discoverable recovery, preserve access to essential equipment, and save the event's completed state.

## 17. Lighter and fluid

- Introduce a reusable lighter and a separate lighter-fluid item.
- They combine/refill through the inventory system in a familiar way comparable to weapon/ammunition interactions.
- Represent empty/filled fuel state clearly. Successful uses consume a defined amount; the exact capacity and refill amounts remain open.
- Failed attempts on unrelated objects should not waste fuel.
- Make both obtainable before the hazard that expects the warming tool. Introduce their relationship with clear discovery/inspection information.
- Create transparent PNG icons for the lighter and fluid, plus suitable detailed inspection art.
- For warming, the lighter ignites an appropriate prepared stove/brazier or similar heat source; the resulting fire warms/dries the player.
- Old cloth as fuel in the laundry was discussed, but the exact warming interaction is not finalized.
- The lighter needs an additional useful interaction. Suggested options are lighting chapel candles to inspect a dark memorial, or melting a wax seal on a small container. Select and integrate a logical use rather than treating every suggestion as mandatory.
- Preserve enough fuel or alternative recovery options to avoid a softlock.

## 18. Audio and finite enemy response to noise

Audio repair:

- Investigate the user's report that sound is not working. Verify actual audible playback, controls and interactions, not only that files exist.
- Cover ambience, footsteps, voices, doors, gunfire, reloads, impacts, machinery, snow/wind, water and phones.
- Subject X needs distinctive heavy footsteps and useful directional cues.
- Sound direction and distance should correspond to connected locations and the current player orientation.
- Use quiet periods intentionally; avoid constant repetition and generic synthetic substitutes where believable recordings are expected.
- Preserve local/offline playback where required by the existing project.

Noise response design:

- Use a finite, persistent population of infected with identities, locations, health and behavior.
- Noise attracts existing eligible enemies; it does not generate unlimited replacements.
- Hearing depends on range, walls, doors and actual connectivity.
- Responders travel through connected rooms with appropriate warnings such as approaching footsteps.
- Repeated shots update an investigation instead of queuing a new wave per shot.
- Dead infected remain dead. Survivors keep damage and can recover or move.
- Enemies eventually conclude unsuccessful searches or return along believable routes.
- Screaming/singing infected can alert nearby existing enemies, with pacing limits rather than endless reinforcement loops.
- Tune population and hearing so most incidents attract manageable groups. Exact counts/ranges are not yet fixed.
- Subject X is a separate persistent pursuer whose search can be redirected by noise once active.

## 19. Regular infected: visuals and combat

- Use visible animated enemies occupying the room, not small icons or ungrounded static cutouts.
- Correct scale, floor contact, perspective, shadows and lighting.
- Make infected bloodier, with torn gowns, damaged staff uniforms and ripped civilian clothing, inspired by classic Resident Evil 1.
- Vary faces, wounds and clothing within the consistent fictional game-art style.
- Provide appropriate idle/approach/attack/hit/stagger/fall/death states.
- Killing an infected removes it after the death sequence and permanently records its defeat.
- Struggling or forcing past causes a temporary stagger/fall and an escape opportunity, with a meaningful health/resource cost.
- A living infected can recover and be present on return. It retains damage and follows persistent location rules rather than respawning or teleporting arbitrarily.
- Real and hallucinated infected share the same visual treatment so appearance does not reveal which is imaginary.

## 20. Subject X

- Follow the master requirements for the persistent pursuer.
- Make him clearly taller, broader and bulkier than ordinary infected, with an imposing silhouette inspired by Mr. X from Resident Evil 2.
- Convey weight through posture, movement, shadows, reactions and heavy footsteps. Keep his room scale believable.
- First half of Chapter 1: foreshadow through heavy sounds, damaged doors, security recordings, shadows and containment evidence.
- Second half: first full introduction and scripted pursuit teaching escape.
- His introduction happens once; the subsequent hunt continues as a gameplay system.
- Show him when physically present and move him through the same connected-room network.
- Detection includes exposed players, movement, noise and gunfire; flashlight use may influence it according to the established system.
- He follows through doors and searches after losing contact.
- Escape involves breaking contact and hiding. Safe rooms and paced downtime provide breathing space.
- Weapons and environmental traps stagger/delay him. Ordinary gunfire cannot permanently kill him.
- Do not make him vanish permanently after one encounter.
- Save pursuit state and preserve meaningful audio/visual warning cues.

## 21. Traps and plank placement

- Let the player deliberately prepare and activate traps, including the suspended load.
- Provide setup/release choices and appropriate confirmations instead of refusing simply because Subject X is not nearby.
- Show prepared, activated and spent states with matching sound and effects.
- State consequences and one-use behavior must be clear where relevant.
- Replace the toothpick-like plank with substantial wood at a believable angle and scale, with proper contact points.
- Selecting its placement offers Place / Cancel. Cancel leaves it in inventory and changes nothing.
- Update hotspots and remaining pickups to fit altered trap/barricade artwork.

## 22. Hiding, peeking and Clara

- Ask before hiding rather than hiding immediately on object selection.
- The hidden view is dark. Peeking reveals a limited physical opening, such as locker-door slats, with the actual room and enemy positions beyond.
- Provide Stay Hidden / Peek / Exit behavior coherently. Seeing the player enter or prolonged peeking can affect safety under the established rules.
- Remove the awkward floating Clara Whitmore presentation. Convey her security role through functioning recordings, messages and references.
- Preserve discoverable information and transcripts. Do not retain an unresponsive character hotspot or a tiny character scaled below furniture.

## 23. Scripted horror incidents — once per run

General rules:

- Distribute major incidents throughout Chapter 1 rather than concentrating them at the opening.
- Save outcomes, completion and original sanity consequences.
- Revisiting or loading must not replay the event or deduct its original penalty again.
- Persistent real aftermath is different from a later temporary hallucination referencing the memory.

Daniel Mercer:

- He is conscious, restrained and begs to be killed before changing.
- Preserve help / leave / end-suffering choices and the requirements for carrying them out.
- Ending his suffering can use the utility knife, with confirmation. A valid loaded firearm can retain its established option.
- Do not require a firearm when the knife option should work.
- Canceling a confirmation must not silently commit another outcome.
- Once killed, he cannot subsequently be left alive or treated as an unresolved choice.
- Show the covered-body aftermath and save it.
- Later thoughts/hallucinations may reference the decision without repeating it.

Dr. Adrian Kessler:

- Hear repeated impacts before discovering him striking his head against the tiled wall.
- Show appropriate fictional blood, environmental damage and the actual incident.
- Allow approach, speech, inspection or leaving.
- Apply the encounter's sanity consequence once and leave its aftermath.
- Later auditory hallucinations may echo the impacts.

Dr. Edmund Rourke's final room:

- Present his disturbing condition/surroundings and final notes.
- Provide LULLABY evidence and an appropriate one-time sanity response.
- Preserve important documents in Files.

Scientist behind plexiglass:

- Show the scientist attempting to communicate or warn the player.
- An experimental creature attacks and kills him behind the reinforced glass.
- Apply the witnessed event's sanity consequence once.
- Preserve aftermath and allow later investigation of his warning.
- This incident is separate from the optional fatal inspection encounter and from Mimi's later surveillance footage.

## 24. Sanity, hallucinations and changing rooms

- Make sanity a meaningful gameplay system, with a readable mental-condition display.
- Trauma, choices and disturbing discoveries affect perception and thoughts.
- Effects may include whispers, footsteps, changing shadows, reflections, altered room appearance and imagined corpses, hanged bodies or body parts.
- Later disturbances can reference earlier events without replaying the real event or its original consequence.
- Hallucinations are occasional and paced with calm periods. The player should not remain constantly insane or continuously hallucinate.
- Provide appropriate recovery through safety, warmth where relevant, and established grounding/recovery opportunities.
- Avoid endless deterioration and repeated event farming.
- Essential exits, clues and mandatory puzzles remain accessible and solvable.
- Distinguish intentional transient hallucination art from real persistent destruction.
- Real staged changes can include a briefly seen figure followed by its absence, or a bang/shuffling sound leading toward newly destroyed furniture. Save authored event completion and actual damage.

## 25. Required imaginary combat

- Implement actual playable combat with a visible animated infected and normal combat controls, not merely a descriptive choice in a text panel.
- Use the same presentation as a real encounter without a label revealing that it is imaginary.
- Shooting spends real ammunition.
- Apparent attacks may be represented, but cannot permanently reduce real health, cause real death or trigger Game Over.
- The enemy disappears after enough apparent damage or after the episode resolves over time.
- Let the player retreat, wait or observe instead of forcing ammunition expenditure.
- Keep these encounters rare and influenced by sanity/story conditions.
- Once a particular authored episode resolves, save that completion so revisiting/loading cannot repeatedly drain resources or sanity.
- Exact duration, damage threshold and encounter eligibility still require tuning.

## 26. Payphone story in gameplay

- Include multiple physical phones. Some remain silent or disconnected.
- Three important calls occur at three different phones and appropriate progression stages.
- First: Emergency Lobby; answering initially brings silence. That phone never repeats its story call.
- Second: a different phone later; the caller accuses the protagonist of being a murderer.
- Third: a later restricted-area phone; a deeper clue about LULLABY or the protagonist's identity.
- Later phone locations may vary among approved eligible rooms by seed. Preserve essential narrative meaning even if incidental wording/audio varies.
- Calls must actually ring, be answerable and deliver content in gameplay.
- Use convincing mechanical telephone ringing and appropriate interaction feedback.
- Save answered/progression state; each call happens once per run.
- Phone interactions must not reveal unrelated window controls, objects or generic lists.
- Preserve the stable room camera during interaction.

## 27. CRT televisions and surveillance room

- Use believable 1998 CRT televisions and hospital surveillance equipment.
- Selected televisions are off, disconnected or show static under normal conditions.
- During occasional hallucinations, screens can display sinister imagery, unsettling text or subliminal messages related to the story.
- Do not hide indispensable puzzle information in an unreadable flash.
- Fix the reported scan effect moving beyond or past the surveillance screens.
- Clip scan lines, static and distortion inside each screen with correct perspective.
- Anchor screen content to the physical monitor while the player pans.
- Show grainy monochrome views of recognizable game rooms, with fixed surveillance camera viewpoints.
- Reflect relevant real room-state changes; intentional unreliable surveillance must be an authored story effect, not accidental inconsistency.
- Exact choice of prepared images, short loops or other feed rendering remains an implementation detail.

## 28. Required rare one-hit-kill observation encounter

- Include the encounter as Chapter 1 content; its eligible later location/timing may vary.
- A dangerous experimental creature is behind reinforced glass, separate from Subject X and the scientist's death.
- Research clues foreshadow the danger.
- First deliberate inspection gives a strong warning and permits safe retreat.
- A second deliberate inspection, understood as a risk, triggers the fatal attack and Game Over.
- Merely entering, walking past or dismissing the first interaction must not cause an instant kill.
- Keep the fatal outcome avoidable even though inclusion of the encounter is required.
- Provide a nearby save/checkpoint to limit excessive progress loss.
- Use fictional game visuals. Preserve established graphic-violence presentation options where applicable, with consistent gameplay consequences.
- Persist appropriate encounter state and avoid inappropriate repeated surprise kills.

## 29. Easter eggs and references

General direction:

- Include optional recognizable references without making outside franchise knowledge a puzzle requirement.
- Preserve Monolith/LULLABY as the main story and the hospital's 1998 technology/appearance.
- Proposed prop forms below remain subject to fitting the scene; the requested reference targets are recorded.

- **Silent Hill:** a disturbing radio/static detail, mirror detail or note referencing a fog-covered town were suggested.
- **Resident Evil:** period typewriters, medicinal-herb notes or a chessboard were suggested; broader puzzle/combat inspiration is recorded separately.
- **Umbrella:** a red-and-white umbrella or subtle supplier reference was suggested.
- **Twisted Metal:** a battered toy ice-cream truck with sinister clown decoration in the Children's Ward was suggested.
- **The Sopranos:** the user requested a more obvious reference. Proposed inspectable Satriale's Pork Store bag in the staff lounge, with the original note text: 'Tony, your gabagool's in the fridge. —Paulie'.
- **Dead Space:** wall graffiti reading MAKE US WHOLE with a rough Marker-like sketch in a maintenance/restricted corridor was proposed.

## 30. Nurse Mimi: Chapter 1 foreshadowing and Chapter 2 story

Established character:

- Known as Crazed Nurse Mimi / Sinister Nurse Mimi.
- Young blonde nurse with glasses, a sinister smile and a distinctive creepy laugh.
- Her real name is redacted everywhere. Personal notes refer to her as Nurse Mimi or Mimi.
- Former nurse experimented on by Monolith Pharmaceuticals, leaving her infected, insane and sadistic.
- Intelligent, unpredictable, cruel and obsessed with treating victims as her patients.
- Her real identity and the full truth about the experiments remain hidden. Do not invent an unredacted name.

Chapter 1 references:

- Scatter appropriate documents, notes and records mentioning her before the player meets her.
- Use redacted identity fields and nickname references consistently.
- Suggested document forms include personnel/experiment records and private handwritten notes, with final wording based on her established story.
- Build unease without explicitly revealing her entire trust/betrayal sequence before Chapter 2.
- Do not automatically equate the earlier generic missing-nurse mystery with Mimi unless deliberately established in the story.

Chapter 2 sequence, recorded for continuity rather than current development:

1. First encounter: friendly, offers medical supplies, does not attack.
2. Surveillance discovery: disturbing fictional game footage shows her sawing off a patient's head.
3. Second encounter: pretends to help, then unexpectedly stabs the player, leaving them injured.
4. Stalking: hunts through the underground laboratories, laughing, taunting and manipulating the player.
5. Chapter ending: the player temporarily traps her in a containment chamber. She hints that they have met before.

- Core progression: trust, discovery, betrayal, pursuit.
- Do not confuse this footage or stalking role with the Chapter 1 scientist incident or Subject X.
- Complete Chapter 1 before implementing Chapter 2's playable sequence.

## 31. Visual production checklist for future implementation

- Corrected reference-based UI, map and lower action controls.
- Unique room panoramas and coherent entrance/door artwork.
- Independent prop layers, seeded placements and removed-item states.
- High-resolution object close-ups and relevant reverse sides.
- Drawer/cabinet/locker interiors and open/empty states.
- Complete item icons, including lighter and fluid PNGs.
- Readable handwritten/typed document art with weathering and redactions.
- Wiring/tuning/equipment puzzle views and feedback states.
- Generator-off, emergency-power, generator-on and temporary-blackout lighting.
- Outdoor snow, open/closed windows, shutters and localized entering flurries.
- Sprinkler action, valve, dropped flashlight and wet/water-off aftermath.
- Chosen warming interaction and its active/inactive visual states.
- Bloody, torn-clothing infected with animated reactions, knockdowns and deaths.
- Bulkier Subject X with weighty movement and appropriate shadows.
- Trap armed/spent art and properly scaled plank placement.
- Kessler action/aftermath, Mercer covered body, Rourke evidence and scientist-glass incident.
- Temporary hallucinated room/body layers and imaginary-enemy encounters.
- Period CRT screens, perspective-correct scan effects and hospital camera views.
- Door-opening transitions matched to actual routes.
- Easter egg props/graffiti and Mimi's redacted Chapter 1 documents.
- Mimi's full character/encounter visuals belong to later Chapter 2 work, not the present chapter scope.

## 32. Verification and acceptance requirements

- Review every room's art, orientation, routes, hotspots and changed states, including panoramic extremes and supported screen sizes.
- Confirm that all doors/map edges agree and intermediate rooms cannot be bypassed accidentally.
- Verify actual controls in every view; no flashlight-toggle workaround for a broken scene.
- Check all Take / Leave, inspect/flip, container and item-icon behaviors.
- Confirm that pickups disappear and completed inspections are handled without losing clues.
- Validate progression over multiple generated seeds, including lock/key dependencies, matching puzzle clues, early lighter/fluid access and all elevator components.
- Verify that required gameplay sequences actually occur, rather than existing only as text in notes.
- Check actual audio playback, noise response, directionality and finite enemy persistence.
- Confirm that living survivors recover appropriately and defeated infected do not respawn.
- Confirm Subject X's second-half introduction, connected pursuit, stagger, hiding and paced downtime.
- Verify cold/sprinkler recovery and their once-per-run completion through revisits and saves.
- Confirm Mercer/Kessler/scientist completion and original sanity penalties never repeat in the same run.
- Verify imaginary combat consumes ammunition but never causes real death/permanent health loss.
- Verify all three calls, CRT boundaries and surveillance state consistency.
- Test the fatal observation encounter's warning, safe retreat and deliberate second trigger.
- Complete the full Chapter 1 route to the elevator and preserve existing offline/delivery behavior.
- Distinguish automated checks from actual human visual/audio playtesting. Do not claim tests, assets or gameplay are completed merely because they are listed here.

## 33. Remaining design choices

- Exact panoramic turning range, controls and visual implementation.
- Final opening-scene artwork and exact door-transition presentation/timing.
- Seed placement pools and clue wording after route validation.
- Shape/theme of the four elevator fuses.
- Flashlight drain, battery refill amounts and charging balance per difficulty.
- Cold warning duration, health/sanity rates, recovery speed and handling penalties.
- Lighter fuel capacity, refill amounts, final warming interaction and additional use.
- Enemy populations, hearing ranges, investigation duration and screaming/singing pacing.
- Hallucination eligibility, intervals and imaginary-combat thresholds/duration.
- Exact Easter egg props and final document texts, including Mimi's foreshadowing.

These choices remain open for later design/implementation. They do not require starting a build now.
