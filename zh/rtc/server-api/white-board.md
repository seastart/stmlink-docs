---
title: "电子白板"
description: "白板的授权、检测与销毁"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 获取电子白板授权Code

`POST /server/v1/white-board/grant-code`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| board | string | 是 | 板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| uid | string | 是 | 第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）（最大长度 100） |
| name | string | 否 | 第三方用户名称 |
| net | string | 否 | 网络线路 |
| sg | string | 否 | 服务分组 |

请求示例：

```json
{
  "board": "",
  "name": "",
  "net": "",
  "sg": "",
  "uid": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| data.auth_code | string |  |
| data.addr | string |  |

响应示例：

```json
{
  "code": 0,
  "data": {
    "addr": "",
    "auth_code": ""
  }
}
```

---

## 检测白板是否存在

`POST /server/v1/white-board/exist`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| board | string | 是 | 板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -） |

请求示例：

```json
{
  "board": ""
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
| --- | --- | --- |

响应示例：

```json
{
  "code": 0,
  "data": false
}
```

---

## 销毁电子白板

`POST /server/v1/white-board/destroy`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| board | string | 是 | 板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -） |
| op_uid | string | 否 | 操作者ID |
| op_name | string | 否 | 操作者名称 |

请求示例：

```json
{
  "board": "",
  "op_name": "",
  "op_uid": ""
}
```

**响应参数**

`data` 为 null

响应示例：

```json
{
  "code": 0,
  "data": null
}
```

---

