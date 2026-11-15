---
title: "Platform Scope and Workload Boundaries"
slug: "platform-scope-and-workload-boundaries"
series: "Azure Landing Zone"
part: ""
post_number: 2
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups"
    checked_on: "2026-10-06"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/"
    checked_on: "2026-10-06"
  - url: "https://learn.microsoft.com/en-us/entra/architecture/secure-resource-management"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/domain-services/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/firewall/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/dns/private-dns-privatednszone"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/sentinel/sentinel-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-local/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/dns/dns-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/networking/hybrid-connectivity/hybrid-connectivity"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-sovereign-clouds/digital-sovereignty"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/developer/terraform/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/reliability/regions-overview"
    checked_on: "2026-10-07"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/lab-vs-enterprise.md"
diagrams:
  - file: "../diagrams/post-02-ownership-boundary.svg"
    type: learn-based
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups"
    icons: "Azure Public Service Icons V24 (Management groups, Subscriptions, Microsoft Entra Domain Services, Virtual networks, Azure Firewall, DNS zones, Log Analytics workspaces, Microsoft Sentinel), unmodified"
    source: "../diagrams/post-02-ownership-boundary.drawio"
production_section_written_by_addy: true  # items confirmed by Addy 2026-10-15; wording drafted by Claude
layout: post.njk
permalink: "/azure-landing-zone/platform-scope-and-workload-boundaries/"
order: 2
deck: "The platform is the shared part of Azure that every team uses. A workload is one application and its own resources. Keeping the line between them clear lets many teams share one Azure environment safely."
next_num: ""
next_title: "Tenant, Billing, Subscriptions and Management Groups"
tags: [alz]
---



The platform is the shared part of Azure (identity, network, monitoring, security). A workload is one application and its own resources. When the line between them is not written down, two things can happen.

First, platform and workload mix. A workload team changes a shared network because it is "just one rule". Or the platform team ends up fixing an application because the application's resources sit in a platform subscription. Each change looks small. Together they make the shared foundation hard to trust.

Second, learners mix up a lab and a real landing zone. A lab is a good way to learn the steps. It is not the same as a production environment. If a post, a repo or a resume presents a lab as production, anyone who knows the topic will notice.

This post sets the boundary, and then shows where the learning lab in my GitHub repo stops short of an enterprise design.


## Key terms

Terms from [the landing zone introduction post](/azure-landing-zone/what-is-an-azure-landing-zone/) (tenant, subscription, management group, Azure Policy, inheritance, virtual network, Log Analytics workspace, Microsoft Sentinel, Microsoft Entra Domain Services, platform team, workload team and workload) keep the same meaning here. The new terms are below, in short, plain words.

| Word | What it means |
|---|---|
| Tenant root group | Every tenant has one management group at the very top. By default it is called Tenant root group. |
| Resource group | A container that holds related resources for an Azure solution. It sits inside a subscription. |
| Azure RBAC | Role-based access control. A system that manages who has access to Azure resources, what they can do with them, and where. |
| Role assignment | How access is given. It gives a user, group or app a role (a set of permissions) at a chosen level, such as a management group or a subscription. |
| Azure region | One or more Azure datacenters, connected by a high-capacity, low-latency network. The datacenters of a region are typically in one large metropolitan area. |
| Data residency | Keeping your data inside the geography (for example the United States or Europe) that your rules require. |
| Azure Firewall | A managed network firewall service in Azure. It inspects network traffic to protect your workloads. |
| DNS and private DNS zone | DNS (Domain Name System) turns a service name into a network address. A private DNS zone manages and resolves names inside a virtual network. Its records cannot be looked up from the internet, only from virtual networks linked to the zone. |
| Hub-and-spoke network | A network layout where a central hub virtual network connects to many spoke virtual networks. The spokes connect to the hub and can isolate workloads. |
| Hybrid connectivity | A link between your own networks (on-premises, for example in your datacenter) and your Azure resources, so that systems in both places work together as one network. |
| Azure Local | Microsoft's distributed infrastructure solution that extends Azure capabilities to environments you own, such as your own datacenter. The Learn management groups page calls the Azure Local systems "Azure Local clusters". |
| Terraform and Terraform state | Terraform is an open-source tool that builds cloud infrastructure from configuration files. Terraform state is what Terraform uses to match the deployed resources to those files, so it knows what to add, update or delete. |

In [the landing zone introduction post](/azure-landing-zone/what-is-an-azure-landing-zone/) we said an Azure landing zone has two parts: the platform landing zone and the workload landing zones. Now we look at where each one lives.

## Where the platform lives

Create a management group called Platform. It holds the common platform policies and role assignments. In the standard Azure landing zone hierarchy, an intermediate root management group sits directly under the tenant root group and is the parent of Platform and the other groups. Under Platform, each shared job has its own management group with a dedicated subscription:

| Management group | What its subscription hosts |
|---|---|
| Identity | Identity services, for example Microsoft Entra Domain Services |
| Connectivity | Shared networking resources, for example a firewall and private DNS zones |
| Management | Monitoring, for example a Log Analytics workspace |
| Security | Security tooling, for example Microsoft Sentinel |

