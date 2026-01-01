# 动态编辑风 (Editorial Dynamic) 封面模板规范

## 设计理念

与 `editorial-warm` 的静态居中布局不同，本模板强调：

- **打破对称** — 使用非对称布局，增加视觉张力
- **独特装饰** — 每个封面根据主题设计专属装饰元素
- **大面积重点色** — 重点色用于色块、装饰线、渐变条等大面积元素
- **视觉冲击** — 更强的视觉层次和吸引力

---

## 示例效果

### 封面示例

![封面示例](examples/cover-example.png)

**特点**：斜线装饰 + 非对称布局 + 色块副标题 + 关键词下划线

### 内容页示例

![内容页示例](examples/page-example.png)

**特点**：左对齐正文 + 重点色强调词 + 引用区块

---

## 画布尺寸

**尺寸**：1080px × 1440px（3:4 比例）

---

## 配色规范

### 基础色板

| 用途 | 色值 | 说明 |
|------|------|------|
| 重点色 | `#C15F3C` | 赭红/珊瑚橙，用于强调 |
| 重点色渐变 | `#C15F3C → #D4765A` | 用于色块渐变 |
| 主文字 | `#2D2D2D` | 深灰，标题 |
| 次文字 | `#3D3D3D` | 次深灰，副标题 |
| 正文 | `#5A5A5A` ~ `#7A7A7A` | 中灰，段落文字 |
| 弱化文字 | `#9A958A` ~ `#B1ADA1` | 浅灰，标签/页码/引用 |

### 装饰色（重点色透明度变体）

| 透明度 | 色值 | 用途 |
|--------|------|------|
| 4-6% | `rgba(193,95,60,0.04-0.06)` | 大字号背景装饰 |
| 8-10% | `rgba(193,95,60,0.08-0.1)` | 圆形填充装饰 |
| 15% | `rgba(193,95,60,0.15)` | 淡色图标/边框 |
| 20-25% | `rgba(193,95,60,0.2-0.25)` | 关键词下划线 |

### 背景渐变

```css
/* 渐变方向可根据内容调整：150°/165°/180° */
.poster {
  background: linear-gradient(
    165deg,
    #FAF6F1 0%,
    #F5EDE4 50%,
    #F0E6D9 100%
  );
}
```

### 纸张纹理

```css
.poster::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,...");
  opacity: 0.04-0.06;  /* 根据背景调整 */
  pointer-events: none;
  z-index: 1;
}
```

---

## 字体规范

```css
font-family: 'Noto Serif SC', serif;
```

| 元素 | 字号 | 字重 | 字距 |
|------|------|------|------|
| **日期+星座** | **48-56px** | **600** | **4-6px** |
| 主标题 | 72-84px | 500-600 | 2-4px |
| 副标题/强调 | 32-42px | 400-500 | 3-4px |
| 正文 | 28-32px | 400 | 2-3px |
| 标签 | 20-24px | 400 | 6-8px |
| 页码 | 24px | 400 | 4px |

### 每日运势专用样式

日期+星座是每日运势封面的**视觉焦点**，需要特别突出：

```css
.date-zodiac {
  font-size: 52px;           /* 大字号，一眼可见 */
  font-weight: 600;          /* 加粗强调 */
  color: #2D2D2D;            /* 深色主文字 */
  letter-spacing: 5px;       /* 舒适字距 */
  text-align: center;
  margin-bottom: 20px;
}

/* 可选：添加装饰下划线 */
.date-zodiac::after {
  content: '';
  display: block;
  width: 60%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #C15F3C, transparent);
  margin: 16px auto 0;
}
```

---

## 装饰元素库

### 1. 大字号背景文字

用于年份、月份等数字装饰。

```css
.year-bg {
  position: absolute;
  top: 180px; left: -60px;
  font-size: 320px;
  font-weight: 700;
  color: rgba(193, 95, 60, 0.06);
  letter-spacing: -20px;
  z-index: 0;
}
```

**适用主题**：年度运势、月运势、数字相关

### 2. 斜线装饰

体现张力和动感。

```css
.deco-line {
  position: absolute;
  width: 400px; height: 3px;
  background: linear-gradient(90deg, #C15F3C 0%, transparent 100%);
  transform: rotate(-35deg);
  top: 280px; right: -100px;
}
```

**适用主题**：性格解析、兴奋点、挑战类

### 3. 圆形装饰

体现温和、稳定。

```css
.circle-deco {
  position: absolute;
  width: 180px; height: 180px;
  border: 2px solid rgba(193, 95, 60, 0.15);
  border-radius: 50%;
}
.circle-inner {
  width: 100px; height: 100px;
  background: rgba(193, 95, 60, 0.08);
  border-radius: 50%;
}
```

**适用主题**：月运势、心态类、情感类

### 4. 竖线装饰组

体现规则感、条理性。

```css
.side-lines {
  position: absolute;
  left: 60px; top: 300px;
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

**适用主题**：规则清单、指南类、列表类

### 5. 箭头装饰

体现方向、指引。

```css
.arrow-deco svg {
  width: 200px; height: 200px;
  stroke: rgba(193, 95, 60, 0.12);
  stroke-width: 2;
  fill: none;
}
```

```html
<svg viewBox="0 0 100 100">
  <line x1="10" y1="90" x2="90" y2="10" stroke-linecap="round"/>
  <polyline points="60,10 90,10 90,40" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

**适用主题**：职业方向、选择类、规划类

### 6. 底部渐变色带

增加视觉完整度。

```css
.gradient-band {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 8px;
  background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
}
```

**适用主题**：通用，增强品牌感

### 7. 放大淡色星座图标

用于留白区域装饰。

