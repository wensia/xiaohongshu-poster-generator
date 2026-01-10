#!/usr/bin/env python3
"""
性格独白风 SVG 模板生成器
每套：1封面 + 5内容页 + 1总结页 = 7张
支持智能高亮
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

# 5条记录ID
RECORD_IDS = [
    "recv7SLDWWqsun",
    "recv7SLEpwXaFg",
    "recv7SLENIkRKM",
    "recv7SLFdsL59Y",
    "recv7SLFBUOE1k"
]

# 双子座 SVG 图标
GEMINI_SVG = '''<svg viewBox="0 0 100 100" width="56" height="56" fill="none" stroke="#C4653A" stroke-width="2">
  <line x1="20" y1="20" x2="80" y2="20"/>
  <line x1="20" y1="80" x2="80" y2="80"/>
  <line x1="35" y1="20" x2="35" y2="80"/>
  <line x1="65" y1="20" x2="65" y2="80"/>
</svg>'''

# SVG 模板头部
SVG_HEADER = '''<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FAF6F1"/>
      <stop offset="50%" stop-color="#F5EDE4"/>
      <stop offset="100%" stop-color="#F0E6D9"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.3"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.03"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>
'''

def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json()["tenant_access_token"]

def fetch_records(token: str) -> list:
    """从飞书获取记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # 搜索指定记录
    data = {
        "filter": {
            "conjunction": "or",
            "conditions": [{"field_name": "record_id", "operator": "is", "value": [rid]} for rid in RECORD_IDS]
        },
        "automatic_fields": True
    }

    records = []
    for rid in RECORD_IDS:
        url_get = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{rid}"
        resp = requests.get(url_get, headers=headers)
        result = resp.json()
        if result.get("code") == 0:
            record = result["data"]["record"]
            fields = record["fields"]
            records.append({
                "record_id": rid,
                "title": fields.get("标题", ""),
                "subtitle": fields.get("副标题", ""),
                "content": fields.get("正文内容", ""),
                "template": fields.get("模板", "")
            })
    return records

def upload_image(token: str, image_path: Path) -> str:
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/png")}
        data = {
            "file_name": image_path.name,
            "parent_type": "bitable_file",
            "parent_node": APP_TOKEN,
            "size": str(image_path.stat().st_size)
        }
        resp = requests.post(url, headers={"Authorization": f"Bearer {token}"}, files=files, data=data)
        result = resp.json()
        if result.get("code") == 0:
            return result["data"]["file_token"]
    return None

def update_record(token: str, record_id: str, file_tokens: list, image_path: str):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    data = {
        "fields": {
            "生成图片": [{"file_token": ft} for ft in file_tokens],
            "生成图片路径": image_path,
            "已生成": True
        }
    }
    resp = requests.put(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=data)
    return resp.json()

def create_header():
    """创建页眉"""
    return f'''
  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#C4653A" letter-spacing="2">双子座</text>
    <text x="210" y="130" font-family="Georgia, serif" font-size="24" fill="#D4CFC8">·</text>
    <text x="240" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#6B6461" letter-spacing="3">性格解读</text>
    <g transform="translate(924, 74) rotate(-10)">
      {GEMINI_SVG}
    </g>
  </g>
'''

def create_footer(page_num: int):
    """创建页脚"""
    return f'''
  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4CFC8" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#6B6461" text-anchor="end" letter-spacing="4">0 {page_num}</text>
  </g>
'''

def parse_highlight_marks(text: str) -> list:
    """
    解析【】标记，返回 [(text, is_highlight), ...] 列表

    这是纯解析函数，不做任何语义判断。
    高亮词由 AI 在内容生成阶段用【】标记。

    示例:
        输入: "【双子座】做【决定】来不及【想】"
        输出: [("双子座", True), ("做", False), ("决定", True), ("来不及", False), ("想", True)]
    """
    result = []
    pattern = r'【([^】]+)】'
    last_end = 0

    for match in re.finditer(pattern, text):
        # 标记前的普通文字
        if match.start() > last_end:
            result.append((text[last_end:match.start()], False))
        # 标记内的高亮文字
        result.append((match.group(1), True))
        last_end = match.end()

    # 剩余的普通文字
    if last_end < len(text):
        result.append((text[last_end:], False))

    # 如果没有任何标记，返回整个文本作为普通文字
    if not result:
        result.append((text, False))

    return result

