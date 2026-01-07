# 命定之约风 (Destined Bond) SVG 模板规范

**格式**：纯 SVG（不使用 HTML/CSS）
**特征**：双星座对称布局 + 无限符号连接 + 暖棕配色 + 配对指数展示
**适用**：星座配对、CP分析、缘分解读、关系解析

---

## 配色系统

| 用途 | 色值 | SVG属性 |
|------|------|---------|
| **主强调色** | `#B86B4A` | fill / stroke |
| **辅助强调色** | `#8B7355` | fill / stroke |
| **主文字** | `#4A3F35` | fill |
| **次要文字** | `#7D7067` | fill |
| **分隔线/装饰** | `#D4C9BE` | stroke |

### 背景渐变定义

```svg
<defs>
  <!-- 主背景渐变 (165度) -->
  <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#FDF8F4"/>
    <stop offset="50%" stop-color="#F8EDE5"/>
    <stop offset="100%" stop-color="#F2E4D8"/>
  </linearGradient>

  <!-- 光照叠加层 -->
  <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/>
    <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
    <stop offset="80%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
  </linearGradient>
</defs>
```

---

## 尺寸规范

**画布**：1080px × 1440px

| 元素 | 尺寸 | 说明 |
|------|------|------|
| 左右边距 | 100px | 内容区 x: 100 ~ 980 |
| 上下边距 | 90px | 内容区 y: 90 ~ 1350 |
| 页眉星座名 | 32px | font-weight: 500 |
| **封面主标题** | **72px** | font-weight: 600, letter-spacing: 6 |
| 章节标题 | 56px | font-weight: 600 |
| 正文 | 32px | line-height: 61px |
| 引用文字 | 28px | font-style: italic |
| 页码 | 28px | font-family: Georgia |
| 星座图标 | 80×80px | 双图标对称布局 |
| 无限符号 | 40×20px | 连接两星座 |

---

## 字体加载

```svg
<defs>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
  </style>
</defs>
```

---

## 核心设计元素

### 1. 双星座图标布局（封面专用）

```svg
<!-- 双星座对称布局 -->
<g id="dual-zodiac" transform="translate(540, 350)">
  <!-- 左星座 -->
  <g transform="translate(-120, 0)">
    {{ZODIAC1_SVG}}
  </g>

  <!-- 无限符号连接 -->
  <g transform="translate(0, 40)">
    <path d="M-25,0 C-25,-15 -10,-15 0,0 C10,15 25,15 25,0 C25,-15 10,-15 0,0 C-10,15 -25,15 -25,0"
          fill="none" stroke="#B86B4A" stroke-width="2"/>
  </g>

  <!-- 右星座 -->
  <g transform="translate(120, 0)">
    {{ZODIAC2_SVG}}
  </g>
</g>
```

### 2. 配对指数展示

```svg
<!-- 配对指数 -->
<g id="match-index" transform="translate(540, 520)">
  <text x="0" y="0" font-family="Georgia, serif" font-size="20" fill="#8B7355" text-anchor="middle" letter-spacing="4">MATCH INDEX</text>
  <text x="0" y="50" font-family="Georgia, serif" font-size="64" font-weight="600" fill="#B86B4A" text-anchor="middle">{{MATCH_PERCENT}}%</text>
</g>
```

### 3. 页眉结构

```svg
<g id="header">
  <!-- 星座配对名 -->
  <text x="100" y="130"
        font-family="Noto Serif SC, serif"
        font-size="32"
        font-weight="500"
        fill="#B86B4A"
        letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>

  <!-- 分隔符 -->
  <text x="280" y="130"
        font-family="Georgia, serif"
        font-size="24"
        fill="#D4C9BE">·</text>

  <!-- 主题词 -->
  <text x="310" y="130"
        font-family="Noto Sans SC, sans-serif"
        font-size="24"
        font-weight="300"
        fill="#7D7067"
        letter-spacing="3">命定之约</text>

  <!-- 右上角装饰：小无限符号 -->
  <g transform="translate(940, 110)">
    <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0"
          fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
  </g>
</g>
```

