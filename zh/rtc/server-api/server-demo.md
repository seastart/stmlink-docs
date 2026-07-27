---
title: "服务端 Demo"
description: "服务端 Demo 接口说明与部署指南"
---

## 服务端demo接口说明
**说明**

给srtc demo的api接口，可以理解为第三方业务后端，组合了demo业务逻辑及对srtc服务端 api的调用。

**请求格式**

application/json 格式传递

**SRTC扩展定义**

频道props扩展

```javascript
{
  "share_state": true, // 是否在共享
  "share_uid": "uid", // 共享的用户
  "share_track": 3, // 共享的流轨道
}
```

用户props扩展

```javascript
{
  "avatar": "https://xxx.jpg", // 头像
  "audio_state": true, // 是否开麦
  "video_state": false, // 是否打开视频
}
```

自定义消息：聊天

```javascript
{
  "action": "chat",
  "content": "聊天消息",
}
```

自定义消息：开视频

```javascript
{
  "action": "video_open",
  "content": {
    "uid": "用户id"
  },
}
```

自定义消息：关视频

```javascript
{
  "action": "video_close",
  "content": {
    "uid": "用户id"
  },
}
```

自定义消息：开麦

```javascript
{
  "action": "audio_open",
  "content": {
    "uid": "用户id"
  },
}
```

自定义消息：关麦

```latex
{
  "action": "audio_close",
  "content": {
    "uid": "用户id"
  },
}
```

自定义消息：共享开始

```latex
{
  "action": "share_start",
  "content": {
    "uid": "用户id",
    "track": 3,
  },
}
```

自定义消息：共享结束

```latex
{
  "action": "share_stop",
  "content": {
    "uid": "用户id",
  },
}
```



流相关

轨道：0摄像头大流，1摄像头小流，2共享流  

描述：摄像头大流，摄像头小流，共享流

## 代理任意srvapi
**接口URL**

> /demo/srvapi
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "api": "channel/detail",
    "params": {
        "channel": "fire"
    }
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| api | channel/detail | String | 是 | 要调用的srv api |
| params | - | Object | 是 | api参数 |
| params.channel | fire | String | 是 | - |


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


## 获取token
**接口URL**

> /demo/token
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1",
    "name": "shu",
    "is_audience": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| uid | 1 | String | 是 | 第三方用户ID |
| name | shu | String | 是 | 频道中昵称 |
| is_audience | false | Boolean | 是 | 是否观众，类似研讨会观众，只收流，不参与互动，不广播 |


**响应示例**

成功（200）

```javascript
{
    "code": 0,
    "data": "wvYKytpMTsR2OK82ghVj1ZFAVCEtfMugr5PwFRjKzIm3b32plqC9Fyuwc2Bj+3qvTYxLFNd/FhN7ydvhQyvu/T6gC6ZyEPuJmWJEv2buiVGAP7a1AwyyXxL7ezSb9TCwVjrV9OR3cpE+Dnvf0LcQnkcFyd57Cco5+cYglDZo05YE2O6aAnhQNSyAru3o1+Ko5Qcu/x4CDQ4NzOUmU2p6uVTOXuuD9oTXV2FIPQDK26q9nlprFpRWYS30CKZVbeoqYurJ+x5boiBtYMlLyfGppBLLapOUNQb6CqNccfJMdsFTy52GHrxOIRMi24g7Y4yy"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | Integer | - |
| data | wvYKytpMTsR2OK82ghVj1ZFAVCEtfMugr5PwFRjKzIm3b32plqC9Fyuwc2Bj+3qvTYxLFNd/FhN7ydvhQyvu/T6gC6ZyEPuJmWJEv2buiVGAP7a1AwyyXxL7ezSb9TCwVjrV9OR3cpE+Dnvf0LcQnkcFyd57Cco5+cYglDZo05YE2O6aAnhQNSyAru3o1+Ko5Qcu/x4CDQ4NzOUmU2p6uVTOXuuD9oTXV2FIPQDK26q9nlprFpRWYS30CKZVbeoqYurJ+x5boiBtYMlLyfGppBLLapOUNQb6CqNccfJMdsFTy52GHrxOIRMi24g7Y4yy | String | - |


## 打开摄像头
**接口URL**

> /demo/open-video
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
| uid | 1 | String | 是 | 第三方用户ID |


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


## 关闭摄像头
**接口URL**

> /demo/close-video
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
| uid | 1 | String | 是 | 第三方用户ID |


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


## 打开麦克风
**接口URL**

> /demo/open-audio
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
| uid | 1 | String | 是 | 第三方用户ID |


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


## 关闭麦克风
**接口URL**

> /demo/close-audio
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
| uid | 1 | String | 是 | 第三方用户ID |


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


## 开始桌面共享
**接口URL**

> /demo/start-share
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1",
    "track": 3
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| uid | 1 | String | 是 | 第三方用户ID |
| track | 3 | Integer | 是 | 共享轨道 |


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


## 结束桌面共享
**接口URL**

> /demo/stop-share
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1",
    "track": 3
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| uid | 1 | String | 是 | 第三方用户ID |
| track | 3 | Integer | 是 | 共享轨道 |


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


## 修改昵称
**接口URL**

> /demo/change-name
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1",
    "name": "帅小伙"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| uid | 1 | String | 是 | 第三方用户ID |
| name | 帅小伙 | String | 是 | 频道中昵称 |


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


## 发送聊天
**接口URL**

> /demo/send-chat
>

**请求参数**

Body请求参数（raw-json）

```javascript
{
    "channel": "fire",
    "uid": "1",
    "ruids": [],
    "content": "how are you"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| channel | fire | String | 是 | 频道名 |
| uid | 1 | String | 是 | 第三方用户ID |
| ruids | - | Array | 是 | 接收者id列表，为空时表示全频道接收 |
| content | how are you | String | 是 | - |


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


