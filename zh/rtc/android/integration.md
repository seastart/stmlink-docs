---
title: "集成"
description: "Android SRTC 音视频 SDK 环境配置与依赖安装"
---

在项目根目录 `build.gradle`（或 `settings.gradle` 的仓库配置）中添加 Maven 仓库：

```gradle
allprojects {
    repositories {
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```

在 App 模块中添加依赖：

```gradle
dependencies {
    implementation 'cn.seastart.rtc:rtc:xxx'
}
```
