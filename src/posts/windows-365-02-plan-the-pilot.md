---
title: "Windows 365 Enterprise: Plan a Pilot That You Can Verify"
seoTitle: "Windows 365: Plan a Verifiable Pilot"
layout: post.njk
permalink: /windows-365/plan-the-pilot/
order: 202
part: 2
tags: w365-series
deck: "A checklist for licensing, roles and assignments, and what to record, before you create the first Cloud PC."
---

A pilot works when you can explain who received a Cloud PC, why, and how you checked the result. A Cloud PC is a Windows PC that runs in Microsoft's cloud. Windows 365 gives one to each licensed user. Start with one test user and one small Microsoft Entra group. Keep the scope small so a mistake does not affect the rest of the organization.

Two terms come up often below. A provisioning policy is the rule that tells Windows 365 how to create Cloud PCs. "Provisioned" means the Cloud PC has been created. An Azure network connection (ANC) links your own Azure virtual network to Windows 365. It is one of two network choices, and the table below explains both.

## What you need

Check the current [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements) before building. Confirm these items:

- **Licenses.** The user needs licenses for Windows Enterprise E3, Intune, Microsoft Entra ID P1 and Windows 365 Enterprise (see Licensing requirements on that page). Without the Windows 365 license, Windows 365 does not provision the Cloud PC.
- **Tenant.** You need a valid and working Intune and Microsoft Entra tenant.
- **Administrator role.** The administrator who provisions Cloud PCs must hold the Intune Administrator or Windows 365 Administrator role in Microsoft Entra ID.
- **Region.** Pick a [supported region](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements#supported-azure-regions-for-cloud-pc-provisioning). With a Microsoft-hosted network you choose a geography in the provisioning wizard.

Record the license name and its assigned user. A license in the inventory does not prove the intended user has it.

Choose a descriptive pilot group such as `W365-Pilot-Users` and record its members before assigning anything. Create a second group, of devices, only if you need to apply Intune policies to the Cloud PCs. Decide who can change the provisioning policy and who checks the provisioning status. Avoid using a broad production group for a learning exercise.

Write down these decisions before you start. The right column says what to record.

| Decision | What to record |
|---|---|
| User and group | A label for the user and the exact group name |
| License | License name, assignment state and date checked |
| Identity | Microsoft Entra join (the Cloud PC joins Entra ID only) or hybrid join (it joins your on-premises Active Directory and Entra ID), with reason |
| Network | Microsoft-hosted network (Microsoft runs the network) or ANC (your own Azure virtual network), with application requirement |
| Image | Gallery image (a default image from Microsoft) or custom image (one you upload), with application requirement |
| Success | Provisioned status, usable session and Intune check-in (the Cloud PC shows in Intune as enrolled and reporting) |

![Diagram: What to confirm, decide and prove in a Cloud PC pilot.](/img/windows-365/windows-365-plan-the-pilot.svg)

*Source: [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements).*

## Walk through the checks

### Step 1: inventory the Enterprise seat

In the Microsoft 365 admin center, go to Billing > Licenses and select the Windows 365 Enterprise product. Record the total, assigned and available counts. Then open the intended pilot user's license details and verify the actual assignment. The inventory shows how many seats exist, not which user has them.

### Step 2: make a narrow pilot group

In the Microsoft Entra admin center, create or select a dedicated user security group for the pilot and add the licensed test user. Do not use a nested group, because provisioning policies do not support them ([Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)). Note the group name and the date and time you added the user. Do not target all users. Save a screenshot of the group members for your own records.

### Step 3: check the administrator

Verify that the administrator holds the Intune Administrator or Windows 365 Administrator role before opening the provisioning wizard.

### Step 4: write the success result

Write a pass condition before you build. For example: the targeted user sees one Cloud PC, signs in from the Windows App or windows.cloud.microsoft, disconnects and reconnects, and the device appears in Intune with the expected join type. Record the identity, network and image decisions from [Choose Identity and Network](/windows-365/identity-network/) before creating a policy.

## What to save

Take a screenshot at each of these points: the license assignment, the group members, the policy target, the provisioning result and the first successful session. Add the date and a one-line note to each image. Remove names, tenant IDs and device identifiers before you share them. If a check fails, keep the error text and write down how you fixed it. The pilot is not done just because the portal accepted a form.

Next: [Windows 365 Enterprise: Choose Identity and Network](/windows-365/identity-network/).

## Sources

- [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)
- [Assign licenses](https://learn.microsoft.com/en-us/windows-365/enterprise/assign-licenses)
