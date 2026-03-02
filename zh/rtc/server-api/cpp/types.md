### RTCClientOptions
```cpp
struct RTCClientOptions
{
    const char* domain = nullptr;   //服务器地址
    const char* appId = nullptr;    //AppID
    const char* appKey = nullptr;    //ClientKey
    const char* netId = nullptr;     //客户端所处的网络ID
    const char* sgId = nullptr;       //分组id
    TerminalType terminalType = TerminalType::Unknown;  //终端类型
    const char* terminalDesc = nullptr;           //终端类型描述
    uint32_t terminalDescSize = 0;               //终端类型描述字符串的字节数
    const char* logPath = nullptr;  //日志文件存放目录
    LogLevel logLevel = LogLevel::Trace;  //日志打印级别
};
```

### Stream
```json

{
  id:0,   //轨道号， 0-7  
  type:0,  //自定义类型
  
  codecType:0,  //编码类型
  mediaType:0,  //媒体类型
  
  width:1280,  //视频宽度 
  height:720,  //视频高度
  fps:25,    //视频帧率，填固定值即可
  bitrate:1024*1240,  //视频码率，填固定值即可 Bps
  angle:0,   //视频角度
 
  prop:{}  //自定义属性
}

enum class CodecType
{
  H264 = 0x1b,
  H265 = 0x24,
  AAC = 0x0f,
  OPUS = 0x5355504f,
};

enum class MediaType
{
  Data = 0,
  Video = 1,
  Audio = 2,
};
```



### User
```json
{
  id:"",        //用户ID
  name:"",     //用户名称
  avatar:"",    //用户头像地址
  props:{}    //自定义属性
}
```

### RoomUser
```typescript

{
  id:"",        //用户ID
  name:"",     //用户名称
  avatar:"",    //用户头像地址
  props:{},    //自定义属性
    
  linkId:"",    //流媒体连接ID
  role:0,     //角色
  streams:[]  //发布的码流  Stream[]
}

  
enum class UserRole
{
  Default = 0,
  Audience = 1,
};
```

### Room
```typescript
{
  id:"",   //房间id
  linkId:"",  //流媒体连接id
  props:{}   //自定义属性
}
```



