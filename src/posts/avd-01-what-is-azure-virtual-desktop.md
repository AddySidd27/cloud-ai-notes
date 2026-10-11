---
title: "What Is Azure Virtual Desktop?"
layout: post.njk
permalink: "/azure-virtual-desktop/what-is-azure-virtual-desktop/"
order: 101
part: 1
tags: [avd-series]
deck: "Understand what AVD delivers, why a business would use it and who manages each part."
---

Azure Virtual Desktop (AVD) delivers Windows desktops and applications remotely. In the Azure deployments covered by this series, they run on virtual machines called session hosts. Users connect from their own devices to work on those machines.

This first post explains what users receive, why a business might choose AVD, and which parts Microsoft and your team manage. The series then moves through preparation, deployment and production operations.

## Key terms

| Term | Meaning |
|---|---|
| Virtual machine (VM) | A software-based computer. |
| Session host | A machine registered with AVD that runs users' desktops or applications. |
| Host pool | A collection of session hosts. |
| Application group | Controls access to a desktop or a set of published applications from one host pool. |
| Workspace | Groups application groups so users can see their assigned desktops and apps. |
| RemoteApp | An individual published application accessed without opening a full desktop. |

## Full desktop or RemoteApp

A full desktop gives the user a remote Windows desktop and its applications. RemoteApp gives them individual applications without opening that desktop.

Both pooled and personal host pools can deliver full desktops. RemoteApp application groups are available with pooled host pools.

## Pooled or personal desktops

| Host pool type | What the user receives |
|---|---|
| Pooled | Access to shared session hosts. A supported multi-session operating system lets several users work on one host in separate sessions. |
| Personal | A session host assigned to that individual user. |

In a pooled deployment, users can reach a different host after signing out and signing in again. FSLogix keeps their Windows profile - account settings and profile data - on shared storage. Applications use that profile as though it were stored locally.

## Why a business would use AVD

Businesses use AVD to make Windows applications available remotely, share desktop resources and adjust capacity around demand. These benefits come from different parts of the service.

**Give users the application they need, wherever they work.**

AVD can publish existing Windows business applications for remote access. Users connect through a supported app or browser. If they only need one application, RemoteApp can deliver it without a full desktop. If their work needs a complete Windows environment, you can provide that instead.

**Share desktop resources between users.**

A separate virtual machine for every employee is not always necessary. With a pooled, multi-session deployment, several users can work on the same machine in separate sessions. Microsoft identifies this as a way to reduce the number of VMs and operating-system overhead. The practical benefit is shared capacity; how many users a host can support still depends on their workload.

**Run capacity around working hours.**

Demand changes during the day. Autoscale can start and stop session hosts using schedules and capacity thresholds. For example, a weekday schedule can prepare capacity before people start work and reduce it as usage falls. This can reduce compute costs. Turning off hosts does not remove every charge: disks, profile storage and other resources still need to be included in the budget.

**Let Microsoft run the broker and gateway.**

With a traditional Remote Desktop Services deployment, the organization operates supporting infrastructure such as the connection broker and gateway. With AVD, Microsoft operates those service components. Your team still manages the desktops themselves: their images, applications, updates, access and supporting resources. Microsoft operates the connection services; your team operates the Windows environment people work in.

**Understand the cost before choosing it.**

AVD has both Azure resource costs and licensing requirements. An estimate needs the number of users working at the same time, their working hours, VM capacity, storage, networking and any supporting services. Shared hosts and autoscale offer ways to reduce costs; the final bill depends on the deployment. There is no fixed saving that applies to every business.

## Read the architecture diagram

![AVD components grouped by Microsoft and customer responsibilities](/img/avd/AVD-Post-01-Components.png)

The diagram groups components by who manages them. The upper group is Microsoft's service infrastructure. The lower group contains the session hosts and user identities you manage.

| Component | Role |
|---|---|
| Web service | Returns the user's connection information to their device. |
| Broker service | Coordinates incoming connections. |
| Gateway service | Provides remote desktop connectivity between the user's device and session host. |
| Resource directory | Identifies which database holds the user's connection information. |
| Geographical database | Stores connection files and resource icons across the host pool's geography. |
| Regional database | Stores that information within the host pool's region. |
| Session hosts | Run the users' desktops and applications. |
| User identities | Identify the users whose access you manage. |

You choose the session-host images and applications, configure network connectivity, and manage identities and access. Your team is also responsible for the resilience, backup and recovery of the session hosts. Microsoft manages the service components shown above them.

The next post follows a user connection through these components and explains the responsibilities in more detail.

## How users connect

Users access their assigned desktops and applications through Windows App on a supported device or through its web experience. They sign in with a work or school account. AVD does not support personal Microsoft accounts for user access.

You assign users to application groups and associate those groups with a workspace so users can see their published resources. The application runs on a session host; Windows App provides access from the user's device.

## What must be ready before deployment

| Requirement | What to prepare |
|---|---|
| Azure subscription | An active subscription for the deployment. |
| Identity | User accounts in Microsoft Entra ID and a supported identity configuration for the session hosts. |
| Operating system | A supported Windows edition and version for the session hosts. |
| Licensing | The appropriate user access rights for the operating system and commercial-use scenario. |
| Networking | Connectivity for the AVD service, identity services, applications and data. |
| Administrative access | The Azure permissions needed to create and configure the resources. |
| User access | A supported client or web experience and the required resource assignments. |

An Azure subscription and user licensing are separate requirements. Windows client and Windows Server deployments have different licensing options. The preparation posts will explain the supported choices before we create resources.

## Where the series goes next

After the architecture, we will prepare the tenant, subscription, identity and network. Then we will build the host pool, configure profiles and applications, and validate user access. Later posts cover security, image maintenance, monitoring, scaling and recovery.

Deployment posts will include numbered steps, real screenshots, expected results, troubleshooting and cleanup. Production decisions will be explained alongside the configuration they affect.

Next: **Azure Virtual Desktop Architecture: From Sign-in to a Working Desktop**.

## References

Microsoft Learn: [Overview](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview) · [Terminology](https://learn.microsoft.com/en-us/azure/virtual-desktop/terminology) · [Architecture](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience) · [Prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites).

[Windows App](https://learn.microsoft.com/en-us/windows-app/overview) · [FSLogix](https://learn.microsoft.com/en-us/fslogix/overview-what-is-fslogix) · [Autoscale](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-create-assign-scaling-plan) · [Costs](https://learn.microsoft.com/en-us/azure/virtual-desktop/understand-estimate-costs) · [Security responsibilities](https://learn.microsoft.com/en-us/azure/virtual-desktop/security-recommendations).
