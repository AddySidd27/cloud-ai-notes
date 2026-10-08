---
title: "Tenant, Billing, Subscriptions and Management Groups"
slug: "tenant-billing-subscriptions-and-management-groups"
series: "Azure Landing Zone"
part: ""
post_number: 3
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-ad-tenant"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-ad-define"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/architecture/secure-resource-management"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/reliability/regions-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/quotas/quotas-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-enterprise-agreement"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-microsoft-customer-agreement"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-cloud-solution-provider"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-government/documentation-government-overview-wwps"
    checked_on: "2026-10-07"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/billing-and-tenant.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/subscription-design.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/resource-organization.md"
diagrams:
  - file: "../diagrams/post-03-azure-building-blocks.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-ad-tenant"
    icons: "Azure Public Service Icons V24 (Management groups, Subscriptions, Resource groups) and Microsoft Entra architecture icons Oct 2023 (Microsoft Entra ID, color), all unmodified"
    source: "../diagrams/post-03-azure-building-blocks.drawio"
production_section_written_by_addy: true  # from Addy's own answers, 2026-10-07; wording drafted by Claude, Addy to review
layout: post.njk
permalink: "/azure-landing-zone/tenant-billing-subscriptions-and-management-groups/"
order: 3
deck: "Every Azure environment is built on four things: a Microsoft Entra tenant for identity, a billing offer for payment, subscriptions that hold your resources, and management groups that organize the subscriptions."
next_num: "4"
next_title: "The Cloud Operating Model"
tags: [alz]
---



## 1. The problem

Four words are easy to mix up when you start with Azure: tenant, billing offer (the type of Azure offer your subscriptions are bought under, such as an Enterprise Agreement), subscription and management group. They sound close, but each one answers a different question.

When they get mixed up, design decisions can go wrong. One mistake is adding extra tenants, which Microsoft says to avoid without a specific business requirement. Another is treating a subscription as only a bill, and missing that it is also a boundary for cost, quotas (the number of resources a subscription is assigned), policy and access.

This post gives you the four words in plain language and shows how they fit together. Later posts go deep: Post 6 covers billing and tenant, and Post 9 covers resource organization.

## 2. Simple explanation

### Words you need first

Terms from Posts 1 and 2 (resource, resource group, subscription, management group, tenant root group, inheritance, Azure Policy, Azure RBAC, Azure region and data residency) keep the same meaning here. The new terms are below, in short, plain words based on Microsoft Learn.

| Word | What it means |
|---|---|
| Authentication | Proving that you are who you say you are. |
| Authorization | Giving a person or app that has proved who they are permission to do something. It sets what they can access and what they can do. |
| Scope | A level at which you can apply a setting. Azure has four: management groups, subscriptions, resource groups and resources. |
| Quota | The number of resources your Azure subscription is assigned. Quotas used to be called limits. |
| Scale | How far your workloads can grow before they reach the limits Azure sets for one subscription. The plain-language wording is mine, based on Learn: "Subscriptions serve as a scale unit so component workloads can scale within platform subscription limits." |
| Billing offer | The type of Azure offer a subscription is bought under, for example an Enterprise Agreement, a Microsoft Customer Agreement or a Cloud Solution Provider agreement. The plain-language wording is mine. |
| Enterprise Agreement (EA) | The commercial relationship between Microsoft and how your organization uses Azure. An EA enrollment provides the billing foundation for your subscriptions. |
| Microsoft Customer Agreement (MCA) | A recent, modern agreement between Microsoft and your organization for how you use Azure. It is a streamlined electronic agreement that does not expire. |
| Cloud Solution Provider (CSP) | A service where a Microsoft partner sets the price and terms, bills you directly, and provisions and manages your subscriptions. |
| Data sovereignty | Data residency, plus rules about who controls customer data stored in the cloud. |

