---
name: creating-zodiac-posters
description: Creates social media zodiac posters by generating HTML from Markdown design specs and capturing screenshots. Use when the user wants to create zodiac-themed vertical posters (1080x1440), design Chinese copywriting images, produce zodiac personality or horoscope content, or batch generate cover and content page sets.
---

# 星座海报生成器 v4.0

生成适用于社交媒体的星座主题竖版海报（1080×1440px，3:4比例）。

---

## ⚠️ 截图工具：唯一授权方式

**❌ 绝对禁止使用任何 MCP Playwright 截图工具**（输出横版，尺寸不正确）。

**✅ 必须使用独立 Python 截图工具**（`skills/_shared/scripts/poster_screenshot.py`）：

```bash
# 单文件截图
python3 /Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/_shared/scripts/poster_screenshot.py \
    /tmp/cover.html \
    /path/to/output/cover.png

# 批量截图（推荐：一套图多页，浏览器只启动一次）
python3 /Users/panyuhang/我的项目/编程/脚本/小红书封面生成/skills/_shared/scripts/poster_screenshot.py \
    --batch /tmp/poster_html/ /path/to/output/
```

**工具特性**：固定 viewport 1080x1440、自动等待字体加载 2 秒、自动截取 `.poster` 元素、支持 `--json` 输出。

---

## 模板系统

| 模板 | ID | 重点色 | 说明 |
|------|-----|--------|------|
| 编辑暖调 | `editorial-warm` | `#C15F3C` | 居中对称，温和内敛 |
| 动态编辑 | `editorial-dynamic` | `#C15F3C` | 非对称布局，视觉张力强 |
| 极简暖调 | `minimal-warm` | `#C8725A` | 大留白，适合封面 |

**模板规范文件**：

```
assets/templates/editorial-warm/TEMPLATE.md
assets/templates/editorial-dynamic/TEMPLATE.md
assets/templates/minimal-warm/TEMPLATE.md
```

### 模板选择指南

| 主题类型 | 推荐模板 | 推荐装饰 |
|----------|----------|----------|
| 每日/年/月运势 | `editorial-dynamic` | 大字号背景 + 圆形装饰 |
| 自由/孤独/情感 | `editorial-dynamic` | 大留白 + 放大淡色图标 |
| 性格/兴奋点 | `editorial-dynamic` | 斜线装饰 + 色块副标题 |
| 规则/清单/指南 | `editorial-dynamic` | 左侧竖线 + 编号列表 |
| 职业/方向/选择 | `editorial-dynamic` | 箭头装饰 + 关键词标签组 |
| 配对/对比/常规 | `editorial-warm` | 居中布局 + 引用块 |

---

## 套图生成规则

### 核心规则：正文段落数 = 内容页数量

每套图固定结构：**封面 + N 内容页 + 总结页**（N = 以空行 `\n\n` 分隔的正文段落数）。

```python
paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
num_pages = len(paragraphs)  # 内容页数量，总图数 = N + 2
```

**示例（5段正文 → 7张图）**：

```
01_cover.png   → 封面
02_page.png    → 第1段
03_page.png    → 第2段
04_page.png    → 第3段
05_page.png    → 第4段
06_page.png    → 第5段
07_end.png     → 总结页
```

每张内容页包含：该段落的**关键词/小标题**（2-4字核心词）、**正文**、**页码**。

### 双锁定规则（风格包 × 布局变体）

**同一套图必须全程使用同一风格包 + 同一布局变体**，不得中途更换。

**风格包**（4种，生成前随机选1种）：

| 编号 | 风格包 |
|-----|-------|
| 1 | 经典强调 |
| 2 | 简约边框 |
| 3 | 杂志双线 |
| 4 | 艺术镂空 |

**布局变体**（5种，生成前随机选1种）：

| 编号 | 变体 | 特征 | 关键CSS类 |
|-----|------|------|---------|
| 1 | A 色块标题居中式 | 居中对称，色块标题 | `.main-a`, `.title-block` |
| 2 | B 杂志章节式 | 左对齐，PART标签 | `.main-b`, `.part-label` |
| 3 | C 数字序号引导式 | 大淡色数字背景 | `.main-c`, `.big-number` |
| 4 | D 引用突出式 | 大引号开头 | `.main-d`, `.big-quote` |
| 5 | E 分栏对比式 | 左侧标签+右侧内容 | `.main-e`, `.left-column` |

**内容类型参考建议**（随机优先，仅供参考）：每日运势→A；年运/月运→B；情感/心理→D；多话题→E；清单/指南→C。

**批量生成时**：每条记录使用不同风格组合（随机公式：`风格包编号 = (记录索引 % 4) + 1`，`布局变体编号 = (记录索引 % 5) + 1`）。

**封面 HTML 必须包含双锁定注释**，所有后续内容页继承：

```html
<!-- [STYLE LOCK: 简约边框] [LAYOUT LOCK: B] -->
<!-- 本套图所有内容页必须使用此风格和布局 -->
```

详细风格变体定义参见各模板的 `TEMPLATE.md`。

---

## 内容类型规范

| 类型 | 封面必含元素 | 示例 |
|------|------------|------|
| 每日运势 | 日期+星座同一行（48-56px 加粗） | `12月31日 · 射手座` |
| 周/月运势 | 时间范围 + 星座名 | `12月末 · 射手座` |
| 年运势 | 年份（建议大字背景装饰）+ 星座名 | `2025 · 射手座` |
| 性格/情感/指南 | 星座名 + 主题分类 | `射手座 暧昧期指南` |

**每日运势日期+星座样式规范**：

```css
.date-zodiac {
  font-size: 48px-56px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 4px-6px;
  text-align: center;
}
```

