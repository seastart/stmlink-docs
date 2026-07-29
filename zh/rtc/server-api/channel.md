---
title: "频道"
description: "频道的创建、查询、成员管理与历史记录"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 设置回调

`POST /server/v1/channel/set-callback`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

注册回调地址，RTC 侧在频道/用户状态变化时通知你的业务后端。
所有事件皆可不订阅，未订阅的事件不会推送。

完整的事件清单、每个事件的字段结构，以及回调必须怎么应答，见「回调事件接入指南」。

**请求参数**

<ParamField body="scene" type="string">
  应用场景(外部业务调用时不需要此参数)
</ParamField>

<ParamField body="events" type="array<string>">
  监听事件列表，取值见「回调事件接入指南」
  示例：`["user_join","user_leave","channel_destroy"]`
</ParamField>

<ParamField body="cb_url" type="string">
  回调地址，需可公网访问
  示例：`https://your-domain.com/server/v1/callback/rtc`
</ParamField>


请求示例：

```json
{
  "cb_url": "https://your-domain.com/server/v1/callback/rtc",
  "events": [
    "user_join",
    "user_leave",
    "channel_destroy"
  ],
  "scene": ""
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

## 获取加入频道token

`POST /server/v1/channel/grant`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

接入 RTC 的第一个接口。典型时序：业务后端确认用户有权进入某个频道 → 调本接口拿到
token 与 sid → 把 token 下发给客户端，客户端用它调 SDK 的 joinChannel。

token 与 channel+uid 绑定且有有效期，不要缓存复用，每次入会都重新获取。
频道无需预先创建，第一个人成功加入时自动打开。

+ 同一个 uid 重复获取 token 会得到新的 sid；若该 uid 已在会中，新会话会把旧会话顶下线
+ is_audience 为 true 的用户只收流、不广播，也不出现在默认的成员列表里（需要 with_audience 才能查到）

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）（最大长度 100）
  示例：`1001`
</ParamField>

<ParamField body="name" type="string" required>
  会中昵称（最大长度 100）
  示例：`张三`
</ParamField>

<ParamField body="props" type="object">
  用户扩展属性
  示例：`{"avatar":"https://cdn.example.com/avatar/1001.png"}`
</ParamField>

<ParamField body="is_audience" type="boolean">
  是否观众，类似研讨会观众，只收流，不参与互动，不广播
</ParamField>

<ParamField body="net" type="string">
  线路，取值是中文线路名，由部署的网络配置决定；留空则由服务端选择
  示例：`内网`
</ParamField>

<ParamField body="sg" type="string">
  服务分组
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "is_audience": false,
  "name": "张三",
  "net": "内网",
  "props": {
    "avatar": "https://cdn.example.com/avatar/1001.png"
  },
  "sg": "",
  "uid": "1001"
}
```

**响应参数**

<ResponseField name="sid" type="string">
  本次会话 ID，由服务端生成，用于按会话维度查询与对账
</ResponseField>

<ResponseField name="token" type="string">
  入会凭证，下发给客户端调用 SDK 的 joinChannel
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "sid": "",
    "token": ""
  }
}
```

---

## 获取频道详情

`POST /server/v1/channel/detail`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询单个频道的当前状态与扩展属性。只能查到已打开的频道 —— 频道未打开或已销毁时
返回空，需要历史信息请用「频道记录」。

响应里的 max_user / max_audio / max_peer / max_video 是流媒体侧的容量参数，
由应用配置决定，一般不需要业务侧关心。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "channel": "fire"
}
```

**响应参数**

<ResponseField name="app_id" type="string">
  应用id
</ResponseField>

<ResponseField name="channel" type="string">
  频道名
</ResponseField>

<ResponseField name="stream_vendor" type="string">
  流媒体供应商
</ResponseField>

<ResponseField name="props" type="object">
  频道扩展属性
</ResponseField>

