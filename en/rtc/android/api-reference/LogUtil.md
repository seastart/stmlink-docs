---
title: "LogUtil"
description: "Android SDK logging utility: reuse LogUtil to write leveled logs (v/d/i/w/e) and structured marker, format, and metric logs into the same local log file as the SDK's own logs. Read when you want app logs collected alongside SDK logs for debugging."
---

`LogUtil` is the SDK's logging utility (a Kotlin `object` singleton). You can reuse it to write leveled logs, which go into the same local file as the SDK's internal logs (when `enableLocalLog = true` in `RTCEngine.create`), making debugging and troubleshooting easier. The log file path is determined by `localLogPath` in `create(...)`.

The `tag` parameter of every leveled method defaults to `LogUtil.TAG`; you can pass a custom tag.

## Leveled logs

### v(msg, tag)
```kotlin
fun v(msg: String, tag: String = TAG)
```
Description: Writes a Verbose-level log.  
Parameters:
- `msg`: `String`, the log content.
- `tag`: `String`, the log tag; defaults to `LogUtil.TAG`.

Returns: None (`Unit`).

### d(msg, tag)
```kotlin
fun d(msg: String, tag: String = TAG)
```
Description: Writes a Debug-level log.  
Parameters: Same as above.  
Returns: None (`Unit`).

### i(msg, tag)
```kotlin
fun i(msg: String, tag: String = TAG)
```
Description: Writes an Info-level log.  
Parameters: Same as above.  
Returns: None (`Unit`).

### w(msg, tag)
```kotlin
fun w(msg: String, tag: String = TAG)
```
Description: Writes a Warn-level log.  
Parameters: Same as above.  
Returns: None (`Unit`).

### e(msg, tag)
```kotlin
fun e(msg: String, tag: String = TAG)
```
Description: Writes an Error-level log.  
Parameters: Same as above.  
Returns: None (`Unit`).

### e(t, tag)
```kotlin
fun e(t: Throwable, tag: String = TAG)
```
Description: Writes an Error-level log with an exception stack trace.  
Parameters:
- `t`: `Throwable`, the exception object; the full stack trace is expanded internally.
- `tag`: `String`, the log tag; defaults to `LogUtil.TAG`.

Returns: None (`Unit`).

## Structured logs (advanced)

### addMarkerLog(content)
```kotlin
fun addMarkerLog(content: String)
```
Description: Writes a marker log, commonly used to mark key business points in the log stream for easier tracing.  
Parameters:
- `content`: `String`, the marker content.

Returns: None (`Unit`).

### addFormatLog(type, attr, body, level)
```kotlin
fun addFormatLog(type: String, attr: Any?, body: String?, level: LoggerLevel = LoggerLevel.Info)
```
Description: Writes a formatted log; `attr` is serialized to JSON and attached to the log.  
Parameters:
- `type`: `String`, the log type identifier.
- `attr`: `Any?`, the attached attribute object; `null` means no attributes.
- `body`: `String?`, the log body; can be `null`.
- `level`: `LoggerLevel`, the log level; defaults to `LoggerLevel.Info`.

Returns: None (`Unit`).

### addMetricLog(metricType, metricInfo)
```kotlin
fun addMetricLog(metricType: String, metricInfo: MetricItem)
```
Description: Writes a metric log; `metricInfo` is serialized to JSON.  
Parameters:
- `metricType`: `String`, the metric type identifier.
- `metricInfo`: `MetricItem`, the metric data object.

Returns: None (`Unit`).
