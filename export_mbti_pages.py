#!/usr/bin/env python3
"""
导出MBTI模板的所有页面为2160x2880px图片
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# 页面名称列表
PAGES = [
    '01_cover',
    '02_intro',
    '03_dim_ei',
    '04_dim_sn',
    '05_dim_tf',
    '06_dim_jp',
    '07_analysts',
    '08_others',
    '09_end',
]

async def export_pages():
    # 输出目录
    output_dir = Path(__file__).parent / "output" / "mbti_claude_brand"
    output_dir.mkdir(parents=True, exist_ok=True)

    # HTML文件路径
    html_path = Path(__file__).parent / "mbti_export.html"

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for i, page_name in enumerate(PAGES):
            print(f"📸 正在导出 {page_name}...")

            # 创建新页面，设置2倍缩放
            page = await browser.new_page(
                viewport={'width': 1080, 'height': 1440},
                device_scale_factor=2  # 2倍分辨率，输出2160x2880
            )

            # 导航到对应页面
            url = f"file://{html_path}?page={i}"
            await page.goto(url, wait_until='networkidle')

            # 等待字体加载
            await page.wait_for_timeout(2000)

            # 截图
            output_path = output_dir / f"{page_name}.png"
            await page.screenshot(
                path=str(output_path),
                clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1440}
            )

            print(f"   ✅ 已保存: {output_path}")
            await page.close()

        await browser.close()

    print(f"\n🎉 全部完成！共导出 {len(PAGES)} 张图片")
    print(f"📁 输出目录: {output_dir}")

if __name__ == "__main__":
    asyncio.run(export_pages())
