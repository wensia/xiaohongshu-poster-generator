#!/usr/bin/env python3
"""Re-upload 射手遇到双鱼 PNG files to Feishu."""

import os
import requests

# Feishu credentials
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
RECORD_ID = "recv7JnB7dSbcX"

BASE_DIR = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09/射手遇到双鱼"


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Failed to get token: {data}")
    return data["tenant_access_token"]


def upload_file(token, file_path):
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        files = {"file": (file_name, f, "image/png")}
        data = {
            "file_name": file_name,
            "parent_type": "bitable_file",
            "parent_node": APP_TOKEN,
            "size": str(file_size),
        }
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(url, headers=headers, files=files, data=data)

    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Upload failed: {result}")
    return result["data"]["file_token"]


def update_record(token, file_tokens):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{RECORD_ID}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    attachments = [{"file_token": ft} for ft in file_tokens]
    data = {"fields": {"生成图片": attachments, "已生成": True}}

    resp = requests.put(url, headers=headers, json=data)
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Update failed: {result}")
    return result


def main():
    print("Getting token...")
    token = get_tenant_access_token()

    # PNG files in order
    png_files = [
        "01_cover.png", "02_page.png", "03_page.png", "04_page.png",
        "05_page.png", "06_page.png", "07_end.png"
    ]

    print("Uploading 7 PNG files...")
    file_tokens = []
    for f in png_files:
        path = os.path.join(BASE_DIR, f)
        size = os.path.getsize(path)
        print(f"  {f}: {size:,} bytes")
        ft = upload_file(token, path)
        file_tokens.append(ft)
        print(f"    -> {ft}")

    print(f"\nUpdating record {RECORD_ID}...")
    update_record(token, file_tokens)
    print("SUCCESS: Record updated!")


if __name__ == "__main__":
    main()
