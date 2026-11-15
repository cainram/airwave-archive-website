import asyncio
from playwright.async_api import async_playwright
IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
# Only two "Continue listening" cards (the others are hidden for the picture).
CSS = "footer.footer{display:none !important} .continue-list > .continue-item:nth-child(n+3){display:none !important}"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for scheme in ("light", "dark"):
            m = await (await b.new_context(viewport={"width": 393, "height": 852}, device_scale_factor=3, is_mobile=True,
                                           has_touch=True, color_scheme=scheme, user_agent=IPHONE)).new_page()
            await m.goto("http://localhost:8090/", wait_until="networkidle")
            await m.add_style_tag(content=CSS)
            await m.wait_for_timeout(400)
            print(scheme, await m.locator(".continue-item:visible").count(), "cards")
            await m.screenshot(path=f"/shots/mobile-home-{scheme}.png")
        await b.close()
asyncio.run(main())
