# 杂志分栏风 (Magazine Part) 模板规范

**特征**：PART 章节编号 + 右侧橙色竖线 + 关键词标签组 + 底部引用
**适用**：职业方向、知识科普、专题系列内容

---

## 核心配色（必须遵守）

| 用途 | 色值 | 说明 |
|------|------|------|
| **强调色** | `#C15F3C` | 图标、关键词、竖线装饰 |
| **弱化色** | `#B1ADA1` / `#9A958A` | 标签、页码、辅助文字 |
| **深色文字** | `#3D3D3D` | 主标题、正文 |
| **次要文字** | `#5A5A5A` | 副标题、正文 |
| **背景色** | `#FAF6F1` | 纯色背景（无渐变） |

---

## 🚨 核心禁令

### 禁止使用的元素

| 禁止 | 原因 |
|------|------|
| 背景渐变 | 此风格使用纯色背景 |
| 噪点纹理 | 保持干净简洁 |
| 双线边框 | 不属于此风格 |
| 星星装饰 | 不属于此风格 |
| 表情符号 | 任何内容禁止表情 |

---

## 风格特征

### 右侧橙色竖线装饰（必须）
```css
.side-line {
  position: absolute;
  top: 200px;
  right: 60px;
  width: 3px;
  height: 120px;
  background: linear-gradient(180deg, #C15F3C 0%, rgba(193, 95, 60, 0.3) 100%);
}
```

### 章节编号样式（内容页必须）
```css
.part-number {
  font-size: 18px;
  font-weight: 400;
  color: #C15F3C;
  letter-spacing: 4px;
  margin-bottom: 20px;
}
```

### 关键词标签组（封面用）
```css
.keyword-tags {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 30px 0;
}
.keyword-tag {
  font-size: 22px;
  color: #5A5A5A;
  letter-spacing: 4px;
  padding: 8px 20px;
  border: 1px solid rgba(193, 95, 60, 0.3);
  border-radius: 4px;
}
```

### 橙色主题标签（封面用）
```css
.theme-tag {
  display: inline-block;
  font-size: 20px;
  font-weight: 500;
  color: #fff;
  background: #C15F3C;
  padding: 8px 20px;
  letter-spacing: 4px;
  margin-bottom: 30px;
}
```

### 底部引用（所有页面）
```css
.bottom-quote {
  position: absolute;
  bottom: 140px;
  left: 80px;
  right: 80px;
  text-align: center;
  font-size: 20px;
  color: #9A958A;
  letter-spacing: 2px;
}
```

---

## 封面模板

```html
<!-- [STYLE: 杂志分栏风] [TYPE: cover] -->
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
      background: #FAF6F1;
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .header {
      position: absolute;
      top: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .tag { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .zodiac-icon svg { width: 44px; height: 44px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }
    .side-line {
      position: absolute;
      top: 200px;
      right: 60px;
      width: 3px;
      height: 120px;
      background: linear-gradient(180deg, #C15F3C 0%, rgba(193, 95, 60, 0.3) 100%);
    }
    .main {
      position: absolute;
      top: 200px;
      left: 80px;
      right: 120px;
      z-index: 10;
    }
    .theme-tag {
      display: inline-block;
      font-size: 20px;
      font-weight: 500;
      color: #fff;
      background: #C15F3C;
      padding: 8px 20px;
      letter-spacing: 4px;
      margin-bottom: 30px;
    }
    .main-title {
      font-size: 72px;
      font-weight: 600;
      color: #3D3D3D;
      letter-spacing: 4px;
      line-height: 1.4;
      margin-bottom: 50px;
    }
    .accent { color: #C15F3C; }
    .keyword-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      margin-bottom: 60px;
    }
    .keyword-tag {
      font-size: 22px;
      color: #5A5A5A;
      letter-spacing: 4px;
      padding: 10px 24px;
      border: 1px solid rgba(193, 95, 60, 0.3);
      border-radius: 4px;
    }
    .sub-title {
      font-size: 28px;
      font-weight: 400;
      color: #5A5A5A;
      letter-spacing: 2px;
      line-height: 1.8;
    }
    .bottom-quote {
      position: absolute;
      bottom: 140px;
      left: 80px;
      right: 80px;
      text-align: left;
      font-size: 18px;
      color: #9A958A;
      letter-spacing: 2px;
    }
    .footer {
      position: absolute;
      bottom: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      z-index: 10;
    }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 2px; }
  </style>
</head>
<body>
  <div class="poster">
    <div class="side-line"></div>
    <div class="header">
      <span class="tag">射手座 · 职业指南</span>
      <div class="zodiac-icon">
        <svg viewBox="0 0 50 50">
          <line x1="8" y1="42" x2="42" y2="8" stroke-linecap="round"/>
          <polyline points="30,8 42,8 42,20" stroke-linecap="round" stroke-linejoin="round"/>
          <line x1="18" y1="32" x2="32" y2="18" stroke-linecap="round"/>
          <line x1="12" y1="28" x2="22" y2="38" stroke-linecap="round"/>
        </svg>
      </div>
    </div>
    <div class="main">
      <div class="theme-tag">职业规划</div>
      <h1 class="main-title">射手座<br/>更适合的<span class="accent">职业方向</span></h1>
      <div class="keyword-tags">
        <span class="keyword-tag">空间</span>
        <span class="keyword-tag">变化</span>
        <span class="keyword-tag">自主</span>
        <span class="keyword-tag">探索</span>
      </div>
      <p class="sub-title">选择让自己更像自己的工作<br/>方向对了，成果自然会来</p>
    </div>
    <div class="bottom-quote">「 对的方向，比努力更重要 」</div>
    <div class="footer">
      <span class="page-num">01</span>
    </div>
  </div>
</body>
</html>
```

