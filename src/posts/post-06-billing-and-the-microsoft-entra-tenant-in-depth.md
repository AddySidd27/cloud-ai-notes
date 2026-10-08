---
title: "Billing and the Microsoft Entra Tenant, in Depth"
slug: "billing-and-tenant-in-depth"
series: "Azure Landing Zone"
part: ""
post_number: 6
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-enterprise-agreement"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-microsoft-customer-agreement"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-cloud-solution-provider"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-ad-define"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/scenarios"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-application-environments"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/considerations-recommendations"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/plan-connect-topologies"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/lighthouse/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/external-id/what-is-b2b"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/plan-connect-userprincipalname"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/understanding-the-active-directory-logical-model"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-whatis"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/fundamentals/new-name"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-ad-tenant"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/lighthouse"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/external-id/tenant-configurations"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/administrative-units"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/mca-section-invoice"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/organize/raci-alignment"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mfa-howitworks"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure"
    checked_on: "2026-10-07"
  - url: "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview"
    checked_on: "2026-10-07"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/billing-and-tenant.md"
diagrams:
  - file: "../diagrams/post-06-billing-and-tenant.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-ad-tenant"
    icons: "Azure Public Service Icons V24 (Subscriptions, Management groups, Azure Policy) and Microsoft Entra architecture icons Oct 2023 (Microsoft Entra ID, color), all unmodified"
    source: "../diagrams/post-06-billing-and-tenant.drawio"
  - file: "../diagrams/post-06-brands-one-tenant.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/scenarios"
    icons: "Azure Public Service Icons V24 (Subscriptions, Management groups) and Microsoft Entra architecture icons Oct 2023 (Microsoft Entra ID, color), all unmodified"
    source: "../diagrams/post-06-brands-one-tenant.drawio"
  - file: "../diagrams/post-06-two-brand-shapes.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/considerations-recommendations and https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/plan-connect-topologies"
    icons: "Azure Public Service Icons V24 (Azure Lighthouse), Microsoft Entra architecture icons Oct 2023 (Microsoft Entra ID, Microsoft Entra Connect Sync), all unmodified"
    source: "../diagrams/post-06-two-brand-shapes.drawio"
production_section_written_by_addy: true  # from Addy's own answers, 2026-10-07; wording drafted by Claude, Addy to review
layout: post.njk
permalink: "/azure-landing-zone/billing-and-tenant-in-depth/"
order: 6
deck: "Your billing agreement decides how subscriptions are created and paid for, your Microsoft Entra tenant decides who can sign in, and Microsoft's default advice is to build the landing zone in one tenant, with many subscriptions inside it."
next_num: "7"
next_title: "Identity and Access in the Landing Zone"
tags: [alz]
---



## 1. The problem

Post 3 gave you the four building blocks. This post goes one level deeper, because two things surprise people.

First, billing access is not Azure access. Microsoft gives this example: a finance user is made Enterprise Administrator (the enrollment role with the highest level of access to the enrollment) on the Enterprise Agreement enrollment. That user can do the enrollment tasks, but cannot open the Azure subscriptions on it, because the enrollment roles do not give that access. Only the account owner (the owner of the account that the subscriptions sit under) has it.

Second, billing can depend on one person's account. Microsoft warns that if the user principal name (UPN, the user's sign-in name) tied to an enrollment account is deleted from Microsoft Entra ID, you cannot create new subscriptions or transfer existing ones from that account.

Both surprises come from not knowing how billing and identity connect. This post shows the connection.

## 2. Simple explanation

### Words you need first

This post uses a few terms that may be new. Here they are in plain words, from Microsoft Learn. Some of them (MFA, Conditional Access and PIM) get their own posts later. Here you only need the short meaning.

