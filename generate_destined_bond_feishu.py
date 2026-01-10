#!/usr/bin/env python3
"""
命定之约风 SVG 模板生成器
从飞书拉取记录，生成套图并回传
"""
import asyncio
import requests
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# 飞书配置
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

# 命定之约风模板路径
TEMPLATE_PATH = Path(__file__).parent / "skills/zodiac-poster/assets/templates/destined-bond/TEMPLATE.md"

def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json()["tenant_access_token"]

def fetch_record_by_title(token: str, title: str) -> dict:
    """根据标题搜索飞书记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    data = {
        "filter": {
            "conjunction": "and",
            "conditions": [{"field_name": "标题", "operator": "contains", "value": [title]}]
        }
    }

    resp = requests.post(url, headers=headers, json=data)
    items = resp.json().get("data", {}).get("items", [])

    if items:
        return items[0]
    return None

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

def render_content_lines(lines):
    """生成正文内容SVG（字间距4px）"""
    svg_lines = []
    y = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "|" in line:
            parts = line.split("|")
            if len(parts) == 2:
                before, highlight = parts
                svg_lines.append(
                    f'<text y="{y}" font-family="Noto Serif SC, serif" font-size="32" letter-spacing="4">'
                    f'<tspan fill="#4A3F35">{before}</tspan>'
                    f'<tspan fill="#B86B4A">{highlight}</tspan>'
                    f'</text>'
                )
            elif len(parts) == 3:
                before, highlight, after = parts
                svg_lines.append(
                    f'<text y="{y}" font-family="Noto Serif SC, serif" font-size="32" letter-spacing="4">'
                    f'<tspan fill="#4A3F35">{before}</tspan>'
                    f'<tspan fill="#B86B4A">{highlight}</tspan>'
                    f'<tspan fill="#4A3F35">{after}</tspan>'
                    f'</text>'
                )
        else:
            svg_lines.append(
                f'<text y="{y}" font-family="Noto Serif SC, serif" font-size="32" fill="#4A3F35" letter-spacing="4">{line}</text>'
            )
        y += 61
    return "\n    ".join(svg_lines)

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
    """包装SVG为HTML"""
    return f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500&family=Noto+Serif+SC:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
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

def parse_feishu_record(record):
    """解析飞书记录"""
    fields = record["fields"]

    # 获取文本内容
    def get_text(field_value):
        if isinstance(field_value, list) and len(field_value) > 0:
            return field_value[0].get("text", "")
        return str(field_value) if field_value else ""

    title = get_text(fields.get("标题", ""))
    subtitle = get_text(fields.get("副标题", ""))
    content = get_text(fields.get("正文内容", ""))

    # 解析正文内容为段落
    paragraphs = content.strip().split("\n\n")
    sections = []
    for para in paragraphs:
        lines = para.strip().split("\n")
        if lines:
            sections.append({
                "title": lines[0],
                "content": lines[1:] if len(lines) > 1 else []
            })

    # 解析最后一段获取适配指数
    match_percent = "80"  # 默认值
    for line in content.split("\n"):
        if "适配指数" in line:
            match = re.search(r'(\d+)%', line)
            if match:
                match_percent = match.group(1)
            break

    return {
        "record_id": record["record_id"],
        "title": title,
        "zodiac1": "射手座",
        "zodiac2": "射手座",  # 射手遇到射手
        "match_percent": match_percent,
        "theme_title": "双倍自由",
        "theme_desc": subtitle,
        "tagline_line1": "两个射手相遇",
        "tagline_highlight": "就像照镜子",
        "tagline_rest": "",
        "summary_highlight": "双火组合",
        "summary_line1_before": "懂得",
        "summary_line1_highlight": "彼此的自由",
        "summary_line2": "",
        "blessing_line1": "愿你们的相遇",
        "blessing_line2": "永远保持这份默契",
        "sections": sections,
        "quotes": [
            "火遇火，一见如故",
            "说走就走×2，才是我们的浪漫",
            "气完就忘，谁都不记仇",
            "不用解释，对方都懂",
            "一起浪很开心，但谁来负责任"
        ]
    }

async def svg_to_png(svg_path: Path, png_path: Path):
    """SVG转PNG"""
    html_content = wrap_svg_html(svg_path.read_text(encoding="utf-8"))
    html_path = svg_path.with_suffix(".html")
    html_path.write_text(html_content, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1440})
        await page.goto(f"file://{html_path.absolute()}")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=str(png_path), type="png")
        await browser.close()

def upload_image(token: str, file_path: Path) -> str:
    """上传图片到飞书"""
    url = f"https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    headers = {"Authorization": f"Bearer {token}"}

    with open(file_path, "rb") as f:
        files = {
            "file": (file_path.name, f, "image/png"),
        }
        data = {
            "file_name": file_path.name,
            "parent_type": "bitable_image",
            "parent_node": APP_TOKEN,
            "size": str(file_path.stat().st_size)
        }
        resp = requests.post(url, headers=headers, files=files, data=data)
        return resp.json().get("data", {}).get("file_token", "")

def update_record(token: str, record_id: str, file_tokens: list):
    """更新飞书记录的图片字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    attachments = [{"file_token": ft} for ft in file_tokens]
    data = {"fields": {"生成图片": attachments, "已生成": True}}

    resp = requests.put(url, headers=headers, json=data)
    return resp.json()

