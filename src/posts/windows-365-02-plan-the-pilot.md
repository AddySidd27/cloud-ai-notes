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

A pilot succeeds when you can explain who received a Cloud PC, why it was assigned, and how you checked the result. Start with one test user and one small Microsoft Entra group. Keep the scope small enough that a mistaken policy does not affect the rest of the organization.

## What you need

Check the current [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements) before building. Confirm the user's eligible Windows 365 Enterprise license, Microsoft Entra and Intune prerequisites, an administrator with the appropriate Windows 365 and Intune permissions, and a supported region. Record the license SKU and its assigned user. A license visible in inventory is not proof that the intended user has it.

Choose a descriptive pilot group such as `W365-Pilot-Users` and record its members before assigning anything. Create a separate group for Cloud PC device policies if your Intune targeting model needs it. Decide who can change the provisioning policy and who will read the results. Avoid using a broad production group for a learning exercise.

| Decision | Pilot record |
| --- | --- |
| User and group | Sanitized user label and exact group name |
| License | SKU, assignment state and date checked |
| Identity | Microsoft Entra join or hybrid join, with reason |
| Network | Microsoft-hosted or ANC, with application requirement |
| Image | Gallery or custom, with application requirement |
| Success | Provisioned status, usable session and Intune check-in |

## Walk through the checks

### Step 1: inventory the Enterprise seat

In Microsoft 365 admin center, open the Windows 365 Enterprise licensing view. Record the total, assigned and available counts. Then open the intended pilot user's license details and verify the actual assignment. In my September 24 capture, one Enterprise seat was assigned and none were available. The crop does not identify the assigned user.

![Sanitized Windows 365 Enterprise license inventory](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-01-2026-09-24-license-inventory.jpg)

### Step 2: make a narrow pilot group

In Microsoft Entra admin center, create or select a dedicated **user** group for the pilot and add the licensed test user. Note the group name and membership time. Do not target all users. Save a sanitized group membership image in your own lab; this repository does not contain a public group membership screenshot.

### Step 3: check the administrator and success result

Verify the administrator's Windows 365 and Intune permissions before opening the provisioning wizard. Write a pass condition: the targeted user sees one Cloud PC, signs in, disconnects and reconnects, and the device appears in Intune with the expected join type. Record the identity, network and image decisions from [Choose Identity and Network](/windows-365/identity-network/) before creating a policy.

The [tenant readiness use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-01-tenant-readiness-and-pilot-design.md) contains a longer worksheet. The screenshot above is real, but it shows inventory, not a new end-to-end assignment. Treat the missing group and assignee screens as checks to capture when you reproduce the lab.

## Evidence to save

Capture the license assignment, group membership, policy target, provisioning result and first successful session at separate checkpoints. Add the date and a one-line observation to each image. Remove names, tenant IDs and device identifiers before publication. If a check fails, keep the error text and document the corrective step; do not call the pilot complete because the portal accepted a form.

Next: [choose identity and network](/windows-365/identity-network/).

### Microsoft Learn

- [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Customer permissions needed for Windows 365 operations](https://learn.microsoft.com/en-us/windows-365/enterprise/customer-permissions)
