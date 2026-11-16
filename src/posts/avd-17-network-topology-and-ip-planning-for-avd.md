---
title: "Choose a Network Topology and Plan IP Addresses for Azure Virtual Desktop"
seoTitle: "AVD Network Topology and IP Planning"
layout: post.njk
permalink: "/azure-virtual-desktop/network-topology-and-ip-planning-for-avd/"
order: 117
part: 17
tags: [avd-series]
deck: "Place AVD in a landing zone, choose hub and spoke or Virtual WAN, and plan address space so that overlap and exhaustion do not stop you later."
description: "Choose a network topology for Azure Virtual Desktop, hub and spoke or Virtual WAN, place it in a landing zone and plan IP address space to avoid overlap and exhaustion."
---

Topology means how your Azure networks are joined to each other and to your own network. Address planning means choosing the IP address ranges for them. These are the two network choices that are hardest to change after users arrive. A subnet (a smaller address range inside a virtual network) that is too small blocks the next image update. A range that overlaps an acquired company's network blocks the VPN (an encrypted link to your network over the internet). The address range of a Virtual WAN hub (the Microsoft-managed network at the center of Virtual WAN) cannot be changed once it is created. None of these is likely to show up in a pilot of ten users.

This article places Azure Virtual Desktop (AVD) in the Azure landing zone model. A landing zone is a ready-made Azure environment for workloads. The article compares hub and spoke with Virtual WAN using the criteria Microsoft gives, and lists the address-planning rules that matter. The [networking article](/azure-virtual-desktop/plan-avd-networking/) covers subnet sizing for one worked example, so this one concentrates on the choices around it.

## Key terms

| Term | Meaning |
|---|---|
| Landing zone | An Azure environment set up with rules (governance), networking, identity and security, so workloads can be placed in it. |
| Platform landing zone | The shared foundation: networking, identity and governance for the whole estate. |
| Workload landing zone | The place a specific workload runs. AVD sits in a workload landing zone. |
| Hub and spoke | A design where a central hub network holds shared services, and spoke networks for workloads connect to it. |
| Peering | A direct link between two virtual networks (private networks in Azure). |
| Transitive | Traffic can pass through one network to reach another. Peering by itself is not transitive. |
| Virtual WAN | A Microsoft-managed networking service that gives global, transitive connectivity across regions and on-premises sites. |
| SD-WAN | Software-defined WAN: software that joins branch offices to a central network over several kinds of link. |
| Virtual hub | The Microsoft-managed network at the center of a Virtual WAN in a region. |
| CIDR | A way to write an address block, such as `10.20.0.0/22`. A smaller number after the slash means a larger block. |
| Overlap | Two networks using the same addresses, so traffic cannot be routed between them. |
| NVA | Network virtual appliance: a firewall or router that runs as a virtual machine. |
| Cloud Adoption Framework (CAF) and Azure Architecture Center | The Cloud Adoption Framework is Microsoft's guidance for adopting Azure. The Azure Architecture Center holds Microsoft's reference designs. |
| Virtual network and subnet | A virtual network is a private network in Azure. A subnet is a smaller address range inside it. Each virtual machine network interface gets its address from one subnet. |
| Subscription | A billing and management boundary in Azure. Landing zones use several subscriptions to separate platform and workloads. |
| Session host, private endpoint | A session host is a virtual machine that runs users' desktops and apps. A private endpoint is a network interface with a private IP address that connects you to an Azure service. |
| User-defined route (UDR) | A route you write to change where traffic from a subnet goes next. |
| Route propagation (BGP) | BGP is a standard way for gateways to tell each other which address ranges they can reach. Route propagation lets a route table learn those ranges automatically. |
| Azure Firewall, VPN Gateway, ExpressRoute | Azure Firewall is Azure's managed firewall. VPN Gateway sends encrypted traffic to your network over the internet. ExpressRoute is a private link between your network and Azure through a connectivity provider. An ExpressRoute circuit is one such link. Private peering is the part of a circuit that carries traffic to your virtual networks. Azure Firewall Manager is the tool that sets up Azure Firewall in a Virtual WAN hub. |
| Route Server | An Azure service that lets a network virtual appliance and the Azure network exchange routes by BGP, so you do not maintain route tables by hand. It can also give transit between VPN and ExpressRoute gateways. |
| Private Link | Lets you reach an Azure service through a private endpoint in your own virtual network instead of its public address. |
| DNS Private Resolver | An Azure service that answers DNS queries between Azure and your own network. It appears in the picture below. |
| IPAM | IP address management: a tool or spreadsheet that records which address ranges are used. |
| Global virtual network peering | Peering between virtual networks in different Azure regions. |
| NAT | Network address translation: swapping one address for another so two networks that use the same addresses can still talk. |
| DNS and domain controller | DNS turns a name into an IP address. A domain controller is a server that runs Active Directory so machines can join a Windows domain. |
| RFC 1918 | The standard that reserves private IPv4 ranges: `10.0.0.0/8`, `172.16.0.0/12` and `192.168.0.0/16`. |
| DDoS Protection plan | An Azure service that protects resources that have public IP addresses against network-layer attacks. |
| Azure Compute Gallery, Log Analytics workspace | A gallery stores and shares VM images. A Log Analytics workspace stores logs and metrics for querying. |