| Word | What it means |
|---|---|
| Microsoft Entra ID | Microsoft's cloud service that manages identities (who someone is) and access (what they can reach). It was called Azure Active Directory (Azure AD) until Microsoft renamed it. It is not the same product as Windows Server Active Directory. |
| Microsoft Entra tenant | One instance of Microsoft Entra ID for one organization. It holds the organization's users, groups and devices. You get one when you sign up for Azure. An Azure subscription trusts only one tenant at a time. |
| Subscription | A container for Azure resources. It is also a boundary for cost, quota, governance, security and identity controls. |
| Management group | A level above subscriptions. Rules you apply to it pass down to all the subscriptions below it. |
| Azure Policy | An Azure service that enforces your organization's standards on resources and checks whether resources follow them. |
| Azure RBAC | Azure role-based access control. It manages who can access Azure resources and what they can do with them. |
| Owner role | An Azure RBAC role that grants full access to manage all resources, including the ability to assign roles in Azure RBAC. |
| Microsoft Entra roles | Roles used to manage Microsoft Entra resources in a directory, for example to create or edit users, assign administrative roles to others and manage domains. |
| Resource group and resource | A resource group sits below a subscription and groups resources. A resource is an item you run in Azure, such as a storage account or a virtual network. |
| User principal name (UPN) | A user's sign-in name, written like an email address, for example someone@example.com. |
| Enrollment | Represents the commercial relationship between Microsoft and how your organization uses Azure. It often reflects your organization's hierarchy of departments, accounts and subscriptions. |
| Department and account | Levels under an enrollment. Departments group costs. Accounts are organizational units used to manage subscriptions and see reports. |
| Enterprise Administrator | An enrollment role. Users with it have the highest level of access to the enrollment. They can, for example, manage accounts and other administrators and create new subscriptions under active enrollment accounts. |
| Department Administrator | An enrollment role. Users with it can create new account owners and view usage details for the departments they manage. |
| Account owner | The person who owns an Enterprise Agreement account. This is the only enrollment role that can reach the Azure subscriptions under that account. |
| Billing account | The billing account of a Microsoft customer agreement. Billing profiles and invoice sections sit under it. |
| Billing profile | Represents an invoice and its payment methods and billing address. |
| Invoice section | A grouping of costs on an invoice. |
| Microsoft Partner Agreement (MPA) | The agreement that a Cloud Solution Provider partner holds. The partner runs it completely. |
| Azure plan | The plan under which a Cloud Solution Provider partner provides Azure. It holds the customer's subscriptions and is hosted in the partner's agreement. |
| Subscription vending | A standard, automated way for the platform team to hand out subscriptions to workload teams. |
| Custom domain | A domain name that you add to your tenant, such as contoso.com, next to the `*.onmicrosoft.com` name. |
| Active Directory forest and domain | On-premises Active Directory (the directory service you run in your own datacenters) is arranged in a hierarchy. The top-level container is the forest. A forest holds one or more domains. |
| Microsoft Entra Connect Sync | A tool that copies identity data from on-premises directories to Microsoft Entra ID. |
| Microsoft Entra B2B | Lets you invite people from other organizations into your tenant as guests. Guests sign in with the credentials from their own organization. |
| Azure Lighthouse | Lets one tenant manage resources that belong to another tenant. The owner delegates subscriptions or resource groups to chosen users in the managing tenant, and can remove that access at any time. |
| Microsoft Entra ID P1 and P2 | Paid plans of Microsoft Entra ID with more features. Using Privileged Identity Management, for example, needs P2 or Microsoft Entra ID Governance. |
| Microsoft 365 | A Microsoft cloud service that includes Exchange Online, SharePoint, OneDrive and Teams. It uses Microsoft Entra ID for sign-in. |
| Multifactor authentication (MFA) | At sign-in, the user is asked for an extra form of identification, such as a code on a phone or a fingerprint scan. Post 8 covers it in full. |
| Conditional Access | A Microsoft Entra feature that looks at details of a sign-in, such as the user, device and location, and then applies your access rules. For example: if a user wants to open Microsoft 365, then they must use MFA. Post 8 covers it in full. |
| Privileged Identity Management (PIM) | A Microsoft Entra service to manage, control and monitor access to important resources. For example, it can give an administrator access only for a limited time. Post 8 covers it in full. |
| Emergency access (break-glass) account | An account kept only for emergencies, to sign in and recover access if all other administrators are locked out. |
| Administrative unit | A container in Microsoft Entra ID that holds other Microsoft Entra resources, such as users, groups and devices, so you can separate them inside one tenant. |
| Log Analytics workspace | A data store that collects log data from your Azure and non-Azure resources and applications. |
| RACI | A table that names who is responsible, accountable, consulted and informed for a task. |
| Independent software vendor (ISV) | A company that builds software and sells it to customers as a service (software as a service, or SaaS). |
| National cloud | A separate Azure cloud instance for certain governments or regions, such as Azure Government (US) and Azure operated by 21Vianet (China). |
| Shadow IT | Teams that set up their own Azure environment, often their own tenant, without using the central platform team's process. |
| Sandbox subscription | A subscription for quick experiments and prototypes that are not meant for production. |

