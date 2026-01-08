#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态编辑风海报生成脚本
为3条射手座记录生成套图
"""

import os
import random
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
import requests

# 配置
BASE_DIR = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成")
OUTPUT_DIR = BASE_DIR / "output"

# 飞书配置
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

# 射手座 SVG
SAGITTARIUS_SVG = """<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'>
  <line x1='20' y1='80' x2='80' y2='20' stroke='#C15F3C' stroke-width='2' stroke-linecap='round'/>
  <line x1='80' y1='20' x2='55' y2='20' stroke='#C15F3C' stroke-width='2' stroke-linecap='round'/>
  <line x1='80' y1='20' x2='80' y2='45' stroke='#C15F3C' stroke-width='2' stroke-linecap='round'/>
  <line x1='25' y1='45' x2='55' y2='75' stroke='#C15F3C' stroke-width='2' stroke-linecap='round'/>
</svg>"""

# 3条记录数据
RECORDS = [
    {
        "record_id": "recv7gpNOuwEQz",
        "title": "射手座的消费指南",
        "subtitle": "花钱不是罪，冲动才是",
        "paragraphs": [
            "射手座最容易为「新鲜感」和「好玩的体验」买单，这本来是优势——人生因此更丰富。但冲动一来，预算就散了。",
            "把消费分成三类：体验（旅行/演出）、成长（课程/工具）、情绪补偿（缓解压力的买买买）。前两类可以花，第三类要停一下。",
            "给自己一个「24小时冷静期」。想买的大件先放购物车，第二天再看：还想要就买，不想了就当省一笔。",
            "再定一个「玩乐预算区间」：每月固定一笔，花完就停。你不是在限制自由，而是在保护长期的自由。"
        ],
        "style": "经典强调"
    },
    {
        "record_id": "recv7gpO7IE6y4",
        "title": "射手座的边界感练习",
        "subtitle": "不喜欢解释，但需要表达",
        "paragraphs": [
            "射手座常被说「忽冷忽热」，其实是你在无声地拉开距离。问题不在冷，而在你太晚才开口。",
            "边界最好在「还没累」的时候说：比如「我今晚想自己待会儿」「这件事我想慢一点」。提前说，比事后消失更温柔。",
            "给自己三句固定句式：「我需要一点空间，但我没离开」；「我想先把自己的事做完」；「这周先别安排太满」。",
            "你守住边界的那一刻，关系才不会靠消耗维持。射手座的真诚，是让彼此都舒服。"
        ],
        "style": "简约边框"
    },
    {
        "record_id": "recv7gpOqwZMfb",
        "title": "射手座的轻计划学习法",
        "subtitle": "不用逼自己，也能持续",
        "paragraphs": [
            "射手座最怕死板学习，但你很擅长把学习变成探索。关键不是逼自己坐住，而是让兴趣变成路线。",
            "先用7天试跑：只学一个小主题，比如「剪辑里的转场」。每天30分钟，7天后再决定要不要继续。",
            "把学习和输出绑定：做一页笔记、一段分享、一条小作品。射手座喜欢被看见，输出就是你的动力。",
            "每月做一次复盘：哪些内容让你兴奋，哪些让你拖延。删掉无趣的，保留能点燃你的。学习会变成你的自由。"
        ],
        "style": "杂志双线"
    }
]

# 通用基础样式
BASE_CSS = """
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