### 4. 页脚结构

```svg
<g id="footer">
  <!-- 分隔线 -->
  <line x1="100" y1="1350" x2="980" y2="1350"
        stroke="#D4C9BE" stroke-width="2"/>

  <!-- 页码 -->
  <text x="980" y="1390"
        font-family="Georgia, serif"
        font-size="28"
        fill="#7D7067"
        text-anchor="end"
        letter-spacing="4">{{PAGE_NUM}}</text>
</g>
```

---

## 封面模板

```svg
<!-- [STYLE: 命定之约风] [TYPE: cover] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/>
      <stop offset="50%" stop-color="#F8EDE5"/>
      <stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#B86B4A" letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>
    <text x="280" y="130" font-family="Georgia, serif" font-size="24" fill="#D4C9BE">·</text>
    <text x="310" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#7D7067" letter-spacing="3">命定之约</text>
    <g transform="translate(940, 110)">
      <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
    </g>
  </g>

  <!-- 双星座对称布局 -->
  <g id="dual-zodiac" transform="translate(540, 320)">
    <!-- 左星座 -->
    <g transform="translate(-120, 0)">
      {{ZODIAC1_SVG_LARGE}}
    </g>

    <!-- 无限符号连接 -->
    <g transform="translate(0, 40)">
      <path d="M-25,0 C-25,-15 -10,-15 0,0 C10,15 25,15 25,0 C25,-15 10,-15 0,0 C-10,15 -25,15 -25,0" fill="none" stroke="#B86B4A" stroke-width="2.5"/>
    </g>

    <!-- 右星座 -->
    <g transform="translate(120, 0)">
      {{ZODIAC2_SVG_LARGE}}
    </g>
  </g>

  <!-- 配对指数 -->
  <g id="match-index" transform="translate(540, 500)">
    <text x="0" y="0" font-family="Georgia, serif" font-size="20" fill="#8B7355" text-anchor="middle" letter-spacing="4">MATCH INDEX</text>
    <text x="0" y="55" font-family="Georgia, serif" font-size="64" font-weight="600" fill="#B86B4A" text-anchor="middle">{{MATCH_PERCENT}}%</text>
  </g>

  <!-- 分隔线 -->
  <rect x="490" y="600" width="100" height="3" fill="#B86B4A"/>

  <!-- 封面标题 -->
  <g id="cover-title" transform="translate(540, 720)">
    <text x="0" y="0" font-family="Noto Serif SC, serif" font-size="72" font-weight="600" fill="#4A3F35" text-anchor="middle" letter-spacing="6">{{TITLE}}</text>
    <text x="0" y="80" font-family="Noto Serif SC, serif" font-size="32" fill="#7D7067" text-anchor="middle" letter-spacing="4">{{SUBTITLE}}</text>
  </g>

  <!-- 标语 -->
  <g id="tagline" transform="translate(540, 920)">
    <text x="0" y="0" font-family="Noto Serif SC, serif" font-size="28" fill="#7D7067" text-anchor="middle" letter-spacing="3">{{TAGLINE_LINE1}}</text>
    <text x="0" y="50" font-family="Noto Serif SC, serif" font-size="28" text-anchor="middle" letter-spacing="3">
      <tspan fill="#B86B4A">{{TAGLINE_HIGHLIGHT}}</tspan><tspan fill="#7D7067">{{TAGLINE_REST}}</tspan>
    </text>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#7D7067" text-anchor="end" letter-spacing="4">0 1</text>
  </g>
</svg>
```

