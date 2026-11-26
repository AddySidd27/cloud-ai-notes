---
title: "Monitor Windows 365: Reports, Connection Quality, Health"
layout: post.njk
permalink: /windows-365/monitoring/
order: 215
part: 16
tags: w365-series
deck: "Pick the right Intune report for a Cloud PC question: health, connection quality, performance, availability or usage."
---

When a user says "my Cloud PC is slow" or "I cannot connect", you need to know where to look. The Microsoft Intune admin center has several reports for Cloud PCs. Each one answers a different question. This article is for administrators who run Cloud PCs and want to know which report to open first.

It covers Windows 365 Enterprise and Windows 365 Flex Cloud PCs. It does not cover Windows 365 Business (see [Windows 365 editions](/windows-365/editions/)). It explains where each report is, what it shows, what to do with the result and which permissions it needs. The table near the end sums up which report answers which question. For restart, settings and the Cloud PC actions report, see [Manage settings, apps, updates and restart](/windows-365/manage-intune/). For a failed Azure network connection check, see [Reading an ANC health failure](/windows-365/anc-troubleshooting/).

## Key terms

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop that Windows 365 runs in the cloud for a user. |
| Microsoft Intune admin center | The web portal where you manage Cloud PCs and see their reports. |
| Enterprise and Flex | The two Windows 365 offerings these reports cover. |
| Windows 365 Flex | A version of Windows 365 where one license lets several users use Cloud PCs, but not at the same time. It runs in Dedicated mode or Shared mode. |
| Dedicated mode | A Flex mode where each Cloud PC is assigned to a single user. |
| Shared mode | A Flex mode where one Cloud PC is shared by a group of users, one at a time. User data is deleted when the user signs out. |
| Concurrency | How many Flex sessions are active at the same time. The limit equals the number of Flex licenses you bought. |
| Round trip time (RTT) | How many milliseconds it takes for communication to go between the client (the user's device) and the Cloud PC and back. The connection quality report measures it at the transport layer only. Lower is better. |
| P50 | The median: half of the measured values were lower and half were higher. A few very high values change it less than they change an average. |
| Remote sign-in time | How long a user waits to sign in to the Cloud PC. Monitor Cloud PCs shows the average time in seconds from sign-in until the first frame is shown. The connection quality report shows a P50 value instead, called remoting sign-in time. |
| Scope tag | A setting that can be assigned to an administrator role. Only administrators whose roles have no scope tags can open Monitor Cloud PCs. |
| Endpoint analytics | An Intune feature that holds the Resource performance report. You must enroll your Cloud PCs in it first. This article does not cover enrollment. |
| CPU and RAM spike | Processor or memory use over 50%. |
| Preview | A feature tagged **(preview)** in the admin center. It can be limited and can change before general availability. |

The column names in the reports are shown here as the reports spell them.

## Where the reports are

The reports are spread over a few places in the Intune admin center.

**Monitor Cloud PCs** is one page that brings together connection health, performance and configuration. Open it from **Devices** > **Manage Windows 365 Cloud PCs** > **Monitor Cloud PCs**. It has three tabs:

- **Connection health** shows the whole environment: the average number of active connections, the share of connection attempts that fail, remote sign-in time, the share of healthy Cloud PCs and round trip time.
- **User and devices** shows one user or one Cloud PC: connection history, connection errors, sign-in time, round trip time and Cloud PC health. It also shows resource use such as CPU and memory.
- **Configuration monitoring** shows how connections are spread across client platforms, deployment settings, Cloud PC configurations, operating system versions and application components.

A fourth page, **License and utilization (preview)**, is also in Monitor Cloud PCs. It is covered below.

The legacy reports are still under **Reports** > **Cloud PC overview**. Resource performance is under **Reports** > **Endpoint analytics**. Cloud PC utilization is under **Devices** > **Cloud PC performance**. Connectivity status is on each Cloud PC's page.

![Nine questions an administrator can ask about Cloud PCs, each matched to the Intune admin center report that answers it, from Connection health to Connected Windows 365 Flex Cloud PCs (preview).](/img/windows-365/windows-365-monitoring.svg)

The arrows match a question to a report. They are not steps in a sequence.

*Source: [Monitor Cloud PCs overview](https://learn.microsoft.com/en-us/windows-365/enterprise/monitor-cloud-pcs-overview) and [Windows 365 operations guide](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-operations-guide).*

## Start wide, then narrow down

The Monitor Cloud PCs pages are built for a top-to-bottom investigation. Start with **Connection health** to find broad patterns. Use **User and devices** to look at the affected Cloud PCs. Use **Configuration monitoring** to see whether the problem follows a shared configuration.

On each page you choose a data series, a time range and filters. Everything below the controls follows your choices. Select **View data** at the bottom of a page to see the table behind the charts.

Three limits to know:

- The pages do not refresh by themselves.
- Newer data is quicker to appear. Data for 2-hour and 4-hour ranges can be as little as 3 minutes old. Longer ranges take longer.
- **Connection health** and **User and devices** keep 28 days of data.

Read the charts as patterns. They do not name a cause on their own. Two reading tips from the connection health page: a high failure rate on very few attempts may not be a wide problem, so check the active connection count too. And an overall total can hide a short spike, so look at the trend chart to see when a change began. The pages also differ: **Connection health** shows an average round trip time, and **User and devices** shows the P50.

## Connection quality report

**Where:** **Reports** > **Cloud PC overview** > **Connection quality**.

**What it answers:** which Cloud PCs may be performing below expectations. It lists one Cloud PC per row with these columns:

- Device name
- Round trip time for the most recent or current connection, and the P50 for the date range
- Available bandwidth for the most recent or current connection, and the P50 for the date range
- Connection gateway
- Remoting sign-in time (P50), in seconds
- Client IP address
- Protocol for the most recent or current connection
- UDP utilization average over the date range
- Device type, which is the offering: Enterprise, Windows 365 Flex dedicated or Windows 365 Flex shared

You can pick the columns, filter each column and choose a date range of 7 or 28 days. Each row links to the Cloud PC, where you see its connection history.

Connection quality is partly a matter of opinion, so decide what "good enough" means for your organization. Then use the filters to find connections that do not meet it. Possible causes to check:

- Network, host or client configurations that limit the protocol choice.
- Geographic distance.
- Authentication methods and architecture.
- Whether the client or host is appropriate.

Use the P50 columns to judge a longer period. Use the "most recent or current" columns to judge what the user is seeing now. Do not mix the two when you describe a problem.

## Connectivity health checks

**Where:** **Devices** > **All Cloud PCs** > select a Cloud PC > **Overview** > **Performance**.

**What it answers:** can this one Cloud PC accept a connection right now. The Windows 365 service runs connectivity checks on each Cloud PC all the time. If a check fails, the user cannot connect. The status shows **Available** when the Cloud PC is connected and **Unavailable** when malfunctioning components cause a problem. Flex Cloud PCs in Shared mode add two states. **In use** shows after a user signs in. **Unavailable (Servicing)** shows after a user signs out, while the Cloud PC resets before it returns to the available pool.

When a check fails, the status pane shows one of these messages:

| Message | Meaning |
|---|---|
| DomainJoin | The Cloud PC is not joined to a domain. |
| DomainReachable | The Cloud PC cannot connect to the domain. Review your Azure virtual network checks. |
| DomainTrust | The domain does not trust the Cloud PC. |
| SxSStackListener | The side-by-side stack on the Cloud PC is malfunctioning or blocked. |
| UrlsAccesibleCheck | The Cloud PC is blocking traffic to the required URLs. |
| Unknown | The Cloud PC might not be running, or the network is not connected to the public internet. |

A passed check does not guarantee a good connection, because connectivity errors can still happen when every check passed. The check names are shown exactly as the report spells them.

The **Troubleshoot this connection** button appears only when the status is **Unavailable**. It checks that the device is ready, checks that the services work and tries to fix what it finds. While it runs, users cannot connect. It can take several minutes and the device might restart. Warn the user first.

The **user connectivity history report** is under **View report** in the **Connectivity status** section of the same page. It lists **Connection started**, **Connection finished** and **Connectivity check** activities. A connection that ends with an unexpected network error shows as **Connection finished** with a **Failure** status. After an error or failed check, the report also shows the other activity from one hour before and after, so you can see whether and when the Cloud PC became healthy again.

## Cloud PCs that aren't available

**Where:** **Reports** > **Cloud PC overview** > **Cloud PCs that aren't available**.

**What it answers:** which Cloud PCs were recently unavailable. The data is 5 to 15 minutes old. A Cloud PC in the list may have recovered already, and one that just failed may not be listed yet.

Columns include user name, host health (the most recent Cloud PC host health check error, if any), connection error, system status, region, device status, last event and issue details. An empty column means there is nothing to report in that area, so it is probably not the cause.

Here is an example of reading the columns together. If **Host health** and **System status** are empty, **Device status** is **Provisioned**, **Connection error** says **Client Disconnect** and other Cloud PCs in the same region are not listed, the problem is probably specific to that user. It may be the physical client configuration, the network configuration or the network infrastructure.

You can select **View details** for the recent history of a Cloud PC. You can also use **Bulk device actions** on selected Cloud PCs (up to 100,000).

## Resource performance report

**Where:** **Reports** > **Endpoint analytics** > **Resource performance**.

**What it answers:** are the Cloud PCs short of processor or memory. Before you use it, enroll your Cloud PCs in Endpoint analytics. This article does not cover enrollment.

The report has four tabs:

- **Resource performance score:** a rating from 0 to 100 for all your Cloud PCs. It is a weighted average of a CPU spike time score and a RAM spike time score. Each spike percentage is the ratio of spike time to total usage time, averaged over 14 days. Use over 50% counts as a spike. A baseline helps you see whether you are meeting your goals. You can set it to the organizational median or a custom value. The tab also lists insights and recommendations.
- **Model performance:** the scores for each Cloud PC model SKU.
- **Device performance:** the scores for each Cloud PC.
- **Device history:** the history for one device you select.

If a device scores below the baseline, you can add resources by taking a resize action. This applies to Enterprise Cloud PCs. Flex Cloud PCs in Dedicated mode are resized in the provisioning policy, and Flex Cloud PCs in Shared mode cannot be resized.

## Cloud PC utilization report

**Where:** **Devices** > **Cloud PC performance** > **Cloud PC utilization**. For one Cloud PC, select **Reports** > **Cloud PC overview** > **Cloud PC utilization**, select the device, then **Performance (preview)**.

**What it answers:** who uses their Cloud PC, and how much. Low use costs money. You can save by reassigning under-used licenses to other users or by deprovisioning Cloud PCs that stay inactive for a long time.

A histogram counts Cloud PCs by time connected: more than 80 hours is high, 40 to 80 hours is average, less than 40 hours is low and zero is none. You choose a timespan of 28, 60 or 90 days. The list shows device name, user, PC type, time connected, date last connected, date created and device type. Time connected is the total hours over the last four weeks, and date last connected looks back up to 60 days. The 40 and 80 hour ranges are given without a stated scaling for 60 or 90 days. You can filter by PC type, time connected and date last connected. In the **Time connected** section of one Cloud PC, select **View report** for more detail.

A related page, **License and utilization (preview)**, is in Monitor Cloud PCs. It shows assigned and available licenses by SKU, peak concurrent connections, total usage hours and trends. It keeps 180 days of data, and its **View data** table keeps 28 days. It shows data only after a connection has been made to the Cloud PC.

## Connected Windows 365 Flex Cloud PCs report

**Where:** **Reports** > **Cloud PC overview** > **Connected Windows 365 Flex Cloud PCs (preview)**, then select a Cloud PC size.

**What it answers:** whether you own enough Flex licenses for your peak use. The report applies only to Windows 365 Flex, in Dedicated or Shared mode. If you have no Flex licenses it shows no data.

The maximum concurrency limit equals the number of licenses you bought. When it is reached, other users cannot connect. In Dedicated mode only, a concurrency buffer lets your organization temporarily go over the limit, so connections above the limit mean the buffer is in use. The report shows current connections, a concurrent connection history aggregated for the last 28 days, the highest number of concurrent connections (daily for the past 7 or 28 days, hourly for the past one, three or seven days), the limit and warnings when you near or reach it. Select **Connected** to see who is connected and for how long. To unblock users when the limit is reached, you can restart Cloud PCs to bring concurrency down, redistribute licenses across the Microsoft Entra group assignment or buy more licenses.

## Admin Insights, alerts and Admin Assistant

Three more tools help you decide where to look first.

- **Admin Insights** is a ranked list of items that the service finds, shown as cards (up to 15). Open it from **Devices** > **Manage Windows 365 Cloud PCs** > **Cloud PC Overview**. It is also on the **Connection health** tab of Monitor Cloud PCs. It needs Windows 365 Enterprise or Flex licensing and read permissions, typically given by the Cloud PC Reader, Cloud PC Administrator or Windows 365 Administrator role. It shows data for all your Cloud PCs and does not apply scope tags.
- **Alerts** notify you when specific events occur, such as connection or provisioning failures. By default they appear as pop-ups in the Intune admin center, and you can turn on email. Alert rules are under **Tenant administration** > **Cloud PC Alerts** > **Alert rules**. To see alerts, your account needs Windows 365 Enterprise and the Intune Administrator or Windows 365 Administrator role.
- **Windows 365 Admin Assistant** (preview) lets you describe a problem in plain language. It is under **Windows 365** > **Windows 365 Admin Assistant**. In the preview it focuses on connectivity problems. It gives guidance but does not change settings or run repairs. Check the data it shows before you act on its explanation.

## Which report answers which question

| Question | Report | Where |
|---|---|---|
| Is the whole environment healthy? | Connection health | **Devices** > **Manage Windows 365 Cloud PCs** > **Monitor Cloud PCs** |
| What happened to one user or one Cloud PC? | User and devices | Same Monitor Cloud PCs page |
| Do connections share a client, setting or version? | Configuration monitoring | Same Monitor Cloud PCs page |
| Which Cloud PCs have a weak connection? | Connection quality | **Reports** > **Cloud PC overview** |
| Which Cloud PCs were recently unavailable? | Cloud PCs that aren't available | **Reports** > **Cloud PC overview** |
| Why can one Cloud PC not connect? | Connectivity health checks and connection history | **Devices** > **All Cloud PCs** > Cloud PC > **Overview** > **Performance** |
| Is a Cloud PC short of CPU or RAM? | Resource performance | **Reports** > **Endpoint analytics** |
| Who barely uses their Cloud PC? | Cloud PC utilization | **Devices** > **Cloud PC performance** |
| Are my Flex licenses enough at peak use? | Connected Windows 365 Flex Cloud PCs | **Reports** > **Cloud PC overview** |

## Permissions

Only some pages state what they need. Check the others in your own environment.

| Item | What is stated |
|---|---|
| Monitor Cloud PCs | Only administrators whose roles have no scope tags assigned can open it. |
| Admin Insights | Windows 365 Enterprise or Flex licensing, and read permissions, typically given by the Cloud PC Reader, Cloud PC Administrator or Windows 365 Administrator role. |
| Alerts | Windows 365 Enterprise, and the Intune Administrator or Windows 365 Administrator role. |
| Connected Windows 365 Flex Cloud PCs | Two permissions with these names: SharedUseLicenseUsageReport and SharedUseServicePlans. To assign them, go to **Tenant administration** > **Roles** > **Create** > **Windows 365 role**. |
| Resource performance | Your Cloud PCs must be enrolled in Endpoint analytics. |

## Common mistakes

- **Treating a chart as a cause.** The charts show patterns. A high round trip time or failure rate does not say why.
- **Reading a rate without the count.** A high failure percentage on a few attempts may not be a wide problem.
- **Mixing "most recent" and P50 values.** They answer different questions. Connection health shows an average and User and devices shows P50, so do not compare them directly.
- **Trusting the not-available list as live.** It is 5 to 15 minutes old.
- **Running Troubleshoot at a bad time.** Users cannot connect during it, and the Cloud PC might restart.
- **Expecting fresh data on a long time range.** Pick a short range for a problem that just happened.

## How to validate this in your environment

1. Open **Devices** > **Manage Windows 365 Cloud PCs** > **Monitor Cloud PCs**. Check that you can open **Connection health**. If you cannot, ask whoever manages your Intune roles whether your role has scope tags assigned.
2. On **Connection health**, pick a 2-hour range. Note the active connection count, failure rate, remote sign-in time, Cloud PC health and round trip time. Then pick a longer range and compare. Check that the trend chart shows when a change began, because a total can hide a short spike.
3. Open **User and devices**. Select one test user or Cloud PC and read its connection history and errors. Select **View data** and look at the table.
4. Open **Reports** > **Cloud PC overview** > **Connection quality**. Switch between 7 and 28 days. Find your test Cloud PC and compare its most recent values with its P50 values.
5. Open the test Cloud PC under **Devices** > **All Cloud PCs** > **Overview** > **Performance**. Confirm the status is **Available**. Open **View report** under **Connectivity status** and find a connection you made.
6. Open **Cloud PCs that aren't available**. Check whether your test Cloud PC is in the list. Remember the 5 to 15 minute delay.
7. This needs Cloud PCs that are already enrolled in Endpoint analytics. Open **Reports** > **Endpoint analytics** > **Resource performance** and find your test Cloud PC on the **Device performance** tab.
8. Open **Cloud PC utilization**, pick 28 days and check the time connected for your test Cloud PC against the 40 and 80 hour ranges (low, average and high).

Do not run **Troubleshoot this connection** on a Cloud PC that is in use just to test it.

## Sources

- [Monitor Cloud PCs overview](https://learn.microsoft.com/en-us/windows-365/enterprise/monitor-cloud-pcs-overview)
- [Windows 365 operations guide](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-operations-guide)
- [Cloud PC connection quality report](https://learn.microsoft.com/en-us/windows-365/enterprise/report-cloud-pc-connection-quality)