.header {
  position: absolute;
  top: 70px;
  left: 80px;
  right: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.tag {
  font-size: 22px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 6px;
}

.zodiac-icon {
  width: 48px;
  height: 48px;
}

.footer {
  position: absolute;
  bottom: 70px;
  left: 80px;
  right: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.footer-text {
  font-size: 20px;
  color: #B1ADA1;
  letter-spacing: 4px;
}

.page-num {
  font-size: 24px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 4px;
}

.accent {
  color: #C15F3C;
  font-weight: 500;
}

.highlight {
  position: relative;
  display: inline;
}
.highlight::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 0;
  right: 0;
  height: 10px;
  background: rgba(193, 95, 60, 0.2);
  z-index: -1;
}

.gradient-band {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
}
"""

# 风格包1：经典强调
STYLE_CLASSIC_CSS = """
.keyword {
  display: inline-block;
  width: fit-content;
  background: linear-gradient(135deg, #C15F3C 0%, #D4765A 100%);
  color: #fff;
  font-size: 32px;
  font-weight: 500;
  letter-spacing: 8px;
  padding: 12px 28px;
  border-radius: 2px;
  margin-bottom: 50px;
}

.year-bg {
  position: absolute;
  top: 180px;
  left: -60px;
  font-size: 320px;
  font-weight: 700;
  color: rgba(193, 95, 60, 0.06);
  letter-spacing: -20px;
  z-index: 0;
}

.circle-deco {
  position: absolute;
  width: 180px;
  height: 180px;
  border: 2px solid rgba(193, 95, 60, 0.15);
  border-radius: 50%;
}
.circle-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: rgba(193, 95, 60, 0.08);
  border-radius: 50%;
}

.main {
  position: absolute;
  top: 50%;
  left: 80px;
  right: 80px;
  transform: translateY(-50%);
  z-index: 10;
  text-align: center;
}

.main-title {
  font-size: 68px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 4px;
  line-height: 1.4;
  margin-bottom: 40px;
}

.sub-title {
  font-size: 36px;
  font-weight: 400;
  color: #5A5A5A;
  letter-spacing: 4px;
  margin-bottom: 50px;
}

.quote {
  font-size: 26px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
  font-style: italic;
}

.content {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  line-height: 2;
  letter-spacing: 2px;
  text-align: justify;
}
"""

# 风格包2：简约边框
STYLE_BORDER_CSS = """
.keyword {
  display: inline-block;
  width: fit-content;
  font-size: 32px;
  font-weight: 500;
  color: #C15F3C;
  letter-spacing: 6px;
  padding: 10px 24px;
  border: 2px solid #C15F3C;
  border-radius: 2px;
  margin-bottom: 50px;
}

.corner-bracket {
  position: absolute;
  width: 60px;
  height: 60px;
  border: 2px solid rgba(193, 95, 60, 0.2);
}
.corner-bracket.top-left {
  top: 140px;
  left: 70px;
  border-right: none;
  border-bottom: none;
}
.corner-bracket.bottom-right {
  bottom: 140px;
  right: 70px;
  border-left: none;
  border-top: none;
}

.side-lines {
  position: absolute;
  left: 60px;
  top: 300px;
}
.side-line {
  width: 3px;
  background: #C15F3C;
  margin-bottom: 12px;
}
.side-line:nth-child(1) { height: 120px; }
.side-line:nth-child(2) { height: 80px; opacity: 0.6; }
.side-line:nth-child(3) { height: 50px; opacity: 0.3; }

.main {
  position: absolute;
  top: 50%;
  left: 80px;
  right: 80px;
  transform: translateY(-50%);
  z-index: 10;
  text-align: center;
}

.main-title {
  font-size: 64px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 4px;
  line-height: 1.4;
  margin-bottom: 40px;
}

.sub-title {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  letter-spacing: 4px;
  margin-bottom: 50px;
}

.quote {
  font-size: 26px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
  font-style: italic;
}

.content {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  line-height: 2;
  letter-spacing: 2px;
  text-align: justify;
}
"""

# 风格包3：杂志双线
STYLE_MAGAZINE_CSS = """
.keyword {
  display: inline-block;
  width: fit-content;
  font-size: 30px;
  font-weight: 500;
  color: #3D3D3D;
  letter-spacing: 6px;
  padding: 10px 0;
  border-top: 1px solid rgba(193, 95, 60, 0.4);
  border-bottom: 1px solid rgba(193, 95, 60, 0.4);
  margin-bottom: 50px;
}

.double-border {
  position: absolute;
  top: 130px;
  left: 70px;
  right: 70px;
  bottom: 130px;
  border: 1px solid rgba(193, 95, 60, 0.1);
}
.double-border::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border: 1px solid rgba(193, 95, 60, 0.05);
}

.stars-scatter {
  position: absolute;
  width: 180px;
  height: 180px;
}
.star {
  position: absolute;
  width: 10px;
  height: 10px;
  background: #C15F3C;
  clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}

.main {
  position: absolute;
  top: 50%;
  left: 80px;
  right: 80px;
  transform: translateY(-50%);
  z-index: 10;
  text-align: center;
}