### 封面变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC1}}` | 星座1名 | 射手座 |
| `{{ZODIAC2}}` | 星座2名 | 狮子座 |
| `{{ZODIAC1_SVG_LARGE}}` | 星座1图标(80px) | `<svg>...</svg>` |
| `{{ZODIAC2_SVG_LARGE}}` | 星座2图标(80px) | `<svg>...</svg>` |
| `{{MATCH_PERCENT}}` | 配对指数 | 85 |
| `{{TITLE}}` | 主标题 | 命中注定 |
| `{{SUBTITLE}}` | 副标题 | 火象最佳CP |
| `{{TAGLINE_LINE1}}` | 标语第一行 | 两个人在一起 |
| `{{TAGLINE_HIGHLIGHT}}` | 标语高亮 | 发光发热 |
| `{{TAGLINE_REST}}` | 标语剩余 | 谁也不用收敛 |

---

## 内页模板

```svg
<!-- [STYLE: 命定之约风] [TYPE: page] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/>
      <stop offset="50%" stop-color="#F8EDE5"/>
      <stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#B86B4A" letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>
    <text x="280" y="130" font-family="Georgia, serif" font-size="24" fill="#D4C9BE">·</text>
    <text x="310" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#7D7067" letter-spacing="3">命定之约</text>
    <g transform="translate(940, 110)">
      <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
    </g>
  </g>

  <!-- 章节标签 -->
  <text x="100" y="220" font-family="Georgia, serif" font-size="24" fill="#B86B4A" letter-spacing="6">BOND {{PART_NUM}}</text>

  <!-- 章节标题 -->
  <text x="100" y="310" font-family="Noto Serif SC, serif" font-size="56" font-weight="600" fill="#4A3F35" letter-spacing="4">{{SECTION_TITLE}}</text>

  <!-- 分隔线 -->
  <rect x="100" y="340" width="80" height="3" fill="#B86B4A"/>

  <!-- 正文内容 -->
  <g id="content" transform="translate(100, 520)">
    {{CONTENT_LINES}}
  </g>

  <!-- 引用区块 -->
  <g id="quote" transform="translate(100, 1050)">
    <!-- 左边框 -->
    <line x1="0" y1="0" x2="0" y2="60" stroke="#B86B4A" stroke-width="3"/>
    <!-- 引用文字 -->
    <text x="30" y="40" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#7D7067" letter-spacing="2">"{{QUOTE}}"</text>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#7D7067" text-anchor="end" letter-spacing="4">{{PAGE_NUM}}</text>
  </g>
</svg>
```

### 正文内容生成规则

**每行文本模板**：
```svg
<text y="{{LINE_Y}}" font-family="Noto Serif SC, serif" font-size="32" fill="#4A3F35" letter-spacing="2">
  <tspan fill="#4A3F35">{{TEXT_BEFORE}}</tspan>
  <tspan fill="#B86B4A">{{HIGHLIGHT}}</tspan>
  <tspan fill="#4A3F35">{{TEXT_AFTER}}</tspan>
</text>
```

**行间距**：61px（y递增）

---

## 结尾页模板

