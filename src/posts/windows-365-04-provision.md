---
title: "Windows 365 Enterprise: Provision a Microsoft Entra Joined Cloud PC"
seoTitle: "Windows 365: Provision an Entra Joined Cloud PC"
layout: post.njk
permalink: /windows-365/provision/
order: 204
part: 4
tags: w365-series
deck: "Follow the license, group, network, image and provisioning policy in the order a first pilot needs them."
---


In the [identity and network article](/windows-365/identity-network/), we chose an identity and network path. Here we use **Microsoft Entra join** and a **Microsoft-hosted network** for a small Enterprise pilot. You can follow the same order in your own tenant.

A Cloud PC is a Windows desktop that Windows 365 builds and runs for one user. A provisioning policy is the set of rules (join type, network, image, region) that tells Windows 365 how to build Cloud PCs for the users in a group. Microsoft Entra join means the Cloud PC joins Microsoft Entra ID directly, with no on-premises domain. A Microsoft-hosted network means Windows 365 runs the Cloud PC network for you. The Azure network connection (ANC) is the other choice: you bring your own Azure virtual network. The ANC path is a separate lab in the [ANC health failure article](/windows-365/anc-troubleshooting/). The [identity and network article](/windows-365/identity-network/) explains both choices.

**What you will build:** one licensed pilot user in one Microsoft Entra group, targeted by one provisioning policy. The intended result is a Cloud PC with the status **Provisioned** (built and ready for sign-in) that the user can open and that an administrator can inspect in Intune. The screenshots below show the wizard only. They are not a finished build.

![Illustrated pilot provisioning sequence for example user AVDtest](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/architecture/diagrams/exported/windows-365-provisioning-illustration.png)

*Illustration 1. Example user AVDtest (only an example name). This is a workflow illustration. It is not an Intune screenshot. Steps 4 and 5 of this article (network, image and wizard) are combined in the third box. Based on [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy). [Edit the draw.io source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/exported/windows-365-provisioning-illustration.drawio).*

**What I did in my lab:** My tenant already has an Enterprise Cloud PC with the status Provisioned. On October 12, 2026, I checked its current policy and inventory. I also opened a new policy wizard in my own Intune tenant and took screenshots of its six pages as an unassigned draft. The General and Review screenshots show only the top of their pages. I closed the wizard without creating a policy. The screenshots show the current wizard. I did not record how my existing Cloud PC was first created, and I have not provisioned a second Cloud PC.

## 1. Check the prerequisites

