---
title: "Windows 365 Flex Licensing in Practice: Concurrency Buffer and the License and Utilization Report"
seoTitle: "Windows 365 Flex Concurrency Buffer and License Report"
layout: post.njk
permalink: /windows-365/flex-concurrency-buffer/
order: 218
part: 19
tags: w365-series
deck: "Understand the Flex concurrency buffer and its limits, find buffer use in the reports, and read the data that helps you check your Flex license count."
---

With Windows 365 Flex, the number of licenses you buy sets how many users can be connected to their Flex Cloud PCs at the same moment. That number is the maximum concurrency limit, and it is set for each Cloud PC license size. When the limit is reached, the next user cannot connect. The concurrency buffer lets you go over that limit for a short time.

This article is for administrators who run Windows 365 Flex Cloud PCs in Dedicated mode, and who want to check whether they bought the right number of licenses. The reports cover Dedicated and Shared mode. The buffer applies to Dedicated mode only. After reading it you can explain how the buffer works and when it is blocked, find buffer use in the reports, read the License and utilization (preview) page, and list the questions to ask about your license count.

What each user needs and how Flex licenses are counted is in [Windows 365 licensing](/windows-365/licensing/). The reports overview is in [Monitor Windows 365](/windows-365/monitoring/). The differences between editions are in [Windows 365 editions](/windows-365/editions/). Removing Cloud PCs that nobody uses is in [Windows 365 grace period and unused licenses](/windows-365/grace-period-unused-licenses/). This article goes further on the buffer limits, the blocks and the License and utilization page.

![The maximum concurrency limit is set by the number of Flex licenses purchased. In Dedicated mode the concurrency buffer allows use over the limit up to four times per day for up to one hour each. Using the buffer for more than one hour on four or more occasions in 24 hours blocks it for 48 hours, and more than two such blocks in seven days block it permanently. While blocked, Flex Cloud PCs can still be used up to the limit. Reports and the License and utilization page show the use.](/img/windows-365/windows-365-flex-concurrency.svg)

