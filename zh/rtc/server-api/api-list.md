---
title: "接口列表"
description: "服务端 API 完整接口列表"
---

**完整api接口列表请参考：**

[https://doc.apipost.net/docs/detail/3ca3c5a4a003000?target_id=51c6eda](https://doc.apipost.net/docs/detail/3ca3c5a4a003000?target_id=51c6eda)

## 获取加入频道token
**接口URL**

> /server/v1/channel/grant
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1",
    "name": "shu",
    "props": {
        "avatar": "https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png"
    },
    "is_audience": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名，长度64以内，支持包括大小写英文字母(a-zA-Z)、数字(0-9)及下划线_和连词符- |
| uid | 1 | String | 是 | 第三方用户ID，长度150以内，支持包括大小写英文字母(a-zA-Z)、数字(0-9)及下划线_和连词符- |
| name | shu | String | 是 | 频道中昵称 |
| props | `{"avatar": "https://xx.com/a.png"}` | Object | 否 | 用户扩展属性 |
| is_audience | false | Boolean | 否 | 是否观众，类似研讨会观众，只收流，不参与互动，不广播 |
| net | 内网 | String | 否 | 网络(内网、外网) |
| sg |  | String | 否 | 服务分组 |


**响应示例**

成功（200）

```javascript
{
	"code": 0,
	"data": {
		"sid": "acee",
		"token": "wvYKytpMTsR2OK82ghVj1ZFAVCEtfMugr5PwFRjKzIm3b32plqC9Fyuwc2Bj+3qv5Ors0UmQQNTXAw4MRV9hxQ054Ytastm7kpsdyrt0Vq068Mz+UgSnR7L+PUCdOmg8ZjfCS4zzNNDnrnUongo/k0zr1MWMaaiE0TFJhgOodZ8Ml/segpAGzze7rh3lkvPvK/BlAVX5a297DmVjxR9RPlfxC1bZWc03cSMrp8XEc0wAE7BhEYXHPW5sIlMI4+Q767UMmMHOwvM0Ozab13RFqx95IwVpcSIa47Cw5ktlP5c="
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |
| data.token | wvYKytpMTsR2OK82ghVj1ZFAVCEtfMugr5PwFRjKzIm3b32plqC9Fyuwc2Bj+3qv5Ors0UmQQNTXAw4MRV9hxQ054Ytastm7kpsdyrt0Vq068Mz+UgSnR7L+PUCdOmg8ZjfCS4zzNNDnrnUongo/k0zr1MWMaaiE0TFJhgOodZ8Ml/segpAGzze7rh3lkvPvK/BlAVX5a297DmVjxR9RPlfxC1bZWc03cSMrp8XEc0wAE7BhEYXHPW5sIlMI4+Q767UMmMHOwvM0Ozab13RFqx95IwVpcSIa47Cw5ktlP5c= | String | token |


## 在线频道列表
**接口URL**

> /server/v1/channel/list
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "per-page": 10,
    "page": 1
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| per-page | 10 | Integer | 否 | - |
| page | 1 | Integer | 否 | - |


**响应示例**

成功（200）

```javascript
{
    "code": 0,
    "data": [
        {
            "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
            "channel": "fire",
            "props": null,
            "created_at": 1718250917,
            "updated_at": 1718250921,
            "link_id": 100000036,
            "max_user": 1024,
            "max_audio": 0,
            "max_peer": 32,
            "max_video": 16
        }
    ],
    "_meta": {
        "totalCount": 1,
        "pageCount": 1,
        "currentPage": 1,
        "perPage": 10
    }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |
| data | - | Array | - |
| data.app_id | - | String | - |
| data.channel | - | String | 频道名 |
| data.props | null | Null | 频道扩展属性 |
| data.created_at | 1718250917 | Integer | - |
| data.updated_at | 1718250921 | Integer | - |
| data.link_id | 100000036 | Integer | - |
| data.max_user | 1024 | Integer | - |
| data.max_audio | 0 | Integer | - |
| data.max_peer | 32 | Integer | - |
| data.max_video | 16 | Integer | - |
| _meta | - | Object | - |
| _meta.totalCount | 1 | Integer | - |
| _meta.pageCount | 1 | Integer | - |
| _meta.currentPage | 1 | Integer | - |
| _meta.perPage | 10 | Integer | - |


## 可选：手动打开频道
**说明：**

默认情况下，第一个用户加入频道时会自动打开频道。  

如需要提前设置一些频道扩展属性，可手动调用此接口先开启频道。  

频道开启后2小时内无人加入，或最后一个用户离开频道2小时后，会自动销毁

**接口URL**

> /server/v1/channel/open
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "props": {
        "watermark_disabled": true
    }
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| props | - | Object | 否 | 频道扩展属性 |
| props.watermark_disabled | true | Boolean | 否 | - |


**响应示例**

成功（200）

```javascript
{
    "code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |


## 在线频道详情
**接口URL**

> /server/v1/channel/detail
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |


**响应示例**

成功（200）

```javascript
{
    "code": 0,
    "data": {
        "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
        "channel": "fire",
        "props": null,
        "created_at": 1718250917,
        "updated_at": 1718250921,
        "link_id": 100000036,
        "max_user": 1024,
        "max_audio": 0,
        "max_peer": 32,
        "max_video": 16
    }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |
| data | - | Object | - |
| data.app_id | - | String | - |
| data.channel | - | String | - |
| data.props | null | Null | 频道扩展属性 |
| data.created_at | 1718250917 | Integer | - |
| data.updated_at | 1718250921 | Integer | - |
| data.link_id | 100000036 | Integer | - |
| data.max_user | 1024 | Integer | - |
| data.max_audio | 0 | Integer | - |
| data.max_peer | 32 | Integer | - |
| data.max_video | 16 | Integer | - |


## 在线/离线用户列表
**接口URL**

> /server/v1/channel/list-user
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "offline": false,
    "with_audience": true,
    "per-page": 10,
    "page": 1
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| offline | true | Boolean | 是 | 获取在线还是离线成员列表 |
| with_audience | true | Boolean | 是 | 是否包括隐身观众 |
| per-page | 10 | Integer | 否 | 分页参数不传则返回所有用户 |
| page | 1 | Integer | 否 | - |


**响应示例**

成功（200）

```javascript
{
    "code": 0,
    "data": [
        {
            "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
            "uid": "1",
            "name": "shu",
            "device_type": 1,
            "device_id": "aacc",
            "version": "1.0",
            "props": {
                "avatar": "https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png"
            },
            "netid": "",
            "sgid": "",
            "updated_at": 1718250918,
            "channel": "fire",
            "sid": "bjcjlbz18tfhbscaz225",
            "is_audience": false,
            "join_at": 1718250918,
            "leave_at": 0,
            "stream_tracks": null,
            "link_id": 100000037,
            "upload_id": "sm0dx5"
        }
    ],
    "_meta": {
        "totalCount": 1,
        "pageCount": 1,
        "currentPage": 1,
        "perPage": 10
    }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |
| data | - | Array | - |
| data.app_id | 68b3ft51smhz0x5glscw9whm78bw57uu | String | - |
| data.uid | 1 | String | 第三方用户ID |
| data.name | shu | String | 会中昵称 |
| data.device_type | 1 | Integer | 0:未知设备 1:Windows 2:Android 3:iOS 4:Linux 5:MacOS 6:WebRTC 7:微信小程序 |
| data.device_id | aacc | String | 设备唯一id |
| data.version | 1.0 | String | 客户端RTCsdk版本号 |
| data.props | - | Object | 用户扩展属性 |
| data.props.avatar | [https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png](https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png) | String | - |
| data.netid | - | String | 线路号 |
| data.sgid | - | String | 服务器分组id |
| data.updated_at | 1718250918 | Integer | 用户信息更新时间 |
| data.channel | fire | String | 频道名 |
| data.sid | bjcjlbz18tfhbscaz225 | String | - |
| data.is_audience | false | Boolean | 是否观众，类似研讨会观众，只收流，不参与互动，不广播 |
| data.join_at | 1718250918 | Integer | 加入频道时间 |
| data.leave_at | 0 | Integer | 离开频道时间 |
| data.stream_tracks | null | Null | 流轨道 |
| data.link_id | 100000037 | Integer | - |
| data.upload_id | sm0dx5 | String | - |
| _meta | - | Object | - |
| _meta.totalCount | 1 | Integer | - |
| _meta.pageCount | 1 | Integer | - |
| _meta.currentPage | 1 | Integer | - |
| _meta.perPage | 10 | Integer | - |


## 频道用户详情
**接口URL**

> /server/v1/channel/user-detail
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |


**响应示例**

成功（200）

```javascript
{
    "code": 0,
    "data": {
        "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
        "uid": "1",
        "name": "shu",
        "device_type": 1,
        "device_id": "aacc",
        "version": "1.0",
        "props": {
            "avatar": "https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png"
        },
        "netid": "",
        "sgid": "",
        "updated_at": 1717639307,
        "channel": "fire",
        "sid": "p8ym6zzpzkzy0pedl97t",
        "is_audience": false,
        "join_at": 1717639307,
        "leave_at": 0,
        "stream_tracks": null,
        "link_id": 100000002,
        "upload_id": "sm0dx5"
    }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |
| data | - | Object | - |
| data.app_id | 68b3ft51smhz0x5glscw9whm78bw57uu | String | - |
| data.uid | 1 | String | - |
| data.name | shu | String | - |
| data.device_type | 1 | Integer | - |
| data.device_id | aacc | String | - |
| data.version | 1.0 | String | - |
| data.props | - | Object | 扩展属性 |
| data.props.avatar | [https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png](https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png) | String | - |
| data.netid | - | String | - |
| data.sgid | - | String | - |
| data.updated_at | 1717639307 | Integer | - |
| data.channel | fire | String | - |
| data.sid | p8ym6zzpzkzy0pedl97t | String | - |
| data.is_audience | false | Boolean | - |
| data.join_at | 1717639307 | Integer | - |
| data.leave_at | 0 | Integer | - |
| data.stream_tracks | null | Null | - |
| data.link_id | 100000002 | Integer | - |
| data.upload_id | sm0dx5 | String | - |


## 更新频道扩展信息
**接口URL**

> /server/v1/channel/update
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "props": {
        "watermark_disabled": true
    }
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| props | - | Object | 是 | 频道扩展属性 |
| props.watermark_disabled | true | Boolean | 是 | - |


**响应示例**

成功（200）

```javascript
{
    "code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |


## 更新频道用户信息
**接口URL**

> /server/v1/channel/update-user
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1",
    "name": "shu1",
    "props": {
        "role": 1
    },
    "is_audience": false,
    "stream_tracks": []
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| uid | 1 | Integer | 是 | 第三方用户ID |
| name | shu1 | String | 否 | 会中昵称 |
| props | - | Object | 否 | 用户扩展属性 |
| is_audience | false | Boolean | 否 | 是否观众，类似研讨会观众，只收流，不参与互动，不广播 |
| stream_tracks | - | Array | 否 | 流轨道 |


**响应示例**

成功（200）

```javascript
{
    "code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |


## 发送频道自定义消息
**接口URL**

> /server/v1/channel/send-custom-msg
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "action": "chat",
    "content": "i love srtc",
    "uid": "1",
    "ruids": [],
	  "important": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| action | chat | String | 是 | 消息命令 |
| content | i love srtc | String | 否 | 消息体 |
| uid | 1 | String | 否 | 发送者uid |
| ruids | - | Array | 否 | 接收者id列表，为空时表示全频道接收 |
| important | false | Bool | 否 | 是否重要消息（一般不需要设置，重要消息会保障到达率，如断线重连后也能继续收到。） |


**响应示例**

成功（200）

```javascript
{
    "code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |


## 踢人
**接口URL**

> /server/v1/channel/kick-user
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| uid | 1 | String | 是 | 第三方用户id |


**响应示例**

成功（200）

```javascript
{
    "code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |


## 销毁频道
**接口URL**

> /server/v1/channel/destroy
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |


**响应示例**

成功（200）

```javascript
{
    "code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |


## 频道记录
**说明**

单人多次进入有多条记录

**接口URL**

> /server/v1/channel/list-record
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "begin_at": 0,
    "end_at": 0,
    "sort": "-open_at",
    "per-page": 10,
    "page": 1
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 否 | 频道名，可不传，传则代表只查询该名称频道记录 |
| begin_at | 0 | Integer | 否 | 过滤区间：开启开始时间 |
| end_at | 0 | Integer | 否 | 过滤区间：开启截止时间 |
| sort | -open_at | String | 否 | open_at开启时间 destroy_at销毁时间 |
| per-page | 10 | Integer | 否 | - |
| page | 1 | Integer | 否 | - |


**响应示例**

成功（200）

```javascript
{
    "code": 0,
    "data": [
        {
            "id": "snp3rp",
            "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
            "channel": "fire",
            "props": {
                "watermark_disabled": true
            },
            "open_at": 1718194666,
            "destroy_at": 1718194705,
            "destroy_reason": 1
        }
    ],
    "_meta": {
        "totalCount": 1,
        "pageCount": 1,
        "currentPage": 1,
        "perPage": 10
    }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |
| data | - | Array | - |
| data.id | snp3rp | String | - |
| data.app_id | 68b3ft51smhz0x5glscw9whm78bw57uu | String | - |
| data.channel | fire | String | 频道名 |
| data.props | - | Object | 频道扩展属性 |
| data.props.watermark_disabled | true | Boolean | - |
| data.open_at | 1718194666 | Integer | 打开时间 |
| data.destroy_at | 1718194705 | Integer | 销毁时间 |
| data.destroy_reason | 1 | Integer | 销毁原因：1主动销毁 2人数为0时自动销毁 |
| _meta | - | Object | - |
| _meta.totalCount | 1 | Integer | - |
| _meta.pageCount | 1 | Integer | - |
| _meta.currentPage | 1 | Integer | - |
| _meta.perPage | 10 | Integer | - |


## 用户出入频道记录
**说明**

单人多次进入有多条记录

**接口URL**

> /server/v1/channel/list-user-record
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "",
    "begin_at": 0,
    "end_at": 0,
    "sort": "-join_at",
    "per-page": 10,
    "page": 1
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| uid | - | String | 否 | 第三方用户ID，可为空，否则进返回指定uid的记录 |
| begin_at | 0 | Integer | 否 | 过滤区间：加入开始时间 |
| end_at | 0 | Integer | 否 | 过滤区间：加入截止时间 |
| sort | -join_at | String | 否 | join_at加入时间 leave_at离开时间 |
| per-page | 10 | Integer | 否 | - |
| page | 1 | Integer | 否 | - |


**响应示例**

成功（200）

```javascript
{
    "code": 0,
    "data": [
        {
            "id": "syd30d",
            "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
            "channel": "fire",
            "sid": "ff6u9joh5c1a0toa7dj1",
            "uid": "1",
            "name": "shu",
            "is_audience": false,
            "device_type": 1,
            "device_id": "aacc",
            "version": "1.0",
            "props": {
                "avatar": "https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png"
            },
            "join_at": 1718194697,
            "leave_at": 1718194700,
            "leave_reason": 1
        },
        {
            "id": "svdp7d",
            "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
            "channel": "fire",
            "sid": "ve46lmunkmgswz8he7s8",
            "uid": "1",
            "name": "shu",
            "is_audience": false,
            "device_type": 1,
            "device_id": "aacc",
            "version": "1.0",
            "props": {
                "avatar": "https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png"
            },
            "join_at": 1718194573,
            "leave_at": 1718194626,
            "leave_reason": 5
        },
        {
            "id": "solvpl",
            "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
            "channel": "fire",
            "sid": "v1jfic8nccb4e5x2gb24",
            "uid": "1",
            "name": "shu",
            "is_audience": false,
            "device_type": 1,
            "device_id": "aacc",
            "version": "1.0",
            "props": {
                "avatar": "https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png"
            },
            "join_at": 1718101904,
            "leave_at": 1718102215,
            "leave_reason": 4
        },
        {
            "id": "skrm8l",
            "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
            "channel": "fire",
            "sid": "0nfxyqcmggkzjh8shlul",
            "uid": "1",
            "name": "shu",
            "is_audience": false,
            "device_type": 1,
            "device_id": "aacc",
            "version": "1.0",
            "props": {
                "avatar": "https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png"
            },
            "join_at": 1718099758,
            "leave_at": 1718100115,
            "leave_reason": 4
        },
        {
            "id": "sprqjd",
            "app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
            "channel": "fire",
            "sid": "epo1fy47x52jt7mlzb1x",
            "uid": "1",
            "name": "shu",
            "is_audience": false,
            "device_type": 1,
            "device_id": "aacc",
            "version": "1.0",
            "props": {
                "avatar": "https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png"
            },
            "join_at": 1718099245,
            "leave_at": 1718194626,
            "leave_reason": 5
        }
    ],
    "_meta": {
        "totalCount": 5,
        "pageCount": 1,
        "currentPage": 1,
        "perPage": 10
    }
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |
| data | - | Array | - |
| data.id | syd30d | String | - |
| data.app_id | 68b3ft51smhz0x5glscw9whm78bw57uu | String | - |
| data.channel | fire | String | 频道名 |
| data.sid | ff6u9joh5c1a0toa7dj1 | String | 会话id |
| data.uid | 1 | String | 第三方用户ID，可为空，否则进返回指定uid的记录 |
| data.name | shu | String | - |
| data.is_audience | false | Boolean | 是否观众，类似研讨会观众，只收流，不参与互动，不广播 |
| data.device_type | 1 | Integer | - |
| data.device_id | aacc | String | - |
| data.version | 1.0 | String | - |
| data.props | - | Object | 用户扩展属性 |
| data.props.avatar | [https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png](https://img.cdn.apipost.cn/user/886686/98959c31ef6b22c5.png) | String | - |
| data.join_at | 1718194697 | Integer | 加入频道时间 |
| data.leave_at | 1718194700 | Integer | 离开频道时间 |
| data.leave_reason | 1 | Integer | 离开原因：1主动离开 2被踢离开 3被顶号 4心跳超时离开 5频道销毁离开 |
| _meta | - | Object | - |
| _meta.totalCount | 5 | Integer | - |
| _meta.pageCount | 1 | Integer | - |
| _meta.currentPage | 1 | Integer | - |
| _meta.perPage | 10 | Integer | - |


# 
