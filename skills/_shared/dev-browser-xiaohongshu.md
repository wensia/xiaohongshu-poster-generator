# Dev-Browser 操作小红书指南

使用 dev-browser Extension Mode 自动化操作小红书网页版的完整指南。

---

## 前置条件

### 1. 启动 Extension Relay Server
```bash
cd ~/.claude/skills/dev-browser && npm run start-extension &
```

等待输出：
```
[relay] Waiting for extension to connect...
[relay] Extension connected
```

### 2. 激活 Chrome 扩展
在 Chrome 工具栏点击 dev-browser 扩展图标，开启 **Active** 开关。

### 3. 登录小红书
在 Chrome 中手动登录 https://www.xiaohongshu.com 或 https://creator.xiaohongshu.com

---

## 已知问题与解决方案

### 问题1: 笔记链接 404 重定向

**现象**: 直接访问 `https://www.xiaohongshu.com/explore/{note_id}` 被重定向到 404 页面

**原因**: 小红书安全机制要求有效的 `xsec_token`

**解决方案**: 使用带完整参数的分享链接

```javascript
// ❌ 直接访问会 404
await page.goto("https://www.xiaohongshu.com/explore/696250f2000000002103e739");

// ✅ 使用带 xsec_token 的分享链接
const url = "https://www.xiaohongshu.com/explore/696250f2000000002103e739" +
  "?xsec_token=CBuDMvtZvFSyfFQ3OMAOCg9Guxu6fuW1EttfAmo-I8vxk=" +
  "&xsec_source=app_share&type=normal";
await page.goto(url);
```

**获取分享链接**:
1. 在小红书 APP 中打开笔记
2. 点击分享 → 复制链接
3. 链接包含有效的 xsec_token

---

### 问题2: page.content() 返回空内容

**现象**: Extension Mode 下 `page.content()` 返回的 HTML 长度只有 39 字节

```javascript
const html = await page.content();
console.log(html.length); // 39 - 几乎为空！
```

**原因**: Extension Mode 通过 CDP 连接浏览器，某些 Playwright API 有限制

**解决方案**: 使用 `getAISnapshot()` 获取 ARIA 快照

```javascript
// ❌ Extension Mode 下无法获取完整 HTML
const html = await page.content();

// ✅ 使用 ARIA 快照
const snapshot = await client.getAISnapshot("page-name");
console.log(snapshot); // 包含完整的页面元素树
```

---

### 问题3: page.evaluate() 访问 DOM 受限

**现象**: `page.evaluate()` 内的 DOM 查询返回空结果

```javascript
const result = await page.evaluate(() => {
  return document.body.innerText; // 返回空字符串
});
```

**原因**: Extension Mode 下 CDP 的 DOM 访问可能受限

**解决方案**:
1. **方案一**: 从 ARIA 快照解析数据
2. **方案二**: 使用 `selectSnapshotRef()` 操作具体元素

```javascript
// 方案一：解析 ARIA 快照
const snapshot = await client.getAISnapshot("xhs-comments");
// 快照是 YAML 格式，包含所有可见元素

// 方案二：使用 ref 操作元素
const element = await client.selectSnapshotRef("xhs-comments", "e604");
await element.click();
```

---

### 问题4: 创作平台笔记点击进入编辑页

**现象**: 在 creator.xiaohongshu.com 点击笔记，进入编辑页面而非详情页

**解决方案**: 直接通过 explore 链接访问笔记详情

```javascript
// ❌ 从创作平台点击会进入编辑模式
await page.goto("https://creator.xiaohongshu.com/new/note-manager");
// 点击笔记 → 进入 /publish/update 编辑页

// ✅ 直接访问 explore 页面
await page.goto("https://www.xiaohongshu.com/explore/{note_id}?xsec_token=...");
```

---

## 完整操作示例

### 拉取笔记评论

```typescript
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
const page = await client.page("xhs-comments");

// 1. 导航到笔记页面（使用带 token 的分享链接）
const noteUrl = "https://www.xiaohongshu.com/explore/696250f2000000002103e739" +
  "?xsec_token=CBuDMvtZvFSyfFQ3OMAOCg9Guxu6fuW1EttfAmo-I8vxk=" +
  "&xsec_source=app_share";

await page.goto(noteUrl);
await waitForPageLoad(page);
await page.waitForTimeout(3000);

// 2. 验证页面加载成功
console.log("页面标题:", await page.title());
// 应输出: "射手遇到处女 - 小红书"

// 3. 获取 ARIA 快照（包含评论数据）
const snapshot = await client.getAISnapshot("xhs-comments");

// 4. 从快照解析评论
// 快照中评论结构示例:
// - link "用户名" [ref=e604] [cursor=pointer]:
//   - /url: /user/profile/xxx?...pc_comment
// - generic [ref=e610]:
//   - text: 评论内容
// - generic [ref=e612]:
//   - generic [ref=e613]: 32分钟前上海

// 5. 解析评论并输出表格
const comments = parseCommentsFromSnapshot(snapshot);
printCommentsTable(comments);

// 6. 截图备份
await page.screenshot({ path: "tmp/comments.png" });

await client.disconnect();

// === 辅助函数 ===
function parseCommentsFromSnapshot(snapshot) {
  // 从 ARIA 快照解析评论数据
  // 返回 [{userName, content, time, location, likes}, ...]
}

function printCommentsTable(comments, noteTitle) {
  console.log("\n=== 笔记评论列表 ===\n");
  console.log(`笔记标题: ${noteTitle}`);
  console.log(`总评论数: ${comments.length} 条\n`);

  // 使用 console.table 在终端显示表格
  console.table(comments.map((c, i) => ({
    '#': i + 1,
    '用户': c.userName,
    '评论内容': c.content.length > 25 ? c.content.slice(0, 25) + '...' : c.content,
    '时间': c.time,
    '地点': c.location,
    '点赞': c.likes || 0
  })));
}
```

