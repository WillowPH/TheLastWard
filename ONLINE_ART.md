# Optional AI-enhanced environments: integration contract

The browser game has a **complete offline baseline**. The `online_art.js` enhancement is off by default until a configured backend is available. No runtime AI, provider credentials or internet are required for the local edition.

If you deploy an image generation server, enable the option through `WardArt.update(true, '/api/ward-art')` (or a same-origin settings UI). The game POSTs JSON with room, roomName, seed, chapter, power state and style. The endpoint must return JSON such as `{ "image_url":"https://example.com/cache/room-123.png" }`. This image is cosmetic only. All doors, hotspots, room descriptions and puzzle logic remain drawn by the local scene engine. Generation is time-limited and cannot delay movement.

**Important:** Real AI generation is NOT wired to a specific provider or paid service. You'll need to deploy and configure your own backend and persistent image host before online art works. The browser bundle contains no secret API key. The current in-memory cache avoids repeat requests during the session; production persistent caching of remote imagery must be implemented server-side or through a site's PWA cache strategy.

A standalone local HTML file uses its embedded artwork. The hosted version can be installed offline once its assets have been cached through its service worker. When online art fails, local artwork renders without depending on the failed request.
