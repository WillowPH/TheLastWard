"""Create a small Python-free Windows launcher patch for an existing project."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'downloads/The_Last_Ward_Windows_Launcher.zip'
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
 for name in ['START_GAME.exe','START_GAME.bat','launcher/GO_LICENSE.txt']:z.write(ROOT/name,name)
 z.writestr('READ_ME_FIRST.txt','THE LAST WARD - WINDOWS LAUNCHER FIX\n\nExtract START_GAME.exe and START_GAME.bat into your existing extracted game folder, beside index.html.\nDouble-click START_GAME.exe. Keep its window open while playing.\nNo Python or internet connection is needed.\nDo not open index.html directly. Keep all original asset folders in place.\nRequires Windows 10/11 x64-compatible and a modern WebGL browser.\n')
 with_check=z.namelist()
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 for name in ['START_GAME.exe','START_GAME.bat']:assert z.read(name)==(ROOT/name).read_bytes()
print(OUT.name,OUT.stat().st_size,'bytes; launcher files verified')
