"""Real room-effect module/assets in an isolated native-resolution compositor.

This checks all 54 source views independently of HUD layout and input tests.
Eight exterior views and 71 glass cells were manually reviewed against the source
artwork, including the generated barricaded lobby and physical laundry stove.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
ROOT=Path(__file__).resolve().parents[1];URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8010';report=[];errors=[];failures=[]
html='''<!doctype html><html><style>body{margin:0;background:black}#base,#effects{position:absolute;left:0;top:0;width:1448px;height:1086px}#effects{pointer-events:none}</style><canvas id="base" width="1448" height="1086"></canvas><canvas id="effects" width="1448" height="1086"></canvas><script>window.S={room:'lobby',roomView:'front',hp:100,san:100,f:{power:1,powerOut:0}};window.WardWinter={asset:p=>'/'+p,flicker:()=>0,roomViewRenderer:()=>({loaded:true,room:S.room,view:S.roomView,effects:canvas=>{let c=document.querySelector('#effects').getContext('2d');c.clearRect(0,0,1448,1086);c.drawImage(canvas,0,0);}})};window.WardScene={options:{motion:true,flashes:false}};window.WardMotion={enabled:options=>options.motion!==false};</script><script src="/js/room_view_effects.js"></script></html>'''
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);q=b.new_page(viewport={'width':1448,'height':1086},service_workers='block');q.on('pageerror',lambda error:errors.append(str(error)));q.on('response',lambda response:failures.append(str(response.status)+' '+response.url) if response.status>=400 else None);q.route('**/effect-probe',lambda route:route.fulfill(content_type='text/html',body=html));q.goto(URL+'/effect-probe');q.evaluate('WardWinter.roomViewEffects.ready');q.evaluate('WardWinter.roomViewEffects.stop()')
 data=json.load(open(ROOT/'data/room_view_effects.json'));assert len(data)==27;assert sum(len(views) for views in data.values())==54;assert sum(bool(v['glass']) for views in data.values() for v in views.values())==8;assert sum(len(v['glass']) for views in data.values() for v in views.values())==71
 for room,views in data.items():
  for view,spec in views.items():
   q.evaluate('''async a=>{S.room=a.room;S.roomView=a.view;let im=new Image();im.src='/'+a.source;await im.decode();document.querySelector('#base').getContext('2d').drawImage(im,0,0,1448,1086);WardWinter.roomViewEffects.draw(1000)}''',{'room':room,'view':view,'source':spec['source']})
   result=q.evaluate('''()=>{let n=WardWinter.roomViewEffects.snowCanvas,c=n.getContext('2d'),d=c.getImageData(0,0,n.width,n.height).data,p=new Path2D();for(let poly of WardWinter.roomViewEffects.data[S.room][S.roomView].glass){p.moveTo(poly[0][0]/100*n.width,poly[0][1]/100*n.height);for(let [x,y]of poly.slice(1))p.lineTo(x/100*n.width,y/100*n.height);p.closePath();}let painted=0,outside=0;for(let i=3;i<d.length;i+=4)if(d[i]){painted++;let index=(i-3)/4,x=index%n.width,y=Math.floor(index/n.width);if(![[.5,.5],[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]].some(([dx,dy])=>c.isPointInPath(p,x+dx,y+dy)))outside++;}return {room:S.room,view:S.roomView,painted,outside}}''')
   assert result['outside']==0,result
   assert (result['painted']>0)==bool(spec['glass']),result
   report.append(result)
   if spec['glass'] or spec['screens']:q.screenshot(path=str(ROOT/f'tests/results/native-weather-{room}-{view}.png'))
 # Every catch changes only its own native window opening. The raised sash
 # has a different rail position, so the snow cells follow the open state too.
 q.evaluate("WardWinter.windowState=()=>S.windows;S.windows={triggered:true,closed:[false,false,false]}")
 q.evaluate("""async()=>{S.room='wardnorth';S.roomView='rear';let im=new Image();im.src='/assets/reverse/wardnorth.webp';await im.decode();document.querySelector('#base').getContext('2d').drawImage(im,0,0,1448,1086);WardWinter.roomViewEffects.draw(1000)}""");q.wait_for_timeout(300)
 window_checks=[]
 for closed in [[False,False,False],[True,False,False],[True,True,False],[True,True,True]]:
  q.evaluate('closed=>{S.windows.closed=closed;WardWinter.roomViewEffects.draw(1000)}',closed)
  alpha=q.evaluate("[260,468,1128].map(x=>WardWinter.roomViewEffects.canvas.getContext('2d').getImageData(x,324,1,1).data[3])")
  assert all(a==255 if not is_closed else a<100 for a,is_closed in zip(alpha,closed)),(closed,alpha)
  window_checks.append({'closed':closed,'rail_pixel_alpha':alpha})
 q.screenshot(path=str(ROOT/'tests/results/native-windows-resolved.png'))
 for view in ['front','rear']:
  spec=data['lobby'][view];q.evaluate('''async a=>{S.room='lobby';S.roomView=a.view;S.f.lobbyShutters=true;let im=new Image();im.src='/'+a.source;await im.decode();document.querySelector('#base').getContext('2d').drawImage(im,0,0,1448,1086);WardWinter.roomViewEffects.draw(1000)}''',{'view':view,'source':spec['source']});q.wait_for_timeout(300);q.evaluate('WardWinter.roomViewEffects.draw(1000)');q.screenshot(path=str(ROOT/f'tests/results/native-shutters-{view}.png'))
 q.evaluate('''async()=>{S.room='laundry';S.roomView='rear';S.f.stoveLit=true;let im=new Image();im.src='/assets/room_views/laundry_rear.webp';await im.decode();document.querySelector('#base').getContext('2d').drawImage(im,0,0,1448,1086);WardWinter.roomViewEffects.draw(1000)}''');q.screenshot(path=str(ROOT/'tests/results/native-stove-fire.png'))
 assert not errors,errors;assert not failures,failures;
 b.close()
(ROOT/'tests/results/native_weather.json').write_text(json.dumps({'views':report,'window_states':window_checks,'javascript_errors':errors,'resource_errors':failures},indent=2)+'\n');print('PASS 54 native room views: moving snow only in the 8 confirmed exterior views, 71 strict glass cells; no pixels outside the glass masks')
