import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for scheme in ("light", "dark"):
            pg = await (await b.new_context(viewport={"width": 1440, "height": 1400}, device_scale_factor=2, color_scheme=scheme)).new_page()
            await pg.goto("http://localhost:8090/inbox", wait_until="networkidle")
            await pg.add_style_tag(content="footer.footer{display:none !important}")
            head = await pg.locator("h2", has_text="Waiting").bounding_box()
            main = await pg.locator("main").bounding_box()
            await pg.screenshot(path=f"/shots/desktop-inbox-{scheme}.png",
                                clip={"x": main["x"], "y": head["y"] - 30, "width": main["width"], "height": main["width"] * 0.625})
        await b.close()
asyncio.run(main())