<ResponseField name="created_at" type="integer">
  频道创建时间
</ResponseField>

<ResponseField name="updated_at" type="integer">
</ResponseField>

<ResponseField name="link_id" type="integer">
  流媒体连接id
</ResponseField>

<ResponseField name="max_user" type="integer">
  房间最大人数，含义参考：https://www.yuque.com/anyconf/czwlh6/prtk0l4s8ylf7mk3
</ResponseField>

<ResponseField name="max_audio" type="integer">
  房间最大参与音频能量竞争路数（针对整个房间设置）
</ResponseField>

<ResponseField name="max_peer" type="integer">
  单人最大转发的人数（音频、视频路数）（针对单人设置）
</ResponseField>

<ResponseField name="max_video" type="integer">
  单人非主动pick模式下最大转发视频路数（针对单人设置，目前我们视频都是主动pick，所以这个设置没有意义）
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "app_id": "",
    "channel": "",
    "created_at": 0,
    "link_id": 0,
    "max_audio": 0,
    "max_peer": 0,
    "max_user": 0,
    "max_video": 0,
    "props": {},
    "stream_vendor": "",
    "updated_at": 0
  }
}
```

---

## 获取频道用户详情

`POST /server/v1/channel/user-detail`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询频道内单个成员的实时状态，包括他当前发布的流轨道（stream_tracks）。

同一个 uid 多端在线时，返回的是其中一个会话；需要区分具体设备请用
「在线/离线成员列表」按 sid 取。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "uid": "1001"
}
```

**响应参数**

<ResponseField name="app_id" type="string">
  应用id
</ResponseField>

<ResponseField name="uid" type="string">
  用户id
</ResponseField>

<ResponseField name="name" type="string">
  会中昵称
</ResponseField>

<ResponseField name="device_type" type="integer">
  设备类型
</ResponseField>

<ResponseField name="device_id" type="string">
  设备ID
</ResponseField>

<ResponseField name="version" type="string">
  客户端RTCsdk版本号
</ResponseField>

<ResponseField name="props" type="object">
  用户扩展属性
</ResponseField>

<ResponseField name="net" type="string">
  线路号
</ResponseField>

<ResponseField name="sg" type="string">
  服务器分组id
</ResponseField>

<ResponseField name="updated_at" type="integer">
</ResponseField>

<ResponseField name="channel" type="string">
  频道名
</ResponseField>

<ResponseField name="sid" type="string">
  会话id
</ResponseField>

<ResponseField name="is_audience" type="boolean">
  是否观众，类似研讨会观众，只收流
</ResponseField>

<ResponseField name="join_at" type="integer">
  进入时间
</ResponseField>

<ResponseField name="leave_at" type="integer">
  退出时间
</ResponseField>

<ResponseField name="stream_tracks" type="array<object>">
  流轨道
  <Expandable title="元素字段">
    <ResponseField name="id" type="string">
      轨道id，在stream里唯一，在全局不一定唯一
    </ResponseField>

    <ResponseField name="desc" type="string">
      自定义描述，如摄像头大流、摄像头小流、共享桌面流等
    </ResponseField>

    <ResponseField name="kind" type="string">
      轨道类型
    </ResponseField>

    <ResponseField name="codec" type="integer">
      编码类型
    </ResponseField>

    <ResponseField name="width" type="integer">
      视频宽
    </ResponseField>

    <ResponseField name="height" type="integer">
      视频高
    </ResponseField>

    <ResponseField name="fps" type="integer">
      视频帧率
    </ResponseField>

    <ResponseField name="angle" type="integer">
      视频角度
    </ResponseField>

    <ResponseField name="bitrate" type="integer">
      码率
    </ResponseField>

    <ResponseField name="sample_rate" type="integer">
      音频采样率
    </ResponseField>

    <ResponseField name="channel_count" type="integer">
      音频声道数
    </ResponseField>

    <ResponseField name="fallback_ids" type="array<string>">
      FallbackIDs simulcast 降级候选层 id 列表，按画质从高到低排列；仅"自己之下的更低层"，不含自己
    </ResponseField>

    <ResponseField name="variant" type="boolean">
      Variant 是否为 simulcast 副层。仅副层为 true，主层不写 (nil/false)
    </ResponseField>

    <ResponseField name="props" type="object">
      流扩展属性
    </ResponseField>

    <ResponseField name="track" type="integer">
      轨道号
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="link_id" type="integer">
  流媒体连接id
