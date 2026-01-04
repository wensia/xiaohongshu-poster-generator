#!/usr/bin/env python3
"""生成7套海报的完整脚本"""
import os
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# 输出目录
OUTPUT_BASE = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/04"

# 7套海报数据
POSTER_DATA = [
    {
        "record_id": "recv7gm4S6DxyK",
        "title": "射手座和天蝎座，千万别在一起？",
        "short_title": "千万别在一起",
        "template": "经典强调风",
        "content": [
            "射手座爱自由\n天蝎座爱占有\n一个想飞 一个想绑",
            "射手座说"我需要空间"\n天蝎座听成"你不爱我了"",
            "射手座的热情来得快去得快\n天蝎座的感情一旦开始就是一辈子",
            "射手座害怕被束缚\n天蝎座害怕被抛弃",
        ],
        "folder": "射手座-千万别在一起-经典"
    },
    {
        "record_id": "recv7gpMRkeDOK",
        "title": "射手座的专注力开关",
        "short_title": "专注力开关",
        "template": "简约边框风",
        "content": [
            "射手座的能量像火\n点对方向就能冲\n方向不清时就会四处跑",
            "你不是没有执行力\n只是大脑还在找\n"值得投入"的理由",
            "把目标缩成一句话\n比如"把作品做成系列"\n"把健身变成习惯"",
            "然后定义完成标准\n一步一步来",
        ],
        "folder": "射手座-专注力开关"
    },
    {
        "record_id": "recv7gpNalnLyp",
        "title": "射手座最舒服的职场关系",
        "short_title": "职场关系",
        "template": "杂志双线风",
        "content": [
            "射手座在职场最怕\n事事报备 步步审批",
            "一旦感到被限制\n热情会快速掉线",
            "对你最有效的管理方式是\n目标清楚 过程放手",
            "适合你的岗位形态是\n项目制 跨部门协作\n对外沟通型",
        ],
        "folder": "射手座-职场关系"
    },
    {
        "record_id": "recv7gpNujOo27",
        "title": "射手座社交电量表",
        "short_title": "社交电量表",
        "template": "优雅留白风",
        "content": [
            "射手座表面热情\n但社交电量掉得很快",
            "连续解释、重复寒暄\n无效聚会\n是你最耗能的三件事",
            "当你开始"只回表情"\n"约饭推到下周"\n就是电量不足的信号",
            "别硬撑\n硬撑只会把热情消耗成冷漠",
        ],
        "folder": "射手座-社交电量表"
    },
    {
        "record_id": "recv7gpNOuwEQz",
        "title": "射手座的消费指南",
        "short_title": "消费指南",
        "template": "暖色编辑风",
        "content": [
            "射手座最容易为\n"新鲜感"和"好玩的体验"买单",
            "这本来是优势\n人生因此更丰富\n但冲动一来 预算就散了",
            "把消费分成三类\n体验 / 成长 / 情绪补偿",
            "前两类可以投入\n第三类需要警惕",
        ],
        "folder": "射手座-消费指南"
    },
    {
        "record_id": "recv7gpO7IE6y4",
        "title": "射手座的边界感练习",
        "short_title": "边界感练习",
        "template": "极简暖色风",
        "content": [
            "射手座常被说"忽冷忽热"\n其实是你在无声地拉开距离",
            "问题不在冷\n而在你太晚才开口",
            "边界最好在"还没累"的时候说\n比如"我今晚想自己待会儿"",
            "提前说\n比事后消失更温柔",
        ],
        "folder": "射手座-边界感练习"
    },
    {
        "record_id": "recv7gpOqwZMfb",
        "title": "射手座的轻计划学习法",
        "short_title": "轻计划学习法",
        "template": "极简留白",
        "content": [
            "射手座最怕死板学习\n但你很擅长把学习变成探索",
            "关键不是逼自己坐住\n而是让兴趣变成路线",
            "先用7天试跑\n只学一个小主题\n每天30分钟",
            "7天后再决定\n要不要继续",
        ],
        "folder": "射手座-轻计划学习法"
    }
]

# 射手座SVG图标
SAGITTARIUS_SVG = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <line x1="20" y1="80" x2="80" y2="20" stroke-linecap="round"/>
  <line x1="80" y1="20" x2="55" y2="20" stroke-linecap="round"/>
  <line x1="80" y1="20" x2="80" y2="45" stroke-linecap="round"/>
  <line x1="25" y1="45" x2="55" y2="75" stroke-linecap="round"/>
