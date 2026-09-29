---
title: "Integration"
description: "Configure the Maven repository (settings.gradle or legacy build.gradle), add the cn.seastart.meeting:meeting dependency, and check AndroidX, minSdk, and runtime permission requirements for the SMeeting Android SDK. Read this before initializing the SDK."
---

This page describes the minimal setup for the Android SMeeting SDK. After finishing it, continue with [Quickstart](/en/meeting/android/quickstart) to initialize the SDK, create a meeting, and enter the meeting.

## Configure the Maven repository

The official sample project uses the **Gradle 7+ / `settings.gradle`** style. We recommend configuring repositories as follows:

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

If your project still uses the legacy Gradle structure, you can add it to the root `build.gradle` instead:

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

## Add the SDK dependency

Add the dependency to your app module's `build.gradle` (usually `app/build.gradle`):

```groovy
dependencies {
    implementation 'cn.seastart.meeting:meeting:<version>'
}
```

Where:

- `groupId`: `cn.seastart.meeting`
- `artifactId`: `meeting`
- `version`: replace with the SDK version you want to integrate

The currently released version is:

```groovy
dependencies {
    implementation 'cn.seastart.meeting:meeting:2.0.39'
}
```

> Meeting `2.0.39` transitively depends on RTC `2.0.34`. Read the [compatibility changes](/en/meeting/android/changelog) before upgrading.

## Integration notes

Before you start coding, we recommend confirming the following:

- **AndroidX**: the current sample project has `android.useAndroidX=true` enabled.
- **Minimum OS version**: the current sample project's `minSdk` is `24`.
- **Runtime permissions**: if your app needs to open the camera and mic, handle the camera and audio recording runtime permissions in your app.
- **Initialization flow**: after adding the dependency, continue with [Quickstart](/en/meeting/android/quickstart) to complete `MeetingEngine.create(...)`, `initSdk(...)`, and the meeting entry flow.
