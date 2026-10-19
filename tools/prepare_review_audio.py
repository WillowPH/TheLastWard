"""Build original quiet hospital ambience, breath foley and the item pickup cue.

This is offline sound design, not a runtime synthesizer. No voice or third-party
game samples are used. NumPy/SciPy and ffmpeg are build-only dependencies.
"""
from pathlib import Path
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


def breathing(periods, inhale_share, intensity):
    # Breath is shaped air, without a voiced/grunted fundamental. Each cycle
    # includes separate inhale/exhale and a silent rest, with slight variation.
    count = int(sum(periods) * RATE)
    air = band_noise(count, 260, 4600)
    low_air = band_noise(count, 120, 1300)
    result = np.zeros(count)
    cursor = 0
    for cycle in periods:
        length = int(cycle * RATE)
        if cursor + length > count:
            length = count - cursor
        duration = length / RATE
        local = np.arange(length) / RATE
        inhale_end = duration * inhale_share
        exhale_start = inhale_end + duration * .075
        exhale_end = duration * .87
        envelope = np.zeros(length)
        inhale = (local > duration * .06) & (local < inhale_end)
        envelope[inhale] = .60 * np.sin(np.pi * (local[inhale] - duration * .06) / (inhale_end - duration * .06)) ** 1.7
        exhale = (local > exhale_start) & (local < exhale_end)
        envelope[exhale] = .88 * np.sin(np.pi * (local[exhale] - exhale_start) / (exhale_end - exhale_start)) ** 1.5
        result[cursor:cursor + length] = envelope * (air[cursor:cursor + length] * .78 + low_air[cursor:cursor + length] * .22)
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
    'breath_calm': (lambda: breathing([6.4, 6.7, 6.2, 6.6], .37, .075), 'Four quiet 6.2–6.7 second shaped-air breath cycles, no voice/grunt recording.'),
    'breath_caution': (lambda: breathing([4.5, 4.3, 4.7, 4.4], .38, .095), 'Four moderately paced 4.3–4.7 second shaped-air breath cycles.'),
    'breath_danger': (lambda: breathing([3.0, 2.8, 3.15, 2.95], .40, .125), 'Four strained 2.8–3.15 second shaped-air breath cycles; no repeated pain vocalization.'),
    'hospital_hum': (lambda: room_hum(40), 'Quiet 40 second transformer/ventilation bed with crossfaded air and steady 50 Hz mains harmonics.'),
    'hospital_machine': (lambda: room_hum(40, True), '40 second fuller low machine/ventilation bed, no recurrent impacts or rattles.'),
    'exterior_wind': (lambda: winter_wind(36), '36 second crossfaded low winter wind with slow broad gusts, no rhythmic percussive loop.'),
    'pickup_chime': (pickup, 'Original 460 ms soft two-note item confirmation cue, no bottle/dishes recording or game sample.'),
    'cloth_soft': (cloth, 'Original 380 ms filtered-air cloth handling foley, without glass clinks.'),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    with tempfile.TemporaryDirectory(prefix='ward-audio-', dir='/tmp') as temporary:
        for name, (make, design) in DESIGNS.items():
            samples = np.clip(make(), -.8, .8)
            source = Path(temporary) / (name + '.wav')
            wavfile.write(source, RATE, (samples * 32767).astype(np.int16))
            target = OUT / (name + '.ogg')
            subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', str(source), '-c:a', 'libvorbis', '-q:a', '5', str(target)], check=True)
            manifest.append({'file': 'chapter1/' + target.name, 'design': design, 'seconds': len(samples) / RATE, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'rms': float(np.sqrt(np.mean(samples ** 2)))})
            print(name, round(len(samples) / RATE, 3), 'seconds')
    (ROOT / 'audio' / 'ORIGINAL_AUDIO.json').write_text(json.dumps({'origin': 'Original offline sound design for The Last Ward. No voice recordings, copyrighted game audio or third-party samples.', 'generator': 'tools/prepare_review_audio.py', 'seed': 19980917, 'sample_rate': RATE, 'files': manifest}, indent=2) + '\n')


if __name__ == '__main__':
    main()
