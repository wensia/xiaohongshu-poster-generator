#!/usr/bin/env python3
"""
批量重新生成套图并回传飞书
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

# 模板路径
TEMPLATE_PATH = Path(__file__).parent / "skills/zodiac-poster/assets/templates/destined-bond/TEMPLATE.md"

# 待处理的记录
RECORDS_TO_PROCESS = [
    "射手遇到射手",
    "射手遇到摩羯",
    "射手遇到水瓶",
    "射手遇到双鱼",
]


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
    return items[0] if items else None


def extract_templates_from_md(md_path: Path) -> dict:
    """从 TEMPLATE.md 中提取 SVG 模板"""
    content = md_path.read_text(encoding="utf-8")
    templates = {}

    cover_match = re.search(
        r'## 封面模板.*?```svg\s*(<!-- \[STYLE: 命定之约风\] \[TYPE: cover\] -->.*?</svg>)\s*```',
        content, re.DOTALL
    )
    if cover_match:
        templates['cover'] = cover_match.group(1).strip()

    page_match = re.search(
        r'## 内页模板.*?```svg\s*(<!-- \[STYLE: 命定之约风\] \[TYPE: page\] -->.*?</svg>)\s*```',
        content, re.DOTALL
    )
    if page_match:
        templates['page'] = page_match.group(1).strip()

    end_match = re.search(
        r'## 结尾页模板.*?```svg\s*(<!-- \[STYLE: 命定之约风\] \[TYPE: end\] -->.*?</svg>)\s*```',
        content, re.DOTALL
    )
    if end_match:
        templates['end'] = end_match.group(1).strip()

    return templates


def extract_style_config(md_path: Path) -> dict:
    """从 TEMPLATE.md 中提取样式配置"""
    content = md_path.read_text(encoding="utf-8")
    config = {}

    font_size_match = re.search(r'字体大小\s*\|\s*\*\*(\d+)px\*\*', content)
    letter_spacing_match = re.search(r'字间距\s*\|\s*\*\*(\d+)px\*\*', content)
    line_height_match = re.search(r'行间距\s*\|\s*\*\*(\d+)px\*\*', content)
    text_color_match = re.search(r'主文字色\s*\|\s*\*\*(#[A-Fa-f0-9]+)\*\*', content)
    highlight_color_match = re.search(r'高亮色\s*\|\s*\*\*(#[A-Fa-f0-9]+)\*\*', content)

    config['font_size'] = font_size_match.group(1) if font_size_match else '32'
    config['letter_spacing'] = letter_spacing_match.group(1) if letter_spacing_match else '4'
    config['line_height'] = int(line_height_match.group(1)) if line_height_match else 61
    config['text_color'] = text_color_match.group(1) if text_color_match else '#4A3F35'
    config['highlight_color'] = highlight_color_match.group(1) if highlight_color_match else '#B86B4A'

    return config


def parse_highlight_marks(text: str) -> list:
    """解析【】标记"""
    result = []
    pattern = r'【([^】]+)】'
    last_end = 0
    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            result.append((text[last_end:match.start()], False))
        result.append((match.group(1), True))
        last_end = match.end()
    if last_end < len(text):
        result.append((text[last_end:], False))
    if not result:
        result.append((text, False))
    return result


def strip_highlight_marks(text: str) -> str:
    """去掉【】标记"""
    return re.sub(r'【([^】]+)】', r'\1', text)


def render_content_lines(lines: list, style: dict) -> str:
    """生成正文内容 SVG"""
    svg_lines = []
    y = 0
    font_size = style['font_size']
    letter_spacing = style['letter_spacing']
    text_color = style['text_color']
    highlight_color = style['highlight_color']
    line_height = style['line_height']

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = parse_highlight_marks(line)
        tspans = ""
        for part_text, is_highlight in parts:
            color = highlight_color if is_highlight else text_color
            tspans += f'<tspan fill="{color}">{part_text}</tspan>'

        svg_lines.append(
            f'<text y="{y}" font-family="Noto Serif SC, serif" '
            f'font-size="{font_size}" letter-spacing="{letter_spacing}">{tspans}</text>'
        )
        y += line_height

    return "\n    ".join(svg_lines)


def render_cover(template: str, data: dict) -> str:
    """渲染封面"""
    svg = template
    for key, value in data.items():
        svg = svg.replace("{{" + key.upper() + "}}", str(value))
    return svg


def render_page(template: str, data: dict, style: dict) -> str:
    """渲染内页"""
    svg = template
    svg = svg.replace("{{ZODIAC1}}", data["zodiac1"])
    svg = svg.replace("{{ZODIAC2}}", data["zodiac2"])
    svg = svg.replace("{{PART_NUM}}", data["part_num"])
    svg = svg.replace("{{SECTION_TITLE}}", data["section_title"])
    svg = svg.replace("{{CONTENT_LINES}}", render_content_lines(data["content_lines"], style))
    svg = svg.replace("{{QUOTE}}", strip_highlight_marks(data["quote"]))
    svg = svg.replace("{{PAGE_NUM}}", data["page_num"])
    return svg


def render_end(template: str, data: dict) -> str:
    """渲染结尾页"""
    svg = template
    for key, value in data.items():
        svg = svg.replace("{{" + key.upper() + "}}", str(value))
    return svg


def wrap_svg_html(svg_content: str) -> str:
    """包装 SVG 为 HTML"""
    return f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
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


def parse_feishu_record(record: dict) -> dict:
    """解析飞书记录，根据内容动态提取数据"""
    fields = record["fields"]

    def get_text(field_value):
        if isinstance(field_value, list) and len(field_value) > 0:
            return field_value[0].get("text", "")
        return str(field_value) if field_value else ""

    title = get_text(fields.get("标题", ""))
    subtitle = get_text(fields.get("副标题", ""))
    content = get_text(fields.get("正文内容", ""))

    # 从标题解析星座
    zodiac_match = re.match(r'(\w+座?)遇到(\w+座?)', title)
    zodiac1 = zodiac_match.group(1) if zodiac_match else "射手座"
    zodiac2 = zodiac_match.group(2) if zodiac_match else "射手座"

    # 确保星座名带"座"
    if not zodiac1.endswith("座"):
        zodiac1 += "座"
    if not zodiac2.endswith("座"):
        zodiac2 += "座"

    # 解析正文内容为段落
    paragraphs = content.strip().split("\n\n")
    sections = []
    for para in paragraphs:
        lines = para.strip().split("\n")
        if lines:
            sections.append({
                "title": strip_highlight_marks(lines[0]),
                "content": lines[1:] if len(lines) > 1 else []
            })

    # 解析适配指数
    match_percent = "80"
    for line in content.split("\n"):
        if "适配指数" in line:
            match = re.search(r'(\d+)%', line)
            if match:
                match_percent = match.group(1)
            break

    # 解析组合类型（如：火火组合、火土组合等）
    combo_type = "双火组合"
    for line in content.split("\n"):
        if "组合" in line:
            combo_match = re.search(r'([\u4e00-\u9fa5]+组合)', line)
            if combo_match:
                combo_type = combo_match.group(1)
            break

    # 解析主题词（从副标题或内容中提取）
    theme_title = subtitle.split("双倍")[0] if "双倍" in subtitle else subtitle[:4] if len(subtitle) >= 4 else subtitle

    # 生成标语（根据内容生成）
    tagline_line1 = f"两个{zodiac1[:-1]}相遇" if zodiac1 == zodiac2 else f"{zodiac1[:-1]}遇到{zodiac2[:-1]}"
    tagline_highlight = "就像照镜子" if zodiac1 == zodiac2 else "会怎样呢"

    # 从内容中提取 quotes
    quotes = []
    for section in sections[:5]:
        if section["content"]:
            # 取第一行作为 quote
            quotes.append(strip_highlight_marks(section["content"][0]) if section["content"] else "")

    return {
        "record_id": record["record_id"],
        "title": title,
        "zodiac1": zodiac1,
        "zodiac2": zodiac2,
        "match_percent": match_percent,
        "theme_title": theme_title if theme_title else "缘分",
        "theme_desc": subtitle,
        "tagline_line1": tagline_line1,
        "tagline_highlight": tagline_highlight,
        "tagline_rest": "",
        "summary_highlight": combo_type,
        "summary_line1_before": "懂得",
        "summary_line1_highlight": "彼此的需要",
        "summary_line2": "",
        "blessing_line1": "愿你们的相遇",
        "blessing_line2": "成就最好的彼此",
        "sections": sections,
        "quotes": quotes if quotes else ["", "", "", "", ""]
    }


async def svg_to_png(svg_path: Path, png_path: Path):
    """SVG 转 PNG"""
    html_content = wrap_svg_html(svg_path.read_text(encoding="utf-8"))
    html_path = svg_path.with_suffix(".html")
    html_path.write_text(html_content, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 1080, "height": 1440},
            device_scale_factor=2  # 2x 导出
        )
        await page.goto(f"file://{html_path.absolute()}")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=str(png_path), type="png")
        await browser.close()


def upload_image(token: str, file_path: Path) -> str:
    """上传图片到飞书"""
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    headers = {"Authorization": f"Bearer {token}"}

    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, "image/png")}
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


async def generate_posters(record_data: dict, templates: dict, style: dict, output_dir: Path) -> list:
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
    print(f"    ✅ 01_cover.png")

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
        page_svg = render_page(templates['page'], page_data, style)
        page_svg_path = output_dir / f"0{i+1}_page.svg"
        page_svg_path.write_text(page_svg, encoding="utf-8")
        page_png_path = output_dir / f"0{i+1}_page.png"
        await svg_to_png(page_svg_path, page_png_path)
        png_files.append(page_png_path)
        print(f"    ✅ 0{i+1}_page.png")

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
    print(f"    ✅ 07_end.png")

    return png_files


async def process_one_record(token: str, title: str, templates: dict, style: dict):
    """处理单条记录"""
    print(f"\n📥 处理: {title}")

    record = fetch_record_by_title(token, title)
    if not record:
        print(f"  ❌ 未找到记录")
        return

    record_data = parse_feishu_record(record)
    print(f"  ✅ 记录ID: {record_data['record_id']}")
    print(f"     星座: {record_data['zodiac1']} × {record_data['zodiac2']}")
    print(f"     契合指数: {record_data['match_percent']}%")

    # 输出目录
    today = datetime.now().strftime("%Y/%m/%d")
    safe_title = title.replace(" ", "_")
    output_dir = Path(f"/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/{today}/{safe_title}_命定之约风")

    print(f"  📄 生成套图...")
    png_files = await generate_posters(record_data, templates, style, output_dir)

    print(f"  ☁️ 上传飞书...")
    file_tokens = []
    for png_path in png_files:
        ft = upload_image(token, png_path)
        if ft:
            file_tokens.append(ft)

    if file_tokens:
        update_record(token, record_data["record_id"], file_tokens)
        print(f"  ✅ 完成! 共 {len(file_tokens)} 张图片")
    else:
        print(f"  ❌ 上传失败")


async def main():
    print("🔑 获取飞书 access token...")
    token = get_access_token()
    print("✅ Token 获取成功")

    print("\n📄 加载模板...")
    templates = extract_templates_from_md(TEMPLATE_PATH)
    style = extract_style_config(TEMPLATE_PATH)
    print(f"✅ 模板加载成功")

    print(f"\n🎯 待处理记录: {len(RECORDS_TO_PROCESS)} 条")
    for title in RECORDS_TO_PROCESS:
        print(f"   - {title}")

    for title in RECORDS_TO_PROCESS:
        await process_one_record(token, title, templates, style)

    print(f"\n🎉 全部完成!")


if __name__ == "__main__":
    asyncio.run(main())
