#!/usr/bin/env python3
"""
将HTML文件批量转换为PNG图片
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def html_to_png(html_dir: Path):
    """将目录中的HTML文件转换为PNG"""
    html_files = sorted(html_dir.glob("*.html"))
    if not html_files:
        print(f"❌ 未找到HTML文件: {html_dir}")
        return []

    png_files = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1440})

        for html_file in html_files:
            png_file = html_file.with_suffix(".png")
            file_url = f"file://{html_file.absolute()}"

            await page.goto(file_url)
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(0.5)  # 等待字体加载

            await page.screenshot(path=str(png_file), full_page=False)
            print(f"✅ {html_file.name} → {png_file.name}")
            png_files.append(png_file)

        await browser.close()

    return png_files

async def main():
    import sys
    if len(sys.argv) > 1:
        html_dir = Path(sys.argv[1])
    else:
        html_dir = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/10/双子座理想的生活")

    if not html_dir.exists():
        print(f"❌ 目录不存在: {html_dir}")
        return

    png_files = await html_to_png(html_dir)
    print(f"\n📁 完成！共生成 {len(png_files)} 张图片")
    print(f"目录: {html_dir}")

if __name__ == "__main__":
    asyncio.run(main())
