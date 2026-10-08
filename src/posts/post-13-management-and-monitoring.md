---
title: "Management and Monitoring"
slug: "management-and-monitoring"
series: "Azure Landing Zone"
part: ""
post_number: 13
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-platform"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-operational-compliance"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-business-continuity-disaster-recovery"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-monitor"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/update-manager/overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/action-groups"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-machines/availability-set-overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/backup/backup-overview"
    checked_on: "2026-10-08"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/management.md"
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/business-continuity.md"
diagrams:
  - file: "../diagrams/post-13-management-and-monitoring.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management and management-monitor (the monitor page has an alert-topology diagram, described in the post text and not redrawn; this picture is an own-layout summary of the whole design area. Deliberate exception to the follow-Learn-layout rule, because the Learn diagram covers only alert topology, not the design area)"
    icons: "Azure Public Service Icons V24 (Log Analytics Workspaces, Monitor, Policy, Update Management Center, Recovery Services Vaults, Alerts), unmodified. Update Manager uses the Update Management Center icon file; Site Recovery has no icon in the set"
    source: "../diagrams/post-13-management-and-monitoring.drawio"
production_section_written_by_addy: true
layout: post.njk
permalink: "/azure-landing-zone/management-and-monitoring/"
order: 13
deck: "The Management design area of an Azure landing zone sets up the common tools for running the cloud every day (Microsoft calls this the operations baseline), which means seeing what is happening, staying in the expected state, and being able to recover, so every workload gets the same set of tools."
next_num: "14"
next_title: "Governance and Azure Policy"
tags: [alz]
---



## 1. The problem

Posts 7 to 11 covered who can sign in, how resources are organized, how networks are laid out and how security is set up. Once all of that exists, someone has to keep it running. Logs have to go somewhere, machines have to be patched, alerts have to reach a person, and a workload has to have a way back after an outage. If every workload team does this alone, you get many different tools and many gaps.

Microsoft says that for stable, ongoing operations in the cloud, a management baseline is required to provide visibility, operations compliance, and protect and recover capabilities. Learn's heading for the middle one is "Operational compliance".

This post follows Microsoft's design area called "Management for Azure environments". Microsoft says the goal is to understand operations management requirements and implement them consistently across all workloads in your cloud platform. The primary scope is operations tooling, which Microsoft also calls your operations baseline. Microsoft puts advanced operations, tech platform operations and workload operations out of scope. These are the later stages beyond the baseline (my plain words). They can be added later with the Manage methodology of the Cloud Adoption Framework (CAF, Microsoft's guidance for adopting the cloud).

Learn's design area is called "Management". Learn also places a page about monitoring the platform in the same design area, so monitoring is not a separate design area. That is why this post is called "Management and Monitoring".

## 2. Simple explanation

### Words you need first

Posts 1 to 11 defined these words: landing zone, workload, subscription, management group, intermediate root management group, Azure Policy, Azure RBAC, Microsoft Entra ID, managed identity, Log Analytics workspace, Azure Monitor Logs, activity log, Microsoft Defender for Cloud, Microsoft Sentinel, SIEM, ExpressRoute, recovery time objective (RTO), recovery point objective (RPO), Azure Backup, Azure Site Recovery, data residency, subscription democratization, brownfield and Microsoft Entra ID P1 or P2.

The words below are new, or are explained more fully here. Each is in plain words, based on Microsoft Learn. Where a row says "my plain words", the explanation is mine, not Microsoft's.

