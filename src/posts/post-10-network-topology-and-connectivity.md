---
title: "Network Topology and Connectivity"
slug: "network-topology-and-connectivity"
series: "Azure Landing Zone"
part: ""
post_number: 10
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/network-topology-and-connectivity"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/define-an-azure-network-topology"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/plan-for-ip-addressing"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-about"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/ddos-protection/ddos-protection-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview"
    checked_on: "2026-10-07"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/networking.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/connectivity-options.md"
diagrams:
  - file: "../diagrams/post-10-hub-spoke-and-virtual-wan.svg"
    type: learn-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology and https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology"
    icons: "Azure Public Service Icons V24 (DDoS Protection Plans, DNS Zones, ExpressRoute Circuits, Virtual Network Gateways, Firewalls, Virtual Networks, Virtual WANs, Route Tables, Network Security Groups, Subscriptions), unmodified"
    source: "../diagrams/post-10-hub-spoke-and-virtual-wan.drawio"
production_section_written_by_addy: true  # from Addy's own taps, 2026-10-07 (Addy confirmed it is all true); wording drafted by Claude
layout: post.njk
permalink: "/azure-landing-zone/network-topology-and-connectivity/"
order: 10
deck: "Network topology and connectivity is the layout of your virtual networks and their links to on-premises networks, and the landing zone guidance offers two layouts, a traditional hub-and-spoke where you manage routing and security and one based on Azure Virtual WAN that Microsoft manages, to be chosen from your requirements."
next_num: ""
next_title: "Security"
tags: [alz]
---



In [the business requirements post](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/) you met connectivity as one of the five business requirements, and saw VPN Gateway, ExpressRoute, hub-and-spoke and Virtual WAN in short. In [the platform scope post](/azure-landing-zone/platform-scope-and-workload-boundaries/) and [the resource organization post](/azure-landing-zone/resource-organization/) you saw where the Connectivity, Corp and Online management groups sit. This post answers the next question: how should the networks themselves be laid out?

It matters early because network topology and connectivity are fundamental when you plan a landing zone design, and networking is central to almost everything inside one. It enables connectivity to other Azure services, to external users and to on-premises systems. Your topology defines how workloads communicate with one another. Your design should also include any hybrid or multicloud connections you plan (multicloud means using more than one cloud provider), and the traffic you expect on them. [The business requirements post](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/) covers choosing between VPN Gateway and ExpressRoute. This post covers the layout around them.


## Key terms

Earlier posts covered landing zone, workload, platform team, management group, subscription, resource group, virtual network, subnet, hub-and-spoke network, hybrid connectivity, VPN Gateway, ExpressRoute, Azure Firewall, private DNS zone, the Connectivity subscription, Corp, Online, tenant, Azure Policy and subscription vending. [The business requirements post](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/) also briefly covered Azure Virtual WAN, overlapping address ranges, and the ideas of branch, IPsec, tunnel and native IPsec termination. The words below are the ones this post depends on most. Other new words are explained where they first appear.

| Word | What it means |
|---|---|
| Virtual network peering | A connection between two or more virtual networks in Azure that makes them appear as one for connectivity. Their traffic stays on Microsoft's private backbone (Microsoft's own network), not the public internet. Global virtual network peering does the same between virtual networks in different Azure regions. |
| Route and user-defined route (UDR) | Azure uses routes to decide where to send traffic. Each route has an address range and a next hop type, which says where traffic for that range goes next. Azure adds default routes to every subnet. You can override some of them with your own routes, called user-defined routes (UDRs), in a route table that you attach to subnets. |
| Network virtual appliance (NVA) | A virtual machine that typically runs a network application, such as a firewall. A partner or non-Microsoft NVA comes from another vendor. |
| Transitive | Traffic can pass through a middle network to reach a third one. Virtual network peering and global virtual network peering are not transitive. To build a transit network you need UDRs and NVAs (in the hub, Azure Firewall or a partner NVA can do this job). |
| Gateway | Short for virtual network gateway, the Azure component that connects a virtual network to a VPN device (a device at your site that ends the VPN link) or to ExpressRoute. A VPN gateway handles VPN links and an ExpressRoute gateway handles ExpressRoute links. In Virtual WAN, the hub has its own gateways instead (this is called a hub gateway). |
| Azure Virtual WAN | A Microsoft-managed networking service that brings many networking, security and routing features together to provide a single operational interface. It builds a hub-and-spoke network that can reach several Azure regions and on-premises locations. |
| Virtual WAN hub | A Microsoft-managed virtual network that is the core of your network in a region. Hubs in a Standard Virtual WAN are connected to each other. |
| Address space and CIDR | The address space of a virtual network is the range or ranges of IP addresses it uses. CIDR notation writes a range as an address, a slash and a number, for example 10.0.0.0/16. A bigger number after the slash means a smaller range. Example sizes are /24 for 256 addresses, /22 for 1,024 and /20 for 4,096. |
| Overlapping address spaces | Two networks that use the same addresses. This creates major contention challenges across on-premises sites and Azure regions. |

