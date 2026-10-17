"""All fixed doorway identities, actual arrival/return clicks and glass-only weather.
Optional URL permits exactly the same acceptance checks against the offline package.
Unlocks prerequisite states ONLY for exhaustive edge testing; test_chapter1.py tests
three unmodified progression routes separately.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/results';url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010';packaged='The_Last_Ward' in url;checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':1000},reduced_motion='no-preference');page.set_default_timeout(7000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.add_init_script("localStorage.setItem('lw_art_mode','offline')");page.goto(url)
 if packaged:page.context.set_offline(True)
 def ev(code,arg=None):return page.evaluate(code,arg)
 ev('newGame();nextIntro();nextIntro();nextIntro()')
 # Shared graph is the authority, not previous-room-dependent rendering.
 edges=ev('Object.entries(D).flatMap(([id,d])=>[[id,d.a,d.b],[id,d.b,d.a]])');assert len(edges)==54
 assert ev('WardChapter.rooms.every(r=>{const v=WardScenes[r].views,front=Object.keys(v.front.doors),rear=Object.keys(v.rear.doors);return rear.length===1&&!front.includes(rear[0])&&front.length+rear.length===Object.keys(WardScenes[r].doors).length})')
 checks.append('54 directed portals across 27 rooms have one permanent view and destination')
 base=ev('JSON.parse(JSON.stringify(S))')
 def setup(room):
  ev('''a=>{S=JSON.parse(JSON.stringify(a.base));S.room=a.room;S.prev=null;S.cameraSchema=2;S.sceneView='front';S.sceneViewRoom=S.room;S.sceneFocus=null;S.hp=100;S.san=100;S.pursuer.active=false;S.en=Object.fromEntries(Object.keys(E).map(r=>[r,0]));for(const r of WardChapter.rooms)S.f['doctor_'+r]=1;for(const id of Object.keys(D))S.dr[id]=1;Object.assign(S.f,{power:1,photoPuzzleSolved:1,plexiIncidentSeen:1,researcherLastRoomSeen:1,doctorWallSeen:1,finalSecurityClearance:1,pursuerStarted:1,pursuerEscapes:1,researchersScene:1,firstFloorCinematicSeen:1,powerOut:0});S.lightOn=true;S.bat=100;WardNavigation.until=0;$('m').innerHTML='';render()}''',{'room':room,'base':base})
 def dismiss():ev("$('m').innerHTML='';S.f.pursuerEncounter=0;S.pursuer.active=false;renderScene()")
 def travel(to):
  wanted=ev('to=>WardScene.portalView(S.room,WardNavigation.edge(S.room,to))',to)
  if ev('S.sceneView')!=wanted:page.get_by_role('button',name='Turn around',exact=True).click()
  plane='.c1-reverse-plane' if wanted=='rear' else '.c1-plane'
  button=page.locator(plane+' [data-destination="'+to+'"]');button.wait_for(state='visible');page.wait_for_function('performance.now()>=WardNavigation.until');box=button.bounding_box();page.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2)
 def entry_behind(previous):
  page.wait_for_function("[...document.querySelectorAll(S.sceneView==='rear'?'.c1-reverse-plane>img':'.c1-background')].every(i=>i.complete&&i.naturalWidth>0)")
  assert ev('p=>S.prev===p&&S.sceneView!==WardScene.portalView(S.room,WardNavigation.edge(S.room,p))',previous),(previous,ev('({room:S.room,prev:S.prev,view:S.sceneView})'))
  visible=ev('''p=>[...document.querySelectorAll('[data-destination="'+p+'"]')].filter(el=>{const r=el.getBoundingClientRect();return r.width&&r.height&&getComputedStyle(el).visibility!=='hidden'&&!el.closest('[inert]')}).length''',previous)
  assert visible==0,(previous,visible)
 for width,height in [(1600,1000),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  for id,origin,destination in edges:
   setup(origin);travel(destination);assert ev('S.room')==destination,(id,origin,destination,ev('S.msg'));dismiss();entry_behind(origin)
   # Turning exposes the true entry; clicking it returns through the SAME edge.
   page.get_by_role('button',name='Turn around',exact=True).click();expected=ev('r=>WardScene.portalView(S.room,WardNavigation.edge(S.room,r))',origin);assert ev('S.sceneView')==expected
   travel(origin);assert ev('S.room')==origin;dismiss();entry_behind(destination)
  checks.append(f'{width}x{height}: all 54 actual doorway clicks and 54 return clicks preserve destination and put entry behind arrival')
 # Pursuer cues use current portal geometry and facing, never removed front slots.
 safe=ev('[...SAFE_FROM_PURSUER]');cue_edges=[e for e in edges if e[1] not in safe and e[2] not in safe]
 for id,origin,destination in cue_edges:
  setup(origin);ev('r=>{S.pursuer.active=true;S.pursuer.room=r}',destination)
  view=ev('id=>WardScene.portalView(S.room,id)',id)
  ev('v=>{S.sceneView=v}',view);ahead=ev('WardSound.distance()');assert ahead['distance']==1 and not ahead['behind']
  ev("S.sceneView=S.sceneView==='front'?'rear':'front'");behind=ev('WardSound.distance()');assert behind['behind'] and abs(ahead['pan']+behind['pan'])<.00001
 checks.append(f'{len(cue_edges)} valid nearby pursuer routes follow the fixed doorway and reverse bearing when the camera turns; safe rooms excluded')
 # Legacy migration and saved camera stability.
 setup('eastcorridor');ev("S.prev='lobby';delete S.cameraSchema;S.sceneViewRoom=S.room;renderScene()");entry_behind('lobby');ev('wardTurnAround()');saved=ev('JSON.parse(JSON.stringify(S))');ev('s=>{S=JSON.parse(JSON.stringify(s));renderScene()}',saved);assert ev('S.sceneView')==saved['sceneView'];assert ev('S.cameraSchema')==2
 checks.append('old-save camera migrates from the entry edge; new saves retain a manually turned view')
 # Weather alpha must be empty everywhere outside authored exterior glass.
 for width,height in [(1600,1000),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});setup('lobby');ev('WardScene.options.motion=true;WardScene.options.motionOverride=true;renderScene()')
  for view in ['front','rear']:
   if ev('S.sceneView')!=view:page.get_by_role('button',name='Turn around',exact=True).click()
   page.wait_for_timeout(180)
   result=ev('''()=>{const canvas=document.querySelector('.c1-weather-rain'),c=canvas.getContext('2d'),a=c.getImageData(0,0,1000,750).data,polys=WardMotion.glazing.lobby[S.sceneView];function inside(x,y,p){let hit=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const A=p[i],B=p[j];if((A[1]>y)!=(B[1]>y)&&x<(B[0]-A[0])*(y-A[1])/(B[1]-A[1])+A[0])hit=!hit;}return hit;}let visible=0,outside=0;for(let y=0;y<750;y++)for(let x=0;x<1000;x++){if(!a[(y*1000+x)*4+3])continue;visible++;let valid=false;for(const dx of [-1,0,1])for(const dy of [-1,0,1])if(polys.some(p=>inside((x+dx)/10,(y+dy)/7.5,p)))valid=true;if(!valid)outside++;}return {visible,outside,frame:canvas.toDataURL()}}''')
   assert result['visible']>50 and result['outside']==0,(width,view,result['visible'],result['outside']);page.wait_for_timeout(150);assert result['frame']!=page.locator('.c1-weather-rain').evaluate('(c)=>c.toDataURL()');assert page.locator('.c1-rain-motion').count()==0
   if width==1600:page.screenshot(path=str(OUT/f'portal-weather-{view}.png'))
  checks.append(f'{width}x{height}: moving rain in both lobby views has zero pixels outside glass masks; no duplicate weather layer')
 for room in ev('WardChapter.rooms'):
  if room=='lobby':continue
  setup(room)
  for view in ['front','rear']:
   ev('v=>{S.sceneView=v;renderScene()}',view);assert not page.locator('.c1-weather-rain,.c1-rain-motion').count(),(room,view)
 checks.append('the other 26 rooms have no rain overlay in either view')
 # Reduced motion and explicit toggle remove both canvases.
 setup('lobby');page.emulate_media(reduced_motion='reduce');ev('WardScene.options.motionOverride=false;renderScene()');assert not page.locator('.c1-motion-canvas,.c1-weather-rain').count()
 assert not errors,errors;b.close()
(OUT/('portal_weather_packaged.json' if packaged else 'portal_weather.json')).write_text(json.dumps({'passed':checks,'count':len(checks)},indent=2))
for c in checks:print('PASS',c)
