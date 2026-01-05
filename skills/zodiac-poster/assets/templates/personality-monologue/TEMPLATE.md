# 性格独白风 (Personality Monologue) 模板规范

**特征**：三段式布局（页眉+内容+页脚）+ 4色径向渐变 + 光照叠加层 + 页码系统
**适用**：星座性格深度解读、情感独白、治愈系内容

---

## 核心配色（CSS 变量系统）

```css
:root {
  --bg-color: #F5F2ED;          /* 背景基础色 */
  --text-primary: #3D3835;      /* 主文字 */
  --text-secondary: #6B6461;    /* 次要文字 */
  --accent-color: #C4653A;      /* 强调色（橙褐色） */
  --line-color: #D4CFC8;        /* 分隔线/装饰线 */
}
```

| 用途 | 色值 | 说明 |
|------|------|------|
| **强调色** | `#C4653A` | 高亮文字、分隔线、图标描边、PART标签 |
| **主文字** | `#3D3835` | 主标题、正文 |
| **次要文字** | `#6B6461` | 页眉标题、副标题、页码、引用 |
| **背景渐变** | 4色 | `#F8F5F0 → #F5F2ED → #EDE9E3 → #E8E4DD` |
| **分隔线** | `#D4CFC8` | 页脚分隔线 |

---

## 尺寸放大规范

**基准转换**：原始 420px → 目标 1080px = **2.57 倍**

| 原始尺寸 | 放大后 | 用途 |
|----------|--------|------|
| 13px | 33px | 页眉标题、页码 |
| 14px | 36px | 封面标语、引用 |
| 15px | 39px | 封面副标题、正文 |
| 28px | 72px | 星座图标 |
| 32px | 82px | 章节标题 |
| 38px | 98px | 封面主标题 |
| 45px | 116px | 页面上下内边距 |
| 50px | 129px | 页面左右内边距、分隔线宽度 |

---

## 禁止使用的元素

| 禁止 | 原因 |
|------|------|
| `.keyword` 色块 | 此风格使用 `.highlight` 文字高亮 |
| 噪点纹理 | 保持纯净背景 |
| 渐变色带 | 不属于此风格 |
| 表情符号 | 任何内容禁止表情 |

---

## 核心样式规范（必须精准复制）

### 1. 页面容器 + 4色渐变背景 + 光照叠加

```css
.poster {
  width: 1080px;
  height: 1440px;
  background: radial-gradient(ellipse at 50% 50%,
    #F8F5F0 0%,
    #F5F2ED 40%,
    #EDE9E3 70%,
    #E8E4DD 100%
  );
  position: relative;
  padding: 116px 129px;  /* 原45px 50px放大2.57倍 */
  display: flex;
  flex-direction: column;
  font-family: 'Noto Serif SC', serif;
}

/* 光照叠加层（必须） */
.poster::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.3) 0%,
    rgba(255,255,255,0) 20%,
    rgba(0,0,0,0) 80%,
    rgba(0,0,0,0.03) 100%
  );
  pointer-events: none;
  z-index: 1;
}

.poster > * {
  position: relative;
  z-index: 2;
}
```

### 2. 页眉（所有页面必须）

```css
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 33px;  /* 原13px */
  font-weight: 400;
  color: var(--text-secondary);
  letter-spacing: 5px;
}

.zodiac-symbol svg {
  width: 72px;   /* 原28px */
  height: 72px;
  stroke: var(--accent-color);
  stroke-width: 1.5;
  fill: none;
  transform: rotate(-10deg);
}
```

### 3. 页脚（所有页面必须）

```css
.footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.footer-line {
  width: 100%;
  height: 3px;  /* 原1px放大 */
  background: var(--line-color);
  margin-bottom: 31px;  /* 原12px */
}

.page-number {
  font-family: 'Georgia', serif;
  font-size: 33px;  /* 原13px */
  color: var(--text-secondary);
  letter-spacing: 5px;
}
```

**页码格式**：`0 1`、`0 2`、`0 3`（数字之间有空格）

### 4. 分隔线（章节标题下方）

```css
.section-divider {
  width: 129px;   /* 原50px */
  height: 5px;    /* 原2px */
  background: var(--accent-color);
  margin-bottom: 154px;  /* 原60px */
}
```

### 5. 章节标签