</ResponseField>

<ResponseField name="upload_srv" type="string">
  流媒体服务
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "app_id": "",
    "channel": "",
    "device_id": "",
    "device_type": 0,
    "is_audience": false,
    "join_at": 0,
    "leave_at": 0,
    "link_id": 0,
    "name": "",
    "net": "",
    "props": {},
    "sg": "",
    "sid": "",
    "stream_tracks": [
      {
        "angle": 0,
        "bitrate": 0,
        "channel_count": 0,
        "codec": 0,
        "desc": "",
        "fallback_ids": [
          ""
        ],
        "fps": 0,
        "height": 0,
        "id": "",
        "kind": "",
        "props": {},
        "sample_rate": 0,
        "track": 0,
        "variant": false,
        "width": 0
      }
    ],
    "uid": "",
    "updated_at": 0,
    "upload_srv": "",
    "version": ""
  }
}
```

---

## 在线频道列表

`POST /server/v1/channel/list`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页列出当前已打开的频道。频道在第一个用户加入时自动打开，最后一人离开 2 小时后
自动销毁，因此这里只反映当下的活跃情况；要查历史请用「频道记录」。

**请求参数**

<ParamField body="with_detail" type="boolean">
  是否包括详情。false 时只返回频道名等基础字段，可显著降低响应体积；需要扩展属性与流媒体参数时再置 true
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
  "page": 1,
  "per-page": 10,
  "with_detail": false
}
```

**响应参数**

<ResponseField name="app_id" type="string">
  应用id
</ResponseField>

<ResponseField name="channel" type="string">
  频道名
</ResponseField>

<ResponseField name="stream_vendor" type="string">
  流媒体供应商
</ResponseField>

<ResponseField name="props" type="object">
  频道扩展属性
</ResponseField>

<ResponseField name="created_at" type="integer">
  频道创建时间
</ResponseField>

<ResponseField name="updated_at" type="integer">
</ResponseField>

<ResponseField name="link_id" type="integer">
  流媒体连接id
</ResponseField>

<ResponseField name="max_user" type="integer">
  房间最大人数，含义参考：https://www.yuque.com/anyconf/czwlh6/prtk0l4s8ylf7mk3
</ResponseField>

<ResponseField name="max_audio" type="integer">
  房间最大参与音频能量竞争路数（针对整个房间设置）
</ResponseField>

<ResponseField name="max_peer" type="integer">
  单人最大转发的人数（音频、视频路数）（针对单人设置）
</ResponseField>

<ResponseField name="max_video" type="integer">
  单人非主动pick模式下最大转发视频路数（针对单人设置，目前我们视频都是主动pick，所以这个设置没有意义）
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
      "channel": "",
      "created_at": 0,
      "link_id": 0,
      "max_audio": 0,
      "max_peer": 0,
      "max_user": 0,
      "max_video": 0,
      "props": {},
      "stream_vendor": "",
      "updated_at": 0
    }
  ]
}
```

---

## 在线/离线成员列表

`POST /server/v1/channel/list-user`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

分页列出频道成员。同一个 uid 从多个端进入会有多条记录，用 sid 区分不同会话。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="offline" type="boolean">
  获取在线还是离线成员列表。false(默认)返回当前在线的成员，true 返回已离开的成员
</ParamField>

<ParamField body="with_audience" type="boolean">
  是否包括隐身观众。观众默认不返回，需要显式传 true
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
  "channel": "fire",
  "offline": false,
  "page": 1,
  "per-page": 10,
  "with_audience": false
}
```

