---
title: "Follow a Connection Step by Step: Reverse Connect, RDP Shortpath and Where It Breaks"
seoTitle: "AVD Connection Flow: Reverse Connect and Shortpath"
layout: post.njk
permalink: "/azure-virtual-desktop/follow-a-connection-step-by-step/"
order: 110
part: 10
tags: [avd-series]
deck: "Walk the connection sequence, see which transport carries the session and learn which stage to check first when a connection fails."
description: "Follow an Azure Virtual Desktop connection from sign-in to RDP, see how reverse connect and RDP Shortpath work, and find the stage where yours fails."
---

A user says "it will not connect". That sentence covers at least five different failures. The user may not be able to sign in. The list of desktops and apps (the feed) may be empty. The desktop may be listed but never start. The session may open and then drop. Or it may open and be slow. Each one points at a different stage of the connection.

This article walks through the connection sequence, explains what reverse connect and RDP Shortpath change, and ends with a table that maps a symptom to a stage and a first check. The [architecture article](/azure-virtual-desktop/azure-virtual-desktop-architecture/) gave the short version. Here each step gets its own explanation.

## Key terms

| Term | Meaning |
|---|---|
| Client | The app on the user's device that opens the desktop or app. For example, Windows App. |
| Session host | The Azure virtual machine that runs the user's desktop or apps. |
| RDP | Remote Desktop Protocol. The protocol that carries the screen, keyboard and mouse between the client and the session host. |
| Feed | The list of desktops and apps a user is allowed to open. The client downloads it after sign-in. |
| Token | Proof from Microsoft Entra ID that the user signed in. The client passes it to AVD services. |
| .rdp file | A small connection file the client saves for each desktop or app in the feed. |
| TLS | The encryption used on a network connection. For connections from clients and session hosts to AVD service components, TLS 1.2 is the minimum. |
| Gateway | A Microsoft-run AVD service. The client and the session host both connect out to it. |
| Azure Front Door | A Microsoft network entry service. In the public cloud, the client reaches an AVD gateway through it. |
| Broker | A Microsoft-run AVD service that decides which session host a connection goes to. |
| Persistent channel | A connection the session host keeps open to the AVD service so the broker can reach it. |
| Remote Desktop Agent Loader | A service on the session host that starts when the host starts and sets up the persistent channel. |
| Reverse connect | The session host opens the connection to the service. Nothing connects inbound to the host. |
| TCP and UDP | The two ways data crosses the network here. TCP is a reliable, ordered connection and is the base transport through the gateway. UDP sends data without confirming each piece. RDP Shortpath uses UDP. |
| Transport | The network path that carries the RDP session: TCP through the gateway, or UDP. |
| RDP Shortpath | An optional direct UDP path between the client and the session host. The gateway is not on that path. |
| STUN | A service that tells a device its public address, so two devices can try to connect directly. |
| TURN | A relay service used when a direct UDP path is not possible. |
| ICE | A method that tries the possible network paths between two devices, using STUN and TURN, and picks one that works. |
| Conditional Access | Microsoft Entra rules that decide whether a sign-in is allowed, for example by requiring multifactor authentication. |
| Log Analytics | An Azure service that stores monitoring data and lets you query it. |
| NAT | Network address translation. A device translates private addresses to a public one. Double NAT and carrier-grade NAT are configurations to avoid for RDP Shortpath on public networks. Carrier-grade NAT is NAT done by an internet provider for many customers at once. |
| Listener | A service on the session host that waits for incoming connections on a port. |
| Force tunneling | Sending all client traffic, including internet traffic, through a VPN. |
| Teredo | A Windows feature that gives IPv4-only networks extra paths for UDP. |
| Managed network | A private connection between client and host, such as ExpressRoute private peering or a VPN. |
| Public network | A path where the traffic crosses the internet. |

## Before anyone connects

