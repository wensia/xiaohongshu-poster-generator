---
name: generate-from-feishu
description: |
  从飞书多维表格获取待生成的内容，自动生成星座海报图片，上传回飞书并标记完成。

  触发关键词：
  - "从飞书拉取" / "拉取飞书" / "飞书拉取"
  - "从表格生成" / "批量生成" / "自动生成"
  - "处理待生成" / "处理未生成" / "生成未完成"
  - "飞书同步" / "同步飞书" / "回传飞书"

  当用户需要：
  (1) 从飞书拉取待生成的记录并批量生成海报
  (2) 自动处理飞书表格中"已生成=false"的记录
  (3) 生成图片后回传飞书并标记已完成
  (4) 查看飞书表格中有多少条待处理任务
invocation: user
---

# 飞书多维表格自动化海报生成器

从飞书多维表格读取待生成的海报内容，自动生成图片并上传回飞书。

---

## ⚠️ 关键要求

### 1. Playwright 浏览器视口尺寸（最重要！）

**截图前必须先设置浏览器视口尺寸为 1080x1440（3:4 竖屏比例）！**

```
使用 mcp__playwright__browser_resize 工具：
- width: 1080
- height: 1440
```

**必须在第一次 navigate 之前执行 resize！** 否则截图尺寸会错误。

正确的截图流程：
```
1. browser_resize(width=1080, height=1440)  ← 先调整尺寸
2. browser_navigate(url)                     ← 再打开页面
3. browser_take_screenshot(filename)         ← 最后截图
```

### 2. 生成后必须回传图片到飞书（重要！）

**生成图片后，必须执行以下两个步骤：**

1. **上传图片文件**到飞书存储，获取 file_token
2. **更新记录**，将 file_token 写入"生成图片"附件字段

**不能只更新文本字段！必须上传实际图片文件！**

---

## 执行前检查

> 飞书配置见 [`skills/_shared/feishu-config.md`](../_shared/feishu-config.md)

### 检查 .env 配置

```bash
cat /Users/panyuhang/我的项目/编程/脚本/小红书封面生成/.env
```

确保 config.py 中已配置飞书凭证和表格信息。

---

## 核心功能

### 功能 1: 从飞书获取待生成记录

```bash
cd "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成"
source .env

# 获取 Token
TOKEN=$(curl -s "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$LARK_APP_ID\", \"app_secret\": \"$LARK_APP_SECRET\"}" | jq -r '.tenant_access_token')

# 查询未生成的记录
curl -s "https://open.feishu.cn/open-apis/bitable/v1/apps/$LARK_BITABLE_APP_TOKEN/tables/$LARK_BITABLE_TABLE_ID/records?page_size=100" \
  -H "Authorization: Bearer $TOKEN" > /tmp/feishu_records.json
```

### 功能 2: 生成海报

**流程：**
1. 读取模板设计规范 `skills/zodiac-poster/assets/templates/{模板ID}/TEMPLATE.md`
2. AI 根据规范生成 HTML（包含智能排版和重点色标记）
3. 保存 HTML 到 `/tmp/`
4. **设置浏览器视口尺寸**（必须！）：
   ```
   mcp__playwright__browser_resize(width=1080, height=1440)
   ```
5. 使用 Playwright MCP 打开 HTML 并截图
6. 保存图片到 `output/{YYYY}/{MM}/{DD}/{星座}-{标题}-{时间戳}/`

**当前可用模板：**

| 模板 | ID | 重点色 | 说明 |
|------|-----|--------|------|
| 编辑暖调 | `editorial-warm` | `#C15F3C` | 编辑杂志风格，带引用块和页码 |
| 极简暖调 | `minimal-warm` | `#C8725A` | 极简居中布局，大留白，适合封面 |

### 功能 3: 回传飞书（⚠️ 必须执行）

**方式一：使用工具脚本（推荐）**

```bash
cd "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成"
./scripts/feishu_upload.sh <record_id> <image_dir>

# 示例
./scripts/feishu_upload.sh recv6ycsM6G5kD "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2025/12/27/射手座-孽缘星座-251227"
```

**方式二：手动执行 API 调用**

```bash
cd "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成"
source .env

RECORD_ID="<记录ID>"
IMAGE_DIR="<图片目录>"

# 1. 获取 Token
TOKEN=$(curl -s "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$LARK_APP_ID\", \"app_secret\": \"$LARK_APP_SECRET\"}" | jq -r '.tenant_access_token')

# 2. 上传每张图片（必须！）
for img in "$IMAGE_DIR"/*.png; do
  filename=$(basename "$img")
  filesize=$(stat -f%z "$img")

  # 上传到飞书存储
  curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all" \
    -H "Authorization: Bearer $TOKEN" \
    -F "file_name=$filename" \
    -F "parent_type=bitable_file" \
    -F "parent_node=$LARK_BITABLE_APP_TOKEN" \
    -F "size=$filesize" \
    -F "file=@$img"

  # 记录返回的 file_token
done

# 3. 更新记录（包含附件字段！）
curl -s -X PUT "https://open.feishu.cn/open-apis/bitable/v1/apps/$LARK_BITABLE_APP_TOKEN/tables/$LARK_BITABLE_TABLE_ID/records/$RECORD_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "已生成": true,
      "生成图片路径": "<IMAGE_DIR>",
      "生成图片": [
        {"file_token": "<token1>"},
        {"file_token": "<token2>"},
        ...
      ]
    }
  }'
```

---

## 飞书多维表格字段

