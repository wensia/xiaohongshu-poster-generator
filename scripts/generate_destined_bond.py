#!/usr/bin/env python3
"""
批量生成命定之约风套图
"""
import os
from pathlib import Path

# 星座图标SVG
ZODIAC_ICONS = {
    "射手座": '<path d="M4 20L20 4M20 4H10M20 4V14" stroke="#B86B4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "金牛座": '<path d="M7 12C7 9 9 7 12 7C15 7 17 9 17 12M12 7V3M5 5C3 7 3 10 5 12M19 5C21 7 21 10 19 12M7 17C7 19 9 21 12 21C15 21 17 19 17 17M7 17H17" stroke="#B86B4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "巨蟹座": '<path d="M4 10C4 6 8 4 12 4C16 4 20 6 20 10M4 14C4 18 8 20 12 20C16 20 20 18 20 14M6 10C6 10 6 8 8 8M18 10C18 10 18 8 16 8M6 14C6 14 6 16 8 16M18 14C18 14 18 16 16 16" stroke="#B86B4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "处女座": '<path d="M8 4V16M8 16C8 18 10 20 12 20M12 4V12M12 12C12 14 14 16 16 16M16 4V16M16 16C18 16 20 14 20 12" stroke="#B86B4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "天秤座": '<path d="M4 16H20M12 16V8M8 8H16M6 12C6 10 8 8 10 8M18 12C18 10 16 8 14 8" stroke="#B86B4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "白羊座": '<path d="M4 20C4 15 8 12 12 12C16 12 20 15 20 20M12 12V4M8 8C6 6 6 4 8 2M16 8C18 6 18 4 16 2" stroke="#B86B4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
}

def get_zodiac_icon(zodiac, size=80):
    icon = ZODIAC_ICONS.get(zodiac, ZODIAC_ICONS["射手座"])
    return f'<svg x="-{size//2}" y="-{size//2}" width="{size}" height="{size}" viewBox="0 0 24 24">{icon}</svg>'

def get_zodiac_short(zodiac):
    return zodiac.replace("座", "")

def create_cover(zodiac1, zodiac2, subtitle, match_percent, tagline1, tagline_highlight):
    z1_short = get_zodiac_short(zodiac1)
    z2_short = get_zodiac_short(zodiac2)
    title = f"{z1_short}遇到{z2_short}"

    return f'''<!-- [STYLE: 命定之约风] [TYPE: cover] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');</style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/><stop offset="50%" stop-color="#F8EDE5"/><stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/><stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#B86B4A" letter-spacing="2">{zodiac1} × {zodiac2}</text>
    <text x="340" y="130" font-family="Georgia, serif" font-size="24" fill="#D4C9BE">·</text>
    <text x="370" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#7D7067" letter-spacing="3">命定之约</text>
    <g transform="translate(940, 110)">
      <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
    </g>
  </g>
  <g id="dual-zodiac" transform="translate(540, 320)">
    <g transform="translate(-120, 0)">{get_zodiac_icon(zodiac1)}</g>
    <g transform="translate(0, 40)">
      <path d="M-25,0 C-25,-15 -10,-15 0,0 C10,15 25,15 25,0 C25,-15 10,-15 0,0 C-10,15 -25,15 -25,0" fill="none" stroke="#B86B4A" stroke-width="2.5"/>
    </g>
    <g transform="translate(120, 0)">{get_zodiac_icon(zodiac2)}</g>
  </g>
  <g id="match-index" transform="translate(540, 500)">
    <text x="0" y="0" font-family="Georgia, serif" font-size="20" fill="#8B7355" text-anchor="middle" letter-spacing="4">MATCH INDEX</text>
    <text x="0" y="55" font-family="Georgia, serif" font-size="64" font-weight="600" fill="#B86B4A" text-anchor="middle">{match_percent}%</text>
  </g>
  <rect x="490" y="600" width="100" height="3" fill="#B86B4A"/>
  <g id="cover-title" transform="translate(540, 720)">
    <text x="0" y="0" font-family="Noto Serif SC, serif" font-size="72" font-weight="600" fill="#4A3F35" text-anchor="middle" letter-spacing="6">{title}</text>
    <text x="0" y="80" font-family="Noto Serif SC, serif" font-size="32" fill="#7D7067" text-anchor="middle" letter-spacing="4">{subtitle}</text>
  </g>
  <g id="tagline" transform="translate(540, 920)">
    <text x="0" y="0" font-family="Noto Serif SC, serif" font-size="28" fill="#7D7067" text-anchor="middle" letter-spacing="3">{tagline1}</text>
    <text x="0" y="50" font-family="Noto Serif SC, serif" font-size="28" text-anchor="middle" letter-spacing="3">
      <tspan fill="#B86B4A">{tagline_highlight}</tspan>
    </text>
  </g>
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#7D7067" text-anchor="end" letter-spacing="4">0 1</text>
  </g>
</svg>'''