## What this design area covers

The goal of network design is to line up your cloud network with your cloud adoption plans. This is one of the eight design areas from [the landing zone introduction post](/azure-landing-zone/what-is-an-azure-landing-zone/), in the environment group. It sets the foundation for networking. It leaves out compliance topics such as advanced network security and automated enforcement guardrails, which are covered in the security and governance design areas (see [the security post](/azure-landing-zone/security/) and [the governance post](/azure-landing-zone/governance-and-azure-policy/)).

## The three management groups and the network

Here is how each of these groups relates to the network:

| Management group | Its job for the network |
|---|---|
| Connectivity | Holds dedicated subscriptions for connectivity, commonly a single one. They host the networking resources the platform needs, such as Azure Virtual WAN, virtual network gateways, Azure Firewall and Azure private DNS zones. Hybrid connectivity to on-premises, for example through ExpressRoute, is set up here. |
| Corp | For workloads that need connectivity, or hybrid connectivity, with the corporate network, through the hub in the connectivity subscription. They are in the same routing domain (a group of networks that can send traffic to each other, as in [the resource organization post](/azure-landing-zone/resource-organization/)). Internal systems are not exposed directly to the internet, though they may be exposed through reverse proxies (servers that sit in front of an application and pass traffic on). |
| Online | For public-facing resources such as websites, online shops (e-commerce applications) and customer-facing services. Keeping them apart from the rest of Azure reduces the attack surface, which means the ways an attacker could get in. |

A simple way to remember it: Corp is internal-facing (private) and Online is public-facing (public, internet). In the conceptual landing zone architecture, the virtual network in Online can optionally be peered with virtual networks in Corp, directly or through the hub with an Azure Firewall or an NVA in the path, so public-facing resources can communicate with internal ones in a secure and controlled way. Also review the Azure Policy assignments that each management group has or inherits, because they shape and protect what is deployed there ([the governance post](/azure-landing-zone/governance-and-azure-policy/)).

## Two topologies, and how to choose

There are two approaches: one based on Azure Virtual WAN, and a traditional hub-and-spoke. In the traditional one, you manage the routing and security. Virtual WAN is a service that Microsoft manages. A spoke is a workload virtual network that connects to the hub, which is the central virtual network ([the platform scope post](/azure-landing-zone/platform-scope-and-workload-boundaries/)).

Two terms for the table. A site-to-site VPN connects an on-premises network, such as a branch (a remote office, see [the business requirements post](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/)), to Azure over an encrypted IPsec tunnel, through a VPN device. SD-WAN (software-defined WAN) is a partner technology that Virtual WAN works with to connect branch locations to Azure.

| | Traditional hub-and-spoke | Azure Virtual WAN |
|---|---|---|
| Use it if any of these apply | You deploy in one or several regions, expect some traffic between regions but do not need every region connected to every other. You have few branches per region, with fewer than 30 site-to-site IPsec tunnels. You want full control and detail to configure routing by hand. | You deploy in several regions and need global connectivity between virtual networks and several on-premises locations. You want to connect a large branch network with SD-WAN, or need more than 30 branch sites for native IPsec termination. You need transit between a VPN and ExpressRoute. |

Two more points:

- Hub-and-spoke also fits when the main hybrid connection is ExpressRoute and you have fewer than 100 VPN connections per VPN gateway, and when you depend on central NVAs and detailed routing. I read these numbers as measuring different things from the 30 above (tunnels and branch sites against connections per gateway), so check your own counts against each. [The business requirements post](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/) gave the 30-branch and 30-tunnel figures too.
- Use Virtual WAN if you need hub-and-spoke across more than two Azure regions, global transit between landing zone virtual networks, and you want to minimize network management overhead.

## Traditional hub-and-spoke: the recommended design

How the pieces connect:

