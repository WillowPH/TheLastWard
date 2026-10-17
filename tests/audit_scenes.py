from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/chapter1_scenes.json').read_text());fail=[]
for room,bp in d.items():
 regions=[('door:'+k,v) for k,v in bp['doors'].items()]+[(f['id'],f['rect']) for f in bp['fixtures']]
 for i,(a,A) in enumerate(regions):
  x,y,w,h=A
  if x-w/2<0 or x+w/2>100 or y-h/2<0 or y+h/2>100:fail.append((room,a,'outside'))
  for b,B in regions[i+1:]:
   dx=min(x+w/2,B[0]+B[2]/2)-max(x-w/2,B[0]-B[2]/2);dy=min(y+h/2,B[1]+B[3]/2)-max(y-h/2,B[1]-B[3]/2)
   if dx>.05 and dy>.05:fail.append((room,a,b,round(dx*dy,2)))
print(json.dumps(fail,indent=2));print(len(d),'rooms',sum(len(r['fixtures']) for r in d.values()),'fixtures')
if fail:raise SystemExit(1)
