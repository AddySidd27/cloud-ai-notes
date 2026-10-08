---
title: "Business Requirements: Compliance, Region, Recovery, Connectivity and Cost"
slug: "business-requirements-compliance-region-recovery-connectivity-and-cost"
series: "Azure Landing Zone"
part: ""
post_number: 5
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-principles"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/landing-zone-multinational"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/regions"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-business-continuity-disaster-recovery"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/manage/protect"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/migration/migrate-from-on-premises-platform-landing-zone"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/network-topology-and-connectivity"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/define-an-azure-network-topology"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/governance"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/tailoring-alz"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/track-costs"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/reliability/concept-business-continuity-high-availability-disaster-recovery"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/reliability/regions-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-sovereign-clouds/data-controls"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/compliance/regulatory/offering-pci-dss"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-ad-define"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/backup/backup-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-about"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/dmz/secure-vnet-dmz"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/architecture/secure-fundamentals"
    checked_on: "2026-10-07"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/01-foundations/design-principles.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/governance.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/multi-region.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/business-continuity.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/connectivity-options.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/naming-tagging-cost.md"
diagrams:
  - file: "../diagrams/post-05-requirements-to-landing-zone.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/"
    icons: "Azure Public Service Icons V24 (Management groups, Policy, Virtual networks), unmodified"
    source: "../diagrams/post-05-requirements-to-landing-zone.drawio"
production_section_written_by_addy: true  # from Addy's own taps, 2026-10-07; wording drafted by Claude, Addy to review
layout: post.njk
permalink: "/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/"
order: 5
deck: "Before you build a landing zone, you write down what the business needs, and five common requirements (compliance, region, recovery, connectivity and cost) each change a specific part of the landing zone."
next_num: "6"
next_title: "Billing and the Microsoft Entra Tenant, in Depth"
tags: [alz]
---



## 1. The problem

Microsoft's guidance starts with a simple step: before you build a platform landing zone, define your organization's requirements across the design areas. Those decisions determine how you design the landing zone.

When teams skip this step, gaps can show up late. Microsoft's pages call out three of them:

- **Region rules added late.** Microsoft says to build data residency and region requirements into the baseline policy (the starting set of policies) from the start, rather than adding them later.
- **Connectivity not planned.** Hybrid connectivity (a link between your own network and Azure) is, in Microsoft's words, one of the few platform prerequisites that can block all workloads at once.
- **No guardrails for compliance.** Without Azure Policy guardrails, keeping environments compliant takes more operational and management effort.

This post covers five requirements and shows which part of the landing zone each one changes. Microsoft does not publish one page that lists these five together. I group them because Microsoft's Learn pages cover each one as an input to the landing zone design. The grouping is mine. The facts below come from Learn pages.

## 2. Simple explanation

### Words you need first

| Word | What it means |
|---|---|
| Microsoft Entra tenant | One instance of Microsoft Entra ID for one organization. It holds the organization's users, groups and devices. |
| Subscription | A logical unit of Azure services. It is the boundary within which resources are created, managed and billed. |
| Management group | A level above subscriptions where you apply rules. Every subscription under it inherits those rules. |
| Azure Policy | An Azure service that enforces your organization's standards on resources and checks whether resources follow them. |
| Policy definition | A business rule that Azure Policy uses to check resources. |
| Policy assignment | A policy definition applied to a chosen level, such as a management group or a subscription. Everything below that level inherits it. |
| Policy exemption | A way to leave a resource, or a group of resources, out of a policy's checks. |
| Azure RBAC | Azure role-based access control. It manages who can access Azure resources and what they can do with them. A role assignment is how someone is given that access. |
| Azure Resource Manager | Azure's built-in management layer. It is one consistent control layer that applies across all Azure resources. |
| Azure region | One or more datacenters connected by a fast network. |
| Data residency | A rule about which part of the world your data must stay in. In Azure, each geography (a group of regions, such as the United States or Europe) is a data residency boundary. |
| Regulatory requirements | Rules that come from laws or standards. Learn says they typically cover data protection, where data is stored, how data moves, keeping systems separate, and staff clearance. |
| PCI DSS | The Payment Card Industry Data Security Standard. It is a global security standard designed to prevent fraud by controlling credit card data more tightly. |
| Baseline policy | The starting set of policy assignments that prevent risk before workloads arrive. |
| Allowed locations policy | An Azure Policy that blocks deployments to every region that is not on your list of allowed regions. |
| RTO (recovery time objective) | The longest downtime you can accept for a workload after a disaster. |
| RPO (recovery point objective) | The longest period of data loss you can accept after a disaster, such as "30 minutes of data". |
| Disaster recovery | Planning how you respond to a disaster. Learn defines a disaster as a rare, major event with a bigger and longer impact than the application can handle with its normal resilience. |
| Azure Backup | An Azure service that protects your data and lets you restore it when you need to. |
| Azure Site Recovery | An Azure service that keeps copying virtual machines to a second location. During an outage you switch to the copy (fail over), and later you switch back (fail back). |
| Hybrid connectivity | A connection that links your on-premises network (the network in your own buildings) to Azure. |
| VPN Gateway | Sends encrypted traffic between an Azure virtual network and your on-premises locations over the public internet. |
| ExpressRoute | A private connection from your on-premises networks to the Microsoft cloud, set up with a connectivity provider. It does not use the public internet. |
| Hub-and-spoke network | A pattern with one central virtual network (the hub) connected to many others (the spokes). The spokes connect to the hub and can keep workloads apart. |
| Azure Virtual WAN | A Microsoft-managed networking service that brings many networking, security and routing functions together in one place. |
| Budget | A spending target in Azure Cost Management. It sends you alerts. It does not stop your resources or your spending. |
| Tags | Labels you add to resources, each with a name and a value, such as Environment = Production. They help you find resources and track cost. |

