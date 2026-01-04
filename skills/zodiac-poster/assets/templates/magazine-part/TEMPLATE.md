# 杂志分栏风 (Magazine Part) 模板规范

**特征**：PART 章节编号 + 右侧橙色竖线 + 关键词标签组 + 底部引用
**适用**：职业方向、知识科普、专题系列内容

---

## 核心配色（必须遵守）

| 用途 | 色值 | 说明 |
|------|------|------|
| **强调色** | `#C15F3C` | 图标、关键词、竖线装饰 |
| **弱化色** | `#B1ADA1` / `#9A958A` | 标签、页码、辅助文字 |
| **深色文字** | `#3D3D3D` | 主标题、正文 |
| **次要文字** | `#5A5A5A` | 副标题、正文 |
| **背景色** | `#FAF6F1` | 纯色背景（无渐变） |

---

## 🚨 核心禁令

### 禁止使用的元素

| 禁止 | 原因 |
|------|------|
| 背景渐变 | 此风格使用纯色背景 |
| 噪点纹理 | 保持干净简洁 |
| 双线边框 | 不属于此风格 |
| 星星装饰 | 不属于此风格 |
| 表情符号 | 任何内容禁止表情 |

---

## 风格特征

### 右侧橙色竖线装饰（必须）
```css
.side-line {
  position: absolute;
  top: 200px;
  right: 60px;
  width: 3px;
  height: 120px;
  background: linear-gradient(180deg, #C15F3C 0%, rgba(193, 95, 60, 0.3) 100%);
}
```

### 章节编号样式（内容页必须）
```css
.part-number {
  font-size: 18px;
  font-weight: 400;
  color: #C15F3C;
  letter-spacing: 4px;
  margin-bottom: 20px;
}
```

### 关键词标签组（封面用）
```css
.keyword-tags {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 30px 0;
}
.keyword-tag {
  font-size: 22px;
  color: #5A5A5A;
  letter-spacing: 4px;
  padding: 8px 20px;
  border: 1px solid rgba(193, 95, 60, 0.3);
  border-radius: 4px;
}
```

### 橙色主题标签（封面用）
```css
.theme-tag {
  display: inline-block;
  font-size: 20px;
  font-weight: 500;
  color: #fff;
  background: #C15F3C;
  padding: 8px 20px;
  letter-spacing: 4px;
  margin-bottom: 30px;
}
```

### 底部引用（所有页面）
```css
.bottom-quote {
  position: absolute;
  bottom: 55px;  /* 紧凑底部留白 */
  left: 80px;
  right: 80px;
  text-align: center;
  font-size: 20px;
  color: #9A958A;
  letter-spacing: 2px;
}
```

### 重点词高亮（必须使用）
```css
.accent { color: #C15F3C; }
```
**规则**：每个页面至少1个重点词使用 `.accent` 高亮，封面标题和内容页正文都需要呼应

---

## 封面模板

```html
<!-- [STYLE: 杂志分栏风] [TYPE: cover] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body { color-scheme: light only; background: #FAF6F1; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .poster {
      width: 1080px;
      height: 1440px;
      position: relative;
      background: #FAF6F1;
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .header {
      position: absolute;
      top: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .tag { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .zodiac-icon svg { width: 44px; height: 44px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }
    .side-line {
      position: absolute;
      top: 200px;
      right: 60px;
      width: 3px;
      height: 120px;
      background: linear-gradient(180deg, #C15F3C 0%, rgba(193, 95, 60, 0.3) 100%);
    }
    .main {
      position: absolute;
      top: 200px;
      left: 80px;
      right: 120px;
      z-index: 10;
    }
    .theme-tag {
      display: inline-block;
      font-size: 20px;
      font-weight: 500;
      color: #fff;
      background: #C15F3C;
      padding: 8px 20px;
      letter-spacing: 4px;
      margin-bottom: 30px;
    }
    .main-title {
      font-size: 72px;
      font-weight: 600;
      color: #3D3D3D;
      letter-spacing: 4px;
      line-height: 1.4;
      margin-bottom: 50px;
    }
    .accent { color: #C15F3C; }
    .keyword-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      margin-bottom: 60px;
    }
    .keyword-tag {
      font-size: 22px;
      color: #5A5A5A;
      letter-spacing: 4px;
      padding: 10px 24px;
      border: 1px solid rgba(193, 95, 60, 0.3);
      border-radius: 4px;
    }
    .sub-title {
      font-size: 28px;
      font-weight: 400;
      color: #5A5A5A;
      letter-spacing: 2px;
      line-height: 1.8;
    }
    .bottom-quote {
      position: absolute;
      bottom: 55px;
      left: 80px;
      right: 80px;
      text-align: left;
      font-size: 18px;
      color: #9A958A;
      letter-spacing: 2px;
    }
    .footer {
      position: absolute;
      bottom: 30px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      z-index: 10;
    }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 2px; }
  </style>
</head>
<body>
  <div class="poster">
    <div class="side-line"></div>
    <div class="header">
      <span class="tag">{{ZODIAC}} · {{THEME_LABEL}}</span>
      <div class="zodiac-icon">{{ZODIAC_SVG}}</div>
    </div>
    <div class="main">
      <div class="theme-tag">{{THEME_TAG}}</div>
      <h1 class="main-title">{{ZODIAC}}<br/>{{TITLE_LINE1}}<span class="accent">{{TITLE_ACCENT}}</span></h1>
      <div class="keyword-tags">
        <span class="keyword-tag">{{KEYWORD_1}}</span>
        <span class="keyword-tag">{{KEYWORD_2}}</span>
        <span class="keyword-tag">{{KEYWORD_3}}</span>
        <span class="keyword-tag">{{KEYWORD_4}}</span>
      </div>
      <p class="sub-title">{{SUB_TITLE}}</p>
    </div>
    <div class="bottom-quote">「 {{QUOTE}} 」</div>
    <div class="footer">
      <span class="page-num">01</span>
    </div>
  </div>
</body>
</html>
```

