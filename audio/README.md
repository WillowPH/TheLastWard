# Chapter 1 recorded audio

The active audio bus uses 26 bundled OGG recordings/derivatives in `chapter1/`.
The original three WAV effects remain in source history but are not the active bus.

Source: https://github.com/lavenderdotpet/CC0-Public-Domain-Sounds
License: CC0 1.0, included in CC0-LICENSE.txt. SOURCES.json records the pinned source
commit, original filenames, original/output SHA-256 hashes and FFmpeg processing.
The selected files come from the 100 CC0 SFX, foley, loop and Warfork CC0 collections.

The phone is sampled mechanical bell foley sequenced into a telephone cadence. The
Subject X boots use recorded metal footfalls with pitch/EQ processing. The recordings
are normalized/encoded locally; the game does not synthesize oscillators or fallback
beeps. There are no voice-acted NPC dialogue recordings.

Regenerate with `python tools/prepare_audio.py /path/to/that/source/checkout`.
The game itself needs neither the source checkout nor FFmpeg. Volume controls separate
ambience, effects and interface. Important sounds also have optional text captions.
