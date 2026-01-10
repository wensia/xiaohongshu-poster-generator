---
name: xiaohongshu-publish
description: 发布内容到小红书创作平台。使用 dev-browser Extension Mode 控制已登录的 Chrome 浏览器。
triggers: ["/publish-xhs", "/xiaohongshu", "/发布小红书"]
---

# 小红书发布 Skill

使用 dev-browser Extension Mode 自动发布内容到小红书创作平台。

## 前置条件

### 1. 安装 dev-browser 扩展到 Chrome
```bash
# 扩展位置
/tmp/dev-browser-ext
# 或
~/.dev-browser-extension
```

在 Chrome 中：
1. 打开 `chrome://extensions/`
2. 开启"开发者模式"
3. 点击"加载已解压的扩展程序"
4. 选择上述目录

### 2. 登录小红书创作平台
在 Chrome 中手动访问并登录：https://creator.xiaohongshu.com

### 3. 启动 Extension Relay Server
```bash
cd ~/.claude/skills/dev-browser && npm run start-extension &
```
等待看到 `[relay] Extension connected` 后再执行发布。

### 4. 激活扩展
点击 Chrome 工具栏的 dev-browser 扩展图标，开启 Active 开关。

## 发布工作流

### 步骤1: 检查登录状态

```bash
cd ~/.claude/skills/dev-browser && npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("xhs-publish");

await page.goto("https://creator.xiaohongshu.com/publish/publish?source=official");
await waitForPageLoad(page);
await page.waitForTimeout(2000);

const isLoggedIn = !page.url().includes("login");
console.log("登录状态:", isLoggedIn ? "已登录" : "未登录");

if (!isLoggedIn) {
  console.log("请先在 Chrome 中登录小红书创作平台");
  await page.screenshot({ path: "tmp/need_login.png" });
}

await client.disconnect();
EOF
```

### 步骤2: 切换到图文模式

默认是视频上传页面，需要切换：

```javascript
await page.evaluate(() => {
  for (const el of document.querySelectorAll('div, span')) {
    if (el.innerText === '上传图文' && el.children.length === 0) {
      el.click();
      return true;
    }
  }
  return false;
});
await page.waitForTimeout(1500);
```

### 步骤3: 上传图片

**选择器**: `input[type="file"]`
**上传完成标志**: `.img-preview-area .pr` 元素出现

```javascript
const images = [
  "/path/to/01_cover.png",
  "/path/to/02_page.png",
  // ... 最多 18 张
];

const fileInput = await page.locator('input[type="file"]').first();
await fileInput.setInputFiles(images);

// 等待上传完成
await page.waitForTimeout(images.length * 2000 + 3000);
```

### 步骤4: 填写标题

**选择器**: `div.d-input input`
**限制**: 最多 20 字符

```javascript
const title = "射手遇到巨蟹";
await page.fill('div.d-input input', title);
```

### 步骤5: 填写正文

**选择器**: `div.ql-editor` 或 `[data-placeholder*="正文"]`
**限制**: 最多 1000 字符

```javascript
const content = `文案内容...

#射手座 #巨蟹座 #星座配对`;

const editor = await page.locator('div.ql-editor').first();
await editor.click();
await editor.fill(content);
```

### 步骤6: 发布

**选择器**: `button:has-text("发布")`
**成功标志**: URL 变为 `/publish/success`

```javascript
await page.click('button:has-text("发布")');
await page.waitForURL('**/publish/success**', { timeout: 30000 });
console.log("发布成功!");
```

## 完整发布脚本

```bash
cd ~/.claude/skills/dev-browser && npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("xhs-publish");

// === 配置 ===
const title = "射手遇到巨蟹";
const content = `自由和安全感的拉扯会怎样？

第一眼
射手觉得巨蟹好温柔
巨蟹觉得射手好阳光

#射手座 #巨蟹座 #星座 #星座配对 #命定之约`;

const images = [
  "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09/射手遇到巨蟹/01_cover.png",
  "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09/射手遇到巨蟹/02_page.png",
  "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成/output/2026/01/09/射手遇到巨蟹/03_page.png",
];

// === 导航 ===
await page.goto("https://creator.xiaohongshu.com/publish/publish?source=official");
await waitForPageLoad(page);
await page.waitForTimeout(2000);

if (page.url().includes("login")) {
  console.log("未登录，请先在 Chrome 中登录");
  await client.disconnect();
  process.exit(1);
}

// === 切换到图文模式 ===
await page.evaluate(() => {
  for (const el of document.querySelectorAll('div, span')) {
    if (el.innerText === '上传图文' && el.children.length === 0) {
      el.click();
      return;
    }
  }
});
await page.waitForTimeout(1500);

// === 上传图片 ===
const fileInput = await page.locator('input[type="file"]').first();
await fileInput.setInputFiles(images);
console.log(`上传 ${images.length} 张图片...`);
await page.waitForTimeout(images.length * 2000 + 3000);

// === 填写标题 ===
await page.fill('div.d-input input', title);
console.log("标题已填写:", title);

// === 填写正文 ===
const editor = await page.locator('div.ql-editor').first();
await editor.click();
await editor.fill(content);
console.log("正文已填写");

// === 发布 ===
await page.click('button:has-text("发布")');
await page.waitForURL('**/publish/success**', { timeout: 30000 });
console.log("发布成功!");

await page.screenshot({ path: "tmp/publish_success.png" });
await client.disconnect();
EOF
```

## 关键选择器

| 元素 | 选择器 | 说明 |
|------|--------|------|
| 图文标签 | `div:has-text("上传图文")` | 切换模式 |
| 文件输入 | `input[type="file"]` | 隐藏上传框 |
| 图片预览 | `.img-preview-area .pr` | 上传完成标志 |
| 标题框 | `div.d-input input` | 最多20字 |
| 正文框 | `div.ql-editor` | Quill编辑器 |
| 话题容器 | `#creator-editor-topic-container` | 话题选择 |
| 发布按钮 | `button:has-text("发布")` | 提交 |

## 与飞书集成

### 获取待发布记录

```
app_token: Qt6Qbzzy6aWBgassGQhcUU5vngc
table_id: tblyDtUqcfFMaDfO
```

查询条件：`已生成=true AND 已发布=false`

### 更新发布状态

发布成功后将 `已发布` 字段设为 `true`。

## 错误处理

| 场景 | 处理 |
|------|------|
| 未登录 | 截图提示，等待用户登录 |
| 上传超时 | 检查网络，重试 |
| 标题超限 | 自动截断到20字 |
| 正文超限 | 自动截断到1000字 |
| 发布失败 | 检查错误提示，保存草稿 |

## 参考来源

- [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) - MCP 实现参考
- [dev-browser](https://github.com/SawyerHood/dev-browser) - 浏览器自动化
