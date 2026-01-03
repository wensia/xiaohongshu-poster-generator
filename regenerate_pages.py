#!/usr/bin/env python3
"""根据封面风格重新生成内页"""

import os
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

# 内页模板 - 极简留白风格
PAGE_TEMPLATE = '''<!-- [STYLE LOCK: 极简留白] [LAYOUT LOCK: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {page_num:02d} - {section_title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF9F7; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{
      width: 1080px;
      height: 1440px;
      position: relative;
      background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%);
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}
    .poster::before {{
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.03;
      pointer-events: none;
      z-index: 1;
    }}
    .part-label {{
      position: absolute;
      top: 100px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 14px;
      font-weight: 400;
      color: #D97757;
      letter-spacing: 8px;
      z-index: 10;
    }}
    .main {{
      position: relative;
      z-index: 10;
      text-align: center;
      padding: 0 100px;
      max-width: 900px;
    }}
    .section-title {{
      font-size: 42px;
      font-weight: 500;
      color: #D97757;
      letter-spacing: 6px;
      margin-bottom: 60px;
    }}
    .content {{
      font-size: 32px;
      font-weight: 400;
      color: #3D3832;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: center;
    }}
    .accent {{
      color: #D97757;
      font-weight: 500;
    }}
    .quote {{
      margin-top: 70px;
      font-size: 22px;
      font-weight: 300;
      color: #9A958E;
      letter-spacing: 3px;
    }}
    .footer {{
      position: absolute;
      bottom: 100px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
    }}
    .page-num {{
      font-size: 14px;
      font-weight: 400;
      color: #B5B0A8;
      letter-spacing: 4px;
    }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="part-label">· {part_num:02d} ·</div>
    <div class="main">
      <h2 class="section-title">{section_title}</h2>
      <p class="content">
        {content_html}
      </p>
      <p class="quote">{quote}</p>
    </div>
    <div class="footer">
      <span class="page-num">{page_num:02d}</span>
    </div>
  </div>
</body>
</html>
'''

# 结尾页模板
END_TEMPLATE = '''<!-- [STYLE LOCK: 极简留白] [LAYOUT LOCK: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {page_num:02d} - {section_title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF9F7; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{
      width: 1080px;
      height: 1440px;
      position: relative;
      background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%);
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }}
    .poster::before {{
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.03;
      pointer-events: none;
      z-index: 1;
    }}
    .zodiac-badge {{
      position: absolute;
      top: 120px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 10;
    }}
    .zodiac-icon svg {{
      width: 52px;
      height: 52px;
      stroke: #D97757;
      stroke-width: 1.5;
      fill: none;
    }}
    .zodiac-name {{
      margin-top: 20px;
      font-size: 18px;
      font-weight: 400;
      color: #D97757;
      letter-spacing: 10px;
      text-indent: 10px;
    }}
    .main {{
      position: relative;
      z-index: 10;
      text-align: center;
      padding: 0 100px;
      margin-top: 60px;
    }}
    .section-title {{
      font-size: 46px;
      font-weight: 500;
      color: #D97757;
      letter-spacing: 6px;
      margin-bottom: 60px;
    }}
    .content {{
      font-size: 32px;
      font-weight: 400;
      color: #3D3832;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: center;
    }}
    .accent {{
      color: #D97757;
      font-weight: 500;
    }}
    .end-mark {{
      margin-top: 60px;
      font-size: 28px;
      color: #D97757;
    }}
    .footer {{
      position: absolute;
      bottom: 100px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
    }}
    .page-num {{
      font-size: 14px;
      font-weight: 400;
      color: #B5B0A8;
      letter-spacing: 4px;
    }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-badge">
      <div class="zodiac-icon">
        <svg viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
          <line x1="12" y1="10" x2="38" y2="10" stroke-linecap="round"/>
          <line x1="12" y1="40" x2="38" y2="40" stroke-linecap="round"/>
          <line x1="18" y1="10" x2="18" y2="40" stroke-linecap="round"/>
          <line x1="32" y1="10" x2="32" y2="40" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="zodiac-name">GEMINI</div>
    </div>
    <div class="main">
      <h2 class="section-title">{section_title}</h2>
      <p class="content">
        {content_html}
      </p>
      <div class="end-mark">✦</div>
    </div>
    <div class="footer">
      <span class="page-num">{page_num:02d}</span>
    </div>
  </div>
</body>
</html>
'''


