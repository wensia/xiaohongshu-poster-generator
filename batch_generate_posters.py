#!/usr/bin/env python3
"""
批量生成星座海报套图
1. 从飞书拉取指定记录
2. 解析正文内容
3. 生成HTML
4. 截图生成PNG
5. 上传到飞书
"""
import os
import re
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# 项目路径
PROJECT_ROOT = Path(__file__).parent
TEMPLATE_DIR = PROJECT_ROOT / "skills/zodiac-poster/assets/templates/personality-monologue"
OUTPUT_DIR = PROJECT_ROOT / "output"

# 飞书配置
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"

# 需要生成的记录标题
TITLES_TO_GENERATE = [
    "射手座喜欢的电影类型",
    "射手座最舍得花钱的地方",
    "射手座的存钱能力",
    "给射手座的人生建议",
    "射手座认定你之后的变化",
    "射手座的朋友圈人格",
]

# 配色
COLORS = {
    'accent': '#C4653A',
    'textPrimary': '#3D3835',
    'textSecondary': '#6B6461',
    'divider': '#D4CFC8',
    'bgStart': '#FAF6F1',
    'bgMid': '#F5EDE4',
    'bgEnd': '#F0E6D9',
}


def get_token():
    """获取飞书访问令牌"""
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    return resp.json()["tenant_access_token"]


def search_record(token, title):
    """根据标题搜索记录"""
    resp = requests.post(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "filter": {
                "conjunction": "and",
                "conditions": [
                    {"field_name": "标题", "operator": "is", "value": [title]}
                ]
            }
        }
    )
    data = resp.json()
    items = data.get("data", {}).get("items", [])
    return items[0] if items else None


def parse_content(content_data):
    """解析正文内容格式"""
    result = {
        'cover': {},
        'pages': [],
        'summary': {}
    }

    # 处理飞书返回的富文本格式
    if isinstance(content_data, list):
        # 从列表中提取文本
        content_text = ""
        for item in content_data:
            if isinstance(item, dict) and "text" in item:
                content_text += item["text"]
            elif isinstance(item, str):
                content_text += item
    else:
        content_text = str(content_data)

    current_section = None
    current_page = None
    lines = content_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检测section标记
        if line.startswith('【封面】'):
            current_section = 'cover'
            continue
        elif line.startswith('【第') and '页】' in line:
            current_section = 'page'
            # 提取页码和章节标题
            match = re.match(r'【第(\d+)页】(.+)', line)
            if match:
                page_num = match.group(1)
                section_title = match.group(2)
                current_page = {
                    'partNum': page_num.zfill(2),
                    'sectionTitle': section_title,
                    'content': [],
                    'quote': ''
                }
                result['pages'].append(current_page)
            continue
        elif line.startswith('【结尾】'):
            current_section = 'summary'
            # 提取结尾章节标题
            match = re.match(r'【结尾】(.+)', line)
            if match:
                result['summary']['sectionTitle'] = match.group(1)
                result['summary']['content'] = []
                result['summary']['endingLine1'] = ''
                result['summary']['endingLine2'] = ''
            continue

        # 解析封面字段
        if current_section == 'cover':
            if line.startswith('副标题:'):
                result['cover']['subtitle'] = line.replace('副标题:', '').strip()
            elif line.startswith('主标题第一行:'):
                result['cover']['titleLine1'] = line.replace('主标题第一行:', '').strip()
            elif line.startswith('主标题第二行:'):
                result['cover']['titleLine2'] = line.replace('主标题第二行:', '').strip()
            elif line.startswith('点缀语:'):
                result['cover']['tagline'] = line.replace('点缀语:', '').strip()

        # 解析内页正文
        elif current_section == 'page' and current_page:
            if line.startswith('"') and line.endswith('"'):
                current_page['quote'] = line.strip('"')
            else:
                current_page['content'].append(line)

        # 解析结尾页
        elif current_section == 'summary':
            if line.startswith('愿'):
                # 这是祝福语
                if not result['summary']['endingLine1']:
                    result['summary']['endingLine1'] = line
                else:
                    result['summary']['endingLine2'] = line
            else:
                result['summary']['content'].append(line)

    return result


def parse_highlight(text):
    """解析高亮词，返回结构化数据"""
    # 查找【高亮词】
    match = re.search(r'(.*)【([^】]+)】(.*)', text)
    if match:
        return {
            'before': match.group(1),
            'highlight': match.group(2),
            'after': match.group(3)
        }
    return text


