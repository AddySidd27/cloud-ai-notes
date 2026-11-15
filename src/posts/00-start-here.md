---
title: "Start Here: How This Blog Works and What to Read First"
seoTitle: "Start Here: What to Read First"
slug: "start-here"
series: "Start Here"
part: ""
post_number: 0
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/azure/architecture/landing-zones/azure-virtual-desktop/design-guide"
    checked_on: "2026-10-13"
  - url: "https://learn.microsoft.com/en-us/azure/virtual-desktop/overview"
    checked_on: "2026-10-13"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone"
  - "https://github.com/AddySidd27/Windows365-enterprise-engineering"
diagrams: []
layout: post.njk
permalink: "/start-here/"
order: 0
deck: "This page shows what to read first. The articles cover Azure landing zones, Azure Virtual Desktop and Windows 365. They are in reading order, and you can start with no background."
next_num: ""
next_title: ""
---

## Pick your route

- **I am new:** start with [What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/), then follow the [Azure Landing Zone series](/azure-landing-zone/) in order. An Azure landing zone is the prepared Azure environment that your workloads run in. Later sections explain it in full.
- **I have 15 minutes:** read that same first post. It is the shortest way to learn what the rest of the blog builds on.
- **After the design-area posts:** read [the greenfield rollout post](/azure-landing-zone/greenfield-rollout/) if you are starting fresh (greenfield means a new environment with nothing built yet), or [the brownfield rollout post](/azure-landing-zone/brownfield-rollout/) if you already have an Azure environment (brownfield). They use words defined in the earlier posts.
- **I already know landing zones:** go to the [Azure Virtual Desktop series](/azure-virtual-desktop/) and start with [What Is Azure Virtual Desktop?](/azure-virtual-desktop/what-is-azure-virtual-desktop/).
- **I am here for Windows 365:** start with [Windows 365 Enterprise: Start Here](/windows-365/start-here/).

## Who this is for

- Engineers and architects who run, or are about to run, Azure Virtual Desktop (AVD), Microsoft's desktop and app virtualization service that runs on Azure.
- People who know some Azure and want the foundation done properly before they build workloads on it.
- Anyone preparing for work or exams around AVD and Azure architecture.

You do not need to know any of these topics. Each post explains its new words first. The blog is a guided reading of the official documentation, not a replacement for it.

## The series

The posts below are listed in reading order.

### [Azure Landing Zone](/azure-landing-zone/)

What a landing zone is, the eight design areas (topics such as identity, network and security), what to build first, how to roll one out new (greenfield) or into an existing environment (brownfield), and use cases. 18 posts.

- [What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/)
- [Platform Scope and Workload Boundaries](/azure-landing-zone/platform-scope-and-workload-boundaries/)
- [Tenant, Billing, Subscriptions and Management Groups](/azure-landing-zone/tenant-billing-subscriptions-and-management-groups/)
- [The Cloud Operating Model](/azure-landing-zone/the-cloud-operating-model/)
- [Business Requirements: Compliance, Region, Recovery, Connectivity and Cost](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/)
- [Billing and the Microsoft Entra Tenant, in Depth](/azure-landing-zone/billing-and-tenant-in-depth/)
- [Identity and Access in the Landing Zone](/azure-landing-zone/identity-and-access-in-the-landing-zone/)
- [Privileged Access: MFA, Conditional Access and PIM](/azure-landing-zone/privileged-access-mfa-conditional-access-and-pim/)
- [Resource Organization](/azure-landing-zone/resource-organization/)
- [Network Topology and Connectivity](/azure-landing-zone/network-topology-and-connectivity/)
- [Security](/azure-landing-zone/security/)
- [Management and Monitoring](/azure-landing-zone/management-and-monitoring/)
- [Governance and Azure Policy](/azure-landing-zone/governance-and-azure-policy/)
- [Platform Automation and DevOps](/azure-landing-zone/platform-automation-and-devops/)
- [Minimum Viable Platform Landing Zone: What to Build First](/azure-landing-zone/minimum-viable-platform-landing-zone/)
- [Greenfield Rollout](/azure-landing-zone/greenfield-rollout/)
- [Brownfield Rollout](/azure-landing-zone/brownfield-rollout/)
- [Landing Zone Use Cases](/azure-landing-zone/landing-zone-use-cases/)

### [Azure Virtual Desktop](/azure-virtual-desktop/)

