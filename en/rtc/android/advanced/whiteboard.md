---
title: "Whiteboard integration"
description: "Embed the SRTC whiteboard H5 page in an Android app: get the URL from onJoinSucceed, load it in a WebView, inject the AndroidInterface JS Bridge, handle export and image-insertion callbacks, and control permissions during the call. Read when adding the whiteboard to Android."
---

The whiteboard itself is an H5 page; drawing and collaboration logic all run on the web side. You only need three steps: **get the URL → load it in a WebView → handle the agreed interaction events**.

<Note>
This page covers only how to embed the whiteboard on Android. For how boards map to channels, when a whiteboard is destroyed, and how to sync the "who opened the whiteboard" state to others (SRTC **doesn't** broadcast it automatically), see [Whiteboard](/en/rtc/whiteboard).
</Note>

## 1. Where the whiteboard URL comes from

SRTC delivers the whiteboard URL when you **successfully join a channel**, through the `whiteBoard` parameter of the `RTCClientEvent.onJoinSucceed` callback:

```kotlin
interface RTCClientEvent {
    /**
     * You joined the channel successfully
     * @param whiteBoard Whiteboard URL, normally not empty; null means the line configuration is abnormal
     */
    fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?)
    // ...
}
```

Implement `RTCClientEvent` (or extend `RTCClientSimpleEvent` and override only the methods you need), and take the URL in the callback:

```kotlin
override fun onJoinSucceed(channel: String, uid: String, whiteBoard: String?) {
    if (!whiteBoard.isNullOrEmpty()) {
        // whiteBoard is the whiteboard URL; hand it to the WebView to load
        openWhiteBoard(whiteBoard)
    }
}
```

> - The URL looks like `https://<api-domain>/white-board/?code=<session-credential>&device_type=2&...`. **Each person's URL is different** (`code` is each user's own session credential—one-time use, invalid after connecting), but they all point to the same board (the board ID is the channel name)—so don't forward your URL to others.
> - `whiteBoard` is normally not empty: the whiteboard is created automatically the first time someone enters, with no need to enable it in advance. If it's empty, the line configuration is abnormal, and you shouldn't open the page.

---

## 2. How to use it (load it in a WebView)

### 2.1 Required WebView configuration

```kotlin
val setting = webView.settings
setting.javaScriptEnabled = true                       // Required: the whiteboard depends on JS
setting.domStorageEnabled = true                       // Required: the whiteboard depends on DOM Storage
setting.databaseEnabled = true
setting.javaScriptCanOpenWindowsAutomatically = true
```

### 2.2 Load the URL (append control parameters)

Append control parameters to the URL when loading:

```kotlin
val param = "&no_menu=1&export_btn=1"
webView.loadUrl(whiteBoard + param)
```

