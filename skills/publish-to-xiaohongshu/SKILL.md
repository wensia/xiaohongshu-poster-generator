---
name: publish-to-xiaohongshu
description: '使用 xiaohongshu-mcp 将内容发布到小红书（图文或视频笔记），发布成功后自动通过飞书 API 将飞书多维表格中对应记录的「已发布」字段标记为 true。支持单条发布和批量发布（过滤已生成未发布记录）。当用户需要将内容发布到小红书平台、发小红书笔记、社交媒体发布、内容发帖，或需要同步飞书多维表格发布状态时使用。Use when: 用户发出"发布小红书"、"发布到小红书"、"/publish-xhs"、"/publish"、"发布笔记"、"同步发布状态"等指令时触发。'
triggers: ["/publish-xhs", "/发布小红书", "/publish"]
---

# 小红书发布器（xiaohongshu-mcp）

使用 `xiaohongshu-mcp` 工具发布内容到小红书，发布成功后自动标记飞书多维表格的「已发布」字段。

---

## 核心工具

| 工具名 | 功能 | 必需参数 |
|--------|------|----------|
| `mcp__xiaohongshu-mcp__check_login_status` | 检查登录状态 | 无 |
| `mcp__xiaohongshu-mcp__publish_content` | 发布图文 | title, content, images |
| `mcp__xiaohongshu-mcp__publish_with_video` | 发布视频 | title, content, video |

---

## 飞书配置

```
app_token: Qt6Qbzzy6aWBgassGQhcUU5vngc
table_id:  tblyDtUqcfFMaDfO
app_id:    cli_a9a7190fef38dbb5
```

### 关键字段

| 字段 | 说明 |
|------|------|
| 标题 | 海报标题 |
| 正文内容 | 套图正文（用于生成小红书文案） |
| 小红书文案 | 预设的发布文案（优先使用） |
| 生成图片路径 | 本地图片目录路径 |
| 已生成 | 图片是否已生成 |
| **已发布** | **发布成功后必须标记为 true** |

---

## 发布流程（5 步）

### 步骤 1: 检查登录状态

```
调用: mcp__xiaohongshu-mcp__check_login_status
```

如果未登录，提示用户运行：
```bash
cd /Users/panyuhang/我的项目/编程/脚本/小红书封面生成/xiaohongshu-mcp
./xiaohongshu-login-darwin-arm64
```

### 步骤 2: 从飞书获取记录

> 获取 token 的方式在步骤 5 中复用，建议封装为函数。

```python
import requests

def get_feishu_token():
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": "cli_a9a7190fef38dbb5", "app_secret": "<从环境变量或配置读取>"}
    )
    return resp.json()["tenant_access_token"]

token = get_feishu_token()

# 查询记录（按标题过滤）
resp = requests.post(
    "https://open.feishu.cn/open-apis/bitable/v1/apps/Qt6Qbzzy6aWBgassGQhcUU5vngc/tables/tblyDtUqcfFMaDfO/records/search",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={
        "filter": {
            "conjunction": "and",
            "conditions": [{"field_name": "标题", "operator": "contains", "value": ["<用户指定的标题>"]}]
        }
    }
)
record = resp.json()["data"]["items"][0]
record_id = record["record_id"]  # ⚠️ 必须保存，用于步骤 5
```

**批量发布时**，将 filter 改为 `已生成=true AND 已发布=false`，获取所有待发布记录列表。

### 步骤 3: 准备发布内容

- **标题**（≤20字）：直接使用记录标题，或提炼核心卖点
- **正文**（100-200字）：优先使用「小红书文案」字段；若为空，AI 根据「正文内容」生成（口语化、短句、个人视角）
- **图片**：从「生成图片路径」读取，使用本地绝对路径
- **话题标签**（3-5个）：必选星座名、"星座"、"12星座"；按主题追加

> 详细文案生成规则、话题标签分类及模板见 `skills/publish-to-xiaohongshu/COPYWRITING.md`。

### 步骤 4: 发布到小红书

```
调用: mcp__xiaohongshu-mcp__publish_content
参数:
- title:   "射手座的发疯文学语录"           # ≤20字
- content: "发疯是一种解压方式..."           # 正文
- images:  ["/path/to/01.png", ...]        # 本地绝对路径
- tags:    ["射手座", "星座", "发疯文学"]   # 可选
```

✅ **验证点**：确认工具返回成功状态后，再进入步骤 5。若发布失败，记录错误原因，不更新飞书，继续下一条（批量场景）。

### 步骤 5: ⚠️ 【必须】标记飞书记录已发布

**发布成功后立即执行，复用步骤 2 的 `get_feishu_token()` 函数。**

```python
APP_TOKEN = "Qt6Qbzzy6aWBgassGQhcUU5vngc"
TABLE_ID  = "tblyDtUqcfFMaDfO"
RECORD_ID = "<步骤 2 保存的 record_id>"

token = get_feishu_token()
resp = requests.put(
    f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{RECORD_ID}",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"fields": {"已发布": True}}
)

if resp.json().get("code") == 0:
    print("✅ 飞书记录已标记为已发布")
else:
    print(f"❌ 标记失败: {resp.json()}")
    # 记录 record_id，提示用户手动勾选「已发布」
```

---

## 使用示例

### 发布单条记录

```
用户: 发布"射手座的发疯文学语录"到小红书

执行:
1. check_login_status
2. 查询飞书 → 获取 record_id、图片路径、文案
3. publish_content
4. 验证发布结果 ✅
5. 更新飞书「已发布」= true
```

### 批量发布

```
用户: 发布所有已生成但未发布的记录

执行:
1. check_login_status
2. 查询飞书: 已生成=true AND 已发布=false → 获取记录列表
3. 遍历每条记录:
   a. publish_content
   b. ✅ 验证发布成功（失败则跳过，记录错误）
   c. 更新飞书「已发布」= true
   d. 等待 3-5 秒（限流保护）
4. 输出发布报告（成功/失败数量及失败原因）
```

---

## 发布限制

| 限制项 | 限制值 |
|--------|--------|
| 标题长度 | ≤ 20 字 |
| 正文长度 | ≤ 1000 字 |
| 图片数量 | 1-18 张 |
| 图片格式 | PNG / JPG |
| 图片来源 | 本地绝对路径 |
| 每日发帖量 | ≤ 50 篇（建议） |

---

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| 小红书未登录 | 运行 `./xiaohongshu-login-darwin-arm64`，重新检查登录状态 |
| 图片路径无效 | 使用绝对路径，确认文件存在 |
| 标题超长 | 提炼至 ≤20 字后重试 |
| 账号限流 | 停止发布，等待后重试 |
| 飞书标记失败 | 记录 record_id，提示用户手动勾选「已发布」，不影响已发布状态 |

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `skills/publish-to-xiaohongshu/SKILL.md` | 本技能文档 |
| `skills/publish-to-xiaohongshu/COPYWRITING.md` | 文案生成规则、话题标签分类、正文模板 |
| `skills/_shared/feishu-config.md` | 飞书配置 |
| `xiaohongshu-mcp/cookies.json` | 登录凭证 |

---

## 参考

- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
