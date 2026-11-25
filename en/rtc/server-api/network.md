---
title: "Network ID"
description: "Queries the access routes (network IDs) configured by the deployer, so end users can pick one on their device and pass it as net to the grant APIs"
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the rtc-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## List of available network IDs

`POST /server/v1/network/list`

Authentication: required (see [Overview](/en/rtc/server-api/overview))

Queries the network IDs available to this app. No request parameters.

A network ID represents a different access route to the same service (such as "intranet", "internet" or "private line"), configured by the deployer in the admin console.
When devices sit on different networks and need different routes, show the result of this API to end users to choose from,
then pass the selected net as-is to the net parameter of APIs such as "Get a channel join token" and "Get an IM token";
when net is not passed, the one with is_default set to true is used. The default network ID is listed first.

**Request parameters**

None

**Response parameters**

<ResponseField name="net" type="string">
  Network ID, i.e. the plane name in "Network ID configuration" of the admin console; pass it as-is as net when the client gets a token or joins
</ResponseField>

<ResponseField name="is_default" type="boolean">
  Whether this is the app's default network ID (used when net is not passed)
</ResponseField>


Response example:

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

