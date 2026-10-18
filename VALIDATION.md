# Chapter 1 multi-file validation — 18 October 2026

System Chromium, Python Playwright, service workers blocked. These are functional
browser checks, not a claim that artwork or first-time player pacing is perfect.

## Ordinary input and presentation

`python tests/test_review_interactions.py`

Eleven focused checks: Options-only Subtle/Strong markers, no Turn Around UI,
ordinary item clicks without camera movement, bounded 64px note artwork,
completed portraits, phone completion through save/reload, local dead-line feedback
and real-call reactivation, separate gun/negative icons, right-HUD flashlight toggle,
continuous full-circle look, one-click adjacent map travel, actual animated snow and
lamp dimming, and HUD bounds at 1672, 1000 and 390 pixels wide.

## Earned progression

`python tests/test_winter_playthrough.py [server URL]`

Two routes, Normal and Story, earn required keys, evidence, generator wiring,
incident decisions, Subject X progression and the four-fuse interlock before the
explicit Chapter 1 elevator ending. Both visit all 27 rooms. QA view/reveal helpers
are used to locate authored targets in this long route test; ordinary-click camera
behavior is tested independently above. No inventory/progression unlock injection
is used to bypass the route.

## Focused systems

`python tests/test_winter_systems.py`

Seventeen checks cover measured audio output, battery drain/exhaustion, traps,
hiding, image identity, cold windows/recovery, sprinkler/flashlight recovery,
plank confirmation, Mercer knife decision persistence, finite enemy/noise behavior,
nonlethal imaginary combat, three once-only phone calls, warned lethal encounter,
photo reverses, all directed arrival orientations, 128 seeded placement sets,
all icons and distinct front art at desktop/tablet/mobile sizes.

## Actual extracted package

`python tools/package_build.py downloads`

`python tests/test_winter_package.py`

The ZIP is extracted into a fresh directory and its own Python launcher starts it.
External requests are blocked while local file requests remain enabled. Checks load
all 27 rooms' four views, handwriting fonts and measured separate audio output.
The complete earned routes also run against an extracted-project launcher.
The archive contains separate source, assets, audio, data and launch instructions.
Direct file:// navigation is blocked by this environment's Chromium policy; use
the included Python launcher. No external internet is required for play.

## Visual review and limits

Reviewed front/rear contact sheets and all 27 side atlases. Corrected reported
North corridor, Mercer and Children targets; added Room 12's second visible route,
blocked unused doors, and barricaded the Lobby exterior exit. Snow remains clipped
to authored glazing and CRT scans remain inside screens. The panoramic camera is
four connected authored views at a fixed position, not a modeled 3D environment;
some joins remain visible. Background motion uses animated layers, not full video.
Automated checks cannot guarantee ideal first-time puzzle pacing or every art detail.
