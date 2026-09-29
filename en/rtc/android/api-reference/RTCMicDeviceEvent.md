---
title: "RTCMicDeviceEvent"
description: "Android Engine-global microphone input device events: input device list changes and invalidation of the device currently capturing, registered with setRtcMicDeviceEvent. Read when you need to react to headset, Bluetooth, or USB microphone plugging on Android."
---

Microphone capture is shared by all channels, so input device events are Engine-global events. Register them with `RTCEngine.setRtcMicDeviceEvent(...)`; pass `null` to unbind. If you only care about some events, extend `RTCMicDeviceSimpleEvent`.

## onMicDeviceListChanged(devices)

```kotlin
fun onMicDeviceListChanged(devices: List<MicDeviceCapability>)
```

The microphone input devices available on the system changed, for example when a wired headset, Bluetooth, or USB microphone is plugged in or removed. The parameter is the full device list after the change.

## onMicDeviceInvalid(deviceId, reason)

```kotlin
fun onMicDeviceInvalid(deviceId: String, reason: String)
```

The input device currently capturing became invalid. The SDK tries to fall back to the system default input and rebuild capture; `deviceId` is the device handle for this connection, and `reason` is why it became invalid.

For input device fields, see [Types](/en/rtc/android/types); for querying and switching devices, see [LocalMicTrack](/en/rtc/android/api-reference/LocalMicTrack).
