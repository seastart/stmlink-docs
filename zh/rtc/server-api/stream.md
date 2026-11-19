---
title: "单路流输出"
description: "把频道内某个用户的音视频以 RTSP / HTTP-FLV 拉流地址输出，接入 NVR、录像机或第三方播放器"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 获取单路 RTSP 拉流地址

`POST /server/v1/stream/rtsp-url`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取频道内某个用户音频/视频的 RTSP 拉流地址。服务端以观众身份订阅该用户的流，
不转码、原样以 RTSP 输出，适合把会中画面接进 NVR、录像机或其它只认 RTSP 的系统。

+ 地址自带签名，有效期内可被多个拉流端反复拉取；过期后新的拉流请求会被拒绝，已在播放的不受影响
+ 有人来拉时才订阅，最后一个拉流端断开后自动退订，不拉不占资源；无需调用停止接口
+ 不校验频道是否开启、用户是否在线，地址可提前生成；拉流时该用户还没发布，拉流端会收到 404，需重试
+ 用户中途离开再回来，拉流不断，中间是一段空白
+ 只支持 RTSP over TCP（拉流端需用 TCP 方式，如 ffplay 加 `-rtsp_transport tcp`）
+ 不转码：音频为 Opus，视频为发布端实际使用的编码（H264 或 VP8），拉流端不支持 VP8 时请让发布端使用 H264

实际有效期以返回的 expire_at 为准（服务端配置的上限可能小于请求值）。

**请求参数**

<ParamField body="channel" type="string" required>
  频道（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  要拉流的发布者用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="media" type="string" required>
  媒体类型 audio 仅音频、video 仅视频、av 音视频
  示例：`av`
</ParamField>

<ParamField body="desc" type="string">
  视频轨道描述，该用户同时发布多路视频（如摄像头与屏幕共享）时用来指定其中一路；不传则输出先到的那一路（最大长度 50）
  示例：`camera`
</ParamField>

<ParamField body="expire" type="integer">
  地址有效期（秒），不传时默认一小时，最长一天
  示例：`3600`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "desc": "camera",
  "expire": 3600,
  "media": "av",
  "uid": "1001"
}
```

**响应参数**

<ResponseField name="url" type="string">
  RTSP 拉流地址，自带签名，有效期内可反复拉
  示例：`rtsp://1.2.3.4:8554/s/eyJhcHBpZCI6...`
</ResponseField>

<ResponseField name="expire_at" type="integer">
  地址过期时间，秒级时间戳；过期后新的拉流请求会被拒绝，已在播放的不受影响
  示例：`1718198266`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "expire_at": 1718198266,
    "url": "rtsp://1.2.3.4:8554/s/eyJhcHBpZCI6..."
  }
}
```

---

## 获取单路 HTTP-FLV 拉流地址（仅 H264 视频）

`POST /server/v1/stream/flv-url`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取频道内某个用户视频的 HTTP-FLV 拉流地址。服务端以观众身份订阅该用户的视频，
不转码、原样封装成 HTTP-FLV 输出，适合接进只认 FLV 的播放器或第三方平台。

+ 只出视频，不含音频；视频须为 H264，发布端使用 VP8 等其它编码时拉流会收到 404，请让发布端使用 H264
+ 地址自带签名，有效期内可被多个拉流端反复拉取；过期后新的拉流请求会被拒绝，已在播放的不受影响
+ 有人来拉时才订阅，最后一个拉流端断开后自动退订，不拉不占资源；无需调用停止接口
+ 不校验频道是否开启、用户是否在线，地址可提前生成；拉流时该用户还没发布，拉流端会收到 404，需重试
+ 用户中途离开再回来，拉流不断，中间是一段空白

实际有效期以返回的 expire_at 为准（服务端配置的上限可能小于请求值）。

**请求参数**

<ParamField body="channel" type="string" required>
  频道（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  要拉流的发布者用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`1001`
</ParamField>

<ParamField body="desc" type="string">
  视频轨道描述，该用户同时发布多路视频（如摄像头与屏幕共享）时用来指定其中一路；不传则输出先到的那一路（最大长度 50）
  示例：`camera`
</ParamField>

<ParamField body="expire" type="integer">
  地址有效期（秒），不传时默认一小时，最长一天
  示例：`3600`
</ParamField>


请求示例：

```json
{
  "channel": "fire",
  "desc": "camera",
  "expire": 3600,
  "uid": "1001"
}
```

**响应参数**

<ResponseField name="url" type="string">
  HTTP-FLV 拉流地址，自带签名，有效期内可反复拉
  示例：`http://1.2.3.4:8080/f/eyJhcHBpZCI6....flv`
</ResponseField>

<ResponseField name="expire_at" type="integer">
  地址过期时间，秒级时间戳；过期后新的拉流请求会被拒绝，已在播放的不受影响
  示例：`1718198266`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "expire_at": 1718198266,
    "url": "http://1.2.3.4:8080/f/eyJhcHBpZCI6....flv"
  }
}
```

---

