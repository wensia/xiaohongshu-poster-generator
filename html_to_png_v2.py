#!/usr/bin/env python3
"""
使用 Playwright 将 HTML 转换为 PNG
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

def convert_html_to_png(html_path: Path, output_path: Path):
    """将单个 HTML 文件转换为 PNG"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1080, "height": 1440},
            device_scale_factor=2  # 2x 导出，实际像素 2160x2880
        )
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        # 等待字体加载
        page.wait_for_timeout(500)
        page.locator(".poster").screenshot(path=str(output_path))
        browser.close()

def main():
    base_dir = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/05")

    dirs = [
        "射手座_轻计划学习法_性格独白风_v2",
        "射手座_边界感练习_性格独白风_v2",
        "射手座_独处方式_性格独白风_v2"
    ]

    for dir_name in dirs:
        output_dir = base_dir / dir_name
        html_files = sorted(output_dir.glob("*.html"))

        print(f"\n📁 处理: {dir_name}")

        for html_file in html_files:
            png_file = html_file.with_suffix(".png")
            print(f"  转换: {html_file.name} → {png_file.name}")
            convert_html_to_png(html_file, png_file)

        print(f"  ✅ 完成！共 {len(html_files)} 张图片")

if __name__ == "__main__":
    main()
