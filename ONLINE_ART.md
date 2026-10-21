# Optional atmospheric texture service

The game is complete offline. Online is the default preference and discovers an
optional service through `/data/art_service.json` before requesting `/api/ward-art`.
No provider or credentials are included, and no service is claimed live in this build.
The normal native Windows build uses the bundled unavailable-service manifest and
complete local artwork; it does not require Python.

An online response supplies an abstract dust/light texture. The client accepts only a
same-origin image and confines it to a faint noninteractive ceiling area. It cannot
replace a room background, relocate a doorway, cover a clue or change collision targets.
Failures and connection loss leave local art and gameplay available immediately.

Configure provider credentials only on the server, as described in server/README.md.
Never put a provider key into the frontend, a downloadable HTML, or a save record.
