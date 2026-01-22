#!/usr/bin/env python3
import requests
import json
import base64

url = "http://localhost:18060/mcp"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

# 初始化
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

# 发送 initialized 通知
requests.post(url, json={
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
}, headers=headers, timeout=30)

# 获取二维码
resp = requests.post(url, json={
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {"name": "get_login_qrcode", "arguments": {}}
}, headers=headers, timeout=60)

result = resp.json()

# 提取二维码图片
for content in result.get("result", {}).get("content", []):
    if content.get("type") == "text":
        print(content.get("text"))
    elif content.get("type") == "image":
        img_data = content.get("data")
        img_bytes = base64.b64decode(img_data)
        qr_path = "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/xiaohongshu_qrcode.png"
        with open(qr_path, "wb") as f:
            f.write(img_bytes)
        print(f"\n二维码已保存到: {qr_path}")
        print("请用小红书 App 扫描二维码登录")