def create_page(zodiac1, zodiac2, bond_num, section_title, lines, quote, page_num):
    content_lines = ""
    y = 0
    for line in lines:
        if isinstance(line, tuple):
            text, highlight = line
            content_lines += f'    <text y="{y}" font-family="Noto Serif SC, serif" font-size="32" fill="#4A3F35" letter-spacing="2">{text}<tspan fill="#B86B4A">{highlight}</tspan></text>\n'
        elif "|" in line:
            parts = line.split("|")
            content_lines += f'    <text y="{y}" font-family="Noto Serif SC, serif" font-size="32" letter-spacing="2"><tspan fill="#B86B4A">{parts[0]}</tspan><tspan fill="#4A3F35">{parts[1]}</tspan></text>\n'
        else:
            content_lines += f'    <text y="{y}" font-family="Noto Serif SC, serif" font-size="32" fill="#4A3F35" letter-spacing="2">{line}</text>\n'
        y += 61

    return f'''<!-- [STYLE: 命定之约风] [TYPE: page] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');</style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/><stop offset="50%" stop-color="#F8EDE5"/><stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/><stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#B86B4A" letter-spacing="2">{zodiac1} × {zodiac2}</text>
    <text x="340" y="130" font-family="Georgia, serif" font-size="24" fill="#D4C9BE">·</text>
    <text x="370" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#7D7067" letter-spacing="3">命定之约</text>
    <g transform="translate(940, 110)">
      <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
    </g>
  </g>
  <text x="100" y="220" font-family="Georgia, serif" font-size="24" fill="#B86B4A" letter-spacing="6">BOND 0{bond_num}</text>
  <text x="100" y="310" font-family="Noto Serif SC, serif" font-size="56" font-weight="600" fill="#4A3F35" letter-spacing="4">{section_title}</text>
  <rect x="100" y="340" width="80" height="3" fill="#B86B4A"/>
  <g id="content" transform="translate(100, 480)">
{content_lines}  </g>
  <g id="quote" transform="translate(100, 1050)">
    <line x1="0" y1="0" x2="0" y2="60" stroke="#B86B4A" stroke-width="3"/>
    <text x="30" y="40" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#7D7067" letter-spacing="2">"{quote}"</text>
  </g>
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#7D7067" text-anchor="end" letter-spacing="4">0 {page_num}</text>
  </g>
</svg>'''

