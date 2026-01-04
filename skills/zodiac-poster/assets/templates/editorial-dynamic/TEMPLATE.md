# 动态编辑风 (Editorial Dynamic) 模板规范

**风格**：经典强调
**特征**：色块填充关键词 + 大字号背景装饰 + 圆形装饰
**适用**：年运势、重要预测、情感内容、正式内容

---

## 🚨 核心禁令

### 禁止使用表情符号作为星座图标

| ❌ 绝对禁止 | ✅ 必须使用 |
|------------|------------|
| ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏ ♐ ♑ ♒ ♓ | SVG 线性图标（见文末"星座图标库"） |
| Unicode/Emoji 表情 | `<svg>` + `<line>` / `<path>` 描边 |

### 禁止在内容中使用表情符号

| 禁止类型 | 禁止示例 | 正确做法 |
|----------|----------|----------|
| 星座符号 | ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏ ♐ ♑ ♒ ♓ | 使用纯文字或 SVG |
| 装饰符号 | ✨ ⭐ 🌟 💫 🔥 ❤️ | 不使用或用 CSS 实现 |
| 表情 Emoji | 😊 🥰 😍 | 不使用 |

---

## 装饰元素

### 经典强调专属元素

| 元素 | 说明 |
|------|------|
| `.year-bg` | 大字号背景装饰（如 2026） |
| `.circle-deco` | 圆形装饰 |
| `.number-lead` | 大数字页码背景装饰（可选） |

---

## 画布尺寸与基础设置

**尺寸**：1080px × 1440px（3:4 比例）

### 通用基础样式

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

