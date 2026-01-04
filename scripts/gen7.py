#!/usr/bin/env python3
"""简化版7套海报生成脚本"""
import os
import json
import re
import requests
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent

# 飞书配置
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

# 模板映射
TEMPLATE_MAP = {
    "经典强调风": "editorial-classic",
    "简约边框风": "editorial-border",
    "杂志双线风": "editorial-magazine",
    "优雅留白风": "editorial-elegant",
    "暖色编辑风": "editorial-warm",
    "极简暖色风": "minimal-warm",
    "极简留白": "minimal-whitespace",
}

ZODIAC_EN = {"射手座": "SAGITTARIUS", "天蝎座": "SCORPIO"}

def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json()["tenant_access_token"]

def get_records(token, titles):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    conditions = [{"field_name": "标题", "operator": "is", "value": [t]} for t in titles]
    data = {"filter": {"conjunction": "or", "conditions": conditions}}
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()
    return result.get("data", {}).get("items", []) if result.get("code") == 0 else []

def extract_text(field):
    if isinstance(field, list):
        return field[0].get('text', '') if field else ''
    return str(field) if field else ''

def load_svg():
    with open(PROJECT_ROOT / "skills/zodiac-poster/assets/zodiac-symbols.json", 'r') as f:
        return json.load(f)

def split_content(content, max_chars=150):
    paras = [p.strip() for p in content.split('\n\n') if p.strip()]
    if len(paras) < 3:
        paras = [p.strip() for p in content.split('\n') if p.strip()]
    pages, current, length = [], [], 0
    for p in paras:
        if length + len(p) > max_chars and current:
            pages.append('\n\n'.join(current))
            current, length = [p], len(p)
        else:
            current.append(p)
            length += len(p)
    if current:
        pages.append('\n\n'.join(current))
    return pages

def gen_cover(template, zodiac, title, subtitle, svg):
    en = ZODIAC_EN.get(zodiac, "SAGITTARIUS")
    main = title.replace(zodiac, '').strip()
    if '，' in main:
        parts = main.split('，')
        main = f'{parts[0]}<br/><span class="accent">{parts[1]}</span>'
    
    # 根据模板选择颜色
    colors = {
        "minimal-whitespace": ("#D97757", "#FAF9F7", "#F5F3F0"),
        "minimal-warm": ("#C8725A", "#FAF8F5", "#F4EFE8"),
        "editorial-warm": ("#C15F3C", "#FAF6F1", "#F2E8DD"),
        "editorial-elegant": ("#C15F3C", "#FAF6F1", "#F0E6D9"),
        "editorial-magazine": ("#C15F3C", "#FAF6F1", "#F0E6D9"),
        "editorial-border": ("#C15F3C", "#FAF6F1", "#F0E6D9"),
        "editorial-classic": ("#C15F3C", "#FAF6F1", "#F0E6D9"),
    }
    accent, bg1, bg2 = colors.get(template, ("#C15F3C", "#FAF6F1", "#F0E6D9"))
    
    return f'''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1440">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
.poster{{width:1080px;height:1440px;position:relative;background:linear-gradient(165deg,{bg1} 0%,{bg2} 100%);font-family:'Noto Serif SC',serif;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.poster::before{{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");opacity:0.04;pointer-events:none;z-index:1}}
.badge{{position:absolute;top:100px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;z-index:10}}
.glow{{position:relative;display:flex;align-items:center;justify-content:center}}
.glow::before{{content:'';position:absolute;width:160px;height:160px;background:radial-gradient(circle,rgba(217,119,87,0.08) 0%,rgba(217,119,87,0) 70%);border-radius:50%;z-index:-1}}
.icon svg{{width:80px;height:80px;stroke:{accent};stroke-width:1.5;fill:none}}
.cn{{margin-top:24px;font-size:28px;font-weight:500;color:{accent};letter-spacing:10px}}
.en{{margin-top:8px;font-size:14px;color:#9A958E;letter-spacing:6px}}
.main{{position:relative;z-index:10;text-align:center;padding:0 100px;margin-top:60px}}
.title{{font-size:62px;font-weight:500;color:#2D2A26;letter-spacing:3px;line-height:1.7;margin-bottom:60px}}
.accent{{color:{accent};font-weight:500}}
.line{{width:50px;height:1px;background:{accent};margin:0 auto 45px}}
.sub{{font-size:24px;font-weight:300;color:#7A756E;letter-spacing:5px}}
.footer{{position:absolute;bottom:100px;left:50%;transform:translateX(-50%);text-align:center;z-index:10}}
.ft{{font-size:15px;color:#B5B0A8;letter-spacing:6px}}
.band{{position:absolute;bottom:0;left:0;right:0;height:6px;background:linear-gradient(90deg,{accent} 0%,#D4765A 50%,#E8A88C 100%)}}
</style></head>
<body><div class="poster">
<div class="badge"><div class="glow"><div class="icon">{svg}</div></div><div class="cn">{zodiac}</div><div class="en">{en}</div></div>
<div class="main"><h1 class="title">{main}</h1><div class="line"></div><p class="sub">{subtitle}</p></div>
<div class="footer"><span class="ft">情感独白</span></div>
<div class="band"></div>
</div></body></html>'''

