#!/usr/bin/env python3
"""
上传修正后的图片到飞书并更新记录
"""
import os
import requests
from pathlib import Path

# 飞书配置
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

# 记录映射
RECORDS = [
    {"record_id": "recv7JnxRujrK7", "name": "射手遇到白羊", "dir": "射手遇到白羊"},
    {"record_id": "recv7JnyfI61HU", "name": "射手遇到金牛", "dir": "射手遇到金牛"},
    {"record_id": "recv7JnyHB1dfF", "name": "射手遇到巨蟹", "dir": "射手遇到巨蟹"},
    {"record_id": "recv7Jnz6ut3mQ", "name": "射手遇到处女", "dir": "射手遇到处女"},
    {"record_id": "recv7JnzvfApUC", "name": "射手遇到天秤", "dir": "射手遇到天秤"},
]

def get_access_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    })
    return resp.json()["tenant_access_token"]

def upload_image(token: str, image_path: Path) -> str:
    """上传图片到飞书，返回 file_token"""
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
    file_size = image_path.stat().st_size

    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/png")}
        data = {
            "file_name": image_path.name,
            "parent_type": "bitable_file",
            "parent_node": APP_TOKEN,
            "size": str(file_size)
        }
        resp = requests.post(url, headers={"Authorization": f"Bearer {token}"}, files=files, data=data)
        result = resp.json()
        if result.get("code") != 0:
            print(f"  上传失败: {result}")
            return None
        return result["data"]["file_token"]

def update_record(token: str, record_id: str, file_tokens: list, image_path: str):
    """更新飞书多维表格记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "生成图片": [{"file_token": ft} for ft in file_tokens],
            "生成图片路径": image_path,
            "已生成": True
        }
    }
    resp = requests.put(url, headers=headers, json=data)
    return resp.json()

def main():
    base_dir = Path("/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09")

    print("获取飞书 access token...")
    token = get_access_token()
    print("Token 获取成功\n")

    for record in RECORDS:
        output_dir = base_dir / record["dir"]
        png_files = sorted(output_dir.glob("*.png"))

        print(f"处理: {record['name']} ({record['record_id']})")
        print(f"   目录: {output_dir}")

        file_tokens = []
        for png_file in png_files:
            print(f"   上传: {png_file.name}...", end=" ")
            ft = upload_image(token, png_file)
            if ft:
                file_tokens.append(ft)
                print(f"-> {ft[:10]}...")

        if file_tokens:
            print(f"   更新记录...")
            result = update_record(token, record["record_id"], file_tokens, str(output_dir))
            if result.get("code") == 0:
                print(f"   记录更新成功! 共 {len(file_tokens)} 张图片")
            else:
                print(f"   记录更新失败: {result}")
        print()

    print("全部完成!")

if __name__ == "__main__":
    main()
