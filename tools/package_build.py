"""Create a self-contained offline HTML and editable ZIP without external packages."""
import base64
import json
import mimetypes
from pathlib import Path
import re
import sys
import zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent/'artifacts'
OUT.mkdir(parents=True,exist_ok=True)
def data(path):
    mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
assets={p.relative_to(ROOT).as_posix():data(p) for folder in ['assets','audio'] for p in (ROOT/folder).rglob('*') if p.suffix.lower() in ['.png','.jpg','.wav']}
html=(ROOT/'index.html').read_text()
# System font fallback preserves a fully local standalone edition.
html=re.sub(r'<link[^>]+https://fonts\.[^>]+>','',html)
def css(match):
    p=ROOT/match[1]
    def local_url(m):
        raw=m[1].strip('"\'')
        f=(p.parent/raw).resolve()
        return 'url("'+data(f)+'")' if f.is_file() else m[0]
    return '<style>'+re.sub(r'url\(([^)]+)\)',local_url,p.read_text())+'</style>'
html=re.sub(r'<link rel="stylesheet" href="([^"]+)">',css,html)
bootstrap='<script>window.WardEmbeddedAssets='+json.dumps(assets)+';window.LW_AUDIO_ASSETS='+json.dumps({k:assets[v] for k,v in {'door':'audio/door.wav','reload':'audio/reload.wav','shot':'audio/gunshot.wav'}.items()})+';</script>'
html=html.replace('<script src="js/bootstrap.js">',bootstrap+'<script src="js/bootstrap.js">')
html=re.sub(r'<script src="([^"]+)"></script>',lambda m:'<script>\n'+(ROOT/m[1]).read_text().replace('</script','<\\/script')+'\n</script>',html)
html=re.sub(r'<script>if\(location.protocol.startsWith\("http"\).*?</script>','',html)
standalone=OUT/'The_Last_Ward_Phase_1_Fixed.html'
standalone.write_text(html)
archive=OUT/'The_Last_Ward_Phase_1_Fixed_Project.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or any(x in p.relative_to(ROOT).parts for x in ['.git','__pycache__']):continue
        z.write(p,'The_Last_Ward_Project/'+p.relative_to(ROOT).as_posix())
print(standalone)
print(archive)
