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

## 踢出授权用户

`POST /server/v1/user-auth/kickout`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

踢出登录用户

**请求参数**

<ParamField body="user_id" type="string" required>
  第三方用户ID
</ParamField>

<ParamField body="device_type" type="integer">
  设备类型
</ParamField>


请求示例：

```json
{
  "device_type": 0,
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

