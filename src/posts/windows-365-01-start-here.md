---
title: "Windows 365 Enterprise: Start Here"
layout: post.njk
permalink: /windows-365/start-here/
order: 201
part: 1
tags: w365-series
deck: "A beginner's guide to Windows 365 Cloud PCs, from the first decision to daily operations. It says what was tested and what was not."
---

Windows 365 gives an assigned user a Cloud PC. The user connects from a supported device or browser, while the organization manages the Cloud PC with Microsoft Intune, Microsoft's device management service. This series follows one pilot (a small trial rollout with a few users) of Windows 365 Enterprise, the edition your organization's IT team manages, from planning to support. Each chapter tells you what to do in your own tenant, what to check, and what I saw in my own lab.

## Words to know

| Term | Meaning |
| --- | --- |
| Cloud PC | The Windows desktop assigned to a user through Windows 365. |
| Provisioning policy | The Intune configuration that defines the Cloud PC's join type, network, image and assignment. |
| Microsoft-hosted network | The network option managed by Microsoft for the Cloud PC. It does not require your Azure subscription for Cloud PC networking. |
| Tenant | Your organization's Microsoft Entra ID directory. |
| Azure network connection (ANC) | An object in the Intune admin center that tells a provisioning policy which Azure subnet to place the Cloud PC's network interface in. It needs subnet, DNS and outbound access planning. |
| ANC health check | A test that Windows 365 runs on an ANC to confirm provisioning can succeed ([Azure network connection health checks](https://learn.microsoft.com/windows-365/enterprise/health-checks)). A policy can use an ANC only after its checks succeed or succeed with warnings. |
| VNet, subnet | An Azure virtual network and a range of addresses inside it. |
| NAT gateway, public IP | Azure resources that give a subnet outbound internet access through a public IP address. I created them temporarily for the ANC test. |
| AD DS | Active Directory Domain Services, the on-premises directory. |
| Hybrid join | A Cloud PC joined to both on-premises Active Directory and Microsoft Entra ID. It needs an ANC; the Microsoft-hosted network supports only Microsoft Entra join. |
| Conditional Access | Microsoft Entra rules that decide who can sign in and under which conditions. Report-only mode logs what a rule would do without enforcing it. |
| Company Portal | The Intune app where users see and install the apps assigned to them. |
| Microsoft Entra join | The Cloud PC is joined to Microsoft Entra ID without an on-premises AD DS device join. |
| Intune | The management service used to deploy settings, apps, security policies and updates. |

In my lab I have one Enterprise Cloud PC. It is provisioned, Microsoft Entra joined and enrolled in Intune, and I connected to it through a web session. I did not record a fresh license assignment through to first sign-in. I also ran a separate Azure network connection (ANC) test, and its health check failed. I then deleted the temporary Azure resources I had created for it, a NAT gateway and a public IP address. Where a step below is only a procedure, I have not run it myself.

## The route through the series

1. **Prepare:** confirm the Enterprise license, the [requirements](https://learn.microsoft.com/windows-365/enterprise/requirements) and the administrator role, pilot user and a small assignment group (see [Plan the Pilot](/windows-365/plan-the-pilot/)). Write success criteria before touching a provisioning policy.
2. **Choose identity and network:** start with Microsoft Entra join and a Microsoft-hosted network for the first exercise. Microsoft calls it the [recommended option for most scenarios](https://learn.microsoft.com/windows-365/enterprise/windows-365-network-deployment-options). Add an ANC when an application needs customer-controlled routing, DNS or private connectivity.
3. **Choose the image:** begin with a gallery image unless the pilot application needs a custom image. Deliver applications through Intune where appropriate.
4. **Provision:** create and assign a Windows 365 Enterprise provisioning policy to the pilot group. Record its join type, network, image, region and group. Check the Cloud PC status and note the exact error if provisioning fails.
5. **Connect:** ask the assigned user to open [windows.cloud.microsoft](https://windows.cloud.microsoft/), reach the desktop, disconnect and reconnect. Record the connection method and outcome.
6. **Verify the device:** compare the assigned user, join type, enrollment and last check-in in the Windows 365 and Intune views. An object in the portal does not prove the session works.
7. **Manage:** test one configuration setting, one app and one update policy at a time. Compare the assignment result with the effective state inside the Cloud PC.
8. **Secure and support:** start Conditional Access in report-only mode, read sign-in logs, and keep an emergency administrator account that Conditional Access does not block (judgement). Test restart and reconnect before a disruptive lifecycle action.
9. **Test the ANC variant separately:** keep the working Microsoft-hosted Cloud PC in place. Use a separate pilot user and group once the ANC health check passes; clean up temporary Azure resources when the test ends.
10. **Operate:** document support ownership, staged rollout, user changes, license checks, recovery steps and cost review.

The [engineering repository's full learning checklist](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/00-complete-learning-journey.md) lists every step. Its [lab status page](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) shows what I ran and what I have not.

## What I saw in my lab

This is the sanitized Enterprise license inventory I recorded on September 24, 2026. It shows a seat in inventory. I did not record a new license assignment through to provisioning.

![Sanitized Windows 365 Enterprise license inventory](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-01-2026-09-24-license-inventory.jpg)

On the same day (September 24, 2026) I checked an Edge setting on the Cloud PC and Company Portal's installed application view. The installed view does not show that a new Available app assignment works. (Available is an Intune assignment type where the user chooses to install the app from Company Portal.) I have not tested a new Available app assignment or an uninstall yet.

![Edge setting on the Enterprise pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-05-2026-09-24-edge-settings.jpg)

![Company Portal installed application view](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg)

On October 1 the ANC health check failed. The check reported the endpoint pattern `*.infra.windows365.microsoft.com:443`. I do not know the exact host or the root cause. See the [Learn network requirements](https://learn.microsoft.com/windows-365/enterprise/requirements-network) and [ANC Troubleshooting](/windows-365/anc-troubleshooting/). I did not get a working customer-network deployment.

![Sanitized failed ANC health result](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-03-2026-10-01-anc-health.jpg)

## Architecture before portal clicks

Use the [editable draw.io diagrams and exports](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/architecture) to compare the Microsoft-hosted and ANC paths. A Cloud PC with ANC still runs in the Windows 365 service; its virtual network interface connects to the customer VNet. The ANC does not move the Cloud PC virtual machine into your Azure subscription. Hybrid join needs an ANC and has additional AD DS and DNS dependencies, so it belongs in a separate lab.

## A simple lab log

For each action, record the date, pilot group, intended setting, assignment status, result inside the Cloud PC, and any delay or error. Remove user names, tenant identifiers, device IDs, addresses and secrets before you share it. Mark a step **verified** only after you see the result. Mark a walkthrough you have not run as **procedure**. If a test stops on an error, write down the error and what you cleaned up.

My lab records are in the repository. The [readiness record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-01-tenant-readiness-and-pilot-design.md) covers readiness, the [network record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-03-network-architecture.md) explains the network choices, the [provisioning record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-02-enterprise-provisioning.md) covers provisioning, and the [first Cloud PC lab](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/02-first-cloud-pc-lab.md) is a short exercise. Read the network and image decisions before you provision, even though their records are numbered higher.

## Read the complete series

The reading path follows the ten topics in the [Windows-Noob getting-started series](https://www.windows-noob.com/forums/topic/23040-getting-started-with-windows-365-part-1-introduction/), a community blog and not a Microsoft site. The Windows-Noob articles were published in 2022 and 2023, so use the current Microsoft Learn links in each chapter for present-day requirements. The series here has ten chapters (parts 1 to 10) across those ten topics. A chapter can cover only part of a topic. Each line below says what I have and have not tested.

1. **Introduction and edition choice.** [Start Here](/windows-365/start-here/) and [Plan the Pilot](/windows-365/plan-the-pilot/) explain licensing, groups, requirements and the first pilot. I recorded the Enterprise seat inventory. I have not tested a fresh license assignment yet.
2. **Provision a Microsoft Entra joined Cloud PC.** [Identity and Network](/windows-365/identity-network/), [Provisioning](/windows-365/provision/) and [ANC Troubleshooting](/windows-365/anc-troubleshooting/) cover the network decision and wizard. Six screenshots of the Intune provisioning wizard, taken without assigning it to a group, illustrate the steps. My Cloud PC is provisioned, but I did not record its creation. The separate ANC health test failed.
3. **Provision a hybrid joined Cloud PC.** Not tested yet. This needs its own lab with AD DS, DNS, directory sync, a customer network and a join. My Entra joined pilot does not show hybrid join.
4. **Connect to the Cloud PC.** [Connect and Verify](/windows-365/connect-verify/) includes my Enterprise browser session. I have not tested the Windows, macOS and mobile clients yet. A sanitized October 15 browser desktop screenshot is published there.
5. **Manage the Cloud PC.** [Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/) covers policy, application and update checks. Some of what I saw has a dated lab record, linked in that chapter. The rest is procedure only.
6. **Point-in-time restore.** [Point-in-Time Restore](/windows-365/point-in-time-restore/) explains the restore points and the admin and user paths; [Secure Access and Plan Recovery](/windows-365/security-recovery/) covers the wider recovery plan. I have not tested a restore yet, because I have only one working Enterprise Cloud PC.
7. **Windows Autopatch.** The [update section](/windows-365/manage-intune/) introduces servicing. Not tested yet.
8. **Windows 365 Boot.** [Operate, Roll Out and Extend](/windows-365/operate-and-extend/) introduces the feature. Not tested yet.
9. **Windows 365 Switch.** [Operations](/windows-365/operate-and-extend/) introduces the feature. Not tested yet.
10. **Windows 365 Offline.** [Operations](/windows-365/operate-and-extend/) notes that I found no Microsoft Learn page for this feature on November 14, 2026, so it is not covered.

The [engineering series map](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/blog-series-sequence.md) tracks the same sequence and the checks still open. Several topics share a chapter, and I have not run a lab for every topic.

### References

- Microsoft Learn: [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements), [network deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options), [create a provisioning policy](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy), [Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections).
- [Windows 365 Enterprise engineering repository](https://github.com/AddySidd27/Windows365-enterprise-engineering): lab records, procedures, screenshots and editable diagrams.
