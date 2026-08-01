---
title: "会议管理"
description: "会前会后的会议编排：创建、修改、取消、查询，以及参会记录与聊天记录"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 meeting-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 设置事件通知

`POST /server/v1/meet/set-callback`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

设置回调信息

**请求参数**

<ParamField body="events" type="array<string>">
  监听事件列表
</ParamField>

<ParamField body="cb_url" type="string">
  回调地址
</ParamField>


请求示例：

```json
{
  "cb_url": "",
  "events": [
    ""
  ]
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

## 查询会议列表

`POST /server/v1/meet/list-meet`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

会议列表

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="meeting_ids" type="array<string>">
  会议id列表
</ParamField>

<ParamField body="meeting_type" type="integer">
  按会议类型筛选 1即时会议 2预约会议
</ParamField>

<ParamField body="meeting_status" type="array<integer>">
  按会议状态筛选，可多选 1未开始 2进行中 3已结束
</ParamField>

<ParamField body="creator" type="string">
  按创建者用户ID筛选
</ParamField>

<ParamField body="begin_at" type="integer">
  开始时间
</ParamField>

<ParamField body="end_at" type="integer">
  结束时间
</ParamField>

<ParamField body="plan_begin_at" type="integer">
  会议计划开始时间区间
</ParamField>

<ParamField body="plan_end_at" type="integer">
  会议计划开始时间区间
</ParamField>

<ParamField body="plan_time" type="integer">
  开始时间 (时间戳)，预约会议必填
</ParamField>

<ParamField body="sort" type="string">
  排序，可排序字段 created_at，前缀 - 表示倒序（可排序字段：created_at）
</ParamField>

<ParamField body="page" type="integer">
  页数，从1开始
  示例：`1`
</ParamField>

<ParamField body="per-page" type="integer">
  每页数据量
  示例：`10`
</ParamField>


请求示例：

```json
{
  "begin_at": 0,
  "creator": "",
  "end_at": 0,
  "meeting_id": "",
  "meeting_ids": [
    ""
  ],
  "meeting_status": [
    0
  ],
  "meeting_type": 0,
  "page": 1,
  "per-page": 10,
  "plan_begin_at": 0,
  "plan_end_at": 0,
  "plan_time": 0,
  "room_no": "",
  "sort": ""
}
```

**响应参数**

<ResponseField name="id" type="string">
  会议id
</ResponseField>

<ResponseField name="room_no" type="string">
  房间号
</ResponseField>

<ResponseField name="title" type="string">
  会议标题
</ResponseField>

<ResponseField name="content" type="string">
  会议说明
</ResponseField>

<ResponseField name="meeting_status" type="integer">
  会议状态 1未开始 2进行中 3结束
</ResponseField>

<ResponseField name="attend_type" type="integer">
  1 无限制(默认) 2 密码进入 3 仅邀请人员参会
</ResponseField>

<ResponseField name="meeting_type" type="integer">
  会议类型 1即时会议 2预约会议
</ResponseField>

<ResponseField name="plan_time" type="integer">
  开始时间 (时间戳)，预约会议必填
</ResponseField>

<ResponseField name="plan_dur" type="integer">
  持续时间(单位分钟)，预约会议必填
</ResponseField>

<ResponseField name="begin_time" type="integer">
  开始时间
</ResponseField>

<ResponseField name="end_time" type="integer">
  结束时间
</ResponseField>

<ResponseField name="last_exit_time" type="integer">
  最后一人离会的时间戳，会议未结束时为 0
</ResponseField>

<ResponseField name="entry_mute_policy" type="integer">
  入会静音选项
</ResponseField>

<ResponseField name="watermark_disabled" type="boolean">
  水印是否关闭 false:不关闭 true:关闭
</ResponseField>

<ResponseField name="screenshot_disabled" type="boolean">
  截屏是否禁止 false:不禁止 true:禁止
</ResponseField>

<ResponseField name="self_unmute_mic_disabled" type="boolean">
  房间禁音允许自我解除 false:允许解除 true:不允许
</ResponseField>

<ResponseField name="self_unmute_camera_disabled" type="boolean">
  房间禁视频允许自我解除 false:允许解除 true:不允许
</ResponseField>

<ResponseField name="mic_disabled" type="boolean">
  房间禁音频 false:不禁音 true:禁音
</ResponseField>

<ResponseField name="camera_disabled" type="boolean">
  房间禁视频 false:不禁视频 true:禁视频
</ResponseField>

<ResponseField name="share_disabled" type="boolean">
  禁止共享 false:不禁止(默认) true：禁止
</ResponseField>

<ResponseField name="chat_disabled" type="boolean">
  房间禁聊天 false:不禁聊天 true:禁聊天
</ResponseField>

<ResponseField name="waiting_room_disabled" type="boolean">
  等待室是否关闭 false:不关闭 true:关闭
</ResponseField>

<ResponseField name="enter_before_host_disabled" type="boolean">
  在主持人前禁入会 false:允许 true:禁止
</ResponseField>

<ResponseField name="force_join" type="boolean">
  强制入会
</ResponseField>

<ResponseField name="locked" type="boolean">
  锁定状态 false:不锁定 true:锁定
</ResponseField>

<ResponseField name="extend_info" type="object">
  扩展字段
</ResponseField>

<ResponseField name="creator" type="string">
  会议创建者ID
</ResponseField>

<ResponseField name="creator_name" type="string">
  会议创建者名称
</ResponseField>

<ResponseField name="host_uid" type="string">
  主持人用户ID
</ResponseField>

<ResponseField name="co_hosts" type="array<string>">
  联席主持人用户ID列表
</ResponseField>

<ResponseField name="conferee" type="array<string>">
  邀请人员ID列表
</ResponseField>

<ResponseField name="conferee_details" type="array<object>">
  邀请人员详情列表
  <Expandable title="元素字段">
    <ResponseField name="user_id" type="string">
      用户ID
    </ResponseField>

    <ResponseField name="account" type="string">
      用户帐号
    </ResponseField>

    <ResponseField name="real_name" type="string">
      真实名称
    </ResponseField>

    <ResponseField name="nickname" type="string">
      会中昵称
    </ResponseField>

    <ResponseField name="avatar" type="string">
      用户头像
    </ResponseField>

    <ResponseField name="role" type="integer">
      用户角色
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="meeting_mode" type="integer">
  会议模式字段 1普通模式 2合成模式
</ResponseField>

<ResponseField name="auto_record" type="boolean">
  是否自动录像
</ResponseField>

<ResponseField name="layout_data" type="any">
  布局数据
</ResponseField>

<ResponseField name="record_status" type="integer">
  录制状态 0待开始 1进行中 2待结束 3异常结束 4正常结束
</ResponseField>

<ResponseField name="created_at" type="integer">
  创建时间(时间戳)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  更新时间
</ResponseField>


响应示例：

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "attend_type": 0,
      "auto_record": false,
      "begin_time": 0,
      "camera_disabled": false,
      "chat_disabled": false,
      "co_hosts": [
        ""
      ],
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
      "content": "",
      "created_at": 0,
      "creator": "",
      "creator_name": "",
      "end_time": 0,
      "enter_before_host_disabled": false,
      "entry_mute_policy": 0,
      "extend_info": {},
      "force_join": false,
      "host_uid": "",
      "id": "",
      "last_exit_time": 0,
      "layout_data": null,
      "locked": false,
      "meeting_mode": 0,
      "meeting_status": 0,
      "meeting_type": 0,
      "mic_disabled": false,
      "plan_dur": 0,
      "plan_time": 0,
      "record_status": 0,
      "room_no": "",
      "screenshot_disabled": false,
      "self_unmute_camera_disabled": false,
      "self_unmute_mic_disabled": false,
      "share_disabled": false,
      "title": "",
      "updated_at": 0,
      "waiting_room_disabled": false,
      "watermark_disabled": false
    }
  ]
}
```

