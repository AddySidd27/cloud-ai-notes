---
title: "Windows 365 Enterprise: Image, Policy and First Provisioning"
layout: post.njk
permalink: /windows-365/provision/
order: 204
part: 4
tags: w365-series
deck: "Choose an image, assign a small pilot policy and verify the Cloud PC instead of stopping at policy creation."
---

A provisioning policy is the instruction set for creating Cloud PCs for its assigned group. Before opening the wizard, decide the join type, network, image, language and pilot group. Keep a dated record of those choices so that later screenshots can be interpreted. This chapter is a portal walkthrough. My existing Enterprise Cloud PC was observed as provisioned and usable, but the repository does not contain a continuous screenshot record of its original wizard and first provisioning run.

## Before opening Intune

Check the current [Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements) and [administrator permissions](https://learn.microsoft.com/en-us/windows-365/enterprise/customer-permissions). Confirm that the intended pilot user has the Enterprise license and belongs to the small Microsoft Entra group you will target. A seat in inventory is not the same as an assignment to that user.

My September 24, 2026 capture shows one Enterprise seat assigned and none available. It does not show the assignee or the date of first provisioning.

![Sanitized Enterprise license inventory from my pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-01-2026-09-24-license-inventory.jpg)

**Checkpoint:** Save separate sanitized license assignment and pilot group membership views in your own tenant. Record the SKU, group, date, administrator role, intended network and success criteria.

## Pick the image

Use a gallery image for an uncomplicated first pilot. It removes a custom image maintenance dependency while you learn provisioning and Intune application delivery. Use a custom image when an actual application or configuration requirement justifies it, and keep an owner for image updates and testing. Review Microsoft's [device images guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images) before using your own image.

## Create the policy in Intune

1. Sign in to [Microsoft Intune admin center](https://intune.microsoft.com/) with the appropriate role. Open **Devices > Provision Cloud PCs > Provisioning policies > Create policy**. Select the Enterprise experience where the wizard offers a product or mode.
2. On **General**, enter a pilot-specific policy name, select **Microsoft Entra join** and **Microsoft-hosted network** for the first cloud-only exercise. Record the geography or region option presented. An ANC is optional and should be selected only after its health checks pass.
3. On **Image**, select the planned gallery image. On **Configuration**, review language and region and any offered update settings. Compare each choice with the current [Microsoft instructions](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy), since the portal can change.
4. On **Assignments**, target only the prepared pilot group. At **Review + create**, compare the join, network, image and group with your written plan before creating the policy.
5. Open **Devices > Provision Cloud PCs > All Cloud PCs**. Locate the intended user, policy and status. Record the exact stage and error if provisioning fails before changing an input.

For a screenshot-led lab, capture the **General**, **Image**, **Configuration**, **Assignments** and **Review + create** screens as you perform them. Sanitize identifiers, and place each image directly after its matching step. I have no public Enterprise pilot screenshot of these five wizard screens, so I am not presenting another author's image as my own.

Do not interpret a saved provisioning policy as a provisioned Cloud PC. The pass result includes a Cloud PC associated with the intended user, successful connection, expected join and Intune enrollment. Check the [automated provisioning sequence](https://learn.microsoft.com/en-us/windows-365/enterprise/automated-provisioning-steps) when a stage stalls.

## Connect and compare four results

Have the assigned user open [windows365.microsoft.com](https://windows365.microsoft.com/), launch the Cloud PC in a browser, sign in, disconnect and reconnect. Compare the device in Intune and Microsoft Entra with the policy and user you recorded. A **Provisioned** status, visible tile, usable session and Intune check-in answer different questions.

| View | What to record | Pass condition |
| --- | --- | --- |
| License and group | SKU, user assignment, group membership | Intended user is in scope |
| All Cloud PCs | User, policy, state and time | Expected Cloud PC is Provisioned |
| User portal | Tile, first sign-in and reconnect | User can use the desktop |
| Intune device | Join type, primary user and check-in | Expected managed device reports |

My [dated Enterprise portal check](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-09-24-portal-check.md) records an existing Provisioned Cloud PC, a pilot-user web session, Intune record and join output. That verifies the state seen on September 24. It cannot reconstruct the original license assignment or policy wizard. [Part 5](/windows-365/connect-verify/) covers the connection check.

## Troubleshoot in order

| Symptom | First check |
| --- | --- |
| No Cloud PC for the user | License, group membership, policy assignment and timing |
| Policy cannot use an ANC | ANC health and selected network |
| Provisioning failure | Exact stage and error in Intune; correlate with network and identity requirements |
| Provisioned but unusable | User connection, sign-in and device status as separate tests |

The [Enterprise provisioning use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-02-enterprise-provisioning.md) and [first Cloud PC lab](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/02-first-cloud-pc-lab.md) expand these checks. My repository documents an existing provisioned, Entra-joined and Intune-enrolled Enterprise Cloud PC. It does **not** yet contain an uninterrupted fresh assignment-to-first-sign-in capture. This chapter is a reproducible procedure, not evidence that I repeated the full sequence.

Next: [connect and inspect the device](/windows-365/connect-verify/).

### Microsoft Learn

- [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)
- [Automated provisioning steps](https://learn.microsoft.com/en-us/windows-365/enterprise/automated-provisioning-steps)
