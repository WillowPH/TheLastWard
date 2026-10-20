"""Measured local heartbeat playback, health/threat routing and pause continuity."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import numpy as np
from scipy.signal import find_peaks
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
checks, errors = [], []


def passed(label):
    checks.append(label)
    print('PASS', label, flush=True)


manifest = json.loads((ROOT / 'audio' / 'ORIGINAL_AUDIO.json').read_text())
decoded = {}
for item in manifest['files']:
    file = ROOT / 'audio' / item['file']
    assert hashlib.sha256(file.read_bytes()).hexdigest() == item['sha256'], file
    raw = subprocess.check_output(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', str(file), '-f', 'f32le', '-ar', '44100', '-ac', '1', '-'])
    samples = np.frombuffer(raw, dtype=np.float32)
    assert abs(len(samples) / 44100 - item['seconds']) < .03, file
    assert .005 < np.sqrt(np.mean(samples ** 2)) < .13, file
    assert np.max(np.abs(samples)) < .8, file
    decoded[file.stem] = samples
for name, beats in [('heartbeat_stress', 4), ('heartbeat_caution', 6), ('heartbeat_danger', 12)]:
    values = decoded[name]
    assert np.max(np.abs(values[:400])) < .001 and np.max(np.abs(values[-44100:])) < .001, name
    frames = values[:len(values) // 441 * 441].reshape(-1, 441)
    envelope = np.sqrt(np.mean(frames ** 2, axis=1))
    peaks, _ = find_peaks(envelope, distance=9, prominence=.006)
    assert len(peaks) == beats * 2, (name, len(peaks), peaks)
    assert (envelope < .001).mean() > .45, name
    power = np.abs(np.fft.rfft(values)) ** 2
    frequencies = np.fft.rfftfreq(len(values), 1 / 44100)
    assert power[frequencies < 300].sum() / power.sum() > .985, name
assert np.sqrt(np.mean(decoded['heartbeat_stress'] ** 2)) < np.sqrt(np.mean(decoded['heartbeat_caution'] ** 2)) < np.sqrt(np.mean(decoded['heartbeat_danger'] ** 2))
passed('all 11 original assets decode and match provenance; new pulse beds have distinct soft lub-dub pairs, low-frequency body, long real rests and no clipping')

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1600, 'height': 1000}, service_workers='block')
    page = context.new_page()
    page.set_default_timeout(10000)
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(URL)
    page.get_by_role('button', name='BEGIN INVESTIGATION', exact=True).click()
    ev = page.evaluate
    ev('nextIntro();nextIntro();nextIntro();S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.phoneRinging=false;S.hp=100;S.san=100;S.f.introComplete=1;WardSound.stop();initAudio();WardSound.sync()')
    page.wait_for_function("WardSound.context().state==='running'&&WardSound.snapshot().filter(a=>a.loop).every(a=>a.ready>=3&&a.time>.1)")
    assert not ev("WardSound.snapshot().some(a=>a.channel==='pulse'||a.clip.startsWith('breath'))")
    assert ev("WardSound.snapshot().some(a=>a.clip==='hospital_hum')")
    energies = []
    for _ in range(8):
        page.wait_for_timeout(90)
        energies.append(ev('WardSound.energy()'))
    assert max(energies) > .00001, energies
    passed('healthy exploration produces room ambience without any constant breathing or heartbeat loop')

    ev('S.room="ward";S.pursuer.active=true;S.pursuer.room=S.room;WardSound.sync()')
    page.wait_for_function("WardSound.snapshot().some(a=>a.channel==='pulse'&&a.clip==='heartbeat_stress'&&a.ready>=3&&!a.paused)")
    ev('S.pursuer.active=false;S.room="lobby";WardSound.sync()')
    page.wait_for_function("!WardSound.snapshot().some(a=>a.channel?.startsWith('pulse'))")
    passed('an immediate live threat adds a brief fear pulse; leaving the threat returns healthy exploration to quiet ambience')

    for hp, name in [(76, None), (75, 'heartbeat_caution'), (26, 'heartbeat_caution'), (25, 'heartbeat_danger')]:
        ev('hp=>{S.hp=hp;S.san=10;WardSound.sync()}', hp)
        if name:
            page.wait_for_function('(name)=>WardSound.snapshot().some(a=>a.clip===name&&a.channel==="pulse"&&a.ready>=3&&!a.paused)', arg=name)
        else:
            assert not ev("WardSound.snapshot().some(a=>a.channel==='pulse')")
        assert ev("WardSound.snapshot().filter(a=>a.channel==='pulse').map(a=>a.clip)") == ([name] if name else [])
    before = ev('WardSound.history.length')
    ev('for(let i=0;i<100;i++)WardSound.sync()')
    assert ev('WardSound.history.length') == before
    assert not ev("WardSound.snapshot().some(a=>a.clip.startsWith('breath')||a.clip==='impact')")
    passed('condition boundaries select only caution/danger pulses; low sanity alone never adds a breathing/grunt bed, and repeated syncs do not duplicate channels')

    page.wait_for_function("!WardSound.snapshot().some(a=>a.channel==='pulse-release')")
    ev("WardSound.pauseAll('manual')")
    snapshot = ev('WardSound.snapshot()')
    page.wait_for_timeout(800)
    after = ev('WardSound.snapshot()')
    assert len(snapshot) == len(after) and all(a['paused'] for a in after), after
    assert all(abs(a['time'] - b['time']) < .025 for a, b in zip(snapshot, after)), (snapshot, after)
    assert ev("WardSound.play('gunshot')") is None
    ev("WardSound.pauseAll('visibility');WardSound.resumeAll('visibility')")
    assert ev('WardSound.snapshot().every(a=>a.paused)')
    ev("WardSound.resumeAll('manual')")
    page.wait_for_timeout(500)
    resumed = ev('WardSound.snapshot()')
    # A positional one-shot from the threat can naturally finish after Resume.
    # Persistent room/pulse loops must retain their identity and playheads.
    old_loops = {a['channel']: a for a in snapshot if a['loop']}
    new_loops = {a['channel']: a for a in resumed if a['loop']}
    assert new_loops.keys() == old_loops.keys(), (resumed, snapshot)
    assert all(not a['paused'] and a['time'] > old_loops[k]['time'] + .15 for k, a in new_loops.items()), (resumed, snapshot)
    passed('Pause freezes every channel and blocks new sounds; tab visibility cannot resume manual Pause, and Resume retains the playheads')

    ev("S.hp=75;WardSound.sync();WardSound.pauseAll('pulse-transition')")
    release = ev("WardSound.snapshot().filter(a=>a.channel==='pulse-release')")
    assert release, ev('WardSound.snapshot()')
    page.wait_for_timeout(500)
    frozen = ev("WardSound.snapshot().filter(a=>a.channel==='pulse-release')")
    assert len(frozen) == len(release) and all(a['paused'] for a in frozen)
    assert all(abs(a['time'] - b['time']) < .025 for a, b in zip(frozen, release))
    ev("WardSound.resumeAll('pulse-transition')")
    page.wait_for_function("!WardSound.snapshot().some(a=>a.channel==='pulse-release')")
    assert ev("WardSound.snapshot().filter(a=>a.channel==='pulse').map(a=>a.clip)") == ['heartbeat_caution']
    passed('condition changes release outgoing bass smoothly; Pause also freezes that transition, leaving one physiological channel after Resume')

    ev('doc("Night Attendant Journal");WardSound.sync()')
    page.wait_for_function("!WardSound.snapshot().some(a=>a.channel?.startsWith('pulse'))")
    assert ev("WardSound.snapshot().some(a=>a.channel==='room'&&!a.paused)")
    ev('closeModal();WardSound.sync()')
    page.wait_for_function("WardSound.snapshot().some(a=>a.channel==='pulse'&&a.clip==='heartbeat_caution'&&!a.paused)")
    passed('reading an actual record quiets the physiological pulse while room ambience continues; closing it restores the correct condition pulse')

    ev("soundEffect('pickup')")
    assert ev("WardSound.history.at(-1).name") == 'pickup_chime'
    assert not ev("WardSound.history.slice(-4).some(a=>a.name==='cloth')")
    page.wait_for_timeout(650)
    assert not ev("WardSound.snapshot().some(a=>a.clip==='pickup_chime')")
    ev("soundEffect('hit')")
    assert ev("WardSound.history.at(-1).name") == 'impact'
    hits = ev("WardSound.history.filter(a=>a.name==='impact').length")
    page.wait_for_timeout(1500)
    assert ev("WardSound.history.filter(a=>a.name==='impact').length") == hits
    passed('pickup uses the short original cue; an explicit damage impact plays once and never becomes a breathing or heartbeat loop')

    ev('window.__audioPauseFunction=WardWinter.isPaused;WardWinter.isPaused=()=>true;WardSound.sync()')
    assert ev('WardSound.snapshot().every(a=>a.paused)')
    ev('WardWinter.isPaused=()=>false;WardSound.sync()')
    page.wait_for_timeout(300)
    assert ev('WardSound.snapshot().filter(a=>a.loop).every(a=>!a.paused)')
    ev('WardWinter.isPaused=window.__audioPauseFunction')
    passed('the game-wide Pause contract stops and restores audio without a parallel sound clock')
    assert not errors, errors
    browser.close()

target = ROOT / 'tests' / 'results' / 'audio_pass.json'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({'checks': checks, 'browser_errors': errors, 'assets': manifest['files']}, indent=2) + '\n')