**响应参数**

<ResponseField name="app_id" type="string">
  应用id
</ResponseField>

<ResponseField name="uid" type="string">
  用户id
</ResponseField>

<ResponseField name="name" type="string">
  会中昵称
</ResponseField>

<ResponseField name="device_type" type="integer">
  设备类型
</ResponseField>

<ResponseField name="device_id" type="string">
  设备ID
</ResponseField>

<ResponseField name="version" type="string">
  客户端RTCsdk版本号
</ResponseField>

<ResponseField name="props" type="object">
  用户扩展属性
</ResponseField>

<ResponseField name="net" type="string">
  线路号
</ResponseField>

<ResponseField name="sg" type="string">
  服务器分组id
</ResponseField>

<ResponseField name="updated_at" type="integer">
</ResponseField>

<ResponseField name="channel" type="string">
  频道名
</ResponseField>

<ResponseField name="sid" type="string">
  会话id
</ResponseField>

<ResponseField name="is_audience" type="boolean">
  是否观众，类似研讨会观众，只收流
</ResponseField>

<ResponseField name="join_at" type="integer">
  进入时间
</ResponseField>

<ResponseField name="leave_at" type="integer">
  退出时间
</ResponseField>

<ResponseField name="stream_tracks" type="array<object>">
  流轨道
  <Expandable title="元素字段">
    <ResponseField name="id" type="string">
      轨道id，在stream里唯一，在全局不一定唯一
    </ResponseField>

    <ResponseField name="desc" type="string">
      自定义描述，如摄像头大流、摄像头小流、共享桌面流等
    </ResponseField>

    <ResponseField name="kind" type="string">
      轨道类型
    </ResponseField>

    <ResponseField name="codec" type="integer">
      编码类型
    </ResponseField>

    <ResponseField name="width" type="integer">
      视频宽
    </ResponseField>

    <ResponseField name="height" type="integer">
      视频高
    </ResponseField>

    <ResponseField name="fps" type="integer">
      视频帧率
    </ResponseField>

    <ResponseField name="angle" type="integer">
      视频角度
    </ResponseField>

    <ResponseField name="bitrate" type="integer">
      码率
    </ResponseField>

    <ResponseField name="sample_rate" type="integer">
      音频采样率
    </ResponseField>

    <ResponseField name="channel_count" type="integer">
      音频声道数
    </ResponseField>

    <ResponseField name="fallback_ids" type="array<string>">
      FallbackIDs simulcast 降级候选层 id 列表，按画质从高到低排列；仅"自己之下的更低层"，不含自己
    </ResponseField>

    <ResponseField name="variant" type="boolean">
      Variant 是否为 simulcast 副层。仅副层为 true，主层不写 (nil/false)
    </ResponseField>

    <ResponseField name="props" type="object">
      流扩展属性
    </ResponseField>

    <ResponseField name="track" type="integer">
      轨道号
    </ResponseField>

  </Expandable>
</ResponseField>

<ResponseField name="link_id" type="integer">
  流媒体连接id
</ResponseField>

