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
      用户角色 0普通成员 1主持人 2联席主持人
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
  用户角色 0普通成员 1主持人 2联席主持人
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
  设备类型 0未知 1Windows 2Android 3iOS 4Linux 5MacOS 6webrtc 7小程序 8鸿蒙，80及以上为接入设备
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
  用户角色 0普通成员 1主持人 2联席主持人
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
  用户角色 0普通成员 1主持人 2联席主持人
</ResponseField>

<ResponseField name="enter_time" type="integer">
  进入时间
</ResponseField>

<ResponseField name="exit_time" type="integer">
  离开时间
</ResponseField>

<ResponseField name="device_type" type="integer">
  设备类型 0未知 1Windows 2Android 3iOS 4Linux 5MacOS 6webrtc 7小程序 8鸿蒙，80及以上为接入设备
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
      用户角色 0普通成员 1主持人 2联席主持人
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
  创建人，即会议主持人。填你系统里的用户唯一标识，与 conferee_details 的 user_id 同一个值
</ParamField>

<ParamField body="creator_name" type="string">
  创建人昵称
</ParamField>

<ParamField body="room_no" type="string">
  房间号（会议号）。不传则随机生成；传入则作为本应用的固定会议号，可反复使用、每场主持人可不同。同一会议号同时只能有一场未结束的会议（含未开始的预约）；未登记过的号在近 90 天内被会议用过则拒绝（最大长度 50）
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
  联席主持ID列表。填你系统里的用户唯一标识，与 conferee_details 的 user_id 同一个值
</ParamField>

<ParamField body="conferee" type="array<string>">
  邀请人员列表（兼容旧接口）
</ParamField>

<ParamField body="conferee_details" type="array<object>">
  邀请人员详情列表（新接口）
  <Expandable title="元素字段">
    <ParamField body="user_id" type="string">
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
    <ParamField body="layout" type="string">
      布局类型: auto自动 full全屏 right_4右侧小窗 top_4顶部小窗 br_7下L型 tl_7上L型 tb_8左右布局, 等分宫格 grids_N (N 取 2,3,4,5,6,8,9,12,16,20,25), 回字型 ring_16大回字型(25宫格合并中间9格) ring_12小回字型(16宫格合并中间4格) 不传时使用服务端默认布局（默认为 auto，可由部署方调整）
      示例：`auto`
    </ParamField>

    <ParamField body="watermark" type="object">
      水印
      <Expandable title="字段">
        <ParamField body="type" type="integer">
          类型 0默认, 1无, 2单排, 3多排
          示例：`1`
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
          示例：`L`
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

    <ParamField body="push_url" type="string">
      推流地址, 仅任务类型含 8(直播流) 时生效: 传了则把合成画面推到该地址(推流模式), 不再提供拉流地址; 支持 rtmp:// 与 rtmps://, 须带推流码(如 rtmp://host/app/ 这类流名为空的地址会被拒绝)。 任务进行中再次调用开始接口时不传则沿用原地址及其音频来源; 没有可用的推流服务时返回错误码 1072
      示例：`rtmp://live.example.com/app/stream_key`
    </ParamField>

    <ParamField body="push_audio" type="string">
      推流的音频来源, 仅传了 push_url 时生效: mix 房间合成音频(默认)、none 不要音频、user 某个用户的音频(须同时传 push_audio_uid)
      示例：`mix`
    </ParamField>

    <ParamField body="push_audio_uid" type="string">
      push_audio 为 user 时必填: 取哪个用户的音频(会中用户ID)
      示例：`1001`
    </ParamField>

    <ParamField body="push_audio_desc" type="string">
      push_audio 为 user 时可选: 该用户的哪条音频轨道(按轨道描述精确匹配), 不传取该用户的第一条音频
      示例：`mic`
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
              "type": "L"
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "auto",
    "nobody_text": "",
    "polling_dur": 0,
    "push_audio": "mix",
    "push_audio_desc": "mic",
    "push_audio_uid": "1001",
    "push_url": "rtmp://live.example.com/app/stream_key",
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": "L"
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 1
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
  创建人，即会议主持人。填你系统里的用户唯一标识，与 conferee_details 的 user_id 同一个值
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
  联席主持ID列表。填你系统里的用户唯一标识，与 conferee_details 的 user_id 同一个值
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
    <ParamField body="layout" type="string">
      布局类型: auto自动 full全屏 right_4右侧小窗 top_4顶部小窗 br_7下L型 tl_7上L型 tb_8左右布局, 等分宫格 grids_N (N 取 2,3,4,5,6,8,9,12,16,20,25), 回字型 ring_16大回字型(25宫格合并中间9格) ring_12小回字型(16宫格合并中间4格) 不传时使用服务端默认布局（默认为 auto，可由部署方调整）
      示例：`auto`
    </ParamField>

    <ParamField body="watermark" type="object">
      水印
      <Expandable title="字段">
        <ParamField body="type" type="integer">
          类型 0默认, 1无, 2单排, 3多排
          示例：`1`
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
          示例：`L`
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

    <ParamField body="push_url" type="string">
      推流地址, 仅任务类型含 8(直播流) 时生效: 传了则把合成画面推到该地址(推流模式), 不再提供拉流地址; 支持 rtmp:// 与 rtmps://, 须带推流码(如 rtmp://host/app/ 这类流名为空的地址会被拒绝)。 任务进行中再次调用开始接口时不传则沿用原地址及其音频来源; 没有可用的推流服务时返回错误码 1072
      示例：`rtmp://live.example.com/app/stream_key`
    </ParamField>

    <ParamField body="push_audio" type="string">
      推流的音频来源, 仅传了 push_url 时生效: mix 房间合成音频(默认)、none 不要音频、user 某个用户的音频(须同时传 push_audio_uid)
      示例：`mix`
    </ParamField>

    <ParamField body="push_audio_uid" type="string">
      push_audio 为 user 时必填: 取哪个用户的音频(会中用户ID)
      示例：`1001`
    </ParamField>

    <ParamField body="push_audio_desc" type="string">
      push_audio 为 user 时可选: 该用户的哪条音频轨道(按轨道描述精确匹配), 不传取该用户的第一条音频
      示例：`mic`
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
              "type": "L"
            }
          }
        ],
        "uids": [
          ""
        ]
      }
    ],
    "layout": "auto",
    "nobody_text": "",
    "polling_dur": 0,
    "push_audio": "mix",
    "push_audio_desc": "mic",
    "push_audio_uid": "1001",
    "push_url": "rtmp://live.example.com/app/stream_key",
    "tag": {
      "bg_color": "",
      "color": "",
      "size": 0,
      "text": "",
      "type": "L"
    },
    "watermark": {
      "color": "",
      "ol_color": "",
      "ol_width": 0,
      "size": 0,
      "text": "",
      "type": 1
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
  消息发送者角色 0普通成员 1主持人 2联席主持人
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

## 开启会议转写

`POST /server/v1/meet/asr-start`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

对进行中的会议开启实时转写，可同时开启实时翻译。返回本次转写的场次 session_id。

+ 会中所有开麦成员的发言都会被转写，客户端通过频道消息 asr_res（原文）、asr_trans（译文）拿到字幕
+ 会议结束时转写自动停止，不必先调「关闭会议转写」
+ 应用开启了纪要时，每场转写结束后自动生成会议纪要，用「查询会议纪要」获取

转写、翻译与纪要依赖平台侧的语音识别与大模型配置，未配置时返回对应错误。

**请求参数**

<ParamField body="meeting_id" type="string" required>
  会议ID，必须是进行中的会议
</ParamField>

<ParamField body="translate_lang" type="string">
  实时翻译目标语言，空表示只转写不翻译（最大长度 10）
  示例：`en`
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "translate_lang": "en"
}
```

**响应参数**

<ResponseField name="session_id" type="string">
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "session_id": ""
  }
}
```

