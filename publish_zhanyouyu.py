#!/usr/bin/env python3
"""
发布"射手座的占有欲有多强"小红书笔记
"""

import os
import requests
import json
import base64

# 飞书配置
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"

def get_feishu_token():
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    return resp.json()["tenant_access_token"]

# 1. 获取飞书记录
print("获取飞书 Token...")
token = get_feishu_token()

print("\n搜索飞书记录...")
search_resp = requests.post(
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={
        "filter": {
            "conjunction": "and",
            "conditions": [
                {"field_name": "标题", "operator": "contains", "value": ["射手座的占有欲有多强"]}
            ]
        }
    }
)

data = search_resp.json()
items = data.get("data", {}).get("items", [])

if not items:
    print("未找到记录")
    exit(1)

# 找已生成图片的记录
record = None
for item in items:
    if item["fields"].get("已生成"):
        record = item
        break

if not record:
    print("未找到已生成图片的记录，使用第一条记录")
    record = items[0]

record_id = record["record_id"]
fields = record["fields"]

title = fields["标题"][0]["text"] if isinstance(fields["标题"], list) else fields["标题"]
image_path = fields.get("生成图片路径", [{}])
if isinstance(image_path, list):
    image_path = image_path[0].get("text", "") if image_path else ""

print(f"\n记录 ID: {record_id}")
print(f"标题: {title}")
print(f"图片路径: {image_path}")
print(f"已生成: {fields.get('已生成', False)}")
print(f"已发布: {fields.get('已发布', False)}")

# 检查图片是否存在
if not image_path or not os.path.exists(image_path):
    print(f"\n❌ 图片路径不存在: {image_path}")
    print("请先生成图片")
    exit(1)

# 2. 获取图片列表
images = sorted([
    os.path.join(image_path, f) for f in os.listdir(image_path)
    if f.endswith('.png')
])
print(f"\n图片列表 ({len(images)} 张):")
for img in images:
    print(f"  - {os.path.basename(img)}")

# 3. 根据正文内容生成小红书文案
raw_content = fields.get("正文内容", [{}])
if isinstance(raw_content, list):
    raw_content = raw_content[0].get("text", "") if raw_content else ""

xhs_title = "射手座的占有欲有多强"  # 最多20字
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

print(f"\n小红书标题: {xhs_title}")
print(f"小红书文案长度: {len(xhs_content)} 字")

# 4. 初始化 xiaohongshu-mcp
print("\n连接 xiaohongshu-mcp...")
url = "http://localhost:18060/mcp"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

try:
    resp = requests.post(url, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }, headers=headers, timeout=30)

    session_id = resp.headers.get("Mcp-Session-Id")
    headers["Mcp-Session-Id"] = session_id
    print(f"Session ID: {session_id}")

    # 发送 initialized 通知
    requests.post(url, json={
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {}
    }, headers=headers, timeout=30)

    # 5. 检查登录状态
    resp = requests.post(url, json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "check_login_status", "arguments": {}}
    }, headers=headers, timeout=60)

    login_result = resp.json()
    login_text = str(login_result)
    print(f"\n登录状态: {'已登录' if '已登录' in login_text else '未登录'}")

    if "已登录" in login_text:
        # 6. 发布笔记
        print("\n开始发布笔记...")
        resp = requests.post(url, json={
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "publish_content",
                "arguments": {
                    "title": xhs_title,
                    "content": xhs_content,
                    "images": images,
                    "tags": ["射手座", "星座", "占有欲", "星座性格"]
                }
            }
        }, headers=headers, timeout=180)

        publish_result = resp.json()
        print(f"\n发布结果: {json.dumps(publish_result, ensure_ascii=False, indent=2)}")

        result_text = str(publish_result)
        if "发布成功" in result_text or "发布完成" in result_text or "success" in result_text.lower():
            # 7. 更新飞书记录
            print("\n更新飞书记录...")
            update_resp = requests.put(
                f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={
                    "fields": {
                        "已发布": True,
                        "小红书文案": xhs_content
                    }
                }
            )
            print(f"飞书更新结果: {update_resp.json().get('msg', update_resp.json())}")
            print("\n✅ 全部完成!")
        else:
            print("\n⚠️ 发布可能未成功，请检查结果")
    else:
        print("\n❌ 未登录，需要先扫码登录")
        # 获取二维码
        resp = requests.post(url, json={
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "get_login_qrcode", "arguments": {}}
        }, headers=headers, timeout=60)
        qr_result = resp.json()

        # 保存二维码
        for content in qr_result.get("result", {}).get("content", []):
            if content.get("type") == "text":
                print(content.get("text"))
            elif content.get("type") == "image":
                img_data = content.get("data")
                img_bytes = base64.b64decode(img_data)
                qr_path = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/xiaohongshu_qrcode.png"
                with open(qr_path, "wb") as f:
                    f.write(img_bytes)
                print(f"\n二维码已保存: {qr_path}")
                os.system(f"open '{qr_path}'")

except requests.exceptions.ConnectionError:
    print("\n❌ 无法连接到 xiaohongshu-mcp，正在启动服务...")
    import subprocess
    subprocess.Popen(
        ["./xiaohongshu-mcp-darwin-arm64"],
        cwd="/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/xiaohongshu-mcp",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("服务已启动，请稍后重试")
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
