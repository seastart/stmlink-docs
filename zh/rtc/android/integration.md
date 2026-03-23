---
title: "集成"
description: "Android SRTC 音视频 SDK 环境配置与依赖安装"
---

# 集成

本文说明 Android SRTC SDK 的最小接入方式。完成本页后，可继续参考 [快速开始](./quickstart.md) 完成 SDK 初始化、加入频道、采集发布与远端订阅流程。

## 接入前确认

基于当前工作区中的 `rtc-android` 示例工程，建议接入前先确认以下环境条件：

- **AndroidX**：示例工程已启用 `android.useAndroidX=true`。
- **最低系统版本**：示例工程的 `minSdk` 为 `24`。
- **编译目标版本**：示例工程的 `compileSdk` / `targetSdk` 为 `35`。
- **Gradle 仓库配置方式**：优先使用 `settings.gradle`（Gradle 7+）配置仓库；旧项目可继续使用根目录 `build.gradle`。

## 配置 Maven 仓库

如果你的项目使用的是 **Gradle 7+**，建议在根目录 `settings.gradle` 中添加仓库：

```groovy
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```

如果你的项目仍使用旧版 Gradle 结构，也可以在根目录 `build.gradle` 中这样添加：

```groovy
allprojects {
    repositories {
        google()
        mavenCentral()
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```

## 添加 SDK 依赖

在业务模块的 `build.gradle`（通常是 `app/build.gradle`）中添加依赖：

```groovy
dependencies {
    implementation 'cn.seastart.rtc:rtc:<version>'
}
```

其中：

- `groupId`：`cn.seastart.rtc`
- `artifactId`：`rtc`
- `version`：请替换为你要接入的 SDK 版本

当前工作区中的 `rtc-android` 示例工程使用的版本号示例为：

```groovy
dependencies {
    implementation 'cn.seastart.rtc:rtc:2.0.6-alpha.9'
}
```

## 接入说明

开始编码前，建议同步确认以下事项：

- **运行时权限**：如果业务中需要采集音视频，请在应用侧主动申请 `CAMERA` 和 `RECORD_AUDIO` 权限。
- **ABI 兼容性**：当前工作区中的 SDK 工程包含 `arm64-v8a` 配置，如业务应用限制 ABI，请在接入前确认目标设备兼容性。
- **后续流程**：依赖接入完成后，请继续参考 [快速开始](./quickstart.md) 完成 `RTCEngine.create(...)`、`initSDK()`、加入频道、发布与订阅等流程；如果需要管理扬声器、听筒、蓝牙耳机等输出设备，可继续参考 [音频路由使用](./音频路由使用.md)。

