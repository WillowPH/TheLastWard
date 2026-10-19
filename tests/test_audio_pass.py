"""Actual browser playback, health-tier selection and pause continuity regressions."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import numpy as np
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
assert len(decoded['breath_calm']) > len(decoded['breath_caution']) > len(decoded['breath_danger'])
for name in ['breath_calm', 'breath_caution', 'breath_danger']:
    values = decoded[name]
    # Calm air rests between breaths; no repeated abrupt impact envelope.
    windows = np.array([np.sqrt(np.mean(w ** 2)) for w in np.array_split(values, 160)])
    assert np.count_nonzero(windows < .003) > 20, name
    assert np.max(np.abs(values[:400])) < .01 and np.max(np.abs(values[-400:])) < .01, name
passed('all 8 original assets decode, match provenance, avoid clipping and contain paced breath/rest cycles')

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
    assert ev("WardSound.snapshot().filter(a=>a.channel==='breathing').map(a=>a.clip)") == ['breath_calm']
    assert ev("WardSound.snapshot().some(a=>a.clip==='hospital_hum')")
    assert not ev("WardSound.snapshot().some(a=>['breathing','room_hum','winter_wind'].includes(a.clip))")
    energies = []
    for _ in range(8):
        page.wait_for_timeout(90)
        energies.append(ev('WardSound.energy()'))
    assert max(energies) > .00001, energies
    passed('new calm air breath and long lobby hum actually advance and produce WebAudio output')

    for hp, name in [(45, 'breath_caution'), (20, 'breath_danger'), (100, 'breath_calm')]:
        ev('hp=>{S.hp=hp;S.san=10;WardSound.sync()}', hp)
        page.wait_for_function('(name)=>WardSound.snapshot().some(a=>a.clip===name&&a.ready>=3&&!a.paused)', arg=name)
        assert ev("WardSound.snapshot().filter(a=>a.channel==='breathing').map(a=>a.clip)") == [name]
    before = ev('WardSound.history.length')
    ev('for(let i=0;i<100;i++)WardSound.sync()')
    assert ev('WardSound.history.length') == before
    assert not ev("WardSound.snapshot().some(a=>a.clip==='breathing'||a.clip==='impact')")
    passed('HP selects calm/caution/danger; low sanity never selects hurt grunts; 100 syncs create no duplicate loops')

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
    assert len(resumed) == len(snapshot), resumed
    assert all(not a['paused'] and a['time'] > b['time'] + .15 for a, b in zip(resumed, snapshot)), (resumed, snapshot)
    passed('pause freezes every channel and blocks new sounds; tab visibility cannot resume manual Pause; resume preserves playheads without duplicates')

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
    passed('pickup uses the original short cue and ends; explicit damage impact plays once without becoming a breathing loop')

    ev('window.__audioPauseFunction=WardWinter.isPaused;WardWinter.isPaused=()=>true;WardSound.sync()')
    assert ev('WardSound.snapshot().every(a=>a.paused)')
    ev('WardWinter.isPaused=()=>false;WardSound.sync()')
    page.wait_for_timeout(300)
    assert ev('WardSound.snapshot().filter(a=>a.loop).every(a=>!a.paused)')
    ev('WardWinter.isPaused=window.__audioPauseFunction')
    passed('the game-wide pause contract automatically stops and restores audio without a parallel sound clock')
    assert not errors, errors
    browser.close()

target = ROOT / 'tests' / 'results' / 'audio_pass.json'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({'checks': checks, 'browser_errors': errors, 'assets': manifest['files']}, indent=2) + '\n')
