---
title: "Governance and Azure Policy"
slug: "governance-and-azure-policy"
series: "Azure Landing Zone"
part: ""
post_number: 14
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/governance"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/dine-guidance"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/update-custom-policies"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/migrate-azure-landing-zone-policies"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-basics"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-append"
    checked_on: "2026-10-08"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/governance.md"
diagrams:
  - file: "../diagrams/post-14-governance-design.svg"
    type: learn-layout-redraw-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/governance (picture lz-design.png, read from the MicrosoftDocs GitHub source)"
    icons: "Azure Public Service Icons V24 (Cost Management, Monitor, Network Watcher, Defender for Cloud, Virtual Machine, SQL Database, Storage Accounts), unmodified"
    source: "../diagrams/post-14-governance-design.drawio"
  - file: "../diagrams/post-14-dine-phases.svg"
    type: learn-layout-redraw
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/dine-guidance (picture dine-phases.png)"
    source: "../diagrams/post-14-dine-phases.drawio"
  - file: "../diagrams/post-14-update-custom-policies.svg"
    type: learn-layout-redraw
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/update-custom-policies (picture azure-landing-zone-policy-to-newer-version.png)"
    source: "../diagrams/post-14-update-custom-policies.drawio"
  - file: "../diagrams/post-14-migrate-to-built-in.svg"
    type: learn-layout-redraw
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/migrate-azure-landing-zone-policies (picture azure-landing-zone-policy-to-built-in.png)"
    source: "../diagrams/post-14-migrate-to-built-in.drawio"
production_section_written_by_addy: true
layout: post.njk
permalink: "/azure-landing-zone/governance-and-azure-policy/"
order: 14
deck: "The Governance design area of an Azure landing zone sets up the tools for cloud governance, compliance auditing and automated guardrails, mainly with Azure Policy, so rules are checked and enforced by automated guardrails and audits instead of change-board reviews."
next_num: "15"
next_title: "Platform Automation and DevOps"
tags: [alz]
---



## 1. The problem

In the earlier posts you saw identity, networks, security and management. Each of them has rules: who may do what, which settings are required, which logs must exist. If those rules live only in a document, they depend on people remembering them. In a large environment, people forget, and teams copy each other's mistakes.

Microsoft's Governance design area asks how to turn those rules into automatic guardrails and audits. It says to look at the choices you made in identity, network, security and management. Then compare them with the automated governance in the landing zone reference architecture (Microsoft's example design). That helps you decide what to audit, what to enforce, and which policies to deploy automatically.

This post covers Learn's Governance page, Microsoft's guidance on adopting policy-driven guardrails (the DeployIfNotExists guidance), and the Learn pages on keeping the landing zone's custom policies up to date.

