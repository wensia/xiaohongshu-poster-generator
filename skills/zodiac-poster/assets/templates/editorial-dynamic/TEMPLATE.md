# 动态编辑风 (Editorial Dynamic) 封面模板规范

---

## ⚠️ 强制品牌约束（必须遵守，不可修改）

### 核心配色（Claude VI 官方配色）

| 用途 | 色值 | 说明 |
|------|------|------|
| **强调色** | `#C15F3C` | 图标、关键词、强调文字、装饰线 |
| **弱化色** | `#B1ADA1` / `#9A958A` | 标签、页码、辅助文字 |
| **深色文字** | `#3D3D3D` | 主标题、正文 |
| **背景浅端** | `#FAF6F1` | 渐变背景起点 |
| **背景深端** | `#F0E6D9` | 渐变背景终点 |

> **🚫 绝对禁止**：使用 `#2C3E50`（藏青）、`#E74C3C`（红色）、`#6B8E7B`（绿色）、`#C5A572`（金色）等非规范配色！

### 星座图标（必须使用 SVG 线性图标）

```
🚫 禁止：使用 emoji 图标（♐ ♈ ♉ ♊ ♋ 等）
✅ 必须：从 zodiac-symbols.json 获取 SVG 代码
```

**图标样式规范**：
```css
.zodiac-icon svg {
  stroke: #C15F3C;      /* 必须使用强调色 */
  stroke-width: 1.5;    /* 线条粗细 */
  fill: none;           /* 必须无填充 */
}
```

**射手座图标示例**（从 zodiac-symbols.json 获取）：
```html
<div class="zodiac-icon">
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <line x1="20" y1="80" x2="80" y2="20" stroke-linecap="round"/>
    <line x1="80" y1="20" x2="55" y2="20" stroke-linecap="round"/>
    <line x1="80" y1="20" x2="80" y2="45" stroke-linecap="round"/>
    <line x1="25" y1="45" x2="55" y2="75" stroke-linecap="round"/>
  </svg>
</div>
```

### 各风格包的差异边界

**只允许差异的部分**：
- 边框样式（实线/双线/无边框/镂空）
- 装饰元素形状（圆形/方形/星星/引号）
- 关键词呈现方式（色块填充/边框/双线/镂空）

**绝对不允许修改**：
- 强调色（必须 `#C15F3C`）
- 弱化色（必须 `#B1ADA1` 或 `#9A958A`）
- 背景渐变色
- 图标颜色和样式

---

## 核心规则：风格与布局双锁定系统

### 为什么需要双锁定？

生成套图（封面 + 多页内容页）时，**所有页面必须使用同一风格包 + 同一布局变体**，确保视觉一致性。

### 双锁定系统

| 锁定项 | 说明 | 选项 |
|--------|------|------|
| **STYLE LOCK** | 风格包锁定 | 经典强调 / 简约边框 / 杂志双线 / 艺术镂空 |
| **LAYOUT LOCK** | 布局变体锁定 | A / B / C / D / E |

### 如何使用双锁定？

1. **生成套图前**：从 4 个风格包中随机选择 1 个 + 从 5 个布局变体中随机选择 1 个
2. **生成第一页时**：在 HTML 开头添加双锁定注释
3. **生成后续页面时**：查看已有页面的双锁定注释，使用相同的风格包和布局变体

```html
<!-- [STYLE LOCK: 经典强调] [LAYOUT LOCK: B] -->
<!-- 本套图所有页面必须使用此风格和布局 -->
<!DOCTYPE html>
...
```

> **⚠️ 绝对禁止**：同一套图混用不同的风格包或布局变体！

---

## 画布尺寸与基础设置

**尺寸**：1080px × 1440px（3:4 比例）

### 通用基础样式（所有风格包共用）

```css
/* 强制浅色模式，防止系统深色模式影响背景颜色 */
:root, html, body {
  color-scheme: light only;
  background: #FAF6F1;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

.poster {
  width: 1080px;
  height: 1440px;
  position: relative;
  background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%);
  font-family: 'Noto Serif SC', serif;
  overflow: hidden;
}

/* 纸张纹理 */
.poster::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.05;
  pointer-events: none;
  z-index: 1;
}

/* 顶部标签区 */
.header {
  position: absolute;
  top: 70px;
  left: 80px;
  right: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.tag {
  font-size: 22px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 6px;
}

/* 底部信息区 */
.footer {
  position: absolute;
  bottom: 70px;
  left: 80px;
  right: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.footer-text {
  font-size: 20px;
  color: #B1ADA1;
  letter-spacing: 4px;
}

.page-num {
  font-size: 24px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 4px;
}

/* 重点色强调 */
.accent {
  color: #C15F3C;
  font-weight: 500;
}

/* 文字高亮下划线 */
.highlight {
  position: relative;
  display: inline;
}
.highlight::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 0;
  right: 0;
  height: 10px;
  background: rgba(193, 95, 60, 0.2);
  z-index: -1;
}

/* 底部渐变色带（可选） */
.gradient-band {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
}
```

### 星座图标（根据星座替换）

```html
<!-- 双子座 -->
<div class="zodiac-icon">
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <line x1="25" y1="20" x2="75" y2="20" stroke-linecap="round"/>
    <line x1="25" y1="80" x2="75" y2="80" stroke-linecap="round"/>
    <line x1="35" y1="20" x2="35" y2="80" stroke-linecap="round"/>
    <line x1="65" y1="20" x2="65" y2="80" stroke-linecap="round"/>
  </svg>
</div>
```

```css
.zodiac-icon svg {
  width: 48px;
  height: 48px;
  stroke: #C15F3C;
  stroke-width: 1.5;
  fill: none;
}
```

---

# 风格包 1：经典强调

**特征**：色块填充关键词 + 大字号背景装饰 + 圆形装饰
**适用**：年运势、重要预测、正式内容

## 风格锁定标记

```html
<!-- [STYLE LOCK: 经典强调] -->
```

## 完整CSS

```css
/* === 经典强调风格 === */

/* 关键词：色块填充 */
.keyword {
  display: inline-block;
  width: fit-content;
  background: linear-gradient(135deg, #C15F3C 0%, #D4765A 100%);
  color: #fff;
  font-size: 36px;
  font-weight: 500;
  letter-spacing: 8px;
  padding: 14px 32px;
  border-radius: 2px;
  margin-bottom: 50px;
}

/* 封面星座醒目标识区（封面专用） */
.zodiac-header {
  position: absolute;
  top: 180px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  z-index: 10;
}
.zodiac-icon-large svg {
  width: 80px;
  height: 80px;
  stroke: #C15F3C;
  stroke-width: 2;
  fill: none;
  margin-bottom: 20px;
}
.zodiac-name {
  font-size: 72px;
  font-weight: 700;
  color: #C15F3C;
  letter-spacing: 16px;
  margin-bottom: 10px;
}
.zodiac-year {
  font-size: 28px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 8px;
}

/* 星座背景大字（封面专用） */
.zodiac-bg {
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 180px;
  font-weight: 700;
  color: rgba(193, 95, 60, 0.08);
  letter-spacing: 20px;
  z-index: 0;
  white-space: nowrap;
}

/* 装饰：大字号背景 */
.year-bg {
  position: absolute;
  top: 180px;
  left: -60px;
  font-size: 320px;
  font-weight: 700;
  color: rgba(193, 95, 60, 0.06);
  letter-spacing: -20px;
  z-index: 0;
}

/* 装饰：圆形装饰 */
.circle-deco {
  position: absolute;
  width: 180px;
  height: 180px;
  border: 2px solid rgba(193, 95, 60, 0.15);
  border-radius: 50%;
}
.circle-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: rgba(193, 95, 60, 0.08);
  border-radius: 50%;
}

/* 主内容区 */
.main {
  position: absolute;
  top: 50%;
  left: 80px;
  right: 80px;
  transform: translateY(-50%);
  z-index: 10;
  text-align: center;
}

/* 封面主标题 */
.main-title {
  font-size: 80px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 6px;
  line-height: 1.4;
  margin-bottom: 40px;
}

/* 副标题 */
.sub-title {
  font-size: 36px;
  font-weight: 400;
  color: #5A5A5A;
  letter-spacing: 4px;
  margin-bottom: 50px;
}

/* 引用语 */
.quote {
  font-size: 26px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
  font-style: italic;
}

/* 内容页正文 */
.content {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  line-height: 2;
  letter-spacing: 2px;
  text-align: justify;
}
```

