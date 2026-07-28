---
title: "电子白板"
description: "白板的授权、检测与销毁"
---

<Info>本页接口结构由后端源码自动生成，请勿手工编辑。</Info>

## 获取电子白板授权Code

`POST /server/v1/white-board/grant-code`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

获取电子白板的授权码。白板是独立于频道的协作画板，多个用户用**同一个 `board`** 就进入同一块白板。

典型时序与频道 token 类似：业务后端确认权限 → 调本接口拿 `auth_code` 和 `addr` → 下发给客户端 → 客户端打开白板。

+ `board` 是白板 ID，字符集限制同频道名（64 字节内，字母数字下划线连字符）。常见做法是**直接用频道名**，这样会议与白板一一对应
+ `uid` / `name` 是进入白板的用户身份，用于显示协作者光标与操作者
+ 白板首次被授权时自动创建，无需预先创建

授权码有有效期，每次打开白板都重新获取，不要缓存。

**请求参数**

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  第三方用户ID（仅支持大小写字母、数字、下划线 _ 与连字符 -）（最大长度 100）
  示例：`1001`
</ParamField>

<ParamField body="name" type="string">
  第三方用户名称
  示例：`张三`
</ParamField>

<ParamField body="net" type="string">
  网络线路
  示例：`内网`
</ParamField>

<ParamField body="sg" type="string">
  服务分组
</ParamField>


请求示例：

```json
{
  "board": "fire",
  "name": "张三",
  "net": "内网",
  "sg": "",
  "uid": "1001"
}
```

**响应参数**

<ResponseField name="auth_code" type="string">
  白板授权码，下发给客户端用于打开白板
  示例：`wb_co63jg6g54hu3b0xhtie`
</ResponseField>

<ResponseField name="addr" type="string">
  白板服务地址，与授权码配合使用
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "addr": "",
    "auth_code": "wb_co63jg6g54hu3b0xhtie"
  }
}
```

---

## 检测白板是否存在

`POST /server/v1/white-board/exist`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

检测白板是否存在（即是否已被创建且未销毁）。

用于判断"这个会议有没有留下白板内容"——比如会议结束后决定要不要展示"查看白板记录"入口。响应的 `data.is_exist` 是布尔值。

**请求参数**

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>


请求示例：

```json
{
  "board": "fire"
}
```

**响应参数**

<ResponseField name="is_exist" type="boolean">
  示例：`true`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "is_exist": true
  }
}
```

---

## 销毁电子白板

`POST /server/v1/white-board/destroy`

鉴权：需要（见[通用说明](/zh/rtc/server-api/common)）

销毁白板。**板上内容会被清除，不可恢复**。

+ `op_uid` / `op_name` 是操作者信息，用于审计
+ 正在白板中的用户会被断开

白板不会随频道销毁而自动清除——这是有意的，会议结束后白板内容仍可查看。所以需要清理时要显式调用本接口。

**请求参数**

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="op_uid" type="string">
  操作者ID
  示例：`1001`
</ParamField>

<ParamField body="op_name" type="string">
  操作者名称
  示例：`张三`
</ParamField>


请求示例：

```json
{
  "board": "fire",
  "op_name": "张三",
  "op_uid": "1001"
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

