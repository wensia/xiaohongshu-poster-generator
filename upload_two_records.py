#!/usr/bin/env python3
"""上传两条记录的图片到飞书多维表格"""
import os
import requests
from pathlib import Path

# Configuration
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
BITABLE_APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
BASE_DIR = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/03")

# 只上传这两条记录
RECORDS = {
    "双子座-被束缚": "recv7ehAQPl6gX",
    "双子座-温柔": "recv7ehBimKrGw",
}

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json()["tenant_access_token"]

def upload_file(token, file_path):
    """Upload file to Feishu and return file_token"""
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        files = {
            "file": (file_name, f, "image/png"),
        }
        data = {
            "file_name": file_name,
            "parent_type": "bitable_file",
            "parent_node": BITABLE_APP_TOKEN,
            "size": str(file_size),
        }
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(url, headers=headers, files=files, data=data)

    result = resp.json()
    if result.get("code") == 0:
        return result["data"]["file_token"]
    else:
        print(f"Error uploading {file_name}: {result}")
        return None

def update_record(token, record_id, file_tokens):
    """Update bitable record with file attachments"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BITABLE_APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"

    attachments = [{"file_token": ft} for ft in file_tokens if ft]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "生成图片": attachments
        }
    }
    resp = requests.put(url, headers=headers, json=data)
    return resp.json()

def main():
    print("Getting access token...")
    token = get_tenant_access_token()
    print(f"Token obtained: {token[:20]}...")

    for folder_name, record_id in RECORDS.items():
        folder_path = BASE_DIR / folder_name
        print(f"\n{'='*50}")
        print(f"Processing: {folder_name}")
        print(f"{'='*50}")

        # Find PNG files and sort them properly
        png_files = sorted(folder_path.glob("*.png"))
        if not png_files:
            print(f"No PNG files found in {folder_path}")
            continue

        # Order files: cover first, then pages
        ordered_files = []
        for png in png_files:
            if "cover" in png.name.lower():
                ordered_files.insert(0, png)
            else:
                ordered_files.append(png)

        print(f"Found {len(ordered_files)} files")

        # Upload each file
        file_tokens = []
        for png_path in ordered_files:
            print(f"  Uploading {png_path.name}...", end=" ")
            file_token = upload_file(token, str(png_path))
            if file_token:
                file_tokens.append(file_token)
                print(f"OK")
            else:
                print(f"FAILED")

        # Update record
        if file_tokens:
            print(f"\nUpdating record with {len(file_tokens)} files...")
            result = update_record(token, record_id, file_tokens)
            if result.get("code") == 0:
                print(f"Success!")
            else:
                print(f"Error: {result}")

    print(f"\n{'='*50}")
    print("All uploads complete!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