</svg>'''

# ========== 经典强调风模板 ==========
def generate_classic_cover(title, keyword="配对指南"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{
      width: 1080px; height: 1440px; position: relative;
      background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%);
      font-family: 'Noto Serif SC', serif; overflow: hidden;
    }}
    .poster::before {{
      content: ''; position: absolute; inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.05; pointer-events: none; z-index: 1;
    }}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-bg {{ position: absolute; top: 120px; left: 50%; transform: translateX(-50%); font-size: 180px; font-weight: 700; color: rgba(193, 95, 60, 0.08); letter-spacing: 20px; z-index: 0; white-space: nowrap; }}
    .circle-deco {{ position: absolute; width: 100px; height: 100px; border: 2px solid rgba(193, 95, 60, 0.15); border-radius: 50%; }}
    .circle-inner {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 50px; height: 50px; background: rgba(193, 95, 60, 0.08); border-radius: 50%; }}
    .zodiac-header {{ position: absolute; top: 180px; left: 50%; transform: translateX(-50%); text-align: center; z-index: 10; }}
    .zodiac-icon-large svg {{ width: 80px; height: 80px; stroke: #C15F3C; stroke-width: 2; fill: none; margin-bottom: 20px; }}
    .zodiac-name {{ font-size: 72px; font-weight: 700; color: #C15F3C; letter-spacing: 16px; margin-bottom: 10px; }}
    .zodiac-year {{ font-size: 28px; font-weight: 400; color: #9A958A; letter-spacing: 8px; }}
    .main {{ position: absolute; top: 520px; left: 80px; right: 80px; z-index: 10; text-align: center; }}
    .keyword {{ display: inline-block; background: linear-gradient(135deg, #C15F3C 0%, #D4765A 100%); color: #fff; font-size: 36px; font-weight: 500; letter-spacing: 8px; padding: 14px 32px; border-radius: 2px; margin-bottom: 50px; }}
    .main-title {{ font-size: 72px; font-weight: 600; color: #2D2D2D; letter-spacing: 6px; line-height: 1.4; margin-bottom: 40px; }}
    .accent {{ color: #C15F3C; font-weight: 500; }}
    .sub-title {{ font-size: 34px; font-weight: 400; color: #5A5A5A; letter-spacing: 4px; margin-bottom: 50px; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-bg">射手座</div>
    <div class="circle-deco" style="top: 140px; right: 80px;"><div class="circle-inner"></div></div>
    <div class="header">
      <span class="tag">射手座 · 天蝎座</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="zodiac-header">
      <div class="zodiac-icon-large">{SAGITTARIUS_SVG}</div>
      <div class="zodiac-name">射手座</div>
      <div class="zodiac-year">2026</div>
    </div>
    <div class="main">
      <div class="keyword">{keyword}</div>
      <h1 class="main-title"><span class="accent">千万</span>别在一起？</h1>
      <p class="sub-title">射手座和天蝎座的相处真相</p>
    </div>
    <div class="footer">
      <span class="footer-text">星座配对解读</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

def generate_classic_content(text, page_num, header_tag="射手座 · 配对解读"):
    lines = text.split('\n')
    first_line = lines[0] if lines else ""
    rest_lines = '<br/>'.join(lines[1:]) if len(lines) > 1 else ""

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
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
      <span class="tag">{header_tag}</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="main">
      <p class="think"><span class="keyword">{first_line}</span></p>
      <div class="truth-box">
        <p class="truth">{rest_lines}</p>
      </div>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">{page_num:02d}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

def generate_classic_ending(quote="两个极端，也许就是最好的互补"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 72px; height: 72px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 42px; font-weight: 600; color: #C15F3C; letter-spacing: 16px; margin-bottom: 50px; }}
    .quote {{ font-size: 46px; font-weight: 500; color: #3D3D3D; letter-spacing: 4px; line-height: 1.8; max-width: 700px; margin-bottom: 50px; }}
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
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote">{quote}</p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS × SCORPIO</span>
      <span class="page-num">06</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

# ========== 简约边框风模板 ==========
def generate_border_cover(title, keyword="专注力"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-bg {{ position: absolute; top: 120px; left: 50%; transform: translateX(-50%); font-size: 180px; font-weight: 700; color: rgba(193, 95, 60, 0.08); letter-spacing: 20px; z-index: 0; white-space: nowrap; }}
    .corner-bracket {{ position: absolute; width: 60px; height: 60px; border: 2px solid rgba(193, 95, 60, 0.2); }}
    .corner-bracket.top-left {{ top: 140px; left: 70px; border-right: none; border-bottom: none; }}
    .corner-bracket.bottom-right {{ bottom: 140px; right: 70px; border-left: none; border-top: none; }}
    .zodiac-header {{ position: absolute; top: 180px; left: 50%; transform: translateX(-50%); text-align: center; z-index: 10; }}
    .zodiac-icon-large svg {{ width: 80px; height: 80px; stroke: #C15F3C; stroke-width: 2; fill: none; margin-bottom: 20px; }}
    .zodiac-name {{ font-size: 72px; font-weight: 700; color: #C15F3C; letter-spacing: 16px; margin-bottom: 10px; }}
    .zodiac-year {{ font-size: 28px; font-weight: 400; color: #9A958A; letter-spacing: 8px; }}
    .main {{ position: absolute; top: 520px; left: 80px; right: 80px; z-index: 10; text-align: center; }}
    .keyword {{ display: inline-block; font-size: 36px; font-weight: 500; color: #C15F3C; letter-spacing: 8px; padding: 12px 28px; border: 2px solid #C15F3C; border-radius: 2px; margin-bottom: 50px; }}
    .main-title {{ font-size: 72px; font-weight: 600; color: #2D2D2D; letter-spacing: 6px; line-height: 1.4; margin-bottom: 40px; }}
    .accent {{ color: #C15F3C; font-weight: 500; }}
    .quote {{ font-size: 26px; font-weight: 400; color: #9A958A; letter-spacing: 3px; font-style: italic; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-bg">射手座</div>
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket bottom-right"></div>
    <div class="header">
      <span class="tag">射手座 · 自我管理</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="zodiac-header">
      <div class="zodiac-icon-large">{SAGITTARIUS_SVG}</div>
      <div class="zodiac-name">射手座</div>
      <div class="zodiac-year">2026</div>
    </div>
    <div class="main">
      <div class="keyword">{keyword}</div>
      <h1 class="main-title"><span class="accent">专注力</span>开关</h1>
      <p class="quote">「 找到方向，能量就会聚焦 」</p>
    </div>
    <div class="footer">
      <span class="footer-text">射手座自我管理</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

def generate_border_content(text, page_num, header_tag="射手座 · 专注力"):
    lines = text.split('\n')
    first_line = lines[0] if lines else ""
    rest_lines = '<br/>'.join(lines[1:]) if len(lines) > 1 else ""

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .corner-bracket {{ position: absolute; width: 40px; height: 40px; border: 2px solid rgba(193, 95, 60, 0.15); }}
    .corner-bracket.top-left {{ top: 60px; left: 60px; border-right: none; border-bottom: none; }}
    .corner-bracket.bottom-right {{ bottom: 60px; right: 60px; border-left: none; border-top: none; }}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 100px; }}
    .think {{ font-size: 44px; color: #5A5A5A; letter-spacing: 3px; line-height: 1.7; margin-bottom: 60px; }}
    .keyword {{ color: #C15F3C; font-weight: 500; }}
    .truth-box {{ background: transparent; padding: 40px 50px; border: 2px solid rgba(193, 95, 60, 0.2); border-radius: 4px; }}
    .truth {{ font-size: 38px; color: #3D3D3D; letter-spacing: 2px; line-height: 1.8; }}
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
      <span class="tag">{header_tag}</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="main">
      <p class="think"><span class="keyword">{first_line}</span></p>
      <div class="truth-box">
        <p class="truth">{rest_lines}</p>
      </div>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">{page_num:02d}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

def generate_border_ending(quote="方向对了，专注就不是难事"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .corner-bracket {{ position: absolute; width: 60px; height: 60px; border: 2px solid rgba(193, 95, 60, 0.2); }}
    .corner-bracket.top-left {{ top: 60px; left: 60px; border-right: none; border-bottom: none; }}
    .corner-bracket.top-right {{ top: 60px; right: 60px; border-left: none; border-bottom: none; }}
    .corner-bracket.bottom-left {{ bottom: 60px; left: 60px; border-right: none; border-top: none; }}
    .corner-bracket.bottom-right {{ bottom: 60px; right: 60px; border-left: none; border-top: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 72px; height: 72px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 42px; font-weight: 600; color: #C15F3C; letter-spacing: 16px; margin-bottom: 50px; }}
    .quote {{ font-size: 46px; font-weight: 500; color: #3D3D3D; letter-spacing: 4px; line-height: 1.8; max-width: 700px; margin-bottom: 50px; }}
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
      <p class="quote">{quote}</p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">06</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

# ========== 杂志双线风模板 ==========
def generate_magazine_cover(title, keyword="职场关系"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-bg {{ position: absolute; top: 120px; left: 50%; transform: translateX(-50%); font-size: 180px; font-weight: 700; color: rgba(193, 95, 60, 0.08); letter-spacing: 20px; z-index: 0; white-space: nowrap; }}
    .double-border {{ position: absolute; top: 130px; left: 70px; right: 70px; bottom: 130px; border: 1px solid rgba(193, 95, 60, 0.1); z-index: 2; }}
    .double-border::before {{ content: ''; position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px; border: 1px solid rgba(193, 95, 60, 0.05); }}
    .stars-scatter {{ position: absolute; width: 180px; height: 180px; z-index: 3; }}
    .star {{ position: absolute; width: 10px; height: 10px; background: #C15F3C; clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%); }}
    .star:nth-child(1) {{ top: 20px; left: 30px; opacity: 0.35; }}
    .star:nth-child(2) {{ top: 60px; left: 130px; opacity: 0.5; transform: scale(0.7); }}
    .star:nth-child(3) {{ top: 100px; left: 50px; opacity: 0.25; transform: scale(1.1); }}
    .star:nth-child(4) {{ top: 30px; left: 150px; opacity: 0.4; transform: scale(0.5); }}
    .star:nth-child(5) {{ top: 140px; left: 100px; opacity: 0.3; }}
    .zodiac-header {{ position: absolute; top: 180px; left: 50%; transform: translateX(-50%); text-align: center; z-index: 10; }}
    .zodiac-icon-large svg {{ width: 80px; height: 80px; stroke: #C15F3C; stroke-width: 2; fill: none; margin-bottom: 20px; }}
    .zodiac-name {{ font-size: 72px; font-weight: 700; color: #C15F3C; letter-spacing: 16px; margin-bottom: 10px; }}
    .zodiac-year {{ font-size: 28px; font-weight: 400; color: #9A958A; letter-spacing: 8px; }}
    .main {{ position: absolute; top: 520px; left: 80px; right: 80px; z-index: 10; text-align: center; }}
    .keyword {{ display: inline-block; font-size: 36px; font-weight: 500; color: #3D3D3D; letter-spacing: 8px; padding: 12px 20px; border-top: 1px solid rgba(193, 95, 60, 0.4); border-bottom: 1px solid rgba(193, 95, 60, 0.4); margin-bottom: 50px; }}
    .main-title {{ font-size: 72px; font-weight: 600; color: #2D2D2D; letter-spacing: 6px; line-height: 1.4; margin-bottom: 40px; }}
    .accent {{ color: #C15F3C; font-weight: 500; }}
    .quote {{ font-size: 26px; font-weight: 400; color: #9A958A; letter-spacing: 3px; font-style: italic; }}
    .footer {{ position: absolute; bottom: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .footer-text {{ font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }}
    .gradient-band {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%); }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-bg">射手座</div>
    <div class="double-border"></div>
    <div class="stars-scatter" style="top: 160px; right: 100px;">
      <div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div><div class="star"></div>
    </div>
    <div class="header">
      <span class="tag">射手座 · 职场</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="zodiac-header">
      <div class="zodiac-icon-large">{SAGITTARIUS_SVG}</div>
      <div class="zodiac-name">射手座</div>
      <div class="zodiac-year">2026</div>
    </div>
    <div class="main">
      <div class="keyword">{keyword}</div>
      <h1 class="main-title">最<span class="accent">舒服</span>的<br/>职场关系</h1>
      <p class="quote">「 目标清楚，过程放手 」</p>
    </div>
    <div class="footer">
      <span class="footer-text">射手座职场指南</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

def generate_magazine_content(text, page_num, header_tag="射手座 · 职场"):
    lines = text.split('\n')
    first_line = lines[0] if lines else ""
    rest_lines = '<br/>'.join(lines[1:]) if len(lines) > 1 else ""

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .double-border {{ position: absolute; top: 50px; left: 50px; right: 50px; bottom: 50px; border: 1px solid rgba(193, 95, 60, 0.08); z-index: 2; }}
    .double-border::before {{ content: ''; position: absolute; top: 8px; left: 8px; right: 8px; bottom: 8px; border: 1px solid rgba(193, 95, 60, 0.04); }}
    .header {{ position: absolute; top: 70px; left: 80px; right: 80px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 100px; }}
    .think {{ font-size: 44px; color: #5A5A5A; letter-spacing: 3px; line-height: 1.7; margin-bottom: 60px; }}
    .keyword {{ color: #C15F3C; font-weight: 500; }}
    .truth-box {{ background: transparent; padding: 40px 50px; border-top: 1px solid rgba(193, 95, 60, 0.2); border-bottom: 1px solid rgba(193, 95, 60, 0.2); }}
    .truth {{ font-size: 38px; color: #3D3D3D; letter-spacing: 2px; line-height: 1.8; }}
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
      <span class="tag">{header_tag}</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="main">
      <p class="think"><span class="keyword">{first_line}</span></p>
      <div class="truth-box">
        <p class="truth">{rest_lines}</p>
      </div>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">{page_num:02d}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

def generate_magazine_ending(quote="不被限制的自由<br/>才是真正的效率"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .double-border {{ position: absolute; top: 80px; left: 80px; right: 80px; bottom: 80px; border: 1px solid rgba(193, 95, 60, 0.1); z-index: 2; }}
    .double-border::before {{ content: ''; position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px; border: 1px solid rgba(193, 95, 60, 0.05); }}
    .stars-scatter {{ position: absolute; width: 120px; height: 120px; z-index: 3; }}
    .star {{ position: absolute; width: 8px; height: 8px; background: #C15F3C; clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%); }}
    .star:nth-child(1) {{ top: 20px; left: 30px; opacity: 0.35; }}
    .star:nth-child(2) {{ top: 60px; left: 80px; opacity: 0.5; transform: scale(0.7); }}
    .star:nth-child(3) {{ top: 90px; left: 40px; opacity: 0.25; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 72px; height: 72px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 42px; font-weight: 600; color: #C15F3C; letter-spacing: 16px; margin-bottom: 50px; }}
    .quote {{ font-size: 46px; font-weight: 500; color: #3D3D3D; letter-spacing: 4px; line-height: 1.8; max-width: 700px; margin-bottom: 50px; }}
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
    <div class="stars-scatter" style="top: 120px; right: 120px;">
      <div class="star"></div><div class="star"></div><div class="star"></div>
    </div>
    <div class="stars-scatter" style="bottom: 200px; left: 100px;">
      <div class="star"></div><div class="star"></div><div class="star"></div>
    </div>
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote">{quote}</p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">06</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

# ========== 优雅留白风模板 ==========
def generate_elegant_cover(title, keyword="社交电量"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .corner-dot {{ position: absolute; width: 4px; height: 4px; background: rgba(193, 95, 60, 0.5); border-radius: 50%; }}
    .line-deco {{ position: absolute; height: 1px; background: linear-gradient(90deg, transparent, rgba(193, 95, 60, 0.3), transparent); }}
    .header {{ position: absolute; top: 70px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-header {{ position: absolute; top: 200px; left: 50%; transform: translateX(-50%); text-align: center; z-index: 10; }}
    .zodiac-icon svg {{ width: 64px; height: 64px; stroke: #C15F3C; stroke-width: 1.5; fill: none; margin-bottom: 24px; }}
    .zodiac-name {{ font-size: 48px; font-weight: 600; color: #C15F3C; letter-spacing: 12px; }}
    .zodiac-sub {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; margin-top: 12px; }}
    .main {{ position: absolute; top: 540px; left: 100px; right: 100px; z-index: 10; text-align: center; }}
    .keyword {{ display: inline-block; font-size: 34px; font-weight: 500; color: #C15F3C; letter-spacing: 8px; padding-bottom: 14px; border-bottom: 1px solid rgba(193, 95, 60, 0.4); margin-bottom: 50px; }}
    .main-title {{ font-size: 56px; font-weight: 600; color: #2D2D2D; letter-spacing: 3px; line-height: 1.6; margin-bottom: 40px; }}
    .accent {{ color: #C15F3C; font-weight: 500; }}
    .sub-title {{ font-size: 28px; font-weight: 400; color: #6A6A6A; letter-spacing: 2px; }}
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
      <span class="tag">射手座 · 社交</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="zodiac-header">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <div class="zodiac-name">射手座</div>
      <div class="zodiac-sub">社交电量表</div>
    </div>
    <div class="main">
      <div class="keyword">{keyword}</div>
      <h1 class="main-title">表面<span class="accent">热情</span><br/>电量却掉得<span class="accent">很快</span></h1>
      <p class="sub-title">射手座的社交真相</p>
    </div>
    <div class="footer">
      <span class="footer-text">射手座 · 2026</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

def generate_elegant_content(text, page_num, header_tag="射手座 · 社交"):
    lines = text.split('\n')
    first_line = lines[0] if lines else ""
    rest_lines = '<br/>'.join(lines[1:]) if len(lines) > 1 else ""

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .corner-dot {{ position: absolute; width: 4px; height: 4px; background: rgba(193, 95, 60, 0.5); border-radius: 50%; }}
    .header {{ position: absolute; top: 70px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 120px; }}
    .think {{ font-size: 42px; color: #5A5A5A; letter-spacing: 3px; line-height: 1.8; margin-bottom: 70px; }}
    .keyword {{ color: #C15F3C; font-weight: 500; }}
    .truth {{ font-size: 36px; color: #3D3D3D; letter-spacing: 2px; line-height: 1.9; padding-top: 50px; border-top: 1px solid rgba(193, 95, 60, 0.2); }}
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
      <span class="tag">{header_tag}</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="main">
      <p class="think"><span class="keyword">{first_line}</span></p>
      <p class="truth">{rest_lines}</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">{page_num:02d}</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

def generate_elegant_ending(quote="别硬撑<br/>硬撑只会把热情<br/>消耗成冷漠"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.05; pointer-events: none; z-index: 1; }}
    .corner-dot {{ position: absolute; width: 4px; height: 4px; background: rgba(193, 95, 60, 0.5); border-radius: 50%; }}
    .dot-deco {{ position: absolute; width: 6px; height: 6px; background: #C15F3C; border-radius: 50%; opacity: 0.3; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 64px; height: 64px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 38px; font-weight: 600; color: #C15F3C; letter-spacing: 12px; margin-bottom: 50px; }}
    .quote {{ font-size: 42px; font-weight: 500; color: #3D3D3D; letter-spacing: 3px; line-height: 1.9; max-width: 650px; margin-bottom: 50px; }}
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
    <div class="dot-deco" style="bottom: 350px; left: 200px;"></div>
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote">{quote}</p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">06</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>'''

