---
title: "接口列表"
description: "服务端 API 完整接口列表"
---

# 会议授权

## 获取会议授权

获取meet_token

**接口URL**

> /server/v1/user-auth/grant

**请求Body参数**

```javascript
{
	"user_id": "user01",
	"nickname": "",
	"net": "内网",
	"sg": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| user_id | user01 | string | 是 | 第三方(您的业务系统)用户ID |
| net | 内网 | string | 否 | 网络线路 |
| sg | - | string | 否 | 服务分组 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "4rjamnKdjonWJBSdwpV3JYc5jPMnCUdyFXuCZZ7p+lWtXfNJWvXV1iOv9bHqJ1ER3f50FeRg0idYmGk+0Bx2UP1QsxzGHmk6hiIxIP4wcATcoEjkZ7aJZJeTJJ7CDU1+fJ40MDfs0MYqDvbBrLv39e3vgq9H/PqbXM+0J4qx6CllBINAKewChw4JqvGZfklDks2KgQM1u62NtiuuntKWzLq3l21qUtz/M9ic/CI1w6fPLE0TkZ2hndBP006e40x8ql0rWlj7befNtNNwAkw8U4RFADeyaI7g2EEMDdFSN/vgg0h0Bvu5OLYEvvw+tAz75+aXPPYSDndODF68ONDWa1/6tmGMhDBFwZ16btvc33M="
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | integer | - |
| data | 4rjamnKdjon...... | string | 会议Token |

***

## 踢出授权用户

**接口URL**

> /server/v1/user-auth/kickout

**请求Body参数**

```javascript
{
	"user_id": "user01",
	"device_type": 1
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| user_id | user02 | string | 是 | 参会用户ID |
| device_type | 0 | string | 否 | 设备类型，不填则踢出user_id的所有端 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | integer | - |

***

# 会议外

## 创建会议

**接口URL**

> /server/v1/meet/create

**请求Body参数**

```javascript
{
	"creator": "uid3",
	"room_no": "",
	"title": "标题",
	"content": "说明",
	"attend_type": 3,
	"conferee_details": [
		{
			"user_id": "s9zv4d",
			"account": "13345678903",
			"nickname": "Nan3",
			"real_name": "小刘",
			"avatar": "",
			"role": 1
		}
	],
	"password": "",
	"meeting_type": 1,
	"plan_time": 1706178794,
	"plan_dur": 10,
	"entry_mute_policy": 3,
	"watermark_disabled": false,
	"screenshot_disabled": true,
	"self_unmute_mic_disabled": false,
	"self_unmute_camera_disabled": false,
	"mic_disabled": false,
	"camera_disabled": false,
	"share_disabled": false,
	"chat_disabled": true,
	"force_join": false,
	"auto_record": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| creator | uid3 | string | 否 | 会议创建者 |
| room_no | - | string | 否 | 房间号，可以用个人房间号或空，空会自动生成 |
| title | 会议标题 | string | 是 | 会议标题 |
| content | 说明 | string | 否 | 会议说明 |
| attend_type | 3 | number | 否 | 1 无限制(默认) 2 密码进入 3 仅邀请人员参会 |
| conferee_details | - | array | 否 | 参会者列表 |
| conferee_details.user_id | s9zv4d | string | 是 | 用户ID |
| conferee_details.account | 13345678903 | string | 否 | 用户帐号 |
| conferee_details.nickname | Nan3 | string | 否 | 用户昵称 |
| conferee_details.real_name | 小刘 | string | 否 | 真实名称 |
| conferee_details.avatar | - | string | 否 | 用户头像 |
| conferee_details.role | 1 | number | 否 | 用户角色 |
| password | - | string | 否 | 密码，attend_type为2时必填 |
| meeting_type | 1 | number | 是 | 1即时会议 2预约会议 |
| plan_time | 1706178794 | number | 否 | 开始时间 (时间戳)，预约会议必填 |
| plan_dur | 10 | number | 否 | 持续时间(单位分钟)，预约会议必填 |
| entry_mute_policy | 3 | number | 否 | 入会静音状态 1:开启入会静音(所有人入会默认静音) 2:关闭(跟随客户端初始音频状态) 3：超6人静音(超过6人后入会静音) 默认值3 |
| watermark_disabled | true | boolean | 否 | 水印是否关闭 false:开启 true:关闭(默认) |
| screenshot_disabled | true | boolean | 否 | 截屏是否禁止 false:不禁止(默认) true：禁止 |
| self_unmute_mic_disabled | false | boolean | 否 | 禁麦时禁止自我解除 false:不禁止(默认) true：禁止 |
| self_unmute_camera_disabled | false | boolean | 否 | 禁视频时禁止自我解除 false:不禁止(默认) true：禁止 |
| mic_disabled | false | boolean | 否 | 禁止开麦 false:不禁止(默认) true：禁止 |
| camera_disabled | false | boolean | 否 | 禁止开视频 false:不禁止(默认) true：禁止 |
| share_disabled | false | boolean | 否 | 禁止共享 false:不禁止(默认) true：禁止 |
| chat_disabled | true | boolean | 否 | 聊天是否禁止 false:不禁止(默认) true：禁止 |
| force_join | false | boolean | 否 | 预约会议是否强制入会 |
| auto_record | false | boolean | 否 | 是否自动录像 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"meeting_id": "snj20o",
		"room_no": "776868796"
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | integer | - |
| data | - | string | - |
| data.meeting_id | snj20o | string | 会议 |
| data.room_no | 776868796 | string | 房间号 |

***

## 会前修改会议

**接口URL**

> /server/v1/meet/update

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"title": "1",
	"content": "1",
	"attend_type": 3,
	"conferee_details": [
		{
			"user_id": "s9zv4d",
			"account": "13345678903",
			"nickname": "Nan3",
			"real_name": "小刘",
			"avatar": "",
			"role": 1
		}
	],
	"password": "",
	"meeting_type": 2,
	"plan_time": 1727409242,
	"plan_dur": 1,
	"entry_mute_policy": 2,
	"watermark_disabled": true,
	"screenshot_disabled": true,
	"self_unmute_mic_disabled": false,
	"self_unmute_camera_disabled": false,
	"mic_disabled": false,
	"camera_disabled": false,
	"share_disabled": false,
	"chat_disabled": true,
	"force_join": false,
	"auto_record": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| creator | uid3 | string | 否 | 会议创建者 |
| title | 标题 | string | 否 | 会议标题 |
| content | 说明 | string | 否 | 自定义内容 |
| attend_type | 3 | number | 否 | 1 无限制(默认) 2 密码进入 3 仅邀请人员参会 |
| conferee_details | - | array | 否 | 参会者列表 |
| conferee_details.user_id | s9zv4d | string | 是 | 用户ID |
| conferee_details.account | 13345678903 | string | 否 | 用户帐号 |
| conferee_details.nickname | Nan3 | string | 否 | 用户昵称 |
| conferee_details.real_name | 小刘 | string | 否 | 真实名称 |
| conferee_details.avatar | - | string | 否 | 用户头像 |
| conferee_details.role | 1 | number | 否 | 用户角色 |
| password | - | string | 否 | 密码，attend_type为2时必填 |
| plan_time | 1706178794 | number | 否 | 开始时间 (时间戳)，预约会议必填 |
| plan_dur | 10 | number | 否 | 持续时间(单位分钟)，预约会议必填 |
| entry_mute_policy | 3 | number | 否 | 入会静音状态 1:开启入会静音(所有人入会默认静音) 2:关闭(跟随客户端初始音频状态) 3：超6人静音(超过6人后入会静音) 默认值3 |
| watermark_disabled | true | boolean | 否 | true 关水印 false 不限 |
| screenshot_disabled | true | boolean | 否 | 截屏是否禁止 false:不禁止 true：禁止 |
| self_unmute_mic_disabled | false | boolean | 否 | 禁麦时禁止自我解除 false:不禁止(默认) true：禁止 |
| self_unmute_camera_disabled | false | boolean | 否 | 禁视频时禁止自我解除 false:不禁止(默认) true：禁止 |
| mic_disabled | false | boolean | 否 | 禁止开麦 false:不禁止(默认) true：禁止 |
| camera_disabled | false | boolean | 否 | 禁止开视频 false:不禁止(默认) true：禁止 |
| share_disabled | false | boolean | 否 | 禁止共享 false:不禁止(默认) true：禁止 |
| chat_disabled | true | boolean | 否 | true 禁止聊天 false 允许聊天 |
| force_join | false | boolean | 否 | 预约会议是否强制入会 |
| auto_record | false | boolean | 否 | 是否自动录像 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | integer | - |
| data | ok | string | - |

***

## 取消会议

**接口URL**

> /server/v1/meet/cancel

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o"
	"room_no": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | ok | string | - |

***

## 会议详情

**接口URL**

> /server/v1/meet/detail

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"id": "sny038",
		"room_no": "803707296",
		"title": "标题",
		"content": "说明",
		"creator": "uid3",
		"meeting_status": 1,
		"meeting_type": 1,
		"plan_time": 1727171730,
		"plan_dur": 10,
		"begin_time": 0,
		"end_time": 0,
		"password": "",
		"online_num": 0,
		"entry_mute_policy": 3,
		"watermark_disabled": true,
		"screenshot_disabled": true,
		"chat_disabled": true,
		"force_join": false,
		"locked": false,
		"share_state": 0,
		"mic_disabled": false,
		"camera_disabled": false,
		"self_unmute_mic_disabled": true,
		"self_unmute_camera_disabled": true,
		"conferee": [
			"s9zv4d"
		],
		"conferee_details": [
			{
				"user_id": "s9zv4d",
				"real_name": "南",
				"account": "13345678903",
				"avatar": "",
				"nickname": "Nan3",
				"role": 1
			}
		]
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | object | 返回数据 |
| data.id | sny038 | string | - |
| data.room_no | 803707296 | string | 会议号 |
| data.title | 标题 | string | 标题 |
| data.content | 说明 | string | - |
| data.creator | uid3 | string | 创建者 |
| data.meeting_status | 1 | number | 1未开始 2进行中 3已结束 |
| data.meeting_type | 1 | number | 1 即时会议 2 预约会议 |
| data.plan_time | 1727171730 | number | 开始时间 (时间戳)，预约会议必填 |
| data.plan_dur | 10 | number | - |
| data.begin_time | 0 | number | 开始时间 |
| data.end_time | 0 | number | 结束时间 |
| data.password | - | string | 密码 |
| data.online_num | 0 | number | - |
| data.entry_mute_policy | 3 | number | - |
| data.watermark_disabled | true | boolean | - |
| data.screenshot_disabled | true | boolean | - |
| data.chat_disabled | true | boolean | - |
| data.force_join | false | boolean | 预约会议是否强制入会 |
| data.locked | false | boolean | - |
| data.share_state | 0 | number | - |
| data.mic_disabled | false | boolean | - |
| data.camera_disabled | false | boolean | - |
| data.self_unmute_mic_disabled | true | boolean | - |
| data.self_unmute_camera_disabled | true | boolean | - |
| data.conferee | ["s9zv4d"] | array | 参会人员用户id数组 |
| data.conferee_details | - | array | 参会人员用户列表 |
| conferee_details.user_id | s9zv4d | string | 用户ID |
| conferee_details.account | 13345678903 | string | 用户帐号 |
| conferee_details.nickname | Nan3 | string | 用户昵称 |
| conferee_details.real_name | 小刘 | string | 真实名称 |
| conferee_details.avatar | - | string | 用户头像 |
| conferee_details.role | 1 | number | 用户角色 |

***

## 查询会议列表

**接口URL**

> /server/v1/meet/list-meet

**请求Body参数**

```javascript
{
	"page": 1,
	"per-page": 10,
	"room_no": "",
	"meeting_ids": [],
	"meeting_status": [1],
	"attendee_id": "",
	"creator": "",
	"begin_at": 0,
	"end_at": 0,
	"plan_begin_at": 0,
	"plan_end_at": 0
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| page | 1 | number | 否 | 分页页码，从1开始，默认为1 |
| per-page | 20 | number | 否 | 每页数据量，最大1000，默认20 |
| room_no | - | string | 否 | 房间号 |
| meeting_ids | [] | array | 否 | 会议id列表 |
| meeting_status | [1] | array | 否 | 会议状态 1 未开始 2 进行中 3 已结束 |
| creator | - | string | 否 | 创建人 |
| begin_at | 0 | number | 否 | 会议实际开始时间区间 |
| end_at | 0 | number | 否 | 会议实际开始时间区间 |
| plan_begin_at | 0 | number | 否 | 会议计划开始时间区间 |
| plan_end_at | 0 | number | 否 | 会议计划开始时间区间 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"id": "sk9o4v",
			"room_no": "678350614",
			"title": "刘君的会议 9.24   18:00",
			"content": "content",
			"meeting_status": 1,
			"meeting_type": 2,
			"plan_time": 1727172000,
			"plan_dur": 60,
			"begin_time": 0,
			"end_time": 0,
			"entry_mute_policy": 3,
			"watermark_disabled": true,
			"screenshot_disabled": false,
			"share_state": 0,
			"share_uid": "",
			"self_unmute_mic_disabled": true,
			"self_unmute_camera_disabled": true,
			"mic_disabled": false,
			"camera_disabled": false,
			"force_join" false,
			"locked": false,
			"chat_disabled": false,
			"auto_record": false,
			"conferee": ["s9zv4d"],
			"conferee_details": [
				{
					"user_id": "s9zv4d",
					"account": "13345678903",
					"nickname": "Nan3",
					"real_name": "小刘",
					"avatar": "",
					"role": 1
				}
			],
			"creator": "s9l7ng",
			"created_at": 1727168102,
			"updated_at": 1727170548
		}
	],
	"_meta": {
		"totalCount": 5,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.id | sny038 | string | 会议ID |
| data.room_no | 803707296 | string | 房间号 |
| data.title | 标题 | string | 会议标题 |
| data.content | 说明 | string | 会议说明 |
| data.meeting_status | 1 | number | 会议状态 |
| data.meeting_type | 1 | number | 会议类型 |
| data.plan_time | 1727163550 | number | - |
| data.plan_dur | 10 | number | - |
| data.begin_time | 0 | number | 开始时间时间戳 |
| data.end_time | 0 | number | 结束时间 |
| data.entry_mute_policy | 3 | number | 入会静音状态 默认2 1:开启入会静音(所有人入会默认静音) 2:关闭(跟随客户端初始音频状态) 3：超6人静音(超过6人后入会静音) |
| data.watermark_disabled | true | boolean | 水印状态  默认true  true:开启 false:关闭 |
| data.screenshot_disabled | true | boolean | 截屏状态 默认true  true：允许 false:不允许 |
| data.share_state | 0 | number | 共享状态 |
| data.share_uid | - | string | 共享者ID |
| data.self_unmute_mic_disabled | true | boolean | 房间允许禁音自我解除 默认true true:允许  false:不允许 |
| data.self_unmute_camera_disabled | true | boolean | 房间允许禁视频自我解除 默认true  true:允许  false:不允许 |
| data.mic_disabled | false | boolean | 房间关音频 默认false   true:关  false:不关 |
| data.camera_disabled | false | boolean | 房间关视频 默认false  true:关  false:不关 |
| data.force_join | false | boolean | 预约会议是否强制入会 |
| data.locked | false | boolean | 锁定状态 默认false  true:锁定 false:未锁定 |
| data.chat_disabled | true | boolean | 聊天模式  默认 true:开放 false:关闭 |
| data.auto_record | false | boolean | 是否自动录像 |
| data.conferee | ["s9zv4d"] | array | 参会人员用户id数组 |
| data.conferee_details | - | array | 参会人员用户列表 |
| conferee_details.user_id | s9zv4d | string | 用户ID |
| conferee_details.account | 13345678903 | string | 用户帐号 |
| conferee_details.nickname | Nan3 | string | 用户昵称 |
| conferee_details.real_name | 小刘 | string | 真实名称 |
| conferee_details.avatar | - | string | 用户头像 |
| conferee_details.role | 1 | number | 用户角色 |
| data.creator | uid3 | string | 创建都ID |
| data.created_at | 1727163550 | number | 创建时间 |
| data.updated_at | 1727163550 | number | 更新时间 |
| _meta | - | object | 页码信息 |
| _meta.totalCount | 29 | number | - |
| _meta.pageCount | 2 | number | - |
| _meta.currentPage | 1 | number | - |
| _meta.perPage | 20 | number | - |

***

## 会议相关人员

**接口URL**

> /server/v1/meet/meeting-users

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"page": 1,
	"per-page": 999
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| page | 1 | number | 否 | 分页页码，从1开始，默认为1 |
| per-page | 20 | number | 否 | 每页数据量，最大1000，默认20 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"user_id": "s9zv4d",
			"account": "13345678903",
			"nickname": "Nan3",
			"real_name": "小刘",
			"avatar": "",
			"role": 1,
			"is_invite": true,
			"enter_at": 1767664888,
			"exit_at": 0,
		}
	],
	"_meta": {
		"totalCount": 2,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | integer | - |
| data | - | array | - |
| data.user_id | s9zv4d | string | 用户ID |
| data.account | 13345678903 | string | 用户帐号 |
| data.nickname | Nan3 | string | 会中名称 |
| data.real_name | 小刘 | string | 真实名称 |
| data.avatar | - | string | 用户头像 |
| data.role | 1 | integer | 会中角色 |
| data.is_invite | true | bool | 是否邀约(白名单) |
| data.enter_at | 1767664888 | integer | 首次入会时间 |
| data.exit_at | 0 | integer | 最后离开会时间 |
| _meta | - | object | - |
| _meta.totalCount | 2 | integer | - |
| _meta.pageCount | 1 | integer | - |
| _meta.currentPage | 1 | integer | - |
| _meta.perPage | 20 | integer | - |

***

## 查询参会记录

**接口URL**

> /server/v1/meet/list-record

**请求Body参数**

```javascript
{
	"page": 1,
	"per-page": 20,
	"room_no": "",
	"meeting_id": "snxjl9",
	"user_id": "",
	"begin_at": 0,
	"end_at": 0
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| page | 1 | number | 否 | 分页页码，从1开始，默认为1 |
| per-page | 20 | number | 否 | 每页数据量，最大1000，默认20 |
| room_no | - | string | 否 | 房间号 |
| meeting_id | sny038 | string | 是 | 会议id |
| user_id | - | string | 否 | 参会用户ID |
| begin_at | 1705978569 | number | 否 | 开始时间 |
| end_at | 1705978569 | number | 否 | 结束时间 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"app_id": "78b3ft51smhz0x5glscw9whm78bw57uu",
			"meeting_id": "snxjl9",
			"user_id": "sq7z3d",
			"nickname": "13000000058",
			"mobile": "13000000058",
			"enter_time": 1767664888,
			"exit_time": 1767665526,
			"device_type": 6
		}
	],
	"_meta": {
		"totalCount": 2,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.app_id | 78b3ft51smhz0x5glscw9whm78bw57uu | string | 应用 |
| data.meeting_id | snxjl9 | string | 会议 |
| data.user_id | sq7z3d | string | 用户ID |
| data.nickname | 13000000058 | string | 会中昵称 |
| data.mobile | 13000000058 | string | 手机号码 |
| data.enter_time | 1767664888 | number | 进入时间 |
| data.exit_time | 1767665526 | number | 离开时间 |
| data.device_type | 6 | number | 设备类型 |
| _meta | - | object | 翻页信息 |
| _meta.totalCount | 2 | number | - |
| _meta.pageCount | 1 | number | - |
| _meta.currentPage | 1 | number | - |
| _meta.perPage | 20 | number | - |

***

## 修改参会人员

**接口URL**

> /server/v1/meet/update-conferee

**请求Body参数**

```javascript
{
	"meeting_id": "sk0222",
	"conferee_details": [
		{
			"user_id": "s9zv4d",
			"account": "13345678903",
			"nickname": "Nan3",
			"real_name": "小刘",
			"avatar": "",
			"role": 1
		}
	],
	"is_additional": true
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| meeting_id | sk8oep | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| conferee_details | - | array | 否 | 参会者列表 |
| conferee_details.user_id | s9zv4d | string | 是 | 用户ID |
| conferee_details.account | 13345678903 | string | 否 | 用户帐号 |
| conferee_details.nickname | Nan3 | string | 否 | 用户昵称 |
| conferee_details.real_name | 小刘 | string | 否 | 真实名称 |
| conferee_details.avatar | - | string | 否 | 用户头像 |
| conferee_details.role | 1 | number | 否 | 用户角色 |
| is_additional | false | boolean | 否 | 是否增量添加 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| code | 0 | number | 错误码 |

* 失败(404)

```javascript
{
	"code": 2103,
	"msg": "会议已结束"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| code | 2103 | number | 错误码 |
| msg | 会议已结束 | string | 返回文字描述 |

***

## 移除参会人员

**接口URL**

> /server/v1/meet/delete-conferee

**请求Body参数**

```javascript
{
	"meeting_id": "sk0222",
	"user_ids": ["s9zv4d"]
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| meeting_id | sk8oep | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| user_ids | ["s9zv4d"] | array | 是 | 用户ID列表 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| code | 0 | number | 错误码 |

* 失败(404)

```javascript
{
	"code": 2103,
	"msg": "会议已结束"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| code | 2103 | number | 错误码 |
| msg | 会议已结束 | string | 返回文字描述 |

***

## 用户聊天记录

**接口URL**

> /server/v1/meet/user-chat-record

**请求Body参数**

```javascript
{
	"page": 1,
	"per-page": 20,
	"room_no": "",
	"meeting_id": "snxjl9",
	"sender_id": "",
	"begin_at": 0,
	"end_at": 0,
	"sort": "id"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| page | 1 | number | 否 | 分页页码，从1开始，默认为1 |
| per-page | 20 | number | 否 | 每页数据量，最大1000，默认20 |
| room_no | - | string | 否 | 房间号 |
| meeting_id | sny038 | string | 在room_no空时必填 | 会议id |
| sender_id | - | string | 否 | 发言者用户ID |
| begin_at | 1705978569 | number | 否 | 开始时间 |
| end_at | 1705978569 | number | 否 | 结束时间 |
| sort | -id | string | 否 | 默认按id(即创建时间)降序, "id"表示升序 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"id": "bw57uu",
			"meeting_id": "snxjl9",
			"sender_id": "sq7z3d",
			"sender_name": "13000000058",
			"real_name": "小王",
			"role": 1,
			"msg_type": 1,
			"msg": "消息内容",
			"created_at": 1767665526
		}
	],
	"_meta": {
		"totalCount": 2,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.id | bw57uu | string | 记录ID |
| data.meeting_id | snxjl9 | string | 会议ID |
| data.sender_id | sq7z3d | string | 发送者用户ID |
| data.sender_name | 13000000058 | string | 发送者用户名称 |
| data.real_name | 小王 | string | 发送者真实名称 |
| conferee_details.role | 1 | number | 用户角色 |
| data.msg_type | 1 | number | 消息类型 1文本 2文件 3图片 4语音 |
| data.msg | 消息内容 | string | 聊天内容 |
| data.created_at | 1767665526 | number | 发送时间 |
| _meta | - | object | 翻页信息 |
| _meta.totalCount | 2 | number | - |
| _meta.pageCount | 1 | number | - |
| _meta.currentPage | 1 | number | - |
| _meta.perPage | 20 | number | - |

***

## 聊天记录文件

**接口URL**

> /server/v1/meet/chat-record-files

**请求Body参数**

```javascript
{
	"room_no": "",
	"meeting_id": "snxjl9"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| room_no | - | string | 否 | 房间号 |
| meeting_id | sny038 | string | 在room_no空时必填 | 会议id |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"name": "会议的名称",
			"size": 102400,
			"key": "snxjl9/chat.pdf",
			"url": "http://xxxxx"
		}
	]
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.name | 会议的名称 | string | 文件名称 |
| data.size | 102400 | number | 文件大小(字节) |
| data.key | snxjl9/chat.pdf | string | 文件的Key |
| data.url | http://xxxxx | string | 文件下载地址 |

***

## 设置事件通知

**接口URL**

> /server/v1/meet/set-callback

**请求Body参数**

```javascript
{
	"events": [
		"meeting_status_change"
	],
	"cb_url": "http://domain.com/callback"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| events | - | array | 否 | 事件类型列表 |
| events.0 | meeting_status_change | string | 是 | 某个事件类型 |
| cb_url | http://domain.com/event/callback | string | 否 | 通知地址 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |

**事件通知的配置方式**

> 通过当前接口(`设置事件通知`)来配置回调。<br/>
> 上层业务方应当在业务服务启动时调用此接口来配置回调地址与监听的事件列表，<br/>
> 也建议在业务服务停止/卸载时同样来调用此接口设置回调地址与事件列表为空。

**事件通知方式**

1.**POST application/json 请求**

> Header头额外项及签名验证方法与`接口调用说明`完全相同<br/>
> 请求的URL尾部会自动附加事件类型参数`?event=xxxxx`<br/>
> 请求体为json串, 结构定义示例如下

```json
{
	"time": 1721731326, //事件发生时间
	"event": "meeting_status_change", //所属事件
	"app_id": "68b3ft51smhz0x5glscw9whm78bw57uu", //应用ID
	"data": {
		"meeting_id": "abcdefg",
		"from_status": 0, //(改变前的)会议状态: 0无意义,1未开始,2会议中,3已结束
		"to_status": 1,  //(改变后的)会议状态
	} //详细业务参数,可能为null值
}
```

2.**异步通知重试策略**

	- http响应超过5秒, 或响应的http状态不是200时判定为失败
	- 响应数据体中code不是0时判定为失败
	- 首次失败2秒后重试, 之后每隔10秒重试, 共重试5次

```json
// 异步通知要求的响应体格式
{
	"code": 0,         // 必填, 非0值表示有错误
	"msg": "错误消息",  // 可选
	"data": null       // 可选, json对象
}
```

3.**events支持的事件及data对象中字段的定义**

- 会议状态变化 **`meeting_status_change`**

| 字段名 | 类型 | 示例值 | 字段说明 |
| --- | --- | --- | --- |
| meeting_id | string | snxjl9 | 会议ID |
| room_no | string | 776868796 | 房间号 |
| from_status | number | 0 | 改变前的会议状态: 0无意义,1未开始,2会议中,3已结束 |
| to_status | number | 1 | 改变后的会议状态：1未开始,2会议中,3已结束 |

- 用户进入会议 **`user_enter`**

| 字段名 | 类型 | 示例值 | 字段说明 |
| --- | --- | --- | --- |
| meeting_id | string | snxjl9 | 会议ID |
| room_no | string | 776868796 | 房间号 |
| user_id | string | sq7z3d | 用户ID |
| account | string | 13000000058 | 用户帐号 |
| real_name | string | 王生 | 真实名称 |
| nickname | string | 小帅 | 会中昵称 |
| role | number | 0 | 会中角色 |

- 用户退出会议 **`user_exit`**

| 字段名 | 类型 | 示例值 | 字段说明 |
| --- | --- | --- | --- |
| meeting_id | string | snxjl9 | 会议ID |
| room_no | string | 776868796 | 房间号 |
| user_id | string | sq7z3d | 用户ID |
| account | string | 13000000058 | 用户帐号 |
| real_name | string | 王生 | 真实名称 |
| nickname | string | 小帅 | 会中昵称 |
| role | number | 0 | 会中角色 |
| reason | number | 0 | 离开原因 1主动离开, 2被踢, 3被顶号 4心跳超时, 5会议结束 |
| online | number | 0 | 离开后会中在线人数 |

- MCU状态变化 **`mcu_status_change`**

| 字段名 | 类型 | 示例值 | 字段说明 |
| --- | --- | --- | --- |
| meeting_id | string | snxjl9 | 会议ID |
| room_no | string | 776868796 | 房间号 |
| task_id | string | swy0ej | MCU任务ID |
| task_type | number | 1 | 1录像模式 2合流模式 4录音模式 8直播流模式 |
| task_status | number | 0 | 0待开始 1进行中 2待结束 3异常结束 4正常结束 |

- MCU录像完成 **`mcu_record_done`**

| 字段名 | 类型 | 示例值 | 字段说明 |
| --- | --- | --- | --- |
| meeting_id | string | snxjl9 | 会议ID |
| room_no | string | 776868796 | 房间号 |
| task_id | string | swy0ej | MCU任务ID |
| task_type | number | 1 | 1录像模式 2合流模式 4录音模式 8直播流模式 |
| vod_key | string | mcu/record/rtc_s36v41/record/20250624_021129/index.m3u8 | 录像文件Key |
| vod_size | number | 949517 | 录像大小(字节) |
| mcu_dur | number | 33 | 录像时长(秒) |

- MCU警告 **`mcu_alarm`**

| 字段名 | 类型 | 示例值 | 字段说明 |
| --- | --- | --- | --- |
| meeting_id | string | snxjl9 | 会议ID |
| room_no | string | 776868796 | 房间号 |
| title | string | 会议标题 | MCU任务标题 |
| task_id | string | swy0ej | MCU任务ID |
| task_type | number | 1 | 1录像模式 2合流模式 4录音模式 8直播流模式 |
| task_status | number | 0 | 0待开始 1进行中 2待结束 3异常结束 4正常结束 |
| gw | string | gw1 | 任务所在网关 |
| alarm_at | number | 1721731326 | 报警时间戳 |
| alarm_brief | string | 网络不稳定 | 报警摘要 |

***

# 会中操作

## 结束会议

**接口URL**

> /server/v1/meet-admin/destroy

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 更新会议全体禁音频

**接口URL**

> /server/v1/meet-admin/update-room-mic-state

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"mic_disabled": true,
	"self_unmute_mic_disabled": true
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| mic_disabled | true | boolean | 是 | true 全体静音 false 解除全体静音 |
| self_unmute_mic_disabled | true | boolean | 是 | true 不允许成员自我解除静音 false 允许成员自我解除静音 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 更新会议全体禁视频

**接口URL**

> /server/v1/meet-admin/update-room-camera-state

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"camera_disabled": false,
	"self_unmute_camera_disabled": true
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| camera_disabled | false | boolean | 是 | true 全体关闭摄像头 false 解除全体关闭摄像头 |
| self_unmute_camera_disabled | true | boolean | 是 | true 不允许成员自我开摄像头 false 允许成员自我开摄像头 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 更新会议全体禁共享

**接口URL**

> /server/v1/meet-admin/update-room-share-disabled

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"share_disabled": true
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| share_disabled | true | boolean | 是 | true 全体禁止共享 false 解除全体禁共享 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 更新会议锁定状态

**接口URL**

> /server/v1/meet-admin/update-locked

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"locked": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| locked | true | boolean | 是 | true 房间锁定  false 不锁定 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 更改会议水印开关状态

**接口URL**

> /server/v1/meet-admin/update-watermark-disabled

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"watermark_disabled": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| watermark_disabled | true | boolean | 是 | true 关水印 false 不限 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 更新会议聊天禁用状态

**接口URL**

> /server/v1/meet-admin/update-room-chat-disabled

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"chat_disabled": true
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| chat_disabled | true | boolean | 是 | true 禁止聊天 false 允许聊天 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 修改会议截屏限制

**接口URL**

> /server/v1/meet-admin/update-room-screenshot-disabled

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": ""
	"screenshot_disabled": true
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| screenshot_disabled | true | boolean | 是 | true:禁止截屏 false:允许截屏 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 修改会议中用户名称

**接口URL**

> /server/v1/meet-admin/update-user-name

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03",
	"nickname": "nickname"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |
| nickname | nickname | string | 是 | 昵称 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 修改会议中用户角色

**接口URL**

> /server/v1/meet-admin/update-user-role

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03",
	"role": 1
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |
| role | 1 | number | 是 | 0 普通成员 1 主持人 2 联席主持人 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 会中踢人

**接口URL**

> /server/v1/meet-admin/kickout-user

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03",
	"remove_conferee": false,
	"join_disabled": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |
| remove_conferee | false | bool | 否 | 是否从白名单中移除 |
| join_disabled | false | bool | 否 | 是否黑名单 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 请求用户共享

**接口URL**

> /server/v1/meet-admin/request-user-share

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 结束进行中的共享

**接口URL**

> /server/v1/meet-admin/stop-room-share

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 请求用户打开摄像头

**接口URL**

> /server/v1/meet-admin/request-user-open-camera

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 关闭用户摄像头

**接口URL**

> /server/v1/meet-admin/close-user-camera

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 请求用户打开麦克风

**接口URL**

> /server/v1/meet-admin/request-user-open-mic

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 关闭用户麦克风

**接口URL**

> /server/v1/meet-admin/close-user-mic

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 处理举手申请

**接口URL**

> /server/v1/meet-admin/confirm-handup

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"target_id": "user03",
	"code": 1,
	"approve": true
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| target_id | user03 | string | 是 | 用户id |
| code | 1 | number | 是 | 1 申请开音频 2 申请开视频 3 申请聊天 |
| approve | true | boolean | 是 | true 允许 false 不允许 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 会中发送自定义消息

**接口URL**

> /server/v1/meet/send-room-custom-message

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"content": "hello",
	"target_id": "sgxkm9"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| content | - | string | 是 | 自定义内容 |
| target_id | 目标用户ID | string | 否 | 为空时表示全房间接收 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "ok"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | string | ok | 返回数据 |

***

## 查询会中人员列表

**接口URL**

> /server/v1/meet/list-user

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"page": 1,
	"per-page": 999
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| page | 1 | number | 否 | 分页页码，从1开始，默认为1 |
| per-page | 20 | number | 否 | 每页数据量，最大1000，默认20 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"user_id": "s9zv4d",
			"nickname": "Nan3",
			"role": 1,
			"mic_state": 1,
			"camera_state": 1,
			"share_state": 0,
			"device_type": 6,
			"extend_info": "",
			"join_at": 1767664888
		}
	],
	"_meta": {
		"totalCount": 2,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | integer | - |
| data | - | array | - |
| data.user_id | s9zv4d | string | 用户ID |
| data.nickname | Nan3 | string | 会中名称 |
| data.role | 1 | integer | 会中角色 |
| data.mic_state | 1 | integer | 音频状态 1开, 2关 |
| data.camera_state | 1 | integer | 视频状态 1开, 2关 |
| data.share_state | 0 | integer | 共享状态 0无, 1屏幕 2白板 |
| data.device_type | 6 | integer | 终端设备类型 |
| data.extend_Info | - | string | 扩展信息 |
| data.join_at | 1767664888 | integer | 进入时间 |
| _meta | - | object | - |
| _meta.totalCount | 2 | integer | - |
| _meta.pageCount | 1 | integer | - |
| _meta.currentPage | 1 | integer | - |
| _meta.perPage | 20 | integer | - |

***

## 会议时呼叫人员

**接口URL**

> /server/v1/meet-admin/call-users

**请求Body参数**

```javascript
{
	"meeting_id": "snj20o",
	"room_no": "",
	"conferee_details": [
		{
			"user_id": "s9zv4d",
			"account": "13345678903",
			"nickname": "Nan3",
			"real_name": "小刘",
			"avatar": "",
			"role": 1
		}
	],
	"is_additional": false,
	"force_join": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| meeting_id | skgvpk | string | 在room_no空时必填 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| conferee_details | - | array | 否 | 参会者列表 |
| conferee_details.user_id | s9zv4d | string | 是 | 用户ID |
| conferee_details.account | 13345678903 | string | 否 | 用户帐号 |
| conferee_details.nickname | Nan3 | string | 否 | 用户昵称 |
| conferee_details.real_name | 小刘 | string | 否 | 真实名称 |
| conferee_details.avatar | - | string | 否 | 用户头像 |
| conferee_details.role | 1 | number | 否 | 用户角色 |
| is_additional | false | boolean | 否 | 是否增量添加 |
| force_join | false | boolean | 否 | 是否强制入会 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| code | 0 | number | 错误码 |

* 失败(404)

```javascript
{
	"code": 2103,
	"msg": "会议已结束"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | ---- | ---- |
| code | 2103 | number | 错误码 |
| msg | 会议已结束 | string | 返回文字描述 |

***

# MCU任务

## 开始/更新MCU任务

**接口URL**

> /server/v1/mcu/start

**请求Body参数**

```javascript
{
	"meeting_id": "sk78ge",
	"room_no": "",
	"task_type": 1,
	"title": "第四次测试",
	"op_uid": "",
	"op_name": "",
	"layout_data": {
		"layout": "auto",
		"is_polling": false,
		"watermark": {
			"type": 0,
			"text": "",
			"size": 0,
			"color": "",
			"ol_color": "",
			"ol_width": 0
		},
		"tag": {
			"type": "L",
			"text": "",
			"size": 0,
			"color": "",
			"bg_color": ""
		},
		"div_list": [
			{
				"cells": [
					{
						"idx": 0,
						"bind_share": false,
						"tag": {
							"type": "L",
							"text": "",
							"size": 0,
							"color": "",
							"bg_color": ""
						}
					}
				],
				"uids": [
					"uid0",
					"uid1"
				]
			}
		]
	}
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | sk78ge | string | 在room_no空时必填 | 会议ID |
| room_no | - | string | 否 | 房间号 |
| task_type | 1 | number | 是 | 1录像模式 2合流模式 3混合模式 |
| title | 第四次测试 | string | 否 | 任务标题 |
| op_uid | - | string | 否 | 任务发起人ID |
| op_name | - | string | 否 | 任务发起人名称 |
| layout_data | - | object | 是 | 布局数据 |
| layout_data.layout | auto | string | 否 | auto 自动布局 full 全屏 grids_2 二等分  grids_3 品字形 grids_4 四宫格 grids_5 五宫格 grids_6 六宫格 grids_8 八宫格 grids_9 九宫格  grids_12 十二宫格 grids_16 十六宫格 grids_20 二十宫格 grids_25 二十五宫格 right_4 右侧小窗口 top_4 顶部小窗口 br_7 下L型布局 tl_7 上L型布局 tb_8 左右布局 |
| layout_data.is_polling | false | boolean | 否 | 是否轮询 |
| layout_data.watermark | - | object | 否 | 水印 |
| layout_data.watermark.type | 0 | number | 否 | 类型 0默认, 1无, 2单排, 3多排 |
| layout_data.watermark.text | - | string | 否 | 指定内容, 空表示自动(会议标题) |
| layout_data.watermark.size | 0 | number | 否 | 字体大小, 0表示默认值 |
| layout_data.watermark.color | 0xFFFFFF22 | string | 否 | 字体颜色(0xFFFFFFFF)最后两位表示透明度, 空表示默认值 |
| layout_data.watermark.ol_color | 0x00000022 | string | 否 | 轮廓颜色, 空表示默认值 |
| layout_data.watermark.ol_width | 0 | number | 否 | 轮廓线宽, 0表示默认值 |
| layout_data.tag | - | object | 否 | - |
| layout_data.tag.type | L | string | 否 | 类型, 字母或组合: L左, R右, T上, B下 |
| layout_data.tag.text | - | string | 否 | 指定内容, 空表示自动(会中名称) |
| layout_data.tag.size | 0 | number | 否 | 字体大小, 0表示默认 |
| layout_data.tag.color | 0xFFFFFFFF | string | 否 | 字体颜色, 空表示默认 |
| layout_data.tag.bg_color | 0x0000004D | string | 否 | 背景颜色, 空表示默认 |
| layout_data.div_list | - | array | 否 | 逻辑块, 包含宫格与用户 |
| layout_data.div_list.cells | - | array | 否 | 宫格列表, 空表示剩余格子共用此处的用户 |
| layout_data.div_list.cells.idx | 0 | number | 否 | 格子序号, 排序规则按HTML中&lt;td&gt;标签的顺序 |
| layout_data.div_list.cells.bind_share | false | boolean | 否 | 是否优化绑定频道内的共享流 |
| layout_data.div_list.cells.tag | - | object | 否 | 标签 |
| layout_data.div_list.cells.tag.type | L | string | 否 | 类型, 字母或组合: L左, R右, T上, B下 |
| layout_data.div_list.cells.tag.text | - | string | 否 | 指定内容, 空表示自动(会中名称) |
| layout_data.div_list.cells.tag.size | 0 | number | 否 | 字体大小, 0表示默认 |
| layout_data.div_list.cells.tag.color | 0xFFFFFFFF | string | 否 | 字体颜色, 空表示默认 |
| layout_data.div_list.cells.tag.bg_color | 0x0000004D | string | 否 | 背景颜色, 空表示默认 |
| layout_data.div_list.uids | - | array | 否 | 用户ID列表, 空表示大轮询在线剩余用户, 多个表示小轮询 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"task_id": "sxjgwy"
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | object | 返回数据 |
| data.task_id | sxjgwy | string | 任务ID |

***

## 结束MCU任务

**接口URL**

> /server/v1/mcu/stop

**请求Body参数**

```javascript
{
	"meeting_id": "sk78ge",
	"room_no": "",
	"task_type": 1
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | sk78ge | string | 在room_no空时必填 | 会议ID |
| room_no | - | string | 否 | 房间号 |
| task_type | 0 | number | 否 | 任务类型 1录像模式 2合流模式 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"task_id": "szyeqy"
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | object | 返回数据 |
| data.task_id | szyeqy | string | 任务id |

***

## 获取录像配置

**接口URL**

> /server/v1/mcu/record-config

**请求Body参数**

```javascript
{}
```

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"app_id": "68b3ft51smhz0x5glscw9whm78bw57uu",
		"layout": "auto",
		"watermark_type": 1,
		"window_tag_type": "",
		"created_at": 1730099431,
		"updated_at": 1730099431
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | object | 返回数据 |
| data.app_id | 68b3ft51smhz0x5glscw9whm78bw57uu | string | 应用的id |
| data.layout | auto | string | auto 自动布局 full 全屏 grids_2 二等分 grids_4 四宫格 grids_5 五宫格 grids_6 六宫格 grids_8 八宫格 grids_9 九宫格 grids_10 十宫格  grids_12 十二宫格 grids_16 十六宫格 grids_25 二十五宫格 right_4 右侧小窗口 top_4 顶部小窗口 br_7 下L型布局 tl_7 上L型布局 tb_8 左右布局 |
| data.watermark_type | 1 | number | 1无, 2单排, 3多排 |
| data.window_tag_type | - | string | 窗口标签位置 字母或组合: L左, R右, T上, B下, 空表示不启用标签 |
| data.created_at | 1730099431 | number | - |
| data.updated_at | 1730099431 | number | - |

***

## 保存录像配置

**接口URL**

> /server/v1/mcu/save-record-config

**请求Body参数**

```javascript
{
	"app_id": "78b3ft51smhz0x5glscw9whm78bw57uu",
	"layout": "auto",
	"watermark_type": 1,
	"window_tag_type": "LT"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| layout | auto | string | 是 | auto 自动布局 full 全屏 grids_2 二等分 grids_4 四宫格 grids_5 五宫格 grids_6 六宫格 grids_8 八宫格 grids_9 九宫格 grids_10 十宫格  grids_12 十二宫格 grids_16 十六宫格 grids_25 二十五宫格 right_4 右侧小窗口 top_4 顶部小窗口 br_7 下L型布局 tl_7 上L型布局 tb_8 左右布局 |
| watermark_type | 1 | string | 是 | 1无, 2单排, 3多排 |
| window_tag_type | - | string | 是 | 窗口标签位置 字母或组合: L左, R右, T上, B下, 空表示不启用标签 |

**响应示例**

* 成功(200)

```javascript
{"code":0}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |

***

## 录像详情

**接口URL**

> /server/v1/mcu/record-detail

**请求Body参数**

```javascript
{
	"task_id": "s9361j"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| task_id | - | string | 否 | 任务ID |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"task_id": "swy0ej",
			"op_uid": "",
			"op_name": "",
			"channel": "fire",
			"title": "第三次测试",
			"room_no": "swy0ej",
			"task_status": 54,
			"err_desc": "",
			"vod_key": "mcu/swy0ej/1696eb928b7c45509c30b50c67864cbe.mp4",
			"vod_size": 27,
			"tags": "",
			"McuAt": 27,
			"McuDur": 83,
			"created_at": 68,
			"updated_at": 84
		}
	],
	"_meta": {
		"totalCount": 51,
		"pageCount": 24,
		"currentPage": 32,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | 状态码 |
| data | - | array | 返回数据 |
| data.task_id | swy0ej | string | 任务ID |
| data.op_uid | - | string | 任务发起人ID |
| data.op_name | - | string | 任务发起人名称 |
| data.channel | fire | string | 频道名称 |
| data.title | 第三次测试 | string | 频道标题 |
| data.room_no | swy0ej | string | 外部会议号 |
| data.task_status | 54 | number | 0待开始 1进行中 2待结束 3异常结束 4正常结束 |
| data.err_desc | - | string | 错误描述 |
| data.vod_key | mcu/swy0ej/1696eb928b7c45509c30b50c67864cbe.mp4 | string | 录像文件key |
| data.vod_size | 27 | number | 录像大小(字节) |
| data.tags | - | string | 录像标签 逗号隔开 |
| data.McuAt | 27 | number | MCU开发台时间(秒) |
| data.McuDur | 83 | number | MCU持续时间 |
| data.created_at | 68 | number | 创建 |
| data.updated_at | 84 | number | 更新时间 |
| _meta | - | object | 页码信息 |
| _meta.totalCount | 51 | number | 总记录数 |
| _meta.pageCount | 24 | number | 总页数 |
| _meta.currentPage | 32 | number | 当前页码 |
| _meta.perPage | 20 | number | 每页记录数 |

***

## 删除录像

**接口URL**

> /server/v1/mcu/del-record

**请求Body参数**

```javascript
{
	"task_id": "s9361j",
	"channel": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| app_id | 68b3ft51smhz0x5glscw9whm78bw57uu | string | 是 | 应用ID |
| task_id | szyeqy | string | 否 | 任务ID频道(二选一) |
| channel | - | string | 否 | 频道(二选一) |

**响应示例**

* 成功(200)

```javascript
{"code":0}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |

***

## 修改录像

**接口URL**

> /server/v1/mcu/update-record

**请求Body参数**

```javascript
{
	"task_id": "s9361j",
	"title": "第三次测试",
	"tags": [
		"标签1"
	]
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| task_id | swy0ej | string | 否 | 任务ID |
| title | 第三次测试 | string | 否 | 标题 |
| tags | - | array | 否 | 标签 |

**响应示例**

* 成功(200)

```javascript
{"code":0}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |

***

## 录像列表

**接口URL**

> /server/v1/mcu/list-record

**请求Body参数**

```javascript
{
	"meeting_id": "sk78ge",
	"room_no": "",
	"begin_at": 1747276170,
	"end_at": 0,
	"sort": "created_at",
	"page": 1,
	"per-page": 20
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | sk78ge | string | 否 | 会议ID |
| room_no | 776868796 | string | 否 | 房间号 |
| begin_at | 1747276170 | number | 否 | 开始时间 |
| end_at | 0 | number | 否 | 结束时间 |
| sort | created_at | string | 否 | 排序 created_at |
| page | 1 | number | 否 | 分页页码，数字类型 |
| per-page | 20 | number | 否 | 分页页码，数字类型 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"task_id": "s7nmy1",
			"op_uid": "",
			"op_name": "system",
			"channel": "sk78ge",
			"title": "SailorGa-6预约的会议",
			"room_no": "757965104",
			"task_status": 4,
			"err_desc": "",
			"vod_key": "mcu-dev/record/rtc_s36v41/record/20250624_021129.mp4",
			"vod_size": 949517,
			"mcu_at": 1750731125,
			"mcu_dur": 33,
			"tags": "",
			"created_at": 1750731086,
			"updated_at": 1756094309
		}
	],
	"_meta": {
		"totalCount": 2,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.task_id | s7nmy1 | string | MCU任务 |
| data.op_uid | - | string | 任务发起人ID |
| data.op_name | system | string | 任务发起人名称 |
| data.channel | sk78ge | string | 会议ID |
| data.title | SailorGa-6预约的会议 | string | 会议标题 |
| data.room_no | 757965104 | string | 外部会议号 |
| data.task_status | 4 | number | 0待开始 1进行中 2待结束 3异常结束 4正常结束 |
| data.err_desc | - | string | MCU任务错误描述 |
| data.vod_key | mcu-dev/record/rtc_s36v41/record/20250624_021129.mp4 | string | 录像文件key |
| data.vod_size | 949517 | number | 录像大小(字节) |
| data.mcu_at | 1750731125 | number | MCU任务开始时间 |
| data.mcu_dur | 33 | number | 录像时长 |
| data.tags | - | string | 录像标签 逗号隔开 |
| data.created_at | 1750731086 | number | 创建时间 |
| data.updated_at | 1756094309 | number | 更新时间 |
| _meta | - | object | 页码信息 |
| _meta.totalCount | 2 | number | - |
| _meta.pageCount | 1 | number | - |
| _meta.currentPage | 1 | number | - |
| _meta.perPage | 20 | number | - |

***

## 录像播放地址

**说明：**
一般用于根据上面的"录像列表"中的数据，用task_id来获取单个录像的播放地址。传`meeting_id`参数时仅返回最后一个录像的播放地址。

**接口URL**

> /server/v1/mcu/vod-url

**请求Body参数**

```javascript
{
	"task_id": "sj98en",
	"meeting_id": "sk78ge",
	"is_lan": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| task_id | sj98en | string | 否 | 任务ID (没有会议ID时必填) |
| meeting_id | sk78ge | string | 否 | 会议ID (没有任务ID时必填) |
| is_lan | false | bool | 否 | 是否地址局域网 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"url": "http://192.168.0.222:9098/mcu-dev/mcu/swy0ej/1696eb928b7c45509c30b50c67864cbe.mp4?AWSAccessKeyId=minio&Expires=1730434361&Signature=ZhBC0YR7e%2B6ehZ%2BmkV8q2HQmUlg%3D",
		"size": 27502682,
		"mcu_at": 1762826916,
		"mcu_dur": 95
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | object | 返回数据 |
| data.url | http://192.168.0.222:9098/... | string | 播放/下载地址 2小时有效 |
| data.size | 27502682 | number | 录像大小(字节) |
| data.mcu_at | 1762826916 | number | 开始时间(时间戳) |
| data.mcu_dur | 95 | number | 录制时长(秒) |


***

## 会议的多录像播放地址

**说明：**
一场会议可能有多个录像。

**接口URL**

> /server/v1/mcu/vods-url

**请求Body参数**

```javascript
{
	"meeting_id": "sk78ge",
	"room_no": "",,
	"is_lan": false
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | sk78ge | string | 在room_no空时必填 | 会议ID |
| room_no | - | string | 否 | 房间号 |
| is_lan | false | bool | 否 | 是否局域网地址 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"url": "http://192.168.0.222:9098/mcu-dev/mcu/swy0ej/1696eb928b7c45509c30b50c67864cbe.mp4?AWSAccessKeyId=minio&Expires=1730434361&Signature=ZhBC0YR7e%2B6ehZ%2BmkV8q2HQmUlg%3D",
			"size": 27502682,
			"mcu_at": 1762826916,
			"mcu_dur": 95
		}
	]
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.url | http://192.168.0.222:9098/... | string | 播放/下载地址 2小时有效 |
| data.size | 27502682 | number | 录像大小(字节) |
| data.mcu_at | 1762826916 | number | 开始时间(时间戳) |
| data.mcu_dur | 95 | number | 录制时长(秒) |

***

## 获取直播流地址

**接口URL**

> /server/v1/mcu/live-url

**请求Body参数**

```javascript
{
	"meeting_id": "sk78ge",
	"room_no": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| meeting_id | sk78ge | string | 否 | 任务ID (没有会议ID时必填) |
| room_no | sk78ge | string | 否 | 会议ID (没有任务ID时必填) |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"rtmp":"rtmp://......",
		"hls":"http://......",
		"http-flv":"http://......"
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | object | 返回数据 |
| data.rtmp | rtmp://...... | string | RTMP流地址 |
| data.hls | http://...... | string | m3u8/ts地址 |
| data.http-flv | http://...... | string | http-flv流地址 |

***

# 设备管理

## 新增设备

**接口URL**

> /server/v1/agent/create?type=regsip

**请求Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| type | regsip | string | 是 | ipsip ip直连sip<br/>regsip 注册模式sip<br/>iph323 ip直连h323<br/>regh323 注册模式h323<br/>rtsp RTSP拉流 |

**请求Body参数**

```javascript
{
	"uri": "192.168.0.189:5060",
	"username": "huaweisip",
	"auth_pwd": "hw",
	"display_name": "华为sip直连",
	"gw": "devgw-1",
	"remark": "备注"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| uri | 192.168.0.8:5060 | string | 是 | rtsp或ip直连模式必填 |
| username | huaweisip | string | 是 | sip用户名或323短号，注册模式必填，H323只能是数字型短号 |
| auth_pwd | hw | string | 是 | 认证密码，注册模式必填 |
| display_name | 华为sip直连 | string | 是 | 显示名称 |
| gw | devgw-1 | string | 是 | 设备网关唯一id |
| remark | 备注 | string | 否 | 备注 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "sw8kjx"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | sw8kjx | string | 返回数据 |

***

## 修改设备

**接口URL**

> /server/v1/agent/update?type=regsip

**请求Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| type | regsip | string | 是 | ipsip ip直连sip<br/>regsip 注册模式sip<br/>iph323 ip直连h323<br/>regh323 注册模式h323<br/>rtsp RTSP拉流 |

**请求Body参数**

```javascript
{
	"id": "sw8kjx",
	"uri": "192.168.0.189:5060",
	"username": "huaweisip",
	"auth_pwd": "hw",
	"display_name": "华为sip直连",
	"gw": "devgw-1",
	"remark": "备注"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| id | sw8kjx | string | 是 | 设备ID |
| uri | 192.168.0.189:5060 | string | 是 | rtsp或ip直连模式必填 |
| username | huaweisip | string | 是 | sip用户名或323短号，注册模式必填，H323只能是数字型短号 |
| auth_pwd | hw | string | 是 | 认证密码，注册模式必填 |
| display_name | 华为sip直连 | string | 是 | 显示名称 |
| gw | devgw-1 | string | 是 | 设备网关唯一id |
| remark | 备注 | string | 否 | 备注 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "sw8kjx"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | sw8kjx | string | 返回数据 |

***

## 设备列表

设备列表，最终由应用层封装接口给应用层前端调用

**接口URL**

> /server/v1/agent/list

**请求Body参数**

```javascript
{
	"type": [2,3],
	"keyword": "huawei",
	"page": 1,
	"per-page": 20
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| type | [2] | array | 是 | 设备类型(目前仅支持2 3 5) 2SIP,3H323,4GB28181,5RTSP拉流,6RTMP拉流,7文件播放,8腾讯会议,9AI |
| keyword | huawei | string | 否 | 搜索关键词 |
| page | 1 | number | 否 | 分页页码，数字类型，从1开始，默认1 |
| per-page | 20 | number | 否 | 每页数据量，最大1000，默认20 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"id": "sz8nk8",
			"name": "华为sip终端",
			"type": 2,
			"status": 1,
			"contact": "huaweisip",
			"remark": ""
		}
	],
	"_meta": {
		"totalCount": 1,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.id | sz8nk8 | string | 设备ID |
| data.name | 华为sip终端 | string | - |
| data.type | 2 | number | 设备类型 2SIP,3H323,4GB28181,5RTSP拉流,6RTMP拉流,7文件播放,8腾讯会议,9AI |
| data.status | 1 | number | 设备状态，0 未知<br/>1 在线<br/>2 离线 |
| data.contact | huaweisip | string | 设备标识，注册模式是用户名，直连模式是uri |
| data.remark | - | string | 备注 |
| _meta | - | object | - |
| _meta.totalCount | 1 | number | - |
| _meta.pageCount | 1 | number | - |
| _meta.currentPage | 1 | number | - |
| _meta.perPage | 20 | number | - |

***

## 设备网关列表

**接口URL**

> /server/v1/agent/list-gw?type=regsip

**Content-Type**

> none

**请求Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| type | regsip | string | 是 | ipsip ip直连sip<br/>regsip 注册模式sip<br/>iph323 ip直连h323<br/>regh323 注册模式h323<br/>rtsp RTSP拉流 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"id": "devgw-1",
			"types": [
				2,
				3,
				4,
				5,
				6,
				7,
				8,
				9
			],
			"heartbeat_at": 1729170026,
			"host": ""
		}
	]
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.id | devgw-1 | string | 设备ID |
| data.types | - | array | 代理类型 1MCU,2SIP,3H323,4GB28181,5RTSP拉流,6RTMP拉流,7文件播放,8腾讯会议,9AI |
| data.heartbeat_at | 1729170026 | number | - |
| data.host | - | string | api接口，用于rtc调设备网关 |

***

## 设备详情

**接口URL**

> /server/v1/agent/detail

**请求Body参数**

```javascript
{
	"id": "sw8kjx"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| id | sw8kjx | string | 是 | 设备ID |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"id": "sw8kjx",
		"name": "华为sipip直连测试",
		"type": 2,
		"status": 0,
		"heartbeat_at": 0,
		"contact": "192.168.0.109:5060",
		"conn_params": null,
		"gw": "devgw-1",
		"remark": "备注"
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | object | 返回数据 |
| data.id | sw8kjx | string | 设备ID |
| data.name | 华为sipip直连测试 | string | - |
| data.type | 2 | number | 代理类型 1MCU,2SIP,3H323,4GB28181,5RTSP拉流,6RTMP拉流,7文件播放,8腾讯会议,9AI |
| data.status | 0 | number | 设备状态，0 未知<br/>1 在线<br/>2 离线 |
| data.heartbeat_at | 0 | number | - |
| data.contact | 192.168.0.109:5060 | string | 设备标识，注册模式是用户名，直连模式是uri |
| data.conn_params | - | null | - |
| data.gw | devgw-1 | string | 设备网关唯一id |
| data.remark | 备注 | string | 备注 |

***

## 删除设备

**接口URL**

> /server/v1/agent/delete

**请求Body参数**

```javascript
{
	"id": "s18v0x"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| id | s18v0x | string | 是 | 设备ID |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "s18v0x"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | s18v0x | string | 返回数据 |

***

## 邀请设备入会

**接口URL**

> /server/v1/agent/invite

**请求Body参数**

```javascript
{
	"agents": [
		{
			"type": 9,
			"contact": "huaweisip",
			"nickname": ""
		}
	],
	"no": "529660637"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| agents | - | array | 是 | 设备列表 |
| agents.type | 9 | number | 是 | 设备类型(目前仅支持2 3 4 5) 2SIP,3H323,4GB28181,5RTSP拉流,6RTMP拉流,7文件播放 |
| agents.contact | huaweisip | string | 是 | 设备标识 |
| agents.nickname |  | string | 否 | 会中名称 |
| no | 529660637 | string | 是 | 目标房间号(如业务层封装了加入频道加入了特有业务，用业务层定义的有意义的号码如会议号，此时业务层需响应agent_join回调(no会在此回调中原封不动传回)并返回加入频道的sid；如没有封装加入频道特有业务，也可直接用频道名 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |

***

## 邀请设备列表

单人多次进入有多条记录

**接口URL**

> /server/v1/agent/list-invite

**请求Body参数**

```javascript
{
	"type": [2,3],
	"keyword": "huawei",
	"name": "",
	"contact": "",
	"page": 1,
	"per-page": 20
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| type | - | array | 是 | 设备类型(目前仅支持2 3 5) 2SIP,3H323,4GB28181,5RTSP拉流,6RTMP拉流,7文件播放,8腾讯会议,9AI |
| keyword | huawei | string | 否 | 搜索关键词 |
| name | - | string | 否 | 会中户名 |
| contact | - | string | 否 | 设备标识 |
| page | 1 | number | 是 | 分页页码，数字类型 |
| per-page | 20 | number | 是 | 分页页码，数字类型 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"id": "sz8nk8",
			"name": "华为sip终端",
			"type": 2,
			"status": 1,
			"heartbeat_at": 1729170027,
			"contact": "huaweisip",
			"conn_params": {
				"auth_pwd": "1234"
			},
			"gw": "devgw-1",
			"remark": ""
		}
	],
	"_meta": {
		"totalCount": 1,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.id | s18v0x | string | 设备ID |
| data.name | 华为sip注册测试2 | string | - |
| data.type | 2 | number | 代理类型 1MCU,2SIP,3H323,4GB28181,5RTSP拉流,6RTMP拉流,7文件播放,8腾讯会议,9AI |
| data.status | 0 | number | 设备状态，0 未知<br/>1 在线<br/>2 离线 |
| data.heartbeat_at | 0 | number | - |
| data.contact | huaweisip2 | string | 设备标识，注册模式是用户名，直连模式是uri |
| data.conn_params | - | object | - |
| data.conn_params.auth_pwd | hw | string | 认证密码 |
| data.gw | devgw-1 | string | 设备网关唯一id |
| data.remark | 备注 | string | 备注 |
| _meta | - | object | 页码信息 |
| _meta.totalCount | 2 | number | - |
| _meta.pageCount | 1 | number | - |
| _meta.currentPage | 1 | number | - |
| _meta.perPage | 10 | number | - |

* 失败(200)

```javascript
{
	"code": 1003,
	"msg": "错误信息"
}
```

***

## 开关设备视频

开关设备视频，应用层后端检测到是操作设备时进行调用，如会中主持人开关设备的音视频,如何判定是否设备：根据uid是否以_agent_开头

**接口URL**

> /server/v1/agent/set-camera-enabled

**请求Body参数**

```javascript
{
	"uid": "_agent_sp81d8",
	"channel": "snj27l",
	"enabled": false,
	"op_uid": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| uid | _agent_sp81d8 | string | 否 | 设备会中用户ID，不传代表对全频道设备操作 |
| channel | sny0r1 | string | 是 | 频道名 |
| enabled | false | boolean | 否 | 是否打开 |
| op_uid | - | string | 否 | 操作者(主持人)uid |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |

* 失败(404)

```javascript
{
	"code": 10000,
	"msg": "没有找到RTSP拉流网关"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 10000 | number | - |
| msg | 没有找到RTSP拉流网关 | string | 返回文字描述 |

***

## 开关设备音频

开关设备音频，应用层后端检测到是操作设备时进行调用，如会中主持人开关设备的音视频,如何判定是否设备：根据uid是否以_agent_开头

**接口URL**

> /server/v1/agent/set-mic-enabled

**请求Body参数**

```javascript
{
	"uid": "_agent_sp81d8",
	"channel": "sny0r1",
	"enabled": false,
	"op_uid": ""
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| uid | _agent_sp81d8 | string | 否 | 设备会中用户ID，不传代表对全频道设备操作 |
| channel | sny0r1 | string | 是 | 频道名 |
| enabled | false | boolean | 否 | 是否启用 |
| op_uid | - | string | 否 | 操作者(主持人)uid |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |

* 失败(404)

```javascript
{
	"code": 10000,
	"msg": "没有找到RTSP拉流网关"
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 10000 | number | - |
| msg | 没有找到RTSP拉流网关 | string | 返回文字描述 |

***

# 用户相关

在评标项类型目中约定的用户角色如下

- 0: 未知
- 1: 澄清人
- 2: 评标专家
- 3: 监管人员
- 4: 见证人员

## 用户信息同步

**接口URL**

> /stm/srvapi/v1/member/sync

**请求Body参数**

```javascript
[
	{
		"account": "13000000058",
		"nickname": "test",
		"password_hash": "b81e354e53367e8fd1b0fa4...",
		"role": 1
	}
]
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| 0 | - | object | 是 | 一次性不要超过1000 |
| 0.account | 13000000058 | string | 是 | 唯一标识 (如果已经导入 则修改下面参数) |
| 0.nickname | test | string | 是 | 昵称 (不超过50字符) |
| 0.password_hash | b81e354e53367e8fd1b0fa4... | string | 否 | sha256(密码) |
| 0.role | 1 | number | 否 | 角色 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": {
		"success": {"13000000058": "sq7z3d"},
		"fail": {"uid_2": "错误描述"}
	}
}
```

***

## 移除用户

**接口URL**

> /stm/srvapi/v1/member/remove

**请求Body参数**

```javascript
{
	"uids": ["uid_1"],
	"accounts": []
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| uids | - | array | 否 | 用户ID列表 |
| accounts | - | array | 否 | 用户帐号列表 |

**响应示例**

* 成功(200)

```javascript
{"code":0}
```

***

## 根据uids取用户信息

**接口URL**

> /stm/srvapi/v1/member/info

**请求Body参数**

```javascript
{
	"uids": [
		"sq7z3d"
	],
	"accounts": [
		"13000000058"
	]
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| uids | - | array | 否 | 用户ID列表 |
| accounts | - | array | 否 | 用户帐号列表 |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": [
		{
			"user_id": "sq7z3d",
			"mobile": "13000000058",
			"nickname": "13000000058",
			"avatar": "",
			"created_at": 1737339891
		}
	]
}
```

| 参数名 | 示例值 | 参数类型 | 参数描述 |
| --- | --- | --- | --- |
| code | 0 | number | - |
| data | - | array | 返回数据 |
| data.user_id | sq7z3d | string | 用户ID |
| data.mobile | 13000000058 | string | 手机号码(帐号) |
| data.nickname | 13000000058 | string | 会中昵称 |
| data.avatar | - | string | 头像 |
| data.created_at | 1737339891 | number | 创建 |

***

## 获取用户授权

**接口URL**

> /stm/srvapi/v1/member/grant

**请求Body参数**

```javascript
{
	"uid": "uid_1"
}
```

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| uid | uid_1 | string | 是 | 外部用户ID, 例如: 登录帐号 (如果不存在会授权失败) |

**响应示例**

* 成功(200)

```javascript
{
	"code": 0,
	"data": "eyJhbGciOiJIUzI......"
}
```

***

## 浏览器直接入会说明

**完全体格式：**

`https://IP或域名/meeting/stm/ui/outer?token=xxxxx&room_no=nnnnn&nickname=mmmmm`


**示例值:**

```
https://192.168.16.10:8012/meeting/stm/ui/outer?
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoic3F4NjJxIiwiYWNj
b3VudCI6IjEzMDAwMDAwNDk5IiwibW9iaWxlIjoiMTMwMDAwMDA0OTkiLCJuaWNrbmFtZSI6IjE
zMDAwMDAwNDk5IiwiYXZhdGFyIjoiIiwib3V0c2lkZSI6ZmFsc2UsImlzcyI6InNlYXN0YXJ0Ii
wiZXhwIjoxNzczOTAyNzUzLCJuYmYiOjE3NzMyOTY5NTMsImlhdCI6MTc3MzI5Nzk1M30.esAw4
1_18_ujq1JPJaiHVRdZkkDrxtqTVhB7A1Ar50Y&room_no=258609195&&nickname=MyName
```


**参数解释：**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | --- | --- | --- |
| token | eyJhbGciOiJIUzI1N... | string | 是 | JWT安全凭证 |
| room_no | 776868796 | string | 否 | 房间号 |
| nickname | MyName | string | 否 | 会中名称 |

> 注：`token`通过`获取用户授权`接口取得。
