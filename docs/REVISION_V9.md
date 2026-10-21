# Chapter 1 character, supply and outcome review — v9

Build `last-ward-ch1-chapter-review-9`, 21 October 2026.

Subject X is now a massive scarred institutional patient with a visible face and
torn clothing, following the requested Outlast reference. Standing and kneeling are
separate authored transparent sprites. The down pose has bent anatomy and grounded
contact; no upright sprite is squeezed, rotated or reused as a fall. Knockdown,
recovery, blocking, finite ammunition and difficulty thresholds remain mechanical
states rather than changes to sprite proportions.

Kessler’s infected aftermath has a visibly uncovered, mottled face, cloudy eyes,
contorted jaw and attached rigid hands. Local shoulder/head movement is limited to
small feathered native patches; room geometry stays fixed. Speak, watch, approach
and leave have distinct saved descriptions, evidence and consequences.

Mercer’s treatment consumes a dressing, stabilizes him and yields a practical
warning. Leaving allows an eighteen-turn window to return with treatment. A later
return shows a once-only restrained transformation: keep distance, explicitly risk
injury securing the strap, or choose mercy. No roaming enemy is spawned repeatedly.
Stabilized, transformed, resecured and dead outcomes have distinct paintings; mercy
remains covered and irreversible. A persistent bedside record preserves chronology.

## Finite supplies and useful rear views

| Guaranteed fresh-run supplies | Story | Normal | Nightmare |
| --- | ---: | ---: | ---: |
| Flashlight cells | 4 | 3 | 2 |
| Floppy Disks | 8 | 6 | 4 |
| Trauma Dressings | 5 | 4 | 3 |
| Field Medkits | 3 | 2 | 2 |
| Total available healing | 235 HP | 170 HP | 150 HP |

Helping Mercer uses one 20-HP dressing. Early ward care and later Observation care
bridge different encounter stretches. Battery, save and medical jackpots no longer
depend on a random shelf roll. Ammunition keeps its finite authored budget and
optional seed bonus. Generator charging has one 65% reserve; the slow, nearly-empty
12% dynamo remains an emergency fallback with its cooldown.

The fixed hospital layout now has useful rear objects in 25 of 27 rooms. Added
targets match painted trolleys, a treatment chart cabinet and a vestry cabinet;
passage-only rear views remain clear. The reception rear counter has discoverable
save disks. Existing object IDs retain collected states across continued saves.

A filled lighter has exactly two useful ignitions: laundry stove and chapel candles.
Legacy fuel normalizes from actual completed ignition flags. Normal/Story retain
automatic removal after both permanent uses; Nightmare retains manual disposal.

Every carried item can be discarded with confirmation. Discard explicitly leaves
it in the current room; a local recovery action is available there. Loaded weapon
rounds, flashlight charge and drops persist without duplication. Dropped equipment
cannot be remotely retrieved through a shared Storage box.

## Weather, memories and online preference

Snow is visibly sized and moving at fitted desktop, tablet and mobile scales, with
75 reviewed glass cells across eight exterior views. Four missing Lobby panes now
receive weather. Room 12 and Isolation have moon-free winter plates composited only
through the existing glass masks. Shutters suppress covered panes. Motion settings
can stop and restart the frame loop; Pause preserves exact effect state. Fire,
sprinklers, lights, monochrome CRT feeds and patient motion have focused checks.

The floating white shroud and hook representation is retired. Brief grounded
infected memories require an actual witnessed incident and UNEASY sanity, with
contextual Thoughts. High sanity and unearned low sanity do not trigger them. The
two-vision cap, quiet intervals and one nonlethal imaginary fight remain saved.

The Umbrella reference is a small red-and-white segmented supplier badge and dossier
in the rear Staff Lounge. The large umbrella inspection picture and Lobby placement
are replaced.

Online preferred is now the default and actually checks host capability metadata.
A connected host can supply a faint, same-origin ceiling texture; authored room
artwork and targets remain unchanged. The native download advertises no provider
and clearly labels its local fallback. Offline makes no artwork-service requests;
pending requests are cancelled, and stale responses cannot start downloads or
overwrite the current room. The optional gateway serializes matching generation
requests and publishes complete cached images atomically. Provider tests use local
mocks; no live paid service is configured or claimed.

## General fixes and compatibility

Reading freezes and rebases actual pursuit, vision and blackout deadlines, including
overlapping Pause without double-counting. New Game clears stale finale checkpoints;
Continue preserves saved progress. Recognized v5–v8 records remain loadable, including
actual v8 Terminal records. New supply plans do not refill already collected objects
or used chargers. A new run exposes the complete revised distribution and outcomes.

See [validation](../VALIDATION.md) for executed scenarios and practical limits.
