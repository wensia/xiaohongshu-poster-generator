#!/usr/bin/env python3
"""Upload PNG files to Feishu and update records."""

import os
import requests
import json

# Feishu credentials
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

# Records to update
RECORDS = {
    "射手遇到射手": "recv7JnzUE6bIV",
    "射手遇到摩羯": "recv7JnAjeTj6s",
    "射手遇到水瓶": "recv7JnAJaLx8y",
    "射手遇到双鱼": "recv7JnB7dSbcX",
}

BASE_DIR = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09"


def get_tenant_access_token():
    """Get tenant access token from Feishu."""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Failed to get token: {data}")
    return data["tenant_access_token"]


def upload_file(token, file_path):
    """Upload a file to Feishu and return file_token."""
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
        raise Exception(f"Upload failed for {file_name}: {result}")
    file_token = result["data"]["file_token"]
    print(f"    Full token: {file_token}")
    return file_token


def update_record(token, record_id, file_tokens):
    """Update Feishu Bitable record with file attachments."""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Prepare attachment field with file tokens
    attachments = [{"file_token": ft} for ft in file_tokens]

    data = {
        "fields": {
            "生成图片": attachments,
            "已生成": True,
        }
    }

    resp = requests.put(url, headers=headers, json=data)
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"Update record failed: {result}")
    return result


def main():
    print("Getting tenant access token...")
    token = get_tenant_access_token()
    print(f"Token obtained successfully")

    for title, record_id in RECORDS.items():
        print(f"\n{'='*50}")
        print(f"Processing: {title}")
        print(f"{'='*50}")
        dir_path = os.path.join(BASE_DIR, title)

        # Get PNG files in order
        png_files = []
        for i in range(1, 8):
            if i == 1:
                filename = f"0{i}_cover.png"
            elif i == 7:
                filename = f"0{i}_end.png"
            else:
                filename = f"0{i}_page.png"

            file_path = os.path.join(dir_path, filename)
            if os.path.exists(file_path):
                png_files.append(file_path)

        if len(png_files) != 7:
            print(f"ERROR: Expected 7 files, found {len(png_files)}")
            continue

        # Upload files and collect tokens
        print(f"Uploading {len(png_files)} files...")
        file_tokens = []
        for file_path in png_files:
            try:
                print(f"  Uploading: {os.path.basename(file_path)}")
                ft = upload_file(token, file_path)
                file_tokens.append(ft)
            except Exception as e:
                print(f"  FAILED: {e}")
                break

        if len(file_tokens) != 7:
            print(f"ERROR: Only uploaded {len(file_tokens)} files")
            continue

        # Update record
        print(f"Updating record {record_id}...")
        try:
            update_record(token, record_id, file_tokens)
            print(f"SUCCESS: Record updated with 7 images!")
        except Exception as e:
            print(f"ERROR: {e}")

    print(f"\n{'='*50}")
    print("All done!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
