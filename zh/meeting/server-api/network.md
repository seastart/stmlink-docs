---
title: "网络号"
description: "查询部署方配置的接入线路（网络号），供最终用户在终端手动选择后传给「获取会议授权」"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 meeting-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 可选网络号列表

`POST /server/v1/network/list`

鉴权：需要（见[概览](/zh/meeting/server-api/overview)）

查询本应用可选的网络号。无请求参数。

网络号对应同一套服务的不同接入线路（如「内网」「外网」「专线」），由部署方配置。
终端所处网络不同、需要走不同线路时，可以把本接口的结果展示给最终用户手动选择，
再把选中的 net 原样传给「获取会议授权」的 net 参数；不传 net 时使用 is_default 为 true 的那个。
默认网络号排在第一位。

**请求参数**

无

**响应参数**

<ResponseField name="net" type="string">
  网络号，获取会议授权时原样作为 net 传入
</ResponseField>

<ResponseField name="is_default" type="boolean">
  是否应用的默认网络号（不传 net 时使用它）
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": [
    {
      "is_default": false,
      "net": ""
    }
  ]
}
```

---