<ResponseField name="upload_srv" type="string">
  流媒体服务
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
      "channel": "",
      "device_id": "",
      "device_type": 0,
      "is_audience": false,
      "join_at": 0,
      "leave_at": 0,
      "link_id": 0,
      "name": "",
      "net": "",
      "props": {},
      "sg": "",
      "sid": "",
      "stream_tracks": [
        {
          "angle": 0,
          "bitrate": 0,
          "channel_count": 0,
          "codec": 0,
          "desc": "",
          "fallback_ids": [
            ""
          ],
          "fps": 0,
          "height": 0,
          "id": "",
          "kind": "",
          "props": {},
          "sample_rate": 0,
          "track": 0,
          "variant": false,
          "width": 0
        }
      ],
      "uid": "",
      "updated_at": 0,
      "upload_srv": "",
      "version": ""
    }
  ]
}
```

---

## 在线/离线成员Uids

`POST /server/v1/channel/list-uids`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

与「在线/离线成员列表」的筛选条件完全一致，但只返回 uid 字符串数组，不含成员详情。

适合只需要判断"谁在会中"的场景（如权限校验、名单比对），响应体积比完整列表小一个数量级。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="offline" type="boolean">
  获取在线还是离线成员列表。false(默认)返回当前在线的成员，true 返回已离开的成员
</ParamField>

<ParamField body="with_audience" type="boolean">
  是否包括隐身观众。观众默认不返回，需要显式传 true
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
  "channel": "fire",
  "offline": false,
  "page": 1,
  "per-page": 10,
  "with_audience": false
}
```

**响应参数**

<ResponseField name="data" type="array<string>">
  返回数据
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
    ""
  ]
}
```

---

## 变更频道信息

`POST /server/v1/channel/update`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

更新频道的扩展属性。频道必须已打开，否则更新无效。
变更会通过信令同步给会中所有客户端。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="props" type="object">
  频道扩展属性。整体替换语义，不是字段级合并 —— 需要保留的字段请一并传入
  示例：`{"watermark_disabled":true}`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "props": {
    "watermark_disabled": true
  }
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

## 变更用户信息

`POST /server/v1/channel/update-user`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

更新会中成员的昵称、扩展属性或观众身份。变更会同步给会中其他成员。
把已在会中的成员改成观众会让他退化为只收流，其已发布的流轨道会被停止。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  用户id（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="name" type="string">
  会中昵称，不传表示不改
  示例：`张三`
</ParamField>

<ParamField body="props" type="object">
  用户扩展属性，整体替换语义
  示例：`{"avatar":"https://cdn.example.com/avatar/1001.png"}`
</ParamField>

<ParamField body="is_audience" type="boolean">
  是否观众，类似研讨会观众，只收流
</ParamField>

<ParamField body="stream_tracks" type="array<object>">
  流轨道
  <Expandable title="元素字段">
    <ParamField body="id" type="string">
      轨道id，在stream里唯一，在全局不一定唯一
    </ParamField>

    <ParamField body="desc" type="string">
      自定义描述，如摄像头大流、摄像头小流、共享桌面流等
    </ParamField>

    <ParamField body="kind" type="string">
      轨道类型
    </ParamField>

    <ParamField body="codec" type="integer">
      编码类型
    </ParamField>

    <ParamField body="width" type="integer">
      视频宽
    </ParamField>

    <ParamField body="height" type="integer">
      视频高
    </ParamField>

    <ParamField body="fps" type="integer">
      视频帧率
    </ParamField>

    <ParamField body="angle" type="integer">
      视频角度
    </ParamField>

    <ParamField body="bitrate" type="integer">
      码率
    </ParamField>

    <ParamField body="sample_rate" type="integer">
      音频采样率
    </ParamField>

    <ParamField body="channel_count" type="integer">
      音频声道数
    </ParamField>

    <ParamField body="fallback_ids" type="array<string>">
      FallbackIDs simulcast 降级候选层 id 列表，按画质从高到低排列；仅"自己之下的更低层"，不含自己
    </ParamField>

    <ParamField body="variant" type="boolean">
      Variant 是否为 simulcast 副层。仅副层为 true，主层不写 (nil/false)
    </ParamField>

    <ParamField body="props" type="object">
      流扩展属性
    </ParamField>

    <ParamField body="track" type="integer">
      轨道号
    </ParamField>

  </Expandable>
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "is_audience": false,
  "name": "张三",
  "props": {
    "avatar": "https://cdn.example.com/avatar/1001.png"
  },
  "stream_tracks": [
    {
      "angle": 0,
      "bitrate": 0,
      "channel_count": 0,
      "codec": 0,
      "desc": "",
      "fallback_ids": [
        ""
      ],
      "fps": 0,
      "height": 0,
      "id": "",
      "kind": "",
      "props": {},
      "sample_rate": 0,
      "track": 0,
      "variant": false,
      "width": 0
    }
  ],
  "uid": "1001"
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

## 发送自定义消息

`POST /server/v1/channel/send-custom-msg`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

通过信令通道向频道内广播一条自定义消息，客户端 SDK 会以事件形式收到。
适合做聊天、举手、投票这类轻量业务信令，不适合传大数据或高频消息。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="action" type="string" required>
  消息命令，由你自定义，客户端按它分发处理
  示例：`chat`
</ParamField>

<ParamField body="content" type="any">
  消息体，任意 JSON，结构由你定
  示例：`&#123;"text": "i love srtc"&#125;`