---

## 内容页模板

```html
<!-- [STYLE: 杂志分栏风] [TYPE: page] -->
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
      background: #FAF6F1;
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .header {
      position: absolute;
      top: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .tag { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .zodiac-icon svg { width: 44px; height: 44px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }
    .side-line {
      position: absolute;
      top: 200px;
      right: 60px;
      width: 3px;
      height: 120px;
      background: linear-gradient(180deg, #C15F3C 0%, rgba(193, 95, 60, 0.3) 100%);
    }
    .main {
      position: absolute;
      top: 180px;
      left: 80px;
      right: 120px;
      z-index: 10;
    }
    .part-number {
      font-size: 18px;
      font-weight: 400;
      color: #C15F3C;
      letter-spacing: 4px;
      margin-bottom: 20px;
    }
    .section-title {
      font-size: 56px;
      font-weight: 600;
      color: #3D3D3D;
      letter-spacing: 4px;
      margin-bottom: 80px;
    }
    .content {
      font-size: 32px;
      font-weight: 400;
      color: #3D3D3D;
      letter-spacing: 2px;
      line-height: 2.2;
    }
    .content p {
      margin-bottom: 40px;
    }
    .accent { color: #C15F3C; }
    .bottom-quote {
      position: absolute;
      bottom: 140px;
      left: 80px;
      right: 80px;
      text-align: left;
      font-size: 18px;
      color: #9A958A;
      letter-spacing: 2px;
    }
    .footer {
      position: absolute;
      bottom: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      z-index: 10;
    }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 2px; }
  </style>
</head>
<body>
  <div class="poster">
    <div class="side-line"></div>
    <div class="header">
      <span class="tag">射手座 · 职业指南</span>
      <div class="zodiac-icon">
        <svg viewBox="0 0 50 50">
          <line x1="8" y1="42" x2="42" y2="8" stroke-linecap="round"/>
          <polyline points="30,8 42,8 42,20" stroke-linecap="round" stroke-linejoin="round"/>
          <line x1="18" y1="32" x2="32" y2="18" stroke-linecap="round"/>
          <line x1="12" y1="28" x2="22" y2="38" stroke-linecap="round"/>
        </svg>
      </div>
    </div>
    <div class="main">
      <div class="part-number">PART 01</div>
      <h2 class="section-title">空间与变化</h2>
      <div class="content">
        <p>射手对工作的核心诉求是<span class="accent">空间与变化</span></p>
        <p>需要能探索、能移动、能<span class="accent">自主决策</span>的舞台<br/>才能持续保持热情</p>
      </div>
    </div>
    <div class="bottom-quote">「 不自由，毋宁死 」</div>
    <div class="footer">
      <span class="page-num">02</span>
    </div>
  </div>
</body>
</html>
```

---

## 尾页模板