def gen_page(template, zodiac, content, page_num, is_end, svg):
    en = ZODIAC_EN.get(zodiac, "SAGITTARIUS")
    colors = {
        "minimal-whitespace": ("#D97757", "#FAF9F7", "#F5F3F0"),
        "minimal-warm": ("#C8725A", "#FAF8F5", "#F4EFE8"),
        "editorial-warm": ("#C15F3C", "#FAF6F1", "#F2E8DD"),
        "editorial-elegant": ("#C15F3C", "#FAF6F1", "#F0E6D9"),
        "editorial-magazine": ("#C15F3C", "#FAF6F1", "#F0E6D9"),
        "editorial-border": ("#C15F3C", "#FAF6F1", "#F0E6D9"),
        "editorial-classic": ("#C15F3C", "#FAF6F1", "#F0E6D9"),
    }
    accent, bg1, bg2 = colors.get(template, ("#C15F3C", "#FAF6F1", "#F0E6D9"))
    content = content.replace('\n\n', '<br/><br/>').replace('\n', '<br/>')
    
    if is_end:
        return f'''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1440">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
.poster{{width:1080px;height:1440px;position:relative;background:linear-gradient(165deg,{bg1} 0%,{bg2} 100%);font-family:'Noto Serif SC',serif;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.poster::before{{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");opacity:0.04;pointer-events:none;z-index:1}}
.badge{{position:absolute;top:120px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;z-index:10}}
.icon svg{{width:52px;height:52px;stroke:{accent};stroke-width:1.5;fill:none}}
.name{{margin-top:20px;font-size:18px;color:{accent};letter-spacing:10px}}
.main{{position:relative;z-index:10;text-align:center;padding:0 100px;margin-top:60px}}
.content{{font-size:32px;color:#3D3832;line-height:2.2;letter-spacing:2px}}
.accent{{color:{accent};font-weight:500}}
.end{{margin-top:60px;font-size:28px;color:{accent}}}
.footer{{position:absolute;bottom:100px;left:50%;transform:translateX(-50%);z-index:10}}
.pn{{font-size:14px;color:#B5B0A8;letter-spacing:4px}}
.band{{position:absolute;bottom:0;left:0;right:0;height:6px;background:linear-gradient(90deg,{accent} 0%,#D4765A 50%,#E8A88C 100%)}}
</style></head>
<body><div class="poster">
<div class="badge"><div class="icon">{svg}</div><div class="name">{en}</div></div>
<div class="main"><p class="content">{content}</p><div class="end">✦</div></div>
<div class="footer"><span class="pn">{page_num:02d}</span></div>
<div class="band"></div>
</div></body></html>'''
    else:
        return f'''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1440">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
.poster{{width:1080px;height:1440px;position:relative;background:linear-gradient(165deg,{bg1} 0%,{bg2} 100%);font-family:'Noto Serif SC',serif;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.poster::before{{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");opacity:0.04;pointer-events:none;z-index:1}}
.label{{position:absolute;top:100px;left:50%;transform:translateX(-50%);font-size:14px;color:{accent};letter-spacing:8px;z-index:10}}
.main{{position:relative;z-index:10;text-align:center;padding:0 100px;max-width:900px}}
.content{{font-size:32px;color:#3D3832;line-height:2.2;letter-spacing:2px}}
.accent{{color:{accent};font-weight:500}}
.footer{{position:absolute;bottom:100px;left:50%;transform:translateX(-50%);z-index:10}}
.pn{{font-size:14px;color:#B5B0A8;letter-spacing:4px}}
.band{{position:absolute;bottom:0;left:0;right:0;height:6px;background:linear-gradient(90deg,{accent} 0%,#D4765A 50%,#E8A88C 100%)}}
</style></head>
<body><div class="poster">
<div class="label">· {page_num-1:02d} ·</div>
<div class="main"><p class="content">{content}</p></div>
<div class="footer"><span class="pn">{page_num:02d}</span></div>
<div class="band"></div>
</div></body></html>'''

