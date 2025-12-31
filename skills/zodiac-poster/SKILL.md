---
name: zodiac-poster
description: |
  创建社交媒体星座海报，基于 Markdown 设计规范生成 HTML 并截图。
  AI 智能优化排版和重点色标记。
  当用户需要：
  (1) 生成星座相关的社交媒体图片/海报
  (2) 创建带有中文文案的竖版海报(1080x1440)
  (3) 制作星座性格/运势/情感类内容海报
  (4) 批量生成一套同风格的封面+长文案图
invocation: user
---

# 星座海报生成器 v4.0

生成适用于社交媒体的星座主题竖版海报（1080×1440px，3:4比例）。

---

## ⚠️ Playwright MCP 使用要求

**生成图片时必须使用无头模式（headless）**

当使用 Playwright MCP 截图时，确保浏览器在后台运行，不弹出窗口：

```javascript
// Playwright MCP 默认配置应为 headless 模式
// 如果需要调试，可临时关闭，但生产环境必须开启
```

**截图流程：**
1. 将生成的 HTML 保存到 output 目录
2. **调整浏览器尺寸**：`mcp__playwright__browser_resize` 设置 width=1080, height=1440
3. 使用 `mcp__playwright__browser_navigate` 打开 HTML 文件
4. 等待字体加载：`mcp__playwright__browser_wait_for` 等待 2 秒
5. 使用 `mcp__playwright__browser_take_screenshot` 截图（相对路径）
6. 复制截图到 output 目录
7. **完成后关闭浏览器页面**：`mcp__playwright__browser_close`

---

## 模板系统 v4.0

使用 Markdown 设计规范文档定义模板样式，AI 根据规范生成 HTML。

### 当前模板

| 模板 | ID | 重点色 | 说明 |
|------|-----|--------|------|
| 编辑暖调 | `editorial-warm` | `#C15F3C` | 编辑杂志风格，居中对称，温和内敛 |
| 动态编辑 | `editorial-dynamic` | `#C15F3C` | 动态编辑风，非对称布局，视觉张力强 |
| 极简暖调 | `minimal-warm` | `#C8725A` | 极简居中布局，大留白，适合封面 |

### 模板选择指南

| 主题类型 | 推荐模板 | 推荐装饰 |
|----------|----------|----------|
| 每日运势 | `editorial-dynamic` | 大字号日期背景 + 圆形装饰 |
| 年运势/月运势 | `editorial-dynamic` | 大字号背景 + 圆形装饰 |
| 自由/孤独/情感 | `editorial-dynamic` | 大留白 + 放大淡色图标 |
| 性格/兴奋点 | `editorial-dynamic` | 斜线装饰 + 色块副标题 |
| 规则/清单/指南 | `editorial-dynamic` | 左侧竖线 + 编号列表 |
| 职业/方向/选择 | `editorial-dynamic` | 箭头装饰 + 关键词标签组 |
| 配对/对比/常规 | `editorial-warm` | 居中布局 + 引用块 |

---

## 内容类型规则

### 每日运势类（必须遵守）

当内容为**每日运势**类型时，封面**必须**包含以下元素：

| 必含元素 | 格式要求 | 示例 |
|----------|----------|------|
| **日期 + 星座** | 必须在同一行显示 | `12月31日 · 射手座`、`12.31 ♐ 射手` |

**封面布局示例：**

```
┌─────────────────────────────────┐
│                      [星座图标] │
│                                 │
│     [12月31日 · 射手座]         │  ← 日期+星座同一行
│         ─────────               │
│           主标题                │
│          副标题                 │
│         「引用金句」            │
│ ─────────────────────────── 01 │
└─────────────────────────────────┘
```

**日期+星座格式选项：**
- `12月31日 · 射手座`
- `12.31 ♐ 射手座`
- `DEC.31 · SAGITTARIUS`
- `12/31 射手座每日运势`

### 周运势/月运势类

封面**必须**包含：

| 必含元素 | 示例 |
|----------|------|
| **时间范围** | `12月末`、`1月第一周`、`2025年1月` |
| **星座名称** | `射手座` |

### 年运势类

封面**必须**包含：

| 必含元素 | 示例 |
|----------|------|
| **年份** | `2025`（建议作为大字号背景装饰） |
| **星座名称** | `射手座` |

### 性格/情感/指南类

封面**建议**包含：

| 建议元素 | 示例 |
|----------|------|
| **星座名称** | 头部标签或副标题 |
| **主题分类** | `暧昧期指南`、`回避型人格` |

### 模板规范文件

```
assets/templates/editorial-warm/TEMPLATE.md     # 编辑暖调规范
assets/templates/editorial-dynamic/TEMPLATE.md  # 动态编辑规范
assets/templates/editorial-dynamic/examples/    # 动态编辑示例
```

---

## 生成流程

### 步骤 1：读取设计规范

```
读取 assets/templates/{模板ID}.md
```

### 步骤 2：AI 智能处理

1. **分析内容长度** → 决定字号调整
2. **识别关键词** → 决定重点色标记
3. **根据规范生成 HTML** → 包含完整 CSS 样式

### 步骤 3：替换内容变量

