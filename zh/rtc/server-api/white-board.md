---
title: "电子白板"
description: "白板的授权、检测与销毁"
---

{/* 本页接口结构由后端源码自动生成，请勿手工编辑 —— 改动会在下次同步时被覆盖。
    内容一律改 rtc-backend 的源码，写法见那边 README 的「对外接口文档（srvapi）」一节。 */}

## 获取电子白板授权Code

`POST /server/v1/white-board/grant-code`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

获取电子白板的授权码。白板是独立于频道的协作画板，多个用户用同一个 board
就进入同一块白板。

典型时序与频道 token 类似：业务后端确认权限 → 调本接口拿 auth_code 和 addr →
下发给客户端 → 客户端把二者拼成 &#123;addr&#125;?code=&#123;auth_code&#125; 打开（白板是一个 H5 页面，
用 iframe 或 WebView 内嵌）。授权码 1 小时内有效且连接后即失效，每次打开白板都重新
获取，不要缓存。

白板首次被授权时自动创建，无需预先创建。

频道内的用户还有更省事的一条路：加入频道的响应里已经带了拼好的白板地址（字段
white_board，授权码就是该用户的 sid），直接内嵌即可，不必再调本接口。本接口是给
「不在频道里的人也要用白板」以及「白板独立于频道使用」的场景准备的。完整对接说明
见《电子白板》。

**请求参数**

<ParamField body="board" type="string" required>
  板子ID，字符集限制同频道名。常见做法是直接用频道名，这样会议与白板一一对应（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="uid" type="string" required>
  第三方用户ID，用于显示协作者光标与操作者（仅支持大小写字母、数字、下划线 _ 与连字符 -）（最大长度 100）
  示例：`1001`
</ParamField>

<ParamField body="name" type="string">
  第三方用户名称
  示例：`张三`
</ParamField>

<ParamField body="net" type="string">
  网络线路，取值是部署的网络配置里的线路名，内网/外网也可写作 lan/wan；留空则由服务端选择
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
  示例：`wb-co63jg6g54hu3b0xhtie`
</ResponseField>

<ResponseField name="addr" type="string">
  白板页面地址，与授权码拼成 &#123;addr&#125;?code=&#123;auth_code&#125; 使用
  示例：`https://api.example.com/white-board/`
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "addr": "https://api.example.com/white-board/",
    "auth_code": "wb-co63jg6g54hu3b0xhtie"
  }
}
```

---

## 检测白板是否存在

`POST /server/v1/white-board/exist`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

检测白板是否存在，即是否已被创建且未销毁。

用于判断"这块板子上还有没有内容"—— 比如决定要不要展示"进入白板"入口，
或确认销毁是否已经生效。

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
  白板是否存在（已创建且未销毁）
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "is_exist": false
  }
}
```

---

## 导出白板内容

`POST /server/v1/white-board/detail`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

导出白板内容。用于把板上内容存到业务方自己的外部存储，之后可用 reload 接口灌回。

返回的是白板的全量快照，结构为 &#123;图形ID: 图形对象&#125;。注意它与白板客户端上行的增量包
（updates.added/modified/deleted）**不是同一种格式**，别拿增量包去调 reload。

compress=true 时返回 content（内容经 zlib 压缩后做 base64），适合内容较多时减少传输量；
默认返回明文 data。两者内容等价，可互相转换。

白板不存在或为空板时不报错，返回 count=0。需要区分「不存在」与「空板」请先调 exist。

**请求参数**

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="compress" type="boolean">
  是否压缩返回。true时content为zlib压缩后的base64串，false(默认)时data为明文
</ParamField>


请求示例：

```json
{
  "board": "fire",
  "compress": false
}
```

**响应参数**

<ResponseField name="board" type="string">
  白板ID
</ResponseField>

<ResponseField name="compress" type="boolean">
  返回的是否为压缩内容
</ResponseField>

<ResponseField name="count" type="integer">
  图形数量
</ResponseField>

<ResponseField name="data" type="object">
  明文内容
</ResponseField>

<ResponseField name="content" type="string">
  zlib+base64压缩内容
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "board": "",
    "compress": false,
    "content": "",
    "count": 0,
    "data": {}
  }
}
```

---

## 导入白板内容

`POST /server/v1/white-board/reload`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

导入白板内容。清空指定白板的现有内容并整体重设，随后通知板内所有客户端
清空画布并重新加载。

数据从 content（zlib+base64，即 detail 接口 compress=true 的产物）或 data（明文）传入，
**二选一**：同时传会报错；都不传是合法的，语义为清空白板。

语义是**整板覆盖**，不是合并：导入前板上的内容全部丢弃。白板不存在时会自动创建。

**请求参数**

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="content" type="string">
  zlib压缩后的base64串，与data二选一
</ParamField>

<ParamField body="data" type="object">
  明文数据，与content二选一
</ParamField>


请求示例：

```json
{
  "board": "fire",
  "content": "",
  "data": {}
}
```

**响应参数**

<ResponseField name="count" type="integer">
  导入后的图形数量
</ResponseField>


响应示例：

```json
{
  "code": 0,
  "data": {
    "count": 0
  }
}
```

---

## 销毁电子白板

`POST /server/v1/white-board/destroy`

鉴权：需要（见[概览](/zh/rtc/server-api/overview)）

销毁白板。板上内容会被清除，不可恢复，正在白板中的用户会被断开。

白板另有两条自动销毁的路径，本接口用于在此之前主动清理（比如会中"关闭白板"）：

- 频道销毁时，会连带销毁同名的白板。频道无人 2 小时后自动销毁，所以按推荐做法
（board 取频道名）用的白板，也会在会议散场 2 小时后一起消失。要让白板内容长期
留存，board 就不能取频道名。
- 白板超过 25 小时无人写入，由定时任务清理。

**请求参数**

<ParamField body="board" type="string" required>
  板子ID（长度 64 字节以内，仅支持大小写字母、数字、下划线 _ 与连字符 -）
  示例：`fire`
</ParamField>

<ParamField body="op_uid" type="string">
  操作者ID，用于审计
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

