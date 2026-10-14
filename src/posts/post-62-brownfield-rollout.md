---
title: "Brownfield Rollout"
slug: "brownfield-rollout"
series: "Azure Landing Zone"
part: ""
post_number: 62
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/landing-zone-journey"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/transition"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-scenario-single-subscription"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-scenario-multiple-management-groups"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-scenario-regional-org"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-approach-duplicate-brownfield-audit-only"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/refactor"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/dine-guidance"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/faq"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/testing-approach"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/tailoring-alz"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-application-environments"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-monitor"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-microsoft-entra-tenant"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-ad-define"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/sandbox-environments"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/azure-migration-guide/ready-alz"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/migration/migrate-from-on-premises-platform-landing-zone"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/manage"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/how-to/protect-resource-hierarchy"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/concepts/assignment-structure"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/assign-policy-portal"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/resource-graph/first-query-portal"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/governance/management-groups/overview"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/move-resource-group-and-subscription"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/architecture/landing-zones/azure-governance-visualizer-accelerator"
    checked_on: "2026-10-09"
  - url: "https://learn.microsoft.com/en-us/azure/architecture/landing-zones/landing-zone-deploy"
    checked_on: "2026-10-09"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/05-use-cases/brownfield.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/05-use-cases/use-cases.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/06-operations/policy-exemptions.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/05-use-cases/decommissioning.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/03-implementation/cost-and-safety.md"
diagrams:
  - file: "../diagrams/post-62-brownfield-path.svg"
    type: own-layout
    based_on: "No official picture shows this sequence. The stages are my grouping of the Align on-ramp (landing-zone-journey), the transition page, the three scenario pages and the duplicate-landing-zone-group approach page, the policy-driven guardrails page, and the migration preparation pages."
    icons: "Azure Public Service Icons V24 (Resource Graph Explorer, Guide, Management groups, Templates, Policy, Subscriptions, Compliance), unmodified"
    source: "../diagrams/post-62-brownfield-path.drawio"
  - file: "../diagrams/post-62-brownfield-existing-subscriptions.svg"
    type: redraw-own-layout-official-icons
    based_on: "The duplicate-landing-zone-group approach page (align-approach-duplicate-brownfield-audit-only), the transition page and the management groups design area table. The official pictures could not be opened, so the layout is my own."
    icons: "Azure Public Service Icons V24 (Management groups, Subscriptions), unmodified"
    source: "../diagrams/post-62-brownfield-existing-subscriptions.drawio"
production_section_written_by_addy: true
layout: post.njk
permalink: "/azure-landing-zone/brownfield-rollout/"
order: 62
deck: "To bring an existing Azure environment to a landing zone, list what you have, choose one of the documented approaches, build the landing zone beside the old environment in the same tenant, try its policies in audit-only mode, and then move workloads and subscriptions in step by step."
next_num: ""
next_title: "Keeping the Landing Zone Up to Date"
tags: [alz]
---



"Brownfield" means an environment that already exists. It has subscriptions, resources and running workloads, so you cannot start from a blank page. You may have adopted Azure before landing zone guidance existed, or teams may have created their own subscriptions. This post is for you if that is your case and you want a landing zone without breaking what already runs. If you have nothing yet, read [the greenfield rollout post](/azure-landing-zone/greenfield-rollout/) instead.

No documentation page is named "brownfield rollout". The page "Journey toward the target architecture" uses the word for its Align on-ramp, and links to a transition page, three scenario pages and one approach page. This post follows those, plus the pages on moving subscriptions and resources, policy roll-out and migration preparation. The link named "Refactor a landing zone" now opens the page on deployment options, which I use in the build section. Where the order or the reading is mine, I say so.

## Key terms

Earlier posts defined these words: [landing zone, platform landing zone, workload landing zone, workload, platform team, workload team, guardrail and subscription vending](/azure-landing-zone/what-is-an-azure-landing-zone/); [subscription, management group and Microsoft Entra tenant](/azure-landing-zone/tenant-billing-subscriptions-and-management-groups/); [Enterprise Agreement and shadow IT](/azure-landing-zone/billing-and-tenant-in-depth/); [Azure RBAC, Microsoft Entra Connect and domain controller](/azure-landing-zone/identity-and-access-in-the-landing-zone/); [intermediate root management group, Corp, Online, Sandbox and Decommissioned](/azure-landing-zone/resource-organization/); [hub network, VPN Gateway, ExpressRoute, virtual network peering and overlapping address spaces](/azure-landing-zone/network-topology-and-connectivity/); [diagnostic settings and Azure Monitor baseline alerts](/azure-landing-zone/management-and-monitoring/); and, in [the governance post](/azure-landing-zone/governance-and-azure-policy/), policy effects, DeployIfNotExists (DINE), Modify, enforcement mode, remediation task and non-compliant. Other new words are explained where they first appear.

