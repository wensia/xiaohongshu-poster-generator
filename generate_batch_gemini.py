#!/usr/bin/env python3
"""
批量生成双子座套图
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

# 双子座 SVG
GEMINI_SVG = '<svg viewBox="0 0 24 24"><path d="M4 4h16M4 20h16M8 4v16M16 4v16" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# CSS 模板
BASE_CSS = """
    :root {
      --bg-color: #F5F2ED;
      --text-primary: #3D3835;
      --text-secondary: #6B6461;
      --accent-color: #C4653A;
      --line-color: #D4CFC8;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    @font-face {
      font-family: 'Noto Serif SC';
      src: local('Noto Serif SC'), local('Noto Serif CJK SC');
    }
    .poster {
      width: 1080px;
      height: 1440px;
      background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%);
      position: relative;
      padding: 90px 100px;
      display: flex;
      flex-direction: column;
      font-family: 'Noto Serif SC', 'Songti SC', serif;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    .header-title {
      display: flex;
      align-items: baseline;
      gap: 6px;
    }
    .header-zodiac {
      font-size: 32px;
      font-weight: 500;
      color: var(--accent-color);
      letter-spacing: 2px;
    }
    .header-separator {
      font-size: 24px;
      color: var(--line-color);
      margin: 0 4px;
    }
    .header-topic {
      font-size: 24px;
      font-weight: 300;
      color: var(--text-secondary);
      letter-spacing: 3px;
    }
    .zodiac-symbol svg {
      width: 56px;
      height: 56px;
      stroke: var(--accent-color);
      stroke-width: 1.5;
      fill: none;
      transform: rotate(-10deg);
    }
    .footer {
      margin-top: auto;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }
    .footer-line {
      width: 100%;
      height: 2px;
      background: var(--line-color);
      margin-bottom: 24px;
    }
    .page-number {
      font-family: 'Georgia', serif;
      font-size: 28px;
      color: var(--text-secondary);
      letter-spacing: 4px;
    }
    .highlight { color: var(--accent-color); }
