---
title: "集成方式"
description: "SMeeting HarmonyOS SDK 的环境要求、HAR 集成方式与权限配置"
---

SMeeting HarmonyOS SDK 是一套 `HAR`（静态共享包）形态的原生会议 SDK，对外模块名为 `smeeting`，当前支持：

+ HarmonyOS 5.0.0（API 12）及以上
+ DevEco Studio 5.0 及以上
+ ArkTS（Stage 模型）
+ **仅 arm64-v8a**

<Warning>
**SMeeting 依赖 SRTC，两个 HAR 都必须引入。**

HarmonyOS 的 HAR 没有依赖传递性，SMeeting 把 `srtc` 声明为 `peerDependencies`，需要由你的工程提供。只声明 `smeeting` 会在 `ohpm install` 阶段报缺少 `srtc`。
</Warning>

<Warning>
**视频编码只有硬编，没有软编兜底，所以视频功能必须在真机上验证。**

视频预设统一使用 H264，底层只走设备硬件编解码器。模拟器上建不出编码器；而在缺少 H264 硬编能力的真机上，SDK **不报错而是静默退回 VP8**，表现为"本机能看到画面，但和其它端互通不上"。自测时请确认实际协商到的编码格式。
</Warning>

---

### 获取 HAR

两个包都从制品仓下载：

```bash
curl -O https://repo.open.seastart.cn/repository/vcs-releases/srtc-harmony-0.0.1.har
curl -O https://repo.open.seastart.cn/repository/vcs-releases/smeeting-harmony-0.0.1.har
```

放进模块的 `libs/` 目录，去掉文件名里的 `-harmony`：

```
your-project/
└── entry/
    ├── libs/
    │   ├── srtc-0.0.1.har
    │   └── smeeting-0.0.1.har
    ├── oh-package.json5
    └── src/main/module.json5
```

<Note>
两个 SDK **独立编号**，版本号不需要对齐。当前 SMeeting 0.0.1 依赖 SRTC 0.0.1。升级 SMeeting 时请按本页说明确认它对应的 SRTC 版本。
</Note>

---

### 声明依赖

在模块的 `oh-package.json5` 中**同时**声明两个包：

```json5
{
  "dependencies": {
    "smeeting": "file:./libs/smeeting-0.0.1.har",
    "srtc": "file:./libs/srtc-0.0.1.har"
  }
}
```

然后执行：

```bash
ohpm install
```

底层依赖的 `@ohos/webrtc` 与 `@ohos/mqtt` 会由 ohpm 从 [OpenHarmony 三方库中心仓](https://ohpm.openharmony.cn/) 自动安装。

<Note>
HarmonyOS 的 ohpm 没有按 Git tag 解析版本的机制，SDK 通过 `file:` 路径直接引用具体的 HAR 文件。因此**升级需要手动替换 `libs/` 下的文件并同步修改上面的版本号**。
</Note>

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

摄像头与麦克风是 `user_grant` 权限，还必须在运行时主动申请：

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

在 `UIAbility` 的 `onCreate` 中把 Context 交给底层的 SRTC：

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
**这一步不要跳过。** 摄像头档位查询需要 Context，而 HAR 形态的库拿不到宿主的 Context。不调用也能跑通，但摄像头分辨率会退化为"由底层自行吸附档位"，你设定的预设不再生效。
</Warning>

---

### 导入 SDK

```typescript
import { SMeetingEngine, SMeetingDelegate } from 'smeeting';
// 渲染组件与轨道类型来自 srtc
import { SRTCVideoView, Track } from 'srtc';
```

---

### 最小接入检查清单

+ `libs/` 下已放入**两个** HAR，`oh-package.json5` 已同时声明 `smeeting` 与 `srtc`
+ `ohpm install` 已执行且无报错
+ `module.json5` 已声明 INTERNET / CAMERA / MICROPHONE
+ 运行时已申请摄像头与麦克风权限
+ `UIAbility.onCreate` 中已调用 `SRTC.init(this.context)`
+ 业务后端已能签发会议 Token
+ 手上有一台 arm64-v8a 真机

完成以上步骤后，可以继续阅读 [快速开始](/zh/meeting/harmony/quickstart)。
