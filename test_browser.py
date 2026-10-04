import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://localhost:8501')
        await page.wait_for_timeout(5000)
        text = await page.evaluate("document.body.innerText")
        with open('page_error.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        await browser.close()

asyncio.run(main())
