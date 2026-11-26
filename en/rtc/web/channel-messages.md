---
title: "Channel messages"
description: "The Web SDK's IM channel (out-of-channel messaging) for pre-call ringing and notifications: enable, receive, send, reconnect, and disconnect. Also the in-channel simultaneous interpretation messages interp_enabled / interp_lang / asr_trans and how to play interpretation audio."
---

SRTC provides an IM channel (out-of-channel messaging) for things like pre-call ringing and notifications.

### Enable
```typescript
// IM session ID
let imSid = "";
let enableIm = async () => {
    // Call your backend API to get the IM enable token
    // api.getImToken
  
    let token = "IM enable token returned by your backend";
    imSid = await srtc.enableIm(token);
}
```



### Receive IM messages
```typescript
srtc.onNotifyImEvent = (evt: ImEvent) => {
    console.log('Received IM event', evt);
    switch (evt.type) {
        case ImEventType.IM_MSG:
            // Received an IM message
            // evt.data as ImMsgData
            break;
        
    }
}
```



### Send IM messages
All IM messages must be sent through your backend API, so you can apply your own logic, such as sensitive-word filtering

```typescript
// Call your backend API to send the IM message
// api.sendImMsg
```



### Reconnecting / reconnected
When the network fluctuates, a reconnecting event fires; once reconnection succeeds, a reconnected event fires

```typescript
// Inside onNotifyImEvent
case ImEventType.RECONNECTING:
  // Reconnecting started
  break;
case ImEventType.RECONNECTED:
  // Reconnected successfully
  break;
```

### Disable / disconnect
Disconnection is either an active disable or a passive disconnect (when an unrecoverable error occurs)

```typescript
// Active disable
await srtc.disableIm();
// Refresh and clean up the UI



// Passive disconnect
// Inside onNotifyImEvent
case ImEventType.DISCONNECTED:
  let data = (evt.data as ImDisconnectEventData);
  // You can show why IM disconnected based on reason
  alert('IM disconnected reason:' + data.reason);
  // Refresh and clean up the UI
  imSid = "";
  break;
```

---

### Simultaneous interpretation messages

After simultaneous interpretation is turned on for a channel (for the server API, see [Simultaneous Interpretation](/en/rtc/server-api/interp)), the server delivers the interpretation status and translations through **in-channel** custom messages. The Web SDK raises them as `ChannelEventType.CUSTOM_MSG` events, with `data` of type `CustomMsgData`, distinguished by `action`:

| `action` | When delivered | `content` fields |
| --- | --- | --- |
| `interp_enabled` | Interpretation turned on / off (including passive shutdown because transcription stopped) | `enabled`: whether it's on; `duck_volume`: the volume the speaker's original voice is lowered to while interpretation audio plays (0–1, `0` is muted); `err_desc`: the reason for a passive shutdown |
| `interp_lang` | A member set their interpretation language | `uid`: member ID; `lang`: language, such as `zh` / `en`; empty means back to the default language |
| `asr_trans` | Translation of each finalized sentence | `session_id`, `sentence_id`, `uid` (speaker), `name`, `text` (original), `trans_text` (translation), `lang` (translation language), and `audio_url` (interpretation audio URL, present only when interpretation is on and synthesis succeeded) |

+ **Status on joining**: members who join later get the interpretation on/off state from the channel properties (`interp_enabled` / `interp_duck_volume` in `ChannelInfo.props`), and your backend calls "Get interpretation status and member languages" for the full language table; after that, update incrementally with the two messages above
+ **Multiple messages per sentence**: when interpretation is on, each sentence arrives as one `asr_trans` per language of the members in the channel; for captions, take only the one whose `lang` equals your own language
+ **`audio_url` is a root-relative path** (like `/aiapi/interp-audio/<id>.wav`); build the full URL with the `client_api` address in the join token: `new URL(audio_url, clientApi)`. The audio expires after 10 minutes, requires no authentication, and allows cross-origin reads from web pages

Play the interpretation audio with [`playAudioClip`](/en/rtc/web/api-reference/SRTC#playaudioclip), and while it plays, lower the speaker's original voice to `duck_volume` with [`setRemoteUserVolume`](/en/rtc/web/api-reference/SRTC#setremoteuservolume) (requires 0.7.7 or later, with remote audio played through `subscribeRemoteAudioMixTrack`):

```typescript
let myLang = 'zh';       // Your own interpretation language
let duckVolume = 0.2;    // From the interp_enabled message or channel properties
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
    // Play one after another so two interpretation clips don't overlap
    queue = queue.then(async () => {
      srtc.setRemoteUserVolume(content.uid, duckVolume);
      try {
        const clip = await srtc.playAudioClip(url);
        await clip.ended;
      } catch (e) {
        console.warn('Interpretation audio playback failed', e);   // Skip a failed sentence; later sentences are unaffected
      } finally {
        srtc.setRemoteUserVolume(content.uid, 1);
      }
    });
  }
};
```

> If you get captions but no interpretation audio: first make sure the AI profile has speech synthesis configured (without it, `asr_trans` has no `audio_url`); then make sure the reverse proxy at deployment allows the `/aiapi/interp-audio/` path, see [Internal network and public internet](/en/product/deploy/networks#what-to-prepare-at-deployment). If you use the meeting SDK, you don't need to write this yourself: SMeeting Web SDK has a built-in interpretation player, see [SMeeting · Simultaneous interpretation](/en/meeting/web/api-reference/SMeeting#simultaneous-interpretation).
