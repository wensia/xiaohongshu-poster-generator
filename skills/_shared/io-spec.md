# Unified Input/Output Specification

This document defines the standard input sources and output formats for all skills in this project.

---

## Input Sources

### Feishu Bitable

All content data is stored in Feishu Bitable (多维表格).

| Table | app_token | table_id | Purpose |
|-------|-----------|----------|---------|
| 星座海报生成表 | `Qt6Qbzzy6aWBgassGQhcUU5vngc` | `tblyDtUqcfFMaDfO` | Store poster content to generate |
| 低粉爆文抓取表 | `Qt6Qbzzy6aWBgassGQhcUU5vngc` | `tblsfs6oJAbTfgaK` | Store viral notes for analysis |

### Xiaohongshu MCP

Used for fetching note details, comments, and publishing content.

**Login check**: Always call `mcp__xiaohongshu-mcp__check_login_status` before operations.

---

## Output Specifications

### Image Output

| Property | Value |
|----------|-------|
| **Path Pattern** | `output/{YYYY}/{MM}/{DD}/{zodiac}-{title}-{YYMMDD}/` |
| **Dimensions** | 1080 × 1440 px (3:4 vertical ratio) |
| **Format** | PNG |
| **Naming** | `{zodiac}-{title}-cover.png`, `{zodiac}-{title}-page-02.png`, etc. |

### File Naming Convention

```
output/
└── 2026/
    └── 01/
        └── 02/
            └── 射手座-脾气好吗-260102/
                ├── 射手座-脾气好吗-cover.png
                ├── 射手座-脾气好吗-page-02.png
                ├── 射手座-脾气好吗-page-03.png
                └── ...
```

---

## Feishu Writeback Rules

After generating content, update these fields in Feishu:

| Field | Type | Description |
|-------|------|-------------|
| 已生成 | Boolean | Set to `true` after images generated |
| 生成图片 | Attachment | Upload actual image files (not just paths) |
| 已发布 | Boolean | Set to `true` after published to Xiaohongshu |
| 小红书文案 | Text | Store the published caption |

**Important**: The `生成图片` field requires actual file upload via the upload script, not just text updates.

---

## Playwright Screenshot Requirements

**Critical**: Set browser viewport BEFORE navigation!

```
1. mcp__playwright__browser_resize(width=1080, height=1440)
2. mcp__playwright__browser_navigate(url)
3. mcp__playwright__browser_wait_for(time=2)  # Wait for fonts
4. mcp__playwright__browser_take_screenshot(filename)
5. mcp__playwright__browser_close()
```

### Dark Mode Prevention

All HTML templates must include:

```css
:root, html, body {
  color-scheme: light only;
  background: #FAF6F1;
}
```

---

## Xiaohongshu Publishing Format

| Property | Requirement |
|----------|-------------|
| Title | ≤ 20 Chinese characters |
| Content | 100-200 characters |
| Images | Local absolute paths or HTTP URLs |
| Tags | 3-5 hashtags |

---

## Cross-Reference

- **Feishu credentials**: See [feishu-config.md](feishu-config.md)
- **Xiaohongshu login**: See [xiaohongshu-login.md](xiaohongshu-login.md)
- **Field mapping**: See [field-mapping.md](field-mapping.md)
- **Validation rules**: See [validation-rules.md](validation-rules.md)