"""

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

def parse_paragraphs(content: str) -> list:
    """解析正文为5个段落"""
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    return paragraphs

def extract_section_title(paragraph: str) -> str:
    """从段落提取2-4字小标题"""
    lines = paragraph.split('\n')
    first_line = lines[0].strip()
    # 提取关键词
    if len(first_line) <= 6:
        return first_line
    # 取前4个字
    return first_line[:4]

def smart_highlight(title: str) -> tuple:
    """智能识别标题高亮词"""
    # 高亮规则：动词/形容词优先
    highlights = {
        "来不及想": ("双子座", "来不及", "想"),
        "是看感觉的": ("双子座", "看感觉", "的"),
        "的拉扯感": ("双子座", "拉扯感", ""),
        "容易被点燃": ("双子座", "容易被点燃", ""),
        "的最终选择": ("双子座", "最终选择", ""),
    }
    for key, val in highlights.items():
        if key in title:
            return val
    return (title, "", "")

def create_cover(record: dict, page_num: int = 1) -> str:
    title = record["title"]
    subtitle = record["subtitle"]
    before, highlight, after = smart_highlight(title)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面 - {title}</title>
  <style>
{BASE_CSS}
    .cover-content {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 40px 0;
    }}
    .cover-subtitle {{
      font-size: 32px;
      color: var(--text-secondary);
      letter-spacing: 6px;
      margin-bottom: 50px;
    }}
    .cover-title {{
      font-size: 72px;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.4;
      letter-spacing: 8px;
      margin-bottom: 60px;
    }}
    .cover-divider {{
      width: 100px;
      height: 4px;
      background: var(--accent-color);
      margin-bottom: 60px;
    }}
    .cover-tagline {{
      font-size: 30px;
      color: var(--text-secondary);
      line-height: 1.9;
      letter-spacing: 4px;
    }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <div class="header-title">
        <span class="header-zodiac">双子座</span>
        <span class="header-separator">·</span>
        <span class="header-topic">性格解读</span>
      </div>
      <div class="zodiac-symbol">{GEMINI_SVG}</div>
    </div>

    <div class="cover-content">
      <p class="cover-subtitle">{subtitle}</p>
      <h1 class="cover-title">{before}<span class="highlight">{highlight}</span>{after}</h1>
      <div class="cover-divider"></div>
      <p class="cover-tagline">
        <span class="highlight">机智灵动</span> · 好奇心爆棚<br>思维跳跃 · <span class="highlight">永远有趣</span>
      </p>
    </div>

    <div class="footer">
      <div class="footer-line"></div>
      <span class="page-number">0{page_num}</span>
    </div>
  </div>
</body>
</html>'''

def create_page(record: dict, part_num: int, paragraph: str, page_num: int) -> str:
    title = record["title"]
    section = extract_section_title(paragraph)
    lines = paragraph.split('\n')
    content_html = "\n".join([f"        <p>{line}</p>" for line in lines])

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {page_num:02d} - {section}</title>
  <style>
{BASE_CSS}
    .part-label {{
      font-family: 'Georgia', serif;
      font-size: 26px;
      color: var(--accent-color);
      letter-spacing: 8px;
      margin-top: 30px;
      margin-bottom: 16px;
    }}
    .section-title {{
      font-size: 64px;
      font-weight: 600;
      color: var(--text-primary);
      letter-spacing: 6px;
      margin-bottom: 24px;
    }}
    .section-divider {{
      width: 100px;
      height: 4px;
      background: var(--accent-color);
      margin-bottom: 80px;
    }}
    .content-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-bottom: 60px;
    }}
    .content-text {{
      font-size: 38px;
      color: var(--text-primary);
      line-height: 2.0;
      letter-spacing: 3px;
      text-align: center;
    }}
    .content-text p {{
      margin-bottom: 16px;
    }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <div class="header-title">
        <span class="header-zodiac">双子座</span>
        <span class="header-separator">·</span>
        <span class="header-topic">性格解读</span>
      </div>
      <div class="zodiac-symbol">{GEMINI_SVG}</div>
    </div>

    <p class="part-label">PART 0{part_num}</p>
    <h2 class="section-title">{section}</h2>
    <div class="section-divider"></div>

    <div class="content-body">
      <div class="content-text">
{content_html}
      </div>
    </div>

    <div class="footer">
      <div class="footer-line"></div>
      <span class="page-number">0{page_num}</span>
    </div>
  </div>
</body>
</html>'''

def create_end(record: dict, page_num: int) -> str:
    title = record["title"]
    subtitle = record["subtitle"]

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {page_num:02d} - 总结</title>
  <style>
{BASE_CSS}
    .part-label {{
      font-family: 'Georgia', serif;
      font-size: 26px;
      color: var(--accent-color);
      letter-spacing: 8px;
      margin-top: 30px;
      margin-bottom: 16px;
    }}
    .section-title {{
      font-size: 56px;
      font-weight: 600;
      color: var(--text-primary);
      letter-spacing: 6px;
      margin-bottom: 24px;
    }}
    .section-divider {{
      width: 100px;
      height: 4px;
      background: var(--accent-color);
      margin-bottom: 80px;
    }}
    .summary-content {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding-bottom: 60px;
      text-align: center;
    }}
    .summary-text {{
      font-size: 36px;
      color: var(--text-primary);
      line-height: 2.0;
      letter-spacing: 2px;
    }}
    .ending-section {{
      margin-top: 80px;
      text-align: center;
    }}
    .ending-wish {{
      font-size: 30px;
      color: var(--text-secondary);
      letter-spacing: 4px;
      line-height: 1.9;
      font-style: italic;
    }}
    .ending-mark {{
      margin-top: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 30px;
    }}
    .ending-mark::before,
    .ending-mark::after {{
      content: '';
      width: 60px;
      height: 2px;
      background: var(--line-color);
    }}
    .ending-mark span {{
      font-family: 'Georgia', serif;
      font-size: 24px;
      color: var(--accent-color);
      letter-spacing: 6px;
    }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <div class="header-title">
        <span class="header-zodiac">双子座</span>
        <span class="header-separator">·</span>
        <span class="header-topic">性格解读</span>
      </div>
      <div class="zodiac-symbol">{GEMINI_SVG}</div>
    </div>

    <p class="part-label">EXTRA</p>
    <h2 class="section-title">屏幕前的双子</h2>
    <div class="section-divider"></div>

    <div class="summary-content">
      <div class="summary-text">
        <p>这就是<span class="highlight">双子座</span></p>
        <p>{subtitle}</p>
        <p>你也是这样吗</p>
      </div>

      <div class="ending-section">
        <p class="ending-wish">
          愿你永远<span class="highlight">有趣</span><br>
          永远被世界的<span class="highlight">新鲜感</span>点燃
        </p>
        <div class="ending-mark">
          <span>END</span>
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-line"></div>
      <span class="page-number">0{page_num}</span>
    </div>
  </div>
</body>
</html>'''

async def html_to_png(html_dir: Path) -> list:
    """将HTML转换为PNG"""
    html_files = sorted(html_dir.glob("*.html"))
    png_files = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1440})

        for html_file in html_files:
            png_file = html_file.with_suffix(".png")
            await page.goto(f"file://{html_file.absolute()}")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(0.3)
            await page.screenshot(path=str(png_file), full_page=False)
            print(f"  ✅ {html_file.name} → {png_file.name}")
            png_files.append(png_file)

        await browser.close()

    return png_files

def generate_one_set(record: dict, base_dir: Path) -> Path:
    """生成一套图片"""
    title = record["title"]
    output_dir = base_dir / title
    output_dir.mkdir(parents=True, exist_ok=True)

    paragraphs = parse_paragraphs(record["content"])

    # 1. 封面
    html = create_cover(record, 1)
    (output_dir / "01_cover.html").write_text(html, encoding="utf-8")

    # 2-6. 内容页
    for i, para in enumerate(paragraphs, start=1):
        html = create_page(record, i, para, i + 1)
        (output_dir / f"{i+1:02d}_page.html").write_text(html, encoding="utf-8")

    # 7. 总结页
    html = create_end(record, 7)
    (output_dir / "07_end.html").write_text(html, encoding="utf-8")

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

        # 1. 生成HTML
        print("📄 生成HTML...")
        output_dir = generate_one_set(record, base_dir)
        print(f"   目录: {output_dir}")

        # 2. 转换PNG
        print("🖼️  转换PNG...")
        png_files = await html_to_png(output_dir)

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
