---
title: "电子白板"
description: "白板的授权、检测与销毁"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 获取电子白板授权Code

`POST /server/v1/white-board/grant-code`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

**请求参数**

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="uid" type="string" required>
  第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）（最大长度 100）
</ParamField>

<ParamField body="name" type="string">
  第三方用户名称
</ParamField>

<ParamField body="net" type="string">
  网络线路
</ParamField>

<ParamField body="sg" type="string">
  服务分组
</ParamField>


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

<ResponseField name="auth_code" type="string">
</ResponseField>

<ResponseField name="addr" type="string">
</ResponseField>


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

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>


请求示例：

```json
{
  "board": ""
}
```

**响应参数**


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

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
</ParamField>

<ParamField body="op_uid" type="string">
  操作者ID
</ParamField>

<ParamField body="op_name" type="string">
  操作者名称
</ParamField>


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

