---
title: "Google Cloud Network Design with Shared VPC"
layout: post.njk
permalink: /google-cloud/network-design-with-shared-vpc/
order: 405
part: 5
tags: gcp-lz
deck: "Choose one of the four network designs for a Google Cloud landing zone and explain how host projects and service projects share one network."
---

This article is for people who plan the network of a Google Cloud landing zone. After reading it you can name the four common network designs, follow the questions that pick one, and explain how a host project and its service projects share a network. You can also say why one Shared VPC network for each environment is the design recommended for most use cases.

Projects, folders and the organization are explained in [Organization, Folders and Projects](/google-cloud/organization-folders-and-projects/). Roles are explained in [Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). Firewall rules and internet access have their own article: [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/). Virtual machines are covered in [Compute Engine in a Landing Zone](/google-cloud/compute-engine-in-a-landing-zone/).

## Key terms

| Term | Meaning |
|---|---|
| VPC network | Short for Virtual Private Cloud network. Shared VPC connects resources from multiple projects to a common one. |
| Shared VPC | Lets an organization connect resources from several projects to one common VPC network, so they talk to each other with internal IP addresses. You designate a project as a host project and attach one or more service projects to it. |
| Host project | A project that contains one or more Shared VPC networks. A Shared VPC Admin (see below) must enable it first. |
| Service project | Any project that a Shared VPC Admin has attached to a host project. It is a common practice to have multiple service projects operated and administered by different departments or teams in your organization. |
| Standalone project | A project that does not take part in Shared VPC. It is neither a host nor a service project. |
| Shared VPC Admin | Someone who has the roles `compute.xpnAdmin` and `resourcemanager.projectIamAdmin`, granted on the organization or on one or more folders. They enable host projects, attach service projects and delegate access to subnets. |
| Shared VPC network | A VPC network defined in a host project and made available as a centrally shared network. |
| Compute Network User | The role `compute.networkUser`. A Service Project Admin (see Who does what below) holds it to use subnets of the host project. |
| Network Admin | The role `compute.networkAdmin`. Full control over network resources except firewall rules and SSL certificates. |
| Dedicated Interconnect | A Dedicated Interconnect connection is a direct link between your on-premises network and Google Cloud. |
| Hub-and-spoke | A hub VPC network connects to on-premises networks, and spoke VPC networks contain the workloads (option 3). In option 2 the hub also holds appliances that traffic between spokes passes through. |
| Private Service Connect | Used in option 4. A Private Service Connect endpoint is attached to a service attachment in the VPC network where the service is located. Option 4 fits when workloads communicate with each other and the on-premises environment only through defined endpoints. |

## What Shared VPC does

Shared VPC lets an organization connect resources from several projects to one common VPC network. You designate a project as a host project and attach one or more service projects to it.

The diagram shows the design called option 1, described in the next sections.

![On-premises network in two locations connects to a group of redundant Cloud Interconnect instances. The group connects to production and development Shared VPC networks, each in a host project with service projects. No traffic between environments.](/img/google-cloud/google-cloud-network-design-shared-vpc.svg)