---

## 关闭会议转写

`POST /server/v1/meet/asr-stop`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

关闭会议的实时转写。已产生的转写结果保留，应用开启了纪要时随后自动生成本场纪要。

**请求参数**

<ParamField body="meeting_id" type="string" required>
  会议ID
</ParamField>


请求示例：

```json
{
  "meeting_id": ""
}
```

**响应参数**

`data` 为 null

响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

## 查询会议纪要

`POST /server/v1/meet/ai-summary`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

查询会议的转写场次及各场最新纪要，按开始时间升序。

+ 一场会议中途关闭再开启转写会产生多个场次，每场单独生成纪要
+ summary 为 null 表示该场尚未生成纪要；status 为 0/1 表示排队或生成中，2 完成，3 失败（error 为原因）
+ content 为 Markdown 格式

**请求参数**

<ParamField body="meeting_id" type="string" required>
  会议ID
</ParamField>


请求示例：

```json
{
  "meeting_id": ""
}
```

**响应参数**

<ResponseField name="session_id" type="string">
  转写场次ID
</ResponseField>

<ResponseField name="started_at" type="integer">
  转写开始时间(秒)
</ResponseField>

<ResponseField name="ended_at" type="integer">
  转写结束时间(秒), 进行中为0
</ResponseField>

<ResponseField name="status" type="integer">
  场次状态 1转写中 2已结束
</ResponseField>

<ResponseField name="sentence_count" type="integer">
  转写句子数
</ResponseField>

<ResponseField name="summary_status" type="integer">
  纪要状态 -1未生成 0排队 1生成中 2完成 3失败
</ResponseField>

