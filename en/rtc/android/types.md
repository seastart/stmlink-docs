---
title: "Types"
description: "Field reference for Android SRTC SDK data structures: ChannelInfo, UserInfo, TrackInfo, UserTrackDesc, VolumeInfo, ActiveSpeakerInfo, NetworkQualityChange, camera and microphone device capabilities, and YuvFormat constants. Read when you need the meaning of a field returned by the SDK."
---

## ChannelInfo

Purpose: Channel info data, describing the channel's basic properties, capacity limits, and extension fields.

| Property | Data type | Description |
| --- | --- | --- |
| appId | String? | App ID. |
| channel | String | Channel name. |
| created_at | Long | Channel creation time. |
| updated_at | Long | Channel update time. |
| link_id | Int | Media streaming connection ID. |
| max_user | Int | Maximum number of users in the channel. |
| max_audio | Int | Maximum number of audio streams forwarded in the channel. |
| max_peer | Int | Maximum number of streams that can be forwarded per user in the channel. |
| max_video | Int | Maximum number of video streams that can be forwarded per user in the channel. |
| props | JsonElement? | Custom properties. |

## UserInfo

Purpose: User info data, describing the user's identity, device info, join status, and published tracks.

| Property | Data type | Description |
| --- | --- | --- |
| app_id | String? | App ID. |
| uid | String | User ID on your platform. |
| sid | String? | Session ID. |
| name | String? | User name. |
| device_type | Int? | Device type. |
| device_id | String? | Unique device identifier. |
| sdk_version | String? | SDK version. |
| version | String? | Version. |
| props | JsonElement? | Custom properties. |
| netid | String? | Network ID. |
| sgid | String? | Group ID. |
| channel | String? | Channel name. |
| is_audience | Boolean | Whether the user is audience. |
| join_at | Long | Join time. |
| updated_at | Long | Update time. |
| leave_at | Long | Leave time. |
| stream_tracks | `ArrayList<TrackInfo>?` | Info on the tracks currently being published. |
| link_id | Int | Media streaming connection ID. |
| session_key | String? | Media streaming connection key. |
| upload_id | String? | ID of the media streaming service the user currently belongs to. |

## TrackInfo

Purpose: Track info data, describing an audio or video stream's identifier, media parameters, and extension fields.

| Property | Data type | Description |
| --- | --- | --- |
| id | String | Stream ID. |
| desc | String | Stream description. |
| kind | String | Stream type (`video` / `audio`). |
| codec | Int | Codec type. |
| width | Int | Video width. |
| height | Int | Video height. |
| fps | Int | Video frame rate. |
| angle | Int | Video angle. |
| bitrate | Int | Bitrate. |
| sample_rate | Int | Audio sample rate. |
| fallback_ids | `MutableList<String>?` | IDs of the lower-layer tracks this layer can fall back to, excluding itself, ordered from highest to lowest quality. |
| variant | Boolean? | Whether this is a simulcast secondary layer; the primary layer is usually `false`. |
| track | Int | Media streaming track (0–6). |
| props | JsonElement? | Custom properties. |

## UserTrackDesc

Purpose: A composite key of user and track description, commonly used to locate statistics or stream info by user track.

| Property | Data type | Description |
| --- | --- | --- |
| uid | String | User UID. |
| trackDesc | String | Track description. |

## VolumeInfo

Purpose: Volume data, describing the user's current audio energy.

| Property | Data type | Description |
| --- | --- | --- |
| uid | String | User UID. |
| db | Int | Audio energy (decibels). |

## ActiveSpeakerInfo

Purpose: Active speaker info, delivered by [`RTCMediaEvent.onActiveSpeakersChanged`](/en/rtc/android/api-reference/RTCMediaEvent).

| Property | Data type | Description |
| --- | --- | --- |
| uid | String | The speaking user's uid. |
| trackId | String | The audio track's trackId. |
| level | Double | Volume intensity quantized by the server. |

## NetworkQualityChange

Purpose: A network quality level event, delivered by [`RTCMediaEvent.onNetworkQualityChanged`](/en/rtc/android/api-reference/RTCMediaEvent). Every quality report from the server fires once each for uplink and downlink (no debouncing); each callback represents only one direction.

| Property | Data type | Description |
| --- | --- | --- |
| direction | QualityDirection | The direction that changed (`UPLINK` / `DOWNLINK`). For the enum, see [Enums](/en/rtc/android/enums). |
| previousLevel | String | The level in the previous callback; an empty string the first time (`INITIAL`). |
| currentLevel | String | The current level (`excellent` / `good` / `poor` / `lost`). |
| trend | QualityTrend | The trend compared with the previous callback (`INITIAL` / `DEGRADED` / `RECOVERED` / `STABLE`). For the enum, see [Enums](/en/rtc/android/enums). |
| report | ServerQualityReport | The FY server quality report that triggered this event. For fields, see [Media quality](/en/rtc/android/media-quality). |

## CameraDeviceCapability

Purpose: Camera device capability info, returned by [`RTCEngine.getCameraDevices`](/en/rtc/android/api-reference/RTCEngine) and [`RTCCameraDeviceEvent.onCameraDeviceListChanged`](/en/rtc/android/api-reference/RTCCameraDeviceEvent).