def generate_cover_html(data, zodiac, topic):
    """生成封面HTML"""
    # 处理标题高亮
    title_line2 = data.get('titleLine2', '')
    highlight_match = re.search(r'【([^】]+)】', title_line2)
    title_line2_clean = re.sub(r'【([^】]+)】', r'\1', title_line2)

    # 处理点缀语
    tagline = data.get('tagline', '')
    tagline_parts = tagline.split(' ', 1) if ' ' in tagline else [tagline, '']

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <style>
    :root, html, body {{ color-scheme: light only; }}
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap');
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #FAF6F1; }}
    .poster {{
      width: 1080px;
      height: 1440px;
      background: linear-gradient(135deg, {COLORS['bgStart']} 0%, {COLORS['bgMid']} 50%, {COLORS['bgEnd']} 100%);
      position: relative;
      font-family: 'Noto Serif SC', serif;
    }}
    .header {{
      position: absolute;
      top: 100px;
      left: 100px;
      right: 100px;
      display: flex;
      align-items: center;
    }}
    .header .zodiac {{
      font-size: 32px;
      font-weight: 500;
      color: {COLORS['accent']};
      letter-spacing: 2px;
    }}
    .header .dot {{
      margin: 0 10px;
      font-size: 24px;
      color: {COLORS['divider']};
    }}
    .header .topic {{
      font-size: 24px;
      font-weight: 300;
      color: {COLORS['textSecondary']};
      letter-spacing: 3px;
      font-family: 'Noto Sans SC', sans-serif;
    }}
    .content {{
      position: absolute;
      top: 400px;
      left: 0;
      right: 0;
      text-align: center;
    }}
    .subtitle {{
      font-size: 32px;
      color: {COLORS['textSecondary']};
      letter-spacing: 6px;
      margin-bottom: 100px;
    }}
    .main-title {{
      font-size: 72px;
      font-weight: 600;
      color: {COLORS['textPrimary']};
      letter-spacing: 6px;
      line-height: 1.3;
    }}
    .main-title .accent {{
      color: {COLORS['accent']};
    }}
    .divider {{
      width: 100px;
      height: 4px;
      background: {COLORS['accent']};
      margin: 60px auto;
    }}
    .tagline {{
      font-size: 30px;
      color: {COLORS['textSecondary']};
      letter-spacing: 4px;
      line-height: 1.8;
    }}
    .tagline .accent {{
      color: {COLORS['accent']};
    }}
    .footer {{
      position: absolute;
      bottom: 50px;
      left: 100px;
      right: 100px;
    }}
    .footer-line {{
      height: 2px;
      background: {COLORS['divider']};
      margin-bottom: 20px;
    }}
    .page-num {{
      text-align: right;
      font-family: Georgia, serif;
      font-size: 28px;
      color: {COLORS['textSecondary']};
      letter-spacing: 4px;
    }}
    .zodiac-icon {{
      position: absolute;
      top: 74px;
      right: 100px;
      transform: rotate(-10deg);
    }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="zodiac">{zodiac}</span>
      <span class="dot">·</span>
      <span class="topic">{topic}</span>
    </div>
    <svg class="zodiac-icon" viewBox="0 0 100 100" width="56" height="56" fill="none" stroke="{COLORS['accent']}" stroke-width="1.5">
      <line x1="20" y1="80" x2="80" y2="20"/>
      <line x1="80" y1="20" x2="55" y2="20"/>
      <line x1="80" y1="20" x2="80" y2="45"/>
      <line x1="25" y1="45" x2="55" y2="75"/>
    </svg>
    <div class="content">
      <div class="subtitle">{data.get('subtitle', '')}</div>
      <div class="main-title">
        {data.get('titleLine1', '')}<br/>
        <span class="accent">{title_line2_clean}</span>
      </div>
      <div class="divider"></div>
      <div class="tagline">{tagline}</div>
    </div>
    <div class="footer">
      <div class="footer-line"></div>
      <div class="page-num">0 1</div>
    </div>
  </div>
</body>
</html>'''
    return html


def generate_page_html(page_data, zodiac, topic, page_num):
    """生成内页HTML"""
    # 处理正文内容
    content_html = ''
    for line in page_data.get('content', []):
        parsed = parse_highlight(line)
        if isinstance(parsed, dict):
            content_html += f'<p>{parsed["before"]}<span class="accent">{parsed["highlight"]}</span>{parsed["after"]}</p>\n'
        else:
            content_html += f'<p>{parsed}</p>\n'

    quote = page_data.get('quote', '')
    quote_html = f'<div class="quote"><div class="quote-bar"></div><p>"{quote}"</p></div>' if quote else ''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <style>
    :root, html, body {{ color-scheme: light only; }}
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap');
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #FAF6F1; }}
    .poster {{
      width: 1080px;
      height: 1440px;
      background: linear-gradient(135deg, {COLORS['bgStart']} 0%, {COLORS['bgMid']} 50%, {COLORS['bgEnd']} 100%);
      position: relative;
      font-family: 'Noto Serif SC', serif;
    }}
    .header {{
      position: absolute;
      top: 100px;
      left: 100px;
      display: flex;
      align-items: center;
    }}
    .header .zodiac {{ font-size: 32px; font-weight: 500; color: {COLORS['accent']}; letter-spacing: 2px; }}
    .header .dot {{ margin: 0 10px; font-size: 24px; color: {COLORS['divider']}; }}
    .header .topic {{ font-size: 24px; font-weight: 300; color: {COLORS['textSecondary']}; letter-spacing: 3px; font-family: 'Noto Sans SC', sans-serif; }}
    .zodiac-icon {{ position: absolute; top: 74px; right: 100px; transform: rotate(-10deg); }}
    .part-label {{
      position: absolute;
      top: 200px;
      left: 100px;
      font-family: Georgia, serif;
      font-size: 26px;
      color: {COLORS['accent']};
      letter-spacing: 8px;
    }}
    .section-title {{
      position: absolute;
      top: 280px;
      left: 100px;
      font-size: 56px;
      font-weight: 600;
      color: {COLORS['textPrimary']};
      letter-spacing: 6px;
    }}
    .section-divider {{
      position: absolute;
      top: 370px;
      left: 100px;
      width: 100px;
      height: 4px;
      background: {COLORS['accent']};
    }}
    .content {{
      position: absolute;
      top: 460px;
      left: 100px;
      right: 100px;
    }}
    .content p {{
      font-size: 32px;
      color: {COLORS['textPrimary']};
      letter-spacing: 2px;
      line-height: 1.9;
    }}
    .content .accent {{ color: {COLORS['accent']}; }}
    .quote {{
      position: absolute;
      top: 1020px;
      left: 100px;
      display: flex;
      align-items: flex-start;
    }}
    .quote-bar {{
      width: 4px;
      height: 60px;
      background: {COLORS['accent']};
      margin-right: 20px;
    }}
    .quote p {{
      font-size: 28px;
      font-style: italic;
      color: {COLORS['textSecondary']};
      letter-spacing: 2px;
    }}
    .footer {{
      position: absolute;
      bottom: 50px;
      left: 100px;
      right: 100px;
    }}
    .footer-line {{ height: 2px; background: {COLORS['divider']}; margin-bottom: 20px; }}
    .page-num {{ text-align: right; font-family: Georgia, serif; font-size: 28px; color: {COLORS['textSecondary']}; letter-spacing: 4px; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="zodiac">{zodiac}</span>
      <span class="dot">·</span>
      <span class="topic">{topic}</span>
    </div>
    <svg class="zodiac-icon" viewBox="0 0 100 100" width="56" height="56" fill="none" stroke="{COLORS['accent']}" stroke-width="1.5">
      <line x1="20" y1="80" x2="80" y2="20"/>
      <line x1="80" y1="20" x2="55" y2="20"/>
      <line x1="80" y1="20" x2="80" y2="45"/>
      <line x1="25" y1="45" x2="55" y2="75"/>
    </svg>
    <div class="part-label">PART {page_data.get('partNum', '01')}</div>
    <div class="section-title">{page_data.get('sectionTitle', '')}</div>
    <div class="section-divider"></div>
    <div class="content">
      {content_html}
    </div>
    {quote_html}
    <div class="footer">
      <div class="footer-line"></div>
      <div class="page-num">0 {page_num}</div>
    </div>
  </div>
</body>
</html>'''
    return html


def generate_summary_html(summary_data, zodiac, topic, page_num):
    """生成结尾页HTML"""
    # 处理内容
    content_html = ''
    for line in summary_data.get('content', []):
        parsed = parse_highlight(line)
        if isinstance(parsed, dict):
            content_html += f'<p>{parsed["before"]}<span class="accent">{parsed["highlight"]}</span>{parsed["after"]}</p>\n'
        else:
            content_html += f'<p>{parsed}</p>\n'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <style>
    :root, html, body {{ color-scheme: light only; }}
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap');
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #FAF6F1; }}
    .poster {{
      width: 1080px;
      height: 1440px;
      background: linear-gradient(135deg, {COLORS['bgStart']} 0%, {COLORS['bgMid']} 50%, {COLORS['bgEnd']} 100%);
      position: relative;
      font-family: 'Noto Serif SC', serif;
    }}
    .header {{
      position: absolute;
      top: 100px;
      left: 100px;
      display: flex;
      align-items: center;
    }}
    .header .zodiac {{ font-size: 32px; font-weight: 500; color: {COLORS['accent']}; letter-spacing: 2px; }}
    .header .dot {{ margin: 0 10px; font-size: 24px; color: {COLORS['divider']}; }}
    .header .topic {{ font-size: 24px; font-weight: 300; color: {COLORS['textSecondary']}; letter-spacing: 3px; font-family: 'Noto Sans SC', sans-serif; }}
    .zodiac-icon {{ position: absolute; top: 74px; right: 100px; transform: rotate(-10deg); }}
    .centered-content {{
      position: absolute;
      top: 200px;
      left: 0;
      right: 0;
      text-align: center;
    }}
    .part-label {{
      font-family: Georgia, serif;
      font-size: 26px;
      color: {COLORS['accent']};
      letter-spacing: 8px;
    }}
    .section-title {{
      font-size: 64px;
      font-weight: 600;
      color: {COLORS['textPrimary']};
      letter-spacing: 6px;
      margin-top: 60px;
    }}
    .section-divider {{
      width: 100px;
      height: 4px;
      background: {COLORS['accent']};
      margin: 40px auto;
    }}
    .content {{
      margin-top: 140px;
    }}
    .content p {{
      font-size: 32px;
      color: {COLORS['textPrimary']};
      letter-spacing: 2px;
      line-height: 1.9;
    }}
    .content .accent {{ color: {COLORS['accent']}; }}
    .divider-decoration {{
      margin: 60px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }}
    .divider-decoration .line {{
      width: 50px;
      height: 1px;
      background: {COLORS['divider']};
    }}
    .divider-decoration .diamond {{
      font-size: 16px;
      color: {COLORS['accent']};
    }}
    .ending {{
      font-size: 28px;
      font-style: italic;
      color: {COLORS['textSecondary']};
      letter-spacing: 3px;
      line-height: 2;
    }}
    .end-mark {{
      margin-top: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 20px;
    }}
    .end-mark .line {{
      width: 60px;
      height: 2px;
      background: {COLORS['divider']};
    }}
    .end-mark .text {{
      font-family: Georgia, serif;
      font-size: 24px;
      color: {COLORS['accent']};
      letter-spacing: 6px;
    }}
    .footer {{
      position: absolute;
      bottom: 50px;
      left: 100px;
      right: 100px;
    }}
    .footer-line {{ height: 2px; background: {COLORS['divider']}; margin-bottom: 20px; }}
    .page-num {{ text-align: right; font-family: Georgia, serif; font-size: 28px; color: {COLORS['textSecondary']}; letter-spacing: 4px; }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="zodiac">{zodiac}</span>
      <span class="dot">·</span>
      <span class="topic">{topic}</span>
    </div>
    <svg class="zodiac-icon" viewBox="0 0 100 100" width="56" height="56" fill="none" stroke="{COLORS['accent']}" stroke-width="1.5">
      <line x1="20" y1="80" x2="80" y2="20"/>
      <line x1="80" y1="20" x2="55" y2="20"/>
      <line x1="80" y1="20" x2="80" y2="45"/>
      <line x1="25" y1="45" x2="55" y2="75"/>
    </svg>
    <div class="centered-content">
      <div class="part-label">EXTRA</div>
      <div class="section-title">{summary_data.get('sectionTitle', '写给射手')}</div>
      <div class="section-divider"></div>
      <div class="content">
        {content_html}
      </div>
      <div class="divider-decoration">
        <div class="line"></div>
        <span class="diamond">◆</span>
        <div class="line"></div>
      </div>
      <div class="ending">
        <p>{summary_data.get('endingLine1', '')}</p>
        <p>{summary_data.get('endingLine2', '')}</p>
      </div>
      <div class="end-mark">
        <div class="line"></div>
        <span class="text">END</span>
        <div class="line"></div>
      </div>
    </div>
    <div class="footer">
      <div class="footer-line"></div>
      <div class="page-num">0 {page_num}</div>
    </div>
  </div>
</body>
</html>'''
    return html


def upload_images_to_feishu(token, record_id, image_dir):
    """上传图片到飞书并更新记录"""
    file_tokens = []

    # 获取所有PNG文件
    png_files = sorted(Path(image_dir).glob("*.png"))

    print(f"   上传 {len(png_files)} 张图片...")

    for img_path in png_files:
        # 上传文件
        with open(img_path, 'rb') as f:
            resp = requests.post(
                "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": (img_path.name, f, "image/png")},
                data={
                    "file_name": img_path.name,
                    "parent_type": "bitable_file",
                    "parent_node": APP_TOKEN,
                    "size": str(img_path.stat().st_size)
                }
            )

        result = resp.json()
        if result.get("code") == 0:
            file_token = result.get("data", {}).get("file_token")
            if file_token:
                file_tokens.append({"file_token": file_token})
                print(f"     ✓ {img_path.name}")
        else:
            print(f"     ✗ {img_path.name}: {result}")

    # 更新记录
    if file_tokens:
        resp = requests.put(
            f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "fields": {
                    "已生成": True,
                    "生成图片": file_tokens
                }
            }
        )
        result = resp.json()
        if result.get("code") == 0:
            print(f"   ✓ 记录更新成功，附件数: {len(file_tokens)}")
            return True
        else:
            print(f"   ✗ 记录更新失败: {result}")
            return False

    return False


def main():
    print("=" * 60)
    print("批量生成星座海报套图")
    print("=" * 60)

    # 1. 获取token
    print("\n1. 获取飞书访问令牌...")
    token = get_token()
    print("   ✓ 获取成功")

    # 2. 创建输出目录
    today = datetime.now()
    date_dir = OUTPUT_DIR / today.strftime("%Y/%m/%d")

    # 3. 处理每个标题
    print(f"\n2. 处理 {len(TITLES_TO_GENERATE)} 个记录...")

    for title in TITLES_TO_GENERATE:
        print(f"\n--- 处理: {title} ---")

        # 搜索记录
        record = search_record(token, title)
        if not record:
            print(f"   ✗ 未找到记录")
            continue

        record_id = record.get("record_id")
        fields = record.get("fields", {})
        content_text = fields.get("正文内容", "")

        if not content_text:
            print(f"   ✗ 正文内容为空")
            continue

        # 解析内容
        print(f"   解析正文内容...")
        parsed = parse_content(content_text)

        if not parsed['cover'] or not parsed['pages']:
            print(f"   ✗ 内容解析失败")
            continue

        # 创建输出目录
        safe_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)
        output_path = date_dir / f"射手座_{safe_title}"
        output_path.mkdir(parents=True, exist_ok=True)
        html_path = output_path / "html"
        html_path.mkdir(exist_ok=True)

        zodiac = "射手座"
        topic = parsed['cover'].get('subtitle', '性格独白')

        # 生成HTML文件
        print(f"   生成HTML文件...")

        # 封面
        cover_html = generate_cover_html(parsed['cover'], zodiac, topic)
        (html_path / "01_cover.html").write_text(cover_html, encoding='utf-8')

        # 内页
        for i, page in enumerate(parsed['pages']):
            page_html = generate_page_html(page, zodiac, topic, i + 2)
            (html_path / f"{str(i+2).zfill(2)}_page.html").write_text(page_html, encoding='utf-8')

        # 结尾页
        summary_html = generate_summary_html(parsed['summary'], zodiac, topic, len(parsed['pages']) + 2)
        (html_path / f"{str(len(parsed['pages'])+2).zfill(2)}_summary.html").write_text(summary_html, encoding='utf-8')

        print(f"   ✓ 生成 {len(parsed['pages']) + 2} 个HTML文件")

        # 截图
        print(f"   截图生成PNG...")
        import subprocess
        screenshot_script = PROJECT_ROOT / "skills/_shared/scripts/poster_screenshot.py"
        result = subprocess.run(
            ["python3", str(screenshot_script), "--batch", str(html_path), str(output_path)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"   ✗ 截图失败: {result.stderr}")
            continue

        print(f"   ✓ 截图完成")

        # 上传到飞书
        print(f"   上传到飞书...")
        success = upload_images_to_feishu(token, record_id, output_path)

        if success:
            print(f"   ✓ 完成: {title}")
        else:
            print(f"   ✗ 上传失败: {title}")

    print("\n" + "=" * 60)
    print("批量生成完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
