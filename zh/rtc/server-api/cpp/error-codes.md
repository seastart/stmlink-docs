| **枚举名** | **枚举值** | **说明** |
| --- | :---: | --- |
| OK | `0` | 无错误 |
| **系统级错误码** | | |
| SystemError | `1` | 系统内部错误 |
| NotInitialized | `2` | 未初始化 |
| MediaNotInitialized | `3` | 媒体模块尚未初始化 |
| VideoCapturerError | `100` | 外部视频设备失败 |
| AudioCapturerError | `101` | 外部音频设备失败 |
| AudioPlayerError | `102` | 外部扬声器失败 |
| ProtocolParsingError | `200` | 协议解析失败 |
| **通用错误码** | | |
| Timeout | `1000` | 超时 |
| InvalidArgs | `1001` | 参数错误 |
| Conflict | `1002` | 重复操作 |
| NotFound | `1100` | 查找的资源不存在 |
| UserNotFound | `1101` | 用户不存在 |
| RoomNotFound | `1102` | 房间不存在 |
| StreamNotFound | `1103` | 码流不存在 |
| **网络类错误码** | | |
| NetError | `2000` | 网络错误 |
| MediaNetError | `2001` | 媒体网络错误 |
| **应用相关错误码** | | |
| InvalidAppId | `3001` | 无效的AppID |
| ApiSignatureError | `3002` | 签名错误 |
| ApiTimestampError | `3003` | Api请求时间戳错误 |
| **权限类错误码** | | |
| Unauthorized | `4000` | 操作未授权 |
| Forbidden | `4001` | 操作不允许 |
| ConcLimited | `4002` | 并发不足 |
| **服务端错误码** | | |
| ServerError | `5000` | 服务器内部错误 |
| MQTTServerLess | `5010` | MQTT服务器资源不足 |
| MQTTServerLineLess | `5011` | MQTT没有服务器线路 |
| UploadServerLess | `5020` | 流媒体服务器资源不足 |
| UploadServerLineLess | `5021` | 流媒体没有服务器线路 |
| UploadWebRtcLess | `5022` | 流媒体服务器绑定的WebRTC网关不足 |
| UploadRtmpLess | `5023` | 流媒体服务器绑定的RTMP网关不足 |
| WebRtcServerLess | `5030` | WebRTC服务器资源不足 |
| WebRtcServerLineLess | `5031` | WebRTC没有服务器线路 |
| RTMPServerLess | `5040` | RTMP服务器资源不足 |
| RTMPServerLineLess | `5041` | RTMP没有服务器线路 |
| **第三方自定义错误码** | | |
| ThirdPartyRefused | `100000` | 第三方平台鉴权错误 |


