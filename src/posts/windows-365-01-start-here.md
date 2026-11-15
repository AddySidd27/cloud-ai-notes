---
title: "Windows 365 Enterprise: Start Here"
layout: post.njk
permalink: /windows-365/start-here/
order: 201
part: 1
tags: w365-series
deck: "A beginner's guide to Windows 365 Cloud PCs, from the first decision to daily operations. It says what was tested and what was not."
---

Windows 365 gives an assigned user a Cloud PC, a Windows desktop they reach from a supported device or a browser. The organization manages it with Microsoft Intune, Microsoft's device management service. This series is for IT administrators who are new to Windows 365 Enterprise, the edition your organization's IT team manages. It follows one pilot (a small trial rollout with a few users) from planning to support. Each chapter says what to do in your own tenant, what to check, and what I saw in my own lab.

## Words to know

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop assigned to a user through Windows 365. |
| Tenant | Your organization's Microsoft Entra ID directory. |
| Microsoft Entra join | The Cloud PC is joined to Microsoft Entra ID without an on-premises AD DS device join. |
| Provisioning policy | The Intune configuration that defines the Cloud PC's join type, network, image and assignment. |
| Microsoft-hosted network | The network option managed by Microsoft for the Cloud PC. It does not require your Azure subscription for Cloud PC networking. |
| Azure network connection (ANC) | An object in the Intune admin center that tells a provisioning policy which Azure subnet to place the Cloud PC's network interface in. It needs subnet, DNS and outbound access planning. |
| ANC health check | A test that Windows 365 runs on an ANC to confirm provisioning can succeed ([Azure network connection health checks](https://learn.microsoft.com/windows-365/enterprise/health-checks)). A policy can use an ANC only after its checks succeed or succeed with warnings. |
| NAT gateway, public IP | Azure resources that give a subnet outbound internet access through a public IP address. I created them temporarily for the ANC test. |
| AD DS | Active Directory Domain Services, the on-premises directory. |
| Hybrid join | A Cloud PC joined to both on-premises Active Directory and Microsoft Entra ID. It needs an ANC; the Microsoft-hosted network supports only Microsoft Entra join. |
| Conditional Access | Microsoft Entra rules that decide who can sign in and under which conditions. Report-only mode logs what a rule would do without enforcing it. |
| Company Portal | The Intune app where users see and install the apps assigned to them. |

<a id="read-the-complete-series"></a>

## The route through the series

1. [Start Here](/windows-365/start-here/): this page.
2. [Plan a Pilot That You Can Verify](/windows-365/plan-the-pilot/): check the license, [requirements](https://learn.microsoft.com/windows-365/enterprise/requirements), administrator role and pilot group, and write success criteria first.
3. [Choose Identity and Network](/windows-365/identity-network/): start with Microsoft Entra join and a Microsoft-hosted network, which Microsoft calls the [recommended option for most scenarios](https://learn.microsoft.com/windows-365/enterprise/windows-365-network-deployment-options). Add an ANC when an application needs customer-controlled routing, DNS or private connectivity. Hybrid join has more AD DS and DNS dependencies and belongs in a separate lab.
4. [Provision a Microsoft Entra Joined Cloud PC](/windows-365/provision/): create a provisioning policy, assign it to the pilot group and record the join type, network, image, region and group.
5. [Connect and Verify the Cloud PC](/windows-365/connect-verify/): ask the assigned user to open [windows.cloud.microsoft](https://windows.cloud.microsoft/), reach the desktop, disconnect and reconnect. An object in the portal does not prove the session works.
6. [Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/): test one setting, one app and one update policy at a time, and compare the assignment with the state inside the Cloud PC.
7. [Point-in-Time Restore](/windows-365/point-in-time-restore/): how restore points work and the admin and user paths.
8. [Secure Access and Plan Recovery](/windows-365/security-recovery/): start Conditional Access in report-only mode, read sign-in logs, and keep an emergency administrator account that Conditional Access does not block (judgement).
9. [Reading an ANC Health Failure](/windows-365/anc-troubleshooting/): how to read a failed ANC health check. Keep the working Microsoft-hosted Cloud PC and test the ANC with a separate user and group.
10. [Operate, Roll Out and Extend](/windows-365/operate-and-extend/): support ownership, staged rollout, license checks, recovery steps and cost review.

The [editable draw.io diagrams](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/architecture) compare the Microsoft-hosted and ANC paths. The [engineering series map](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/blog-series-sequence.md) and [lab status page](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) track what I ran and what is still open.

## What I tested in my lab

- On September 24, 2026 I recorded the sanitized Enterprise license inventory. It shows a seat in inventory. I did not record a new license assignment through to provisioning.

  ![Sanitized Windows 365 Enterprise license inventory](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-01-2026-09-24-license-inventory.jpg)

- I have one Enterprise Cloud PC. It is provisioned, Microsoft Entra joined and enrolled in Intune, and I connected to it through a web session.
- On the same day I checked an Edge setting on the Cloud PC and Company Portal's installed application view. The installed view does not show that a new Available app assignment works. (Available is an Intune assignment type where the user chooses to install the app from Company Portal.)

  ![Edge setting on the Enterprise pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-05-2026-09-24-edge-settings.jpg)

  ![Company Portal installed application view](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg)

- On October 1 the ANC health check failed. The check reported the endpoint pattern `*.infra.windows365.microsoft.com:443`. I do not know the exact host or the root cause (see the [Learn network requirements](https://learn.microsoft.com/windows-365/enterprise/requirements-network)). I did not get a working customer-network deployment, and I deleted the temporary NAT gateway and public IP address I had created.

  ![Sanitized failed ANC health result](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-03-2026-10-01-anc-health.jpg)

I have not tested hybrid join, point-in-time restore, Windows Autopatch, Windows 365 Boot, Switch or Offline. Where a step in the series is only a procedure, I have not run it myself.

## Sources

- Microsoft Learn: [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements), [network deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options), [create a provisioning policy](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy), [Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections).
- [Windows 365 Enterprise engineering repository](https://github.com/AddySidd27/Windows365-enterprise-engineering): lab records, procedures, screenshots and editable diagrams.
