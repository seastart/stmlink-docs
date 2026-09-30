---
title: "Types"
description: "Field and enum reference for the iOS (Objective-C) SRTC SDK: engine, user, track, channel, media, QoS, debug, and speed test models, stream statistics and quality samples, plus enums such as RTCLeaveReason, RTCCodecType, and RTCAudioRoute. Read when you need the meaning of a field or enum value."
---

### RTCEngineConfig
RTC initialization configuration

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| NSString *logPath | No | Log file path |
| BOOL enableLocalLog | No | Whether to enable local logging. Default: NO |


### RTCEngineUserModel
User info

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| NSString *appId | Yes | App ID |
| NSString *userId | Yes | User ID |
| NSString *sessionId | Yes | Session ID |
| NSString *name | Yes | User name |
| [SRTCDeviceType](/en/rtc/ios/types#srtcdevicetype) deviceType | Yes | Device type. Default: `SRTCDeviceTypeIOS` |
| NSString *deviceId | Yes | Device ID |
| NSString *version | Yes | Component version |
| NSString *netid | Yes | Network ID |
| NSString *sgid | Yes | Group ID |
| NSString *channel | Yes | Channel name |
| int linkId | Yes | Connection ID (media streaming) |
| NSString *sessionKey | Yes | Session key (media streaming) |
| NSString *uploadId | Yes | Media streaming service ID |
| BOOL isAudience | Yes | Whether the user is in audience mode |
| NSInteger joinAt | No | Join time |
| NSInteger updatedAt | No | Update time |
| NSInteger leaveAt | No | Leave time |
| NSMutableArray &lt;[RTCEngineStreamTrackModel](#rtcenginestreamtrackmodel) \*&gt; \*streamTracks | No | Stream track list |
| id props | No | Custom properties |


### RTCEngineStreamTrackModel
Stream track info

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| NSString *streamId | Yes | Stream ID |
| NSString *desc | Yes | Stream description |
| [RTCStreamTrackKind](#rtcstreamtrackkind) kind | Yes | Stream kind |
| [RTCCodecType](#rtccodectype) codecType | Yes | Codec type |
| int width | Yes | Resolution width |
| int height | Yes | Resolution height |
| int fps | Yes | Video frame rate |
| int bitrate | Yes | Video bitrate, in kbps |
| int angle | Yes | Video angle |
| int sampleRate | No | Audio sample rate |
| [RTCTrackIdentifierFlags](#rtctrackidentifierflags) track | Yes | Track number |
| `NSArray<NSString *> *fallbackIds` | No | Lower-layer tracks the current layer can fall back to. Only with the SeaStart engine |
| BOOL variant | No | Whether this is a simulcast secondary layer. Only with the SeaStart engine |
| id props | No | Custom properties |


### RTCEngineChannelModel
Channel info

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| NSString *appId | Yes | App ID |
| NSString *channel | Yes | Channel name |
| int linkId | Yes | Connection ID (media streaming) |
| int maxUser | Yes | Maximum number of users in the channel |
| int maxAudio | Yes | Maximum number of audio streams forwarded in the channel |
| int maxPeer | Yes | Maximum number of streams that can be forwarded per user in the channel |
| int maxVideo | Yes | Maximum number of video streams that can be forwarded per user in the channel |
| NSInteger createdAt | No | Creation time |
| NSInteger updatedAt | No | Update time |
| id props | No | Custom properties |


### RTCEngineMediaConfig
Media streaming configuration

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| int aec | No | Acoustic echo cancellation (AEC). Default: 12 |
| int agc | No | Automatic gain control (AGC). Default: 16000 |
| int audioSampe | No | Audio sample rate. Default: 48000 |
| [RTCCodecType](#rtccodectype) audioEncode | No | Audio encoding format. Default: AAC |
| [RTCAudioRoute](#rtcaudioroute) audioRoute | No | Default built-in audio route when no external device is connected; speaker or earpiece. Default: RTCAudioRouteSpeaker |
| int videoWidth | No | Resolution width. Default: 480 |
| int videoHeight | No | Resolution height. Default: 640 |
| BOOL videoMirror | No | Video mirroring. Default: YES |
| int fps | No | Video frame rate. Default: 25 |
| int bitrate | No | Video bitrate, in kbps. Default: 0.9*1024 |


### RTCEngineNetworkQosParam
Network quality control parameters

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| int secondGear | No | Second level of receive-side adaptive latency. Default: 500 |
| int thirdGear | No | Third level of receive-side adaptive latency. Default: 1200 |
| float onAudioCycle | No | Interval for fetching cloud audio data info. Default: 500 ms |
| BOOL isHardwarede | No | Enable hardware decoding. YES: on; NO: off. Default: YES |
| BOOL isNetworkAdaptive | No | Enable network adaptive latency. YES: on; NO: off. Default: YES |
| BOOL isBitrateAdaptive | No | Enable adaptive bitrate. YES: on; NO: off. Default: YES |
| [RTCNetworkQosShakeLevel](#rtcnetworkqosshakelevel) shakeLevel | No | Anti-jitter level for network latency. Default: RTCNetworkQosShakeLevelMedium |


### RTCEngineDebugParam
Debug mode parameters

| **Property** | **Required** | **Description** |
| :--- | :---: | --- |
| NSString *debugHost | No | Remote debugging address |
| BOOL enableSaveVideo | No | Save the video stream. Default: NO |
| BOOL enableSaveAudioCapture | No | Save the captured audio stream. Default: NO |
| BOOL enableSaveAudioReceive | No | Save the remote audio stream. Default: NO |


### RTCSpeedTestParams
Speed test parameters

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| int linkId | Yes | Connection ID (media streaming) |
| NSString *streamHost | Yes | Media streaming service address |
| int streamPort | Yes | Media streaming service port |
| int expectedUpBandwidth | No | Expected uplink bandwidth. Default: 2000 kbps. Set to 0 to skip the uplink test |
| int expectedDownBandwidth | No | Expected downlink bandwidth. Default: 2000 kbps. Set to 0 to skip the downlink test |
| int duration | No | Test duration. Default: 30 s |


### RTCSpeedTestResult
Speed test result

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| NSInteger recv | No | Total packets received/sent |
| NSInteger miss | No | Out-of-order count |
| NSInteger losf | No | Packets lost |
| NSInteger speed | No | Rate/bitrate (kbps) |
| NSInteger delay | No | Network latency |
| float dropRate | No | Packet loss rate |
| [RTCNetworkState](#rtcnetworkstate) state | No | Network condition |


### RTCSpeedTestConnectResult
Speed test connection status result

| **Property** | **Required** | **Description** |
| :--- | :---: | --- |
| NSInteger delay | No | Network round-trip latency |
| BOOL internetConnect | No | Internet connectivity. YES: normal; NO: abnormal |
| BOOL streamConnect | No | Media streaming connectivity. YES: normal; NO: abnormal |
| BOOL signalingConnect | No | Channel control service connectivity. YES: normal; NO: abnormal |


### RTCStreamAudioModel
User audio info

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| NSString *userId | No | User ID. Nullable since `3.0.0` |
| int linkId | Yes | Connection ID (media streaming). With Wangsu media streaming the server doesn't send this value, so it's always `0` |
| NSInteger power | No | Audio power |
| NSInteger db | No | Audio decibel value |

> Note: To identify the speaking user, use `userId` directly; don't look up the user by `linkId`. With Wangsu media streaming, `linkId` is always `0` for every user, so a lookup by it is bound to hit the wrong person. Since `3.1.2`, the SDK resolves `userId` from the underlying connection on this path.


### RTCStreamSendModel
Media streaming send status

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| int buffer | No | Upload buffer packet count |
| int delay | No | Upload latency |
| int overflow | No | Overflowed buffer packet count |
| NSString *speed | No | Upload rate (in kbps) |
| NSInteger status | No | Upload status |
| float loss_r | No | Packet loss rate before compensation |
| float loss_c | No | Packet loss rate after compensation |


### RTCStreamReceiveModel
Media streaming receive status

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| NSString *userId | No | User ID. Nullable since `3.0.0` |
| int linkId | Yes | Connection ID (media streaming) |
| int recv | No | Packets received |
| int comp | No | Compensated packets |
| int losf | No | Total packets lost |
| float lrl | No | End-to-end packet loss rate |
| float lrd | No | Server-to-client packet loss rate |
| int audio | No | Audio packet count |
| int video | No | Video packet count |


### RTCStreamQualitySampleModel
Media streaming quality sample data. Only with the SeaStart engine 

| **Property** | **Required** | **Description** |
| --- | :---: | --- |
| NSInteger score | Yes | Overall score (0–100) |
| RTCStreamQualityLevel level | Yes | Quality level |
| double mos | Yes | Voice MOS value |
| double loss | Yes | Packet loss rate (0–1) |
| double rtt | Yes | Round-trip time (ms) |
| double jitter | Yes | Jitter (ms) |
| NSInteger packets | Yes | Packet count |
| NSInteger bitrate | Yes | Bitrate (bps) |
| NSInteger bytes | Yes | Byte count |


### RTCEngineLogLevel
Log level

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCEngineLogLevelTrace | `0` | All logs |
| RTCEngineLogLevelDebug | `1` | DEBUG, INFO, WARN, ERROR, and CRITICAL logs |
| RTCEngineLogLevelInfo | `2` | INFO, WARN, ERROR, and CRITICAL logs |
| RTCEngineLogLevelWarn | `3` | WARN, ERROR, and CRITICAL logs |
| RTCEngineLogLevelError | `4` | ERROR and CRITICAL logs |
| RTCEngineLogLevelCritical | `5` | CRITICAL logs |
| RTCEngineLogLevelOff | `6` | No logging |


### SRTCDeviceType
Device type

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| SRTCDeviceTypeUnknown | `0` | Unknown client |
| SRTCDeviceTypeWindows | `1` | Windows |
| SRTCDeviceTypeAndroid | `2` | Android |
| SRTCDeviceTypeIOS | `3` | iOS |
| SRTCDeviceTypeLinux | `4` | Linux |
| SRTCDeviceTypeMacOS | `5` | MacOS |
| SRTCDeviceTypeWebRTC | `6` | WebRTC |
| SRTCDeviceTypeRtmp | `7` | RTMP |
| SRTCDeviceTypeHarmonyOS | `8` | HarmonyOS |


### RTCUserRole
User role

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCUserRoleDefault | `0` | Regular user |
| RTCUserRoleAudience | `1` | Audience |


### RTCMediaType
Media type

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCMediaTypeData | `0` | Data |
| RTCMediaTypeVideo | `1` | Video |
| RTCMediaTypeAudio | `2` | Audio |


### RTCStreamType
Media stream type

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCStreamTypeAudio | `0` | Audio stream |
| RTCStreamTypeVideo | `1` | Video stream |


### RTCCodecType
Codec type

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCCodecTypeUnknown | `0` | Unknown |
| RTCCodecTypeH264 | `0x1b` | H264 |
| RTCCodecTypeH265 | `0x24` | H265 |
| RTCCodecTypeAAC | `0x0f` | AAC |
| RTCCodecTypeOPUS | `0x5355504f` | OPUS |


### RTCChangeType
Change operation type

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCChangeTypeNone | `0` | No operation |
| RTCChangeTypeUpdate | `1` | Update |
| RTCChangeTypeAppend | `2` | Add |
| RTCChangeTypeRemove | `3` | Remove |


### RTCLeaveReason
Reason for leaving the channel

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCLeaveReasonError | `-1` | An error occurred |
| RTCLeaveReasonNormal | `1` | Left voluntarily |
| RTCLeaveReasonKickout | `2` | Removed from the channel |
| RTCLeaveReasonReplaced | `3` | Replaced by another session with the same uid |
| RTCLeaveReasonTimeout | `4` | Left due to heartbeat timeout |
| RTCLeaveReasonDestroy | `5` | Left because the channel was destroyed |
| RTCLeaveReasonAudience | `6` | Switched to audience |


### RTCImDisconnectReason
Disconnect reason for IM (out-of-channel messaging)

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCImDisconnectReasonError | `-1` | An error occurred |
| RTCImDisconnectReasonNormal | `1` | Disconnected voluntarily |
| RTCImDisconnectReasonKickout | `2` | Removed from the IM service |
| RTCImDisconnectReasonTimeout | `4` | Left due to heartbeat timeout |


### RTCTrackIdentifierFlags
Stream track identifier

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCTrackIdentifierFlags0 | `0` | Track 0 |
| RTCTrackIdentifierFlags1 | `1` | Track 1 |
| RTCTrackIdentifierFlags2 | `2` | Track 2 |
| RTCTrackIdentifierFlags3 | `3` | Track 3 |
| RTCTrackIdentifierFlags4 | `4` | Track 4 |
| RTCTrackIdentifierFlags5 | `5` | Track 5 |
| RTCTrackIdentifierFlags6 | `6` | Track 6 |


### RTCNetworkState
Network condition

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCNetworkStateNormal | `0` | Good |
| RTCNetworkStatePoor | `1` | Poor |
| RTCNetworkStateBad | `2` | Bad |
| RTCNetworkStateVeryBad | `3` | Very bad |


### RTCScreenRecordStatus
Screen sharing status

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCScreenRecordStatusError | `-1` | Sharing connection error |
| RTCScreenRecordStatusStop | `0` | Sharing has stopped |
| RTCScreenRecordStatusStart | `1` | Sharing has started |


### RTCAudioRoute
Audio route type

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCAudioRouteUnknown | `0` | Invalid route |
| RTCAudioRouteSpeaker | `1` | Speaker |
| RTCAudioRouteReceiver | `2` | Earpiece |
| RTCAudioRouteBluetooth | `3` | Bluetooth headset |
| RTCAudioRouteHeadset | `4` | Wired headset |

### RTCEngineCameraDirection
Camera direction

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCEngineCameraDirectionFront | `1` | Front camera |
| RTCEngineCameraDirectionBack | `2` | Rear camera |


### RTCNetworkQosShakeLevel
Anti-jitter level for network latency

| **Constant** | **Value** | **Description** |
| --- | :---: | --- |
| RTCNetworkQosShakeLevelUltraShort | `0` | Ultra-short (0): about 120 ms one-way latency. No packet loss compensation in this mode, and B-frames are disabled in encoding. Generally not recommended for real use |
| RTCNetworkQosShakeLevelShort | `1` | Short (1): about 200 ms one-way latency. Single packet loss compensation, 1 B-frame. Usable for two-way talk |
| RTCNetworkQosShakeLevelMedium | `2` | Medium (2): about 350 ms one-way latency. Double packet loss compensation, 1 B-frame. Recommended for two-way talk |
| RTCNetworkQosShakeLevelLong | `3` | Long (3): about 600 ms one-way latency. Triple packet loss compensation, 3 B-frames. Only for one-way viewing; not recommended for two-way talk. This value can't be set dynamically |


### RTCUploadBitrateAdaptiveState
Uplink adaptive bitrate state

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCUploadBitrateAdaptiveStateStart | `1000` | Adaptive bitrate starts working |
| RTCUploadBitrateAdaptiveStateNormal | `0` | Bitrate restored to the initial setting |
| RTCUploadBitrateAdaptiveStateHalf | `-1` | Bitrate reduced to half |
| RTCUploadBitrateAdaptiveStateQuarter | `-2` | Bitrate reduced to a quarter |
| RTCUploadBitrateAdaptiveStateVeryBad | `-3` | The current network is very poor |


### RTCDownBitrateAdaptiveState
Downlink adaptive bitrate state

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCDownBitrateAdaptiveStateNormal | `0` | Normal |
| RTCDownBitrateAdaptiveStatePoor | `-1` | Poor |
| RTCDownBitrateAdaptiveStateBad | `-2` | Bad |
| RTCDownBitrateAdaptiveStateVeryBad | `-3` | Very bad |
| RTCDownBitrateAdaptiveStateLose | `-4` | Link offline |


### RTCDownLossLevelState
Downlink average packet loss level

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCDownLossLevelStateInvalid | `-1` | Invalid |
| RTCDownLossLevelStateNormal | `0` | Normal |
| RTCDownLossLevelStatePoor | `1` | Poor |
| RTCDownLossLevelStateBad | `2` | Bad |
| RTCDownLossLevelStateVeryBad | `3` | Very bad |


### RTCStreamTrackKind
Stream track kind

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCStreamTrackKindVideo | `video` | Video |
| RTCStreamTrackKindAudio | `audio` | Audio |


### RTCStreamQualityLevel
Media streaming quality level

| **Enum name** | **Value** | **Description** |
| --- | :---: | --- |
| RTCStreamQualityLevelUnknown | `0` | Unknown |
| RTCStreamQualityLevelExcellent | `1` | Excellent (`excellent`) |
| RTCStreamQualityLevelGood | `2` | Good (`good`) |
| RTCStreamQualityLevelPoor | `3` | Poor (`poor`) |
| RTCStreamQualityLevelLost | `4` | Stream lost (`lost`) |

