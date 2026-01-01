# 动态编辑风 (Editorial Dynamic) 封面模板规范

## 核心规则：风格锁定系统

### 为什么需要风格锁定？

生成套图（封面 + 多页内容页）时，**所有页面必须使用同一风格包**，确保视觉一致性。

### 如何使用风格锁定？

1. **生成套图前**：从下方 4 个风格包中随机选择 1 个
2. **生成第一页时**：在 HTML 开头添加风格锁定注释
3. **生成后续页面时**：查看已有页面的风格锁定注释，使用相同风格包

```html
<!-- [STYLE LOCK: 风格包名称] -->
<!-- 本套图所有页面必须使用此风格 -->
<!DOCTYPE html>
...
```

---

## 画布尺寸与基础设置

**尺寸**：1080px × 1440px（3:4 比例）

### 通用基础样式（所有风格包共用）

```css
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
    <div class="zodiac-bg">双子座</div>

    <!-- 装饰：圆形 -->
    <div class="circle-deco" style="top: 140px; right: 80px; width: 100px; height: 100px;">
      <div class="circle-inner" style="width: 50px; height: 50px;"></div>
    </div>

    <div class="header">
      <span class="tag">2026 年度运势</span>
      <span class="tag">GEMINI</span>
    </div>

    <!-- 醒目的星座标识（封面核心元素） -->
    <div class="zodiac-header">
      <div class="zodiac-icon-large">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <!-- 替换为对应星座SVG -->
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

> **重要规则**：每页内容应随机选择一种布局变体，增加视觉多样性。同一套图中可以混用不同布局变体（只要使用相同的风格包CSS）。

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

> **重要规则**：每页内容应随机选择一种布局变体，增加视觉多样性。同一套图中可以混用不同布局变体（只要使用相同的风格包CSS）。

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

> **重要规则**：每页内容应随机选择一种布局变体，增加视觉多样性。同一套图中可以混用不同布局变体（只要使用相同的风格包CSS）。

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

---

# 风格包 4：艺术镂空

**特征**：轮廓镂空关键词 + 大引号装饰 + 书法笔触
**适用**：金句类、艺术主题、创意内容

## 风格锁定标记

```html
<!-- [STYLE LOCK: 艺术镂空] -->
```

## 完整CSS

```css
/* === 艺术镂空风格 === */

