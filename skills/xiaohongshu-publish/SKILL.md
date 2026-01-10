---
name: xiaohongshu-publish
description: 发布内容到小红书创作平台。使用 dev-browser Extension Mode 控制已登录的 Chrome 浏览器。
triggers: ["/publish-xhs", "/xiaohongshu", "/发布小红书"]
---

# 小红书发布 Skill

使用 dev-browser Extension Mode 自动发布内容到小红书创作平台。

## 前置条件

### 1. 安装 dev-browser 扩展到 Chrome（一次性）
```bash
# 扩展位置
/tmp/dev-browser-ext
```

在 **用户日常使用的 Chrome**（不是 Chrome for Testing）中：
1. 打开 `chrome://extensions/`
2. 开启"开发者模式"
3. 点击"加载已解压的扩展程序"
4. 选择上述目录

### 2. 登录小红书创作平台（一次性）
在 Chrome 中手动访问并登录：https://creator.xiaohongshu.com

### 3. 每次发布前的准备
```bash
# 启动 Extension Relay Server
cd ~/.claude/skills/dev-browser && npm run start-extension &

# 等待看到以下输出后再执行发布：
# [relay] Extension connected
# [extension:log] Connected to relay server
```

然后点击 Chrome 工具栏的 **dev-browser 扩展图标**，开启 **Active** 开关。

---

## 已知问题与解决方案

### 问题1: ARIA ref 点击失败 - "element is outside of viewport"
**原因**: Extension Mode 下元素定位与视口计算有偏差
**解决**: 使用 `page.evaluate()` 执行 JavaScript 直接操作 DOM

```javascript
// ❌ 不要这样做
const tab = await client.selectSnapshotRef("page", "e105");
await tab.click(); // 会超时

// ✅ 正确做法
await page.evaluate(() => {
  for (const el of document.querySelectorAll('div, span')) {
    if (el.innerText === '上传图文' && el.children.length === 0) {
      el.scrollIntoView({ behavior: 'instant', block: 'center' });
      el.click();
      return;
    }
  }
});
```

### 问题2: CSS 选择器定位失败
**原因**: 页面动态加载，选择器可能不稳定
**解决**: 使用 evaluate 配合多重回退选择器

```javascript
// ❌ 可能失败
await page.locator('div.ql-editor').click();

// ✅ 使用 evaluate 配合回退
await page.evaluate((content) => {
  const editor = document.querySelector('.ql-editor') ||
                 document.querySelector('[contenteditable="true"]') ||
                 document.querySelector('textarea');
  if (editor) {
    editor.innerHTML = content.replace(/\n/g, '<br>');
    editor.dispatchEvent(new Event('input', { bubbles: true }));
  }
}, content);
```

### 问题3: waitForURL 超时但实际已成功
**原因**: Extension Mode 下事件监听可能不完整
**解决**: 不依赖 waitForURL，改用轮询检查

```javascript
// ❌ 可能超时
await page.waitForURL('**/publish/success**', { timeout: 30000 });

// ✅ 轮询检查
for (let i = 0; i < 30; i++) {
  await page.waitForTimeout(1000);
  const url = page.url();
  if (url.includes('publish/success') || url.includes('published=true')) {
    console.log("发布成功!");
    break;
  }
}
```

### 问题4: 输入框内容未生效
**原因**: 直接设置 value 不会触发 Vue/React 事件
**解决**: 必须 dispatchEvent

```javascript
await page.evaluate((title) => {
  const input = document.querySelector('input[placeholder*="标题"]') ||
                document.querySelector('.d-input input');
  if (input) {
    input.value = title;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }
}, title);
```

---

## 完整发布脚本（经过验证）

```bash
cd ~/.claude/skills/dev-browser && npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("xhs-publish");

// ==================== 配置区域 ====================
const title = "射手遇到处女";
const content = `粗线条撞上细节控会怎样？

第一眼
射手觉得处女好认真
处女觉得射手好随性
一个不拘小节
一个精益求精

#射手座 #处女座 #星座 #星座配对 #命定之约`;

const images = [
  "/path/to/01_cover.png",
  "/path/to/02_page.png",
  "/path/to/03_page.png",
  "/path/to/04_page.png",
  "/path/to/05_page.png",
  "/path/to/06_page.png",
  "/path/to/07_end.png"
];
// ==================== 配置结束 ====================

// 步骤1: 导航并检查登录
console.log("1. 导航到发布页...");
await page.goto("https://creator.xiaohongshu.com/publish/publish?source=official");
await waitForPageLoad(page);
await page.waitForTimeout(2000);

if (page.url().includes("login")) {
  console.log("❌ 未登录，请先在 Chrome 中登录 creator.xiaohongshu.com");
  await page.screenshot({ path: "tmp/need_login.png" });
  await client.disconnect();
  process.exit(1);
}
console.log("✅ 已登录");

