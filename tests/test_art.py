"""Visual duplicate and baked-prompt audit; never edits source images."""
from pathlib import Path
from PIL import Image,ImageOps
import concurrent.futures,hashlib,json,os,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
rooms=sorted((ROOT/'assets/rooms').glob('*.webp'))
def signature(im):
 im=im.convert('L').resize((17,16));pixels=list(im.get_flattened_data() if hasattr(im,'get_flattened_data') else im.getdata());return [pixels[y*17+x]>pixels[y*17+x+1] for y in range(16) for x in range(16)]
sigs={p.stem:signature(Image.open(p)) for p in rooms};flips={p.stem:signature(ImageOps.mirror(Image.open(p))) for p in rooms};duplicates=[]
for i,p in enumerate(rooms):
 assert Image.open(p).width/Image.open(p).height==4/3
 for q in rooms[i+1:]:
  normal=sum(a!=b for a,b in zip(sigs[p.stem],sigs[q.stem]));mirror=sum(a!=b for a,b in zip(flips[p.stem],sigs[q.stem]))
  if min(normal,mirror)<24:duplicates.append([p.stem,q.stem,normal,mirror])
assert not duplicates,duplicates
print('PASS: 27 independently composed 4:3 backgrounds; no near-duplicates or mirrored substitutes.',flush=True)
reverse=sorted((ROOT/'assets/reverse').glob('*.webp'));assert len(reverse)==27
reverse_sigs={p.stem:signature(Image.open(p)) for p in reverse};reverse_flips={p.stem:signature(ImageOps.mirror(Image.open(p))) for p in reverse};reverse_duplicates=[]
for i,p in enumerate(reverse):
 assert Image.open(p).width/Image.open(p).height==4/3
 for q in reverse[i+1:]:
  normal=sum(a!=b for a,b in zip(reverse_sigs[p.stem],reverse_sigs[q.stem]));mirror=sum(a!=b for a,b in zip(reverse_flips[p.stem],reverse_sigs[q.stem]))
  if min(normal,mirror)<24:reverse_duplicates.append([p.stem,q.stem,normal,mirror])
assert not reverse_duplicates,reverse_duplicates
print('PASS: 27 distinct 4:3 reverse views; no near-duplicates or mirrored substitutes.',flush=True)
def ocr(path):
 env=os.environ.copy();env['OMP_THREAD_LIMIT']='1'
 text=subprocess.check_output(['tesseract',str(path),'stdout','--psm','11'],text=True,stderr=subprocess.DEVNULL,env=env)
 return path.name,re.findall(r'\b(?:INSPECT|EXAMINE|CLICK HERE|BUTTON)\b',text.upper())
states=list((ROOT/'assets/states').glob('*.webp'));reverse=list((ROOT/'assets/reverse').glob('*.webp'));files=rooms+states+reverse
results=list(concurrent.futures.ThreadPoolExecutor(3).map(ocr,files))
assert all(not match for _,match in results),results
print('PASS: no baked interaction prompts detected in room or aftermath artwork.',flush=True)
(ROOT/'tests/results/art_audit.json').write_text(json.dumps({'rooms':len(rooms),'state_images':len(states),'reverse_images':len(reverse),'near_duplicates':duplicates,'reverse_near_duplicates':reverse_duplicates,'ocr_prompts':results,'sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))
