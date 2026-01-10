# 性格独白风 (Personality Monologue) SVG 模板规范

**格式**：纯 SVG（不使用 HTML/CSS）
**特征**：三段式布局（页眉+内容+页脚）+ 渐变背景 + 光照叠加 + 页码系统
**适用**：星座性格深度解读、情感独白、治愈系内容

---

## 配色系统

| 用途 | 色值 | SVG属性 |
|------|------|---------|
| **强调色** | `#C4653A` | fill / stroke |
| **主文字** | `#3D3835` | fill |
| **次要文字** | `#6B6461` | fill |
| **分隔线** | `#D4CFC8` | stroke |

### 背景渐变定义

```svg
<defs>
  <!-- 主背景渐变 (165°) -->
  <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#FAF6F1"/>
    <stop offset="50%" stop-color="#F5EDE4"/>
    <stop offset="100%" stop-color="#F0E6D9"/>
  </linearGradient>

  <!-- 光照叠加层 -->
  <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="#FFF" stop-opacity="0.3"/>
    <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
    <stop offset="80%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity="0.03"/>
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
| 主题词 | 24px | font-weight: 300 |
| **封面主标题** | **72px** | font-weight: 600, letter-spacing: 6 |
| 章节标题 | 64px | font-weight: 600 |
| 正文 | 32px | line-height: 61px |
| 引用文字 | 28px | font-style: italic |
| 页码 | 28px | font-family: Georgia |
| 分隔线 | 100×4px | 强调色 |
| 星座图标 | 56×56px | rotate(-10deg) |

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

## 通用结构

### 页眉（所有页面必须）

```svg
<g id="header">
  <!-- 星座名 -->
  <text x="100" y="130"
        font-family="Noto Serif SC, serif"
        font-size="32"
        font-weight="500"
        fill="#C4653A"
        letter-spacing="2">{{ZODIAC}}</text>

  <!-- 分隔符 -->
  <text x="210" y="130"
        font-family="Georgia, serif"
        font-size="24"
        fill="#D4CFC8">·</text>

  <!-- 主题词 -->
  <text x="240" y="130"
        font-family="Noto Sans SC, sans-serif"
        font-size="24"
        font-weight="300"
        fill="#6B6461"
        letter-spacing="3">{{TOPIC}}</text>

  <!-- 星座图标 -->
  <g transform="translate(924, 74) rotate(-10)">
    {{ZODIAC_SVG}}
  </g>
</g>
```

### 页脚（所有页面必须）

```svg
<g id="footer">
  <!-- 分隔线 -->
  <line x1="100" y1="1350" x2="980" y2="1350"
        stroke="#D4CFC8" stroke-width="2"/>

  <!-- 页码 -->
  <text x="980" y="1390"
        font-family="Georgia, serif"
        font-size="28"
        fill="#6B6461"
        text-anchor="end"
        letter-spacing="4">{{PAGE_NUM}}</text>
