---
title: "Plan Bandwidth, Latency and Quality of Service for Azure Virtual Desktop"
seoTitle: "AVD Bandwidth, Latency and QoS: Plan for a Fast Session"
layout: post.njk
permalink: "/azure-virtual-desktop/plan-bandwidth-latency-and-quality-of-service/"
order: 123
part: 23
tags: [avd-series]
deck: "Learn what uses bandwidth in a remote session, which round-trip times the documentation treats as good or poor, what Quality of Service can and cannot do, how Teams is set up, and where to look when a user says the session is slow."
description: "What the Azure Virtual Desktop documentation says about bandwidth, latency and Quality of Service, where QoS applies, how Teams is set up, and which logs show what a connection saw."
---

A user says the session is slow. The picture stutters, typing lags behind the keys, or a video call breaks up. Those complaints can come from the network between the user's device and the session host (the virtual machine that runs the session), or from the session host itself. The documentation puts it this way: graphical quality during a connection is affected by many factors, such as network configuration, network load or virtual machine load.

This article covers the network part and shows how to tell it from the others. It explains bandwidth, round-trip time, packet loss and jitter, what the documentation says about each, what Quality of Service (QoS, a way to give real-time traffic priority) can and cannot do, which settings decide whether UDP (a fast transport that does not resend lost packets) is used, how Microsoft Teams is set up, and which logs show what a connection saw.

The terms are defined in Key terms below. Which transport carries a session (TCP through the gateway, or UDP with RDP Shortpath) and how a connection is built are covered in [the connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/). Sizing the session hosts is covered in [the host pool planning article](/azure-virtual-desktop/plan-your-host-pools/).

## Key terms

| Term | Meaning |
|---|---|
| Remote Desktop Protocol (RDP) | The protocol that carries the remote session between the user's device and the session host. |
| Session host and host pool | A session host is a virtual machine that runs the user's session. A host pool is a group of session hosts managed together. |
| TCP and UDP | The two transport types. TCP resends lost packets and delivers them in order. UDP does not guarantee delivery on its own, which suits real-time traffic. RDP Shortpath adds its own rate control on top of UDP. |
| Gateway | The Azure Virtual Desktop service component that, by default, carries the session over TCP when no direct UDP path is used. The connection article explains it. |
| Reverse connect transport | The documentation's name for the default path, in which the session host and the client both connect outward to the service, and the session runs through the gateway over TCP. |
| Bandwidth | How much data a network link can carry in a given time. It is measured in kilobits per second (Kbps) or megabits per second (Mbps). |
| Round-trip time (RTT) | How long a network request takes to go from the user's device to the session host through the network, and back again. The documentation uses the words latency and round-trip time interchangeably. |
| Packet loss | Packets (the small pieces that data is sent in) that are dropped on the way. With TCP they are sent again, which takes extra time. |
| Jitter | Variation in the time between packets arriving. It can cause visual and audio glitches. |
| Frame rate and resolution | How many pictures per second are sent, and how large each picture is. A higher frame rate or a higher resolution needs more bandwidth. |
| Graphics mode | The way RDP encodes the picture. The documentation compares the default mode with the H.264/AVC 444 mode. |
| ICE, STUN and TURN | Methods that help two devices find a UDP path when a direct one is not possible. ICE is the process that tries the possible paths and picks one. STUN helps a device learn its public address. TURN relays the traffic through a server in Azure. The connection article covers them. |
| RDP Shortpath for managed networks | A direct UDP path between a client and a session host over a private connection, such as ExpressRoute private peering (a private link from your network to Azure) or a VPN (a private, encrypted tunnel over another network). By default the session host listens on UDP port 3390. The connection article explains it in full. |
| Quality of Service (QoS) | A way to tell the network which traffic to handle first, so real-time traffic such as RDP is not stuck behind traffic that can wait. |
| DSCP (Differentiated Services Code Point) | A marker in the header of an IP packet that says what type of traffic it is. Routers and other network devices can be set up to read the marker and place the packet in a higher-priority queue. |
| Expedited Forwarding (EF) | A traffic class, marked with DSCP value 46, that network devices can send first. |
| Throttle rate | A limit on how much outbound data RDP sends for each session. |
| Media optimization for Teams | A setup that sends Teams calling and meeting media to the user's own device. The documentation describes it as redirecting calling and meeting functionality to the user's local device. It uses a component called SlimCore or the WebRTC Redirector Service. |
| Input delay | How long a user's input waits in a queue on the session host before the application handles it. It is not a network round-trip measure. Azure Virtual Desktop Insights shows it for each session host. |
| Connection Information | A dialog in Windows App or the Remote Desktop client that shows which transport the session uses. |
| Gateway region | The Azure region of the gateway that a connection uses. Insights groups round-trip time by it. |
| NAT (network address translation) | A router feature that lets many devices on a home or office network share one public address. It can block or change UDP paths. |
| Log Analytics | The Azure service that stores and queries logs. Azure Virtual Desktop can send its diagnostic data there. |
| Azure Virtual Desktop Insights | A set of dashboards in the Azure portal that shows connection, session host and client data for a host pool. |

