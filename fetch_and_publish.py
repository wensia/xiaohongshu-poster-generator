#!/usr/bin/env python3
import requests
import json
import os

# 飞书配置
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"

# 1. 获取飞书 token
token_resp = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": APP_ID, "app_secret": APP_SECRET}
)
feishu_token = token_resp.json()["tenant_access_token"]
print(f"飞书 Token: {feishu_token[:20]}...")

# 2. 搜索记录
search_resp = requests.post(
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search",
    headers={"Authorization": f"Bearer {feishu_token}", "Content-Type": "application/json"},
    json={
        "filter": {
            "conjunction": "and",
            "conditions": [
                {"field_name": "标题", "operator": "contains", "value": ["射手座的隐藏技能"]}
            ]
        }
    }
)

records = search_resp.json()["data"]["items"]
print(f"\n找到 {len(records)} 条记录")

# 找到已生成图片的记录
target_record = None
for r in records:
    fields = r["fields"]
    if fields.get("已生成") == True:
        target_record = r
        break

if not target_record:
    print("未找到已生成图片的记录")
    exit(1)

record_id = target_record["record_id"]
fields = target_record["fields"]

# 提取信息
title_text = fields["标题"][0]["text"] if isinstance(fields["标题"], list) else fields["标题"]
subtitle_text = fields["副标题"][0]["text"] if isinstance(fields["副标题"], list) else fields["副标题"]
content_text = fields["正文内容"][0]["text"] if isinstance(fields["正文内容"], list) else fields["正文内容"]
image_path = fields["生成图片路径"][0]["text"] if isinstance(fields["生成图片路径"], list) else fields["生成图片路径"]

print(f"\n记录 ID: {record_id}")
print(f"标题: {title_text}")
print(f"副标题: {subtitle_text}")
print(f"图片路径: {image_path}")

# 3. 获取图片列表
images = sorted([
    os.path.join(image_path, f) for f in os.listdir(image_path)
    if f.endswith('.png')
])
print(f"\n图片列表 ({len(images)} 张):")
for img in images:
    print(f"  - {os.path.basename(img)}")

# 4. 生成小红书文案
xhs_title = "射手座的隐藏技能"  # 最多20字
xhs_content = """射手座的隐藏技能，你知道几个？

🎯 察言观色
看似大大咧咧，其实什么都看在眼里
只是懒得说破而已

📚 快速学习
对感兴趣的东西学得超快
三分钟热度但效率惊人

🎤 临场发挥
没准备也能侃侃而谈
越是紧急越淡定

🔮 读心术
一眼就能看穿你的心思
但装作不知道

💪 自愈能力
受伤了自己舔伤口
给点时间就能恢复

射手的隐藏技能是底牌
关键时刻才亮出来
低调也是一种高级 ✨

#射手座 #星座 #隐藏技能 #星座性格"""

print(f"\n小红书标题: {xhs_title}")
print(f"小红书文案:\n{xhs_content[:100]}...")

# 5. 初始化 xiaohongshu-mcp
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
    print(f"\nMCP Session: {session_id}")

    # 发送 initialized 通知
    requests.post(url, json={
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {}
    }, headers=headers, timeout=30)

    # 6. 检查登录状态
    resp = requests.post(url, json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "check_login_status", "arguments": {}}
    }, headers=headers, timeout=60)

    login_result = resp.json()
    print(f"\n登录状态: {json.dumps(login_result, ensure_ascii=False)}")

    if "已登录" in str(login_result):
        # 7. 发布笔记
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
                    "tags": ["射手座", "星座", "隐藏技能"]
                }
            }
        }, headers=headers, timeout=180)

        publish_result = resp.json()
        print(f"\n发布结果: {json.dumps(publish_result, ensure_ascii=False, indent=2)}")

        if "发布成功" in str(publish_result) or "发布完成" in str(publish_result) or "success" in str(publish_result).lower():
            # 8. 更新飞书记录
            print("\n更新飞书记录...")
            update_resp = requests.put(
                f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}",
                headers={"Authorization": f"Bearer {feishu_token}", "Content-Type": "application/json"},
                json={
                    "fields": {
                        "已发布": True,
                        "小红书文案": xhs_content
                    }
                }
            )
            print(f"飞书更新结果: {update_resp.json()}")
            print("\n✅ 全部完成！")
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
        print(f"二维码信息: {json.dumps(qr_result, ensure_ascii=False)[:200]}...")

except requests.exceptions.ConnectionError:
    print("\n❌ 无法连接到 xiaohongshu-mcp，请先启动服务")
except Exception as e:
    print(f"\n❌ 错误: {e}")
