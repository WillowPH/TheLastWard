"""Actual HUD, paper contrast and mouse navigation at the supported reference sizes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
report={'checks':[],'screens':[],'documents':[],'javascript_errors':[]}
OUT=ROOT/'tests/results';OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
 context=browser.new_context(viewport={'width':1672,'height':941},service_workers='block')
 page=context.new_page();page.set_default_timeout(12000);page.on('pageerror',lambda err:report['javascript_errors'].append(str(err)))
 page.goto(URL);page.get_by_role('button',name='BEGIN INVESTIGATION').click();page.evaluate('nextIntro();nextIntro();nextIntro()')
 def ready():page.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
 ready();page.evaluate('S.mapParts=3;S.vis.security=1;render();WardWinter.think("I need to switch on the flashlight before searching this dark room.")');ready()
 for width,height in [(1672,941),(1000,800),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(200)
  row=page.evaluate('''()=>{const box=s=>{const n=document.querySelector(s),r=n.getBoundingClientRect(),c=getComputedStyle(n);return {display:c.display,height:n.clientHeight,scrollHeight:n.scrollHeight,width:n.clientWidth,scrollWidth:n.scrollWidth,x:r.x,y:r.y,right:r.right,bottom:r.bottom,background:c.backgroundColor};};const renderer=WardWinter.roomViewRenderer();return {width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,thought:box('.scene-thought'),narration:box('.narration-block'),heading:box('.unified-inventory-panel .panel-heading'),frame:box('.room-view-frame'),viewport:box('.room-view-viewport'),center:box('.ward-center'),source:renderer.sourceSize,toolbar:getComputedStyle(document.querySelector('.winter-look-controls')).display};}''')
  assert row['scrollWidth']<=width,row
  assert row['thought']['display']!='none',row
  assert row['thought']['height']==row['thought']['scrollHeight'],row
  assert row['narration']['height']==row['narration']['scrollHeight'],row
  assert row['heading']['width']==row['heading']['scrollWidth'],row
  assert row['toolbar']=='none',row
  frame,viewport,source=row['frame'],row['viewport'],row['source']
  assert frame['x']>=viewport['x']-1 and frame['y']>=viewport['y']-1 and frame['right']<=viewport['right']+1 and frame['bottom']<=viewport['bottom']+1,row
  assert frame['width']<=source['width'] and frame['height']<=source['height'],row
  assert abs(frame['width']/frame['height']-source['width']/source['height'])<.004,row
  assert row['center']['bottom']<=height+1,row
  path=OUT/f'reference-theme-{width}.png';page.screenshot(path=str(path));report['screens'].append({'path':path.name,**row})
 report['checks'].append('Reference, tablet and mobile layouts retain all Thoughts text, no narration scrolling, no bottom control bar, and fit whole native art without cropping, stretching or enlargement.')
 page.set_viewport_size({'width':1672,'height':941});ready();before=page.evaluate('S.roomView');page.get_by_role('button',name='Look right',exact=True).hover();page.get_by_role('button',name='Look right',exact=True).click();ready();assert page.evaluate('S.roomView')!=before
 page.get_by_role('button',name='Look left',exact=True).click();ready();assert page.evaluate('S.roomView')==before
 report['checks'].append('Native mouse clicks on left and right edge chevrons change room-facing views and return; no keyboard input is required.')
 page.get_by_role('button',name='Options',exact=True).click();surfaces=page.evaluate('''()=>['#m .md','#m .mh','.options-violence'].map(s=>({selector:s,bg:getComputedStyle(document.querySelector(s)).backgroundColor}))''')
 for entry in surfaces:
  rgb=[int(v) for v in entry['bg'].replace('rgba(','').replace('rgb(','').split(')')[0].split(',')[:3]]
  assert max(rgb)-min(rgb)<=8,entry
 page.screenshot(path=str(OUT/'reference-theme-options.png'));page.evaluate('closeModal()');report['checks'].append('Options/modal surfaces use neutral charcoal instead of a dark green fill.');report['surfaces']=surfaces
 for title,kind in [('Heller’s winter maintenance note','handwritten'),('Nursing personnel amendment','typed')]:
  page.evaluate('(title)=>doc(title)',title)
  paper=page.locator('.winter-document').evaluate('''e=>({background:getComputedStyle(e).backgroundColor,color:getComputedStyle(e.querySelector('.winter-paper-text')).color,font:getComputedStyle(e.querySelector('.winter-paper-text')).font,textLength:e.querySelector('.winter-paper-text').textContent.length})''')
  ink=[int(v) for v in paper['color'].removeprefix('rgb(').removesuffix(')').split(',')]
  assert max(ink)<65 and paper['textLength']>100,paper
  assert page.locator('.winter-document').evaluate('e=>e.scrollHeight<=e.clientHeight+2'),paper
  assert page.locator('.record-modal .mb').evaluate('e=>e.scrollHeight<=e.clientHeight+2'),paper
  page.screenshot(path=str(OUT/f'reference-theme-paper-{kind}.png'));report['documents'].append({'title':title,**paper});page.evaluate('closeModal()')
 report['checks'].append('Real handwritten and typed records retain dark readable text on damaged parchment; modal colours do not leak into document ink.')
 assert not report['javascript_errors'],report['javascript_errors'];browser.close()
(OUT/'reference_theme.json').write_text(json.dumps(report,indent=2)+'\n')
for check in report['checks']:print('PASS',check)
