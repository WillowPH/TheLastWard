"""Small native-view update for the previously delivered complete Chapter 1 project."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'downloads/The_Last_Ward_Visual_Update.zip'
files=[ROOT/n for n in ['index.html','START_GAME.exe','START_GAME.bat','START_HERE.txt','README.md','VALIDATION.md','sw.js','launcher/GO_LICENSE.txt','docs/ROOM_VIEW_SETUP.md','docs/REVISION_V7.md','docs/REVISION_V6.md','docs/REVISION_2026-10-19.md']]
for folder in ['js','css','data','assets/room_views','assets/panoramic360/materials','assets/items','audio']:
 files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(set(files)):z.write(f,f.relative_to(ROOT).as_posix())
 z.writestr('UPDATE_INSTRUCTIONS.txt','THE LAST WARD - NATIVE ROOM VIEW UPDATE\n\nExtract this update into your EXISTING extracted game folder, the one containing index.html.\nAllow it to replace the matching files. Keep all original assets and audio folders.\nThen double-click START_GAME.exe. No Python is needed on Windows.\nExisting v5 and v6 saves can continue in the same browser/local port; a new game also works.\n\nClick objects. Drag sideways to see the other room view.\nPause stays below Options in the left menu, including while a dialog is open.\nHints stay in Options. Select an item in the right inventory to use, combine, inspect or discard it.\nIf you do not already have the complete Chapter 1 project, download the complete Project ZIP instead.\n')
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 for f in files:assert z.read(f.relative_to(ROOT).as_posix())==f.read_bytes()
print(OUT.name,OUT.stat().st_size,'bytes; all update files verified')
