#!/usr/bin/env python3
"""
生成双子座理想的生活套图
"""
from pathlib import Path
from datetime import datetime

# 双子座 SVG
GEMINI_SVG = '<svg viewBox="0 0 24 24"><path d="M4 4h16M4 20h16M8 4v16M16 4v16" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# 基础模板
BASE_CSS = """
    :root {
      --bg-color: #F5F2ED;
      --text-primary: #3D3835;
      --text-secondary: #6B6461;
      --accent-color: #C4653A;
      --line-color: #D4CFC8;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }

    .poster {
      width: 1080px;
      height: 1440px;
      background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%);
      position: relative;
      padding: 90px 100px;
      display: flex;
      flex-direction: column;
      font-family: 'Noto Serif SC', serif;
    }

    .poster::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(180deg,
        rgba(255,255,255,0.3) 0%,
        rgba(255,255,255,0) 20%,
        rgba(0,0,0,0) 80%,
        rgba(0,0,0,0.03) 100%
      );
      pointer-events: none;
      z-index: 1;
    }

    .poster > * { position: relative; z-index: 2; }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    .header-title {
      display: flex;
      align-items: baseline;
      gap: 6px;
    }
    .header-zodiac {
      font-family: 'Noto Serif SC', serif;
      font-size: 32px;
      font-weight: 500;
      color: var(--accent-color);
      letter-spacing: 2px;
    }
    .header-separator {
      font-family: 'Georgia', serif;
      font-size: 24px;
      color: var(--line-color);
      margin: 0 4px;
    }
    .header-topic {
      font-family: 'Noto Sans SC', sans-serif;
      font-size: 24px;
      font-weight: 300;
      color: var(--text-secondary);
      letter-spacing: 3px;
    }
    .zodiac-symbol svg {
      width: 56px;
      height: 56px;
      stroke: var(--accent-color);
      stroke-width: 1.5;
      fill: none;
      transform: rotate(-10deg);
    }

    .footer {
      margin-top: auto;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }
    .footer-line {
      width: 100%;
      height: 2px;
      background: var(--line-color);
      margin-bottom: 24px;
    }
    .page-number {
      font-family: 'Georgia', serif;
      font-size: 28px;
      color: var(--text-secondary);
      letter-spacing: 4px;
    }

    .highlight {
      color: var(--accent-color);
    }
"""

COVER_CSS = BASE_CSS + """
    .header {
      margin-bottom: auto;
    }
    .cover-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 40px 0;
    }
    .cover-subtitle {
      font-size: 32px;
      color: var(--text-secondary);
      letter-spacing: 6px;
      margin-bottom: 50px;
    }
    .cover-title {
      font-size: 72px;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.4;
      letter-spacing: 8px;
      margin-bottom: 60px;
    }
    .cover-divider {
      width: 100px;
      height: 4px;
      background: var(--accent-color);
      margin-bottom: 60px;
    }
    .cover-tagline {
      font-size: 30px;
      color: var(--text-secondary);
      line-height: 1.9;
      letter-spacing: 4px;
    }
"""

PAGE_CSS = BASE_CSS + """
    .part-label {
      font-family: 'Georgia', serif;
      font-size: 26px;
      color: var(--accent-color);
      letter-spacing: 8px;
      margin-top: 30px;
      margin-bottom: 16px;
    }
    .section-title {
      font-size: 64px;
      font-weight: 600;
      color: var(--text-primary);
      letter-spacing: 6px;
      margin-bottom: 24px;
    }
    .section-divider {
      width: 100px;
      height: 4px;
      background: var(--accent-color);
      margin-bottom: 80px;
    }
    .content-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-bottom: 60px;
    }
    .content-text {
      font-size: 36px;
      color: var(--text-primary);
      line-height: 2.2;
      letter-spacing: 3px;
      text-align: center;
    }
    .content-text p {
      margin-bottom: 20px;
    }
"""

END_CSS = BASE_CSS + """
    .part-label {
      font-family: 'Georgia', serif;
      font-size: 26px;
      color: var(--accent-color);
      letter-spacing: 8px;
      margin-top: 30px;
      margin-bottom: 16px;
    }
    .section-title {
      font-size: 56px;
      font-weight: 600;
      color: var(--text-primary);
      letter-spacing: 6px;
      margin-bottom: 24px;
    }
    .section-divider {
      width: 100px;
      height: 4px;
      background: var(--accent-color);
      margin-bottom: 80px;
    }
    .summary-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding-bottom: 60px;
      text-align: center;
    }
    .summary-text {
      font-size: 32px;
      color: var(--text-primary);
      line-height: 2.0;
      letter-spacing: 2px;
      text-align: center;
    }
    .summary-text p {
      margin-bottom: 16px;
    }
    .ending-section {
      margin-top: 80px;
      text-align: center;
    }
    .ending-wish {
      font-size: 30px;
      color: var(--text-secondary);
      letter-spacing: 4px;
      line-height: 1.9;
      font-style: italic;
    }
    .ending-mark {
      margin-top: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 30px;
    }
    .ending-mark::before,
    .ending-mark::after {
      content: '';
      width: 60px;
      height: 2px;
      background: var(--line-color);
    }
    .ending-mark span {
      font-family: 'Georgia', serif;
      font-size: 24px;
      color: var(--accent-color);
      letter-spacing: 6px;
    }
"""