## 封面模板

> **🔴 封面必须包含至少 2 个重点色词（accent），形成视觉呼应！这是最常见的错误！**

```html
<!-- [STYLE LOCK: 经典强调] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入经典强调风格CSS */

    /* 封面专用：主内容区下移，为星座标识留空间 */
    .main {
      top: 520px;
      transform: none;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 星座背景大字 -->
    <div class="zodiac-bg">射手座</div>

    <!-- 装饰：圆形 -->
    <div class="circle-deco" style="top: 140px; right: 80px; width: 100px; height: 100px;">
      <div class="circle-inner" style="width: 50px; height: 50px;"></div>
    </div>

    <div class="header">
      <span class="tag">2026 新年愿望</span>
      <span class="tag">SAGITTARIUS</span>
    </div>

    <!-- 醒目的星座标识（封面核心元素） -->
    <div class="zodiac-header">
      <div class="zodiac-icon-large">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <!-- 射手座SVG -->
          <line x1="20" y1="80" x2="80" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="55" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="80" y2="45" stroke-linecap="round"/>
          <line x1="25" y1="45" x2="55" y2="75" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="zodiac-name">射手座</div>
      <div class="zodiac-year">2026</div>
    </div>

    <!-- 🔴 主内容区：必须包含至少2个accent词！ -->
    <div class="main">
      <div class="keyword">新年愿望</div>
      <!-- ✅ 正确：主标题包含2个accent词，形成对比呼应 -->
      <h1 class="main-title">少一点<span class="accent">期待</span><br/>多一点<span class="accent">随缘</span></h1>
      <p class="sub-title">射手座的2026新年愿望</p>
      <p class="quote">「 期望越少，惊喜越多 」</p>
    </div>

    <div class="footer">
      <span class="footer-text">射手座2026新年愿望</span>
      <span class="page-num">01</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 🔴 封面重点色词规则（必须遵守！）

| 检查项 | 要求 |
|--------|------|
| accent词数量 | **至少2个** |
| 分布位置 | 主标题1-2个 + 副标题0-1个 |
| 词语选择 | 核心情感词、对比词（非虚词） |
| 视觉效果 | 形成上下呼应 |

**常见正确模式：**
```html
<!-- 模式1：主标题两行各1个 -->
<h1>少一点<span class="accent">期待</span><br/>多一点<span class="accent">随缘</span></h1>

<!-- 模式2：主标题1个 + 副标题1个 -->
<h1>不是<span class="accent">孤独</span></h1>
<p class="sub-title">是事事都要报备的<span class="accent">窒息感</span></p>