### Three billing agreements

The landing zone supports subscriptions from any Azure offer, and you can use several offers at the same time. These are the three Microsoft covers in detail.

| Agreement | Hierarchy | Good to know |
|---|---|---|
| Enterprise Agreement (EA) | Enrollment, departments, accounts, subscriptions | The account owner is the subscription owner for subscriptions under that account. A subscription belongs to one account at a time. Manage enrollments in the Cost Management area of the Azure portal, because the old EA portal retired on February 15, 2024. |
| Microsoft customer agreement (MCA) | Billing account, billing profiles, invoice sections, subscriptions | A billing account is managed by one Microsoft Entra tenant, but one agreement can include subscriptions in other tenants. New subscriptions are linked to the tenant where the billing account is. A subscription belongs to one invoice section and can move only within the same billing profile. |
| Cloud Solution Provider (CSP) | The partner's Microsoft Partner Agreement (MPA), an Azure plan, subscriptions | The partner runs the MPA, and only the partner can create CSP subscriptions. A reseller relationship must exist between the partner and each tenant. |

### Billing roles are not Azure roles

For an Enterprise Agreement, apart from the account owner, enrollment roles do not give access to Microsoft Entra ID or to the Azure subscriptions. For a Microsoft customer agreement, billing roles sit outside standard Azure role-based access control (Azure RBAC) and cannot be assigned at a management group or resource group.

In plain words: the person who can see or pay the bill is not automatically the person who can change the resources, and the reverse is also true.

### What Microsoft recommends for all three

- **Plan subscription vending.** Automate subscription creation as a self-service function, from the start of the landing zone journey.
- **Protect subscription creators.** Anyone who can create subscriptions must use multifactor authentication, like any privileged account.
- **Set budgets and alerts.** For EA, per department and account. For MCA, per invoice section or billing profile.
- **Set a notification contact** that goes to a group mailbox, and do not ignore what Microsoft sends there. This applies to EA and MCA.
- **Use the dev/test offers** (discounted offers for development and testing) where available, and follow their terms.
- **Audit who has billing access** from time to time.

Agreement-specific points:

- **EA:** use the *Work or school account* type (a sign-in managed by an organization), not a personal Microsoft account. Do not move, rename or delete the Microsoft Entra user tied to the enrollment account.
- **CSP:** the partner should create subscriptions in your own Microsoft Entra tenant, not in a partner-managed one. Microsoft also recommends Azure Lighthouse for most support access.

### The tenant: one is the default

Microsoft says to avoid creating multiple Microsoft Entra tenants for the same organization unless there is a specific business requirement. The landing zone deploys to one tenant, and management groups and Azure Policy operate only inside a single tenant.

Microsoft lists what extra tenants cost you:

- more than one set of identities for users and administrators, unless Microsoft Entra B2B is used;
- some Azure services only support identities from the tenant they are bound to;
- no central configuration or management across tenants;
- possible duplicate Microsoft Entra ID P1 or P2 licensing.

Microsoft's advice is to use your existing corporate tenant, and to create another one only when a requirement cannot be met there.

### Tenant checklist from Microsoft

