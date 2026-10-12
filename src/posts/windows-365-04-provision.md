---
title: "Windows 365 Enterprise: Provision a Microsoft Entra Joined Cloud PC"
layout: post.njk
permalink: /windows-365/provision/
order: 204
part: 4
tags: w365-series
deck: "Follow the license, group, network, image and provisioning policy in the order a first pilot needs them."
---


In [Part 3](/windows-365/identity-network/), we chose an identity and network path. Here we use **Microsoft Entra join** and a **Microsoft-hosted network** for a small Enterprise pilot. You can follow the same order in your own tenant. The Azure network connection (ANC) path is a separate lab in [Part 8](/windows-365/anc-troubleshooting/).

**What you will build:** one licensed pilot user in one Microsoft Entra group, targeted by one provisioning policy. The intended result is a provisioned Cloud PC that the user can open and that an administrator can inspect in Intune.

![Illustrated pilot provisioning sequence for example user AVDtest](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/architecture/diagrams/exported/windows-365-provisioning-illustration.png)

*Illustration 1. Example user AVDtest. This is an original workflow diagram, not an Intune screenshot or proof of a completed lab. [Edit the draw.io source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/exported/windows-365-provisioning-illustration.drawio).*

**Evidence boundary:** My tenant already has a Provisioned Enterprise Cloud PC. I verified its current policy and inventory on October 12, 2026. I did not record its original five wizard pages or the initial license-to-first-sign-in sequence. The portal steps below are a reproducible walkthrough, and the images are identified by what they actually prove.

## 1. Check the prerequisites

