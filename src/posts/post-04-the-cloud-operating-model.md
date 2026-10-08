---
title: "The Cloud Operating Model"
slug: "the-cloud-operating-model"
series: "Azure Landing Zone"
part: ""
post_number: 4
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/prepare-organization-for-cloud"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/shared-management-operating-model"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/manage/ready-cloud-operations"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/govern/build-cloud-governance-team"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/quotas/quotas-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/developer/intro/hosting-apps-on-azure"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/fundamentals/what-is-entra"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-create-budget-bicep"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/overview-cost-management"
    checked_on: "2026-10-07"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/01-foundations/operating-model.md"
diagrams:
  - file: "../diagrams/post-04-cloud-operating-models.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/prepare-organization-for-cloud"
    icons: "Azure Public Service Icons V24 (Subscriptions, Azure Policy), unmodified"
    source: "../diagrams/post-04-cloud-operating-models.drawio"
production_section_written_by_addy: true  # from Addy's own answers, 2026-10-07; wording drafted by Claude, Addy to review
layout: post.njk
permalink: "/azure-landing-zone/the-cloud-operating-model/"
order: 4
deck: "A cloud operating model is the answer to \"who does what in the cloud?\", and Microsoft describes three models: centralized, shared management and decentralized."
next_num: "5"
next_title: "Business Requirements: Compliance, Region, Recovery, Connectivity and Cost"
tags: [alz]
---



## 1. The problem

A landing zone covers areas such as management groups, subscriptions, networking and policy (Post 1). In my words: tools do not decide who approves a new subscription, who owns the network, or who gets the call when something breaks. People decide that.

Microsoft defines a cloud operating model as how your organization manages cloud resources, team responsibilities and collaboration. A well-designed model helps align cloud work with business goals, speed up workload delivery, clarify accountability and reduce operational overhead.

## 2. Simple explanation

Microsoft's Cloud Adoption Framework (defined in the first row of the table below) describes three models. This topic comes from the Cloud Adoption Framework, not from the eight Azure landing zone design areas in Post 1. Think of them as three answers to one question: how much does one central team own?

### Words you need first

This post uses a few terms that may be new. Here they are in plain words, based on Microsoft Learn definitions.

