"""The actual Examine action and long narration must not rescale the scene."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
ROOT=Path(__file__).resolve().parents[1];url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010';packaged='The_Last_Ward' in url;checked=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();page.set_default_timeout(6000);page.goto(url)
 if packaged:page.context.set_offline(True)
 page.evaluate('newGame();nextIntro();nextIntro();nextIntro()')
 for width,height in [(1600,1000),(1000,800),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});page.evaluate("$('m').innerHTML='';S.room='lobby';S.sceneFocus=null;delete S.ob.win;S.sceneView='front';S.sceneViewRoom=S.room;S.cameraSchema=2;render()");before=page.locator('.c1-plane').bounding_box();page.locator('[data-fixture=window]').click();page.get_by_role('button',name='Examine',exact=True).click();page.wait_for_timeout(80);assert page.locator('.c1-plane').bounding_box()==before
  page.evaluate("interaction('A deliberately long discovered clue. '.repeat(40));render()");page.wait_for_timeout(80);assert page.locator('.c1-plane').bounding_box()==before;checked.append(f'{width}x{height}: actual Examine and long narration preserve scene bounds')
 b.close()
(ROOT/'tests/results'/('inspection_actions_packaged.json' if packaged else 'inspection_actions.json')).write_text(json.dumps({'count':len(checked),'passed':checked},indent=2))
for c in checked:print('PASS',c)
