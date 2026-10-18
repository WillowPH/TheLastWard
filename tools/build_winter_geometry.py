"""Embed the reviewed coordinates; the runtime never guesses a missing hotspot."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
geometry=json.loads((root/'data/winter_geometry.json').read_text())
(root/'js/winter_geometry.js').write_text('''/* Explicit per-room coordinates. Edit data/winter_geometry.json and run
   python tools/build_winter_geometry.py; no generic runtime placement. */
(function(){'use strict';
const geometry='''+json.dumps(geometry,separators=(',',':'))+''';
for(const [room,g]of Object.entries(geometry)){const bp=WardScenes[room];Object.assign(bp.views.front.doors,g.doors);bp.threat=structuredClone(g.threat);for(const [id,values]of Object.entries(g.fixtures)){const f=bp.fixtures.find(f=>f.id===id);if(f)Object.assign(f,structuredClone(values));}}
window.WardGeometryCalibration=geometry;
})();
''')
