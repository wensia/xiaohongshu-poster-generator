#!/usr/bin/env python3
"""
命定之约风 SVG 模板生成器
从飞书拉取记录，生成套图并回传

架构原则：
- 所有样式由 SVG + TEMPLATE.md 定义
- 脚本只负责：解析【】标记、替换变量、生成文件
- 不在脚本中硬编码任何样式值
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


def extract_style_config(md_path: Path) -> dict:
    """从 TEMPLATE.md 中提取样式配置"""
    content = md_path.read_text(encoding="utf-8")
    config = {}

    # 提取字体规范表格
    # | 字体大小 | **32px** | 正文主字号 |
    # | 字间距 | **4px** | letter-spacing |
    # | 行间距 | **61px** | y 坐标递增值 |
    # | 主文字色 | **#4A3F35** | fill |
    # | 高亮色 | **#B86B4A** | fill |

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
    """解析【】标记，返回 [(text, is_highlight), ...] 列表"""
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
    """去掉【】标记，只保留内容"""
    return re.sub(r'【([^】]+)】', r'\1', text)


def render_content_lines(lines: list, style: dict) -> str:
    """
    生成正文内容 SVG
    样式参数从 TEMPLATE.md 读取，不在此硬编码
    """
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
    """渲染封面（只替换变量，不定义样式）"""
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
    """包装 SVG 为 HTML（用于截图）"""
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


def parse_feishu_record(record: dict) -> dict:
    """解析飞书记录"""
    fields = record["fields"]

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

    return {
        "record_id": record["record_id"],
        "title": title,
        "zodiac1": "射手座",
        "zodiac2": "射手座",
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
    """SVG 转 PNG"""
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
    print(f"  ✅ 01_cover.png")

    # 2-6. 内页（使用 style 配置）
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

    print("📄 从 TEMPLATE.md 加载模板和样式...")
    templates = extract_templates_from_md(TEMPLATE_PATH)
    style = extract_style_config(TEMPLATE_PATH)
    if not templates.get('cover') or not templates.get('page') or not templates.get('end'):
        print("❌ 无法从 TEMPLATE.md 提取模板")
        return
    print(f"✅ 模板加载成功")
    print(f"   字体: {style['font_size']}px, 字间距: {style['letter_spacing']}px")
    print(f"   主文字色: {style['text_color']}, 高亮色: {style['highlight_color']}\n")

    print("🎨 解析记录数据...")
    record_data = parse_feishu_record(record)
    print(f"✅ 标题: {record_data['title']}\n")

    # 输出目录
    today = datetime.now().strftime("%Y/%m/%d")
    output_dir = Path(f"/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/{today}/射手遇到射手_命定之约风")

    print(f"📄 生成 SVG 并转换 PNG...")
    print(f"   目录: {output_dir}")
    png_files = await generate_posters(record_data, templates, style, output_dir)

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