def create_end(zodiac1, zodiac2, match_percent, element_combo, summary, ending1, ending2):
    z1_short = get_zodiac_short(zodiac1)
    z2_short = get_zodiac_short(zodiac2)

    return f'''<!-- [STYLE: 命定之约风] [TYPE: end] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');</style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/><stop offset="50%" stop-color="#F8EDE5"/><stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/><stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#B86B4A" letter-spacing="2">{zodiac1} × {zodiac2}</text>
    <text x="340" y="130" font-family="Georgia, serif" font-size="24" fill="#D4C9BE">·</text>
    <text x="370" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#7D7067" letter-spacing="3">命定之约</text>
    <g transform="translate(940, 110)">
      <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
    </g>
  </g>
  <g id="centered-content" transform="translate(540, 0)">
    <text x="0" y="220" font-family="Georgia, serif" font-size="24" fill="#B86B4A" letter-spacing="6" text-anchor="middle">DESTINY</text>
    <g transform="translate(0, 300)">
      <g transform="translate(-60, 0)">{get_zodiac_icon(zodiac1, 40)}</g>
      <path d="M-15,0 C-15,-8 -5,-8 0,0 C5,8 15,8 15,0 C15,-8 5,-8 0,0 C-5,8 -15,8 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" transform="translate(0, 20)"/>
      <g transform="translate(60, 0)">{get_zodiac_icon(zodiac2, 40)}</g>
    </g>
    <rect x="-40" y="380" width="80" height="3" fill="#B86B4A"/>
    <g id="summary" transform="translate(0, 500)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="36" fill="#4A3F35" text-anchor="middle" letter-spacing="3">{z1_short} × {z2_short}</text>
      <text y="70" font-family="Georgia, serif" font-size="48" font-weight="600" fill="#B86B4A" text-anchor="middle">{match_percent}%</text>
      <text y="150" font-family="Noto Serif SC, serif" font-size="32" fill="#4A3F35" text-anchor="middle" letter-spacing="2"><tspan fill="#B86B4A">{element_combo}</tspan></text>
      <text y="211" font-family="Noto Serif SC, serif" font-size="32" fill="#4A3F35" text-anchor="middle" letter-spacing="2">{summary}</text>
    </g>
    <g id="content-divider" transform="translate(0, 800)">
      <line x1="-70" y1="0" x2="-20" y2="0" stroke="#D4C9BE" stroke-width="1"/>
      <path d="M-8,0 C-8,-5 -3,-5 0,0 C3,5 8,5 8,0 C8,-5 3,-5 0,0 C-3,5 -8,5 -8,0" fill="none" stroke="#B86B4A" stroke-width="1.5"/>
      <line x1="20" y1="0" x2="70" y2="0" stroke="#D4C9BE" stroke-width="1"/>
    </g>
    <g id="ending" transform="translate(0, 900)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#7D7067" text-anchor="middle" letter-spacing="3">{ending1}</text>
      <text y="50" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#7D7067" text-anchor="middle" letter-spacing="3">{ending2}</text>
      <g transform="translate(0, 120)">
        <line x1="-80" y1="0" x2="-25" y2="0" stroke="#D4C9BE" stroke-width="2"/>
        <text x="0" y="8" font-family="Georgia, serif" font-size="22" fill="#B86B4A" text-anchor="middle" letter-spacing="5">BOND</text>
        <line x1="25" y1="0" x2="80" y2="0" stroke="#D4C9BE" stroke-width="2"/>
      </g>
    </g>
  </g>
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#7D7067" text-anchor="end" letter-spacing="4">0 7</text>
  </g>
</svg>'''

def wrap_svg_html(svg_content):
    return f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
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

def parse_content(content_text):
    """解析正文内容，返回各章节数据"""
    sections = content_text.strip().split("\n\n")
    result = []

    for section in sections:
        lines = section.strip().split("\n")
        if lines:
            title = lines[0]
            content = lines[1:] if len(lines) > 1 else []
            result.append({"title": title, "content": content})

    return result