| Word | What it means |
|---|---|
| Brownfield | An environment that already exists, with subscriptions, resources and running workloads. Its opposite, greenfield, is a new environment where nothing is built yet. |
| Align on-ramp | The starting point for an existing environment that needs changes to match the landing zone target architecture. The other two on-ramps are Start (a new environment) and Enhance (an environment already in line, to which you add more controls). |
| Parallel deployment | Building the landing zone in the same Microsoft Entra tenant as your current environment, beside it. It creates a new management group structure and does not affect the existing environment. |
| Duplicate landing zone group | The documented approach marked as recommended. You copy the Landing zones management group, its children Corp and Online, and all their policy assignments, and set the copies to audit only. |
| Audit only mode | A policy assignment whose enforcement mode is DoNotEnforce (called Disabled in the portal). It reports compliance but does not enforce its effect when resources are created or updated. |
| Azure Resource Graph | An Azure service that queries resources across many subscriptions at once, with a query language based on Kusto Query Language (KQL). You need at least read access to what you query. |
| Resource ID | The full address of a resource. It contains the subscription and resource group names, so it changes when you move the resource to another resource group or subscription. |
| Move a subscription, move a resource | Two different actions. Moving a subscription to another management group does not change its resource IDs. Moving a resource to another resource group or subscription does. |

## The brownfield path at a glance

The sections below cover these seven stages in order. Stage 5, see the effect, is the audit-only part of "Build beside the old environment". Stage 7, finish, is the last part of "Move in" plus "Check that it worked". Stages 5 and 6 repeat for each wave of subscriptions you move.

**Figure 1. The brownfield path, from today's environment to governed workloads.**

![A path of seven numbered stages in three grouped panels. Look and decide: 1 Take stock, 2 Choose a path, 3 Plan the target. Build beside, then test: 4 Build beside, 5 See the effect. Move and finish: 6 Move in, 7 Finish. Each stage shows what you decide and what you end up with, ending in governed workloads and retired subscriptions waiting in the Decommissioned group. A loop arrow from stage 6 back to stage 5 is labelled "Repeat for each wave".](/diagrams/post-62-brownfield-path.svg)

*Simplified diagram, drawn by me with my own layout. No official picture shows this sequence. The stages are my grouping of the Align on-ramp, the transition guidance, the scenario and approach pages and the policy roll-out guidance. Not an official Microsoft diagram. Icons are from the official [Azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) architecture icon set, unmodified.*

## What you will have at the end