```css
.part-label {
  font-family: 'Georgia', serif;
  font-size: 31px;  /* 原12px */
  color: var(--accent-color);
  letter-spacing: 10px;
  margin-top: 39px;
  margin-bottom: 21px;
}
```

### 6. 正文内容

```css
.content-text {
  font-size: 39px;   /* 原15px */
  color: var(--text-primary);
  line-height: 2.2;
  letter-spacing: 3px;
}

.content-text p {
  margin-bottom: 51px;  /* 原20px */
}

.highlight {
  color: var(--accent-color);
}
```

### 7. 引用区块

```css
.quote {
  margin-top: 90px;  /* 原35px */
  padding-left: 39px;  /* 原15px */
  border-left: 5px solid var(--accent-color);  /* 原2px */
}

.quote-text {
  font-style: italic;
  font-size: 36px;  /* 原14px */
  color: var(--text-secondary);
  letter-spacing: 3px;
  line-height: 1.8;
}
```

---

## 封面模板

```html
<!-- [STYLE: 性格独白风] [TYPE: cover] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面 - {{ZODIAC}} · {{TOPIC}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-color: #F5F2ED;
      --text-primary: #3D3835;
      --text-secondary: #6B6461;
      --accent-color: #C4653A;
      --line-color: #D4CFC8;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }

    .poster {
      width: 1080px;
      height: 1440px;
      background: radial-gradient(ellipse at 50% 50%,
        #F8F5F0 0%,
        #F5F2ED 40%,
        #EDE9E3 70%,
        #E8E4DD 100%
      );
      position: relative;
      padding: 116px 129px;
      display: flex;
      flex-direction: column;
      font-family: 'Noto Serif SC', serif;
    }

    .poster::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(180deg,
        rgba(255,255,255,0.3) 0%,
        rgba(255,255,255,0) 20%,
        rgba(0,0,0,0) 80%,
        rgba(0,0,0,0.03) 100%
      );
      pointer-events: none;
      z-index: 1;
    }

    .poster > * { position: relative; z-index: 2; }

    /* 页眉 */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: auto;
    }
    .header-title {
      font-family: 'Noto Sans SC', sans-serif;
      font-size: 33px;
      font-weight: 400;
      color: var(--text-secondary);
      letter-spacing: 5px;
    }
    .zodiac-symbol svg {
      width: 72px;
      height: 72px;
      stroke: var(--accent-color);
      stroke-width: 1.5;
      fill: none;
      transform: rotate(-10deg);
    }

    /* 封面内容 */
    .cover-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 51px 0;
    }
    .cover-subtitle {
      font-size: 39px;
      color: var(--text-secondary);
      letter-spacing: 8px;
      margin-bottom: 64px;
    }
    .cover-title {
      font-size: 98px;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.5;
      letter-spacing: 10px;
      margin-bottom: 77px;
    }
    .cover-title .highlight {
      color: var(--accent-color);
    }
    .cover-divider {
      width: 129px;
      height: 5px;
      background: var(--accent-color);
      margin-bottom: 77px;
    }
    .cover-tagline {
      font-size: 36px;
      color: var(--text-secondary);
      line-height: 2;
      letter-spacing: 5px;
    }

    /* 页脚 */
    .footer {
      margin-top: auto;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }
    .footer-line {
      width: 100%;
      height: 3px;
      background: var(--line-color);
      margin-bottom: 31px;
    }
    .page-number {
      font-family: 'Georgia', serif;
      font-size: 33px;
      color: var(--text-secondary);
      letter-spacing: 5px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="header-title">{{ZODIAC}} · {{TOPIC}}</span>
      <div class="zodiac-symbol">
        {{ZODIAC_SVG}}
      </div>
    </div>

    <div class="cover-content">
      <p class="cover-subtitle">{{SUBTITLE}}</p>
      <h1 class="cover-title">
        {{TITLE_LINE1}}<br><span class="highlight">{{TITLE_HIGHLIGHT}}</span>
      </h1>
      <div class="cover-divider"></div>
      <p class="cover-tagline">
        {{TAGLINE_LINE1}}<br>{{TAGLINE_LINE2}}
      </p>
    </div>

    <div class="footer">
      <div class="footer-line"></div>
      <span class="page-number">0 1</span>
    </div>
  </div>
</body>
</html>
```

