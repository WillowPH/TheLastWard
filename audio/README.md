# Chapter 1 audio

The active audio bus uses bundled OGG recordings/derivatives and original project
sound design in `chapter1/`.
The original three WAV effects remain in source history but are not the active bus.

Source: https://github.com/lavenderdotpet/CC0-Public-Domain-Sounds
License: CC0 1.0, included in CC0-LICENSE.txt. SOURCES.json records the pinned source
commit, original filenames, original/output SHA-256 hashes and FFmpeg processing.
The selected files come from the 100 CC0 SFX, foley, loop and Warfork CC0 collections.

The phone is sampled mechanical bell foley sequenced into a telephone cadence. The
Subject X boots use recorded metal footfalls with pitch/EQ processing. The recordings
are normalized/encoded locally. There are no voice-acted NPC dialogue recordings.

The review pass replaces the old creature `breathing.ogg` with three original
air-breath beds: calm, caution and danger. These contain inhale/exhale/rest cycles
without grunts, and only health selects their pace. Original 36–40 second wind,
transformer and ventilation beds replace the short repeating room loops. A quiet
460 ms original two-note pickup cue replaces the dishes/bottle-like pickup sample;
heal/combine use soft cloth foley. These are project sound design generated offline
with `python tools/prepare_review_audio.py`; they contain no game samples or voice
recordings. `ORIGINAL_AUDIO.json` records their design, duration and output hashes.
The old creature and dishes clips remain for source history but are not selected
by the Chapter 1 audio bus.

The runtime only plays local files. It does not synthesize sounds or fallback
bleeps. Pause and background-tab handling stop every playing channel at its current
position and resume it once. Re-rendering the scene never creates extra breath or
ambience loops.

Regenerate with `python tools/prepare_audio.py /path/to/that/source/checkout`.
The game itself needs neither the source checkout nor FFmpeg. Volume controls separate
ambience, effects and interface. Important sounds also have optional text captions.
