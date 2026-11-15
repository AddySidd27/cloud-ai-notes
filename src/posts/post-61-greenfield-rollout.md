---
title: "Greenfield Rollout"
description: "Build a new Azure landing zone: prerequisites, decisions per design area, deployment options, checks and the first workload handover, based on Cloud Adoption Framework guidance."
slug: "greenfield-rollout"
series: "Azure Landing Zone"
part: ""
post_number: 61
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/landing-zone-journey"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/implementation-options"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/architecture/landing-zones/landing-zone-deploy"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-areas"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-principles"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-microsoft-entra-tenant"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-ad-define"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/identity-access"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/network-topology-and-connectivity"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/security"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/governance"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/platform-automation-devops"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/tailoring-alz"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/regions"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-setup-guide/initial-subscriptions"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/architecture/landing-zones/subscription-vending"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/networking/design-guide/virtual-wan"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/how-to/protect-resource-hierarchy"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/migration/migrate-from-on-premises-platform-landing-zone"
    checked_on: "2026-10-09"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/learning-path.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/prerequisites.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/lab-vs-enterprise.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/05-use-cases/greenfield.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/03-implementation/avm-and-accelerator.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/03-implementation/deployment-guide.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/03-implementation/cost-and-safety.md"
diagrams:
  - file: "../diagrams/post-61-greenfield-path.svg"
    type: learn-based
    based_on: "No official picture shows this sequence. The stages follow the Start on-ramp (landing-zone-journey), the design areas page, the implementation options page, the four-step lifecycle on the subscription vending page (create platform subscriptions, create the platform, establish subscription vending, deploy workloads), and the IaC accelerator phases. The six stages group this guidance."
    icons: "Azure Public Service Icons V24 (Cost Management and Billing, Guide, Templates, Management groups, Compliance, Subscriptions), unmodified"
    source: "../diagrams/post-61-greenfield-path.drawio"
  - file: "../diagrams/post-61-greenfield-architecture.svg"
    type: learn-based
    based_on: "The management group table (resource-org-management-groups), the text descriptions of the reference architecture pictures (landing-zone, design-areas, network and subscription pages) and the tailoring page. The layout is simplified: management groups above their subscriptions."
    icons: "Azure Public Service Icons V24 (Management groups, Subscriptions, Policy, Microsoft Sentinel, Log Analytics workspaces, Microsoft Entra Domain Services, Virtual networks, Azure Firewall, Virtual Network Gateways, DNS zones, DDoS protection plans), unmodified"
    source: "../diagrams/post-61-greenfield-architecture.drawio"
layout: post.njk
permalink: "/azure-landing-zone/greenfield-rollout/"
order: 61
deck: "Build a new Azure landing zone step by step: get ready, decide, choose a tool, build, check, and hand over the first workload."
next_num: ""
next_title: "Brownfield Rollout"
tags: [alz]
---

"Greenfield" means a new environment where nothing is built yet. You have an Azure account, or can get one, and no governed environment. This post walks you through that start.

No documentation page is named "greenfield". The page "Journey toward the target architecture" uses the word for its Start on-ramp, the starting path for a brand-new environment. This post follows that page, the pages it links to, and the subscription, management group and network pages they rely on.

## Key terms

Read these posts first if a word is new.

They define these words: [landing zone, platform landing zone, workload landing zone, workload, platform team, workload team, guardrail, design area, design principle, Azure Policy, Microsoft Sentinel, Log Analytics workspace and subscription vending](/azure-landing-zone/what-is-an-azure-landing-zone/); [subscription, management group and Microsoft Entra tenant](/azure-landing-zone/tenant-billing-subscriptions-and-management-groups/); [Billing agreements and shadow IT](/azure-landing-zone/billing-and-tenant-in-depth/); [Azure RBAC and Active Directory Domain Services](/azure-landing-zone/identity-and-access-in-the-landing-zone/); [Privileged Identity Management, multifactor authentication, Conditional Access and emergency access](/azure-landing-zone/privileged-access-mfa-conditional-access-and-pim/); [intermediate root management group, Corp, Online, Local, Sandbox, Cloud Center of Excellence and landing zone archetype](/azure-landing-zone/resource-organization/); [hub-and-spoke network, Virtual WAN, ExpressRoute, VPN Gateway and Azure Firewall](/azure-landing-zone/network-topology-and-connectivity/); [Microsoft Defender for Cloud](/azure-landing-zone/management-and-monitoring/); and, in [the platform automation post](/azure-landing-zone/platform-automation-and-devops/), infrastructure as code (IaC), Bicep, Terraform, accelerator, Azure Verified Modules, version control and pipeline.