**封面变量说明**：
| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC}}` | 星座名称 | 射手座 |
| `{{TOPIC}}` | 主题 | 性格解读 |
| `{{ZODIAC_SVG}}` | 星座图标SVG | `<svg>...</svg>` |
| `{{SUBTITLE}}` | 副标题 | 为什么说射手座是 |
| `{{TITLE_LINE1}}` | 主标题第一行 | 最 |
| `{{TITLE_HIGHLIGHT}}` | 高亮词（第二行） | 孤独 |
| `{{TAGLINE_LINE1}}` | 标语第一行 | 笑着的人 |
| `{{TAGLINE_LINE2}}` | 标语第二行 | 不一定真的快乐 |

---

## 内容页模板

```html
<!-- [STYLE: 性格独白风] [TYPE: page] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {{PAGE_NUM}} - {{SECTION_TITLE}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-color: #F5F2ED;
      --text-primary: #3D3835;
      --text-secondary: #6B6461;
      --accent-color: #C4653A;
      --line-color: #D4CFC8;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }

    .poster {
      width: 1080px;
      height: 1440px;
      background: radial-gradient(ellipse at 50% 50%,
        #F8F5F0 0%,
        #F5F2ED 40%,
        #EDE9E3 70%,
        #E8E4DD 100%
      );
      position: relative;
      padding: 116px 129px;
      display: flex;
      flex-direction: column;
      font-family: 'Noto Serif SC', serif;
    }

    .poster::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(180deg,
        rgba(255,255,255,0.3) 0%,
        rgba(255,255,255,0) 20%,
        rgba(0,0,0,0) 80%,
        rgba(0,0,0,0.03) 100%
      );
      pointer-events: none;
      z-index: 1;
    }

    .poster > * { position: relative; z-index: 2; }

    /* 页眉 */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    .header-title {
      font-family: 'Noto Sans SC', sans-serif;
      font-size: 33px;
      font-weight: 400;
      color: var(--text-secondary);
      letter-spacing: 5px;
    }
    .zodiac-symbol svg {
      width: 72px;
      height: 72px;
      stroke: var(--accent-color);
      stroke-width: 1.5;
      fill: none;
      transform: rotate(-10deg);
    }

    /* 章节标签 */
    .part-label {
      font-family: 'Georgia', serif;
      font-size: 31px;
      color: var(--accent-color);
      letter-spacing: 10px;
      margin-top: 39px;
      margin-bottom: 21px;
    }

    /* 章节标题 */
    .section-title {
      font-size: 82px;
      font-weight: 600;
      color: var(--text-primary);
      letter-spacing: 8px;
      margin-bottom: 31px;
    }

    /* 分隔线 */
    .section-divider {
      width: 129px;
      height: 5px;
      background: var(--accent-color);
      margin-bottom: 154px;
    }

    /* 内容区域 */
    .content-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-bottom: 103px;
    }

    .content-text {
      font-size: 39px;
      color: var(--text-primary);
      line-height: 2.2;
      letter-spacing: 3px;
    }
    .content-text p {
      margin-bottom: 51px;
    }
    .content-text .highlight {
      color: var(--accent-color);
    }

    /* 引用区块 */
    .quote {
      margin-top: 90px;
      padding-left: 39px;
      border-left: 5px solid var(--accent-color);
    }
    .quote-text {
      font-style: italic;
      font-size: 36px;
      color: var(--text-secondary);
      letter-spacing: 3px;
      line-height: 1.8;
    }

    /* 页脚 */
    .footer {
      margin-top: auto;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }
    .footer-line {
      width: 100%;
      height: 3px;
      background: var(--line-color);
      margin-bottom: 31px;
    }
    .page-number {
      font-family: 'Georgia', serif;
      font-size: 33px;
      color: var(--text-secondary);
      letter-spacing: 5px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="header-title">{{ZODIAC}} · {{TOPIC}}</span>
      <div class="zodiac-symbol">
        {{ZODIAC_SVG}}
      </div>
    </div>

    <p class="part-label">PART {{PART_NUM}}</p>
    <h2 class="section-title">{{SECTION_TITLE}}</h2>
    <div class="section-divider"></div>

    <div class="content-body">
      <div class="content-text">
        {{CONTENT}}
      </div>

      <div class="quote">
        <p class="quote-text">"{{QUOTE}}"</p>
      </div>
    </div>

    <div class="footer">
      <div class="footer-line"></div>
      <span class="page-number">{{PAGE_NUMBER}}</span>
    </div>
  </div>
</body>
</html>
```

**内容页变量说明**：
| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC}}` | 星座名称 | 射手座 |
| `{{TOPIC}}` | 主题 | 性格解读 |
| `{{ZODIAC_SVG}}` | 星座图标SVG | `<svg>...</svg>` |
| `{{PART_NUM}}` | 章节编号 | 01、02... |
| `{{SECTION_TITLE}}` | 章节标题 | 最可怕的地方 |
| `{{CONTENT}}` | 正文内容 | `<p>...</p>` |
| `{{QUOTE}}` | 引用文字 | 走得洒脱，是因为早就做好了准备 |
| `{{PAGE_NUMBER}}` | 页码 | 0 2（带空格） |

---

## 总结页模板

```html
<!-- [STYLE: 性格独白风] [TYPE: end] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {{PAGE_NUM}} - 总结</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-color: #F5F2ED;
      --text-primary: #3D3835;
      --text-secondary: #6B6461;
      --accent-color: #C4653A;
      --line-color: #D4CFC8;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }

    .poster {
      width: 1080px;
      height: 1440px;
      background: radial-gradient(ellipse at 50% 50%,
        #F8F5F0 0%,
        #F5F2ED 40%,
        #EDE9E3 70%,
        #E8E4DD 100%
      );
      position: relative;
      padding: 116px 129px;
      display: flex;
      flex-direction: column;
      font-family: 'Noto Serif SC', serif;
    }

    .poster::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(180deg,
        rgba(255,255,255,0.3) 0%,
        rgba(255,255,255,0) 20%,
        rgba(0,0,0,0) 80%,
        rgba(0,0,0,0.03) 100%
      );
      pointer-events: none;
      z-index: 1;
    }

    .poster > * { position: relative; z-index: 2; }

    /* 页眉 */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    .header-title {
      font-family: 'Noto Sans SC', sans-serif;
      font-size: 33px;
      font-weight: 400;
      color: var(--text-secondary);
      letter-spacing: 5px;
    }
    .zodiac-symbol svg {
      width: 72px;
      height: 72px;
      stroke: var(--accent-color);
      stroke-width: 1.5;
      fill: none;
      transform: rotate(-10deg);
    }

    /* 章节标签 */
    .part-label {
      font-family: 'Georgia', serif;
      font-size: 31px;
      color: var(--accent-color);
      letter-spacing: 10px;
      margin-top: 39px;
      margin-bottom: 21px;
    }

    /* 章节标题 */
    .section-title {
      font-size: 82px;
      font-weight: 600;
      color: var(--text-primary);
      letter-spacing: 8px;
      margin-bottom: 31px;
    }

    /* 分隔线 */
    .section-divider {
      width: 129px;
      height: 5px;
      background: var(--accent-color);
      margin-bottom: 129px;
    }

    /* 总结内容区域 */
    .summary-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-bottom: 77px;
    }

    .summary-text {
      font-size: 39px;
      color: var(--text-primary);
      line-height: 2.4;
      letter-spacing: 3px;
    }
    .summary-text p {
      margin-bottom: 21px;
    }
    .summary-text .highlight {
      color: var(--accent-color);
    }

    /* 结语区域 */
    .ending-section {
      margin-top: 116px;
      text-align: center;
    }
    .ending-wish {
      font-size: 36px;
      color: var(--text-secondary);
      letter-spacing: 5px;
      line-height: 2;
      font-style: italic;
    }
    .ending-mark {
      margin-top: 64px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 39px;
    }
    .ending-mark::before,
    .ending-mark::after {
      content: '';
      width: 77px;
      height: 3px;
      background: var(--line-color);
    }
    .ending-mark span {
      font-family: 'Georgia', serif;
      font-size: 28px;
      color: var(--accent-color);
      letter-spacing: 8px;
    }

    /* 页脚 */
    .footer {
      margin-top: auto;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }
    .footer-line {
      width: 100%;
      height: 3px;
      background: var(--line-color);
      margin-bottom: 31px;
    }
    .page-number {
      font-family: 'Georgia', serif;
      font-size: 33px;
      color: var(--text-secondary);
      letter-spacing: 5px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="header-title">{{ZODIAC}} · {{TOPIC}}</span>
      <div class="zodiac-symbol">
        {{ZODIAC_SVG}}
      </div>
    </div>

    <p class="part-label">EXTRA</p>
    <h2 class="section-title">{{SUMMARY_TITLE}}</h2>
    <div class="section-divider"></div>

    <div class="summary-content">
      <div class="summary-text">
        {{CONTENT}}
      </div>

      <div class="ending-section">
        <p class="ending-wish">
          {{ENDING_LINE1}}<br>{{ENDING_LINE2}}
        </p>
        <div class="ending-mark">
          <span>END</span>
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-line"></div>
      <span class="page-number">{{PAGE_NUMBER}}</span>
    </div>
  </div>
</body>
</html>
```

**总结页变量说明**：
| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC}}` | 星座名称 | 射手座 |
| `{{TOPIC}}` | 主题 | 性格解读 |
| `{{ZODIAC_SVG}}` | 星座图标SVG | `<svg>...</svg>` |
| `{{SUMMARY_TITLE}}` | 总结标题 | 写给射手座 |
| `{{CONTENT}}` | 总结正文 | `<p>...</p>` |
| `{{ENDING_LINE1}}` | 结语第一行 | 愿每一个射手座 |
| `{{ENDING_LINE2}}` | 结语第二行 | 都能被温柔以待 |
| `{{PAGE_NUMBER}}` | 页码 | 0 3（带空格） |

---

## 星座图标 SVG

射手座图标（其他星座从 zodiac-symbols.json 获取）：
```html
<svg viewBox="0 0 24 24">
  <path d="M4 20L20 4M20 4H10M20 4V14" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

