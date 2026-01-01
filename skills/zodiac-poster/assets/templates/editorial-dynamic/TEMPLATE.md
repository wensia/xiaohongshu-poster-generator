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

## 内容页模板

```html
<!-- [STYLE LOCK: 经典强调] -->
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

    /* 内容页布局调整 */
    .main {
      top: 280px;
      transform: none;
      text-align: left;
    }
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：圆形（位置可变化） -->
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

## 内容页模板

```html
<!-- [STYLE LOCK: 简约边框] -->
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

## 内容页模板

```html
<!-- [STYLE LOCK: 杂志双线] -->
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

## 内容页模板

```html
<!-- [STYLE LOCK: 艺术镂空] -->
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

---

# 生成检查清单

## 生成套图前（必须完成）

- [ ] 从 4 个风格包中随机选择 1 个
- [ ] 记录选择的风格包名称

## 生成每页时（必须完成）

- [ ] 在 HTML 开头添加 `<!-- [STYLE LOCK: 风格包名称] -->` 注释
- [ ] 使用该风格包的完整 CSS（直接复制，不要混用其他风格包）
- [ ] 使用该风格包定义的装饰元素
- [ ] 关键词样式使用该风格包的 `.keyword` 样式

## 装饰元素变化规则

同一风格包内，不同页面可以通过以下方式增加变化（而非更换风格）：

1. **位置变化**：同样的装饰元素放在不同位置
2. **大小变化**：调整 width/height 值
3. **数量变化**：增减装饰元素数量
4. **透明度变化**：微调 opacity 值
5. **简化/完整版**：如双线边框可以只用角落版

## 禁止事项

- **禁止**在同一套图中混用不同风格包
- **禁止**在内容页使用与封面不同的关键词样式类型
- **禁止**混用不同风格包的装饰元素
- **禁止**每页随机选择不同风格

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