- A virtual network cannot cross a subscription boundary. To connect virtual networks in different subscriptions you can use peering, an ExpressRoute circuit (the ExpressRoute connection between your network and Microsoft, see [the business requirements post](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/)) or VPN gateways. Peering is the preferred way, and it works in the same region, across regions and across Microsoft Entra tenants. You pay a nominal fee for traffic over a peering.
- Peering alone does not let one spoke reach another: both are peered with the hub, but traffic does not pass through the hub by itself. For spoke-to-spoke traffic, use NVAs and UDRs, which send the traffic to the firewall or NVA in the hub.
- You can apply NSGs (network security groups: sets of security rules that allow or deny network traffic to or from several types of Azure resources, so you can filter traffic in a virtual network) in either peered virtual network to block access to other virtual networks or subnets.
- BGP (Border Gateway Protocol) lets an on-premises gateway and an Azure gateway exchange routes. VPN gateways that use BGP are transitive within Azure and on-premises networks. By default they do not give transitive access to networks connected through ExpressRoute.
- If you need transit between ExpressRoute and VPN in a hub-and-spoke network, use Azure Route Server. It is a service that lets an NVA and the virtual network exchange routes through BGP, so you do not set up or maintain route tables by hand.
- Route propagation means routes learned through BGP are added to the route tables of subnets automatically. A route table can switch that off.

What goes in the hub:

- A minimal set of shared services, including ExpressRoute gateways, VPN gateways (as required), and Azure Firewall or partner NVAs (as required) to protect and filter traffic. If necessary, also Active Directory domain controllers and DNS servers. Azure private DNS zones sit in the Connectivity subscription.
- Use a single DDoS Protection plan in the connectivity subscription for all landing zone and platform virtual networks. A DDoS (distributed denial of service) attack tries to use up an application's resources so real users cannot reach it. Azure DDoS Protection helps protect resources in a virtual network. Its plans cover only resources that have public IP addresses (addresses reachable from the internet). One plan can be shared across the virtual networks in a tenant.
- For regional deployments, a hub in each region with the spokes of that region peered to it. Put each region's hub resources in their own resource groups.

If you have several regions, pick by how many landing zones need cross-region traffic:

- To connect a few landing zones across regions, use global virtual network peering directly between them. That traffic skips the hub NVAs, and global peering has traffic fees.
- To connect most landing zones across regions, use hub NVAs to join the hubs and route traffic across regions. You can also use this if direct peering would break your security needs. Global peering or ExpressRoute can join the hubs. ExpressRoute can add latency (delay, [the business requirements post](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/)), and the gateway size limits throughput (how much data can pass, [the business requirements post](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/)).
- To join two regions, global peering between the hubs works. Beyond two regions, use Virtual WAN, or connect the hubs to the same ExpressRoute circuits.
- If you use ExpressRoute between regions, spokes in different regions can communicate directly and bypass the firewall, because they learn through BGP the routes to the remote spokes. To keep the firewall in the path, add more specific routes to the spoke UDRs that point to the firewall in the local hub, or turn off BGP route propagation on the spoke route tables.

Limits and tools: check two limits when you connect spokes to the hub: the maximum number of peerings per virtual network, and the maximum number of address ranges (prefixes) that ExpressRoute private peering advertises from Azure to on-premises. Private peering is the ExpressRoute connection to your private virtual networks. Also use Azure Virtual Network Manager (an extra tool recommended alongside the topologies, not a topology itself) to manage connectivity and security configuration across subscriptions.

## Virtual WAN: the recommended design

Virtual WAN is a hub-and-spoke network in which Microsoft runs the hubs. It reduces overall network complexity. Transit works in a region and across regions between any two connected parts: virtual network to virtual network, virtual network to branch, branch to virtual network, and branch to branch.

- Use one or more Virtual WAN hubs per Azure region. If one hub's limits are not enough, you can add more hubs in the same region.
- Put all Virtual WAN resources, Azure Firewall and the DDoS plan in the connectivity subscription, and keep all Virtual WAN resources in one resource group. The portal needs them deployed together.
- Each spoke virtual network connects to a hub through a hub virtual network connection (the official diagram labels it "VWAN Hub Connection"). One virtual network can connect to only one hub.
- Hubs hold only Microsoft-managed resources: gateways (point-to-site VPN, which connects individual users through a VPN client on their computer, for secure remote access from many locations, site-to-site VPN and ExpressRoute), Azure Firewall through Azure Firewall Manager (the tool that configures security and routing policies in a hub), route tables and some NVAs for partner SD-WAN features. Your own shared services, such as DNS servers, go in a dedicated spoke virtual network, not inside the hub.
- Connect ExpressRoute to the hub, branches to the nearest hub with site-to-site VPN or an SD-WAN partner, and individual users with point-to-site VPN.
- Use virtual hub routing (route tables in the hub that you can customize) to control and segment traffic between virtual networks and branches. Keep Azure traffic on the Microsoft backbone, and filter internet-bound traffic with Azure Firewall.
- A secured virtual hub is a hub with security and routing policies added. Secured virtual hubs do not support Azure DDoS standard protection plans. The plan is for your landing zone and platform virtual networks, so I read this as: it protects those, not the hub.

