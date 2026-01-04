#!/usr/bin/env python3
"""批量生成7套海报的脚本"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成")
OUTPUT_DIR = BASE_DIR / "output/2026/01/04"

# 射手座SVG图标
SAGITTARIUS_SVG = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <line x1="20" y1="80" x2="80" y2="20" stroke-linecap="round"/>
  <line x1="80" y1="20" x2="55" y2="20" stroke-linecap="round"/>
  <line x1="80" y1="20" x2="80" y2="45" stroke-linecap="round"/>
  <line x1="25" y1="45" x2="55" y2="75" stroke-linecap="round"/>
</svg>'''

# 天蝎座SVG图标
SCORPIO_SVG = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M15 50 Q25 30, 35 50 Q45 70, 55 50 Q65 30, 75 50" stroke-linecap="round"/>
  <line x1="75" y1="50" x2="85" y2="60" stroke-linecap="round"/>
  <line x1="85" y1="60" x2="80" y2="65" stroke-linecap="round"/>
</svg>'''

# 通用基础样式
BASE_STYLE = '''
:root, html, body { color-scheme: light only; background: #FAF6F1; }
* { margin: 0; padding: 0; box-sizing: border-box; }
.poster {
  width: 1080px;
  height: 1440px;
  position: relative;
  background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%);
  font-family: 'Noto Serif SC', serif;
  overflow: hidden;
}
.poster::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.05;
  pointer-events: none;
  z-index: 1;
}
'''

def generate_html_to_png(html_content, output_path, browser):
    """将HTML转换为PNG"""
    temp_html = output_path.with_suffix('.html')
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    page = browser.new_page(viewport={"width": 1080, "height": 1440})
    page.goto(f"file://{temp_html}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)
    page.locator(".poster").screenshot(path=str(output_path))
    page.close()
    return True


def generate_set_1_classic(browser):
    """1. 千万别在一起 - 经典强调风"""
    output_dir = OUTPUT_DIR / "射手座-千万别在一起-经典"

    pages_content = [
        # (page_num, think_text, truth_text)
        ("02", "都说射手<span class=\"keyword\">太花心</span><br/>天蝎<span class=\"keyword\">太多疑</span>", "其实射手的自由不是花心<br/>天蝎的敏锐是因为太在乎"),
        ("03", "都说射手<span class=\"keyword\">直来直去</span><br/>天蝎<span class=\"keyword\">爱藏心事</span>", "其实一个负责点燃热情<br/>一个负责守护深情"),
        ("04", "都说射手<span class=\"keyword\">吵完就忘</span><br/>天蝎<span class=\"keyword\">永远记仇</span>", "其实射手的释然是真原谅<br/>天蝎的记得是怕再受伤"),
        ("05", "都说射手<span class=\"keyword\">给不了安全感</span><br/>天蝎<span class=\"keyword\">太需要掌控</span>", "其实当射手真的爱了<br/>Ta的忠诚比天蝎还坚定"),
        ("06", "都说这对<span class=\"keyword\">火水不容</span><br/>注定<span class=\"keyword\">互相消耗</span>", "其实火能温暖水的心<br/>水能平息火的躁动"),
    ]

    # 封面
    cover_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-bg {{ position: absolute; top: 100px; left: 50%; transform: translateX(-50%); font-size: 160px; font-weight: 700; color: rgba(193, 95, 60, 0.06); letter-spacing: 10px; z-index: 0; white-space: nowrap; }}
    .circle-deco {{ position: absolute; width: 120px; height: 120px; border: 2px solid rgba(193, 95, 60, 0.15); border-radius: 50%; }}
    .circle-inner {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: rgba(193, 95, 60, 0.08); border-radius: 50%; }}
    .zodiac-icons {{ display: flex; gap: 20px; justify-content: center; margin-bottom: 30px; }}
    .zodiac-icons svg {{ width: 72px; height: 72px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .warning-badge {{ display: inline-block; background: linear-gradient(135deg, #C15F3C 0%, #D4765A 100%); color: #fff; font-size: 28px; font-weight: 600; letter-spacing: 8px; padding: 16px 40px; border-radius: 4px; margin-bottom: 40px; }}
    .vs-box {{ display: flex; align-items: center; justify-content: center; gap: 30px; margin-bottom: 40px; }}
    .zodiac-name {{ font-size: 48px; font-weight: 600; color: #3D3D3D; letter-spacing: 4px; }}
    .vs {{ font-size: 32px; font-weight: 700; color: #C15F3C; background: rgba(193, 95, 60, 0.1); padding: 10px 20px; border-radius: 50%; }}
    .title {{ font-size: 72px; font-weight: 700; color: #3D3D3D; letter-spacing: 4px; line-height: 1.4; margin-bottom: 30px; }}
    .title .accent {{ color: #C15F3C; }}
    .subtitle {{ font-size: 32px; font-weight: 400; color: #5A5A5A; letter-spacing: 4px; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-bg">射手×天蝎</div>
    <div class="circle-deco" style="top: 150px; right: 100px;"><div class="circle-inner"></div></div>
    <div class="circle-deco" style="bottom: 200px; left: 80px; width: 80px; height: 80px;"><div class="circle-inner" style="width: 40px; height: 40px;"></div></div>
    <div class="header">
      <span class="tag">星座配对 · 深度解读</span>
      <span class="tag">SAGITTARIUS × SCORPIO</span>
    </div>
    <div class="main">
      <div class="warning-badge">争议话题</div>
      <div class="zodiac-icons">
        {SAGITTARIUS_SVG}
        {SCORPIO_SVG}
      </div>
      <div class="vs-box">
        <span class="zodiac-name">射手座</span>
        <span class="vs">VS</span>
        <span class="zodiac-name">天蝎座</span>
      </div>
      <p class="title">千万<span class="accent">别</span>在一起<span class="accent">？</span></p>
      <p class="subtitle">真相可能和你想的不一样</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS × SCORPIO</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

    generate_html_to_png(cover_html, output_dir / "01-cover.png", browser)
    print("  ✓ 01-cover.png")

    # 内容页
    for page_num, think, truth in pages_content:
        page_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-icons {{ display: flex; gap: 12px; }}
    .zodiac-icons svg {{ width: 40px; height: 40px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 100px; }}
    .think {{ font-size: 44px; color: #5A5A5A; letter-spacing: 3px; line-height: 1.7; margin-bottom: 60px; }}
    .keyword {{ color: #C15F3C; font-weight: 500; }}
    .truth-box {{ background: rgba(193, 95, 60, 0.08); padding: 40px 50px; border-radius: 4px; border-left: 4px solid #C15F3C; }}
    .truth {{ font-size: 38px; color: #3D3D3D; letter-spacing: 2px; line-height: 1.8; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="tag">争议点 · 深度解读</span>
      <div class="zodiac-icons">
        {SAGITTARIUS_SVG}
        {SCORPIO_SVG}
      </div>
    </div>
    <div class="main">
      <p class="think">{think}</p>
      <div class="truth-box">
        <p class="truth">{truth}</p>
      </div>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS × SCORPIO</span>
      <span class="page-num">{page_num}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''
        generate_html_to_png(page_html, output_dir / f"{page_num}-page.png", browser)
        print(f"  ✓ {page_num}-page.png")

    # 结尾页
    end_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icons {{ display: flex; justify-content: center; gap: 30px; margin-bottom: 40px; }}
    .zodiac-icons svg {{ width: 64px; height: 64px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-names {{ font-size: 36px; font-weight: 600; color: #C15F3C; letter-spacing: 8px; margin-bottom: 50px; }}
    .quote {{ font-size: 46px; font-weight: 500; color: #3D3D3D; letter-spacing: 4px; line-height: 1.8; max-width: 750px; margin-bottom: 50px; }}
    .accent {{ color: #C15F3C; }}
    .tagline {{ font-size: 24px; color: #9A958A; letter-spacing: 6px; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="main">
      <div class="zodiac-icons">
        {SAGITTARIUS_SVG}
        {SCORPIO_SVG}
      </div>
      <p class="zodiac-names">射 手 × 天 蝎</p>
      <p class="quote"><span class="accent">爱情没有标准答案</span><br/>合不合适<br/>只有<span class="accent">经历过的人</span>才知道</p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS × SCORPIO</span>
      <span class="page-num">07</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''
    generate_html_to_png(end_html, output_dir / "07-end.png", browser)
    print("  ✓ 07-end.png")

    return str(output_dir)


def generate_content_pages_border(browser, output_dir, title, subtitle, contents, zodiac="射手座"):
    """生成简约边框风套图"""

    # 封面
    cover_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .corner-bracket {{ position: absolute; width: 60px; height: 60px; border: 2px solid rgba(193, 95, 60, 0.2); }}
    .corner-bracket.top-left {{ top: 140px; left: 70px; border-right: none; border-bottom: none; }}
    .corner-bracket.bottom-right {{ bottom: 140px; right: 70px; border-left: none; border-top: none; }}
    .main {{ position: absolute; top: 50%; left: 80px; right: 80px; transform: translateY(-50%); z-index: 10; text-align: center; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 72px; height: 72px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 48px; font-weight: 600; color: #C15F3C; letter-spacing: 12px; margin-bottom: 20px; }}
    .keyword {{ display: inline-block; font-size: 32px; font-weight: 500; color: #C15F3C; letter-spacing: 8px; padding: 12px 28px; border: 2px solid #C15F3C; border-radius: 2px; margin-bottom: 50px; }}
    .main-title {{ font-size: 64px; font-weight: 600; color: #2D2D2D; letter-spacing: 4px; line-height: 1.5; margin-bottom: 30px; }}
    .accent {{ color: #C15F3C; }}
    .sub-title {{ font-size: 28px; font-weight: 400; color: #5A5A5A; letter-spacing: 4px; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket bottom-right"></div>
    <div class="header">
      <span class="tag">{zodiac} · 成长指南</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">{zodiac}</p>
      <div class="keyword">成长指南</div>
      <h1 class="main-title">{title}</h1>
      <p class="sub-title">{subtitle}</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

    generate_html_to_png(cover_html, output_dir / "01-cover.png", browser)
    print("  ✓ 01-cover.png")

    # 内容页
    for i, content in enumerate(contents, 2):
        page_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .corner-bracket {{ position: absolute; width: 40px; height: 40px; border: 2px solid rgba(193, 95, 60, 0.15); }}
    .corner-bracket.top-left {{ top: 60px; left: 60px; border-right: none; border-bottom: none; }}
    .corner-bracket.bottom-right {{ bottom: 60px; right: 60px; border-left: none; border-top: none; }}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 100px; }}
    .content {{ font-size: 38px; color: #3D3D3D; letter-spacing: 2px; line-height: 2; text-align: center; }}
    .accent {{ color: #C15F3C; font-weight: 500; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket bottom-right"></div>
    <div class="header">
      <span class="tag">{zodiac} · 成长指南</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="main">
      <p class="content">{content}</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">0{i}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''
        generate_html_to_png(page_html, output_dir / f"0{i}-page.png", browser)
        print(f"  ✓ 0{i}-page.png")

    # 结尾页
    end_num = len(contents) + 2
    end_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .corner-bracket {{ position: absolute; width: 60px; height: 60px; border: 2px solid rgba(193, 95, 60, 0.2); }}
    .corner-bracket.top-left {{ top: 60px; left: 60px; border-right: none; border-bottom: none; }}
    .corner-bracket.top-right {{ top: 60px; right: 60px; border-left: none; border-bottom: none; }}
    .corner-bracket.bottom-left {{ bottom: 60px; left: 60px; border-right: none; border-top: none; }}
    .corner-bracket.bottom-right {{ bottom: 60px; right: 60px; border-left: none; border-top: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 72px; height: 72px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 42px; font-weight: 600; color: #C15F3C; letter-spacing: 16px; margin-bottom: 50px; }}
    .quote {{ font-size: 42px; font-weight: 500; color: #3D3D3D; letter-spacing: 3px; line-height: 1.8; max-width: 700px; margin-bottom: 50px; }}
    .accent {{ color: #C15F3C; }}
    .tagline {{ font-size: 24px; color: #9A958A; letter-spacing: 6px; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket top-right"></div>
    <div class="corner-bracket bottom-left"></div>
    <div class="corner-bracket bottom-right"></div>
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote"><span class="accent">方向对了</span><br/>每一步都是<span class="accent">进步</span></p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">0{end_num}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''
    generate_html_to_png(end_html, output_dir / f"0{end_num}-end.png", browser)
    print(f"  ✓ 0{end_num}-end.png")

    return str(output_dir)


def generate_content_pages_magazine(browser, output_dir, title, subtitle, contents, zodiac="射手座"):
    """生成杂志双线风套图"""

    # 封面
    cover_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .double-border {{ position: absolute; top: 130px; left: 70px; right: 70px; bottom: 130px; border: 1px solid rgba(193, 95, 60, 0.1); z-index: 2; }}
    .double-border::before {{ content: ''; position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px; border: 1px solid rgba(193, 95, 60, 0.05); }}
    .stars-scatter {{ position: absolute; width: 180px; height: 180px; z-index: 3; }}
    .star {{ position: absolute; width: 10px; height: 10px; background: #C15F3C; clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%); }}
    .star:nth-child(1) {{ top: 20px; left: 30px; opacity: 0.35; }}
    .star:nth-child(2) {{ top: 60px; left: 130px; opacity: 0.5; transform: scale(0.7); }}
    .star:nth-child(3) {{ top: 100px; left: 50px; opacity: 0.25; transform: scale(1.1); }}
    .main {{ position: absolute; top: 50%; left: 80px; right: 80px; transform: translateY(-50%); z-index: 10; text-align: center; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 72px; height: 72px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 48px; font-weight: 600; color: #C15F3C; letter-spacing: 12px; margin-bottom: 20px; }}
    .keyword {{ display: inline-block; font-size: 32px; font-weight: 500; color: #3D3D3D; letter-spacing: 8px; padding: 12px 20px; border-top: 1px solid rgba(193, 95, 60, 0.4); border-bottom: 1px solid rgba(193, 95, 60, 0.4); margin-bottom: 50px; }}
    .main-title {{ font-size: 64px; font-weight: 600; color: #2D2D2D; letter-spacing: 4px; line-height: 1.5; margin-bottom: 30px; }}
    .accent {{ color: #C15F3C; }}
    .sub-title {{ font-size: 28px; font-weight: 400; color: #5A5A5A; letter-spacing: 4px; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="double-border"></div>
    <div class="stars-scatter" style="top: 160px; right: 100px;">
      <div class="star"></div><div class="star"></div><div class="star"></div>
    </div>
    <div class="header">
      <span class="tag">{zodiac} · 职场指南</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">{zodiac}</p>
      <div class="keyword">职场指南</div>
      <h1 class="main-title">{title}</h1>
      <p class="sub-title">{subtitle}</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

    generate_html_to_png(cover_html, output_dir / "01-cover.png", browser)
    print("  ✓ 01-cover.png")

    # 内容页
    for i, content in enumerate(contents, 2):
        page_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .double-border {{ position: absolute; top: 50px; left: 50px; right: 50px; bottom: 50px; border: 1px solid rgba(193, 95, 60, 0.08); z-index: 2; }}
    .double-border::before {{ content: ''; position: absolute; top: 8px; left: 8px; right: 8px; bottom: 8px; border: 1px solid rgba(193, 95, 60, 0.04); }}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 100px; }}
    .content {{ font-size: 38px; color: #3D3D3D; letter-spacing: 2px; line-height: 2; text-align: center; }}
    .accent {{ color: #C15F3C; font-weight: 500; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="double-border"></div>
    <div class="header">
      <span class="tag">{zodiac} · 职场指南</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="main">
      <p class="content">{content}</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">0{i}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''
        generate_html_to_png(page_html, output_dir / f"0{i}-page.png", browser)
        print(f"  ✓ 0{i}-page.png")

    # 结尾页
    end_num = len(contents) + 2
    end_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .double-border {{ position: absolute; top: 80px; left: 80px; right: 80px; bottom: 80px; border: 1px solid rgba(193, 95, 60, 0.1); z-index: 2; }}
    .double-border::before {{ content: ''; position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px; border: 1px solid rgba(193, 95, 60, 0.05); }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 72px; height: 72px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 42px; font-weight: 600; color: #C15F3C; letter-spacing: 16px; margin-bottom: 50px; }}
    .quote {{ font-size: 42px; font-weight: 500; color: #3D3D3D; letter-spacing: 3px; line-height: 1.8; max-width: 700px; margin-bottom: 50px; }}
    .accent {{ color: #C15F3C; }}
    .tagline {{ font-size: 24px; color: #9A958A; letter-spacing: 6px; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="double-border"></div>
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote"><span class="accent">别管过程</span><br/>管<span class="accent">结果</span></p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">0{end_num}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''
    generate_html_to_png(end_html, output_dir / f"0{end_num}-end.png", browser)
    print(f"  ✓ 0{end_num}-end.png")

    return str(output_dir)


def generate_content_pages_elegant(browser, output_dir, title, subtitle, contents, zodiac="射手座"):
    """生成优雅留白风套图"""

    # 封面
    cover_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .corner-dot {{ position: absolute; width: 4px; height: 4px; background: rgba(193, 95, 60, 0.5); border-radius: 50%; }}
    .line-deco {{ position: absolute; height: 1px; background: linear-gradient(90deg, transparent, rgba(193, 95, 60, 0.3), transparent); }}
    .header {{ position: absolute; top: 70px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .main {{ position: absolute; top: 50%; left: 100px; right: 100px; transform: translateY(-50%); z-index: 10; text-align: center; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 64px; height: 64px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 42px; font-weight: 600; color: #C15F3C; letter-spacing: 12px; margin-bottom: 20px; }}
    .keyword {{ display: inline-block; font-size: 28px; font-weight: 500; color: #C15F3C; letter-spacing: 8px; padding-bottom: 14px; border-bottom: 1px solid rgba(193, 95, 60, 0.4); margin-bottom: 50px; }}
    .main-title {{ font-size: 56px; font-weight: 600; color: #2D2D2D; letter-spacing: 3px; line-height: 1.6; margin-bottom: 30px; }}
    .accent {{ color: #C15F3C; }}
    .sub-title {{ font-size: 26px; font-weight: 400; color: #6A6A6A; letter-spacing: 3px; }}
    .footer {{ position: absolute; bottom: 80px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 18px; color: #B1ADA1; letter-spacing: 3px; }}
    .page-num {{ font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 3px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>
    <div class="line-deco" style="top: 160px; left: 100px; right: 100px;"></div>
    <div class="header">
      <span class="tag">{zodiac} · 社交指南</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">{zodiac}</p>
      <div class="keyword">社交指南</div>
      <h1 class="main-title">{title}</h1>
      <p class="sub-title">{subtitle}</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

    generate_html_to_png(cover_html, output_dir / "01-cover.png", browser)
    print("  ✓ 01-cover.png")

    # 内容页
    for i, content in enumerate(contents, 2):
        page_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .corner-dot {{ position: absolute; width: 4px; height: 4px; background: rgba(193, 95, 60, 0.5); border-radius: 50%; }}
    .header {{ position: absolute; top: 70px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 120px; }}
    .content {{ font-size: 36px; color: #3D3D3D; letter-spacing: 2px; line-height: 2.2; text-align: center; }}
    .accent {{ color: #C15F3C; font-weight: 500; }}
    .footer {{ position: absolute; bottom: 80px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 18px; color: #B1ADA1; letter-spacing: 3px; }}
    .page-num {{ font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 3px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>
    <div class="header">
      <span class="tag">{zodiac} · 社交指南</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="main">
      <p class="content">{content}</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">0{i}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''
        generate_html_to_png(page_html, output_dir / f"0{i}-page.png", browser)
        print(f"  ✓ 0{i}-page.png")

    # 结尾页
    end_num = len(contents) + 2
    end_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_STYLE}
    .corner-dot {{ position: absolute; width: 4px; height: 4px; background: rgba(193, 95, 60, 0.5); border-radius: 50%; }}
    .dot-deco {{ position: absolute; width: 6px; height: 6px; background: #C15F3C; border-radius: 50%; opacity: 0.3; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 64px; height: 64px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 38px; font-weight: 600; color: #C15F3C; letter-spacing: 12px; margin-bottom: 50px; }}
    .quote {{ font-size: 40px; font-weight: 500; color: #3D3D3D; letter-spacing: 3px; line-height: 1.9; max-width: 650px; margin-bottom: 50px; }}
    .accent {{ color: #C15F3C; }}
    .tagline {{ font-size: 22px; color: #9A958A; letter-spacing: 6px; }}
    .footer {{ position: absolute; bottom: 80px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 18px; color: #B1ADA1; letter-spacing: 3px; }}
    .page-num {{ font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 3px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>
    <div class="dot-deco" style="top: 300px; left: 150px;"></div>
    <div class="dot-deco" style="top: 400px; right: 180px;"></div>
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote"><span class="accent">不是冷淡</span><br/>是<span class="accent">电量在掉</span></p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">0{end_num}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''
    generate_html_to_png(end_html, output_dir / f"0{end_num}-end.png", browser)
    print(f"  ✓ 0{end_num}-end.png")

    return str(output_dir)


if __name__ == "__main__":
    print("开始批量生成7套海报...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. 千万别在一起 - 经典强调风
        print("1/7 千万别在一起 (经典强调风)")
        path1 = generate_set_1_classic(browser)

        # 2. 专注力开关 - 简约边框风
        print("\n2/7 专注力开关 (简约边框风)")
        contents_2 = [
            "射手座的<span class=\"accent\">能量像火</span><br/>点对方向就能冲<br/>方向不清时就会四处跑",
            "把目标缩成一句<span class=\"accent\">"方向词"</span><br/>然后定义完成标准<br/>今天做到哪一步就算赢",
            "用<span class=\"accent\">45分钟冲刺</span><br/>加10分钟回顾的节奏<br/>短时冲刺比长时间熬更稳",
            "每周允许<span class=\"accent\">调整一次方向</span><br/>不是反复横跳<br/>而是有节奏地校准",
        ]
        path2 = generate_content_pages_border(browser, OUTPUT_DIR / "射手座-专注力开关",
            "射手座的<span class=\"accent\">专注力</span>开关", "先定方向，再点火", contents_2)

        # 3. 职场关系 - 杂志双线风
        print("\n3/7 职场关系 (杂志双线风)")
        contents_3 = [
            "射手座在职场最怕<br/><span class=\"accent\">事事报备、步步审批</span><br/>热情会快速掉线",
            "适合你的岗位形态是<br/><span class=\"accent\">项目制、跨部门协作</span><br/>对外沟通型",
            "用<span class=\"accent\">"成果清单"</span>保护自由<br/>每周列出你交付的3件事<br/>让别人看到结果",
            "相处的黄金规则是<br/><span class=\"accent\">直说 + 不拖</span><br/>把话说在前面更轻松",
        ]
        path3 = generate_content_pages_magazine(browser, OUTPUT_DIR / "射手座-职场关系",
            "射手座最舒服的<br/><span class=\"accent\">职场关系</span>", "别管过程，管结果", contents_3)

        # 4. 社交电量表 - 优雅留白风
        print("\n4/7 社交电量表 (优雅留白风)")
        contents_4 = [
            "射手座表面热情<br/>但<span class=\"accent\">社交电量掉得很快</span><br/>连续解释、重复寒暄<br/>是你最耗能的事",
            "当你开始<br/><span class=\"accent\">回消息只回表情</span><br/>约饭推到下周<br/>就是电量不足的信号",
            "快速回血方式是<br/><span class=\"accent\">独处 + 轻运动 + 户外</span><br/>身体动起来<br/>心就会重新亮起来",
            "准备一句缓冲话术<br/><span class=\"accent\">"等我回满电再找你"</span><br/>射手座的边界<br/>越说清楚越被尊重",
        ]
        path4 = generate_content_pages_elegant(browser, OUTPUT_DIR / "射手座-社交电量表",
            "射手座<span class=\"accent\">社交电量表</span>", "不是冷淡，是电量在掉", contents_4)

        browser.close()

    print("\n✅ 前4套生成完成！")