| 序号 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 1 | 标题 | 文本 | 海报主标题 |
| 2 | 副标题 | 文本 | 海报副标题 |
| 3 | 正文内容 | 文本 | 内容页正文 |
| 4 | 星座 | 单选 | 12 星座 |
| 5 | 模板 | 单选 | 编辑暖调 |
| 6 | 用途 | 单选 | 封面/长文案/套图 |
| 7 | 已生成 | 复选框 | 生成状态 |
| 8 | 已发布 | 复选框 | 发布状态 |
| 9 | **生成图片** | **附件** | **上传的图片（必须回传！）** |
| 10 | 生成图片路径 | 文本 | 本地路径 |
| 11 | 小红书文案 | 文本 | 发布用文案 |
| 12 | 小红书发送文案 | 文本 | 实际发送的文案 |

---

## 完整生成流程（重要！）

```
用户: 从飞书拉取待生成的海报

Claude 执行:
1. 读取 .env 获取飞书配置
2. 调用飞书 API 查询记录
3. 遍历每条记录:
   a. 读取模板规范
   b. AI 生成 HTML
   c. 保存 HTML 到 /tmp/

   ⚠️ 【必须】Playwright 截图步骤:
   d. browser_resize(width=1080, height=1440)  ← 先设置视口尺寸！
   e. browser_navigate(file:///tmp/xxx.html)   ← 打开 HTML
   f. browser_wait_for(time=2)                 ← 等待字体加载
   g. browser_run_code 截取 .poster 元素:      ← 确保尺寸 1080x1440
      async (page) => {
        const poster = await page.$('.poster');
        await poster.screenshot({
          path: '/output/path/cover.png',
          scale: 'css'  // 避免 Retina 2x 缩放
        });
      }

   ⚠️ 【必须】防止深色模式：
   生成的 HTML 必须在 CSS 开头包含以下样式：
   ```css
   :root, html, body {
     color-scheme: light only;
     background: #FAF6F1;
   }
   ```
   否则系统深色模式会导致背景变成深灰色！

   ⚠️ 【必须】回传飞书:
   h. 上传所有图片到飞书存储，获取 file_token
   i. 更新记录:
      - 已生成 = true
      - 生成图片路径 = <目录路径>
      - 生成图片 = [file_tokens...]  ← 必须包含附件！

4. 汇报生成结果
```

---

## 输出位置

```
/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/{YYYY}/{MM}/{DD}/
└── {星座}-{标题缩写}-{YYMMDD}-{HHMM}/
    ├── 01-cover.png     # 封面
    ├── 02-xxx.png       # 内容页1
    ├── 03-xxx.png       # 内容页2
    └── ...
```

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `.env` | 飞书配置 |
| `scripts/feishu_upload.sh` | **图片上传工具脚本** |
| `skills/zodiac-poster/assets/templates.json` | 模板配置 |
| `skills/zodiac-poster/assets/templates/*.md` | 模板设计规范 |

---

## ⚠️ 发布到小红书后标记已发布（重要！）

**如果从飞书拉取的记录被发布到小红书，必须立即将该记录标记为「已发布」。**

### 触发条件

当以下情况发生时，必须执行标记操作：
1. 用户要求"从飞书拉取xxx并发布到小红书"
2. 用户要求"发布飞书记录到小红书"
3. 任何涉及飞书记录 + 小红书发布的操作

### 标记方式

**方式一：使用工具脚本（推荐）**

```bash
cd "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成"
./scripts/feishu_mark_published.sh <record_id> "<发布的文案>"

# 示例
./scripts/feishu_mark_published.sh recv6Gc0wjHbf9 "射手座的感情..."
```

**方式二：直接调用 MCP API**

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_update
参数:
- path: { app_token, table_id, record_id }
- data: {
    fields: {
      "已发布": true,
      "小红书文案": "<实际发布的文案>"
    }
  }
```

### 完整流程（从飞书拉取 → 发布小红书 → 标记已发布）

```
1. 从飞书拉取记录
   └── 保存 record_id（重要！）

2. 生成/获取图片
   └── 从飞书下载或本地生成

3. 准备文案
   ├── 使用飞书"小红书发送文案"字段
   └── 或 AI 生成新文案

4. ⚠️ 自动生成话题标签
   ├── 分析文案内容
   └── 生成 3-5 个标签（如 ["射手座", "星座", "情感"]）

5. 发布到小红书
   ├── title + content + images + tags
   └── 确认发布成功

6. ⚠️ 立即标记飞书记录为已发布
   ├── "已发布" = true
   └── "小红书文案" = 实际发布的文案
```

### 注意事项

- **必须在发布成功后立即执行标记**，不要遗漏
- 如果标记失败，提示用户手动在飞书中勾选
- record_id 在拉取记录时就要保存，不要发布后再查询

---

## 错误处理

### 图片未回传到飞书

**症状**：飞书表格中"生成图片"字段为空

**原因**：只更新了文本字段，没有上传实际图片

**解决**：
```bash
# 使用工具脚本补传
./scripts/feishu_upload.sh <record_id> <image_dir>
```

### 飞书 API 调用失败

1. 检查 .env 配置是否正确
2. 检查 APP_ID 和 APP_SECRET 是否有效
3. 确认应用已开通多维表格和云文档权限

### 图片生成失败

1. 检查 Playwright MCP 是否正常
2. 确认 HTML 语法正确
3. 查看 /tmp/ 目录下的 HTML 文件

### 截图尺寸错误（不是 1080x1440）

**症状**：生成的图片尺寸不正确，不是竖屏 3:4 比例

**原因**：没有在截图前设置浏览器视口尺寸

**解决**：
```
在 browser_navigate 之前，必须先执行：
mcp__playwright__browser_resize(width=1080, height=1440)
```

**注意**：resize 必须在 navigate 之前执行，否则不生效！