One thing has already happened before a user clicks anything. When the session host starts, the Remote Desktop Agent Loader on the host sets up a persistent communication channel to the AVD service. This channel is a bus for service messages between the session host and the AVD infrastructure, and the broker uses it to initialize a connection (step 9 in [Understanding Azure Virtual Desktop network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity#session-host-communication-channel)). The host opens the channel outward, so no inbound port is needed on the host.

It also means that a session host that cannot reach the service looks fine in Azure (the VM is running) but cannot take a connection. The [failure article](/azure-virtual-desktop/how-azure-virtual-desktop-fails/) covers the host status values that show this.

## The twelve steps

A connection has twelve numbered steps. The table follows those steps. The third column says what usually goes wrong at that point.

| Step | What happens | What can go wrong |
|---|---|---|
| 1 to 2 | The client signs the user in to Microsoft Entra ID and receives a token. | Sign-in is blocked or interrupted: wrong account, Conditional Access, or a blocked sign-in endpoint. |
| 3 to 6 | The client passes the token to the feed service, which validates it and returns a signed connection configuration. The client stores that configuration in .rdp files. | An empty or partial feed. Often an assignment, workspace or application group type problem (see the [rules article](/azure-virtual-desktop/host-pool-application-group-workspace-rules/)). |
| 7 | The client opens a TLS connection to a gateway. In the public cloud the entry point is Azure Front Door, and the gateways are grouped by response time. | A proxy, firewall or inspection device on the client side breaks or rewrites the TLS connection. |
| 8 | The gateway asks the broker to orchestrate the connection. | No available session host, or a host in the wrong status. |
| 9 | The broker uses the persistent channel to tell the session host a connection is coming. | The host is running but its agent has no channel. The host status in the portal is the place to look. |
| 10 to 11 | The session host opens its own outbound TLS connection to the same gateway, and the gateway relays between the two. | The host's outbound path is blocked. The user waits and then gets a generic error. |
| 12 | The RDP handshake starts. | Connection opens but sign-in to Windows is slow or fails, which is a Windows or profile problem and not a connection problem. |

The diagram shows the same sequence with the same step numbers. The panel at the bottom says where a connection stops for each group of steps.

![A user device on the left. Orange arrows go to Microsoft Entra ID for steps one and two, to the feed subscription service for steps three to six, and to the gateway service, entered through Azure Front Door, for step seven. A blue arrow from the gateway to the broker is step eight. A dashed blue arrow from the broker down to the session host is step nine, the persistent channel. A green arrow from the session host to the gateway is steps ten and eleven. A label marks step twelve, the RDP handshake. A dashed green line goes directly from the user device to the session host and is labeled as optional RDP Shortpath. A panel at the bottom lists where a connection stops for each group of steps.](/img/avd/AVD-Post-10-Connection-Steps-v3.png)

*The twelve steps of a connection and where a connection stops. Source: [Understanding Azure Virtual Desktop network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity).*

## What reverse connect gives and what it costs

Reverse connect is the base transport. The session host connects out, so the host needs no inbound port open to the internet for this path.

**Gain:** reverse connect uses no TCP listener for incoming RDP connections ([network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity#reverse-connect-transport)), and the [required FQDNs and endpoints](https://learn.microsoft.com/en-us/azure/virtual-desktop/required-fqdn-endpoint#session-host-virtual-machines) page says all session host entries are outbound and you don't need to open inbound ports for AVD.

**What to plan for:** the host's outbound access becomes a hard requirement. If a firewall, proxy or route table blocks the endpoints the host needs, the host cannot hold its channel or open its connection, and no inbound rule will fix it. The [networking article](/azure-virtual-desktop/plan-avd-networking/) shows a worked example, and the [required connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) lists the endpoints and the proxy rules.

Two further details help with troubleshooting. By default the RDP certificate on the session host is self-generated by the operating system, and certificates from a certification authority are not supported at this time. And the connection uses TLS 1.2 as a minimum and can use TLS 1.3 if both sides support it.

The [proxy guidelines](https://learn.microsoft.com/en-us/azure/virtual-desktop/proxy-server-support#dont-use-ssl-termination-on-the-proxy-server) say not to use SSL termination, because SSL inspection can stop the agent working. A device that rewrites TLS in the middle could therefore break step 7 or steps 10 to 11. What the user sees depends on which connection the device breaks, so test it before you rely on an inspection device.

## RDP Shortpath: the optional direct path

RDP Shortpath adds a UDP path. When it is available, the session moves from the gateway relay to a direct or relayed UDP connection. There are four ways to get one. A managed network is a private connection such as ExpressRoute or a VPN. A public network is the internet.

| Option | What it needs | Notes |
|---|---|---|
| Managed networks, direct | A managed network (private connection) between client and host. A listener on the session host, UDP port 3390 by default. | The listener is turned on with Intune or Group Policy. An inbound rule on that port is needed. |
| Managed networks, with ICE and STUN | A managed network (private connection). The listener is not enabled. | ICE and STUN find usable addresses and a dynamic port, so no inbound port is required on the host. |
| Public networks, STUN | Outbound UDP from client and host so they can find each other's public address. | Works with no extra configuration if the networks allow it. |
| Public networks, TURN | Outbound UDP to the relay range, 51.5.0.0/16 on UDP 3478 (public cloud). | Used when a direct path is not possible. The relay can drop briefly during relay updates, and the client reconnects. |

Other details:

- The session host subnet needs outbound UDP from 1024 to 65535. The default range used is 49152 to 65535.
- Both the client and the host must have UDP enabled, which is the default.
- The host pool network setting can allow or disallow each option (managed private, direct, public, relay). When settings disagree, the most restrictive one wins.
- When both a managed and a public path are available, the client uses whichever is established first. This is called the first-found algorithm.
- If UDP is blocked, the connection falls back to TCP through the gateway. The user still connects.
- A TURN relay is chosen by the physical location of the client. If the client is far from a relay, the UDP connection might fall back to TCP. The [RDP Shortpath page](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-shortpath) lists the regions.

That last point is the one that surprises people. Blocking UDP does not stop the connection. The session stays on TCP through the gateway, so nothing visibly fails and Shortpath is simply absent, which is easy to miss. UDP gives better reliability and more consistent latency, so the cost is a less consistent session, not an outage.

For Shortpath on public networks, Microsoft recommends avoiding force tunneling, double NAT or carrier-grade NAT, cloud-based packet inspection and TCP-based VPNs. It recommends enabling IPv6 or Teredo. It also asks you to tell users not to turn off UPnP on their home routers. Some network configurations lower the success rate of the direct connection. Test from your users' real networks.

**Azure Government.** STUN is available in Azure Government. The pages on RDP Shortpath and on configuring it describe TURN there differently: the first lists a relay range (20.140.236.0/22) and the second says TURN is available only in the public cloud. Confirm TURN support before you plan it for Azure Government.

## How to tell which transport is in use

Do not guess. There are three ways to look.

1. **In the client.** In a client that has it (see the [client article](/azure-virtual-desktop/choose-the-avd-client/)), the Connection Information dialog shows the transport. It reads "UDP (Private Network)" for a managed path, "UDP" for a STUN path and "UDP (Relay)" for a TURN path. If it shows none of these, the session is probably not using UDP. Confirm with the other two checks.
2. **On the session host, in the event log.** Event ID 135 in the `RemoteDesktopServices-RdpCoreCDV/Operational` log records the UDP transport.
3. **In Log Analytics.** The connection data records the transport for each connection. The column is called `UdpUse` in the [configure RDP Shortpath](https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-rdp-shortpath#verify-rdp-shortpath-is-working) steps. Value 1 is Shortpath for managed networks, 2 is public networks with STUN, 4 is public networks with TURN, and any other value is TCP. The [WVDConnections table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/wvdconnections) uses `TransportType`, with the values Shortpath, TURN and Websocket. Check the column names in your own workspace before you build a query.

If the transport is TCP when you expected UDP, Microsoft lists checks for the Windows client (the `fClientDisableUDP` setting), for the session host (a transport selection check) and a command-line tool, `avdnettest.exe`, that checks whether a client can reach the STUN and TURN servers and what type of NAT it is behind. Follow the steps on the configuration page for each.

## Where connections break

Use this table as a first-check list, not a proof of cause.

| Symptom | Stage | First check |
|---|---|---|
| User cannot sign in | Steps 1 to 2 | Sign-in logs in Microsoft Entra ID. Look for a Conditional Access result. |
| Signed in, feed empty | Steps 3 to 6 | The user's assignment on the application group, and that group is in a workspace. The [rules article](/azure-virtual-desktop/host-pool-application-group-workspace-rules/) has the order of checks. |
| Desktop listed, spinner, then error | Steps 7 to 9 | Session host status and health checks in the portal. Is any host available? |
| Fails after a long wait | Steps 10 to 11 | Outbound access from the session host. Check the host against the required endpoints. |
| Opens, then drops after a while | After step 12 | Network quality, an inspection device, or TURN relay updates. Look at the transport in use. |
| Opens, but slow to reach the desktop | After step 12 | Windows sign-in time and profile loading, before blaming the network. |
| Opens, but laggy or choppy | After step 12 | Which transport. TCP through the gateway is the fallback when UDP is blocked. |

For host-side endpoint checks, there are two tools. The Agent URL Tool, `WVDAgentUrlTool.exe` ([Check access to required FQDNs and endpoints](https://learn.microsoft.com/en-us/azure/virtual-desktop/check-access-validate-required-fqdn-endpoint)), checks the agent's required addresses from the host.

It needs .NET 4.6.2 and a recent agent version, the tool and its configuration file must be in the same folder, and it does not verify wildcard entries. Event ID 3701 in the `WVD-Agent` log under Application lists the region-specific addresses the agent tried to reach ([Required FQDNs and endpoints](https://learn.microsoft.com/en-us/azure/virtual-desktop/required-fqdn-endpoint#session-host-virtual-machines), tip under the tables).

## Common mistakes

- **Opening inbound ports on the session host for the base connection.** Reverse connect does not need them. They add exposure and fix nothing.
- **Turning TURN off.** Keep TURN enabled unless you disable it for troubleshooting. Without it, more connections fall back to TCP.
- **Blocking UDP and calling it secure.** The session still works over TCP, and Shortpath offers the same security as the TCP path. You have only removed the direct path and the more consistent latency.
- **Putting a TLS-inspecting proxy in front of the AVD endpoints.** The [proxy guidelines](https://learn.microsoft.com/en-us/azure/virtual-desktop/proxy-server-support) say not to use SSL termination. It replaces the service certificates, adds sign-in time and can stop the agent working. They also say a proxy that is the only path forces RDP over TCP instead of UDP. See the [required connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) for the proxy rules.
- **Testing from one location and generalizing.** Shortpath depends on the client's network. A home user behind carrier-grade NAT can behave differently from an office user.
- **Reading "VM running" as "host ready".** A running VM with no persistent channel cannot take a connection.

## How to validate your understanding of the path

Run these checks in a test environment.

1. Connect from a managed network and from a home network. Note the transport shown in Connection Information for each.
2. Block outbound UDP for a test client. Confirm the user still connects and note what changed.
3. Stop the agent on a test host. Note what the host status shows and what the user sees.
4. Run the Agent URL Tool on a host and compare its output with the event 3701 list.

Next: [Choose the Session Host Operating System and Licensing](/azure-virtual-desktop/session-host-operating-system-and-licensing/).

## Sources

- [Understanding Azure Virtual Desktop network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity)
- [RDP Shortpath](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-shortpath)
- [Configure RDP Shortpath](https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-rdp-shortpath)
