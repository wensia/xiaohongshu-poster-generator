# 小红书星座海报生成器

基于 Claude Code + MCP 的小红书星座内容自动化工作流，支持海报生成、爆文分析、内容发布等功能。

## 功能特性

- **星座海报生成** - 从飞书拉取内容，生成精美的 1080x1440 竖版海报
- **低粉爆文抓取** - 搜索小红书内容，筛选低粉高互动的爆款笔记
- **爆文分析** - AI 分析爆文元素，提取可复用的创作技巧
- **内容生成** - 参考爆文生成原创星座内容
- **自动发布** - 一键发布到小红书
- **评论回复** - 智能生成评论回复

## 项目结构

```
├── skills/                       # Claude Code 技能包
│   ├── _shared/                  # 共享配置和脚本
│   ├── zodiac-poster/            # 海报生成
│   ├── generate-from-feishu/     # 飞书集成
│   ├── upload-to-feishu/         # 上传到飞书
│   ├── fetch-viral-notes/        # 爆文抓取
│   ├── analyze-viral-notes/      # 爆文分析
│   ├── generate-from-viral/      # 从爆文生成
│   ├── publish-to-xiaohongshu/   # 小红书发布
│   └── reply-comments/           # 评论回复
├── xiaohongshu-mcp/              # 小红书 MCP 服务（二进制）
├── config.py.example             # Python 配置模板
├── .mcp.json.example             # MCP 配置模板
└── output/                       # 生成的海报输出
```

---

## 快速开始

### 前置要求

