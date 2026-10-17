# Optional online AI environment-art server

Offline standalone HTML does not require this server. The website game always uses bundled base artwork; an online provider can supply extra atmosphere as a translucent overlay. Doors, objects, and puzzles are rendered separately from fixed game data.

Run `python server/ward_art_server.py` from the project directory for local hosting. It serves the same game over HTTP at http://127.0.0.1:8787/. With no provider configured, `/api/ward-art` returns HTTP 503 and the game stays on local graphics.

To enable AI art, set `WARD_ART_UPSTREAM_URL` to a **compatible image-generation gateway** you operate and, optionally, `WARD_ART_UPSTREAM_KEY`. The gateway accepts `{ "prompt": "...", "room": "...", "seed": "...", "size": "1536x1024" }` and returns an `image_base64`, a `data[0].b64_json`, or an HTTPS `image_url`. The server caches generated images by seed, room, and power state, serving them from the same origin.

This is an integration adapter, not an included AI generation model or an already configured paid service. Before public deployment add rate limits, authentication, size/content validation, TLS, output review, and operating-budget controls. Never place API keys in the browser build.