### 输出格式示例

拉取评论后，使用 `console.table()` 在终端以表格格式展示：

```
=== 笔记评论列表 ===

笔记标题: 射手遇到处女
总评论数: 6 条

┌─────────┬─────┬────────────────────┬─────────────────────────────┬───────────┬────────┬────────┐
│ (index) │  #  │        用户        │          评论内容           │   时间    │  地点  │  点赞  │
├─────────┼─────┼────────────────────┼─────────────────────────────┼───────────┼────────┼────────┤
│    0    │  1  │       '九峰'       │ '认识20多年了，结婚15年了...'│ '32分钟前' │ '上海' │   0    │
│    1    │  2  │    '云天_LYJ'      │ '射手座➕上升处女座，唉！'    │ '33分钟前' │ '上海' │   0    │
│    2    │  3  │    '红茶可可屋'    │ '射手，从来就是无敌...'      │ '1小时前'  │ '湖北' │   1    │
│    3    │  4  │    'TonyStank'     │ '被处女较真折磨死...'        │ '1小时前'  │ '辽宁' │   0    │
│    4    │  5  │ '不会弹琴的喵桑'   │ '回复 @yuuu_🌷'              │ '35分钟前' │ '陕西' │   0    │
│    5    │  6  │ '是小吉不是大吉'   │ '回复 @吉速小羊'             │ '32分钟前' │ '福建' │   0    │
└─────────┴─────┴────────────────────┴─────────────────────────────┴───────────┴────────┴────────┘
```

---

### ARIA 快照中的评论结构

```yaml
- generic [ref=e597]:           # 评论区容器
  - link [ref=e599]:            # 用户头像链接
    - /url: /user/profile/xxx?...pc_comment
    - img [ref=e600]
  - generic [ref=e601]:         # 评论内容区
    - generic [ref=e602]:       # 用户名行
      - link "九峰" [ref=e604]  # 用户名
      - img [ref=e607]          # 认证图标
    - generic [ref=e610]:       # 评论文本
      - text: 认识20多年了...
    - generic [ref=e612]:       # 时间地点
      - generic [ref=e613]: 32分钟前上海
      - generic [ref=e614]:     # 操作按钮
        - generic: 赞
        - generic: 回复
```

---

## Extension Mode vs Standalone Mode 对比

| 特性 | Extension Mode | Standalone Mode |
|------|---------------|-----------------|
| 登录状态 | ✅ 使用用户已登录的 Chrome | ❌ 需要重新登录 |
| page.content() | ❌ 返回空/不完整 | ✅ 正常工作 |
| page.evaluate() | ⚠️ 部分受限 | ✅ 正常工作 |
| getAISnapshot() | ✅ 正常工作 | ✅ 正常工作 |
| selectSnapshotRef() | ✅ 正常工作 | ✅ 正常工作 |
| 小红书安全验证 | ✅ 复用 cookies | ❌ 可能触发验证 |

**推荐**: 操作小红书使用 Extension Mode，可以复用登录状态和绕过安全验证。

---

## 数据提取策略

由于 Extension Mode 的 DOM 访问限制，推荐以下策略：

### 策略一：ARIA 快照解析（推荐）

```typescript
const snapshot = await client.getAISnapshot("page-name");
// 解析 YAML 格式的快照字符串
// 提取用户名、评论内容、时间等信息
```

### 策略二：网络请求拦截

```typescript
// 拦截小红书 API 请求
page.on('response', async response => {
  if (response.url().includes('/api/')) {
    const data = await response.json();
    // 解析 API 响应数据
  }
});
```

### 策略三：结合 MCP 工具

对于更复杂的数据获取，可以使用 `xiaohongshu-mcp` 的 API：

```
mcp__xiaohongshu-mcp__get_feed_detail(feed_id, xsec_token, load_all_comments=true)
```

---

## 调试技巧

```typescript
// 1. 截图查看当前状态
await page.screenshot({ path: "tmp/debug.png" });

// 2. 获取 ARIA 快照
const snapshot = await client.getAISnapshot("page-name");
console.log(snapshot);

// 3. 检查 URL
console.log("URL:", page.url());

// 4. 检查标题
console.log("Title:", await page.title());

// 5. 列出所有打开的页面
const pages = await client.list();
console.log("Pages:", pages);
```

---

## 相关 Skills

- `xiaohongshu-publish/SKILL.md` - 发布笔记
- `reply-comments/SKILL.md` - 回复评论
- `_shared/xiaohongshu-login.md` - MCP 登录管理