---

## 查询会中人员列表

`POST /server/v1/meet/list-user`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

会中人员

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="page" type="integer">
  页数，从1开始
  示例：`1`
</ParamField>

<ParamField body="per-page" type="integer">
  每页数据量
  示例：`10`
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "room_no": ""
}
```

**响应参数**

<ResponseField name="user_id" type="string">
  用户ID
</ResponseField>

<ResponseField name="nickname" type="string">
  会中昵称
</ResponseField>

<ResponseField name="role" type="integer">
  用户角色
</ResponseField>

<ResponseField name="mic_state" type="integer">
  音频状态 1开, 2关
</ResponseField>

<ResponseField name="camera_state" type="integer">
  视频状态 1开, 2关
</ResponseField>

<ResponseField name="share_state" type="integer">
  共享状态 0无共享 1屏幕 2白板
</ResponseField>

<ResponseField name="is_kickout" type="boolean">
  是否已被踢出
</ResponseField>

<ResponseField name="chat_disabled" type="boolean">
  是否被禁止聊天 false:未禁止 true:已禁止
</ResponseField>

<ResponseField name="device_type" type="integer">
  设备类型 0未知 1Windows 2Android 3iOS 4Linux 5MacOS 6webrtc 7小程序，80及以上为接入设备
</ResponseField>

<ResponseField name="extend_info" type="string">
  扩展字段，入会时由客户端带入
</ResponseField>

<ResponseField name="join_at" type="integer">
  进入时间
</ResponseField>


响应示例：

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "camera_state": 0,
      "chat_disabled": false,
      "device_type": 0,
      "extend_info": "",
      "is_kickout": false,
      "join_at": 0,
      "mic_state": 0,
      "nickname": "",
      "role": 0,
      "share_state": 0,
      "user_id": ""
    }
  ]
}
```

