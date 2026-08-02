---
title: "服务端极简对接"
description: "不集成 SDK、不做会议界面，业务后端只对四个接口：同步用户、创建会议、换免登录 token、拉起会议页"
---

如果你的诉求是「把会议能力挂到既有业务流程上」——一次招投标、一场评审、一个工单派发——
而不是做一款会议产品，那么你不需要集成 SMeeting SDK，也不需要写会议界面。

会议客户端、用户体系、登录态我们都已经部署好了，你的后端只做四件事：

| 步骤 | 接口 | 服务 |
| --- | --- | --- |
| 1. 把你的用户同步过来 | `POST /stm/srvapi/v1/member/sync` | 用户体系 |
| 2. 建会议，挂上你的业务单据号 | `POST /server/v1/meet/create` | 会议服务 |
| 3. 给某个用户换一张免登录票 | `POST /stm/srvapi/v1/member/grant` | 用户体系 |
| 4. 拉起会议页 | `GET /stm/ui/outer?...` | 会议客户端 |

第 1 步在用户变动时做，第 2 步在业务活动创建时做，第 3、4 步在用户点「进入会议」时做。

<Note>
这条路径和[带 UI 极简对接](/zh/meeting/ui-sdk/web)的区别：那边是你拿走前端源码自己改界面、
自己部署；这边是连界面都用我们部署好的，你只在服务端拼一个 URL。
</Note>

## 两组基地址

对接会用到两个前缀，域名相同：

```
https://<你的域名>/server/v1/...        会议服务（建会、会控、录制）
https://<你的域名>/stm/srvapi/v1/...    用户体系（同步、授权）
```

两者的**鉴权方式完全一致**——`app_id` / `nonce` / `timestamp` / `signature` 四个请求头，
HMAC-SHA256 签名，算法见[服务端 API 概览](/zh/meeting/server-api/overview)。
两者用的 `app_key` 是否为同一把，以我们交付给你的配置为准。

<Warning>
`app_key` 只能待在你的后端。上面四步里，只有第 4 步的 URL 会到达浏览器，
它携带的是一次性的用户票据，不是密钥。
</Warning>

## 第 1 步：同步用户

```
POST /stm/srvapi/v1/member/sync
```

请求体是一个**数组**，单次不超过 1000 条：

```json
[
  {
    "account": "310101199001011234",
    "nickname": "张三",
    "real_name": "张三",
    "department": "招标一部",
    "role": 1
  }
]
```

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `account` | 是 | 用户在**你的系统**里的唯一标识，工号、身份证号、手机号都行 |
| `nickname` | 是 | 会中显示的名字 |
| `real_name` | 否 | 真实姓名，留空则取 `nickname` |
| `department` | 否 | 组织名称 |
| `role` | 否 | `1` 普通用户、`2` 管理员，传 `0` 或不传按 `1` 处理 |
| `password_hash` / `salt` | 否 | 只有当用户还需要用账号密码登录会议页时才传 |

返回按 `account` 分成成功与失败两张表：

```json
{
  "success": { "310101199001011234": "01hq8x7k2m" },
  "fail": { "310101199001011299": "..." }
}
```

`success` 的值是我们侧的用户 ID，可以存下来，但后续接口用 `account` 就够了。

<Warning>
**`account` 一旦同步就不要再改。** 它是认人的唯一依据，改了等于新建了一个用户，
原来的参会记录不会跟过来。
</Warning>

重复同步同一个 `account` 是更新而不是新建，所以全量推和增量推都行。同一时刻只允许一个
同步任务在跑，并发调用会收到「频率过快 请稍候」。

### 组织结构的能力边界

`department` 是一个**平铺的字符串**，不是层级。多级部门树目前只能在管理后台用 Excel
导入（最多四级、单次 500 行），**没有对应的 API**。

所以如果你只是想让参会人看到「张三（招标一部）」，`department` 够用；如果你要把整棵
组织树同步过来供用户在通讯录里逐级点选，当前这条路径做不到，需要单独提。

## 第 2 步：创建会议

```
POST /server/v1/meet/create
```