</g>
```

---

## 封面模板

```svg
<!-- [STYLE: 性格独白风] [TYPE: cover] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FAF6F1"/>
      <stop offset="50%" stop-color="#F5EDE4"/>
      <stop offset="100%" stop-color="#F0E6D9"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.3"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.03"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#C4653A" letter-spacing="2">{{ZODIAC}}</text>
    <text x="210" y="130" font-family="Georgia, serif" font-size="24" fill="#D4CFC8">·</text>
    <text x="240" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#6B6461" letter-spacing="3">{{TOPIC}}</text>
    <g transform="translate(924, 74) rotate(-10)">
      {{ZODIAC_SVG}}
    </g>
  </g>

  <!-- 封面内容 -->
  <g id="cover-content">
    <!-- 副标题 -->
    <text x="540" y="520" font-family="Noto Serif SC, serif" font-size="32" fill="#6B6461" text-anchor="middle" letter-spacing="6">{{SUBTITLE}}</text>

    <!-- 主标题（支持单行/双行两种模式） -->
    <!-- 模式A: 单行标题（使用 tspan 实现内联高亮） -->
    <text x="540" y="660" font-family="Noto Serif SC, serif" font-size="72" font-weight="600" text-anchor="middle" letter-spacing="6">
      <tspan fill="#3D3835">{{TITLE_BEFORE}}</tspan><tspan fill="#C4653A">{{TITLE_HIGHLIGHT}}</tspan><tspan fill="#3D3835">{{TITLE_AFTER}}</tspan>
    </text>
    <!-- 模式B: 双行标题（第二行整行高亮，可选） -->
    <text x="540" y="750" font-family="Noto Serif SC, serif" font-size="72" font-weight="600" fill="#C4653A" text-anchor="middle" letter-spacing="6">{{TITLE_LINE2}}</text>

    <!-- 分隔线 -->
    <rect x="490" y="830" width="100" height="4" fill="#C4653A"/>

    <!-- 标语 -->
    <text x="540" y="920" font-family="Noto Serif SC, serif" font-size="30" fill="#6B6461" text-anchor="middle" letter-spacing="4">{{TAGLINE_LINE1}}</text>
    <text x="540" y="980" font-family="Noto Serif SC, serif" font-size="30" text-anchor="middle" letter-spacing="4">
      <tspan fill="#C4653A">{{TAGLINE_HIGHLIGHT}}</tspan><tspan fill="#6B6461">{{TAGLINE_REST}}</tspan>
    </text>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4CFC8" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#6B6461" text-anchor="end" letter-spacing="4">0 1</text>
  </g>
</svg>
```

### 封面变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ZODIAC}}` | 星座名 | 射手座 |
| `{{TOPIC}}` | 主题 | 性格独白 |
| `{{ZODIAC_SVG}}` | 星座图标 | `<svg>...</svg>` |
| `{{SUBTITLE}}` | 副标题 | 表面乐观 |
| **主标题（模式A：单行内联高亮）** | | |
| `{{TITLE_BEFORE}}` | 高亮词前的文字 | 双子座 |
| `{{TITLE_HIGHLIGHT}}` | **高亮词**（强调色） | 理想的 |
| `{{TITLE_AFTER}}` | 高亮词后的文字 | 生活 |
| **主标题（模式B：双行标题）** | | |
| `{{TITLE_LINE2}}` | 第二行（整行高亮，可选） | 唯独心寒不行 |
| `{{TAGLINE_LINE1}}` | 标语第一行 | 走得洒脱 |
| `{{TAGLINE_HIGHLIGHT}}` | **标语高亮**（强调色） | 是因为 |
| `{{TAGLINE_REST}}` | 标语剩余 | 早就做好了准备 |

### 主标题智能高亮规则

封面标题支持**双行模式**，第一行智能高亮，第二行整行高亮。

#### ⚠️ 核心原则

1. **高亮标记由 AI 在内容生成阶段添加**，使用 `【词】` 语法
2. **生成脚本只负责解析标记**，不做任何语义判断
3. **高亮要精简**，宁少勿多，突出核心

#### 封面标题高亮规则

**双行标题格式**：
```
第一行：星座名 + 主题词（只高亮1个核心词，星座名不高亮）
第二行：核心形容词/描述词（整行 accent 色，无需标记）
```

**⚠️ 重要：星座名称不需要高亮！**
- 星座名是常见词，高亮没有强调效果
- 应该高亮的是**主题相关的核心动词或名词**

**标题示例**：

| 主题 | 飞书标题字段内容 | 说明 |
|------|-----------------|------|
| 双子座做决定 | `双子座做【决定】\n来不及想` | 只高亮"决定" |
| 双子座选择 | `双子座【选择】\n全凭感觉` | 只高亮"选择" |
| 双子座的内心 | `双子座的【内心】\n充满拉扯` | 只高亮"内心" |
| 双子座的热情 | `双子座的【热情】\n一点就燃` | 只高亮"热情" |
| 双子座的选择 | `双子座的【选择】\n回到直觉` | 只高亮"选择" |

