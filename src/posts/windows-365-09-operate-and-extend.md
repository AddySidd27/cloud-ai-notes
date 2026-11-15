---
title: "Windows 365 Enterprise: Operate, Roll Out and Extend"
seoTitle: "Windows 365: Operate, Roll Out and Extend"
layout: post.njk
permalink: /windows-365/operate-and-extend/
order: 209
part: 10
tags: w365-series
deck: "How to go from one tested pilot to a service your team can support. It also introduces Windows 365 Boot and Switch."
---

A Cloud PC is the Windows desktop that Windows 365 hosts in the cloud for one user. A Cloud PC pilot becomes a service when someone owns assignment, support, updates, recovery and cost. Keep your pilot records, then expand in small groups with a clear rollback decision for each wave (judgement). A provisioning policy is the Intune setting that tells Windows 365 how to build Cloud PCs, and provisioning is the act of building them; see [Plan the Pilot](/windows-365/plan-the-pilot/) and [Provision](/windows-365/provision/).

## Write down how you will run it

| Area | Write down before rollout |
|---|---|
| Eligibility | Who approves a license and group membership change |
| Provisioning | Policy owner, image, join type, network and region |
| User support | Connection method, how errors are recorded and who to escalate to |
| Endpoint management | Configuration, application, update and compliance owners |
| Recovery | Restore decision owner, user data location and the recovery time you promise users (see [Point-in-Time Restore](/windows-365/point-in-time-restore/)) |
| Cost | Seat inventory, unused licenses and any Azure resources you pay for, such as a virtual network for an Azure network connection (ANC) |