```html
<!-- [STYLE: 杂志分栏风] [TYPE: end] -->
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
      background: #FAF6F1;
      font-family: 'Noto Serif SC', serif;
      overflow: hidden;
    }
    .header {
      position: absolute;
      top: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .tag { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 4px; }
    .zodiac-icon svg { width: 44px; height: 44px; stroke: #C15F3C; stroke-width: 1.5; fill: none; }
    .side-line {
      position: absolute;
      top: 200px;
      right: 60px;
      width: 3px;
      height: 120px;
      background: linear-gradient(180deg, #C15F3C 0%, rgba(193, 95, 60, 0.3) 100%);
    }
    .main {
      position: absolute;
      top: 180px;
      left: 80px;
      right: 120px;
      z-index: 10;
    }
    .part-number {
      font-size: 18px;
      font-weight: 400;
      color: #C15F3C;
      letter-spacing: 4px;
      margin-bottom: 20px;
    }
    .section-title {
      font-size: 56px;
      font-weight: 600;
      color: #3D3D3D;
      letter-spacing: 4px;
      margin-bottom: 80px;
    }
    .content {
      font-size: 32px;
      font-weight: 400;
      color: #3D3D3D;
      letter-spacing: 2px;
      line-height: 2.2;
      text-align: center;
    }
    .accent { color: #C15F3C; }
    .bottom-quote {
      position: absolute;
      bottom: 140px;
      left: 80px;
      right: 80px;
      text-align: center;
      font-size: 18px;
      color: #9A958A;
      letter-spacing: 2px;
    }
    .footer {
      position: absolute;
      bottom: 60px;
      left: 70px;
      right: 70px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      z-index: 10;
    }
    .page-num { font-size: 20px; font-weight: 400; color: #9A958A; letter-spacing: 2px; }
  </style>
</head>
<body>
  <div class="poster">
    <div class="side-line"></div>
    <div class="header">
      <span class="tag">射手座 · 职业指南</span>
      <div class="zodiac-icon">
        <svg viewBox="0 0 50 50">
          <line x1="8" y1="42" x2="42" y2="8" stroke-linecap="round"/>
          <polyline points="30,8 42,8 42,20" stroke-linecap="round" stroke-linejoin="round"/>
          <line x1="18" y1="32" x2="32" y2="18" stroke-linecap="round"/>
          <line x1="12" y1="28" x2="22" y2="38" stroke-linecap="round"/>
        </svg>
      </div>
    </div>
    <div class="main">
      <div class="part-number">PART 05</div>
      <h2 class="section-title">做自己</h2>
      <div class="content">
        <p>与其追求体面</p>
        <p>不如选择让自己<span class="accent">更像自己</span>的工作</p>
        <p>方向对了<br/>成果自然会来</p>
      </div>
    </div>
    <div class="bottom-quote">「 对的方向，比努力更重要 」</div>
    <div class="footer">
      <span class="page-num">06</span>
    </div>
  </div>
</body>
</html>
```

---

## 生成规则

### 1. 行尾排版规则（必须遵守）

**禁止标点符号作为每行的结尾**

| 错误 | 正确 |
|------|------|
| `射手对工作的核心诉求是，` | `射手对工作的核心诉求是` |
| `空间与变化。` | `空间与变化` |

### 2. 内容页 PART 编号规则

- 封面页：无 PART 编号
- 内容页：从 `PART 01` 开始递增
- 尾页：使用最后一个 PART 编号

### 3. 页码规则

- 封面：`01`
- 内容页：从 `02` 开始递增
- 页码位置：右下角

### 4. 关键词标签使用

- 仅封面使用 `.keyword-tags`
- 标签数量：3-5 个
- 内容：与主题相关的关键概念

### 5. 底部引用规则

- 每页必须有底部引用
- 格式：`「 引用内容 」`
- 内容：与当页内容相关的金句

---

## 检查清单

生成后检查：

- [ ] 背景是否为纯色 `#FAF6F1`（无渐变、无噪点）
- [ ] 右侧橙色竖线是否存在
- [ ] 内容页是否有 `PART 0X` 编号
- [ ] 行尾是否有标点符号（不应有）
- [ ] 底部引用是否存在
- [ ] 页码是否正确递增
- [ ] 关键词是否使用 `.accent` 类高亮
