#!/usr/bin/env python3
"""
将模板示例SVG转换为PNG并上传到飞书模板库
"""

import os
import glob
import requests
from playwright.sync_api import sync_playwright

# 飞书配置
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tbl4FKgtMDv3HCWP"

# 模板记录映射
TEMPLATE_RECORDS = {
    "destined-bond": "recv7DuTaqiyKN",
    "cosmic-gravity": "recv7DuTN63n8P"
}

# 模板目录
TEMPLATES_DIR = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/zodiac-poster/assets/templates"


def get_tenant_access_token():
    """获取飞书租户访问令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json()["tenant_access_token"]


def svg_to_png(svg_path, png_path):
    """使用Playwright将SVG转换为PNG"""
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; }}
            body {{ width: 1080px; height: 1440px; background: transparent; }}
        </style>
    </head>
    <body>{svg_content}</body>
    </html>
    '''

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1440})
        page.set_content(html)
        page.wait_for_timeout(2500)  # 等待字体加载
        page.screenshot(path=png_path)
        browser.close()

    print(f"  转换完成: {png_path}")


def upload_to_feishu(file_path, token):
    """上传文件到飞书"""
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    upload_url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"

    with open(file_path, "rb") as f:
        files = {"file": (filename, f, "image/png")}
        data = {
            "file_name": filename,
            "parent_type": "bitable_file",
            "parent_node": APP_TOKEN,
            "size": str(file_size)
        }
        resp = requests.post(
            upload_url,
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data
        )

    result = resp.json()
    if result.get("code") == 0:
        file_token = result["data"]["file_token"]
        print(f"  上传成功: {filename} -> {file_token}")
        return file_token
    else:
        print(f"  上传失败: {filename} - {result}")
        return None


def update_record(record_id, file_tokens, token):
    """更新飞书记录的示例图字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"

    attachments = [{"file_token": ft} for ft in file_tokens if ft]

    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "fields": {
                "示例图": attachments
            }
        }
    )

    result = resp.json()
    if result.get("code") == 0:
        print(f"  记录更新成功: {record_id}")
        return True
    else:
        print(f"  记录更新失败: {result}")
        return False


def process_template(template_id, token):
    """处理单个模板的转换和上传"""
    print(f"\n处理模板: {template_id}")

    examples_dir = os.path.join(TEMPLATES_DIR, template_id, "examples")
    svg_files = sorted(glob.glob(os.path.join(examples_dir, "*.svg")))

    if not svg_files:
        print(f"  未找到SVG文件")
        return

    file_tokens = []

    for svg_path in svg_files:
        # 转换SVG为PNG
        png_path = svg_path.replace(".svg", ".png")
        print(f"  转换: {os.path.basename(svg_path)}")
        svg_to_png(svg_path, png_path)

        # 上传到飞书
        file_token = upload_to_feishu(png_path, token)
        if file_token:
            file_tokens.append(file_token)

    # 更新记录
    if file_tokens and template_id in TEMPLATE_RECORDS:
        record_id = TEMPLATE_RECORDS[template_id]
        update_record(record_id, file_tokens, token)


def main():
    print("=" * 50)
    print("模板示例图生成与上传工具")
    print("=" * 50)

    # 获取访问令牌
    print("\n获取飞书访问令牌...")
    token = get_tenant_access_token()
    print(f"  令牌获取成功")

    # 处理每个模板
    for template_id in TEMPLATE_RECORDS.keys():
        process_template(template_id, token)

    print("\n" + "=" * 50)
    print("处理完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