**封面高亮原则**：
1. **第一行只高亮1个核心词**（动词或名词）
2. **星座名不高亮**
3. **第二行整行 accent 色**，无需【】标记

---

### 内容页正文高亮规则

**⚠️ 内容页正文也需要高亮，形成语义呼应！**

**每段正文高亮 2 个呼应词**，形成对比/递进/因果/转折关系：

```
示例段落：
别人还在列清单分析利弊的时候
我已经做完了
不是冲动 是【直觉】比【脑子】快

高亮词："直觉" 和 "脑子" 形成对比呼应
```

**呼应类型**：

| 类型 | 说明 | 示例 |
|------|------|------|
| 对比 | 两个词形成对比 | 【直觉】vs【脑子】、【表面】vs【内心】 |
| 递进 | 层层递进 | 【想】→【做】→【冲】 |
| 因果 | 原因和结果 | 因为【感觉】所以【选择】 |
| 转折 | 前后反差 | 表面【冷】内心【热】 |

**内容页高亮原则**：
1. **每段只高亮2个呼应词**
2. **两个词必须有语义关联**
3. **避免连续高亮**（中间要有普通色间隔）
4. **不是每行都要高亮**，只在关键句中高亮

---

### 生成脚本解析规则

**脚本只解析【】标记，不做语义判断：**

```python
import re

def parse_highlight_marks(text: str) -> list:
    """解析【】标记，返回 [(text, is_highlight), ...] 列表"""
    result = []
    pattern = r'【([^】]+)】'
    last_end = 0
    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            result.append((text[last_end:match.start()], False))
        result.append((match.group(1), True))
        last_end = match.end()
    if last_end < len(text):
        result.append((text[last_end:], False))
    return result
```

**SVG 渲染示例**：

输入：`双子座做【决定】`

输出：
```svg
<text>
  <tspan fill="#3D3835">双子座做</tspan>
  <tspan fill="#C4653A">决定</tspan>
</text>
```

---

## 内页模板

```svg
<!-- [STYLE: 性格独白风] [TYPE: page] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FAF6F1"/>
      <stop offset="50%" stop-color="#F5EDE4"/>
      <stop offset="100%" stop-color="#F0E6D9"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.3"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.03"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 页眉 -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#C4653A" letter-spacing="2">{{ZODIAC}}</text>
    <text x="210" y="130" font-family="Georgia, serif" font-size="24" fill="#D4CFC8">·</text>
    <text x="240" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#6B6461" letter-spacing="3">{{TOPIC}}</text>
    <g transform="translate(924, 74) rotate(-10)">
      {{ZODIAC_SVG}}
    </g>
  </g>

  <!-- 章节标签 -->
  <text x="100" y="220" font-family="Georgia, serif" font-size="26" fill="#C4653A" letter-spacing="8">PART {{PART_NUM}}</text>

  <!-- 章节标题 -->
  <text x="100" y="310" font-family="Noto Serif SC, serif" font-size="64" font-weight="600" fill="#3D3835" letter-spacing="6">{{SECTION_TITLE}}</text>

  <!-- 分隔线 -->
  <rect x="100" y="340" width="100" height="4" fill="#C4653A"/>

  <!-- 正文内容 -->
  <g id="content" transform="translate(100, 480)">
    <!-- 动态生成每行文本，字体36px，字间距4px，行高70px -->
    {{CONTENT_LINES}}
  </g>

  <!-- 引用区块 -->
  <g id="quote" transform="translate(100, 1050)">
    <!-- 左边框 -->
    <line x1="0" y1="0" x2="0" y2="60" stroke="#C4653A" stroke-width="4"/>
    <!-- 引用文字 -->
    <text x="30" y="40" font-family="Noto Serif SC, serif" font-size="28" font-style="italic" fill="#6B6461" letter-spacing="2">"{{QUOTE}}"</text>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4CFC8" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#6B6461" text-anchor="end" letter-spacing="4">{{PAGE_NUM}}</text>
  </g>
</svg>
```