---

## 查询会议相关人员

`POST /server/v1/meet/meeting-users`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

会议相关人员

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="page" type="integer">
  页数，从1开始
  示例：`1`
</ParamField>

<ParamField body="per-page" type="integer">
  每页数据量
  示例：`10`
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "room_no": ""
}
```

**响应参数**

<ResponseField name="user_id" type="string">
  用户ID
</ResponseField>

<ResponseField name="account" type="string">
  用户帐号
</ResponseField>

<ResponseField name="real_name" type="string">
  真实名称
</ResponseField>

<ResponseField name="nickname" type="string">
  会中昵称
</ResponseField>

<ResponseField name="avatar" type="string">
  用户头像
</ResponseField>

<ResponseField name="role" type="integer">
  用户角色
</ResponseField>

<ResponseField name="is_invite" type="boolean">
  是否邀约(白名单)
</ResponseField>

<ResponseField name="enter_at" type="integer">
  首次入会时间
</ResponseField>

<ResponseField name="exit_at" type="integer">
  最后离开会时间
</ResponseField>


响应示例：

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "account": "",
      "avatar": "",
      "enter_at": 0,
      "exit_at": 0,
      "is_invite": false,
      "nickname": "",
      "real_name": "",
      "role": 0,
      "user_id": ""
    }
  ]
}
```

---

## 查询参会记录

`POST /server/v1/meet/list-record`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

参会记录

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="user_id" type="string">
  用户ID
</ParamField>

<ParamField body="begin_at" type="integer">
  开始时间
</ParamField>

<ParamField body="end_at" type="integer">
  结束时间
</ParamField>

<ParamField body="sort" type="string">
  排序，可排序字段 updated_at / created_at，逗号分隔，前缀 - 表示倒序（可排序字段：updated_at、created_at）
</ParamField>

<ParamField body="page" type="integer">
  页数，从1开始
  示例：`1`
</ParamField>

<ParamField body="per-page" type="integer">
  每页数据量
  示例：`10`
</ParamField>


请求示例：

```json
{
  "begin_at": 0,
  "end_at": 0,
  "meeting_id": "",
  "page": 1,
  "per-page": 10,
  "room_no": "",
  "sort": "",
  "user_id": ""
}
```

**响应参数**

<ResponseField name="app_id" type="string">
  应用ID
</ResponseField>

<ResponseField name="meeting_id" type="string">
  会议ID
</ResponseField>

<ResponseField name="user_id" type="string">
  用户ID
</ResponseField>

<ResponseField name="nickname" type="string">
  会中昵称
</ResponseField>

<ResponseField name="mobile" type="string">
  手机号
</ResponseField>

<ResponseField name="role" type="integer">
  用户角色
</ResponseField>

<ResponseField name="enter_time" type="integer">
  进入时间
</ResponseField>

<ResponseField name="exit_time" type="integer">
  离开时间
</ResponseField>

<ResponseField name="device_type" type="integer">
  设备类型 0未知 1Windows 2Android 3iOS 4Linux 5MacOS 6webrtc 7小程序，80及以上为接入设备
</ResponseField>

<ResponseField name="extend_info" type="string">
  扩展字段，入会时由客户端带入
</ResponseField>


