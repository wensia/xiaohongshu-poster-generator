---
name: generating-content-from-viral
description: Generates new zodiac poster content by learning from analyzed viral notes in Feishu Bitable. Use when the user wants to create content inspired by successful viral patterns, transform viral note structures into new zodiac content, or batch generate poster ideas from viral references.
---

# 从爆文生成星座海报内容

从飞书"低粉爆文抓取"表获取已分析的爆文，结合小红书MCP获取完整内容，AI智能生成新的星座海报素材，自动写入"星座海报生成"表。

---

## 上下文优化指南

1. **限制处理数量**：默认每次只处理 1 条笔记
2. **精简输出**：不输出完整笔记内容，只输出关键信息和生成结果

---

## 飞书表格配置

> 详细配置见 [`skills/_shared/feishu-config.md`](../_shared/feishu-config.md)

| 表名 | table_id |
|------|----------|
| 低粉爆文抓取（源表） | `tblsfs6oJAbTfgaK` |
| 星座海报生成（目标表） | `tblyDtUqcfFMaDfO` |

```
app_token: Qt6Qbzzy6aWBgassGQhcUU5vngc
```

---

## 执行前检查

> 详细登录流程见 [`skills/_shared/xiaohongshu-login.md`](../_shared/xiaohongshu-login.md)

```
调用 mcp__xiaohongshu-mcp__check_login_status
```

如果未登录，执行扫码登录。

---

## 核心执行流程

### 步骤 1: 从飞书获取爆文记录

**用户指定笔记ID：**

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_search
参数:
- path: {
    app_token: "Qt6Qbzzy6aWBgassGQhcUU5vngc",
    table_id: "tblsfs6oJAbTfgaK"
  }
- data: {
    filter: {
      conjunction: "and",
      conditions: [{
        field_name: "笔记ID",
        operator: "is",
        value: ["<用户指定的笔记ID>"]
      }]
    }
  }
```

**✅ 验证**：如果返回结果为空，停止执行并提示用户检查笔记ID是否正确，或先执行爆文抓取。

**保存关键信息：**
- `record_id` - 源记录ID
- `笔记ID` - 用于获取详情
- `xsec_token` - 访问令牌
- `备注` - AI分析结果

### 步骤 2: 获取小红书笔记完整内容

```
调用 mcp__xiaohongshu-mcp__get_feed_detail
参数:
- feed_id: "<笔记ID>"
- xsec_token: "<xsec_token>"
- load_all_comments: false
```

**提取信息：**
- 完整正文内容
- 标题
- 互动数据（点赞、收藏、评论）

> **备注**：若 `xsec_token` 过期导致请求失败，使用飞书记录中的"内容摘要"和"备注"字段替代继续执行。

### 步骤 3: AI 智能提取星座

**星座识别优先级：**
1. 标题中包含的星座名称
2. 正文中提到最多的星座
3. 若无法识别，询问用户指定星座

### 步骤 4: AI 生成星座海报内容

> 完整提示词模板及风格指南见 [`skills/generating-content-from-viral/prompt-template.md`](./prompt-template.md)

使用提示词模板，传入以下变量生成内容：
- `{title}` / `{content}` / `{likes}` / `{favorites}` / `{comments}` — 来自步骤 2
- `{analysis}` — 来自飞书记录的"备注"字段
- `{zodiac}` — 来自步骤 3

**期望输出（JSON）：**

```json
{
  "标题": "xxx（10-15字，直接点名星座）",
  "副标题": "xxx 或留空",
  "正文内容": "第一段\n\n第二段\n\n第三段\n\n第四段\n\n第五段",
  "星座": "{zodiac}",
  "用途": "套图",
  "小红书文案": "xxx（200字左右，有人味但不浮躁）"
}
```

**✅ 验证**：确认 JSON 结构完整、"正文内容"包含5段、"标题"在10-15字范围内，再进入步骤 5。

### 步骤 5: 写入飞书"星座海报生成"表

```
调用 mcp__lark-mcp__bitable_v1_appTableRecord_create
参数:
- path: {
    app_token: "Qt6Qbzzy6aWBgassGQhcUU5vngc",
    table_id: "tblyDtUqcfFMaDfO"
  }
- data: {
    fields: {
      "标题": "<生成的标题，10-15字>",
      "副标题": "<生成的副标题>",
      "正文内容": "<5段式正文，每段约50字>",
      "星座": "<提取的星座>",
      "用途": "套图",
      "小红书文案": "<200字左右的发布文案>"
    }
  }
```

---

## 输出格式

```
已从爆文生成星座海报内容！

【参考爆文】
- 标题: {原标题}
- 点赞: {likes} | 收藏: {favorites}

【生成内容】
| 字段 | 内容 |
|------|------|
| 星座 | {zodiac} |
| 标题 | {10-15字标题} |
| 副标题 | {副标题} |
| 用途 | 套图 |

【正文内容（5段式）】
{5段正文}

【小红书文案】
{200字左右，有人味但不浮躁}

已写入飞书「星座海报生成」表
```

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `skills/generating-content-from-viral/prompt-template.md` | 生成提示词模板及风格指南 |
| `skills/analyze-viral-notes/SKILL.md` | 爆文分析技能 |
| `skills/generate-copywriting/SKILL.md` | 文案风格指南 |
