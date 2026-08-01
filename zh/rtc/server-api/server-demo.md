---
title: "业务后端参考实现"
description: "业务后端该封装哪些能力、怎么划权限边界，以及扩展 props 与自定义消息约定"
---

**业务后端**：
接收业务客户端请求、做业务判断、再用 `app_key` 调 srtc 服务端 API。

本页供你搭自己的后端时参考，业务后端会调用[srtc服务端srv API](/zh/rtc/server-api/overview)。

## 为什么必须有这一层

srtc 服务端 api 拥有**全局最高的权力**，每个请求都要用 `app_key` 做 HMAC 签名，而 **`app_key` 绝不能出现在客户端**
——它一旦泄露，别人就能用你的应用身份进任意频道、踢任意用户。

所以下面这些只能由你的后端做：

| 能力 | 对应 srtc srvapi |
| --- | --- |
| 签发加入频道token | `channel/grant` |
| 会控（踢人、改用户属性） | `channel/kick-user`、`channel/update-user` |
| 录制、直播、语音录制、转写的启停 | `mcu/*`、`talkrec/*`、`asr/*` |
| 设备接入（SIP / 国标监控等） | `agent/*` |

客户端只拿 token 入频道、收发流，其余一律走你的后端。

## 一个能力一条接口

一般一条业务接口对应一个能力，要调哪个 srtc srvapi 在你的后端代码里指定：

```
POST /你的后端/room/start-record   →  内部调 mcu/start
POST /你的后端/room/kick           →  内部调 channel/kick-user
```

每个接口都应做相关的参数校验和权限判断。

## 音视频权限判断放在哪

如开关摄像头、开关麦、共享等，封装业务后端「接口」——`/open-video`、`/open-audio`、`/start-share`，它们只用判定权限，不需要调任何 srtc srvapi。

相当于业务客户端开摄像头前先问一次业务后端，
「这个用户现在允许开视频吗」（通话是否已开始、是否被主持人禁视频、
是否超出并发上限），拒绝就返回错误码，客户端据此提示用户。

## props 约定

srtc 的频道和用户都带一个 `props` 扩展字段，内容由业务侧定义、srtc服务端只负责存储与广播。
如：

**频道 props** —— 放整个频道的共享状态

```json
{
  "share_state": true,
  "share_uid": "1001",
  "share_track": 3
}
```

**用户 props** —— 放单个用户的状态

```json
{
  "avatar": "https://example.com/avatar.jpg",
  "audio_state": true,
  "video_state": false
}
```

改 `props` 用 [变更用户信息](/zh/rtc/server-api/channel#变更用户信息) 或
[变更频道信息](/zh/rtc/server-api/channel#变更频道信息)，服务端会向频道内所有人广播变更事件，
客户端据此刷新界面。**这是实现「谁在共享」这类状态同步最省事的办法**，
不需要你自己搭一条消息通道。

## 自定义消息约定

需要传递一次性的通知（而不是持久状态）时，用
[发送自定义消息](/zh/rtc/server-api/channel#发送自定义消息)。消息体的结构完全由你定义，
可参考 `action` + `content` 两段式：

```json
{ "action": "chat",        "content": "消息正文" }
{ "action": "video_open",  "content": { "uid": "1001" } }
{ "action": "video_close", "content": { "uid": "1001" } }
{ "action": "audio_open",  "content": { "uid": "1001" } }
{ "action": "audio_close", "content": { "uid": "1001" } }
{ "action": "share_start", "content": { "uid": "1001", "track": 3 } }
{ "action": "share_stop",  "content": { "uid": "1001" } }
```

**状态用 props，动作用自定义消息**：props 是「当前是什么样」，后进频道的人也能读到；
自定义消息是「刚发生了什么」，只有当时在线的人收得到。

## IM 消息 vs 频道内自定义消息

这两个都能"发一条消息给某人"，很容易混。**分界线是：收信人在不在频道里。**

| | 频道内自定义消息 | IM 消息 |
| --- | --- | --- |
| 接口 | [发送自定义消息](/zh/rtc/server-api/channel#发送自定义消息) | [发送IM消息](/zh/rtc/server-api/im#发送im消息) |
| 前提 | 收发双方**都已在同一频道** | 设备 IM 在线即可，**不必在任何频道** |
| 必填 | `channel` | 无频道概念 |
| 寻址 | `ruids`，**留空即广播全频道** | `ruids` 按用户 / `rsids` 按设备，**必须点名** |
| 凭证 | 加入频道 token | 另发的 IM token（`im/grant`） |

一句话记：**频道内的事用自定义消息，把人叫进频道的事用 IM。**

### 什么时候只能用 IM

关键在于**对方还没进频道**，此时频道消息根本送不到他。下面两个是最典型的场景。

#### 呼叫：把人叫进频道

1. 主叫方请求你的后端发起呼叫。后端生成频道名，用 IM 通知被叫方：

```json
{
  "action": "call_invite",
  "content": { "channel": "room-a1b2c3", "caller": "1001", "name": "张三" }
}
```

2. 被叫方收到后振铃。接听、拒接、忙线各回一条 IM 给主叫方：

```json
{ "action": "call_answer", "content": { "channel": "room-a1b2c3" } }
{ "action": "call_refuse", "content": { "channel": "room-a1b2c3" } }
{ "action": "call_busy",   "content": { "channel": "room-a1b2c3" } }
```

3. 接听后两端各自拿 token 加入频道。**此后的交互（静音、共享、聊天）就该换成频道内
   自定义消息了** —— 人已经在频道里，不必再绕 IM。

呼叫超时、主叫取消同理各发一条（`call_timeout` / `call_cancel`），命令名由你定。

#### 让终端无感进频道

被控终端没有交互界面，由后端下发指令让它自己加入频道推流：

```json
{
  "action": "monitor_start",
  "content": { "channel": "mon-9527", "audio": true }
}
{ "action": "monitor_stop", "content": {} }
```

终端收到 `monitor_start` 后自行取 token、加入指定频道、发布摄像头流，全程无需用户操作。
它在收到这条消息之前不在任何频道，所以只能走 IM。

#### 其它

跨频道通知（给不在这个频道里的人发消息）、系统公告等，凡是"收信人不在这个频道"的
场景都归 IM。

### 三个 IM 独有的能力

+ **按设备投递**：一个 uid 可能多端同时在线（手机 + PC）。`rsids` 精确投递到某台设备，
  `ruids` 则发给该用户的全部在线设备。频道消息没有这个维度
+ **查在线设备**：[获取用户所有在线设备](/zh/rtc/server-api/im#获取用户所有在线设备)，
  呼叫前可以先确认对方在不在线
+ **踢设备下线**：[强制下线IM设备](/zh/rtc/server-api/im#强制下线im设备)，用于顶号

设备上下线还会回调 `im_connect` / `im_disconnect` 给你的后端，可以据此维护在线状态。

<Note>
呼叫、邀请这类**不能丢**的消息记得把 `important` 设为 `true` —— 断线重连后会重发。
普通状态同步不必开，它的代价是延迟略高。这两个接口都有这个字段。
</Note>

## 流轨道

客户端发布的每条流带一个 `desc` 描述，服务端和其他客户端靠它区分用途：

| `desc` | 含义 |
| --- | --- |
| `mic` | 麦克风 |
| `camera_big` | 摄像头大流 |
| `camera_small` | 摄像头小流（simulcast 副层） |
| `screen` | 桌面共享 |

订阅时按 `desc` 挑要的那一路，比如九宫格监控只订 `camera_big`。