</ParamField>

<ParamField body="uid" type="string">
  发送者ID，用于客户端展示"谁发来的"；服务端下发的系统消息可留空（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="name" type="string">
  发送者昵称
  示例：`张三`
</ParamField>

<ParamField body="ruids" type="array<string>">
  接收者ID列表(空时给全频道发)
  示例：`["1002","1003"]`
</ParamField>

<ParamField body="important" type="boolean">
  是否重要，重要消息在断线重连后会重发确保收到，代价是延迟略高
</ParamField>


请求示例：

```json
{
  "action": "chat",
  "channel": "fire",
  "content": "{\"text\": \"i love srtc\"}",
  "important": false,
  "name": "张三",
  "ruids": [
    "1002",
    "1003"
  ],
  "uid": "1001"
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

## 踢人

`POST /server/v1/channel/kick-user`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

把指定成员踢出频道。该成员的客户端会收到被踢事件，并触发 user_leave 回调
（reason 标识为被踢）。

踢出是一次性操作，不会拉黑 —— 被踢的 uid 重新获取 token 后仍可再次进入。
需要禁止再入请在你自己的业务侧拦截 token 发放。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "uid": "1001"
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

## 手动打开频道

`POST /server/v1/channel/open`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

默认情况下第一个用户加入频道时会自动打开频道，无需调用本接口。

只有一种场景需要它：你想在任何人进入之前就设置好频道的扩展属性（如水印开关、
业务侧的房间配置），这样第一个人进来时就能读到正确的配置，避免"先进来再改属性"
的时序问题。

频道开启后 2 小时内无人加入，或最后一个用户离开 2 小时后，会自动销毁。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="props" type="object">
  频道扩展属性
  示例：`{"watermark_disabled":true}`
</ParamField>

<ParamField body="stream_vendor" type="string">
  流媒体供应商
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "props": {
    "watermark_disabled": true
  },
  "stream_vendor": ""
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

## 销毁频道

`POST /server/v1/channel/destroy`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

立即销毁频道，会中所有人被强制退出，会触发 channel_destroy 回调。

正常情况下频道会在最后一人离开 2 小时后自动销毁，不需要手动调用。本接口用于需要
立即回收频道的场景（如会议被管理员强制结束）。频道内进行中的录制任务会一并停止。

销毁后同名频道可以重新打开，但会是一条新的频道记录。

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "channel": "fire"
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

## 频道记录

`POST /server/v1/channel/list-record`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询频道的历史开启记录。同一个频道名多次开启会有多条记录，每条对应一个完整的
生命周期（open_at → destroy_at）。响应里 destroy_at 为 0 表示该频道仍在进行中。

**请求参数**

<ParamField body="channel" type="string">
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="begin_at" type="integer">
  起始时间，秒级时间戳，按频道开启时间过滤；0 表示不限
  示例：`1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
  终止时间，秒级时间戳；0 表示不限
  示例：`1718799878`
</ParamField>

