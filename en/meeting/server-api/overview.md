---
title: "Overview"
description: "Basics of the SMeeting Server API: request method and format, base URL, request headers, the HMAC-SHA256 signing algorithm, and the response format. Read this before calling any SMeeting server endpoint."
---

The server API is called by your backend.

### Basic usage

Use the server endpoints that fit your business needs to control your meetings.


---

### Calling conventions

1. **Request method**: POST

2. **Request format**: `application/json`, encoded in UTF-8

3. **Base URL**: `https://{server-domain-or-IP}/meeting/{endpoint-path}`

4. **Request headers**

| Key | Description | Notes |
| --- | --- | --- |
| appid | App ID | Required. `app_id` or `app-id` is also accepted, for languages or gateways that don't support underscores |
| nonce | Unique request ID, prevents duplicate submission | Required, a random 16-character string |
| timestamp | Unix timestamp in seconds | Required, accurate to the second, within ±5 minutes |
| signature | Signature value | Required, computed with HMAC-SHA256 as described below |

5. **Signing algorithm**

- **Step 1**: Build the string to sign by joining the app ID, `nonce`, `timestamp`, and the JSON string of the request body with `&`

```javascript
// Assume appid=1 nonce=2 timestamp=3 and the request body is {}
appid=1&nonce=2&timestamp=3&{}
```

<Warning>
**The field names in the string to sign must match the request header names you actually send.** You can use any of the three header names, but whichever you pick,
the string to sign must start with that name—sending an `app_id` header while signing `appid=...` fails authentication.

```text
With the appid  header → appid=1&nonce=2&timestamp=3&{}
With the app_id header → app_id=1&nonce=2&timestamp=3&{}
```

Also, sign the request body as the **raw string**. It must be byte-for-byte identical to what you send (including whitespace and field order);
don't serialize it again.
</Warning>

- **Step 2**: Compute HMAC-SHA256 over the string. The key is the `appkey` secret key.

```javascript
HMACSHA256(key, stringToSign)
```

- **Step 3**: Convert the binary result to lowercase hexadecimal to get the `signature`

6. **Response format**: JSON

```json
// On success, `data` contains the data
{
	"code": 0,
	"data": 123
}

// On error, `msg` is the error description ("认证失败" means "Authentication failed")
{
	"code": 10041,
	"msg": "认证失败"
}

// For list data, `_meta` contains the pagination info
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
