---
name: generating-posters-from-feishu
description: Generates zodiac poster sets from Feishu Bitable records with automatic HTML rendering and screenshot capture. Use when the user wants to batch generate posters from spreadsheet data, process pending Feishu records, sync generated images back to Feishu, or check how many tasks are pending in the Bitable.
---

# 飞书多维表格自动化海报生成器

从飞书多维表格读取待生成的海报内容，自动生成图片并上传回飞书。

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [io-spec.md](../_shared/io-spec.md) | Unified input/output specifications |
| [field-mapping.md](../_shared/field-mapping.md) | Feishu field definitions（飞书多维表格字段定义） |
| [validation-rules.md](../_shared/validation-rules.md) | Content validation rules |
| [cover-generation.md](workflows/cover-generation.md) | Cover page workflow |
| [content-generation.md](workflows/content-generation.md) | Content page workflow |
| [copywriting-rules.md](reference/copywriting-rules.md) | Xiaohongshu copywriting style guide |
| [accent-rules.md](reference/accent-rules.md) | Accent color span rules for cover, content, and summary pages |

---

## 执行前检查

> 飞书配置见 [`skills/_shared/feishu-config.md`](../_shared/feishu-config.md)

```bash
cat /Users/panyuhang/我的项目/编程/脚本/小红书封面生成/.env
```

确保 `.env` 中已配置飞书凭证和表格信息。

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

### 功能 2: 生成并回传海报（完整流程）

> 字段定义见 [`_shared/field-mapping.md`](../_shared/field-mapping.md)

```
遍历每条待生成记录（保存 record_id！）:

a. 读取模板规范（TEMPLATE.md）
b. AI 生成 HTML（遵循 accent-rules.md）
c. 保存 HTML 到 /tmp/

⚠️ 【必须】使用独立截图工具:
d. python3 $SCREENSHOT_TOOL --batch /tmp/html_dir/ /path/to/output/
   工具自动处理：viewport 1080x1440、字体等待、截取 .poster 元素

⚠️ 【必须】验证生成结果:
e. 检查所有 .png 文件存在且尺寸为 2160×2880
   → 若异常，检查 HTML 并重新截图

⚠️ 【必须】回传飞书:
f. 上传所有图片到飞书存储，获取 file_token（验证每张上传成功）
g. 更新记录:
   - 已生成 = true
   - 生成图片路径 = <目录路径>
   - 生成图片 = [file_tokens...]  ← 必须包含附件！
h. 验证更新响应 code == 0；失败则提示用户手动处理

4. 汇报生成结果
```

**当前可用模板：**

| 模板 | ID | 重点色 | 说明 |
|------|-----|--------|------|
| 编辑暖调 | `editorial-warm` | `#C15F3C` | 编辑杂志风格，带引用块和页码 |
| 极简暖调 | `minimal-warm` | `#C8725A` | 极简居中布局，大留白，适合封面 |
| 动态编辑风 | `editorial-dynamic` | `#C15F3C` | 4种风格包 × 5种布局变体，随机组合（详见 TEMPLATE.md）|

> ⚠️ **封面与内容页必须使用相同风格包。** 具体风格包定义、套图一致性规则和 Layout S 总结页规范见模板文件 `TEMPLATE.md`。

**⚠️ 防止深色模式：** 生成的 HTML 必须在 CSS 开头包含：
```css
:root, html, body {
  color-scheme: light only;
  background: #FAF6F1;
}
```

**⚠️ 重点色词（accent）规则：** 封面、内容页和总结页均有强制要求，详见 [`reference/accent-rules.md`](reference/accent-rules.md)。

#### 截图工具

**截图脚本路径（全局唯一）：**
```
SCREENSHOT_TOOL=/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/_shared/scripts/poster_screenshot.py
```

**批量截图（推荐，一套图多页时浏览器只启动一次）：**
```bash
python3 $SCREENSHOT_TOOL --batch /tmp/html_dir/ /path/to/output/
```

**单文件截图：**
```bash
python3 $SCREENSHOT_TOOL /tmp/cover.html /path/to/output/cover.png
```

**如需 1x 导出（1080×1440）：**
```bash
python3 $SCREENSHOT_TOOL --scale 1 input.html output.png
```

