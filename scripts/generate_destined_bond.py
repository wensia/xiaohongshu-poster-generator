#!/usr/bin/env python3
"""
批量生成命定之约风套图
正确做法：从TEMPLATE.md读取SVG模板，替换变量
"""
import os
import re
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "skills/zodiac-poster/assets/templates/destined-bond/TEMPLATE.md"

def extract_templates_from_md(md_path):
    """从TEMPLATE.md中提取SVG模板"""
    content = md_path.read_text(encoding="utf-8")

    templates = {}

    # 提取封面模板
    cover_match = re.search(
        r'## 封面模板.*?```svg\s*(<!-- \[STYLE: 命定之约风\] \[TYPE: cover\] -->.*?</svg>)\s*```',
        content, re.DOTALL
    )
    if cover_match:
        templates['cover'] = cover_match.group(1).strip()

    # 提取内页模板
    page_match = re.search(
        r'## 内页模板.*?```svg\s*(<!-- \[STYLE: 命定之约风\] \[TYPE: page\] -->.*?</svg>)\s*```',
        content, re.DOTALL
    )
    if page_match:
        templates['page'] = page_match.group(1).strip()

    # 提取结尾页模板
    end_match = re.search(
        r'## 结尾页模板.*?```svg\s*(<!-- \[STYLE: 命定之约风\] \[TYPE: end\] -->.*?</svg>)\s*```',
        content, re.DOTALL
    )
    if end_match:
        templates['end'] = end_match.group(1).strip()

    return templates

def render_cover(template, data):
    """渲染封面"""
    svg = template
    svg = svg.replace("{{ZODIAC1}}", data["zodiac1"])
    svg = svg.replace("{{ZODIAC2}}", data["zodiac2"])
    svg = svg.replace("{{MATCH_PERCENT}}", data["match_percent"])
    svg = svg.replace("{{THEME_TITLE}}", data["theme_title"])
    svg = svg.replace("{{THEME_DESC}}", data["theme_desc"])
    svg = svg.replace("{{TAGLINE_LINE1}}", data["tagline_line1"])
    svg = svg.replace("{{TAGLINE_HIGHLIGHT}}", data["tagline_highlight"])
    svg = svg.replace("{{TAGLINE_REST}}", data["tagline_rest"])
    return svg

def render_content_lines(lines):
    """生成正文内容SVG"""
    svg_lines = []
    y = 0
    for line in lines:
        if "|" in line:
            # 包含高亮标记
            parts = line.split("|")
            if len(parts) == 2:
                before, highlight = parts
                svg_lines.append(
                    f'<text y="{y}" font-family="Noto Serif SC, serif" font-size="32" letter-spacing="2">'
                    f'<tspan fill="#4A3F35">{before}</tspan>'
                    f'<tspan fill="#B86B4A">{highlight}</tspan>'
                    f'</text>'
                )
            elif len(parts) == 3:
                before, highlight, after = parts
                svg_lines.append(
                    f'<text y="{y}" font-family="Noto Serif SC, serif" font-size="32" letter-spacing="2">'
                    f'<tspan fill="#4A3F35">{before}</tspan>'
                    f'<tspan fill="#B86B4A">{highlight}</tspan>'
                    f'<tspan fill="#4A3F35">{after}</tspan>'
                    f'</text>'
                )
        else:
            svg_lines.append(
                f'<text y="{y}" font-family="Noto Serif SC, serif" font-size="32" fill="#4A3F35" letter-spacing="2">{line}</text>'
            )
        y += 61
    return "\n    ".join(svg_lines)

def render_page(template, data):
    """渲染内页"""
    svg = template
    svg = svg.replace("{{ZODIAC1}}", data["zodiac1"])
    svg = svg.replace("{{ZODIAC2}}", data["zodiac2"])
    svg = svg.replace("{{PART_NUM}}", data["part_num"])
    svg = svg.replace("{{SECTION_TITLE}}", data["section_title"])
    svg = svg.replace("{{CONTENT_LINES}}", render_content_lines(data["content_lines"]))
    svg = svg.replace("{{QUOTE}}", data["quote"])
    svg = svg.replace("{{PAGE_NUM}}", data["page_num"])
    return svg