/* 星座图标 */
.zodiac-icon svg {
  width: 48px;
  height: 48px;
  stroke: #C15F3C;
  stroke-width: 1.5;
  fill: none;
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

/* 底部渐变色带 */
.gradient-band {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #C15F3C 0%, #D4765A 50%, #E8A88C 100%);
}
```

---

## 经典强调风格 CSS

```css
/* === 经典强调风格 === */

/* 关键词：色块填充 */
.keyword {
  display: inline-block;
  width: fit-content;
  height: 75px;  /* 固定高度，确保所有页面色块高度一致 */
  background: linear-gradient(135deg, #C15F3C 0%, #D4765A 100%);
  color: #fff;
  font-size: 36px;
  font-weight: 600;
  letter-spacing: 10px;
  padding: 16px 36px;
  border-radius: 2px;
  margin-bottom: 60px;
  line-height: 1.2;
  white-space: nowrap;  /* 防止换行 */
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
  font-size: 68px;
  font-weight: 600;
  color: #2D2D2D;
  letter-spacing: 4px;
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
  font-size: 32px;
  font-weight: 400;
  color: #4A4A4A;
  line-height: 2.2;
  letter-spacing: 3px;
  text-align: left;
}

.content p {
  margin-bottom: 36px;
}

/* 总结句 */
.summary {
  font-size: 28px;
  font-weight: 400;
  color: #9A958A;
  letter-spacing: 4px;
  font-style: italic;
  margin-top: 50px;
  padding-top: 30px;
  border-top: 1px solid rgba(193, 95, 60, 0.2);
  text-align: center;
}
.summary::before { content: '「 '; }
.summary::after { content: ' 」'; }

/* 重点色 */
.accent {
  color: #C15F3C;
  font-weight: 600;
}

/* 重点色变体：背景高亮 */
.accent-bg {
  color: #fff;
  background: linear-gradient(135deg, #C15F3C 0%, #D4765A 100%);
  padding: 2px 8px;
  border-radius: 2px;
}

/* 重点色变体：下划线 */
.accent-underline {
  color: #C15F3C;
  font-weight: 500;
  border-bottom: 3px solid rgba(193, 95, 60, 0.4);
  padding-bottom: 2px;
}

/* 文字高亮下划线 */
.highlight {
  position: relative;
  display: inline;
}
.highlight::after {
  content: '';
  position: absolute;
  bottom: 4px;
  left: -2px;
  right: -2px;
  height: 12px;
  background: rgba(193, 95, 60, 0.15);
  z-index: -1;
  border-radius: 2px;
}
```

---

## 封面模板

```html
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
  </style>
</head>
<body>
  <div class="poster">
    <!-- 装饰：大字号背景 -->
    <div class="year-bg">2026</div>

    <!-- 装饰：圆形 -->
    <div class="circle-deco" style="top: 200px; right: 100px;">
      <div class="circle-inner"></div>
    </div>

    <div class="header">
      <span class="tag">射手座 · 情感</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main">
      <div class="keyword">射手座的放弃</div>
      <h1 class="main-title">当我的<span class="accent">计划</span><br>被一个个<span class="accent">否认</span></h1>
      <p class="sub-title">直到我的计划里再也<span class="accent">没有你</span></p>
      <p class="quote">「 不是突然放弃，是失望攒够了 」</p>
    </div>

    <div class="footer">
      <span class="footer-text">射手座的告别</span>
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

    /* 内容页布局调整：垂直居中 */
    .main {
      top: 50%;
      transform: translateY(-50%);
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
      <span class="tag">射手座 · 情感</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main">
      <div class="keyword">小标题</div>
      <div class="content">
        <p>正文内容第一段</p>
        <p>正文内容第二段</p>
        <p><span class="accent">情感核心句放在这里</span></p>
      </div>
      <p class="summary">总结金句放在这里</p>
    </div>

    <div class="footer">
      <span class="footer-text">射手座的告别</span>
      <span class="page-num">02</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

**内容页变量说明**：

| 变量 | 说明 | 示例 |
|------|------|------|
| `小标题` | 当页主题关键词 | 体验优先 |
| `.content p` | 正文段落（每段一个p标签） | 多个 `<p>` 元素 |
| `.accent` | **内容页首选**，情感核心（橙色字） | 好，那就不去了 |
| `.accent-underline` | 辅助强调（下划线） | 次要关键词 |
| `.summary` | 总结句（自带引号） | 金句/结论 |

> **注意**：内容页已有 `.keyword` 色块，正文禁止使用 `.accent-bg`（会产生两个色块）

---

## 尾页模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1440">
  <title>End</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* 插入通用基础样式 */
    /* 插入经典强调风格CSS */

    /* 尾页布局调整：居中 */
    .main {
      top: 280px;
      transform: none;
      text-align: center;
    }
    .content {
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="circle-deco" style="top: 180px; right: 80px; width: 120px; height: 120px;">
      <div class="circle-inner" style="width: 60px; height: 60px;"></div>
    </div>

    <div class="header">
      <span class="tag">射手座 · 情感</span>
      <div class="zodiac-icon"><!-- SVG --></div>
    </div>

    <div class="main">
      <div class="keyword">结语</div>
      <div class="content">
        <p>总结内容，使用<span class="accent">强调词</span></p>
        <p>呼应主题的金句</p>
      </div>
      <p class="summary">收尾金句</p>
    </div>

    <div class="footer">
      <span class="footer-text">射手座的告别</span>
      <span class="page-num">06</span>
    </div>

    <div class="gradient-band"></div>
  </div>
</body>
</html>
```

---

## 配色参考

| 用途 | 色值 | 说明 |
|------|------|------|
| 重点色 | `#C15F3C` | 赭红/珊瑚橙 |
| 重点色渐变 | `#C15F3C → #D4765A` | 色块渐变 |
| 主文字 | `#2D2D2D` | 深灰，标题 |
| 次文字 | `#3D3D3D` | 次深灰，副标题 |
| 正文 | `#4A4A4A` | 中灰，段落 |
| 弱化文字 | `#9A958A` | 浅灰，标签/引用 |

---

## 智能标记指南

> 详细规则参见：`/skills/generate-from-feishu/reference/accent-rules.md`

### 封面 vs 内容页

| 页面类型 | 标记目标 | 标记位置 |
|----------|----------|----------|
| **封面** | 核心概念词（2-4字） | 主标题 + 副标题 |
| **内容页** | 情感转折句 | 正文最后一句 |

### 封面标记规则

**标记主标题中的核心动词/名词 + 副标题中的情感结果词**

```html
<!-- 示例：当我的计划被一个个否认 -->
<h1 class="main-title">
  当我的<span class="accent">计划</span><br>
  被一个个<span class="accent">否认</span>
</h1>
<p class="sub-title">
  直到我的计划里再也<span class="accent">没有你</span>
</p>
```

| 优先级 | 标记位置 | 标记内容 |
|--------|----------|----------|
| 1 | 主标题 | 核心动词/名词 |
| 2 | 副标题 | 情感结果词 |

### 内容页标记规则

**标记情感转折点/最终决定**

| 优先级 | 标记目标 | 示例 |
|--------|----------|------|
| 1 | 情感转折点 | "好，那就不去了"、"算了" |
| 2 | 最终决定 | "我选择离开"、"我不要了" |

### 禁止标记

| 类型 | 示例 | 原因 |
|------|------|------|
| 星座名称 | "射手座" | 主体标识 |
| 时间词 | "去年"、"那天" | 背景信息 |
| 语气词 | "的"、"了" | 无实义 |
| 整句标记 | 整个标题 | 失去重点 |

### 样式选择

| 样式 | 适用场景 |
|------|----------|
| `.accent` | **所有页面首选**（文字变色） |
| `.accent-underline` | 辅助强调（下划线） |

### 色块唯一原则

**一张图片只能有一个色块！**

```
❌ 错误：.keyword 色块 + .accent-bg 色块 = 两个色块，视觉重复
✅ 正确：.keyword 色块 + .accent 文字 = 一个色块 + 文字强调
```

| 页面类型 | 有 `.keyword` | 正文强调样式 |
|----------|---------------|--------------|
| 封面 | 有 | 用 `.accent`（文字） |
| 内容页 | 有 | 用 `.accent`（文字） |
| 无关键词页 | 无 | 可用 `.accent-bg`（色块） |

### 标记数量

- 每页 **1-2 处**（最多 3 处）
- 原则：少即是多

---

## 总结句生成指南

### 总结句本质

总结是**情感提炼**，不是内容概括。

```
正文说具体事件 → 总结说情感本质
正文说情感状态 → 总结说哲理升华
```

### 总结类型

| 类型 | 示例 |
|------|------|
| 情感命名 | "第一次妥协"、"最后的温柔" |
| 哲理升华 | "放手也是一种爱" |
| 状态描述 | "心已经凉了" |
| 反问留白 | "又能怎样呢" |

### 生成规则

1. **字数**：3-8字（最多12字）
2. **不重复**：不使用正文原话
3. **角度转换**：叙事→情感，情感→哲理

### 示例对照

| 正文 | 错误总结 | 正确总结 |
|------|----------|----------|
| 好，那就不去了 | "那就不去了" | "第一次妥协" |
| 算了，我累了 | "我累了" | "不是不爱，是真的累了" |
| 但我还是想试试 | "想试试" | "明知不可为" |

---

## 生成检查清单

### 基础检查
- [ ] 星座图标使用 SVG 线性图标（禁止 ♐ 等表情符号）
- [ ] 文字内容不含装饰表情（禁止 ✨ 🔥 等）
- [ ] `.keyword` 色块填充样式正确
- [ ] 装饰元素仅使用 `.year-bg` 和 `.circle-deco`

### 色块统一检查
- [ ] 所有内容页（包含结尾页）使用相同的 `.keyword` 样式
- [ ] `.keyword` 包含 `line-height: 1.2` 确保高度统一

### 智能标记检查
- [ ] **色块唯一**：有 `.keyword` 的页面，正文只用 `.accent`（禁止 `.accent-bg`）
- [ ] 标记的是**情感核心**，不是主题词
- [ ] 标记的是**句子结论**，不是开头背景
- [ ] 每页标记 **1-2 处**（最多 3 处）

### 总结句检查
- [ ] 每个内容页有 `.summary` 总结句
- [ ] 总结是**情感提炼**，不是内容重复
- [ ] 总结字数 **3-12 字**
- [ ] 总结与正文**角度不同**（叙事→情感 / 情感→哲理）

---

## 星座图标库

### 射手座 (Sagittarius)
```html
<svg viewBox="0 0 50 50">
  <line x1="8" y1="42" x2="42" y2="8" stroke-linecap="round"/>
  <polyline points="30,8 42,8 42,20" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="18" y1="32" x2="32" y2="18" stroke-linecap="round"/>
  <line x1="12" y1="28" x2="22" y2="38" stroke-linecap="round"/>
</svg>
```

### 双子座 (Gemini)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <line x1="25" y1="20" x2="75" y2="20" stroke-linecap="round"/>
  <line x1="25" y1="80" x2="75" y2="80" stroke-linecap="round"/>
  <line x1="35" y1="20" x2="35" y2="80" stroke-linecap="round"/>
  <line x1="65" y1="20" x2="65" y2="80" stroke-linecap="round"/>
</svg>
```

### 白羊座 (Aries)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M30,70 C30,35 50,25 50,25 C50,25 70,35 70,70" stroke-linecap="round"/>
  <path d="M20,40 C20,25 35,20 35,35" stroke-linecap="round"/>
  <path d="M80,40 C80,25 65,20 65,35" stroke-linecap="round"/>
</svg>
```

### 金牛座 (Taurus)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="55" r="25"/>
  <path d="M25,40 C25,25 40,20 50,30 C60,20 75,25 75,40" stroke-linecap="round"/>
</svg>
```

### 巨蟹座 (Cancer)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="30" cy="40" r="12"/>
  <circle cx="70" cy="60" r="12"/>
  <path d="M42,40 C60,40 70,30 70,48" stroke-linecap="round"/>
  <path d="M58,60 C40,60 30,70 30,52" stroke-linecap="round"/>
</svg>
```

### 狮子座 (Leo)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="35" cy="35" r="15"/>
  <path d="M35,50 C35,70 50,80 70,80" stroke-linecap="round"/>
  <circle cx="70" cy="80" r="8"/>
</svg>
```

### 处女座 (Virgo)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <line x1="25" y1="20" x2="25" y2="80" stroke-linecap="round"/>
  <line x1="45" y1="20" x2="45" y2="80" stroke-linecap="round"/>
  <line x1="65" y1="20" x2="65" y2="60" stroke-linecap="round"/>
  <path d="M65,60 C65,75 80,80 80,65" stroke-linecap="round"/>
</svg>
```

### 天秤座 (Libra)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <line x1="20" y1="70" x2="80" y2="70" stroke-linecap="round"/>
  <path d="M20,50 C20,30 50,20 50,40 C50,20 80,30 80,50" stroke-linecap="round"/>
</svg>
```

### 天蝎座 (Scorpio)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <line x1="25" y1="20" x2="25" y2="70" stroke-linecap="round"/>
  <line x1="45" y1="20" x2="45" y2="70" stroke-linecap="round"/>
  <path d="M65,20 L65,70 L80,55" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

### 摩羯座 (Capricorn)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M30,30 L30,70 C30,80 50,80 50,70 L50,40" stroke-linecap="round"/>
  <circle cx="65" cy="70" r="12"/>
</svg>
```

### 水瓶座 (Aquarius)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M20,40 Q35,30 50,40 Q65,50 80,40" stroke-linecap="round"/>
  <path d="M20,60 Q35,50 50,60 Q65,70 80,60" stroke-linecap="round"/>
</svg>
```

### 双鱼座 (Pisces)
```html
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M30,20 C15,35 15,65 30,80" stroke-linecap="round"/>
  <path d="M70,20 C85,35 85,65 70,80" stroke-linecap="round"/>
  <line x1="20" y1="50" x2="80" y2="50" stroke-linecap="round"/>
</svg>
```
