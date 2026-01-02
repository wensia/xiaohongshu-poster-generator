---
name: publishing-to-xiaohongshu
description: Publishes content from Feishu Bitable records to Xiaohongshu (Little Red Book) with auto-generated copywriting. Use when the user wants to publish posters to Xiaohongshu, generate platform-specific captions (100-200 chars), batch publish records with generated images, or check Xiaohongshu login status.
---

# 小红书自动发布器

从飞书多维表格拉取指定记录，自动生成文案并发布到小红书。

---

## 执行前检查（必须）

**⚠️ 重要：在执行任何 MCP 操作前，Claude 必须先运行检查脚本。如果检查失败，立即中断并提示用户。**

### 步骤 1: 运行 MCP 状态检查

```bash
cd /Users/panyuhang/我的项目/编程/脚本/小红书封面生成
# 检查小红书 MCP（自动启动服务）
python3 skills/mcp_checker.py --check xiaohongshu --auto-start

# 如果需要从飞书获取数据，同时检查飞书 MCP
python3 skills/mcp_checker.py --check all --auto-start
```

### 步骤 2: 根据返回结果决定是否继续

**如果检查通过（退出码 0）：** 继续执行后续流程

**如果检查失败（退出码 1）：**
1. **立即中断**，不执行任何 MCP 调用
2. 将错误信息和修复步骤展示给用户
3. 等待用户完成修复后再重试

### 检查失败的常见情况及解决方案

**情况 A: 小红书 MCP 服务未运行**

```bash
cd /Users/panyuhang/我的项目/编程/脚本/小红书封面生成/xiaohongshu-mcp
./xiaohongshu-mcp-darwin-arm64 -headless=true &
```

**情况 B: 小红书未登录**

```bash
cd /Users/panyuhang/我的项目/编程/脚本/小红书封面生成/xiaohongshu-mcp
./xiaohongshu-login-darwin-arm64
```

或使用自动登录（会启动登录窗口）：

```bash
python3 skills/mcp_checker.py --check xiaohongshu --auto-login
```

**情况 C: 飞书 MCP 未就绪**

参考 `generate-from-feishu` skill 的配置说明。

---

## 核心功能

### 功能 1: 发布指定记录到小红书

**用户说：** "发布标题为xxx的记录到小红书"

**执行流程：**

1. 从飞书表格查询指定记录
2. 获取记录的图片路径
3. 根据记录内容生成小红书文案
4. 调用发布接口

```
调用 mcp__lark-mcp__bitable_v1_app_table_record_list
参数:
- app_token: <LARK_BITABLE_APP_TOKEN>
- table_id: <LARK_BITABLE_TABLE_ID>
- filter: "CurrentValue.[标题] = \"<用户指定的标题>\""
```

### 功能 2: 发布图文到小红书

**文案来源优先级：**

1. **优先使用**：飞书表格中"小红书发送文案"字段的内容
2. **备选方案**：如果该字段为空，则由 AI 根据模板生成文案

```
# 判断逻辑
if 记录["小红书发送文案"] 不为空:
    content = 记录["小红书发送文案"]
else:
    content = AI根据模板生成(星座, 标题, 副标题, 正文内容)
```

```
调用 mcp__xiaohongshu__publish_content
参数:
- title: <标题，不超过20字>
- content: <正文，不超过1000字>
- images: [<图片路径数组，支持本地绝对路径或HTTP链接>]
- tags: [<根据文案自动生成的话题标签数组>]
```

---

## ⚠️ 自动生成话题标签（必须）

**每次发布时，必须根据文案内容自动生成合适的话题标签（tags）。**

### 标签生成规则

1. **必选标签**（根据内容类型）：
   - 星座类内容：`星座`、`{具体星座名}`（如"射手座"、"天蝎座"）
   - 情感类内容：`情感`、`恋爱`
   - 性格类内容：`星座性格`、`MBTI`

2. **推荐标签**（提升曝光）：
   - `12星座`
   - `星座运势`
   - `星座配对`
   - `星座分析`