def render_highlighted_text(text: str, base_x: int, base_y: int, font_size: int = 72,
                           font_weight: str = "600", anchor: str = "middle") -> str:
    """
    渲染带【】标记的文本为 SVG tspan

    解析【】标记，将标记内的文字渲染为 accent 色，其余为普通色。
    """
    parts = parse_highlight_marks(text)

    tspans = ""
    for part_text, is_highlight in parts:
        color = "#C4653A" if is_highlight else "#3D3835"
        tspans += f'<tspan fill="{color}">{part_text}</tspan>'

    return f'''<text x="{base_x}" y="{base_y}" font-family="Noto Serif SC, serif" font-size="{font_size}" font-weight="{font_weight}" text-anchor="{anchor}" letter-spacing="6">{tspans}</text>'''

def strip_highlight_marks(text: str) -> str:
    """去掉【】标记，只保留内容"""
    return re.sub(r'【([^】]+)】', r'\1', text)

def create_cover(record: dict, page_num: int = 1) -> str:
    """创建封面 SVG - 支持两行标题和智能高亮"""
    title = record["title"]
    subtitle = record["subtitle"]

    # 解析两行标题
    title_lines = title.split('\n') if '\n' in title else [title]
    line1 = title_lines[0] if len(title_lines) > 0 else ""
    line2 = title_lines[1] if len(title_lines) > 1 else ""

    # 渲染第一行（解析【】标记，高亮标记内的文字）
    line1_svg = render_highlighted_text(line1, 540, 600, font_size=72, font_weight="600", anchor="middle")

    # 第二行：去掉【】标记，整行使用 accent 色
    line2_clean = strip_highlight_marks(line2)
    line2_svg = f'<text x="540" y="700" font-family="Noto Serif SC, serif" font-size="56" font-weight="500" fill="#C4653A" text-anchor="middle" letter-spacing="8">{line2_clean}</text>' if line2_clean else ""

    svg = SVG_HEADER + create_header() + f'''
  <!-- 封面内容 -->
  <g id="cover-content">
    <!-- 副标题 -->
    <text x="540" y="480" font-family="Noto Serif SC, serif" font-size="32" fill="#6B6461" text-anchor="middle" letter-spacing="6">{subtitle}</text>

    <!-- 主标题第一行（智能高亮） -->
    {line1_svg}

    <!-- 主标题第二行（accent色） -->
    {line2_svg}

    <!-- 分隔线 -->
    <rect x="490" y="780" width="100" height="4" fill="#C4653A"/>

    <!-- 标语 -->
    <text x="540" y="890" font-family="Noto Serif SC, serif" font-size="30" fill="#6B6461" text-anchor="middle" letter-spacing="4">
      <tspan fill="#C4653A">机智灵动</tspan><tspan fill="#6B6461"> · 好奇心爆棚</tspan>
    </text>
    <text x="540" y="950" font-family="Noto Serif SC, serif" font-size="30" fill="#6B6461" text-anchor="middle" letter-spacing="4">
      <tspan fill="#6B6461">思维跳跃 · </tspan><tspan fill="#C4653A">永远有趣</tspan>
    </text>
  </g>
''' + create_footer(page_num) + '\n</svg>'
    return svg

def extract_section_title(paragraph: str) -> str:
    """从段落提取小标题"""
    lines = paragraph.split('\n')
    first_line = lines[0].strip()
    if len(first_line) <= 6:
        return first_line
    return first_line[:4]

