#!/usr/bin/env python3
"""
性格独白风 SVG 模板生成器
每套：1封面 + 5内容页 + 1总结页 = 7张
"""
import asyncio
import requests
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# 飞书配置
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

# 5条记录数据
RECORDS = [
    {
        "record_id": "recv7SLDWWqsun",
        "title": "双子座来不及想",
        "subtitle": "直觉比脑子快",
        "content": """别人还在列清单分析利弊的时候
我已经做完了
不是冲动 是直觉比脑子快

想太多真的会错过
机会不等人 感觉不等人
双子的第六感 比逻辑靠谱

后悔这件事
等做完再说吧
反正现在这一秒 我很爽

有人说我不过脑子
其实是脑子太快
快到来不及解释给你听

双子的人生哲学就四个字
先冲了再说
想不通的事 做完就通了"""
    },
    {
        "record_id": "recv7SLEpwXaFg",
        "title": "双子座是看感觉的",
        "subtitle": "感觉对了什么都对",
        "content": """逻辑我有的
但感觉永远排第一
脑子说可以 心说不行
那就是不行

道理我都懂
可是感觉不对啊
这句话我说了一万遍

选人选事选未来
最后都是一个字
感觉
感觉对了 什么都对

你问我为什么选这个
我也说不清
就是感觉它在发光

感觉不对的时候
理由再多也没用
硬撑只会更累
不如相信直觉 然后走人"""
    },
    {
        "record_id": "recv7SLENIkRKM",
        "title": "双子座的拉扯感",
        "subtitle": "两个我在开会",
        "content": """想靠近 又想逃
想要 又怕真的要到
这不是矛盾
是两个我在开会

一边说无所谓
一边偷偷在意
表面风轻云淡
内心戏比电视剧还多

纠结的时候
脑子里像开辩论赛
正方反方都是我
而且永远打成平手

别催我做决定
我需要让两个自己先吵完
吵完才能统一意见

所以双子的犹豫不是优柔寡断
是内心在做民主决策
投票还没出结果而已"""
    },
    {
        "record_id": "recv7SLFdsL59Y",
        "title": "双子座容易被点燃",
        "subtitle": "一点就着",
        "content": """一个眼神 一句话
甚至一个表情包
都能让我瞬间上头
双子就是这么容易被点燃

热情来得快 燃得猛
但也可能说灭就灭
不是善变
是太容易被触动

有趣的人 有趣的事
都是我的火柴
一点就着 根本控制不住

新鲜感就是我的氧气
没有它 火就灭了
所以别怪我冷
是你没有持续给燃料

想让双子一直在线
秘诀只有一个
不断给新鲜感
让我永远有东西可以期待"""
    },
    {
        "record_id": "recv7SLFBUOE1k",
        "title": "双子座的最终选择",
        "subtitle": "绕一圈回到直觉",
        "content": """纠结了很久 分析了很久
问了很多人 列了很多单
最后怎么选的
闭眼 随便选一个

选完才发现
这不就是我一开始想要的吗
绕了一大圈
还是回到了最初的直觉

双子的选择题永远是
A想要 B也想要
最终答案
先A后B 或者都要

选不出来的时候
就别选了
等一个新选项出现
说不定比AB都好

所以双子的最终选择
往往不是选出来的
是等出来的
或者 是心里早就定了的"""
    }
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

def smart_highlight(title: str) -> tuple:
    """智能识别标题高亮词"""
    highlights = {
        "来不及想": ("双子座", "来不及", "想"),
        "是看感觉的": ("双子座", "看感觉", "的"),
        "的拉扯感": ("双子座的", "拉扯感", ""),
        "容易被点燃": ("双子座", "容易被点燃", ""),
        "的最终选择": ("双子座的", "最终选择", ""),
    }
    for key, val in highlights.items():
        if key in title:
            return val
    return (title, "", "")

def create_cover(record: dict, page_num: int = 1) -> str:
    """创建封面 SVG"""
    title = record["title"]
    subtitle = record["subtitle"]
    before, highlight, after = smart_highlight(title)

    svg = SVG_HEADER + create_header() + f'''
  <!-- 封面内容 -->
  <g id="cover-content">
    <!-- 副标题 -->
    <text x="540" y="520" font-family="Noto Serif SC, serif" font-size="32" fill="#6B6461" text-anchor="middle" letter-spacing="6">{subtitle}</text>

    <!-- 主标题 -->
    <text x="540" y="680" font-family="Noto Serif SC, serif" font-size="72" font-weight="600" text-anchor="middle" letter-spacing="6">
      <tspan fill="#3D3835">{before}</tspan><tspan fill="#C4653A">{highlight}</tspan><tspan fill="#3D3835">{after}</tspan>
    </text>

    <!-- 分隔线 -->
    <rect x="490" y="750" width="100" height="4" fill="#C4653A"/>

    <!-- 标语 -->
    <text x="540" y="860" font-family="Noto Serif SC, serif" font-size="30" fill="#6B6461" text-anchor="middle" letter-spacing="4">
      <tspan fill="#C4653A">机智灵动</tspan><tspan fill="#6B6461"> · 好奇心爆棚</tspan>
    </text>
    <text x="540" y="920" font-family="Noto Serif SC, serif" font-size="30" fill="#6B6461" text-anchor="middle" letter-spacing="4">
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

    # 生成正文内容
    content_lines = ""
    y = 0
    for line in lines:
        line = line.strip()
        if line:
            content_lines += f'    <text y="{y}" font-family="Noto Serif SC, serif" font-size="36" fill="#3D3835" letter-spacing="2">{line}</text>\n'
            y += 65

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
    output_dir = base_dir / title
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

    for record in RECORDS:
        title = record["title"]
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
