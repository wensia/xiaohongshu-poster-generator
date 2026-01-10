# 小红书发布 Skill

## 概述
使用 dev-browser 插件控制浏览器，实现小红书笔记的自动发布。

## 触发方式
```
/publish-xhs <标题>
/xiaohongshu <标题>
```

## 前置要求
1. 安装 dev-browser 插件：
   ```
   /plugin marketplace add sawyerhood/dev-browser
   /plugin install dev-browser@sawyerhood/dev-browser
   ```
2. Chrome 已登录小红书账号

## 工作流程

### 1. 获取发布内容
从飞书「星座海报生成」表中拉取记录：
- app_token: `Qt6Qbzzy6aWBgassGQhcUU5vngc`
- table_id: `tblyDtUqcfFMaDfO`
- 字段：标题、正文内容、生成图片路径

### 2. 检查登录状态
使用 dev-browser 打开小红书创作者中心：
```
打开 https://creator.xiaohongshu.com/publish/publish
检查是否需要登录（查找登录按钮或二维码）
如果未登录，提示用户扫码登录
```

### 3. 上传图片
```
点击上传区域或拖拽图片
等待所有图片上传完成（检查上传进度）
```

### 4. 填写内容
```
在标题输入框填入标题（最多20字）
在正文区域填入文案
添加话题标签：#星座 #射手座 等
```

### 5. 发布
```
点击「发布」按钮
等待发布成功提示
```

### 6. 更新状态
更新飞书记录的「已发布」字段为 true

## 降级方案
如果 dev-browser 不可用：
1. 复制文案到剪贴板
2. 打开浏览器让用户手动发布
3. 提供文案和图片路径供手动操作

## 小红书发布页面结构

### URL
- 发布页：`https://creator.xiaohongshu.com/publish/publish`

### 关键元素
- 上传区域：`.upload-wrapper` 或 `input[type="file"]`
- 标题输入：`input[placeholder*="标题"]` 或 `.title-input`
- 正文输入：`.ql-editor` 或 `[contenteditable="true"]`
- 话题添加：点击 `#` 按钮或输入 `#话题名`
- 发布按钮：`.publish-btn` 或 `button:contains("发布")`

## 文案格式化规则

### 标题
- 最多 20 字
- 包含关键词（如星座名）

### 正文
- 保持原有换行格式
- 末尾添加话题标签
- 可选添加 emoji

### 话题标签示例
```
#星座 #射手座 #巨蟹座 #星座配对 #命定之约
```

## 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| 未登录 | 提示用户扫码，等待登录完成 |
| 上传失败 | 重试 3 次，失败则降级手动模式 |
| 网络超时 | 等待并重试 |
| 内容违规 | 提示修改内容 |

## 使用示例

```
用户: /publish-xhs 射手遇到巨蟹

AI:
1. 从飞书拉取「射手遇到巨蟹」记录
2. 打开小红书创作者中心
3. 上传 7 张图片
4. 填入标题和文案
5. 添加话题标签
6. 点击发布
7. 更新飞书记录为已发布
```
