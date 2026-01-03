# 极简留白 (Minimal Whitespace) 模板规范

---

## 风格概述

**极简留白风格**是一种以大面积留白为核心的设计风格，强调：
- 垂直居中布局
- 大量呼吸空间
- 简洁的视觉层次
- 柔和的色彩过渡

**适用场景**：情感类、哲理类、治愈系内容

---

## 核心配色规范

| 用途 | 色值 | 说明 |
|------|------|------|
| **强调色** | `#D97757` | 图标、关键词、分隔线 |
| **深色文字** | `#2D2A26` | 主标题 |
| **次级文字** | `#3D3832` | 内页正文 |
| **弱化文字** | `#7A756E` | 副标题 |
| **辅助文字** | `#9A958E` | 引用语 |
| **底部文字** | `#B5B0A8` | 页码、底部信息 |
| **背景浅端** | `#FAF9F7` | 渐变背景起点 |
| **背景深端** | `#F5F3F0` | 渐变背景终点 |

---

## 星座图标规范

**必须使用 SVG 线性图标**，从 `zodiac-symbols.json` 获取。

### 封面图标（突出显示）

```css
.zodiac-icon svg {
  width: 80px;          /* 封面使用大尺寸 */
  height: 80px;
  stroke: #D97757;      /* 必须使用强调色 */
  stroke-width: 1.5;
  fill: none;           /* 无填充 */
}

/* 柔和光晕效果 */
.zodiac-glow::before {
  width: 160px;
  height: 160px;
  background: radial-gradient(circle, rgba(217, 119, 87, 0.08) 0%, rgba(217, 119, 87, 0) 70%);
  border-radius: 50%;
}
```

### 内页/结尾页图标（标准尺寸）

```css
.zodiac-icon svg {
  width: 52px;          /* 内页使用标准尺寸 */
  height: 52px;
  stroke: #D97757;
  stroke-width: 1.5;
  fill: none;
}
```

**双子座示例**：
```html
<div class="zodiac-icon">
  <svg viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
    <line x1="12" y1="10" x2="38" y2="10" stroke-linecap="round"/>
    <line x1="12" y1="40" x2="38" y2="40" stroke-linecap="round"/>
    <line x1="18" y1="10" x2="18" y2="40" stroke-linecap="round"/>
    <line x1="32" y1="10" x2="32" y2="40" stroke-linecap="round"/>
  </svg>
</div>
```

---

## 画布尺寸与基础设置

**尺寸**：1080px × 1440px（3:4 比例）

### 通用基础样式

```css
:root, html, body {
  color-scheme: light only;
  background: #FAF9F7;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

.poster {
  width: 1080px;
  height: 1440px;
  position: relative;
  background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%);
  font-family: 'Noto Serif SC', serif;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 喷砂纸质纹理 - 更细腻 */
.poster::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
  z-index: 1;
}
```

---

## 封面布局规范

### 结构

```
┌─────────────────────────────────────┐
│                                     │
│          ╭─────────────╮            │  ← top: 100px
│          │  [星座图标]  │            │  ← 80px 图标 + 柔和光晕
│          ╰─────────────╯            │
│             GEMINI                  │
│              双子座                  │
│                                     │
│         最怕的不是孤独               │  ← 垂直居中
│          是被束缚                    │
│                                     │
│            ───                      │  ← 分隔线
│                                     │
│        自由比什么都重要              │
│                                     │
│                                     │
│          情感独白                    │  ← bottom: 100px
│                                     │
└─────────────────────────────────────┘
```

### 设计要点

- **星座图标放大**：从 52px 增大到 80px，更醒目
- **柔和光晕**：图标背后添加 160px 半透明圆形光晕，不突兀
- **双语标识**：英文名 + 中文名，强化星座识别
- **视觉层次**：图标区域作为视觉入口，引导阅读

### 完整封面 HTML

