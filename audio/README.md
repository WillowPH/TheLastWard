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

The active condition layer uses original muffled heartbeat foley instead of the
previous air-breath beds. Healthy exploration is quiet apart from the room's
ambience. An immediate visible threat adds a short four-beat fear response with
an extended rest; low sanity alone does not create a permanent sound bed.
Caution uses six gentle paired pulses at 76 BPM followed by 4.1 seconds of quiet.
Danger uses twelve deeper pairs at 98 BPM and a 2.7-second recovery interval.
These are restrained condition cues, not repeated hurt sounds or an endless
respiratory hiss. They are generated game sound design, not human recordings.

Opening a paper or object inspection quiets the pulse while the room ambience
continues. Changes in condition release the outgoing pulse over 180 ms; Pause
freezes the release and all playback positions. Existing air-breath assets remain
for source history but are never selected by the active sound bus.

Original 36–40 second wind, transformer and ventilation beds replace the short
repeating room loops. A quiet 460 ms original two-note pickup cue replaces the
dishes/bottle-like pickup sample; heal/combine use soft cloth foley. These are
project sound design generated offline; they contain no game samples or voice
recordings. `ORIGINAL_AUDIO.json` records design, duration and output hashes.
The old creature and dishes clips remain for source history but are not selected
by the Chapter 1 audio bus.

Regenerate only the new heartbeat assets with:

```sh
python tools/prepare_review_audio.py heartbeat_stress heartbeat_caution heartbeat_danger
```

Omit names to regenerate all original designs, including historical unused breath
files. Selecting names preserves other sound files and their provenance. Encoding
is deterministic; the game needs neither NumPy, SciPy nor FFmpeg at runtime.

The runtime only plays local files. It does not synthesize sounds or fallback
bleeps. Pause and background-tab handling stop every playing channel at its current
position and resume it once. Re-rendering the scene never creates extra pulse or
ambience loops.

Regenerate with `python tools/prepare_audio.py /path/to/that/source/checkout`.
The game itself needs neither the source checkout nor FFmpeg. Volume controls separate
ambience, effects and interface. Important sounds also have optional text captions.