## Where AVD sits

The Azure Architecture Center's [AVD landing zone design guide](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop) says to deploy a Cloud Adoption Framework platform landing zone first, and then deploy AVD into a workload landing zone. In the reference design, AVD uses its own subscription or subscriptions for workload resources (virtual machines, storage accounts, key vaults, private endpoints) and a shared services subscription for things used across AVD workloads (Log Analytics workspaces, Azure Compute Gallery).

The platform provides connectivity, identity and management subscriptions. The connectivity subscription holds the hub networking, Azure Firewall and the ExpressRoute or VPN gateways. The identity subscription holds the domain services for domain-joined session hosts. In this design the AVD workload does not depend on the management subscription, so the workload team builds its own monitoring and automation.

In practice, the network team owns the hub and the address plan, and the AVD team owns the spoke. Settle that line early.

The topology rules below come from the general Cloud Adoption Framework network topology pages, which apply to any workload, not only AVD. The hub range rule comes from the Virtual WAN hub settings.

## Hub and spoke or Virtual WAN

Each topology fits different conditions. Which one fits you is a decision.

| Choose traditional hub and spoke when | Choose Virtual WAN when |
|---|---|
| A single Azure region, or several regions where you do not need transit between networks in different regions, or where global virtual network peering can connect them | You need hub-and-spoke across more than two regions ([Traditional topology page](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology#design-recommendations)) |
| You do not need transit between VPN and ExpressRoute connections (with Route Server you can add it) | You need transit between VPN and ExpressRoute, or global transit between landing zone networks across regions |
| ExpressRoute is the main hybrid link and there are fewer than 100 VPN connections per VPN gateway ([Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology#design-recommendations)). The [Define an Azure network topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/define-an-azure-network-topology) page says fewer than 30 IPsec site-to-site tunnels | You want to minimize network management work |
| You depend on central network virtual appliances and granular routing | You use SD-WAN to bring branch offices into Azure, or need native IPsec for more than 30 branch sites ([Define an Azure network topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/define-an-azure-network-topology)) |

![Left: traditional hub and spoke, a hub with gateway and firewall peered to three spokes. Right: Virtual WAN with a managed hub per region, each linked to a workload network and a DNS spoke. Boxes below say when each fits and list address plan checks.](/img/avd/AVD-Post-17-Topology-Choice-v3.png)

*Source: [Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology).*

Points that change the AVD design:

- **Peering is not transitive.** To get transit through a hub you need user-defined routes and network virtual appliances. That is how a hub firewall sees spoke-to-spoke traffic.
- **Shared services live differently.** In traditional hub and spoke, the hub may hold domain controllers and DNS servers. In Virtual WAN, customer-deployed resources cannot be deployed inside the virtual hub. Put shared services such as DNS servers in a dedicated spoke. Domain controllers are customer-deployed servers too, so they also go in a spoke.
- **Virtual WAN hubs hold Microsoft-managed resources.** That means gateways, Azure Firewall through Azure Firewall Manager, route tables and certain NVAs for SD-WAN.
- **Hub-to-hub across regions.**
  - With two regions in hub and spoke, connect the hubs with global virtual network peering.
  - Beyond two regions, use Virtual WAN, or hubs that connect to the same ExpressRoute circuits.
  - When the hubs are joined through ExpressRoute, spokes in different regions reach each other directly. Their traffic skips the hub firewalls.
  - To make the firewalls inspect that traffic, add more specific routes in the spoke route tables. Or switch off BGP route propagation on them, so the spokes stop learning the remote spoke ranges and send traffic to the firewall instead.
- **Transit between VPN and ExpressRoute.** In hub and spoke you can add Route Server to get it. Virtual WAN does it natively.
- **Limits apply to both.** Check the maximum number of peerings per virtual network and the route limits on ExpressRoute private peering against your spoke count.

Do not choose Virtual WAN for AVD alone. The topology is decided by the whole estate. If the platform team already runs one, place AVD in it. If the choice is yours, use the conditions above. Then test the routing for the AVD paths: session host to the AVD service (outbound, see the [connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/)), session host to DNS, session host to identity, and session host to profile storage. The user's client path runs through the client's own network, not yours.

## Address planning rules

Follow these rules.

- Plan non-overlapping address space across Azure regions and on-premises locations before you build.
- Use private (RFC 1918) addresses.
- Do not use public IP addresses for your virtual networks, especially addresses that do not belong to your organization.
- Do not use these ranges: `224.0.0.0/4` (multicast), `255.255.255.255/32` (broadcast), `127.0.0.0/8` (loopback), `169.254.0.0/16` (link-local) and `168.63.129.16/32` (the planning page labels it "internal DNS"; the [Azure fabric communication IPs](https://learn.microsoft.com/en-us/azure/virtual-desktop/azurecommunicationips) page calls it the Azure platform address). These are listed under design recommendations in [Plan for IP addressing](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/plan-for-ip-addressing). Session hosts must still reach `169.254.169.254` (inside the link-local range) and `168.63.129.16`, so never assign them to your own networks. See the [connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/).
- Do not create large virtual networks such as `/16`, so that address space is not wasted. Treat any `/16` in a worked example as a placeholder.
- The smallest IPv4 subnet Azure supports is `/29` ([Plan for IP addressing](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/plan-for-ip-addressing)).
- Do not create virtual networks without planning the address space.
- Azure reserves five addresses in each subnet ([Plan for IP addressing](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/plan-for-ip-addressing), [virtual network FAQ](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq#are-there-any-restrictions-on-using-ip-addresses-within-these-subnets)), so a `/24` has 251 usable addresses. The [networking article](/azure-virtual-desktop/plan-avd-networking/) shows the sizing.
- Some services need their own subnets, such as Azure Firewall and VPN Gateway.
- You can add address space to a virtual network later. If it is peered, each remote peering needs a resync (a refresh so the peer learns the new range).
- An overlapping on-premises site can be reached through NAT on VPN Gateway or Virtual WAN. Treat that as a workaround, not a plan.
- An IPAM tool, even a spreadsheet, helps prevent overlap. Use T-shirt sizes (fixed small, medium and large request sizes) of `/24`, `/22` and `/20` for workload requests, with an API so address requests fit into subscription creation.
- When a workload is retired, return its address range to the pool.
- If private addresses run short, consider nonroutable spoke virtual networks and Azure Private Link service. IPv6 dual stack is an option, but check which AVD features support IPv6 before you plan on it. See [Plan for IP addressing](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/plan-for-ip-addressing).

For the Virtual WAN hub:

- The minimum hub address space is `/24`, and `/23` or larger is recommended ([About virtual hub settings](https://learn.microsoft.com/en-us/azure/virtual-wan/hub-settings#virtual-hub-address-space)).
- If you use Azure Firewall in the hub, the minimum is `/22`.
- The hub address space cannot be changed after the hub is created.
- It must not overlap with other hubs in the same Virtual WAN, on-premises networks, or any virtual network connected to the hub.

## Three ways address plans fail

These are illustrations, not case histories.

1. **An overlap discovered after a merger.** Two companies each used `10.0.0.0/16`. AVD hosts need to reach the other company's file servers. The fix is renumbering or NAT, both expensive. Check for overlap before you assign ranges, including partner and acquired networks that are not yet connected.
2. **A subnet that cannot hold a rolling update.** In a rolling update you add new hosts from a new image before you remove the old ones. The subnet then holds both sets of network interfaces. The [networking article](/azure-virtual-desktop/plan-avd-networking/) shows the arithmetic. Size for the overlap, with Azure's five reserved addresses taken off.
3. **A hub range that is too small.** A virtual hub's range cannot change. If you later want Azure Firewall in a `/24` hub, the range is already below the `/22` minimum and cannot be changed, so you would be looking at a new hub. Choose the size for what the hub will hold, not what it holds on day one.

Another trap: Private Link needs addresses too. The [Set up Private Link with Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-setup) page notes that IP address allocations can change as demand for addresses increases, so leave headroom for private endpoints. It links to the [Private Link hub and spoke decision tree](https://learn.microsoft.com/en-us/azure/architecture/networking/guide/private-link-hub-spoke-network#decision-tree-for-private-link-deployment) for placing private endpoints in a hub or a spoke.

## Cost drivers

This article gives no prices. Prices change and are on the pricing pages. Ask about these cost drivers in the design:

- **Global virtual network peering** generates traffic fees.
- **A Virtual WAN virtual hub** has pricing from the moment it is created, even without gateways.
- **An Azure DDoS Protection plan** includes protection for 100 public IP addresses ([Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology#design-considerations)). More cost more. It covers only resources that have public IP addresses. Secured Virtual WAN hubs do not support a DDoS Protection plan. See [Virtual WAN network topology in an Azure landing zone](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology).
- **Routing through ExpressRoute between regions** can add latency, and the gateway SKU limits throughput.

Ask the network team which of these your AVD spoke will add to the bill, and who pays.

## Common mistakes

- **Treating the address plan as an AVD decision.** The estate decides it, and the network team often owns it.
- **Using `/16` for a spoke "to be safe".** The guidance is not to waste address space.
- **Forgetting that a spoke needs reachable DNS and domain controllers.** In Virtual WAN, they live in a spoke.
- **Sizing the host subnet for today's host count.** Size for replacement overlap and growth.
- **Choosing the Virtual WAN hub range casually.** It cannot be changed.
- **Relying on NAT to hide an overlap.** It is a workaround.

## How to validate your plan

These are recommended checks on paper before you build anything.

1. List every address range in use or planned: on-premises, other regions, hubs, partner networks, other clouds. Check for overlap.
2. For each AVD host subnet, calculate peak host interfaces plus replacement overlap, then subtract five addresses and compare with the subnet size.
3. For each hub, list what it will hold and check the range against the minimums above.
4. Draw the path from a session host to the AVD service, to DNS, to the domain controllers and to profile storage. Mark the route and the control at each hop.
5. Write down who owns the address plan and how a request for a new range is made.

Next: [How FSLogix Profile Containers Work](/azure-virtual-desktop/how-fslogix-profile-containers-work/).

## Sources

- [AVD landing zone design guide](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop)
- [Plan for IP addressing](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/plan-for-ip-addressing)
- [Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology)