Before you create anything, check the [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements). You need a suitable Windows 365 Enterprise license, a user who receives that license, a Microsoft Entra group for the policy assignment, and an administrator who holds the Intune Administrator or Windows 365 Administrator role in Microsoft Entra ID ([Role and identity requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements#role-and-identity-requirements)). Users also need licenses for Windows E3, Intune and Microsoft Entra ID P1 as well as Windows 365, and Intune must allow Windows (MDM) enrollment; the [plan the pilot article](/windows-365/plan-the-pilot/) lists these. For this Microsoft-hosted, Entra joined path, you do not need to create an Azure virtual network.

| Check | Where | Continue when |
| --- | --- | --- |
| Enterprise license | Microsoft 365 admin center > Billing > Licenses | The intended user has the license assigned |
| Pilot group | Microsoft Entra admin center > Groups | The intended user is a member |
| Administrator | Microsoft Entra roles | You hold the Intune Administrator or Windows 365 Administrator role |
| Network choice | Your pilot plan (a decision, not a portal page) | Microsoft-hosted network is selected |

My sanitized license inventory from September 24 shows **one assigned Enterprise seat and zero available**. It shows inventory, not which user received the license.

![Sanitized Enterprise license inventory showing one assigned seat](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-01-2026-09-24-license-inventory.jpg)

*Figure 1. License inventory from my pilot tenant, September 24, 2026 (sanitized). Check the user's license assignment separately in your own tenant.*

## 2. Assign the license to the pilot user

Assign a Windows 365 Enterprise license to the intended user, as described in step 1 of [plan the pilot](/windows-365/plan-the-pilot/). A purchased seat alone does not start provisioning. Follow Microsoft's [license assignment guide](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses) if the navigation differs in your tenant.

**Checkpoint:** Record the license type (SKU), assigned user, date and license state in a private lab worksheet (judgement). Blur the user principal name before you share any screenshot.

## 3. Put the user in a pilot group

In the [Microsoft Entra admin center](https://entra.microsoft.com/), open **Groups > All groups**. Use the narrow pilot group from step 2 of [plan the pilot](/windows-365/plan-the-pilot/) and add the licensed user under **Members**. Do not use a nested group; provisioning policies do not support them. A narrow group stops a new policy from targeting a wider population (judgement).

**Checkpoint:** Confirm the same user appears in both the license assignment and group membership views. The provisioning policy will target the group, while the license makes the member eligible for a Cloud PC. Microsoft's [provisioning policy guide](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) describes this relationship.

## 4. Choose the network and image

For this first pilot choose **Microsoft Entra join** and **Microsoft-hosted network**. Windows 365 manages the Cloud PC network for that choice. If your Cloud PC must use a specific Azure virtual network, DNS path or private resources, plan an ANC, meet its Azure permissions and network requirements, and wait for the ANC health checks before selecting it in a policy. Do not select an ANC that has failed its health checks. My failed example is in the [ANC health failure article](/windows-365/anc-troubleshooting/).

Choose a **gallery image** for the first exercise. Gallery images need no preparation and Microsoft updates them monthly. This avoids custom image maintenance in the first pilot (judgement). A custom image can come later when an application requirement justifies it; it must meet the image requirements in [device images](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images).

## 5. Walk through the provisioning policy wizard

In [Microsoft Intune admin center](https://intune.microsoft.com/), open **Devices > Provision Cloud PCs > Provisioning policies > Create policy**. I used a new, unassigned Enterprise draft for the six screenshots below.

### General: desktop, license, join and network

Enter a policy name and description. To give each user their own Cloud PC, select **Access a full Cloud PC desktop** and the license type **Enterprise**. Choose the **Microsoft Entra Join** option and the **Microsoft hosted network** option (the wizard's own labels). Select the geography and look at its region groups (a region group is a set of Azure regions inside the geography). Learn recommends all default regions within the geography for resiliency, unless you must pin a region group or region. The draft below used the example name **AVDtest-pilot-draft** and **US Central**. Choose the geography based on your own data residency and user needs. The single sign-on setting is optional and was left off in this draft.

![General page in my Intune provisioning policy draft](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/w365-general-own-20261012.png)

*Figure 2. General page, October 12, 2026. I did not save or assign this draft.*

**Before Next:** Record the join type, network, geography and region group. An ANC is not selected here.

### Image: operating system

Select a gallery or custom image that meets the pilot's requirements. The wizard offered **Windows 11 Enterprise + Microsoft 365 Apps 26H2** as the draft gallery selection when I opened it. The existing working policy in this tenant uses **25H2**. These names are Windows 11 feature-update versions. They show what the portal offered me. Pick a supported gallery image for your pilot. I did not deploy or test the 26H2 image.

![Image page in my Intune provisioning policy draft](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/w365-image-own-20261012.png)

*Figure 3. Image page, October 12, 2026. I did not deploy the 26H2 gallery image.*

**Before Next:** Gallery images need no preparation; custom images must meet Microsoft's image requirements, and the OS disk size follows the license. See [Microsoft's device image guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images).

### Configuration: language, naming and services

Choose a language and region. The draft showed **English (United States)**, optional device naming, an optional Windows Autopilot device preparation policy (it prepares the device at first sign-in), and **Windows Autopatch** (it manages Windows updates for you) or **None** under Additional Services. Selecting Autopatch replaces an existing Autopatch policy for those Cloud PCs. I left optional naming and Autopilot unset and selected **None** for the draft. Seeing the Autopatch option does not mean it is enabled.

![Configuration page in my Intune provisioning policy draft](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/w365-configuration-own-20261012.png)

*Figure 4. Configuration page, October 12, 2026. I did not configure or test Autopatch here.*

### Scope tags: administrator visibility

Scope tags limit which administrators can see and manage this policy. Review them. The draft showed **Default**. Use your organization's delegated administration design before adding or removing tags.

![Scope tags page in my Intune provisioning policy draft](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/w365-scope-own-20261012.png)

*Figure 5. Scope tags page, October 12, 2026. I made no scope tag change.*

### Assignments: who receives the policy

For a real pilot, select the dedicated **pilot user group** from step 3, then confirm its members are licensed. The screenshot below intentionally has **no group selected**. I did not target any user while taking these screenshots.

![Empty Assignments page in my Intune provisioning policy draft](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/w365-assignments-own-20261012.png)

*Figure 6. Assignments page, October 12, 2026. No user or group was assigned.*

### Review + create: inspect before saving

Compare the join type, network, region, image, configuration, scope tags and group with your worksheet. The draft review below shows **Microsoft Entra Join**, **US Central** and a gallery image. The lower part (scope tags and assignments) is not in the screenshot. Figure 6 shows the empty Assignments page. I used **Close**, not **Create**. In your own deployment, selecting Create saves the policy. Then check provisioning for an eligible licensed user separately.

![Review page of my unassigned Intune provisioning policy draft](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/w365-review-own-20261012.png)

*Figure 7. Review + create page, October 12, 2026. I closed the draft without creating a policy.*

Follow the current [Microsoft Learn provisioning policy instructions](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) if a portal control differs from these screenshots.

## 6. Watch provisioning, then test the user session

In Intune, open **Devices > Provision Cloud PCs > All Cloud PCs**. Find the pilot user and record the policy, status and any error. If the status fails, note the exact stage before changing a setting. Microsoft's [automated provisioning steps](https://learn.microsoft.com/en-us/windows-365/enterprise/automated-provisioning-steps) list the stages Windows 365 runs (core provisioning, post-provisioning configuration and assignment), so you can name the stage that failed. A failed post-provisioning step gives the status **Success with warnings** on that page; Intune lists it as **Provisioned with warnings** on [Device management overview](https://learn.microsoft.com/en-us/windows-365/enterprise/device-management-overview#column-details).

When the Cloud PC is **Provisioned**, have the user open [windows.cloud.microsoft](https://windows.cloud.microsoft/) or Windows App, select the Cloud PC and sign in; see [connect and verify](/windows-365/connect-verify/). Then ask them to disconnect and reconnect. I have not tested the reconnect step yet. Back in Intune, inspect its managed device record and last check-in. A Provisioned status and a working user session are two separate checks.

| Result | What to record |
| --- | --- |
| Eligible user | License assignment and pilot group membership |
| Policy in scope | Assigned group, join, network and image |
| Provisioning complete | All Cloud PCs row with Provisioned status |
| Usable desktop | User sign-in and reconnect |
| Managed device | Intune device record and check-in |

## What I saw in my lab

On October 12, 2026, the live policy showed **Microsoft Entra join**, a **US Central** Microsoft-hosted geography, and a gallery image labelled **Windows 11 Enterprise with Microsoft 365 Apps 25H2**. **All Cloud PCs** showed one Provisioned Enterprise Cloud PC associated with this policy, sized **2 vCPU, 4 GB RAM and 64 GB storage**; its row showed no ANC. The policy's own device list showed zero entries, so I used All Cloud PCs for this count.

My [October 12 lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-10-12-enterprise-policy-inventory.md) lists exactly what I checked. My [September 24 lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-09-24-portal-check.md) covers a user session and the Intune device state.

I have not run a fresh provisioning from start to finish. My separate ANC health check failed, so I have no working ANC deployment. The wizard screenshots above are an unassigned draft. The working Cloud PC stays on its existing policy.

## If your result differs

| Symptom | First place to look |
| --- | --- |
| No row at all | The license is not assigned or not yet applied |
| Row shows Not provisioned | No policy targets the user; check the group and policy assignment |
| Row shows Pending | Not enough free licenses |
| ANC unavailable | ANC health and network prerequisites; return to the Microsoft-hosted pilot path |
| Provisioning failed | Exact Intune stage and error, then identity and network requirements |
| Provisioned but cannot sign in | The user's sign-in result and Conditional Access, then connection diagnostics |
| Sign-in works but device is missing | Intune enrollment and device record |

Continue to [connect and verify](/windows-365/connect-verify/). The [Enterprise provisioning lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-02-enterprise-provisioning.md) has a longer checklist.

### Microsoft Learn

- [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Assign Windows 365 licenses](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses)
- [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)
- [Role and identity requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements#role-and-identity-requirements)
- [Device images](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images)
- [Automated provisioning steps](https://learn.microsoft.com/en-us/windows-365/enterprise/automated-provisioning-steps)