<!-- 模式3：主标题2个对比词 -->
<h1>来的都<span class="accent">欢迎</span><br/>走的不<span class="accent">强留</span></h1>
```

## 内容页布局变体

> **⚠️ 核心规则**：同一套图的所有内容页必须使用相同的布局变体！生成套图前先确定一个布局变体（A/B/C/D/E），然后所有内容页都使用这个布局。禁止在同一套图中混用不同布局变体。

### 变体 A：色块标题居中式

```html
<!-- [STYLE LOCK: 经典强调] [LAYOUT: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入经典强调风格CSS */

    .main {
      position: absolute;
      top: 50%;
      left: 80px;
      right: 80px;
      transform: translateY(-50%);
      z-index: 10;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="year-bg">2026</div>
    <div class="circle-deco" style="top: 180px; right: 80px; width: 120px; height: 120px;">
      <div class="circle-inner" style="width: 60px; height: 60px;"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main">
      <div class="keyword">小标题</div>
      <p class="content">
        正文内容第一段。<br/><br/>
        正文内容第二段，<br/>
        包含<span class="accent">强调词</span>。<br/><br/>
        正文内容第三段，<br/>
        可以使用<span class="highlight">高亮文字</span>。
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 B：杂志章节式（PART XX + 大标题左对齐）

```html
<!-- [STYLE LOCK: 经典强调] [LAYOUT: B] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入经典强调风格CSS */

    /* 变体B专用样式 */
    .part-label {
      font-size: 22px;
      font-weight: 500;
      color: #C15F3C;
      letter-spacing: 8px;
      margin-bottom: 16px;
    }
    .section-title {
      font-size: 56px;
      font-weight: 700;
      color: #2D2D2D;
      letter-spacing: 4px;
      line-height: 1.3;
      margin-bottom: 80px;
    }
    .main-b {
      position: absolute;
      top: 160px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .content-b {
      font-size: 32px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: left;
    }
    .quote-line {
      display: flex;
      align-items: stretch;
      margin-top: 60px;
    }
    .quote-bar {
      width: 4px;
      background: #C15F3C;
      margin-right: 24px;
      flex-shrink: 0;
    }
    .quote-text {
      font-size: 28px;
      font-weight: 400;
      color: #9A958A;
      line-height: 1.8;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="tag">射手座 · 2026运势</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-b">
      <div class="part-label">PART 01</div>
      <h2 class="section-title">好运终于来了</h2>
      <p class="content-b">
        2026年，木星进入射手的福位，属于你的<span class="accent">好运终于来了</span>。<br/><br/>
        过去那些被压着的、憋着的、等着的——都要开始<span class="accent">兑现了</span>。
      </p>
      <div class="quote-line">
        <div class="quote-bar"></div>
        <p class="quote-text">"保持行动感，运气自然来"</p>
      </div>
    </div>

    <div class="footer">
      <span class="footer-text">2026 射手座运势</span>
      <span class="page-num">02</span>
    </div>
  </div>
</body>
</html>
```

### 变体 C：数字序号引导式

```html
<!-- [STYLE LOCK: 经典强调] [LAYOUT: C] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入经典强调风格CSS */

    /* 变体C专用样式 */
    .number-lead {
      position: absolute;
      top: 180px;
      left: 80px;
      font-size: 180px;
      font-weight: 700;
      color: rgba(193, 95, 60, 0.12);
      line-height: 1;
    }
    .main-c {
      position: absolute;
      top: 280px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .section-keyword {
      font-size: 42px;
      font-weight: 600;
      color: #C15F3C;
      letter-spacing: 6px;
      margin-bottom: 50px;
    }
    .content-c {
      font-size: 32px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="number-lead">02</div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-c">
      <h2 class="section-keyword">感情运势</h2>
      <p class="content-c">
        单身的双子座今年桃花运旺盛，<br/>
        特别是<span class="accent">下半年</span>会有不错的机会。<br/><br/>
        有伴的双子座则要注意沟通，<br/>
        <span class="highlight">真诚比技巧更重要</span>。
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 D：引用突出式（大引号开头）

```html
<!-- [STYLE LOCK: 经典强调] [LAYOUT: D] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入经典强调风格CSS */

    /* 变体D专用样式 */
    .big-quote {
      position: absolute;
      top: 140px;
      left: 60px;
      font-size: 200px;
      font-family: Georgia, serif;
      color: rgba(193, 95, 60, 0.1);
      line-height: 1;
    }
    .main-d {
      position: absolute;
      top: 300px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .lead-text {
      font-size: 40px;
      font-weight: 500;
      color: #3D3D3D;
      line-height: 1.8;
      letter-spacing: 3px;
      margin-bottom: 50px;
    }
    .content-d {
      font-size: 30px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2;
      letter-spacing: 2px;
    }
    .end-mark {
      display: inline-block;
      width: 8px;
      height: 8px;
      background: #C15F3C;
      border-radius: 50%;
      margin-left: 12px;
      vertical-align: middle;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="big-quote">"</div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-d">
      <p class="lead-text">
        不再为不值得的人消耗情绪，<br/>
        不再为无意义的事浪费时间。
      </p>
      <p class="content-d">
        你来，我<span class="accent">热情相迎</span>；<br/>
        你走，我<span class="accent">安然独处</span>。<br/><br/>
        这一年的双子，<br/>
        会更懂<span class="highlight">"不勉强"的智慧</span>。<span class="end-mark"></span>
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">03</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 E：分栏对比式

```html
<!-- [STYLE LOCK: 经典强调] [LAYOUT: E] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入经典强调风格CSS */

    /* 变体E专用样式 */
    .main-e {
      position: absolute;
      top: 200px;
      left: 80px;
      right: 80px;
      z-index: 10;
    }
    .topic-row {
      display: flex;
      align-items: flex-start;
      margin-bottom: 60px;
    }
    .topic-label {
      width: 140px;
      flex-shrink: 0;
      font-size: 24px;
      font-weight: 500;
      color: #C15F3C;
      letter-spacing: 4px;
      padding-top: 8px;
      border-top: 2px solid #C15F3C;
    }
    .topic-content {
      flex: 1;
      font-size: 30px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2;
      letter-spacing: 2px;
      padding-left: 40px;
    }
    .divider {
      width: 100%;
      height: 1px;
      background: rgba(193, 95, 60, 0.15);
      margin: 40px 0;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-e">
      <div class="topic-row">
        <div class="topic-label">事业</div>
        <p class="topic-content">
          事业上会有<span class="accent">惊喜</span>。<br/>
          那些看似随意的连接，<br/>
          可能带来意想不到的机会。
        </p>
      </div>
      <div class="divider"></div>
      <div class="topic-row">
        <div class="topic-label">财运</div>
        <p class="topic-content">
          财运稳中有升，<br/>
          <span class="highlight">下半年尤为明显</span>。<br/>
          适合稳健投资，不宜冒进。
        </p>
      </div>
      <div class="divider"></div>
      <div class="topic-row">
        <div class="topic-label">健康</div>
        <p class="topic-content">
          注意作息规律，<br/>
          给大脑足够的<span class="accent">休息时间</span>。
        </p>
      </div>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">04</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

---

# 风格包 2：简约边框

**特征**：边框线条关键词 + 角标装饰 + 底部色带
**适用**：规则清单、指南类、简洁内容

## 风格锁定标记

```html
<!-- [STYLE LOCK: 简约边框] -->
```

## 完整CSS

```css
/* === 简约边框风格 === */

/* 关键词：边框线条 */
.keyword {
  display: inline-block;
  width: fit-content;
  font-size: 36px;
  font-weight: 500;
  color: #C15F3C;
  letter-spacing: 8px;
  padding: 12px 28px;
  border: 2px solid #C15F3C;
  border-radius: 2px;
  margin-bottom: 50px;
}

/* 封面星座醒目标识区（封面专用） */
.zodiac-header {
  position: absolute;
  top: 180px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  z-index: 10;
}
.zodiac-icon-large svg {
  width: 80px;
  height: 80px;
  stroke: #C15F3C;
  stroke-width: 2;
  fill: none;
  margin-bottom: 20px;
}
.zodiac-name {
  font-size: 72px;
  font-weight: 700;
  color: #C15F3C;
  letter-spacing: 16px;
  margin-bottom: 10px;
}
.zodiac-year {
  font-size: 28px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 8px;
}

/* 星座背景大字（封面专用） */
.zodiac-bg {
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 180px;
  font-weight: 700;
  color: rgba(193, 95, 60, 0.08);
  letter-spacing: 20px;
  z-index: 0;
  white-space: nowrap;
}

/* 装饰：角标 */
.corner-bracket {
  position: absolute;
  width: 60px;
  height: 60px;
  border: 2px solid rgba(193, 95, 60, 0.2);
}
.corner-bracket.top-left {
  top: 140px;
  left: 70px;
  border-right: none;
  border-bottom: none;
}
.corner-bracket.top-right {
  top: 140px;
  right: 70px;
  border-left: none;
  border-bottom: none;
}
.corner-bracket.bottom-left {
  bottom: 140px;
  left: 70px;
  border-right: none;
  border-top: none;
}
.corner-bracket.bottom-right {
  bottom: 140px;
  right: 70px;
  border-left: none;
  border-top: none;
}

/* 装饰：竖线组 */
.side-lines {
  position: absolute;
  left: 60px;
  top: 300px;
}
.side-line {
  width: 3px;
  background: #C15F3C;
  margin-bottom: 12px;
}
.side-line:nth-child(1) { height: 120px; }
.side-line:nth-child(2) { height: 80px; opacity: 0.6; }
.side-line:nth-child(3) { height: 50px; opacity: 0.3; }

/* 主内容区 */
.main {
  position: absolute;
  top: 50%;
  left: 80px;
  right: 80px;
  transform: translateY(-50%);
  z-index: 10;
  text-align: center;
}

/* 封面主标题 */
.main-title {
  font-size: 80px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 6px;
  line-height: 1.4;
  margin-bottom: 40px;
}

/* 副标题 */
.sub-title {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  letter-spacing: 4px;
  margin-bottom: 50px;
}

/* 引用语 */
.quote {
  font-size: 26px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
  font-style: italic;
}

/* 内容页正文 */
.content {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  line-height: 2;
  letter-spacing: 2px;
  text-align: justify;
}
```

## 封面模板

```html
<!-- [STYLE LOCK: 简约边框] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入简约边框风格CSS */

    /* 封面专用：主内容区下移 */
    .main {
      top: 520px;
      transform: none;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 星座背景大字 -->
    <div class="zodiac-bg">双子座</div>

    <!-- 装饰：角标 -->
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket bottom-right"></div>

    <div class="header">
      <span class="tag">2026 年度运势</span>
      <span class="tag">GEMINI</span>
    </div>

    <!-- 醒目的星座标识 -->
    <div class="zodiac-header">
      <div class="zodiac-icon-large">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <line x1="20" y1="15" x2="80" y2="15" stroke-linecap="round"/>
          <line x1="20" y1="85" x2="80" y2="85" stroke-linecap="round"/>
          <line x1="35" y1="15" x2="35" y2="85" stroke-linecap="round"/>
          <line x1="65" y1="15" x2="65" y2="85" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="zodiac-name">双子座</div>
      <div class="zodiac-year">2026</div>
    </div>

    <div class="main">
      <div class="keyword">关键词</div>
      <h1 class="main-title">主标题<br/><span class="accent">强调词</span></h1>
      <p class="quote">「 引用金句 」</p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">01</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

## 内容页布局变体

> **⚠️ 核心规则**：同一套图的所有内容页必须使用相同的布局变体！生成套图前先确定一个布局变体（A/B/C/D/E），然后所有内容页都使用这个布局。禁止在同一套图中混用不同布局变体。

### 变体 A：色块标题居中式

```html
<!-- [STYLE LOCK: 简约边框] [LAYOUT: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入简约边框风格CSS */

    /* 内容页布局调整 */
    .main {
      top: 300px;
      transform: none;
      text-align: left;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：竖线组 -->
    <div class="side-lines">
      <div class="side-line"></div>
      <div class="side-line"></div>
      <div class="side-line"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main">
      <div class="keyword">小标题</div>
      <p class="content">
        正文内容第一段。<br/><br/>
        正文内容第二段，<br/>
        包含<span class="accent">强调词</span>。<br/><br/>
        正文内容第三段。
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 B：杂志章节式（PART XX + 大标题左对齐）

```html
<!-- [STYLE LOCK: 简约边框] [LAYOUT: B] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入简约边框风格CSS */

    /* 变体B专用样式 */
    .part-label {
      font-size: 22px;
      font-weight: 500;
      color: #C15F3C;
      letter-spacing: 8px;
      margin-bottom: 16px;
    }
    .section-title {
      font-size: 56px;
      font-weight: 700;
      color: #2D2D2D;
      letter-spacing: 4px;
      line-height: 1.3;
      margin-bottom: 80px;
    }
    .main-b {
      position: absolute;
      top: 160px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .content-b {
      font-size: 32px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: left;
    }
    .quote-line {
      display: flex;
      align-items: stretch;
      margin-top: 60px;
    }
    .quote-bar {
      width: 4px;
      background: #C15F3C;
      margin-right: 24px;
      flex-shrink: 0;
    }
    .quote-text {
      font-size: 28px;
      font-weight: 400;
      color: #9A958A;
      line-height: 1.8;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：角标 -->
    <div class="corner-bracket top-right"></div>
    <div class="corner-bracket bottom-left"></div>

    <div class="header">
      <span class="tag">双子座 · 2026运势</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-b">
      <div class="part-label">PART 01</div>
      <h2 class="section-title">好运终于来了</h2>
      <p class="content-b">
        2026年，木星进入射手的福位，属于你的<span class="accent">好运终于来了</span>。<br/><br/>
        过去那些被压着的、憋着的、等着的——都要开始<span class="accent">兑现了</span>。
      </p>
      <div class="quote-line">
        <div class="quote-bar"></div>
        <p class="quote-text">"保持行动感，运气自然来"</p>
      </div>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">02</span>
    </div>
  </div>
</body>
</html>
```

### 变体 C：数字序号引导式

```html
<!-- [STYLE LOCK: 简约边框] [LAYOUT: C] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入简约边框风格CSS */

    /* 变体C专用样式 */
    .number-lead {
      position: absolute;
      top: 180px;
      left: 80px;
      font-size: 180px;
      font-weight: 700;
      color: rgba(193, 95, 60, 0.12);
      line-height: 1;
    }
    .main-c {
      position: absolute;
      top: 280px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .section-keyword {
      font-size: 42px;
      font-weight: 600;
      color: #C15F3C;
      letter-spacing: 6px;
      margin-bottom: 50px;
    }
    .content-c {
      font-size: 32px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="number-lead">02</div>

    <!-- 装饰：角标 -->
    <div class="corner-bracket top-right"></div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-c">
      <h2 class="section-keyword">感情运势</h2>
      <p class="content-c">
        单身的双子座今年桃花运旺盛，<br/>
        特别是<span class="accent">下半年</span>会有不错的机会。<br/><br/>
        有伴的双子座则要注意沟通，<br/>
        <span class="highlight">真诚比技巧更重要</span>。
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 D：引用突出式（大引号开头）

```html
<!-- [STYLE LOCK: 简约边框] [LAYOUT: D] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入简约边框风格CSS */

    /* 变体D专用样式 */
    .big-quote {
      position: absolute;
      top: 140px;
      left: 60px;
      font-size: 200px;
      font-family: Georgia, serif;
      color: rgba(193, 95, 60, 0.1);
      line-height: 1;
    }
    .main-d {
      position: absolute;
      top: 300px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .lead-text {
      font-size: 40px;
      font-weight: 500;
      color: #3D3D3D;
      line-height: 1.8;
      letter-spacing: 3px;
      margin-bottom: 50px;
    }
    .content-d {
      font-size: 30px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2;
      letter-spacing: 2px;
    }
    .end-mark {
      display: inline-block;
      width: 8px;
      height: 8px;
      background: #C15F3C;
      border-radius: 50%;
      margin-left: 12px;
      vertical-align: middle;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="big-quote">"</div>

    <!-- 装饰：竖线组 -->
    <div class="side-lines" style="top: 800px;">
      <div class="side-line"></div>
      <div class="side-line"></div>
      <div class="side-line"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-d">
      <p class="lead-text">
        不再为不值得的人消耗情绪，<br/>
        不再为无意义的事浪费时间。
      </p>
      <p class="content-d">
        你来，我<span class="accent">热情相迎</span>；<br/>
        你走，我<span class="accent">安然独处</span>。<br/><br/>
        这一年的双子，<br/>
        会更懂<span class="highlight">"不勉强"的智慧</span>。<span class="end-mark"></span>
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">03</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 E：分栏对比式

```html
<!-- [STYLE LOCK: 简约边框] [LAYOUT: E] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入简约边框风格CSS */

    /* 变体E专用样式 */
    .main-e {
      position: absolute;
      top: 200px;
      left: 80px;
      right: 80px;
      z-index: 10;
    }
    .topic-row {
      display: flex;
      align-items: flex-start;
      margin-bottom: 60px;
    }
    .topic-label {
      width: 140px;
      flex-shrink: 0;
      font-size: 24px;
      font-weight: 500;
      color: #C15F3C;
      letter-spacing: 4px;
      padding-top: 8px;
      border-top: 2px solid #C15F3C;
    }
    .topic-content {
      flex: 1;
      font-size: 30px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2;
      letter-spacing: 2px;
      padding-left: 40px;
    }
    .divider {
      width: 100%;
      height: 1px;
      background: rgba(193, 95, 60, 0.15);
      margin: 40px 0;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：角标 -->
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket bottom-right"></div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-e">
      <div class="topic-row">
        <div class="topic-label">事业</div>
        <p class="topic-content">
          事业上会有<span class="accent">惊喜</span>。<br/>
          那些看似随意的连接，<br/>
          可能带来意想不到的机会。
        </p>
      </div>
      <div class="divider"></div>
      <div class="topic-row">
        <div class="topic-label">财运</div>
        <p class="topic-content">
          财运稳中有升，<br/>
          <span class="highlight">下半年尤为明显</span>。<br/>
          适合稳健投资，不宜冒进。
        </p>
      </div>
      <div class="divider"></div>
      <div class="topic-row">
        <div class="topic-label">健康</div>
        <p class="topic-content">
          注意作息规律，<br/>
          给大脑足够的<span class="accent">休息时间</span>。
        </p>
      </div>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">04</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

---

# 风格包 3：杂志双线

**特征**：双线装饰关键词 + 双线边框 + 星星散布
**适用**：精致主题、专题类、高级感内容

## 风格锁定标记

```html
<!-- [STYLE LOCK: 杂志双线] -->
```

## 完整CSS

```css
/* === 杂志双线风格 === */

/* 关键词：双线装饰 */
.keyword {
  display: inline-block;
  width: fit-content;
  font-size: 36px;
  font-weight: 500;
  color: #3D3D3D;
  letter-spacing: 8px;
  padding: 12px 0;
  border-top: 1px solid rgba(193, 95, 60, 0.4);
  border-bottom: 1px solid rgba(193, 95, 60, 0.4);
  margin-bottom: 50px;
}

/* 封面星座醒目标识区（封面专用） */
.zodiac-header {
  position: absolute;
  top: 180px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  z-index: 10;
}
.zodiac-icon-large svg {
  width: 80px;
  height: 80px;
  stroke: #C15F3C;
  stroke-width: 2;
  fill: none;
  margin-bottom: 20px;
}
.zodiac-name {
  font-size: 72px;
  font-weight: 700;
  color: #C15F3C;
  letter-spacing: 16px;
  margin-bottom: 10px;
}
.zodiac-year {
  font-size: 28px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 8px;
}

/* 星座背景大字（封面专用） */
.zodiac-bg {
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 180px;
  font-weight: 700;
  color: rgba(193, 95, 60, 0.08);
  letter-spacing: 20px;
  z-index: 0;
  white-space: nowrap;
}

/* 装饰：双线边框 */
.double-border {
  position: absolute;
  top: 130px;
  left: 70px;
  right: 70px;
  bottom: 130px;
  border: 1px solid rgba(193, 95, 60, 0.1);
}
.double-border::before {
  content: '';
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border: 1px solid rgba(193, 95, 60, 0.05);
}

/* 双线边框角落变体 */
.double-border-corners .corner {
  position: absolute;
  width: 50px;
  height: 50px;
  border: 1px solid rgba(193, 95, 60, 0.15);
}
.double-border-corners .corner::before {
  content: '';
  position: absolute;
  top: 8px;
  left: 8px;
  width: 34px;
  height: 34px;
  border: 1px solid rgba(193, 95, 60, 0.08);
}
.corner.top-left { top: 140px; left: 70px; border-right: none; border-bottom: none; }
.corner.top-left::before { border-right: none; border-bottom: none; }
.corner.bottom-right { bottom: 140px; right: 70px; border-left: none; border-top: none; }
.corner.bottom-right::before { border-left: none; border-top: none; }

/* 装饰：星星散布 */
.stars-scatter {
  position: absolute;
  width: 180px;
  height: 180px;
}
.star {
  position: absolute;
  width: 10px;
  height: 10px;
  background: #C15F3C;
  clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}
.star:nth-child(1) { top: 20px; left: 30px; opacity: 0.35; }
.star:nth-child(2) { top: 60px; left: 130px; opacity: 0.5; transform: scale(0.7); }
.star:nth-child(3) { top: 100px; left: 50px; opacity: 0.25; transform: scale(1.1); }
.star:nth-child(4) { top: 30px; left: 150px; opacity: 0.4; transform: scale(0.5); }
.star:nth-child(5) { top: 140px; left: 100px; opacity: 0.3; }

/* 主内容区 */
.main {
  position: absolute;
  top: 50%;
  left: 80px;
  right: 80px;
  transform: translateY(-50%);
  z-index: 10;
  text-align: center;
}

/* 封面主标题 */
.main-title {
  font-size: 80px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 6px;
  line-height: 1.4;
  margin-bottom: 40px;
}

/* 副标题 */
.sub-title {
  font-size: 36px;
  font-weight: 400;
  color: #5A5A5A;
  letter-spacing: 4px;
  margin-bottom: 50px;
}

/* 引用语 */
.quote {
  font-size: 26px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
  font-style: italic;
}

/* 内容页正文 */
.content {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  line-height: 2;
  letter-spacing: 2px;
  text-align: justify;
}
```

## 封面模板

```html
<!-- [STYLE LOCK: 杂志双线] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入杂志双线风格CSS */

    /* 封面专用：主内容区下移 */
    .main {
      top: 520px;
      transform: none;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 星座背景大字 -->
    <div class="zodiac-bg">双子座</div>

    <!-- 装饰：双线边框 -->
    <div class="double-border"></div>

    <!-- 装饰：星星散布 -->
    <div class="stars-scatter" style="top: 160px; right: 100px;">
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
    </div>

    <div class="header">
      <span class="tag">2026 年度运势</span>
      <span class="tag">GEMINI</span>
    </div>

    <!-- 醒目的星座标识 -->
    <div class="zodiac-header">
      <div class="zodiac-icon-large">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <line x1="20" y1="15" x2="80" y2="15" stroke-linecap="round"/>
          <line x1="20" y1="85" x2="80" y2="85" stroke-linecap="round"/>
          <line x1="35" y1="15" x2="35" y2="85" stroke-linecap="round"/>
          <line x1="65" y1="15" x2="65" y2="85" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="zodiac-name">双子座</div>
      <div class="zodiac-year">2026</div>
    </div>

    <div class="main">
      <div class="keyword">关键词</div>
      <h1 class="main-title">主标题<br/><span class="accent">强调词</span></h1>
      <p class="quote">「 引用金句 」</p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">01</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

## 内容页布局变体

> **⚠️ 核心规则**：同一套图的所有内容页必须使用相同的布局变体！生成套图前先确定一个布局变体（A/B/C/D/E），然后所有内容页都使用这个布局。禁止在同一套图中混用不同布局变体。
>
> **🎯 总结页例外**：套图的**最后一页**必须使用 **Layout S（总结收尾式）**，内容居中呈现，与前面的布局变体无关。

### 变体 A：色块标题居中式

```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入杂志双线风格CSS */

    /* 内容页布局调整 */
    .main {
      top: 360px;
      transform: none;
      text-align: left;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：双线边框角落变体 -->
    <div class="double-border-corners">
      <div class="corner top-left"></div>
      <div class="corner bottom-right"></div>
    </div>

    <!-- 装饰：星星散布（位置变化） -->
    <div class="stars-scatter" style="top: 200px; left: 80px; width: 150px; height: 150px;">
      <div class="star" style="top: 20px; left: 35px; opacity: 0.3;"></div>
      <div class="star" style="top: 70px; left: 110px; opacity: 0.5; transform: scale(0.7);"></div>
      <div class="star" style="top: 100px; left: 55px; opacity: 0.2; transform: scale(1.1);"></div>
      <div class="star" style="top: 40px; left: 130px; opacity: 0.4; transform: scale(0.5);"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main">
      <div class="keyword">小标题</div>
      <p class="content">
        正文内容第一段。<br/><br/>
        正文内容第二段，<br/>
        包含<span class="accent">强调词</span>。<br/><br/>
        正文内容第三段，<br/>
        可以使用<span class="highlight">高亮文字</span>。
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 B：杂志章节式（PART XX + 大标题左对齐）

```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT: B] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入杂志双线风格CSS */

    /* 变体B专用样式 */
    .part-label {
      font-size: 22px;
      font-weight: 500;
      color: #C15F3C;
      letter-spacing: 8px;
      margin-bottom: 16px;
    }
    .section-title {
      font-size: 56px;
      font-weight: 700;
      color: #2D2D2D;
      letter-spacing: 4px;
      line-height: 1.3;
      margin-bottom: 80px;
    }
    .main-b {
      position: absolute;
      top: 160px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .content-b {
      font-size: 32px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: left;
    }
    .quote-line {
      display: flex;
      align-items: stretch;
      margin-top: 60px;
    }
    .quote-bar {
      width: 4px;
      background: #C15F3C;
      margin-right: 24px;
      flex-shrink: 0;
    }
    .quote-text {
      font-size: 28px;
      font-weight: 400;
      color: #9A958A;
      line-height: 1.8;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：双线边框 -->
    <div class="double-border"></div>

    <!-- 装饰：星星散布 -->
    <div class="stars-scatter" style="top: 120px; right: 100px;">
      <div class="star"></div>
      <div class="star"></div>
      <div class="star"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026运势</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-b">
      <div class="part-label">PART 01</div>
      <h2 class="section-title">好运终于来了</h2>
      <p class="content-b">
        2026年，木星进入射手的福位，属于你的<span class="accent">好运终于来了</span>。<br/><br/>
        过去那些被压着的、憋着的、等着的——都要开始<span class="accent">兑现了</span>。
      </p>
      <div class="quote-line">
        <div class="quote-bar"></div>
        <p class="quote-text">"保持行动感，运气自然来"</p>
      </div>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">02</span>
    </div>
  </div>
</body>
</html>
```

### 变体 C：数字序号引导式

```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT: C] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入杂志双线风格CSS */

    /* 变体C专用样式 */
    .number-lead {
      position: absolute;
      top: 180px;
      left: 80px;
      font-size: 180px;
      font-weight: 700;
      color: rgba(193, 95, 60, 0.12);
      line-height: 1;
    }
    .main-c {
      position: absolute;
      top: 280px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .section-keyword {
      font-size: 42px;
      font-weight: 600;
      color: #C15F3C;
      letter-spacing: 6px;
      margin-bottom: 50px;
    }
    .content-c {
      font-size: 32px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="number-lead">02</div>

    <!-- 装饰：双线边框角落变体 -->
    <div class="double-border-corners">
      <div class="corner top-left"></div>
      <div class="corner bottom-right"></div>
    </div>

    <!-- 装饰：星星散布 -->
    <div class="stars-scatter" style="bottom: 200px; right: 100px; width: 120px; height: 120px;">
      <div class="star" style="top: 10px; left: 20px; opacity: 0.4;"></div>
      <div class="star" style="top: 50px; left: 80px; opacity: 0.3; transform: scale(0.8);"></div>
      <div class="star" style="top: 80px; left: 40px; opacity: 0.25;"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-c">
      <h2 class="section-keyword">感情运势</h2>
      <p class="content-c">
        单身的双子座今年桃花运旺盛，<br/>
        特别是<span class="accent">下半年</span>会有不错的机会。<br/><br/>
        有伴的双子座则要注意沟通，<br/>
        <span class="highlight">真诚比技巧更重要</span>。
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 D：引用突出式（大引号开头）

```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT: D] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入杂志双线风格CSS */

    /* 变体D专用样式 */
    .big-quote {
      position: absolute;
      top: 140px;
      left: 60px;
      font-size: 200px;
      font-family: Georgia, serif;
      color: rgba(193, 95, 60, 0.1);
      line-height: 1;
    }
    .main-d {
      position: absolute;
      top: 300px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: left;
    }
    .lead-text {
      font-size: 40px;
      font-weight: 500;
      color: #3D3D3D;
      line-height: 1.8;
      letter-spacing: 3px;
      margin-bottom: 50px;
    }
    .content-d {
      font-size: 30px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2;
      letter-spacing: 2px;
    }
    .end-mark {
      display: inline-block;
      width: 8px;
      height: 8px;
      background: #C15F3C;
      border-radius: 50%;
      margin-left: 12px;
      vertical-align: middle;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="big-quote">"</div>

    <!-- 装饰：星星散布 -->
    <div class="stars-scatter" style="top: 180px; right: 80px; width: 100px; height: 100px;">
      <div class="star" style="top: 15px; left: 25px; opacity: 0.35;"></div>
      <div class="star" style="top: 55px; left: 70px; opacity: 0.25; transform: scale(0.7);"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-d">
      <p class="lead-text">
        不再为不值得的人消耗情绪，<br/>
        不再为无意义的事浪费时间。
      </p>
      <p class="content-d">
        你来，我<span class="accent">热情相迎</span>；<br/>
        你走，我<span class="accent">安然独处</span>。<br/><br/>
        这一年的双子，<br/>
        会更懂<span class="highlight">"不勉强"的智慧</span>。<span class="end-mark"></span>
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">03</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 E：分栏对比式

```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT: E] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入杂志双线风格CSS */

    /* 变体E专用样式 */
    .main-e {
      position: absolute;
      top: 200px;
      left: 80px;
      right: 80px;
      z-index: 10;
    }
    .topic-row {
      display: flex;
      align-items: flex-start;
      margin-bottom: 60px;
    }
    .topic-label {
      width: 140px;
      flex-shrink: 0;
      font-size: 24px;
      font-weight: 500;
      color: #C15F3C;
      letter-spacing: 4px;
      padding-top: 8px;
      border-top: 2px solid #C15F3C;
    }
    .topic-content {
      flex: 1;
      font-size: 30px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2;
      letter-spacing: 2px;
      padding-left: 40px;
    }
    .divider {
      width: 100%;
      height: 1px;
      background: rgba(193, 95, 60, 0.15);
      margin: 40px 0;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：双线边框 -->
    <div class="double-border"></div>

    <!-- 装饰：星星散布 -->
    <div class="stars-scatter" style="top: 140px; right: 100px; width: 100px; height: 100px;">
      <div class="star" style="top: 10px; left: 30px; opacity: 0.3;"></div>
      <div class="star" style="top: 45px; left: 65px; opacity: 0.4; transform: scale(0.6);"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main-e">
      <div class="topic-row">
        <div class="topic-label">事业</div>
        <p class="topic-content">
          事业上会有<span class="accent">惊喜</span>。<br/>
          那些看似随意的连接，<br/>
          可能带来意想不到的机会。
        </p>
      </div>
      <div class="divider"></div>
      <div class="topic-row">
        <div class="topic-label">财运</div>
        <p class="topic-content">
          财运稳中有升，<br/>
          <span class="highlight">下半年尤为明显</span>。<br/>
          适合稳健投资，不宜冒进。
        </p>
      </div>
      <div class="divider"></div>
      <div class="topic-row">
        <div class="topic-label">健康</div>
        <p class="topic-content">
          注意作息规律，<br/>
          给大脑足够的<span class="accent">休息时间</span>。
        </p>
      </div>
    </div>

    <div class="footer">
      <span class="footer-text">2026 双子座运势</span>
      <span class="page-num">04</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 S：总结收尾式（最后一页专用）

> **🎯 重要**：Layout S 专门用于套图的最后一页！无论前面使用哪种布局变体 (A/B/C/D/E)，最后一页都应使用 Layout S 来收尾。

**特征**：
- 内容水平居中
- 大引号装饰（淡色背景）
- 标题带渐变下划线
- 结束星星装饰符

```html
<!-- [STYLE LOCK: 杂志双线] [LAYOUT LOCK: S] -->
<!-- 套图最后一页：总结页 -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Summary Page</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入杂志双线风格CSS */

    /* 变体S专用样式：总结收尾式 */

    /* 大引号装饰 */
    .summary-quote {
      position: absolute;
      top: 200px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 160px;
      font-family: Georgia, serif;
      color: rgba(193, 95, 60, 0.08);
      line-height: 1;
    }

    /* 主容器 - 居中 */
    .main-summary {
      position: absolute;
      top: 50%;
      left: 80px;
      right: 80px;
      transform: translateY(-50%);
      z-index: 10;
      text-align: center;
    }

    /* 标题 - 带下划线 */
    .summary-title {
      font-size: 48px;
      font-weight: 600;
      color: #C15F3C;
      letter-spacing: 8px;
      margin-bottom: 20px;
      display: inline-block;
    }

    .summary-title::after {
      content: '';
      display: block;
      width: 60%;
      height: 3px;
      background: linear-gradient(90deg, transparent, #C15F3C, transparent);
      margin: 16px auto 0;
    }

    /* 正文 - 居中 */
    .summary-content {
      font-size: 34px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: center;
      margin-top: 50px;
    }

    /* 结束装饰符 */
    .summary-end {
      margin-top: 60px;
    }

    .summary-end .end-star {
      width: 16px;
      height: 16px;
      background: #C15F3C;
      clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
      display: inline-block;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 大引号装饰 -->
    <div class="summary-quote">❝</div>

    <!-- 装饰：双线边框角落 -->
    <div class="double-border-corners">
      <div class="corner top-left"></div>
      <div class="corner bottom-right"></div>
    </div>

    <!-- 装饰：星星散布 -->
    <div class="stars-scatter" style="top: 180px; right: 120px; width: 100px; height: 100px;">
      <div class="star" style="top: 10px; left: 30px; opacity: 0.3;"></div>
      <div class="star" style="top: 45px; left: 65px; opacity: 0.4; transform: scale(0.6);"></div>
    </div>

    <div class="header">
      <span class="tag">双子座 · 生理性喜欢</span>
      <div class="zodiac-icon">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <line x1="25" y1="20" x2="75" y2="20" stroke-linecap="round"/>
          <line x1="25" y1="80" x2="75" y2="80" stroke-linecap="round"/>
          <line x1="35" y1="20" x2="35" y2="80" stroke-linecap="round"/>
          <line x1="65" y1="20" x2="65" y2="80" stroke-linecap="round"/>
        </svg>
      </div>
    </div>

    <!-- 主内容 - 居中 -->
    <div class="main-summary">
      <h2 class="summary-title">这就是双子</h2>
      <p class="summary-content">
        来的都是<span class="accent">缘分</span>，<br/>
        留下的才是真心。<br/><br/>
        这就是双子座。
      </p>
      <div class="summary-end">
        <span class="end-star"></span>
      </div>
    </div>

    <div class="footer">
      <span class="footer-text">双子座亲密关系真相</span>
      <span class="page-num">06</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

---

# 风格包 4：优雅留白

**特征**：细边框实心文字 + 小圆点装饰 + 大量留白
**适用**：所有类型内容，特别适合金句、情感、日常更新

## 风格锁定标记

```html
<!-- [STYLE LOCK: 优雅留白] -->
```

## 完整CSS

```css
/* === 优雅留白风格 === */

/* 关键词：纯文字+下划线（极简） */
.keyword {
  display: inline-block;
  font-size: 34px;
  font-weight: 500;
  color: #C15F3C;
  letter-spacing: 8px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(193, 95, 60, 0.4);
  margin-bottom: 50px;
}

/* 装饰：角落小圆点 */
.corner-dot {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(193, 95, 60, 0.5);
  border-radius: 50%;
}

/* 装饰：细线条 */
.line-deco {
  position: absolute;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(193, 95, 60, 0.3), transparent);
}

/* 装饰：小圆点 */
.dot-deco {
  position: absolute;
  width: 6px;
  height: 6px;
  background: #C15F3C;
  border-radius: 50%;
}

/* 封面星座标识区（封面专用） */
.zodiac-header {
  position: absolute;
  top: 200px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  z-index: 10;
}
.zodiac-icon svg {
  width: 64px;
  height: 64px;
  stroke: #C15F3C;
  stroke-width: 1.5;
  fill: none;
  margin-bottom: 24px;
}
.zodiac-name {
  font-size: 48px;
  font-weight: 600;
  color: #C15F3C;
  letter-spacing: 12px;
}
.zodiac-sub {
  font-size: 22px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 6px;
  margin-top: 12px;
}

/* 主内容区 */
.main {
  position: absolute;
  top: 50%;
  left: 100px;
  right: 100px;
  transform: translateY(-50%);
  z-index: 10;
  text-align: center;
}

/* 封面主标题 */
.main-title {
  font-size: 56px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 3px;
  line-height: 1.6;
  margin-bottom: 40px;
}

/* 副标题 */
.sub-title {
  font-size: 28px;
  font-weight: 400;
  color: #6A6A6A;
  letter-spacing: 2px;
}

/* 引用语 */
.quote {
  font-size: 24px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 2px;
  margin-top: 50px;
}

/* 内容页正文 */
.content {
  font-size: 34px;
  font-weight: 400;
  color: #5A5A5A;
  line-height: 2.2;
  letter-spacing: 2px;
  text-align: center;
}

/* 强调文字 */
.accent {
  color: #C15F3C;
  font-weight: 500;
}

/* 页脚 */
.footer {
  position: absolute;
  bottom: 80px;
  left: 100px;
  right: 100px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}
.footer-text {
  font-size: 18px;
  color: #B1ADA1;
  letter-spacing: 3px;
}
.page-num {
  font-size: 20px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
}

/* 底部渐变色带 */
.gradient-band {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
}
```

## 封面模板

```html
<!-- [STYLE LOCK: 优雅留白] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入优雅留白风格CSS */

    /* 封面专用：主内容区下移 */
    .main {
      top: 540px;
      transform: none;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 极简装饰：角落小圆点 -->
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>

    <!-- 装饰细线 -->
    <div class="line-deco" style="top: 160px; left: 100px; right: 100px;"></div>

    <div class="header">
      <span class="tag">2026 年度运势</span>
      <span class="tag">GEMINI</span>
    </div>

    <!-- 星座标识区 -->
    <div class="zodiac-header">
      <div class="zodiac-icon">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <line x1="20" y1="15" x2="80" y2="15" stroke-linecap="round"/>
          <line x1="20" y1="85" x2="80" y2="85" stroke-linecap="round"/>
          <line x1="35" y1="15" x2="35" y2="85" stroke-linecap="round"/>
          <line x1="65" y1="15" x2="65" y2="85" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="zodiac-name">双子座</div>
      <div class="zodiac-sub">2026 年度宣言</div>
    </div>

    <div class="main">
      <div class="keyword">关键词</div>
      <h1 class="main-title">主标题<br/><span class="accent">强调词</span></h1>
      <p class="sub-title">副标题说明文字</p>
    </div>

    <div class="footer">
      <span class="footer-text">双子座 · 2026</span>
      <span class="page-num">01</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

## 内容页布局变体

> **⚠️ 核心规则**：同一套图的所有内容页必须使用相同的布局变体！生成套图前先确定一个布局变体（A/B/S），然后所有内容页都使用这个布局。禁止在同一套图中混用不同布局变体。

### 变体 A：居中式（默认）

适用：通用内容，金句展示

```html
<!-- [STYLE LOCK: 优雅留白] [LAYOUT LOCK: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入优雅留白风格CSS */
  </style>
</head>
<body>
  <div class="poster">
    <!-- 极简装饰：角落小圆点 -->
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>

    <!-- 装饰：小圆点 -->
    <div class="dot-deco" style="top: 180px; left: 100px;"></div>
    <div class="dot-deco" style="bottom: 180px; right: 100px;"></div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <span class="tag">GEMINI</span>
    </div>

    <div class="main">
      <div class="keyword">小标题</div>
      <p class="content">
        正文内容第一段，<br/>
        采用居中排版。<br/><br/>
        正文内容包含<span class="accent">强调词</span>。
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">双子座 · 情感独白</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 B：章节式

适用：分段叙述，条理清晰

```html
<!-- [STYLE LOCK: 优雅留白] [LAYOUT LOCK: B] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入优雅留白风格CSS */

    /* 变体B专用样式 */
    .part-label {
      font-size: 20px;
      font-weight: 400;
      color: #C15F3C;
      letter-spacing: 4px;
      margin-bottom: 20px;
    }
    .section-title {
      font-size: 42px;
      font-weight: 600;
      color: #2D2D2D;
      letter-spacing: 3px;
      margin-bottom: 50px;
    }
    .main-b {
      position: absolute;
      top: 50%;
      left: 100px;
      right: 100px;
      transform: translateY(-50%);
      z-index: 10;
      text-align: center;
    }
    .content-b {
      font-size: 32px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 极简装饰：角落小圆点 -->
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>

    <!-- 装饰细线 -->
    <div class="line-deco" style="top: 180px; left: 100px; right: 100px;"></div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <span class="tag">GEMINI</span>
    </div>

    <div class="main-b">
      <div class="part-label">· 01 ·</div>
      <h2 class="section-title">小节标题</h2>
      <p class="content-b">
        正文内容第一段，<br/>
        采用居中排版。<br/><br/>
        正文内容包含<span class="accent">强调词</span>。
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">双子座 · 情感独白</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

### 变体 S：总结页

适用：套图最后一页，总结升华

```html
<!-- [STYLE LOCK: 优雅留白] [LAYOUT LOCK: S] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX - Summary</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入优雅留白风格CSS */

    /* 变体S专用样式 */
    .summary-main {
      position: absolute;
      top: 50%;
      left: 100px;
      right: 100px;
      transform: translateY(-50%);
      z-index: 10;
      text-align: center;
    }
    .summary-icon {
      font-size: 40px;
      color: #C15F3C;
      margin-bottom: 40px;
    }
    .summary-title {
      font-size: 44px;
      font-weight: 600;
      color: #C15F3C;
      letter-spacing: 6px;
      margin-bottom: 50px;
    }
    .summary-content {
      font-size: 34px;
      font-weight: 400;
      color: #5A5A5A;
      line-height: 2.2;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 极简装饰：角落小圆点 -->
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>

    <!-- 装饰细线 -->
    <div class="line-deco" style="top: 180px; left: 100px; right: 100px;"></div>
    <div class="line-deco" style="bottom: 180px; left: 100px; right: 100px;"></div>

    <div class="header">
      <span class="tag">双子座</span>
      <span class="tag">GEMINI</span>
    </div>

    <div class="summary-main">
      <div class="summary-icon">✦</div>
      <h2 class="summary-title">总结标题</h2>
      <p class="summary-content">
        总结文字第一段<br/><br/>
        总结文字包含<span class="accent">强调词</span><br/><br/>
        升华收尾
      </p>
    </div>

    <div class="footer">
      <span class="footer-text">双子座 · 情感独白</span>
      <span class="page-num">06</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

---

# 生成检查清单

## ⚠️ 核心规则：布局变体保持一致

**重要**：同一套图的所有内容页必须使用相同的布局变体！

**风格包 1-3**（经典强调、简约边框、杂志双线）支持5种布局变体（A/B/C/D/E）

**风格包 4**（优雅留白）支持3种布局变体：
- 变体A：居中式（关键词 + 居中正文）
- 变体B：章节式（章节标号 + 小节标题 + 居中正文）
- 变体S：总结页（用于套图最后一页）

---

## 生成套图前（必须完成）

- [ ] 从 4 个风格包中随机选择 1 个
- [ ] 记录选择的风格包名称
- [ ] **预先规划使用哪个布局变体**

## 生成封面时

- [ ] 在 HTML 开头添加 `<!-- [STYLE LOCK: 风格包名称] -->` 注释
- [ ] 使用该风格包的封面模板

## 生成内容页时（⚠️ 必须使用统一布局变体）

- [ ] 在 HTML 开头添加 `<!-- [STYLE LOCK: 风格包名称] [LAYOUT LOCK: X] -->` 注释
- [ ] **所有内容页必须使用相同的布局变体**
- [ ] 使用该风格包的基础 CSS + 所选变体的专用样式

### 布局变体快速参考

**风格包 1-3 布局变体**：
| 变体 | 名称 | 核心特征 | 适合内容 |
|------|------|----------|----------|
| A | 色块标题居中式 | 关键词色块 + 居中排版 | 主题明确的段落 |
| B | 杂志章节式 | PART XX + 大标题 + 竖线引用 | 重要观点、开篇 |
| C | 数字序号引导式 | 大数字背景 + 左对齐 | 分点阐述 |
| D | 引用突出式 | 大引号 + 金句突出 | 金句、感悟类 |
| E | 分栏对比式 | 左侧标签 + 右侧内容 | 多主题概览 |
| **S** | **总结收尾式** | **居中 + 收尾装饰** | **套图最后一页** |

**风格包 4（优雅留白）布局变体**：
| 变体 | 名称 | 核心特征 | 适合内容 |
|------|------|----------|----------|
| A | 居中式 | 关键词边框 + 居中正文 + 小圆点装饰 | 通用，金句展示 |
| B | 章节式 | 章节标号 + 小节标题 + 居中正文 | 分段叙述 |
| **S** | **总结页** | **✦图标 + 总结标题 + 升华文字** | **套图最后一页** |

### 如何选择布局变体

| 内容类型 | 推荐变体 | 原因 |
|----------|----------|------|
| 年运势/月运势 | A 或 B | 正式、有仪式感 |
| 每日运势 | A | 简洁明了 |
| 情感/金句类 | A | 居中突出金句 |
| 性格分析/指南 | B | 结构清晰 |
| **套图最后一页** | **S** | **总结收尾，升华主题** |

> **🎯 总结页规则**：无论套图使用哪种布局变体 (A/B)，**最后一页必须使用 Layout S**！这是套图的收尾页，有独立的总结风格。

---

## 禁止事项

- ❌ **禁止**在同一套图中混用不同风格包
- ❌ **禁止**在同一套图中混用不同布局变体
- ❌ **禁止**封面和内容页使用不同的装饰元素风格
- ❌ **禁止**每页随机选择布局变体

---

# 配色参考

| 用途 | 色值 | 说明 |
|------|------|------|
| 重点色 | `#C15F3C` | 赭红/珊瑚橙 |
| 重点色渐变 | `#C15F3C → #D4765A` | 色块渐变 |
| 主文字 | `#2D2D2D` | 深灰，标题 |
| 次文字 | `#3D3D3D` | 次深灰，副标题 |
| 正文 | `#5A5A5A` | 中灰，段落 |
| 弱化文字 | `#9A958A` | 浅灰，标签/引用 |

---

# 星座图标库

根据不同星座替换 SVG 内容。以下是常用星座图标：

## 双子座 (Gemini)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <line x1="25" y1="20" x2="75" y2="20" stroke-linecap="round"/>
  <line x1="25" y1="80" x2="75" y2="80" stroke-linecap="round"/>
  <line x1="35" y1="20" x2="35" y2="80" stroke-linecap="round"/>
  <line x1="65" y1="20" x2="65" y2="80" stroke-linecap="round"/>
</svg>
```

## 射手座 (Sagittarius)
```html
<svg viewBox="0 0 50 50">
  <line x1="8" y1="42" x2="42" y2="8" stroke-linecap="round"/>
  <polyline points="30,8 42,8 42,20" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="18" y1="32" x2="32" y2="18" stroke-linecap="round"/>
  <line x1="12" y1="28" x2="22" y2="38" stroke-linecap="round"/>
</svg>
```

## 白羊座 (Aries)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M30,70 C30,35 50,25 50,25 C50,25 70,35 70,70" stroke-linecap="round"/>
  <path d="M20,40 C20,25 35,20 35,35" stroke-linecap="round"/>
  <path d="M80,40 C80,25 65,20 65,35" stroke-linecap="round"/>
</svg>
```

## 金牛座 (Taurus)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="55" r="25"/>
  <path d="M25,40 C25,25 40,20 50,30 C60,20 75,25 75,40" stroke-linecap="round"/>
</svg>
```

---

# 风格包快速参考

| 风格包 | 关键词 | 装饰1 | 装饰2 | 视觉感受 |
|--------|--------|-------|-------|----------|
| 1. 经典强调 | 色块填充 | 大字号背景 | 圆形装饰 | 温暖稳重 |
| 2. 简约边框 | 边框线条 | 角标装饰 | 竖线组 | 简洁精致 |
| 3. 杂志双线 | 双线装饰 | 双线边框 | 星星散布 | 高级杂志感 |
| 4. 艺术镂空 | 轮廓镂空 | 大引号 | 书法笔触 | 艺术创意 |

**随机选择时，可用公式**：`风格包编号 = (当前时间戳 % 4) + 1`