- Add a custom domain. The `*.onmicrosoft.com` name must be globally unique and cannot be changed once created.
- Plan emergency access (break-glass) accounts, to prevent a tenant-wide lockout.
- Use multifactor authentication, and add Conditional Access policies for privileged accounts.
- Use Microsoft Entra Privileged Identity Management to manage privileged access.
- Send Microsoft Entra diagnostic logs to a central Log Analytics workspace.
- Use Azure Lighthouse to give partners access to resources in your tenant.

### Many subscriptions in one tenant: environments, applications and billing

A subscription is where cost, quotas, policy and access are separated. Microsoft calls it a boundary for scale, quota, cost, governance, security and identity controls. So having many subscriptions inside one tenant is normal.

- **Environments.** Microsoft says that, ideally, each application environment (development, test, production) has its own subscription. This keeps the environments isolated and contains problems to one environment. A single subscription for several environments can make sense if they cannot be isolated, the same teams hold the functional roles, and they can use the same policies. Workload owners should decide this together with the platform team. Microsoft advises against separate management groups for development, test and production. Its reason is that a workload can pass in an environment with weaker policies and then fail when it is promoted to one with stricter policies, so Microsoft recommends one consistent set of policies for these environments (sandbox subscriptions are the exception). If one environment needs something different, Microsoft suggests policies set at the subscription level, or audit policies at the management group level. Post 9 covers management groups in detail.
- **Applications.** Microsoft says to avoid a rigid model. Some applications can share a landing zone subscription, while others need their own. Reasons for their own include scale limits for large specialized workloads, a different policy boundary (for example PCI, a payment-card security standard), and a separate management boundary.
- **Billing.** A subscription is a cost boundary, so separate subscriptions are the base for separate cost reporting. On top of that, Microsoft suggests mapping your organization to the billing hierarchy: departments and accounts for an Enterprise Agreement, invoice sections for a Microsoft customer agreement. Cost Management reports and views can also use tags. For the platform, Microsoft says to keep management, security, connectivity and identity in separate subscriptions, which also separates their billing.

### Several brands or business units: tenant or subscription?

If your organization has several brands, the question is whether each brand needs its own tenant or just its own subscriptions. Microsoft's default is one tenant. A business unit gets its own subscriptions (Microsoft says to treat a subscription as a unit of management that matches business needs), and its own billing unit if you want separate billing. Microsoft suggests more tenants for isolation or autonomy only when the tools for isolating resources inside a single tenant cannot give the level of isolation you need.

Three cautions from Microsoft about brand-level tenants:

- If you do create separate tenants, the business unit often runs its own tenant, and Microsoft says the Azure team and the identity team need a clear RACI (who is responsible, accountable, consulted and informed).
- Do not use more tenants to escape friction between the cloud team and the identity team. Microsoft says to fix the operating problem instead.
- Microsoft Entra ID P1 and P2 licenses do not span tenants, so costs can grow.

Microsoft lists these common reasons for multiple tenants, and what it says about each:

| Scenario | What Microsoft says |
|---|---|
| Business unit or brand isolation | Use more tenants only when single-tenant isolation tools are not enough |
| Mergers and acquisitions | Tenants are usually consolidated, but may stay separate for a long time. A custom domain name can belong to only one tenant at a time |
| Regulatory or country/region rules | Most organizations can comply inside one tenant, using Privileged Identity Management and administrative units. Azure Government and Azure operated by 21Vianet need their own tenants |
| Software vendor delivering SaaS from Azure | A separate tenant for the SaaS subscriptions is common and sensible |
| Tenant-level testing | A separate tenant is for testing features such as Microsoft 365 or Microsoft Entra Connect, not for hosting workloads. Even dev/test workloads stay in the main tenant |
| Shadow IT and start-ups | Give teams an easy way to get a sandbox subscription in the main tenant |

### Do you need more than one tenant? Ask these questions first

This checklist is my own summary of the Microsoft Learn scenarios above. If you answer "no" to all of them, stay with one tenant.