*Source: [Concurrency buffer for Windows 365 Flex Cloud PCs in Dedicated mode](https://learn.microsoft.com/en-us/windows-365/enterprise/concurrency-buffer), [Connected Windows 365 Flex Cloud PCs report](https://learn.microsoft.com/en-us/windows-365/enterprise/report-connected-windows-365-flex-cloud-pcs) and [License and utilization in Monitor Cloud PCs (preview)](https://learn.microsoft.com/en-us/windows-365/enterprise/license-utilization).*

## Key terms

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop that Windows 365 runs in the cloud for a user. |
| Windows 365 Flex | A version of Windows 365. It has two modes: Dedicated and Shared. |
| Dedicated mode | A Flex mode for a Cloud PC assigned to one user. The concurrency buffer applies only to this mode. |
| Shared mode | A Flex mode for Cloud PCs that users share. It has no concurrency buffer. |
| Concurrent connections | Users connected to their Flex Cloud PCs at the same time. |
| Maximum concurrency limit | The most concurrent connections you can have for each Cloud PC license size. It is set by the total number of Flex licenses you bought. |
| Concurrency buffer | An allowance that lets your tenant go over the maximum concurrency limit for a short time. A tenant is your organization's own space in Microsoft's cloud. |
| Temporary block | A 48-hour period in which the buffer cannot be used. |
| Permanent block | The buffer cannot be used until support removes the block. |
| SKU | A specific license product. On the License and utilization page, licenses are grouped by type and SKU. |
| Microsoft Intune admin center | The web portal where you sign in to see the Flex reports. |
| Preview | A feature that is not yet generally available. It can change before it is. |

## What the concurrency buffer is

Think of a shift change. A worker on the old shift needs a few more minutes to finish. A worker on the new shift needs to start a bit early. For a short time you have more people connected than your licenses allow. The buffer lets that happen so these workers are not locked out.

The buffer is meant for rare and brief overuse.

## Who gets it

| Case | Concurrency buffer |
|---|---|
| Windows 365 Flex Cloud PCs in Dedicated mode | Yes |
| Windows 365 Flex Cloud PCs in Shared mode | No |
| GPU-enabled Cloud PCs | No |

## The limits

- You can use the buffer up to four times per day.
- Each use is for a maximum of one hour.
- The hour starts from the moment your tenant went over the maximum concurrency limit.

### Temporary block

Excessive use of the buffer blocks it for the next 48 hours. A temporary block starts when, on four or more occasions within a 24-hour period, the buffer is used for more than one hour. While blocked, you can still use your Flex Cloud PCs in Dedicated mode up to the maximum concurrency limit.

### Permanent block

If your tenant is temporarily blocked more than two times in a seven day period, it is permanently blocked from using the buffer. You can still use your Flex Cloud PCs up to the maximum concurrency limit. To remove the block, open a ticket with support from the Intune portal.

## See buffer use

Three places show it.

| Where | What it gives you |
|---|---|
| Connected Windows 365 Flex Cloud PCs report | Current connections, the limit and a history. It also shows which users are using the buffer now. If total connections go over the limit, you are using the buffer (Dedicated mode only). |
| Windows 365 Flex connection hourly report | Buffer use. |
| Windows 365 Flex concurrency alert | An alert each time the buffer is activated. |

### The Connected Windows 365 Flex Cloud PCs report

The report applies to Flex Dedicated and Shared mode. It does not apply to other Windows 365 plans. If you have no Flex licenses in your tenant, it shows no data. The buffer part applies to Dedicated mode only.

To open it, sign in to the Microsoft Intune admin center and select **Reports** > **Cloud PC overview** > **Connected Windows 365 Flex Cloud PCs (preview)**. Then select a Cloud PC size. Shared mode assignments appear under the size you select.

To view it you need the permissions **SharedUseLicenseUsageReport** and **SharedUseServicePlans**. To assign them, go to **Tenant administration** > **Roles** > **Create** > **Windows 365 role**.

The report shows data for the last 28 days:

| Item | Meaning |
|---|---|
| Current connections | Flex Cloud PCs connected now. |
| Concurrent connection history | A graph that can help you decide whether to buy more licenses. |
| Most concurrent connections | The highest number connected. You can view it daily for the past 7 or 28 days, or hourly for the past one, three or seven days. |
| Limit | The maximum concurrency limit, equal to the number of licenses you bought. |
| Reached concurrency limit | Warnings when you approach and when you reach the limit. |

Select **Connected** to see which Cloud PCs are connected now and how long their sessions are.

### If the limit is reached

Users after that point cannot connect. The history chart shows when you reach or exceed the limit for your tenant or for a selected group assignment. To unblock users you can:

- Restart some Cloud PCs to lower the number of connections. Use the session length to pick which ones. Restarting disconnects the user from their session.
- Redistribute licenses across the Microsoft Entra group assignment.
- Buy more licenses.

## The License and utilization (preview) page

This page gives you one view of Windows 365 license inventory and use. It shows assigned and available licenses by SKU, the peak number of concurrent Cloud PC connections, total hours used, and trends. Data appears after a connection has been made to a Cloud PC. The page keeps data for 180 days, and the **View data** table keeps 28 days.

### What is on it

| Section | What it shows |
|---|---|
| License breakdown | Total licenses in the tenant by license type. |
| Licenses by type & SKU | Total, assigned and available licenses for each type and SKU. |
| Max concurrent connections trend and Max concurrent connections | The peak number of simultaneous Cloud PC connections in the time range you pick. |
| Total hours used trend and Total hours used | The hours that Cloud PCs were used in the time range. |
| View data table | A closer view by device or by user. The **Devices** tab shows device name, device ID and session information. The **Users** tab shows the user principal name and, for certain license types, the number and length of sessions. |

The connection and hours charts support Enterprise, Flex Dedicated and Flex Shared. You can use them to see use by Cloud PC SKU, region and provisioning policy name.

### How fresh the data is

- Current license information normally updates within 3 minutes and is reconciled (checked for accuracy) once a day. Some license assignments can take up to 24 hours to appear, even though the Microsoft 365 admin center updates at once.
- For the usage charts, 2-hour and 12-hour data is available within 3 minutes. The 24-hour, 4-day, 7-day and 14-day views update every 30 minutes. The 28-day views and longer update daily.
- The **View data** table is always about 3 minutes behind.

### How to read it

1. Pick a time range.
2. Look at **License breakdown** and **Licenses by type & SKU** to see how many licenses you have, how many are assigned and how many are available.
3. Pick the type you want to explore.
4. Read the trend chart and the total chart to see how heavily the licenses are used compared with what is available, assigned or expected.

Assigned and available counts do not on their own tell you whether licenses are used well. Read them together with how you assign licenses in your organization.

## Questions to ask about your license count

These questions use only what the reports show.

- Does the peak on the Connected report reach **Limit** for a Cloud PC size? The report is there to help you make sure you bought the right number of licenses for your peak usage.
- Does **Concurrent connection history** show when you reach or exceed the limit? The graph can help you decide whether to buy more licenses. If total connections go over the limit, you are using the buffer (Dedicated mode only).
- Do **Max concurrent connections** and **Total hours used** show under-use or over-use by Cloud PC SKU, region and provisioning policy name? These charts also cover Enterprise Cloud PCs, so check which type you are looking at.
- Do the assigned and available counts tell the whole story? They do not. Read them together with how you assign licenses.

If users are blocked at the limit, the options are to restart some Cloud PCs, redistribute licenses across the Microsoft Entra group assignment, or buy more licenses.

## Common mistakes

- **Treating the buffer as extra licenses.** It is for rare and brief overuse, up to four times per day, up to one hour each time.
- **Expecting a buffer in Shared mode or on GPU-enabled Cloud PCs.** They do not have one.
- **Ignoring repeated use of the buffer.** Using it for more than one hour, four or more times within 24 hours, causes a 48-hour block. More than two blocks in seven days cause a permanent block.
- **Reading the Connected report without the right permissions.** You need SharedUseLicenseUsageReport and SharedUseServicePlans.
- **Deciding from assigned and available counts only.** Use the connection and hours charts too.
- **Reading new license changes too early.** Some can take up to 24 hours to appear on the License and utilization page.

## How to validate this in your environment

1. In the Intune admin center, go to **Tenant administration** > **Roles** and check that your role has the two report permissions.
2. Open **Reports** > **Cloud PC overview** > **Connected Windows 365 Flex Cloud PCs (preview)** and select a Cloud PC size. Compare **Limit** with the number of Flex licenses you bought.
3. Look at **Most concurrent connections** for 7 and 28 days. Note whether the peak reaches **Limit**.
4. Look at **Concurrent connection history** for any time when connections went over the limit. If they did, the buffer was used.
5. Select **Connected** and check which Cloud PCs are connected and how long their sessions are.
6. Check the Windows 365 Flex connection hourly report for buffer use.
7. Check whether anyone in your team receives the Windows 365 Flex concurrency alert. It is sent each time the buffer is activated.
8. Open the License and utilization (preview) page. Compare **Licenses by type & SKU** with your purchase, then read the peak concurrent connections and total hours for the time range you care about.

## Sources

- [Concurrency buffer for Windows 365 Flex Cloud PCs in Dedicated mode](https://learn.microsoft.com/en-us/windows-365/enterprise/concurrency-buffer)
- [Connected Windows 365 Flex Cloud PCs report](https://learn.microsoft.com/en-us/windows-365/enterprise/report-connected-windows-365-flex-cloud-pcs)
- [License and utilization in Monitor Cloud PCs (preview)](https://learn.microsoft.com/en-us/windows-365/enterprise/license-utilization)
