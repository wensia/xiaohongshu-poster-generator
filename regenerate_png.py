#!/usr/bin/env python3
"""Regenerate PNG files from SVG using Playwright."""

import asyncio
import os
import base64
from playwright.async_api import async_playwright

SVG_DIR = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09/射手遇到双鱼"

# SVG files to convert
SVG_FILES = [
    "01_cover.svg",
    "02_page.svg",
    "03_page.svg",
    "04_page.svg",
    "05_page.svg",
    "06_page.svg",
    "07_end.svg",
]


async def svg_to_png(page, svg_path, png_path):
    """Convert SVG to PNG at 2x resolution."""
    # Read SVG content
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
    
    # Create HTML with the SVG
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
    
    # Set content and wait for fonts to load
    await page.set_content(html_content)
    await page.wait_for_timeout(2000)  # Wait for fonts
    
    # Get the SVG element
    svg_element = await page.query_selector("svg")
    if not svg_element:
        raise Exception("SVG element not found")
    
    # Take screenshot at 2x scale
    await svg_element.screenshot(
        path=png_path,
        scale="device",
        type="png",
    )
    
    return png_path


async def main():
    print("Starting PNG regeneration...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1200, "height": 1600},
            device_scale_factor=2,  # 2x resolution
        )
        page = await context.new_page()
        
        for svg_file in SVG_FILES:
            svg_path = os.path.join(SVG_DIR, svg_file)
            png_file = svg_file.replace(".svg", ".png")
            png_path = os.path.join(SVG_DIR, png_file)
            
            if not os.path.exists(svg_path):
                print(f"SKIP: {svg_file} not found")
                continue
            
            print(f"Converting: {svg_file} -> {png_file}")
            try:
                await svg_to_png(page, svg_path, png_path)
                # Verify file size
                size = os.path.getsize(png_path)
                print(f"  Done: {size:,} bytes")
            except Exception as e:
                print(f"  ERROR: {e}")
        
        await browser.close()
    
    print("\nRegeneration complete!")


if __name__ == "__main__":
    asyncio.run(main())