<ResponseField name="summary" type="object">
  最新纪要; 尚未生成(或应用未开纪要)时为 null
  <Expandable title="字段">
    <ResponseField name="summary_id" type="string">
      纪要ID
    </ResponseField>

    <ResponseField name="session_id" type="string">
      识别场次ID
    </ResponseField>

    <ResponseField name="channel" type="string">
      频道名, 即会议ID
    </ResponseField>

    <ResponseField name="template_id" type="string">
      纪要模板ID
    </ResponseField>

    <ResponseField name="status" type="integer">
      状态 0排队 1生成中 2完成 3失败
    </ResponseField>

    <ResponseField name="content" type="string">
      纪要正文(Markdown); 重新生成失败时保留上一次成功的内容
    </ResponseField>

    <ResponseField name="model" type="string">
      生成所用模型
    </ResponseField>

    <ResponseField name="prompt_tokens" type="integer">
      输入token数
    </ResponseField>

    <ResponseField name="completion_tokens" type="integer">
      输出token数
    </ResponseField>

    <ResponseField name="error" type="string">
      失败原因(状态为失败时)
    </ResponseField>

    <ResponseField name="finished_at" type="integer">
      完成时间(秒)
    </ResponseField>

    <ResponseField name="created_at" type="integer">
      创建时间(秒)
    </ResponseField>

    <ResponseField name="updated_at" type="integer">
      最后变更时间(秒)
    </ResponseField>

  </Expandable>
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "ended_at": 0,
      "sentence_count": 0,
      "session_id": "",
      "started_at": 0,
      "status": 0,
      "summary": {
        "channel": "",
        "completion_tokens": 0,
        "content": "",
        "created_at": 0,
        "error": "",
        "finished_at": 0,
        "model": "",
        "prompt_tokens": 0,
        "session_id": "",
        "status": 0,
        "summary_id": "",
        "template_id": "",
        "updated_at": 0
      },
      "summary_status": 0
    }
  ]
}
```

---

## 查询会议转写原文

`POST /server/v1/meet/ai-transcript`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

查询会议的转写原文，按场次组织（按开始时间升序），每场返回全部定稿句子。

+ 场次划分与「查询会议纪要」一致，传 session_id 只取该场
+ 句子按 begin_ms 升序；begin_ms / end_ms 是相对该场 started_at 的毫秒
+ trans_text 为译文，未开启实时翻译时为空

**请求参数**

<ParamField body="meeting_id" type="string" required>
  会议ID
</ParamField>

<ParamField body="session_id" type="string">
  转写场次ID，不传表示取本会议全部场次
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "session_id": ""
}
```

**响应参数**

<ResponseField name="session_id" type="string">
  转写场次ID
</ResponseField>

<ResponseField name="started_at" type="integer">
  转写开始时间(秒), 句子的 begin_ms/end_ms 相对它计算
</ResponseField>

<ResponseField name="ended_at" type="integer">
  转写结束时间(秒), 进行中为0
</ResponseField>

<ResponseField name="status" type="integer">
  场次状态 1转写中 2已结束
</ResponseField>

<ResponseField name="sentences" type="array<object>">
  定稿句子, 按句首时刻升序; 没有句子时为空数组
  <Expandable title="元素字段">
    <ResponseField name="sentence_id" type="string">
      句子ID, 与频道消息 asr_trans 里的 sentence_id 对应
    </ResponseField>

    <ResponseField name="channel" type="string">
      频道名, 即会议ID
    </ResponseField>

    <ResponseField name="session_id" type="string">
      所属识别场次ID
    </ResponseField>

    <ResponseField name="uid" type="string">
      说话人用户ID
    </ResponseField>

    <ResponseField name="name" type="string">
      说话人会中昵称
    </ResponseField>

    <ResponseField name="sentence" type="string">
      原文
    </ResponseField>

    <ResponseField name="begin_ms" type="integer">
      句首时刻, 相对场次开始的毫秒
    </ResponseField>

    <ResponseField name="end_ms" type="integer">
      句尾时刻, 相对场次开始的毫秒
    </ResponseField>

    <ResponseField name="trans_text" type="string">
      译文, 未开启翻译时为空
    </ResponseField>

    <ResponseField name="trans_lang" type="string">
      译文语言, 如 en
    </ResponseField>

    <ResponseField name="created_at" type="integer">
      产生时间(秒)
    </ResponseField>

  </Expandable>
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "ended_at": 0,
      "sentences": [
        {
          "begin_ms": 0,
          "channel": "",
          "created_at": 0,
          "end_ms": 0,
          "name": "",
          "sentence": "",
          "sentence_id": "",
          "session_id": "",
          "trans_lang": "",
          "trans_text": "",
          "uid": ""
        }
      ],
      "session_id": "",
      "started_at": 0,
      "status": 0
    }
  ]
}
```

---

## 重新生成会议纪要

`POST /server/v1/meet/ai-summary-generate`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

重新生成某场转写的会议纪要，可换用其它纪要模板。异步执行，完成后用「查询会议纪要」获取最新结果。

**请求参数**

<ParamField body="meeting_id" type="string" required>
  会议ID
</ParamField>

<ParamField body="session_id" type="string" required>
  转写场次ID，取自「查询会议纪要」返回的 session_id
</ParamField>

<ParamField body="template_id" type="string">
  纪要模板ID，空表示用应用设置的默认模板
</ParamField>


请求示例：

```json
{
  "meeting_id": "",
  "session_id": "",
  "template_id": ""
}
```

**响应参数**

`data` 为 null

响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