```html
<!-- [STYLE LOCK: 极简留白] [LAYOUT LOCK: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>封面 - {{TITLE}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body { color-scheme: light only; background: #FAF9F7; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .poster {
      width: 1080px;
      height: 1440px;
      position: relative;
      background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%);
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .poster::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.03;
      pointer-events: none;
      z-index: 1;
    }
    .zodiac-badge {
      position: absolute;
      top: 100px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 10;
    }
    .zodiac-glow {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .zodiac-glow::before {
      content: '';
      position: absolute;
      width: 160px;
      height: 160px;
      background: radial-gradient(circle, rgba(217, 119, 87, 0.08) 0%, rgba(217, 119, 87, 0) 70%);
      border-radius: 50%;
      z-index: -1;
    }
    .zodiac-icon svg {
      width: 80px;
      height: 80px;
      stroke: #D97757;
      stroke-width: 1.5;
      fill: none;
    }
    .zodiac-cn {
      margin-top: 24px;
      font-size: 28px;
      font-weight: 500;
      color: #D97757;
      letter-spacing: 10px;
      text-indent: 10px;
    }
    .zodiac-en {
      margin-top: 8px;
      font-size: 14px;
      font-weight: 400;
      color: #9A958E;
      letter-spacing: 6px;
      text-indent: 6px;
    }
    .main {
      position: relative;
      z-index: 10;
      text-align: center;
      padding: 0 100px;
      margin-top: 60px;
    }
    .main-title {
      font-size: 62px;
      font-weight: 500;
      color: #2D2A26;
      letter-spacing: 3px;
      line-height: 1.7;
      margin-bottom: 60px;
    }
    .accent {
      color: #D97757;
      font-weight: 500;
    }
    .sub-line {
      width: 50px;
      height: 1px;
      background: #D97757;
      margin: 0 auto 45px;
    }
    .sub-title {
      font-size: 24px;
      font-weight: 300;
      color: #7A756E;
      letter-spacing: 5px;
    }
    .footer {
      position: absolute;
      bottom: 100px;
      left: 50%;
      transform: translateX(-50%);
      text-align: center;
      z-index: 10;
    }
    .footer-text {
      font-size: 15px;
      font-weight: 400;
      color: #B5B0A8;
      letter-spacing: 6px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-badge">
      <div class="zodiac-glow">
        <div class="zodiac-icon">
          {{ZODIAC_SVG}}
        </div>
      </div>
      <div class="zodiac-cn">{{ZODIAC_CN}}</div>
      <div class="zodiac-en">{{ZODIAC_EN}}</div>
    </div>
    <div class="main">
      <h1 class="main-title">
        {{HEADLINE}}
      </h1>
      <div class="sub-line"></div>
      <p class="sub-title">{{SUB_TITLE}}</p>
    </div>
    <div class="footer">
      <span class="footer-text">情感独白</span>
    </div>
  </div>
</body>
</html>
```

---

## 内页布局规范

### 结构

```
┌─────────────────────────────────────┐
│                                     │
│              · 01 ·                 │  ← top: 100px (页码标识)
│                                     │
│                                     │
│            不是怕孤独                │  ← 小标题（强调色）
│                                     │
│         我们双子座啊                 │  ← 正文内容
│      真正怕的从来不是一个人待着       │
│                                     │
│     怕的是那种事事都要报备的感觉      │
│                                     │
│                                     │
│  「 孤独不可怕，失去自由才可怕 」     │  ← 引用语
│                                     │
│                                     │
│               02                    │  ← bottom: 100px (页码)
│                                     │
└─────────────────────────────────────┘
```

### 完整内页 HTML

```html
<!-- [STYLE LOCK: 极简留白] [LAYOUT LOCK: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {{PAGE_NUM}} - {{SECTION_TITLE}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body { color-scheme: light only; background: #FAF9F7; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .poster {
      width: 1080px;
      height: 1440px;
      position: relative;
      background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%);
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .poster::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.03;
      pointer-events: none;
      z-index: 1;
    }
    .part-label {
      position: absolute;
      top: 100px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 14px;
      font-weight: 400;
      color: #D97757;
      letter-spacing: 8px;
      z-index: 10;
    }
    .main {
      position: relative;
      z-index: 10;
      text-align: center;
      padding: 0 100px;
      max-width: 900px;
    }
    .section-title {
      font-size: 42px;
      font-weight: 500;
      color: #D97757;
      letter-spacing: 6px;
      margin-bottom: 60px;
    }
    .content {
      font-size: 32px;
      font-weight: 400;
      color: #3D3832;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: center;
    }
    .accent {
      color: #D97757;
      font-weight: 500;
    }
    .quote {
      margin-top: 70px;
      font-size: 22px;
      font-weight: 300;
      color: #9A958E;
      letter-spacing: 3px;
    }
    .footer {
      position: absolute;
      bottom: 100px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
    }
    .page-num {
      font-size: 14px;
      font-weight: 400;
      color: #B5B0A8;
      letter-spacing: 4px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="part-label">· {{PART_NUM}} ·</div>
    <div class="main">
      <h2 class="section-title">{{SECTION_TITLE}}</h2>
      <p class="content">
        {{CONTENT}}
      </p>
      <p class="quote">{{QUOTE}}</p>
    </div>
    <div class="footer">
      <span class="page-num">{{PAGE_NUM}}</span>
    </div>
  </div>
</body>
</html>
```

