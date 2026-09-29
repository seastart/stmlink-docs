---
title: "Whiteboard sharing"
description: "Open a whiteboard in an Android meeting: get the whiteboard URL with requestShareBoard() and host it in a WebView, respond to others' sharing and to entering mid-meeting, and inject the JS interface the WebView needs."
---

The whiteboard in a meeting is an **H5 page hosted by the server**, displayed on Android in a `WebView`. Strokes sync over the whiteboard's own connection; it produces no media stream and doesn't use camera or screen capture.

<Note>
The capabilities of the whiteboard page itself (URL parameters, overlay annotation mode, lifecycle and when boards are destroyed) are exactly the same as on the SRTC layer; see [SRTC · Whiteboard](/en/rtc/whiteboard). This page covers only meeting-layer usage.
</Note>

---

### Start whiteboard sharing

`requestShareBoard()` does two things: it broadcasts "I'm sharing a whiteboard" to the meeting, and returns the whiteboard URL in the callback.

```kotlin
meetingEngine.requestShareBoard(object : MeetingValueResultCallback<String> {
    override fun onSuccess(whiteBoard: String) {
        // whiteBoard is the full URL with the auth code already appended; load it directly
        showBoard(whiteBoard)
    }

    override fun onFailure(errorCode: Int, message: String?) {
        // Common failures: the host has disabled sharing for the room, or someone else is already sharing
        toast(errorMessageFor(errorCode))
    }
})
```

Only one member can share in a meeting at a time; screen sharing and the whiteboard are mutually exclusive.

Stop sharing:

```kotlin
meetingEngine.stopShareWhiteBoard()
```

<Note>
To handle other members' sharing requests, the host uses [`confirmStartWhiteBoardShareAgree()`](/en/meeting/android/api-reference/MeetingEngine) / `confirmStartWhiteBoardShareRefuse()`; when approving, the host also gets the whiteboard URL in the callback.
</Note>

---

### Respond to others' whiteboard sharing

When you aren't the one who started it, you learn about it from room events and read the URL from `infosManager`:

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

**Members who enter mid-meeting don't receive this event**, so check once yourself after entering the meeting:

```kotlin
val info = meetingEngine.infosManager.getMeetingInfo()
if (info?.shareState == ShareType.WhiteBoardShare) {
    // Someone in the meeting is already sharing a whiteboard
    showBoard(meetingEngine.infosManager.whiteBoard ?: return)
}
```

---

### Host it in a WebView

The whiteboard page is a standard web app and **must have JavaScript enabled**. When the whiteboard is destroyed it needs to tell the host to close the view, so you also need to inject a JS interface named `AndroidInterface`:

```kotlin
webView.settings.javaScriptEnabled = true
webView.settings.domStorageEnabled = true
webView.addJavascriptInterface(object {
    /** The whiteboard was destroyed (someone destroyed it or it was cleaned up on expiry); the host should close the whiteboard view */
    @JavascriptInterface
    fun onWbDestroy(reason: String?) {
        runOnUiThread { hideBoard() }
    }

    /** The user tapped the export button (requires export_btn=1 on the URL); returns the image as base64 */
    @JavascriptInterface
    fun onExportImage(base64: String) {
        saveImage(base64)
    }
}, "AndroidInterface")

webView.loadUrl(whiteBoard)
```

When you exit the meeting or receive `onRoomShareStop`, remember to destroy the WebView so it doesn't keep the whiteboard connection open in the background.

---

### Related

+ [SRTC · Whiteboard](/en/rtc/whiteboard)—URL parameters of the whiteboard page, how state sync works, lifecycle and destruction
+ [MeetingEngine](/en/meeting/android/api-reference/MeetingEngine)—signatures of `requestShareBoard()` / `stopShareWhiteBoard()`
+ [Meeting result callbacks](/en/meeting/android/api-reference/MeetingResultCallback)—callbacks for the whiteboard URL and failure results
+ [MeetingRoomEvent](/en/meeting/android/api-reference/MeetingRoomEvent)—sharing start / stop events
