# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

StmLink 开发者文档站，基于 [Mintlify](https://mintlify.com) 构建，覆盖两款 SDK 产品：

- **SRTC 音视频 SDK** (`zh/rtc/`) - 底层音视频流媒体 SDK，支持 iOS、Android、Windows、Web、微信小程序、全平台 C++
- **SMeeting 会议 SDK** (`zh/meeting/`) - 基于 SRTC 的会议业务 SDK，同样覆盖上述平台

## 本地开发

```bash
# 安装 Mintlify CLI（只需一次）
npm install -g mint

# 启动本地预览（localhost:3000）
mint dev

# 检查断链
mint broken-links

# 校验文档构建
mint validate
```

## 架构说明

### 配置文件

`docs.json` 是站点的核心配置，定义了：
- 导航结构（`navigation.languages[].tabs[].groups`）
- 主题色、Logo、页脚链接
- 站点 URL 和基本元数据

**添加新页面后，必须同步更新 `docs.json` 的导航配置，否则页面不会出现在侧边栏。**

### 文档文件

- 格式：Markdown (`.md`)，每个文件需包含正文（目前使用 `.md`，非 `.mdx`）
- 路径即 URL：`zh/rtc/ios/quickstart.md` → `/zh/rtc/ios/quickstart`
- 命名规范：小写英文 + 连字符（kebab-case）
- 图片存放在同目录的 `images/` 子目录下

### 语言目录

- `zh/` - 中文文档（当前主要维护）
- `en/` - 英文文档（待补充，目前为空）

### 导航层级结构

```
navigation.languages（中文/英文）
  └── tabs（SRTC SDK / SMeeting SDK）
        └── groups（概览 / iOS SDK / Android SDK ...）
              └── pages（具体文档路径）
                    └── group（嵌套子分组，如"进阶实践"、"接口文档"）
```

## 注意事项

- 配置文件为 `docs.json`，**不要使用已废弃的 `mint.json`**
- 内部链接使用根相对路径，不带文件扩展名：`/zh/rtc/ios/quickstart`
- 代码块必须标注语言标识符
- 推送到 Git 主分支后 Mintlify 自动部署

---

## 各端通用文档规范

整理新平台文档时，参照以下结构和格式规范，保持各端文档风格统一。

### 通用目录结构

```
{platform}/
├── integration.md          # 集成（环境要求 + 安装 + 引入）
├── quickstart.md           # 快速开始（目标：10 分钟内最小可跑 demo，~80 行代码）
├── key-concepts.md         # 核心概念（SRTC/Channel/Track/事件体系）
├── advanced/               # 进阶实践（每个场景独立一页）
│   ├── mute-vs-unpublish.md    # 静音 vs 停止发布（轻操作 vs 重操作对比）
│   ├── screen-sharing.md       # 屏幕共享（含平台特有特性）
│   └── custom-track.md         # 自定义推流
├── api-reference/          # 接口文档（结构化，含参数表格）
│   ├── {MainClass}.md      # 主类接口
│   └── media-tracks.md     # 轨道类（含继承关系说明）
├── events.md               # 事件参考（表格：事件名 + 触发时机 + data 类型）
├── types.md                # 完整类型定义
├── error-codes.md          # 错误码
├── changelog.md            # 更新日志
└── faq.md                  # 常见问题
```

### 格式规范

- 无 YAML frontmatter（与现有 iOS/Android 文档一致）
- 标题层级：`###` 主标题，`####` 小标题
- 列表用 `+`
- 代码块注明语言标识符（`typescript` / `swift` / `kotlin` 等）
- 接口文档每个方法格式：签名 + 参数表格（参数名 / 类型 / 必填 / 说明）+ 返回值 + 异常（如有）
- `quickstart.md` 只覆盖核心最小流程（~80 行代码），进阶内容放 `advanced/` 下独立页面

### docs.json 导航模板

```json
{ "group": "{平台} SDK", "pages": [
  "{platform}/integration",
  "{platform}/quickstart",
  "{platform}/key-concepts",
  { "group": "进阶实践", "pages": [
    "{platform}/advanced/mute-vs-unpublish",
    "{platform}/advanced/screen-sharing",
    "{platform}/advanced/custom-track"
  ]},
  { "group": "接口文档", "pages": [
    "{platform}/api-reference/{MainClass}",
    "{platform}/api-reference/media-tracks"
  ]},
  "{platform}/events",
  "{platform}/types",
  "{platform}/error-codes",
  "{platform}/changelog",
  "{platform}/faq"
]}
```
