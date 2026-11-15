# How the screenshots were made

The pictures on the site come from a throwaway copy of Airwave Archive
filled with **invented** series (abstract generated artwork, silent audio).

1. `make_demo.py` builds the demo library and three messy inbox files. Run it
   inside the app's Docker image (it has ffmpeg and Pillow).
2. Start a throwaway copy of the app on port 8090 with that library, its own
   data folder and inbox. Give the series genres, start a few episodes, mark
   some played, and make and publish a feed for "Night Signal". For the
   calendar picture, many episodes were moved into March 2024 in the demo's
   own database.
3. `screenshots.py` and `screenshot_inbox.py` take the pictures with
   Playwright (the `mcr.microsoft.com/playwright/python` image, run with
   `--network host`).
4. The PNGs are converted to WebP (desktop 2400 px wide, phone 900 px) into
   `images/`.

`tools/` isn't served as part of the site.
