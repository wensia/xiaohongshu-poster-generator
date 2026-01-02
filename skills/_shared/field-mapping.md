# Feishu Bitable Field Mapping

This document defines all field names and their types used across Feishu tables.

---

## Table 1: 星座海报生成表 (tblyDtUqcfFMaDfO)

### Input Fields (User fills)

| Field Name | Type | Description | Example |
|------------|------|-------------|---------|
| 星座 | SingleSelect | Zodiac sign (12 options) | 射手座 |
| 标题 | Text | Main poster title | 别追了 |
| 副标题 | Text | Subtitle | 射手回避型 |
| 正文内容 | Text (multiline) | Content paragraphs (newline-separated) | 段落1\n段落2 |
| 模板 | SingleSelect | Template ID | editorial-warm |
| 用途 | SingleSelect | Purpose (封面/内容页/套图) | 套图 |

### Output Fields (System fills)

| Field Name | Type | Description |
|------------|------|-------------|
| 已生成 | Checkbox | Whether images have been generated |
| 生成图片 | Attachment | Uploaded poster images |
| 已发布 | Checkbox | Whether published to Xiaohongshu |
| 小红书文案 | Text | Published caption text |
| 生成时间 | DateTime | Generation timestamp |

---

## Table 2: 低粉爆文抓取表 (tblsfs6oJAbTfgaK)

### Input Fields (Scraped data)

| Field Name | Type | Description |
|------------|------|-------------|
| 笔记ID | Text | Xiaohongshu note ID (feed_id) |
| 标题 | Text | Note title |
| 作者 | Text | Author name |
| 粉丝数 | Number | Author follower count |
| 点赞数 | Number | Like count |
| 收藏数 | Number | Save count |
| 评论数 | Number | Comment count |
| xsec_token | Text | Access token for fetching details |
| 抓取时间 | DateTime | Scrape timestamp |

### Analysis Fields (AI fills)

| Field Name | Type | Description |
|------------|------|-------------|
| 已分析 | Checkbox | Whether analysis is complete |
| 分析时间 | DateTime | Analysis timestamp |
| 标题分析 | Text | Title pattern analysis |
| 开头钩子 | Text | Opening hook analysis |
| 内容结构 | Text | Content structure analysis |
| 情绪价值 | Text | Emotional value analysis |
| 爆款元素 | Text | Viral elements summary |
| 可复用点 | Text | Reusable patterns |

---

## Field Type Reference

| Type | MCP `type` value | Notes |
|------|------------------|-------|
| Text | 1 | Single or multiline |
| Number | 2 | |
| SingleSelect | 3 | |
| MultiSelect | 4 | |
| DateTime | 5 | Use `date_formatter: "yyyy/MM/dd HH:mm"` |
| Checkbox | 7 | Boolean |
| Attachment | 17 | Requires file upload |

---

## Zodiac Options (星座)

| Chinese | English | Symbol |
|---------|---------|--------|
| 白羊座 | Aries | ♈ |
| 金牛座 | Taurus | ♉ |
| 双子座 | Gemini | ♊ |
| 巨蟹座 | Cancer | ♋ |
| 狮子座 | Leo | ♌ |
| 处女座 | Virgo | ♍ |
| 天秤座 | Libra | ♎ |
| 天蝎座 | Scorpio | ♏ |
| 射手座 | Sagittarius | ♐ |
| 摩羯座 | Capricorn | ♑ |
| 水瓶座 | Aquarius | ♒ |
| 双鱼座 | Pisces | ♓ |

---

## Template Options (模板)

| ID | Name | Description |
|----|------|-------------|
| editorial-warm | 编辑暖调 | Magazine style, warm colors |
| editorial-dynamic | 动态编辑风 | Dynamic magazine style |
| minimal-warm | 简约暖调 | Minimal warm style |