def create_page(record: dict, part_num: int, paragraph: str, page_num: int) -> str:
    """创建内容页 SVG"""
    section = extract_section_title(paragraph)
    lines = paragraph.split('\n')

    # 生成正文内容（字体36px，字间距4px，行高70px - 按 TEMPLATE.md 规范）
    content_lines = ""
    y = 0
    for line in lines:
        line = line.strip()
        if line:
            # 解析【】高亮标记
            parts = parse_highlight_marks(line)
            tspans = ""
            for part_text, is_highlight in parts:
                color = "#C4653A" if is_highlight else "#3D3835"
                tspans += f'<tspan fill="{color}">{part_text}</tspan>'
            content_lines += f'    <text y="{y}" font-family="Noto Serif SC, serif" font-size="36" letter-spacing="4">{tspans}</text>\n'
            y += 70

    # 生成引用
    quote = lines[-1] if lines else ""

    svg = SVG_HEADER + create_header() + f'''
  <!-- 章节标签 -->
  <text x="100" y="240" font-family="Georgia, serif" font-size="26" fill="#C4653A" letter-spacing="8">PART 0{part_num}</text>

  <!-- 章节标题 -->
  <text x="100" y="340" font-family="Noto Serif SC, serif" font-size="64" font-weight="600" fill="#3D3835" letter-spacing="6">{section}</text>

  <!-- 分隔线 -->
  <rect x="100" y="380" width="100" height="4" fill="#C4653A"/>

  <!-- 正文内容 -->
  <g id="content" transform="translate(100, 520)">
{content_lines}  </g>

  <!-- 引用区块 -->
  <g id="quote" transform="translate(100, 1150)">
    <line x1="0" y1="0" x2="0" y2="60" stroke="#C4653A" stroke-width="4"/>
    <text x="30" y="40" font-family="Noto Serif SC, serif" font-size="28" font-style="italic" fill="#6B6461" letter-spacing="2">"{quote}"</text>
  </g>
''' + create_footer(page_num) + '\n</svg>'
    return svg

def create_end(record: dict, page_num: int) -> str:
    """创建结尾页 SVG"""
    subtitle = record["subtitle"]

    svg = SVG_HEADER + create_header() + f'''
  <!-- 居中内容区域 -->
  <g id="centered-content" transform="translate(540, 0)">
    <!-- 章节标签 -->
    <text x="0" y="240" font-family="Georgia, serif" font-size="26" fill="#C4653A" letter-spacing="8" text-anchor="middle">EXTRA</text>

    <!-- 章节标题 -->
    <text x="0" y="340" font-family="Noto Serif SC, serif" font-size="64" font-weight="600" fill="#3D3835" letter-spacing="6" text-anchor="middle">屏幕前的双子</text>

    <!-- 分隔线 -->
    <rect x="-50" y="380" width="100" height="4" fill="#C4653A"/>

    <!-- 主文案区域 -->
    <g id="summary" transform="translate(0, 520)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="36" fill="#3D3835" letter-spacing="2" text-anchor="middle">这就是<tspan fill="#C4653A">双子座</tspan></text>
      <text y="70" font-family="Noto Serif SC, serif" font-size="36" fill="#3D3835" letter-spacing="2" text-anchor="middle">{subtitle}</text>
      <text y="140" font-family="Noto Serif SC, serif" font-size="36" fill="#3D3835" letter-spacing="2" text-anchor="middle">你也是这样吗</text>
    </g>

    <!-- 装饰分隔线 -->
    <g id="content-divider" transform="translate(0, 780)">
      <line x1="-70" y1="0" x2="-20" y2="0" stroke="#D4CFC8" stroke-width="1"/>
      <text x="0" y="5" font-size="16" fill="#C4653A" text-anchor="middle">◆</text>
      <line x1="20" y1="0" x2="70" y2="0" stroke="#D4CFC8" stroke-width="1"/>
    </g>

    <!-- 祝福语区域 -->
    <g id="ending" transform="translate(0, 880)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="28" font-style="italic" fill="#6B6461" text-anchor="middle" letter-spacing="3">愿你永远<tspan fill="#C4653A">有趣</tspan></text>
      <text y="55" font-family="Noto Serif SC, serif" font-size="28" font-style="italic" fill="#6B6461" text-anchor="middle" letter-spacing="3">永远被世界的<tspan fill="#C4653A">新鲜感</tspan>点燃</text>

      <!-- END 标记 -->
      <g transform="translate(0, 130)">
        <line x1="-90" y1="0" x2="-30" y2="0" stroke="#D4CFC8" stroke-width="2"/>
        <text x="0" y="8" font-family="Georgia, serif" font-size="24" fill="#C4653A" text-anchor="middle" letter-spacing="6">END</text>
        <line x1="30" y1="0" x2="90" y2="0" stroke="#D4CFC8" stroke-width="2"/>
      </g>
    </g>
  </g>
''' + create_footer(page_num) + '\n</svg>'
    return svg