---

## 生成流程

### 步骤 0：读取飞书记录的模板字段

从飞书记录获取"模板"字段值，映射到模板 ID：

| 字段值 | 模板 ID |
|--------|---------|
| 编辑暖调 | `editorial-warm` |
| 动态编辑风 | `editorial-dynamic` |
| 极简暖调 | `minimal-warm` |

字段为空时默认使用 `editorial-warm`。飞书多维表格字段定义详见 `assets/docs/FEISHU_SCHEMA.md`。

### 步骤 1：读取设计规范

```
读取 assets/templates/{模板ID}/TEMPLATE.md
```

### 步骤 1.5：确定并记录双锁定配置

生成任何页面前，确定并记录：

```
套图配置：
- 风格包：简约边框 ← 随机选择（编号2）
- 布局变体：B（杂志章节式）← 随机选择（编号2）
```

**⚠️ 从封面到最后一张内容页，严格使用上述配置。**

### 步骤 2：AI 智能处理

1. **分析内容长度** → 决定字号调整（字号规则见 `assets/docs/TYPOGRAPHY.md`）
2. **识别关键词** → 用 `【词】` 标记高亮（高亮规则见 `assets/docs/TYPOGRAPHY.md`）
3. **根据规范生成 HTML** → 包含完整 CSS 样式

**防止深色模式**（必须在 CSS 开头添加）：

```css
:root, html, body {
  color-scheme: light only;
  background: #FAF6F1;
}
```

### 步骤 3：替换内容变量

**封面变量**：`{{header_tag}}`、`{{keyword}}`、`{{line1}}`、`{{line2}}`、`{{desc}}`、`{{zodiac_symbol}}`

**内容页变量**：`{{keyword}}`、`{{mini_title}}`、`{{body_text}}`、`{{quote_text}}`、`{{zodiac_symbol}}`

### 步骤 4：保存 HTML 并截图

```bash
# 保存路径
output/{YYYY}/{MM}/{DD}/{zodiac}-{title}-{YYMMDD}/cover.html
output/{YYYY}/{MM}/{DD}/{zodiac}-{title}-{YYMMDD}/page-01.html
# ...

# 批量截图
python3 .../poster_screenshot.py --batch /path/to/html_dir/ /path/to/output/
```

**验证检查点**：

| 检查项 | 预期 | 失败时处理 |
|--------|------|-----------|
| HTML 文件存在 | `ls /path/*.html` 输出非空 | 重新生成该页 HTML |
| PNG 输出存在 | `ls /path/*.png` 输出非空 | 重新运行截图工具 |
| 截图工具 JSON 输出 | `"status": "success"` | 检查 Python 环境和文件路径 |
| 页数正确 | PNG 数量 = 段落数 + 2 | 检查段落解析逻辑 |

---

## AI 智能处理指南

> 完整字号表、行尾排版规则、高亮解析代码及 SVG 渲染示例详见 `assets/docs/TYPOGRAPHY.md`。

### 1. 智能排版（字号速查）

**封面标题**：≤4字 → 96-110px；5-8字 → 72-96px；>8字 → 56-72px。

**内容页正文**：≤150字 → 40-44px（行高2.0）；150-300字 → 36-40px（行高1.9）；>300字 → 32-36px（行高1.8）。

### 2. 行尾排版规则

**🚫 禁止标点符号作为每行结尾。** 逗号/句号/感叹号/问号删除，破折号移到下一行开头。

```html
<!-- ❌ 错误 -->
<p class="content">射手表面上看起来，<br/>不在乎任何人。</p>

<!-- ✅ 正确 -->
<p class="content">射手表面上看起来<br/>不在乎任何人</p>
```

**长句拆分示例**：

原文：`射手表面上看起来不在乎任何人，其实心里早就给你留了位置——只是嘴硬不说。`

```html
<p class="content">
  射手表面上看起来<br/>
  <span class="accent">不在乎</span>任何人<br/><br/>
  其实心里早就<br/>
  给你<span class="accent">留了位置</span><br/>
  ——只是嘴硬不说
</p>
```

### 3. 重点色标记（智能高亮）

使用 `【词】` 标记需要高亮的词汇，脚本解析后渲染为 accent 色（`#C4653A`）。

**高亮优先级**：①星座名称 ②核心动词 ③核心名词 ④情感形容词 ⑤数字/程度词

**封面双行标题格式**：

| 主题 | 标题字段（含标记） |
|------|-----------------|
| 双子座做决定 | `【双子座】做【决定】\n来不及【想】` |
| 双子座的热情 | `【双子座】的【热情】\n一点就【燃】` |

规则：每行高亮 2-4 个词，避免连续高亮，星座名必须高亮。

**正文高亮**：每段高亮 2-3 个关键词，形成对比/递进/因果/转折语义呼应。

解析逻辑与 SVG 渲染结果示例见 `assets/docs/TYPOGRAPHY.md`。

---

## 输出位置

```
/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/{YYYY}/{MM}/{DD}/
├── 射手座-标题-241227-1430-cover.png
├── 射手座-标题-241227-1430-page-01.png
└── ...
```

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `assets/templates.json` | 模板配置（含重点色、星座符号 SVG） |
| `assets/templates/*.md` | Markdown 设计规范文档 |
| `assets/previews/*/` | 模板预览图片 |
| `skills/_shared/scripts/poster_screenshot.py` | 截图工具 |
| `assets/docs/TYPOGRAPHY.md` | 字号规则、行尾排版、高亮解析代码及 SVG 示例 |
| `assets/docs/FEISHU_SCHEMA.md` | 飞书多维表格字段定义 |