Before you create anything, check the [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements). You need a suitable Windows 365 Enterprise license, a user who receives that license, a Microsoft Entra group for the policy assignment, and an administrator with the required [Windows 365 permissions](https://learn.microsoft.com/en-us/windows-365/enterprise/customer-permissions). For this Microsoft-hosted, Entra joined path, you do not need to create an Azure virtual network.

| Check | Where | Continue when |
| --- | --- | --- |
| Enterprise license | Microsoft 365 admin center > Billing > Licenses | The intended user has the license assigned |
| Pilot group | Microsoft Entra admin center > Groups | The intended user is a member |
| Administrator | Intune and Entra roles | You can create a provisioning policy |
| Network choice | Pilot design | Microsoft-hosted network is selected |

My sanitized license inventory from September 24 shows **one assigned Enterprise seat and zero available**. It proves inventory, not which user received the license.

![Sanitized Enterprise license inventory showing one assigned seat](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-01-2026-09-24-license-inventory.jpg)

*Figure 1. Real pilot license inventory. Verify the user's license assignment separately in your own tenant.*

## 2. Assign the license to the pilot user

Open the [Microsoft 365 admin center](https://admin.microsoft.com/), go to **Billing > Licenses**, and select your Windows 365 Enterprise product. Assign a license to the intended user and confirm it appears on that user's license page. If your organization uses group-based licensing, check that the assignment has completed before expecting a Cloud PC. A purchased seat alone does not trigger provisioning. Follow Microsoft's [license assignment guide](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses) if the navigation differs in your tenant.

**Checkpoint:** Record the SKU, assigned user, date and license state in a private lab worksheet. Blur the user principal name before publishing any screenshot.

## 3. Put the user in a pilot group

In the [Microsoft Entra admin center](https://entra.microsoft.com/), open **Groups > All groups**. Create a security group with a clear pilot name, or open a dedicated existing group. Under **Members**, add the licensed user. Use a narrow group so a new policy cannot accidentally target a wider population.

**Checkpoint:** Confirm the same user appears in both the license assignment and group membership views. The provisioning policy will target the group, while the license makes the member eligible for a Cloud PC. Microsoft's [provisioning policy guide](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) describes this relationship.

## 4. Choose the network and image

For this first pilot choose **Microsoft Entra join** and **Microsoft-hosted network**. Windows 365 manages the Cloud PC network for that choice. If your Cloud PC must use a specific Azure virtual network, DNS path or private resources, plan an ANC, meet its Azure permissions and network requirements, and wait for the ANC health checks before selecting it in a policy. Do not select my failed ANC for a production policy.

Choose a **gallery image** for the first exercise. This avoids adding custom image maintenance to the initial pilot. A custom image can come later when an application or configuration requirement justifies it; see [device images](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images).

## 5. Create the provisioning policy

Open [Microsoft Intune admin center](https://intune.microsoft.com/) and select **Devices > Provision Cloud PCs > Provisioning policies > Create policy**. Select Windows 365 Enterprise if the page offers a product choice. Work through the wizard in this order:

### General: identity and network

Enter a clear name, such as a pilot policy name used only in your tenant. Choose **Microsoft Entra join** and **Microsoft-hosted network**. Review the geography and region choices shown in your portal. The exact options can change, so read each label before continuing.

**Before Next:** Write down the join type, network type and geography. An Azure network connection is not part of this exercise.

### Image: operating system

Select a **gallery image** that meets your pilot's Windows and Microsoft 365 Apps requirements. Record the full image name and version shown by Intune. Do not describe an image as tested merely because it appears in the gallery.

**Before Next:** Check that the chosen image and the Windows 365 license size suit the pilot's application needs.

### Configuration: user experience

Review the offered language and region options and any update-related choices. Choose values appropriate for your pilot, then record them. Follow the current [Microsoft wizard instructions](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) for controls that have changed since this article.

### Assignments: who receives the policy

Select the dedicated **pilot user group** from step 3. Recheck its membership before proceeding. Avoid broad groups in a first deployment.

### Review + create: final check

Compare **join type, network, image, configuration and group** with your worksheet. Select **Create** only after they match. Saving a policy starts a provisioning workflow for eligible licensed users; a saved policy is not proof that the desktop exists.

**Screenshot record to collect during a fresh run:** General, Image, Configuration, Assignments and Review + create, each placed after the matching step above. Those original wizard captures are not in my public evidence set, so this article does not display substitute screens.

## 6. Watch provisioning, then test the user session

In Intune, open **Devices > Provision Cloud PCs > All Cloud PCs**. Find the pilot user and record the policy, status and any error. If the status fails, note the exact stage before changing a setting. Microsoft's [automated provisioning steps](https://learn.microsoft.com/en-us/windows-365/enterprise/automated-provisioning-steps) explain where to investigate.

When the Cloud PC is **Provisioned**, have the user open [windows365.microsoft.com](https://windows365.microsoft.com/), select the Cloud PC, sign in, then disconnect and reconnect. Back in Intune, inspect its managed device record and last check-in. A Provisioned status and a working user session are two separate checks.

| Result | Evidence to record |
| --- | --- |
| Eligible user | License assignment and pilot group membership |
| Policy in scope | Assigned group, join, network and image |
| Provisioning complete | All Cloud PCs row with Provisioned status |
| Usable desktop | User sign-in and reconnect |
| Managed device | Intune device record and check-in |

## What my lab currently proves

On October 12, the live policy showed **Microsoft Entra join**, a **US Central** Microsoft-hosted geography, and a gallery image labelled **Windows 11 Enterprise with Microsoft 365 Apps 25H2**. **All Cloud PCs** showed one Provisioned Enterprise Cloud PC associated with this policy, sized **2 vCPU, 4 GB RAM and 64 GB storage**; its row showed no ANC. The policy's separate Devices action view displayed zero entries, so I used All Cloud PCs for this count. The [dated inventory note](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-10-12-enterprise-policy-inventory.md) records exactly what I checked. The September [portal check](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-09-24-portal-check.md) records a user session and Intune device state.

That evidence does **not** establish a fresh end-to-end provisioning run. It also does not turn the separate failed ANC health check into a successful ANC deployment. I will add wizard images only when I can capture and sanitize my own new run without disrupting the current single-seat Cloud PC.

## If your result differs

| Symptom | First place to look |
| --- | --- |
| No Cloud PC row | User license, pilot group, policy assignment and time since assignment |
| ANC unavailable | ANC health and network prerequisites; return to the Microsoft-hosted pilot path |
| Provisioning failed | Exact Intune stage and error, then identity and network requirements |
| Provisioned but cannot sign in | User access, authentication and connection diagnostics |
| Sign-in works but device is missing | Intune enrollment and device record |

Continue to [Part 5: connect and verify](/windows-365/connect-verify/). The [Enterprise provisioning use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-02-enterprise-provisioning.md) has the deeper operator checklist.

### Microsoft Learn

- [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Assign Windows 365 licenses](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses)
- [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)
- [Automated provisioning steps](https://learn.microsoft.com/en-us/windows-365/enterprise/automated-provisioning-steps)
