---
title: "Windows 365 Enterprise: Image, Policy and First Provisioning"
layout: post.njk
permalink: /windows-365/provision/
order: 204
part: 4
tags: w365-series
deck: "Choose an image, assign a small pilot policy and verify the Cloud PC instead of stopping at policy creation."
---

A provisioning policy is the instruction set for creating Cloud PCs for its assigned group. Before opening the wizard, decide the join type, network, image, language and pilot group. Keep a dated record of those choices so that later screenshots can be interpreted.

## Pick the image

Use a gallery image for an uncomplicated first pilot. It removes a custom image maintenance dependency while you learn provisioning and Intune application delivery. Use a custom image when an actual application or configuration requirement justifies it, and keep an owner for image updates and testing. Review Microsoft's [device images guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/device-images) before using your own image.

## Create the policy

1. In the Microsoft Intune admin center, go to **Devices > Provision Cloud PCs > Provisioning policies** and create a policy. The labels may evolve; follow the [current Microsoft instructions](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) when the portal differs.
2. Give the policy a name that identifies the pilot. Select the planned join type and either the Microsoft-hosted network or a healthy ANC. Record the selected geography or network connection.
3. Select a gallery image and the desired language and region settings. Keep the first policy simple.
4. Assign only the prepared pilot group. Review the wizard summary and save the policy.
5. Check that the intended user has the proper license and group membership. Watch the provisioning status in Intune until it reaches a result, and save any failure details before changing inputs.

Do not interpret a saved provisioning policy as a provisioned Cloud PC. The pass result includes a Cloud PC associated with the intended user, successful connection, expected join and Intune enrollment. Check the [automated provisioning sequence](https://learn.microsoft.com/en-us/windows-365/enterprise/automated-provisioning-steps) when a stage stalls.

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