| Word | What it means |
|---|---|
| Operations baseline | Microsoft's name for the initial set of operations tooling that is used across all workloads. |
| Inventory and visibility | My plain words: knowing what you have and seeing what it is doing. Microsoft says management controls that span the environment become more important as the environment grows. |
| Telemetry, metrics and logs | My plain words: telemetry is data that resources send out about themselves. Metrics are numbers, such as processor use. Logs are records of events. |
| Azure Monitor | My plain words: the Azure service that collects and analyzes this data. Azure Monitor Logs, the part that stores log data in a Log Analytics workspace, was defined in Post 11. |
| Administrative boundary | Microsoft says a Log Analytics workspace can be used as an administrative boundary. My plain words: a boundary that decides who can see which logs and how they are managed. |
| Diagnostic settings | My plain words: the settings on a resource that say which logs and metrics to send, and where. The reference architecture sets them for activity logs, virtual machines and platform as a service (PaaS) resources, which are cloud services where Azure runs the platform for you (my plain words). |
| Data retention | How long data is kept. Microsoft gives default periods: 30 days for Azure Monitor Logs, 30 days for Microsoft Entra reports (premium, meaning Microsoft Entra ID P1 or P2), and 90 days for the Azure activity log and Application Insights logs (Application Insights is Azure's application monitoring feature, my plain words). |
| Immutable storage and WORM | When you export logs to Azure Storage for retention beyond seven years, Microsoft says to use immutable storage with a write-once, read-many (WORM) policy. It makes data non-erasable and non-modifiable for a user-specified interval. |
| Resource lock | A lock on a subscription, resource group or resource that protects it from accidental deletion or change. There are two kinds: CanNotDelete (authorized users can read and modify but not delete) and ReadOnly (authorized users can read but not delete or update). Locks apply to everyone, whatever their role. |
| Deny policy | An Azure Policy effect that blocks resource deployments and settings that do not meet your standards. Microsoft says it does this by blocking requests before they are sent to resource providers (the Azure services that create resources). |
| Initiative | My plain words: a group of Azure Policy definitions that you assign together. |
| DeployIfNotExists | An Azure Policy effect that deploys something, such as alert rules, when a resource is created. |
| Alert, alert rule and action group | An alert is raised when monitoring data shows a possible problem. An alert rule (my plain words) is the condition that decides when an alert is raised. An action group is a collection of notification preferences and automated actions that says who is told and what happens when an alert fires. Notification types include voice call, SMS, push notification and email. |
| Alert processing rule | A rule that routes alerts to one or more action groups. Microsoft says service health alerts do not support alert processing rules. |
| Service health and resource health | Microsoft says to include service health events and resource health events in platform monitoring. My plain words: service health is about problems in Azure services, and resource health is about a single resource. |
| Traffic Analytics | A tool to gather deep insights about IP traffic within virtual networks (Post 10). |
| Configuration drift | My plain words: a resource or machine moving away from the configuration you expect. |
| Azure Automanage Machine Configuration | Microsoft says Azure Policy can also audit settings inside a machine, and that this validation is done by the Azure Automanage Machine Configuration extension and client (the software that Azure puts on the machine for this, my plain words). It checks operating system configuration, application configuration or presence, and environment settings. |
| Infrastructure as Code (IaC) | My plain words: managing infrastructure with code that you can repeat and review. Microsoft says it can help you monitor for configuration drift and keep your landing zone up to date. |
| Azure Update Manager | A unified service to help manage and govern updates for machines that run a server operating system, in Azure, on-premises or in other clouds (the last two connected by Azure Arc). You can monitor update compliance and install updates in real time or on a schedule. |
| Business continuity and disaster recovery (BCDR) | Keeping your data safe and your apps and workloads online when planned and unplanned outages occur. |
| Active-active and active-passive | Two availability patterns that Microsoft lists. My plain words: in active-active, more than one copy of a workload serves users at the same time. In active-passive, one copy serves users and another waits to take over. |
| Availability Zone | A separated group of one or more datacenters within an Azure region, with independent power, cooling and networking. If one zone has an outage, the other zones keep working. |
| Availability set | A logical grouping of virtual machines (VMs) that reduces the chance of failures bringing down related VMs at the same time. Microsoft says availability sets do not offer the same level of resiliency as availability zones. |
| VM and SKU | A VM is a virtual machine. A SKU (stock-keeping unit) is a specific size or type of a product. |
| Recovery Services vault | A vault that Azure Backup uses to store backups and provide built-in management of recovery points. Azure Backup also has a second vault type, the Backup vault. The business continuity page lists subscription limits on the number and size of Recovery Services vaults as something to consider. |
| Failover and failback | Failover means moving to a secondary location when the primary one is down. Failback means moving back when the primary is running again. |
| Azure Monitor baseline alerts (AMBA) | The name Microsoft's page uses for the framework solution that deploys baseline alerts with Azure Policy. |

### What the design area covers

Microsoft's overview page names three parts of the operations baseline and links a page for each. Learn also has a page on monitoring the platform components, which this post adds as a fourth part.

| Part | The question it answers |
|---|---|
| Inventory and visibility | Where do logs go, who sees them, and who is told about problems? |
| Operational compliance | How do you patch machines and notice when they drift away from the expected configuration? |
| Protect and recover | What basic business continuity and disaster recovery can every workload depend on? |
| Monitor the platform | Which alerts exist for the landing zone itself, and how are they deployed? |

### Inventory and visibility

Microsoft says the cloud operating model decisions you made early (Post 4) directly influence how management operations are delivered, and how centralized management is for your platform is a key example.

For basic inventory, Microsoft asks you to consider two things: using tools such as an Azure Monitor Log Analytics workspace as administrative boundaries, and deciding which teams should use the system-generated logs from the platform and who needs access to them.

Microsoft also lists the kinds of logging data to think about:

- **Application-centric platform monitoring.** Metrics and logs, which Microsoft says use a hot path and a cold path (my plain words: a fast route and a slower route). It lists operating system performance counters and custom metrics, and operating system logs such as Internet Information Services logs (Windows web server logs), Event Tracing for Windows, syslogs and resource health events.
- **Security audit logging.** Microsoft's aim is a horizontal security lens across the whole Azure estate. It lists possible integration with on-premises SIEM systems (Post 11) and with software as a service (SaaS) offerings, which are applications delivered as a service. The data it lists is Azure activity logs, Microsoft Entra audit reports, Azure diagnostic logs and metrics, Key Vault audit events, network security group (NSG) flow logs (records of traffic through an NSG, my plain words) and event logs. The tools it names are Azure Monitor, Azure Network Watcher (a network monitoring service, my plain words), Microsoft Defender for Cloud and Microsoft Sentinel.
- **Retention and archiving.** The default periods in the words list above, and a link to extending retention for a table in a Log Analytics workspace.
- **Operational requirements.** Dashboards with native or third-party tools, centralized roles for privileged activities, managed identities for access to Azure services, and resource locks to protect from editing and deleting.

Visibility questions from Microsoft: Which teams need to receive alert notifications? Do you have groups of services that need multiple teams to be notified? Do you have existing service management tools (my plain words: ticketing or IT service tools) that alerts must be sent to? Which services are business critical and need high priority notifications?

Microsoft's recommendations:

- Use a single Azure Monitor Logs workspace to manage platforms centrally, except where Azure RBAC, data sovereignty requirements and data retention policies need separate workspaces. Microsoft says centralized logging is critical to the visibility that operations teams need, and that a centralized workspace model reduces administrative effort and the chance of gaps in observability.
- Workload teams can deploy their own Log Analytics workspaces in their own subscriptions, next to the central platform workspace, for logs and metrics that are specific to their workload.
- Export logs to Azure Storage if your log retention requirements exceed seven years. Use immutable storage with a write-once, read-many policy. (Post 11 quotes two years for Azure activity logs. Here Microsoft's page speaks about log retention in general.)
- Use Azure Policy for access control and compliance reporting.
- Use Traffic Analytics.
- Use resource locks to prevent accidental deletion of critical shared services.
- Use deny policies to supplement Azure role assignments. Combined, Microsoft says they control who can deploy and configure resources and which resources they can deploy and configure.
- Include service health and resource health events in platform monitoring.
- Do not send raw log entries back to on-premises monitoring systems. Microsoft's principle is that data born in Azure stays in Azure. If you need on-premises SIEM integration, send critical alerts instead of logs.

### Operational compliance

Microsoft says your environments will keep growing, so you need capabilities that monitor for deviations from the expected configuration, and your tools should include automation wherever possible.

**Configuration drift.** Azure Policy can audit and remediate Azure resources and can audit settings inside a machine, using Azure Automanage Machine Configuration. Microsoft also says Infrastructure as Code can help you monitor for configuration drift and keep your landing zone up to date.

**Update management.** Microsoft asks four questions. Does your organization use update management tools, and can they cover the cloud, or do you need new ones? Which teams oversee update management? Do some groups of resources share update schedules? Do some groups of resources not update at the same time for business continuity reasons?

Microsoft's recommendations:

- Use Azure Update Manager as a long-term patching mechanism for Windows and Linux VMs. Enforce Update Manager configurations with Azure Policy so all VMs are included. Microsoft says this lets workload teams manage patch deployment for their VMs and gives the central IT team visibility and enforcement across all VMs.
- Use Azure Policy to monitor in-machine VM configuration drift. Enabling Machine Configuration audit capabilities through policy lets workload teams use the feature with little effort.

### Protect and recover

Microsoft says enterprise workloads have RTO and RPO requirements (Post 5), and that BCDR design should provide platform-level capabilities that meet them. To design that, capture the platform's disaster recovery (DR) requirements.

Design considerations from Microsoft:

- Application and data availability: RTO and RPO for each workload, and support for active-active and active-passive patterns.
- BCDR for PaaS services: native DR and high availability features, and geo-replication.
- Multiregion deployments for failover, with components close enough for performance.
- Running with reduced functionality or degraded performance during an outage.
- Whether workloads suit Availability Zones or availability sets: data sharing between zones, the effect on update domains (groups of VMs that are updated together, my plain words), what share of workloads can be under maintenance at once, and whether a VM SKU supports zones.
- Consistent backups for applications and data: snapshots of VMs, Azure Backup Recovery Services vaults and their subscription limits.
- Network connectivity during a failover: ExpressRoute bandwidth planning and traffic routing during a regional, zone or network outage.
- Planned and unplanned failovers: IP address consistency after failover and failback, keeping engineering DevOps capabilities, and Key Vault disaster recovery for application keys, certificates and secrets.
- Data residency: in-country or in-region rules that affect cross-region replication.

Design recommendations from Microsoft:

- Use Azure Site Recovery for Azure-to-Azure VM disaster recovery. Microsoft says it uses real-time replication and recovery automation, can run recovery drills without affecting production, and can use Azure Policy to enable replication and audit VM protection.
- Use native PaaS disaster recovery capabilities.
- Use Azure-native backup capabilities. Microsoft says Azure Backup and PaaS-native backup remove the need for third-party backup software and infrastructure, and that backup settings can be set, audited and enforced with Azure Policy.
- Use multiple regions and peering locations for ExpressRoute connectivity (peering locations are the places where your network connects to Azure's, my plain words).
- Avoid overlapping IP address ranges in production and DR networks. Microsoft says overlapping ranges need a failover process that can complicate and delay application failover.

### Monitor the platform landing zone

Microsoft says monitoring platform components helps your organization detect and resolve issues quickly, watch performance and health, and plan capacity.

Microsoft says baseline metric, activity log and log query alerts are available for the landing zone platform components and other selected components. Components with one or more alerts defined are: Azure ExpressRoute, Azure Firewall, Azure Virtual Network, Azure Virtual WAN, Azure Monitor Log Analytics workspace, Azure Private DNS zone, Azure Key Vault, Azure Virtual Machine and Azure Storage account.

Alerts only help if someone is told. Microsoft says to configure action groups with the right notification channels and to test the alerts. Following the principle of subscription democratization, configure at least one action group for each subscription. The action group should include at least an email notification channel. If you use alert processing rules to route alerts, note that service health alerts do not support them, so configure service health alerts directly with the action group.

To scale alerting, Microsoft describes a framework solution, called Azure Monitor baseline alerts (AMBA), that uses Azure Policy with the DeployIfNotExists effect. It deploys the alert rules, alert processing rules and action groups when you create a resource, in platform services and in landing zones. The default baseline can be changed, and you can write your own policies for other metrics. Microsoft says alerts are only deployed when the matching resources are created, which avoids unnecessary cost and keeps alert settings current at deployment time. The solution is part of the Azure landing zone installation experience, so new deployments can set up baseline alerting at installation time.

The Learn monitor page has a diagram of this baseline alert topology, which I describe here instead of redrawing. The initiatives for the platform management groups (connectivity, identity and management) apply to those groups. The landing zone initiative applies to the landing zones management group. The service health initiative and the notifications assets initiative apply at the intermediate root management group (Post 9), so they reach all subscriptions.

If you use another way to deploy alerts, such as Azure Resource Manager, Bicep, Terraform or the portal, Microsoft says its guidance for alerts, severity and thresholds still applies.

### Testing and existing environments

Microsoft says to test policies and alerting before a deployment to production, to make sure resources are properly monitored and to find problems early. It points to the testing approach for Azure landing zones.

For a brownfield environment (an existing Azure footprint, aligned to a landing zone or not), Microsoft gives three high-level steps for baseline monitoring: import the relevant policies and initiatives from the AMBA repository, assign the required policies, and remediate the noncompliant ones. If the environment is not aligned to a landing zone, import them to the top-most management group where you want to assign them.

### What the landing zone reference architecture includes

Microsoft says the reference architecture deployment includes key management and monitoring tools such as a Log Analytics workspace, Microsoft Defender for Cloud monitoring, and diagnostic settings for activity logs, virtual machines and PaaS resources sent to Log Analytics.

Centralized logging in the reference architecture is mainly about platform operations. Microsoft says the same workspace can be used for VM-based application logging, because in resource-centric access control mode (a workspace setting), Azure RBAC makes sure workload teams only see logs from their own resources. For non-compute resources, such as web apps or databases, workload teams can use their own Log Analytics workspaces. Workload teams can also duplicate some logs from the central workspace for their own efficiency, and Microsoft says this is a supported approach.

## 3. Diagram

![Management and monitoring in the landing zone. Three columns for the operations baseline. Inventory and visibility: a central logging workspace, guardrails (Azure Policy, deny policies, resource locks), service and resource health events, Traffic Analytics, and the rule that data born in Azure stays in Azure. Operational compliance: Azure Update Manager for patching, and Azure Policy and Machine Configuration for configuration drift. Protect and recover: Azure Site Recovery, Azure Backup, availability zones or sets, ExpressRoute in several regions and no overlapping IP ranges. Below, platform monitoring: policy initiatives assigned at management groups deploy alert rules, alert processing rules and action groups.](/diagrams/post-13-management-and-monitoring.svg)

*Simplified diagram, drawn by me with my own layout. Microsoft's monitor page has an alert-topology diagram, which I describe in the text instead of redrawing: [Monitor Azure platform landing zone components](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-monitor). Not an official Microsoft diagram. Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/), unmodified.*

## 4. What I have seen in production

### Mistakes to check for first

Most of these are risks I worked out from Microsoft's recommendations, one line each. The part after this list says which ones I saw myself.

- **Many workspaces with no reason.** Microsoft says to use a single workspace except where Azure RBAC, data sovereignty or retention rules need separate ones.
- **Alerts that nobody receives.** Microsoft says to configure action groups with real notification channels, at least one per subscription, and to test them.
- **Raw logs copied to on-premises tools.** Microsoft says data born in Azure stays in Azure, and to send critical alerts instead.
- **Retention never planned.** Microsoft gives the defaults (30 or 90 days), links to extending retention for a table in a workspace, and says to export to Azure Storage if you need more than seven years.
- **Critical shared services with no lock.** Microsoft says to use resource locks to prevent accidental deletion.
- **Machines outside the patching plan.** Microsoft says to enforce Update Manager with Azure Policy so all VMs are included.
- **No recovery drill.** Microsoft says Site Recovery can run drills without affecting production.
- **Overlapping IP ranges in production and DR.** Microsoft says this complicates and delays failover.
- **Alerts never tested before production.** Microsoft says to test policies and alerting before a deployment to production.

### From my own projects

In my own projects, three of the points above were real problems:

- **Alerts that nobody gets.** This was a real problem.
- **Patching gaps.** This was a real problem.
- **Disaster recovery and backup.** This was a real problem.

I leave out project details.

## 5. Repo

- Management for Azure environments: logging, patching, drift and alerts (my own short checklist): [management.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/management.md)
- Business continuity and disaster recovery questions for the platform (my own short checklist): [business-continuity.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/business-continuity.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Design area: Management for Azure environments](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management) · [Inventory and visibility](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-platform) · [Monitor platform landing zone components](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-monitor)

Where a sentence says "my plain words", it is my own explanation. The operational compliance and business continuity pages are linked from the first page. Short definitions of Azure Update Manager, action groups, resource locks, Availability Zones, availability sets, Azure Site Recovery and Azure Backup come from their own Learn overview pages. The mistakes list and the repo checklists are mine too.

