---
title: "Windows 365 Licensing for Enterprise and Flex"
layout: post.njk
permalink: /windows-365/licensing/
order: 214
part: 15
tags: w365-series
deck: "Work out which licenses each Windows 365 Enterprise and Flex user needs, how Flex licenses are counted, and what to check when a Cloud PC does not appear."
---

Windows 365 gives a user a Windows desktop that runs in the cloud, called a Cloud PC. Someone has to buy and check the licenses behind it. This article is for that person.

It covers two editions: Windows 365 Enterprise and Windows 365 Flex. By the end you can list what each user needs, explain how Flex licenses are counted, and check your own tenant.

The article does not quote prices. Prices change and depend on how you buy. Use the [Windows 365 pricing page](https://www.microsoft.com/windows-365/all-pricing) for those.

![Every Enterprise and Flex user needs Windows Enterprise, Microsoft Intune and Microsoft Entra ID P1 licenses. In Enterprise, the user also has a Windows 365 license and uses a Cloud PC. In Flex, licenses are pooled for the tenant and apply to Dedicated and Shared mode. Users must be in the Microsoft Entra security group named in the provisioning policy.](/img/windows-365/windows-365-licensing.svg)

*Source: [Requirements for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements), [Windows 365 Flex licensing](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-flex-license) and [What is Windows 365 Flex?](https://learn.microsoft.com/en-us/windows-365/enterprise/introduction-windows-365-flex).*

## Key terms

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop that Windows 365 gives to a user. |
| Windows 365 Enterprise | The edition for organizations that manage Cloud PCs with Microsoft Intune. Each user needs a Windows 365 license. |
| Windows 365 Flex | A version of Windows 365 where one license can serve more than one user. It has two modes: Dedicated and Shared. |
| Dedicated mode | A Flex mode. One license can provide up to three Cloud PCs, each assigned to one user. |
| Shared mode | A Flex mode. One license provides one Cloud PC that a group of users share, one user at a time. |
| Active session | A Cloud PC that a user is connected to at that moment. The source pages also call it a concurrent session. |
| Tenant | Your organization's own space in Microsoft's cloud, where users, groups and licenses live. |
| Microsoft 365 admin center | The portal where you buy licenses and see how many you have. |
| Microsoft Intune | The Microsoft service that manages devices. You manage Cloud PCs in the Microsoft Intune admin center. |
| Microsoft Entra ID P1 | A license for Microsoft Entra ID, the Microsoft identity service that holds your users and groups. |
| Windows Enterprise license | The license for Windows 11 Enterprise or Windows 10 Enterprise. One Microsoft page names it Windows E3. This article says Windows Enterprise. |
| Microsoft Entra security group | A named set of users. |
| Provisioning policy | The setting that says how Cloud PCs are created for the users in a group. See the [provisioning article](/windows-365/provision/). |
| Concurrency buffer | A feature that lets a Flex tenant go over its active-session maximum a limited number of times per day. |
| Prestart | Dedicated mode starts a user's Cloud PC shortly before the time they usually connect, so it is ready. |
| Hybrid identity | A user identity that works both on-premises and in the cloud. |

## What each user needs

What a user needs depends on the edition.

| Edition | What each user needs |
|---|---|
| Enterprise | Licenses for Windows Enterprise, Microsoft Intune, Microsoft Entra ID P1 and Windows 365. |
| Flex | Licenses for Windows Enterprise, Microsoft Intune and Microsoft Entra ID P1. The user must also be in the Microsoft Entra security group named in the provisioning policy. |

Windows 365 Business, Government and Reserve are not covered here.

Two more rules apply to both editions:

- You must have an Intune license to use Intune to manage the devices.
- You must have a Windows 365 Enterprise or Windows 365 Flex license to manage Cloud PC configurations.

For Flex, the Windows Enterprise, Intune and Microsoft Entra ID licenses are also included in these subscriptions, so you may already own them:

- Microsoft 365 E3
- Microsoft 365 E5
- Microsoft 365 F3
- Microsoft 365 A3
- Microsoft 365 A5
- Microsoft 365 Business Premium
- Microsoft 365 Education Student Use Benefit

### Tenant and role requirements

Licenses are not the only requirement. You also need:

- A valid and working Intune and Microsoft Entra tenant.
- Intune enrollment restrictions that allow Windows (MDM) devices for corporate enrollment. The setting is the Intune default device type enrollment restriction.
- To provision Cloud PCs, the Intune Administrator role in Microsoft Entra ID or the Windows 365 Administrator role.
- Hybrid identities for Cloud PC users.
- No Azure requirement if you use Microsoft Entra joined Cloud PCs on a Microsoft hosted network. If you use your own network, you need an active Azure subscription.

If you use Microsoft Entra hybrid joined Cloud PCs, two more points apply. Users need a synced identity in both Active Directory and Microsoft Entra ID. Microsoft Entra Domain Services is not supported, because it does not support Microsoft Entra hybrid join.

The [plan the pilot article](/windows-365/plan-the-pilot/) puts these checks into a pilot checklist.

## How Flex licenses are counted

Flex licenses work differently from Enterprise licenses. This is the order of events:

1. You buy the licenses in the Microsoft 365 admin center. You can check the quantities under **Billing - Your Products**.
2. Each user holds the Windows Enterprise, Intune and Microsoft Entra ID P1 licenses.
3. The users are in the Microsoft Entra security group that the provisioning policy names.
4. The provisioning policy creates the Cloud PCs. The Flex licenses can be applied to either mode.

The Flex licenses are pooled at the tenant level. You do not assign them to individual users, so the Microsoft 365 admin center shows them as assigned to zero users. To see how many are in use, use the Windows 365 utilization report.

### Dedicated mode and Shared mode

| | Dedicated mode | Shared mode |
|---|---|---|
| Cloud PCs per license | Up to 3, each assigned to one user | 1, shared by a group of users |
| Active sessions per license | 1 | 1 |
| Who can use a Cloud PC | Each Cloud PC is assigned to one user through a Microsoft Entra user group | Any user in the assigned Microsoft Entra user group |
| Data between sessions | User data persists | User data is deleted after each session. With User Experience Sync turned on, app data and Windows settings are stored in the cloud. |
| Active sessions are limited by | The total number of Flex licenses bought for the tenant, not counting licenses used for Shared mode | The number of Flex licenses set up for the group |

Two examples:

- Dedicated mode: you buy 10 licenses. Up to 30 Cloud PCs can be provisioned, but only 10 of them can be active at one time. When a user signs off from their Cloud PC, the session is released for another user.
- Shared mode: you set up 10 shared licenses for a group. 10 Cloud PCs can be provisioned for that group. Only one user can connect to each shared Cloud PC at a time.

More rules:

- If the group on a Dedicated mode policy has more users than there are available Cloud PCs for the selected size, some users might not receive a Cloud PC.
- If a tenant has both Dedicated and Shared mode policies and you add licenses, Dedicated mode Cloud PCs are provisioned first.
- A prestarted Cloud PC does not use the license for the session until the user finishes connecting. If the user does not connect within two hours, the Cloud PC shuts down. Prestart exists for Dedicated mode.

### The concurrency buffer

The concurrency buffer lets a tenant go over the maximum number of active sessions a limited number of times per day. It exists in Dedicated mode only. It does not apply to Shared mode or to GPU-enabled Cloud PCs, which are Cloud PCs with a graphics processor.

To see how often the buffer is used, use the Windows 365 Flex connection hourly report. The Windows 365 Flex concurrency alert warns you each time the buffer is activated.

## Check how many Flex licenses are in use

The utilization report shows how many Flex licenses are being used. Compare that number with the quantity you bought under **Billing - Your Products**.

## Common mistakes

- **Assigning only the Windows 365 license.** Enterprise users also need Windows Enterprise, Intune and Microsoft Entra ID P1. Flex users need those three as well.
- **Looking for Flex licenses on users.** Flex licenses are pooled, so the Microsoft 365 admin center shows zero users. Use the utilization report.
- **Forgetting the security group.** A Flex user must be in the Microsoft Entra security group that the provisioning policy names.
- **Expecting three people online per Dedicated license.** One license gives up to three Cloud PCs, but only one active session.
- **Expecting more Cloud PCs than the pool allows.** In Dedicated mode, some users in a large group might not receive a Cloud PC.
- **Expecting the buffer to cover every Flex Cloud PC.** It does not apply to Shared mode or to GPU-enabled Cloud PCs.

## How to validate this in your environment

1. In the Microsoft 365 admin center, check your Windows 365 license quantities. For Flex, check the quantity under **Billing - Your Products**. A count of zero assigned users is expected for Flex.
2. For a test user, confirm that the user holds the Windows Enterprise, Intune and Microsoft Entra ID P1 licenses. For Enterprise, also confirm the Windows 365 license.
3. For a Flex test user, confirm that the user is in the Microsoft Entra security group named in the provisioning policy.
4. Open the Windows 365 utilization report and note how many Flex licenses are in use.
5. For Dedicated mode, open the Windows 365 Flex connection hourly report and check whether the buffer is being used.
6. Compare the number of licenses with the number of users you expect to be connected at the same time.

Next step: the [provision article](/windows-365/provision/) shows how the license, the group and the provisioning policy fit together.

## Sources

- [Requirements for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Windows 365 Flex licensing](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-flex-license)
- [What is Windows 365 Flex?](https://learn.microsoft.com/en-us/windows-365/enterprise/introduction-windows-365-flex)