Microsoft says this design area focuses on design decisions for your landing zone. Governance processes and tools in more depth are in the Govern methodology of the Cloud Adoption Framework (CAF, Microsoft's guidance for adopting the cloud).

## 2. Simple explanation

### Words you need first

Earlier posts defined these words: landing zone, platform team, workload, subscription, resource group, scope, inheritance, management group, root and intermediate root management group, Corp, Sandbox, Azure Policy, guardrails, Azure RBAC, Microsoft Entra ID, Microsoft Defender for Cloud, Log Analytics workspace, Azure Monitor Logs, activity log, initiative, DeployIfNotExists, deny policy, tag, and brownfield.

The words below are new, or are explained more fully here. Each is in plain words, based on Microsoft Learn. Where a row says "my plain words", the explanation is mine, not Microsoft's.

| Word | What it means |
|---|---|
| Governance | Microsoft's design area goal: the tooling you need to support cloud governance, compliance auditing and automated guardrails. |
| Policy definition and policy assignment | My plain words: a policy definition is the rule. A policy assignment applies that rule to a scope (a management group, subscription or resource group). Microsoft says definitions can be reused at several inherited assignment scopes. |
| Policy effect | What a policy does when a resource matches the rule's condition. My plain words for the main ones: Deny blocks the request. Append adds settings to a resource as it is created or updated. Modify adds, updates or removes settings or tags. DeployIfNotExists (DINE) deploys a missing supporting setting. Audit and AuditIfNotExists (AINE) only record that a resource is not compliant. Disabled switches the rule off. |
| Compliant and non-compliant | My plain words: a resource that follows the rule is compliant. One that does not is non-compliant. |
| DINE and Modify policies | Microsoft says DINE and Modify policies are part of the landing zone reference implementation (Microsoft's ready-made deployment of the reference architecture). They help make sure landing zones (subscriptions) and the resources in them follow the rules, and they remove work from the platform and landing zone teams. |
| Enforcement mode | A setting on a policy assignment. Microsoft's DINE page names two values: Enabled and Disabled in the portal, and Default and DoNotEnforce in templates and APIs. Enabled and Default mean the same thing: the effect runs. With DoNotEnforce, the assignment effectively becomes audit-only without changing the policy definition. |
| Remediation task | A task that brings non-compliant resources into compliance. Microsoft says you can start one by hand even when the enforcement mode is DoNotEnforce. |
| Built-in policy and custom policy | A built-in policy is one that Azure already provides. A custom policy is one you or the landing zone reference implementation define yourself. Microsoft says the landing zone custom policies sit in the intermediate root management group, and some may later be replaced by built-in policies. |
| Diagnostic settings | My plain words: the setting on a resource that sends its logs and metrics to a place such as a Log Analytics workspace. |
| Infrastructure as code | My plain words: describing Azure resources in code files, so they can be deployed the same way every time. Bicep and Terraform are two languages for this. |
| Canary environment | My plain words: a separate, smaller environment where you try a change before it reaches everything. Microsoft describes testing in a separate management group hierarchy in the same tenant as a "canary" deployment. |
| Change advisory review board | Microsoft's name for a group that reviews changes before they happen. |
| Regulatory compliance policies | Policies that match a regulation or standard. Microsoft names HIPAA, PCI-DSS and SOC 2 Trust Services Criteria as examples. |
| Resource provider registration | My plain words: switching on an Azure service type for a subscription so that its resources can be created. |
| SKU | My plain words: the size or pricing level of an Azure resource, for example the size of a virtual machine. |

### What the design area covers

Microsoft's Governance page has these parts. This post follows the same order and then adds the policy guidance from the other three pages.

| Part | The question it answers |
|---|---|
| Deployment considerations | Which policies do you need, and how do you assign and keep them compliant? |
| Cost management considerations | How do you see, control and lower cloud spend? |
| Resource management, security and identity considerations | What shared baseline do resources, security tools and identity logs need? |
| Recommendations | What does Microsoft say to do first? |
| Adopting policy-driven guardrails | Can you turn on automatic remediation step by step? |
| Keeping custom policies up to date | How do you update or retire landing zone policies over time? |

### Deployment considerations

Microsoft says change advisory review boards can hinder innovation and business agility, and that Azure Policy replaces such reviews with automated guardrails and checks that people follow the rules. Its deployment considerations are:

- Decide which Azure policies you need, based on your business controls or compliance rules. Use the policies in the landing zone reference architecture as a starting point.
- Use the policies in the landing zone reference implementation to look for other policies that fit your requirements.
- Enforce automated networking, identity, management and security conventions.
- Create policy assignments from policy definitions that you can reuse at several inherited scopes. You can have central baseline assignments (the same assignments for everyone) at the management group, subscription and resource group scope.
- Keep compliance continuous with compliance reporting and auditing.
- Know that Azure Policy has limits on how much you can define and assign. Check the current limits before you design.
- Understand regulatory compliance policies, such as HIPAA, PCI-DSS or SOC 2.

### Cost management considerations

Microsoft says Microsoft Cost Management (its tool for cost oversight, with billing scopes, budgets and alerts) can help support ongoing governance of cost and spending in Azure or in other clouds. Its considerations are:

- Think about how your organization splits cost between teams and charges them for what they use, and decide which data points show your cloud spend.
- Choose a tag structure that fits how you split and charge cost.
- Use the Azure pricing calculator to estimate monthly costs.
- Use Azure Hybrid Benefit, Azure reservations and the Azure savings plan for compute. Reservations and the savings plan are commitments of one or three years. Hybrid Benefit lets you use on-premises Windows Server and SQL Server licenses that have Software Assurance. Microsoft says reservations can cut resource costs by up to 72 percent compared with pay-as-you-go prices, and the savings plan by up to 65 percent. You can combine a savings plan with reservations.
- Use Azure policies to allow only specific regions, resource types and SKUs.
- Use the rule-based policy of Azure Storage lifecycle management (a Storage feature, not an Azure Policy) to move stored data to a cheaper access tier, or delete it at the end of its life.
- Use Azure dev/test subscriptions for a discount on selected services for nonproduction workloads.
- Use automatic scaling to add and remove resources to match performance needs.
- Use Azure Spot Virtual Machines (low-price machines that Azure can take back) for workloads that can handle interruptions, such as batch jobs and dev/test.
- Choose the right Azure services and the right compute service for your application.

### Resource management, security and identity considerations

**Resource management.** Decide whether groups of resources can share required configuration, a common lifecycle or common access limits such as RBAC. For example, resources that are created and deleted together can sit in one resource group. Choose a subscription design for each application or workload that suits your operations. Use standard resource configurations for a consistent baseline.

**Security.** Enforce tools and guardrails across the environment as part of a security baseline, and notify the right people when you find deviations. Microsoft suggests using Azure Policy to enforce tools such as Microsoft Defender for Cloud, or guardrails such as the Microsoft cloud security benchmark (Microsoft's set of security recommendations).

**Identity management.** Decide who can access audit logs for identity and access management, and notify the right people about suspicious sign-in events. Consider Microsoft Entra reports to govern activity, and sending Microsoft Entra ID logs to the platform's central Azure Monitor Logs workspace. Explore Microsoft Entra ID Governance features such as access reviews (regular checks that people still need their access) and entitlement management (Microsoft Entra's way to automate access requests, assignments, reviews and expiration).

**Non-Microsoft tooling.** Learn lists two tools under "Non-Microsoft tooling": AzAdvertizer, for governance updates such as policy definitions, initiatives and role definitions, and Azure Governance Visualizer, to keep track of your technical governance setup. Microsoft says the visualizer's policy version checker can keep your environment up to date with the latest landing zone policy release.

### Microsoft's recommendations

For deployment:

- Identify the tags you need and enforce them with Azure Policy. Learn's Governance page says to use the append policy mode. Learn's effects page says append is meant for non-tag properties and recommends Modify for tags, so check both pages when you choose.
- Map regulatory and compliance requirements to Azure Policy definitions and Azure role assignments.
- Create Azure Policy definitions at the top-level root management group, because they might be assigned at inherited scopes. Learn uses "top-level root" on the Governance page and "intermediate root" on the update pages. Post 9 explains the levels.
- Manage policy assignments at the highest appropriate level, with exclusions (places where the assignment does not apply) at lower levels if needed.
- Use Azure Policy to control resource provider registrations at the subscription or management group level.
- Use built-in policies to reduce day-to-day work.
- Assign the built-in Resource Policy Contributor role (an Azure RBAC role) at a specific scope to allow application-level governance.
- Limit the number of Azure Policy assignments at the root management group scope, so you do not have to manage exclusions at inherited scopes.

For cost:

- Use Cost Management for financial oversight of resources.
- Use tags, such as a cost center or project name, to add metadata to resources and allow detailed cost analysis.

### Governance in the reference architecture

Microsoft says the reference architecture gives organizations well-developed governance controls. For example, a management group hierarchy groups resources by function or workload type, and a rich set of Azure policies enables governance controls at the management group level, which helps verify that all resources are in scope (Post 9).

### Adopting policy-driven guardrails: the DINE guidance

Microsoft explains where DINE and Modify policies are used and why. Its example is a new landing zone subscription that is created and placed in the Corp management group (the group for workloads that connect to the company network, Post 9). DINE and Modify policies then act on that subscription:

- Enable Microsoft Defender for Cloud, and configure Defender for Cloud exports (Defender data sent on to another place) to the central Log Analytics workspace in the management subscription (the subscription for platform management tools, Post 13).
- Enable Defender for Cloud for the supported offerings, based on the policy parameters in the assignment.
- Send Azure activity logs to the central workspace.
- Set diagnostic settings on all resources so their logs go to the central workspace.
- Deploy the required Azure Monitor agents (small programs that collect logs) on virtual machines and virtual machine scale sets, including servers connected through Azure Arc, and connect them to the central workspace.

Microsoft says you can disable these options at any time or during deployment. It adds one limit. DINE and Modify policies do not deploy workload resources, and Microsoft does not recommend using policy for that. They only deploy or configure supporting resources and settings.

Some organizations cannot, or are not ready to, use DINE or Modify policies. Microsoft names four reasons: regulatory compliance rules or law, strict change control that needs human approval for every action, lack of experience with DINE policies, and a requirement that workload teams define all resource configuration, including supporting resources, in infrastructure as code. Microsoft says the three phases below are not intended for the majority of customers. Most customers can and should use DINE and Modify policies from the start.

For those organizations, Microsoft suggests three phases:

| Phase | What you do |
|---|---|
| 1. Disable the automatic actions | Set the enforcement mode to DoNotEnforce on policy assignments. Leave the policy definition and its effect as they are. The assignment becomes audit-only, and you can still start remediation tasks by hand. |
| 2. Enable on a reduced scope | Set the enforcement mode to Default on a specific policy or a reduced scope, such as the Sandbox management group or a nonproduction workload subscription. Test a workload from start to finish: first deployment, code deployment, day 2 operations (running it day to day) and decommissioning (shutting it down). |
| 3. Enable everywhere | Remove the assignments used only for testing, set the enforcement mode to Default on all DINE and Modify assignments across the environment, and create remediation tasks for existing non-compliant resources. New resources are remediated automatically if they match the policy rules. |

Microsoft says some customers cannot move past phase 1 because of regulatory restrictions, and that is supported. Even in phase 3, enabling every policy is optional. You can choose per policy.

Two details from Microsoft's page are worth knowing. When the enforcement mode is DoNotEnforce, no Azure activity log entries are generated, so you are not notified when a non-compliant resource is created. If you plan to stay in phase 1 for a long time, Microsoft says it may be better to change the effect to AuditIfNotExists and set the enforcement mode back to Default.

You then get the activity log entries back. But you lose manual remediation tasks, because AuditIfNotExists never deploys anything.

Microsoft summarizes the combinations in a table. "Enabled or Default" means the effect runs. "Disabled or DoNotEnforce" means it does not.

| Policy effect | Enforcement mode | Activity log entry | Remediation |
|---|---|---|---|
| DINE | Enabled or Default | Yes | Done by the platform after a resource is created or updated. You need to start a remediation task by hand if a related resource is changed, or if the resource existed before the assignment. |
| DINE | Disabled or DoNotEnforce | No | A remediation task by hand. |
| Modify | Enabled or Default | Yes | Automatic during creation or update. |
| Modify | Disabled or DoNotEnforce | No | A remediation task by hand. |
| Deny | Enabled or Default | Yes | Creation or update is denied. |
| Deny | Disabled or DoNotEnforce | No | Creation or update is allowed. Manual remediation is needed. |
| Audit or AINE | Enabled or Default | Yes | Manual remediation. |
| Audit or AINE | Disabled or DoNotEnforce | No | Manual remediation. |

Microsoft also mentions resource selectors. They let you roll out a policy assignment step by step, based on resource location, resource type, or whether the resource has a location.

### Keeping the landing zone policies up to date

Microsoft says the landing zone custom policies and initiatives are updated to newer versions over time, and that some may be replaced by built-in Azure policies. Two Learn pages describe the manual, high-level steps. They also point to separate update guides for Microsoft's ready-made Terraform and Bicep modules.

**Detect updates.** Two options: read the "What's New" page of the Enterprise-Scale wiki on GitHub (Enterprise-Scale is the earlier name for the landing zone reference implementation; the wiki is not on Learn), or use the Azure Governance Visualizer, which marks policies as outdated or obsolete.

**Apply updates.** Check three things: whether any outdated custom policies are assigned at any scope, whether they are part of a landing zone custom policy initiative, and whether that initiative is assigned. Then follow the case that fits:

- Not assigned and not in an initiative: replace the definition (or the initiative) at the intermediate root management group.
- Assigned, parameters unchanged: replace the contents of the definition at the intermediate root management group. If it is in an initiative, nothing else changes.
- Assigned, parameters changed: record the assignments, scopes and parameter values. Delete the assignments, delete the outdated policy, import the updated one, and reassign. Then check the compliance section (in Azure Policy) for resources that fail. If an assignment holds more than one policy definition, Microsoft says to remove only the outdated policy from it, and to delete the whole assignment only if it holds just that policy. For an initiative, you cannot delete parameters from a custom initiative, so reuse them instead.
- A whole initiative updated: record the assignments, delete them, delete the old initiative, import the new one with your management group name in the policy IDs, reassign, and check compliance.

Microsoft cautions that after you delete assignments, your environment is not protected until you reassign.

**Migrate to built-in policies.** If a built-in policy replaces a landing zone custom policy: if it is not assigned, delete the custom definition. If it is assigned, create new assignments at the same scopes with matching settings using the built-in policy, delete the old assignments, then delete the custom definition. If it is assigned through an initiative, update the initiative's policy references. If the whole initiative is replaced, create new assignments of the built-in initiative at the same scopes, delete the old assignments, and then delete the custom initiative.

### New and existing environments

For a new (greenfield) environment, Microsoft points to creating a small set of subscriptions and to the Bicep deployment templates for the landing zones. For an existing (brownfield) environment, Microsoft suggests five things:

- Set up a management baseline (Post 13).
- Use Microsoft Cost Management features, such as billing scopes, budgets and alerts, so you do not exceed your expense limit.
- Use Azure Policy to enforce guardrails on deployments and to start remediation tasks that bring existing resources into compliance.
- Consider Microsoft Entra entitlement management for access requests, assignments, reviews and expiration.
- Use Azure Advisor (a Microsoft service that gives recommendations) for cost optimization and operational excellence.

Microsoft says the Bicep templates can speed up both greenfield and brownfield deployments and have integrated governance guidance. It also suggests the Azure landing zone default policy assignments Bicep module as a head start on policy.

## 3. Diagram

Microsoft Learn has four pictures for this topic. I redrew each one with the same layout, so they follow the same order as the text above.

**Figure 1. The landing zone governance design.**

![Landing zone governance design. A landing zone subscription holds IAM and Policy next to Management and Monitoring. Roles (for example NetOps, SecOps, DevOps) sit beside IAM. Subscription policy (for example allowed resource providers, encryption at rest, no public IP) sits beside Policy. Metrics, logs and alerts and Security Center sit beside Management and Monitoring. Inside are applications, with Cost Management and Azure Monitor on the left. An application template holds app resources (VM, DB, storage, hybrid), IAM, Policy, Keys and Monitor, with Network Watcher and Microsoft Defender for Cloud on the right. Shared Services and Networking sit at the bottom.](/diagrams/post-14-governance-design.svg)

**Figure 2. The three DINE phases.**

![DINE phases overview. Three arrows from left to right: disable DINE and Modify policies automated actions; enable DINE and Modify policies on a specific policy or reduced scope; enable DINE and Modify policies everywhere.](/diagrams/post-14-dine-phases.svg)

**Figure 3. Updating landing zone custom policies.**

![Decision tree for custom policy updates. Start: policy updates required, policies in scope for updating. Not assigned: replace the outdated definition. Assigned directly: if parameters are unchanged, replace the policy contents; if changed, delete or update the assignments, update the outdated policy and reassign. Assigned through an initiative that is not outdated: replace the policy contents if parameters are unchanged; otherwise delete the initiative assignments, update the policy or initiative definition and reassign. Initiative outdated: delete the initiative assignments, update the definition and assign the initiative.](/diagrams/post-14-update-custom-policies.svg)

**Figure 4. Moving landing zone custom policies to built-in policies.**

![Decision tree for migrating to built-in policies. Not assigned: delete the landing zone policy or initiative definition. Assigned directly: assign the Azure built-in policy and delete the landing zone policy assignments. Assigned through an initiative that a built-in initiative replaces: assign the built-in initiative, delete the landing zone initiative assignments, then delete the initiative definition. If the initiative is not replaced: update the landing zone initiative definition.](/diagrams/post-14-migrate-to-built-in.svg)

*Simplified diagrams, redrawn by me from the Microsoft Learn pictures, with the same layout. Not official Microsoft diagrams. Icons are from the official Azure architecture icons, unmodified.*

## 4. What I have seen in production

### Mistakes to check for first

These come from Microsoft's recommendations, one line each. The next part says which ones I saw myself.

- **Rules only in a document.** Microsoft says Azure Policy replaces review boards with automated guardrails and checks.
- **Policies defined too low.** Microsoft says to create definitions at the top-level root management group, because they may be assigned at inherited scopes.
- **Too many assignments at the root.** Microsoft says to limit them, to avoid managing exclusions at inherited scopes.
- **Custom policies when a built-in one exists.** Microsoft says to use built-in policies to reduce day-to-day work.
- **Skipping the safe path when you are not ready for DINE.** For teams that cannot or are not ready to use DINE, Microsoft describes three phases: audit only, then a small scope, then everywhere. Most customers can use DINE from the start.
- **Setting DoNotEnforce and expecting activity log entries.** Microsoft says no activity log entries are generated in that mode.
- **Never updating landing zone policies.** Microsoft says to detect outdated policies and update or migrate them, and warns that deleting assignments leaves the environment unprotected until you reassign.
- **No tags for cost.** Microsoft says to choose a tag structure that fits your cost model and enforce it.
- **Treating cost as someone else's job.** Microsoft puts Cost Management inside the governance design area.

### From my own projects

I saw these from the list above in my own projects:

- Rules only in a document. This was a real problem.
- Policies defined too low. This was a real problem.
- Too many assignments at the root. This was a real problem.
- Custom policies when a built-in one exists. This was a real problem.
- Never updating landing zone policies. This was a real problem.
- No tags for cost. This was a real problem.
- Treating cost as someone else's job. This was a real problem.

I did not mark the other two items from the list as something I saw. I leave out project details.

## 5. Repo

- Governance and Azure Policy: guardrails, assignments and the questions to ask (my own short checklist): [governance.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/governance.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Design area: Azure governance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/governance) · [Adopt policy-driven guardrails](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/enterprise-scale/dine-guidance) · [Update Azure landing zone custom policies](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/update-custom-policies)

