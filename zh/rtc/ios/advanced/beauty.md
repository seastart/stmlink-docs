---
title: "视频美颜"
description: "iOS SRTC 音视频 SDK 视频渲染与美颜组件集成"
---

### step 1：**加载视频渲染组件**
使用视频渲染组件密钥加载并初始化美颜服务可设置日志等级，建议程序启动时对视频渲染组件进行装载。

```objectivec
/// 装载视频渲染组件
/// @param authData 密钥
/// @param authDataSize 密钥长度
/// @param logLevel 日志等级
[[RTCEngineKit sharedEngine] installRenderModule:g_auth_package authDataSize:sizeof(g_auth_package) logLevel:RTCEngineLogLevelError];
```

### step 2：**美颜效果参数设置**
当前视频渲染组件只提供基础美颜效果，加载视频渲染组件之后，可通过以下属性来设置相应的美颜效果：

| **属性名** | **类型** | **说明** |
| --- | :---: | --- |
| blurLevel | float | 磨皮等级，取值范围 0.0-1.0，默认0.5 |
| whiteLevel | float | 美白等级，取值范围 0.0-1.0，默认值0.3 |
| redLevel | float | 红润等级，取值范围 0.0-1.0，默认值0.3 |
| sharpenLevel | float | 锐化等级，取值范围 0.0-1.0，默认0.3 |
| filterLevel | float | 滤镜等级，取值范围 0.0-1.0，默认值0.8 |
| filterName | NSString | 滤镜效果，默认值为 “origin” ，origin即为使用原图效果 |


当前视频渲染组件支持以下滤镜效果：

| **滤镜效果** | **说明** |
| --- | --- |
| origin | 原图效果 |
| bailiang1 | 白亮1 |
| bailiang2 | 白亮2 |
| bailiang3 | 白亮3 |
| bailiang4 | 白亮4 |
| bailiang5 | 白亮5 |
| bailiang6 | 白亮6 |
| bailiang7 | 白亮7 |
| fennen1 | 粉嫩1 |
| fennen2 | 粉嫩2 |
| fennen3 | 粉嫩3 |
| fennen4 | 粉嫩4 |
| fennen5 | 粉嫩5 |
| fennen6 | 粉嫩6 |
| gexing1 | 个性1 |
| gexing2 | 个性2 |
| gexing3 | 个性3 |
| gexing4 | 个性4 |
| gexing5 | 个性5 |
| gexing6 | 个性6 |
| gexing7 | 个性7 |
| gexing10 | 个性10 |
| gexing11 | 个性11 |
| heibai1 | 黑白1 |
| heibai2 | 黑白2 |
| heibai3 | 黑白3 |
| heibai4 | 黑白4 |
| lengsediao1 | 冷色调1 |
| lengsediao2 | 冷色调2 |
| lengsediao3 | 冷色调3 |
| lengsediao4 | 冷色调4 |
| lengsediao5 | 冷色调5 |
| lengsediao6 | 冷色调6 |
| lengsediao7 | 冷色调7 |
| lengsediao8 | 冷色调8 |
| lengsediao11 | 冷色调11 |
| nuansediao1 | 暖色调1 |
| nuansediao2 | 暖色调2 |


### step 3：**设置美颜功能开关**
加载视频渲染组件之后默认开启美颜功能，程序中途预想开启或关闭美颜效果可通过一下接口实现：

```objectivec
/// 美颜功能开关
/// @param enabled YES-开启美颜 NO-关闭美颜
[[RTCEngineKit sharedEngine] enabledBeauty:YES];
```

### step 4：**卸载视频渲染组件**
```objectivec
/// 卸载视频渲染组件
[[RTCEngineKit sharedEngine] uninstallRenderModule];
```

