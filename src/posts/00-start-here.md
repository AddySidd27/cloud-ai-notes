---
title: "Start Here: How This Blog Works and What to Read First"
seoTitle: "Start Here: What to Read First"
slug: "start-here"
series: "Start Here"
part: ""
post_number: 0
status: draft
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
production_section_written_by_addy: false
layout: post.njk
permalink: "/start-here/"
order: 0
deck: "This blog explains Azure Landing Zone, Azure Virtual Desktop and Windows 365 in reading order, so you can start with no background and build up one step at a time."
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

## The three series

The posts below are listed in reading order.

### [Azure Landing Zone](/azure-landing-zone/)

What a landing zone is, the eight design areas (topics such as identity, network and security), what to build first, how to roll one out new (greenfield) or into an existing environment (brownfield), and use cases. 18 posts.

1. [What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/)
2. [Platform Scope and Workload Boundaries](/azure-landing-zone/platform-scope-and-workload-boundaries/)
3. [Tenant, Billing, Subscriptions and Management Groups](/azure-landing-zone/tenant-billing-subscriptions-and-management-groups/)
4. [The Cloud Operating Model](/azure-landing-zone/the-cloud-operating-model/)
5. [Business Requirements: Compliance, Region, Recovery, Connectivity and Cost](/azure-landing-zone/business-requirements-compliance-region-recovery-connectivity-and-cost/)
6. [Billing and the Microsoft Entra Tenant, in Depth](/azure-landing-zone/billing-and-tenant-in-depth/)
7. [Identity and Access in the Landing Zone](/azure-landing-zone/identity-and-access-in-the-landing-zone/)
8. [Privileged Access: MFA, Conditional Access and PIM](/azure-landing-zone/privileged-access-mfa-conditional-access-and-pim/)
9. [Resource Organization](/azure-landing-zone/resource-organization/)
10. [Network Topology and Connectivity](/azure-landing-zone/network-topology-and-connectivity/)
11. [Security](/azure-landing-zone/security/)
12. [Management and Monitoring](/azure-landing-zone/management-and-monitoring/)
13. [Governance and Azure Policy](/azure-landing-zone/governance-and-azure-policy/)
14. [Platform Automation and DevOps](/azure-landing-zone/platform-automation-and-devops/)
15. [Minimum Viable Platform Landing Zone: What to Build First](/azure-landing-zone/minimum-viable-platform-landing-zone/)
16. [Greenfield Rollout](/azure-landing-zone/greenfield-rollout/)
17. [Brownfield Rollout](/azure-landing-zone/brownfield-rollout/)
18. [Landing Zone Use Cases](/azure-landing-zone/landing-zone-use-cases/)

### [Azure Virtual Desktop](/azure-virtual-desktop/)

