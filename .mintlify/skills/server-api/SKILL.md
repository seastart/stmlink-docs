---
name: SRTC / SMeeting 服务端接入
description: 从业务后端调 SRTC 或 SMeeting 的 HTTP 接口时使用——HMAC-SHA256 签名怎么算、Token 怎么签发下发、事件回调怎么接、两个产品的服务端差异在哪。出现「认证失败」「签名错误」时先读这个。
metadata:
  version: "1.0"
  docs: https://docs.stmlink.com
---

# SRTC / SMeeting 服务端接入

服务端接口只能从**业务方自己的后端**调用，因为签名要用 `app_key`。

## 铁律：app_key 不出后端

| 凭据 | 用途 | 能否到客户端 |
| --- | --- | --- |
| `app_id` | 标识应用 | 可以 |
| `app_key` | 签名密钥 | **绝对不行** |

拿到 `app_key` 的人可以签发任意用户身份的 token、踢人、销毁频道。它不能出现在：客户端代码、前端配置文件、移动 App 包体、Git 仓库、日志。

**客户端拿到的永远只是后端签发好的 token，不是密钥。**

## 签名算法（两个产品完全一致）

四个请求头：`app_id`、`nonce`、`timestamp`、`signature`。

```text
第一步  拼待签名串：  {应用id头名}={app_id}&nonce={nonce}&timestamp={timestamp}&{原始请求体}
第二步  HMAC-SHA256(app_key, 待签名串)
第三步  转成小写十六进制 → signature
```

约束：

- `nonce` 16 位随机字符串，防重复提交
- `timestamp` unix 秒，与服务器相差不能超过 **5 分钟**
- 只支持 `POST`，`application/json`，UTF-8

### 三个最常见的签名失败原因


**1. 头名和签名串不一致（最高频）**

应用 id 的请求头有三种写法都接受：`app_id`、`app-id`、`appid`（按此优先级取第一个非空的）。但**签名串开头必须写你实际用的那个**：

```text
用 app_id 请求头 → app_id=1&nonce=2&timestamp=3&{}
用 appid  请求头 → appid=1&nonce=2&timestamp=3&{}   ← 不能写成 app_id=
```

用了 `app_id` 头却拼 `appid=...` 会直接认证失败。三种写法存在只是为了兼容部分语言/网关不支持下划线。

**2. 请求体被重新序列化**

签名必须用**实际发出的原始字节**，含空格与字段顺序。先 `JSON.stringify` 算签名、再让 HTTP 库自己序列化一遍 body，两次结果不同就会失败。正确做法是先生成 body 字符串，签名和发送都用同一份。

**3. 把 app_key 放进了请求**

`app_key` 只用于本地计算签名，不作为任何请求头或字段发送。

## Token 签发流程

```text
1. 客户端向你的后端请求进入某频道/会议
2. 你的后端校验用户身份与权限   ← 你自己的业务逻辑，我们不管
3. 后端调签发接口（带签名）
4. 拿到 token 下发给客户端
5. 客户端用 token 加入
```

第 2 步是关键：**SRTC / SMeeting 都不管你的用户体系**，谁有资格进、进去是什么身份，全由你的后端判断。

| 产品 | 签发接口 |
| --- | --- |
| SRTC | `POST /server/v1/channel/grant` |
| SMeeting | `POST /stm/srvapi/v1/member/grant` |

**token 与一次会话绑定，用过即失效**。每个客户端实例单独签发；复用会拿到「会话不在线」类错误。

## 两个产品的服务端差异

签名一致，但其余不同——**不要把一层的接口套到另一层**。

| | SRTC | SMeeting |
| --- | --- | --- |
| 基地址 | `https://{域名}/` | `https://{域名}/meeting/` |
| 接口前缀 | `/server/v1/...` | `/server/v1/...`（会议主接口）与 `/stm/srvapi/v1/...`（用户体系） |
| 业务错误码段 | `1xxx` | `2xxx` |
| 列表响应 | `code` / `data` | `code` / `data` / `_meta`（翻页信息） |
| 概念 | 频道 channel、uid、流轨道 | 房间 room、会议 meeting、参会成员 |

