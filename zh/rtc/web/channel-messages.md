---
title: "频道消息"
description: "Web SRTC 音视频 SDK 的频道外 IM 消息通道（启用、收发、重连与断开），以及同声传译相关的频道内消息 interp_enabled / interp_lang / asr_trans 的字段与译音播放做法"
---

SRTC提供便捷易用的频道外消息通道，方便开发者集成使用，如会前呼叫、通知等。

### 启用
```typescript
// im会话id
let imSid = "";
let enableIm = async () => {
    // 调后台api获取启用im token
    // api.getImToken
  
    let token = "后台返回的启用im token";
    imSid = await srtc.enableIm(token);
}
```



### 接收im消息
```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
    console.log('收到im事件', evt);
    switch (evt.type) {
        case ImEventType.IM_MSG:
            // 收到im消息
            // evt.data as ImMsgData
            break;
        
    }
}
```



### 发送im消息
发送im消息都需要通过后台api，这样可以根据自己的业务做如敏感词拦截等处理

```typescript
// 调后台api发送im消息
// api.sendImMsg
```



### 开始重连/重连成功
当网络发生波动时，会触发重连开始事件，成功后会触发重连成功事件

```typescript
// 在onNotifyImEvent里
case ImEventType.RECONNECTING:
  // 开始重连
  break;
case ImEventType.RECONNECTED:
  // 重连成功
  break;
```

### 停用/断开
断开分主动停用和被动(发生不可恢复错误时)断开

```typescript
// 主动停用
await srtc.disableIm();
// 界面刷新清理



// 被动断开
// 在onNotifyImEvent里
case ImEventType.DISCONNECTED:
  let data = (evt.data as ImDisconnectEventData);
  // 可根据reason提示退出原因
  alert('im已断开 reason:' + data.reason);
  // 界面刷新清理
  imSid = "";
  break;
```

---

### 同声传译消息

频道开启同声传译（服务端接口见[同声传译](/zh/rtc/server-api/interp)）后，服务端通过**频道内**自定义消息下发同传状态和译文，Web SDK 以 `ChannelEventType.CUSTOM_MSG` 事件抛出，`data` 为 `CustomMsgData`，按 `action` 区分：

| `action` | 何时下发 | `content` 字段 |
| --- | --- | --- |
| `interp_enabled` | 同传开启 / 关闭（含转写停止导致的被动关闭） | `enabled`：是否开启；`duck_volume`：播译音时说话人原声压低到的音量（0~1，`0` 为静音）；`err_desc`：被动关闭时的原因 |
| `interp_lang` | 某成员设置了同传语言 | `uid`：成员 ID；`lang`：语言，如 `zh` / `en`，空表示恢复默认语言 |
| `asr_trans` | 每句定稿后的译文 | `session_id`、`sentence_id`、`uid`（说话人）、`name`、`text`（原文）、`trans_text`（译文）、`lang`（译文语言），以及 `audio_url`（译音地址，同传开启且合成成功时才有） |

+ **入会时的状态**：后入会的成员从频道属性（`ChannelInfo.props` 的 `interp_enabled` / `interp_duck_volume`）取同传开关，由你的服务端调「查询频道同传状态与成员语言」取全量语言表，之后按上面两条消息增量更新
+ **一句多条**：同传开启时同一句按在会成员的语言各来一条 `asr_trans`，字幕只取 `lang` 等于本人语言的那条
+ **`audio_url` 是根相对路径**（形如 `/aiapi/interp-audio/<id>.wav`），要用入会 token 里 `client_api` 的地址拼成完整 URL：`new URL(audio_url, clientApi)`。音频 10 分钟后过期，不需要鉴权，允许网页跨域读取

译音的播放用 [`playAudioClip`](/zh/rtc/web/api-reference/SRTC#playaudioclip) 插播，播放期间用 [`setRemoteUserVolume`](/zh/rtc/web/api-reference/SRTC#setremoteuservolume) 把说话人原声压到 `duck_volume`（需要 0.7.7 及以上，且用 `subscribeRemoteAudioMixTrack` 播放远端声音）：

```typescript
let myLang = 'zh';       // 本人的同传语言
let duckVolume = 0.2;    // 来自 interp_enabled 消息或频道属性
let queue = Promise.resolve();

srtc.onNotifyChannelEvent = (evt: ChannelEvent) => {
  if (evt.type !== ChannelEventType.CUSTOM_MSG) {
    return;
  }
  const { action, content } = evt.data;
  if (action === 'interp_enabled') {
    duckVolume = content.duck_volume;
  } else if (action === 'asr_trans' && content.lang === myLang && content.audio_url) {
    const url = new URL(content.audio_url, clientApi).toString();
    // 依次播放，避免两段译音叠在一起
    queue = queue.then(async () => {
      srtc.setRemoteUserVolume(content.uid, duckVolume);
      try {
        const clip = await srtc.playAudioClip(url);
        await clip.ended;
      } catch (e) {
        console.warn('译音播放失败', e);   // 单句失败跳过，不影响后面的句子
      } finally {
        srtc.setRemoteUserVolume(content.uid, 1);
      }
    });
  }
};
```

> 只有字幕、听不到译音时：先确认 AI 方案配了语音合成（没配时 `asr_trans` 不带 `audio_url`）；再确认部署时的反向代理放行了 `/aiapi/interp-audio/` 路径，见 [内外网与多线路](/zh/product/deploy/networks#部署时要准备什么)。使用会议 SDK 时不需要自己写这段，SMeeting Web SDK 已内置同传播放器，见 [SMeeting · 同声传译](/zh/meeting/web/api-reference/SMeeting#同声传译)。