def render_end(template, data):
    """渲染结尾页"""
    svg = template
    svg = svg.replace("{{ZODIAC1}}", data["zodiac1"])
    svg = svg.replace("{{ZODIAC2}}", data["zodiac2"])
    svg = svg.replace("{{MATCH_PERCENT}}", data["match_percent"])
    svg = svg.replace("{{SUMMARY_HIGHLIGHT}}", data["summary_highlight"])
    svg = svg.replace("{{SUMMARY_LINE1_BEFORE}}", data["summary_line1_before"])
    svg = svg.replace("{{SUMMARY_LINE1_HIGHLIGHT}}", data["summary_line1_highlight"])
    svg = svg.replace("{{SUMMARY_LINE2}}", data["summary_line2"])
    svg = svg.replace("{{BLESSING_LINE1}}", data["blessing_line1"])
    svg = svg.replace("{{BLESSING_LINE2}}", data["blessing_line2"])
    svg = svg.replace("{{PAGE_NUM}}", data["page_num"])
    return svg

def wrap_svg_html(svg_content):
    """包装SVG为HTML用于截图（字体已嵌入SVG模板中）"""
    return f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <!-- 中文字体 CDN -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{
      color-scheme: light only;
      background: #FDF8F4;
      margin: 0;
      padding: 0;
    }}
    .poster {{
      width: 1080px;
      height: 1440px;
    }}
  </style>
</head>
<body>
  <div class="poster">
{svg_content}
  </div>