## What decides how a session feels

Three questions come first. The diagram below numbers them the same way:

1. Is the path long (round-trip time)?
2. Is the path full or lossy (bandwidth, packet loss, jitter)?
3. Is the virtual machine busy?

(This three-way split is my judgement, not a list from the documentation.) The next sections take bandwidth and then round-trip time, then packet loss and QoS, then Teams. The last sections cover the logs and the checks that tell the three causes apart.

![A diagram of a user's device on the left and a session host on the right are joined by a box called the network path, which holds two checks: how long the path is (round-trip time) and how full it is (bandwidth, packet loss, jitter). A third check, how busy the host is (CPU, memory and input delay), is attached to the session host. Below, a box called Where to look has four items: the Connection Information dialog on the client, the connection network data table and the connection graphics data table in Log Analytics, and Azure Virtual Desktop Insights. A note says QoS and the throttle rate apply only to the RDP Shortpath for managed networks path.](/img/avd/AVD-Session-Quality-Checks.svg)

*Source: based on [RDP bandwidth requirements](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-bandwidth), [Quality of Service for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-quality-of-service-qos) and [Troubleshoot connection quality](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-connection-quality). The documentation has no single diagram of these checks, so the layout is simplified.*

## Bandwidth

### What uses it

RDP carries many kinds of data, and the amount depends on what the user does. A user can work with plain text for most of a session and use very little bandwidth, then print a large document to a local printer, and that print job can use a lot. The documentation gives the 200-page printout as its own example. It gives these starting points for what to expect:

| Type of data | Direction | How to estimate |
|---|---|---|
| Remote graphics | Session host to client | See the graphics numbers below. |
| Heartbeats (small keep-alive messages) | Both ways | About 20 bytes every 5 seconds. |
| Input | Client to session host | Based on user activity. Less than 100 bytes for most operations. |
| File transfers | Both ways | The data is compressed in bulk, so use `.zip` compression rates as an approximation. |
| Printing | Session host to client | Depends on the driver. The data is compressed in bulk, so use `.zip` rates as an approximation. |

Graphics are the largest part. RDP sends the whole desktop picture, composed on the server. The page says an uncompressed 1080p picture is about 8 Mb, and that showing it at 30 frames per second would need about 237 Mbps. The units look like megabytes, not megabits (judgement), but the point stands: raw video is far too large to send. RDP uses several techniques to cut that down: frame rate optimization, screen content classification, content-specific codecs, progressive image encoding and client-side caching. Because of them:

- Text, window elements and solid color areas use the least bandwidth. Natural images use the most, although caching reduces it.
- Only the parts of the screen that changed are sent. With no visible change, nothing is sent, and an idle session needs very little.
- When the client window is minimized, no graphical updates are sent from the session host.
- Video and other high-frame-rate content is the largest contributor to bandwidth use.
- A higher resolution or a higher frame rate raises the requirement.

RDP also does not work to a fixed limit. It keeps measuring the available bandwidth and the round-trip time, then chooses the graphics encoding options and shares bandwidth among the channels. It uses the full pipe when the pipe is free and backs off when the network is needed for something else.

### Two sets of numbers

The documentation has two sets of numbers, and they answer different questions.

The Remote Desktop network guidance page gives the minimum bandwidth it recommends for a smooth experience, for workload types it names Light, Medium, Heavy and Power. It says the recommendations apply to networks with less than 0.1% loss, and however many sessions the virtual machines host.

| Workload type | Minimum recommended bandwidth |
|---|---|
| Light | 1.5 Mbps |
| Medium | 3 Mbps |
| Heavy | 5 Mbps |
| Power | 15 Mbps |

| Display resolution at 30 frames per second | Minimum recommended bandwidth |
|---|---|
| About 1024 × 768 | 1.5 Mbps |
| About 1280 × 720 | 3 Mbps |
| About 1920 × 1080 | 5 Mbps |
| About 3840 × 2160 (4K) | 15 Mbps |

The bandwidth requirements page gives measured estimates for one monitor at 1920 × 1080, in the default graphics mode and in H.264/AVC 444 mode:

| Scenario | Default mode | H.264/AVC 444 mode |
|---|---|---|
| Idle | 0.3 Kbps | 0.3 Kbps |
| Microsoft Word | 100–150 Kbps | 200–300 Kbps |
| Microsoft Excel | 150–200 Kbps | 400–500 Kbps |
| Microsoft PowerPoint | 4–4.5 Mbps | 1.6–1.8 Mbps |
| Web browsing | 6–6.5 Mbps | 0.9–1 Mbps |
| Image gallery | 3.3–3.6 Mbps | 0.7–0.8 Mbps |
| Video playback (half the screen) | 8.5–9.5 Mbps | 2.5–2.8 Mbps |
| Video playback (full screen) | 7.5–8.5 Mbps | 2.5–3.1 Mbps |

The second table shows that the graphics mode changes the numbers in both directions: H.264/AVC 444 mode uses less for graphically rich content and more for Word and Excel. The pages do not say how the two sets relate. The measured browsing and video figures in the default mode are above the 5 Mbps minimum for 1080p, so one reasonable reading (judgement) is to treat the minimums as a floor, not as a sizing figure, and to measure real sessions.

Neither page gives a formula for a site with many users. One way to use the numbers (judgement, not a documented method) is to take the figure that fits what your users do, multiply it by the number of users who are connected at the same time over the same link, and then check the result against real measurements. The documentation says the best way to understand bandwidth requirements is to monitor real user connections, with the built-in performance counters or with the network equipment. It also says to load test scenarios such as voice and video conferencing, real-time communication and 4K video, with a simulation tool such as Login VSI.

### Limiting bandwidth with a throttle rate

In most cases there is no need to limit bandwidth, and limiting can hurt the user experience. The documentation names two cases where it can make sense: a constrained network, and a leased network that is charged for the traffic. The limit is a throttle rate set in a QoS policy on the session host. It works only on the RDP Shortpath for managed networks transport. It is not supported for reverse connect transport. To set a throttle rate instead of a DSCP marker, replace `-DSCPAction 46` with `-ThrottleRateActionBitsPerSecond 10mb` in the QoS policy command shown later. The bandwidth requirements page shows that form.

## Latency

### What the pages say

The documentation gives several round-trip time numbers, and they are not the same:

| Page | What it says about round-trip time |
|---|---|
| Prerequisites for Azure Virtual Desktop | Round-trip time from the client's network to the Azure region that holds the host pools should be less than 150 ms. |
| Troubleshoot connection quality | Up to 150 ms should not affect an experience that does not involve rendering or video. Between 150 ms and 200 ms should be fine for text processing. Above 200 ms might affect the experience. |
| Use cases for Azure Virtual Desktop Insights | Ideal interaction times need latency generally below 100 ms, and a session broadly becomes low quality over 200 ms. |
| Remote Desktop network guidance | Assistive technology, such as Narrator in the remote session, needs a round-trip time of 20 ms or better. |
| [Optimal provisioning of Cloud PCs (Windows 365)](https://learn.microsoft.com/en-us/windows-365/enterprise/optimal-provisioning-cloud-pc#reliable-network-connectivity-for-cloud-pc-performance) | For Windows 365, the page says RDP can accommodate latencies of up to 200 ms. |

The pages do not reconcile these figures, and this article does not pick one. The troubleshooting page does separate text work from rendering and video, so one reasonable reading (judgement) is to hold graphics and video users to the stricter figures and text users to the looser ones.

### Reducing round-trip time

The documentation lists four steps:

- **Move the session hosts closer to the users.** Where possible, users should connect to virtual machines in the Azure region nearest to them. (The prerequisites page adds that the virtual network for the session hosts must be in the same region as the session hosts.)
- **Check the network configuration.** Firewalls, ExpressRoute and other network features can affect round-trip time.
- **Check what is using the bandwidth.** If the available bandwidth is too low, the network settings might need to change to follow the network guidelines.
- **Check the session host.** Look at CPU use and available memory on the virtual machine. If CPU use is too high or memory too low, the virtual machine size or storage might be too small for the workload.

To choose a region, the documentation points to the Azure network round-trip latency statistics and to the Azure Virtual Desktop experience estimator, and says the region can affect the experience as much as network conditions. The statistics page lists the median (P50) round-trip time between Azure regions over 30 days. Each value is for one direction, so A to B can differ from B to A. The page says to expect an update every 6 to 9 months. The troubleshooting page recommends reviewing them every two to three months, as the service rolls out to new areas.

## Packet loss, jitter and Quality of Service

When a path is full or poor, packets can arrive at uneven intervals (jitter), some can be dropped (packet loss), and round-trip time can grow. The QoS page explains that without QoS, traffic is handled in one queue, so RDP traffic can wait behind traffic that could easily have waited, and compares QoS to carpool lanes with separate queues. It recommends using QoS first and adding bandwidth only where necessary, because adding bandwidth is often cost-prohibitive. The page says a small business with few users might not need QoS, but that it should be helpful even there.

### Where QoS applies

QoS has limits that decide whether it will help your users:

- **Only on one transport.** QoS policies are supported for RDP Shortpath for managed networks. They are not supported for reverse connect transport. One reasonable reading (judgement) is that a session on TCP through the gateway gets no benefit from a QoS policy.
- **End to end.** QoS works as expected only when it is implemented on every link between clients and session hosts. If a user signs in from a remote location, you can prioritize traffic only inside your managed network. A VPN can give a remote location a managed connection, but it adds packet overhead and delay to real-time traffic.
- **A short path.** The shortest path to the session host is best, and obstacles such as proxies or packet inspection devices are not recommended.
- **Matching network devices.** The session host marks the packets. Routers and other network devices must be set up to read the marks and queue the traffic. The page says the devices can be configured this way. That part is for your network team.

### How it is set up

The [QoS page](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-quality-of-service-qos) sets QoS in a Group Policy Object, or with PowerShell on the session host. The policy marks the Remote Desktop traffic with DSCP value 46, which maps to the Expedited Forwarding (EF) class. It applies to the `svchost.exe` application, to UDP, and to source port 3390, which is the default port of the RDP Shortpath listener.

```powershell
New-NetQosPolicy -Name "RDP Shortpath for managed networks" -AppPathNameMatchCondition "svchost.exe" -IPProtocolMatchCondition UDP -IPSrcPortStartMatchCondition 3390 -IPSrcPortEndMatchCondition 3390 -DSCPAction 46 -NetworkProfile All
```

A Group Policy version takes effect after the policy refreshes on the session hosts, which `gpupdate /force` forces. The pages do not say what to match if you change the listener port, or if the connection does not use the listener. The example matches the listener port, so it applies only when the RDP Shortpath listener is enabled on the session host (see the connection article). Managed networks with ICE/STUN use a dynamic port, so this policy would not match them (judgement, based on the documented port match).

## Settings that decide whether UDP is used

The connection article covers how the UDP paths work, which ports to allow and how to verify the transport. These settings decide whether a session can use UDP at all. QoS and the throttle rate need the managed-network path in particular, which is covered by the first two switches below.

- **Windows settings can turn UDP off.** UDP and TCP are both on by default. A policy named "Select RDP transport protocols" on the session host, or "Turn Off UDP On Client" on a Windows client, can change that. The configuration page gives PowerShell checks for both, and says a value of "Use only TCP" is likely to have come from an Intune policy or Group Policy.
- **The host pool has its own switches.** Under Networking in the host pool, four RDP Shortpath options (managed networks, managed networks with ICE/STUN, public networks with ICE/STUN, and public networks through TURN) can each be Default, Enabled or Disabled. ICE, STUN and TURN are defined in Key terms. Default means Enabled. Where the host pool and the session host disagree, the most restrictive setting is used. For example, if the host pool disables RDP Shortpath for managed networks, it does not work even when the listener is on.
- **Keep TURN on, and mind the port range.** The configuration page says to keep the TURN option enabled unless you are troubleshooting. The ports for ICE, STUN and TURN, and how to narrow them, are covered in [the connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/).

## Microsoft Teams

Teams calls and meetings are real-time traffic that depends on delay, so I treat them as their own setup (judgement). With media optimization, the documentation says calling and meeting functionality is redirected to the user's local device. The documentation lists what this needs:

- **A redirect component.** New Teams can use either SlimCore or the WebRTC Redirector Service, and the page says to also install the WebRTC Redirector Service so users can fall back to it, for example when they move to a device that does not support the newer setup. Classic Teams uses the WebRTC Redirector Service. SlimCore comes with new Teams and the client.
- **The latest Microsoft Visual C++ Redistributable.** It is required on the client device and on the session hosts for Windows.
- **The WebRTC Redirector Service on each session host.** It is installed from an MSI file.
- **A registry value on each session host.** `IsWVDEnvironment` set to 1 under `HKLM\SOFTWARE\Microsoft\Teams`.
- **Supported setups.** Windows 10 or 11 multi-session or Enterprise on the session host (N and KN editions are not supported), and one of the supported clients. For a pooled host pool, Teams is installed per machine. With FSLogix (the profile container software) and new Teams, FSLogix 2210 hotfix 3 or later.
- **Classic Teams dates.** The [Teams on Azure Virtual Desktop page](https://learn.microsoft.com/en-us/azure/virtual-desktop/teams-on-avd) says that for classic Teams in VDI environments on Windows endpoints, end of support was October 1, 2026 and end of availability is April 1, 2027, after which the new Teams app is required. Check these dates against the Teams pages before you plan.

To check that it works, restart Teams in a remote session and open About Teams. The banner reads "AVD SlimCore Media Optimized" or "AVD Media Optimized" when optimization is loaded. "AVD Media not connected" means quit Teams and try again. If media optimization is not used, the documentation lists RDP properties that redirect the microphone and camera instead: `audiocapturemode:i:1`, `audiomode:i:0` and `camerastoredirect:s:*`. Do not put a proxy in the path of Teams media optimization traffic. [The connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) says it is not supported.

## Measure what a connection saw

Four sources show what a connection experienced. None of the pages used for this article names a built-in view of packet loss or jitter, so for those two use your network monitoring tools (judgement). The first source is on the client, and the others are in Azure.

### Connection Information on the client

It shows the transport: UDP (Private Network), UDP, or UDP (Relay). The connection article covers it.

### The connection network data table

This Log Analytics table is called NetworkData in the documentation, and the sample queries use the name `WVDConnectionNetworkData`. Choose Network Data Logs in the host pool's diagnostic settings. Data can take up to 15 minutes to appear. Send the host pool's diagnostics to a Log Analytics workspace first. The service writes a record every two minutes during an active session, with the estimated available bandwidth, the estimated round-trip time and the correlation ID of the connection, so a record can be tied to a connection.

The round-trip time in this table is measured the same way for TCP and UDP. The page lists this as an advantage over the RemoteFX network performance counters (older Windows counters for remote sessions). Bandwidth in this table is in kilobytes per second (column `EstAvailableBandwidthKBps`), not bits, and is an average over the interval. Multiply by 8 (simple arithmetic) to compare it with the Mbps figures in this article.

### The connection graphics data table (preview)

The service writes a record only when the metrics are rated Okay or Bad, and at most once every two minutes. Each record includes the end-to-end delay, the encoding delay on the server, the decoding and rendering delay on the client, the percentage of frames dropped by the client, the network and the server, the available bandwidth and the round-trip time. The thresholds are:

| Metric | Bad | Okay | Good |
|---|---|---|---|
| Dropped frames at a frame rate under 15 per second | Over 15% | 10%–15% | Under 10% |
| Dropped frames at a frame rate over 15 per second | Over 50% | 20%–50% | Under 20% |
| End-to-end delay per frame | Over 300 ms | 150–300 ms | Under 150 ms |

The table is not filled regularly through a session, so the page says it is not a reliable baseline. It also covers only the graphics stream. It does not record slowness from an application or from the virtual machine's CPU or storage, so it should be read with the virtual machine's own metrics.

### Azure Virtual Desktop Insights

The Connection Performance tab shows round-trip time by gateway region (the Azure region of the gateway), with the median (the middle value) and the 95th percentile (the value that 95% of measurements stay below). The 95th percentile is often much higher than the median, which means some users have periods of higher latency. The Host Performance tab shows user input delay for each session host, and the page says it should ideally be below 100 ms. If it is higher, the page suggests looking at CPU, memory, disk timing and disk queue length for the same period.

## Work through a slow-session report

This table maps a report to the first thing to look at. This mapping is my judgement, built on the pages. It is not a table from the documentation.

| What the user reports | Look first at | Why |
|---|---|---|
| Fine in the office, slow at home | The transport in Connection Information | UDP might be blocked at home or the user might be on TCP through the gateway. See the connection article. |
| Slow for everyone in one place | Round-trip time by gateway region in Insights, then the path to the Azure region | Distance, VPN, proxy or firewall in the path can add delay. |
| Picture stutters or freezes, but typing is fine | The connection network data and graphics data tables | Look at available bandwidth and at which of the client, network and server dropped frames. |
| Typing lags | Input delay by host in Insights, then CPU, memory and disk for the same period | The page names input delay above 100 ms as the signal to check the host's resources. |
| Slow only at busy times on a shared link | Bandwidth on the link, and whether QoS can apply to the users' transport | QoS applies only to the RDP Shortpath for managed networks path. |
| Teams calls are poor | The About Teams banner | The banner shows whether media optimization is loaded. See the Teams section for what to do if it is not. |

## Where the documentation differs

| # | Topic | What the pages say | How this article treats it |
|---|---|---|---|
| 1 | Acceptable round-trip time | 150 ms (prerequisites), 150–200 ms for text and over 200 ms as risky (troubleshooting), below 100 ms ideal and over 200 ms low quality (Insights), 20 ms for assistive technology, and up to 200 ms for Windows 365. | Not resolved. All the figures are shown. |
| 2 | Bandwidth per user | Recommended minimums on the network guidelines page, and measured estimates on the bandwidth requirements page. They use different bases and the pages do not say how they relate. | Both are shown. They are not combined. |
| 3 | QoS when the port is not 3390 | The QoS pages show only a policy that matches source port 3390. | The pages do not say what to match for another port or for a connection that does not use the listener. |

## Common mistakes

- **Expecting QoS or a throttle rate to help every session.** The pages support them for RDP Shortpath for managed networks and say they are not supported for reverse connect transport.
- **Using one latency number for every user.** Text, graphics and assistive technology work have different figures in the documentation.
- **Testing from one network.** An office test says little about home users, who can differ in NAT (see Key terms), VPN and UDP rules.
- **Treating the connection graphics data as a baseline.** It is written only when quality drops and it ignores the virtual machine.

## How to check a setup

1. Find the UDP switches. Check the host pool's RDP Shortpath networking settings, the "Select RDP transport protocols" policy on the session hosts and the "Turn Off UDP On Client" policy on clients.
2. Connect from a typical user network. In Connection Information, confirm the transport is UDP. For a managed network, confirm it says UDP (Private Network).
3. Check Log Analytics, after the host pool's diagnostics are sent to a workspace. Confirm that connection network data arrives every two minutes for an active session.
4. Open Insights, once it is set up for the host pool. Note the median and 95th percentile round-trip time by gateway region, and the median input delay by host.
5. If you set QoS, confirm the policy exists with `Get-NetQosPolicy`, then test with a managed-network user, and compare with a user on TCP.
6. For Teams, restart the app in a remote session and read the About Teams banner.
7. Run a load test with real workloads before you decide on link sizes or QoS.

Next: [Choose Session Host VM Sizes: Compute, GPU, Disks and Quota](/azure-virtual-desktop/choose-session-host-vm-sizes/).

## Sources

- [RDP bandwidth requirements](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-bandwidth)
- [Quality of Service for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-quality-of-service-qos)
- [troubleshoot connection quality](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-connection-quality)
- [Prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)
- [Network guidelines](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/network-guidance)
- [Use cases for Azure Virtual Desktop Insights](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights-use-cases)
- [RDP Shortpath](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-shortpath)
- [Configure RDP Shortpath](https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-rdp-shortpath)
- [Use Microsoft Teams on Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/teams-on-avd)
- [Azure network round-trip latency statistics](https://learn.microsoft.com/en-us/azure/networking/azure-network-latency)
- [Connection latency](https://learn.microsoft.com/en-us/azure/virtual-desktop/connection-latency)
- [Collect and query connection quality data](https://learn.microsoft.com/en-us/azure/virtual-desktop/connection-quality-monitoring)
