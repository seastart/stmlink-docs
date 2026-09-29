---
title: "Overview"
description: "Basics of the SRTC Server API: channel lifecycle and naming rules, base URL, request headers, the HMAC-SHA256 signing algorithm, uid and sid, and the response format. Read this before calling any SRTC server endpoint."
---

The server API is called by your backend (see the reference backend implementation).

### Basic concepts
**Channel**: A channel is an audio and video space (think of it as a meeting). Users in the same channel can receive each other's real-time audio and video.

#### Joining a channel
1. Your client calls your backend's endpoint for joining a channel
2. Your backend calls `channel/grant` of the `server API` to get a token and returns it to your client
3. Your client passes the `token` to the RTC SDK to join the channel

#### Opening and destroying a channel
+ A channel can be opened manually (for example, when you need to set some channel properties in advance)
+ If the channel is not open when the first user joins, it opens automatically
+ A channel is destroyed automatically if no one joins within 2 hours after it opens, or 2 hours after the last user leaves

#### Channel name rules
A string of up to 64 bytes. The supported character set is:

+ The 26 lowercase letters a-z.
+ The 26 uppercase letters A-Z.
+ The 10 digits 0-9.
+ "-", "_".

### Conventions
+ This protocol uses HTTP + JSON for transport (`application/json`)
+ All endpoints of the protocol support `POST` only
+ Strings are encoded in UTF-8

### Base URL

```text
https://<your-domain>/server/v1/...
```

<Note>
In a standard deployment, SRTC is served at the domain root. The `/meeting/` prefix on the same domain goes to the SMeeting service,
and the two sets of endpoints are not interchangeable (see [Choosing SRTC or SMeeting](/en/choose)). For deployments on a dedicated domain, follow the access information we provide.
</Note>

### Prerequisites
You need an `app_id` and an `app_key` before making calls

### Request headers
| Header | Description | Notes |
| --- | --- | --- |
| app_id | App ID | Required. `app-id` or `appid` is also accepted, for languages or gateways that don't support underscores |
| nonce | Unique request ID, prevents duplicate submission | Required, a random 16-character string |
| timestamp | Unix timestamp in seconds | Required, the client's local timestamp, accurate to the second.<br/>The client's local time must be within 5 minutes of the server's time; otherwise the server rejects the request. |
| signature | Signature value | Required. Computed with HMAC-SHA256, using the app_key issued by the server as the key, over the request data other than signature. |


#### Signing algorithm
Step 1: Build the string to sign by joining `app_id`, `nonce`, `timestamp`, and the JSON string of the request body with &

```typescript
// Assume app_id=1 nonce=2 timestamp=3 and the request body is {}
app_id=1&nonce=2&timestamp=3&{}
```

Step 2: Compute HMAC-SHA256 over the string. The key is the `app_key` secret key.

```typescript
HMACSHA256(key, stringToSign)
```

Step 3: Convert the binary result to lowercase hexadecimal to get the `signature`

Three details that are easy to get wrong:

+ The field names in the string to sign must match the **request header names you actually use**—if you use `app-id`, write `app-id=`, not `app_id=`
+ Sign the request body as the **raw string**. It must be byte-for-byte identical to what you send (including whitespace and field order); don't serialize it again
+ `app_key` is only used to compute the signature locally on your server. It **must never appear in a request or be sent to a client**

### uid and sid
+ `uid` is the user ID from your own system. You assign it; the RTC side does not generate it
+ `sid` is the ID of this session. The RTC side generates it when issuing the grant, and the same `uid` gets a different `sid` each time it joins

### Callbacks
Besides the endpoints you call, the RTC side also calls back your backend when the state of a channel, user, or recording changes.
See the [Callback events guide](/en/rtc/server-api/guides/callbacks).



### Response format
Both success and failure return HTTP 200. The business result is determined by `code`.

On success, `code` is 0 and `data` contains the data

```json
{
    "code": 0,
    "data": 123
}
```

On error, `code` is the error code and `msg` is the error description

```json
{
    "code": 1003,
    "msg": "请求头中的signature无效"
}
```

The `msg` above means "Invalid signature in request headers". **Check `code`**; don't match on the `msg` text. For all values, see [Error codes](/en/rtc/server-api/error-codes).




