---
title: "Azure Virtual Desktop in a Hub-and-Spoke Network: Peering, Routing, Firewall and DNS"
seoTitle: "AVD Hub-and-Spoke: Peering, Routing, Firewall, DNS"
layout: post.njk
permalink: "/azure-virtual-desktop/hub-and-spoke-network/"
order: 135
part: 35
tags: [avd-series]
deck: "Decide what lives in the hub and what lives in the spoke, which peering settings to turn on, which routes the host subnet needs, and how the firewall and DNS must be set up."
description: "How Azure Virtual Desktop fits a hub-and-spoke network: hub and spoke contents, peering settings, user-defined routes, Azure Firewall rules, DNS, gateways and Private Link."
---

When you run Azure Virtual Desktop (AVD) in a hub-and-spoke network, a central platform team usually owns the hub and you get a spoke. The questions that follow are practical. What may you put in your spoke? What must the hub provide? Which settings on the peering do you need? Which routes does the host subnet need so that sessions do not drop?

This article answers those questions for the person who builds the AVD spoke and for the person who owns the hub. It covers a hub that you manage yourself, with Azure Firewall in the hub. Azure Virtual WAN is a Microsoft-managed alternative, and this article mentions it only for one route. The article does not repeat three earlier articles. [Plan Azure Virtual Desktop Networking](/azure-virtual-desktop/plan-avd-networking/) gives the step-by-step build of the VNet, peering, DNS and firewall policy. [Required Connectivity for Azure Virtual Desktop](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) covers the endpoints that session hosts must reach. [Choose a Network Topology and Plan IP Addresses for Azure Virtual Desktop](/azure-virtual-desktop/network-topology-and-ip-planning-for-avd/) covers choosing a topology and planning addresses. This article goes deeper on who owns what, what crosses the peering, and where a general hub recommendation does not fit AVD.

## Key terms