.main-title {
  font-size: 68px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 4px;
  line-height: 1.4;
  margin-bottom: 40px;
}

.sub-title {
  font-size: 36px;
  font-weight: 400;
  color: #5A5A5A;
  letter-spacing: 4px;
  margin-bottom: 50px;
}

.quote {
  font-size: 26px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
  font-style: italic;
}

.content {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  line-height: 2;
  letter-spacing: 2px;
  text-align: justify;
}
"""

def get_style_css(style_name):
    """获取风格包CSS"""
    if style_name == "经典强调":
        return STYLE_CLASSIC_CSS
    elif style_name == "简约边框":
        return STYLE_BORDER_CSS
    elif style_name == "杂志双线":
        return STYLE_MAGAZINE_CSS
    else:
        return STYLE_CLASSIC_CSS

def add_accent_words(text):
    """为正文添加强调词"""
    accent_words = ["射手座", "自由", "冲动", "边界", "学习", "兴趣", "预算", "体验", "输出", "复盘"]
    result = text
    count = 0
    for word in accent_words:
        if word in result and count < 2:
            result = result.replace(word, f'<span class="accent">{word}</span>', 1)
            count += 1
    return result

def generate_cover_html(record, style_name):
    """生成封面HTML"""
    style_css = get_style_css(style_name)

    # 根据风格选择装饰
    if style_name == "经典强调":
        decorations = '''
    <div class="year-bg">2026</div>
    <div class="circle-deco" style="top: 200px; right: 100px;">
      <div class="circle-inner"></div>
    </div>
'''
    elif style_name == "简约边框":
        decorations = '''
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket bottom-right"></div>
'''
    elif style_name == "杂志双线":
        decorations = '''
    <div class="double-border"></div>
    <div class="stars-scatter" style="top: 160px; right: 100px;">
      <div class="star" style="top: 20px; left: 30px; opacity: 0.35;"></div>
      <div class="star" style="top: 60px; left: 130px; opacity: 0.5; transform: scale(0.7);"></div>
      <div class="star" style="top: 100px; left: 50px; opacity: 0.25; transform: scale(1.1);"></div>
      <div class="star" style="top: 30px; left: 150px; opacity: 0.4; transform: scale(0.5);"></div>
      <div class="star" style="top: 140px; left: 100px; opacity: 0.3;"></div>
    </div>
'''
    else:
        decorations = ''

    html = f'''<!-- [STYLE LOCK: {style_name}] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_CSS}
    {style_css}
  </style>
</head>
<body>
  <div class="poster">
{decorations}
    <div class="header">
      <span class="tag">射手座 · SAGITTARIUS</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>

    <div class="main">
      <div class="keyword">射手座</div>
      <h1 class="main-title">{record["title"]}</h1>
      <p class="sub-title">{record["subtitle"]}</p>
    </div>

    <div class="footer">
      <span class="footer-text">星座指南</span>
      <span class="page-num">01</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
'''
    return html

def generate_page_html(record, paragraph, page_num, style_name, is_last=False):
    """生成内页HTML"""
    style_css = get_style_css(style_name)

    # 根据风格选择装饰
    if style_name == "经典强调":
        decorations = f'''
    <div class="circle-deco" style="top: 180px; right: 80px; width: 120px; height: 120px;">
      <div class="circle-inner" style="width: 60px; height: 60px;"></div>
    </div>
'''
    elif style_name == "简约边框":
        decorations = '''
    <div class="side-lines">
      <div class="side-line"></div>
      <div class="side-line"></div>
      <div class="side-line"></div>
    </div>
'''
    elif style_name == "杂志双线":
        decorations = '''
    <div class="stars-scatter" style="top: 200px; left: 80px; width: 150px; height: 150px;">
      <div class="star" style="top: 20px; left: 35px; opacity: 0.3;"></div>
      <div class="star" style="top: 70px; left: 110px; opacity: 0.5; transform: scale(0.7);"></div>
      <div class="star" style="top: 100px; left: 55px; opacity: 0.2; transform: scale(1.1);"></div>
    </div>
'''
    else:
        decorations = ''

    # 添加强调词
    content_with_accent = add_accent_words(paragraph)

    # 结尾页特殊处理
    if is_last:
        ending_section = f'''
      <div style="margin-top: 80px; text-align: center;">
        <div style="width: 80px; height: 80px; margin: 0 auto 30px;">
          {SAGITTARIUS_SVG}
        </div>
        <p style="font-size: 24px; color: #9A958A; letter-spacing: 6px;">SAGITTARIUS</p>
      </div>
'''
    else:
        ending_section = ''

    html = f'''<!-- [STYLE LOCK: {style_name}] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {page_num:02d}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    {BASE_CSS}
    {style_css}

    .main {{
      top: 50%;
      transform: translateY(-50%);
      text-align: center;
    }}

    .content {{
      text-align: center;
      line-height: 2.2;
    }}
  </style>
</head>
<body>
  <div class="poster">
{decorations}
    <div class="header">
      <span class="tag">射手座 · SAGITTARIUS</span>
      <div class="zodiac-icon">{SAGITTARIUS_SVG}</div>
    </div>

    <div class="main">
      <p class="content">{content_with_accent}</p>
{ending_section}
    </div>

    <div class="footer">
      <span class="footer-text">星座指南</span>
      <span class="page-num">{page_num:02d}</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
'''
    return html

def html_to_png(html_content, output_path):
    """将HTML转换为PNG"""
    html_path = output_path.replace('.png', '.html')

    # 保存HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 使用Playwright截图
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1080, "height": 1440},
            device_scale_factor=2  # 2x 导出，实际像素 2160x2880
        )
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)  # 等待字体加载
        page.locator(".poster").screenshot(path=output_path)
        browser.close()

    print(f"  生成: {output_path}")
    return output_path

def get_feishu_token():
    """获取飞书access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    })
    return resp.json()["tenant_access_token"]