| Property | Data type | Description |
| --- | --- | --- |
| cameraId | String | The native Camera2 camera id, usable with `LocalCameraTrack.switchCameraDevice`. |
| position | CamraPosition | The SDK's unified camera position (`FRONT` / `BACK` / `External`). |
| displayName | String? | The default display name generated by the SDK. |
| sensorOrientation | Int | The Camera2 sensor mounting orientation. |
| hardwareLevel | Int | The Camera2 hardware capability level. |
| formats | List\<CameraFormatCapability\> | The YUV capture formats supported by the device. |
| controls | CameraControlCapability | The control capabilities supported by the device. |

## CameraFormatCapability

Purpose: Camera capture format capability.

| Property | Data type | Description |
| --- | --- | --- |
| width | Int | Capture width. |
| height | Int | Capture height. |
| minFps | Int | Minimum frame rate of the AE fps range. |
| maxFps | Int | Maximum frame rate of the AE fps range. |

## CameraControlCapability

Purpose: Camera control capability.

| Property | Data type | Description |
| --- | --- | --- |
| supportsTorch | Boolean | Whether a flash or fill light is supported. |
| supportsZoom | Boolean | Whether zoom is supported. |
| supportsFocus | Boolean | Whether focus control is supported. |
| supportsExposure | Boolean | Whether exposure compensation is supported. |
| supportsWhiteBalance | Boolean | Whether white balance mode control is supported. |

## MicDeviceCapability

Purpose: Microphone input device capability info, returned by `RTCEngine.getMicDevices()`, `LocalMicTrack.getMicDevices()`, and [`RTCMicDeviceEvent.onMicDeviceListChanged`](/en/rtc/android/api-reference/RTCMicDeviceEvent).

| Property | Data type | Description |
| --- | --- | --- |
| deviceId | String | The `AudioDeviceInfo.id` string currently assigned by the system, valid only while the device stays connected; usable with `switchMicDevice(...)`. |
| key | MicDeviceKey | A persistent key for matching the device across re-plugging. |
| type | Int | The `AudioDeviceInfo.TYPE_*` input device type. |
| displayName | String? | The display name generated by the SDK. |
| productName | String? | The device product name reported by the system. |
| address | String? | The device address, such as a Bluetooth address or USB path; may be empty. |
| sampleRates | List\<Int\> | The sample rates the device reports as supported. |
| channelCounts | List\<Int\> | The channel counts the device reports as supported. |
| isDefault | Boolean | Whether this is the system's current default input device. |
| isCurrent | Boolean | Whether this is the device currently used by the SDK's microphone capture module. |

## MicDeviceKey

Purpose: The persistent matching key for a microphone device. The system `deviceId` may change after re-plugging, so the SDK uses `type + address + productName` to match the device again.

| Property | Data type | Description |
| --- | --- | --- |
| type | Int | The `AudioDeviceInfo.TYPE_*` input device type. |
| address | String? | The device address; may be empty. |
| productName | String? | The device product name; may be empty. |

## YuvFormat

Package path: `cn.seastart.rtc.media.format.YuvFormat`. Identifies the pixel layout of raw video frames; it doesn't mean every input API supports every format.

| Constant | Value | Pixel layout |
| --- | --- | --- |
| `NV21` | `17` | Y plane + interleaved VU plane. |
| `NV12` | `19` | Y plane + interleaved UV plane. |
| `I420` | `808596553` | Separate Y, U, and V planes. |
| `YV12` | `842094169` | Separate Y, V, and U planes. |
| `YUY2` | `20` | Packed YUYV format. |

The raw screen frame callback and `LocalCustomVideoTrack.inputData` use I420. The render view's `updateFrame` supports I420, NV12, and NV21, but not YV12 or YUY2.

## AudioCaptureProcessor

Package path: `cn.seastart.rtc.audio.AudioCaptureProcessor`, available since 2.0.39. A microphone capture processor attached with `RTCEngine.setAudioCaptureProcessor(...)`. It processes each PCM frame in place on the SDK capture thread before the data is distributed to all channels.

| Member | Description |
| --- | --- |
| `audioProcessing: AudioProcessingConstraints?` | Requirements for the built-in 3A; defaults to `null` (no change). |
| `initialize(sampleRate: Int, channelCount: Int)` | Called when the capture format is determined (each time a capture session starts, including rebuilds after device switches or route changes, and when a processor is attached while capturing). Must return quickly. |
| `process(data: ByteArray, offset: Int, length: Int)` | Processes one frame of 16-bit little-endian PCM (interleaved channels) in place; by default 48 kHz mono 10 ms, i.e. 960 bytes. Called synchronously every 10 ms and must return within a few milliseconds; the buffer is reused after return, so don't keep `data`. Exceptions thrown are caught by the SDK, and that frame is sent unchanged. |
| `release()` | Called when the processor is replaced or cleared; `process` isn't called afterward. |

## AudioProcessingConstraints

Package path: `cn.seastart.rtc.audio.AudioProcessingConstraints`, available since 2.0.39. A capture processor's requirements for the built-in audio preprocessing (3A), with the same meaning as the same-named type in the Web and Swift SDKs.

