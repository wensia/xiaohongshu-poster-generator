# 飞书多维表格配置

本项目使用飞书多维表格作为数据中心，统一管理内容生成、爆文分析等数据。

---

## 应用凭证

```
app_token: Qt6Qbzzy6aWBgassGQhcUU5vngc
```

---

## 数据表清单

| 表名 | table_id | 用途 |
|------|----------|------|
| 星座海报生成 | `tblyDtUqcfFMaDfO` | 存储待生成的海报内容 |
| 低粉爆文抓取 | `tblsfs6oJAbTfgaK` | 存储抓取的爆文及分析结果 |

---

## 星座海报生成表字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 星座 | 单选 | 12星座 |
| 模板 | 单选 | 模板中文名 |
| 标题 | 文本 | 海报主标题 |
| 副标题 | 文本 | 海报副标题 |
| 正文内容 | 长文本 | 内容页正文 |
| 小红书文案 | 长文本 | 发布时配文 |
| 用途 | 单选 | 封面/长文案/套图 |
| 已生成 | 复选框 | 生成状态 |
| 已发布 | 复选框 | 发布状态 |
| 附件 | 附件 | 生成的图片 |

---

## 低粉爆文抓取表字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 笔记ID | 文本 | 小红书笔记ID |
| xsec_token | 文本 | 访问令牌 |
| 标题 | 文本 | 笔记标题 |
| 点赞数 | 数字 | 点赞数 |
| 收藏数 | 数字 | 收藏数 |
| 评论数 | 数字 | 评论数 |
| 粉丝数 | 数字 | 作者粉丝数 |
| 已分析 | 复选框 | 分析状态 |
| 标题分析 | 文本 | AI分析结果 |
| 开头钩子 | 文本 | AI分析结果 |
| 内容结构 | 文本 | AI分析结果 |
| 情绪价值 | 文本 | AI分析结果 |
| 互动引导 | 文本 | AI分析结果 |
| 封面类型 | 单选 | 文字/图片/人物封面 |
| 爆款元素 | 文本 | AI分析结果 |
| 可借鉴点 | 文本 | AI分析结果 |

---

## MCP 调用示例

### 查询记录

```
mcp__lark-mcp__bitable_v1_appTableRecord_search
参数:
- path: {
    app_token: "Qt6Qbzzy6aWBgassGQhcUU5vngc",
    table_id: "<table_id>"
  }
- data: {
    filter: {
      conjunction: "and",
      conditions: [{
        field_name: "字段名",
        operator: "is",
        value: ["值"]
      }]
    }
  }
```

### 创建记录

```
mcp__lark-mcp__bitable_v1_appTableRecord_create
参数:
- path: {
    app_token: "Qt6Qbzzy6aWBgassGQhcUU5vngc",
    table_id: "<table_id>"
  }
- data: {
    fields: {
      "字段名": "值"
    }
  }
```

### 更新记录

```
mcp__lark-mcp__bitable_v1_appTableRecord_update
参数:
- path: {
    app_token: "Qt6Qbzzy6aWBgassGQhcUU5vngc",
    table_id: "<table_id>",
    record_id: "<record_id>"
  }
- data: {
    fields: {
      "字段名": "新值"
    }
  }
```

---

## 相关 Skills

- `generate-from-feishu` - 从飞书生成内容
- `analyze-viral-notes` - 分析爆文
- `generate-from-viral` - 从爆文生成内容
- `fetch-viral-notes` - 抓取低粉爆文
- `upload-to-feishu` - 上传图片到飞书