3. **内容相关标签**（根据主题）：
   | 主题类型 | 推荐标签 |
   |----------|----------|
   | 配对/恋爱 | `星座配对`、`恋爱`、`情感` |
   | 性格/特点 | `星座性格`、`性格分析` |
   | 黑化/反差 | `星座黑化`、`反差萌` |
   | 放弃/分手 | `分手`、`情感` |
   | 暧昧/追求 | `暧昧`、`恋爱技巧` |

### 标签数量

- **推荐 3-5 个标签**
- 不要超过 8 个
- 第一个标签应为最核心的（如具体星座名）

### 示例

```
文案主题: 射手座配对指南
自动生成标签: ["射手座", "星座配对", "星座", "情感", "12星座"]

文案主题: 黑化后的射手有多恐怖
自动生成标签: ["射手座", "星座黑化", "星座", "星座性格", "反差"]

文案主题: 放弃型射手
自动生成标签: ["射手座", "星座", "情感", "分手", "12星座"]
```

---

## 文案生成规则（重要）

### 标题规则（不超过20字）

从原标题提炼，保持吸引力：

```
原标题: "别追了"
小红书标题: "射手座：别追了，真的追不上"

原标题: "选择困难"
小红书标题: "天秤座的选择困难症有多严重"
```

### 正文规则（100-200字）

**核心要求：**
1. 段落清晰，2-4段为宜
2. 语言简洁干净，不堆砌形容词
3. 保留人味，避免AI腔调
4. 适当使用口语化表达

**防AI检测技巧：**
- 加入个人视角："我发现..." / "说实话..."
- 使用不完美表达："emmm" / "有点" / "好像"
- 适当省略主语
- 用短句，避免长复合句
- 加入情绪词："笑死" / "真的会" / "太真实"

### 文案模板

**星座性格类：**
```
{星座}就是这样的存在

说实话，{核心特点}这件事，{星座}真的太典了

{展开描述1，1-2句}

{展开描述2，口语化}

所以别怪我们{行为}，这就是{星座}的日常啊
```

**星座情感类：**
```
关于{星座}的{主题}

emmm怎么说呢，{星座}在这方面确实有点{特点}

{具体表现，2-3句}

但其实{反转或补充}

懂的都懂，不懂的...算了不解释了
```

**星座日常类：**
```
{星座}的日常真的很离谱

就比如{场景描述}

{具体行为1}
{具体行为2}

没错说的就是我自己，笑死
```

---

## 使用示例

### 发布单条记录

```
发布标题为"别追了"的记录到小红书
```

### 发布指定ID

```
发布飞书ID为recXXXX的记录到小红书
```

### 批量发布

```
把飞书表格里已生成图片的记录都发布到小红书
```

### 自定义文案发布

```
用这个文案发布到小红书：
标题：射手座真的太自由了
内容：...
图片：/path/to/image.png
```

---

## 发布限制

| 限制项 | 限制值 |
|--------|--------|
| 标题长度 | ≤ 20 字 |
| 正文长度 | ≤ 1000 字 |
| 每日发帖量 | ≤ 50 篇（建议） |
| 图片格式 | PNG/JPG |
| 图片来源 | 本地绝对路径或 HTTP 链接 |

---

## xiaohongshu-mcp 工具列表

| 工具名 | 功能 | 必需参数 |
|--------|------|----------|
| `check_login_status` | 检查登录状态 | 无 |
| `publish_content` | 发布图文 | title, content, images |
| `publish_with_video` | 发布视频 | title, content, video |
| `list_feeds` | 获取首页推荐 | 无 |
| `search_feeds` | 搜索内容 | keyword |
| `get_feed_detail` | 获取帖子详情 | feed_id, xsec_token |
| `post_comment_to_feed` | 发表评论 | feed_id, xsec_token, content |
| `user_profile` | 获取用户主页 | user_id, xsec_token |

---

## 完整发布流程（重要）