| Property | Data type | Description |
| --- | --- | --- |
| noiseSuppression | Boolean? | Noise suppression. `false` turns off the system's and WebRTC's built-in noise suppression. |
| echoCancellation | Boolean? | Echo cancellation; not yet handled on Android, keeps the SDK default. |
| autoGainControl | Boolean? | Automatic gain control; not yet handled on Android, keeps the SDK default. |

`false` requires the feature off; `true` or `null` leaves the SDK default unchanged.

## NetworkCheckOptions

Package path: `cn.seastart.rtc.netcheck.NetworkCheckOptions`, available since 2.0.40. Input for the [pre-call network check](/en/rtc/android/api-reference/RTCEngine#networkcheck-options-listener). Provide the server information in one of two ways: pass `appId` + `serverUrl` directly, or pass a join / IM token for the SDK to extract them from. If both are given, `appId` / `serverUrl` take precedence. The check itself doesn't use the token for authentication.

| Property | Data type | Description |
| --- | --- | --- |
| appId | String? | App ID. |
| serverUrl | String? | SDK API prefix, i.e. `client_api` in the token (such as `https://host/client/`). |
| token | String? | Optional join or IM token, used only to extract `appId` and `serverUrl`. |
| timeoutMs | Int | Per-item timeout in milliseconds, default `3000`. |

## NetworkCheckItem

Package path: `cn.seastart.rtc.netcheck.NetworkCheckItem`, available since 2.0.40. Result of a single check item.

| Property | Data type | Description |
| --- | --- | --- |
| id | String | Check item; see `NetworkCheckItemId`. |
| status | String | Check status: `pass` / `warning` / `fail` / `skipped` / `unsupported`; see `NetworkCheckStatus`. |
| reason | String | Machine-readable reason code, empty for `pass`; see `NetworkCheckReason`. |
| message | String | Chinese description that can be shown to users directly. |
| costMs | Long | Time spent on this item, in milliseconds. |
| data | Map\<String, Any?\> | Measured values for this item, such as `netType` for `connectivity`, `maxSize` for `mtu`, `hosts` for `dns`, and the `api` / `signal` / `media` sub-checks for `server` (each with `ok`, `status`, `reason`, and `rttMs`). |

## NetworkCheckResult

Package path: `cn.seastart.rtc.netcheck.NetworkCheckResult`, available since 2.0.40. Overall check result.

| Property | Data type | Description |
| --- | --- | --- |
| status | String | Overall status: `fail` if any item fails; otherwise `warning` if any item warns; otherwise `ok`. |
| items | List\<NetworkCheckItem\> | Always 5 items, in the order `permission`, `connectivity`, `mtu`, `dns`, `server`. |
| costMs | Long | Total time, in milliseconds. |

## Network check constants

Available since 2.0.40, all in the `cn.seastart.rtc.netcheck` package.

`NetworkCheckItemId` (check items):

| Constant | Value | Description |
| --- | --- | --- |
| `PERMISSION` | `permission` | Network permission |
| `CONNECTIVITY` | `connectivity` | Network connection |
| `MTU` | `mtu` | Maximum transmission unit |
| `DNS` | `dns` | DNS resolution |
| `SERVER` | `server` | Server connectivity (API / signaling / media) |

`NetworkCheckStatus` (check status):

| Constant | Value | Description |
| --- | --- | --- |
| `OK` | `ok` | Overall: everything is normal |
| `PASS` | `pass` | Item: passed |
| `WARNING` | `warning` | At risk but usable |
| `FAIL` | `fail` | Failed |
| `SKIPPED` | `skipped` | Item: no check needed |
| `UNSUPPORTED` | `unsupported` | Item: not supported on the current device |

`NetworkCheckReason` (reason codes):

| Constant | Value | Description |
| --- | --- | --- |
| `NO_PERMISSION` | `no_permission` | Network permission not granted |
| `CELLULAR_RESTRICTED` | `cellular_restricted` | The system restricts background or cellular data |
| `OFFLINE` | `offline` | No network connection |
| `MTU_TOO_SMALL` | `mtu_too_small` | 1200-byte probe packets don't get through, but the media server is reachable |
| `UDP_BLOCKED` | `udp_blocked` | Media UDP is blocked |
| `DNS_FAILED` | `dns_failed` | DNS resolution failed |
| `API_UNREACHABLE` | `api_unreachable` | The check information API is unreachable (including when the server doesn't support the pre-call network check) |
| `SERVER_INFO_UNAVAILABLE` | `server_info_unavailable` | Server check information is unavailable; checks that depend on it are `skipped` |
| `SIGNAL_UNREACHABLE` | `signal_unreachable` | The signaling server is unreachable |
| `VENDOR_NOT_SUPPORTED` | `vendor_not_supported` | Media checks aren't needed for the current streaming engine |
| `MEDIA_UNAVAILABLE` | `media_unavailable` | The server has no available media node |
| `DF_NOT_SUPPORTED` | `df_not_supported` | The system doesn't allow setting Don't Fragment, so the MTU check isn't available |
