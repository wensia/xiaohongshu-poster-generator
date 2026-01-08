#!/usr/bin/env python3
"""
SVG/HTML 截图工具 - 使用 Playwright + Canvas API 实现精确 2x 截图

使用方法:
    from utils.screenshot import svg_to_png, html_to_png

    # SVG 转 PNG (2x 分辨率)
    svg_to_png('input.svg', 'output.png')

    # HTML 转 PNG (2x 分辨率)
    html_to_png('input.html', 'output.png')

    # 批量转换
    batch_svg_to_png(['1.svg', '2.svg'], 'output_dir/')
"""

import os
import base64
import asyncio
from playwright.async_api import async_playwright


# 默认画布尺寸 (小红书 3:4 比例)
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1440
DEFAULT_SCALE = 2  # 2x 分辨率


def _create_canvas_html(svg_content: str, width: int, height: int, scale: int) -> str:
    """创建使用 Canvas API 渲染 SVG 的 HTML"""
    out_width = width * scale
    out_height = height * scale
    # SVG 内容 base64 编码以避免转义问题
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


async def _svg_to_png_async(
    svg_path: str,
    output_path: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE
) -> bool:
    """异步将 SVG 转换为 PNG"""
    out_width = width * scale
    out_height = height * scale

    # 读取 SVG 内容
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    html_content = _create_canvas_html(svg_content, width, height, scale)

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

    return True


async def _html_to_png_async(
    html_path: str,
    output_path: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE,
    wait_time: int = 2500
) -> bool:
    """异步将 HTML 转换为 PNG (使用 Canvas API 导出)"""
    out_width = width * scale
    out_height = height * scale

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': out_width, 'height': out_height})

        # 打开 HTML 文件
        await page.goto(f'file://{os.path.abspath(html_path)}')

        # 等待字体加载
        await page.wait_for_timeout(wait_time)

        # 注入 Canvas 导出脚本
        png_data_url = await page.evaluate(f'''() => {{
            return new Promise((resolve, reject) => {{
                const svg = document.querySelector('svg');
                if (!svg) {{
                    reject(new Error('No SVG found'));
                    return;
                }}

                // Clone SVG
                const svgClone = svg.cloneNode(true);
                svgClone.setAttribute('width', '{out_width}');
                svgClone.setAttribute('height', '{out_height}');

                const svgString = new XMLSerializer().serializeToString(svgClone);
                const blob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
                const url = URL.createObjectURL(blob);

                const img = new Image();
                img.onload = () => {{
                    const canvas = document.createElement('canvas');
                    canvas.width = {out_width};
                    canvas.height = {out_height};
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, {out_width}, {out_height});
                    URL.revokeObjectURL(url);
                    resolve(canvas.toDataURL('image/png'));
                }};
                img.onerror = reject;
                img.src = url;
            }});
        }}''')

        await browser.close()

    # 解码并保存 PNG
    png_b64 = png_data_url.split(',')[1]
    png_bytes = base64.b64decode(png_b64)

    with open(output_path, 'wb') as f:
        f.write(png_bytes)

    return True


def svg_to_png(
    svg_path: str,
    output_path: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE
) -> bool:
    """
    将 SVG 文件转换为 PNG 图片

    参数:
        svg_path: SVG 文件路径
        output_path: 输出 PNG 文件路径
        width: 画布宽度 (默认 1080)
        height: 画布高度 (默认 1440)
        scale: 缩放倍数 (默认 2, 即 2x 分辨率)

    返回:
        bool: 是否成功
    """
    return asyncio.run(_svg_to_png_async(svg_path, output_path, width, height, scale))


def html_to_png(
    html_path: str,
    output_path: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE,
    wait_time: int = 2500
) -> bool:
    """
    将 HTML 文件转换为 PNG 图片 (HTML 中需包含 SVG)

    参数:
        html_path: HTML 文件路径
        output_path: 输出 PNG 文件路径
        width: 画布宽度 (默认 1080)
        height: 画布高度 (默认 1440)
        scale: 缩放倍数 (默认 2, 即 2x 分辨率)
        wait_time: 等待字体加载时间 (毫秒, 默认 2500)

    返回:
        bool: 是否成功
    """
    return asyncio.run(_html_to_png_async(html_path, output_path, width, height, scale, wait_time))


def batch_svg_to_png(
    svg_paths: list,
    output_dir: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    scale: int = DEFAULT_SCALE
) -> list:
    """
    批量将 SVG 文件转换为 PNG

    参数:
        svg_paths: SVG 文件路径列表
        output_dir: 输出目录
        width: 画布宽度
        height: 画布高度
        scale: 缩放倍数

    返回:
        list: 成功生成的 PNG 文件路径列表
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for svg_path in svg_paths:
        filename = os.path.splitext(os.path.basename(svg_path))[0] + '.png'
        output_path = os.path.join(output_dir, filename)

        try:
            svg_to_png(svg_path, output_path, width, height, scale)
            results.append(output_path)
            print(f"✅ {filename} ({width * scale}x{height * scale})")
        except Exception as e:
            print(f"❌ {filename}: {e}")

    return results


# CLI 入口
if __name__ == "__main__":
    import sys
    import glob

    if len(sys.argv) < 2:
        print("Usage: python screenshot.py <svg_file_or_pattern> [output_dir]")
        print("Example: python screenshot.py '*.svg' ./output")
        sys.exit(1)

    pattern = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'

    svg_files = glob.glob(pattern)
    if not svg_files:
        print(f"No files found matching: {pattern}")
        sys.exit(1)

    print(f"📸 开始截图 (3:4 比例, 2x 分辨率)...")
    results = batch_svg_to_png(svg_files, output_dir)
    print(f"✨ 完成! 共 {len(results)} 张")
