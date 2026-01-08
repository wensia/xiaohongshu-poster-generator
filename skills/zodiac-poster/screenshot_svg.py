#!/usr/bin/env python3
"""
SVG 截图脚本 - 将 SVG 转换为 PNG
使用 Playwright + Canvas API 实现精确截图
"""

import os
import base64
import asyncio
from playwright.async_api import async_playwright


def create_canvas_html(svg_content, width=1080, height=1440, scale=2):
    """创建使用 Canvas API 渲染 SVG 的 HTML"""
    out_width = width * scale
    out_height = height * scale
    # SVG 内容需要 base64 编码以避免转义问题
    svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode('ascii')

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{ background: transparent; }}
        canvas {{ display: block; }}
    </style>
</head>
<body>
    <canvas id="canvas" width="{out_width}" height="{out_height}"></canvas>
    <script>
        async function render() {{
            const svgB64 = "{svg_b64}";
            // 正确处理 UTF-8 编码
            const binaryString = atob(svgB64);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {{
                bytes[i] = binaryString.charCodeAt(i);
            }}
            const svgContent = new TextDecoder('utf-8').decode(bytes);

            const blob = new Blob([svgContent], {{type: 'image/svg+xml;charset=utf-8'}});
            const url = URL.createObjectURL(blob);

            const img = new Image();
            img.width = {out_width};
            img.height = {out_height};

            await new Promise((resolve, reject) => {{
                img.onload = resolve;
                img.onerror = reject;
                img.src = url;
            }});

            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, {out_width}, {out_height});

            URL.revokeObjectURL(url);

            // 返回 base64 PNG 数据
            window.pngData = canvas.toDataURL('image/png');
            window.renderDone = true;
        }}
        render();
    </script>
</body>
</html>"""


async def screenshot_svg_async(svg_path, output_path, scale=2):
    """使用 Playwright + Canvas API 截图"""
    width = 1080
    height = 1440
    out_width = width * scale
    out_height = height * scale

    # 读取 SVG 内容
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    html_content = create_canvas_html(svg_content, width, height, scale)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': out_width, 'height': out_height})

        # 加载 HTML
        await page.set_content(html_content)

        # 等待渲染完成
        await page.wait_for_function('window.renderDone === true', timeout=10000)

        # 获取 PNG 数据
        png_data_url = await page.evaluate('window.pngData')

        await browser.close()

    # 解码并保存 PNG
    png_b64 = png_data_url.split(',')[1]
    png_bytes = base64.b64decode(png_b64)

    with open(output_path, 'wb') as f:
        f.write(png_bytes)

    print(f"✅ {os.path.basename(output_path)} ({out_width}x{out_height})")
    return True


def screenshot_svg(svg_path, output_path, scale=2):
    """同步包装器"""
    return asyncio.run(screenshot_svg_async(svg_path, output_path, scale))


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.join(base_dir, "assets/templates/destined-bond/examples")

    files = ['01_cover', '02_page', '03_end']

    print("📸 开始截图 (3:4 比例, 2x 分辨率)...")

    for name in files:
        svg_path = os.path.join(examples_dir, f"{name}.svg")
        png_path = os.path.join(examples_dir, f"{name}.png")

        if os.path.exists(svg_path):
            screenshot_svg(svg_path, png_path, scale=2)
        else:
            print(f"⚠️ 未找到: {svg_path}")

    print("✨ 完成!")


if __name__ == "__main__":
    main()
