---
title: "Windows 365 Editions: Enterprise, Flex and Business"
seoTitle: "Windows 365 Editions: Enterprise, Flex, Business"
layout: post.njk
permalink: /windows-365/editions/
order: 210
part: 11
tags: w365-series
deck: "Compare the Business, Enterprise and Flex editions of Windows 365 and pick the one that fits your users."
---

Windows 365 comes in more than one edition. An edition is one version of Windows 365 with its own rules and license. Every edition gives users a Cloud PC, which is a Windows desktop that Windows 365 builds and runs for them. The editions differ in who they are for, how many Cloud PCs a license gives, how you set them up and how much you can manage them.

This article compares three editions: Business, Enterprise and Flex. After reading it, you can match your users to an edition. Windows 365 has other editions too, such as Windows 365 Government. They are not covered here. The [licensing article](/windows-365/licensing/) covers licenses in more detail.

Flex was called Frontline until Microsoft [renamed it](https://learn.microsoft.com/en-us/windows-365/whats-new). The product, licensing and capabilities are unchanged. Older articles may still say Frontline. This article says Flex.

The rest of this series builds an Enterprise pilot. If you have not chosen an edition yet, read this article first.

## Key terms

| Term | Meaning |
|---|---|
| Cloud PC | A Windows desktop that Windows 365 builds and runs for you. Users reach it with an app or a web browser. |
| Tenant | Your organization's own space in Microsoft cloud services. Users and licenses belong to it. |
| Microsoft Intune | Microsoft's device management service. Admins use it to set up and manage devices, including Cloud PCs. |
| Microsoft Entra ID | Microsoft's identity service. It holds the users and groups, and it signs users in. |
| Provisioning policy | The settings an admin chooses for Enterprise and Flex Cloud PCs, such as the network and whether users are local administrators. It is assigned to a Microsoft Entra group. Provisioning means creating the Cloud PCs. |
| Image | The Windows setup a Cloud PC is built from. Enterprise can use a gallery image (a standard image that Windows 365 offers) or a custom image (your own). |
| Join type | How a Cloud PC is registered with your directory. Business supports Microsoft Entra join only. |
| Azure virtual network | A network in your own Azure subscription that a Cloud PC can use to reach your resources. |
| Group Policy | A Windows way to apply settings to many PCs from one place. |
| Dedicated mode | A Flex mode where each Cloud PC is assigned to one user. One license can back up to three Cloud PCs. |
| Shared mode | A Flex mode where one Cloud PC is shared by a group of users, one user at a time. |
| Concurrent session | One user connected to a Cloud PC at a given time. A Flex license provides one. |
| Concurrency buffer | A way for Dedicated mode to go over its session maximum, a limited number of times per day. |
| Intelligent prestart | A Dedicated mode feature that starts a Cloud PC before the user usually connects. |
| User Experience Sync | A Shared mode setting that stores user-specific app data and Windows settings in the cloud. |
| Cloud Apps | Individual apps that Shared mode can give users instead of the full Cloud PC desktop. |
| Windows App | The app users install to connect to a Cloud PC. They can also use a web browser. |

## The editions at a glance

![A comparison grid with four columns: Windows 365 Business, Windows 365 Enterprise, Windows 365 Flex in Dedicated mode and Flex in Shared mode. Rows cover who it is for, Cloud PCs per license, setup, and how users connect. Shared mode deletes data on the Cloud PC at sign-out. Flex was formerly called Frontline.](/img/windows-365/windows-365-editions.svg)

*Source: [Compare Windows 365 Business and Enterprise](https://learn.microsoft.com/en-us/windows-365/business-enterprise-comparison), [What is Windows 365 Flex?](https://learn.microsoft.com/en-us/windows-365/enterprise/introduction-windows-365-flex), and [Access a Cloud PC](https://learn.microsoft.com/en-us/windows-365/end-user-access-cloud-pc).*

Business and Enterprise are set up per user. Flex works differently. A Flex license covers one active session at a time. In Dedicated mode it can back up to three Cloud PCs, each assigned to one user. In Shared mode it backs one Cloud PC that a group takes turns using.

## Windows 365 Business

Business is made for smaller organizations, up to 300 users. It is a simple way to buy and set up Cloud PCs.

- **Limit:** Business is capped at 300 users per tenant. Enterprise has no limit.
- **Licenses to buy:** There are no licensing prerequisites to buy and deploy Business. Some features, such as device management, can be used if users have the matching Microsoft license.
- **Setup:** When you assign a license to a user, Windows 365 creates a Cloud PC for that user with a standard image. You do not make a provisioning policy.
- **Join type:** Microsoft Entra join, without support for your own Azure virtual network.
- **Management:** Device management is limited to assigning and unassigning Cloud PC licenses in the Microsoft 365 admin center. You can do some device management in Intune if you have an Intune license, but the Cloud PCs do not show on the Windows 365 page in Intune.

Business does not support these things that Enterprise does: Group Policy and Intune policy management, monitoring, Intune troubleshooting, partner and programmatic access, and security baselines. Business uses a standard image only.

## Windows 365 Enterprise

Enterprise is for organizations that want to manage Cloud PCs with Intune. It has no user limit.

- **Licenses:** Each user needs a license for Windows 10 or 11 Enterprise, Microsoft Intune and Microsoft Entra ID P1.
- **Setup:** You create a provisioning policy. You choose the network, decide whether users are local administrators, and assign the policy to a Microsoft Entra group. Cloud PCs are built from gallery images or your own custom images. The [provisioning article](/windows-365/provision/) walks through this.
- **Join type:** Microsoft Entra join with or without an Azure virtual network, or Microsoft Entra hybrid join with an Azure virtual network.
- **Management:** Group Policy objects and Intune policies, app deployment, Windows updates through Intune, image management, resizing Cloud PCs, and the other management options that physical devices have in Intune.
- **Monitoring and support:** Endpoint analytics, service health and operational health alerts. Troubleshooting in Intune includes reprovisioning a Cloud PC to its initial state. Support tickets can be filed through Intune or the Microsoft 365 admin center.

## Windows 365 Flex

Flex helps save cost by letting several users use Cloud PCs on one license. Dedicated mode is for workers who need their own Cloud PC but not 24/7 access. Shared mode is for short tasks where data does not need to persist.

A Flex license is not a seat for one user. Here is an example. Buy 10 licenses, and 10 users can be connected at the same time. In Dedicated mode you can create up to 30 Cloud PCs for those users, but only 10 can be active at once.

Flex licenses are also [pooled at the tenant level](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-flex-license) and are not assigned to users. The Microsoft 365 admin center shows them as assigned to zero users. That is expected. To see how many licenses are being used, use the Windows 365 utilization report in the Microsoft Intune admin center: **Devices** > **Cloud PC performance** > **Cloud PC utilization**. Each user still needs a license for Windows 10 or 11 Enterprise, Microsoft Intune and Microsoft Entra ID P1.

Flex has two modes. Flex licenses can be used in either mode. How many sessions can be active depends on the mode:

- **Dedicated mode:** the total number of Flex licenses you bought for the tenant, not counting licenses used for Shared mode.
- **Shared mode:** the number of Flex licenses set up for the group.

### Dedicated mode

- One license lets you create up to three Cloud PCs, each assigned to a single user. Only one of them can be active at a time (one concurrent session).
- User data persists between sessions.
- It suits workers on a rotation schedule, workers across time zones and regions, part-time workers and contingent staff.
- When a user signs off, the session is released for another user.
- The concurrency buffer lets you go over the maximum a limited number of times per day. It does not apply to Shared mode or to GPU-enabled Cloud PCs.
- **Power off and start:** a Cloud PC powers off after the user signs off and powers on when a user connects, so the first connection can take longer. After sign-off it stays on for two hours. Reconnecting in that time is as fast as an Enterprise Cloud PC.
- **Intelligent prestart:** the system learns when a user usually connects and starts the Cloud PC before then. It needs the user to have connected on at least three of the past 30 days.
- **Session State Retention:** where it is available, an eligible Cloud PC hibernates after a set idle time instead of powering off, and resumes with apps and windows as they were. Cloud PCs with 2 vCPU and 4 GB of memory are not eligible. It is being rolled out in phases, so it may not be available for all tenants.
- If the group has more users than Cloud PCs available for the selected size, some users might not get a Cloud PC.

### Shared mode

- One license gives one Cloud PC that a group of users shares, one user at a time (one concurrent session).
- Any user in the assigned Microsoft Entra group can use it.
- When a user signs out, all user data is deleted and the Cloud PC is released for the next user. If User Experience Sync is turned on, user-specific app data and Windows settings are stored in the cloud.
- It suits customer-facing workers and external contractors who need a Cloud PC for specialized tasks for a short time and do not need data to stay.
- You can give users Cloud Apps instead of the full desktop.
- There is no concurrency buffer in Shared mode.
- Shared mode is currently available only for Azure Global Cloud. The [requirements article](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements) lists the regions where Shared mode can be provisioned.

### What Flex does not support yet

Flex does not yet support the resize remote action or cross-region disaster recovery.

## Compare how you manage them

| Area | Business | Enterprise | Flex |
|---|---|---|---|
| Who builds the Cloud PC | Windows 365, after you assign a license | Windows 365, from your provisioning policy | Windows 365, from a provisioning policy assigned to a Microsoft Entra group |
| Image | Standard image | Gallery or custom image | - |
| Group Policy and Intune policies | Not supported | Supported | - |
| Monitoring and troubleshooting | Not supported | Endpoint analytics, health alerts, Intune troubleshooting | - |
| Resize a Cloud PC | - | Supported | Not supported yet |
| Partner and Graph API access | Not supported | Supported for partners (Microsoft 365 Lighthouse and Graph APIs), up to 300 seats | - |

A dash (-) means the published material does not state this for that edition. Do not assume it matches Enterprise. Check it before you rely on it. Graph APIs are the Microsoft Graph web APIs that partners and tools use to manage Cloud PCs.

## Compare how users connect

The Windows App and the web client at windows.cloud.microsoft work for Business, Enterprise and Flex.

| Client | Business | Enterprise | Flex |
|---|---|---|---|
| Windows App | Yes | Yes | Yes |
| Web client (windows.cloud.microsoft) | Yes | Yes | Yes |
| Microsoft Remote Desktop app | Yes, but being retired | Yes, but being retired | No |
| LG webOS (web client on an LG TV with webOS 23) | Yes | Yes | No |

Windows App is the recommended app. The Microsoft Remote Desktop app is being retired. The Remote Desktop client for Windows (MSI) and the Microsoft Store version of the Remote Desktop app are no longer supported. Move users to Windows App. The Remote Desktop Connection client (mstsc.exe) is not a supported way to connect. It may work for troubleshooting, but it should not be used for daily access.

Users see their Cloud PCs under **Your Cloud PCs** on the Windows 365 home page at windows.cloud.microsoft. On a Cloud PC card, the gear icon lets them rename, reset, restart or troubleshoot the Cloud PC, or view its system information. Reset reinstalls Windows and removes personal files, settings and apps.

## How to choose

Work through these in order.

1. **Do you have more than 300 users?** Business is capped at 300 per tenant, so it is not an option. Consider Enterprise or Flex.
2. **Do you need Group Policy or Intune policies, your own image, monitoring, hybrid join or your own Azure virtual network?** Business does not support these. Choose Enterprise.
3. **Do users need a Cloud PC only part of the day, in shifts or part-time?** Consider Flex in Dedicated mode. Each user keeps their own Cloud PC and data.
4. **Do users need a Cloud PC for a short task and not need to keep any data?** Consider Flex in Shared mode.
5. **Does each user need their own Cloud PC available all day, every day?** Choose Enterprise or, for a small organization with simple needs, Business. Flex Dedicated mode is for workers who do not need 24/7 access.
6. **Are you a small organization that wants the simplest setup and does not need the items in step 2?** Business fits.

## Common mistakes

- **Choosing Business for a larger company.** It stops at 300 users per tenant.
- **Expecting Business to be managed like Enterprise.** Business has no provisioning policy, and policy management, monitoring and Intune troubleshooting are not supported.
- **Looking for Flex licenses on each user.** Flex licenses are pooled for the tenant. The admin center shows them as assigned to zero users.
- **Counting Cloud PCs as seats in Flex.** In Dedicated mode, the number of active sessions equals the number of licenses, and the number of Cloud PCs you can create is up to three times the number of licenses. In Shared mode, one license gives one Cloud PC and one session.
- **Using Shared mode for users who need to keep files.** Data is deleted at sign-out, unless User Experience Sync is turned on for app data and Windows settings.
- **Forgetting the wait on first connect in Dedicated mode.** The Cloud PC powers off after sign-off and starts on connect. Reconnecting within two hours is quick.
- **Searching for only one name.** Older articles may use the old name, Frontline. Search for both.

## How to validate this in your environment

1. In the Microsoft 365 admin center, open **Billing** > **Your products**, and confirm which Windows 365 licenses you have and how many.
2. For Flex, open the Windows 365 utilization report in Intune (**Devices** > **Cloud PC performance** > **Cloud PC utilization**) to see how many licenses are in use. Do not expect to see them assigned to users.
3. For Business, assign a license to one test user, wait for the Cloud PC to be created, and check that it appears for them under **Your Cloud PCs** at windows.cloud.microsoft.
4. For Enterprise or Flex, create a provisioning policy for a small test group, as in [Provision a Microsoft Entra Joined Cloud PC](/windows-365/provision/), and check the Cloud PC in the Microsoft Intune admin center.
5. Have a test user open the Cloud PC at windows.cloud.microsoft and in Windows App, and confirm both work. The [connect and verify article](/windows-365/connect-verify/) lists the checks.
6. After you create a Shared mode policy in step 4, with User Experience Sync off, sign in, create a file, sign out, sign in again and confirm the file is gone.
7. After you create a Dedicated mode policy in step 4, sign out, wait more than two hours, and note how long the next connection takes while the Cloud PC powers on.

## Sources

- [Compare Windows 365 Business and Enterprise](https://learn.microsoft.com/en-us/windows-365/business-enterprise-comparison)
- [What is Windows 365 Flex?](https://learn.microsoft.com/en-us/windows-365/enterprise/introduction-windows-365-flex)
- [Access a Cloud PC](https://learn.microsoft.com/en-us/windows-365/end-user-access-cloud-pc)