<ParamField body="sort" type="string">
  排序（可排序字段：open_at、destroy_at）
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
  "begin_at": 1718194666,
  "channel": "fire",
  "end_at": 1718799878,
  "page": 1,
  "per-page": 10,
  "sort": ""
}
```

**响应参数**

<ResponseField name="id" type="string">
</ResponseField>

<ResponseField name="app_id" type="string">
</ResponseField>

<ResponseField name="channel" type="string">
  频道
</ResponseField>

<ResponseField name="props" type="object">
  扩展属性
</ResponseField>

<ResponseField name="open_at" type="integer">
  开启时间
</ResponseField>

<ResponseField name="destroy_at" type="integer">
  销毁时间
</ResponseField>

<ResponseField name="destroy_reason" type="integer">
  销毁原因
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
      "channel": "",
      "destroy_at": 0,
      "destroy_reason": 0,
      "id": "",
      "open_at": 0,
      "props": {}
    }
  ]
}
```

---

## 出入频道记录

`POST /server/v1/channel/list-user-record`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

查询成员的进出频道记录，单人多次进入会有多条记录，用 sid 区分。
这是做时长计费、参会审计的主要数据源。

+ 响应里 leave_at 为 0 表示该成员仍在会中
+ 单次参会时长 = leave_at - join_at（秒）

**请求参数**

<ParamField body="channel" type="string" required>
  频道名（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string">
  用户id，留空表示不限（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="name" type="string">
  会中昵称，留空表示不限
  示例：`张三`
</ParamField>

<ParamField body="begin_at" type="integer">
  起始时间，秒级时间戳，按进入时间过滤；0 表示不限
  示例：`1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
  终止时间，秒级时间戳；0 表示不限
  示例：`1718799878`
</ParamField>

<ParamField body="with_audience" type="boolean">
  是否包括隐身观众
</ParamField>

<ParamField body="sort" type="string">
  排序（可排序字段：join_at、leave_at）
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
  "begin_at": 1718194666,
  "channel": "fire",
  "end_at": 1718799878,
  "name": "张三",
  "page": 1,
  "per-page": 10,
  "sort": "",
  "uid": "1001",
  "with_audience": false
}
```

**响应参数**

<ResponseField name="id" type="string">
</ResponseField>

<ResponseField name="app_id" type="string">
</ResponseField>

<ResponseField name="channel" type="string">
  频道
</ResponseField>

<ResponseField name="sid" type="string">
</ResponseField>

<ResponseField name="uid" type="string">
</ResponseField>

<ResponseField name="name" type="string">
  会中昵称
</ResponseField>

<ResponseField name="is_audience" type="boolean">
  是否观众，类似研讨会观众，只收流
</ResponseField>

<ResponseField name="device_type" type="integer">
  设备类型
</ResponseField>

<ResponseField name="device_id" type="string">
  设备ID
</ResponseField>

<ResponseField name="version" type="string">
  客户端RTCsdk版本号
</ResponseField>

<ResponseField name="props" type="object">
  扩展属性
</ResponseField>

<ResponseField name="join_at" type="integer">
  进入时间
</ResponseField>

<ResponseField name="leave_at" type="integer">
  退出时间
</ResponseField>

<ResponseField name="leave_reason" type="integer">
  退出原因
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
      "channel": "",
      "device_id": "",
      "device_type": 0,
      "id": "",
      "is_audience": false,
      "join_at": 0,
      "leave_at": 0,
      "leave_reason": 0,
      "name": "",
      "props": {},
      "sid": "",
      "uid": "",
      "version": ""
    }
  ]
}
```

---

## 查询在线人数

`POST /server/v1/channel/online-user-num`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

批量查询多个频道的当前在线人数，一次请求即可，适合列表页展示。

响应的 data 是「频道名 → 人数」的映射，如 `{"fire": 4}`；未打开或不存在的频道
不会出现在结果里（而不是返回 0），需要区分请自行对照请求的 channels。

**请求参数**

<ParamField body="channels" type="array<string>" required>
  频道名列表
  示例：`["fire","water"]`
</ParamField>

<ParamField body="with_audience" type="boolean">
  是否包括隐身观众
</ParamField>


请求示例：

```json
{
  "channels": [
    "fire",
    "water"
  ],
  "with_audience": false
}
```

**响应参数**

<ResponseField name="<键>" type="integer">
  键为动态值，见上方说明
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {}
}
```