What AVD is, its architecture and how it fails, then identity, network, host pools, sign-in, FSLogix user profiles (the service that stores each user's profile in a container), images, applications and day-to-day operation. 25 posts.

1. [What Is Azure Virtual Desktop?](/azure-virtual-desktop/what-is-azure-virtual-desktop/)
2. [Azure Virtual Desktop Architecture: From Sign-in to a Working Desktop](/azure-virtual-desktop/azure-virtual-desktop-architecture/)
3. [Prepare Your Azure Environment for Azure Virtual Desktop](/azure-virtual-desktop/prepare-your-azure-environment/)
4. [Choose the Right Identity Model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/)
5. [Plan Azure Virtual Desktop Networking: Address Space, Subnets, DNS and Connectivity](/azure-virtual-desktop/plan-avd-networking/)
6. [Plan Your AVD Host Pools: Users, Applications, VM Sizing and Images](/azure-virtual-desktop/plan-your-host-pools/)
7. [Decide Whether Azure Virtual Desktop Fits](/azure-virtual-desktop/decide-whether-azure-virtual-desktop-fits/)
8. [How Azure Virtual Desktop Fails: The Control, Management and Data Planes](/azure-virtual-desktop/how-azure-virtual-desktop-fails/)
9. [Host Pools, Application Groups and Workspaces: The Rules That Connect Them](/azure-virtual-desktop/host-pool-application-group-workspace-rules/)
10. [Follow a Connection Step by Step: Reverse Connect, RDP Shortpath and Where It Breaks](/azure-virtual-desktop/follow-a-connection-step-by-step/)
11. [Choose the Session Host Operating System and Licensing](/azure-virtual-desktop/session-host-operating-system-and-licensing/)
12. [Choose the Client: Windows App, Remote Desktop and the Web](/azure-virtual-desktop/choose-the-avd-client/)
13. [How Sign-in Works: Three Authentications and Single Sign-on](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/)
14. [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/)
15. [Who Can Administer Azure Virtual Desktop: Roles, Scopes and Delegation](/azure-virtual-desktop/who-can-administer-azure-virtual-desktop/)
16. [Required Connectivity for Azure Virtual Desktop: Endpoints, Proxies, DNS and Private Link](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/)
17. [Choose a Network Topology and Plan IP Addresses for Azure Virtual Desktop](/azure-virtual-desktop/network-topology-and-ip-planning-for-avd/)
18. [How FSLogix Profile Containers Work](/azure-virtual-desktop/how-fslogix-profile-containers-work/)
19. [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/)
20. [Build and Maintain a Golden Image](/azure-virtual-desktop/build-and-maintain-a-golden-image/)
21. [Create, Update and Replace Session Hosts](/azure-virtual-desktop/create-update-replace-session-hosts/)
22. [Deliver Applications with RemoteApp and App Attach](/azure-virtual-desktop/deliver-applications-remoteapp-app-attach/)
23. [Plan Bandwidth, Latency and Quality of Service for Azure Virtual Desktop](/azure-virtual-desktop/plan-bandwidth-latency-and-quality-of-service/)
24. [Choose Session Host VM Sizes: Compute, GPU, Disks and Quota](/azure-virtual-desktop/choose-session-host-vm-sizes/)
25. [Operate FSLogix Profiles Day to Day: Cloud Cache, Size, Locks and Corruption](/azure-virtual-desktop/operate-fslogix-profiles-day-to-day/)

### [Windows 365 Enterprise](/windows-365-enterprise/)

A pilot of Cloud PCs (Windows desktops that Microsoft runs for each user) from planning to operations. The posts keep results that were observed in a lab apart from procedures. 10 posts.

1. [Windows 365 Enterprise: Start Here](/windows-365/start-here/)
2. [Windows 365 Enterprise: Plan a Pilot That You Can Verify](/windows-365/plan-the-pilot/)
3. [Windows 365 Enterprise: Choose Identity and Network](/windows-365/identity-network/)
4. [Windows 365 Enterprise: Provision a Microsoft Entra Joined Cloud PC](/windows-365/provision/)
5. [Windows 365 Enterprise: Connect and Verify the Cloud PC](/windows-365/connect-verify/)
6. [Windows 365 Enterprise: Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/)
7. [Windows 365 Enterprise: Point-in-Time Restore](/windows-365/point-in-time-restore/)
8. [Windows 365 Enterprise: Secure Access and Plan Recovery](/windows-365/security-recovery/)
9. [Windows 365 Enterprise: Reading an ANC Health Failure](/windows-365/anc-troubleshooting/)
10. [Windows 365 Enterprise: Operate, Roll Out and Extend](/windows-365/operate-and-extend/)

## Why the landing zone comes first

A workload is an application or service you run in the cloud, and AVD is one. An Azure landing zone is the prepared Azure environment that workloads run in. Microsoft Learn says it provides the foundation for cloud workloads such as AVD and defines components like governance, security, networking, identity and operations. A platform landing zone is the part that holds shared services such as networking and identity. Microsoft's AVD reference implementation (its sample deployment code) requires you to deploy a platform landing zone first, so the blog builds AVD on top of that foundation. (judgement: this reading order is my own plan.) Security is covered inside each topic, and the [Security](/azure-landing-zone/security/) post brings the platform-level controls together.

## How each post is built

- Each post defines its new terms before it uses them.
- A post that has a diagram shows it near the top. Not every post has one.
- Each post lists the Microsoft Learn pages it is based on, with the month I checked them, and says what comes next.
- The Azure Landing Zone posts also list common mistakes, what I have seen in my own projects (they say so when I have nothing to report) and the matching repo file.

My rules:

- Facts come from official Microsoft documentation. If a statement is my own opinion or experience and is not on Microsoft Learn, the post labels it "(judgement)".
- If a feature is in Preview (not yet generally available), the post says so, and I check it again before publishing.
- If a post uses a fictional case study, it is labelled fictional. It is a worked example, not customer work.
- Diagrams are simplified. They use the official Azure architecture icons. Where Microsoft Learn has a diagram for the topic, the picture follows its layout and the caption links to that page. Where Learn has none, the caption says so and names the page the text comes from.

## How the repo labs fit in

A repo is a folder of files on GitHub. [Azure_landing_zone](https://github.com/AddySidd27/Azure_landing_zone) is my public learning and reference lab. It is built with Terraform (a tool that creates Azure resources from code). It is not production-ready and it is not the official accelerator (Microsoft's ready-made deployment code for landing zones). Use it to see how the parts fit together, and use the official accelerator for real environments. [lab-vs-enterprise.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/lab-vs-enterprise.md) lists what a personal lab can and cannot reproduce, and [learning-path.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/00-start-here/learning-path.md) gives a suggested reading order. The Windows 365 posts link to their own repo, [Windows365-enterprise-engineering](https://github.com/AddySidd27/Windows365-enterprise-engineering).

## What the posts show as evidence

The evidence differs by series, and each post says what it did and did not test.

- **Azure Landing Zone:** no post includes a real deployment yet. The repo's status table says real-deployment evidence is not published.
- **Azure Virtual Desktop:** some posts, such as [Prepare Your Azure Environment for Azure Virtual Desktop](/azure-virtual-desktop/prepare-your-azure-environment/), show screenshots from an existing development environment, with account details hidden. They are inventory checks, not a full deployment.
- **Windows 365:** posts such as [Provision a Microsoft Entra Joined Cloud PC](/windows-365/provision/) show captures from an existing Cloud PC and an unsaved draft policy in my own tenant, dated October 12, 2026. They do not show a fresh end-to-end provisioning run.

## About me

I am Addy (Adnan Ahmed), a Senior Solutions Architect with 15 years in enterprise IT. The [About page](/about/) has more.

## Sources

Microsoft Learn, checked October 2026: [AVD landing zone design guide](https://learn.microsoft.com/azure/architecture/landing-zones/azure-virtual-desktop/design-guide) · [What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)

## Start reading

[What Is an Azure Landing Zone](/azure-landing-zone/what-is-an-azure-landing-zone/)