// 步骤2: 关闭弹窗 + 切换到图文模式（使用 JS 点击）
console.log("2. 切换到图文模式...");
await page.keyboard.press("Escape"); // 关闭可能的弹窗
await page.waitForTimeout(500);

await page.evaluate(() => {
  window.scrollTo(0, 0);
  for (const el of document.querySelectorAll('div, span')) {
    if (el.innerText === '上传图文' && el.children.length === 0) {
      el.scrollIntoView({ behavior: 'instant', block: 'center' });
      el.click();
      return true;
    }
  }
  return false;
});
await page.waitForTimeout(2000);
console.log("✅ 已切换到图文模式");

// 步骤3: 上传图片
console.log("3. 上传图片...");
const fileInput = await page.locator('input[type="file"]').first();
await fileInput.setInputFiles(images);
console.log(`   等待 ${images.length} 张图片上传...`);
await page.waitForTimeout(images.length * 3000 + 5000);
console.log("✅ 图片上传完成");

// 步骤4: 填写标题（使用 JS + dispatchEvent）
console.log("4. 填写标题...");
await page.evaluate((t) => {
  const input = document.querySelector('input[placeholder*="标题"]') ||
                document.querySelector('.d-input input') ||
                document.querySelector('input[maxlength="20"]');
  if (input) {
    input.value = t;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }
}, title);
console.log(`✅ 标题: ${title}`);

// 步骤5: 填写正文（使用 JS + innerHTML）
console.log("5. 填写正文...");
await page.evaluate((c) => {
  const editor = document.querySelector('.ql-editor') ||
                 document.querySelector('[contenteditable="true"]') ||
                 document.querySelector('textarea');
  if (editor) {
    if (editor.tagName === 'TEXTAREA') {
      editor.value = c;
    } else {
      editor.innerHTML = c.replace(/\n/g, '<br>');
    }
    editor.dispatchEvent(new Event('input', { bubbles: true }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
  }
}, content);
console.log("✅ 正文已填写");

await page.waitForTimeout(1000);
await page.screenshot({ path: "tmp/before_publish.png" });

// 步骤6: 点击发布按钮
console.log("6. 发布笔记...");
await page.evaluate(() => {
  for (const btn of document.querySelectorAll('button')) {
    if (btn.textContent.includes('发布') && !btn.textContent.includes('暂存')) {
      btn.click();
      return true;
    }
  }
  return false;
});

// 步骤7: 等待发布完成（轮询检查，不用 waitForURL）
console.log("   等待发布完成...");
let success = false;
for (let i = 0; i < 30; i++) {
  await page.waitForTimeout(1000);
  const url = page.url();
  if (url.includes('publish/success') || url.includes('published=true')) {
    success = true;
    break;
  }
}

if (success) {
  console.log("✅ 发布成功!");
} else {
  console.log("⚠️ 发布状态未确认，请检查页面");
}

await page.screenshot({ path: "tmp/publish_result.png" });
await client.disconnect();
EOF
```

---

## 关键选择器（按可靠性排序）

| 元素 | 推荐方法 | 备用方法 |
|------|---------|---------|
| 图文标签 | `evaluate` 遍历查找 `innerText === '上传图文'` | - |
| 文件输入 | `page.locator('input[type="file"]').first()` | - |
| 标题框 | `evaluate` 查找 `input[placeholder*="标题"]` | `.d-input input` |
| 正文框 | `evaluate` 查找 `.ql-editor` | `[contenteditable="true"]` |
| 发布按钮 | `evaluate` 遍历查找 `textContent.includes('发布')` | - |

---

## 与飞书集成

### 获取待发布记录
```
app_token: Qt6Qbzzy6aWBgassGQhcUU5vngc
table_id: tblyDtUqcfFMaDfO
```

查询条件：`已生成=true AND 已发布=false`

### 更新发布状态
发布成功后调用飞书 API 将 `已发布` 字段设为 `true`。

---

## 错误处理清单

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Extension not connected` | Relay server 未启动或扩展未激活 | 启动 server + 激活扩展 |
| `element is outside of viewport` | ARIA ref 点击问题 | 改用 evaluate |
| `Timeout exceeded` | 等待超时 | 使用轮询代替 waitFor |
| URL 包含 `login` | 未登录或登录过期 | 手动在 Chrome 登录 |
| 图片上传失败 | 文件路径错误或网络问题 | 检查路径、重试 |

---

## 调试技巧

```javascript
// 截图当前状态
await page.screenshot({ path: "tmp/debug.png" });

// 获取 ARIA 快照查看页面结构
const snapshot = await client.getAISnapshot("xhs-publish");
console.log(snapshot);

// 检查当前 URL
console.log("URL:", page.url());

// 打印页面标题
console.log("Title:", await page.title());
```

---

## 参考来源

- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - MCP 实现参考
- [dev-browser](https://github.com/SawyerHood/dev-browser) - 浏览器自动化
