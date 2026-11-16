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

A Cloud PC is a Windows desktop that Windows 365 builds and runs for one user. A provisioning policy is the set of rules (join type, network, image, region) that tells Windows 365 how to build Cloud PCs for the users in a group. Microsoft Entra join means the Cloud PC joins Microsoft Entra ID directly, with no on-premises domain.

A Microsoft-hosted network means Windows 365 runs the Cloud PC network for you. The Azure network connection (ANC) is the other choice: you bring your own Azure virtual network. The ANC path is a separate exercise, covered in the [ANC health failure article](/windows-365/anc-troubleshooting/). The [identity and network article](/windows-365/identity-network/) explains both choices.

**What you will build:** one licensed pilot user in one Microsoft Entra group, targeted by one provisioning policy. The intended result is a Cloud PC with the status **Provisioned** (built and ready for sign-in) that the user can open and that an administrator can inspect in Intune.

![A licensed pilot user is in a pilot group. An administrator creates a provisioning policy in Intune with Entra join, a Microsoft-hosted network, a gallery image and a region. Windows 365 builds the Cloud PC, which shows Provisioned and opens in Windows App.](/img/windows-365/windows-365-provision.svg)

*Source: [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) and [Windows 365 architecture](https://learn.microsoft.com/en-us/windows-365/enterprise/architecture).*

## 1. Check the prerequisites

Before you create anything, check the [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements). You need a suitable Windows 365 Enterprise license, a user who receives that license, a Microsoft Entra group for the policy assignment, and an administrator who holds the Intune Administrator or Windows 365 Administrator role in Microsoft Entra ID ([Role and identity requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements#role-and-identity-requirements)).

Users also need licenses for Windows E3, Intune and Microsoft Entra ID P1 as well as Windows 365, and Intune must allow Windows (MDM) enrollment; the [plan the pilot article](/windows-365/plan-the-pilot/) lists these. For this Microsoft-hosted, Entra joined path, you do not need to create an Azure virtual network.

| Check | Where | Continue when |
|---|---|---|
| Enterprise license | Microsoft 365 admin center > Billing > Licenses | The intended user has the license assigned |
| Pilot group | Microsoft Entra admin center > Groups | The intended user is a member |
| Administrator | Microsoft Entra roles | You hold the Intune Administrator or Windows 365 Administrator role |
| Network choice | Your pilot plan (a decision, not a portal page) | Microsoft-hosted network is selected |

## 2. Assign the license to the pilot user

Assign a Windows 365 Enterprise license to the intended user, as described in step 1 of [plan the pilot](/windows-365/plan-the-pilot/). A purchased seat alone does not start provisioning. Follow Microsoft's [license assignment guide](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses) if the navigation differs in your tenant.

**Checkpoint:** Record the license type (SKU), assigned user, date and license state in a private worksheet. Hide the user principal name before you share any screenshot.

## 3. Put the user in a pilot group

In the [Microsoft Entra admin center](https://entra.microsoft.com/), open **Groups > All groups**. Use the narrow pilot group from step 2 of [plan the pilot](/windows-365/plan-the-pilot/) and add the licensed user under **Members**. Do not use a nested group; provisioning policies do not support them. A narrow group stops a new policy from targeting a wider population.

**Checkpoint:** Confirm the same user appears in both the license assignment and group membership views. The provisioning policy will target the group, while the license makes the member eligible for a Cloud PC. Microsoft's [provisioning policy guide](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) describes this relationship.

## 4. Choose the network and image

For this first pilot choose **Microsoft Entra join** and **Microsoft-hosted network**. Windows 365 manages the Cloud PC network for that choice. If your Cloud PC must use a specific Azure virtual network, DNS path or private resources, plan an ANC, meet its Azure permissions and network requirements, and wait for the ANC health checks before selecting it in a policy. Do not select an ANC that has failed its health checks. The [ANC health failure article](/windows-365/anc-troubleshooting/) shows how to read a failed check.

Choose a **gallery image** for the first exercise. Gallery images need no preparation and Microsoft updates them monthly. This avoids custom image maintenance in the first pilot. A custom image can come later when an application requirement justifies it; it must meet the image requirements in [device images](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images).

## 5. Walk through the provisioning policy wizard

In [Microsoft Intune admin center](https://intune.microsoft.com/), open **Devices > Provision Cloud PCs > Provisioning policies > Create policy**.

### General: desktop, license, join and network

Enter a policy name and description. To give each user their own Cloud PC, select **Access a full Cloud PC desktop** and the license type **Enterprise**. Choose the **Microsoft Entra Join** option and the **Microsoft hosted network** option (the wizard's own labels). Select the geography and look at its region groups (a region group is a set of Azure regions inside the geography).

Microsoft recommends all default regions within the geography for resiliency, unless you must pin a region group or region. Choose the geography based on your own data residency and user needs. The single sign-on setting is optional.

**Before Next:** Record the join type, network, geography and region group. An ANC is not selected here.

### Image: operating system

Select a gallery or custom image that meets the pilot's requirements. The gallery lists current Windows 11 Enterprise images with Microsoft 365 Apps. Pick a supported gallery image for your pilot.

**Before Next:** Gallery images need no preparation; custom images must meet Microsoft's image requirements, and the OS disk size follows the license. See [Microsoft's device image guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images).

### Configuration: language, naming and services

Choose a language and region. The page offers a language, optional device naming, an optional Windows Autopilot device preparation policy (it prepares the device at first sign-in), and **Windows Autopatch** (it manages Windows updates for you) or **None** under Additional Services. Selecting Autopatch replaces an existing Autopatch policy for those Cloud PCs. For a first pilot, leave naming and Autopilot unset and select **None**.

### Scope tags: administrator visibility

Scope tags limit which administrators can see and manage this policy. Review them. The default is **Default**. Use your organization's delegated administration design before adding or removing tags.

### Assignments: who receives the policy

Select the dedicated **pilot user group** from step 3, then confirm its members are licensed.

### Review + create: inspect before saving

Compare the join type, network, region, image, configuration, scope tags and group with your worksheet. Selecting **Create** saves the policy. Then check provisioning for an eligible licensed user separately.

Follow the current [provisioning policy instructions](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) if a portal control differs from this description.

## 6. Watch provisioning, then test the user session

In Intune, open **Devices > Provision Cloud PCs > All Cloud PCs**. Find the pilot user and record the policy, status and any error. If the status fails, note the exact stage before changing a setting. Microsoft's [automated provisioning steps](https://learn.microsoft.com/en-us/windows-365/enterprise/automated-provisioning-steps) list the stages Windows 365 runs (core provisioning, post-provisioning configuration and assignment), so you can name the stage that failed.

A failed post-provisioning step gives the status **Success with warnings** on that page; Intune lists it as **Provisioned with warnings** on [Device management overview](https://learn.microsoft.com/en-us/windows-365/enterprise/device-management-overview#column-details).

When the Cloud PC is **Provisioned**, have the user open [windows.cloud.microsoft](https://windows.cloud.microsoft/) or Windows App, select the Cloud PC and sign in; see [connect and verify](/windows-365/connect-verify/). Then ask them to disconnect and reconnect. Back in Intune, inspect its managed device record and last check-in. A Provisioned status and a working user session are two separate checks.

| Result | What to record |
|---|---|
| Eligible user | License assignment and pilot group membership |
| Policy in scope | Assigned group, join, network and image |
| Provisioning complete | All Cloud PCs row with Provisioned status |
| Usable desktop | User sign-in and reconnect |
| Managed device | Intune device record and check-in |

## If your result differs

| Symptom | First place to look |
|---|---|
| No row at all | The license is not assigned or not yet applied |
| Row shows Not provisioned | No policy targets the user; check the group and policy assignment |
| Row shows Pending | Not enough free licenses |
| ANC unavailable | ANC health and network prerequisites; return to the Microsoft-hosted pilot path |
| Provisioning failed | Exact Intune stage and error, then identity and network requirements |
| Provisioned but cannot sign in | The user's sign-in result and Conditional Access, then connection diagnostics |
| Sign-in works but device is missing | Intune enrollment and device record |

Continue to [connect and verify](/windows-365/connect-verify/).

Next: [Windows 365 Enterprise: Connect and Verify the Cloud PC](/windows-365/connect-verify/).

## Sources

- [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Assign Windows 365 licenses](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses)
- [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)
