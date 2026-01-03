# 简约边框风 (Editorial Border) 模板规范

**特征**：边框线条关键词 + 角标装饰 + 竖线组装饰
**适用**：规则清单、指南类、简洁内容

---

## 核心配色（必须遵守）

| 用途 | 色值 | 说明 |
|------|------|------|
| **强调色** | `#C15F3C` | 图标、关键词边框、强调文字 |
| **弱化色** | `#B1ADA1` / `#9A958A` | 标签、页码、辅助文字 |
| **深色文字** | `#3D3D3D` | 主标题、正文 |
| **背景浅端** | `#FAF6F1` | 渐变背景起点 |
| **背景深端** | `#F0E6D9` | 渐变背景终点 |

---

## 风格特征

### 关键词样式：边框线条
```css
.keyword {
  display: inline-block;
  font-size: 36px;
  font-weight: 500;
  color: #C15F3C;
  letter-spacing: 8px;
  padding: 12px 28px;
  border: 2px solid #C15F3C;
  border-radius: 2px;
}
```

### 装饰元素：角标
```css
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
.corner-bracket.bottom-right {
  bottom: 140px;
  right: 70px;
  border-left: none;
  border-top: none;
}
```

### 装饰元素：竖线组
```css
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
```

---

## 封面模板

```html
<!-- [STYLE: 简约边框风] -->
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
      background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%);
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .poster::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.05;
      pointer-events: none;
      z-index: 1;
    }
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
    .tag { font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }
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
    .corner-bracket.bottom-right {
      bottom: 140px;
      right: 70px;
      border-left: none;
      border-top: none;
    }
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
    .main {
      position: absolute;
      top: 520px;
      left: 80px;
      right: 80px;
      z-index: 10;
      text-align: center;
    }
    .keyword {
      display: inline-block;
      font-size: 36px;
      font-weight: 500;
      color: #C15F3C;
      letter-spacing: 8px;
      padding: 12px 28px;
      border: 2px solid #C15F3C;
      border-radius: 2px;
      margin-bottom: 50px;
    }
    .main-title {
      font-size: 80px;
      font-weight: 600;
      color: #2D2D2D;
      letter-spacing: 6px;
      line-height: 1.4;
      margin-bottom: 40px;
    }
    .accent { color: #C15F3C; font-weight: 500; }
    .sub-title {
      font-size: 34px;
      font-weight: 400;
      color: #5A5A5A;
      letter-spacing: 4px;
      margin-bottom: 50px;
    }
    .quote {
      font-size: 26px;
      font-weight: 400;
      color: #9A958A;
      letter-spacing: 3px;
      font-style: italic;
    }
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
    .footer-text { font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }
    .page-num { font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .gradient-band {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-bg">射手座</div>
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket bottom-right"></div>
    <div class="header">
      <span class="tag">2026 年度运势</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="zodiac-header">
      <div class="zodiac-icon-large">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <line x1="20" y1="80" x2="80" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="55" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="80" y2="45" stroke-linecap="round"/>
          <line x1="25" y1="45" x2="55" y2="75" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="zodiac-name">射手座</div>
      <div class="zodiac-year">2026</div>
    </div>
    <div class="main">
      <div class="keyword">年度关键词</div>
      <h1 class="main-title">勇敢<span class="accent">出发</span><br/>不问<span class="accent">终点</span></h1>
      <p class="quote">「 旅途本身就是意义 」</p>
    </div>
    <div class="footer">
      <span class="footer-text">2026 射手座运势</span>
      <span class="page-num">01</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

---

## 内容页模板

```html
<!-- [STYLE: 简约边框风] 内容页 -->
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
      background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%);
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .poster::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.05;
      pointer-events: none;
      z-index: 1;
    }
    .corner-bracket {
      position: absolute;
      width: 40px;
      height: 40px;
      border: 2px solid rgba(193, 95, 60, 0.15);
    }
    .corner-bracket.top-left {
      top: 60px;
      left: 60px;
      border-right: none;
      border-bottom: none;
    }
    .corner-bracket.bottom-right {
      bottom: 60px;
      right: 60px;
      border-left: none;
      border-top: none;
    }
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
    .tag { font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }
    .zodiac-icon svg { width: 48px; height: 48px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }
    .main {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      z-index: 10;
      width: 100%;
      padding: 0 100px;
    }
    .think {
      font-size: 44px;
      color: #5A5A5A;
      letter-spacing: 3px;
      line-height: 1.7;
      margin-bottom: 60px;
    }
    .keyword { color: #C15F3C; font-weight: 500; }
    .truth-box {
      background: transparent;
      padding: 40px 50px;
      border: 2px solid rgba(193, 95, 60, 0.2);
      border-radius: 4px;
    }
    .truth {
      font-size: 38px;
      color: #3D3D3D;
      letter-spacing: 2px;
      line-height: 1.8;
    }
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
    .footer-text { font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }
    .page-num { font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .gradient-band {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket bottom-right"></div>
    <div class="header">
      <span class="tag">射手座 · 情感解读</span>
      <div class="zodiac-icon">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <line x1="20" y1="80" x2="80" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="55" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="80" y2="45" stroke-linecap="round"/>
          <line x1="25" y1="45" x2="55" y2="75" stroke-linecap="round"/>
        </svg>
      </div>
    </div>
    <div class="main">
      <p class="think">你以为射手<span class="keyword">不回消息</span><br/>是不在乎</p>
      <div class="truth-box">
        <p class="truth">其实Ta只是不想<br/>让你觉得自己太黏人</p>
      </div>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">02</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

---

## 结尾页模板

```html
<!-- [STYLE: 简约边框风] 结尾页 -->
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
      background: linear-gradient(165deg, #FAF6F1 0%, #F5EDE4 50%, #F0E6D9 100%);
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .poster::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.05;
      pointer-events: none;
      z-index: 1;
    }
    .corner-bracket {
      position: absolute;
      width: 60px;
      height: 60px;
      border: 2px solid rgba(193, 95, 60, 0.2);
    }
    .corner-bracket.top-left { top: 60px; left: 60px; border-right: none; border-bottom: none; }
    .corner-bracket.top-right { top: 60px; right: 60px; border-left: none; border-bottom: none; }
    .corner-bracket.bottom-left { bottom: 60px; left: 60px; border-right: none; border-top: none; }
    .corner-bracket.bottom-right { bottom: 60px; right: 60px; border-left: none; border-top: none; }
    .main {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      z-index: 10;
    }
    .zodiac-icon {
      margin-bottom: 30px;
    }
    .zodiac-icon svg {
      width: 72px;
      height: 72px;
      stroke: #C15F3C;
      stroke-width: 1.5;
      fill: none;
    }
    .zodiac-name {
      font-size: 42px;
      font-weight: 600;
      color: #C15F3C;
      letter-spacing: 16px;
      margin-bottom: 50px;
    }
    .quote {
      font-size: 46px;
      font-weight: 500;
      color: #3D3D3D;
      letter-spacing: 4px;
      line-height: 1.8;
      max-width: 700px;
      margin-bottom: 50px;
    }
    .accent { color: #C15F3C; }
    .tagline {
      font-size: 24px;
      color: #9A958A;
      letter-spacing: 6px;
    }
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
    .footer-text { font-size: 20px; color: #B1ADA1; letter-spacing: 4px; }
    .page-num { font-size: 24px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .gradient-band {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-bracket top-left"></div>
    <div class="corner-bracket top-right"></div>
    <div class="corner-bracket bottom-left"></div>
    <div class="corner-bracket bottom-right"></div>
    <div class="main">
      <div class="zodiac-icon">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <line x1="20" y1="80" x2="80" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="55" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="80" y2="45" stroke-linecap="round"/>
          <line x1="25" y1="45" x2="55" y2="75" stroke-linecap="round"/>
        </svg>
      </div>
      <p class="zodiac-name">射 手 座</p>
      <p class="quote">爱<span class="accent">从来不挂在嘴边</span><br/>但每一个细节<br/>都藏着<span class="accent">对你的在意</span></p>
      <p class="tagline">感谢阅读 · 点赞收藏</p>
    </div>
    <div class="footer">
      <span class="footer-text">SAGITTARIUS</span>
      <span class="page-num">07</span>
    </div>
    <div class="gradient-band"></div>
  </div>
</body>
</html>
```
