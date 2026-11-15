---
title: "Windows 365 Enterprise: Start Here"
layout: post.njk
permalink: /windows-365/start-here/
order: 201
part: 1
tags: w365-series
deck: "A beginner's guide to Windows 365 Cloud PCs, from the first decision to daily operations."
---

Windows 365 gives an assigned user a Cloud PC, a Windows desktop they reach from a supported device or a browser. The organization manages it with Microsoft Intune, Microsoft's device management service. This series is for IT administrators who are new to Windows 365 Enterprise, the edition your organization's IT team manages. It follows one pilot (a small trial rollout with a few users) from planning to support. Each article says what to do in your own tenant and what to check.

## Words to know

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop assigned to a user through Windows 365. |
| Tenant | Your organization's Microsoft Entra ID directory. |
| Microsoft Entra join | The Cloud PC is joined to Microsoft Entra ID without an on-premises AD DS device join. |
| Provisioning policy | The Intune configuration that defines the Cloud PC's join type, network, image and assignment. |
| Microsoft-hosted network | The network option managed by Microsoft for the Cloud PC. It does not require your Azure subscription for Cloud PC networking. |
| Azure network connection (ANC) | An object in the Intune admin center that tells a provisioning policy which Azure subnet to place the Cloud PC's network interface in. It needs subnet, DNS and outbound access planning. |
| ANC health check | A test that Windows 365 runs on an ANC to confirm provisioning can succeed. A policy can use an ANC only after its checks succeed or succeed with warnings. |
| NAT gateway, public IP | Azure resources that give a subnet outbound internet access through a public IP address. |
| AD DS | Active Directory Domain Services, the on-premises directory. |
| Hybrid join | A Cloud PC joined to both on-premises Active Directory and Microsoft Entra ID. It needs an ANC; the Microsoft-hosted network supports only Microsoft Entra join. |
| Conditional Access | Microsoft Entra rules that decide who can sign in and under which conditions. Report-only mode logs what a rule would do without enforcing it. |
| Company Portal | The Intune app where users see and install the apps assigned to them. |

## The route through the series

- [Start Here](/windows-365/start-here/): this page.
- [Plan a Pilot That You Can Verify](/windows-365/plan-the-pilot/): check the license, [requirements](https://learn.microsoft.com/windows-365/enterprise/requirements), administrator role and pilot group, and write success criteria first.
- [Choose Identity and Network](/windows-365/identity-network/): start with Microsoft Entra join and a Microsoft-hosted network, which Microsoft calls the [recommended option for most scenarios](https://learn.microsoft.com/windows-365/enterprise/windows-365-network-deployment-options). Add an ANC when an application needs customer-controlled routing, DNS or private connectivity. Hybrid join has more AD DS and DNS dependencies and is best tested separately.
- [Provision a Microsoft Entra Joined Cloud PC](/windows-365/provision/): create a provisioning policy, assign it to the pilot group and record the join type, network, image, region and group.
- [Connect and Verify the Cloud PC](/windows-365/connect-verify/): ask the assigned user to open [windows.cloud.microsoft](https://windows.cloud.microsoft/), reach the desktop, disconnect and reconnect. An object in the portal does not prove the session works.
- [Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/): test one setting, one app and one update policy at a time, and compare the assignment with the state inside the Cloud PC.
- [Point-in-Time Restore](/windows-365/point-in-time-restore/): how restore points work and the admin and user paths.
- [Secure Access and Plan Recovery](/windows-365/security-recovery/): start Conditional Access in report-only mode, read sign-in logs, and keep an emergency administrator account that Conditional Access does not block.
- [Reading an ANC Health Failure](/windows-365/anc-troubleshooting/): how to read a failed ANC health check. Keep the working Microsoft-hosted Cloud PC and test the ANC with a separate user and group.
- [Operate, Roll Out and Extend](/windows-365/operate-and-extend/): support ownership, staged rollout, license checks, recovery steps and cost review.

The [editable draw.io diagrams](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/architecture) compare the Microsoft-hosted and ANC paths.

Next: [Windows 365 Enterprise: Plan a Pilot That You Can Verify](/windows-365/plan-the-pilot/).

## Sources

- [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Network deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options)
- [Create a provisioning policy](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)