### Ask five questions

For each requirement, ask one question, and know which part of the landing zone it changes. This table is my own summary.

| Requirement | The question to ask | What it changes in the landing zone |
|---|---|---|
| Compliance | Which rules must we follow, and for which workloads? | Azure Policy assignments, and where subscriptions sit in the management group hierarchy |
| Region | Where may our data live, and in which regions will we deploy? | An allowed locations policy, and a network hub in each region you use |
| Recovery | How much downtime and data loss can each workload accept? | Backup and disaster recovery design, in the Protect & Recover part of the Management design area |
| Connectivity | How do users and workloads reach Azure and on-premises? | The hub network, the hybrid connection and the topology, in the Connectivity subscription |
| Cost | Who owns the spending, and how do we see it? | Budgets and alerts at management group or subscription level, and tags on resources |

### Compliance: which rules apply, and where

Regulatory requirements typically cover data protection, data residency, data transfers, isolation or personnel clearance. Microsoft's steps are:

- Decide which Azure policies you need, based on your business controls or compliance regulations.
- Map the regulatory and compliance requirements to Azure Policy definitions and Azure role assignments.
- Keep checking compliance with reporting and auditing.

Scope matters. If a rule applies to only some workloads, it should not apply to all workloads. Microsoft's example is PCI DSS: create a management group called PCI under the Landing zones management group, assign the extra policies there, and place the subscriptions that need them in that group. They inherit the policies. Post 9 covers the hierarchy in detail.

Some organizations must meet conflicting rules in several countries. Microsoft says you do not need to change the landing zone when the rules need identical policy assignments, when one rule's controls are a superset of the other's, when the assignments do not overlap, or when you can choose the implementation that suits you. If the rules produce conflicting policy controls, you must adjust the landing zone architecture and the policy assignments. The more conditions a regulation has, the more the landing zone needs to change.

Microsoft recommends one Microsoft Entra tenant for most scenarios, including multinational ones. If you do not need separate tenants for strict isolation, it suggests deploying more than one landing zone in the same tenant and adjusting the management group hierarchy. Whatever you choose, Microsoft says to keep policy assignments, exceptions and exemptions as few as possible.

### Region: where data lives, and where you deploy

The landing zone architecture is region-agnostic, but you must choose the regions to deploy to. Three points:

- **Put region rules in the baseline.** If data residency rules apply, Microsoft says region restriction is a compliance control, so build it into the baseline policy, for example with an allowed locations policy, instead of adding it later.
- **Design the platform for more than one region.** Even if your workloads use one region today, Microsoft says to design the platform to support several, especially connectivity, identity and management, so you can enable multi-region workloads quickly.
- **Do not build management groups by region.** Microsoft says you should not create a management group structure based on regions. Subscriptions are not tied to a region either.

When you add a region later, Microsoft's list includes two changes: update the allowed locations policy to allow the new region, and add a network hub in the new region, in your existing Connectivity subscription.

### Recovery: how much downtime and data loss

Microsoft says to capture platform disaster recovery requirements first, and then design business continuity and disaster recovery. The inputs are the RTO and RPO of each workload. Data residency matters here too, because it affects where you can replicate data across regions.

How do you get an RTO and an RPO? Microsoft's guidance starts by giving each workload a priority (high, medium or low) based on how important it is to the business and how much money is invested in it. Then you set an uptime target for each priority. The RTO is worked out from that target: you divide the downtime the target allows in a year by the number of failures you expect in a year. For example, 52 minutes a year with 4 expected failures gives an RTO of 13 minutes or less. The RPO comes from how much data loss the business can accept. Microsoft's rules after that:

- The time it takes to recover must be less than your RTO.
- Test your failover (moving traffic to a second deployment in another location when the main one is hit by a disaster) and failback (restoring operations in the main region after it has recovered) regularly, to confirm you meet your RTO and RPO.
- Backups must support the RTO and RPO of each workload.

For tools, Microsoft recommends Azure Backup, Azure Site Recovery for virtual machine recovery between Azure regions, and the native disaster recovery features of platform services.

### Connectivity: how people and workloads reach Azure

If your plans include hybrid dependencies, Microsoft says your network design should include those connection options and the traffic patterns you expect. In the landing zone, the hub network and its hybrid connection are built in the Connectivity subscription, which sits under the Connectivity management group (the platform management group for shared networking).

Three points from Microsoft's guidance:

