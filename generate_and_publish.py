#!/usr/bin/env python3
"""
生成套图并发布小红书笔记 - 射手座的占有欲有多强
"""

import os
import re
import sys
import json
import requests
import base64

# 添加工具库路径
sys.path.insert(0, '/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster')
from utils.screenshot import render_template_to_png

# 配置
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"

TEMPLATE_DIR = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster/assets/templates/personality-monologue"
OUTPUT_BASE = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output"


def get_feishu_token():
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    return resp.json()["tenant_access_token"]


def parse_highlight(text):
    """解析高亮词【】"""
    match = re.search(r'【([^】]+)】', text)
    if not match:
        return text

    before = text[:match.start()]
    highlight = match.group(1)
    after = text[match.end():]
    return {"before": before, "highlight": highlight, "after": after}


def parse_content(raw_content):
    """解析飞书正文内容"""
    pages = []
    sections = re.split(r'\n【', raw_content)

    for section in sections:
        if not section.strip():
            continue

        if not section.startswith('【'):
            section = '【' + section

        lines = section.strip().split('\n')
        first_line = lines[0]

        # 封面
        if first_line.startswith('【封面】'):
            cover_data = {'type': 'cover', 'zodiac': '射手座', 'topic': '占有欲解读'}
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('副标题:') or line.startswith('副标题：'):
                    cover_data['subtitle'] = line.split(':', 1)[1].strip().split('：', 1)[-1].strip()
                elif line.startswith('主标题第一行:') or line.startswith('主标题第一行：'):
                    cover_data['titleLine1'] = line.split(':', 1)[1].strip().split('：', 1)[-1].strip()
                elif line.startswith('主标题第二行:') or line.startswith('主标题第二行：'):
                    title2 = line.split(':', 1)[1].strip().split('：', 1)[-1].strip()
                    cover_data['titleLine2'] = re.sub(r'【([^】]+)】', r'\1', title2)
                elif line.startswith('点缀语:') or line.startswith('点缀语：'):
                    cover_data['tagline1'] = line.split(':', 1)[1].strip().split('：', 1)[-1].strip()
                    cover_data['tagline2Text'] = ''
                    cover_data['tagline2Highlight'] = ''
            pages.append(cover_data)

        # 内页
        elif re.match(r'【第(\d+)页】', first_line):
            match = re.match(r'【第(\d+)页】(.+)', first_line)
            page_num = match.group(1)
            section_title = match.group(2).strip()

            page_data = {
                'type': 'page',
                'zodiac': '射手座',
                'topic': '占有欲解读',
                'partNum': page_num.zfill(2),
                'sectionTitle': section_title,
                'content': [],
                'quote': ''
            }

            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('"') or line.startswith('"'):
                    page_data['quote'] = line.strip('"').strip('"').strip('"')
                else:
                    page_data['content'].append(parse_highlight(line))

            pages.append(page_data)

        # 结尾
        elif first_line.startswith('【结尾】'):
            match = re.match(r'【结尾】(.+)', first_line)
            section_title = match.group(1).strip() if match else '写给射手'

            summary_data = {
                'type': 'summary',
                'zodiac': '射手座',
                'topic': '占有欲解读',
                'sectionTitle': section_title,
                'content': [],
                'endingLine1': '',
                'endingLine2': ''
            }

            content_lines = []
            ending_lines = []
            in_ending = False

            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('愿'):
                    in_ending = True
                if in_ending:
                    ending_lines.append(line)
                else:
                    content_lines.append(parse_highlight(line))

            summary_data['content'] = content_lines
            if len(ending_lines) >= 2:
                summary_data['endingLine1'] = ending_lines[0]
                summary_data['endingLine2'] = ending_lines[1]
            elif len(ending_lines) == 1:
                summary_data['endingLine1'] = ending_lines[0]

            pages.append(summary_data)

    return pages


def generate_posters(raw_content, output_dir):
    """生成套图"""
    os.makedirs(output_dir, exist_ok=True)
    pages = parse_content(raw_content)
    print(f"解析到 {len(pages)} 个页面")

    generated_files = []
    page_index = 1

    for page in pages:
        page_type = page.pop('type')

        if page_type == 'cover':
            template = os.path.join(TEMPLATE_DIR, 'cover.html')
            output_name = f"{page_index:02d}_封面.png"
        elif page_type == 'page':
            template = os.path.join(TEMPLATE_DIR, 'page.html')
            section_title = page.get('sectionTitle', 'page')
            output_name = f"{page_index:02d}_{section_title}.png"
        elif page_type == 'summary':
            template = os.path.join(TEMPLATE_DIR, 'summary.html')
            output_name = f"{page_index:02d}_结尾.png"
        else:
            continue

        page['pageNum'] = f"0 {page_index}"
        output_path = os.path.join(output_dir, output_name)
        print(f"[{page_index}] 生成 {output_name}...")

        try:
            render_template_to_png(template, output_path, page)
            size_kb = os.path.getsize(output_path) // 1024
            print(f"    ✓ 完成 ({size_kb}KB)")
            generated_files.append(output_path)
        except Exception as e:
            print(f"    ✗ 失败: {e}")

        page_index += 1

    return generated_files