### 正文内容生成规则

**字体规范**：
| 属性 | 值 | 说明 |
|------|-----|------|
| 字体大小 | **36px** | 正文主字号 |
| 字间距 | **4px** | letter-spacing |
| 行间距 | **70px** | y 坐标递增值 |

**每行文本模板**：
```svg
<text y="{{LINE_Y}}" font-family="Noto Serif SC, serif" font-size="36" fill="#3D3835" letter-spacing="4">
  <tspan fill="#3D3835">{{TEXT_BEFORE}}</tspan>
  <tspan fill="#C4653A">{{HIGHLIGHT}}</tspan>
  <tspan fill="#3D3835">{{TEXT_AFTER}}</tspan>
</text>
```

**示例**：
```svg
<text y="0" font-family="Noto Serif SC, serif" font-size="36" fill="#3D3835" letter-spacing="4">射手表面乐观</text>
<text y="70" font-family="Noto Serif SC, serif" font-size="36" letter-spacing="4">
  <tspan fill="#3D3835">其实内心</tspan><tspan fill="#C4653A">敏感</tspan><tspan fill="#3D3835">得要命</tspan>
</text>
<text y="140" font-family="Noto Serif SC, serif" font-size="36" fill="#3D3835" letter-spacing="4">只是不想给别人添麻烦</text>
<text y="210" font-family="Noto Serif SC, serif" font-size="36" letter-spacing="4">
  <tspan fill="#3D3835">习惯了</tspan><tspan fill="#C4653A">自己扛</tspan>
</text>
```

---

## 结尾页模板

> **设计理念**：尾页是套图的收尾，采用**整体居中布局**增强仪式感和总结感，与内容页的左对齐形成差异化。
>
> **重要**：尾页分为**两个内容区域**，需用**装饰分隔线**明确区分：
> 1. **主文案区域** - 陈述性总结（正体字）
> 2. **祝福语区域** - 情感升华收尾（斜体字，与内容页 `.quote` 风格呼应）

### 尾页内容结构

```
┌─────────────────────────────┐
│  [页眉]                      │
│                             │
│         EXTRA               │
│       写给XX座               │
│         ────                │
│                             │
│    [主文案区域 - 正体32px]   │
│    你的XX不是缺点            │
│    是你保护自己的本能         │
│    ...                      │
│                             │
│      ─── ◆ ───              │  ← 装饰分隔线
│                             │
│    [祝福语区域 - 斜体28px]   │
│    愿你永远忠于自己的感觉     │
│    不必讨好任何人            │
│                             │
│      ─── END ───            │
│                             │
│  [页脚]                      │
└─────────────────────────────┘
```

### 两区域样式对比

| 区域 | 字体 | 字号 | 颜色 | 间距 |
|------|------|------|------|------|
| **主文案** | Noto Serif SC（正体） | 32px | #3D3835 主文字 | line-height: 2.0 |
| **祝福语** | Noto Serif SC（斜体） | 28px | #6B6461 次要文字 | line-height: 1.9 |

### 内容区域布局规范

**关键CSS**：使用 Flexbox 垂直居中，确保上下留白均衡

```css
.centered-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  justify-content: center;  /* ⭐ 垂直居中 */
  padding-bottom: 60px;     /* 微调视觉重心 */
}
```

### 装饰分隔线规范

- **上边距**：70px（与主文案的间隔）
- **下边距**：50px（与祝福语的间隔）
- **样式**：`─── ◆ ───`（两侧线条 50px + 中间菱形符号）
- **颜色**：线条 #D4CFC8，符号 #C4653A

