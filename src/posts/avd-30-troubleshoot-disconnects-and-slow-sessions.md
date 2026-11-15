---
title: "Troubleshoot AVD Disconnects and Slow Sessions"
seoTitle: "Troubleshoot AVD Disconnects, Lag and Slow Sessions"
layout: post.njk
permalink: "/azure-virtual-desktop/troubleshoot-disconnects-and-slow-sessions/"
order: 130
part: 30
tags: [avd-series]
deck: "Work out whether a dropped session, laggy typing or a slow sign-in comes from the network, the transport, the session host or the logon steps, and which logs show it."
description: "Ordered checks for Azure Virtual Desktop sessions that drop, lag or sign in slowly: scope, round-trip time, RDP Shortpath, host load, proxies and log queries."
---

A user says the session keeps dropping. Another says the mouse lags behind their hand. A third waits minutes for the desktop to appear after signing in. These sound alike, but they have different causes, and the quickest way to find the cause is to check things in a fixed order.

This article gives that order. It covers three symptoms: a session that drops and reconnects, a session that is slow while connected, and a slow sign-in. Each check says where to look and what the documentation says about it. The checks use Log Analytics (Azure's log search tool) and Azure Virtual Desktop Insights (a ready-made dashboard built on Azure Monitor workbooks). Neither returns anything until diagnostics are switched on. The [Turn on the logs and learn to read them](/azure-virtual-desktop/troubleshoot-avd-start-here/) shows how to turn them on and how to read the tables, so do that first.

Before any check, look at the Azure status page and Azure Service Health (the pages that show current Azure problems). The troubleshooting overview says to do this before anything else.

## Key terms

| Term | Meaning |
|---|---|
| Session host | A virtual machine that runs users' desktops or apps. |
| Host pool | A group of session hosts that users share. |
| Gateway | The Azure Virtual Desktop service part that connects a user's device to a session host. Each gateway has a region code. |
| Round-trip time (RTT) | How long a network request takes to go from the user's device to the session host and back. It is measured in milliseconds (ms). |
| Transport | The network protocol that carries the session. TCP goes through the gateway. UDP is a faster protocol that does not resend lost packets. |
| RDP Shortpath | A feature that sets up a direct UDP path between the user's device and the session host. If it fails, the session stays on TCP. |
| STUN and TURN | Two ways to set up a UDP path through a NAT. STUN finds the device's public address so the two sides can connect directly. TURN sends the traffic through a relay server when a direct path is not possible. |
| NAT | Network address translation. A device that lets many computers share one public IP address. |
| Input delay | How long a mouse or keyboard action waits in the queue before the program on the session host picks it up. |
| Log Analytics workspace | The Azure store where the logs go. You search it with queries. |
| Diagnostic setting | The setting on a host pool, application group or workspace that sends its logs to a Log Analytics workspace. |
| KQL (Kusto Query Language) | The language used to write those queries. |
| CorrelationId | An ID that every log row of one connection shares. Use it to follow one connection across tables. |
| Insights | Azure Virtual Desktop Insights. A dashboard of tabs, built on Azure Monitor workbooks. |
| Proxy | A server that web traffic passes through on its way out of a network. |
| SSL inspection | A proxy feature that opens encrypted traffic to read it. The proxy replaces the real certificates with its own. |
| FSLogix profile container | A virtual disk file that holds a user's profile and attaches at sign-in. |
| Group Policy | A Windows feature that applies settings to computers and users at sign-in. |

## What the user says, and where to start

This table is a suggested mapping, not one from the documentation.

| What the user says | Start with |
|---|---|
| "The session keeps dropping and reconnecting" | Checks 1, 3 and 4 |
| "Typing and the mouse lag" | Checks 2, 5 and 6 |
| "The picture is choppy or video stutters" | Check 2 (network data and graphics data) |
| "It takes forever after I sign in" | Check 7 |
| "I have to sign in again after the screen locks" | Check 8 |

The picture asks the sign-in question early because the user can answer it in seconds. The numbered checks below go deeper into each branch, in the order of the Insights tabs.

![Decision tree for disconnects and slow sessions. The first question is whether the problem affects one user or many; many leads to Service Health and Insights, one leads on to a series of yes or no questions. Those ask about sign-in only, high round-trip time, a busy host, TCP instead of UDP, and Shortpath, client or server disconnect errors, and each yes leads to one action.](/img/avd/troubleshoot-disconnects-and-slow-sessions.svg)

*Source: Troubleshooting overview, Insights use cases and glossary, Troubleshoot connection quality, Troubleshoot RDP Shortpath, RDP Shortpath and Proxy server guidelines. The order of the questions is a suggestion.*

## Check 1: how wide is the problem?

Find out first if one user, one host, one place or everyone is affected. The answer saves time. One user usually points to that user's device or network. Everyone on one host points to the host. Everyone from one place points to the network path from that place.

Insights is the quickest place for this. Open it from the host pool (Azure portal, Azure Virtual Desktop, Host pools, your host pool, Insights), or go to `https://aka.ms/avdi`. Pick the subscription, resource group, host pool and time range. Three tabs matter here:

- **Connection Reliability.** It shows a graph of disconnections against concurrent connections and a table of the 20 time slices with the most disconnections. Select a row, then pivot (group the same events a different way) by session host, gateway region, client type, client version, transport and others. A pivot where one value stands out shows what the disconnects have in common.
- **Connection Performance.** It shows round-trip time by gateway region, with the median (the middle value) and the 95th percentile (the value that 95% of measurements stay below). A 95th percentile far above the median means some users have periods of high latency.
- **Host Performance.** It shows input delay for each session host, and CPU, memory and disk graphs.

The documentation also lists a **Clients** tab that shows users with outdated clients. It says older clients may lack fixes. If the drops cluster on one client version, update that client.

You can get the same client information with a query. This one is a documentation sample:

```kusto
WVDConnections
| summarize UserCount=dcount(UserName) by ClientType, ClientVersion
| sort by ClientVersion, ClientType, UserCount desc
```

It counts the different users (`dcount`) for each client type and version. The result shows one row per client and version. If the affected user's client version is much older than the others in the list, update that client first.

## Check 2: network or host?

A slow session is slow either because the path between the user and the host is slow, or because the host itself is busy. Look at both.

**The network side.** The `WVDConnectionNetworkData` table holds the estimated round-trip time and the estimated available bandwidth of each connection. The service writes a row every two minutes during an active session. Each row carries the connection's CorrelationId. The round-trip time is measured the same way for TCP and UDP. Two cautions from the documentation: a session that is not actively used sends data less often, and if no rows arrive, check the diagnostic settings, the session host configuration and whether the session is in use.

The documentation gives different numbers for what is acceptable. They are not reconciled, and this article does not pick one:

| Page | What it says about round-trip time |
|---|---|
| Troubleshoot connection quality | Up to 150 ms should not affect work that has no rendering or video. 150 to 200 ms should be fine for text processing. Above 200 ms might affect the experience. Round-trip time from the client's network to the Azure region of the host pool should be under 150 ms. |
| Use cases for Insights | Ideal interaction needs latency generally below 100 ms. A session broadly becomes low quality over 200 ms. |

One reasonable reading: hold graphics and video users to the lower numbers and text users to the higher ones. The first query below shows round-trip time for one user.

**The graphics side.** If the complaint is a choppy picture, the documentation also describes a connection graphics table (preview). The service writes to it only when the quality drops to "okay" or "bad", at most once every two minutes. It covers the graphics stream only. It does not capture slowness from an application or from the virtual machine's CPU or storage. The page says to read it together with the VM's own metrics. The thresholds it gives for end-to-end delay per frame are under 150 ms good, 150 to 300 ms okay and over 300 ms bad. To collect this table, select the Connection Graphics category in the host pool's diagnostic setting.

**The host side.** Open the Host Performance tab and read the **Input delay by host** table. Input delay is the time a mouse or keyboard action waits before the program picks it up. The documentation gives two sets of numbers here as well:

| Page | What it says about input delay |
|---|---|
| Insights glossary | Good is below 150 ms. Acceptable is 150 to 500 ms. Poor is 500 to 2,000 ms. Bad is over 2,000 ms. |
| Use cases for Insights | Ideally the input delay for each host should be below 100 ms. Above 100 ms, look at CPU, memory and disk. |

The counter behind it is `User Input Delay per Session` (and `per Process`). It reports the longest delay in each interval, because users notice the slowest input, not the average. It works on Windows Server 2019 or later and Windows 10 version 1809 or later. Insights collects it every 30 seconds.

## Check 3: which transport is the session using?

By default, a session starts on TCP through the gateway and then tries to set up UDP. If UDP works, the TCP connection drops. If not, the session stays on TCP. The documentation says UDP offers better connection reliability and more consistent latency, while TCP has the best compatibility.

To see which transport sessions use, query `WVDConnections` and look at the `TransportType` column. The table page lists the values `Shortpath`, `TURN` and `Websocket`. Insights groups the same data by **Transport** and lists different words: `Multipath`, `Relay`, `ShortpathPublic` and `ShortpathPrivate` for UDP, and `NotUsed` for TCP. The pages do not explain the difference, so expect different words in the two places.

To test one device, run the `avdnettest.exe` tool from the Troubleshoot RDP Shortpath page on that device. It checks DNS, TURN support and the NAT type. On success, the page shows output that ends with a line like this:

```output
You have access to TURN servers and your NAT type appears to be 'cone shaped'.
Shortpath for public networks is very likely to work on this host.
```

The page presents this as example output. If the test fails, UDP is probably blocked. The documentation says the session then falls back to TCP. The [connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/) covers the ports and the switches that decide whether UDP is used. The [bandwidth and latency article](/azure-virtual-desktop/plan-bandwidth-latency-and-quality-of-service/) covers what a good round-trip time looks like.

## Check 4: which disconnect reasons appear?

The Shortpath troubleshooting page names a few errors that "might be logged in Log Analytics". These are the only disconnect names this article uses:

| Name | What the documentation says |
|---|---|
| `ShortpathTransportNetworkDrop` | Under this name the page explains how TCP and UDP differ. TCP can signal a hard shutdown with a reset, but UDP has no such signal, so the only way to know the other side is gone is a time-out. |
| `ShortpathTransportReliabilityThresholdFailure` | A specific packet did not get through even though the connection was not dead. The packet is resent up to 50 times. It can happen when a fast, stable connection suddenly stops working, or when the packet is large and the maximum packet size has shrunk. |
| `ConnectionBrokenMissedHeartbeatThresholdExceeded` | An RDP-level time-out. Because of a misconfiguration, it can sometimes trigger before the UDP time-out. |
| `ConnectionFailedClientDisconnect` and `ConnectionFailedServerDisconnect` | Most errors like these are caused by TCP Reset packets (a signal that hard-closes a TCP connection), not by a time-out. |

The page does not say which table or column holds these names. The query in the next section searches two columns that exist in `WVDErrors`, `CodeSymbolic` and `Message`, and it is written for this article. If it returns nothing, that does not prove there were no drops.

## Check 5: the path between the user and the host

If round-trip time is high, the documentation lists these steps:

- **Reduce the distance.** Where possible, users should connect to VMs in the Azure region closest to them. The Azure network round-trip latency statistics page shows which regions are closest. The documentation suggests reviewing it every two to three months.
- **Check the network configuration.** Firewalls, ExpressRoute and other network features can affect round-trip time.
- **Check the bandwidth.** The documentation says users may lose the connection or see input delay when the network is saturated or rate-limited, or when a user's internet connection is unstable and latency is over 200 ms.

Proxies are a common cause of slow or unstable sessions. The proxy guidelines say:

- Bypass proxies for Azure Virtual Desktop traffic where you can. Most proxies are not built for long-running WebSocket connections, and that can hurt stability.
- A proxy that is the only path forces RDP over TCP instead of UDP, which lowers visual quality and responsiveness.
- Do not use SSL inspection. It can slow sign-in and can stop the Azure Virtual Desktop agent working.
- Do not use a proxy that needs authentication, because the session host components do not support one.
- Place any proxy in the same geography as the clients and the hosts.

The Shortpath page adds general advice for UDP to work: avoid force tunnelling if users connect over the internet, avoid double NAT or carrier-grade NAT, avoid cloud packet-inspection services and TCP-based VPNs, and enable IPv6 or Teredo. It also says a TURN relay update can drop a session, and that the client reconnects within a few seconds. The [required connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) covers the URLs and ports.

## Check 6: is the session host overloaded?

On the Host Performance tab, if input delay is above 100 ms, look at the graphs for CPU, memory, disk timing and disk queue length for the same period. The Host Diagnostics tab shows which hosts crossed thresholds for available memory, page faults, CPU use, disk space and input delay per session.

The documentation says that if CPU use is too high or available memory too low, the VM size or storage might be too small for the workload. It also says that where a host has long periods of high use, you should consider a larger VM size. The [VM size article](/azure-virtual-desktop/choose-session-host-vm-sizes/) covers sizing. The documentation does not give a sessions-per-host number here, so fewer sessions per host is an inference from an overloaded host, not a documented figure.

## Check 7: is the slow part the sign-in?

Insights breaks "time to connect" into parts. It starts when the connection state is `Started` and ends when the shell is ready (`ShellReady` for a desktop). The parts are:

| Part | What it is | Where the documentation points |
|---|---|---|
| User route | From selecting the icon to the service finding a host | Network paths |
| Stack connected | From finding the host to the remote client connecting to it | Network routing, proxy settings on client and hosts |
| Logon | From the connection to the start of the shell. It has four parts: profiles, Group Policy objects, shell start and FSLogix | Profile size and location, number of policies, how close the domain controller is, FSLogix share placement |
| Shell start to shell ready | From the shell starting to it being ready | Host overload (CPU, memory, disk) or configuration |

The page also says a new session takes longer than reconnecting to an existing one, and the time the user spends typing credentials is subtracted.

The four parts run partly in parallel, so they do not add up to the total. The total is measured separately. This query from the documentation shows the average time between the `Started` and `Connected` states by host pool and by session type. That is not the same as the Insights "time to connect": it ends at `Connected`, not at shell ready, and it still includes the time a user spends typing credentials. Use it to compare hosts and pools, not as a logon time:

```kusto
WVDConnections
| where TimeGenerated > ago(24h)
| where State == "Started"
| project CorrelationId , UserName, ConnectionType , StartTime=TimeGenerated, _ResourceId
| join kind=inner
(
    WVDConnections
    | where State == "Connected"
    | project ConnectTime=TimeGenerated, CorrelationId
) on CorrelationId
| join kind=inner
(
    WVDCheckpoints
    | where Name =~ "LoadBalancedNewConnection"
    | extend LoadBalanceOutcome=tostring(parse_json(Parameters).LoadBalanceOutcome)
) on CorrelationId
| project Duration = ConnectTime - StartTime, _ResourceId, Session=case(LoadBalanceOutcome in ("Active", "Disconnected"), "ExistingSession", LoadBalanceOutcome == "Pending", "Creating", LoadBalanceOutcome)
// Exclude connections that are happening while another connection kicked off the session creation, since results will be inconclusive
| where Session != "Creating"
| summarize AvgDuration=avg(Duration) by _ResourceId, Session
| parse _ResourceId with "/subscriptions/" subscription "/resourcegroups/" ResourceGroup "/providers/microsoft.desktopvirtualization/hostpools/" HostPool
| project ResourceGroup, HostPool, Session, AvgDuration
| sort by AvgDuration desc
```

How to read it: each row is one host pool and one session type (`ExistingSession` means the user reconnected, any other value is a new session). `AvgDuration` is the average time from `Started` to `Connected`, in `hh:mm:ss` form. The same query is explained in the [FSLogix playbook](/azure-virtual-desktop/troubleshoot-fslogix-profile-fails-to-load/). The documentation gives no "too long" number, so compare host pools and days with each other. A host pool that is much slower than the others, or slower than it was last week, is the one to look into.

If the logon part is the long one, look at the profile first. Go to the [FSLogix playbook](/azure-virtual-desktop/troubleshoot-fslogix-profile-fails-to-load/). The glossary says a long FSLogix launch time might mean a problem with the shares that hold profiles, and that large profiles slow it down.

## Check 8: prompted for credentials after a lock

If users must give full credentials after the session locks, the session lock behaviour is the likely cause. With single sign-on through Microsoft Entra ID, the default is to disconnect the session on lock. The user can then reconnect without being asked again, when the Conditional Access policies allow it. If an admin changed it to show the remote lock screen, users have to enter full credentials. The setting is "Disconnect remote session on lock for Microsoft identity platform authentication". The [sign-in article](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/) and the [sign-in playbook](/azure-virtual-desktop/troubleshoot-sign-in-and-conditional-access/) cover the rest.

## Queries

Replace `userupn` with the user's sign-in name. The first query is a documentation sample. The other three are written for this article and are not documentation samples. They use only columns listed on the table pages. Read the results with care and check them against Insights.

**Session length by user (documentation sample).** A run of short durations for one user means repeated drops:

```kusto
let Events = WVDConnections | where UserName == "userupn" ;
Events
| where State == "Connected"
| project CorrelationId , UserName, ResourceAlias , StartTime=TimeGenerated
| join (Events
| where State == "Completed"
| project EndTime=TimeGenerated, CorrelationId)
on CorrelationId
| project Duration = EndTime - StartTime, ResourceAlias
| sort by Duration asc
```

How it works: the first line saves the user's connection rows as `Events`. The query then pairs each `Connected` row with the `Completed` row that has the same `CorrelationId` and subtracts the times to get the session length. Healthy: a few long sessions, such as hours, that match the user's working time. Bad: many sessions of a few minutes or less, or only short ones at the top of the list. A session that never completed has no `Completed` row, so it does not appear at all.

**Automatic reconnects per day (written for this article).** The table page says `PredecessorConnectionId` is filled when a connection is an automatic reconnect:

```kusto
WVDConnections
| where UserName == "userupn"
| where isnotempty(PredecessorConnectionId)
| summarize AutoReconnects = dcount(CorrelationId) by bin(TimeGenerated, 1d)
```

Line 2 keeps this user's rows. Line 3 keeps only rows where `PredecessorConnectionId` is not empty, which are automatic reconnects. Line 4 counts the different connections for each day (`bin(TimeGenerated, 1d)` groups times into one-day buckets). Healthy: no rows, or a count of 0 to 1 on most days. Bad: a day with many reconnects, which matches "keeps dropping". No fixed number is given in the documentation, so compare days with each other.

**Round-trip time for one user's connections (written for this article).** It joins the network data to the connection rows on CorrelationId. The latest row of each connection supplies the gateway region, transport and session host. The documentation notes that client information can be missing from some connection rows, so some values may be blank:

```kusto
let userConnections =
    WVDConnections
    | where TimeGenerated > ago(1d)
    | where UserName == "userupn"
    | summarize arg_max(TimeGenerated, GatewayRegion, TransportType, SessionHostName) by CorrelationId;
WVDConnectionNetworkData
| where TimeGenerated > ago(1d)
| join kind=inner userConnections on CorrelationId
| summarize MedianRTTms = percentile(EstRoundTripTimeInMs, 50),
            P95RTTms = percentile(EstRoundTripTimeInMs, 95),
            MinBandwidthKBps = min(EstAvailableBandwidthKBps)
    by CorrelationId, GatewayRegion, TransportType, SessionHostName
| sort by P95RTTms desc
```

Bandwidth in this table is in kilobytes per second, not bits.

How it works: the `let` block builds a short list of this user's connections from the last day, with one row per `CorrelationId`. The main part reads the network data rows, matches them to that list, and works out the middle value (`MedianRTTms`) and the 95th percentile (`P95RTTms`) of round-trip time for each connection, plus the lowest bandwidth. The slowest connection is on top. Healthy: median and 95th percentile both low and close to each other, judged against the round-trip table in check 2. Bad: a 95th percentile far above the median, a high median, or a low `MinBandwidthKBps`. Look at which `GatewayRegion`, `TransportType` and `SessionHostName` the bad rows share. If the query returns no rows, there is no network data for that user in the last day. Check the Network category in the diagnostic setting.

**Disconnect names in the error table (written for this article).** The page that names these errors does not say where they are logged, so this searches two columns that exist. Treat an empty result as "not found here", not as "did not happen":

```kusto
let names = dynamic(["ShortpathTransportNetworkDrop", "ShortpathTransportReliabilityThresholdFailure", "ConnectionBrokenMissedHeartbeatThresholdExceeded", "ConnectionFailedClientDisconnect", "ConnectionFailedServerDisconnect"]);
WVDErrors
| where TimeGenerated > ago(7d)
| where CodeSymbolic has_any (names) or Message has_any (names)
| summarize Count = count() by CodeSymbolic, bin(TimeGenerated, 1d)
```

The first line lists the five names as a set (`dynamic` makes a list). The query looks at the last seven days of errors, keeps rows where either column contains one of the names (`has_any`), and counts them for each name and day. Healthy: no rows. Bad: a name that repeats on many days or on the day the user complained. Then look up that name in the table in check 4.

To check whether an error hit other users, the documentation sample swaps in the symbolic code you found:

```kusto
WVDErrors
| where CodeSymbolic =="ErrorSymbolicCode"
| summarize count(UserName) by CodeSymbolic
```

## Fix by cause

Every row comes from the documentation pages listed at the end.

| Cause | How you know | Fix |
|---|---|---|
| Users far from the host region | High round-trip time for one gateway region in Insights | Create session hosts in the Azure region closest to users. Check the Azure network round-trip latency statistics. |
| Firewall, ExpressRoute or other network feature adds delay | High round-trip time on a path that goes through it | Check that network configuration. |
| Saturated or rate-limited network, or unstable local internet | High round-trip time, low available bandwidth, drops | Follow the Remote Desktop network guidelines. Check what is using the bandwidth. |
| Host short of CPU, memory or disk | High input delay, with high CPU, low available memory or slow disk in the same period | Move to a larger VM size. The documentation names storage as a possible limit too. |
| Session stuck on TCP | `TransportType` is `Websocket`, or `avdnettest.exe` fails | Allow outbound UDP. Avoid force tunnelling, double NAT, TCP-based VPNs and packet inspection. |
| Proxy in the path | Sessions on TCP, unstable sessions, slow sign-in | Bypass the proxy for Azure Virtual Desktop traffic. No SSL inspection. No proxy that needs authentication. |
| TURN relay update | A short drop, then an automatic reconnect | The client reconnects within a few seconds. Nothing to fix. |
| Old client version | Drops cluster on one client version | Update the client. |
| Slow logon | Long logon part of time to connect | Check the profile size and share location, the number of Group Policy objects and the distance to the domain controller. |
| Reprompt after lock | Users enter full credentials after a lock | Set the session to disconnect on lock. |
| Connection network data missing | No rows in `WVDConnectionNetworkData` | Check the diagnostic settings and the VM configuration. Check that the session is in use. |

## If you are still stuck

1. Write down the CorrelationId of one bad connection, the user, the session host, the time (UTC) and the transport.
2. In `WVDErrors`, look at `ServiceError`. `false` means the problem is one you can fix. `true` means escalate to Microsoft with the CorrelationId.
3. If the problem is tied to one application or product, the documentation says to contact the team responsible for that product.
4. Otherwise, open an Azure support request and choose Azure Virtual Desktop as the service. Include the CorrelationId.

Next: [Troubleshoot AVD Sign-in Failures: Conditional Access, MFA and Single Sign-on](/azure-virtual-desktop/troubleshoot-sign-in-and-conditional-access/).

## Sources

- [Troubleshoot connection quality](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-connection-quality)
- [Troubleshoot RDP Shortpath](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-rdp-shortpath)
- [Use cases for Insights](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights-use-cases)