*Source: [Decide the network design for your Google Cloud landing zone](https://docs.cloud.google.com/architecture/landing-zones/decide-network-design).*

- The host project holds the Shared VPC network and the networking resources shared with the service projects. Network resources such as subnets, routes and firewalls are controlled centrally.
- Service projects are attached to the host project. Teams put their workloads in them.
- Each service project can be attached to only one host project. You can have several host projects.
- A project cannot be a host project and a service project at the same time.
- Host and service projects cannot belong to different organizations, except while projects are being moved from one organization to another. They can sit in different folders, but the admin needs Shared VPC Admin rights on both folders.
- A host project can share all its subnets, including those in future networks, or only chosen subnets.
- An existing virtual machine (VM) instance in a service project cannot be changed to use a Shared VPC network. Create a new one.
- Charges for a resource go to the service project where the resource is, even when it uses the host project's network. Outbound traffic through the VPN gateway is attributed to the host project, whichever service project starts it.

### Who does what

| Role | What it does |
|---|---|
| Organization Admin (`resourcemanager.organizationAdmin`) | Nominates Shared VPC Admins. |
| Shared VPC Admin (`compute.xpnAdmin` and `resourcemanager.projectIamAdmin`) | Enables host projects, attaches service projects and delegates access to subnets. |
| Service Project Admin (Compute Network User, `compute.networkUser`) | Uses the subnets of the host project. It can be granted for the whole host project or for chosen subnets only. |
| Network Admin (`compute.networkAdmin`) | Controls network resources, except firewall rules and SSL certificates. |
| Security Admin (`compute.securityAdmin`) | Manages firewall rules and SSL certificates. |

If you share chosen subnets only, only those subnets are shared until you change the list. A new subnet is not shared until you add it.

## The four network designs

The choice depends mainly on four things:

- **Control.** Central control of IP addressing, routing and firewalls, or team autonomy over their own environments.
- **Connectivity.** All designs connect to on-premises through Cloud VPN or Cloud Interconnect. Some designs need multiple connections set up in parallel, and others use the same connection for all workloads.
- **Security.** Whether traffic between workloads must be inspected by centralized network appliances, such as next-generation firewalls (NGFW). The decision questions call this Layer 7 inspection using network appliances.
- **Scalability.** The number of workloads and of resources such as virtual machines (VMs) and internal load balancers.

| Option | Design | Use it when | Avoid it when |
|---|---|---|---|
| 1 | One Shared VPC network for each environment | You want central control of firewall and routing rules, a simple and scalable setup, and central IP address management. | Teams need full autonomy over their own firewall rules, routing and peering, or you need Layer 7 inspection with NGFW appliances. |
| 2 | Hub-and-spoke with central appliances | You need Layer 7 inspection between workloads or applications, or your company requires a specific security appliance vendor. | Most workloads do not need Layer 7 inspection, workloads must not talk to each other at all, or you only need inspection for traffic to on-premises networks. |
| 3 | Hub-and-spoke without appliances | Workloads should not talk to each other over internal IP addresses but should share on-premises connectivity, and teams should manage their own firewall and routing rules. | You need Layer 7 inspection between workloads, you want central routing and firewall management, or on-premises services must reach managed services connected through another peering, because VPC Network Peering is non-transitive. |
| 4 | Consumer-producer model with Private Service Connect | Workloads only communicate with each other and the on-premises environment through defined endpoints, and teams need independence over IP space, firewalls and routing. | Communication uses many ports or channels that change often, protocols other than TCP or UDP, or Layer 7 inspection. |

### How to pick one

Answer the questions in order until you reach an option.

1. Do you need Layer 7 inspection between workloads using appliances? If yes, choose option 2. If no, go to question 2.
2. Do many workloads need on-premises connectivity? If yes, go to question 4. If no, go to question 3.
3. Can workloads talk through private endpoints in a producer and consumer model? If yes, choose option 4. If no, go to question 4.
4. Do you want to manage firewalling and routing centrally? If yes, choose option 1. If no, choose option 3.

Several designs may suit you, and the best fit can combine parts of more than one.

## Option 1 in more detail

Option 1 is the design recommended for most use cases. You make a separate Shared VPC network for each environment, for example development, testing and production. This centralizes network management and keeps environments apart.

- Traffic between environments is blocked by design. If data must move between them, use controlled on-premises channels or services such as Cloud Storage or Pub/Sub.
- Avoid connecting separated environments directly with VPC Network Peering. It increases the risk of accidentally mixing data and of hitting VPC quotas.
- Firewall rules are managed centrally in the host project.

## Other designs

- Option 2 puts network virtual appliances (NVA), such as next-generation firewalls (NGFW), in a hub VPC network behind a load balancer called an internal passthrough Network Load Balancer. Spoke VPC networks send traffic through those appliances. Keep the appliances in the same region as the workloads. For several regions, use one appliance set and hub VPC network for each environment in each region. Cloud VPN can connect spokes when you reach peering limits, at extra cost and complexity.
- Option 3 has no appliances. A hub VPC network connects to on-premises through Cloud Interconnect, and spokes connect to the hub with VPC Network Peering. VPC Network Peering is non-transitive, so spoke networks cannot communicate with each other directly. Peering connection limits cap how far it scales, so large organizations with many workloads typically avoid it. Cloud VPN can replace peering to allow more spokes, and with custom advertised routes it can also give spokes a path to each other.
- Option 4 gives each team or workload its own VPC network, which can also be a Shared VPC network. A Private Service Connect endpoint is attached to a service attachment in the VPC network where the service is located.

## How the enterprise foundations blueprint does it

The blueprint describes the structure of VPC networks, IP address space, DNS and firewall policies. It offers two topologies. Separate Shared VPC networks for each environment fit when you do not want direct network connectivity between environments. Hub-and-spoke fits when you want connectivity between environments that is filtered by a network virtual appliance (NVA).

- The blueprint names its environments development, non-production and production. The hub-and-spoke topology adds a hub environment. Each Shared VPC network has two subnets, each in a different region.
- In the hub-and-spoke variant, the environment networks connect to a hub network with VPC Network Peering, and an NVA in each region controls traffic between environments.
- Projects follow one of three patterns. Shared VPC service projects are attached to a host project. Floating projects are not connected to other VPC networks in the topology. Peering projects create their own VPC networks and peer them to other VPC networks in the topology.
- The blueprint recommends Dedicated Interconnect for hybrid connectivity. A Dedicated Interconnect connection is a direct link between your on-premises network and Google Cloud.
- The blueprint does not allow inbound or outbound traffic between its VPC networks and the internet.

## Best practices

- Use custom mode VPC networks and delete the default network, for better control over your network's IP addresses. The organization policies in [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/) can help enforce this.
- Use Cloud NAT for resources that need internet access, and Cloud Load Balancing to reduce public IP addresses. Hierarchical firewall policies apply firewall policies across the organization or folders. Both are covered in [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/).
- For Cloud Interconnect, use redundant connections. Cloud VPN is an alternative.
- Enforce organization policies that restrict direct internet access from VPC networks.
- Follow DNS best practices for hybrid DNS between on-premises and Google Cloud.

## Common mistakes

- Connecting development and production directly with VPC Network Peering. Avoid it; option 1 avoids this.
- Treating a project as both a host and a service project. A project cannot be both.
- Attaching one service project to two host projects. Each service project attaches to only one.
- Keeping the default network.
- Planning to switch an existing VM instance onto a shared network. It cannot be reconfigured, so create a new one.
- Expecting Network Admin to manage firewall rules. Network Admin has full control of network resources except firewall rules and SSL certificates. Those belong to Security Admin. A service project admin needs Compute Network User to use the shared subnets.
- Picking option 3 when you need central control of routing and firewall rules.

## How to check this in your own project

1. Write down your answers to the four decision questions and note which option they lead to.
2. List the host projects and the service projects attached to each. A Shared VPC Admin attaches service projects.
3. Check each service project: it must be attached to only one host project.
4. Check each VPC network in the host projects: is it custom mode, and is the default network gone?
5. For each service project admin, check whether Compute Network User is granted on the whole host project or on chosen subnets. With chosen subnets, check whether new subnets still need to be added.
6. Check that no VPC Network Peering joins your production and development networks.

## Sources

- [Decide the network design for your Google Cloud landing zone](https://docs.cloud.google.com/architecture/landing-zones/decide-network-design)
- [Shared VPC](https://docs.cloud.google.com/vpc/docs/shared-vpc)
- [Networking (enterprise foundations blueprint)](https://docs.cloud.google.com/architecture/security-foundations/networking)
