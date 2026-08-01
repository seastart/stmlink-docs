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

### 给 AI 看的产物（llms.txt）

Mintlify 自动生成 `/llms.txt` 和 `/llms-full.txt`，**无需配置**，内容取自各页 frontmatter
的 `title` / `description` —— 所以新页面务必写 `description`，它直接决定 AI 拿到的页面摘要
质量。`docs.json` 里另有两处影响 AI 侧的配置：

| 字段 | 作用 |
| --- | --- |
| `description` | 站点总览，出现在 llms.txt 开头的引言里 |
| `markdown.instructions` | 逐页追加到喂给 AI 的 markdown 末尾。放的是客户的 AI 最容易搞错的硬约束（对外接口前缀、app_key 不进客户端、SRTC/SMeeting 术语不通用、各端 API 不通用），改动前想清楚是不是所有页面都该带这句 |

`contextual.options` 给每页加「复制 / 查看 markdown / 在 ChatGPT 或 Claude 中打开」按钮。

### 文档文件

- 格式：Markdown (`.md`)，每个文件需包含正文（目前使用 `.md`，非 `.mdx`）
- **例外**：文件名为 `changelog`、`readme` 等仓库元文件名的页面必须用 `.mdx` 扩展名——Mintlify 构建时会把任意目录下的 `changelog.md`/`readme.md`（不分大小写）当作仓库元文件排除，导致页面 404；`.mdx` 不受此规则影响，URL 不变
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

## 自动生成的页面（服务端 API）

**两个产品的服务端 API 页面都是生成的**，不要手工编辑，改动会在下次同步时被覆盖：

| 产品 | 目录 | 源码仓 | 生成的页 |
| --- | --- | --- | --- |
| SRTC | `zh/rtc/server-api/` | `rtc-backend` | `channel` / `mcu` / `talkrec` / `agent` / `im` / `white-board` / `asr` + `error-codes` |
| SMeeting | `zh/meeting/server-api/` | `meeting-backend` | `user-auth` / `meet` / `meet-admin` / `mcu` + `error-codes` |

页面清单不是写死的 —— 分组来自 `router.go` 的 gin group，新增分组会自动多出一页。

```bash
python3 scripts/sync-server-api.py            # 两个都同步
python3 scripts/sync-server-api.py meeting    # 只同步 SMeeting
mint broken-links                              # 提交前校验
```

后端默认在同级目录（`../rtc-backend`、`../meeting-backend`），可用 `RTC_BACKEND` /
`MEETING_BACKEND` 覆盖。生成器只有一份，在 `rtc-backend/tools/apidoc`，SMeeting 也是跑它，
只是换一套参数（见脚本里的 `PROJECTS`）。

**本仓不存任何接口内容。** 页面上的每一个字——接口名（router.go 路由行上方那一行）、
简介（controller 方法的文档注释）、字段说明与示例值（DTO 字段行尾注释）、错误码
（`app/internal/enum/errcode` 的常量 + sgo/serror 的内置码）——全部来自后端源码，要改
就去改代码（写法见对应后端 README 的「对外接口文档（srvapi）」一节）。本仓只维护两类东西：

| 内容 | 位置 |
| --- | --- |
| 概览（鉴权、签名、响应格式、uid/sid） | `zh/{rtc,meeting}/server-api/overview.md`（手写） |
| 篇幅长的玩法说明（调用时序、多接口配合、值域表格） | `zh/{rtc,meeting}/server-api/guides/`（手写，新增时在脚本对应 `Project` 的 `manual_guides` 里加一行） |

分组的中文标题是唯一的例外：gin group 名是英文，标题表 SRTC 内置在生成器里，
SMeeting 在 `meeting-backend/openapi/groups.json`。**两个产品不能共用一张表** ——
都有 `mcu` / `im` / `agent` 分组但含义不同。

`docs.json` 里「服务端 API」整个分组的 `pages` 由脚本整块重写，顺序固定为
概览 → 接入指南 → 接口文档 → 错误码 → 其它 —— 所以手工往里加页面、调顺序
都会在下次同步时丢失，要改去改脚本里对应 `Project` 的 `manual_head` / `manual_guides` /
`tail`。脚本还会清理孤儿页：接口从代码删除后，对应页面自动消失。

**不进对外文档的路由**用 `Project.skip` 排除。SMeeting 排掉了两类：`callback/rtc` 是
RTC 调进来的入站回调（客户不会调），`im/*api` 与 `agent/*api` 是原样转发到 RTC 的通配
代理（真正的接口文档在 SRTC 那两页，由手写的 `guides/agent-and-im.md` 交代指向）。

**参数渲染用 Mintlify 的 `<ParamField>` / `<ResponseField>` 组件，不用 markdown 表格**
（与下面「各端通用文档规范」里 SDK 文档的表格约定不同）。原因是 Mintlify 把表格列等宽
均分，5 列时每列仅 150px，长的参数说明会被压成竖条。生成器另有 `-render table` 输出
不依赖 Mintlify 组件的通用 markdown，供将来做 llms.txt 这类纯文本产物使用。

接口页与指南页互相引用时：**指南页可以用链接**（`/zh/rtc/server-api/agent#新增设备`），
**代码注释里只用书名号写页名**（如「设备接入指南」）—— 注释同时会进 `openapi/srvapi.json`，
那里的站内相对链接对 apipost 用户是无效的。

下面的「各端通用文档规范」针对**客户端 SDK** 文档（iOS/Android/Web 等手写页面），
不适用于本节所述的自动生成页面。

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
