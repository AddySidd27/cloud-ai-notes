---
title: "Required Connectivity for Azure Virtual Desktop: Endpoints, Proxies, DNS and Private Link"
seoTitle: "AVD Required Endpoints, Proxies and DNS"
layout: post.njk
permalink: "/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/"
order: 116
part: 16
tags: [avd-series]
deck: "Know what the service must reach, why there is no IP allow list, how proxies and DNS affect it and what Private Link changes."
description: "Understand the network access Azure Virtual Desktop requires: endpoints, service tags, platform addresses, proxy rules, DNS and what Private Link changes."
---

"Open the firewall for AVD" is not a complete instruction. The service has no list of IP addresses to allow. It has names, tags, two special platform addresses and a few ports. A team that treats it like an ordinary application can end up with hosts that look healthy and never take a connection, or with a proxy that works for web browsing and breaks long-running sessions.

This article explains what is required and where each control sits. The [networking article](/azure-virtual-desktop/plan-avd-networking/) walks through one worked example with firewall rules and routes. This one covers the rules behind it, proxies, DNS and Private Link.

## Key terms

| Term | Meaning |
|---|---|
| Outbound | Traffic that starts on the session host or client and goes out. AVD needs no inbound ports. |
| FQDN | Fully qualified domain name, such as a full web address without the path. |
| Wildcard | A name with `*` in it, such as `*.wvd.microsoft.com`, that matches many names. |
| Service tag | A named group of IP address prefixes for an Azure service. Microsoft keeps it up to date. You use it in network security group rules, Azure Firewall and routes. |
| FQDN tag | An Azure Firewall name for a group of domain names for a Microsoft service. |
| Network security group (NSG) | Rules that allow or deny traffic to and from a subnet or network interface. |
| UDR | User-defined route. A route you write to change where traffic goes. |
| Proxy | A server that sits between a device and the internet and may inspect or filter traffic. |
| Private Link | Azure's way to reach a service through a private IP address in your network. |
| Private endpoint | The network interface with a private IP that connects you to the service through Private Link. |
| Private DNS zone | A DNS zone that is visible only inside your network. It maps service names to private endpoint addresses. |
| Sub-resource | The part of a service that a private endpoint attaches to. For AVD the three are `global`, `feed` and `connection`. |
| DNS | The system that turns a name into an IP address. Azure-provided DNS is the resolver Azure gives every virtual network. Custom DNS is a resolver you run or choose. |
| Session host and host pool | A session host is a virtual machine that runs users' desktops and apps. A host pool is a group of session hosts managed together. |
| Workspace and feed | A workspace is the AVD object that lists the desktops and apps a user can open. The feed is that list as the client downloads it. |
| AVD agent | Software on each session host that registers it with the service and keeps a connection to it. Its Windows services are RDAgent and Remote Desktop Agent Loader (RDAgentBootLoader). |
| Agent URL Tool | A tool from Microsoft that you run on a session host. It tests whether the host can reach each required name. |
| IMDS | Instance Metadata Service. A local address that a virtual machine asks for its own details, such as its identity and settings. |
| Event Viewer | The Windows tool that shows the event logs of a computer. |
| Reverse connect | Both the client and the session host open outbound connections to the service, which joins them. No inbound port is opened on the host. |
| Gateway | The Microsoft-run part of the AVD service that joins the client's connection to the session host's connection. |
| Azure Front Door | A Microsoft global entry service. In the public cloud, client connections to AVD reach a gateway through it. |
| RDP Shortpath, STUN and TURN | RDP Shortpath adds a UDP path for the remote session. STUN is the method that finds a direct UDP path over the public internet. TURN is a relay method that carries that UDP traffic through a Microsoft server when no direct path works. RDP Shortpath for managed networks is the UDP path over a private connection such as ExpressRoute or a VPN. |
| TCP and UDP | Two ways to send data over a network. TCP checks that data arrives. UDP sends data without checking that each piece arrives. |
| WebSocket | A long-lived connection that stays open so both sides can send data at any time. |
| SSL termination (SSL inspection) | A proxy opens encrypted traffic, reads it and re-encrypts it with its own certificate. |
| PAC file and WPAD | A PAC file is a small script that tells a device which proxy to use for which address. WPAD is a way for a device to find that script automatically through DNS. |
| Azure Firewall | Azure's managed firewall service. It can allow traffic by name, FQDN tag or service tag. |
| AD DS | Active Directory Domain Services: a Windows domain run on domain controllers. |
| Microsoft Entra Domain Services | A managed domain service in Azure. Microsoft runs the domain controllers for you. |
| Intune Remote Help | A remote assistance feature from Microsoft Intune. A helper can see and control a user's session. |

