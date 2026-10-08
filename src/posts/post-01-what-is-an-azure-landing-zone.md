---
title: "What Is an Azure Landing Zone"
slug: "what-is-an-azure-landing-zone"
series: "Azure Landing Zone"
part: ""
post_number: 1
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/"
    checked_on: "2026-10-06"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-areas"
    checked_on: "2026-10-06"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-principles"
    checked_on: "2026-10-06"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/architecture/secure-resource-management"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/govern/build-cloud-governance-team"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-ad-define"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/infrastructure-as-code-updates"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/developer/terraform/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/sentinel/sentinel-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/domain-services/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/architecture/guide-for-independent-software-developers"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/fundamentals/what-is-entra"
    checked_on: "2026-10-07"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/01-foundations/what-is-an-azure-landing-zone.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/learning-path.md"
diagrams:
  - file: "../diagrams/post-01-platform-vs-workload.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/"
    icons: "Azure Public Service Icons V24 (Management groups, Subscriptions, Virtual networks, Microsoft Sentinel, Microsoft Entra Domain Services, Log Analytics workspaces, Azure Policy), unmodified"
    source: "../diagrams/post-01-platform-vs-workload.drawio"
production_section_written_by_addy: true  # from Addy's own answers, 2026-10-07; wording drafted by Claude, Addy to review
layout: post.njk
permalink: "/azure-landing-zone/what-is-an-azure-landing-zone/"
order: 1
deck: "An Azure landing zone is the prepared Azure environment where teams run what they build, under shared rules that help govern, secure and scale it."
next_num: "2"
next_title: "Platform Scope and Workload Boundaries"
tags: [alz]
---



## 1. The problem

Imagine an Azure environment where every project team made its own subscription (a container for a team's Azure resources, explained below). One team built its own network. Another chose its own logging, which means its own records of what happens in a system. A third decided its own access rules.

A year later, simple questions are hard to answer. Who can see what? Which networks connect to which? Where do the logs go? Who pays for this?

Moving resources into different subscriptions later can lead to complicated technical migrations.

An Azure landing zone (defined below) avoids this by preparing the environment first. Microsoft says its platform part sets up governance, security and shared resources for everything your teams run in Azure. Teams then start from a known place with shared rules, instead of from nothing.

## 2. Simple explanation

### Words you need first

This post uses a few terms that may be new. Here they are in short, plain words, based on Microsoft Learn.

| Word | What it means |
|---|---|
| Resource | Something you can manage in Azure. Examples are virtual machines (computers that run in Azure), storage accounts (places to keep files and data), web apps (websites and apps that Azure runs for you), databases and virtual networks. |
| Microsoft Entra ID | Microsoft's cloud service that manages who users are and what they are allowed to access. |
| Microsoft Entra tenant | A dedicated instance of Microsoft Entra ID, usually for one organization (or a group within a larger company). It holds that organization's users, groups, devices and apps. |
| Azure subscription | A container for resources that Azure uses for billing and management. Each subscription trusts one Microsoft Entra tenant to check who people are. |
| Management group | A level above subscriptions where you group subscriptions together. Rules you set on a management group apply to every subscription under it. |
| Inheritance | A setting applied at a higher level also applies to everything below it. Learn says: "Lower levels inherit settings from higher levels." |
| Azure Policy | A service that sets rules for what is allowed in Azure and checks whether your resources follow them. |
| Governance and guardrails | Governance is how an organization controls its use of cloud services. It does this with guardrails: policies, procedures and tools that say which cloud activities are acceptable and which are not. |
| Workload | A group of Azure resources, code, data and other parts that work together to deliver one business result. AI models can be part of a workload too. |
| Platform team and workload team | The platform team manages the shared foundation. A workload team manages its own workload. |
| DevOps | Working practices and tools that let the people who build software and the people who run it work together, often with automated steps that build, test and release the software. (My plain wording, not a Learn quote.) |
| Infrastructure as code (IaC) | Managing infrastructure resources, from creation through later changes, by using definition files that a machine can read. |
| Subscription vending | A way for the platform to hand out new subscriptions to workload teams by using automation. |
| Virtual network | The building block of a private network in Azure. It lets resources such as virtual machines talk safely to each other, to the internet, and to your own networks outside Azure. |
| Log Analytics workspace | A place where you collect log data (records of what happens) from your Azure and non-Azure resources and apps. |
| Microsoft Sentinel | A Microsoft cloud service that helps security teams find, investigate and respond to threats. |
| Microsoft Entra Domain Services | A managed service that lets Azure workloads sign in with older (legacy) methods, without you building and running your own domain servers. |

The last four rows appear as examples in the diagram below. There, the Platform management group has four child groups (Security, Management, Identity and Connectivity). They match the kinds of centralized resources Learn lists later in this post: security monitoring, management services, identity services, and connectivity and networking. Post 2 explains them.

Microsoft describes an Azure landing zone as an architecture for governing, securing and scaling an Azure environment that uses many subscriptions. It has two parts:

1. **The platform landing zone.** The shared foundation.
2. **Workload landing zones.** The places where teams run their workloads.

A rough way to picture it: an apartment building has shared things, such as water, power and fire rules. Each apartment is a workload. Residents live their own lives, but inside the building's rules. (This comparison is my own, not Microsoft's.)