def upload_to_feishu(token, files, record_id, output_dir):
    """上传图片到飞书"""
    file_tokens = []

    for filepath in files:
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)

        print(f"上传 {filename}...")
        with open(filepath, 'rb') as f:
            resp = requests.post(
                "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": (filename, f, "image/png")},
                data={
                    "file_name": filename,
                    "parent_type": "bitable_file",
                    "parent_node": APP_TOKEN,
                    "size": str(file_size)
                }
            )

        result = resp.json()
        if result.get("code") == 0:
            ft = result["data"]["file_token"]
            file_tokens.append({"file_token": ft})
            print(f"    ✓ {ft}")
        else:
            print(f"    ✗ {result}")

    # 更新记录
    if file_tokens:
        print(f"\n更新飞书记录...")
        requests.put(
            f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "fields": {
                    "生成图片": file_tokens,
                    "生成图片路径": output_dir,
                    "已生成": True
                }
            }
        )

    return file_tokens


def publish_to_xiaohongshu(images, xhs_title, xhs_content):
    """发布到小红书"""
    url = "http://localhost:18060/mcp"
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}

    # 初始化
    resp = requests.post(url, json={
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}
    }, headers=headers, timeout=30)

    session_id = resp.headers.get("Mcp-Session-Id")
    headers["Mcp-Session-Id"] = session_id

    requests.post(url, json={"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}, headers=headers, timeout=30)

    # 检查登录
    resp = requests.post(url, json={
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "check_login_status", "arguments": {}}
    }, headers=headers, timeout=60)

    if "已登录" not in str(resp.json()):
        print("❌ 未登录小红书")
        return False

    print("✓ 已登录小红书")

    # 发布
    print("开始发布...")
    resp = requests.post(url, json={
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {
            "name": "publish_content",
            "arguments": {"title": xhs_title, "content": xhs_content, "images": images, "tags": ["射手座", "星座", "占有欲", "星座性格"]}
        }
    }, headers=headers, timeout=180)

    result = resp.json()
    print(f"发布结果: {json.dumps(result, ensure_ascii=False)[:200]}...")
    return "发布成功" in str(result) or "发布完成" in str(result)


# ========== 主流程 ==========
print("=" * 50)
print("射手座的占有欲有多强 - 生成并发布")
print("=" * 50)

# 1. 获取记录
print("\n[1] 获取飞书记录...")
token = get_feishu_token()

search_resp = requests.post(
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"filter": {"conjunction": "and", "conditions": [{"field_name": "标题", "operator": "contains", "value": ["射手座的占有欲有多强"]}]}}
)

items = search_resp.json().get("data", {}).get("items", [])
if not items:
    print("❌ 未找到记录")
    exit(1)

record = items[0]
record_id = record["record_id"]
fields = record["fields"]
raw_content = fields["正文内容"][0]["text"] if isinstance(fields["正文内容"], list) else fields["正文内容"]

print(f"记录 ID: {record_id}")
print(f"标题: {fields['标题'][0]['text'] if isinstance(fields['标题'], list) else fields['标题']}")

# 2. 生成套图
print("\n[2] 生成套图...")
output_dir = os.path.join(OUTPUT_BASE, "占有欲")
generated_files = generate_posters(raw_content, output_dir)

if not generated_files:
    print("❌ 生成失败")
    exit(1)

print(f"\n共生成 {len(generated_files)} 张图片")

# 3. 上传到飞书
print("\n[3] 上传到飞书...")
upload_to_feishu(token, generated_files, record_id, output_dir)

# 4. 发布小红书
print("\n[4] 发布小红书...")
xhs_title = "射手座的占有欲有多强"
xhs_content = """射手座的占有欲，你真的了解吗？

🔥 表面洒脱
嘴上说无所谓
心里却把你当成唯一

👀 默默关注
不会天天黏着你
但你的动态一条不落

😤 吃醋方式
不会直接说吃醋
而是突然变得安静

💕 占有信号
开始介意你和谁聊天
开始在意你的行踪

🎯 认定之后
一旦认定你是我的人
就容不得任何暧昧

射手的占有欲
藏在洒脱的外表下
爱上了 就想独占 💫

#射手座 #星座 #占有欲 #星座性格"""

if publish_to_xiaohongshu(generated_files, xhs_title, xhs_content):
    # 更新飞书已发布
    requests.put(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"fields": {"已发布": True, "小红书文案": xhs_content}}
    )
    print("\n✅ 全部完成!")
else:
    print("\n⚠️ 发布可能未成功")
