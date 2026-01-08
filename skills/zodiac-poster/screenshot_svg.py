#!/usr/bin/env python3
"""
SVG 截图脚本 - 将 SVG 转换为 PNG
使用 HTML 包装器确保 SVG 正确填充整个画布
"""

import os
import subprocess
import tempfile

def create_html_wrapper(svg_path, width=1080, height=1440):
    """创建 HTML 包装器，确保 SVG 正确填充"""
    svg_url = f"file://{os.path.abspath(svg_path)}"
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; }}
        html, body {{
            width: {width}px;
            height: {height}px;
            overflow: hidden;
        }}
        img {{
            width: {width}px;
            height: {height}px;
            display: block;
        }}
    </style>
</head>
<body>
    <img src="{svg_url}" width="{width}" height="{height}">
</body>
</html>"""


def screenshot_svg(svg_path, output_path, scale=2):
    """使用 Chrome headless 截图"""
    width = 1080
    height = 1440

    # 输出尺寸
    out_width = width * scale
    out_height = height * scale

    # 创建临时 HTML 文件，使用输出尺寸
    html_content = create_html_wrapper(svg_path, out_width, out_height)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        html_path = f.name

    try:
        # 使用 Chrome headless 截图
        chrome_paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            'google-chrome',
            'chromium'
        ]

        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path) or subprocess.run(['which', path], capture_output=True).returncode == 0:
                chrome_path = path
                break

        if not chrome_path:
            raise Exception("Chrome not found")

        # Chrome headless 截图命令 - 不使用 scale factor，直接用目标尺寸
        cmd = [
            chrome_path,
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-software-rasterizer',
            f'--window-size={out_width},{out_height}',
            f'--screenshot={output_path}',
            f'file://{html_path}'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if os.path.exists(output_path):
            print(f"✅ {os.path.basename(output_path)} ({out_width}x{out_height})")
            return True
        else:
            print(f"❌ Failed: {result.stderr}")
            return False

    finally:
        os.unlink(html_path)


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