### The platform landing zone

The platform landing zone is the central foundation. It sets up governance, security and shared resources for all your Azure workloads. Microsoft says most organizations should have only one platform landing zone per Microsoft Entra tenant.

It has three parts:

- **A management group hierarchy.** This organizes your subscriptions and applies governance standards to them. It keeps platform resources and workload resources apart.
- **Centralized resources, only as needed.** Common examples are connectivity and networking, security monitoring, identity services and management services. Microsoft's advice is to centralize something only when it gives a clear benefit across several workloads.
- **A way to hand out workload landing zones.** You need a repeatable process to request, create and give workload landing zones to teams. You can do this by hand or automate it. As requests grow, automation matters more. Microsoft's guidance on this is called subscription vending.

### Workload landing zones

Each workload has one workload landing zone. It holds all the environments the workload needs, such as development, test and production (the live version that real users use). Each environment is one or more Azure subscriptions.

Based on what the workload needs, the platform team places each workload subscription in one of three management groups: Online, Internal (also called "Corp") or Local. These sit under the "(Application) Landing zones" management group. Post 2 explains what each one is for. The subscriptions inherit the Azure Policy rules applied higher in the hierarchy. That is how workloads get consistent guardrails, while still having room for their own needs.

(In my repo's example, Corp and Online are the main groups, and Local is optional. This is my repo's choice, not a Microsoft statement.)

### Who owns what

Here is a simple way to split the work. This is my own summary, not a Microsoft table.

| Platform team | Workload team |
|---|---|
| Management groups | Application resources |
| Policy rules that apply to everyone | Workload network and data |
| Shared connectivity | Workload monitoring |
| Central monitoring | Application updates |
| Platform security | Recovery plans for the application |

The platform team does not own every application resource. The workload team does not redesign the enterprise platform for each application.

### Two ways to build it

Microsoft describes two ways to implement each part:

- **Accelerators.** Microsoft provides accelerators that use infrastructure as code to deploy an environment based on recommended practices.
- **Custom build.** You design and build it yourself, or with help from Microsoft or a partner.

For most organizations, Microsoft says accelerators are the fastest route. We cover the options in more detail later in this series.

### Eight design areas

Microsoft says to define your requirements across the design areas before you build a platform landing zone. There are eight. Microsoft names them like this:

1. Azure billing and Active Directory tenant (the name on the Learn design-areas page; the Learn page for this area is now titled "Azure billing offers and Microsoft Entra tenants", and "Active Directory" here means Microsoft Entra ID)
2. Identity and access management
3. Resource organization
4. Network topology and connectivity
5. Security
6. Management
7. Governance
8. Platform automation and DevOps

Area 8 has "DevOps" in its name (defined above). Learn describes that area as aligning the best tools and templates to deploy your landing zones and supporting resources.

Microsoft also defines five design principles that guide these decisions. We cover them, and the design areas one by one, in later posts.

### What a landing zone is not

It is not one resource, one subscription or one script. It is the combination of the design areas above, working together. This is my explanation, based on how Microsoft describes it as a multi-subscription architecture.

## 3. Diagram

![Inside one Azure landing zone, the platform landing zone panel on top shows the Platform and Landing zones management groups (Corp, Online and Local), Azure Policy and the platform subscriptions. An arrow leads down to the workload landing zones panel, which shows example Internal (Corp), Online and Local workloads, each with production, test and development environments in subscriptions](/diagrams/post-01-platform-vs-workload.svg)

*Simplified diagram, redrawn by me to follow the layout of the detailed architecture diagram on Microsoft Learn: [What is an Azure landing zone?](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) (platform landing zone on top, workload landing zones below). I left out parts of Microsoft's diagram that this series explains later. Not an official Microsoft diagram. Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/) set. Microsoft's own diagrams are on that page.*

## 4. What I have seen in production

### Common mistakes (from Microsoft's guidance)

These come from Microsoft's guidance, in my own words.

- **Teams create their own subscriptions.** If getting a subscription is slow or complicated, teams may create their own, paid for in another way and sometimes in Microsoft Entra tenants that nobody manages. "Shadow IT" is Microsoft's term for this situation. A simple, repeatable way to request subscriptions (subscription vending) helps avoid it.
- **The structure does not match how you operate.** Microsoft warns that moving resources into separate subscriptions later can lead to complicated technical migrations. Microsoft advises reviewing its guidance on moving to the target architecture before you commit to an approach.
- **Everything is centralized.** This is my reading of Microsoft's advice to centralize a capability only when it gives a clear benefit across several workloads.
- **No policy guardrails.** Microsoft says that without Azure Policy guardrails, the work of keeping to your rules grows (more operational and management overhead).

### From my own projects

I have seen environments where teams created their own subscriptions, and each project had its own network, logging and access rules. Nobody could say clearly what things cost. The effects were slower delivery, security and audit issues, and confusion about who pays.

Where a landing zone was in place, things moved faster. New projects started in an environment that was already prepared, instead of building the basics themselves.

## 5. Repo

- This post: [what-is-an-azure-landing-zone.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/01-foundations/what-is-an-azure-landing-zone.md)
- Suggested reading order for the whole repo: [learning-path.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/learning-path.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Landing zone overview](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) · [Design areas](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-areas) · [Design principles](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-principles)