**工具自动处理：** viewport 1080x1440、**默认 2x 导出（实际像素 2160×2880）**、字体加载等待 2 秒、截取 `.poster` 元素。

**📋 生成后验证（自动执行）：**
```bash
# 验证图片文件存在且尺寸正确（预期 2160×2880）
for img in /path/to/output/*.png; do
  dims=$(python3 -c "from PIL import Image; img=Image.open('$img'); print(f'{img.width}x{img.height}')" 2>/dev/null)
  echo "$img: $dims"
  [[ "$dims" != "2160x2880" ]] && echo "⚠️ 尺寸异常: $img"
done
```

### 功能 3: 回传飞书（⚠️ 每次生成后必须执行）

生成图片后，必须执行以下两步：**①上传图片文件** 到飞书存储获取 file_token，**②更新记录** 将 file_token 写入"生成图片"附件字段。不能只更新文本字段。

**方式一：使用工具脚本（推荐）**

```bash
cd "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成"
./scripts/feishu_upload.sh <record_id> <image_dir>

# 示例
./scripts/feishu_upload.sh recv6ycsM6G5kD "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2025/12/27/射手座-孽缘星座-251227"
```

**方式二：手动 API 调用（参见 [`scripts/feishu_upload.sh`](../../scripts/feishu_upload.sh) 内部实现）**

如脚本不可用，参考脚本内的 curl 调用逻辑手动执行：获取 Token → 逐一上传 `.png` 文件至 `drive/v1/medias/upload_all`（`parent_type=bitable_file`）→ 收集所有 `file_token` → PUT 更新记录字段 `已生成=true`、`生成图片路径`、`生成图片=[{file_token}...]`，验证响应 `code == 0`。

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
| `scripts/feishu_mark_published.sh` | 标记已发布工具脚本 |
| `skills/zodiac-poster/assets/templates.json` | 模板配置 |
| `skills/zodiac-poster/assets/templates/*.md` | 模板设计规范（含风格包、布局详情）|
| `skills/_shared/scripts/poster_screenshot.py` | 截图工具 |
| `reference/accent-rules.md` | 重点色词规则（封面/内容页/总结页）|

---

## ⚠️ 发布到小红书后标记已发布（重要！）

**如果从飞书拉取的记录被发布到小红书，必须立即将该记录标记为「已发布」。**

### 触发条件

1. 用户要求"从飞书拉取xxx并发布到小红书"
2. 用户要求"发布飞书记录到小红书"
3. 任何涉及飞书记录 + 小红书发布的操作

### 标记方式

**方式一：使用工具脚本（推荐）**

```bash
cd "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成"
./scripts/feishu_mark_published.sh <record_id> "<发布的文案>"
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
1. 从飞书拉取记录 → 保存 record_id（重要！）
2. 生成/获取图片（从飞书下载或本地生成）
3. 准备文案（使用"小红书发送文案"字段或 AI 生成）
4. ⚠️ 自动生成话题标签（分析文案，生成 3-5 个标签）
5. 发布到小红书（title + content + images + tags）→ 确认成功
6. ⚠️ 立即标记飞书记录为已发布
   └── "已发布" = true，"小红书文案" = 实际发布的文案
```

**注意：** 必须在发布成功后立即执行标记，不要遗漏。如果标记失败，提示用户手动在飞书中勾选。

---

## 错误处理

### 图片未回传到飞书

**症状**：飞书表格"生成图片"字段为空  
**原因**：只更新了文本字段，没有上传实际图片  
**解决**：`./scripts/feishu_upload.sh <record_id> <image_dir>`

### 飞书 API 调用失败

1. 检查 `.env` 配置是否正确
2. 检查 APP_ID 和 APP_SECRET 是否有效
3. 确认应用已开通多维表格和云文档权限

### 图片生成失败

1. 确认 HTML 语法正确（查看 `/tmp/` 目录下文件）
2. 重新执行截图命令

### 截图尺寸错误（不是 2160×2880）

**原因**：未使用独立截图工具（`device_scale_factor` 未设置）  
**解决**：始终使用 `poster_screenshot.py`，默认已设置 2x 导出
