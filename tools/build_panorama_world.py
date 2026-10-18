"""Validate the hand-authored panoramic world and emit its browser data module."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
world=json.loads((ROOT/'data/panorama360_world.json').read_text());plan=json.loads((ROOT/'data/panorama360_plan.json').read_text());assert set(world)==set(plan) and len(world)==27
seen=set()
for room,v in world.items():
 assert v['reviewed'],f'Unreviewed room: {room}'
 assert set(v['fixtures'])=={f['id'] for f in plan[room]['fixtures']},room
 assert set(v['doors'])=={d['id'] for d in plan[room]['doors']},room
 path=ROOT/v['asset'];assert path.is_file(),path
 digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest not in seen,f'Reused panorama: {room}';seen.add(digest)
 for kind in ['fixtures','doors']:
  for name,entry in v[kind].items():
   assert entry['reviewed'],f'Unreviewed {room}/{name}'
   x,y,w,h=entry['rect'];assert 0<=x<=100 and 0<=y<=100 and 0<w<100 and 0<h<100,(room,name,entry['rect'])
 for state,path in v.get('states',{}).items():
  assert (ROOT/path).is_file(),path;assert v['stateMasks'].get(state),(room,state)
 for poly in v.get('glazing',[]):assert len(poly)>=3 and all(0<=x<=100 and 0<=y<=100 for x,y in poly),(room,poly)
(ROOT/'js/panorama360_world.js').write_text('window.WardPanoramaWorld='+json.dumps(world,separators=(',',':'))+';\n')
floor=json.loads((ROOT/'data/floorplan.json').read_text());assert set(floor['rooms'])==set(world);cells={}
for room,points in floor['rooms'].items():
 for point in points:
  key=tuple(point);assert key not in cells,(room,key);cells[key]=room
for room,v in world.items():
 for d in v['doors'].values():
  target=d['to'];assert any(cells.get((x+dx,y+dy))==target for x,y in floor['rooms'][room] for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]),(room,target)
(ROOT/'js/floorplan_data.js').write_text('window.WardArchitecturalPlan='+json.dumps(floor,separators=(',',':'))+';\n')
print('PASS 27 unique panoramas, all authored targets/states, and physical floor-plan adjacency')
