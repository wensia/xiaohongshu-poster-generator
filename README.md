# 小红书星座海报生成器

基于 Claude Code + MCP 的小红书星座内容自动化工作流，支持海报生成、爆文分析、内容发布等功能。

## 功能特性

- **星座海报生成** - 从飞书拉取内容，生成精美的 1080x1440 竖版海报
- **低粉爆文抓取** - 搜索小红书内容，筛选低粉高互动的爆款笔记
- **爆文分析** - AI 分析爆文元素，提取可复用的创作技巧
- **内容生成** - 参考爆文生成原创星座内容
- **文案优化** - 生成符合小红书风格的"有人味"文案
- **自动发布** - 一键发布到小红书
- **评论回复** - 智能生成评论回复

## 项目结构

```
├── skills/                    # 技能包
│   ├── _shared/              # 共享配置
│   │   ├── feishu-config.md
│   │   └── xiaohongshu-login.md
│   ├── zodiac-poster/        # 海报生成
│   ├── publish-to-xiaohongshu/  # 小红书发布
│   ├── generate-from-feishu/ # 飞书集成
│   ├── fetch-viral-notes/    # 爆文抓取
│   ├── analyze-viral-notes/  # 爆文分析
│   ├── generate-from-viral/  # 从爆文生成
│   ├── generate-copywriting/ # 文案生成
│   ├── reply-comments/       # 评论回复
│   └── upload-to-feishu/     # 上传到飞书
├── xiaohongshu-mcp/          # 小红书 MCP 服务
├── config.py.example         # 配置模板
├── .env.example              # 环境变量模板
└── output/                   # 生成的海报输出
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/xiaohongshu-poster-generator.git
cd xiaohongshu-poster-generator
```

### 2. 配置环境

```bash
# 复制配置文件
cp config.py.example config.py
cp .env.example .env

# 编辑 config.py，填入飞书凭证
```

### 3. 配置飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app) 创建应用
2. 获取 App ID 和 App Secret
3. 添加多维表格权限
4. 填入 `config.py`

### 4. 配置小红书 MCP

```bash
cd xiaohongshu-mcp
./xiaohongshu-login-darwin-arm64  # macOS ARM
# 扫码登录
```

### 5. 配置 Claude Code MCP

在 Claude Code 中添加 MCP 服务器：

```json
{
  "mcpServers": {
    "xiaohongshu-mcp": {
      "command": "./xiaohongshu-mcp/xiaohongshu-login-darwin-arm64",
      "args": ["mcp"]
    },
    "lark-mcp": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/lark-mcp@latest"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/playwright-mcp@latest"]
    }
  }
}
```

## 使用方法

### 在 Claude Code 中使用技能

```
# 生成海报
从飞书拉取记录，生成海报

# 抓取爆文
抓取"星座运势"相关的低粉爆文

# 分析爆文
分析飞书里的爆文

# 发布到小红书
发布一篇小红书，标题：xxx
```

### 技能触发关键词

| 技能 | 触发关键词 |
|------|-----------|
| zodiac-poster | 生成海报、制作封面 |
| fetch-viral-notes | 抓取爆文、低粉爆文 |
| analyze-viral-notes | 分析爆文、爆文分析 |
| generate-from-viral | 从爆文生成、爆文转海报 |
| generate-copywriting | 生成文案、写文案 |
| publish-to-xiaohongshu | 发布小红书、发到小红书 |
| reply-comments | 回复评论、处理评论 |

## 海报模板

### editorial-warm（编辑暖调）
- 居中对称布局
- 温和内敛风格
- 适合：配对、对比、常规内容

### editorial-dynamic（动态编辑）
- 非对称布局
- 视觉张力强
- 适合：运势、性格、规则类内容

## 飞书多维表格

### 星座海报生成表

| 字段 | 类型 | 说明 |
|------|------|------|
| 星座 | 单选 | 12星座 |
| 标题 | 文本 | 海报主标题 |
| 正文内容 | 长文本 | 内容页正文 |
| 小红书文案 | 长文本 | 发布文案 |
| 已生成 | 复选框 | 生成状态 |
| 已发布 | 复选框 | 发布状态 |

### 低粉爆文抓取表

| 字段 | 类型 | 说明 |
|------|------|------|
| 笔记ID | 文本 | 小红书笔记ID |
| 标题 | 文本 | 笔记标题 |
| 点赞数 | 数字 | 互动数据 |
| 已分析 | 复选框 | 分析状态 |
| 爆款元素 | 文本 | AI分析结果 |

## 依赖服务

- [Claude Code](https://claude.com/claude-code) - AI 编程助手
- [飞书开放平台](https://open.feishu.cn) - 数据存储
- [Playwright MCP](https://github.com/anthropics/playwright-mcp) - 浏览器自动化
- [Lark MCP](https://github.com/anthropics/lark-mcp) - 飞书 API
- xiaohongshu-mcp - 小红书 API

## 注意事项

1. **敏感信息**：`config.py` 和 `.env` 包含密钥，请勿提交到公开仓库
2. **登录状态**：小红书 cookies 有效期约 7 天，过期需重新登录
3. **发布频率**：避免短时间内大量发布，建议间隔 5-10 分钟
4. **内容合规**：确保生成的内容符合平台规范

## 贡献

欢迎提交 Issue 和 Pull Request！

## License

MIT