def html_to_png(html_path: str, output_path: str, width: int = 1080, height: int = 1440) -> str:
    """使用 Playwright 将 HTML 转换为 PNG"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)

        poster = page.locator(".poster")
        poster.screenshot(path=output_path)

        browser.close()
    return output_path


def generate_pages(output_dir: Path, pages_data: list):
    """生成多张内页"""
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []

    for i, page_data in enumerate(pages_data, 2):  # 从第2页开始（封面是第1页）
        is_end_page = i == len(pages_data) + 1
        template = END_TEMPLATE if is_end_page else PAGE_TEMPLATE

        html = template.format(
            page_num=i,
            part_num=i - 1,
            section_title=page_data['title'],
            content_html=page_data['content'],
            quote=page_data.get('quote', '')
        )

        # 保存HTML
        html_path = output_dir / f"page-{i:02d}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

        # 生成PNG
        png_path = output_dir / f"page-{i:02d}.png"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            temp_html = f.name

        try:
            html_to_png(temp_html, str(png_path))
            generated_files.append(str(png_path))
            print(f"  [Page {i:02d}] {page_data['title']}")
            os.unlink(temp_html)
        except Exception as e:
            print(f"  [Page {i:02d}] 失败: {e}")

    return generated_files


# 记录1的内页数据 - 双子座最怕的不是孤独，是被束缚
record1_pages = [
    {
        "title": "不是怕孤独",
        "content": '''我们双子座啊<br/>
        真正怕的从来不是<span class="accent">一个人待着</span><br/><br/>
        怕的是那种事事都要<span class="accent">报备</span>的感觉<br/>
        出门要说 回来要讲<br/>
        消息晚回一会儿都能被追问半天''',
        "quote": "「 孤独不可怕，失去自由才可怕 」"
    },
    {
        "title": "需要呼吸空间",
        "content": '''不是不想<span class="accent">负责</span><br/>
        是受不了那种被盯着的<span class="accent">压迫感</span><br/><br/>
        爱自由的人<br/>
        骨子里需要<span class="accent">呼吸的空间</span>''',
        "quote": "「 给我空间，不是不爱你 」"
    },
    {
        "title": "双子的沉默",
        "content": '''你问双子为什么有时候会<span class="accent">突然沉默</span>？<br/><br/>
        不是生气<br/>
        是需要一个人待会儿<br/>
        把自己<span class="accent">捋顺了</span>''',
        "quote": "「 沉默是我整理自己的方式 」"
    },
    {
        "title": "两个极端",
        "content": '''热情的时候能<span class="accent">聊到凌晨三点</span><br/><br/>
        想静静的时候<br/>
        谁来都不想搭理<br/><br/>
        这就是双子<br/>
        <span class="accent">两个极端</span>都是真的''',
        "quote": "「 热烈与安静，都是我 」"
    },
    {
        "title": "这就是双子",
        "content": '''有些人觉得我们<span class="accent">善变</span><br/><br/>
        其实只是在找一个<br/>
        能让我们安心<span class="accent">做自己</span>的人''',
        "quote": ""
    }
]

# 记录2的内页数据 - 双子座的温柔，只给读得懂的人
record2_pages = [
    {
        "title": "表面与内心",
        "content": '''双子对谁都能笑<br/>
        但真正的<span class="accent">温柔</span>藏得很深<br/><br/>
        表面嘻嘻哈哈什么都能聊<br/>
        其实内心装着<span class="accent">一整片海</span><br/>
        只是不轻易让人靠近''',
        "quote": "「 笑容给所有人，真心只给你 」"
    },
    {
        "title": "笨拙的在意",
        "content": '''那些没说出口的<span class="accent">关心</span><br/><br/>
        那些假装不在意的<span class="accent">紧张</span><br/><br/>
        都是双子<br/>
        笨拙的<span class="accent">在意方式</span>''',
        "quote": "「 我的在意，藏在沉默里 」"
    },
    {
        "title": "独自消化",
        "content": '''我们习惯了<span class="accent">独自消化</span>情绪<br/><br/>
        不是不想倾诉<br/>
        是怕说出来<br/>
        显得<span class="accent">矫情</span>''',
        "quote": "「 自己扛着，也是一种温柔 」"
    },
    {
        "title": "读懂沉默",
        "content": '''能读懂双子<span class="accent">沉默</span>的人<br/>
        才配得上那份<span class="accent">真心</span><br/><br/>
        我们不是不会爱<br/>
        只是不想<span class="accent">爱错人</span>''',
        "quote": "「 懂我的人，才值得我爱 」"
    },
    {
        "title": "温柔留给你",
        "content": '''有些<span class="accent">温柔</span><br/><br/>
        只留给那个<br/>
        愿意<span class="accent">懂</span>的人''',
        "quote": ""
    }
]


if __name__ == "__main__":
    # 生成记录1的内页
    print("=" * 50)
    print("生成记录1: 双子座最怕的不是孤独，是被束缚")
    print("=" * 50)
    output_dir1 = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/03/双子座-被束缚")
    files1 = generate_pages(output_dir1, record1_pages)
    print(f"\n完成！共生成 {len(files1)} 张内页")

    print()

    # 生成记录2的内页
    print("=" * 50)
    print("生成记录2: 双子座的温柔，只给读得懂的人")
    print("=" * 50)
    output_dir2 = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/03/双子座-温柔")
    files2 = generate_pages(output_dir2, record2_pages)
    print(f"\n完成！共生成 {len(files2)} 张内页")

    print()
    print("=" * 50)
    print(f"全部完成！共生成 {len(files1) + len(files2)} 张内页")
    print("=" * 50)
