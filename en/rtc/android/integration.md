---
title: "Integration"
description: "Set up an Android project for the SRTC SDK: environment requirements (AndroidX, minSdk 24, compileSdk 35), Maven repository and dependency configuration, runtime permissions, ABIs, background microphone capture, and video rendering views. Read before writing any Android SRTC code."
---

This page describes the minimal way to integrate the Android SRTC SDK. After finishing it, continue with [Quickstart](/en/rtc/android/quickstart) to initialize the SDK, join a channel, capture and publish, and subscribe to remote users.

## Before you start

Based on the official sample project, confirm the following environment requirements before integrating:

- **AndroidX**: the sample project enables `android.useAndroidX=true`.
- **Minimum OS version**: the sample project's `minSdk` is `24`.
- **Compile and target version**: the sample project's `compileSdk` / `targetSdk` is `35`.
- **Gradle repository configuration**: prefer configuring repositories in `settings.gradle` (Gradle 7+); older projects can keep using the root `build.gradle`.

## Configure the Maven repository

If your project uses **Gradle 7+**, add the repository to the root `settings.gradle`:

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

If your project still uses the older Gradle structure, you can add it to the root `build.gradle` instead:

```groovy
allprojects {
    repositories {
        google()
        mavenCentral()
        maven { url 'https://maven.open.seastart.cn/repository/maven-vcs/' }
    }
}
```

## Add the SDK dependency

Add the dependency to your app module's `build.gradle` (usually `app/build.gradle`):

```groovy
dependencies {
    implementation 'cn.seastart.rtc:rtc:<version>'
}
```

Where:

- `groupId`: `cn.seastart.rtc`
- `artifactId`: `rtc`
- `version`: replace with the SDK version you want to integrate

Example using the current stable version:

```groovy
dependencies {
    implementation 'cn.seastart.rtc:rtc:2.0.36'
}
```

## Integration notes

Before you start coding, also confirm the following:

- **Runtime permissions**: if your app captures audio and video, request the `CAMERA` and `RECORD_AUDIO` permissions in your app.
- **ABI compatibility**: the SDK currently supports `arm64-v8a` and `armeabi-v7a`; include the ABIs that match your target devices.
- **Background microphone capture**: capture is decoupled from joining and publishing. If you need to keep calling `LocalMicTrack.startCapture(...)` in the background, configure a microphone-type foreground service and the related permissions as required by your Android version.
- **Next steps**: after adding the dependency, continue with [Quickstart](/en/rtc/android/quickstart) for `RTCEngine.create(...)`, `initSDK()`, joining a channel, publishing, and subscribing. To manage output devices such as the speaker, earpiece, and Bluetooth headsets, see [Audio routing](/en/rtc/android/advanced/audio-routing).

## Media streaming and video display

+ Supports the FY (Freewind) and Wangsu media streaming services, using the vendor configuration assigned by the server.
+ For local preview and remote video display, use `VcsPlayerGlTextureView` or `VcsPlayerGlSurfaceView` from the `cn.seastart.rtc.media.original.render` package. Use the same package path in code imports and XML layouts. For usage, see [Video rendering](/en/rtc/android/api-reference/RemoteVideoTrack).
+ External video is fed through `LocalCustomVideoTrack` as unencoded I420 frames, and the SDK handles encoding and publishing. For integration, see [Custom tracks](/en/rtc/android/advanced/custom-track).