## IP addressing: plan it before you build

Plan IP addressing in advance so that address space does not overlap across on-premises locations and Azure regions. Guidance:

- Use RFC 1918 private addresses (the ranges set aside for private networks: 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16). Do not use these special ranges: 224.0.0.0/4 (multicast), 255.255.255.255/32 (broadcast), 127.0.0.0/8 (loopback), 169.254.0.0/16 (link-local) or 168.63.129.16/32 (internal DNS).
- Do not use public IP addresses for virtual networks, especially ones your organization does not own.
- Do not create virtual networks without planning the space you need, and do not create large ones such as /16, so address space is not wasted.
- Azure reserves five addresses in each subnet, so count them when you size subnets. Some services, such as Azure Firewall and VPN Gateway, need their own dedicated subnet.
- You can add address space to a virtual network later. If it is peered, each peer needs a resync afterwards (a sync step that you run in the Azure portal or with Azure PowerShell), and this needs no outage.
- If private addresses are scarce, consider IPv6 (a newer kind of IP address, much longer than the older IPv4 kind, so there are far more of them). A virtual network can be IPv4-only or dual stack, which means both IPv4 and IPv6.
- Consider an IPAM tool (an IP address management tool, which gives central management and visibility of IP address use and helps prevent overlaps) that has an API for reserving non-overlapping address space, so it can plug into subscription vending ([the resource organization post](/azure-landing-zone/resource-organization/)). An example is simple sizes that workload teams can ask for: small /24, medium /22 and large /20.
- When a workload is decommissioned, release its address space so it can be reused.

## The two network topologies at a glance

![Two network topologies. Top: traditional hub-and-spoke, with two regional hub virtual networks in the Connectivity subscription peered to spoke virtual networks in a workload landing zone subscription. Bottom: Azure Virtual WAN, with two Virtual WAN hubs in the Connectivity subscription connected to the same spoke virtual networks](/diagrams/post-10-hub-spoke-and-virtual-wan.svg)

*Simplified diagram, redrawn by me to follow the layout of the two topology diagrams in the official documentation (a Connectivity subscription on the left, a workload landing zone subscription on the right): [Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology) and [Virtual WAN network topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology). Not an official Microsoft diagram; the official ones are on those pages. Region N means any further region. A Virtual WAN hub with security and routing policies from Azure Firewall Manager is a secured virtual hub; here that is Azure Firewall. Both topologies in my redraw show UDRs and NSGs in the spoke virtual networks. The words "private zones" come from the design area page. I left out Azure Firewall policies, the DNS Private Resolver, the monitoring and management icons, resource groups, application components and the compliant virtual machine templates. Icons are from the official [Azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) architecture icon set.*


## Common mistakes

- **Overlapping IP address spaces.** This creates major contention challenges, so plan non-overlapping space across Azure regions and on-premises in advance.
- **Treating peering as transitive.** Peering is not transitive, so spoke-to-spoke traffic needs UDRs and an NVA or firewall in the hub.
- **Spokes that skip the firewall.** With ExpressRoute between regions, spokes learn routes to remote spokes through BGP and can bypass the firewall. Add more specific UDRs or turn off BGP propagation on spoke route tables.
- **Too much in the hub.** Keep a minimal set of shared services there. In Virtual WAN, your own shared services cannot go inside the hub at all.
- **A DDoS plan per network.** Use a single DDoS Protection plan in the connectivity subscription for all landing zone and platform virtual networks.
- **Address space guessed at the start.** Do not create virtual networks without planning the space, and do not create large ones such as /16.
- **Forgetting limits.** Check the peering and route limits before you add spokes, and Virtual WAN limits before you plan hubs.
- **Choosing the topology without checking the numbers.** Choose from your requirements. Some numbers (30 branch sites, 30 tunnels, more than two regions) tip the choice.

## From my own projects

I have seen a firewall deployed while traffic still did not go through it, peering treated as if it were transitive, and overlapping IP ranges. I have also seen private DNS and name resolution problems, address space created by guess, and workload servers placed in the hub. These showed up as long troubleshooting, security gaps, and redesign work.

Agreeing the topology, the address plan, the internet exit path and the DNS path before the first workload arrives helps avoid problems like these.

## The files in my repo

- Network topology and connectivity, with hub and spoke responsibilities and the decisions to make before deployment: [networking.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/networking.md)
- Hub-spoke, Virtual WAN, VPN and ExpressRoute, with the questions to ask before choosing: [connectivity-options.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/connectivity-options.md)

## Sources

Microsoft Learn, checked October 2026: [Network topology and connectivity](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/network-topology-and-connectivity) · [Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology) · [Virtual WAN network topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology)