| Parameter | Value | Meaning |
|------|----|------|
| `no_menu` | `1` | Hides the main menu button in the top-left corner |
| `no_tool` | `1` | Hides the bottom toolbar |
| `readonly` | `1` | Read-only: can view but not draw (and can't create / delete pages) |
| `export_btn` | `1` | Shows the "Export image" button |

> Parameters are joined with `&`, relying on the URL already having a query string (the address from the `joinChannel` callback already includes `?code=...`). **Don't add a second `?`**, or all the parameters after it are swallowed.

> These parameters only set the **initial state**. To change them during the call (showing/hiding the toolbar, taking away or giving back the pen), call the JS methods in 3.4; changing the URL without reloading has no effect.

### 2.3 Inject the JS Bridge

The whiteboard communicates with native code through a JS interface with the fixed name **`AndroidInterface`**, which must be injected before loading:

```kotlin
webView.addJavascriptInterface(JsBridgeForWhiteboard(callback), "AndroidInterface")
```

JS Bridge implementation (reusable as is):

```kotlin
class JsBridgeForWhiteboard(private val callback: Callback) {

    @JavascriptInterface
    fun onExportImage(dataUrl: String) {   // Whiteboard exported an image
        callback.onExportImage(dataUrl)
    }

    @JavascriptInterface
    fun onWbDestroy(reason: String) {      // Whiteboard destroyed notification
        callback.onWbDestroy(reason)
    }

    interface Callback {
        fun onExportImage(dataUrl: String)
        fun onWbDestroy(reason: String)
    }
}
```

### 2.4 Release

Release the WebView when the screen is destroyed:

```kotlin
override fun onDestroy() {
    super.onDestroy()
    webView.destroy()
}
```

---

## 3. Interaction events and commands

There are four kinds of interaction: **① Native → whiteboard (URL parameters, initial values only)**, **② Whiteboard → native (JS Bridge)**, **③ Whiteboard calls into WebView system capabilities**, and **④ Native → whiteboard (JS methods for dynamic control during the call)**.

### 3.1 Native → whiteboard: URL control parameters

Passed through the URL query when loading (see 2.2) to control the whiteboard UI:

| Parameter | Description |
|------|------|
| `no_menu=1` | Hides the main menu button in the top-left corner |
| `no_tool=1` | Hides the bottom toolbar |
| `readonly=1` | Read-only; editing is disabled |
| `export_btn=1` | Shows the export button |

### 3.2 Whiteboard → native: JS Bridge events

The interface object name is fixed as **`AndroidInterface`**; the whiteboard calls it as `window.AndroidInterface.<method>(...)`.

| Method | Parameter | When it fires | Description |
|------|------|----------|------|
| `onExportImage(dataUrl)` | `dataUrl: String`, a Base64 Data URL (in the form `data:image/png;base64,xxxx`) | The export button is clicked on the whiteboard | Native code parses the Base64 and saves it as an image (the example saves a PNG to the system gallery; on Android 9 and earlier, request the write storage permission first) |
| `onWbDestroy(reason)` | `reason: String`, the reason for destruction | The whiteboard is destroyed | Native code can close the screen or clean up resources accordingly |

Reference implementation for saving the image in `onExportImage`:

```kotlin
private fun saveBase64DataUrl(dataUrl: String) {
    val prefix = "base64,"
    val index = dataUrl.indexOf(prefix)
    if (index == -1) return
    val bytes = Base64.decode(dataUrl.substring(index + prefix.length), Base64.DEFAULT)
    // Write bytes to the gallery / a file (on Android 9 and earlier, request the WRITE permission first)
}
```

### 3.3 Whiteboard calls into WebView system capabilities

Whiteboard features such as "Insert image" and "Upload image" trigger WebView system callbacks, which you need to handle in `WebChromeClient`:

| Callback | What to do |
|------|--------------|
| `onPermissionRequest(request)` | Grant the capabilities the whiteboard requests (such as camera and microphone): `request.grant(request.resources)` |
| `onShowFileChooser(...)` | Fires when the whiteboard picks an image. Show a source picker (camera / gallery), and after selection return the result to the whiteboard through `filePathCallback.onReceiveValue(uris)`; on cancel, return `null` |

```kotlin
webView.webChromeClient = object : WebChromeClient() {
    override fun onPermissionRequest(request: PermissionRequest) {
        request.grant(request.resources)
    }

    override fun onShowFileChooser(
        webView: WebView?,
        filePathCallback: ValueCallback<Array<Uri>>?,
        params: FileChooserParams?
    ): Boolean {
        // Take a photo / pick from the gallery; once you have the uri:
        // filePathCallback?.onReceiveValue(arrayOf(uri))
        // User canceled: filePathCallback?.onReceiveValue(null)
        return true
    }
}
```

> Tip: the whiteboard has a size limit for images. We recommend compressing images before returning them (for example, to under 1 MB) to avoid upload failures with large images.

### 3.4 Native → whiteboard: dynamic control during the call

URL parameters take effect only when the page opens. To show/hide UI or take away/give back the pen during the call, use `evaluateJavascript` to call the methods the whiteboard attaches to `window`:

| Method | Description |
|------|------|
| `window.setReadonly(readonly)` | **Permission switch**: whether the user can draw (including creating / deleting pages); also decides who controls page turning |
| `window.setShowMenu(show)` | Shows or hides the main menu button in the top-left corner |
| `window.setShowToolUi(show)` | Shows or hides the bottom toolbar (use it when you want to draw your own toolbar) |
| `window.setCurrentTool(tool)` | Switches the tool: `select` / `hand` / `draw` / `eraser` / `arrow` / `text` / `geo` / `line` / `highlight` / `laser` |

> **Hiding UI isn't the same as disabling actions**: `setShowMenu` / `setShowToolUi` only hide the interface; users can still draw with keyboard shortcuts and the context menu. To make "this person unable to draw", you can only use `setReadonly`.

```kotlin
webView.webViewClient = object : WebViewClient() {
    override fun onPageFinished(view: WebView?, url: String?) {
        super.onPageFinished(view, url)
        // The methods are attached only after the page finishes loading; calling them earlier gives undefined
        webView.evaluateJavascript("window.setReadonly(${!canDraw})", null)
    }
}

// You can call it again at any time during the call without reloading the page
fun revokeDrawPermission() {
    webView.evaluateJavascript("window.setReadonly(true)", null)
}
```

> The page-following rule for multi-page whiteboards is "whoever can draw turns the page, and everyone else follows"; read-only clients only follow and don't broadcast. See [SRTC · Whiteboard · Multi-page whiteboards](/en/rtc/whiteboard#multi-page-whiteboards-and-page-following). You don't need to designate anyone as host.
