#!/usr/bin/env python3
"""
根据新规则生成性格独白风套图（包含.quote引用区块）
"""
import os
from pathlib import Path

# 射手座 SVG
SAGITTARIUS_SVG = '<svg viewBox="0 0 24 24"><path d="M4 20L20 4M20 4H10M20 4V14" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# 基础模板 - 优化版（2.0倍缩放，更紧凑）
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

    /* 页眉 */
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

    /* 页脚 */
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
      font-size: 80px;
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
      font-size: 32px;
      color: var(--text-primary);
      line-height: 1.9;
      letter-spacing: 2px;
    }
    .content-text p {
      margin-bottom: 28px;
    }
    .quote {
      margin-top: 50px;
      padding-left: 30px;
      border-left: 4px solid var(--accent-color);
    }
    .quote-text {
      font-style: italic;
      font-size: 28px;
      color: var(--text-secondary);
      letter-spacing: 2px;
      line-height: 1.6;
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
        {SAGITTARIUS_SVG}
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

def create_cover(zodiac, topic, subtitle, title_line1, title_highlight, tagline_line1, tagline_highlight, tagline_rest=""):
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
      <h1 class="cover-title">
        {title_line1}<br><span class="highlight">{title_highlight}</span>
      </h1>
      <div class="cover-divider"></div>
      <p class="cover-tagline">
        {tagline_line1}<br><span class="highlight">{tagline_highlight}</span>{tagline_rest}
      </p>
    </div>

    {create_footer(1)}
  </div>
</body>
</html>
'''
    return html

def create_page(zodiac, topic, part_num, section_title, content_lines, quote, page_num):
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

      <div class="quote">
        <p class="quote-text">"{quote}"</p>
      </div>
    </div>

    {create_footer(page_num)}
  </div>
</body>
</html>
'''
    return html

def create_end(zodiac, topic, summary_title, content_lines, ending_line1, ending_line2, page_num):
    content_html = "\n".join([f"        <p>{line}</p>" for line in content_lines])
    html = f'''<!-- [STYLE: 性格独白风] [TYPE: end] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {page_num:02d} - 总结</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
  <style>{END_CSS}</style>
</head>
<body>
  <div class="poster">
    {create_header(zodiac, topic)}

    <p class="part-label">EXTRA</p>
    <h2 class="section-title">{summary_title}</h2>
    <div class="section-divider"></div>

    <div class="summary-content">
      <div class="summary-text">
{content_html}
      </div>

      <div class="ending-section">
        <p class="ending-wish">
          {ending_line1}<br>{ending_line2}
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

# 数据定义
RECORDS = [
    {
        "name": "轻计划学习法",
        "dir": "射手座_轻计划学习法_性格独白风_v2",
        "topic": "轻计划学习法",
        "cover": {
            "subtitle": "学习不必太用力",
            "title_line1": "适合射手的",
            "title_highlight": "学习法",
            "tagline_line1": "有趣比系统重要",
            "tagline_highlight": "能动",
            "tagline_rest": "比学全更重要"
        },
        "pages": [
            {
                "section": "核心诉求",
                "lines": [
                    "射手对学习的核心诉求",
                    "是<span class=\"highlight\">有趣</span>而非系统",
                    "能激发好奇的内容",
                    "才能<span class=\"highlight\">持续保持动力</span>"
                ],
                "quote": "有趣，是学习最好的燃料"
            },
            {
                "section": "适合的方式",
                "lines": [
                    "短视频教程、实战项目",
                    "<span class=\"highlight\">兴趣驱动</span>、跨界尝试",
                    "都能满足探索欲",
                    "太枯燥的理论<span class=\"highlight\">反而想逃</span>"
                ],
                "quote": "探索欲，是射手最强的学习引擎"
            },
            {
                "section": "计划方式",
                "lines": [
                    "计划太细会<span class=\"highlight\">耗光兴趣</span>",
                    "适度留白、随时调整",
                    "允许跳跃",
                    "反而<span class=\"highlight\">更有乐趣</span>"
                ],
                "quote": "留白，是给好奇心的呼吸空间"
            },
            {
                "section": "学习节奏",
                "lines": [
                    "学习方式上更适合",
                    "<span class=\"highlight\">边做边学</span>",
                    "不需要准备万全",
                    "但要<span class=\"highlight\">敢于开始</span>"
                ],
                "quote": "行动中修正，比完美计划更有效"
            },
            {
                "section": "核心原则",
                "lines": [
                    "与其追求<span class=\"highlight\">学得全</span>",
                    "不如追求学得动",
                    "方向对了",
                    "知识自然会<span class=\"highlight\">串联</span>"
                ],
                "quote": "学得动，比学得全更重要"
            }
        ],
        "end": {
            "title": "写给射手座",
            "lines": [
                "学习不必太用力",
                "找到<span class=\"highlight\">让你兴奋的方向</span>",
                "保持好奇",
                "知识自然会来"
            ],
            "ending1": "愿你的每一次学习",
            "ending2": "都有<span class=\"highlight\">发现的快乐</span>"
        }
    },
    {
        "name": "边界感练习",
        "dir": "射手座_边界感练习_性格独白风_v2",
        "topic": "边界感练习",
        "cover": {
            "subtitle": "关系需要呼吸感",
            "title_line1": "射手座的",
            "title_highlight": "边界感",
            "tagline_line1": "距离不是冷漠",
            "tagline_highlight": "而是",
            "tagline_rest": "更好的靠近"
        },
        "pages": [
            {
                "section": "核心诉求",
                "lines": [
                    "射手对关系的核心诉求",
                    "是<span class=\"highlight\">自由与尊重</span>",
                    "有空间、有边界",
                    "才能<span class=\"highlight\">持续保持热情</span>"
                ],
                "quote": "自由，是爱最好的养分"
            },
            {
                "section": "舒适模式",
                "lines": [
                    "适度的距离、清晰的底线",
                    "<span class=\"highlight\">不过度付出</span>",
                    "不强求回应",
                    "太黏的模式<span class=\"highlight\">反而想逃</span>"
                ],
                "quote": "不黏腻，反而更长久"
            },
            {
                "section": "边界管理",
                "lines": [
                    "边界太模糊会<span class=\"highlight\">耗光耐心</span>",
                    "学会说不、主动表达",
                    "及时止损",
                    "反而让关系<span class=\"highlight\">更有质量</span>"
                ],
                "quote": "说不，是对自己最好的尊重"
            },
            {
                "section": "相处节奏",
                "lines": [
                    "相处模式上更适合",
                    "<span class=\"highlight\">各自精彩</span>",
                    "不需要时刻同步",
                    "但要有<span class=\"highlight\">共识和默契</span>"
                ],
                "quote": "各自精彩，才能共同发光"
            },
            {
                "section": "核心原则",
                "lines": [
                    "与其追求<span class=\"highlight\">融为一体</span>",
                    "不如追求各自完整",
                    "边界清了",
                    "爱意自然会<span class=\"highlight\">流动</span>"
                ],
                "quote": "完整的自己，才能给出完整的爱"
            }
        ],
        "end": {
            "title": "写给射手座",
            "lines": [
                "关系不必太紧密",
                "保持<span class=\"highlight\">自己的节奏</span>",
                "边界清晰",
                "爱意自然会来"
            ],
            "ending1": "愿你的每一段关系",
            "ending2": "都有<span class=\"highlight\">舒适的距离</span>"
        }
    },
    {
        "name": "独处方式",
        "dir": "射手座_独处方式_性格独白风_v2",
        "topic": "独处方式",
        "cover": {
            "subtitle": "一个人也很好",
            "title_line1": "射手座最舒服的",
            "title_highlight": "独处",
            "tagline_line1": "独处不是逃避",
            "tagline_highlight": "而是",
            "tagline_rest": "更好的充电"
        },
        "pages": [
            {
                "section": "核心诉求",
                "lines": [
                    "射手对独处的核心诉求",
                    "是<span class=\"highlight\">充电</span>而非逃避",
                    "有自由、有选择",
                    "才能<span class=\"highlight\">真正放松下来</span>"
                ],
                "quote": "独处，是给自己最好的礼物"
            },
            {
                "section": "充电方式",
                "lines": [
                    "刷剧发呆、漫无目的地逛",
                    "<span class=\"highlight\">一个人吃好吃的</span>",
                    "窝在家里什么都不想",
                    "被安排的独处<span class=\"highlight\">反而没用</span>"
                ],
                "quote": "随心所欲，才是真正的休息"
            },
            {
                "section": "能量管理",
                "lines": [
                    "社交太满会<span class=\"highlight\">耗光电量</span>",
                    "适度留白、主动独处",
                    "定期清空",
                    "反而以<span class=\"highlight\">更好的状态</span>回来"
                ],
                "quote": "留白，是为了更好的出发"
            },
            {
                "section": "独处节奏",
                "lines": [
                    "独处方式上更适合",
                    "<span class=\"highlight\">随性自由</span>",
                    "不需要仪式感",
                    "但要有<span class=\"highlight\">完全属于自己</span>的时间"
                ],
                "quote": "属于自己的时间，最珍贵"
            },
            {
                "section": "核心原则",
                "lines": [
                    "与其追求<span class=\"highlight\">热闹</span>",
                    "不如追求松弛",
                    "独处对了",
                    "能量自然会<span class=\"highlight\">回来</span>"
                ],
                "quote": "松弛，是射手最好的能量来源"
            }
        ],
        "end": {
            "title": "写给射手座",
            "lines": [
                "独处不必有负担",
                "找到<span class=\"highlight\">让你放松的方式</span>",
                "好好充电",
                "能量自然会回来"
            ],
            "ending1": "愿你的每一次独处",
            "ending2": "都有<span class=\"highlight\">满满的能量</span>"
        }
    }
]

def main():
    base_dir = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/05")

    for record in RECORDS:
        output_dir = base_dir / record["dir"]
        output_dir.mkdir(parents=True, exist_ok=True)

        zodiac = "射手座"
        topic = record["topic"]

        # 1. 封面
        cover = record["cover"]
        html = create_cover(
            zodiac, topic,
            cover["subtitle"],
            cover["title_line1"],
            cover["title_highlight"],
            cover["tagline_line1"],
            cover["tagline_highlight"],
            cover.get("tagline_rest", "")
        )
        (output_dir / "01_cover.html").write_text(html, encoding="utf-8")
        print(f"✅ {record['name']} - 01_cover.html")

        # 2-6. 内容页
        for i, page in enumerate(record["pages"], start=1):
            html = create_page(
                zodiac, topic,
                i,  # part_num
                page["section"],
                page["lines"],
                page["quote"],
                i + 1  # page_num (从02开始)
            )
            filename = f"{i+1:02d}_page.html"
            (output_dir / filename).write_text(html, encoding="utf-8")
            print(f"✅ {record['name']} - {filename}")

        # 7. 结尾页
        end = record["end"]
        html = create_end(
            zodiac, topic,
            end["title"],
            end["lines"],
            end["ending1"],
            end["ending2"],
            7  # page_num
        )
        (output_dir / "07_end.html").write_text(html, encoding="utf-8")
        print(f"✅ {record['name']} - 07_end.html")

        print(f"📁 {record['name']} 完成！目录: {output_dir}")
        print()

if __name__ == "__main__":
    main()
