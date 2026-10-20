"""Rendered body occlusion and real, usable physical hiding apertures."""
from pathlib import Path
from io import BytesIO
import json,sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010'
checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);q=b.new_page(viewport={'width':1672,'height':941},service_workers='block',reduced_motion='reduce');q.on('pageerror',lambda e:errors.append(str(e)));q.goto(URL);q.get_by_role('button',name='BEGIN INVESTIGATION',exact=True).click();q.evaluate('nextIntro();nextIntro();nextIntro()')
 q.add_style_tag(content='.winter-actor,.winter-walk-sheet{animation:none!important}.winter-walk-sheet{background-position:0 0!important}')
 def ev(code,arg=None):return q.evaluate(code,arg)
 def ready():q.wait_for_function('WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy')
 def stage(variant=0,room='wardnorth'):
  ev('''({variant,room})=>{S.enemyActors=[{id:'infected-'+variant,room,home:room,hp:20,maxHp:20,name:'Infected',dmg:[3,5],down:false,dormant:false}];WardWinter.enemies.project();S.room=room;S.prev=null;S.roomView='front';S.roomViewRoom=room;S.sceneFocus=null;S.f.hidingRoom=null;S.f.wet=0;S.f.coldExposure=0;S.f.shivering=0;S.f.power=1;S.f.powerOut=0;S.f.phoneRinging=false;S.f.sprinklerTriggered=1;S.f.sprinklerStopped=1;S.f.windowBarricaded=1;S.sceneDisturbance=null;S.pursuer={active:variant===3,room,cooldown:999};S.f.pursuerEncounter=0;S.hallCombat=null;cm=0;$('m').innerHTML='';render();}''',{'variant':variant,'room':room});ready()
 for variant in range(4):
  stage(variant)
  src=ev('document.querySelector("[data-solid-source]").dataset.solidSource')
  ev('src=>WardRoomViewRenderer.opaqueReady(src)',src)
  data=ev('''src=>{const c=WardRoomViewRenderer.opaqueCanvas(src),a=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let core=0,soft=0,empty=0;const width=c.width/(src.includes('_walk.')?4:1),points=[];for(let y=60;y<c.height-40;y+=9)for(let x=0;x<Math.floor(width);x+=7){const k=(y*c.width+x)*4;if(a[k+3]===255){core++;if(points.length<600&&x>width*.2&&x<width*.8)points.push([x/width,y/c.height]);}else if(a[k+3])soft++;else empty++;}return {core,soft,empty,points};}''',src)
  assert data['core']>300 and data['empty']>100,data
  # Actual rendered sprite over two contrasting backgrounds. Body interiors
  # must return identical pixels: room/background cannot show through skin.
  node=q.locator('.winter-actor');body=node.locator('[data-solid-source]');r=node.bounding_box();br=body.bounding_box();is_sheet=body.evaluate("e=>e.tagName==='SPAN'")
  if not is_sheet:
   # The still orderly has one frame, not a four-frame sheet.
   data=ev('''src=>{const c=WardRoomViewRenderer.opaqueCanvas(src),a=c.getContext('2d').getImageData(0,0,c.width,c.height).data,points=[];for(let y=60;y<c.height-40;y+=9)for(let x=c.width*.25|0;x<c.width*.75;x+=7){const k=(y*c.width+x)*4;if(a[k+3]===255&&a[k-4+3]===255&&a[k+4+3]===255)points.push([x/c.width,y/c.height]);}return {points};}''',src)
  ev("document.querySelector('.room-view-canvas').style.visibility='hidden';document.querySelector('.room-view-frame').style.backgroundColor='#ff00ff'");a=np.array(Image.open(BytesIO(node.screenshot())).convert('RGB'))
  ev("document.querySelector('.room-view-frame').style.backgroundColor='#00ff00'");z=np.array(Image.open(BytesIO(node.screenshot())).convert('RGB'))
  coords=[]
  for x,y in data['points']:
   px=int(br['x']-r['x']+x*br['width']);py=int(br['y']-r['y']+y*br['height'])
   if 2<=px<a.shape[1]-2 and 2<=py<a.shape[0]-2:coords.append((px,py))
  difference=[np.max(np.abs(a[y,x].astype(int)-z[y,x].astype(int))) for x,y in coords]
  assert len(difference)>80,(variant,len(difference))
  assert np.quantile(difference,.8)<=2,(variant,np.quantile(difference,[.5,.8,.95]))
  ev("document.querySelector('.room-view-canvas').style.visibility='';document.querySelector('.room-view-frame').style.backgroundColor=''")
 checks.append('all three infected bodies and Subject X occlude contrasting live backgrounds with solid alpha rather than a CSS transparency filter')
 for cover in ['locker','desk','crates']:
  stage(0);ev('''cover=>{S.f.power=0;S.lightOn=false;S.bat=0;S.f.hidingRoom=S.room;S.f.hidingType=cover;S.f.lockerPeeking=false;render();}''',cover);ready()
  host=q.locator('#interactiveScene');closed=np.array(Image.open(BytesIO(host.screenshot())).convert('RGB'))
  q.get_by_role('button',name='Peek',exact=True).click();q.wait_for_timeout(100)
  assert ev('WardWinter.roomViewRenderer().peeking&&document.querySelector(".room-view-frame").classList.contains("peek-adapted")')
  peek=np.array(Image.open(BytesIO(host.screenshot())).convert('RGB'));apertures=ev('WardWinter.peekApertures')
  mask=np.zeros(peek.shape[:2],dtype=bool)
  for x,y,w,h in apertures:
   x0=int((x+.3)/100*mask.shape[1]);x1=int((x+w-.3)/100*mask.shape[1]);y0=int((y+.3)/100*mask.shape[0]);y1=int((y+h-.3)/100*mask.shape[0]);mask[y0:y1,x0:x1]=True
  values=peek[mask].mean(axis=1);assert len(values)>2000,(cover,len(values));assert np.quantile(values,.8)>18,(cover,np.quantile(values,[.5,.8,.95]));assert values.std()>7,(cover,values.std())
  assert np.mean(np.abs(peek[mask].astype(int)-closed[mask].astype(int)))>12,cover
  # Beyond the physical openings the upper hiding shell stays opaque.
  outside=~mask;outside[int(mask.shape[0]*.72):]=False
  # Exclude antialias rims at openings by dilating test masks locally.
  for x,y,w,h in apertures:
   outside[max(0,int(y/100*mask.shape[0])-4):min(mask.shape[0],int((y+h)/100*mask.shape[0])+4),max(0,int(x/100*mask.shape[1])-4):min(mask.shape[1],int((x+w)/100*mask.shape[1])+4)]=False
  assert np.quantile(peek[outside].mean(axis=1),.99)<8,(cover,np.quantile(peek[outside].mean(axis=1),.99))
  assert .025<mask.mean()<.18,(cover,mask.mean())
  q.screenshot(path=str(ROOT/'tests/results'/('peek-v8-'+cover+'.png')))
  q.get_by_role('button',name='Pause game',exact=True).click();assert ev('WardWinter.isPaused()');q.get_by_role('button',name='Resume game',exact=True).click();q.get_by_role('button',name='Exit',exact=True).click();ready();assert not ev('WardWinter.roomViewRenderer().peeking||document.querySelector(".room-view-frame").classList.contains("peek-adapted")')
 checks.append('locker vents, desk opening and crate gaps expose readable live dark-room pixels, while opaque cover stays black and exit restores room darkness')
 stage(0);ev('S.f.hidingRoom=S.room;S.f.hidingType="locker";S.f.lockerPeeking=true;render()');ready()
 for width,height in [(1000,800),(390,844),(1672,941)]:
  q.set_viewport_size({'width':width,'height':height});q.wait_for_timeout(120)
  assert ev('(()=>{const host=interactiveScene.getBoundingClientRect(),frame=document.querySelector(".room-view-frame").getBoundingClientRect();return WardWinter.peekApertures.every(([x,y,w,h])=>x/100*host.width>=frame.left-host.left&&((y+h)/100*host.height)<=frame.bottom-host.top+1);})()')
  assert q.locator('.hiding-physical.peeking').is_visible()
 q.get_by_role('button',name='Exit',exact=True).click();ready()
 checks.append('physical hiding apertures stay aligned with the fitted room across live desktop, tablet and mobile resizes')

 stage(0,'surgery');ev('S.enemyActors.forEach(a=>a.hp=0);WardWinter.enemies.project();S.f.doctorWallSeen=0;render()');ready();before=ev('WardWinter.roomViewAsset("surgery","front")');assert before.endswith('surgery_front.webp');ev('doctorAtWall()');assert q.get_by_role('button',name='Call his name',exact=True).is_visible();q.get_by_role('button',name='Call his name',exact=True).click();assert ev('S.f.doctorWallSeen&&S.ob.kessler==="read"');ev('closeModal()');ready();assert ev('WardWinter.roomViewAsset("surgery","front")').endswith('surgery_after.webp');assert not q.locator('[data-fixture="kessler"]').count();assert ev('!WardWinter.orbit.points().some(p=>p.id==="fixture:kessler")')
 checks.append('Kessler uses coherent standing/attached-hands encounter art and persistent seated aftermath; completed person target is retired')
 ev('S.sceneDisturbance={room:S.room,view:"front",kind:"hanged",deadline:Date.now()+15000};renderScene()');assert q.locator('[data-sanity-vision]').count()==1;assert ev('S.roomView')=='front';ev('WardWinter.orbit.face("rear")');ready();assert not q.locator('[data-sanity-vision]').count()
 checks.append('earned sanity vision renders in its saved current-facing view without forcing a camera turn')
 assert not errors,errors;b.close()
(ROOT/'tests/results/visual_solid_peek_v8.json').write_text(json.dumps({'checks':checks,'javascript_errors':errors},indent=2)+'\n');print('\n'.join('PASS '+c for c in checks))
