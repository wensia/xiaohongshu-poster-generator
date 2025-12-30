# 极简暖调 (Minimal Warm) 模板规范

## 画布尺寸

**尺寸**：1080px × 1440px（3:4 比例）

> 注：小红书竖版图片推荐比例为 3:4，宽度1080px时高度为1440px

---

## 设计系统

### 配色规范

| 用途 | 色值 | 说明 |
|------|------|------|
| 重点色 | `#C8725A` | 珊瑚橙/赭红，用于强调 |
| 主标题 | `#2D2D2D` | 深灰黑，主标题文字 |
| 正文 | `#5A5A5A` | 中灰，正文段落 |
| 辅助文字 | `#9A9590` | 浅灰，星座标签/装饰文字 |
| 装饰线 | `#D4A990` | 暖橙色，分隔横线 |
| 图标 | `#9A9590` | 浅灰，底部星座符号 |

### 背景渐变

```css
.poster {
  background: linear-gradient(
    180deg,
    #FAF8F5 0%,
    #F7F3EE 50%,
    #F4EFE8 100%
  );
}
```

**渐变规则：**
- 方向：自上而下（180°）
- 色调：统一米白/象牙色
- 变化幅度：微妙渐变，从亮到略暖

### 纸张纹理

```css
.poster::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.04;
  pointer-events: none;
}
```

---

## 字体规范

```css
font-family: 'Noto Serif SC', 'Source Han Serif SC', serif;
```

| 元素 | 字号 | 字重 | 字距 | 颜色 |
|------|------|------|------|------|
| 星座标签 | 28px | 400 | 16px | `#9A9590` |
| 主标题 | 72px | 600 | 4px | `#2D2D2D` |
| 副标题/强调 | 56px | 500 | 4px | `#C8725A` |
| 正文段落 | 36px | 400 | 2px | `#5A5A5A` |
| 内页标题 | 42px | 500 | 4px | `#C8725A` |

---

## 封面模板

### 布局结构

```
┌─────────────────────────────────┐
│                                 │
│                                 │
│                                 │
│         ✦ 星座名 ✦              │  ← 星座标签（居中）
│         ─────────               │  ← 装饰横线（居中）
│                                 │
│          主标题                 │  ← 主标题（居中）
│          副标题                 │  ← 副标题/强调（居中）
│                                 │
│                                 │
│                                 │
└─────────────────────────────────┘
```

### 元素规格

| 元素 | 样式 | 说明 |
|------|------|------|
| 星座标签 | `✦ 射 手 座 ✦` | 四角星装饰，字符间加空格，字距16px |
| 装饰横线 | 120px宽，1.5px高 | 颜色 `#D4A990`，居中 |
| 主标题 | 72px，深灰 | 核心钩子文案 |
| 副标题 | 56px，重点色 | 强调语/结论 |

### 间距规范

```css
.cover {
  padding: 200px 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
}

.zodiac-label { margin-bottom: 8px; }
.divider { margin: 16px 0 48px 0; }
.main-title { margin-bottom: 16px; }
```

---

## 正文模板

### 布局结构

```
┌─────────────────────────────────┐
│                                 │
│                                 │
│        信号X：标题文字          │  ← 内页标题（居中）
│                                 │
│  正文段落正文段落正文段落正文   │
│  段落正文段落正文段落正文段落   │  ← 正文区（左对齐）
│  正文段落正文段落。             │
│                                 │
│  ┃ "总结句/金句"               │  ← 引用区块（左边框装饰）
│                                 │
│              ↗                  │  ← 星座符号（底部居中）
│                                 │
└─────────────────────────────────┘
```

### 元素规格

| 元素 | 样式 | 说明 |
|------|------|------|
| 内页标题 | 42px，重点色 | 格式：`信号X：主题` |
| 正文段落 | 36px，中灰 | 行高 2.2，首行无缩进 |
| 关键词强调 | 36px，重点色 | 正文中的核心关键词 |
| 总结句/引用 | 30px，中灰 | 带左边框装饰，一句话金句 |
| 底部符号 | 32px，浅灰 | 星座线性图标，居中 |

### 间距规范

```css
.content-page {
  padding: 160px 100px 120px;
}

.page-title {
  text-align: center;
  margin-bottom: 56px;
}

.body-text {
  text-align: justify;
  line-height: 2.2;
}

/* 总结句/引用区块 */
.quote {
  margin-top: 40px;
  padding-left: 20px;
  border-left: 4px solid rgba(200, 114, 90, 0.5);  /* 重点色40%透明度 */
  font-size: 30px;
  color: #5A5A5A;
  line-height: 1.8;
}

.zodiac-icon {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
}
```

---

## 星座符号 SVG

射手座（♐）简化线性图标：

```html
<svg viewBox="0 0 24 24" width="32" height="32">
  <line x1="4" y1="20" x2="20" y2="4" stroke="#9A9590" stroke-width="1.5" stroke-linecap="round"/>
  <polyline points="12,4 20,4 20,12" fill="none" stroke="#9A9590" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

---

## 重点色使用规则

`#C8725A` 仅用于以下元素：

1. **必用** — 副标题/强调文字
2. **必用** — 内页标题
3. **可选** — 装饰横线

**禁止** — 正文段落、星座标签、底部符号

---

## 文案结构模板

### 封面

```
星座标签：✦ [星座名] ✦
装饰线：────
主标题：[钩子文案，5-7字]
副标题：[强调语，5-8字]
```

### 正文页

```
标题：信号[编号]：[主题]
正文：1段，100-150字
      关键词用重点色强调
总结句：一句话金句（带左边框装饰）
      如 "装傻是选择，聪明是本能"
底部：星座符号图标
```

---

## 质量检查清单

- [ ] 画布尺寸为 1080×1440px
- [ ] 背景使用暖调渐变 + 纸张纹理
- [ ] 封面完全居中布局
- [ ] 星座标签带 ✦ 装饰且字符间有空格
- [ ] 重点色仅用于副标题和内页标题
- [ ] 正文行高 ≥ 2.0
- [ ] 底部星座符号居中且颜色为浅灰
- [ ] 整体留白充足，呼吸感强
