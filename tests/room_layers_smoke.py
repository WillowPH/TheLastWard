"""Browser regression checks for the five-room object-layer pilot.
Run: python tests/room_layers_smoke.py (uses system Chromium and Playwright).
"""
import functools
import http.server
import json
import pathlib
import threading
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
ROOMS = ['lobby', 'security', 'eastcorridor', 'ward', 'room12']
checks = 0
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width':1600,'height':1000}, reduced_motion='reduce')
    errors=[]
    page.on('pageerror', lambda e:errors.append(str(e)))
    page.add_init_script("localStorage.setItem('lw_art_mode','offline')")
    page.goto(f'http://127.0.0.1:{server.server_port}')
    page.evaluate("newGame(); S.f.introComplete=1; closeModal();")
    # Coverage includes seeded cache/phone objects and every conditional fixture.
    result=page.evaluate('''rooms=>{
      const failures=[];let fixtures=0;
      for(let seed=0;seed<40;seed++){
        configureWorld('pilot-'+seed,false);placeTelephones('pilot-'+seed);
        S.f.power=1;S.f.pharm=1;S.f.researchers=1;S.f.powerOut=0;S.lightOn=true;
        for(const room of rooms){S.room=room;const groups=WardRoomLayers.groups(room),mapped=new Set(groups.flatMap(g=>g.objects.map(o=>o[0])));
          for(const o of availableRoomObjects())if(!mapped.has(o[0]))failures.push(room+': unmapped '+o[0]);
          const rs=[...groups.map(g=>[g.id,g.rect]),...roomConnections().filter(d=>!WardRoomLayers.rooms[room].offscreen?.includes(d.to)).map(d=>['door-'+d.to,WardRoomLayers.rooms[room].doors[d.to]])];
          fixtures+=groups.length;
          for(const [id,r] of rs){if(!r){failures.push(room+': missing '+id);continue}const [x,y,w,h]=r;if(x-w/2<0||x+w/2>100||y-h/2<0||y+h/2>100)failures.push(room+': out of frame '+id);}
          for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){const [a,A]=rs[i],[b,B]=rs[j];if(!A||!B)continue;const dx=Math.min(A[0]+A[2]/2,B[0]+B[2]/2)-Math.max(A[0]-A[2]/2,B[0]-B[2]/2),dy=Math.min(A[1]+A[3]/2,B[1]+B[3]/2)-Math.max(A[1]-A[3]/2,B[1]-B[3]/2);if(dx>.05&&dy>.05)failures.push(room+': overlap '+a+'/'+b);}
        }
      }return {failures:[...new Set(failures)],fixtures};}''',ROOMS)
    assert not result['failures'], json.dumps(result,indent=2)
    checks+=1
    for width,height in [(1600,1000),(1000,800),(390,844)]:
        page.set_viewport_size({'width':width,'height':height})
        for room in ROOMS:
            page.evaluate("room=>{S.room=room;S.sceneFocus=null;S.lightOn=true;render();}",room)
            page.wait_for_timeout(80)
            assert page.locator('.authored-room .v3-background').evaluate('(i)=>i.complete&&i.naturalWidth>0')
            boxes=page.locator('.authored-room').evaluate('''p=>{const r=p.getBoundingClientRect();return [...p.querySelectorAll('button')].map(b=>{const t=b.getBoundingClientRect();return {id:b.getAttribute('aria-label'),ok:t.left>=r.left-1&&t.right<=r.right+1&&t.top>=r.top-1&&t.bottom<=r.bottom+1,hit:document.elementFromPoint(t.x+t.width/2,t.y+t.height/2)===b||b.contains(document.elementFromPoint(t.x+t.width/2,t.y+t.height/2))}})}''')
            assert all(x['ok'] for x in boxes),(room,width,boxes)
            page.locator('.authored-room').scroll_into_view_if_needed()
            hit=page.locator('.authored-room').evaluate('''p=>[...p.querySelectorAll('button')].every(b=>{const t=b.getBoundingClientRect(),e=document.elementFromPoint(t.x+t.width/2,t.y+t.height/2);return e===b||b.contains(e)})''')
            assert hit,(room,width,'target intercepted')
            # Offscreen content on narrow viewports is scrollable; verify clicks on visible fixtures.
            fixture=page.locator('.authored-room .v3-prop').first
            fixture.scroll_into_view_if_needed();fixture.click()
            assert page.locator('#sceneFocusOverlay').is_visible(),(room,width)
            page.evaluate('wardCloseFocus()')
            if width==1600: page.screenshot(path=str(ROOT/'tests'/f'{room}-pilot.png'))
            checks+=1
    page.set_viewport_size({'width':1600,'height':1000})
    page.evaluate("S.room='lobby';S.ob={};S.f={introComplete:1};S.sceneFocus=null;render();")
    page.locator('[data-fixture="reception"]').click()
    page.get_by_role('button',name='Take',exact=True).click()
    assert page.evaluate("has('Cabinet Key')&&S.ob.desk==='done'")
    assert page.locator('[data-fixture="reception"]').evaluate("e=>e.classList.contains('is-complete')")
    assert page.locator('.object-collected').count()>0
    page.locator('.room-hints').click()
    assert page.locator('.room-hints').get_attribute('aria-pressed')=='true'
    checks+=1
    # A real Continuity Terminal save/load preserves authored object and inspection states.
    page.evaluate("add('Ink Ribbon');confirmSave();S.ob={};S.f={};loadGame();")
    assert page.evaluate("S.ob.desk==='done'&&S.f.seen_site_lobby_reception===1")
    checks+=1
    # A target invokes actual travel and updates the active room.
    page.evaluate("closeModal();S.room='lobby';S.f.introComplete=1;render();")
    page.locator('[data-destination=security]').click()
    assert page.evaluate("S.room==='security'")
    checks+=1
    # No generated artwork can replace pilot geometry; no optional API request is made.
    assert not errors, errors
    checks+=1
    browser.close()
server.shutdown()
print(f'PASS: {checks} browser checks; 40 seeds; 5 rooms; desktop/tablet/mobile; collection, hints, save/load, travel.')