```svg
<!-- [STYLE: 性格独白风] [TYPE: end] -->
<svg width="1080" height="1440" viewBox="0 0 1080 1440" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@300;400;500&amp;display=swap');
    </style>
    <linearGradient id="bgGradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FAF6F1"/>
      <stop offset="50%" stop-color="#F5EDE4"/>
      <stop offset="100%" stop-color="#F0E6D9"/>
    </linearGradient>
    <linearGradient id="lightOverlay" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF" stop-opacity="0.3"/>
      <stop offset="20%" stop-color="#FFF" stop-opacity="0"/>
      <stop offset="80%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.03"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1080" height="1440" fill="url(#bgGradient)"/>
  <rect width="1080" height="1440" fill="url(#lightOverlay)"/>

  <!-- 页眉（保持左对齐，与其他页面一致） -->
  <g id="header">
    <text x="100" y="130" font-family="Noto Serif SC, serif" font-size="32" font-weight="500" fill="#C4653A" letter-spacing="2">{{ZODIAC}}</text>
    <text x="210" y="130" font-family="Georgia, serif" font-size="24" fill="#D4CFC8">·</text>
    <text x="240" y="130" font-family="Noto Sans SC, sans-serif" font-size="24" font-weight="300" fill="#6B6461" letter-spacing="3">{{TOPIC}}</text>
    <g transform="translate(924, 74) rotate(-10)">
      {{ZODIAC_SVG}}
    </g>
  </g>

  <!-- ⭐ 居中内容区域（与内容页的左对齐形成差异） -->
  <g id="centered-content" transform="translate(540, 0)">
    <!-- 章节标签 -->
    <text x="0" y="220" font-family="Georgia, serif" font-size="26" fill="#C4653A" letter-spacing="8" text-anchor="middle">EXTRA</text>

    <!-- 章节标题 -->
    <text x="0" y="310" font-family="Noto Serif SC, serif" font-size="64" font-weight="600" fill="#3D3835" letter-spacing="6" text-anchor="middle">{{SECTION_TITLE}}</text>

    <!-- 分隔线（居中） -->
    <rect x="-50" y="340" width="100" height="4" fill="#C4653A"/>

    <!-- ⭐ 主文案区域（正体32px，主文字色） -->
    <g id="summary" transform="translate(0, 520)">
      {{CONTENT_LINES}}
      <!-- 每行使用 text-anchor="middle"，font-size="32"，fill="#3D3835" -->
    </g>

    <!-- ⭐ 装饰分隔线 ─── ◆ ─── -->
    <g id="content-divider" transform="translate(0, 820)">
      <line x1="-70" y1="0" x2="-20" y2="0" stroke="#D4CFC8" stroke-width="1"/>
      <text x="0" y="5" font-size="16" fill="#C4653A" text-anchor="middle">◆</text>
      <line x1="20" y1="0" x2="70" y2="0" stroke="#D4CFC8" stroke-width="1"/>
    </g>

    <!-- ⭐ 祝福语区域（斜体28px，次要文字色） -->
    <g id="ending" transform="translate(0, 920)">
      <text y="0" font-family="Noto Serif SC, serif" font-size="28" font-style="italic" fill="#6B6461" text-anchor="middle" letter-spacing="3">{{ENDING_LINE1}}</text>
      <text y="55" font-family="Noto Serif SC, serif" font-size="28" font-style="italic" fill="#6B6461" text-anchor="middle" letter-spacing="3">{{ENDING_LINE2}}</text>

      <!-- END 标记 -->
      <g transform="translate(0, 130)">
        <line x1="-90" y1="0" x2="-30" y2="0" stroke="#D4CFC8" stroke-width="2"/>
        <text x="0" y="8" font-family="Georgia, serif" font-size="24" fill="#C4653A" text-anchor="middle" letter-spacing="6">END</text>
        <line x1="30" y1="0" x2="90" y2="0" stroke="#D4CFC8" stroke-width="2"/>
      </g>
    </g>
  </g>

  <!-- 页脚 -->
  <g id="footer">
    <line x1="100" y1="1350" x2="980" y2="1350" stroke="#D4CFC8" stroke-width="2"/>
    <text x="980" y="1390" font-family="Georgia, serif" font-size="28" fill="#6B6461" text-anchor="end" letter-spacing="4">{{PAGE_NUM}}</text>
  </g>
</svg>
```

