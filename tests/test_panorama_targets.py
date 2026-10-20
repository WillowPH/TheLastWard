"""Native whole-room artwork: every active object/door center accepts a mouse hit.

The filename is retained for existing validation commands. No panoramic camera
test hooks or keyboard controls are used: real mouse drags expose views.
"""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright
from mouse_controls import turn_room

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8010'
OUT = ROOT / 'tests/results'
OUT.mkdir(exist_ok=True)
failures = []
errors = []
counts = 0

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--enable-unsafe-swiftshader'])
    context = browser.new_context(viewport={'width': 1672, 'height': 941}, service_workers='block', reduced_motion='reduce')
    context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(URL.rstrip('/') + '/') else route.abort())
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(URL)
    page.get_by_role('button', name='BEGIN INVESTIGATION').click()
    page.evaluate('nextIntro();nextIntro();nextIntro()')
    page.evaluate('WardScene.options.snapMotion=false;S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.pursuer.active=false;S.f.power=1;S.f.pharm=1;S.f.chapel=1;S.f.photoPuzzleSolved=0;S.f.researchers=1;S.f.drained=1')
    for room in page.evaluate('Object.keys(R)'):
        page.evaluate('r=>{S.room=r;S.prev=r;S.roomViewRoom=null;S.sceneFocus=null;render()}', room)
        page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
        if room == 'wardnorth':
            page.evaluate('wardOpenWindows()')
            page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
        points = page.evaluate('WardWinter.orbit.points()')
        for point in points:
            if page.evaluate('S.roomView') != point['view']:
                turn_room(page)
                page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
            assert page.evaluate('S.roomView') == point['view'], (room, point)
            result = page.evaluate('''p=>{
                const selector=p.id.startsWith('door:')?'[data-door="'+p.id.slice(5)+'"]':'[data-fixture="'+p.id.slice(8)+'"]';
                const node=document.querySelector(selector);
                if(!node)return {wanted:p.id,ok:false,hit:'MISSING_TARGET'};
                const rect=node.getBoundingClientRect(),x=rect.x+rect.width/2,y=rect.y+rect.height/2,hit=document.elementFromPoint(x,y);
                return {wanted:p.id,view:S.roomView,hit:hit?.dataset.fixture||hit?.dataset.door||hit?.id||hit?.getAttribute('aria-label')||hit?.tagName,ok:hit===node,rect:[rect.x,rect.y,rect.width,rect.height]};
            }''', point)
            counts += 1
            if not result['ok']:
                failures.append({'room': room, **result})
                page.screenshot(path=str(OUT / ('native-target-failure-' + room + '.png')))
        print(room, 'checked', len(points), flush=True)
    browser.close()

report = {'mode': 'native-full-image-room-views', 'count': counts, 'failures': failures, 'errors': errors, 'transport': URL}
(OUT / 'room_view_targets.json').write_text(json.dumps(report, indent=2))
(OUT / 'panorama_targets.json').write_text(json.dumps(report, indent=2))
assert not failures, failures
assert not errors, errors
print('PASS', counts, 'available native room target centers receive the expected ordinary mouse hit')