async def generate_posters(record_data, templates, output_dir):
    """生成全部海报"""
    output_dir.mkdir(parents=True, exist_ok=True)

    zodiac1 = record_data["zodiac1"]
    zodiac2 = record_data["zodiac2"]
    sections = record_data["sections"]

    png_files = []

    # 1. 封面
    cover_data = {
        "zodiac1": zodiac1,
        "zodiac2": zodiac2,
        "match_percent": record_data["match_percent"],
        "theme_title": record_data["theme_title"],
        "theme_desc": record_data["theme_desc"],
        "tagline_line1": record_data["tagline_line1"],
        "tagline_highlight": record_data["tagline_highlight"],
        "tagline_rest": record_data["tagline_rest"],
    }
    cover_svg = render_cover(templates['cover'], cover_data)
    cover_svg_path = output_dir / "01_cover.svg"
    cover_svg_path.write_text(cover_svg, encoding="utf-8")
    cover_png_path = output_dir / "01_cover.png"
    await svg_to_png(cover_svg_path, cover_png_path)
    png_files.append(cover_png_path)
    print(f"  ✅ 01_cover.png")

    # 2-6. 内页
    for i, section in enumerate(sections[:5], start=1):
        page_data = {
            "zodiac1": zodiac1,
            "zodiac2": zodiac2,
            "part_num": f"0{i}",
            "section_title": section["title"],
            "content_lines": section["content"],
            "quote": record_data["quotes"][i-1] if i <= len(record_data.get("quotes", [])) else "",
            "page_num": f"0 {i+1}",
        }
        page_svg = render_page(templates['page'], page_data)
        page_svg_path = output_dir / f"0{i+1}_page.svg"
        page_svg_path.write_text(page_svg, encoding="utf-8")
        page_png_path = output_dir / f"0{i+1}_page.png"
        await svg_to_png(page_svg_path, page_png_path)
        png_files.append(page_png_path)
        print(f"  ✅ 0{i+1}_page.png")

    # 7. 结尾页
    end_data = {
        "zodiac1": zodiac1,
        "zodiac2": zodiac2,
        "match_percent": record_data["match_percent"],
        "summary_highlight": record_data["summary_highlight"],
        "summary_line1_before": record_data["summary_line1_before"],
        "summary_line1_highlight": record_data["summary_line1_highlight"],
        "summary_line2": record_data["summary_line2"],
        "blessing_line1": record_data["blessing_line1"],
        "blessing_line2": record_data["blessing_line2"],
        "page_num": "07",
    }
    end_svg = render_end(templates['end'], end_data)
    end_svg_path = output_dir / "07_end.svg"
    end_svg_path.write_text(end_svg, encoding="utf-8")
    end_png_path = output_dir / "07_end.png"
    await svg_to_png(end_svg_path, end_png_path)
    png_files.append(end_png_path)
    print(f"  ✅ 07_end.png")

    return png_files

async def main():
    print("🔑 获取飞书 access token...")
    token = get_access_token()
    print("✅ Token 获取成功\n")

    print("📥 从飞书获取记录...")
    record = fetch_record_by_title(token, "射手遇到射手")
    if not record:
        print("❌ 未找到记录")
        return
    print(f"✅ 找到记录: {record['record_id']}\n")

    print("📄 加载模板...")
    templates = extract_templates_from_md(TEMPLATE_PATH)
    if not templates.get('cover') or not templates.get('page') or not templates.get('end'):
        print("❌ 无法从TEMPLATE.md提取模板")
        return
    print("✅ 模板加载成功\n")

    print("🎨 解析记录数据...")
    record_data = parse_feishu_record(record)
    print(f"✅ 标题: {record_data['title']}\n")

    # 输出目录
    today = datetime.now().strftime("%Y/%m/%d")
    output_dir = Path(f"/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/{today}/射手遇到射手_命定之约风")

    print(f"📄 生成SVG并转换PNG...")
    print(f"   目录: {output_dir}")
    png_files = await generate_posters(record_data, templates, output_dir)

    print(f"\n☁️ 上传飞书...")
    file_tokens = []
    for png_path in png_files:
        ft = upload_image(token, png_path)
        if ft:
            file_tokens.append(ft)
            print(f"  ✅ {png_path.name}")
        else:
            print(f"  ❌ {png_path.name} 上传失败")

    print(f"\n📝 更新飞书记录...")
    update_record(token, record_data["record_id"], file_tokens)
    print(f"✅ 记录更新成功！共 {len(file_tokens)} 张图片")

    print(f"\n🎉 全部完成！")

if __name__ == "__main__":
    asyncio.run(main())
