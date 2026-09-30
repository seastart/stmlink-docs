---
title: "错误码"
description: "Web SMeeting SDK（0.3.0 起）的错误码：怎么按 code 区分会议层 206xxx、透传的 SRTC 层 106xxx 与服务端业务码，language 参数如何影响服务端报错语言，以及各码的含义、常见原因与建议给用户的提示。"
---

<Warning>
**0.3.0 起错误码重排，报错文案改为英文**（破坏性变更）。本页按 0.3.0 及以后的版本列出；旧版以前除 `206001`–`206004` 外都落在 `206000`，与新码的对照见 [更新日志 · v0.3.0](/zh/meeting/web/changelog)。
</Warning>

### 怎么判断错误

会议 SDK 抛出的错误可能来自三处，**按完整的 `code` 区分**：

| `code` | 来源 | 说明 |
| --- | --- | --- |
| `206xxx` | 会议层 SDK | 见下方「会议层错误码」 |
| `106xxx` | 底层 SRTC SDK，原样透传 | 采集失败、设备权限被拒、推拉流失败等，见 [Web SRTC 错误码](/zh/rtc/web/error-codes) |
| `1000`–`99999` | 服务端业务错误，原样透传 | 会议服务端见 [服务端 API 错误码](/zh/meeting/server-api/error-codes)；给用户看时直接展示服务端返回的 `message` |

错误对象的字段与 SRTC 的 `SdkError` 相同：`code`（完整码）、`baseCode`（低 3 位）、`message` / `msg`（英文详情）。包里导出了 `SdkError` 与 `MeetingErrorCode`（会议层低 3 位）。

+ **请按 `code` 判断，不要按文案判断** —— 文案只给开发者和日志看，会随版本调整。需要给终端用户看的提示，按下表「建议给用户的提示」自行映射，不要直接展示 `message`
+ **会议层和 SRTC 层的低 3 位是两套独立的表**（`206003` 是不在会议中，`106003` 是流轨道不存在），在会议 SDK 里请比较完整的 `code`，只比 `baseCode` 会混淆
+ 不要用 `instanceof` 判断：用 UMD 包时 SDK 自带一份 SRTC，与业务侧单独引入的 SRTC 不是同一个类

```typescript
import { SMeeting } from '@seastart/smeeting-web-sdk';

try {
  await smeeting.requestOpenCamera(container);
} catch (e: any) {
  switch (e?.code) {
    case 206004: // 主持人已禁止打开摄像头
      showToast('主持人已禁止打开摄像头');
      break;
    case 106231: // SRTC 层透传：无摄像头权限
      showToast('请允许浏览器使用摄像头');
      break;
    case 106018: // SRTC 层透传：设备被占用
      showToast('设备可能被其它程序占用，请关闭后重试');
      break;
    default:
      if (e?.code >= 1000 && e?.code < 100000) {
        showToast(e.message); // 服务端业务错误，文案语言跟随 language
      } else {
        console.error(e?.code, e?.message);
      }
  }
}
```

### language 参数

初始化参数 `language` 设置 SDK 语言（语言标签，如 `zh-CN`、`en`），是进程级全局配置，**会同时设置底层 SRTC**：

```typescript
const smeeting = new SMeeting({
  language: 'en',   // 不传则跟随 navigator.language，取不到时为 zh
});
```

+ 请求会议服务端和 SRTC 服务端时都带上 `Accept-Language`，**服务端业务错误（`1000`–`99999`）的 `message` 随之返回中文或英文**
+ 浏览器阻止自动播放时弹出的提示框按 `language` 显示中文或英文，可用初始化参数 `autoPlayDialogText` 覆盖文案
+ **SDK 自身的报错（`206xxx`，以及透传的 `106xxx`）固定为英文，不受 `language` 影响**

---

### 会议层错误码

低 3 位的跨端含义见 [错误码规则与总表](/zh/meeting/error-codes)。

| 错误码 | `MeetingErrorCode` | 含义 | 常见原因 | 建议给用户的提示 |
| --- | --- | --- | --- | --- |
| `206000` | `Unknown` | 未分类错误 | 兜底码，正常不应出现，看 `message` 与日志 | —— |
| `206001` | `NotLoggedIn` | 未登录 | 没调 `login`，或登录失败后调用了需要登录的方法 | —— |
| `206002` | `TokenExpired` | Token 已过期 | `login` 时 Token 已超过有效期，重新签发 | 登录已过期，请重新进入 |
| `206003` | `NotInMeeting` | 不在会议中 | 没进入会议，或已退出后调用会中方法 | —— |
| `206004` | `Unauthorized` | 无权限 | 非主持人执行主持人操作；或房间已禁止打开摄像头 / 麦克风 / 共享 | 主持人已禁止该操作 |
| `206005` | `TokenInvalid` | Token 无效 | `login` 的 Token 无法解析，检查是否完整拷贝、是否为本环境签发 | —— |
| `206006` | `AlreadyInMeeting` | 已在会议中 | 重复进入会议，需先退出当前会议 | —— |
| `206007` | `NetworkError` | 网络错误 | 请求会议服务端失败或 HTTP 非 200（状态见 `message`） | 网络异常，请检查网络后重试 |
| `206010` | `UserNotFound` | 会议中没有该成员 | 按 uid 查询的用户不在房间内 | —— |
| `206011` | `InvalidState` | 当前状态不允许 | 摄像头 / 麦克风 / 共享已开启时重复开启，或尚未开启时切换设备、先关摄像头才能开高拍仪等 | —— |
| `206012` | `InvalidArgument` | 参数非法 | 预留，本版暂未使用 | —— |
| `206356` | `ResponseParseFailed` | 响应解析失败 | 会议服务端的响应不是 JSON 或缺 `code` 字段，多为服务地址配置错误，或中间有代理改写 | —— |

---

### 透传的 SRTC 层错误码

采集、权限、推拉流相关的失败由底层 SRTC 抛出、原样透传，常见的有：

| 错误码 | 含义 | 建议给用户的提示 |
| --- | --- | --- |
| `106231` | 无摄像头权限 | 请允许浏览器使用摄像头 |
| `106251` | 无麦克风权限 | 请允许浏览器使用麦克风 |
| `106039` | 屏幕共享被拒绝 | 已取消屏幕共享；若没有弹出选择窗口，请在系统设置中允许浏览器录屏 |
| `106021` | 设备不存在 | 未检测到摄像头或麦克风，请检查设备连接 |
| `106018` | 采集失败（设备被占用等） | 设备可能被其它程序占用，请关闭后重试 |
| `106006` / `106007` / `106014` / `106015` / `106300`–`106303` | 网络 / 媒体连接失败 | 网络异常，请检查网络后重试 |

完整清单见 [Web SRTC 错误码](/zh/rtc/web/error-codes)。
