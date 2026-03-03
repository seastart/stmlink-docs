---
title: "集成"
description: "Android SMeeting 会议 SDK 环境配置与 SDK 安装指南"
---

# 远程依赖
在根目录下的 build.gradle 中，添加 maven

```plain
allprojects {
    repositories {
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```kotlin



在app目录下的build.gradle中添加依赖

```plain

	dependencies {
    implementation 'cn.seastart.meeting:meeting:xxx'
	}
```

