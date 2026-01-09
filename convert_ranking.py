#!/usr/bin/env python3
"""Convert zodiac ranking SVG to PNG."""

import asyncio
import os
from playwright.async_api import async_playwright

SVG_PATH = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09/星座花心排行榜/01_cover.svg"
PNG_PATH = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09/星座花心排行榜/01_cover.png"


async def main():
    with open(SVG_PATH, "r", encoding="utf-8") as f:
        svg_content = f.read()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; }}
            body {{ background: white; }}
        </style>
    </head>
    <body>
        {svg_content}
    </body>
    </html>
    """
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1200, "height": 1600},
            device_scale_factor=2,
        )
        page = await context.new_page()
        
        await page.set_content(html_content)
        await page.wait_for_timeout(2000)
        
        svg_element = await page.query_selector("svg")
        await svg_element.screenshot(path=PNG_PATH, scale="device", type="png")
        
        await browser.close()
    
    size = os.path.getsize(PNG_PATH)
    print(f"Created: {PNG_PATH}")
    print(f"Size: {size:,} bytes")


if __name__ == "__main__":
    asyncio.run(main())
