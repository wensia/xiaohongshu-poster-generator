#!/usr/bin/env python3
"""
从飞书记录生成套图并上传
"""

import os
import re
import sys
import json
import requests

# 添加工具库路径
sys.path.insert(0, '/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster')
from utils.screenshot import render_template_to_png, batch_render_templates

# 配置
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"

TEMPLATE_DIR = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster/assets/templates/personality-monologue"
OUTPUT_BASE = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output"


def get_feishu_token():
    """获取飞书 access token"""
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    return resp.json()["tenant_access_token"]


def parse_highlight(text):
    """
    解析高亮词【】，返回结构化数据
    输入: "三分钟热度是【天性】"
    输出: {"before": "三分钟热度是", "highlight": "天性", "after": ""}
    """
    match = re.search(r'【([^】]+)】', text)
    if not match:
        return text  # 无高亮，返回纯字符串

    before = text[:match.start()]
    highlight = match.group(1)
    after = text[match.end():]

    # 检查 after 中是否还有高亮
    after_match = re.search(r'【([^】]+)】', after)
    if after_match:
        # 有两个高亮词
        after_before = after[:after_match.start()]
        after_highlight = after_match.group(1)
        after_after = after[after_match.end():]
        return {
            "before": before,
            "highlight": highlight,
            "after": after_before,
            "highlight2": after_highlight,
            "after2": after_after
        }

    return {"before": before, "highlight": highlight, "after": after}


def parse_content(raw_content):
    """
    解析飞书正文内容，返回页面数据列表
    """
    pages = []
    sections = re.split(r'\n【', raw_content)

    for section in sections:
        if not section.strip():
            continue

        # 恢复【开头
        if not section.startswith('【'):
            section = '【' + section

        lines = section.strip().split('\n')
        first_line = lines[0]

        # 解析封面
        if first_line.startswith('【封面】'):
            cover_data = {
                'type': 'cover',
                'zodiac': '射手座',
                'topic': '成长课题'
            }
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('副标题:') or line.startswith('副标题：'):
                    cover_data['subtitle'] = line.split(':', 1)[1].strip().split('：', 1)[-1].strip()
                elif line.startswith('主标题第一行:') or line.startswith('主标题第一行：'):
                    cover_data['titleLine1'] = line.split(':', 1)[1].strip().split('：', 1)[-1].strip()
                elif line.startswith('主标题第二行:') or line.startswith('主标题第二行：'):
                    title2 = line.split(':', 1)[1].strip().split('：', 1)[-1].strip()
                    # 移除高亮标记用于显示
                    cover_data['titleLine2'] = re.sub(r'【([^】]+)】', r'\1', title2)
                elif line.startswith('点缀语:') or line.startswith('点缀语：'):
                    tagline = line.split(':', 1)[1].strip().split('：', 1)[-1].strip()
                    cover_data['tagline1'] = tagline
                    cover_data['tagline2Text'] = ''
                    cover_data['tagline2Highlight'] = ''
            pages.append(cover_data)

        # 解析内页
        elif re.match(r'【第(\d+)页】', first_line):
            match = re.match(r'【第(\d+)页】(.+)', first_line)
            page_num = match.group(1)
            section_title = match.group(2).strip()

            page_data = {
                'type': 'page',
                'zodiac': '射手座',
                'topic': '成长课题',
                'partNum': page_num.zfill(2),
                'sectionTitle': section_title,
                'content': [],
                'quote': ''
            }

            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                # 引用（带引号）
                if line.startswith('"') or line.startswith('"'):
                    page_data['quote'] = line.strip('"').strip('"').strip('"')
                else:
                    page_data['content'].append(parse_highlight(line))

            pages.append(page_data)

        # 解析结尾
        elif first_line.startswith('【结尾】'):
            match = re.match(r'【结尾】(.+)', first_line)
            section_title = match.group(1).strip() if match else '写给射手'

            summary_data = {
                'type': 'summary',
                'zodiac': '射手座',
                'topic': '成长课题',
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
                # 检测祝福语（通常以"愿"开头）
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


def generate_posters(record_id, raw_content, output_dir):
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
            page['pageNum'] = f"0 {page_index}"
        elif page_type == 'page':
            template = os.path.join(TEMPLATE_DIR, 'page.html')
            section_title = page.get('sectionTitle', 'page')
            output_name = f"{page_index:02d}_{section_title}.png"
            page['pageNum'] = f"0 {page_index}"
        elif page_type == 'summary':
            template = os.path.join(TEMPLATE_DIR, 'summary.html')
            output_name = f"{page_index:02d}_结尾.png"
            page['pageNum'] = f"0 {page_index}"
        else:
            continue

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


def upload_to_feishu(token, files, record_id):
    """上传图片到飞书并更新记录"""
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
            print(f"    ✗ 上传失败: {result}")

    # 更新记录
    if file_tokens:
        print(f"\n更新飞书记录 {record_id}...")
        update_resp = requests.put(
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
        print(f"更新结果: {update_resp.json().get('msg', update_resp.json())}")

    return file_tokens


if __name__ == "__main__":
    # 获取飞书 token
    print("获取飞书 Token...")
    token = get_feishu_token()

    # 搜索记录
    print("\n搜索飞书记录...")
    search_resp = requests.post(
        f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={
            "filter": {
                "conjunction": "and",
                "conditions": [
                    {"field_name": "标题", "operator": "contains", "value": ["射手座需要学会的课题"]},
                    {"field_name": "已生成", "operator": "is", "value": [False]}
                ]
            }
        }
    )

    data = search_resp.json()
    if data.get("code") != 0 or not data.get("data", {}).get("items"):
        print("未找到待生成的记录")
        # 尝试不带已生成过滤
        search_resp = requests.post(
            f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "filter": {
                    "conjunction": "and",
                    "conditions": [
                        {"field_name": "标题", "operator": "contains", "value": ["射手座需要学会的课题"]}
                    ]
                }
            }
        )
        data = search_resp.json()

    items = data.get("data", {}).get("items", [])
    if not items:
        print("未找到记录")
        exit(1)

    # 使用第一条未生成的记录，或第一条记录
    record = None
    for item in items:
        if not item["fields"].get("已生成"):
            record = item
            break
    if not record:
        record = items[0]

    record_id = record["record_id"]
    fields = record["fields"]

    title = fields["标题"][0]["text"] if isinstance(fields["标题"], list) else fields["标题"]
    raw_content = fields["正文内容"][0]["text"] if isinstance(fields["正文内容"], list) else fields["正文内容"]

    print(f"\n记录 ID: {record_id}")
    print(f"标题: {title}")
    print(f"已生成: {fields.get('已生成', False)}")

    # 创建输出目录
    output_dir = os.path.join(OUTPUT_BASE, "成长课题")

    # 生成套图
    print(f"\n开始生成套图...")
    print(f"输出目录: {output_dir}")

    generated_files = generate_posters(record_id, raw_content, output_dir)

    if generated_files:
        print(f"\n共生成 {len(generated_files)} 张图片")

        # 上传到飞书
        print("\n开始上传到飞书...")
        upload_to_feishu(token, generated_files, record_id)

        print("\n✅ 全部完成!")
    else:
        print("\n❌ 生成失败")
