"""Build original quiet hospital ambience, breath foley and the item pickup cue.

This is offline sound design, not a runtime synthesizer. No voice or third-party
game samples are used. NumPy/SciPy and ffmpeg are build-only dependencies.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import tempfile

import numpy as np
from scipy import signal
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audio' / 'chapter1'
RATE = 44100
RNG = np.random.default_rng(19980917)


def band_noise(count, lo, hi):
    white = RNG.standard_normal(count)
    filtered = signal.sosfilt(signal.butter(3, [lo, hi], fs=RATE, btype='band', output='sos'), white)
    return filtered / max(np.sqrt(np.mean(filtered ** 2)), 1e-8)


def loop_noise(count, lo, hi):
    # Overlap/crossfade ends so an HTML loop has no cut or audible seam.
    overlap = RATE * 2
    raw = band_noise(count + overlap, lo, hi)
    phase = np.linspace(0, np.pi / 2, overlap, endpoint=False)
    raw[:overlap] = raw[:overlap] * np.sin(phase) + raw[count:] * np.cos(phase)
    return raw[:count]


def breathing(periods, inhale_share, intensity, seed):
    """Close, unvoiced air foley with a different airway on each breath.

    A repeated single band of noise under a sine envelope sounds like a pump.
    Here nasal inhalation and warmer mouth exhalation have separate resonances,
    asymmetric flow, irregular turbulence and changing pauses. There is no
    pitched throat oscillator, so strain cannot turn into repeated pain grunts.
    """
    rng = np.random.default_rng(seed)
    count = int(sum(periods) * RATE)
    result = np.zeros(count)

    def air(length, low, high):
        raw = rng.standard_normal(length)
        filtered = signal.sosfilt(signal.butter(2, [low, high], fs=RATE,
                                               btype='band', output='sos'), raw)
        return filtered / max(np.sqrt(np.mean(filtered ** 2)), 1e-8)

    def resonant(values, frequency, width):
        b, a = signal.iirpeak(frequency, width, fs=RATE)
        shaped = signal.lfilter(b, a, values)
        return shaped / max(np.sqrt(np.mean(shaped ** 2)), 1e-8)

    def flow(length, inhaling):
        u = np.linspace(0, 1, length)
        # Inhalation builds through the nose; exhalation arrives sooner and
        # decays more slowly. Both include small non-rhythmic fluctuations.
        knots = [0, .12, .30, .61, .84, 1] if inhaling else [0, .075, .24, .57, .82, 1]
        levels = [0, .36, .85, 1, .64, 0] if inhaling else [0, .82, 1, .70, .26, 0]
        levels = np.array(levels) * rng.uniform(.91, 1.09, len(levels))
        envelope = np.interp(u, knots, levels)
        envelope = signal.sosfilt(signal.butter(2, 16, fs=RATE, output='sos'), envelope)
        flutter = np.interp(u, np.linspace(0, 1, max(5, length // 4200)),
                            rng.uniform(.80, 1.14, max(5, length // 4200)))
        envelope *= flutter
        fade = min(int(.055 * RATE), length // 5)
        envelope[:fade] *= np.linspace(0, 1, fade) ** 1.5
        envelope[-fade:] *= np.linspace(1, 0, fade) ** 1.5

        if inhaling:
            source = air(length, 190, rng.uniform(4800, 5700))
            nasal = resonant(source, rng.uniform(1050, 1350), 1.15)
            high = resonant(source, rng.uniform(2450, 2900), .75)
            colour = .44 * source + .43 * nasal + .13 * high
        else:
            source = air(length, 110, rng.uniform(2500, 3300))
            warm = resonant(source, rng.uniform(420, 560), .85)
            mouth = resonant(source, rng.uniform(940, 1180), 1.0)
            colour = .43 * source + .40 * warm + .17 * mouth
        # Broad spectral drift follows the changing airway opening rather
        # than a steady hiss. Avoid a repeated low-frequency thump.
        colour = signal.sosfilt(signal.butter(2, 100, fs=RATE,
                                              btype='highpass', output='sos'), colour)
        return colour * envelope

    cursor = 0
    for cycle in periods:
        length = min(int(cycle * RATE), count - cursor)
        inhale_start = int(length * rng.uniform(.035, .060))
        inhale_end = int(length * (inhale_share + rng.uniform(-.025, .025)))
        exhale_start = inhale_end + int(length * rng.uniform(.035, .065))
        exhale_end = int(length * rng.uniform(.77, .83))
        inhale = flow(inhale_end - inhale_start, True)
        exhale = flow(exhale_end - exhale_start, False)
        depth = rng.uniform(.83, 1.12)
        result[cursor + inhale_start:cursor + inhale_end] += inhale * .64 * depth
        result[cursor + exhale_start:cursor + exhale_end] += exhale * .84 * depth
        cursor += length
    return result * intensity


def room_hum(seconds, machinery=False):
    count = int(seconds * RATE)
    t = np.arange(count) / RATE
    # Quiet transformer/fan bed. All harmonic frequencies fit the loop length.
    bed = sum(np.sin(2 * np.pi * f * t + phase) * amount for f, phase, amount in [(50, 0, .25), (100, .65, .08), (150, 1.4, .035)])
    air = loop_noise(count, 65 if machinery else 90, 550 if machinery else 360)
    slow = 1 + .035 * np.sin(2 * np.pi * t / seconds)
    return (bed + air * (.16 if machinery else .055)) * slow * (.21 if machinery else .12)


def winter_wind(seconds):
    count = int(seconds * RATE)
    t = np.arange(count) / RATE
    air = loop_noise(count, 75, 1700)
    gust = .73 + .13 * np.sin(2 * np.pi * t / seconds + .4) + .08 * np.sin(2 * np.pi * 3 * t / seconds)
    return air * gust * .10


def pickup():
    count = int(.46 * RATE)
    t = np.arange(count) / RATE
    # An original short two-note wooden/metallic selection cue, reminiscent of
    # the restrained interfaces of the era, without sampling another game.
    result = np.zeros(count)
    for start, frequency, level in [(0, 622.25, .12), (.075, 830.61, .085)]:
        u = t - start
        env = np.where(u >= 0, np.minimum(np.maximum(u, 0) / .008, 1) * np.exp(-np.maximum(u, 0) * 19), 0)
        result += level * env * (np.sin(2 * np.pi * frequency * u) + .17 * np.sin(2 * np.pi * frequency * 2.01 * u))
    result += band_noise(count, 700, 5200) * np.exp(-t * 70) * .006
    result *= np.minimum(t / .003, 1) * np.minimum((.46 - t) / .03, 1)
    return result


def cloth():
    count = int(.38 * RATE)
    t = np.arange(count) / RATE
    return band_noise(count, 300, 4800) * np.sin(np.pi * t / .38) ** 2 * .028


DESIGNS = {
    'breath_calm': (lambda: breathing([5.7, 6.1, 5.4, 5.9, 6.3, 5.6, 6.0, 5.5, 6.2, 5.8, 5.3, 6.0], .35, .043, 461998), 'Twelve quiet irregular 5.3–6.3 second close-air cycles: nasal inhale, warmer mouth exhale, asymmetric airflow and changing rests. No voice/grunt recording.'),
    'breath_caution': (lambda: breathing([3.8, 4.1, 3.6, 3.9, 4.2, 3.7, 4.0, 3.5, 3.8, 4.15, 3.65, 3.95], .36, .073, 471998), 'Twelve moderately paced irregular 3.5–4.2 second cycles with independent inhale/exhale resonances and breathing depth.'),
    'breath_danger': (lambda: breathing([2.9, 2.65, 3.05, 2.8, 3.1, 2.7, 2.95, 2.6, 2.85, 3.0, 2.75, 2.9], .38, .105, 481998), 'Twelve strained irregular 2.6–3.1 second cycles: audible close breath with short rests, no voiced groans or pain syllables.'),
    'hospital_hum': (lambda: room_hum(40), 'Quiet 40 second transformer/ventilation bed with crossfaded air and steady 50 Hz mains harmonics.'),
    'hospital_machine': (lambda: room_hum(40, True), '40 second fuller low machine/ventilation bed, no recurrent impacts or rattles.'),
    'exterior_wind': (lambda: winter_wind(36), '36 second crossfaded low winter wind with slow broad gusts, no rhythmic percussive loop.'),
    'pickup_chime': (pickup, 'Original 460 ms soft two-note item confirmation cue, no bottle/dishes recording or game sample.'),
    'cloth_soft': (cloth, 'Original 380 ms filtered-air cloth handling foley, without glass clinks.'),
}


def main():
    # Keep the established ambience/pickup random stream byte-for-byte stable.
    # The earlier four-cycle breath designs consumed this much random air;
    # the new breath designs use their own independent seeds above.
    global RNG
    RNG = np.random.default_rng(19980917)
    old_breath_periods = [[6.4, 6.7, 6.2, 6.6], [4.5, 4.3, 4.7, 4.4],
                         [3.0, 2.8, 3.15, 2.95]]
    RNG.standard_normal(sum(2 * int(sum(periods) * RATE)
                            for periods in old_breath_periods))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('names', nargs='*', help='Optional asset names; leave other bundled audio untouched.')
    selected = set(parser.parse_args().names or DESIGNS)
    if selected - DESIGNS.keys():
        parser.error('Unknown audio design: ' + ', '.join(sorted(selected - DESIGNS.keys())))
    OUT.mkdir(parents=True, exist_ok=True)
    metadata = ROOT / 'audio' / 'ORIGINAL_AUDIO.json'
    previous = json.loads(metadata.read_text())['files'] if metadata.exists() else []
    manifest = {item['file']: item for item in previous}
    with tempfile.TemporaryDirectory(prefix='ward-audio-', dir='/tmp') as temporary:
        for name, (make, design) in DESIGNS.items():
            samples = np.clip(make(), -.8, .8)
            if name not in selected:
                continue
            source = Path(temporary) / (name + '.wav')
            wavfile.write(source, RATE, (samples * 32767).astype(np.int16))
            target = OUT / (name + '.ogg')
            subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(source), '-c:a', 'libvorbis', '-q:a', '5', '-fflags', '+bitexact', '-flags:a', '+bitexact', str(target)], check=True)
            manifest['chapter1/' + target.name] = {'file': 'chapter1/' + target.name, 'design': design, 'seconds': len(samples) / RATE, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'rms': float(np.sqrt(np.mean(samples ** 2)))}
            print(name, round(len(samples) / RATE, 3), 'seconds')
    (ROOT / 'audio' / 'ORIGINAL_AUDIO.json').write_text(json.dumps({'origin': 'Original offline sound design for The Last Ward. No voice recordings, copyrighted game audio or third-party samples.', 'generator': 'tools/prepare_review_audio.py', 'seed': 19980917, 'sample_rate': RATE, 'files': [manifest['chapter1/' + name + '.ogg'] for name in DESIGNS if 'chapter1/' + name + '.ogg' in manifest]}, indent=2) + '\n')


if __name__ == '__main__':
    main()