响应示例：

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "app_id": "",
      "device_type": 0,
      "enter_time": 0,
      "exit_time": 0,
      "extend_info": "",
      "meeting_id": "",
      "mobile": "",
      "nickname": "",
      "role": 0,
      "user_id": ""
    }
  ]
}
```

---

## 会中发送自定义消息

`POST /server/v1/meet/send-room-custom-message`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="meeting_id" type="string" required>
  会议ID
</ParamField>

<ParamField body="content" type="string" required>
  消息内容，最长500字符（最大长度 500）
</ParamField>

<ParamField body="target_id" type="string">
  用户id
</ParamField>


请求示例：

```json
{
  "content": "",
  "meeting_id": "",
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

## 会议详情

`POST /server/v1/meet/detail`

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

<ResponseField name="id" type="string">
  设备ID
</ResponseField>

<ResponseField name="room_no" type="string">
  房间号
</ResponseField>

<ResponseField name="title" type="string">
  会议标题
</ResponseField>

<ResponseField name="content" type="string">
  会议说明
</ResponseField>

<ResponseField name="meeting_status" type="integer">
  会议状态 1未开始 2进行中 3已结束
</ResponseField>

<ResponseField name="attend_type" type="integer">
  1 无限制(默认) 2 密码进入 3 仅邀请人员参会
</ResponseField>

<ResponseField name="meeting_type" type="integer">
  会议类型 1即时会议 2预约会议
</ResponseField>

<ResponseField name="password" type="string">
  密码，attend_type为2时必填
</ResponseField>

<ResponseField name="plan_time" type="integer">
  开始时间 (时间戳)，预约会议必填
</ResponseField>

<ResponseField name="plan_dur" type="integer">
  持续时间(单位分钟)，预约会议必填
</ResponseField>

<ResponseField name="begin_time" type="integer">
  实际开始时间(时间戳)，未开始为 0
</ResponseField>

<ResponseField name="end_time" type="integer">
  结束时间
</ResponseField>

<ResponseField name="last_exit_time" type="integer">
  最后一人离会的时间戳，会议未结束时为 0
</ResponseField>

<ResponseField name="online_num" type="integer">
  当前在线人数
</ResponseField>

<ResponseField name="entry_mute_policy" type="integer">
  入会静音状态 1:开启入会静音(所有人入会默认静音) 2:关闭(跟随客户端初始音频状态) 3：超6人静音(超过6人后入会静音) 默认值3
</ResponseField>

<ResponseField name="watermark_disabled" type="boolean">
  水印是否关闭 false:不关闭 true:关闭
</ResponseField>

<ResponseField name="screenshot_disabled" type="boolean">
  截屏是否禁止 false:不禁止 true:禁止
</ResponseField>

<ResponseField name="self_unmute_mic_disabled" type="boolean">
  全体静音时是否禁止成员自行解除 false:不禁止 true:禁止
</ResponseField>

<ResponseField name="self_unmute_camera_disabled" type="boolean">
  全体关视频时是否禁止成员自行打开 false:不禁止 true:禁止
</ResponseField>

<ResponseField name="mic_disabled" type="boolean">
  全体静音 false:未静音 true:已静音
</ResponseField>

<ResponseField name="camera_disabled" type="boolean">
  全体关视频 false:未关 true:已关
</ResponseField>

<ResponseField name="share_disabled" type="boolean">
  禁止共享 false:不禁止(默认) true：禁止
</ResponseField>

<ResponseField name="chat_disabled" type="boolean">
  是否禁止全体聊天 false:不禁止 true:禁止
</ResponseField>

<ResponseField name="waiting_room_disabled" type="boolean">
  等待室是否关闭 false:不关闭 true:关闭
</ResponseField>

<ResponseField name="enter_before_host_disabled" type="boolean">
  主持人入会前是否禁止他人进入 false:允许 true:禁止
</ResponseField>

<ResponseField name="force_join" type="boolean">
  强制入会
</ResponseField>

<ResponseField name="locked" type="boolean">
  锁定状态，锁定后新人无法进入 false:不锁定 true:锁定
</ResponseField>

<ResponseField name="extend_info" type="object">
  扩展字段
</ResponseField>

<ResponseField name="creator" type="string">
  会议创建者ID
</ResponseField>

<ResponseField name="creator_name" type="string">
  会议创建者名称
</ResponseField>

<ResponseField name="host_uid" type="string">
  主持人用户ID
</ResponseField>

<ResponseField name="co_hosts" type="array<string>">
  联席主持人用户ID列表
</ResponseField>

<ResponseField name="conferee" type="array<string>">
  邀请人员ID列表
</ResponseField>

<ResponseField name="conferee_details" type="array<object>">
  邀请人员详情列表
  <Expandable title="元素字段">
    <ResponseField name="user_id" type="string">
      用户ID
    </ResponseField>

    <ResponseField name="account" type="string">
      用户帐号
    </ResponseField>

    <ResponseField name="real_name" type="string">
      真实名称
    </ResponseField>

    <ResponseField name="nickname" type="string">
      会中昵称
    </ResponseField>

    <ResponseField name="avatar" type="string">
      用户头像
    </ResponseField>

    <ResponseField name="role" type="integer">
      用户角色
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="meeting_mode" type="integer">
  会议模式字段 1普通模式 2合成模式 3语音模式 4培训模式 5小组讨论模式
</ResponseField>

<ResponseField name="auto_record" type="boolean">
  是否自动录像
</ResponseField>

<ResponseField name="layout_data" type="any">
  布局数据
</ResponseField>

<ResponseField name="record_status" type="integer">
  录制状态 0待开始 1进行中 2待结束 3异常结束 4正常结束
</ResponseField>

<ResponseField name="created_at" type="integer">
  创建时间(时间戳)
</ResponseField>

<ResponseField name="updated_at" type="integer">
  更新时间
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "attend_type": 0,
    "auto_record": false,
    "begin_time": 0,
    "camera_disabled": false,
    "chat_disabled": false,
    "co_hosts": [
      ""
    ],
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
    "content": "",
    "created_at": 0,
    "creator": "",
    "creator_name": "",
    "end_time": 0,
    "enter_before_host_disabled": false,
    "entry_mute_policy": 0,
    "extend_info": {},
    "force_join": false,
    "host_uid": "",
    "id": "",
    "last_exit_time": 0,
    "layout_data": null,
    "locked": false,
    "meeting_mode": 0,
    "meeting_status": 0,
    "meeting_type": 0,
    "mic_disabled": false,
    "online_num": 0,
    "password": "",
    "plan_dur": 0,
    "plan_time": 0,
    "record_status": 0,
    "room_no": "",
    "screenshot_disabled": false,
    "self_unmute_camera_disabled": false,
    "self_unmute_mic_disabled": false,
    "share_disabled": false,
    "title": "",
    "updated_at": 0,
    "waiting_room_disabled": false,
    "watermark_disabled": false
  }
}
```

---

## 取消会议

`POST /server/v1/meet/cancel`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

取消会议(仅会议前)

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

## 创建会议

`POST /server/v1/meet/create`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

**请求参数**

<ParamField body="creator" type="string">
  创建人
</ParamField>

<ParamField body="creator_name" type="string">
  创建人昵称
</ParamField>

<ParamField body="room_no" type="string">
  房间号（最大长度 50）
</ParamField>

<ParamField body="title" type="string" required>
  会议标题（最大长度 100）
</ParamField>

<ParamField body="content" type="string">
  会议说明（最大长度 500）
</ParamField>

<ParamField body="password" type="string">
  入会密码（最大长度 50）
</ParamField>

<ParamField body="meeting_type" type="integer" required>
  会议类型 1:即时会议 2：预约会议
</ParamField>

<ParamField body="attend_type" type="integer">
  加入会议类型 1 无限制 2 密码进入 3 邀请人员参会 4密码+白名单
</ParamField>

<ParamField body="co_hosts" type="array<string>">
  联席主持ID列表
</ParamField>

<ParamField body="conferee" type="array<string>">
  邀请人员列表（兼容旧接口）
</ParamField>

<ParamField body="conferee_details" type="array<object>">
  邀请人员详情列表（新接口）
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

<ParamField body="plan_time" type="integer">
  开始时间
</ParamField>

<ParamField body="plan_dur" type="integer">
  持续时长 (单位分钟)
</ParamField>

<ParamField body="entry_mute_policy" type="integer">
  入会静音选项
</ParamField>

<ParamField body="watermark_disabled" type="boolean">
  水印是否关闭 false:不关闭 true:关闭
</ParamField>

<ParamField body="screenshot_disabled" type="boolean">
  截屏是否禁止 false:不禁止 true:禁止
</ParamField>

<ParamField body="self_unmute_mic_disabled" type="boolean">
  房间禁音允许自我解除 false:允许解除 true:不允许
</ParamField>

<ParamField body="self_unmute_camera_disabled" type="boolean">
  房间禁视频允许自我解除 false:允许解除 true:不允许
</ParamField>

<ParamField body="mic_disabled" type="boolean">
  房间禁音频 false:不禁音 true:禁音
</ParamField>

<ParamField body="camera_disabled" type="boolean">
  房间禁视频 false:不禁视频 true:禁视频
</ParamField>

<ParamField body="share_disabled" type="boolean">
  房间禁共享 false:不禁共享 true:禁共享
</ParamField>

<ParamField body="chat_disabled" type="boolean">
  房间禁聊天 false:不禁聊天 true:禁聊天
</ParamField>

<ParamField body="waiting_room_disabled" type="boolean">
  等待室是否关闭 false:不关闭 true:关闭
</ParamField>

<ParamField body="enter_before_host_disabled" type="boolean">
  主持人入会前是否允许其他人加入 false:允许 true:不允许
</ParamField>

<ParamField body="force_join" type="boolean">
  是否强制加入
</ParamField>

<ParamField body="extend_info" type="object">
  扩展字段
</ParamField>

<ParamField body="meeting_mode" type="integer">
  会议模式字段 1普通模式 2合成模式
</ParamField>

<ParamField body="auto_record" type="boolean">
  是否自动录像
</ParamField>

<ParamField body="layout_data" type="object">
  布局数据
  <Expandable title="字段">
    <ParamField body="layout" type="string" required>
      布局类型
    </ParamField>

    <ParamField body="watermark" type="object">
      水印
      <Expandable title="字段">
        <ParamField body="type" type="integer">
          类型 0默认, 1无, 2单排, 3多排
        </ParamField>

        <ParamField body="text" type="string">
          指定内容, 空表示自动(会议标题)
        </ParamField>

        <ParamField body="size" type="integer">
          字体大小, 0表示默认值
        </ParamField>

        <ParamField body="color" type="string">
          字体颜色, 空表示默认值
        </ParamField>

        <ParamField body="ol_color" type="string">
          轮廓颜色, 空表示默认值
        </ParamField>

        <ParamField body="ol_width" type="integer">
          轮廓线宽, 0表示默认值
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="nobody_text" type="string">
      会中无人时显示的文本, 空表示无人时停止录制
    </ParamField>

    <ParamField body="tag" type="object">
      默认标签
      <Expandable title="字段">
        <ParamField body="type" type="string">
          类型, 字母或组合: L左, R右, T上, B下
        </ParamField>

        <ParamField body="text" type="string">
          指定内容, 空表示自动(会中名称)
        </ParamField>

        <ParamField body="size" type="integer">
          字体大小, 0表示默认
        </ParamField>

        <ParamField body="color" type="string">
          字体颜色, 空表示默认
        </ParamField>

        <ParamField body="bg_color" type="string">
          背景颜色, 空表示默认
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="polling_dur" type="integer">
      轮询时长(秒) 0不轮询
    </ParamField>

    <ParamField body="div_list" type="array<object>">
      逻辑块列表
      <Expandable title="元素字段">
        <ParamField body="cells" type="array<object>">
          宫格列表, 空表示剩余格子共用此处的用户
        </ParamField>

        <ParamField body="uids" type="array<string>">
          用户ID列表, 空表示大轮询在线剩余用户, 多个表示小轮询
        </ParamField>

      </Expandable>
    </ParamField>

  </Expandable>
</ParamField>


请求示例：

```json
{
  "attend_type": 0,
  "auto_record": false,
  "camera_disabled": false,
  "chat_disabled": false,
  "co_hosts": [
    ""
  ],
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
  "content": "",
  "creator": "",
  "creator_name": "",
  "enter_before_host_disabled": false,
  "entry_mute_policy": 0,
  "extend_info": {},
  "force_join": false,
  "layout_data": {
    "div_list": [
      {
        "cells": [
          {
            "bind_share": false,
            "idx": 0,
            "tag": {
              "bg_color": "",
              "color": "",
              "size": 0,
              "text": "",
              "type": ""
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "",
    "nobody_text": "",
    "polling_dur": 0,
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": ""
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 0
    }
  },
  "meeting_mode": 0,
  "meeting_type": 0,
  "mic_disabled": false,
  "password": "",
  "plan_dur": 0,
  "plan_time": 0,
  "room_no": "",
  "screenshot_disabled": false,
  "self_unmute_camera_disabled": false,
  "self_unmute_mic_disabled": false,
  "share_disabled": false,
  "title": "",
  "waiting_room_disabled": false,
  "watermark_disabled": false
}
```

**响应参数**

<ResponseField name="meeting_id" type="string">
  会议ID，后续所有会议接口都用它
</ResponseField>

<ResponseField name="room_no" type="string">
  房间号，用户在客户端输入这个号码进会
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "meeting_id": "",
    "room_no": ""
  }
}
```

---

## 会前修改会议

`POST /server/v1/meet/update`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

更新会议

**请求参数**

<ParamField body="meeting_id" type="string" required>
  会议ID
</ParamField>

<ParamField body="creator" type="string">
  创建人
</ParamField>

<ParamField body="title" type="string">
  会议标题（最大长度 100）
</ParamField>

<ParamField body="content" type="string">
  会议说明（最大长度 500）
</ParamField>

<ParamField body="attend_type" type="integer">
  加入会议类型 1 无限制 2 密码进入 3 邀请人员参会 4密码+白名单
</ParamField>

<ParamField body="password" type="string">
  入会密码（最大长度 50）
</ParamField>

<ParamField body="conferee" type="array<string>">
  邀请人员列表（兼容旧接口）
</ParamField>

<ParamField body="conferee_details" type="array<object>">
  邀请人员详情列表（新接口）
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

<ParamField body="plan_time" type="integer">
  开始时间
</ParamField>

<ParamField body="plan_dur" type="integer">
  持续时长 (单位分钟)
</ParamField>

<ParamField body="entry_mute_policy" type="integer">
  入会静音选项
</ParamField>

<ParamField body="watermark_disabled" type="boolean">
  水印是否关闭 false:不关闭 true:关闭
</ParamField>

<ParamField body="screenshot_disabled" type="boolean">
  截屏是否禁止 false:不禁止 true:禁止
</ParamField>

<ParamField body="chat_disabled" type="boolean">
  房间禁聊天 false:不禁聊天 true:禁聊天
</ParamField>

<ParamField body="waiting_room_disabled" type="boolean">
  等待室是否关闭 false:不关闭 true:关闭
</ParamField>

<ParamField body="enter_before_host_disabled" type="boolean">
  主持人入会前是否允许其他人加入 false:允许 true:不允许
</ParamField>

<ParamField body="force_join" type="boolean">
  是否强制加入
</ParamField>

<ParamField body="co_hosts" type="array<string>">
  联席主持ID列表
</ParamField>

<ParamField body="extend_info" type="object">
  扩展字段
</ParamField>

<ParamField body="meeting_mode" type="integer">
  会议模式字段 1普通模式 2合成模式
</ParamField>

<ParamField body="auto_record" type="boolean">
  是否自动录像
</ParamField>

<ParamField body="layout_data" type="object">
  布局数据
  <Expandable title="字段">
    <ParamField body="layout" type="string" required>
      布局类型
    </ParamField>

    <ParamField body="watermark" type="object">
      水印
      <Expandable title="字段">
        <ParamField body="type" type="integer">
          类型 0默认, 1无, 2单排, 3多排
        </ParamField>

        <ParamField body="text" type="string">
          指定内容, 空表示自动(会议标题)
        </ParamField>

        <ParamField body="size" type="integer">
          字体大小, 0表示默认值
        </ParamField>

        <ParamField body="color" type="string">
          字体颜色, 空表示默认值
        </ParamField>

        <ParamField body="ol_color" type="string">
          轮廓颜色, 空表示默认值
        </ParamField>

        <ParamField body="ol_width" type="integer">
          轮廓线宽, 0表示默认值
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="nobody_text" type="string">
      会中无人时显示的文本, 空表示无人时停止录制
    </ParamField>

    <ParamField body="tag" type="object">
      默认标签
      <Expandable title="字段">
        <ParamField body="type" type="string">
          类型, 字母或组合: L左, R右, T上, B下
        </ParamField>

        <ParamField body="text" type="string">
          指定内容, 空表示自动(会中名称)
        </ParamField>

        <ParamField body="size" type="integer">
          字体大小, 0表示默认
        </ParamField>

        <ParamField body="color" type="string">
          字体颜色, 空表示默认
        </ParamField>

        <ParamField body="bg_color" type="string">
          背景颜色, 空表示默认
        </ParamField>

      </Expandable>
    </ParamField>

    <ParamField body="polling_dur" type="integer">
      轮询时长(秒) 0不轮询
    </ParamField>

    <ParamField body="div_list" type="array<object>">
      逻辑块列表
      <Expandable title="元素字段">
        <ParamField body="cells" type="array<object>">
          宫格列表, 空表示剩余格子共用此处的用户
        </ParamField>

        <ParamField body="uids" type="array<string>">
          用户ID列表, 空表示大轮询在线剩余用户, 多个表示小轮询
        </ParamField>

      </Expandable>
    </ParamField>

  </Expandable>
</ParamField>


请求示例：

```json
{
  "attend_type": 0,
  "auto_record": false,
  "chat_disabled": false,
  "co_hosts": [
    ""
  ],
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
  "content": "",
  "creator": "",
  "enter_before_host_disabled": false,
  "entry_mute_policy": 0,
  "extend_info": {},
  "force_join": false,
  "layout_data": {
    "div_list": [
      {
        "cells": [
          {
            "bind_share": false,
            "idx": 0,
            "tag": {
              "bg_color": "",
              "color": "",
              "size": 0,
              "text": "",
              "type": ""
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "",
    "nobody_text": "",
    "polling_dur": 0,
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": ""
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 0
    }
  },
  "meeting_id": "",
  "meeting_mode": 0,
  "password": "",
  "plan_dur": 0,
  "plan_time": 0,
  "screenshot_disabled": false,
  "title": "",
  "waiting_room_disabled": false,
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

## 修改参会人员

`POST /server/v1/meet/update-conferee`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

会议时修改参会人员

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

## 移除参会人员

`POST /server/v1/meet/delete-conferee`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

删除白名单用户

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="user_ids" type="array<string>" required>
  用户ID列表
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "room_no": "",
  "user_ids": [
    ""
  ]
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

## 查询用户聊天记录

`POST /server/v1/meet/user-chat-record`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

用户聊天记录

**请求参数**

<ParamField body="room_no" type="string">
  房间号
</ParamField>

<ParamField body="meeting_id" type="string">
  会议ID
</ParamField>

<ParamField body="sender_id" type="string">
  按发送者用户ID筛选
</ParamField>

<ParamField body="msg_type" type="integer">
  消息类型  1:文本 2:文件 3:图片 4:语音
</ParamField>

<ParamField body="msg" type="string">
  消息内容
</ParamField>

<ParamField body="begin_at" type="integer">
  聊天时间区间
</ParamField>

<ParamField body="end_at" type="integer">
  聊天时间区间
</ParamField>

<ParamField body="sort" type="string">
  排序字段，逗号分隔，前缀 - 表示倒序，如 -created_at
</ParamField>

<ParamField body="page" type="integer">
  页数，从1开始
  示例：`1`
</ParamField>

<ParamField body="per-page" type="integer">
  每页数据量
  示例：`10`
</ParamField>


请求示例：

```json
{
  "begin_at": 0,
  "end_at": 0,
  "meeting_id": "",
  "msg": "",
  "msg_type": 0,
  "page": 1,
  "per-page": 10,
  "room_no": "",
  "sender_id": "",
  "sort": ""
}
```

**响应参数**

<ResponseField name="id" type="string">
  设备ID
</ResponseField>

<ResponseField name="meeting_id" type="string">
  会议ID
</ResponseField>

<ResponseField name="sender_id" type="string">
  消息发送者第三方用户ID
</ResponseField>

<ResponseField name="sender_name" type="string">
  消息发送者名称
</ResponseField>

<ResponseField name="real_name" type="string">
  消息发送者真实姓名
</ResponseField>

<ResponseField name="role" type="integer">
  消息发送者角色
</ResponseField>

<ResponseField name="msg_type" type="integer">
  消息类型  1:文本 2:文件 3:图片 4:语音
</ResponseField>

<ResponseField name="msg" type="string">
  消息内容
</ResponseField>

<ResponseField name="created_at" type="integer">
  发送时间(时间戳)
</ResponseField>


响应示例：

```json
{
  "_meta": {
    "currentPage": 1,
    "pageCount": 5,
    "perPage": 20,
    "totalCount": 100
  },
  "code": 0,
  "data": [
    {
      "created_at": 0,
      "id": "",
      "meeting_id": "",
      "msg": "",
      "msg_type": 0,
      "real_name": "",
      "role": 0,
      "sender_id": "",
      "sender_name": ""
    }
  ]
}
```

---

## 查询聊天记录中的文件

`POST /server/v1/meet/chat-record-files`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

聊天记录文件

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

<ResponseField name="name" type="string">
  文件名
</ResponseField>

<ResponseField name="size" type="string">
  文件大小(字节)
</ResponseField>

<ResponseField name="key" type="string">
  文件的Key
</ResponseField>

<ResponseField name="url" type="string">
  播放/下载地址 2小时有效
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "key": "",
      "name": "",
      "size": "",
      "url": ""
    }
  ]
}
```

---

## 今日会议概况

`POST /server/v1/meet/today`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

今日数据

**请求参数**

无

**响应参数**

<ResponseField name="time" type="integer">
  日期
</ResponseField>

<ResponseField name="num" type="integer">
  次数
</ResponseField>

<ResponseField name="dur" type="integer">
  时长(秒)
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "dur": 0,
    "num": 0,
    "time": 0
  }
}
```

---

## 会议量统计

`POST /server/v1/meet/stats`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

会议统计

**请求参数**

<ParamField body="begin_at" type="integer">
  开始时间
</ParamField>

<ParamField body="end_at" type="integer">
  结束时间
</ParamField>


请求示例：

```json
{
  "begin_at": 0,
  "end_at": 0
}
```

**响应参数**

<ResponseField name="day" type="string">
  日期
</ResponseField>

<ResponseField name="num" type="integer">
  次数
</ResponseField>

<ResponseField name="dur" type="integer">
  时长(秒)
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "day": "",
      "dur": 0,
      "num": 0
    }
  ]
}
```

---