1. Do you need Azure Government or Azure operated by 21Vianet? These national clouds need their own tenants.
2. Might a company or business unit be sold or acquired later, so you want to keep it separate? Microsoft's example keeps acquired companies in separate tenants for this reason.
3. Do you deliver a SaaS product to customers from Azure (an ISV)? A separate tenant for the SaaS subscriptions is common and sensible.
4. Do you need extreme isolation or autonomy that single-tenant tools cannot give? Try the single-tenant tools first, such as administrative units and Privileged Identity Management.
5. Do you only need to test Microsoft 365 or Microsoft Entra features? A test tenant is fine for that, but not for Azure workloads, not even dev/test.

Everything else (a new brand, a new team, a dev/test environment, friction between teams) stays in one tenant. Brands get subscriptions, and teams that want to experiment get a sandbox subscription.

Regulatory rules and tenants you already inherited from an acquisition can also lead to more than one tenant. Microsoft says most regulatory needs can still be met in one tenant with Privileged Identity Management and administrative units.

### Several brands, each with its own Active Directory: two common shapes

Here is an example setup for a group with several brands. One parent organization runs a main tenant. Other brands are separate businesses, connected to the parent and managed from it. Each brand has its own on-premises Active Directory and its own domain name. The question is: does a separate directory and domain per brand mean a separate Microsoft Entra tenant? Microsoft Learn does not answer this exact question, but its Microsoft Entra Connect topologies page shows that several on-premises forests can sync to one tenant. So a separate directory per brand does not by itself force a separate tenant. This is my reading of that page. This is a generic example to explain the choice, not a description of any customer.

**Shape 1: one tenant, many Active Directory domains.** Microsoft Entra Connect Sync supports multiple on-premises forests that sync to a single Microsoft Entra tenant. Microsoft says this can be the situation after a merger or acquisition, or in an organization where each business unit operates independently. Three things to know:

