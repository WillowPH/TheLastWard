# Optional online AI environment-art server

The native Windows game and offline standalone HTML do not require Python or this server. Every mode uses complete bundled room artwork and fixed doors, objects, and puzzles. An online provider can add a faint atmospheric texture clipped to the ceiling area.

Run `python server/ward_art_server.py` from the project directory for local hosting. It serves the same game over HTTP at http://127.0.0.1:8787/. The default Online preference uses `/data/art_service.json` to discover whether a provider is configured. This server returns HTTP 200 with `available: false` when unconfigured; `/api/ward-art` then returns HTTP 503 and the game stays on bundled graphics. The native build includes an unavailable-service manifest and uses bundled graphics by default.

To enable AI art, set `WARD_ART_UPSTREAM_URL` to a **compatible image-generation gateway** you operate and, optionally, `WARD_ART_UPSTREAM_KEY`. The gateway accepts `{ "prompt": "...", "room": "...", "seed": "...", "size": "1536x1024" }` and returns an `image_base64`, a `data[0].b64_json`, or an HTTPS `image_url`. The server caches generated images by seed, room, and power state, serving them from the same origin. Concurrent requests for the same image share one generation call within this server process, and completed files are published atomically. Run one server process for this cache; multiple processes need a shared lock or a gateway that deduplicates requests.

This is an integration adapter, not an included AI generation model or an already configured paid service. Before public deployment add rate limits, authentication, size/content validation, TLS, output review, and operating-budget controls. Never place API keys in the browser build.

Run local regression tests with `python -m unittest discover -s server -v`. They use temporary game roots and a local mock gateway; no paid provider requests are made.
