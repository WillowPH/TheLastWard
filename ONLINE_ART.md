# Optional atmospheric texture service

The game is complete offline. Automatic/Online modes may request `/api/ward-art` from
the optional Python server. No provider is configured or claimed live in this build.

An online response supplies an abstract dust/light texture. The client accepts only a
same-origin image and confines it to a faint noninteractive ceiling area. It cannot
replace a room background, relocate a doorway, cover a clue or change collision targets.
Failures and connection loss leave local art and gameplay available immediately.

Configure provider credentials only on the server, as described in server/README.md.
Never put a provider key into the frontend, a downloadable HTML, or a save record.
