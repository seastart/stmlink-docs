---
title: "IRTCLocalVideoTrack"
description: "Windows SRTC 音视频 SDK IRTCLocalVideoTrack 接口参考"
---

## 函数说明
视频轨道基类，提供推流，停止推流。渲染对象绑定等操作。



## 继承关系
[IRTCTrack](./IRTCTrack.md) -> IRTCLocalVideoTrack



## 函数方法
### 添加渲染对象
```cpp
virtual StatusCode addPlayView(IRTCView* v) = 0;
```

**参数**

| v | 渲染对象类[查看](./IRTCView.md) |
| --- | --- |




### 移除渲染对象
```cpp
virtual StatusCode removePlayView(IRTCView* v) = 0;
```

**参数**

| v | 渲染对象类[查看](./IRTCView.md) |
| --- | --- |


注：移除渲染对象，如果是CallBack类型，将对比对象地址，如果是HWND 类型将对比HWND



### 移除所有渲染对象
```cpp
virtual StatusCode removePlayView() = 0;
```

