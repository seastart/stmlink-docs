---
title: "用户同步"
description: "把业务系统的用户同步进我们部署的会议用户体系，以及换免登录 token、查在线状态、删除用户；服务端极简对接与通讯录场景使用，接口前缀为 /stm/srvapi/v1"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 meeting-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 批量同步用户

`POST /stm/srvapi/v1/member/sync`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

把你系统里的用户批量推过来，供会议客户端的通讯录、按人员列表挑人入会使用。
只用「换免登录 token」进会的话不需要先同步：那个接口带上昵称时会现场建人。

单次最多 1000 条。按 user_id 认人：库里没有就新建，已有就更新——全量推、增量推都行。
已有用户的 nickname、real_name、department 每次都以本次传的为准（department 不传会被清空），
avatar、mobile、password_hash / salt、camera_disabled / share_disabled 不传则保持原值。

同一应用同一时刻只允许一个同步在跑，并发调用会收到「频率过快 请稍候」，等上一批返回后再推下一批。
某一条写库失败不影响其它条，结果按 user_id 分进 success / fail 两张表。

**请求参数**

请求体是一个 **JSON 数组**，下面是每个元素的字段。

<ParamField body="user_id" type="string" required>
  用户ID，即你系统里的用户唯一标识（最大长度 100）
</ParamField>

<ParamField body="nickname" type="string" required>
  会中显示的名字（最大长度 100）
  示例：`张三`
</ParamField>

<ParamField body="real_name" type="string">
  真实姓名，留空取 nickname（最大长度 100）
</ParamField>

<ParamField body="avatar" type="string">
  留空表示不改，不会清掉已有头像（最大长度 300）
</ParamField>

<ParamField body="mobile" type="string">
  手机号。纯展示用，不参与认人——认人只认 user_id。 留空表示不改，不会清掉已有值（最大长度 100）
</ParamField>

<ParamField body="password_hash" type="string">
  只有用户还要用账号密码登录会议页时才传：sha256(密码 + salt) 的小写十六进制， 与 salt 成对传；不传表示不改（最大长度 100）
</ParamField>

<ParamField body="salt" type="string">
  计算 password_hash 用的盐，可为空（最大长度 100）
</ParamField>

<ParamField body="department" type="string">
  组织名称，平铺的字符串而非层级（最大长度 100）
  示例：`招标一部`
</ParamField>

<ParamField body="camera_disabled" type="boolean">
  禁止开摄像头
</ParamField>

<ParamField body="share_disabled" type="boolean">
  禁止共享（屏幕与白板）
</ParamField>


请求示例：

```json
[
  {
    "avatar": "",
    "camera_disabled": false,
    "department": "招标一部",
    "mobile": "",
    "nickname": "张三",
    "password_hash": "",
    "real_name": "",
    "salt": "",
    "share_disabled": false,
    "user_id": ""
  }
]
```

**响应参数**

<ResponseField name="success" type="object">
  成功的用户，键与值都是你传的 user_id
</ResponseField>

<ResponseField name="fail" type="object">
  失败的用户，键是 user_id，值是失败原因
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "fail": {},
    "success": {}
  }
}
```

---

## 换免登录 token

`POST /stm/srvapi/v1/member/grant`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

用户点「进入会议」时实时调用，换一个免登录 token，拼进会议页地址即可免登录进会。
data 直接就是 token 字符串。

带上 nickname 等资料时，用户不存在就现场建、已存在就顺带更新，所以不必先调「批量同步用户」，
每次把最新的昵称、头像带上即可。只传 user_id 而这个人从没同步过时会报错——没有昵称，
建出来在会中没有名字。

**请求参数**

<ParamField body="user_id" type="string" required>
  用户ID，同 member/sync 的 user_id（最大长度 100）
</ParamField>

<ParamField body="nickname" type="string">
  会中昵称（最大长度 100）
</ParamField>

<ParamField body="real_name" type="string">
  真实姓名，留空取 nickname（最大长度 100）
</ParamField>

<ParamField body="avatar" type="string">
  头像地址，留空表示不改（最大长度 300）
</ParamField>

<ParamField body="mobile" type="string">
  手机号。纯展示用，不参与认人——认人只认 user_id。留空表示不改（最大长度 100）
</ParamField>

<ParamField body="camera_disabled" type="boolean">
  禁止开摄像头
</ParamField>

<ParamField body="share_disabled" type="boolean">
  禁止共享（屏幕与白板）
</ParamField>


请求示例：

```json
{
  "avatar": "",
  "camera_disabled": false,
  "mobile": "",
  "nickname": "",
  "real_name": "",
  "share_disabled": false,
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

## 查询用户与在线状态

`POST /stm/srvapi/v1/member/info`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

按 user_id 批量查询已同步的用户资料，返回里带 is_online，可用来在你的界面上显示在线状态。
不存在的 user_id 不会出现在返回里。

**请求参数**

<ParamField body="user_ids" type="array<string>">
  用户ID列表，即同步时传的 user_id
</ParamField>


请求示例：

```json
{
  "user_ids": [
    ""
  ]
}
```

**响应参数**

<ResponseField name="user_id" type="string">
  用户ID
</ResponseField>

<ResponseField name="mobile" type="string">
  手机号
</ResponseField>

<ResponseField name="nickname" type="string">
  昵称
</ResponseField>

<ResponseField name="real_name" type="string">
  真实姓名
</ResponseField>

<ResponseField name="avatar" type="string">
  头像
</ResponseField>

<ResponseField name="is_online" type="boolean">
  是否在线
</ResponseField>

<ResponseField name="created_at" type="integer">
  创建时间，Unix 秒
</ResponseField>

<ResponseField name="camera_disabled" type="boolean">
  禁止开摄像头
</ResponseField>

<ResponseField name="share_disabled" type="boolean">
  禁止共享
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "avatar": "",
      "camera_disabled": false,
      "created_at": 0,
      "is_online": false,
      "mobile": "",
      "nickname": "",
      "real_name": "",
      "share_disabled": false,
      "user_id": ""
    }
  ]
}
```

---

## 删除用户

`POST /stm/srvapi/v1/member/remove`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

按 user_id 批量删除用户（如员工离职）。删除后该用户无法再换 token 进会；
不存在的 user_id 直接忽略。

**请求参数**

<ParamField body="user_ids" type="array<string>">
  用户ID列表，即同步时传的 user_id
</ParamField>


请求示例：

```json
{
  "user_ids": [
    ""
  ]
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

