#!/usr/bin/env python3
import requests
import json

url = "http://localhost:18060/mcp"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

# 1. 初始化
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
print(f"Session ID: {session_id}")
headers["Mcp-Session-Id"] = session_id

# 2. 发送 initialized 通知
requests.post(url, json={
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
}, headers=headers, timeout=30)

# 3. 检查登录状态
resp = requests.post(url, json={
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {"name": "check_login_status", "arguments": {}}
}, headers=headers, timeout=60)

result = resp.json()
print("登录状态:", json.dumps(result, ensure_ascii=False, indent=2))

if "未登录" in str(result):
    # 4. 获取二维码
    resp = requests.post(url, json={
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "get_login_qrcode", "arguments": {}}
    }, headers=headers, timeout=60)

    result = resp.json()
    print("二维码:", json.dumps(result, ensure_ascii=False, indent=2))