A license plus membership in a group that a provisioning policy targets starts automatic provisioning, and the new user should sign in soon after so quality updates install promptly ([Cloud PC lifecycle](https://learn.microsoft.com/en-us/windows-365/enterprise/lifecycle)). When a user leaves, follow the organization's retention and offboarding process before changing licensing. If you remove the license or the user's provisioning policy assignment, the Cloud PC enters a seven-day grace period. After that, Windows 365 deprovisions the Cloud PC and deletes its storage. To block access at once, Learn says to disable the user account in on-premises Active Directory and revoke the user's refresh tokens in Microsoft Entra ID ([Cloud PC lifecycle](https://learn.microsoft.com/en-us/windows-365/enterprise/lifecycle)). Test the support process with one real ticket before expanding to the next group.

## Walk one user through the service

Joiner, mover, leaver (JML) means a user who starts, changes role, or leaves. These are the four steps I walk through (judgement).

1. **Joiner:** approve the user and license, add the user to the intended pilot group, and check the provisioning and first-session result. Save timestamps and owner.
2. **Mover:** document the new requirements before changing group or policy targeting. Check whether the user's license, policy and Cloud PC will change, and whether their data stays. Moving a Cloud PC to another network or region is not done by changing group membership, so plan it on its own.
3. **Support:** ask the user for the exact client, error, time and last successful sign-in. Check Windows 365 service health, the Cloud PC status in Intune, whether the device last checked in to Intune, and the user's sign-in log in Microsoft Entra before taking a remote action. The Troubleshoot remote action and the user's Troubleshoot page are safe first steps ([Access a Cloud PC](https://learn.microsoft.com/en-us/windows-365/end-user-access-cloud-pc)).
4. **Leaver:** follow the organization's retention and recovery policy, record the license and Cloud PC state, then deprovision only through an approved offboarding workflow. Removing the license or policy starts the seven-day grace period; Deprovision and End grace period are remote actions ([Remotely manage Windows 365 devices](https://learn.microsoft.com/en-us/windows-365/enterprise/remotely-manage-cloud-pc)).

The [editable joiner/mover/leaver draw.io source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/source/09-joiner-mover-leaver-lifecycle.drawio) and [Cloud PC operations source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/source/10-cloud-pc-lifecycle-operations.drawio) show the decision paths. They are draw.io source files (open them in draw.io, also called diagrams.net). They are design diagrams. I have not tested a leaver or a restore.

On October 7, 2026, I restarted my pilot Cloud PC and reconnected (see my [restart lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-07-controlled-restart.md)). I have not tested point-in-time restore (see [Point-in-Time Restore](/windows-365/point-in-time-restore/)), resize, reprovision or a full offboarding yet. [Remotely manage Windows 365 devices](https://learn.microsoft.com/en-us/windows-365/enterprise/remotely-manage-cloud-pc) explains the supported actions. Check their status in the Cloud PC actions report in the Intune admin center. The [Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/) and [Secure Access and Plan Recovery](/windows-365/security-recovery/) posts cover the restart.

## Roll out in waves

Start with the pilot user, add a small group with varied applications, then widen only after connection, management and support results are recorded. For each wave, track assigned licenses, provisioned Cloud PCs, connection failures, Intune policy conflicts (two policies setting the same value) and time to resolve. Keep known gaps visible. I suggest a progress tracker (a table or board) with four states: **planned**, **configured**, **tested** and **stopped**. That way a written procedure is never counted as a finished test (judgement). Microsoft's [management guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management) supports starting with Intune, gallery images and a security baseline tested on pilot Cloud PCs; the waves and status labels are my own approach.

My [full learning checklist](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/00-complete-learning-journey.md) links my lab records and says how far each test went. My [lab status page](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) shows what I actually saw. My Microsoft-hosted Cloud PC (the network option where Microsoft runs the network; see [Identity and Network](/windows-365/identity-network/)) works well as a management pilot. My separate Azure network connection (ANC) test failed its health check, and I do not know the cause. See [ANC Troubleshooting](/windows-365/anc-troubleshooting/).

## Optional features come after the core pilot

I suggest treating optional features as a later phase (judgement). Two have Learn pages. I have not tested either yet.

- **Windows 365 Boot:** a physical Windows 11 device signs the user straight in to their Cloud PC. Learn requires Windows 11 Enterprise or Professional (or Windows IoT Enterprise, per the requirements page), version 22621.3374 or later, on both the physical device and the Cloud PC. The device must be registered with Windows Autopilot (which enrolls it in Intune), you need the Intune Service Administrator role, and a Windows 365 Enterprise license is required to make Boot provisioning policies ([What is Windows 365 Boot?](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-boot-overview), [requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-boot-physical-device-requirements), [guided scenario](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-boot-guide)).
- **Windows 365 Switch:** the user moves between the local desktop and one Cloud PC in Windows 11 Task view. It needs a supported Windows 11 Enterprise, Pro or Home device and a Windows 365 license, and only one Cloud PC can be added to Task view ([What is Windows 365 Switch?](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-switch-overview)).

I could not find a Microsoft Learn page for a Windows 365 feature called Offline when I searched on November 14, 2026, so this article does not describe it or its prerequisites. Check Learn again before you plan it.

For each feature, pick a supported device, write a clear success test and plan how to recover. A Cloud PC existing does not mean the feature works. Test its launch, reconnect behavior and policy impact separately.

This series is a starting route. I have not tested every optional feature or every destructive recovery action in my tenant. A destructive recovery action is one that removes or rebuilds a Cloud PC, such as reprovision. Use the worksheets in the [engineering repository](https://github.com/AddySidd27/Windows365-enterprise-engineering) to repeat the steps, and compare each portal choice with the linked product documentation.

Return to [Start Here](/windows-365/start-here/) or explore the [engineering repository](https://github.com/AddySidd27/Windows365-enterprise-engineering).

## Microsoft Learn

- [Management: Microsoft Intune as the management plane for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management)
- [Remotely manage Windows 365 devices](https://learn.microsoft.com/en-us/windows-365/enterprise/remotely-manage-cloud-pc)
- [Access a Cloud PC](https://learn.microsoft.com/en-us/windows-365/end-user-access-cloud-pc)
- [What is Windows 365 Boot?](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-boot-overview)
- [What is Windows 365 Switch?](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-switch-overview)
- [Windows 365 Cloud PC lifecycle](https://learn.microsoft.com/en-us/windows-365/enterprise/lifecycle)
- [Windows 365 documentation](https://learn.microsoft.com/en-us/windows-365/)
