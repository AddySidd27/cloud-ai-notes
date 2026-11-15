---
title: "Troubleshoot AVD Sign-in Failures: Conditional Access, MFA and Single Sign-on"
seoTitle: "Troubleshoot AVD Sign-in: Conditional Access, MFA, SSO"
layout: post.njk
permalink: "/azure-virtual-desktop/troubleshoot-sign-in-and-conditional-access/"
order: 131
part: 31
tags: [avd-series]
deck: "Find where a sign-in fails, read the Microsoft Entra sign-in log and the Conditional Access tab, and match the error code or repeated prompt to a fix."
description: "Ordered checks for Azure Virtual Desktop users who cannot sign in, loop through MFA or see no desktops: assignment, sign-in logs, AADSTS codes and policies."
---

A user cannot get in. Maybe they are asked to sign in again and again. Maybe multifactor authentication (MFA, a second proof of identity such as a phone prompt) loops. Maybe a message says "The sign-in method you're trying to use isn't allowed". Maybe they sign in fine and then see no desktops at all, or the list appears and the session fails to start.

These all happen at the sign-in stage, but the cause can sit in three different places: the user's access to the desktops, a Conditional Access policy, or a setting on the session host. This article gives an order of checks that finds the place first, then matches the error to a fix.

Two earlier articles explain the background and this article does not repeat it. [How sign-in works](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/) describes the three sign-ins and single sign-on. [Conditional Access and MFA for AVD](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/) shows how to build the policies. Some checks below use Log Analytics (Azure's log search tool), which returns nothing until diagnostics are on. The article [Turn on the logs and learn to read them](/azure-virtual-desktop/troubleshoot-avd-start-here/) shows how to turn them on and explains the query keywords. Before any check, look at the public Azure status page and Azure Service Health (in the Azure portal, search for **Service Health**), as the troubleshooting overview says.

## Key terms

| Term | Meaning |
|---|---|
| Microsoft Entra ID | Microsoft's cloud identity service, where user accounts and sign-in policies live. |
| Sign-in log | The Microsoft Entra record of each sign-in attempt, with the result and the policies that applied. |
| Conditional Access | Microsoft Entra rules that decide whether a sign-in is allowed, blocked or needs more proof, such as MFA. |
| Per-user MFA | The older way to require MFA, set on each user account. Conditional Access is the newer way. |
| AADSTS code | A Microsoft Entra error code that starts with the letters AADSTS followed by a number. |
| Feed | The list of desktops and apps that appears in the client after sign-in. |
| Application group | The Azure Virtual Desktop object that gives users access to a desktop or apps. |
| Single sign-on (SSO) | Signing in once to the cloud service and then entering the session host without a second password prompt. |
| Azure Virtual Desktop app | The Microsoft Entra application used when a user signs in to the service, loads the feed and connects through the gateway. |
| Windows Cloud Login app | The Microsoft Entra application used when a user signs in to the session host with SSO. |
| Sign-in frequency | A Conditional Access setting for how often users must sign in again. |
| Security Defaults | A tenant-wide set of basic security rules that Microsoft Entra can switch on. |
| AD FS | Active Directory Federation Services. A server that handles sign-in for federated domains. |
| Web Account Manager (WAM) cache | The Windows store of cached sign-in tokens on the client device. |
| Windows App | Microsoft's client app for connecting to Azure Virtual Desktop. |
| Session host | A virtual machine that runs users' desktops or apps. |
| Entra joined | A session host that is joined to Microsoft Entra ID instead of a domain. |
| Intune | Microsoft's device management service. It can mark a device as compliant or not compliant with your rules. |
| Compliant device | A device that meets the rules your organization set in Intune, such as having a screen lock. A Conditional Access policy can require it. |
| Named location | A saved set of IP addresses or countries that a Conditional Access policy can allow or block. |
| Admin center | The Microsoft Entra admin center is the web portal at `entra.microsoft.com` where you manage sign-ins and policies. |
| CorrelationId | An ID that every log row of one connection shares. |
| Kusto Query Language (KQL) | The language used to write Log Analytics queries. |

## What the user sees

| Symptom | Likely area |
|---|---|
| Signs in, but the list of desktops is empty | Assignment, or a Conditional Access policy that blocks an app |
| Asked to sign in or complete MFA again and again | Conditional Access settings on the two apps, per-user MFA, or the consent prompt |
| "The sign-in method you're trying to use isn't allowed" | Per-user MFA turned on beside Conditional Access, on an Entra joined host |
| An error that contains an AADSTS code | The sign-in log. See the table in check 6. |
| Feed loads but the session does not start | Conditional Access on the Windows Cloud Login app, or a role on the session host |
| Asked for full credentials after a screen lock | Session lock setting |

This grouping is a guide built from the pages listed at the end, not a documented list.

![Decision tree for Azure Virtual Desktop sign-in failures. The first question is whether the feed is empty after sign-in, which leads to the application group assignment; if not, it asks whether the Microsoft Entra sign-in log shows a failed entry and whether the user is prompted again and again. Then it asks which error code appears, grouped as AADSTS50058 or 50076, AADSTS530002 or 530032, and AADSTS65001 or registration required, and each yes leads to one fix. Anything left over leads to the session host roles and a support request.](/img/avd/troubleshoot-sign-in-and-conditional-access.svg)

*Source: Troubleshoot single sign-on and Conditional Access, Troubleshoot service connections, Log Analytics diagnostics, Enforce MFA with Conditional Access and Troubleshooting overview.*

## Check 1: where does it fail?

A user goes through three sign-ins: to the service (which loads the feed), through the gateway to start a connection, and to the session host. The documentation puts it this way: when a user can start the client and sign in but sees no icons, check permissions and Conditional Access. If the feed appears but the session fails to start, the problem is probably in the connection or on the session host. Ask the user two things: what did you see, and at which step?

## Check 2: is the user assigned to a desktop?

If the feed is empty, run this command in PowerShell (it needs the Az PowerShell module and a sign-in with `Connect-AzAccount`). It lists the Azure roles the user holds. Replace `<userupn>` with the user's sign-in name:

```powershell
Get-AzRoleAssignment -SignInName <userupn>
```

Look in the output for the role **Desktop Virtualization User** and a `Scope` that is an application group (the path contains `applicationGroups`). If the user is meant to get access through a group, check the group on the application group's **Assignments** page instead. If neither the user nor one of their groups is assigned, the user has no desktops and the feed is empty. To fix it, in the Azure portal open **Azure Virtual Desktop**, then **Application groups**, then the application group, select **Assignments**, then **+ Add**, and pick the user or a security group.

The documentation then lists these checks:

1. Confirm the user is assigned to an application group.
2. Confirm the user signs in with the right credentials.
3. If the web client is used, check for cached credential problems.
4. If the user is in a Microsoft Entra group, make sure it is a security group. Azure Virtual Desktop does not support Microsoft Entra distribution groups (mail lists).

The documentation also names two causes of a feed that disappears: a subscription moved from one Microsoft Entra tenant to another (reassign the users to their application groups), and a subscription created by a CSP provider and then transferred to the customer (re-register the Microsoft.DesktopVirtualization resource provider under Subscriptions, Resource providers).

## Check 3: did the user reach Azure Virtual Desktop at all?

Connections that never reach the service do not show up in diagnostics. Look the user up in the connection table. These are documentation samples; replace `userupn` with the user's sign-in name:

```kusto
WVDConnections
|where UserName == "userupn"
|take 100
|sort by TimeGenerated asc, CorrelationId
```

```kusto
WVDErrors
| where UserName == "userupn"
|take 100
```

The first query lists the user's connection rows, oldest first. The second lists the user's error rows. Both are explained line by line in the start article. Reading the result:

- **No rows at all.** The documentation says connections that do not reach the service are missing from the data. So the failure probably happened before Azure Virtual Desktop, in the client, the network or the Microsoft Entra sign-in. Go to check 5.
- **Rows in `WVDErrors`.** Note the `CodeSymbolic`, the `Message` and the `ServiceError` value. `false` means an admin can fix it. `true` means escalate to Microsoft with the CorrelationId.
- **Rows in `WVDConnections`.** `SessionHostJoinType` shows how the host is joined (`DomainJoined`, `HybridAzureADJoined` or `AzureADJoined`), and `AadTenantId` shows the user's tenant. Use them to pick the right checks below.

If the problem is the feed, this sample lists the top 10 feed errors that an admin can fix, by user count:

```kusto
WVDErrors
| where ServiceError == "false"
| where ActivityType == "Feed"
| summarize UserCount = dcount(UserName), SampleMessage = take_any(Message) by CodeSymbolic
| project SampleMessage, UserCount
| top 10 by UserCount desc
```

Line by line: line 2 keeps errors where `ServiceError` is `false`, the ones an admin can fix. Line 3 keeps errors from feed activities. Line 4 groups by `CodeSymbolic` and, for each group, counts the different users and keeps one example message (`take_any`). Line 5 keeps only the message and the user count. Line 6 puts the ten groups with the most users first. A healthy result is empty. A bad result is a message with a high `UserCount`, which means many users cannot load their feed for the same reason. Search the message text in the fix tables below.

## Check 4: the prerequisites

The sign-in troubleshooting page asks you to confirm three things before anything else:

- Single sign-on is enabled on the host pool.
- The Azure Virtual Desktop app and the Windows Cloud Login app exist in the tenant (the app IDs are in the table below).
- Per-user MFA is disabled for Azure Virtual Desktop users. Use Conditional Access policies instead.

Conditional Access needs Microsoft Entra ID P1 or P2 licensing. It cannot be used while Security Defaults are on.

These are the apps that matter, from the Conditional Access setup page:

| App | App ID | What it covers |
|---|---|---|
| Azure Virtual Desktop | `9cdead84-a844-4324-93f2-b2e6bb768d07` | Subscribing to the feed, signing in to the gateway, sending diagnostics from the user's device. Older tenants may show it as "Windows Virtual Desktop". |
| Windows Cloud Login | `270efc09-cd0d-444b-a71f-39af4910ec45` | Signing in to the session host when SSO is on. |
| Windows 365 | `0af06dc6-e4b5-4f28-818e-e78e62d137a5` | Windows App signs in to this app too, even if the user has no Cloud PC. No policy should block it. |
| Azure Virtual Desktop Azure Resource Manager Provider | `50e95039-b200-4007-bc97-8d5790743a63` | Used only to get the feed. Do not add it to a Conditional Access policy, and do not require MFA on it. |

When a user signs in through the web client, the sign-in log lists the client app ID `a85cf173-4192-42f8-81fa-777a763e6e2c` (Azure Virtual Desktop client). The documentation explains that this client app is linked to the server app where the policy was set.

## Check 5: read the Microsoft Entra sign-in log

This is the main tool for any sign-in problem. The documentation gives these steps:

1. In the Microsoft Entra admin center, go to Identity, then Monitoring & health, then Sign-in logs.
2. Filter by the affected user.
3. Find the entries for the **Azure Virtual Desktop** app and the **Windows Cloud Login** app around the time of the failure.
4. For each failed entry, note the **sign-in error code** (the AADSTS code). On the **Conditional Access** tab, see which policies were evaluated and which one blocked the sign-in. On the **Authentication Details** tab, see which method was used or required.

If the sign-in log shows no failed entry for these apps, the sign-in probably did not get that far. Check the client and the network. The [client article](/azure-virtual-desktop/choose-the-avd-client/) and the [connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) cover those.

**Optional: query the sign-in log in Log Analytics.** The sign-in log only reaches a workspace if you send it there. In the Microsoft Entra admin center, go to Entra ID, Monitoring & health, Diagnostic settings, add a diagnostic setting, select `SigninLogs`, choose Send to Log Analytics workspace and save. You need at least the Security Administrator role, and the data can take up to 15 minutes to appear. The query below is written for this article. It is not a documentation sample. It uses only columns on the `SigninLogs` table page:

```kusto
SigninLogs
| where TimeGenerated > ago(1d)
| where UserPrincipalName == "userupn"
| where AppId in ("9cdead84-a844-4324-93f2-b2e6bb768d07", "270efc09-cd0d-444b-a71f-39af4910ec45")
| project TimeGenerated, AppDisplayName, ResultType, ResultDescription, ConditionalAccessStatus, IPAddress, CorrelationId
| sort by TimeGenerated desc
```

Line by line: line 2 keeps the last day. Line 3 keeps this user (replace `userupn` as before). Line 4 keeps only sign-ins to the Azure Virtual Desktop app and the Windows Cloud Login app, using their app IDs from the table above. Line 5 keeps the columns that matter. Line 6 puts the newest first. Healthy: the rows have `ResultType` 0. Bad: a row with another `ResultType`, which is the error number without the `AADSTS` letters, such as 50076. Look it up in the table in check 6. If `ConditionalAccessStatus` is `failure` on that row, a policy blocked it, and the **Conditional Access** tab of the same entry in the sign-in log names the policy.

The table page says `ResultType` is the error code and 0 means success, and that `ConditionalAccessStatus` is `success`, `failure` or `notApplied`. Note that this CorrelationId belongs to the Microsoft Entra sign-in. It is not the same value as the CorrelationId in the Azure Virtual Desktop tables (they come from different services, and the pages do not say the two match).

## Check 6: match the error to a fix

| Error text or code | What it means | Fix |
|---|---|---|
| `AADSTS50058` SSO session not found or invalid | The client has no active Microsoft Entra session, or the session cannot be used for this request. | Sign out of Windows App and sign in again. If it continues, clear the Web Account Manager cache on the client device. |
| `AADSTS50076` MFA required | MFA is required by Conditional Access or per-user MFA, and was not satisfied. | Confirm the user has a registered MFA method. Check that the connection meets the Conditional Access conditions (named locations, compliant device). If per-user MFA is on, disable it and use Conditional Access. |
| `AADSTS530002` device not compliant | A policy requires a compliant device and the device used is not compliant. | On the sign-in log's Conditional Access tab, find the policy that reports Failure and its app. If the policy targets the Azure Virtual Desktop or Windows Cloud Login app, the rule applies to the client device: make it compliant in Intune, or exclude that device group. If it targets an app used inside the session, such as a Microsoft 365 app, the rule applies to the session host: enrol it in Intune, or exclude session hosts by device filter. |
| `AADSTS530032` blocked by tenant security policy | A tenant-level control blocked the sign-in. It can be Security Defaults, a Conditional Access policy that blocks access, or another tenant restriction. | In Identity, Overview, Properties, check whether Security Defaults are on. If you need Conditional Access, disable them, but only once Conditional Access policies that require MFA are ready to replace them, so the tenant is not left without that protection. Review the policies on the two apps for Grant set to Block access. The Conditional Access tab shows the policy that blocked it. |
| `AADSTS65001` consent required | The user or admin has not consented to the application. | Hide the consent prompt (steps under check 7), or grant admin consent for the Windows Cloud Login app. |
| "User strong authentication registration required" | The user is not registered for MFA. | Have the user register at `https://aka.ms/mfasetup`, or enrol them through a Conditional Access registration campaign. |
| A Conditional Access block when signing in to Windows App or connecting | A policy blocks access to an Entra resource. | If Windows App is used in a browser, the user needs access to both the Azure Virtual Desktop and Windows 365 apps. If SSO is on, the user needs access to the Windows Cloud Login app. |
| AD FS log shows `MSIS7102: Requested Authentication Method is not supported on the STS` | Windows App sends `prompt=login`. If the federated domain's `PromptLoginBehavior` is unset, Microsoft Entra ID can turn it into a password request that AD FS does not support. | For supported AD FS versions, set `PromptLoginBehavior = nativeSupport` on the affected federated domain. |

For `AADSTS530002`, the documentation adds that most deployments should not apply user-device compliance policies to session hosts at connection time, and should scope connection-time compliance to client devices.

## Check 7: repeated prompts

If the user is asked again and again, the documentation lists these causes:

| Cause | Fix |
|---|---|
| Sign-in frequency differs between the Azure Virtual Desktop app and the Windows Cloud Login app, so one expires before the other | Set the same value on both, or make the Windows Cloud Login policy equal to or longer than the other. |
| **Every time** is set as the sign-in frequency on the Azure Virtual Desktop app. It causes constant prompts on feed refresh and diagnostics upload | Use **Every time** only on the Windows Cloud Login app. |
| Per-user MFA is on beside Conditional Access. Users see "The sign-in method you're trying to use isn't allowed" or repeated prompts | In Identity, Users, All users, Per-user MFA, set each Azure Virtual Desktop user to Disabled. Enforce MFA with Conditional Access. |
| Only the Azure Virtual Desktop app has a policy. The user gets MFA at the service and again at the session host | Add a separate policy for the Windows Cloud Login app. |
| The consent prompt is not hidden. It looks like a sign-in prompt on the first connection to each session host | Hide the consent prompt. |
| The session lock shows the remote lock screen, so users enter full credentials after a lock or idle time | Set the session to disconnect on lock. The user can then reconnect with SSO. |

The Conditional Access setup page also says reauthentication happens when a new access token is needed, and that users must reauthenticate if a network drop forces the session to be set up again after the sign-in frequency has passed. That can mean more prompts on unstable networks. For slow or dropped sessions, see the [disconnects and slow sessions playbook](/azure-virtual-desktop/troubleshoot-disconnects-and-slow-sessions/).

### How to hide the consent prompt

By default, with single sign-on on, users see a dialog that asks them to allow the Remote Desktop connection when they connect to a new session host. Microsoft Entra remembers up to 15 hosts for 30 days before it asks again. To hide the dialog, you give Microsoft Entra a list of trusted session hosts:

1. In Microsoft Entra ID, create a dynamic device group that contains the session hosts. A dynamic group fills itself from a rule, and it needs a Microsoft Entra ID P1 license.
2. In the Azure portal, search for **Microsoft Entra ID**. Select **Devices**, then **Remote connection configuration**.
3. Select **Windows Cloud Login**, then the link under **Target device groups to enable SSO**.
4. Search for and select the group. You can add up to 10 groups.
5. Select **Save**.

## Check 8: the session host

If the feed loads and the Conditional Access checks pass, but the session still will not start, look at the host. For Entra joined session hosts in host pools that do not use a session host configuration, the documentation says to assign users the **Virtual Machine User Login** role, and admins who need local administrator rights the **Virtual Machine Administrator Login** role. You can assign them on the VMs, the resource group or the subscription. For host pools that use a session host configuration, the page says the extra role assignment is not required.

Two more points from the same page:

- If you use MFA with Entra joined hosts and do not want to limit sign-in to strong methods such as Windows Hello for Business, exclude the Azure Windows VM Sign-In app from the Conditional Access policy.
- If you do not use SSO, a Windows desktop client can connect to an Entra joined host only when the local PC is Entra joined, hybrid joined, or Entra registered (on Windows 11 or Windows 10 version 2004 or later) in the same tenant as the host. Otherwise, and for web, Android, macOS and iOS clients, add the custom RDP property `targetisaadjoined:i:1` to the host pool. These connections accept only a user name and password.

## If you are still stuck

1. Note the AADSTS code, the time (UTC), the user, the app and the CorrelationId from the sign-in log. Note the policy name from the Conditional Access tab.
2. If the failure is in `WVDErrors`, note the `ServiceError` value. `true` means escalate to Microsoft with the CorrelationId.
3. Check the Azure status page and Azure Service Health once more.
4. Open an Azure support request and choose Azure Virtual Desktop as the service. For third-party sign-in tools, the documentation says to check that the provider supports Azure Virtual Desktop and ask them about known issues.

Next: [Troubleshoot AVD Session Hosts That Do Not Register to the Host Pool](/azure-virtual-desktop/troubleshoot-host-pool-registration-failures/).

## Sources

[Troubleshoot single sign-on and Conditional Access](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-sso-conditional-access), [Troubleshoot service connections](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-service-connection) and [Enforce MFA with Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa).