**封面变量：**
- `{{header_tag}}` → 头部标签（如"射手座 · 回避型"）
- `{{keyword}}` → 关键词（如"暧昧期指南"）
- `{{line1}}` → 主标题
- `{{line2}}` → 副标题（支持高亮）
- `{{desc}}` → 底部描述
- `{{zodiac_symbol}}` → 星座符号 SVG

**内容页变量：**
- `{{keyword}}` → 分类标签
- `{{mini_title}}` → 小标题
- `{{body_text}}` → 正文（支持高亮）
- `{{quote_text}}` → 引用块文字
- `{{zodiac_symbol}}` → 星座符号 SVG

### 步骤 4：保存并截图

```bash
# 1. 保存 HTML 到 output 目录
output/{YYYY}/{MM}/{DD}/{zodiac}-{title}-{YYMMDD}/cover.html
output/{YYYY}/{MM}/{DD}/{zodiac}-{title}-{YYMMDD}/page-01.html
...

# 2. 调整浏览器尺寸为海报尺寸（必须！）
mcp__playwright__browser_resize → width=1080, height=1440

# 3. 打开 HTML 文件
mcp__playwright__browser_navigate → file:///path/to/cover.html

# 4. 等待字体加载
mcp__playwright__browser_wait_for → time=2

# 5. 截图（⚠️ 必须使用 run_code 截取 .poster 元素，确保尺寸为 1080x1440）
mcp__playwright__browser_run_code → code:
  async (page) => {
    const poster = await page.$('.poster');
    await poster.screenshot({
      path: '/absolute/path/to/output/cover.png',
      scale: 'css'  // 避免 Retina 屏幕 2x 缩放
    });
  }

# 6. 关闭浏览器
mcp__playwright__browser_close
```

**⚠️ 截图注意事项：**
- **必须**使用 `browser_run_code` 截取 `.poster` 元素
- **必须**设置 `scale: 'css'` 避免 Retina 屏幕导致 2x 放大
- **禁止**使用 `browser_take_screenshot`，会导致尺寸错误

---

## AI 智能处理指南

### 1. 智能排版（根据内容调整字号）

**封面标题**：根据文字长度动态调整字号

| 情况 | 处理方式 |
|------|----------|
| 标题 ≤4 字 | 使用大字号（96-110px） |
| 标题 5-8 字 | 使用中等字号（72-96px） |
| 标题 >8 字 | 使用较小字号（56-72px） |

**内容页正文**：根据内容长度调整字号

| 情况 | 处理方式 |
|------|----------|
| 内容 ≤150 字 | 大字号（40-44px），行高 2.0 |
| 内容 150-300 字 | 中等字号（36-40px），行高 1.9 |
| 内容 >300 字 | 较小字号（32-36px），行高 1.8 |

### 2. 重点色标记（高亮关键词）

使用模板的 accent 重点色（`#C15F3C`）高亮以下内容：

1. **数字百分比**：`100%`、`80%`、`3个` 等
2. **星座名称**：出现在正文中的星座名
3. **情感关键词**：爱、心动、暗恋、分手、自由、安全感 等
4. **用户标记**：用户用 `**文字**` 或 `「文字」` 标记的内容
5. **核心观点**：标题中最想强调的词汇

**实现方式**：
```html
<span class="highlight">关键词</span>
```

---

## 飞书多维表格字段

| 字段 | 类型 | 说明 |
|------|------|------|
| 星座 | 单选 | 12星座 |
| 模板 | 单选 | 模板中文名（编辑暖调） |
| 标题 | 文本 | 海报主标题 |
| 副标题 | 文本 | 海报副标题 |
| 正文内容 | 长文本 | 内容页正文 |
| 用途 | 单选 | 封面/长文案 |
| 已生成 | 复选框 | 状态标记 |
| 已发布 | 复选框 | 发布状态 |

---

## 输出位置

```
/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/{YYYY}/{MM}/{DD}/
├── 射手座-标题-241227-1430-cover.png   # 封面
├── 射手座-标题-241227-1430-long.png    # 内容页
└── ...
```

---

## 星座符号

从 `templates.json` 的 `zodiac_symbols` 获取 SVG 路径：

| 星座 | ID | 符号 |
|------|-----|------|
| 白羊座 | `aries` | ♈ |
| 金牛座 | `taurus` | ♉ |
| 双子座 | `gemini` | ♊ |
| 巨蟹座 | `cancer` | ♋ |
| 狮子座 | `leo` | ♌ |
| 处女座 | `virgo` | ♍ |
| 天秤座 | `libra` | ♎ |
| 天蝎座 | `scorpio` | ♏ |
| 射手座 | `sagittarius` | ♐ |
| 摩羯座 | `capricorn` | ♑ |
| 水瓶座 | `aquarius` | ♒ |
| 双鱼座 | `pisces` | ♓ |

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `assets/templates.json` | 模板配置（含重点色、星座符号） |
| `assets/templates/*.md` | Markdown 设计规范文档 |
| `assets/previews/*/` | 模板预览图片 |

---

## 版本历史

- **v4.0**: Markdown 设计规范模式，单一模板
- **v3.1**: AI 智能排版 + 重点色标记
- **v3.0**: 模板套装模式，12种预设模板
- **v2.0**: 四维度配置（配色×风格×字体×用途）
- **v1.0**: 基础海报生成