A brownfield transition is not a rebuild. You end with the reference architecture described in [the greenfield rollout](post-61-greenfield-rollout.md#what-you-will-have-at-the-end), built beside your old environment: a new management group structure under one intermediate root, platform subscriptions (the shared subscriptions for management, security, connectivity and identity), and policy assigned on the groups. Three things are special to an existing environment.

- **Your old environment keeps running.** The landing zone is deployed in the same Microsoft Entra tenant, in parallel. This gives a phased transition with minimal disruption to active workloads, and the new structure does not affect the existing environment.
- **Moving workloads is optional.** You do not have to migrate every existing application into new landing zones or subscriptions. New subscriptions for new workloads, or for migration projects, go under the right management group, such as Corp or Online.
- **Old subscriptions can retire.** You can eventually cancel an existing subscription and place it in the Decommissioned group, where Azure deletes it after 30 to 60 days.

The journey takes time. How long depends on the size of the organization, its current technical footprint and the skills of its teams.

## Take stock of what you already have

You cannot judge what a policy or a move will do to a running workload without knowing what runs. Two tools help. Azure Resource Graph inventories existing resources, so you can compare their configuration with the policies at the destination, and it can assess the effect of applying policies across a large environment. Azure Governance Visualizer, an open-source PowerShell script, walks your management group hierarchy down to the subscriptions and records Azure Policy, Azure RBAC and Microsoft Entra settings as HTML, Markdown or CSV files. Keep its output private: it describes your security controls, and it needs a service principal with Microsoft Entra permissions.

**A first step you can take today.** In the Azure portal, search for "resource graph" and select Resource Graph Explorer. To change what you query, select Directory and pick the directory, a management group or a subscription. Paste this query and select Run query; it lists five resources by name and type:

```kusto
resources
| project name, type
| limit 5
```

The schema browser on the left lists the resource types that exist in your tenant and adds them to your query when you select them, and Download as CSV saves results (up to 55,000 records). In my reading, this is a way to see what kinds of resources you have before you build the checklist below; the page shows only this starter query, not a full inventory query.

The table is my checklist, built from the move, policy and readiness guidance. No page gives one single inventory list.

| What to list | Why it matters |
|---|---|
| Tenant and billing | A subscription trusts one tenant, and the landing zone is deployed to one tenant. An Enterprise Agreement enrollment can hold subscriptions in different tenants. Moving a subscription to a new tenant is mainly done to transfer billing ownership. |
| Subscriptions and their management groups | New subscriptions land in the tenant root group by default. A subscription has only one parent management group. |
| Policy assignments, direct and on groups | Before a move, assess the policies on the subscription now and the policies in the new group and above it. |
| Role assignments | A moved subscription inherits access from its new parent. Inherited Owner limits where you can move it (see "Move in"). |
| Resources and their dependencies | Not every resource type supports a move. Check dependencies first: moving a peered virtual network needs the peering disabled, then enabled again. |
| Networks and connections | Confirm that no on-premises or existing Azure virtual network overlaps the address range you plan to use. Note existing VPN Gateway or ExpressRoute links. |
| Identity | Note your Active Directory domains and whether Microsoft Entra Connect is in place. Workloads that need legacy Active Directory sign-in (Lightweight Directory Access Protocol, Kerberos, Group Policy) need an early decision. |
| Alerts and dashboards | A resource move changes resource IDs, which affects existing monitoring, alerts and control plane operations (management actions on a resource). |
| Owners and budgets | Set budgets and alerts at group or subscription level, and name an owner to review them. Tell subscription owners what they are responsible for. |

Two kinds of existing platform are named. A **partial** platform has Azure infrastructure that nobody assembled as one platform, often through shadow IT, with fragmented subscriptions, overlapping address spaces, partial policy coverage, misdirected connectivity and mixed identity patterns. The task is remediation. A **mature** platform already has clear subscription boundaries, working connectivity, policy assignments and an access model, and the task is to check that the controls match the workloads about to arrive. For either one, start with the readiness checks in [the minimum viable platform post](/azure-landing-zone/minimum-viable-platform-landing-zone/), then fill the gaps.

In my repo case I add a habit that is mine, not the documentation's: every subscription gets a named owner, and no production subscription may stay "ownerless" or "dependency unknown" before the first move.

## Decide your path

Start with the on-ramp. Start is for a new environment. Align is for an existing one that needs changes to match the target architecture, and this post covers it. Enhance is for an environment already in line that wants more controls, with pages on improving operations, governance and security.

The Align pages offer three scenarios, named for the state your environment is in today, and one approach, which the transition page marks as recommended.

| Option | Fits when | What the page adds |
|---|---|---|
| [Single subscription, no management groups](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-scenario-single-subscription) | One subscription and no custom management groups. Platform and workload resources share it. Policy is assigned per resource group, with exceptions. One virtual network, no hybrid connection. Applications sit in their own resource groups, run by different teams. | Nothing beyond the shared steps. |
| [Existing management groups](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-scenario-multiple-management-groups) | Management groups that follow your organization or geography. A subscription for each environment (development, test, production), with platform and workload resources together. Policy at group and subscription level. A hub virtual network for hybrid connectivity and a central IT team. | A link to the [FAQ on development, test and production landing zones](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/faq#how-do-we-handle-devtestproduction-workload-landing-zones-in-azure-landing-zone-architecture). |
| [Regional organization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-scenario-regional-org) | Groups organized by environment first, then by region, with a subscription for each region and environment. Some critical workloads need the same governance in every environment. A central IT team per region struggles with consistency. | Links to the same [FAQ on development, test and production landing zones](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/faq#how-do-we-handle-devtestproduction-workload-landing-zones-in-azure-landing-zone-architecture), to the sandbox guidance and to the policy-driven guardrails guidance. |
| [Duplicate the landing zone group](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-approach-duplicate-brownfield-audit-only) (recommended) | You want quick access to the target architecture, and you want to check workload subscriptions for compliance without risk to the teams. | Copies of Corp and Online with audit-only policy; the page names its example copies "corporate brownfield" and "online brownfield" (see "Build beside the old environment"). |

The three scenarios share the same steps. First, deploy the landing zone into the same tenant, in parallel with the current environment. Second, optionally work with the application teams to migrate workloads from the original subscriptions into new subscriptions, placed under the right group, such as Corp or Online, and eventually cancel the old subscription and place it in Decommissioned. Third, create new subscriptions for new landing zones. The scenarios differ in their description of today's state and in the pages they link, not in these steps.

In my reading, because the steps are the same, pick the scenario that matches your state for its extra reading, and use the duplicate approach on top of it: it is the one marked as recommended, and it removes the risk to workload teams.

## Plan the target

Plan the same design areas as for a new environment. The table lists the decisions an existing environment adds, and only where the documentation guides.

| Decision | Choices | How to decide |
|---|---|---|
| Tenant | One tenant or several. | Deploy into the same tenant as the current environment. Avoid several tenants for one organization unless a specific business need requires it. A subscription trusts one tenant at a time. |
| Group layout | The standard hierarchy, or a tailored one. | Do not copy your current structure if it follows departments, regions or environments. Keep to three or four levels, and never more than six. Do not create groups for production, test and development, or only for regions, unless a regulation ties data to a location. See [the resource organization post](/azure-landing-zone/resource-organization/). |
| Environments | One subscription for each environment in the same group, or one subscription for several environments. | Ideally each environment has its own subscription, in the same Corp or Online group. Use one subscription for several environments only if they cannot be isolated, have the same teams in the functional roles and can use the same policies. |
| Platform subscriptions | Separate management, security, connectivity and identity subscriptions. | Do not combine platform roles in one subscription: you can then apply different policies and roles to each, and bill each separately. In my reading, the scenarios list platform and workload resources sharing subscriptions as a weakness, so the platform pieces get their own subscriptions in the new structure. |
| Policy roll-out | Audit-only copies first. DINE and Modify from the start. A staged roll-out of DINE and Modify. | Most customers can and should use DINE and Modify policies. The three-phase approach (audit only, then a reduced scope, then everywhere) is for those who cannot yet, for reasons such as regulation or change control. See [the governance post](/azure-landing-zone/governance-and-azure-policy/). |
| Address ranges and links | VPN Gateway or ExpressRoute. | Confirm that nothing overlaps first. Choose between the two by throughput, latency, compliance, lead time and routing complexity, not by whether your organization is new to Azure. ExpressRoute can take weeks or months, so run a VPN Gateway in parallel if dates cannot wait. |
| Identity | Microsoft Entra only, with Active Directory, or domain controllers in Azure. | For workloads migrating from on-premises, most already join an Active Directory domain, so you typically deploy domain controllers into the identity area. Decide early if a workload needs legacy sign-in. |
| Monitoring | Policy-driven baseline alerts. | Import the relevant policies and initiatives from the Azure Monitor baseline alerts repository, assign them and remediate the non-compliant ones. If you are not aligned to a landing zone, import them to the top-most group where you want to assign them. |

**What I could not find.** The documentation gives no steps for merging an existing hub network into the new connectivity subscription, or for deciding whether to keep both. They give the checks above: overlap, peering and routing. Treat the hub as a decision you test, not a step you copy.

## Build beside the old environment

### Before you start

The tools, rights and cost are the same as for a new environment, so I only summarize them here.

| What you need | Why |
|---|---|
| Rights to build the top of the hierarchy | In my reading, an Owner at the top of the hierarchy, because setting up the platform creates management groups and assigns access and policy. By default no one has access to the root management group; how a Global Administrator grants it is in [before you start](post-61-greenfield-rollout.md#before-you-start). |
| A tool | The portal, Bicep and Terraform deployment options all work in Azure public clouds. Azure sovereign clouds (such as US Government and 21Vianet) are not supported by those options as they are: only Bicep and Terraform can be modified, after manual changes. A sovereign landing zone variant exists for strict sovereignty rules. The options are on [Deploy Azure landing zones](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/refactor) (the page behind the link named "Refactor a landing zone"). See also [choose how to implement it](post-61-greenfield-rollout.md#choose-how-to-implement-it). |
| A cost note | The parallel build creates the same billable platform resources as a new environment, so read the cost note in [the greenfield build section](post-61-greenfield-rollout.md#build-the-platform-then-check-it). The audit-only copies add no cost: they duplicate only the management groups and the policy assignments. |
| The inventory from the section above | You need to know which subscriptions you will move first. |

### Steps

1. **Deploy the landing zone in parallel.** Use the portal, Bicep or Terraform in the same Microsoft Entra tenant as your current environment. This creates the new management group structure and does not affect the existing environment.
2. **Protect the top of the hierarchy.** Two hierarchy settings on the tenant root group help where other people already create subscriptions. Set a default, dedicated management group for new subscriptions, so none land under the root; this is especially important if users have Visual Studio or Microsoft Developer Network (MSDN) subscriptions (developer benefit subscriptions), and a sandbox group is a good candidate. Also turn on the require-authorization setting, because by default any user in the tenant can create management groups. You need the Hierarchy Settings Administrator role, or the same permissions. See [protect your resource hierarchy](https://learn.microsoft.com/en-us/azure/governance/management-groups/how-to/protect-resource-hierarchy).
3. **Create the duplicate groups.** Under the new hierarchy, create a copy of the Landing zones group and of its children Corp and Online. The approach page calls its example copies "corporate brownfield" and "online brownfield". Management group IDs must be unique in a tenant. In my reading, that applies to your copies, so give them distinct IDs and a visible suffix in the name.
4. **Assign the same policies to the copies, in audit-only mode.** In the portal, open Policy, select Assignments, then Assign policy. On the Basics tab, set the scope to the duplicate group. The field named Policy enforcement defaults to Enabled; change it to Disabled, which is the portal name for `DoNotEnforce`. If a policy uses DeployIfNotExists or Modify, check Create a managed identity on the Remediation tab. In code, set the assignment's `enforcementMode` property to `DoNotEnforce`. In my reading, with Bicep or Terraform you deploy the same assignments again at the new scope with that one property changed; the page does not describe how to copy assignments.
5. **Read the results.** A few minutes after you create an assignment, open Compliance in Azure Policy. An existing resource that meets the rule's condition is marked non-compliant.
6. **Optionally, move a first workload into the duplicate groups,** then continue in "Move in" for each wave.

Audit-only mode has three consequences. The assignment evaluates compliance but does not enforce its effect when resources are created or updated. No Azure Activity log entries are written, so you cannot rely on the log to tell you when a non-compliant resource is created. And you can still start remediation tasks by hand.

Subscription vending, the standard way to give workload teams new subscriptions, is covered on the same deployment page, with Bicep and Terraform modules; the hand-over section below links the steps.

To test changes to the platform itself, there is also a canary hierarchy: a full copy of the production group structure under the tenant root group, used to try platform changes before they reach production. It is not a common approach and it is not mandatory. Sandbox subscriptions are the alternative, but they cannot test inheritance from the hierarchy. See [testing approach](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/testing-approach).

## Subscription placement at a glance

**Figure 2. How existing subscriptions meet the new groups.**

![Left, the existing environment with its existing subscriptions, which keeps running. Right, the new landing zone hierarchy, built beside it in the same Microsoft Entra tenant: an intermediate root management group above duplicate landing zones (Corp and Online, policy assignments copied and set to audit only) and landing zones (Corp and Online, policies as designed). Below them, Decommissioned and Platform. Arrow 1: migrate workloads into new subscriptions in the duplicate groups (optional). Arrow 2: when compliance is in the required state, the subscription moves to the matching group. Arrow 3: eventually cancel the old subscription and place it in Decommissioned.](/diagrams/post-62-brownfield-existing-subscriptions.svg)

*Simplified diagram, drawn by me, based on [Scenario: Transition an environment by duplicating a landing zone management group](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-approach-duplicate-brownfield-audit-only), [Transition an existing Azure environment](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/transition) and [Management groups](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups). I could not open the official pictures, so the layout is mine, including where the duplicate groups sit. Not an official Microsoft diagram. I left out Sandboxes, Local and the platform subscriptions in detail. Icons are from the official [Azure](https://learn.microsoft.com/en-us/azure/architecture/icons/) architecture icon set, unmodified.*

## Move in: what happens to running workloads

**Move a subscription.** A subscription that moves to another management group inherits all access and policy from its new parent. Resource IDs do not change, so the move itself has no effect on the resources inside. You need permissions on the subscription, on the target group and on the current group. The simple case is Owner assigned directly on the subscription, plus write permission on the target group (Owner, Contributor and Management Group Contributor all have it). If you hold Owner only through the current group, you can move the subscription only to a group where you also hold Owner. If the target or current parent is the tenant root group (the root management group), you need no permissions on it to move an item. The [management group guide](https://learn.microsoft.com/en-us/azure/governance/management-groups/manage#move-management-groups-and-subscriptions) shows the portal, PowerShell, Azure CLI, and Azure Resource Manager (ARM) or Bicep template methods. Inherited access can take up to 30 minutes to appear. Signing out and in, or requesting a new token (a fresh proof of your sign-in), shows it sooner.

What the new group's policies do to the resources already there:

| Effect on an existing resource | After the move |
|---|---|
| DeployIfNotExists | Shown as non-compliant. Not fixed automatically: a person must remediate it. |
| Deny | Shown as non-compliant. Not rejected: a person must decide how to fix it. |
| Append and Modify | Shown as non-compliant, and a person must fix it. |
| Audit and AuditIfNotExists | Shown as non-compliant, and a person must fix it. |

Running resources are not blocked. But all new writes to resources in the moved subscription are judged by the assigned policies in real time. In my reading, this means a pipeline that redeploys a running workload can start failing right after the move. That is why audit-only copies come first.

**Move resources.** You move resources to group them by lifecycle, or to put them in another subscription for cost, ownership or access reasons. Validate first: the portal checks that the resources can be moved before it starts, and Azure CLI, PowerShell, Python and the REST API each offer a validate-only call that moves nothing. Then check these:

- The resource type must support a move. The [move guide](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/move-resource-group-and-subscription) links the list of supported types. I did not open that list.
- For a move across subscriptions, both subscriptions must be active and in the same Microsoft Entra tenant. A resource and its dependent resources must sit in the same resource group and move together, like a virtual machine and its disks.
- The destination subscription must be registered for the resource provider of what you move (the service that owns the resource type). If it is not, you get an error that the subscription is not registered for a resource type.
- Check the destination subscription's quota before you start.
- A read-only lock on the source or destination resource group, or on the subscription, blocks the move.
- You need permission to move resources on the source resource group (`Microsoft.Resources/subscriptions/resourceGroups/moveResources/action`) and permission to write on the destination resource group (`Microsoft.Resources/subscriptions/resourceGroups/write`).
- Name only top-level resources in the request. Child resources, such as a virtual machine's extensions, move with their parent and cannot move alone.
- A move can fail on the destination's policy. Resource Manager checks policies during validation, so a policy that denies a type of resource in the target resource group makes the move fail with the error code `RequestDisallowedByPolicy`.
- A resource's role assignment does not move. It is orphaned, so create it again afterward.
- The resource ID changes. Update dashboards, scripts and templates that use it.
- The source and target resource groups are locked during the move, for up to four hours. You cannot add, update or delete resources in them, but the resources already there keep running without downtime.
- A peered virtual network needs its peering disabled before the move and enabled again after it.
- A single operation of more than 800 resources fails at once, so split large moves.
- You cannot move a resource group to a new subscription. You move its resources instead, and tags, role assignments and policies do not follow.

**Order of moves.** The documentation gives no order. My own practice, not an official method, is to move in waves (small batches), starting with a low-risk pilot. After it: sandbox and development, test and shared services, low-risk production, business-critical production, and last the subscriptions with complex network, regulatory or vendor dependencies. Before each move I record inherited roles and policies, routes, DNS behavior, log flow and application health, and name a rollback owner. Afterward I observe for an agreed time.

**Finish the policy side.** When a workload team and the platform team bring that team's policy compliance into the required state, its subscription moves from the audit-only copy to the matching real group, here Corp or Online. From then on the full policies cover it. If you use DINE and Modify policies, the [policy-driven guardrails page](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/dine-guidance) describes how to enable them in stages: first on a reduced scope such as Sandbox or a non-production subscription, with tests of the whole workload life, then everywhere.

## Check that it worked

The checks are adapted from the readiness checks in [the minimum viable platform post](/azure-landing-zone/minimum-viable-platform-landing-zone/) and from the move guidance. The owner-and-plan check, the pipeline check and the last row are my own additions.

| After | Check |
|---|---|
| The parallel build | The platform subscriptions and groups exist. The policy that sends diagnostic settings to the central workspace works, and one expected alert reaches the right place. |
| Audit-only assignments | The Compliance page shows results for each subscription. Every non-compliant resource has an owner and a plan. |
| A subscription move | The subscription is in the right group. Access through Microsoft Entra groups works on the new scopes (allow up to 30 minutes). The workload's deployment pipeline still runs. |
| A resource move | Dashboards, alerts and scripts use the new resource IDs. Role assignments are recreated. Peering is enabled again. Policy and access at the destination are validated. |
| Enforcement (my practice) | One test deployment that should succeed does, and one that should be denied is denied. |

## Hand the workloads over

Moving in is a talk with each team, not only a click. The optional migration step in each scenario means working with the application or service teams. For each team, say which group its subscription is in, which policies now apply, which of its resources are non-compliant, and who fixes them: existing resources are not fixed automatically after a move. Agree on a management model for each workload. Three are described: the central team runs the landing zone, the workload team runs it inside the platform's guardrails, or the two share it, as with a hosting platform such as Azure Kubernetes Service. New subscriptions follow [the subscription vending steps](post-61-greenfield-rollout.md#hand-over-the-first-workload). Also review the security recommendations in Microsoft Defender for Cloud and plan to improve your posture as resources move.

## What comes next

A landing zone is not finished when the last subscription is in place. The next post covers keeping it up to date. Once your environment is in line, the Enhance on-ramp (pages on improving operations, governance and security) is where you add more controls.

## Common mistakes

- **Treating "non-compliant, not rejected" as safe.** After a move, existing resources keep running. But new writes are judged in real time, so a routine redeploy can be denied. Test with audit-only first.
- **Moving a resource without planning the side effects.** A move changes the resource ID, orphans role assignments, locks both resource groups and needs peering turned off and on again.
- **Copying today's structure into management groups.** Departments, regions and environments belong in subscriptions and tags, not in a deep management group tree.
- **Leaving new subscriptions under the root.** Set a default management group, or others' new subscriptions pick up whatever you assign at the top.
- **Checking access too soon.** Inherited access can take up to 30 minutes to show after a move.
- **Cancelling the old subscription first.** Migrate, check and only then cancel. In my practice I add a holding period in Decommissioned and a final approval.

## From my own projects

I have not marked any item in the list above as something I saw in my own projects. I leave out project details.

## The files in my repo

My repo is a learning implementation, and its own order and habits are my practice, not the documentation's.

- Govern an existing Azure environment: an end-to-end case for a fictional company with 45 subscriptions made by different teams, in thirteen phases, each with evidence and an exit condition. My habits: inventory first, audit mode before enforcement, a low-risk pilot wave and a rollback path for every wave. It ends with an example migration record. The phases are my own process, not an official one: [brownfield.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/05-use-cases/brownfield.md)
- Landing zone use cases: ten short cases, including this one: [use-cases.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/05-use-cases/use-cases.md)
- Policy exemptions: what I record for a time-limited exception: [policy-exemptions.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/06-operations/policy-exemptions.md)
- Subscription decommissioning: a ten-step process that ends with cancelling the subscription and says not to cancel first: [decommissioning.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/05-use-cases/decommissioning.md)
- Cost and safety: which services keep charging while idle, and the controls I use in the lab, such as a dedicated lab subscription and audit-mode policies: [cost-and-safety.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/03-implementation/cost-and-safety.md)

## Sources

Microsoft Learn, checked October 2026: [Journey toward the target architecture](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/landing-zone-journey) · [Transition an existing Azure environment to the Azure landing zone reference architecture](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/transition) · [Scenario: Transition an environment by duplicating a landing zone management group](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/align-approach-duplicate-brownfield-audit-only)