/* 关键词：轮廓镂空 */
.keyword {
  display: inline-block;
  width: fit-content;
  font-size: 36px;
  font-weight: 700;
  color: transparent;
  -webkit-text-stroke: 1.5px #C15F3C;
  letter-spacing: 8px;
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

/* 装饰：大引号 */
.quote-mark {
  position: absolute;
  font-size: 200px;
  font-family: Georgia, serif;
  color: rgba(193, 95, 60, 0.08);
  line-height: 1;
}
.quote-mark.open {
  top: 180px;
  left: 60px;
}
.quote-mark.close {
  bottom: 200px;
  right: 60px;
}

/* 装饰：书法笔触 */
.brush-stroke {
  position: absolute;
  width: 120px;
  height: 20px;
}
.brush-stroke svg {
  width: 100%;
  height: 100%;
  stroke: rgba(193, 95, 60, 0.2);
  stroke-width: 4;
  stroke-linecap: round;
  fill: none;
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
  font-size: 64px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 4px;
  line-height: 1.5;
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
  font-size: 28px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
  font-style: italic;
}

/* 内容页正文 */
.content {
  font-size: 36px;
  font-weight: 400;
  color: #5A5A5A;
  line-height: 2;
  letter-spacing: 2px;
  text-align: center;
}

/* 内容页引用居中 */
.content-quote {
  font-size: 28px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 3px;
  font-style: italic;
  margin-top: 40px;
}
```

## 封面模板

```html
<!-- [STYLE LOCK: 艺术镂空] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入艺术镂空风格CSS */

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

    <!-- 装饰：大引号 -->
    <div class="quote-mark open">"</div>
    <div class="quote-mark close">"</div>

    <!-- 装饰：书法笔触 -->
    <div class="brush-stroke" style="top: 350px; left: 50px;">
      <svg viewBox="0 0 120 20">
        <path d="M5,15 Q20,5 40,12 T80,8 T115,14"/>
      </svg>
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

> **重要规则**：每页内容应随机选择一种布局变体，增加视觉多样性。同一套图中可以混用不同布局变体（只要使用相同的风格包CSS）。

### 变体 A：色块标题居中式

```html
<!-- [STYLE LOCK: 艺术镂空] [LAYOUT: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入艺术镂空风格CSS */
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：大引号（简化版，只用一个） -->
    <div class="quote-mark open" style="font-size: 160px; top: 160px; left: 80px;">"</div>

    <!-- 装饰：书法笔触（位置变化） -->
    <div class="brush-stroke" style="bottom: 280px; right: 60px;">
      <svg viewBox="0 0 120 20">
        <path d="M5,10 Q30,18 60,8 T115,12"/>
      </svg>
    </div>

    <div class="header">
      <span class="tag">双子座 · 2026</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main">
      <div class="keyword">小标题</div>
      <p class="content">
        正文内容第一段，<br/>
        采用居中排版。<br/><br/>
        正文内容包含<span class="accent">强调词</span>，<br/>
        以及<span class="highlight">高亮文字</span>。
      </p>
      <p class="content-quote">「 页面引用语 」</p>
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
<!-- [STYLE LOCK: 艺术镂空] [LAYOUT: B] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入艺术镂空风格CSS */

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
    <!-- 装饰：大引号 -->
    <div class="quote-mark open" style="font-size: 140px; top: 100px; right: 100px;">"</div>

    <!-- 装饰：书法笔触 -->
    <div class="brush-stroke" style="bottom: 200px; left: 60px;">
      <svg viewBox="0 0 120 20">
        <path d="M5,15 Q20,5 40,12 T80,8 T115,14"/>
      </svg>
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
<!-- [STYLE LOCK: 艺术镂空] [LAYOUT: C] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入艺术镂空风格CSS */

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

    <!-- 装饰：书法笔触 -->
    <div class="brush-stroke" style="top: 140px; right: 80px;">
      <svg viewBox="0 0 120 20">
        <path d="M5,10 Q30,18 60,8 T115,12"/>
      </svg>
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
<!-- [STYLE LOCK: 艺术镂空] [LAYOUT: D] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入艺术镂空风格CSS */

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

    <!-- 装饰：书法笔触 -->
    <div class="brush-stroke" style="bottom: 240px; right: 80px;">
      <svg viewBox="0 0 120 20">
        <path d="M5,12 Q25,5 50,14 T95,8 T115,15"/>
      </svg>
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
<!-- [STYLE LOCK: 艺术镂空] [LAYOUT: E] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page XX</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入艺术镂空风格CSS */

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
    <!-- 装饰：大引号 -->
    <div class="quote-mark open" style="font-size: 120px; top: 120px; right: 100px; opacity: 0.06;">"</div>

    <!-- 装饰：书法笔触 -->
    <div class="brush-stroke" style="bottom: 180px; left: 60px;">
      <svg viewBox="0 0 120 20">
        <path d="M5,15 Q20,5 40,12 T80,8 T115,14"/>
      </svg>
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

---

# 生成检查清单

## ⚠️ 核心规则：布局变体必须随机化

**绝对禁止**：所有内容页都使用变体A（色块标题居中式）！

生成内容页时，**必须**从5种布局变体中随机选择，确保视觉多样性：
- 变体A：色块标题居中式（标题在色块内）
- 变体B：杂志章节式（PART标签 + 大标题左对齐，**无色块**）
- 变体C：数字序号引导式（大数字背景 + 红色关键词，**无色块**）
- 变体D：引用突出式（大引号装饰 + 金句左对齐，**无色块**）
- 变体E：分栏对比式（左侧标签栏 + 右侧内容，**无色块**）

**每种变体在一套图中最多出现1-2次**，确保视觉变化。

---

## 生成套图前（必须完成）

- [ ] 从 4 个风格包中随机选择 1 个
- [ ] 记录选择的风格包名称
- [ ] **预先规划每页使用哪个布局变体**（参考下方示例）

## 生成封面时

- [ ] 在 HTML 开头添加 `<!-- [STYLE LOCK: 风格包名称] -->` 注释
- [ ] 使用该风格包的封面模板

## 生成内容页时（⚠️ 必须随机选择布局变体）

- [ ] 在 HTML 开头添加 `<!-- [STYLE LOCK: 风格包名称] [LAYOUT: X] -->` 注释
- [ ] **必须按照预先规划选择布局变体**，不能全部使用变体A
- [ ] 同一套图中**必须混用至少3种不同布局变体**
- [ ] 使用该风格包的基础 CSS + 所选变体的专用样式

### 布局变体快速参考

| 变体 | 名称 | 核心特征 | 标题形式 | 适合内容 |
|------|------|----------|----------|----------|
| A | 色块标题居中式 | 关键词色块 + 居中排版 | 色块内 | 主题明确的段落 |
| B | 杂志章节式 | PART XX + 大标题 + 竖线引用 | **无色块，左对齐** | 重要观点、开篇 |
| C | 数字序号引导式 | 大数字背景 + 左对齐 | **无色块，红色文字** | 分点阐述 |
| D | 引用突出式 | 大引号 + 金句突出 | **无色块，左对齐** | 金句、感悟类 |
| E | 分栏对比式 | 左侧标签 + 右侧内容 | **无色块，标签式** | 多主题概览 |

### 推荐的变体分配（5页内容页）

```
Page 02: 变体 B（杂志章节式）- 作为开篇，PART 01
Page 03: 变体 D（引用突出式）- 金句段落
Page 04: 变体 C（数字序号式）- 具体运势
Page 05: 变体 A（色块居中式）- 主题段落
Page 06: 变体 E（分栏对比式）- 多方面概览或总结
```

### 变体随机公式

生成每页前，使用以下方法确定变体：
```
变体 = ['A', 'B', 'C', 'D', 'E'][页码 % 5]
```
或根据内容特点选择最适合的变体。

---

## 禁止事项

- ❌ **禁止**在同一套图中混用不同风格包（风格包 ≠ 布局变体）
- ❌ **禁止**所有内容页都使用变体A（这是最常见的错误！）
- ❌ **禁止**连续两页使用相同布局变体
- ❌ **禁止**混用不同风格包的配色和装饰元素

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
