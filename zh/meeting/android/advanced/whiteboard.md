---
title: "白板共享"
description: "会议里怎么开白板：用 requestShareBoard() 拿到白板地址并用 WebView 承载，处理他人共享与中途入会，以及 WebView 需要的 JS 接口"
---

会议里的电子白板是一个**由服务端托管的 H5 页面**，Android 端用 `WebView` 承载。笔迹同步走白板自己的通道，不产生媒体流，也不占用摄像头 / 屏幕采集。

<Note>
白板页面本身的能力（URL 参数、桌面批注模式、生命周期与销毁时机）与 SRTC 层完全一致，见 [SRTC · 电子白板](/zh/rtc/whiteboard)。本页只讲会议层的用法。
</Note>

---

### 发起白板共享

`requestShareBoard()` 做两件事：向会议广播「我在共享白板」，并在回调里返回白板地址。

```kotlin
meetingEngine.requestShareBoard(object : MeetingValueResultCallback<String> {
    override fun onSuccess(whiteBoard: String) {
        // whiteBoard 是拼好授权码的完整 URL，直接加载
        showBoard(whiteBoard)
    }

    override fun onFailure(errorCode: Int, message: String?) {
        // 常见失败：主持人开启了「房间禁共享」、已有他人在共享
        toast(errorMessageFor(errorCode))
    }
})
```

同一时刻一个会议只允许一位成员共享，屏幕共享与白板互斥。

停止共享：

```kotlin
meetingEngine.stopShareWhiteBoard()
```

<Note>
主持人处理他人的共享申请，用 [`confirmStartWhiteBoardShareAgree()`](/zh/meeting/android/api-reference/MeetingEngine) / `confirmStartWhiteBoardShareRefuse()`，同意时同样会在回调里拿到白板地址。
</Note>

---

### 响应他人的白板共享

自己不是发起者时，从房间事件里得知，地址从 `infosManager` 读：

```kotlin
override fun onRoomShareStart(shareUid: String, shareType: ShareType) {
    if (shareType == ShareType.WhiteBoardShare) {
        showBoard(meetingEngine.infosManager.whiteBoard ?: return)
    }
}

override fun onRoomShareStop(shareUid: String, shareType: ShareType) {
    if (shareType == ShareType.WhiteBoardShare) {
        hideBoard()
    }
}
```

**中途入会的人收不到这个事件**，进会后要自己补一次判断：

```kotlin
val info = meetingEngine.infosManager.getMeetingInfo()
if (info?.shareState == ShareType.WhiteBoardShare) {
    // 会议中已经有人在共享白板
    showBoard(meetingEngine.infosManager.whiteBoard ?: return)
}
```

---

### 用 WebView 承载

白板页是一个标准的 Web 应用，**必须启用 JavaScript**；白板销毁时要通知宿主关掉视图，所以还要注入一个名为 `AndroidInterface` 的 JS 接口：

```kotlin
webView.settings.javaScriptEnabled = true
webView.settings.domStorageEnabled = true
webView.addJavascriptInterface(object {
    /** 白板被销毁（有人主动销毁或到期清理），宿主应关掉白板视图 */
    @JavascriptInterface
    fun onWbDestroy(reason: String?) {
        runOnUiThread { hideBoard() }
    }

    /** 用户点了导出按钮（需在 URL 上加 export_btn=1），回传图片 base64 */
    @JavascriptInterface
    fun onExportImage(base64: String) {
        saveImage(base64)
    }
}, "AndroidInterface")

webView.loadUrl(whiteBoard)
```

退出会议或收到 `onRoomShareStop` 时，记得销毁 WebView，避免它在后台继续保持白板连接。

---

### 相关

+ [SRTC · 电子白板](/zh/rtc/whiteboard) —— 白板页面的 URL 参数、状态同步原理、生命周期与销毁
+ [MeetingEngine](/zh/meeting/android/api-reference/MeetingEngine) —— `requestShareBoard()` / `stopShareWhiteBoard()` 接口签名
+ [Meeting 结果回调](/zh/meeting/android/api-reference/MeetingResultCallback) —— 白板地址与失败结果回调
+ [MeetingRoomEvent](/zh/meeting/android/api-reference/MeetingRoomEvent) —— 共享开始 / 结束事件
