---
title: "Network ID"
description: "Queries the access routes (network IDs) configured by the deployer, so end users can pick one on their device and pass it to \"Get meeting authorization\""
---

{/* The API reference on this page is auto-generated from the backend source. Do not edit it by hand—changes are overwritten on the next sync.
    Edit the meeting-backend source instead; see the "对外接口文档（srvapi）" section of its README. */}

## List of available network IDs

`POST /server/v1/network/list`

Authentication: required (see [Overview](/en/meeting/server-api/overview))

Queries the network IDs available to this app. No request parameters.

A network ID represents a different access route to the same service (such as "intranet", "internet" or "private line"), configured by the deployer.
When devices sit on different networks and need different routes, show the result of this API to end users to choose from,
then pass the selected net as-is to the net parameter of "Get meeting authorization"; when net is not passed, the one with is_default set to true is used.
The default network ID is listed first.

**Request parameters**

None

**Response parameters**

<ResponseField name="net" type="string">
  Network ID; pass it as-is as net when getting meeting authorization
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

