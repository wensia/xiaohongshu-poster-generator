#!/usr/bin/env python3
"""
准备小红书发布内容
从飞书拉取记录，格式化为小红书发布格式
"""
import json
import sys
import requests
from pathlib import Path

# 飞书配置
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

def get_access_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json().get("tenant_access_token")

def search_record(title: str):
    """搜索飞书记录"""
    token = get_access_token()
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "filter": {
            "conjunction": "and",
            "conditions": [
                {"field_name": "标题", "operator": "is", "value": [title]}
            ]
        }
    }
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()

    if result.get("data", {}).get("items"):
        return result["data"]["items"][0]
    return None

def format_for_xiaohongshu(record: dict) -> dict:
    """格式化为小红书发布格式"""
    fields = record.get("fields", {})

    # 提取字段
    title = fields.get("标题", [{}])[0].get("text", "") if fields.get("标题") else ""
    subtitle = fields.get("副标题", [{}])[0].get("text", "") if fields.get("副标题") else ""
    content = fields.get("正文内容", [{}])[0].get("text", "") if fields.get("正文内容") else ""
    zodiac = fields.get("星座", "")
    image_path = fields.get("生成图片路径", [{}])[0].get("text", "") if fields.get("生成图片路径") else ""

    # 提取星座名（从标题中）
    zodiac1 = ""
    zodiac2 = ""
    if "遇到" in title:
        parts = title.split("遇到")
        zodiac1 = parts[0] + "座"
        zodiac2 = parts[1] + "座" if len(parts) > 1 else ""

    # 构建小红书文案
    xhs_content = f"{subtitle}会怎样？\n\n{content}"

    # 话题标签
    tags = ["星座", "星座配对", "命定之约"]
    if zodiac1:
        tags.insert(0, zodiac1)
    if zodiac2:
        tags.insert(1, zodiac2)

    # 获取图片列表
    images = []
    if image_path:
        image_dir = Path(image_path)
        if image_dir.exists():
            images = sorted([str(p) for p in image_dir.glob("*.png")])

    return {
        "title": title,
        "content": xhs_content,
        "tags": tags,
        "images": images,
        "record_id": record.get("record_id", "")
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python prepare_content.py <标题>")
        print("示例: python prepare_content.py 射手遇到巨蟹")
        sys.exit(1)

    title = sys.argv[1]
    print(f"搜索记录: {title}")

    record = search_record(title)
    if not record:
        print(f"未找到记录: {title}")
        sys.exit(1)

    result = format_for_xiaohongshu(record)

    # 输出 JSON 格式
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