```css
.zodiac-icon svg {
  width: 140px; height: 140px;
  stroke: rgba(193, 95, 60, 0.15);
  stroke-width: 1;
  fill: none;
}
```

**适用主题**：自由、孤独、情感类

---

## 布局变体

### A. 内容偏下 + 上方大留白

适合：自由、空间感主题

```
┌─────────────────────────────────┐
│ [标签]                          │
│                    [大淡色图标]  │
│                                 │
│                                 │
│                                 │
│ 主标题                          │
│ ────                            │
│ 副标题                          │
│                                 │
│ 「引用」                     01 │
└─────────────────────────────────┘
```

### B. 内容居中 + 背景大字装饰

适合：年份、月份、数字主题

```
┌─────────────────────────────────┐
│ [标签]              [星座图标]  │
│      ╔════════════════╗         │
│      ║   2026（淡色） ║         │
│      ╚════════════════╝         │
│         [关键词色块]            │
│           主标题                │
│          副标题                 │
│          「引用」               │
│ ─────────────────────────── 01 │
└─────────────────────────────────┘
```

### C. 左对齐 + 左侧装饰线

适合：规则、清单、列表主题

```
┌─────────────────────────────────┐
│ [标签]              [星座图标]  │
│ │                               │
│ │  [分类标签]                   │
│ │  主标题                       │
│ │                               │
│    01 列表项                    │
│    02 列表项                    │
│    03 列表项                    │
│                                 │
│    副标题                       │
│ ─────────────────────────── 01 │
└─────────────────────────────────┘
```

### D. 非对称 + 斜线装饰

适合：张力、兴奋、挑战主题

```
┌─────────────────────────────────┐
│ [标签]              [星座图标]  │
│                        ╲        │
│                         ╲       │
│ 前置标题                        │
│ 主标题                          │
│ [色块副标题]                    │
│                                 │
│ 描述文字                        │
│                                 │
│ 「引用」                     01 │
└─────────────────────────────────┘
```

---

## 重点色使用原则

### 必用场景（大面积）

1. **色块标签** — 关键词/分类标签背景
   ```css
   .keyword {
     display: inline-block;        /* 宽度自适应文字长度，不占满整行 */
     width: fit-content;           /* 确保宽度跟随内容 */
     background: linear-gradient(135deg, #C15F3C 0%, #D4765A 100%);
     color: #fff;
     font-size: 20-24px;
     letter-spacing: 6-8px;
     padding: 8px 20px;            /* 内边距提供呼吸空间 */
     border-radius: 2px;
     margin-bottom: 30-40px;
   }
   ```
   **⚠️ 重要**：色块宽度必须自适应文字长度，禁止使用 `width: 100%` 或 `display: block`

2. **装饰线** — 分隔线、竖线装饰
   ```css
   background: #C15F3C;
   /* 或渐变 */
   background: linear-gradient(90deg, #C15F3C 0%, transparent 100%);
   ```

3. **关键词下划线**
   ```css
   .keyword::after {
     height: 8-12px;
     background: rgba(193, 95, 60, 0.2-0.25);
   }
   ```

### 必用场景（小面积）

4. **星座图标** — stroke: #C15F3C
5. **强调文字** — color: #C15F3C
6. **左边框装饰** — border-left: 3px solid #C15F3C

### 可选场景

7. **底部渐变色带**
8. **圆形装饰边框/填充**

---

## 星座图标 SVG

射手座（♐）线性图标：

```html
<svg viewBox="0 0 50 50">
  <line x1="8" y1="42" x2="42" y2="8" stroke-linecap="round"/>
  <polyline points="30,8 42,8 42,20" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="18" y1="32" x2="32" y2="18" stroke-linecap="round"/>
  <line x1="12" y1="28" x2="22" y2="38" stroke-linecap="round"/>
</svg>
```

样式根据用途调整：
- 标准：`stroke: #C15F3C; stroke-width: 1.5;`
- 装饰（淡）：`stroke: rgba(193,95,60,0.15); stroke-width: 1;`
- 装饰（大）：`width: 140px; height: 140px;`

---

## 封面结构示例

### 通用元素

```html
<div class="poster">
  <!-- 装饰元素（根据主题选择） -->
  <div class="装饰元素"></div>

  <!-- 顶部 -->
  <div class="header">
    <span class="tag">星座 · 主题</span>
    <div class="zodiac-icon">...</div>
  </div>

  <!-- 主内容 -->
  <div class="main">
    <div class="keyword">分类标签</div>
    <h1 class="main-title">主标题<span class="accent">强调词</span></h1>
    <p class="sub-title">副标题</p>
    <p class="quote">「 引用/金句 」</p>
  </div>

  <!-- 底部 -->
  <div class="footer">
    <span class="footer-text">附加信息</span>
    <span class="page-num">01</span>
  </div>
</div>
```

---

## 主题与装饰对照表

| 主题类型 | 推荐装饰 | 布局变体 |
|---------|---------|---------|
| 年运势/月运势 | 大字号背景 + 圆形装饰 | B |
| 自由/孤独/情感 | 大留白 + 放大淡色图标 | A |
| 性格/兴奋点 | 斜线装饰 + 色块副标题 | D |
| 规则/清单/指南 | 左侧竖线 + 编号列表 | C |
| 职业/方向/选择 | 箭头装饰 + 关键词标签组 | B/C |

---

## 质量检查清单

- [ ] 布局打破居中对称，有视觉变化
- [ ] 根据主题选择了合适的装饰元素
- [ ] 重点色用于大面积装饰（色块/线条）
- [ ] 装饰元素不干扰主要内容阅读
- [ ] 纸张纹理已添加（opacity 0.04-0.06）
- [ ] 字体使用思源宋体 (Noto Serif SC)
- [ ] 页码位于右下角
- [ ] 整体视觉层次清晰