```svg
<!-- [STYLE: 命定之约风] [TYPE: end] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDF8F4"/>
      <stop offset="50%" stop-color="#F8EDE5"/>
      <stop offset="100%" stop-color="#F2E4D8"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.25"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.02"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#B86B4A" letter-spacing="2">{{ZODIAC1}} × {{ZODIAC2}}</text>
    <text x="280" y="130" font-family="Georgia, serif" font-size="24" fill="#D4C9BE">·</text>
    <text x="310" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#7D7067" letter-spacing="3">命定之约</text>
    <g transform="translate(940, 110)">
      <path d="M-15,0 C-15,-10 -5,-10 0,0 C5,10 15,10 15,0 C15,-10 5,-10 0,0 C-5,10 -15,10 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" opacity="0.6"/>
    </g>
  </g>

  <!-- 居中内容区域 -->
  <g id="centered-content" transform="translate(540, 0)">
    <!-- 章节标签 -->
    <text x="0" y="220" font-family="Georgia, serif" font-size="24" fill="#B86B4A" letter-spacing="6" text-anchor="middle">DESTINY</text>

    <!-- 双星座小图标 -->
    <g transform="translate(0, 280)">
      <g transform="translate(-60, 0) scale(0.7)">{{ZODIAC1_SVG}}</g>
      <path d="M-15,0 C-15,-8 -5,-8 0,0 C5,8 15,8 15,0 C15,-8 5,-8 0,0 C-5,8 -15,8 -15,0" fill="none" stroke="#B86B4A" stroke-width="1.5" transform="translate(0, 25)"/>
      <g transform="translate(60, 0) scale(0.7)">{{ZODIAC2_SVG}}</g>
    </g>

    <!-- 分隔线 -->
    <rect x="-40" y="360" width="80" height="3" fill="#B86B4A"/>

    <!-- 主文案区域 -->
    <g id="summary" transform="translate(0, 480)">
      {{CONTENT_LINES}}
    </g>

    <!-- 装饰分隔线 -->
    <g id="content-divider" transform="translate(0, 780)">
      <line x1="-70" y1="0" x2="-20" y2="0" stroke="#D4C9BE" stroke-width="1"/>
      <path d="M-8,0 C-8,-5 -3,-5 0,0 C3,5 8,5 8,0 C8,-5 3,-5 0,0 C-3,5 -8,5 -8,0" fill="none" stroke="#B86B4A" stroke-width="1.5"/>
      <line x1="20" y1="0" x2="70" y2="0" stroke="#D4C9BE" stroke-width="1"/>
    </g>

    <!-- 祝福语区域 -->
    <g id="ending" transform="translate(0, 880)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#7D7067" text-anchor="middle" letter-spacing="3">{{ENDING_LINE1}}</text>
      <text y="50" font-family="Noto Serif SC, serif" font-size="26" font-style="italic" fill="#7D7067" text-anchor="middle" letter-spacing="3">{{ENDING_LINE2}}</text>

      <!-- END 标记 -->
      <g transform="translate(0, 120)">
        <line x1="-80" y1="0" x2="-25" y2="0" stroke="#D4C9BE" stroke-width="2"/>
        <text x="0" y="8" font-family="Georgia, serif" font-size="22" fill="#B86B4A" text-anchor="middle" letter-spacing="5">BOND</text>
        <line x1="25" y1="0" x2="80" y2="0" stroke="#D4C9BE" stroke-width="2"/>
      </g>
    </g>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4C9BE" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#7D7067" text-anchor="end" letter-spacing="4">{{PAGE_NUM}}</text>
  </g>
</svg>
```

---

## 高亮词规则

### 封面（必须2个）
- 标语1个高亮
- 使用 `fill="#B86B4A"`

### 内页（必须2个呼应对）
- 使用 `<tspan fill="#B86B4A">` 包裹高亮词
- 两个词形成语义呼应

### 结尾页（1-2个）
- 与封面形成首尾呼应

---

## 章节标题建议

| 章节 | 标题示例 |
|------|----------|
| BOND 01 | 初见时刻 |
| BOND 02 | 相处模式 |
| BOND 03 | 争执瞬间 |
| BOND 04 | 心动时刻 |
| BOND 05 | 挑战关卡 |
| DESTINY | 命定结语 |

---

## 检查清单

### 基础检查
- [ ] 画布尺寸 1080×1440
- [ ] 背景渐变定义正确（暖棕色系）
- [ ] 字体 @import 已添加
- [ ] 页眉结构完整（双星座名+分隔符+主题词+无限符号）
- [ ] 页脚分隔线 + 右对齐页码
- [ ] 页码格式 "0 X"（带空格）

### 特色元素检查
- [ ] 封面有双星座对称布局
- [ ] 封面有配对指数展示
- [ ] 封面有无限符号连接
- [ ] 页眉右上角有小无限符号装饰
- [ ] 结尾页有双星座小图标

### 高亮检查
- [ ] 封面：标语1个高亮词
- [ ] 内页：2个高亮词呼应对
- [ ] 结尾页：1-2个高亮词
- [ ] 高亮使用 `fill="#B86B4A"`

### 结尾页专项检查
- [ ] 有装饰分隔线（小无限符号）
- [ ] 主文案使用正体 32px
- [ ] 祝福语使用斜体 26px
- [ ] END 标记改为 BOND
