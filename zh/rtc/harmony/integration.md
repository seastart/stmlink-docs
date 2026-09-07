---
title: "集成方式"
description: "SRTC HarmonyOS SDK 的环境要求、HAR 集成方式与权限配置"
---

SRTC HarmonyOS SDK 是一套 `HAR`（静态共享包）形态的原生音视频 SDK，对外模块名为 `srtc`，当前支持：

+ HarmonyOS 5.0.0（API 12）及以上
+ DevEco Studio 5.0 及以上
+ ArkTS（Stage 模型）
+ **仅 arm64-v8a**

<Warning>
**视频编码只有硬编，没有软编兜底，所以视频功能必须在真机上验证。**

SDK 的视频预设统一使用 H264，底层的 H264 / H265 编解码只走设备硬件编解码器。模拟器上建不出编码器，SDP 中不会出现任何 H264，视频通路直接不可用。

更需要注意的是：**在缺少 H264 硬编能力的真机上，SDK 不会报错，而是静默退回 VP8**。表现为"本机能看到画面，但和 Web / iOS / Android 端互通不上"。所以自测时不要以"看到画面"为准，要确认实际协商到的编码格式。
</Warning>

---

### 获取 HAR

SDK 以预编译 HAR 分发，从制品仓下载：

```bash
curl -O https://repo.open.seastart.cn/repository/vcs-releases/srtc-harmony-0.0.1.har
```

把下载到的文件放进模块的 `libs/` 目录，并重命名为 `srtc-0.0.1.har`：

```
your-project/
└── entry/
    ├── libs/
    │   └── srtc-0.0.1.har
    ├── oh-package.json5
    └── src/main/module.json5
```

<Note>
HarmonyOS 的 ohpm 没有按 Git tag 解析版本的机制，SDK 通过 `file:` 路径直接引用具体的 HAR 文件。因此**升级 SDK 需要手动替换 `libs/` 下的文件并同步修改下面的版本号**，不会自动更新。
</Note>

---

### 声明依赖

在模块的 `oh-package.json5` 中加入：

```json5
{
  "dependencies": {
    "srtc": "file:./libs/srtc-0.0.1.har"
  }
}
```

然后执行：

```bash
ohpm install
```

底层依赖的 `@ohos/webrtc` 与 `@ohos/mqtt` 会由 ohpm 从 [OpenHarmony 三方库中心仓](https://ohpm.openharmony.cn/) 自动安装，你不需要手动声明。

---

### 权限配置

在模块的 `src/main/module.json5` 中声明：

```json5
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET",
        "reason": "$string:internet_reason"
      },
      {
        "name": "ohos.permission.CAMERA",
        "reason": "$string:camera_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      },
      {
        "name": "ohos.permission.MICROPHONE",
        "reason": "$string:mic_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      }
    ]
  }
}
```

摄像头与麦克风属于 `user_grant` 权限，除了在 `module.json5` 中声明，还必须在运行时主动申请：

```typescript
import { abilityAccessCtrl, common, Permissions } from '@kit.AbilityKit';

const permissions: Permissions[] = [
  'ohos.permission.CAMERA',
  'ohos.permission.MICROPHONE'
];

const mgr = abilityAccessCtrl.createAtManager();
await mgr.requestPermissionsFromUser(
  getContext(this) as common.UIAbilityContext,
  permissions
);
```

---

### 初始化

在 `UIAbility` 的 `onCreate` 中把 Ability 的 Context 交给 SDK：

```typescript
import UIAbility from '@ohos.app.ability.UIAbility';
import { SRTC } from 'srtc';

export default class EntryAbility extends UIAbility {
  onCreate(): void {
    SRTC.init(this.context);
  }
}
```

<Warning>
**这一步不要跳过。** 摄像头档位查询需要 Context，而 HAR 形态的库拿不到宿主的 Context（`getContext()` 只在 UI 组件里可用）。

不调用 `SRTC.init` 也能跑通，但摄像头分辨率会退化为"由底层自行吸附档位"，实际分辨率因机型而异，你在 `CameraPreset` 里设定的值不再生效。
</Warning>

---

### 导入 SDK

```typescript
import { SRTCEngine, SRTCVideoView, Channel, Track } from 'srtc';
```

---

### 最小接入检查清单

+ `libs/` 下已放入 HAR，`oh-package.json5` 已声明依赖，`ohpm install` 已执行
+ `module.json5` 已声明 INTERNET / CAMERA / MICROPHONE
+ 运行时已申请摄像头与麦克风权限
+ `UIAbility.onCreate` 中已调用 `SRTC.init(this.context)`
+ 业务后端已能签发加入频道所需的 Token
+ 手上有一台 arm64-v8a 真机（视频功能无法在模拟器上验证）

完成以上步骤后，可以继续阅读 [快速开始](/zh/rtc/harmony/quickstart)。
