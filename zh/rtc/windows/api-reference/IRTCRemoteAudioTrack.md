## 函数说明
远端音频混音对象。



## 继承关系
[IRTCTrack](https://www.yuque.com/anyconf/rtcengine/fkp5s07gsry40a9i) ->IRTCRemoteAudioTrack





## 函数方法
### 开启音频输出
```cpp
virtual StatusCode startPlay(RTCAudioOutputOptions* opt = nullptr) = 0;
```

**参数**

| opt | 音频轨道输出信息[查看](https://www.yuque.com/anyconf/rtcengine/rhsp7k#aqSxT) |
| --- | --- |




### 停止音频输出
```cpp
virtual StatusCode stopPlay() = 0;
```



