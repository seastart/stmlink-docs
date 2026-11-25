---
title: "会中控制"
description: "会议进行中主持人可做的操作：全体音视频管控、成员角色与踢人、举手处理、呼叫入会"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 meeting-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 结束会议

`POST /server/v1/meet-admin/destroy`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 更新房间视频状态

`POST /server/v1/meet-admin/update-room-camera-state`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="self_unmute_camera_disabled" type="boolean">
  全体关视频时，是否禁止成员自行打开 false:不禁止(默认) true：禁止。camera_disabled 传 false 时会一并重置为 false
</ParamField>

<ParamField body="camera_disabled" type="boolean">
  全体关视频 false:不关(默认) true：关
</ParamField>


请求示例：

```json
{
  "camera_disabled": false,
  "meeting_id": "",
  "room_no": "",
  "self_unmute_camera_disabled": false
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 更新房间音频状态

`POST /server/v1/meet-admin/update-room-mic-state`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="self_unmute_mic_disabled" type="boolean">
  全体静音时，是否禁止成员自行解除 false:不禁止(默认) true：禁止。mic_disabled 传 false 时会一并重置为 false
</ParamField>

<ParamField body="mic_disabled" type="boolean">
  全体静音 false:不静音(默认) true：静音
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "mic_disabled": false,
  "room_no": "",
  "self_unmute_mic_disabled": false
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人更新房间共享状态

`POST /server/v1/meet-admin/update-room-share-disabled`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新房间共享状态

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="share_disabled" type="boolean">
  禁止共享 false:不禁止(默认) true：禁止
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "share_disabled": false
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人更新房间聊天禁用状态

`POST /server/v1/meet-admin/update-room-chat-disabled`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新房间聊天禁用状态

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="chat_disabled" type="boolean" required>
  禁止全体聊天 false:不禁止 true：禁止
</ParamField>


请求示例：

```json
{
  "chat_disabled": false,
  "meeting_id": "",
  "room_no": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人更新房间截屏开关状态

`POST /server/v1/meet-admin/update-room-screenshot-disabled`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新房间截屏开关状态

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="screenshot_disabled" type="boolean" required>
  禁止截屏 false:不禁止 true：禁止
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "screenshot_disabled": false
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人更新房间水印开关状态

`POST /server/v1/meet-admin/update-watermark-disabled`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新房间水印开关状态

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="watermark_disabled" type="boolean" required>
  关闭水印 false:开启水印 true：关闭水印
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "watermark_disabled": false
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人更新房间锁定状态

`POST /server/v1/meet-admin/update-locked`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新房间锁定状态

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="locked" type="boolean" required>
  锁定会议，锁定后新人无法进入 false:不锁定 true：锁定
</ParamField>


请求示例：

```json
{
  "locked": false,
  "meeting_id": "",
  "room_no": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人结束共享

`POST /server/v1/meet-admin/stop-room-share`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

结束会中当前的共享（屏幕或白板），会中没有共享时直接成功。

+ 共享者是设备时，会同时通知设备网关停止发送共享画面

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 转移主持人

`POST /server/v1/meet-admin/move-host`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

转移主持人

把会议的主持人转给会中另一位成员：新主持人的角色变为 1（主持人），原主持人降为 0（普通成员），
会议的 host_uid 同步改为新主持人。变更会以会中自定义消息广播给全体成员，各端 SDK 会同步刷新
成员列表与会控权限。

新主持人必须在会中；目标已经是主持人时直接返回成功。
开启了外部角色模式（业务自定义角色体系）时不支持本接口，请改用「更新用户角色」调整。

**请求参数**

<ParamField body="room_no" type="string">
  房间号，与会议ID二选一
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID，与房间号二选一
</ParamField>

<ParamField body="target_id" type="string" required>
  新主持人的用户ID，必须在会中
  示例：`1001`
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "target_id": "1001"
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人更新用户会中角色

`POST /server/v1/meet-admin/update-user-role`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新用户角色

会中角色默认走内置的三档：0 普通成员、1 主持人、2 联席主持人，各端 SDK 按角色决定会控入口
是否可用。内置角色也可以整套不启用，改用业务自己定义的角色体系（外部角色模式），那时 role 的
取值与含义由业务决定，本接口就是会中调整它的入口（此时也可以改自己的角色），详见《核心概念》
的「自定义角色」一节。以下说明针对使用内置角色的默认情况。

本接口用于「普通成员 ⇄ 联席主持人」的互相设置：传 2 把成员提升为联席主持人，传 0 收回，
变更会同步写入会议的 co_hosts 列表，会后再次入会依然生效。

主持人一场会议只有一位，由会议的 host_uid 决定（服务端创建会议时取 creator），
**不能**用本接口把角色改成 1。
目标用户必须在会中，且不能修改自己的角色。角色变更会以会中自定义消息广播给全体成员，
各端 SDK 会同步刷新成员列表。

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>

<ParamField body="role" type="integer" required>
  目标角色 0普通成员 2联席主持人；主持人(1)由会议的 host_uid 决定，不能在这里指定
  示例：`2`
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "role": 2,
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人更新用户会中昵称

`POST /server/v1/meet-admin/update-user-name`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新用户会中呢称

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>

<ParamField body="nickname" type="string" required>
  改成的会中昵称
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "nickname": "",
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人更新用户聊天禁用状态

`POST /server/v1/meet-admin/update-user-chat-disabled`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新用户聊天禁用状态

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>

<ParamField body="chat_disabled" type="boolean" required>
  禁止该用户聊天 false:不禁止 true：禁止
</ParamField>


请求示例：

```json
{
  "chat_disabled": false,
  "meeting_id": "",
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人关闭用户摄像头

`POST /server/v1/meet-admin/close-user-camera`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

关闭用户摄像头

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人关闭用户麦克风

`POST /server/v1/meet-admin/close-user-mic`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

关闭用户麦克风

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人请求用户共享

`POST /server/v1/meet-admin/request-user-share`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

请求会中成员开始共享，目标可以是普通成员，也可以是设备。

+ 目标是普通成员：给对方发共享邀请，对方同意后才开始共享，接口返回成功只代表邀请已发出
+ 目标是设备（RTSP/国标等经设备网关入会的拉流设备）：设备无法确认，服务端直接让它开始共享
+ 目标是 SIP/H.323 终端：不支持远程开启共享，返回错误码 2126，终端要共享请在终端上按共享键
+ 设备共享与普通成员共享互斥：已有别人在共享返回错误码 2104；设备网关切换失败时共享状态会回滚，并返回网关的错误
+ 结束设备的共享用「结束共享」接口

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id，可以是设备
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人请求用户开视频

`POST /server/v1/meet-admin/request-user-open-camera`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人请求用户开音频

`POST /server/v1/meet-admin/request-user-open-mic`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人踢人

`POST /server/v1/meet-admin/kickout-user`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

把人员或设备移出会议。

经设备网关入会的设备也用本接口移出：target_id 填设备在会中的用户 ID（带 _agent_ 前缀）。

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>

<ParamField body="remove_conferee" type="boolean">
  是否从白名单中移除
</ParamField>

<ParamField body="join_disabled" type="boolean">
  是否黑名单
</ParamField>


请求示例：

```json
{
  "join_disabled": false,
  "meeting_id": "",
  "remove_conferee": false,
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 主持人处理举手申请

`POST /server/v1/meet-admin/confirm-handup`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

处理举手申请

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="target_id" type="string" required>
  用户id
</ParamField>

<ParamField body="code" type="integer" required>
  申请类型 1开音频 2开视频 3聊天 4共享 5绘画(涂鸦)
</ParamField>

<ParamField body="approve" type="boolean" required>
  true 允许 false 不允许
</ParamField>


请求示例：

```json
{
  "approve": false,
  "code": 0,
  "meeting_id": "",
  "room_no": "",
  "target_id": ""
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 会议时呼叫人员入会

`POST /server/v1/meet-admin/call-users`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

把被叫人同步进参会人员（白名单），并给他们的各端推送呼叫。被叫人凭这次呼叫在 30 分钟内入会：
- 普通呼叫（force_join=false）：进入密码会议免输密码，锁定、等候室等其它限制照常
- 强制呼叫（force_join=true）：免密码，并且不受会议锁定、等候室、「主持人入会前不允许他人加入」限制，直接进会

返回 offline_user_ids：呼叫当时即时通讯不在线、一定收不到这次呼叫的被叫人（在线状态查不到时按在线处理，不误报）。
收到但没接、拒接的不在其中，可用「60 秒内没收到该用户的 user_enter 回调」判断。

人员与设备的邀请、强制入会、移出和失败通知的对照，见「邀请入会与移出」指南。

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="conferee" type="array<string>">
  参会人员（兼容旧接口）
</ParamField>

<ParamField body="conferee_details" type="array<object>">
  参会人员详情列表（新接口）
  <Expandable title="元素字段">
    <ParamField body="user_id" type="string" required>
      用户ID，即你系统里的用户唯一标识
    </ParamField>

    <ParamField body="real_name" type="string">
      真实名称
    </ParamField>

    <ParamField body="nickname" type="string">
      会中昵称，不填则用 real_name
    </ParamField>

    <ParamField body="avatar" type="string">
      用户头像
    </ParamField>

    <ParamField body="role" type="integer">
      用户角色 0普通成员 1主持人 2联席主持人。用内置角色时这里不生效，要指定主持人用 creator、指定联席主持人用 co_hosts；只有改用业务自定义角色(外部角色模式)时，会中角色才取这里的值，见《核心概念》的「自定义角色」一节。不传或传 0 时会取用户库里这个人登记的角色，建议显式传，别依赖这层兜底
    </ParamField>

  </Expandable>
</ParamField>

<ParamField body="is_additional" type="boolean">
  是否是追加
</ParamField>

<ParamField body="force_join" type="boolean">
  是否强制加入（仅呼叫入会时有效）。true 时被叫人各端自动入会，且凭这次呼叫 30 分钟内入会不受密码、会议锁定、等候室、主持人入会前不允许他人加入的限制；false 时只免密码
</ParamField>


请求示例：

```json
{
  "conferee": [
    ""
  ],
  "conferee_details": [
    {
      "avatar": "",
      "nickname": "",
      "real_name": "",
      "role": 0,
      "user_id": ""
    }
  ],
  "force_join": false,
  "is_additional": false,
  "meeting_id": "",
  "room_no": ""
}
```

**响应参数**

<ResponseField name="offline_user_ids" type="array<string>">
  呼叫当时即时通讯不在线、一定收不到呼叫的被叫人用户ID；都在线（或在线状态暂时查不到）时为空数组。 在线的人收到但没接、拒接不在其中，可用「60 秒内没收到 user_enter 回调」判断
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "offline_user_ids": [
      ""
    ]
  }
}
```

---

## 主持人更新会议等候室开关

`POST /server/v1/meet-admin/update-waiting-room-disabled`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

会中开启或关闭等候室。

+ 开启后，主持人、联席主持人和会议创建者以外的人入会会先进入等候室，由主持人放行
+ 关闭时，等候室里的人会被全部放行入会
+ 会前也可以调用，会议开始后生效；已结束的会议返回错误码 2103

**请求参数**

<ParamField body="room_no" type="string">
  房间号，与会议ID二选一
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID，与房间号二选一
</ParamField>

<ParamField body="waiting_room_disabled" type="boolean" required>
  是否关闭等候室 false:开启 true:关闭。关闭时等候室里的人会全部被放行入会
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "waiting_room_disabled": false
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 查询等候室成员

`POST /server/v1/meet-admin/waiting-room-users`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

查询当前在等候室里等待的成员，按进入等候室的时间先后排序。

**请求参数**

<ParamField body="room_no" type="string">
  房间号，与会议ID二选一
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID，与房间号二选一
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": ""
}
```

**响应参数**

<ResponseField name="user_id" type="string">
  用户ID
</ResponseField>

<ResponseField name="nickname" type="string">
  昵称
</ResponseField>

<ResponseField name="enter_at" type="integer">
  进入等候室的时间，秒级时间戳
  示例：`1718194667`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "enter_at": 1718194667,
      "nickname": "",
      "user_id": ""
    }
  ]
}
```

---

## 把会中成员移入等候室

`POST /server/v1/meet-admin/move-in-waiting-room`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

把会中成员移入等候室：该成员会被移出会议、进入等候室，等主持人放行后才能重新入会。

+ 会议未开启等候室时返回错误码 2127，先用「更新会议等候室开关」开启
+ 主持人、联席主持人和会议创建者不能移入等候室，返回错误码 2128
+ 目标不在会中返回错误码 2111

**请求参数**

<ParamField body="room_no" type="string">
  房间号，与会议ID二选一
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID，与房间号二选一
</ParamField>

<ParamField body="user_id" type="string" required>
  要移入等候室的用户ID，必须在会中，且不能是主持人或联席主持人
  示例：`1001`
</ParamField>

<ParamField body="nickname" type="string">
  在等候室显示的昵称，不传则沿用其会中昵称
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "nickname": "",
  "room_no": "",
  "user_id": "1001"
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

## 把等候室成员放行入会

`POST /server/v1/meet-admin/move-out-waiting-room`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

把等候室成员放行入会，被放行的成员会收到可以入会的通知。

+ 传 user_id 只放行这一人，该用户不在等候室时返回错误
+ 不传 user_id 则放行等候室里的全部成员

**请求参数**

<ParamField body="room_no" type="string">
  房间号，与会议ID二选一
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID，与房间号二选一
</ParamField>

<ParamField body="user_id" type="string">
  要放行的用户ID，不传则放行等候室里的全部成员
  示例：`1001`
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "user_id": "1001"
}
```

**响应参数**

<ResponseField name="data" type="string">
  返回数据
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": ""
}
```

---