**基地址最容易拼错**：标准部署下 SRTC 在域名根路径，SMeeting 在 `/meeting/` 之下。
两层都有 `/server/v1/` 前缀，所以漏掉 `/meeting` 时请求会打到 SRTC 上找不到会议接口。

```text
建会议  https://{域名}/meeting/server/v1/meet/create
签 token https://{域名}/meeting/stm/srvapi/v1/member/grant
会议页  https://{域名}/meeting/stm/ui/outer?token=...&room_no=...

加入频道 token（SRTC） https://{域名}/server/v1/channel/grant
```

独立域名部署时前缀可能不同，以我们提供的接入信息为准。除上述前缀外的接口都是内部接口，不要调用。

## 常用接口

**SRTC**

| 接口 | 用途 |
| --- | --- |
| `POST /server/v1/channel/grant` | 签发加入频道 token |
| `POST /server/v1/channel/detail` | 查频道状态 |
| `POST /server/v1/channel/list-user` | 查频道成员 |
| `POST /server/v1/channel/kick-user` | 踢人 |
| `POST /server/v1/channel/set-callback` | 注册事件回调地址（一次性） |
| `POST /server/v1/mcu/start` / `stop` | 起停录制 / 合流 / 转推任务 |
| `POST /server/v1/im/grant` / `send-msg` | IM 令牌与发消息 |

**SMeeting**

| 接口 | 用途 |
| --- | --- |
| `POST /server/v1/meet/create` | 建会议，返回 `room_no` |
| `POST /server/v1/meet/set-callback` | 注册事件回调地址 |
| `POST /server/v1/meet/list-meet` / `list-user` | 查会议 / 查成员 |
| `POST /stm/srvapi/v1/member/grant` | 签发免登录 token |
| `POST /stm/srvapi/v1/member/sync` / `info` | 同步用户 / 查在线状态 |

接口的完整参数以文档站为准，**不要凭记忆编字段名**。

## 响应与错误码

```json
{ "code": 0, "data": { } }          // 成功
{ "code": 1003, "msg": "签名错误" }  // 失败
```

**按 `code` 判断，不要匹配 `msg` 文案**——文案会随版本变。

排查方向：

| 码 | 含义 | 先查 |
| --- | --- | --- |
| `1002` | AppID 无效 | 用错环境的 app_id |
| `1003` | 签名错误 | 上面那三个签名失败原因 |
| `1021` | Token 已被使用 | token 复用，重新签发 |
| `1032` | 会话不在线 | 同一 token 起了第二个实例 |

4 位码来自服务端；客户端 SDK 自身的错误是 6 位（`100xxx` 通用、`10Nxxx` 分平台、`180xxx` C SDK）。

## 事件回调

调 `set-callback` 注册一次你的 webhook 地址，之后服务端会推送 `user_join`、`user_leave`、`channel_destroy`、录制完成等事件。

- 回调要**幂等**——可能重复投递
- 及时返回 2xx，耗时逻辑异步做
- 频道会在最后一人离开 2 小时后自动销毁，别假设频道长期存在

## 交付前自检

- [ ] `app_key` 只存在于后端，不在代码库、配置、日志里
- [ ] 签名串的应用 id 字段名与实际请求头名一致
- [ ] 请求体用原始字符串签名，没有二次序列化
- [ ] `timestamp` 用服务器同步过的时间，误差在 5 分钟内
- [ ] `nonce` 每次随机，没有写死
- [ ] token 每次新签，没有缓存复用
- [ ] 用对了产品对应的接口前缀，没跨层混用
- [ ] 回调接口幂等且快速返回
- [ ] 按 `code` 判断结果，没匹配 `msg`

## 深入查阅

先取 https://docs.stmlink.com/llms.txt 看全站目录，再按需读页面（URL 末尾加 `.md` 拿 Markdown）。

- SRTC 服务端 API `/zh/rtc/server-api/overview` · 错误码 `/zh/rtc/server-api/error-codes`
- SMeeting 服务端 API `/zh/meeting/server-api/overview`
- 服务端极简对接 `/zh/meeting/ui-sdk/server-integration`
