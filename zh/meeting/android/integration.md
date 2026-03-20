---
title: "集成"
description: "Android SMeeting 会议 SDK 环境配置与 SDK 安装指南"
---

# 集成

本文说明 Android SMeeting SDK 的最小接入方式。完成本页后，可继续参考 [快速开始](./quickstart.md) 完成 SDK 初始化、创建会议与入会流程。

## 配置 Maven 仓库

当前工作区内的 Android 工程使用的是 **Gradle 7+ / `settings.gradle`** 写法，建议优先按下面方式配置仓库：

```groovy
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
        mavenLocal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
        mavenLocal()
    }
}
```

如果你的项目还是旧版 Gradle 结构，也可以在根目录 `build.gradle` 中这样添加：

```groovy
allprojects {
    repositories {
        google()
        mavenCentral()
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
        mavenLocal()
    }
}
```

## 添加 SDK 依赖

在业务模块的 `build.gradle`（通常是 `app/build.gradle`）中添加依赖：

```groovy
dependencies {
    implementation 'cn.seastart.meeting:meeting:<version>'
}
```

其中：

- `groupId`：`cn.seastart.meeting`
- `artifactId`：`meeting`
- `version`：请替换为你要接入的 SDK 版本

当前工作区内 `meeting-android` 工程使用的版本号示例为：

```groovy
dependencies {
    implementation 'cn.seastart.meeting:meeting:2.0.27-alpha.7'
}
```

## 接入说明

开始编码前，建议同步确认以下事项：

- **AndroidX**：当前示例工程已启用 `android.useAndroidX=true`。
- **最低系统版本**：当前示例工程的 `minSdk` 为 `24`。
- **运行时权限**：如果业务中需要打开摄像头和麦克风，请在应用侧处理相机、录音等运行时权限。
- **初始化流程**：添加依赖后，请继续参考 [快速开始](./quickstart.md) 完成 `MeetingEngine.create(...)`、`initSdk(...)` 和入会流程。