def html_to_png(html, output):
    from playwright.sync_api import sync_playwright
    temp = output.with_suffix('.html')
    with open(temp, 'w', encoding='utf-8') as f:
        f.write(html)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1080, "height": 1440})
            page.goto(f"file://{temp}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(500)
            page.locator(".poster").screenshot(path=str(output))
            browser.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if temp.exists():
            temp.unlink()

def upload(token, record_id, paths):
    tokens = []
    for path in paths:
        url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
        size = os.path.getsize(path)
        name = os.path.basename(path)
        with open(path, "rb") as f:
            resp = requests.post(url, headers={"Authorization": f"Bearer {token}"}, 
                files={"file": (name, f, "image/png")},
                data={"file_name": name, "parent_type": "bitable_file", "parent_node": APP_TOKEN, "size": str(size)})
            result = resp.json()
            if result.get("code") == 0:
                tokens.append(result["data"]["file_token"])
                print(f"  ✓ {name}")
    
    if tokens:
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
        resp = requests.put(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"fields": {"生成图片": [{"file_token": t} for t in tokens], "已生成": True}})
        return resp.json().get("code") == 0
    return False

def process(record, token, symbols):
    fields = record.get("fields", {})
    rid = record.get("record_id")
    title = extract_text(fields.get("标题", ""))
    zodiac = fields.get("星座", "射手座")
    subtitle = extract_text(fields.get("副标题", ""))
    content = extract_text(fields.get("正文内容", ""))
    template_name = fields.get("模板", "极简留白")
    template = TEMPLATE_MAP.get(template_name, "minimal-whitespace")
    svg = symbols.get(zodiac, {}).get("svg", "")
    
    print(f"\n{'='*50}")
    print(f"处理: {title}")
    print(f"模板: {template_name} → {template}")
    
    safe = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)[:30]
    out_dir = PROJECT_ROOT / "output" / f"{zodiac}_{safe}"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    images = []
    
    # 封面
    print("生成封面...")
    cover = gen_cover(template, zodiac, title, subtitle, svg)
    cover_path = out_dir / "01_cover.png"
    if html_to_png(cover, cover_path):
        images.append(cover_path)
        print("  ✓ 封面完成")
    
    # 内页
    pages = split_content(content)
    print(f"正文 {len(pages)} 页")
    for i, page_content in enumerate(pages):
        num = i + 2
        is_end = (i == len(pages) - 1)
        print(f"生成第 {num} 页{'(结尾)' if is_end else ''}...")
        html = gen_page(template, zodiac, page_content, num, is_end, svg)
        path = out_dir / f"{num:02d}_page.png"
        if html_to_png(html, path):
            images.append(path)
            print(f"  ✓ 第 {num} 页完成")
    
    # 上传
    print(f"上传 {len(images)} 张图片...")
    if upload(token, rid, images):
        print(f"✓ {title} 完成")
        return True
    return False

def main():
    titles = [
        "射手座和天蝎座，千万别在一起？",
        "射手座的专注力开关",
        "射手座最舒服的职场关系",
        "射手座社交电量表",
        "射手座的消费指南",
        "射手座的边界感练习",
        "射手座的轻计划学习法"
    ]
    
    print("="*50)
    print(f"开始: {datetime.now()}")
    
    token = get_token()
    print("✓ Token获取成功")
    
    symbols = load_svg()
    print(f"✓ 加载 {len(symbols)} 个星座图标")
    
    records = get_records(token, titles)
    print(f"✓ 找到 {len(records)} 条记录")
    
    success = 0
    for record in records:
        try:
            if process(record, token, symbols):
                success += 1
        except Exception as e:
            print(f"✗ 失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*50)
    print(f"完成: {success}/{len(records)}")
    print(f"时间: {datetime.now()}")

if __name__ == "__main__":
    main()
