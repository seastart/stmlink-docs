---
title: "会议授权"
description: "把业务系统的用户换成会议 Token，以及把已授权的用户踢下线"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 meeting-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 获取会议授权

`POST /server/v1/user-auth/grant`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

获取授权

**请求参数**

<ParamField body="user_id" type="string" required>
  第三方用户ID（最大长度 100）
</ParamField>

<ParamField body="nickname" type="string">
  昵称（最大长度 100）
</ParamField>

<ParamField body="net" type="string">
  线路
</ParamField>

<ParamField body="sg" type="string">
  服务分组
</ParamField>


请求示例：

```json
{
  "net": "",
  "nickname": "",
  "sg": "",
  "user_id": ""
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

## 下线登录用户

`POST /server/v1/user-auth/kickout`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

让用户的登录态（meet_token 换来的会话）立即失效，下次调接口就要重新授权。

注意这个接口**不会把人从正在进行的会议里踢出去**，被下线的人还在会中，
直到心跳超时才掉线（`user_exit` 回调的 `reason` 为 4）。
要立刻把人踢出会议，用[会中控制](/zh/meeting/server-api/meet-admin)里的「主持人踢人」。

+ 不传 device_type：该用户所有端一起下线
+ 传了 device_type：只下线这一端，其它端不受影响
+ 该用户当前没有有效登录态时会报错

**请求参数**

<ParamField body="user_id" type="string" required>
  第三方用户ID
</ParamField>

<ParamField body="device_type" type="integer">
  只下线该端的登录态 0未知设备 1Windows 2Android 3iOS 4Linux 5MacOS 6WebRTC 7微信小程序；不传则该用户所有端一起下线
  示例：`3`
</ParamField>


请求示例：

```json
{
  "device_type": 3,
  "user_id": ""
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

