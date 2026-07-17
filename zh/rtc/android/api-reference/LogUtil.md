---
title: "LogUtil"
description: "Android SRTC 音视频 SDK 日志工具 LogUtil 接口参考"
---

`LogUtil` 是 SDK 提供的日志工具（Kotlin `object` 单例）。上层接入方可复用它输出分级日志，日志会与 SDK 内部日志统一写入本地文件（当 `RTCEngine.create` 时 `enableLocalLog = true`），便于联调与排障。日志文件路径由 `create(...)` 的 `localLogPath` 决定。

所有分级方法的 `tag` 参数默认取 `LogUtil.TAG`，可传入自定义 tag。

## 分级日志

### v(msg, tag)
```kotlin
fun v(msg: String, tag: String = TAG)
```
方法说明：输出 Verbose 级日志。  
参数说明：
- `msg`：`String`，日志内容。
- `tag`：`String`，日志标签，默认 `LogUtil.TAG`。

返回值说明：无（`Unit`）。

### d(msg, tag)
```kotlin
fun d(msg: String, tag: String = TAG)
```
方法说明：输出 Debug 级日志。  
参数说明：同上。  
返回值说明：无（`Unit`）。

### i(msg, tag)
```kotlin
fun i(msg: String, tag: String = TAG)
```
方法说明：输出 Info 级日志。  
参数说明：同上。  
返回值说明：无（`Unit`）。

### w(msg, tag)
```kotlin
fun w(msg: String, tag: String = TAG)
```
方法说明：输出 Warn 级日志。  
参数说明：同上。  
返回值说明：无（`Unit`）。

### e(msg, tag)
```kotlin
fun e(msg: String, tag: String = TAG)
```
方法说明：输出 Error 级日志。  
参数说明：同上。  
返回值说明：无（`Unit`）。

### e(t, tag)
```kotlin
fun e(t: Throwable, tag: String = TAG)
```
方法说明：输出异常堆栈的 Error 级日志。  
参数说明：
- `t`：`Throwable`，异常对象；内部会展开完整堆栈。
- `tag`：`String`，日志标签，默认 `LogUtil.TAG`。

返回值说明：无（`Unit`）。

## 结构化日志（高级）

### addMarkerLog(content)
```kotlin
fun addMarkerLog(content: String)
```
方法说明：写入一条标记（Marker）日志，常用于在日志流中标注关键业务节点，便于回溯定位。  
参数说明：
- `content`：`String`，标记内容。

返回值说明：无（`Unit`）。

### addFormatLog(type, attr, body, level)
```kotlin
fun addFormatLog(type: String, attr: Any?, body: String?, level: LoggerLevel = LoggerLevel.Info)
```
方法说明：写入一条格式化日志，`attr` 会被序列化为 JSON 附加到日志中。  
参数说明：
- `type`：`String`，日志类型标识。
- `attr`：`Any?`，附加属性对象；`null` 表示无附加属性。
- `body`：`String?`，日志正文，可为 `null`。
- `level`：`LoggerLevel`，日志级别，默认 `LoggerLevel.Info`。

返回值说明：无（`Unit`）。

### addMetricLog(metricType, metricInfo)
```kotlin
fun addMetricLog(metricType: String, metricInfo: MetricItem)
```
方法说明：写入一条指标（Metric）日志，`metricInfo` 会被序列化为 JSON。  
参数说明：
- `metricType`：`String`，指标类型标识。
- `metricInfo`：`MetricItem`，指标数据对象。

返回值说明：无（`Unit`）。
