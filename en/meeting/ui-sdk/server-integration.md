---
title: "Server-side low-code integration"
description: "Add meetings to an existing business workflow without integrating any SDK or building a meeting UI: your backend calls three endpoints to create a meeting, get a login-free token, and open the meeting page. Read this when you only need a meeting entry point, not a meeting product."
---

If what you need is "attach meeting capabilities to an existing business workflow"—a round of tendering and bidding, a review, a dispatched work order—rather than building a meeting product, you don't need to integrate the SMeeting SDK or write a meeting UI.

The meeting client, user system, and login state are already deployed by us. Your backend does only three things:

| Step | Endpoint | Service |
| --- | --- | --- |
| 1. Create the meeting and attach your business document number | `POST /server/v1/meet/create` | Meeting service |
| 2. Issue a login-free token for a user | `POST /stm/srvapi/v1/member/grant` | User system |
| 3. Open the meeting page | `GET /stm/ui/outer?...` | Meeting client |

Do step 1 when the business activity is created, and steps 2 and 3 when the user clicks **Enter meeting**.

**You don't need to register users in advance.** When you get the token, pass the `user_id` together with a nickname: if the user doesn't exist, it is created on the spot; if it already exists, its profile is updated along the way. You only need to [batch sync users](#batch-sync-users) additionally when you want to provide a contact list in the meeting client.

<Note>
How this path differs from [low-code integration with UI](/en/meeting/ui-sdk/web): there, you take the frontend source code, modify the UI, and deploy it yourself; here, even the UI is the one we have deployed, and you only build a URL on the server.
</Note>

## Two base URLs

The integration uses two prefixes on the same domain:

```text
https://<your-domain>/meeting/server/v1/...        Meeting service (creating meetings, meeting controls, recording)
https://<your-domain>/meeting/stm/srvapi/v1/...    User system (sync, grants)
```

<Note>
In a standard deployment, the meeting service sits under the `/meeting/` gateway prefix. **Don't leave this prefix out**—the root path `/server/v1/...` on the same domain goes to the SRTC audio and video service, and requests sent there won't find the meeting endpoints.

The steps below only show endpoint paths (such as `POST /server/v1/meet/create`); prepend the base URL `https://<your-domain>/meeting` to every actual request. If your environment is deployed on a dedicated domain, the prefix may differ; follow the integration information we provide.
</Note>

Both use **the same `app_id` / `app_key`**, and authentication is exactly the same—four request headers, `app_id` / `nonce` / `timestamp` / `signature`, with an HMAC-SHA256 signature. See [Server API overview](/en/meeting/server-api/overview) for the algorithm. Write the signing code once and it works for both prefixes.

<Warning>
`app_key` must stay on your backend. Of the three steps above, only the URL in step 3 reaches the browser, and it carries a one-time user token, not the secret key.
</Warning>

## How users are identified

The entire flow identifies a user by a single value: **the unique user identifier in your system**. A user ID, employee number, national ID number, or mobile number all work, as long as it is unique on your side and never changes.

In every endpoint it is called **`user_id`**—getting a token, syncing, and the invitee whitelist all take the same value.

<Warning>
**Once this value has been used, don't change it.** It is the only basis for identifying a user; changing it is the same as switching to a different person, and the earlier attendance records don't carry over.
</Warning>

<Note>
We no longer generate a separate set of user IDs, so there is no mapping for you to store.
</Note>

## Step 1: Create a meeting

```text
POST /server/v1/meet/create
```

See [Meeting management](/en/meeting/server-api/meet#create-a-meeting) for the full parameters. Only the few that matter for low-code integration are covered here:

```json
{
  "title": "Project XX bid opening meeting",
  "meeting_type": 2,
  "plan_time": 1718250917,
  "plan_dur": 120,
  "attend_type": 3,
  "creator": "01hq8x7k2m",
  "co_hosts": ["01hq8x7k3n"],
  "conferee_details": [
    { "user_id": "310101199001011234", "real_name": "Alice" }
  ],
  "extend_info": { "bid_no": "ZB-2026-0731", "biz_type": "kaibiao" }
}
```

+ **`extend_info`** is where you attach the business document. It is a free-form object that we only store and return. Put the tendering number in it, and when you receive callbacks later you can look up your own business record
+ **`conferee_details`** specifies the invitee whitelist. Combined with `attend_type: 3` (invitees only), it keeps unrelated people out. The people listed don't need to exist in advance: `user_id` is the identity, so even with only a `user_id` and no matching user in the system, that person can still enter the meeting. But then this whitelist entry has no name, and the invitee list can't show it until the person enters the meeting. **So include `real_name` or `nickname` in each entry whenever possible**—if you do, the user is created along the way.
+ **The host** is determined by `creator`, and **co-hosts** go in `co_hosts` (an array). Both also take the `user_id`, the same value as in the whitelist; you don't need to sync the user first and get a different ID back. If `creator` is omitted, the server marks no one as host, and no one in the meeting gets meeting control permissions—remember to include it when creating the meeting
+ **You usually don't need to pass `role` in `conferee_details`**: it has no effect with built-in roles, and host / co-host are specified with the two fields above. Only projects that have enabled [custom roles](/en/meeting/key-concepts#custom-roles) (for example, tendering and bidding that distinguishes experts and witnesses) rely on it to assign each person an identity
+ **`meeting_type`**: `1` instant meeting, `2` scheduled meeting. A scheduled meeting must include `plan_time` and `plan_dur`
+ To record automatically, add `auto_record: true`; you don't need to manage recording start and stop in your business logic. See the [Cloud recording and live streaming guide](/en/meeting/server-api/guides/recording)

The returned **`room_no`** is the room number used in step 3, and `meeting_id` is the input for all subsequent meeting endpoints:

```json
{ "meeting_id": "sny038", "room_no": "803707296" }
```

<Warning>
**Don't use password meetings with `attend_type` set to `2` or `4`.** The launch URL in step 3 doesn't support passing a password, so users would have to type it manually again after landing on the meeting page, which defeats the purpose of low-code integration. Use `1` (unrestricted) or `3` (invitees only).
</Warning>

## Step 2: Get a login-free token

When a user clicks **Enter meeting** in your system, your backend calls this in real time:

```text
POST /stm/srvapi/v1/member/grant
```

```json
{
  "user_id": "310101199001011234",
  "nickname": "Alice",
  "avatar": "https://example.com/avatar/zhangsan.png"
}
```

| Field | Required | Description |
| --- | --- | --- |
| `user_id` | Yes | Unique user identifier; see [How users are identified](#how-users-are-identified) |
| `nickname` | No | Name displayed in the meeting |
| `real_name` | No | Real name; defaults to `nickname` if empty |
| `avatar` | No | Avatar URL; empty means unchanged and doesn't clear the existing avatar |
| `mobile` | No | Mobile number, for display only and not used to identify the user; empty means unchanged |

**If the user doesn't exist, these fields are used to create it on the spot; if it already exists, it is updated along the way.** So you don't need to keep a ledger of "who has been synced"—just include the latest nickname and avatar every time you get a token, and a name change takes effect the next time the user enters a meeting.

<Note>
Passing only `user_id` for a user who has never appeared returns an error—without a nickname, the created user would have no name in the meeting. Include `nickname` and it works.
</Note>

The return value is the token string itself:

```json
{ "code": 0, "data": "eyJhbGciOiJIUzI1NiIs..." }
```

It is valid for 7 days. **We recommend issuing a new one before every launch** rather than caching and reusing it—it is equivalent to this user's login state.

## Step 3: Open the meeting page

Build a URL from the token and room number, and have the user's browser open it:

```text
https://<your-domain>/meeting/stm/ui/outer?token=<token from step 2>&room_no=<room_no from step 1>&nickname=<in-meeting display name>
```

| Parameter | Required | Description |
| --- | --- | --- |
| `token` | Yes | Token issued in step 2 |
| `room_no` | No | If omitted, the user lands on the meeting list home page and chooses a meeting |
| `nickname` | No | Overrides the nickname in the user profile, for temporary identities such as "Alice (client representative)" |

If `nickname` contains Chinese or special characters, remember to URL-encode it.

When entering the meeting, **the mic and camera are off by default**; users turn them on themselves during the meeting.

## Complete sequence

```text
When the business activity is created
  └─ POST /server/v1/meet/create        attach the document number in extend_info → store room_no

User clicks "Enter meeting"
  ├─ POST /stm/srvapi/v1/member/grant   user_id + nickname + avatar → token (created on the spot if missing)
  └─ 302 to /stm/ui/outer?token=&room_no=&nickname=

During the meeting (optional)
  ├─ Subscribe to callback events       entering/exiting, recording done; see the callback events guide
  └─ POST /stm/srvapi/v1/member/info    check who is online

After the activity ends (optional)
  └─ POST /server/v1/mcu/vods-url       get playback after the mcu_record_done callback;
                                        one recording may have multiple segments, all returned here
```

For how to receive callbacks and verify signatures, see the [Callback events guide](/en/meeting/server-api/guides/callbacks). `meeting_id` is included in each event; use it to look up the document number you stored in `extend_info`.

## Batch sync users

The three steps above don't need it. **You only need to push users in advance when you want users to browse a contact list in the meeting client and pick people from the member list to invite into the meeting.**

```text
POST /stm/srvapi/v1/member/sync
```

The request body is an **array** of no more than 1,000 entries per call:

```json
[
  {
    "user_id": "310101199001011234",
    "nickname": "Alice",
    "real_name": "Alice",
    "avatar": "https://example.com/avatar/zhangsan.png",
    "department": "Tendering Dept. 1"
  }
]
```

| Field | Required | Description |
| --- | --- | --- |
| `user_id` | Yes | Unique user identifier; see [How users are identified](#how-users-are-identified) |
| `nickname` | Yes | Name displayed in the meeting |
| `real_name` | No | Real name; defaults to `nickname` if empty |
| `avatar` | No | Avatar URL; empty means unchanged and doesn't clear the existing avatar |
| `department` | No | Organization name |
| `mobile` | No | Mobile number, for display only and not used to identify the user; empty means unchanged |
| `password_hash` / `salt` | No | Pass these only if the user also needs to log in to the meeting page with an account and password |

The response splits results by `user_id` into success and failure maps:

```json
{
  "success": { "310101199001011234": "310101199001011234" },
  "fail": { "310101199001011299": "昵称不能为空" }
}
```

In this example, `"昵称不能为空"` means "Nickname cannot be empty".

Both the keys and values of `success` are the `user_id` values you passed, **so there is nothing to store**—use the `user_id` directly for `creator` and `co_hosts` when creating a meeting. The values of `fail` are the reasons each entry failed.

Syncing the same `user_id` again updates the user rather than creating a new one, so both full and incremental pushes work. Only one sync task can run at a time; concurrent calls receive "频率过快 请稍候" ("Too frequent, please wait").

### Limits of the organization structure

`department` is a **flat string**, not a hierarchy. A multi-level department tree can currently only be imported with Excel in the admin console (up to four levels, 500 rows per import), and **there is no corresponding API**.

So if you just want invitees to see "Alice (Tendering Dept. 1)", `department` is enough; if you want to sync your whole organization tree so users can drill down level by level in the contact list, this path can't do it today—raise it as a separate request.

## Two other optional endpoints

**Query users and online status** — `POST /stm/srvapi/v1/member/info`

```json
{ "user_ids": ["310101199001011234"] }
```

The response includes `is_online`, so you can show "Alice online" in your UI.

**Clean up departed users** — `POST /stm/srvapi/v1/member/remove`

Same input as above. After removal, the user can no longer get a token to enter meetings.

## When to switch to the full SDK

The cost of this path is that **the UI isn't yours**. If any of the following applies, consider integrating the SMeeting SDK:

+ The meeting UI must use your own branding, layout, or interactions
+ The meeting must be embedded inside your app rather than opening a separate web page
+ You need business logic tied into the meeting, such as automatically lifting mute all when the bid opening stage starts

See the "iOS SDK (Objective-C)", "Android SDK", and other groups in the left sidebar for how to integrate each platform. Both paths use the same set of server endpoints, so you can get the business flow working with low-code integration first and switch to the SDK for the UI later—the integration work you've already done isn't wasted.