The idea is simple: each shared job gets its own subscription, instead of one big pile of shared resources. This lets you apply different policies and role assignments to each area. The Platform group also keeps the billing for common resources in one set of foundational subscriptions. (judgement) I would not combine platform jobs in one subscription.

The full hierarchy, the six-level limit, the default management group and the sandbox group are explained in [Resource organization](/azure-landing-zone/resource-organization/).

## Where workloads live

Workload landing zones are kept apart from the platform, under a separate **Landing zones** management group (the Learn overview page also calls it "Workload landing zones"). Each workload has one workload landing zone, which holds its environments such as dev, test and production, each as one or more subscriptions. Three management groups sit under it:

- **Corp (also called Internal):** for workloads that need connectivity, or hybrid connectivity, with the corporate network. That connection goes through the hub in the connectivity subscription.
- **Online:** for workloads that might need direct internet access, or that might not need a virtual network.
- **Local:** for workloads that run on Azure Local (see Key terms) clusters, and for the clusters themselves. These have different policy requirements from the other groups.

Workload subscriptions inherit the Azure Policy rules applied above them, so workloads get consistent guardrails. For many organizations, Corp, Online and Local are a good starting point. Some add more.

## Two rules that keep the boundary clean

- **Keep workload resources apart from platform resources.** Workload teams manage the workload landing zones. Platform teams manage the platform landing zone.
- **Keep the hierarchy shallow.** Ideally use no more than three to four levels. The six-level limit and the policy-at-the-root advice are in [Resource organization](/azure-landing-zone/resource-organization/).

## The lab in my repo, and where it stops

My repo's lab is for learning the deployment steps. The "core lab" is the basic, hands-on version of that lab, and the repo says plainly not to present it as a complete production landing zone. In the table, "Enterprise target" means what a real organization's design would add. Here is how the lab compares with an enterprise target. The Enterprise target column is my own design choice (judgement), not a Microsoft statement. Later posts cover [identity](/azure-landing-zone/identity-and-access-in-the-landing-zone/), [network](/azure-landing-zone/network-topology-and-connectivity/) and [governance](/azure-landing-zone/governance-and-azure-policy/) in detail.

| Area | Core lab | Enterprise target |
|---|---|---|
| Subscriptions | One existing subscription | Separate platform and workload subscriptions |
| Management groups | Explained; optional controlled exercise | The standard hierarchy, with subscriptions placed in it under control |
| Connectivity | Hub and one spoke | A dedicated connectivity subscription and many workload spokes |
| Firewall | Disabled by default | Enabled only when the approved network design requires it |
| DNS | Azure-provided DNS by default | One central set of private DNS zones, plus DNS lookup between Azure and your own networks where needed |
| Identity | The signed-in person or an app identity | A dedicated identity for automated deployments, extra approval for admin access, regular checks of who has access, and emergency (break-glass) accounts (see [privileged access](/azure-landing-zone/privileged-access-mfa-conditional-access-and-pim/)) |
| Monitoring | One workspace | A central workspace plan, rules that switch logging on, alerts, how long logs are kept, and named owners |
| Policy | Safe example rules that only report problems | Groups of rules, switched on in stages, with approved exceptions, automatic fixes for resources that break the rules, and evidence |
| State | A dedicated storage account | The Terraform state kept in a protected subscription or resource group, with controlled access for automation |

The lab teaches the workflow. The enterprise column shows what a real design adds.

## Platform and workload boundary at a glance

![Platform landing zone with four subscriptions (Identity, Connectivity, Management, Security) on the left, workload landing zones under the Corp, Online and Local management groups on the right, separated by a dashed ownership boundary](/diagrams/post-02-ownership-boundary.svg)

*Simplified diagram based on [Management groups in the Azure landing zone architecture](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups). It shows the Platform group with its four child management groups and subscriptions, and the Corp, Online and Local groups with example subscriptions. Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/) set. Microsoft's own reference diagrams are on the [What is an Azure landing zone?](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) page.*


## Common mistakes

- **New subscriptions land at the root.** By default, new subscriptions go under the tenant root management group. Set a default management group for new subscriptions, so none sit at the root.
- **Anyone can create management groups.** By default, any user or app identity in the tenant can. Turn on Azure RBAC authorization for management group operations, so only privileged users can.
- **Workload teams get access at management group level.** Avoid this because it gives people more access than they need and adds risk through inheritance. Give workload teams access at the subscription or resource group instead. Platform teams may need wider access, but give it through Privileged Identity Management (PIM) so it is only active when needed.
- **Management groups copy the org chart, the environments or the regions.** Do not copy your organization chart into a deeply nested hierarchy. Use management groups for policy, not for billing or access control. Do not create groups for production, test and development, or groups made only to model Azure regions. If you need separate environments, use separate subscriptions in the same management group. The exception is a location-based regulatory requirement, such as data residency, which can justify a structure based on location.

## From my own projects

These situations came up in my own work: platform and workload resources in the same subscription, and broad access given high up in the hierarchy. (judgement) In my experience, typical results are slower delivery, security and audit issues, and confusion about cost.

## The files in my repo

- This post: [lab-vs-enterprise.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/lab-vs-enterprise.md)

## Sources

Microsoft Learn, checked October 2026: [Management groups](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups) · [Landing zone overview](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) · [Subscriptions](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions)