- [Claude Code](https://claude.ai/claude-code) - Anthropic 官方 CLI 工具
- Node.js 18+ - 运行 MCP 服务
- Python 3.10+ - 运行脚本

### 第一步：克隆项目

```bash
git clone https://github.com/wensia/xiaohongshu-poster-generator.git
cd xiaohongshu-poster-generator
```

### 第二步：配置 Python 环境

```bash
# 复制配置文件
cp config.py.example config.py

# 编辑 config.py，填入你的飞书配置（见下方说明）
```

---

## MCP 服务配置

本项目依赖 3 个 MCP 服务，需要分别配置：

| MCP 服务 | 用途 | 来源 |
|----------|------|------|
| lark-mcp | 飞书多维表格读写 | 官方 npm 包 |
| xiaohongshu-mcp | 小红书内容操作 | 项目内置二进制 |
| playwright | 浏览器截图 | 官方 npm 包 |

### 配置方式

**推荐：项目级配置**（`.mcp.json`）

```bash
# 复制模板
cp .mcp.json.example .mcp.json

# 编辑 .mcp.json，填入你的配置
```

`.mcp.json` 内容示例：

```json
{
  "mcpServers": {
    "xiaohongshu-mcp": {
      "type": "sse",
      "url": "http://localhost:18060/mcp/"
    },
    "lark-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@larksuiteoapi/lark-mcp",
        "mcp",
        "-a", "你的飞书AppID",
        "-s", "你的飞书AppSecret"
      ]
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

> **注意**：`.mcp.json` 已在 `.gitignore` 中，不会被提交到 git。

---

## 飞书配置详解

### 1. 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击「创建企业自建应用」
3. 填写应用名称（如：星座海报助手）
4. 创建完成后，进入应用详情页

### 2. 获取凭证

在应用详情页的「凭证与基础信息」中获取：

- **App ID**：`cli_xxxxxxxxxx`
- **App Secret**：`xxxxxxxxxxxxxxxxxxxxxxxx`

### 3. 添加权限

进入「权限管理」→「API 权限」，搜索并添加以下权限：

| 权限名称 | 权限标识 | 用途 |
|----------|----------|------|
| 查看、评论、编辑和管理多维表格 | `bitable:app` | 读写多维表格 |
| 查看、评论和下载云文档 | `drive:drive:readonly` | 读取文档 |
| 上传、下载云文档文件 | `drive:file` | 上传附件 |

### 4. 发布应用

1. 进入「版本管理与发布」
2. 创建版本并提交审核
3. 审核通过后，应用才能正常使用

### 5. 创建多维表格

创建一个多维表格，包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 星座 | 单选 | 12 星座选项 |
| 主题 | 文本 | 海报主题 |
| 标题 | 文本 | 海报标题 |
| 副标题 | 文本 | 海报副标题 |
| 正文内容 | 多行文本 | 内容页正文 |
| 模板 | 单选 | 海报模板样式 |
| 套图 | 附件 | 生成的图片 |
| 已生成 | 复选框 | 生成状态 |
| 已发布 | 复选框 | 发布状态 |

### 6. 配置 config.py

```python
# 飞书应用凭证
LARK_APP_ID = "cli_xxxxxxxxxx"          # 替换为你的 App ID
LARK_APP_SECRET = "xxxxxxxxxxxxxxxx"    # 替换为你的 App Secret

# 多维表格配置
LARK_BITABLES = {
    "星座海报生成": {
        "app_token": "Qt6Qbzzy6axxxxxxxxxx",  # 从表格 URL 获取
        "table_id": "tblyDtUqxxxxxxxx",        # 表格 ID
    },
}
```

**如何获取 app_token**：
- 打开多维表格，URL 格式为：`https://xxx.feishu.cn/base/<app_token>`
- `<app_token>` 就是你需要的值

**如何获取 table_id**：
- 在多维表格中点击数据表名称旁的「...」→「复制链接」
- URL 中 `table=` 后面的值就是 table_id

---

## 小红书 MCP 配置

### 1. 启动服务

```bash
cd xiaohongshu-mcp

# macOS ARM (M1/M2/M3)
./xiaohongshu-login-darwin-arm64

# macOS Intel
./xiaohongshu-login-darwin-amd64

# Linux
./xiaohongshu-login-linux-amd64
```

### 2. 扫码登录

启动后会显示二维码，使用小红书 APP 扫码登录。

### 3. 保持服务运行

登录成功后，服务会在 `http://localhost:18060` 运行。

> **注意**：
> - Cookies 有效期约 7 天，过期需重新扫码
> - 服务需要保持运行状态

### 4. 验证登录状态

在 Claude Code 中运行：

```
检查小红书登录状态
```

---

## 使用方法

### 在 Claude Code 中使用

```bash
# 进入项目目录
cd xiaohongshu-poster-generator

# 启动 Claude Code
claude .
```

### 常用命令

```
# 生成海报
从飞书拉取待生成的记录，生成海报

# 发布指定记录
发布记录 recvXXXXXX 到小红书

# 抓取爆文
抓取"双子座"相关的低粉爆文

# 分析爆文
分析飞书里的待分析爆文

# 回复评论
查看并回复小红书评论
```

### 技能触发词

| 技能 | 触发关键词 |
|------|-----------|
| generate-from-feishu | 从飞书生成、拉取记录 |
| zodiac-poster | 生成海报、制作封面 |
| upload-to-feishu | 上传飞书、回传图片 |
| fetch-viral-notes | 抓取爆文、低粉爆文 |
| analyze-viral-notes | 分析爆文、爆文分析 |
| publish-to-xiaohongshu | 发布小红书、发到小红书 |
| reply-comments | 回复评论、处理评论 |

---

## 海报模板

### 性格独白风 (personality-monologue)
- 7 页结构：封面 + 5 内容页 + 尾页
- 文艺简约风格
- 适合：性格分析、情感共鸣类内容

### 动态编辑风 (editorial-dynamic)
- 6 页结构：封面 + 5 内容页
- 杂志双线布局
- 适合：运势、规则、对比类内容

### 编辑暖调风 (editorial-warm)
- 居中对称布局
- 温和内敛风格
- 适合：配对、常规内容

---

## 常见问题

### Q: lark-mcp 报权限错误？

确保：
1. 飞书应用已添加所需权限
2. 应用已发布（审核通过）
3. 多维表格已授权给应用

### Q: xiaohongshu-mcp 连接失败？

确保：
1. 服务已启动（终端显示 `Server running on port 18060`）
2. 已扫码登录
3. 检查端口是否被占用：`lsof -i :18060`

### Q: 海报截图失败？

确保：
1. Playwright 已安装：`npx playwright install chromium`
2. 使用项目内的截图脚本，而非 MCP Playwright

### Q: Cookies 过期了？

重新启动 xiaohongshu-mcp 并扫码登录。

---

## 注意事项

1. **敏感信息**：`config.py` 和 `.mcp.json` 包含密钥，已在 `.gitignore` 中排除
2. **登录状态**：小红书 cookies 有效期约 7 天
3. **发布频率**：避免短时间内大量发布，建议间隔 5-10 分钟
4. **内容合规**：确保生成的内容符合平台规范

---

## 开发

### 添加新技能

1. 在 `skills/` 下创建目录
2. 添加 `SKILL.md` 描述文件
3. Claude Code 会自动识别

### 目录约定

```
skills/your-skill/
├── SKILL.md           # 技能描述（必须）
├── scripts/           # Python 脚本
├── workflows/         # 工作流文档
└── reference/         # 参考资料
```

---

## License

MIT
