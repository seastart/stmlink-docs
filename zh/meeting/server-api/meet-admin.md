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

结束共享

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

## 主持人更新用户会中角色

`POST /server/v1/meet-admin/update-user-role`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新用户角色

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
  用户角色
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "role": 0,
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
    <ParamField body="user_id" type="string">
      用户ID
    </ParamField>

    <ParamField body="account" type="string">
      用户帐号
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
      用户角色
    </ParamField>

  </Expandable>
</ParamField>

<ParamField body="is_additional" type="boolean">
  是否是追加
</ParamField>

<ParamField body="force_join" type="boolean">
  是否强制加入(调呼叫入会时参数才有效)
</ParamField>


请求示例：

```json
{
  "conferee": [
    ""
  ],
  "conferee_details": [
    {
      "account": "",
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