def create_header(zodiac, topic):
    return f'''
    <div class="header">
      <div class="header-title">
        <span class="header-zodiac">{zodiac}</span>
        <span class="header-separator">·</span>
        <span class="header-topic">{topic}</span>
      </div>
      <div class="zodiac-symbol">
        {GEMINI_SVG}
      </div>
    </div>
'''

def create_footer(page_num):
    return f'''
    <div class="footer">
      <div class="footer-line"></div>
      <span class="page-number">0 {page_num}</span>
    </div>
'''

def create_cover(zodiac, topic, subtitle, title_before, title_highlight, title_after, taglines):
    """
    创建封面
    主标题支持智能高亮：title_before + title_highlight(强调色) + title_after
    """
    html = f'''<!-- [STYLE: 性格独白风] [TYPE: cover] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面 - {zodiac} · {topic}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
  <style>{COVER_CSS}</style>
</head>
<body>
  <div class="poster">
    {create_header(zodiac, topic)}

    <div class="cover-content">
      <p class="cover-subtitle">{subtitle}</p>
      <h1 class="cover-title">{title_before}<span class="highlight">{title_highlight}</span>{title_after}</h1>
      <div class="cover-divider"></div>
      <p class="cover-tagline">
        {taglines}
      </p>
    </div>

    {create_footer(1)}
  </div>
</body>
</html>
'''
    return html

def create_page(zodiac, topic, part_num, section_title, content_lines, page_num):
    content_html = "\n".join([f"        <p>{line}</p>" for line in content_lines])
    html = f'''<!-- [STYLE: 性格独白风] [TYPE: page] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {page_num:02d} - {section_title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
  <style>{PAGE_CSS}</style>
</head>
<body>
  <div class="poster">
    {create_header(zodiac, topic)}

    <p class="part-label">PART {part_num:02d}</p>
    <h2 class="section-title">{section_title}</h2>
    <div class="section-divider"></div>

    <div class="content-body">
      <div class="content-text">
{content_html}
      </div>
    </div>

    {create_footer(page_num)}
  </div>
</body>
</html>
'''
    return html

def create_end(zodiac, topic, page_num):
    html = f'''<!-- [STYLE: 性格独白风] [TYPE: end] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {page_num:02d} - 结尾</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
  <style>{END_CSS}</style>
</head>
<body>
  <div class="poster">
    {create_header(zodiac, topic)}

    <p class="part-label">EXTRA</p>
    <h2 class="section-title">屏幕前的双子</h2>
    <div class="section-divider"></div>

    <div class="summary-content">
      <div class="summary-text">
        <p>这些都是</p>
        <p><span class="highlight">理想生活</span>中的</p>
        <p>美好时刻</p>
      </div>

      <div class="ending-section">
        <p class="ending-wish">
          愿你的每一天<br>都有<span class="highlight">新鲜感</span>和<span class="highlight">好奇心</span>
        </p>
        <div class="ending-mark">
          <span>END</span>
        </div>
      </div>
    </div>

    {create_footer(page_num)}
  </div>
</body>
</html>
'''
    return html

def main():
    today = datetime.now().strftime("%Y/%m/%d")
    base_dir = Path(f"/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/{today}")
    output_dir = base_dir / "双子座理想的生活"
    output_dir.mkdir(parents=True, exist_ok=True)

    zodiac = "双子座"
    topic = "理想的生活"

    # 页面数据
    pages_data = [
        {
            "section": "新鲜有趣",
            "lines": [
                "每天都有<span class=\"highlight\">新发现</span>",
                "世界永远不无聊"
            ]
        },
        {
            "section": "朋友遍天下",
            "lines": [
                "聊天<span class=\"highlight\">不冷场</span>",
                "话题接不完"
            ]
        },
        {
            "section": "想法被听见",
            "lines": [
                "有人懂我的<span class=\"highlight\">双面</span>",
                "变化被接受"
            ]
        },
        {
            "section": "信息自由",
            "lines": [
                "八卦<span class=\"highlight\">第一时间</span>知道",
                "脑子永远在线"
            ]
        },
        {
            "section": "不被定义",
            "lines": [
                "今天可以<span class=\"highlight\">安静</span>",
                "明天可以<span class=\"highlight\">疯狂</span>"
            ]
        },
        {
            "section": "知心闺蜜",
            "lines": [
                "想聊就聊",
                "深夜也能<span class=\"highlight\">接电话</span>"
            ]
        }
    ]

    # 1. 封面（主标题智能高亮："理想的"作为高亮词）
    taglines = '<span class="highlight">新鲜有趣</span> · 永远好奇<br>朋友遍天下 · <span class="highlight">不被定义</span>'
    html = create_cover(
        zodiac, topic,
        subtitle="每天都有新鲜感",
        title_before="双子座",
        title_highlight="理想的",
        title_after="生活",
        taglines=taglines
    )
    (output_dir / "01_cover.html").write_text(html, encoding="utf-8")
    print(f"✅ 01_cover.html")

    # 2-7. 内容页
    for i, page in enumerate(pages_data, start=1):
        html = create_page(zodiac, topic, i, page["section"], page["lines"], i + 1)
        filename = f"{i+1:02d}_page.html"
        (output_dir / filename).write_text(html, encoding="utf-8")
        print(f"✅ {filename}")

    # 8. 结尾页
    html = create_end(zodiac, topic, 8)
    (output_dir / "08_end.html").write_text(html, encoding="utf-8")
    print(f"✅ 08_end.html")

    print(f"\n📁 完成！目录: {output_dir}")
    return output_dir

if __name__ == "__main__":
    main()