---

## 结尾页布局规范

结尾页带有星座图标，视觉上呼应封面。

### 完整结尾页 HTML

```html
<!-- [STYLE LOCK: 极简留白] [LAYOUT LOCK: A] -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>Page {{PAGE_NUM}} - {{SECTION_TITLE}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root, html, body { color-scheme: light only; background: #FAF9F7; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .poster {
      width: 1080px;
      height: 1440px;
      position: relative;
      background: linear-gradient(180deg, #FAF9F7 0%, #F5F3F0 100%);
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .poster::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      opacity: 0.03;
      pointer-events: none;
      z-index: 1;
    }
    .zodiac-badge {
      position: absolute;
      top: 120px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 10;
    }
    .zodiac-icon svg {
      width: 52px;
      height: 52px;
      stroke: #D97757;
      stroke-width: 1.5;
      fill: none;
    }
    .zodiac-name {
      margin-top: 20px;
      font-size: 18px;
      font-weight: 400;
      color: #D97757;
      letter-spacing: 10px;
      text-indent: 10px;
    }
    .main {
      position: relative;
      z-index: 10;
      text-align: center;
      padding: 0 100px;
      margin-top: 60px;
    }
    .section-title {
      font-size: 46px;
      font-weight: 500;
      color: #D97757;
      letter-spacing: 6px;
      margin-bottom: 60px;
    }
    .content {
      font-size: 32px;
      font-weight: 400;
      color: #3D3832;
      line-height: 2.2;
      letter-spacing: 2px;
      text-align: center;
    }
    .accent {
      color: #D97757;
      font-weight: 500;
    }
    .end-mark {
      margin-top: 60px;
      font-size: 28px;
      color: #D97757;
    }
    .footer {
      position: absolute;
      bottom: 100px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
    }
    .page-num {
      font-size: 14px;
      font-weight: 400;
      color: #B5B0A8;
      letter-spacing: 4px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="zodiac-badge">
      <div class="zodiac-icon">
        {{ZODIAC_SVG}}
      </div>
      <div class="zodiac-name">{{ZODIAC_EN}}</div>
    </div>
    <div class="main">
      <h2 class="section-title">{{SECTION_TITLE}}</h2>
      <p class="content">
        {{CONTENT}}
      </p>
      <div class="end-mark">✦</div>
    </div>
    <div class="footer">
      <span class="page-num">{{PAGE_NUM}}</span>
    </div>
  </div>
</body>
</html>
```

---

## 变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC_SVG}}` | 星座 SVG 图标代码 | 从 zodiac-symbols.json 获取 |
| `{{ZODIAC_EN}}` | 星座英文名 | GEMINI |
| `{{ZODIAC_CN}}` | 星座中文名 | 双子座 |
| `{{TITLE}}` | 完整标题 | 双子座最怕的不是孤独，是被束缚 |
| `{{HEADLINE}}` | 封面主标题（带换行和强调） | 最怕的不是`<span class="accent">`孤独`</span>` |
| `{{SUB_TITLE}}` | 副标题 | 自由比什么都重要 |
| `{{SECTION_TITLE}}` | 内页小标题 | 不是怕孤独 |
| `{{CONTENT}}` | 内页正文内容 | 我们双子座啊... |
| `{{QUOTE}}` | 引用语 | 「 孤独不可怕，失去自由才可怕 」 |
| `{{PAGE_NUM}}` | 页码（两位数） | 02 |
| `{{PART_NUM}}` | 章节编号 | 01 |

---

## 与动态编辑风的区别

| 特性 | 极简留白 | 动态编辑风 |
|------|----------|-----------|
| 布局方式 | 垂直居中 | 绝对定位 |
| 星座图标位置 | 顶部居中 | 右上角 |
| 背景渐变 | 180deg 垂直 | 165deg 斜向 |
| 强调色 | `#D97757` | `#C15F3C` |
| 底部装饰 | 无 | 渐变色带 |
| 纹理透明度 | 0.03 | 0.05 |
| 整体风格 | 简约、留白、呼吸感 | 杂志、编辑、动态感 |

---

## 使用场景

- 情感类内容（爱情、友情、亲情）
- 治愈系文案
- 哲理思考
- 星座性格分析
- 需要大量留白的设计

---

## 注意事项

1. **保持一致性**：同一套图必须使用相同的 STYLE LOCK 和 LAYOUT LOCK
2. **关键词强调**：使用 `<span class="accent">关键词</span>` 标记重点
3. **换行控制**：使用 `<br/>` 控制文字换行
4. **引用语格式**：使用「 」包裹引用内容
