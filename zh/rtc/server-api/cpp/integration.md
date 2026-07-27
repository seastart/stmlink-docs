---
title: "集成"
description: "全平台 C++ SRTC 音视频 SDK 环境配置与 SDK 安装指南"
---

### 头文件
`#include<rtc-linux.h>`

### 库文件
librtc-linux.so

linkmic_service.so

### 第三方库
zlib

openssl

curl

### 其他
linkmic_service.so 在运行过程中动态加载，需要设置SO查找路径，或者放入系统目录。

```bash
export LD_LIBRARY_PATH=./
```



