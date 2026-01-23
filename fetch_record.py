#!/usr/bin/env python3
import requests
import json

# 飞书配置
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID = "tblyDtUqcfFMaDfO"
APP_ID = "cli_a9a7190fef38dbb5"
APP_SECRET = "CyANTKyK1HhZ569m9vasodAGqsjKwh1u"

# 获取 token
token_resp = requests.post(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": APP_ID, "app_secret": APP_SECRET}
)
token = token_resp.json()["tenant_access_token"]

# 搜索记录
search_resp = requests.post(
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/search",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={
        "filter": {
            "conjunction": "and",
            "conditions": [
                {"field_name": "标题", "operator": "contains", "value": ["射手座需要学会的课题"]}
            ]
        }
    }
)

data = search_resp.json()
print(json.dumps(data, ensure_ascii=False, indent=2))