---

## 生成规则

### 1. 页面结构规则（必须遵守）

**所有页面必须包含三段式布局**：
- **页眉**：左侧标题 + 右侧星座图标
- **内容区**：封面/章节/总结内容
- **页脚**：分隔线 + 页码（右对齐）

### 2. 页码格式

| 页面 | 页码格式 |
|------|---------|
| 封面 | `0 1` |
| 第2页 | `0 2` |
| 第3页 | `0 3` |
| ... | `0 X` |

**注意**：数字之间有空格

### 3. 文字高亮规则

| 页面类型 | 高亮要求 | 示例 |
|----------|---------|------|
| 封面 | 主标题核心词（1个） | `<span class="highlight">孤独</span>` |
| 内容页 | 正文关键词（1-2个） | `<span class="highlight">随时抽身离开</span>` |
| 总结页 | 结语关键词（可选） | `<span class="highlight">用笑容掩饰脆弱</span>` |

### 4. 章节编号规则

- 封面页：无章节标签
- 内容页：`PART 01`、`PART 02`...
- 总结页：`EXTRA`（固定值）

### 5. 引用区块规则

- 仅内容页使用引用区块
- 引用内容使用引号包裹
- 左边框使用强调色 `#C4653A`

### 6. 行尾排版规则

**禁止标点符号作为每行的结尾**

| 错误 | 正确 |
|------|------|
| `射手的快乐，` | `射手的快乐` |
| `是真的乐观。` | `是真的乐观` |

---

## 检查清单

生成后检查：

- [ ] 尺寸是否为 1080x1440
- [ ] 背景是否为 4 色径向渐变（非 2 色）
- [ ] 是否有 ::before 光照叠加层
- [ ] 页眉是否有左标题 + 右星座图标
- [ ] 星座图标是否旋转 -10deg
- [ ] 页脚是否有分隔线 + 右对齐页码
- [ ] 页码格式是否为 "0 X"（带空格）
- [ ] 分隔线是否为 129px × 5px 强调色
- [ ] 正文字号是否为 39px（非 26px）
- [ ] 封面是否有 `.highlight` 高亮词
- [ ] 内容页是否有 `PART 0X` 标签
- [ ] 内容页是否有左边框 `.quote` 引用区块
- [ ] 总结页是否有 `EXTRA` 和 `END` 标记
- [ ] END 标记是否有左右装饰线
- [ ] 行尾是否有标点符号（不应有）
- [ ] **所有页面强调色是否为 `#C4653A`**
- [ ] **所有页面视觉风格是否统一**
