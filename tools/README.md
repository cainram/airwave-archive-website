# How the screenshots were made

The pictures on the site come from a throwaway copy of Airwave Archive
filled with **invented** series (abstract generated artwork, silent audio).

1. `make_demo.py` builds the demo library and three messy inbox files. Run it
   inside the app's Docker image (it has ffmpeg and Pillow).
   `make_covers.py` then draws the ten series' covers (each its own idea, a
   nod to old-time radio: a tuning dial, sound waves, a studio microphone, a
   lighthouse…); they replace each series folder's `cover.jpg`, and the app
   is rescanned.
2. Start a throwaway copy of the app on port 8090 with that library, its own
   data folder and inbox. Give the series genres, start a few episodes, mark
   some played, and make and publish a feed for "Night Signal". For the
   calendar picture, many episodes were moved into March 2024 in the demo's
   own database.
3. `screenshots.py`, `screenshot_inbox.py` and `screenshot_mobile_home.py`
   (the phone's home page, with only two "Continue listening" cards) take the pictures with
   Playwright (the `mcr.microsoft.com/playwright/python` image, run with
   `--network host`).
4. The PNGs are converted to WebP (desktop 2400 px wide, phone 900 px) into
   `images/`.

`tools/` isn't served as part of the site.