- All forests must be reachable by one Microsoft Entra Connect Sync server. Microsoft does not support several sync servers (other than a staging server, a standby copy that reads the data but writes nothing) connected to the same tenant.
- A custom domain name can be associated with only one tenant at a time, so each brand's domain name belongs to one tenant.
- One landing zone in that tenant covers all brands (my reading of Microsoft's rule that a landing zone is deployed within a single tenant). Each brand gets its own subscriptions (and billing unit, if you want separate billing), as in the second diagram below.

**Shape 2: several separate tenants.** Microsoft's own example is a corporate tenant plus tenants of acquired companies that are kept separate because parts of the group might be sold in the future. Use this only when a requirement cannot be met in one tenant. Then:

- Management groups and Azure Policy work only inside one tenant. So, to govern and monitor a tenant with Azure landing zones, Microsoft says you deploy the landing zone in that tenant. Each tenant you govern gets its own deployment.
- Microsoft recommends Azure Lighthouse for cross-tenant management, and says it can be used in both directions between tenants. It delegates subscriptions or resource groups, not whole tenants. Microsoft also lists Microsoft Entra B2B collaboration, cross-tenant access settings, cross-tenant synchronization and the multitenant organization feature to make the multitenant experience easier.
- One Enterprise Agreement enrollment or Microsoft customer agreement can provide subscriptions to several tenants, so billing can stay central.
- Microsoft Entra ID P1 and P2 licenses do not span tenants.
- Azure services that have built-in Microsoft Entra sign-in, such as Azure Virtual Desktop, Azure Files and Azure SQL, are typically supported against the home tenant, normally your corporate Microsoft Entra tenant where your users' identities are. Azure Virtual Desktop is a virtual desktop service, Azure Files a file-share service and Azure SQL a database service. Check which tenant your identities live in before you choose.
- Moving a subscription to another tenant is complex. Microsoft says it is easier to rebuild the workload in a new subscription in the destination tenant.

My own rule of thumb, based on Microsoft's default of one tenant: start with Shape 1. Move to Shape 2 only for a clear requirement, such as a brand that may be sold, or a regulatory need.

## 3. Diagram

![Left, Enterprise Agreement: a Microsoft Entra tenant above the Azure RBAC tree of management groups, subscriptions, resource groups and resources, beside the EA roles (Enterprise Administrator, Department Administrator, Account Owner). Dashed arrows show the EA account owner getting the Azure RBAC Owner role on its subscriptions. Right, Microsoft customer agreement: a billing account holds a billing profile, then invoice sections, then subscriptions](/diagrams/post-06-billing-and-tenant.svg)

*First diagram: simplified, redrawn by me to follow the layout of two diagrams on Microsoft Learn: the Enterprise Agreement relationship diagram and the Microsoft customer agreement hierarchy diagram, both from [Azure billing offers and Microsoft Entra tenants](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-ad-tenant) and its linked pages. Learn has no diagram for Cloud Solution Provider, so it is not drawn. Names such as invoice section A are generic. Not an official Microsoft diagram. Icons are from the official [Azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) and [Microsoft Entra](https://learn.microsoft.com/en-us/entra/architecture/architecture-icons) architecture icon sets.*

![One Microsoft Entra tenant holds a management group such as Corp. Brand A and Brand B each have Production, Test and Development subscriptions. A billing unit per brand, a department and account for EA or an invoice section for MCA, sits on the left](/diagrams/post-06-brands-one-tenant.svg)

*Second diagram: simplified, my own layout and my own summary of Microsoft's guidance in [Scenarios for multiple tenants](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/scenarios) and [Subscription considerations](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions). Not an official Microsoft diagram. Icons are from the official Azure and Microsoft Entra architecture icon sets.*

![Left, Shape 1: Brand A, B and C each keep their own Active Directory. One Microsoft Entra Connect Sync server syncs all of them to one Microsoft Entra tenant. Right, Shape 2: a corporate tenant is connected through Azure Lighthouse and cross-tenant features to separate Brand A and Brand B tenants, each with its own landing zone deployment](/diagrams/post-06-two-brand-shapes.svg)

*Third diagram: simplified. In Shape 2, each tenant has its own management group hierarchy and subscriptions, as in the multitenant diagram on Microsoft Learn (Learn's picture also shows Decommissioned and Sandbox groups and more detail, which I left out; the Azure Lighthouse arrows come from Learn's text, not its picture). Shape 1 is my own layout. Based on Microsoft Learn: [Considerations and recommendations for multitenant landing zones](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/considerations-recommendations) and [Topologies for Microsoft Entra Connect](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/plan-connect-topologies). Not an official Microsoft diagram. Brand names are generic. Icons are from the official Azure and Microsoft Entra architecture icon sets.*

## 4. What I have seen in production

### Mistakes to check for first

These come from Microsoft's guidance.

- **Treating a billing role as Azure access.** Enrollment and billing roles do not give access to subscriptions, so plan billing access and Azure access separately.
- **Tying billing to one person.** Microsoft says not to move, rename or delete the Microsoft Entra user tied to an EA enrollment account. If that user is deleted, you cannot create new subscriptions or transfer existing ones from that account.
- **Subscription creators without multifactor authentication.** Microsoft treats them as privileged accounts.
- **No emergency access accounts.** Microsoft recommends planning them to prevent a tenant-wide lockout.
- **Subscriptions created in a partner-managed tenant.** Microsoft says a CSP partner should create them in the customer's own tenant.
- **A separate tenant just because a brand has its own Active Directory domain.** Microsoft supports several forests syncing to one tenant, and says to create more tenants only for requirements one tenant cannot meet.
- **An extra tenant as a workaround.** Microsoft says a separate tenant is not the place to host dev/test workloads, and it is not the fix for friction between teams.

### From my own projects

I have seen environments with no emergency (break-glass) access plan, and environments where a partner (CSP) managed subscriptions or access. These showed up as billing confusion, slow subscription creation and access or security gaps.

Naming a billing owner, a tenant owner and an emergency access plan early helps avoid problems like these.

## 5. Repo

- Billing and tenant, with a list of decisions to make (my own checklist): [billing-and-tenant.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/billing-and-tenant.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Billing offers and tenants](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-ad-tenant) · [Multitenant considerations](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/multi-tenant/considerations-recommendations) · [Entra Connect topologies](https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/plan-connect-topologies)

The table summaries, the two brand shapes, the brand example and the plain-language wording are my own explanation. The repo checklist is my own.