# 记录数据
RECORDS = [
    {
        "title": "射手遇到金牛",
        "zodiac1": "射手座",
        "zodiac2": "金牛座",
        "subtitle": "一个想飞一个要稳",
        "match_percent": "55",
        "element_combo": "火土组合",
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
        "summary": "需要很多很多耐心",
        "ending1": "愿你们在磨合中",
        "ending2": "找到彼此的节奏",
        "quotes": ["一个追风，一个守土", "节奏不同，但心意相通", "急什么？慢慢来", "不一样，才有意思", "舍不得，就好好珍惜"]
    },
    {
        "title": "射手遇到巨蟹",
        "zodiac1": "射手座",
        "zodiac2": "巨蟹座",
        "subtitle": "自由和安全感的拉扯",
        "match_percent": "50",
        "element_combo": "火水组合",
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
        "summary": "要学会彼此理解",
        "ending1": "愿你们在拉扯中",
        "ending2": "找到平衡的温度",
        "quotes": ["温柔遇上阳光", "安全感是一道难题", "直话直说？小心玻璃心", "温暖和自由可以兼得", "飞与留的抉择"]
    },
    {
        "title": "射手遇到处女",
        "zodiac1": "射手座",
        "zodiac2": "处女座",
        "subtitle": "粗线条撞上细节控",
        "match_percent": "45",
        "element_combo": "火土组合",
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
        "summary": "挑战很大但值得尝试",
        "ending1": "愿你们在碰撞中",
        "ending2": "发现彼此的闪光点",
        "quotes": ["随性遇上认真", "差不多？不存在的", "累和烦，都是爱的代价", "成全彼此最浪漫", "委屈都是暂时的"]
    },
    {
        "title": "射手遇到天秤",
        "zodiac1": "射手座",
        "zodiac2": "天秤座",
        "subtitle": "互相欣赏各自美丽",
        "match_percent": "78",
        "element_combo": "火风组合",
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
        "summary": "轻松又和谐的搭配",
        "ending1": "愿你们的相遇",
        "ending2": "永远保持这份默契",
        "quotes": ["优雅遇上有趣", "敢想+敢美=天生一对", "直话伤人，但真诚可贵", "懂你，是最好的告白", "理性是最后的防线"]
    }
]

def main():
    base_dir = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09")

    for record in RECORDS:
        dir_name = record["title"].replace("射手遇到", "射手遇到")
        output_dir = base_dir / dir_name
        output_dir.mkdir(parents=True, exist_ok=True)

        zodiac1 = record["zodiac1"]
        zodiac2 = record["zodiac2"]

        # 解析内容
        sections = record["content"].strip().split("\n\n")

        # 1. 封面
        svg = create_cover(
            zodiac1, zodiac2,
            record["subtitle"],
            record["match_percent"],
            sections[0].split("\n")[1] if len(sections) > 0 else "",
            sections[0].split("\n")[2] if len(sections) > 0 and len(sections[0].split("\n")) > 2 else ""
        )
        (output_dir / "01_cover.svg").write_text(svg, encoding="utf-8")
        (output_dir / "01_cover.html").write_text(wrap_svg_html(svg), encoding="utf-8")

        # 2-6. 内容页
        section_titles = ["第一眼", "约会/相处", "吵架的时候", "最甜的瞬间", "最难的时刻"]
        for i, section in enumerate(sections[:5], start=1):
            lines = section.strip().split("\n")
            title = lines[0]
            content = lines[1:]

            # 处理高亮
            processed_lines = []
            for line in content:
                if "|" in line:
                    parts = line.split("|")
                    processed_lines.append(f"{parts[0]}|{parts[1]}")
                else:
                    processed_lines.append(line)

            svg = create_page(
                zodiac1, zodiac2,
                i,
                title,
                processed_lines,
                record["quotes"][i-1] if i <= len(record["quotes"]) else "",
                i + 1
            )
            (output_dir / f"0{i+1}_page.svg").write_text(svg, encoding="utf-8")
            (output_dir / f"0{i+1}_page.html").write_text(wrap_svg_html(svg), encoding="utf-8")

        # 7. 结尾页
        svg = create_end(
            zodiac1, zodiac2,
            record["match_percent"],
            record["element_combo"],
            record["summary"],
            record["ending1"],
            record["ending2"]
        )
        (output_dir / "07_end.svg").write_text(svg, encoding="utf-8")
        (output_dir / "07_end.html").write_text(wrap_svg_html(svg), encoding="utf-8")

        print(f"✅ {record['title']} 生成完成: {output_dir}")

if __name__ == "__main__":
    main()
