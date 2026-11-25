---
title: "Invite and remove"
description: "Bring users (App / Web) or devices such as meeting room endpoints and cameras into a meeting from your backend, force entry, remove them, and find out when an invitation fails: APIs, parameters, and limits for users and devices side by side"
---

There are two ways for the platform to bring someone into a meeting: **users** (people signed in to an App / Web client) are called with the meeting-layer
[Call users into the meeting](/en/meeting/server-api/meet-admin#call-users-into-the-meeting) (`call-users`), and
**devices** (SIP / H.323 endpoints, GB28181 cameras, RTSP, and so on) are invited with
[Invite devices to the channel](/en/rtc/server-api/agent#invite-devices-to-the-channel) (`agent/invite`), forwarded through SMeeting. Both are removed with the same API.

## Comparison

| | Users | Devices |
| --- | --- | --- |
| Invite API | `POST /server/v1/meet-admin/call-users` | `POST /server/v1/agent/invite` |
| Meeting identifier | Either `room_no` or `meeting_id` | `no` takes the meeting room number `room_no` (not `meeting_id`) |
| Does the other side confirm? | Yes: the callee's clients ring, and the callee enters after answering | No: the device gateway calls the endpoint or pulls the stream directly. Whether a SIP / H.323 endpoint auto-answers depends on the endpoint's own settings |
| Forced entry | Pass `force_join=true`: no incoming call UI, the callee enters directly; if already in another meeting, the callee leaves it first | Always forced: a device already in another meeting switches straight to this one, and the endpoint doesn't hang up |
| Restricted meetings it can enter | See "Which restricted meetings can be entered" below | See "Which restricted meetings can be entered" below |
| Remove | [Remove a member](/en/meeting/server-api/meet-admin#remove-a-member) (`kickout-user`), `target_id` is the user ID | The same API, `target_id` is the device's in-meeting ID (prefixed with `_agent_`) |
| How to detect failure | The `offline_user_ids` return value lists users who are offline; for no answer or declined, use "no `user_enter` callback within 60 seconds" | The [`device_invite_failed` callback](/en/meeting/server-api/guides/callbacks#device_invite_failed-—-device-invitation-failed) |

## Invite users: call-users

```json
{
  "room_no": "021890611",
  "conferee_details": [{ "user_id": "1001" }, { "user_id": "1002" }],
  "is_additional": true,
  "force_join": true
}
```

+ Callees are added to the invitee list (allowlist) and receive a call; `is_additional=true` appends them instead of replacing the existing invitees
+ A callee must be **signed in** on at least one App / Web client (IM online) to receive the call
+ The response returns `data.offline_user_ids`: callees whose IM was offline at the time of the call and who therefore cannot receive it. It's an empty array when everyone is online;
  if online status is temporarily unavailable, the callee is treated as online, so there are no false reports

```json
{ "code": 0, "data": { "offline_user_ids": ["1002"] } }
```

### Forced entry (force_join)

With `force_join=true`, our Apps (STM Link and others) handle the call like this:

+ No incoming call screen; they show a short notice and enter directly. The nickname and camera / microphone defaults follow the App's join settings
+ Already in another meeting (including the waiting room or while joining): leave the current meeting first, then enter this one. Leaving only removes the user; it doesn't end the meeting even for the host, and no confirmation dialog is shown
+ Already in this meeting: ignored
+ If entry fails (for example, the meeting has ended), the regular join-failure message is shown and there is no retry

Without it, or with `false`, the regular incoming call screen is shown (answer / decline, 60-second timeout).

## Invite devices: agent/invite

Device invitations are forwarded by SMeeting to SRTC as is. For how to fill in the parameters and sign the request, see [Device integration and IM](/en/meeting/server-api/guides/agent-and-im#what-to-use-as-the-target-when-a-device-enters-the-meeting);
for field descriptions, see SRTC's [Invite devices to the channel](/en/rtc/server-api/agent#invite-devices-to-the-channel).

```json
{
  "agents": [{ "type": 2, "contact": "192.168.0.18:5060" }],
  "no": "021890611"
}
```

+ Devices don't confirm. The device gateway calls the SIP / H.323 endpoint: if the endpoint is set to auto-answer it enters directly, otherwise someone has to answer on the endpoint. Stream-pulling devices such as GB28181 and RTSP pull the stream and enter directly
+ A device already in another meeting switches straight to this one; the call continues and the endpoint doesn't hang up
+ A successful response only means the invitation was handed to the device gateway, **not that the device has entered**. Watch the `user_enter` callback for success and the `device_invite_failed` callback for failure

## Which restricted meetings can be entered

An invitation lets the invitee past some of the meeting's entry restrictions, so they don't need the password and don't get stuck in the waiting room:

| Entry restriction | Device (platform invitation) | User, `force_join=true` | User, regular call |
| --- | --- | --- | --- |
| Meeting password | Bypassed | Bypassed | Bypassed |
| Invitee allowlist | Bypassed | Bypassed (added to the allowlist by the call) | Bypassed (added to the allowlist by the call) |
| Meeting lock | Bypassed | Bypassed | Blocked as usual |
| Waiting room | Bypassed (enters directly) | Bypassed (enters directly) | Goes to the waiting room as usual |
| No one may join before the host | Bypassed | Bypassed | Blocked as usual |

+ For users the bypass is **valid for 30 minutes**: the callee must enter within 30 minutes of the call, after which entry is handled as a regular join. If the same user is called again, the latest call applies
+ **A device dialing in by itself** (the endpoint dials the meeting number) is not a platform invitation and goes through the regular entry checks
+ Other rules, such as the meeting having ended or being blocked (removed with `join_disabled`), still apply

## Remove: kickout-user

Both users and devices are removed with [Remove a member](/en/meeting/server-api/meet-admin#remove-a-member):

```json
{
  "room_no": "021890611",
  "target_id": "_agent_co63jg6g54hu3b0xhtie",
  "join_disabled": true
}
```

+ `target_id`: the user ID for a user; for a device, its in-meeting user ID, which starts with `_agent_`. Get it from [List in-meeting members](/en/meeting/server-api/meet#list-in-meeting-members) or the `user_enter` callback
+ `join_disabled=true`: block the target from entering this meeting again; `remove_conferee=true`: also remove the target from the invitee list
+ If the target is no longer in the meeting, the call simply succeeds

## How to detect a failed invitation

### Users

| Case | How to tell |
| --- | --- |
| Offline, the call can't be received | `offline_user_ids` returned by `call-users` |
| Received but not answered or declined, or forced entry failed | **No `user_enter` callback for that user within 60 seconds** of the call |

### Devices

Subscribe to the [`device_invite_failed` callback](/en/meeting/server-api/guides/callbacks#device_invite_failed-—-device-invitation-failed): it's sent when the endpoint is busy, declines, doesn't answer, can't be reached, the stream can't be pulled, or entry is refused,
with the failure reason `reason` and the original description `msg`.

<Warning>
  This callback is sent only when all three are in place:

  + **A newer device gateway version**: older device gateways don't report invitation failures
  + **Enabled by the deployer**: `agent_invite_failed` must be appended to `rtc.callback_events` in the SMeeting server configuration (off by default)
  + **Your subscription**: include `device_invite_failed` in `events` when you [Configure event notifications](/en/meeting/server-api/meet#configure-event-notifications)

  It's sent only for devices invited by the platform; failures of devices dialing in by themselves are not sent.
</Warning>

## Limits

+ **An App that isn't online can't be brought in**: a user must be signed in on some client (IM online) to receive the call, and forced entry is no exception; offline users are listed in `offline_user_ids`
+ **When a mobile App is in the background**: if the system allows it, the App is brought to the foreground and enters; otherwise it can only post a local notification first, and enters if the user taps the notification or returns to the App within 60 seconds; after 60 seconds the call is discarded
+ **If you build your own UI with the SDK**: the "Forced entry" behavior above is how our Apps handle it; the SDK only passes the flag to you. Read `force_join` from the call event yourself
  and handle it the same way (no incoming call screen, leave the current meeting first, then enter); if you don't, a forced call behaves like a regular call in your App. Each SDK exposes the field from the following version:

| Platform | Version | Field |
| --- | --- | --- |
| Web | 0.2.0 and later | `content.force_join` of the `call_calling` event, see [Events](/en/meeting/web/events#out-of-meeting-message-events) |
| Android | 2.0.37 and later | `ImContent.CallingMsg.forceJoin`, see [Model types](/en/meeting/android/types#imcontent-callingmsg) |
| iOS (Objective-C) | 2.5.0 and later | `onCallReceived:nickname:roomNo:title:meetingId:forceJoin:`, see [MeetingKitIMDelegate](/en/meeting/ios/api-reference/MeetingKitIMDelegate#oncallreceivednicknameroomnotitlemeetingidforcejoin) |
| Swift | 1.13.0 and later | `ImCallContent.forceJoin`, see [Out-of-meeting messages](/en/meeting/swift/advanced/im#someone-is-calling-you) |
| HarmonyOS | 1.9.0 and later | `ImCallContent.forceJoin`, see [IM and calls](/zh/meeting/harmony/advanced/im#被呼叫入会) (Chinese) |
| Windows | Not supported yet | — |