# ========== 暖色编辑风模板 ==========
def generate_warm_cover(title, keyword="消费指南"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F8F2EB 30%, #F5EDE4 60%, #F2E8DD 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.06; pointer-events: none; z-index: 1; }}
    .header {{ position: absolute; top: 120px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 24px; font-weight: 400; color: #B1ADA1; letter-spacing: 4px; }}
    .zodiac-icon svg {{ width: 64px; height: 64px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 100px; }}
    .keyword-wrap {{ display: flex; align-items: center; justify-content: center; margin-bottom: 50px; }}
    .keyword-line {{ width: 48px; height: 2px; background: #C15F3C; }}
    .keyword {{ font-size: 28px; font-weight: 400; color: #C15F3C; letter-spacing: 8px; margin: 0 20px; }}
    .main-title {{ font-size: 84px; font-weight: 400; color: #2D2D2D; letter-spacing: 8px; line-height: 1.3; margin-bottom: 30px; }}
    .sub-title {{ font-size: 52px; font-weight: 400; color: #5A5A5A; letter-spacing: 4px; margin-bottom: 40px; }}
    .accent {{ color: #C15F3C; }}
    .tagline {{ font-size: 24px; font-weight: 400; color: #B1ADA1; letter-spacing: 2px; }}
    .bottom-line {{ position: absolute; bottom: 120px; left: 100px; right: 100px; height: 1px; background: #D9D6D0; z-index: 10; }}
    .page-num {{ position: absolute; bottom: 130px; right: 100px; font-size: 24px; font-weight: 400; color: #B1ADA1; letter-spacing: 4px; z-index: 10; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="tag">射手座 · 消费</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="main">
      <div class="keyword-wrap">
        <div class="keyword-line"></div>
        <span class="keyword">{keyword}</span>
        <div class="keyword-line"></div>
      </div>
      <h1 class="main-title">射手座的<br/><span class="accent">消费</span>指南</h1>
      <p class="sub-title">别让冲动散了预算</p>
      <p class="tagline">为"新鲜感"买单的正确姿势</p>
    </div>
    <div class="bottom-line"></div>
    <span class="page-num">01</span>
  </div>
</body>
</html>'''

def generate_warm_content(text, page_num, part_title="PART 0X", header_tag="射手座 · 消费"):
    lines = text.split('\n')
    content_html = '<br/>'.join(lines)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F8F2EB 30%, #F5EDE4 60%, #F2E8DD 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.06; pointer-events: none; z-index: 1; }}
    .header {{ position: absolute; top: 110px; left: 100px; right: 100px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }}
    .tag {{ font-size: 24px; font-weight: 400; color: #B1ADA1; letter-spacing: 4px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .part-num {{ position: absolute; top: 200px; left: 100px; font-size: 28px; font-weight: 400; color: #C15F3C; letter-spacing: 4px; z-index: 10; }}
    .part-title {{ position: absolute; top: 250px; left: 100px; font-size: 72px; font-weight: 400; color: #2D2D2D; letter-spacing: 4px; z-index: 10; }}
    .divider {{ position: absolute; top: 360px; left: 100px; width: 120px; height: 2px; background: #C15F3C; z-index: 10; }}
    .main {{ position: absolute; top: 420px; left: 100px; right: 100px; z-index: 10; }}
    .content {{ font-size: 34px; font-weight: 400; color: #5A5A5A; letter-spacing: 2px; line-height: 2; text-align: justify; }}
    .accent {{ color: #C15F3C; }}
    .page-num {{ position: absolute; bottom: 80px; right: 100px; font-size: 24px; font-weight: 400; color: #B1ADA1; letter-spacing: 4px; z-index: 10; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="tag">{header_tag}</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>
    <div class="part-num">{part_title}</div>
    <div class="part-title">消费心理</div>
    <div class="divider"></div>
    <div class="main">
      <p class="content">{content_html}</p>
    </div>
    <span class="page-num">{page_num:02d}</span>
  </div>
</body>
</html>'''

def generate_warm_ending(quote="体验和成长值得投入<br/>情绪补偿需要警惕"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF6F1; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(165deg, #FAF6F1 0%, #F8F2EB 30%, #F5EDE4 60%, #F2E8DD 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.06; pointer-events: none; z-index: 1; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 64px; height: 64px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 42px; font-weight: 400; color: #C15F3C; letter-spacing: 12px; margin-bottom: 50px; }}
    .quote {{ font-size: 42px; font-weight: 400; color: #3D3D3D; letter-spacing: 3px; line-height: 1.8; max-width: 700px; margin-bottom: 50px; }}
    .accent {{ color: #C15F3C; }}
    .tagline {{ font-size: 24px; color: #B1ADA1; letter-spacing: 4px; }}
    .page-num {{ position: absolute; bottom: 80px; right: 100px; font-size: 24px; font-weight: 400; color: #B1ADA1; letter-spacing: 4px; z-index: 10; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote">{quote}</p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <span class="page-num">06</span>
  </div>
</body>
</html>'''

# ========== 极简暖色风模板 ==========
def generate_minimal_warm_cover(title, keyword="边界感"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF8F5; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(180deg, #FAF8F5 0%, #F7F3EE 50%, #F4EFE8 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.04; pointer-events: none; }}
    .main {{ position: relative; z-index: 10; text-align: center; padding: 0 100px; }}
    .zodiac-label {{ font-size: 28px; font-weight: 400; color: #9A9590; letter-spacing: 16px; margin-bottom: 16px; }}
    .divider {{ width: 120px; height: 1.5px; background: #D4A990; margin: 0 auto 56px; }}
    .main-title {{ font-size: 72px; font-weight: 600; color: #2D2D2D; letter-spacing: 4px; line-height: 1.4; margin-bottom: 24px; }}
    .sub-title {{ font-size: 56px; font-weight: 500; color: #C8725A; letter-spacing: 4px; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="main">
      <p class="zodiac-label">✦ 射 手 座 ✦</p>
      <div class="divider"></div>
      <h1 class="main-title">射手座的<br/>{keyword}练习</h1>
      <p class="sub-title">学会提前说</p>
    </div>
  </div>
</body>
</html>'''

def generate_minimal_warm_content(text, page_num, section_title="信号X：主题"):
    lines = text.split('\n')
    content_html = '<br/>'.join(lines)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF8F5; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(180deg, #FAF8F5 0%, #F7F3EE 50%, #F4EFE8 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.04; pointer-events: none; }}
    .main {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; width: 100%; padding: 0 100px; }}
    .section-title {{ font-size: 42px; font-weight: 500; color: #C8725A; letter-spacing: 4px; margin-bottom: 56px; }}
    .content {{ font-size: 36px; font-weight: 400; color: #5A5A5A; letter-spacing: 2px; line-height: 2.2; text-align: justify; }}
    .accent {{ color: #C8725A; font-weight: 500; }}
    .zodiac-icon {{ position: absolute; bottom: 80px; left: 50%; transform: translateX(-50%); z-index: 10; }}
    .zodiac-icon svg {{ width: 32px; height: 32px; stroke: #9A9590; stroke-width: 1.5; fill: none; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="main">
      <h2 class="section-title">{section_title}</h2>
      <p class="content">{content_html}</p>
    </div>
    <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
  </div>
</body>
</html>'''

def generate_minimal_warm_ending(quote="提前说<br/>比事后消失更温柔"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF8F5; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(180deg, #FAF8F5 0%, #F7F3EE 50%, #F4EFE8 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.04; pointer-events: none; }}
    .main {{ position: relative; z-index: 10; text-align: center; }}
    .zodiac-icon {{ margin-bottom: 30px; }}
    .zodiac-icon svg {{ width: 48px; height: 48px; stroke: #C8725A; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ font-size: 36px; font-weight: 500; color: #C8725A; letter-spacing: 12px; margin-bottom: 50px; }}
    .quote {{ font-size: 42px; font-weight: 500; color: #2D2D2D; letter-spacing: 3px; line-height: 1.8; max-width: 650px; margin-bottom: 50px; }}
    .tagline {{ font-size: 22px; color: #9A9590; letter-spacing: 6px; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="main">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote">{quote}</p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
  </div>
</body>
</html>'''

# ========== 极简留白模板 ==========
def generate_whitespace_cover(title, keyword="轻计划"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF9F7; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.03; pointer-events: none; z-index: 1; }}
    .zodiac-badge {{ position: absolute; top: 100px; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; z-index: 10; }}
    .zodiac-glow {{ position: relative; display: flex; align-items: center; justify-content: center; }}
    .zodiac-glow::before {{ content: ''; position: absolute; width: 160px; height: 160px; background: radial-gradient(circle, rgba(217, 119, 87, 0.08) 0%, rgba(217, 119, 87, 0) 70%); border-radius: 50%; z-index: -1; }}
    .zodiac-icon svg {{ width: 80px; height: 80px; stroke: #D97757; stroke-width: 1.5; fill: none; }}
    .zodiac-cn {{ margin-top: 24px; font-size: 28px; font-weight: 500; color: #D97757; letter-spacing: 10px; text-indent: 10px; }}
    .zodiac-en {{ margin-top: 8px; font-size: 14px; font-weight: 400; color: #9A958E; letter-spacing: 6px; text-indent: 6px; }}
    .main {{ position: relative; z-index: 10; text-align: center; padding: 0 100px; margin-top: 60px; }}
    .main-title {{ font-size: 62px; font-weight: 500; color: #2D2A26; letter-spacing: 3px; line-height: 1.7; margin-bottom: 60px; }}
    .accent {{ color: #D97757; font-weight: 500; }}
    .sub-line {{ width: 50px; height: 1px; background: #D97757; margin: 0 auto 45px; }}
    .sub-title {{ font-size: 24px; font-weight: 300; color: #7A756E; letter-spacing: 5px; }}
    .footer {{ position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%); text-align: center; z-index: 10; }}
    .footer-text {{ font-size: 15px; font-weight: 400; color: #B5B0A8; letter-spacing: 6px; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-badge">
      <div class="zodiac-glow">
        <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      </div>
      <div class="zodiac-cn">射手座</div>
      <div class="zodiac-en">SAGITTARIUS</div>
    </div>
    <div class="main">
      <h1 class="main-title"><span class="accent">轻计划</span>学习法<br/>把学习变成<span class="accent">探索</span></h1>
      <div class="sub-line"></div>
      <p class="sub-title">先用7天试跑</p>
    </div>
    <div class="footer">
      <span class="footer-text">学习指南</span>
    </div>
  </div>
</body>
</html>'''

def generate_whitespace_content(text, page_num, section_title="不是怕孤独"):
    lines = text.split('\n')
    content_html = '<br/>'.join(lines)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF9F7; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.03; pointer-events: none; z-index: 1; }}
    .part-label {{ position: absolute; top: 100px; left: 50%; transform: translateX(-50%); font-size: 14px; font-weight: 400; color: #D97757; letter-spacing: 8px; z-index: 10; }}
    .main {{ position: relative; z-index: 10; text-align: center; padding: 0 100px; max-width: 900px; }}
    .section-title {{ font-size: 42px; font-weight: 500; color: #D97757; letter-spacing: 6px; margin-bottom: 60px; }}
    .content {{ font-size: 32px; font-weight: 400; color: #3D3832; line-height: 2.2; letter-spacing: 2px; text-align: center; }}
    .accent {{ color: #D97757; font-weight: 500; }}
    .footer {{ position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%); z-index: 10; }}
    .page-num {{ font-size: 14px; font-weight: 400; color: #B5B0A8; letter-spacing: 4px; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="part-label">· 0{page_num-1} ·</div>
    <div class="main">
      <h2 class="section-title">{section_title}</h2>
      <p class="content">{content_html}</p>
    </div>
    <div class="footer">
      <span class="page-num">{page_num:02d}</span>
    </div>
  </div>
</body>
</html>'''

def generate_whitespace_ending(quote="让兴趣变成路线<br/>学习就不再是负担"):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body {{ color-scheme: light only; background: #FAF9F7; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    .poster {{ width: 1080px; height: 1440px; position: relative; background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%); font-family: 'Noto Serif SC', serif; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .poster::before {{ content: ''; position: absolute; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity: 0.03; pointer-events: none; z-index: 1; }}
    .zodiac-badge {{ position: absolute; top: 120px; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; z-index: 10; }}
    .zodiac-icon svg {{ width: 52px; height: 52px; stroke: #D97757; stroke-width: 1.5; fill: none; }}
    .zodiac-name {{ margin-top: 20px; font-size: 18px; font-weight: 400; color: #D97757; letter-spacing: 10px; text-indent: 10px; }}
    .main {{ position: relative; z-index: 10; text-align: center; padding: 0 100px; margin-top: 60px; }}
    .section-title {{ font-size: 46px; font-weight: 500; color: #D97757; letter-spacing: 6px; margin-bottom: 60px; }}
    .content {{ font-size: 32px; font-weight: 400; color: #3D3832; line-height: 2.2; letter-spacing: 2px; text-align: center; }}
    .accent {{ color: #D97757; font-weight: 500; }}
    .end-mark {{ margin-top: 60px; font-size: 28px; color: #D97757; }}
    .footer {{ position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%); z-index: 10; }}
    .page-num {{ font-size: 14px; font-weight: 400; color: #B5B0A8; letter-spacing: 4px; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-badge">
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
      <div class="zodiac-name">SAGITTARIUS</div>
    </div>
    <div class="main">
      <h2 class="section-title">学习指南</h2>
      <p class="content">{quote}</p>
      <div class="end-mark">✦</div>
    </div>
    <div class="footer">
      <span class="page-num">06</span>
    </div>
  </div>
</body>
</html>'''

# ========== 主生成函数 ==========
async def generate_all_posters():
    """生成所有海报"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for poster in POSTER_DATA:
            print(f"\n{'='*50}")
            print(f"生成: {poster['title']} ({poster['template']})")

            folder = os.path.join(OUTPUT_BASE, poster['folder'])
            os.makedirs(folder, exist_ok=True)

            pages_html = []
            template = poster['template']
            content = poster['content']

            # 根据模板类型生成页面
            if template == "经典强调风":
                pages_html.append(generate_classic_cover(poster['title']))
                for i, text in enumerate(content):
                    pages_html.append(generate_classic_content(text, i+2))
                pages_html.append(generate_classic_ending())
            elif template == "简约边框风":
                pages_html.append(generate_border_cover(poster['title']))
                for i, text in enumerate(content):
                    pages_html.append(generate_border_content(text, i+2))
                pages_html.append(generate_border_ending())
            elif template == "杂志双线风":
                pages_html.append(generate_magazine_cover(poster['title']))
                for i, text in enumerate(content):
                    pages_html.append(generate_magazine_content(text, i+2))
                pages_html.append(generate_magazine_ending())
            elif template == "优雅留白风":
                pages_html.append(generate_elegant_cover(poster['title']))
                for i, text in enumerate(content):
                    pages_html.append(generate_elegant_content(text, i+2))
                pages_html.append(generate_elegant_ending())
            elif template == "暖色编辑风":
                pages_html.append(generate_warm_cover(poster['title']))
                for i, text in enumerate(content):
                    pages_html.append(generate_warm_content(text, i+2, f"PART 0{i+1}"))
                pages_html.append(generate_warm_ending())
            elif template == "极简暖色风":
                pages_html.append(generate_minimal_warm_cover(poster['title']))
                for i, text in enumerate(content):
                    pages_html.append(generate_minimal_warm_content(text, i+2, f"信号{i+1}：边界"))
                pages_html.append(generate_minimal_warm_ending())
            elif template == "极简留白":
                pages_html.append(generate_whitespace_cover(poster['title']))
                for i, text in enumerate(content):
                    pages_html.append(generate_whitespace_content(text, i+2, f"学习方法"))
                pages_html.append(generate_whitespace_ending())

            # 生成PNG
            page = await browser.new_page(viewport={'width': 1080, 'height': 1440})

            for i, html in enumerate(pages_html):
                html_path = os.path.join(folder, f"{i+1:02d}.html")
                png_path = os.path.join(folder, f"{i+1:02d}.png")

                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html)

                await page.goto(f'file://{html_path}')
                await page.wait_for_timeout(500)
                await page.screenshot(path=png_path, full_page=False)
                print(f"  ✓ {png_path}")

            await page.close()

        await browser.close()

    print(f"\n{'='*50}")
    print("✅ 所有7套海报生成完成！")

if __name__ == "__main__":
    asyncio.run(generate_all_posters())