- **Do not leave it late.** Hybrid connectivity is one of the few platform prerequisites that can block all workloads at once. If you migrate a workload before connectivity is stable, you might not be able to reach it.
- **Choose VPN Gateway or ExpressRoute from your needs.** Microsoft lists throughput (how much data can pass), latency sensitivity (how much delay you can accept), compliance requirements, lead time tolerance and routing complexity. It says not to choose based on whether your organization is new to Azure. ExpressRoute can take weeks or months, so run a VPN Gateway in parallel if your migration dates cannot wait.
- **Choose the topology from your needs too.** Microsoft suggests Virtual WAN if you need global connectivity between virtual networks in several Azure regions and multiple on-premises locations, or need more than 30 branch sites (remote offices) for native IPsec termination (IPsec is a standard way to encrypt VPN traffic, and "native" means the encrypted links end directly in Azure). It suggests hub-and-spoke if you have fewer than 30 site-to-site VPN tunnels (encrypted links between your sites and Azure), do not need every region connected to every other region, or want full control of your network routing.

### Cost: who owns the spending

Microsoft's migration guidance says to set budgets and alerts at the management group or subscription level before migration, and to assign an owner to review them. A budget only notifies. It does not stop your resources. It also says not to let the design of a perfect tagging system delay building the management group.

Other points from Microsoft:

- The management group and subscription hierarchy controls Azure Policy, role-based access control and cost reporting. Cost allocation is easier with one subscription per workload, but not every organization does that.
- Choose tags that fit how your organization tracks cost, for example cost center or project name.
- You can use Azure Policy to allow only specific regions and resource types.

### Use the design principles as a guide

Microsoft gives five design principles to guide decisions when requirements change:

1. **Subscription democratization.** Workload teams get and manage their own subscriptions, inside the platform's guardrails.
2. **Policy-driven governance.** Use Azure Policy to provide the guardrails.
3. **Single control and management plane.** Use Azure's one built-in management layer (Azure Resource Manager) for all Azure resources, and avoid extra layers such as custom-built portals.
4. **Application-centric service model.** Focus on applications, rather than only moving virtual machines as they are.
5. **Alignment with Azure-native design and roadmaps.** Use Azure-native services where you can.

Microsoft says you can deviate from them for valid reasons, but you should understand the impact on the design and on future operations, and be ready to balance requirements and functionality. Requirements also change over time. For new technologies, Microsoft's landing zone overview says you update the governance and security policies in the platform landing zone, and they then apply across the workload landing zones.

One more warning: do not spend months or years designing the landing zone without moving any workload. Post 16 covers what to build first.

## 3. Diagram

![Five business requirements on the left, compliance, region, recovery, connectivity and cost, with arrows to the landing zone parts they change on the right: management group hierarchy, Azure Policy, Protect & Recover, Connectivity subscription, and Cost Management and tags](/diagrams/post-05-requirements-to-landing-zone.svg)

*Simplified diagram, my own layout, based on Microsoft Learn: [What is an Azure landing zone?](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) The grouping of the five requirements is my own. Not an official Microsoft diagram. Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/) set.*

## 4. What I have seen in production

### Mistakes to check for first

These come from Microsoft's guidance.

- **Region rules added late.** Build the allowed locations policy into the baseline from the start.
- **Management groups built by region.** Microsoft says not to. Management groups and subscriptions are not tied to a region, so Microsoft says not to build the hierarchy by region.
- **Too many policy assignments and exceptions.** When rules conflict, Microsoft says to keep assignments, exceptions and exemptions as few as possible.
- **No recovery targets, or recovery never tested.** Capture the RTO and RPO of each workload, and test failover and failback.
- **Overlapping IP address ranges (two networks that use the same addresses).** Microsoft says not to overlap IP ranges between production and disaster recovery networks, and to confirm that your on-premises and Azure address spaces do not overlap.
- **Hybrid connection chosen by habit, with no lead time planned.** Choose VPN Gateway or ExpressRoute from your needs, and plan for ExpressRoute lead time.
- **Budgets with no owner.** Set budgets and alerts before migration, and name someone to review them.

### From my own projects

I have seen environments where the requirements were not collected first, where region or data residency rules were decided late, where recovery targets (RTO and RPO) were never defined, and where hybrid connectivity delayed workloads. The effects were rework or redesign, compliance or audit findings, and unexpected cost.

In my view, writing the five requirements down first, with a named owner for each, helps avoid problems like these.

## 5. Repo

- This post: [design-principles.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/01-foundations/design-principles.md)
- Compliance and policy: [governance.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/governance.md)
- Region: [multi-region.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/multi-region.md)
- Recovery: [business-continuity.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/business-continuity.md)
- Connectivity: [connectivity-options.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/connectivity-options.md)
- Cost: [naming-tagging-cost.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/naming-tagging-cost.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Design principles](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-principles) · [Multiple locations](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/landing-zone-multinational) · [Platform landing zone for on-premises experts](https://learn.microsoft.com/en-us/azure/migration/migrate-from-on-premises-platform-landing-zone)

The five-requirement grouping and the summary table are my own explanation.