| Term | Meaning |
|---|---|
| Virtual network (VNet) | A private network in Azure that virtual machines connect to. |
| Hub-and-spoke | A network layout with one central VNet (the hub) and several VNets (the spokes) that each connect to the hub. |
| Hub VNet | The central VNet. It holds shared network services that the spokes use, and it is the central point of connectivity for networks outside Azure. |
| Spoke VNet | A VNet that isolates and manages a workload separately from the others. For AVD, the session hosts live here. |
| VNet peering | A connection between two VNets. Traffic goes over the Azure backbone without a router. Peering is nontransitive. |
| Nontransitive | If spoke A is peered to the hub and spoke B is peered to the hub, A and B are not connected to each other. |
| Gateway transit | A peering setting that lets a spoke use the VPN or ExpressRoute gateway that sits in the hub. |
| Cross-premises | Outside Azure, for example your own office or datacenter network. |
| VPN gateway | A virtual network gateway that sends encrypted traffic between a VNet in Azure and other networks over the public internet. |
| ExpressRoute gateway | A gateway that exchanges IP routes and routes network traffic between your on-premises network and your Azure VNet. |
| Session host | An Azure virtual machine in a host pool. A user's session comes from a session host. |
| Host pool | A collection of Azure virtual machines that register to AVD as session hosts. |
| Control plane | The AVD service that users connect to. It includes the web service, the broker service that orchestrates incoming connections, and the gateway service that provides the connection between a user's device and the session hosts. |
| User-defined route (UDR) | A route you create to tell Azure where to send traffic for an address range. |
| Next hop | The place Azure sends matching traffic next, such as the internet or a firewall. |
| Service tag | A name for a group of IP addresses that belong to one Azure service. `WindowsVirtualDesktop` is the one for AVD. A route can use it. |
| FQDN | Fully qualified domain name: a full name such as `www.contoso.com`. |
| FQDN tag | An Azure Firewall name for a group of FQDNs that one Microsoft service needs. AVD has one, also called `WindowsVirtualDesktop`. Firewall rules use it. It is not the service tag. |
| IP Group | A list of IP addresses that you can use as the source of a firewall rule. For AVD, one IP Group can hold every session host of a host pool. |
| Forced tunneling | Sending all internet-bound traffic to a chosen next hop, instead of straight to the internet. |
| Virtual WAN | A Microsoft-managed hub for hub-and-spoke networks. The alternative to a hub that you manage yourself. |
| Virtual Network Manager | A service that helps you group, configure, deploy and manage VNets at scale. |
| DNS | The Domain Name System. It turns a name into an IP address. |
| DNS proxy | An Azure Firewall setting that lets the firewall answer DNS queries for the hosts behind it. |
| SNAT | Source network address translation. For traffic to the internet, the firewall replaces the spoke's source address with one of the firewall's public IP addresses. |
| Azure NAT Gateway | A network address translation service that lets all instances in a subnet connect outbound to the internet while staying private. |
| TLS inspection | Reading encrypted HTTPS traffic. The inspecting device replaces the security certificates of the service with certificates that it generates. |
| Network security group (NSG) | A set of rules that allow or deny network traffic to or from Azure resources in a VNet. |
| Network virtual appliance (NVA) | A firewall or router from another vendor that runs as a virtual machine. |
| Private Link | An Azure feature that connects you to a service over a private IP address in your VNet. The network interface that holds that address is called a private endpoint. |
| FSLogix | The profile solution for AVD. It redirects a user's Windows profile into a virtual hard disk that sits on a storage provider, such as an SMB file share. |
| Availability zones | Physically separate datacenter locations within an Azure region, each with independent power, cooling and networking. |
| Azure DDoS Protection | A service that defends against distributed denial of service attacks. These attacks try to exhaust an application's resources and make it unavailable. |
| Azure Network Watcher | A service to monitor and troubleshoot network components. Connection monitor is part of it. It checks connectivity at regular intervals and reports changes in reachability and latency. |
| AD DS | Active Directory Domain Services. A directory service that stores information about user accounts, computers and other objects on a network. |
| Microsoft Entra Domain Services | Managed domain services, such as domain join and Group Policy, that you use without running your own domain controllers. |
| Landing zone | An Azure environment built on design rules so that many workloads can be hosted and managed at scale. |
| Platform landing zone | The landing zone that holds shared services such as networking, identity, DNS and security controls. |
| Workload landing zone | The landing zone that holds one workload, here AVD. |

## What lives in the hub and what lives in the spoke

Resource placement can vary with your governance, so treat the table as a starting point and agree the final split with the owner of the hub. The hub VNet is the networking part of the platform landing zone. The spoke VNet is the networking part of the workload landing zone.

| Area | Platform landing zone (hub side) | Workload landing zone (spoke side) |
|---|---|---|
| Network | Hub connectivity, DNS services, shared network security services and outbound connectivity controls. | Virtual networks, subnets and the connectivity that the AVD deployment needs. |
| Identity | Microsoft Entra ID and shared identity services. | The identity integration and access settings for AVD. |
| AVD resources | Not typically hosted here. | Host pools, session hosts, workspaces, application groups and autoscale settings. |
| User environment | Shared identity, networking, security and management capabilities. | FSLogix profile storage, application delivery and custom images. |

Two more points change how you divide the work.

- **Who owns the hub.** In an Azure landing zone, a central platform team manages the hub's shared resources and network. The spokes are co-owned by the platform team and the team that uses the spoke. Hubs sit in a Connectivity subscription. Spokes sit in many separate workload subscriptions.
- **Where domain controllers go.** For session hosts that join a domain, the domain services sit in the Identity subscription. This is a platform subscription, next to the Connectivity subscription. These services are Microsoft Entra Domain Services or self-managed AD DS domain controllers hosted in Azure. AD DS is also an example of a shared service that can be placed in the hub VNet. So the domain controllers are a platform service, not part of your spoke. Ask the hub owner which network they run in. Whichever you have, users must still be discoverable through Microsoft Entra ID. Identities that exist only in AD DS are not supported. [Choose the Right Identity Model](/azure-virtual-desktop/choose-the-right-identity-model/) explains the join choices.

## The three paths through the network

