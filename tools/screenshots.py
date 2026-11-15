import asyncio
from playwright.async_api import async_playwright
B = "http://localhost:8090"; OUT = "/shots"
HIDE = "footer.footer{display:none !important}"
IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"

async def go(page, url):
    await page.goto(B + url, wait_until="networkidle")
    await page.add_style_tag(content=HIDE)
    await page.wait_for_timeout(400)

async def play(page):
    await page.click(".actions [data-play]", timeout=3000)
    await page.wait_for_timeout(1500)
    await page.evaluate("document.getElementById('player-audio').pause()")
    await page.wait_for_timeout(300)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for scheme in ("light", "dark"):
            ctx = await b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, color_scheme=scheme)
            d = await ctx.new_page()
            await go(d, "/"); await d.screenshot(path=f"{OUT}/desktop-home-{scheme}.png")
            await go(d, "/series"); await d.screenshot(path=f"{OUT}/desktop-series-{scheme}.png", clip={"x": 0, "y": 0, "width": 1440, "height": 720})
            await d.set_viewport_size({"width": 1440, "height": 1300})
            await go(d, "/calendar?year=2024&month=3")
            grid = await d.locator(".month-grid").bounding_box()
            top = await d.locator("h1").bounding_box()
            await d.screenshot(path=f"{OUT}/desktop-calendar-{scheme}.png",
                               clip={"x": grid["x"] - 28, "y": top["y"] - 24, "width": grid["width"] + 56, "height": grid["y"] + grid["height"] - top["y"] + 48})
            await d.set_viewport_size({"width": 1440, "height": 900})
            await go(d, "/inbox"); await d.screenshot(path=f"{OUT}/desktop-inbox-{scheme}.png")
            m = await (await b.new_context(viewport={"width": 393, "height": 852}, device_scale_factor=3, is_mobile=True,
                                           has_touch=True, color_scheme=scheme, user_agent=IPHONE)).new_page()
            await go(m, "/"); await m.screenshot(path=f"{OUT}/mobile-home-{scheme}.png")
            await go(m, "/series"); await m.click(".genre-drop summary"); await m.wait_for_timeout(300)
            await m.screenshot(path=f"{OUT}/mobile-genres-{scheme}.png")
            await go(m, "/feeds/1")
            await m.evaluate("document.getElementById('feed-address').value = 'https://archive.home.example/feeds/k3Jv9…/feed.xml'")
            await m.screenshot(path=f"{OUT}/mobile-feed-{scheme}.png")
            await go(m, "/files/28"); await play(m); await m.screenshot(path=f"{OUT}/mobile-episode-{scheme}.png")
        await b.close()
asyncio.run(main())