| Word | What it means |
|---|---|
| Cloud Adoption Framework | Microsoft's guidance that helps decision makers make better decisions, faster, about adopting Azure. It aims to reduce risk, speed up adoption, and build a foundation that supports current and future workloads. |
| Governance | How an organization controls its use of cloud services, by setting guardrails. |
| Guardrails | Policies, procedures and tools that say which cloud activities are acceptable and which are not. |
| Subscription vending | A standard, automated way for the platform team to hand out subscriptions to workload teams. |
| Hybrid cloud | On-premises systems (the ones you run in your own datacenters) and a public cloud, connected so they work together as one environment. |
| Azure Policy | An Azure service that enforces your organization's standards on resources and checks whether resources follow them. |
| Microsoft Entra ID | Microsoft's cloud service that manages identities (who someone is) and access (what they can reach). |
| Microsoft Defender for Cloud | A security service that combines several cloud security tools into one, to protect applications across their whole lifecycle. |
| Resource group | A container that holds related resources for an Azure solution. |
| Quota | The number of a resource type that your Azure subscription is allowed to use. Quotas used to be called limits. |
| Tags | Labels you add to resources, each with a name and a value, such as Environment = Production. They help you find resources and track cost. |
| Budget | A spending amount you set in Azure Cost Management (Microsoft's tools for analyzing, monitoring and optimizing cloud costs). When spending passes the thresholds you choose, it sends alerts. On its own it does not stop your resources or your spending. |

### Centralized: one team owns everything

A single team is responsible for governance, security and operations across the whole cloud environment and all workloads. Policies are applied consistently. Microsoft says this is ideal for small organizations, startups or highly regulated industries. The warning: it can become a bottleneck as cloud adoption grows, so responsibilities need regular review.

### Shared management: platform team and workload teams

Responsibilities are divided between platform teams and workload teams. Platform teams provide a standard set of platform "products" (shared services) that the whole organization uses. They enforce baseline governance policies and maintain the platform landing zone for shared services such as connectivity, identity, management and security. They can also offer services like subscription vending. Workload teams operate autonomously within those guardrails.

Microsoft says this suits mid-size and enterprise organizations, and is especially effective in hybrid environments and in environments that use more than one cloud provider. It needs clear responsibilities and strong coordination.

This model uses the two parts you met in Posts 1 and 2: a platform landing zone run by the platform team, and workload landing zones used by workload teams.

### Decentralized: each team owns its own platform

Each team owns its platform landing zone and manages its workloads independently, including governance and operations. Microsoft says this suits highly skilled teams in startups or innovation programs. To reduce security and compliance risk, assess team capabilities, provide training and run regular audits.

### Hybrid, and changing over time

Here "hybrid" means a mix of models, not on-premises plus cloud. Microsoft notes that many organizations mix models. Core systems might follow a centralized or shared model, while innovation teams work more independently. And as the organization grows, you should regularly check whether the current model still fits.

### The three models side by side

| Model | Best for | Main strength | Main risk |
|---|---|---|---|
| Centralized | Startups, organizations that use one cloud | Simpler control, uniform standards | One team becomes a bottleneck as scale grows |
| Shared management | Mid-size or enterprise organizations, hybrid setups, organizations that use more than one cloud | Balances standards with team agility | Requires clear responsibilities and strong coordination |
| Decentralized | Tech-savvy startups, innovation programs | High speed and autonomy | Weaker standardization, higher risk of security gaps |

*Table based on Microsoft's comparison, shortened by me.*

### Who does what in the shared management model

Microsoft lists central (platform) and workload responsibilities for each management area. Here are four of them, shortened and reworded:

| Area | Platform team | Workload team |
|---|---|---|
| Security | Manages identities in Microsoft Entra ID, grants access to Azure subscriptions, keeps security standards in place with Azure Policy and Microsoft Defender for Cloud | Designs the workload securely, responds to workload-specific security alerts |
| Resource management | Decides how management groups, subscriptions and resource groups are arranged, creates workload subscriptions as requested, configures shared networking, handles quota increase requests | Manages resource groups and resources, follows naming and tagging standards, stays within subscription quotas |
| Monitoring | Plans the monitoring strategy, alerts on central responsibilities | Monitors the workload, extends central alerts for workload needs |
| Cost | Allocates budgets for the whole organization or for a subscription, monitors spending across the organization, assigns costs to business units or products, applies the tagging strategy | Optimizes the workload design, respects budget constraints |

Microsoft's full table also covers compliance, deployment, development, reliability and performance. The link is in Sources.

## 3. Diagram

![Three panels. Centralized: one cloud team owns governance, security and operations for all workloads. Shared management: a platform team owns the platform landing zone, guardrails and subscription vending, and workload teams operate within the guardrails, with Azure Policy shown as the guardrails. Decentralized: each team owns its own platform landing zone and workloads](/diagrams/post-04-cloud-operating-models.svg)

*Simplified diagram, my own layout (Learn has no diagram of these three models), based on Microsoft Learn: [Prepare your organization for the cloud](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/prepare-organization-for-cloud#choose-a-cloud-operating-model). The subscription boxes and the three example teams are my own illustration, not from Learn. Not an official Microsoft diagram. Icons are from the official [Azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) architecture icon set.*

## 4. What I have seen in production

### Mistakes to check for first

The headings are my wording. The guidance behind each one comes from Microsoft.

- **Nobody is named as the owner.** Microsoft says to name specific owners for all cloud management responsibilities, with both primary and backup owners so work continues during absences.
- **No responsibility matrix.** In the shared model, Microsoft recommends a matrix that records who owns which services, operations and support functions across platform, workload and traditional IT teams (the teams that run on-premises systems; that explanation is mine).
- **No governance team before workloads arrive.** Microsoft says a governance team should be in place before you deploy workloads.
- **The model is chosen once and never reviewed.** Microsoft says to reassess regularly whether the current model still supports your goals and needs. For a centralized model it adds that one team can become a bottleneck as adoption scales.
- **Platform services are hard to find or use.** Microsoft says platform services should be easy to find, and ready for workload teams to use on their own, which reduces dependency on the platform team.

### From my own projects

I have seen a central team become a bottleneck for everyone else. I have also seen platform and workload teams work well together. The problems showed up as slow delivery and confusion during incidents about who should act.

Microsoft also advises assigning ownership early, and in my experience writing down who owns what before the first workload arrives helps.

## 5. Repo

- Operating model, with a responsibility table and a list of decisions to record (my own checklist): [operating-model.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/01-foundations/operating-model.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Choose a cloud operating model](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/prepare-organization-for-cloud#choose-a-cloud-operating-model) · [Shared management operations](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/shared-management-operating-model) · [Ready your cloud operations](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/manage/ready-cloud-operations)

The plain-language wording and the shortened tables are my own explanation. The repo checklist is my own.