---

## 查询频道历史参与人数

`POST /server/v1/channel/history-join-num`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

统计一个频道在指定时间范围内的历史参与规模。

+ user_num 按 uid 去重，回答"有多少人参加过"
+ user_times 不去重，回答"一共进出了多少次"

**请求参数**

<ParamField body="channel" type="string" required>
  频道名
  示例：`fire`
</ParamField>

<ParamField body="begin_at" type="integer" required>
  起始时间，秒级时间戳
  示例：`1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
  终止时间，秒级时间戳；0 表示统计到当前时刻
  示例：`1718799878`
</ParamField>

<ParamField body="with_audience" type="boolean">
  是否包括隐身观众
</ParamField>


请求示例：

```json
{
  "begin_at": 1718194666,
  "channel": "fire",
  "end_at": 1718799878,
  "with_audience": false
}
```

**响应参数**

<ResponseField name="user_num" type="integer">
  参会人数，按uid去重
  示例：`60`
</ResponseField>

<ResponseField name="user_times" type="integer">
  参会人次，同一人多次进入累计
  示例：`1935`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "user_num": 60,
    "user_times": 1935
  }
}
```

---

## 今日频道统计

`POST /server/v1/channel/today`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

你自己应用今日的频道开启次数与累计时长汇总。无请求参数 —— 统计范围由鉴权得到的
应用身份决定，只会返回属于你的数据。

只统计已销毁的频道（destroy_at 大于 0），进行中的频道不计入，因此数值会随当天推进
而增长。时区固定为东八区（Asia/Shanghai）。

**请求参数**

无

**响应参数**

<ResponseField name="time" type="integer">
  统计时刻，响应生成时的秒级时间戳
  示例：`1718250917`
</ResponseField>

<ResponseField name="num" type="integer">
  今日频道开启次数
  示例：`120`
</ResponseField>

<ResponseField name="dur" type="integer">
  今日频道累计时长(秒)
  示例：`43200`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "dur": 43200,
    "num": 120,
    "time": 1718250917
  }
}
```

---

## 频道统计（按天聚合）

`POST /server/v1/channel/stats`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

按天聚合的频道开启次数与时长，用于画趋势图。统计范围由鉴权得到的应用身份决定，
只返回你自己应用的数据。

+ 只统计已销毁的频道（destroy_at 大于 0），进行中的不计入
+ 没有数据的日期不会出现在结果里（不补零），画图时需自行填充

注意: 不接受调用方传入 app_id，应用维度一律取鉴权得到的 app_id，避免跨租户查询

**请求参数**

<ParamField body="begin_at" type="integer">
  起始时间，秒级时间戳；0 表示统计最近 31 天
  示例：`1718194666`
</ParamField>

<ParamField body="end_at" type="integer">
  终止时间，秒级时间戳；0 或超过当前时间按当前时间处理
  示例：`1718799878`
</ParamField>


请求示例：

```json
{
  "begin_at": 1718194666,
  "end_at": 1718799878
}
```

**响应参数**

<ResponseField name="day" type="string">
  日期，格式 YYYY-MM-DD
  示例：`2024-06-12`
</ResponseField>

<ResponseField name="num" type="integer">
  当日频道开启次数
  示例：`120`
</ResponseField>

<ResponseField name="dur" type="integer">
  当日频道累计时长(秒)
  示例：`43200`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "day": "2024-06-12",
      "dur": 43200,
      "num": 120
    }
  ]
}
```

---