### 结尾页正文居中规则

**主文案每行（32px 正体）**：

```svg
<text y="0" font-family="Noto Serif SC, serif" font-size="32" fill="#3D3835" letter-spacing="2" text-anchor="middle">你不需要对每个人都好</text>
<text y="61" font-family="Noto Serif SC, serif" font-size="32" letter-spacing="2" text-anchor="middle">
  <tspan fill="#3D3835">生理性讨厌</tspan><tspan fill="#C4653A">不是缺点</tspan>
</text>
```

**祝福语每行（28px 斜体）**：

```svg
<text y="0" font-family="Noto Serif SC, serif" font-size="28" font-style="italic" fill="#6B6461" letter-spacing="3" text-anchor="middle">愿你永远忠于自己的感觉</text>
```

### 结尾页 vs 内容页对比

| 元素 | 内容页 | 结尾页 |
|------|--------|--------|
| PART/EXTRA 标签 | 左对齐 x=100 | **居中** text-anchor="middle" |
| 章节标题 | 左对齐 x=100 | **居中** text-anchor="middle" |
| 分隔线 | 左对齐 x=100 | **居中** x=-50 (相对于540) |
| 正文内容 | 左对齐 | **居中** text-anchor="middle" |
| **装饰分隔线** | - | ─── ◆ ─── |
| 祝福语 | `.quote` 左边框 | 居中斜体 |
| END 标记 | - | 居中 |

---

## 星座图标

射手座 SVG（56×56，描边模式）：
```svg
<svg viewBox="0 0 100 100" width="56" height="56" fill="none" stroke="#C4653A" stroke-width="1.5">
  <line x1="20" y1="80" x2="80" y2="20"/>
  <line x1="80" y1="20" x2="55" y2="20"/>
  <line x1="80" y1="20" x2="80" y2="45"/>
  <line x1="25" y1="45" x2="55" y2="75"/>
</svg>
```

其他星座从 `zodiac-symbols.json` 获取。

---

## 高亮词规则

### 封面（必须2个）
- 主标题1个 + 标语1个
- 使用 `fill="#C4653A"`

### 内页（必须2个呼应对）
- 使用 `<tspan fill="#C4653A">` 包裹高亮词
- 两个词形成语义呼应（因果/对比/递进/转折）

### 结尾页（1-2个）
- 与封面形成首尾呼应

---

## 检查清单

### 基础检查
- [ ] 画布尺寸 1080×1440
- [ ] 背景渐变定义正确（bgGradient + lightOverlay）
- [ ] 字体 @import 已添加
- [ ] 页眉结构完整（星座名+分隔符+主题词+图标）
- [ ] 星座图标 rotate(-10deg)
- [ ] 页脚分隔线 + 右对齐页码
- [ ] 页码格式 "0 X"（带空格）

### 高亮检查
- [ ] 封面：2个高亮词
- [ ] 内页：2个高亮词呼应对
- [ ] 结尾页：1-2个高亮词
- [ ] 高亮使用 `fill="#C4653A"`

### 结构检查
- [ ] 内页有引用区块（左边框4px）
- [ ] 结尾页有 END 标记（带左右装饰线）
- [ ] 正文行间距 61px

### 结尾页专项检查
- [ ] 主文案和祝福语之间有**装饰分隔线** `─── ◆ ───`
- [ ] 主文案使用正体 32px，主文字色 #3D3835
- [ ] 祝福语使用斜体 28px，次要文字色 #6B6461
- [ ] 装饰分隔线上边距 70px，下边距 50px
