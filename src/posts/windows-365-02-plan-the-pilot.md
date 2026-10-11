---
title: "Windows 365 Enterprise: Plan a Pilot That You Can Verify"
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

1. Review the license inventory and the pilot user's actual license assignment in Microsoft 365 admin center or Microsoft Entra admin center.
2. Verify the pilot group membership in Microsoft Entra. Record the time, because group and policy assignments can take time to apply.
3. Check the administrator role before opening the Intune Windows 365 provisioning area. Use the permissions your organization grants for the task.
4. Choose the identity, network and image using the next chapter. Write down the application or connectivity requirement behind each choice.
5. Define a pass result: the named pilot user sees one Cloud PC, connects, signs in, and its device appears in Intune with the expected join state.

The [tenant readiness use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-01-tenant-readiness-and-pilot-design.md) contains a longer worksheet. My sanitized [license inventory capture](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-01-2026-09-24-license-inventory.jpg) is real, but it shows inventory, not a new end-to-end assignment. Treat the five checks above as a procedure until you record them in your own tenant.

## Evidence to save

Capture the license assignment, group membership, policy target, provisioning result and first successful session at separate checkpoints. Add the date and a one-line observation to each image. Remove names, tenant IDs and device identifiers before publication. If a check fails, keep the error text and document the corrective step; do not call the pilot complete because the portal accepted a form.

Next: [choose identity and network](/windows-365/identity-network/).

### Microsoft Learn

- [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements)
- [Customer permissions needed for Windows 365 operations](https://learn.microsoft.com/en-us/windows-365/enterprise/customer-permissions)