完整参数见[会议管理](/zh/meeting/server-api/meet#创建会议)，这里只说极简对接关心的几个：

```json
{
  "title": "XX 项目开标会",
  "meeting_type": 2,
  "plan_time": 1718250917,
  "plan_dur": 120,
  "attend_type": 3,
  "conferee_details": [
    { "account": "310101199001011234", "real_name": "张三", "role": 1 }
  ],
  "extend_info": { "bid_no": "ZB-2026-0731", "biz_type": "kaibiao" }
}
```

+ **`extend_info`** 是挂业务单据的地方。它是一个自由结构的对象，我们只存储和回传，
  把招投标编号放进去，后面收到回调时就能反查到自己的业务
+ **`conferee_details`** 用第 1 步的 `account` 指定参会白名单，配合 `attend_type: 3`
  （邀请人员参会）就能挡住无关的人
+ **`meeting_type`**：`1` 即时会议、`2` 预约会议。预约会议必须给 `plan_time` 和 `plan_dur`
+ 要自动录像就加 `auto_record: true`，不用在业务里管录制启停，详见
  [云录制与直播接入指南](/zh/meeting/server-api/guides/recording)

返回里的 **`room_no`** 是第 4 步要用的房间号，`meeting_id` 是后续所有会议接口的入参：

```json
{ "meeting_id": "sny038", "room_no": "803707296" }
```

<Warning>
**不要用 `attend_type` 为 `2` 或 `4` 的密码会议。** 第 4 步的拉起地址不支持传密码，
用户落到会议页后还得手动输一次，极简对接的意义就没了。用 `1`（无限制）或
`3`（邀请人员参会）。
</Warning>

## 第 3 步：换免登录票

用户在你的系统里点「进入会议」时，后端实时调一次：

```
POST /stm/srvapi/v1/member/grant
```

```json
{ "uid": "310101199001011234" }
```

<Note>
字段名是 `uid`，但值填的是第 1 步的 **`account`**，不是 `success` 里返回的用户 ID。
这是历史命名，改了会破坏已对接的客户，所以保留。
</Note>

返回值直接就是一个 token 字符串：

```json
{ "code": 0, "data": "eyJhbGciOiJIUzI1NiIs..." }
```

有效期 7 天。**建议每次拉起前重新签发**，不要缓存下来复用——它等价于这个用户的登录态。

## 第 4 步：拉起会议页

把 token 和房间号拼成地址，让用户的浏览器打开它：

```
https://<你的域名>/stm/ui/outer?token=<第3步的token>&room_no=<第2步的room_no>&nickname=<会中昵称>
```

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `token` | 是 | 第 3 步签发的票据 |
| `room_no` | 否 | 省略则落到会议列表首页，让用户自己选 |
| `nickname` | 否 | 覆盖同步时的昵称，用于「张三（甲方代表）」这类临时身份 |

`nickname` 里如果有中文或特殊字符，记得做 URL 编码。

进入会议时**麦克风与摄像头默认关闭**，由用户自己在会中打开。

## 完整时序

```
业务活动创建时
  ├─ POST /stm/srvapi/v1/member/sync    同步这次活动涉及的人（可提前批量做）
  └─ POST /server/v1/meet/create        extend_info 挂单据号 → 存下 room_no

用户点「进入会议」
  ├─ POST /stm/srvapi/v1/member/grant   {"uid": "<account>"} → token
  └─ 302 到 /stm/ui/outer?token=&room_no=&nickname=

会议过程中（可选）
  ├─ 订阅回调事件                        进出会、录制完成，见回调事件接入指南
  └─ POST /stm/srvapi/v1/member/info    查谁在线

活动结束后（可选）
  └─ POST /server/v1/mcu/vods-url       取回放，等 mcu_record_done 回调之后
```

回调怎么接、怎么验签见[回调事件接入指南](/zh/meeting/server-api/guides/callbacks)。
`meeting_id` 会随事件回传，用它反查你在 `extend_info` 里存的单据号。

## 两个可选接口

**查用户与在线状态** —— `POST /stm/srvapi/v1/member/info`

```json
{ "accounts": ["310101199001011234"] }
```

返回里带 `is_online`，可以在你的界面上显示「张三 在线」。也可以用 `uids` 按我们侧的
用户 ID 查。

**清理离职用户** —— `POST /stm/srvapi/v1/member/remove`

入参同上。删除后该用户无法再换票进会。

## 什么时候该改用完整 SDK

这条路径的代价是**界面不是你的**。出现下面任何一条，就该考虑集成 SMeeting SDK：

+ 会议界面要用你自己的品牌、布局或交互
+ 会议要嵌在你的 App 内部，而不是跳出去一个网页
+ 需要在会中做业务联动，比如开标环节到点自动解除全员静音

各端的集成方式见左侧「iOS SDK」「Android SDK」等分组。两条路径的服务端接口是同一套，
先用极简对接跑通业务流程、之后再换 SDK 做界面，前面的对接不会白做。