The diagram shows the three paths that matter. Each one needs a different setting.

![A spoke with a session host subnet, optional private endpoints and FSLogix profile storage is peered to a hub with Azure Firewall, a VPN or ExpressRoute gateway to on-premises and shared DNS. The host subnet sends a default route to the firewall and the WindowsVirtualDesktop service tag to the internet. Users on noncorporate networks reach the AVD control plane over the internet.](/img/avd/avd-hub-and-spoke.svg)

*Sources: [Hub-spoke network topology in Azure](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke), [Use Azure Firewall to protect Azure Virtual Desktop deployments](https://learn.microsoft.com/en-us/azure/firewall/protect-azure-virtual-desktop) and [Azure Virtual Desktop landing zone design guide](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/azure-virtual-desktop/design-guide).*

1. **Users to the service.** Users on noncorporate networks reach the AVD control plane directly over the internet. They do not need a VPN or ExpressRoute.
2. **Session hosts to the AVD service.** This is outbound traffic from the host subnet. Traffic to the AVD gateway and broker needs its own route that goes direct (see the routing section). The other required endpoints go to the hub firewall, which needs rules for them.
3. **Session hosts to your own networks.** Traffic to on-premises networks goes through the gateway in the hub. Spokes use the hub gateway, and you must set up routing to make that work.

## Peering settings

A spoke connects to the hub with VNet peering. Peering is nontransitive and low latency. Several design rules come from that.

| Topic | What to do |
|---|---|
| Which hub | In most cases, peer each spoke to a single hub in the same region. A hub is a regional resource. Use at least one hub per region and connect only spokes from the same region to it. This keeps a failure in one region's hub from causing routing failures in other regions. |
| Subscriptions and tenants | A spoke can be in a different subscription from the hub. The two subscriptions can be in the same or different Microsoft Entra tenants. |
| Use the hub gateway | On the hub's peering connection, set **Allow** gateway transit. On each spoke's peering connection, set **Use the remote virtual network's gateway**. |
| Forwarded traffic | Set **Allow** forwarded traffic on all peering connections. Do this for the gateway arrangement and when traffic goes through a firewall or NVA. |
| Spoke to spoke | Peering is nontransitive. To connect two spokes, add a peering between them, or place them in the same Virtual Network Manager network group, or route their traffic through the firewall (see the routing section). |
| Direct peering between spokes | Use it only in special circumstances. Limit it to spokes that belong to the same environment and workload. It adds no extra hop, so it keeps latency low. |

Spokes typically do not deploy their own gateway. They use the hub gateway, and routing must be configured too. The peering setting alone does not finish the job. Settings on the hub side of the peering are changes in the hub, so ask the hub owner to make or confirm them.

If you manage many spokes, Virtual Network Manager can create peerings and routes for you. Compare its cost with the time it saves before you decide.

## Routing: user-defined routes and the AVD exception

A core purpose of hub-and-spoke is to send outbound internet traffic through the controls in the hub. You do this with a route table on the host subnet. A route table holds user-defined routes (UDRs).

For spoke-to-spoke traffic, one pattern is to use UDRs that force spoke traffic to the firewall or an NVA in the hub. The firewall then routes it to the other spoke. This uses Azure Firewall with forced tunneling turned on, and the peering connections must accept forwarded traffic. It also avoids needing a peering between every pair of spokes. Peerings per VNet are limited, so many spokes can run out of peering connections.

AVD adds one rule to this. If you send all traffic to the firewall with a default route, AVD disconnections can happen when Azure Firewall scales in. To avoid that, session hosts need direct access to the AVD gateway and broker. In a hub-and-spoke network, add a route to the route table on the AVD subnet with these values:

| Field | Value |
|---|---|
| Destination type | Service tag |
| Destination service | WindowsVirtualDesktop |
| Next hop | Internet |

This route is for the gateway and broker. The other required endpoints still go to the firewall, so the firewall rules must allow them (see the next section).

The same route applies in an Azure Virtual WAN design, on the route table of the spoke subnet that hosts the AVD workload. The [Plan Azure Virtual Desktop Networking](/azure-virtual-desktop/plan-avd-networking/) article shows how to create it.

## The firewall and the required endpoints

Session hosts run in your VNet and are subject to its security controls. They need outbound access to the AVD service to work. Azure Firewall can filter that traffic.

- **Use the FQDN tag.** Azure Firewall has an AVD FQDN tag, `WindowsVirtualDesktop`. It is not the service tag used in the route. It simplifies the rules. You create a firewall policy and rule collections for network rules and application rules. You still need rules for each of the required FQDNs and endpoints. [Required Connectivity for Azure Virtual Desktop](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) lists them.
- **Name the host pool as the source.** To identify a specific host pool as the source, create an IP Group that contains each session host.
- **Use the sample policy as a starting point.** A published template deploys the mandatory and optional rules in one firewall policy. Review every rule against the AVD requirements before you use it in production.
- **Do not use TLS inspection with AVD.** TLS inspection can stop the AVD agent working, because it interferes with the trusted connections between the agent and the service. The general hub-spoke design recommends Azure Firewall Premium for TLS inspection. If the hub owner turns it on, ask them to confirm that AVD traffic is not inspected.
- **Keep user internet access separate.** If the allowed destinations are well defined, such as Microsoft 365, use firewall application and network rules. This sends end-user traffic directly to the internet. To use an existing on-premises secure web gateway instead, set an explicit proxy in the browsers or applications on the host pool. Those proxy settings only influence end-user internet access.
- **Control websites by category.** Add a rule to an application rule collection that allows or denies web categories for your host pool's IP address.

### Outbound addresses (SNAT)

The hub firewall sits between every spoke and the internet, on-premises networks and any spoke that routes through it. Outbound flows to the internet leave a spoke from one of the firewall's public IP addresses (SNAT). That has three effects.

- A partner's allow list and your audit logs must cover every public IP address on the firewall. A public IP address prefix expresses that set as one range.
- The number of public IPs sets the SNAT port budget and so the ceiling on concurrent outbound connections for every spoke.
- To go beyond that ceiling, you can attach an Azure NAT Gateway to the `AzureFirewallSubnet`. It provides up to 16 public IPs and a larger SNAT port pool. Return traffic still goes back through the firewall.

Two subnet rules also matter. The firewall needs a subnet named `AzureFirewallSubnet`, with an address range of at least `/26`, and that subnet does not support network security groups. The gateway needs a subnet named `GatewaySubnet`. Use `/26` or larger. A `/26` gives enough room to avoid gateway size limits and to add ExpressRoute circuits later.

## DNS

Hub-spoke designs often provide one DNS solution that all peered spokes use. The two reasons given are routing to cross-premises networks and the DNS records for private endpoints. For AVD, three DNS rules follow.

1. **Turn on DNS and DNS proxy in the firewall policy** if you use FQDNs in network rules. This is a prerequisite.
2. **Use one DNS provider for the firewall and the hosts.** Because of how Azure Firewall implements FQDN application rules, the firewall and the resources behind it should use the same DNS provider. If the firewall and the traffic source resolve a name to different IP addresses, the firewall can block legitimate traffic. You can include the firewall's DNS proxy in the spoke's DNS resolution to keep the answers in sync.
3. **Agree where shared DNS and domain services live.** DNS and AD DS are examples of shared services that can sit in the hub. Domain services can also sit in the Identity subscription. Ask the hub owner which design you have.

## Connecting to on-premises networks

A VPN or ExpressRoute gateway in the hub gives every spoke a path to the networks outside Azure. Spokes do not deploy their own gateways. They use the hub's, and you must set up routing to make that work.

- **Availability.** For higher availability you can use ExpressRoute with a VPN as failover. Use availability zones for hub services that support them.
- **Throughput.** A single ExpressRoute gateway limits the traffic from on-premises into the VNet to the gateway's aggregate throughput limit, no matter how much circuit bandwidth you have. The gateway also caps the throughput of any single TCP flow and limits the number of concurrent flows.
- **Addresses.** The address space must not overlap across your cross-premises locations and your Azure locations.
- **Protection.** Turn on Azure DDoS Protection on any perimeter VNet. The public IP addresses of the firewall, the VPN gateway and the ExpressRoute control plane need protection even if your workloads are not exposed publicly.

## Where Private Link and shared services fit

Private Link can expose individual resources to other VNets without a peering or routing relationship between them. In the AVD baseline deployment, Azure Storage and Key Vault can have optional private endpoints with private DNS zones. A private endpoint is a network interface in your VNet, so the diagram shows the endpoints inside the spoke and the FSLogix profile storage outside it. Hub-spoke designs often keep the DNS records for private endpoints in the shared DNS (see the DNS section).

For flows that are sensitive to latency, such as access to storage, you can bypass the firewall or hub routing. Private Link or direct peering are the tools the hub-spoke design names for this. Test the delay the firewall adds before you decide. Direct peering also reduces Azure Firewall processing cost for high-throughput traffic between spokes, such as large file copies.

## Common mistakes

- **Sending all traffic to the firewall with no exception for the AVD gateway and broker.** Sessions can drop when the firewall scales in. Add the `WindowsVirtualDesktop` service tag route with next hop Internet.
- **Turning on TLS inspection for AVD traffic.** Do not use it with AVD.
- **Assuming peering connects spokes.** Peering is nontransitive. Add a route to the firewall or a peering between the two spokes.
- **Setting only one side of the gateway arrangement.** The hub needs Allow gateway transit. The spoke needs Use the remote virtual network's gateway. Both need Allow forwarded traffic.
- **Deploying a gateway in every spoke.** Spokes typically do not deploy their own gateway. They use the one in the hub.
- **Different DNS for hosts and firewall.** FQDN rules can block legitimate traffic when the two resolve a name differently.
- **Forgetting the firewall's public IPs.** Partners and audit logs must cover all of them.
- **Putting a network security group on `AzureFirewallSubnet`.** That subnet does not support them.
- **Overlapping address ranges with on-premises or other Azure networks.** Plan the ranges before you peer.
- **Adding spokes without checking hub capacity.** The firewall's bandwidth limits apply to all spokes that use it.

## How to validate this in your environment

Some of these checks are in the hub. If you cannot see the hub side, ask the hub owner to run or confirm them.

1. Open the peering on the hub side and on the spoke side. Check that Allow gateway transit is on the hub link, that Use the remote virtual network's gateway is on the spoke link, and that Allow forwarded traffic is on all links.
2. Open the route table linked to the AVD host subnet. Check for the default route to the firewall. Check for the route with destination type Service tag, destination service `WindowsVirtualDesktop` and next hop Internet.
3. Open the firewall policy. Check that DNS and DNS proxy are on if any network rule uses an FQDN. Check that the rules cover the required FQDNs and endpoints, and that no TLS inspection applies to AVD traffic.
4. Compare the DNS servers on the session hosts with the DNS the firewall uses. They should be the same provider, or the hosts should use the firewall DNS proxy.
5. Check the subnet names and sizes in the hub: `AzureFirewallSubnet` at least `/26`, `GatewaySubnet` `/26` or larger, and no network security group on `AzureFirewallSubnet`.
6. Compare the address ranges of the hub, the spokes, on-premises and other Azure networks. None should overlap.
7. Check that diagnostic settings are on for the firewall and the cross-premises gateway. Firewall logs can be large, so turn off settings you do not use.
8. Use Connection monitor in Azure Network Watcher to watch the path from a session host to the services it needs, and to find anomalies.
9. Ask the hub owner for the list of public IP addresses on the firewall, and give it to any partner that keeps an allow list for your users' traffic.

## Sources

- [Hub-spoke network topology in Azure](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke)
- [Use Azure Firewall to protect Azure Virtual Desktop deployments](https://learn.microsoft.com/en-us/azure/firewall/protect-azure-virtual-desktop)
- [Azure Virtual Desktop landing zone design guide](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/azure-virtual-desktop/design-guide)