Picture one tenant at the top (this picture is my own summary of Learn's diagram). Below it are management groups, and below those are subscriptions. Inside each subscription are resource groups, and inside those are the resources you actually run. Each subscription is bought under a billing offer (the picture shows EA, CSP and MCA), and the offer decides how that subscription is paid for.

### Microsoft Entra tenant: who can sign in

A Microsoft Entra tenant provides identity and access management, which means it keeps track of who users are and what they are allowed to reach. It makes sure that only authenticated and authorized users reach the resources they have permission for (authentication and authorization are defined above). Three facts matter most here:

- An Azure subscription can trust only one tenant at a time. One tenant can have many subscriptions.
- Microsoft recommends avoiding several tenants for the same organization unless there is a specific business requirement. More tenants mean more management work and more security risk.
- The Azure landing zone reference architecture is deployed to one tenant.

### Billing offer: how you pay

A billing offer is the type of Azure offer a subscription is bought under. Common examples are an Enterprise Agreement, a Microsoft Customer Agreement and a cloud solution provider agreement. You can use more than one at the same time, and an Azure landing zone supports subscriptions from any offer.

Billing can reach further than one tenant. For example, an Enterprise Agreement enrollment supports subscriptions in different tenants, even though the landing zone itself is built in one tenant.

### Subscription: where resources live

Microsoft describes a subscription as a unit of management, billing and scale (scale is defined above). It is a boundary for scale, quota, cost, governance, security and identity controls. It is also the boundary for Azure Policy assignments. For example, a workload that needs stricter rules can sit in its own subscription, and the stricter rules do not get in the way of other workloads.

### Management group: rules for many subscriptions

Management groups sit above subscriptions, as a level for governance. Rules you apply to a management group flow down to every subscription under it. Microsoft's example: apply a policy to a management group that allows virtual machines (computers you run in Azure) only in approved regions, and it applies to every nested group, subscription and resource. One Azure RBAC role assignment on a management group can give a person access to all the subscriptions below it.

Every tenant has one top-level management group, called the *tenant root group* by default. By default, new subscriptions land there automatically. Anything assigned at the root applies to the whole tenant, so Microsoft says to keep root assignments to "must have" items only. Post 2 showed how the landing zone arranges the groups below the root.

### Below the subscription: resource groups and resources

A resource group holds related resources that share the same lifecycle, which means you deploy, update and delete them together.

Azure has four levels of management scope: management groups, subscriptions, resource groups and resources. Lower levels inherit settings from higher levels.

### The four building blocks side by side

This table is my own plain-language summary.

| Building block | Plain meaning | The question it answers |
|---|---|---|
| Microsoft Entra tenant | The identity home | Who can sign in? |
| Billing offer | The agreement you pay under | How is Azure paid for? |
| Subscription | A unit of management, billing and scale | Where do resources live, and what is the boundary for cost and policy? |
| Management group | A level above subscriptions where you apply rules | Which rules apply to which subscriptions? |

### Three common mix-ups

1. **Tenant and subscription.** A tenant is the identity home. A subscription is a container for resources. One tenant holds many subscriptions, and each subscription trusts one tenant.
2. **Subscription and region.** A subscription is not tied to a region. One subscription can hold resources from different regions, so you do not need one subscription per region. Microsoft suggests extra subscriptions per region only for region-specific governance needs, such as data sovereignty, or to get past quota limits.
3. **Management group and resource group.** A management group sits above subscriptions and groups subscriptions (and other management groups). A resource group sits below a subscription and groups resources. A management group is the top of the four levels. A resource group is the third level, just above the resources.

## 3. Diagram

![One Microsoft Entra tenant at the top, then a management group with two management groups below it. One holds a subscription bought under an Enterprise Agreement (EA). The other holds two subscriptions, one under a Cloud Solution Provider agreement (CSP) and one under a Microsoft Customer Agreement (MCA). Each subscription has a resource group, and each resource group holds resources](/diagrams/post-03-azure-building-blocks.svg)

*Simplified diagram, redrawn by me to follow the layout of the Azure scopes diagram on Microsoft Learn (one tenant, management groups, subscriptions, resource groups, resources). Learn labels its third subscription PAYG (pay-as-you-go); I show MCA instead, because this post defines MCA. Based on Microsoft Learn: [Azure billing offers and Microsoft Entra tenants](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-ad-tenant) and [What are Azure management groups?](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview) Not an official Microsoft diagram. Icons are from the official [Azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) and [Microsoft Entra](https://learn.microsoft.com/en-us/entra/architecture/architecture-icons) architecture icon sets. Microsoft's own diagram is on the first linked Learn page.*

## 4. What I have seen in production

### Mistakes to check for first

These come from Microsoft's guidance.

- **More tenants than you need.** Microsoft recommends against several tenants for one organization without a specific business requirement.
- **Subscriptions can move in and out of your tenant.** A user with the required permissions can change which tenant a subscription is linked to. Microsoft recommends setting both the "subscription leaving" and "subscription entering" directory options (Learn's settings call the tenant a directory) to *Permit no one*, with a short list of exempted users, for example members of the platform operations team.
- **Too much assigned at the root.** Whatever you assign at the tenant root group reaches everything in the tenant.
- **Big workloads share a subscription with everything else.** Microsoft says large specialized workloads should use their own subscriptions so they do not run into subscription limits. Its examples are high-performance computing (very demanding calculation jobs), Internet of Things (IoT) device systems and large business-software systems.

### From my own projects

I have seen environments with more than one tenant, a large workload that ran into subscription limits, and subscriptions where nobody was clear who owned the cost. Problems like these showed up as extra admin work, security and access gaps, slower delivery, and confusion about billing.

Deciding the tenant, the billing owner and the subscription layout early helps avoid many of them. This is my own view, not a Microsoft statement.

## 5. Repo

- Billing and tenant: [billing-and-tenant.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/billing-and-tenant.md)
- Subscriptions: [subscription-design.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/subscription-design.md)
- Management groups: [resource-organization.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/resource-organization.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Defining tenants](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-ad-define) · [Subscriptions](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions) · [Management groups](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview)

The summary table and the plain-language wording of each building block are my own explanation.

