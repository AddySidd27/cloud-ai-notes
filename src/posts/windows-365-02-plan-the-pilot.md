---
title: "Windows 365 Enterprise: Plan a Pilot That You Can Verify"
seoTitle: "Windows 365: Plan a Verifiable Pilot"
layout: post.njk
permalink: /windows-365/plan-the-pilot/
order: 202
part: 2
tags: w365-series
deck: "A practical checklist for licensing, roles, assignments and evidence before the first Cloud PC is provisioned."
---

A pilot succeeds when you can explain who received a Cloud PC, why it was assigned, and how you checked the result. A Cloud PC is a Windows PC that runs in Microsoft's cloud. Windows 365 gives one to each licensed user. Start with one test user and one small Microsoft Entra group. Keep the scope small, so a mistaken policy does not affect the rest of the organization.

Two terms come up often below. A provisioning policy is the rule that tells Windows 365 how to create Cloud PCs. "Provisioned" means the Cloud PC has been created. An Azure network connection (ANC) links your own Azure virtual network to Windows 365. It is one of two network choices, and the table below explains both.

## What you need

Check the current [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements) before building. Confirm these items:

- **Licenses.** The user needs licenses for Windows Enterprise E3, Intune, Microsoft Entra ID P1 and Windows 365 Enterprise (see Licensing requirements on that page). Without the Windows 365 license, Windows 365 does not provision the Cloud PC.
- **Tenant.** You need a valid and working Intune and Microsoft Entra tenant.
- **Administrator role.** The administrator who provisions Cloud PCs must hold the Intune Administrator or Windows 365 Administrator role in Microsoft Entra ID.
- **Region.** Pick a [supported region](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements#supported-azure-regions-for-cloud-pc-provisioning). With a Microsoft-hosted network you choose a geography in the provisioning wizard.

Record the license name and its assigned user. A license visible in inventory is not proof that the intended user has it.

Choose a descriptive pilot group such as `W365-Pilot-Users` and record its members before assigning anything. Create a second group, of devices, only if you need to apply Intune policies to the Cloud PCs (judgement). Decide who can change the provisioning policy and who checks the provisioning status. Avoid using a broad production group for a learning exercise (judgement).

Write down these decisions before you start:

| Decision | Pilot record |
| --- | --- |
| User and group | Sanitized user label and exact group name |
| License | License name, assignment state and date checked |
| Identity | Microsoft Entra join (the Cloud PC joins Entra ID only) or hybrid join (it joins your on-premises Active Directory and Entra ID), with reason |
| Network | Microsoft-hosted network (Microsoft runs the network) or ANC (your own Azure virtual network), with application requirement |
| Image | Gallery image (a default image from Microsoft) or custom image (one you upload), with application requirement |
| Success | Provisioned status, usable session and Intune check-in (the Cloud PC shows in Intune as enrolled and reporting) |

## Walk through the checks

### Step 1: inventory the Enterprise seat

In the Microsoft 365 admin center, go to Billing > Licenses and select the Windows 365 Enterprise product. Record the total, assigned and available counts. Then open the intended pilot user's license details and verify the actual assignment. In my September 24, 2026 capture, one Enterprise seat was assigned and none were available. The crop does not identify the assigned user.

![Sanitized Windows 365 Enterprise license inventory. The Enterprise row shows Total 1, Assigned 1, Available 0](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-01-2026-09-24-license-inventory.jpg)

*Sanitized crop from my lab, observed on September 24, 2026. Only the Enterprise row matters here (Total 1, Assigned 1, Available 0). The other rows are other licenses in my lab tenant: a Windows 365 Business row (1, 1, 0), an Entra ID P2 row that shows Available -1, and an Intune row (25, 2, 23). I did not investigate the -1 and it is not part of this pilot. The top header row is partly cropped.*

### Step 2: make a narrow pilot group

In the Microsoft Entra admin center, create or select a dedicated user security group for the pilot and add the licensed test user. Do not use a nested group, because provisioning policies do not support them ([Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)). Note the group name and the date and time you added the user. Do not target all users. Save a sanitized group membership image in your own lab. My public lab evidence does not include a group membership screenshot.

### Step 3: check the administrator

Verify that the administrator holds the Intune Administrator or Windows 365 Administrator role before opening the provisioning wizard.

### Step 4: write the success result

Write a pass condition (judgement). For example: the targeted user sees one Cloud PC, signs in from the Windows App or windows365.microsoft.com, disconnects and reconnects, and the device appears in Intune with the expected join type. The disconnect and reconnect step is a plan, not yet verified in my lab. Record the identity, network and image decisions from [Choose Identity and Network](/windows-365/identity-network/) before creating a policy.

The [tenant readiness use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-01-tenant-readiness-and-pilot-design.md) in my GitHub lab repository contains a longer worksheet. The screenshot above is a real capture, but it shows inventory only, not a new end-to-end assignment. Treat the missing group and assignee screens as checks to capture when you reproduce the lab.

## Evidence to save

Capture the license assignment, group membership, policy target, provisioning result and first successful session at separate checkpoints. Add the date and a one-line observation to each image. Remove names, tenant IDs and device identifiers before publication. If a check fails, keep the error text and document the corrective step; do not call the pilot complete because the portal accepted a form.

Next: [choose identity and network](/windows-365/identity-network/).

## Microsoft Learn

- [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)
- [Assign licenses (Windows 365 Enterprise)](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses)
- [Customer permissions](https://learn.microsoft.com/en-us/windows-365/enterprise/customer-permissions): Azure roles that the Windows 365 service needs when you create an ANC or add a custom image (not the administrator role)
