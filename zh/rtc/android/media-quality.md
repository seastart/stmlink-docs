### Metric
质量监测数据类

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| localAudios | MutableMap | 本地音频信息统计<br/>key：UserTrackDesc；<br/>value：[AudioSenderStats](#MB8TV) |
| localVideos | MutableMap | 本地视频信息统计<br/>key：UserTrackDesc<br/>value：[VideoSenderStats](#FsVir) |
| remoteAudios | MutableMap | 远端音频信息统计<br/>key：UserTrackDesc<br/>value：[AudioReceiverStats](#qTngM) |
| remoteVideos | MutableMap | 远端视频信息统计<br/>key：UserTrackDesc<br/>value：[VideoReceiverStats](#L2yco) |
| localUploadStats | [LocalUploadStats](#XwMxq) | 本地上传信息统计 |
| remoteDownloadStats | MutableMap | 远端下载信息统计<br/>Key：uid<br/>value：[RemoteDownloadStats](#mBM7l) |
| networkStats | [NetworkStats](#wn1qC) | 网络状态统计 |


### AudioSenderStats
音频发送状态

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| trackId | String | 轨道 id |
| packetsSent | Long | 发送的包数 |
| byteSent | Long | 发送的字节数 |
| bitrateSent | Float | 发送的码率 kb/s |
| jitter | Float | 网络抖动，单位秒 |
| packetsLost | Int | 丢失的包数，没有减去重传的包数 |
| roundTripTime | Float | 往返延时，单位 秒 |
| mimeType | String | 当前媒体使用的编解码器类型 |
| timestamp | Long | 时间戳，单位毫秒 |
| type | String | 媒体类型 |
| audioLevel | Float | 音频能量 |


### VideoSenderStats
视频发送状态

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| trackId | String | 轨道 id |
| packetsSent | Long | 发送的包数 |
| byteSent | Long | 发送的字节数 |
| bitrateSent | Float | 发送的码率 kb/s |
| jitter | Float | 网络抖动，单位秒 |
| packetsLost | Int | 丢失的包数，没有减去重传的包数 |
| roundTripTime | Float | 往返延时，单位 秒 |
| mimeType | String | 当前媒体使用的编解码器类型 |
| timestamp | Long | 时间戳，单位毫秒 |
| type | String | 媒体类型 |
| firCount | Long | 用于衡量传输过程中的纠错机制被触发的频率，请求发送 I 帧的请求数 |
| pliCount | Long | 用于衡量传输过程中的纠错机制被触发的频率，请求发送 P 帧的请求数 |
| nackCount | Long | 用于衡量传输过程中的纠错机制被触发的频率，请求重传丢失的RTP包的请求数 |
| rid | String | 当启用 Simulcast（多分辨率编码）时，发送端会同时发送多个分辨率的 RTP 流，每个流会用一个唯一的 rid 标识 |
| frameWidth | Int | 视频帧的宽度 |
| frameHeight | Int | 视频帧的高度 |
| framesPerSecond | Float | 视频帧率 |
| frameSent | Long | 视频帧数 |
| qualityLimitationReason | String | 当前限制视频质量的主要原因<br/>none、cpu、bandwidth、other、inactive |
| qualityLimitationDurations | Map<String, Float> | 每种原因导致的总限制时长（单位秒） |
| qualityLImitationResolutionChange | Long | 分辨率因质量限制而发生改变的次数 |
| retransmittedPacketsSent | Long | 已经重传的 RTP 包数，只有视频存在该数据 |
| targetBitrate | Float | 编码器当前的目标比特率，单位（比特每秒 bps） |


### AudioReceiverStats
音频接收状态

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| trackId | String | 轨道 id |
| packetsReceived | Long | 接收包数 |
| bytesReceived | Long | 接收字节数 |
| bitrateReceived | Float | 接收的码率 kb/s |
| jitter | Float | 网络抖动，单位秒 |
| jitterBufferDelay | Float | 由于网络抖动，媒体包在 jitter buffer（抖动缓冲区）中总共的延迟时间。这个指标能反映网络抖动对实际播放的影响程度<br/>单位 秒 |
| packetsLost | Int | 丢包数，没有减去重传的包数 |
| mimeType | String | 当前媒体使用的编解码器类型 |
| timestamp | Long | 时间戳，单位毫秒 |
| audioLevel | Float | 音频能量 |
| concealedSamples | Long | 补偿恢复的音频样本总数(采样点) |
| concealEvents | Long | 发生插值操作的的次数 |
| silentConcealedSamples | Long | 因为丢包或抖动被插补为静音的音频采样数量 |
| silentConcealmentEvents | Long | 发生了多少次“静音补偿”的事件 |
| totalAudioEnergy | Double | 累计的接收音频信号能量总和 |
| totalSamplesDuration | Double | 累计接收音频的播放时长, 单位秒 |


### VideoReceiverStats
视频接收状态

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| trackId | String | 轨道 id |
| packetsReceived | Long | 接收包数 |
| bytesReceived | Long | 接收字节数 |
| bitrateReceived | Float | 接收的码率 kb/s |
| jitter | Float | 网络抖动，单位秒 |
| jitterBufferDelay | Float | 由于网络抖动，媒体包在 jitter buffer（抖动缓冲区）中总共的延迟时间。这个指标能反映网络抖动对实际播放的影响程度<br/>单位 秒 |
| packetsLost | Int | 丢包数，没有减去重传的包数 |
| mimeType | String | 当前媒体使用的编解码器类型 |
| timestamp | Long | 时间戳，单位毫秒 |
| framesDecoded | Long | 成功解码的视频总帧数 |
| framesDropped | Long | 解码过程中被丢弃的帧数 |
| framesReceived | Long | 接收到的视频总帧数 |
| framesPerSecond | Float | 接收视频帧的帧率，单位 fps |
| frameWidth | Int | 接收视频帧的宽度 |
| frameHeight | Int | 接收视频帧的高度 |
| firCount | Int | 用于衡量传输过程中的纠错机制被触发的频率，请求发送 I 帧的请求数。 |
| pliCount | Int | 用于衡量传输过程中的纠错机制被触发的频率，请求发送 P 帧的请求数 |
| nackCount | Int | 用于衡量传输过程中的纠错机制被触发的频率，请求重传丢失的RTP包的请求数 |
| retransmittedPacketsReceived | Long | 已经重传的 RTP 包数，只有视频存在该数据 |
| decoderImplementation | String | 前使用的视频 解码器实现名称 |


### LocalUploadStats
本地上传信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 uid |
| delay | Float | 上传延时 |
| videoBitrate | Float | 视频上传码率 kb/s |
| audioBitrate | Float | 音频上传码率 kb/s |
| lossrate | Float | 丢包率 |


### RemoteDownloadStats
远端下载信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| uid | String | 用户 uid |
| audioPacketsReceived | Long | 接收的音频包数 |
| videoPacketsReceived | Long | 接收的视频包数，包含重传的包数 |
| packetsLost | Long | 丢包数 |
| retransmittedPackets | Long | 重传包数，只有视频有重传包 |
| lossrate | Float | 丢包率 |
| downLevel | MediaDownLevel | 下行等级 |
| audioBitrate | Float | 音频码率 kb/s |
| videoBitrate | Float | 视频码率 kb/s |


### NetworkStats
网络状态信息

| 属性名称 | 数据类型 | 说明 |
| --- | --- | --- |
| bitrateUp | Float | 上行码率 kb/s |
| bitrateDown | Float | 下行码率 kb/s |
| delay | Float | 延迟 ms |
| lossrateUp | Float | 上行丢包率 |
| lossrateDown | Float | 下行丢包率 |
| upLevel | MediaUploadLevel | 上行等级 |
| downLossLevel | MediaDownLossLevel | 下行丢包等级 |
| pktUp | Long | 上行包数 |
| pktDown | Long | 下行包数 |
| pktLossUp | Long | 上行丢包数 |
| pktLossDown | Long | 下行丢包数 |


