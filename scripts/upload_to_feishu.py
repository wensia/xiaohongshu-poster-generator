#!/usr/bin/env python3
"""
上传图片到飞书并更新记录
"""
import os
import json
import requests

# 飞书配置
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"

# 结果文件
RESULTS_FILE = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/batch_results.json"


def get_access_token():
    """获取飞书 tenant access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    })
    return resp.json()["tenant_access_token"]


def upload_file(token: str, file_path: str) -> str:
    """上传文件到飞书，返回 file_token"""
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"

    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        files = {"file": (filename, f, "image/png")}
        data = {
            "file_name": filename,
            "parent_type": "bitable_file",
            "parent_node": APP_TOKEN,
            "size": str(file_size)
        }
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data
        )

    result = resp.json()
    if result.get("code") == 0:
        return result["data"]["file_token"]
    else:
        raise Exception(f"上传失败: {result}")


def update_record(token: str, record_id: str, file_tokens: list, output_dir: str):
    """更新飞书记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"

    data = {
        "fields": {
            "生成图片": [{"file_token": ft} for ft in file_tokens],
            "生成图片路径": output_dir,
            "已生成": True
        }
    }

    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json=data
    )

    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"更新记录失败: {result}")


def main():
    print("🚀 开始上传图片到飞书...\n")

    # 读取生成结果
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    # 获取 token
    token = get_access_token()
    print(f"✅ 获取 access token 成功\n")

    success_count = 0
    for result in results:
        record_id = result["record_id"]
        output_dir = result["output_dir"]
        png_files = result["png_files"]

        print(f"📤 上传记录 {record_id}...")

        try:
            # 上传所有图片
            file_tokens = []
            for png_file in png_files:
                filename = os.path.basename(png_file)
                print(f"   上传 {filename}...", end=" ")
                file_token = upload_file(token, png_file)
                file_tokens.append(file_token)
                print("✅")

            # 更新记录
            print(f"   更新记录...", end=" ")
            update_record(token, record_id, file_tokens, output_dir)
            print("✅")

            success_count += 1
            print(f"   ✨ 完成! 共上传 {len(file_tokens)} 张图片\n")

        except Exception as e:
            print(f"   ❌ 失败: {e}\n")

    print(f"\n🎉 完成! 成功处理 {success_count}/{len(results)} 条记录")


if __name__ == "__main__":
    main()