def upload_image_to_feishu(image_path, token):
    """上传图片到飞书"""
    filename = os.path.basename(image_path)
    file_size = os.path.getsize(image_path)

    upload_url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"

    with open(image_path, "rb") as f:
        files = {"file": (filename, f, "image/png")}
        data = {
            "file_name": filename,
            "parent_type": "bitable_file",
            "parent_node": APP_TOKEN,
            "size": str(file_size)
        }
        resp = requests.post(
            upload_url,
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data
        )

    result = resp.json()
    if "data" in result and "file_token" in result["data"]:
        return result["data"]["file_token"]
    else:
        print(f"  上传失败: {result}")
        return None

def update_feishu_record(record_id, file_tokens, token):
    """更新飞书记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"

    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "fields": {
                "生成图片": [{"file_token": ft} for ft in file_tokens],
                "已生成": True
            }
        }
    )

    return resp.json()

def main():
    """主函数"""
    print("=" * 50)
    print("动态编辑风海报生成")
    print("=" * 50)

    for record in RECORDS:
        print(f"\n处理记录: {record['title']}")
        print(f"  风格: {record['style']}")

        # 创建输出目录
        output_dir = OUTPUT_DIR / record["title"]
        output_dir.mkdir(parents=True, exist_ok=True)

        generated_images = []

        # 生成封面
        print("  生成封面...")
        cover_html = generate_cover_html(record, record["style"])
        cover_path = str(output_dir / "01_cover.png")
        html_to_png(cover_html, cover_path)
        generated_images.append(cover_path)

        # 生成内页（每段一张）
        for i, paragraph in enumerate(record["paragraphs"]):
            page_num = i + 2
            is_last = (i == len(record["paragraphs"]) - 1)
            print(f"  生成内页 {page_num:02d}...")

            page_html = generate_page_html(record, paragraph, page_num, record["style"], is_last)
            page_path = str(output_dir / f"{page_num:02d}_page.png")
            html_to_png(page_html, page_path)
            generated_images.append(page_path)

        print(f"  共生成 {len(generated_images)} 张图片")

        # 上传到飞书
        print("  上传到飞书...")
        token = get_feishu_token()
        file_tokens = []

        for img_path in generated_images:
            ft = upload_image_to_feishu(img_path, token)
            if ft:
                file_tokens.append(ft)
                print(f"    上传成功: {os.path.basename(img_path)}")

        # 更新记录
        if file_tokens:
            result = update_feishu_record(record["record_id"], file_tokens, token)
            if "data" in result:
                print(f"  记录更新成功!")
            else:
                print(f"  记录更新失败: {result}")

    print("\n" + "=" * 50)
    print("全部完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()
