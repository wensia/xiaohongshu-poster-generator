# 优雅留白风 (Editorial Elegant) 模板规范

**特征**：纯文字下划线关键词 + 小圆点装饰 + 大量留白
**适用**：金句、情感内容、日常更新、极简风格

---

## 核心配色（必须遵守）

| 用途 | 色值 | 说明 |
|------|------|------|
| **强调色** | `#C15F3C` | 图标、关键词、强调文字 |
| **弱化色** | `#B1ADA1` / `#9A958A` | 标签、页码、辅助文字 |
| **深色文字** | `#3D3D3D` / `#2D2D2D` | 主标题、正文 |
| **背景浅端** | `#FAF6F1` | 渐变背景起点 |
| **背景深端** | `#F0E6D9` | 渐变背景终点 |

---

## 风格特征

### 关键词样式：纯文字+下划线
```css
.keyword {
  display: inline-block;
  font-size: 34px;
  font-weight: 500;
  color: #C15F3C;
  letter-spacing: 8px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(193, 95, 60, 0.4);
}
```

### 装饰元素：角落小圆点
```css
.corner-dot {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(193, 95, 60, 0.5);
  border-radius: 50%;
}
```

### 装饰元素：细线条
```css
.line-deco {
  position: absolute;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(193, 95, 60, 0.3), transparent);
}
```

---

## 封面模板

```html
<!-- [STYLE: 优雅留白风] -->
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
    .corner-dot {
      position: absolute;
      width: 4px;
      height: 4px;
      background: rgba(193, 95, 60, 0.5);
      border-radius: 50%;
    }
    .line-deco {
      position: absolute;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(193, 95, 60, 0.3), transparent);
    }
    .header {
      position: absolute;
      top: 70px;
      left: 100px;
      right: 100px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .tag { font-size: 22px; font-weight: 400; color: #9A958A; letter-spacing: 6px; }
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
    .main {
      position: absolute;
      top: 540px;
      left: 100px;
      right: 100px;
      z-index: 10;
      text-align: center;
    }
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
    .main-title {
      font-size: 56px;
      font-weight: 600;
      color: #2D2D2D;
      letter-spacing: 3px;
      line-height: 1.6;
      margin-bottom: 40px;
    }
    .accent { color: #C15F3C; font-weight: 500; }
    .sub-title {
      font-size: 28px;
      font-weight: 400;
      color: #6A6A6A;
      letter-spacing: 2px;
    }
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
    .footer-text { font-size: 18px; color: #B1ADA1; letter-spacing: 3px; }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 3px; }
    .gradient-band {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>
    <div class="line-deco" style="top: 160px; left: 100px; right: 100px;"></div>
    <div class="header">
      <span class="tag">2026 年度运势</span>
      <span class="tag">SAGITTARIUS</span>
    </div>
    <div class="zodiac-header">
      <div class="zodiac-icon">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <line x1="20" y1="80" x2="80" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="55" y2="20" stroke-linecap="round"/>
          <line x1="80" y1="20" x2="80" y2="45" stroke-linecap="round"/>
          <line x1="25" y1="45" x2="55" y2="75" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="zodiac-name">射手座</div>
      <div class="zodiac-sub">2026 年度宣言</div>
    </div>
    <div class="main">
      <div class="keyword">年度宣言</div>
      <h1 class="main-title">不必<span class="accent">讨好</span>任何人<br/>做自己就<span class="accent">很好</span></h1>
      <p class="sub-title">射手座的 2026 生活态度</p>
    </div>
    <div class="footer">
      <span class="footer-text">射手座 · 2026</span>
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
<!-- [STYLE: 优雅留白风] 内容页 -->
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
    .corner-dot {
      position: absolute;
      width: 4px;
      height: 4px;
      background: rgba(193, 95, 60, 0.5);
      border-radius: 50%;
    }
    .header {
      position: absolute;
      top: 70px;
      left: 100px;
      right: 100px;
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
      padding: 0 120px;
    }
    .think {
      font-size: 42px;
      color: #5A5A5A;
      letter-spacing: 3px;
      line-height: 1.8;
      margin-bottom: 70px;
    }
    .keyword { color: #C15F3C; font-weight: 500; }
    .truth {
      font-size: 36px;
      color: #3D3D3D;
      letter-spacing: 2px;
      line-height: 1.9;
      padding-top: 50px;
      border-top: 1px solid rgba(193, 95, 60, 0.2);
    }
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
    .footer-text { font-size: 18px; color: #B1ADA1; letter-spacing: 3px; }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 3px; }
    .gradient-band {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>
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
      <p class="truth">其实Ta只是不想<br/>让你觉得自己太黏人</p>
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
<!-- [STYLE: 优雅留白风] 结尾页 -->
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
    .corner-dot {
      position: absolute;
      width: 4px;
      height: 4px;
      background: rgba(193, 95, 60, 0.5);
      border-radius: 50%;
    }
    .dot-deco {
      position: absolute;
      width: 6px;
      height: 6px;
      background: #C15F3C;
      border-radius: 50%;
      opacity: 0.3;
    }
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
      width: 64px;
      height: 64px;
      stroke: #C15F3C;
      stroke-width: 1.5;
      fill: none;
    }
    .zodiac-name {
      font-size: 38px;
      font-weight: 600;
      color: #C15F3C;
      letter-spacing: 12px;
      margin-bottom: 50px;
    }
    .quote {
      font-size: 42px;
      font-weight: 500;
      color: #3D3D3D;
      letter-spacing: 3px;
      line-height: 1.9;
      max-width: 650px;
      margin-bottom: 50px;
    }
    .accent { color: #C15F3C; }
    .tagline {
      font-size: 22px;
      color: #9A958A;
      letter-spacing: 6px;
    }
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
    .footer-text { font-size: 18px; color: #B1ADA1; letter-spacing: 3px; }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 3px; }
    .gradient-band {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="corner-dot" style="top: 60px; left: 60px;"></div>
    <div class="corner-dot" style="top: 60px; right: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; left: 60px;"></div>
    <div class="corner-dot" style="bottom: 60px; right: 60px;"></div>
    <div class="dot-deco" style="top: 300px; left: 150px;"></div>
    <div class="dot-deco" style="top: 400px; right: 180px;"></div>
    <div class="dot-deco" style="bottom: 350px; left: 200px;"></div>
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