def parse_paragraphs(content: str) -> list:
    """解析正文为5个段落"""
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    return paragraphs

async def svg_to_png(svg_dir: Path) -> list:
    """将SVG转换为PNG"""
    svg_files = sorted(svg_dir.glob("*.svg"))
    png_files = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1440})

        for svg_file in svg_files:
            png_file = svg_file.with_suffix(".png")
            # 创建一个简单的HTML来渲染SVG
            html_content = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * {{ margin: 0; padding: 0; }}
    body {{ width: 1080px; height: 1440px; }}
  </style>
</head>
<body>
{svg_file.read_text(encoding='utf-8')}
</body>
</html>'''
            html_file = svg_file.with_suffix(".html")
            html_file.write_text(html_content, encoding='utf-8')

            await page.goto(f"file://{html_file.absolute()}")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(0.5)
            await page.screenshot(path=str(png_file), full_page=False)
            print(f"  ✅ {svg_file.name} → {png_file.name}")
            png_files.append(png_file)

            # 清理临时HTML
            html_file.unlink()

        await browser.close()

    return png_files

def generate_one_set(record: dict, base_dir: Path) -> Path:
    """生成一套图片"""
    title = record["title"]
    # 处理两行标题，用目录安全的名称
    dir_name = title.split('\n')[0] if '\n' in title else title
    # 去掉【】标记
    dir_name = strip_highlight_marks(dir_name)
    # 确保目录名安全（移除可能导致问题的字符）
    dir_name = dir_name.replace('/', '_').replace('\\', '_')
    output_dir = base_dir / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)

    paragraphs = parse_paragraphs(record["content"])

    # 1. 封面
    svg = create_cover(record, 1)
    (output_dir / "01_cover.svg").write_text(svg, encoding="utf-8")

    # 2-6. 内容页
    for i, para in enumerate(paragraphs, start=1):
        svg = create_page(record, i, para, i + 1)
        (output_dir / f"{i+1:02d}_page.svg").write_text(svg, encoding="utf-8")

    # 7. 总结页
    svg = create_end(record, 7)
    (output_dir / "07_end.svg").write_text(svg, encoding="utf-8")

    return output_dir

async def main():
    today = datetime.now().strftime("%Y/%m/%d")
    base_dir = Path(f"/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/{today}")

    print("🔑 获取飞书 access token...")
    token = get_access_token()
    print("✅ Token 获取成功\n")

    print("📥 从飞书获取记录...")
    records = fetch_records(token)
    print(f"✅ 获取到 {len(records)} 条记录\n")

    for record in records:
        title = record["title"].replace('\n', ' / ')
        print(f"\n{'='*50}")
        print(f"📝 处理: {title}")
        print(f"{'='*50}")

        # 1. 生成SVG
        print("📄 生成SVG...")
        output_dir = generate_one_set(record, base_dir)
        print(f"   目录: {output_dir}")

        # 2. 转换PNG
        print("🖼️  转换PNG...")
        png_files = await svg_to_png(output_dir)

        # 3. 上传飞书
        print("☁️  上传飞书...")
        file_tokens = []
        for png_file in png_files:
            ft = upload_image(token, png_file)
            if ft:
                file_tokens.append(ft)
                print(f"  ✅ {png_file.name}")

        # 4. 更新记录
        if file_tokens:
            result = update_record(token, record["record_id"], file_tokens, str(output_dir))
            if result.get("code") == 0:
                print(f"✅ 记录更新成功！共 {len(file_tokens)} 张图片")
            else:
                print(f"❌ 记录更新失败: {result}")

    print("\n" + "="*50)
    print("🎉 全部完成！共处理 5 套图，35 张图片")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