Other new words are explained where they first appear.

| Term | Meaning |
|---|---|
| Greenfield | A new environment where nothing is built yet. Its opposite, brownfield, is an environment that already exists. |
| On-ramp | A starting point on the journey to the target architecture (the end state every on-ramp leads to). There are three: Start (a new environment), Align (an existing environment that is brought in line) and Enhance (an environment already in line, to which you add more controls). |
| Reference architecture | An example design, with a diagram, of the end state of a landing zone for a large organization. You use it as a starting point and change it to fit your needs. |
| Platform subscriptions | The subscriptions that hold the shared platform: management (monitoring), security, connectivity (networking) and identity. |
| Portal accelerator | A graphical tool in the Azure portal (Azure's web interface) that deploys the reference architecture with preset settings for key parts such as management groups and policies. |
| IaC accelerator | A ready-made tool that sets up and deploys the platform landing zone from code, with Bicep or Terraform. |
| Custom build | You design and build the landing zone yourself, or with help from Microsoft or a Microsoft partner. |
| Tenant root group | The single top management group of a tenant. Everything in the tenant sits under it, and anything assigned on it applies to the whole tenant. |
| Elevated access | A way for a Global Administrator (a top Microsoft Entra role) to give themselves the User Access Administrator role at the top of the Azure hierarchy (the tenant root). It lets them view all resources and assign access in any subscription or management group. You remove it when the work is done. |
| Commercial agreement | A billing agreement such as an Enterprise Agreement, a Microsoft Customer Agreement or a Microsoft Partner Agreement (Cloud Solution Provider, CSP). You need one to create subscriptions from code. |

## The greenfield path at a glance

The sections below follow these six stages in order. Stage 1 is the section "Before you start", and stages 4 and 5 share the section "Build the platform, then check it".

**Figure 1. The greenfield path, from preparation to the first workload.**

![A path of six numbered stages in three grouped panels. Prepare and plan: 1 Get ready, 2 Plan, 3 Choose a tool. Build and check: 4 Build the platform, 5 Check it. Hand over: 6 Hand over the first workload. Each stage shows what you decide and what you end up with, ending in a governed workload subscription.](/diagrams/post-61-greenfield-path.svg)

*Simplified diagram. No Microsoft diagram shows this sequence, so the six stages group the guidance in [Journey toward the target architecture](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/landing-zone-journey), [Platform landing zone implementation options](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/implementation-options) and [Subscription vending](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending). Icons are from the official [Azure architecture icon set](https://learn.microsoft.com/en-us/azure/architecture/icons/), unmodified.*

## What you will have at the end

The Start on-ramp begins with the reference architecture, so look at the end state first. The deployment options differ in technology and in how you customize them, so the result might not be identical for each option.

- **Management groups.** One intermediate root management group sits below the tenant root group, named with your organization's prefix (the Microsoft example is Contoso) so you do not build on the tenant root group. Below it: Platform (Security, Management, Identity and Connectivity), Landing zones (Corp, Online and Local; Local is for workloads on Azure Local, Microsoft's Azure infrastructure that runs in your own datacenter), Sandboxes, and Decommissioned. Azure deletes canceled landing zones that you move to Decommissioned after 30-60 days. For many organizations, Corp, Online and Local are an ideal starting point.
- **Platform subscriptions.** One dedicated subscription under each Platform group. Security holds Microsoft Sentinel and other security tooling. Management holds the central Azure Monitor Logs workspace (the Log Analytics workspace, where logs are stored). Connectivity holds the shared network: a hub network (the shared central network that other networks connect to) or Virtual WAN, Azure Firewall, private DNS zones and gateways. The documentation recommends one Azure DDoS Network Protection plan in the connectivity subscription, shared by the platform and workload virtual networks ([Virtual WAN network topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology#plan-your-virtual-wan-deployment)), so it sits here in the picture below. Identity is a placeholder for Active Directory Domain Services (AD DS) virtual machines or Microsoft Entra Domain Services. Large deployments can hit subscription quota limits (limits on how many resources a subscription can hold) and may add dedicated connectivity subscriptions per region.
- **Policy.** Azure Policy is assigned at management group level and inherited downward. Rules for all workloads go on the intermediate root. Landing zones get rules that fit every kind of workload. Sandboxes get a less restrictive set.

## The architecture you end up with at a glance

**Figure 2. The architecture you end up with.**

![Management groups above their subscriptions. Top: the Microsoft Entra tenant, the tenant root group, then the intermediate root management group, where policy for every workload is assigned. Left: the Platform group with Connectivity (hub network, Azure Firewall, gateways, private DNS, DDoS plan), Security (Microsoft Sentinel), Management (Log Analytics workspace) and Identity (Active Directory Domain Services or Microsoft Entra Domain Services) subscriptions. Right: the Landing zones group with Corp, Online and Local, each with example workload subscriptions; a dashed arrow labeled private connection links Corp to the hub. Below: Sandboxes and Decommissioned.](/diagrams/post-61-greenfield-architecture.svg)

*Simplified diagram based on [Management groups](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups) and [What is an Azure landing zone?](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/). Management groups are drawn above their subscriptions. The picture shows a hub network; Virtual WAN is the alternative. The second region and the workload contents are left out. Icons are from the official [Azure architecture icon set](https://learn.microsoft.com/en-us/azure/architecture/icons/), unmodified.*

## Before you start

These are the things to have in place before you deploy anything. Each has a reason.

| What you need | Why |
|---|---|
| An Azure account | You need one to create subscriptions. |
| One Microsoft Entra tenant | A subscription trusts only one tenant, and the landing zone is deployed to one tenant. Avoid several tenants for one organization unless a business need requires it: they add complexity and security risk. The `onmicrosoft.com` name must be globally unique and cannot be changed, so choose it with care. Add your own custom domain names. |
| A billing offer | Subscriptions come from a billing offer, such as an Enterprise Agreement, a Microsoft Customer Agreement or a Microsoft Partner Agreement (Cloud Solution Provider, CSP). Any of them works. The documentation lists these three agreement types for [creating subscriptions from code](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/programmatically-create-subscription). If your offer is not one of them, create subscriptions by hand and automate the rest. |
| A Global Administrator, for set-up only | By default no one has access to the root management group. Only a Global Administrator can give themselves access (steps below), and then assign roles to others, including making their own account an Owner of the tenant root group. Global Administrator is a highly privileged role, so use it only for this step. |
| Azure roles for the person who deploys | Owner is the built-in role that can create management groups, assign access and assign policy. Contributor can create groups but cannot assign access or policy ([Management group access](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview#management-group-access)). For a platform landing zone generated from Azure Migrate, the documentation says Owner may be needed temporarily at the tenant root group or a management group for initial tenant setup, and that a standard deployment needs Contributor and User Access Administrator at the target management group ([Platform landing zone from Azure Migrate](https://learn.microsoft.com/en-us/azure/migrate/platform-landing-zone#permissions)). That page is about the Azure Migrate route. Each accelerator's own guide states the exact role and scope it needs. The Global Administrator grants the role. |
| Emergency access, multifactor authentication and privileged access | Plan emergency access (break-glass) accounts, which are accounts kept aside so you cannot lock yourself out of the tenant. Enforce multifactor authentication and Conditional Access for privileged accounts, and use Privileged Identity Management (PIM). |
| The tools for your option | The portal option needs a browser and a sign-in. The IaC option needs your choice of Bicep or Terraform, a version control system (Azure DevOps or GitHub, which stores your code and its history), a PowerShell module (a package of PowerShell commands) that does the one-time bootstrap (the first run that sets up Azure and your code repository), and pipelines (automated steps that deploy your code, run on machines called runners). |

Each accelerator's own guide lists its detailed prerequisites, so read the guide for your option first. The IaC accelerator has a prerequisites phase for this.

**How to elevate access.**

1. Sign in to the Azure portal as a Global Administrator. If you use Privileged Identity Management, activate the role first.
2. Go to **Microsoft Entra ID**, then **Manage**, then **Properties**.
3. Under **Access management for Azure resources**, set the toggle to **Yes** and save.
4. Sign out and back in.

You now hold the User Access Administrator role at the root. It lets you view all resources and assign access in every subscription and management group of the tenant. On the role table, it can assign access and policy but cannot create, rename, move or delete management groups ([Management group access](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview#management-group-access)). So the person who deploys also needs the roles that the permissions row above describes for the rest of the work. This setting applies only to you.

When the set-up is done, set the toggle back to No, as the same user, and sign out. If you use PIM, set the toggle to No before you deactivate your role: deactivating the role does not reset the toggle.

## Plan the decisions in each design area

Define your organization's requirements across the design areas before you build the platform landing zone. The [design principles](/azure-landing-zone/what-is-an-azure-landing-zone/) are a compass for these decisions. You may deviate from them, but know what you give up ([Azure landing zone design principles](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-principles#impact-of-design-deviations)).

A new environment has settled none of the eight areas, so expect to work through all of them. The table gives the main decisions, the simple choices, and what to pick if you are unsure. The last column is a suggestion based on the Microsoft recommendations, not a default set by Microsoft. Where Microsoft gives no default, the table says so.

| Design area | Decide | Simple choices | If unsure |
|---|---|---|---|
| [Billing and tenant](/azure-landing-zone/billing-and-tenant-in-depth/) | Which billing offer. How many tenants. | Enterprise Agreement, Microsoft Customer Agreement or Microsoft Partner Agreement (CSP). One tenant or several. | No offer is preferred, so use the agreement you have. Use one tenant. |
| [Identity](/azure-landing-zone/identity-and-access-in-the-landing-zone/) | How people and workloads sign in. | Microsoft Entra only; Microsoft Entra with on-premises Active Directory; Microsoft Entra Domain Services; domain controllers in the identity subscription. | With no identity infrastructure, start Microsoft Entra-only. Use groups, least privilege and PIM. |
| [Resource organization](/azure-landing-zone/resource-organization/) | The management group layout. The subscriptions. | The standard hierarchy, or a tailored one. | Use the standard one. Keep it to three or four levels, and never more than six. Do not make management groups for departments, regions or environments: use separate subscriptions for those. A location rule such as data residency is the exception for regions. Add a new group under Landing zones only for a real need, such as a Payment Card Industry (PCI) rule. Start with a small set of subscriptions. |
| [Network](/azure-landing-zone/network-topology-and-connectivity/) | The topology. The link to your office or datacenter. The address ranges. | Hub-and-spoke or Virtual WAN. VPN Gateway or ExpressRoute, or none yet. | Hub-and-spoke if you want full control of the routing and your regions do not all need to reach each other. Virtual WAN for more than two regions, global transit between regions, or Microsoft-managed hub routing ([traditional topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology)). Branch limits differ by page: the [Virtual WAN topology page](https://learn.microsoft.com/en-us/azure/networking/design-guide/virtual-wan) uses about 30 VPN branch connections as the guide, and the traditional topology page says a VPN gateway supports up to 100 tunnels. [The network post](/azure-landing-zone/network-topology-and-connectivity/) explains the difference. Never use overlapping address ranges in one routing domain (a set of networks that can reach each other). |
| [Security](/azure-landing-zone/security/) | Who gets alerts. How long logs are kept. Who holds keys. How traffic enters and leaves. | A decision for each. | Enable Microsoft Defender for Cloud standard on all subscriptions and use Azure Policy to check it. Export activity logs to Azure Monitor Logs. |
| [Management and monitoring](/azure-landing-zone/management-and-monitoring/) | Where logs go. How much recovery you need. | One central Log Analytics workspace or one per region. Recovery time objective (RTO, how long a service may be down) and recovery point objective (RPO, how much data you may lose). | No default for the workspace choice: each has pros and cons, including cross-region network charges. Capture the RTO and RPO requirements, because workloads need platform-level capabilities for a basic level of business continuity and disaster recovery ([Management design area](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management#protect--recover)). |
| [Governance](/azure-landing-zone/governance-and-azure-policy/) | Which policies. How to track cost. | The reference architecture's policies as a start. Budgets and tags. | Use built-in policies to cut effort. Assign at the highest sensible group. Create a budget with alerts when you create each subscription. |
| [Platform automation and DevOps](/azure-landing-zone/platform-automation-and-devops/) | Portal or code. Which language and version control. | See the next section. | Infrastructure as code is the recommended route. |

**Regions.** The architecture works in any region, but you must name the regions you deploy to. Management groups, policies and role assignments are global, but a region is still needed for their metadata. The Log Analytics workspace and the network resources are regional. You can start with one region and add more later, so design connectivity, identity and management to fit more. When you add a region, update any allowed-locations policy (an Azure Policy that lists the only regions where resources may be created) ([Landing zone regions](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/regions)).

## Choose how to implement it

You can use an accelerator or a custom build. The reference implementations help an organization get started quickly. The three standard options (portal, Bicep, Terraform) all work in Azure public clouds. An accelerator does the platform build for you, so the next section is what to check afterward, not a list of manual steps. You only do those steps yourself in a custom build.

| Option | What it is and deploys | Pick it when | Watch for |
|---|---|---|---|
| Portal accelerator | A deployment in the Azure portal that gives a complete implementation of the reference architecture, with preset settings for key parts, including management groups and policies. | Your organization lacks IaC expertise or prefers a visual approach. | Less flexible and scalable. Updates and version control are hard without IaC. Move to IaC when you can. |
| IaC accelerator with Bicep or Terraform | A customizable deployment built on Azure Verified Modules. It also sets up the delivery environment: version control, deployment pipelines and runners, with Azure DevOps or GitHub. | You can work with code. It is the recommended approach. | Four phases: planning, prerequisites, bootstrap and run. [The platform automation post](/azure-landing-zone/platform-automation-and-devops/) explains them. |
| Azure Verified Modules alone | The same building blocks, used without the accelerator. | You want to assemble your own deployment. | You then set up the delivery environment yourself. |
| Custom build or partner | You design and build it, or work with Microsoft or a partner. Partner programs such as Azure Accelerate can help. | Neither standard option fits. | More design and maintenance work for you. Verified modules reduce the maintenance burden of custom code. |

Between Bicep and Terraform, the planning phase asks you to select your preferred language and version control system. Choose the one your team knows.

**Where to start with each route.**

- Portal: open the [portal accelerator](https://aka.ms/alz/portal), a Deploy to Azure button, signed in with the account that has the rights from the previous section. Read its prerequisites first.
- IaC with Bicep or Terraform: do phase 0 first. Pick the language and version control system, then open the [IaC accelerator](https://aka.ms/alz/accelerator) and follow the getting-started guide for your language: [Bicep](https://azure.github.io/Azure-Landing-Zones/bicep/gettingstarted/) or [Terraform](https://azure.github.io/Azure-Landing-Zones/terraform/gettingstarted/). Phase 1 configures credentials and subscriptions, so have your platform subscriptions in mind. Phase 2 bootstraps (the PowerShell module sets up Azure and your version control system), and phase 3 customizes the code and runs the pipelines.
- Azure Verified Modules alone: start at [Azure Verified Modules](https://aka.ms/avm).
- Custom build or partner: start with [Azure Accelerate](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/partner-landing-zone#option-1---azure-accelerate).

The accelerator guides on azure.github.io change often, so this post does not copy their steps. Open the guide for your option and read its prerequisites before you start.

Two special cases. If you must deploy to Azure US Government or Azure operated by 21Vianet, none of the three standard options is supported as an automated deployment. Only the Bicep and Terraform code can be modified for those clouds: use the [Bicep code](https://github.com/Azure/alz-bicep-accelerator/tree/main/templates) or the [Terraform code](https://github.com/Azure/alz-terraform-accelerator/tree/main/templates/platform_landing_zone) as a starting point. If you have strict sovereignty (legal control over your data) and data residency (data must stay in a country or region) needs, a sovereign landing zone variant exists.

## Build the platform, then check it

With an accelerator, the tool performs the build for you, so the table below is what to check afterward. The steps are manual only in a custom build. The lifecycle runs in this order: create the platform subscriptions, create the platform, set up subscription vending, then deploy workloads. Inside "create the platform", the grouping below follows what the reference architecture contains. The checks are adapted from the readiness checks in [the minimum viable platform landing zone post](/azure-landing-zone/minimum-viable-platform-landing-zone/). That post is written for migrations from on-premises, so skip checks about an on-premises network if you have none.

| Step | What gets created | How to check |
|---|---|---|
| 1. Platform subscriptions | The security, management, connectivity and identity subscriptions. Do not combine these roles in one subscription: that way you can apply different policies and roles to each, and bill each separately. | They appear in the Subscriptions list with a clear name, an owner, tags and a budget. |
| 2. Management groups | The hierarchy from the section above. | Each subscription sits in the right group. New subscriptions land in the tenant root group by default, so move them. |
| 3. Policy and access | Azure Policy assignments and role assignments on the management groups. | The assignments are attached and the compliance state is reviewed. Access through Microsoft Entra groups works on the scopes you expect. The privileged access process is tested. |
| 4. Management and security tooling | The Log Analytics workspace, alerts, Defender for Cloud and Microsoft Sentinel. | The policy that sends diagnostic settings to the central workspace works, and one expected alert reaches the right place. |
| 5. Connectivity and identity | The hub network or Virtual WAN, Azure Firewall, gateways, private DNS, and the identity services you chose. | Names resolve from a representative spoke network once one is connected, and the path that traffic takes through the firewall is confirmed. |

To create a subscription by hand under a Microsoft Customer Agreement, go to Subscriptions in the Azure portal and select Add. Give it a name that shows the workload and the environment. Choose the billing account, billing profile, invoice section and plan, then on the Advanced tab the directory, the management group and one or more subscription owners, and on the Tags tab your standard tags ([Create a Microsoft Customer Agreement subscription](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/create-subscription)). Other agreement types have their own pages. Set a budget for spending alerts afterward.

Two settings protect the hierarchy while you build it. By default any user can create management groups, and new subscriptions land in the root group. It is recommended to turn on Azure RBAC authorization for management group operations (the "require authorization" setting) and to set a default, dedicated management group for new subscriptions, with sandbox as a good candidate.

Both are set on the root management group, in **Settings**. The first is the toggle named **Permissions for creating new management groups**. You need permission to change hierarchy settings (the Hierarchy Settings Administrator role has it) ([Protect your resource hierarchy](https://learn.microsoft.com/en-us/azure/governance/management-groups/how-to/protect-resource-hierarchy)).

When the checks pass, remove the elevated access you used.

**A cost note.** A full platform deployment creates billable resources. Hub resources such as Azure Firewall and gateways are billed separately ([Virtual WAN topology](https://learn.microsoft.com/en-us/azure/networking/design-guide/virtual-wan) and [Azure pricing](https://azure.microsoft.com/pricing/)). Before you apply a full-platform profile, review the services that can keep charging while idle, such as Azure Firewall, Log Analytics ingestion and public IP addresses, plus Azure Bastion and DNS Private Resolver if you deploy them, and set a subscription budget first. This is advice, not a Microsoft rule.

## Hand over the first workload

Before the first workload, you need a repeatable way to give teams their landing zones. That is subscription vending. It involves three groups. A cloud center of excellence (the team that sets the business rules) builds the approval process. The workload team asks for a subscription. The platform team creates and configures it, then hands it over.

Collect these facts when a team asks: the expected budget, the owners, networking expectations, and how critical and confidential the workload is. You also say whether it is Production or DevTest (a cheaper offer for non-production; the DevTest offer is not available for a Microsoft Partner Agreement) ([Subscription vending](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending)). The answers tell you which management group fits: Corp for workloads that connect to your private network, Online for internet-facing ones, Local for Azure Local clusters, and Sandboxes for experiments.

The platform team then does this:

- Places the subscription in that management group, so it inherits the policies.
- Names the subscription owner and gives groups the minimum access they need.
- Assigns subscription-level policies and enrolls it in Defender for Cloud.
- Creates a virtual network peered to the hub, if the workload needs one.
- Creates a first budget.

Then the platform team hands the subscription over, usually empty but already governed. The workload team updates the budget, builds its resources and runs the workload. The platform team keeps control of governance.

You can do this by hand for the first few requests. As requests grow, automate it: vending modules exist for Bicep and for Terraform. Without vending, teams wait, or create subscriptions elsewhere without management, which is shadow IT.

## What comes next

A landing zone is not finished when it is built, and the journey takes time. How long depends on the size of the organization, its technical footprint and the skills of its teams. The documentation covers this in [Keep your Azure landing zone up to date](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/keep-azure-landing-zone-up-to-date).

## Common mistakes

- **Too many policy assignments at the root.** Debugging inherited rules in lower groups becomes hard. Keep root assignments to the ones that must apply everywhere.
- **Giving workload teams access at management group level.** It over-permissions them. Give access on their own subscriptions or resource groups.
- **Elevated access left on after set-up.** Set the toggle back to No.

## Sources

- [Journey toward the target architecture](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/landing-zone-journey)
- [Deploy Azure landing zones](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/landing-zone-deploy)
- [Platform landing zone implementation options](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/implementation-options)