What AVD is, its architecture and how it fails, then identity, network, host pools, sign-in, FSLogix user profiles (the service that stores each user's profile in a container), images, applications and day-to-day operation. 25 posts.

- [What Is Azure Virtual Desktop?](/azure-virtual-desktop/what-is-azure-virtual-desktop/)
- [Azure Virtual Desktop Architecture: From Sign-in to a Working Desktop](/azure-virtual-desktop/azure-virtual-desktop-architecture/)
- [Prepare Your Azure Environment for Azure Virtual Desktop](/azure-virtual-desktop/prepare-your-azure-environment/)
- [Choose the Right Identity Model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/)
- [Plan Azure Virtual Desktop Networking: Address Space, Subnets, DNS and Connectivity](/azure-virtual-desktop/plan-avd-networking/)
- [Plan Your AVD Host Pools: Users, Applications, VM Sizing and Images](/azure-virtual-desktop/plan-your-host-pools/)
- [Decide Whether Azure Virtual Desktop Fits](/azure-virtual-desktop/decide-whether-azure-virtual-desktop-fits/)
- [How Azure Virtual Desktop Fails: The Control, Management and Data Planes](/azure-virtual-desktop/how-azure-virtual-desktop-fails/)
- [Host Pools, Application Groups and Workspaces: The Rules That Connect Them](/azure-virtual-desktop/host-pool-application-group-workspace-rules/)
- [Follow a Connection Step by Step: Reverse Connect, RDP Shortpath and Where It Breaks](/azure-virtual-desktop/follow-a-connection-step-by-step/)
- [Choose the Session Host Operating System and Licensing](/azure-virtual-desktop/session-host-operating-system-and-licensing/)
- [Choose the Client: Windows App, Remote Desktop and the Web](/azure-virtual-desktop/choose-the-avd-client/)
- [How Sign-in Works: Three Authentications and Single Sign-on](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/)
- [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/)
- [Who Can Administer Azure Virtual Desktop: Roles, Scopes and Delegation](/azure-virtual-desktop/who-can-administer-azure-virtual-desktop/)
- [Required Connectivity for Azure Virtual Desktop: Endpoints, Proxies, DNS and Private Link](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/)
- [Choose a Network Topology and Plan IP Addresses for Azure Virtual Desktop](/azure-virtual-desktop/network-topology-and-ip-planning-for-avd/)
- [How FSLogix Profile Containers Work](/azure-virtual-desktop/how-fslogix-profile-containers-work/)
- [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/)
- [Build and Maintain a Golden Image](/azure-virtual-desktop/build-and-maintain-a-golden-image/)
- [Create, Update and Replace Session Hosts](/azure-virtual-desktop/create-update-replace-session-hosts/)
- [Deliver Applications with RemoteApp and App Attach](/azure-virtual-desktop/deliver-applications-remoteapp-app-attach/)
- [Plan Bandwidth, Latency and Quality of Service for Azure Virtual Desktop](/azure-virtual-desktop/plan-bandwidth-latency-and-quality-of-service/)
- [Choose Session Host VM Sizes: Compute, GPU, Disks and Quota](/azure-virtual-desktop/choose-session-host-vm-sizes/)
- [Operate FSLogix Profiles Day to Day: Cloud Cache, Size, Locks and Corruption](/azure-virtual-desktop/operate-fslogix-profiles-day-to-day/)

### [Windows 365 Enterprise](/windows-365-enterprise/)

A pilot of Cloud PCs (Windows desktops that Microsoft runs for each user), from planning to daily operations. 10 articles.

- [Windows 365 Enterprise: Start Here](/windows-365/start-here/)
- [Windows 365 Enterprise: Plan a Pilot That You Can Verify](/windows-365/plan-the-pilot/)
- [Windows 365 Enterprise: Choose Identity and Network](/windows-365/identity-network/)
- [Windows 365 Enterprise: Provision a Microsoft Entra Joined Cloud PC](/windows-365/provision/)
- [Windows 365 Enterprise: Connect and Verify the Cloud PC](/windows-365/connect-verify/)
- [Windows 365 Enterprise: Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/)
- [Windows 365 Enterprise: Point-in-Time Restore](/windows-365/point-in-time-restore/)
- [Windows 365 Enterprise: Secure Access and Plan Recovery](/windows-365/security-recovery/)
- [Windows 365 Enterprise: Reading an ANC Health Failure](/windows-365/anc-troubleshooting/)
- [Windows 365 Enterprise: Operate, Roll Out and Extend](/windows-365/operate-and-extend/)

### [Terraform labs](/terraform-labs/)

Four labs that build Azure Virtual Desktop environments from Terraform code, from a first host pool to monitoring.

- [Deploy an AVD Quick Lab with Terraform: Host Pool, Two Session Hosts and FSLogix Profiles](/terraform-labs/avd-quick-lab/)
- [AVD Autoscale Lab with Terraform: Weekday and Weekend Schedules and How to Measure the Saving](/terraform-labs/avd-autoscale-cost-lab/)
- [Add a Cost Budget and Alerts to Your AVD Lab with Terraform](/terraform-labs/avd-budget-alert-lab/)
- [AVD Monitoring Starter Lab with Terraform: Log Analytics, Insights Data and One Alert](/terraform-labs/avd-monitoring-lab/)

## Why the landing zone comes first

A workload is an application or service you run in the cloud, and AVD is one. An Azure landing zone is the prepared Azure environment that workloads run in. Microsoft's documentation says it provides the foundation for cloud workloads such as AVD and defines components like governance, security, networking, identity and operations. A platform landing zone is the part that holds shared services such as networking and identity.

Microsoft's AVD reference implementation (its sample deployment code) requires you to deploy a platform landing zone first, so the blog builds AVD on top of that foundation. Security is covered inside each topic, and the [Security](/azure-landing-zone/security/) post brings the platform-level controls together.

## How the articles are written

Each article defines new terms before it uses them and ends with a short list of sources. Diagrams are simplified and use the official Azure architecture icons.

## The public repositories

A repo is a folder of files on GitHub. [Azure_landing_zone](https://github.com/AddySidd27/Azure_landing_zone) is a public learning lab built with Terraform (a tool that creates Azure resources from code). It is not production-ready and it is not the official accelerator (Microsoft's ready-made deployment code for landing zones). Use it to see how the parts fit together, and use the official accelerator for real environments. The Windows 365 articles use their own repo, [Windows365-enterprise-engineering](https://github.com/AddySidd27/Windows365-enterprise-engineering).

## Sources

- [AVD landing zone design guide](https://learn.microsoft.com/azure/architecture/landing-zones/azure-virtual-desktop/design-guide)
- [What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)

## Start reading

[What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/)