```
用户: 发布"别追了"到小红书

Claude 执行:
1. 检查小红书登录状态 ✓
2. 从飞书查询标题为"别追了"的记录
3. 获取记录详情:
   - 星座: 射手座
   - 标题: 别追了
   - record_id: recv6xxxxx（⚠️ 必须记录，用于后续标记已发布）
   - 图片路径: /path/to/image.png
   - 小红书发送文案: (可能为空)
4. 确定发布文案:
   - 如果"小红书发送文案"有内容 → 直接使用
   - 如果为空 → AI 根据模板生成(100-200字)
5. ⚠️【必须】根据文案自动生成话题标签:
   - 分析文案主题（配对/黑化/放弃/性格等）
   - 生成 3-5 个相关标签
   - 示例: ["射手座", "星座", "情感", "12星座"]
6. 调用 publish_content 发布:
   - title: 射手座：别追了，追不上的
   - content: <文案内容>
   - images: [图片路径]
   - tags: [自动生成的标签数组]
7. ⚠️【必须】发布成功后，立即标记飞书记录为已发布:
   - 调用 feishu_mark_published.sh 或直接更新记录
   - "已发布" → true
   - "小红书文案" → 实际发布的文案
```

### 流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    小红书发布完整流程                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 从飞书拉取记录                                           │
│     ├── 记录 record_id（必须保存！）                         │
│     ├── 获取图片路径                                         │
│     └── 获取文案内容                                         │
│                    ↓                                        │
│  2. 自动生成话题标签                                         │
│     ├── 分析文案主题                                         │
│     ├── 匹配标签规则                                         │
│     └── 生成 3-5 个标签                                      │
│                    ↓                                        │
│  3. 发布到小红书                                             │
│     ├── title + content + images + tags                     │
│     └── 确认发布成功                                         │
│                    ↓                                        │
│  4. ⚠️ 回写飞书（必须！）                                    │
│     ├── 标记「已发布」= true                                 │
│     └── 记录发布的文案                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ 发布后必须回写飞书（重要）

**发布成功后，必须立即更新飞书记录的"已发布"字段为 true。**

### 方式一：使用工具脚本（推荐）

```bash
cd "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成"
./scripts/feishu_mark_published.sh <record_id> "<发布的文案>"

# 示例
./scripts/feishu_mark_published.sh recv6ycsM6G5kD "射手宝宝们，遇到这三个星座..."
```

### 方式二：手动 API 调用

```bash
cd "/Users/panyuhang/我的项目/编程/脚本/小红书封面生成"
source .env

RECORD_ID="<记录ID>"
CONTENT="<发布的文案>"

# 获取 Token
TOKEN=$(curl -s "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$LARK_APP_ID\", \"app_secret\": \"$LARK_APP_SECRET\"}" | jq -r '.tenant_access_token')

# 更新记录
curl -s -X PUT "https://open.feishu.cn/open-apis/bitable/v1/apps/$LARK_BITABLE_APP_TOKEN/tables/$LARK_BITABLE_TABLE_ID/records/$RECORD_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"fields\": {\"已发布\": true, \"小红书文案\": \"$CONTENT\"}}"
```

### 失败处理

如果回写失败：
1. 记录失败的 record_id
2. 提示用户手动在飞书中勾选"已发布"
3. 不影响发布成功的状态

---

## 错误处理

### 小红书未登录

提示用户运行登录工具：

```bash
cd xiaohongshu-mcp && ./xiaohongshu-login-darwin-arm64
```

### 图片路径无效

检查图片是否存在，路径是否为绝对路径。

### 发布失败

检查：
1. 标题是否超过20字
2. 正文是否超过1000字
3. 账号是否被限流

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `.mcp.json` | MCP 服务配置 |
| `scripts/feishu_mark_published.sh` | **发布后回写脚本** |
| `xiaohongshu-mcp/` | 小红书 MCP 服务 |
| `xiaohongshu-mcp/cookies.json` | 登录凭证 |
| `skills/publish-to-xiaohongshu/SKILL.md` | 本技能文档 |
| `skills/generate-from-feishu/` | 飞书集成 |

---

## 参考来源

基于 [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 项目。
