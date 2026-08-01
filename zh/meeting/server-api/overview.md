---
title: "概览"
description: "SMeeting 会议服务端 产品概览"
---

服务端接口是供业务方后端调用的接口。

### 基本使用说明

根据实际业务需要使用合适的服务端接口对会议业务进行操控。


---

### 接口调用说明

1. **请求方法**：POST

2. **请求格式**：application/json 格式传递，内容使用UTF-8编码

3. **请求地址**：`https://{服务器域名或IP}/meeting/{接口路径及名称}`

4. **Header头参数**

| Key | 说明 | 备注 |
| --- | --- | --- |
| appid | 应用id | 必填 |
| nonce | 请求唯一ID,防重复提交 | 必填，16位随机字符串 |
| timestamp | unix时间戳s | 必填，精确到秒，误差±5分钟 |
| signature | 签名值 | 必填, 采用HMAC-SHA256算法，方法如下所示 |

5. **签名方法**

- **第一步**：拼接待签名字符串，将appid nonce timestamp以及请求body的json字符串用`&`拼接

```javascript
// 假定appid=1 nonce=2 timestamp=3 请求体为{}
appid=1&nonce=2&timestamp=3&{}
```

- **第二步**：使用HMAC-SHA256加密字符串。key是`appkey`秘钥。

```javascript
HMACSHA256(key, 待签名字符串)
```

- **第三步**：把二进制转化为小写的十六进制得到`signature`

6. **响应格式**：json格式

```json
// 正常时返回, `data`为数据
{
	"code": 0,
	"data": 123
}

// 有错误时返回, `msg`为错误描述
{
	"code": 10041,
	"msg": "认证失败"
}

// 返回列表数据, `_meta`为翻页信息
{
	"code": 0,
	"data": [
		{"id": 123}
	],
	"_meta": {
		"totalCount": 5,
		"pageCount": 1,
		"currentPage": 1,
		"perPage": 20
	}
}
```

---