## There is no IP list

The documentation is direct: AVD has no list of IP address ranges that you can allow instead of names ([Required FQDNs and endpoints](https://learn.microsoft.com/en-us/azure/virtual-desktop/required-fqdn-endpoint#service-tags-and-fqdn-tags)).

The tables below have two exceptions. One is the relay range for RDP Shortpath (`51.5.0.0/16`). The other is the two Azure platform addresses. They are listed separately and are not a substitute for the names.

A next-generation firewall is a non-Microsoft firewall that filters by application or name, not only by address and port. For one, the documentation says to use a dynamic list built for Azure addresses. It recommends service tags and FQDN tags where you can, because they are kept current for you.

It also says Microsoft does not support AVD deployments where the listed FQDNs and endpoints are blocked. That does not mean "it may be slow". It means "not supported".

## What the session host needs

All entries are outbound. The documentation lists them in a table with the address, protocol, port, purpose and service tag. The list changes, so treat any copy, including this one, as a snapshot and read the current page. These rows show the shape of the list. They are not the full list. They use the Azure public cloud names. Azure for US Government has its own names and relay range, so use the tab for your cloud.

| Need | Example | Port |
|---|---|---|
| Sign in to Microsoft Entra ID | `login.microsoftonline.com` | TCP 443 |
| Service traffic, including TCP-based RDP | `*.wvd.microsoft.com` and the newer `*.service.windows.cloud.microsoft`, `*.windows.cloud.microsoft` and `*.windows.static.microsoft` families | TCP 443 |
| Relayed RDP (RDP Shortpath through TURN) | `51.5.0.0/16` | UDP 3478 |
| Agent and monitoring traffic | `*.prod.warm.ingest.monitor.core.windows.net`, `gcs.prod.monitoring.core.windows.net` | TCP 443 |
| Agent and stack updates | `mrsglobalsteus2prod.blob.core.windows.net` | TCP 443 |
| Windows activation | `azkms.core.windows.net` | TCP 1688 |
| Certificates | Several names, including `ctldl.windowsupdate.com` and `www.microsoft.com` | TCP 80 |

Allow all of these families. The documentation lists each name.

The documentation says the wildcard form is required for service traffic. For agent traffic, if you prefer not to use a wildcard, you can find the exact names yourself. On a registered session host, open the Event Viewer, go to Windows logs, then Application, then WVD-Agent, and read event ID 3701. Those names are region-specific, so repeat it for each region you deploy to. The [Agent URL Tool](https://learn.microsoft.com/en-us/azure/virtual-desktop/check-access-validate-required-fqdn-endpoint) checks that a host can reach the required names.

The list does not cover every name for Microsoft Entra ID, Office 365, custom DNS providers or time services. For restricted networks the documentation points to the Office 365 URL and address ranges list (the Microsoft Entra rows, with IDs 46, 56, 59 and 125, in [Office 365 URLs and IP address ranges](https://learn.microsoft.com/en-us/microsoft-365/enterprise/urls-and-ip-address-ranges)) for the Microsoft Entra names. If users need Microsoft 365 apps inside the session, the session hosts must reach the Microsoft 365 endpoints as well. The page also lists optional names, for example for Windows Update, OneDrive updates and diagnostic settings, and a separate list if you use Intune Remote Help. If your network is closed, you may also need the names for certificate checks in [Azure Certificate Authority details](https://learn.microsoft.com/en-us/azure/security/fundamentals/azure-CA-details#certificate-downloads-and-revocation-lists).

### The two platform addresses

Two addresses behave differently from everything above.

| Address | Port | Purpose |
|---|---|---|
| `169.254.169.254` | TCP 80 | Azure Instance Metadata Service (IMDS) |
| `168.63.129.16` | TCP 80 and 32526, TCP and UDP 53 | Azure platform services: health signals, DNS when you use Azure-provided DNS, and DHCP |

The documentation says traffic to these addresses must not be intercepted, proxied or sent through VPN tunnels or secure web gateways ([Azure fabric communication IPs](https://learn.microsoft.com/en-us/azure/virtual-desktop/azurecommunicationips#differences-from-standard-endpoints)). A full-tunnel VPN client or a secure web gateway agent on the session host can break it. Doing so causes provisioning failures, health monitoring problems and connection problems. Azure protects this traffic inside its own network layer, so ordinary NSG rules and routes do not affect it by default. The risk is a setting you add. Examples are an explicit deny rule or route aimed at these addresses or their service tags (`AzurePlatformIMDS` and `AzurePlatformDNS`), a proxy or PAC setting, a firewall on the host, or endpoint security software inside the VM. See [Azure fabric communication IPs](https://learn.microsoft.com/en-us/azure/virtual-desktop/azurecommunicationips). Port 53 is only needed with Azure-provided DNS. With custom DNS, queries go to your servers, so make sure they are reachable.

## What clients need

Any device that runs an AVD client app, such as the Remote Desktop client or Windows App, must reach a separate list of names, mostly on TCP 443. It includes the sign-in, service and troubleshooting names, and `51.5.0.0/16` on UDP 3478 for relayed connections. Blocking these is not supported either. The documentation says that allowing these names is essential for a reliable client experience.

## Where each control sits

![At the top, the Microsoft-run Azure Virtual Desktop service reached by name on TCP 443 (UDP 3478 for the relay), with no IP range list to use instead of names, but an FQDN tag or a service tag. On the left, a user device behind a firewall or proxy on the client network. On the right, a session host in a subnet, with network security group rules, a route table and a firewall or proxy on its outbound path. At the bottom left, an optional Private Link panel with the private endpoints and DNS zones. At the bottom right, a red panel for the two Azure platform addresses that must not be proxied, intercepted or sent through VPN tunnels.](/img/avd/AVD-Post-16-Enforcement-Points-v3.png)

*Source: [Required FQDNs and endpoints for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/required-fqdn-endpoint), [proxy server guidelines](https://learn.microsoft.com/en-us/azure/virtual-desktop/proxy-server-support), [Private Link with Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview) and [Azure fabric communication IPs](https://learn.microsoft.com/en-us/azure/virtual-desktop/azurecommunicationips). The documentation's Private Link diagram is not reproduced, so the layout is simplified. The drawing leaves out the client path through Azure Front Door and RDP Shortpath. Checked against the cited pages in October 2026. Icons: Microsoft Azure and Microsoft Entra architecture icons, used unmodified under the terms on Microsoft's icons page.*

Three places can block a connection, and they are often owned by different teams (judgement): the client network, the session host subnet and the platform addresses. When a user cannot connect, find out which side is failing before you open any rule.

## Proxies

The documentation recommends bypassing proxies for AVD traffic. Its reasons:

- The traffic is already encrypted, so a proxy does not make it more secure.
- Most proxies are not built for long-running WebSocket connections, and AVD uses several long-lived connections per user, so proxy scale and stability matter.
- A distant proxy adds latency and makes the geographic routing less accurate.
- If the proxy is the only path, RDP data is forced over TCP instead of UDP, which lowers visual quality and responsiveness.

If you must use one, the documentation recommends:

- **Keep it in the same Azure geography** as the AVD agent and client.
- **Use RDP Shortpath for managed networks** so the RDP data can bypass the proxy where possible. Sign-in lookup, connection setup and diagnostics still go through it.
- **Do not terminate SSL on the proxy.** Replacing certificates adds sign-in time and can stop the agent working by interfering with its trusted connection to the service. The documentation says to turn inspection off and test again before opening a support case.
- **Do not use a proxy that needs authentication.** The agent components run in the operating system's own context, so they do not support a proxy that asks for credentials, and the connection fails.
- **Plan its capacity.** RDP traffic is long-running and chatty.
- **Do not use a proxy with Microsoft Teams media optimization** (Teams audio and video handled on the user's device). It is not supported.

For bypass, the documentation lists Azure Firewall with service tags, proxy auto-configuration (PAC) files, a bypass list and per-user configuration. On session hosts the agent tries to find a proxy with WPAD: it looks in DNS for a name of the form `wpad.<your domain suffix>`, and if it finds one it downloads the proxy script from it. (judgement) A stray WPAD record in your DNS could therefore change how the agent connects. For a manual system-wide proxy, at a minimum set a proxy for the RDAgent and Remote Desktop Services Windows services (the services of the AVD agent). The documentation shows the `bitsadmin` command for it. `bitsadmin` is a Windows command-line tool.

The Remote Desktop client and Windows App are the apps users run to open their desktops. Client support for proxies, per the [proxy guidelines](https://learn.microsoft.com/en-us/azure/virtual-desktop/proxy-server-support#client-side-proxy-support): yes for the Remote Desktop client, the web client, iOS, macOS and Windows App on Windows. No for Android.

The documentation says support is limited for connections through a proxy. It recommends configuring a bypass and reproducing the issue before you open a support case.

## DNS

The prerequisites and endpoint pages give the DNS requirements you need to plan for:

- If session hosts are joined to AD DS or Microsoft Entra Domain Services, the virtual network must reach the domain controllers and the relevant DNS servers.
- With Azure-provided DNS, hosts use `168.63.129.16` on port 53. With custom DNS, make sure the hosts can reach your servers.
- With Private Link, names for the service resolve to private addresses through private DNS zones. The next section lists the zones.

## What Private Link changes

Private Link lets traffic to the AVD service use private IP addresses in your network instead of public routes. The documentation describes three workflows, each with its own private endpoint.

| Purpose | Target | Quantity |
|---|---|---|
| Initial feed discovery (the first lookup where the client finds out which workspace feed to use) | Workspace, `global` sub-resource | One for your whole AVD deployment |
| Feed download | Workspace, `feed` sub-resource | One per workspace |
| Connection to a host pool | Host pool, `connection` sub-resource | One per host pool |

You can use Private Link for all three, for the feed and connections only (initial discovery stays public), for connections only, or not at all. Which one you choose is a design decision.

Documented rules and limits:

- For the initial feed discovery endpoint, the documentation says you should use a separate workspace that is used only for that purpose and has no application groups. Deleting that workspace stops feed discovery. Access control on that workspace is ignored: it is always reachable on public routes.
- With reverse connect there are two connections to the gateway: the client's and the session host's. You can allow public access for clients and private only for session hosts. Remote sessions are denied if the session host uses a public route in that case.
- If you restrict ports to the connection endpoint, you must allow the whole TCP range 1 to 65535 to it ([client connection sequence](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview#client-connection-sequence)). Azure private networking maps those ports to the gateway chosen during connection. Restricting them can stop users connecting.
- UDP over Private Link is blocked unless you opt in on the host pool networking page ([UDP with Private Link](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview#udp-with-private-link-optin)). The opt-in is required for RDP Shortpath for managed networks. After you opt in, you must turn off Shortpath for public networks (which uses STUN and TURN), or the portal refuses to save.
- Enable Private Link on each subscription before you use it. After you change a host pool's private endpoint or network configuration, restart the Remote Desktop Agent Loader service on each session host, or restart the hosts.
- Use the zone `privatelink-global.wvd.microsoft.com` for the global endpoint and `privatelink.wvd.microsoft.com` for the others. Sharing the older single zone is no longer supported (since September 1, 2023, per the [Private Link overview](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview#known-issues-and-limitations)).
- Private endpoints use IP addresses and demand can grow, so plan address headroom.
- To close public routes, the documentation uses the `WindowsVirtualDesktop` service tag in an NSG or Azure Firewall rule. Do not block traffic between your private endpoints and the [required endpoint list](https://learn.microsoft.com/en-us/azure/virtual-desktop/safe-url-list). See [Set up Private Link](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-setup).
- Azure PowerShell cmdlets for Azure Virtual Desktop that support Private Link are described as being in preview on the [setup page](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-setup#prerequisites) (check the page for the current state).

**Which clients support Private Link.** The documentation pages do not fully agree. The [setup page](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-setup) lists the Remote Desktop app on any platform (on Windows, version 1.2.4066 or later) and Windows App on macOS and iOS/iPadOS. The [overview page](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview) says all Remote Desktop clients can be used. The [Windows App feature comparison](https://learn.microsoft.com/en-us/windows-app/compare-platforms-features#network) marks Private Link as supported on Windows, macOS, iOS/iPadOS and Android/Chrome OS, and not in a web browser. The Remote Desktop client for Windows (MSI) is not supported from March 27, 2026 ([Access a Cloud PC](https://learn.microsoft.com/en-us/windows-365/end-user-access-cloud-pc#remote-desktop) and the [Remote Desktop client overview](https://learn.microsoft.com/en-us/previous-versions/remote-desktop-client/overview)). Test your client against a Private Link host pool before you commit to it.

## Common mistakes

- **Writing an IP allow list.** There is none. Use names, tags and FQDN tags.
- **Blocking the platform addresses with a catch-all rule or proxy.** The result is failures that look like unrelated problems.
- **Sending all traffic through a proxy that terminates SSL.** It can stop the agent working.
- **Restricting ports to the connection private endpoint.** Allow the whole TCP range.
- **Forgetting to restart the agent loader after changing the private endpoint.**
- **Opting in to UDP over Private Link and leaving public Shortpath on.** The save fails.
- **Treating the client network as someone else's problem.** Clients need their own endpoint list.

## How to validate your network design

These are recommended checks to run in a test environment.

1. Run the Agent URL Tool on a session host and read the result against the current endpoint page.
2. Read event ID 3701 on the host and compare the names with your firewall's allow list.
3. From a client on a restricted network, connect and check the transport shown in the client.
4. Check the effective routes on a session host's network interface and confirm nothing redirects the two platform addresses (judgement: the routing check itself is general Azure practice, although Learn lists "no routes explicitly target" these addresses under [Azure fabric communication IPs](https://learn.microsoft.com/en-us/azure/virtual-desktop/azurecommunicationips#user-defined-routes-and-network-virtual-appliances), see [diagnose a network routing problem](https://learn.microsoft.com/en-us/azure/virtual-network/diagnose-network-routing-problem)). Check the host's own proxy settings, VPN clients, host firewall and endpoint security software too.
5. For Private Link, resolve each service name from a client and from a session host, and confirm you get private addresses.

## Related book chapter, lab and project

[Chapter 11](https://github.com/AddySidd27/azure-virtual-desktop-architect/blob/main/chapters/ch11-network-fundamentals-required-connectivity.md) of the book covers network fundamentals and required connectivity. [Lab 3](https://github.com/AddySidd27/azure-virtual-desktop-architect/blob/main/labs/lab-03-vnet-subnets-nsg-dns.md) builds the network. The lab has not been run end to end in Azure. [Project 11](https://github.com/AddySidd27/azure-virtual-desktop-architect/blob/main/scenarios/project-11-highly-secure-regulated.md) is a fictional case study.

Next: [Choose a Network Topology and Plan IP Addresses for Azure Virtual Desktop](/azure-virtual-desktop/network-topology-and-ip-planning-for-avd/).

## Sources

- [Required FQDNs and endpoints](https://learn.microsoft.com/en-us/azure/virtual-desktop/required-fqdn-endpoint)
- [proxy server guidelines](https://learn.microsoft.com/en-us/azure/virtual-desktop/proxy-server-support)
- [Private Link with Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview)
- [Private Link setup](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-setup)
- [Azure fabric communication IPs](https://learn.microsoft.com/en-us/azure/virtual-desktop/azurecommunicationips)
- [Windows App feature comparison](https://learn.microsoft.com/en-us/windows-app/compare-platforms-features#network)
- [Access a Cloud PC](https://learn.microsoft.com/en-us/windows-365/end-user-access-cloud-pc#remote-desktop)