</body>
</html>'''

def parse_record_content(content_text):
    """解析飞书记录的正文内容"""
    sections = content_text.strip().split("\n\n")
    result = []
    for section in sections:
        lines = section.strip().split("\n")
        if lines:
            result.append({
                "title": lines[0],
                "content": lines[1:] if len(lines) > 1 else []
            })
    return result

def generate_posters(record, templates, output_dir):
    """为一条记录生成全部海报"""
    output_dir.mkdir(parents=True, exist_ok=True)

    zodiac1 = record["zodiac1"]
    zodiac2 = record["zodiac2"]
    sections = parse_record_content(record["content"])

    # 1. 封面
    cover_data = {
        "zodiac1": zodiac1,
        "zodiac2": zodiac2,
        "match_percent": record["match_percent"],
        "theme_title": record["theme_title"],
        "theme_desc": record["theme_desc"],
        "tagline_line1": record["tagline_line1"],
        "tagline_highlight": record["tagline_highlight"],
        "tagline_rest": record["tagline_rest"],
    }
    cover_svg = render_cover(templates['cover'], cover_data)
    (output_dir / "01_cover.svg").write_text(cover_svg, encoding="utf-8")
    (output_dir / "01_cover.html").write_text(wrap_svg_html(cover_svg), encoding="utf-8")

    # 2-6. 内页
    for i, section in enumerate(sections[:5], start=1):
        page_data = {
            "zodiac1": zodiac1,
            "zodiac2": zodiac2,
            "part_num": f"0{i}",
            "section_title": section["title"],
            "content_lines": section["content"],
            "quote": record["quotes"][i-1] if i <= len(record.get("quotes", [])) else "",
            "page_num": f"0 {i+1}",
        }
        page_svg = render_page(templates['page'], page_data)
        (output_dir / f"0{i+1}_page.svg").write_text(page_svg, encoding="utf-8")
        (output_dir / f"0{i+1}_page.html").write_text(wrap_svg_html(page_svg), encoding="utf-8")

    # 7. 结尾页
    end_data = {
        "zodiac1": zodiac1,
        "zodiac2": zodiac2,
        "match_percent": record["match_percent"],
        "summary_highlight": record["summary_highlight"],
        "summary_line1_before": record["summary_line1_before"],
        "summary_line1_highlight": record["summary_line1_highlight"],
        "summary_line2": record["summary_line2"],
        "blessing_line1": record["blessing_line1"],
        "blessing_line2": record["blessing_line2"],
        "page_num": "07",
    }
    end_svg = render_end(templates['end'], end_data)
    (output_dir / "07_end.svg").write_text(end_svg, encoding="utf-8")
    (output_dir / "07_end.html").write_text(wrap_svg_html(end_svg), encoding="utf-8")

    print(f"✅ {record['title']} 生成完成: {output_dir}")

# 记录数据 - 符合新模板变量
RECORDS = [
    {
        "title": "射手遇到白羊",
        "zodiac1": "射手座",
        "zodiac2": "白羊座",
        "match_percent": "88",
        "theme_title": "火象神仙",
        "theme_desc": "两团火撞在一起",
        "tagline_line1": "两个人一见面",
        "tagline_highlight": "就像认识了很久",
        "tagline_rest": "",
        "summary_highlight": "火象神仙组合",
        "summary_line1_before": "一起",
        "summary_line1_highlight": "燃烧",
        "summary_line2": "最快乐",
        "blessing_line1": "愿每一次碰撞",
        "blessing_line2": "都能擦出最美的火花",
        "content": """第一眼
射手觉得白羊|好直接
白羊觉得射手|好有趣
两个人一见面
就像认识了很久

一起疯的时候
说干就干
说走就走
想法|一拍即合
行动力|直接拉满
最怕的就是冷静

吵架的时候
射手和白羊吵架
来得快|去得更快
上一秒还在吼
下一秒就忘了吵什么
两个都|不记仇

最甜的瞬间
白羊|护着|射手的时候
射手|陪|白羊冲动的时候
两个人都觉得
终于有人懂我的节奏

最难的时刻
两个都想|当老大
都|不肯先低头
火上浇油是常态
但好在
谁都不会真的走""",
        "quotes": ["火遇火，一见如故", "说走就走，才是我们的浪漫", "打归打，闹归闹，谁也别想跑", "终于有人跟得上我的节奏", "打归打，闹归闹，谁也别想跑"]
    },
    {
        "title": "射手遇到金牛",
        "zodiac1": "射手座",
        "zodiac2": "金牛座",
        "match_percent": "55",
        "theme_title": "互补挑战",
        "theme_desc": "一个想飞一个要稳",
        "tagline_line1": "节奏不同",
        "tagline_highlight": "但心意相通",
        "tagline_rest": "",
        "summary_highlight": "火土组合",
        "summary_line1_before": "需要",
        "summary_line1_highlight": "很多很多",
        "summary_line2": "耐心",
        "blessing_line1": "愿你们在磨合中",
        "blessing_line2": "找到彼此的节奏",
        "content": """第一眼
射手觉得金牛|好踏实
金牛觉得射手|好洒脱
互相吸引
又互相看不懂

约会的时候
射手|说走就走
金牛|要做攻略
射手说随便吃
金牛要看评分
节奏永远对不上

吵架的时候
射手说完就想|翻篇
金牛却还在|生闷气
一个急
一个慢
越急越慢越崩溃

最甜的瞬间
金牛默默记住射手的喜好
射手带金牛去|没去过的地方
原来不一样
也可以互补

最难的时刻
射手觉得金牛|太无聊
金牛觉得射手|不靠谱
谁都觉得自己没错
但又舍不得放手""",
        "quotes": ["一个追风，一个守土", "节奏不同，但心意相通", "急什么？慢慢来", "不一样，才有意思", "舍不得，就好好珍惜"]
    },
    {
        "title": "射手遇到巨蟹",
        "zodiac1": "射手座",
        "zodiac2": "巨蟹座",
        "match_percent": "50",
        "theme_title": "温暖与自由",
        "theme_desc": "自由和安全感的拉扯",
        "tagline_line1": "一个被暖到",
        "tagline_highlight": "一个被照亮",
        "tagline_rest": "",
        "summary_highlight": "火水组合",
        "summary_line1_before": "要学会",
        "summary_line1_highlight": "彼此理解",
        "summary_line2": "",
        "blessing_line1": "愿你们在拉扯中",
        "blessing_line2": "找到平衡的温度",
        "content": """第一眼
射手觉得巨蟹|好温柔
巨蟹觉得射手|好阳光
一个被暖到
一个被照亮

相处的时候
射手|想出去浪
巨蟹|想待在家
射手说别粘人
巨蟹说你不爱我
安全感永远不够用

吵架的时候
射手|说话太直
巨蟹|玻璃心碎一地
一个觉得没什么
一个觉得伤透了

最甜的瞬间
巨蟹把射手|照顾得很好
射手带巨蟹|看更大的世界
原来可以既温暖
又自由

最难的时刻
射手觉得|被束缚
巨蟹觉得|被忽略
一个要飞
一个要留
谁都不想妥协""",
        "quotes": ["温柔遇上阳光", "安全感是一道难题", "直话直说？小心玻璃心", "温暖和自由可以兼得", "飞与留的抉择"]
    },
    {
        "title": "射手遇到处女",
        "zodiac1": "射手座",
        "zodiac2": "处女座",
        "match_percent": "45",
        "theme_title": "意外碰撞",
        "theme_desc": "粗线条撞上细节控",
        "tagline_line1": "一个不拘小节",
        "tagline_highlight": "一个精益求精",
        "tagline_rest": "",
        "summary_highlight": "火土组合",
        "summary_line1_before": "挑战很大",
        "summary_line1_highlight": "但值得尝试",
        "summary_line2": "",
        "blessing_line1": "愿你们在碰撞中",
        "blessing_line2": "发现彼此的闪光点",
        "content": """第一眼
射手觉得处女|好认真
处女觉得射手|好随性
一个不拘小节
一个精益求精

相处的时候
射手|随手一放
处女|强迫症发作
射手说差不多得了
处女说怎么能差不多
标准永远统一不了

吵架的时候
射手嫌处女|太啰嗦
处女嫌射手|太粗心
一个觉得累
一个觉得烦

最甜的瞬间
处女帮射手|收拾烂摊子
射手带处女|放松下来
原来可以互相成全

最难的时刻
射手觉得|被挑剔
处女觉得|不被重视
一个要自由
一个要完美
谁都觉得委屈""",
        "quotes": ["随性遇上认真", "差不多？不存在的", "累和烦，都是爱的代价", "成全彼此最浪漫", "委屈都是暂时的"]
    },
    {
        "title": "射手遇到天秤",
        "zodiac1": "射手座",
        "zodiac2": "天秤座",
        "match_percent": "78",
        "theme_title": "默契天成",
        "theme_desc": "互相欣赏各自美丽",
        "tagline_line1": "两个人聊起来",
        "tagline_highlight": "停都停不下来",
        "tagline_rest": "",
        "summary_highlight": "火风组合",
        "summary_line1_before": "轻松又",
        "summary_line1_highlight": "和谐",
        "summary_line2": "的搭配",
        "blessing_line1": "愿你们的相遇",
        "blessing_line2": "永远保持这份默契",
        "content": """第一眼
射手觉得天秤|好优雅
天秤觉得射手|好有趣
两个人聊起来
停都停不下来

一起玩的时候
射手|负责出主意
天秤|负责优化细节
一个敢想
一个敢美
怎么搭都好看

吵架的时候
射手|说话太直
天秤|玻璃心但不说
一个不懂察言观色
一个憋着不讲
需要主动沟通

最甜的瞬间
天秤懂射手的|幽默
射手欣赏天秤的|品味
在一起
就是最好的状态

最难的时刻
射手嫌天秤|犹豫不决
天秤嫌射手|太冲动
但好在都理性
吵完还是能好好说话""",
        "quotes": ["优雅遇上有趣", "敢想+敢美=天生一对", "直话伤人，但真诚可贵", "懂你，是最好的告白", "理性是最后的防线"]
    }
]

def main():
    # 从模板文件读取SVG模板
    templates = extract_templates_from_md(TEMPLATE_PATH)

    if not templates.get('cover') or not templates.get('page') or not templates.get('end'):
        print("❌ 无法从TEMPLATE.md提取模板")
        return

    print(f"✅ 已从TEMPLATE.md加载模板: cover, page, end")

    base_dir = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09")

    for record in RECORDS:
        output_dir = base_dir / record["title"]
        generate_posters(record, templates, output_dir)

if __name__ == "__main__":
    main()