**封面变量说明**：
| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC}}` | 星座名称 | 射手座 |
| `{{THEME_LABEL}}` | 顶部主题标签 | 职业指南 |
| `{{ZODIAC_SVG}}` | 星座SVG图标 | `<svg>...</svg>` |
| `{{THEME_TAG}}` | 橙色主题标签 | 职业规划 |
| `{{TITLE_LINE1}}` | 标题第一部分 | 更适合的 |
| `{{TITLE_ACCENT}}` | 标题重点词（橙色） | 职业方向 |
| `{{KEYWORD_1-4}}` | 关键词标签 | 空间、变化、自主、探索 |
| `{{SUB_TITLE}}` | 副标题 | 选择让自己更像自己的工作 |
| `{{QUOTE}}` | 底部引用 | 对的方向，比努力更重要 |

---

## 内容页模板

```html
<!-- [STYLE: 杂志分栏风] [TYPE: page] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body { color-scheme: light only; background: #FAF6F1; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .poster {
      width: 1080px;
      height: 1440px;
      position: relative;
      background: #FAF6F1;
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .header {
      position: absolute;
      top: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .tag { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .zodiac-icon svg { width: 44px; height: 44px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }
    .side-line {
      position: absolute;
      top: 200px;
      right: 60px;
      width: 3px;
      height: 120px;
      background: linear-gradient(180deg, #C15F3C 0%, rgba(193, 95, 60, 0.3) 100%);
    }
    .main {
      position: absolute;
      top: 180px;
      left: 80px;
      right: 120px;
      z-index: 10;
    }
    .part-number {
      font-size: 18px;
      font-weight: 400;
      color: #C15F3C;
      letter-spacing: 4px;
      margin-bottom: 20px;
    }
    .section-title {
      font-size: 56px;
      font-weight: 600;
      color: #3D3D3D;
      letter-spacing: 4px;
      margin-bottom: 80px;
    }
    .content {
      font-size: 32px;
      font-weight: 400;
      color: #3D3D3D;
      letter-spacing: 2px;
      line-height: 2.2;
    }
    .content p {
      margin-bottom: 40px;
    }
    .accent { color: #C15F3C; }
    .bottom-quote {
      position: absolute;
      bottom: 55px;
      left: 80px;
      right: 80px;
      text-align: left;
      font-size: 18px;
      color: #9A958A;
      letter-spacing: 2px;
    }
    .footer {
      position: absolute;
      bottom: 30px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      z-index: 10;
    }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 2px; }
  </style>
</head>
<body>
  <div class="poster">
    <div class="side-line"></div>
    <div class="header">
      <span class="tag">{{ZODIAC}} · {{THEME_LABEL}}</span>
      <div class="zodiac-icon">{{ZODIAC_SVG}}</div>
    </div>
    <div class="main">
      <div class="part-number">PART {{PART_NUM}}</div>
      <h2 class="section-title">{{SECTION_TITLE}}</h2>
      <div class="content">
        {{CONTENT}}
        <!-- 正文中必须包含 <span class="accent">重点词</span> -->
      </div>
    </div>
    <div class="bottom-quote">「 {{QUOTE}} 」</div>
    <div class="footer">
      <span class="page-num">{{PAGE_NUM}}</span>
    </div>
  </div>
</body>
</html>
```

**内容页变量说明**：
| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC}}` | 星座名称 | 射手座 |
| `{{THEME_LABEL}}` | 顶部主题标签 | 职业指南 |
| `{{ZODIAC_SVG}}` | 星座SVG图标 | `<svg>...</svg>` |
| `{{PART_NUM}}` | 章节编号 | 01、02、03... |
| `{{SECTION_TITLE}}` | 章节标题 | 空间与变化 |
| `{{CONTENT}}` | 正文内容（含accent标签） | `<p>...</p>` |
| `{{QUOTE}}` | 底部引用 | 不自由，毋宁死 |
| `{{PAGE_NUM}}` | 页码 | 02、03、04... |

---

## 尾页模板

```html
<!-- [STYLE: 杂志分栏风] [TYPE: end] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root, html, body { color-scheme: light only; background: #FAF6F1; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .poster {
      width: 1080px;
      height: 1440px;
      position: relative;
      background: #FAF6F1;
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .header {
      position: absolute;
      top: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .tag { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .zodiac-icon svg { width: 44px; height: 44px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }
    .side-line {
      position: absolute;
      top: 200px;
      right: 60px;
      width: 3px;
      height: 120px;
      background: linear-gradient(180deg, #C15F3C 0%, rgba(193, 95, 60, 0.3) 100%);
    }
    .main {
      position: absolute;
      top: 180px;
      left: 80px;
      right: 120px;
      z-index: 10;
    }
    .part-number {
      font-size: 18px;
      font-weight: 400;
      color: #C15F3C;
      letter-spacing: 4px;
      margin-bottom: 20px;
    }
    .section-title {
      font-size: 56px;
      font-weight: 600;
      color: #3D3D3D;
      letter-spacing: 4px;
      margin-bottom: 80px;
    }
    .content {
      font-size: 32px;
      font-weight: 400;
      color: #3D3D3D;
      letter-spacing: 2px;
      line-height: 2.2;
      text-align: center;
    }
    .accent { color: #C15F3C; }
    .bottom-quote {
      position: absolute;
      bottom: 55px;
      left: 80px;
      right: 80px;
      text-align: center;
      font-size: 18px;
      color: #9A958A;
      letter-spacing: 2px;
    }
    .footer {
      position: absolute;
      bottom: 30px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      z-index: 10;
    }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 2px; }
  </style>
</head>
<body>
  <div class="poster">
    <div class="side-line"></div>
    <div class="header">
      <span class="tag">{{ZODIAC}} · {{THEME_LABEL}}</span>
      <div class="zodiac-icon">{{ZODIAC_SVG}}</div>
    </div>
    <div class="main">
      <div class="part-number">PART {{PART_NUM}}</div>
      <h2 class="section-title">{{SECTION_TITLE}}</h2>
      <div class="content">
        {{CONTENT}}
        <!-- 尾页正文必须包含 <span class="accent">重点词</span> 呼应封面 -->
      </div>
    </div>
    <div class="bottom-quote">「 {{QUOTE}} 」</div>
    <div class="footer">
      <span class="page-num">{{PAGE_NUM}}</span>
    </div>
  </div>
</body>
</html>
```

**尾页变量说明**：与内容页相同，但尾页的 `{{CONTENT}}` 通常为总结性文字，居中显示

---

## 生成规则

### 1. 重点词高亮规则（必须遵守）

**每页必须有至少1个重点词使用 `.accent` 高亮**

| 页面类型 | 重点词要求 | 示例 |
|----------|-----------|------|
| 封面 | 标题中1个核心词 | `<span class="accent">职业方向</span>` |
| 内容页 | 正文中1-2个关键词 | `<span class="accent">空间与变化</span>` |
| 尾页 | 总结词呼应封面 | `<span class="accent">更像自己</span>` |

**重点词选择原则**：
- 封面重点词 = 标题核心概念
- 内容页重点词 = 当页核心观点
- 尾页重点词 = 呼应封面或总结升华

### 2. 行尾排版规则（必须遵守）

**禁止标点符号作为每行的结尾**

| 错误 | 正确 |
|------|------|
| `射手对工作的核心诉求是，` | `射手对工作的核心诉求是` |
| `空间与变化。` | `空间与变化` |

### 3. 内容页 PART 编号规则

- 封面页：无 PART 编号
- 内容页：从 `PART 01` 开始递增
- 尾页：使用最后一个 PART 编号

### 4. 页码规则

- 封面：`01`
- 内容页：从 `02` 开始递增
- 页码位置：右下角

### 5. 关键词标签使用

- 仅封面使用 `.keyword-tags`
- 标签数量：3-5 个
- 内容：与主题相关的关键概念

### 6. 底部引用规则

- 每页必须有底部引用
- 格式：`「 引用内容 」`
- 内容：与当页内容相关的金句

---

## 检查清单

生成后检查：

- [ ] 背景是否为纯色 `#FAF6F1`（无渐变、无噪点）
- [ ] 右侧橙色竖线是否存在
- [ ] 内容页是否有 `PART 0X` 编号
- [ ] 行尾是否有标点符号（不应有）
- [ ] 底部引用是否存在
- [ ] 页码是否正确递增
- [ ] **每页是否有 `.accent` 重点词高亮**
- [ ] **封面与尾页重点词是否呼应**
- [ ] 底部留白是否紧凑（bottom-quote: 55px, footer: 30px）
