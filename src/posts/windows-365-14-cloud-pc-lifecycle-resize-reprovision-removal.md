---
title: "The life of a Cloud PC: resize, reprovision, grace period and removal"
seoTitle: "Windows 365 Cloud PC lifecycle: resize, reprovision, removal"
layout: post.njk
permalink: /windows-365/cloud-pc-lifecycle/
order: 213
part: 14
tags: w365-series
deck: "Choose between resize, reprovision and deprovision, know what each one keeps or deletes, and use the grace period before a Cloud PC is lost."
---

A Cloud PC is a Windows desktop that Windows 365 gives to a user. Administrators manage it in Microsoft Intune, the Microsoft service for managing devices. Over time an administrator may need to give a user more memory, fix a Cloud PC that is broken, or deal with a Cloud PC that is in a grace period. Each case has a different action, and the actions do very different things to the user's data.

This article is for administrators who run Windows 365 Enterprise. It covers Enterprise Cloud PCs that are managed in Intune. After reading it you can pick the right action, say what it keeps and what it deletes, check what must be true before you start, and explain what a grace period is.

![A Cloud PC with the status Provisioned can follow three paths. Resize keeps data and changes the size. Reprovision deletes everything and builds a new Cloud PC. A Cloud PC in a grace period keeps working for seven days, then it is deprovisioned and its data is deleted.](/img/windows-365/windows-365-lifecycle.svg)

*Source: [Resize a single Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/resize-cloud-pc-single), [Reprovision a Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/reprovision-cloud-pc) and [Deprovision or end grace period for Cloud PCs](https://learn.microsoft.com/en-us/windows-365/enterprise/end-grace-period).*

## Key terms

- **Cloud PC:** the Windows desktop a user gets from Windows 365.
- **Microsoft Intune:** the service where administrators manage Cloud PCs. The **Intune admin center** is its web portal.
- **Status:** the state shown for each Cloud PC in the Windows 365 provisioning area of Intune. This article uses four: **Provisioned**, **Failed**, **Resize pending license** and **In grace period**.
- **Provisioning policy:** the settings Windows 365 uses to build Cloud PCs for a group of users, such as the image and the network.
- **Provision:** to build a Cloud PC. **Reprovision:** to delete the Cloud PC and build a new one.
- **Base image:** the Windows image a Cloud PC is built from.
- **Resize:** to change the size of an existing Cloud PC. Size here means the vCPU (processor cores), RAM (memory) and disk.
- **Remote action:** a task an administrator starts on a Cloud PC from Intune. **Resize** and **Reprovision** are remote actions.
- **License inventory:** the Windows 365 licenses you have available to assign. A resize needs an available license of the new size in it.
- **Direct license:** a license assigned to one user. **Group-based license:** a license a user gets through a Microsoft Entra group. A **Microsoft Entra group** is a group of users in Microsoft Entra.
- **Microsoft Entra hybrid join, bring your own network:** a Cloud PC setup that uses a virtual network you provide. A **subnet** is a range of IP addresses inside that network.
- **Grace period:** a seven-day period in which the user can keep using a Cloud PC. After it ends the user is logged off and loses access.
- **Deprovision:** to remove the Cloud PC. Its operating system and data are deleted. This article also calls this "removal".
- **End user reset:** an action that reinstalls the operating system on the same Cloud PC and deletes data and settings.

## The actions at a glance

| Action | Who starts it | Must be true first | Data and apps | What the user sees |
|---|---|---|---|---|
| Resize | Administrator, in Intune | Status is Provisioned. A license of the new size is available in the inventory | User and disk data are kept | Disconnected briefly |
| Reprovision | Administrator, in Intune | Status is Failed or Provisioned | All data, apps and customizations are deleted | Signed out. No Cloud PC until the new one is built |
| End user reset | The end user | Not covered here | Reinstalls the operating system. Data and settings are deleted | Cloud PC is down about 30 minutes or more. Same Cloud PC, fresh Windows |
| Deprovision (end the grace period) | Administrator, in Intune | The Cloud PC is in a grace period. It also happens by itself when the seven days end | The operating system and data are deleted | The user loses access |

Only deliberate "wipe and rebuild" actions, such as reprovision or reset, cause a Cloud PC to be completely reprovisioned. Moving, resizing, restarting and restoring do not. A move to another region or network keeps the data, but the Cloud PC is offline during the move. Restore is covered in [Point-in-Time Restore](/windows-365/point-in-time-restore/), so this article does not repeat it. Reset does not wipe Cloud Apps or Windows 365 Flex in shared mode. Neither is covered here.

The portal path depends on the task. Resize and Reprovision start from **Devices > All Devices**. Ending a grace period starts from **Devices > All Cloud PCs**.

## Resize: change the size, keep the data

Resize changes the vCPU, RAM and disk of a Cloud PC without reprovisioning it. You can raise or lower the RAM and vCPU. You can only raise the disk. When you downsize, sizes with less disk are grayed out. Resize is not currently supported for GPU Cloud PCs (Cloud PCs with a graphics processor).

### What must be true first

- **Role.** The admin needs certain built-in Microsoft Entra roles. A custom role with the same permissions also works. For a Cloud PC with a direct license, at least one of:
  - Intune Service Administrator
  - Intune Reader plus Cloud PC Admin roles
  - Intune Reader plus Windows 365 Administrator
- For a Cloud PC with a group-based license, at least one of Intune Service Administrator or Intune Reader plus Windows 365 Administrator, and in addition a role with Microsoft Entra group read and write membership and licensing permissions, like the Windows 365 Admin role.
- **Status.** The Cloud PC must be **Provisioned** in the Windows 365 provisioning area.
- **License.** There must be an available license in the inventory for the new size.
- **IP address (hybrid join, bring your own network only).** The subnet needs a second free IP address for the Cloud PC. The service uses it while it moves to the new size, so the Cloud PC can be rolled back if something goes wrong. It is released a few minutes after the resize ends. Make sure enough addresses are free for all the Cloud PCs you resize, or stagger your resizes. If too few addresses are free, resize can fail.

Resizing is simpler when the Microsoft Entra groups used for licensing are different from the groups used to target provisioning policies.

### Direct license

Open the Intune admin center, then **Devices > All Devices**, choose the device and select **Resize**. The list shows the sizes you can move to, based on the licenses in your inventory. Select one, then select **Resize**. If a license is available, the resize starts. Windows 365 removes the old license and assigns the new one for you.

### Group-based license

Here you handle the licenses yourself:

1. Create a new target Microsoft Entra group and add the users you want to resize. You can also use existing groups, if each group maps to one Windows 365 license type.
2. Assign the existing provisioning policy to the new target group. Do this only if you do not already have a separate group for provisioning policy assignment.
3. In **Devices > All Devices**, choose the device, select **Resize**, pick the new size and select **Resize** again.
4. The Cloud PC moves to the status **Resize pending license**.
5. Select **Users**, search for the user and select it, then select **Groups**.
6. Complete two licensing actions: remove the old license and assign the new license. The order does not matter. The resize starts only after both are done. To remove the old license, select **Groups**, select the group you are changing, then **Licenses**, select the old license, **Remove license**, **Yes** and **Save**. To assign the new one, select **Assignments**, select the license you want to resize to and select **Save**.
7. Follow the progress in the Windows 365 provisioning area.

What happens if you stop halfway, within 48 hours:

- You removed the old license but did not assign the new one: the Cloud PC goes into a grace period.
- You did neither: the Cloud PC returns to **Provisioned**.

If you assign a license of a different size than the one you chose, the Cloud PC is provisioned to match the configuration of the license you assigned.

### What the user sees

The user is disconnected briefly while the hardware is updated.

## Reprovision: delete and rebuild

Reprovision wipes the user's Cloud PC and builds a new one from the current provisioning policy. The user is signed out. All data, apps and customizations are deleted. The new Cloud PC often has a new device name. Windows 365 sends access information to the user after the new Cloud PC is created.

Use it when a problem cannot be fixed in a less disruptive way, for example a Cloud PC that is malfunctioning or corrupted, or whose earlier provisioning failed. Also use it when a change must be applied to the Cloud PC itself, such as a new provisioning policy with a different base image. Editing a provisioning policy does not change existing Cloud PCs. Changes to the network or image reach only new or reprovisioned Cloud PCs. Many organizations keep reprovision for special cases or as a last resort.

**Before you start:** the status must be **Failed** or **Provisioned**. Tell the user and make sure any critical data is saved somewhere else.

**How:** in the Intune admin center, select **Devices > All Devices**, choose the Cloud PC, select **Reprovision**, then select **Yes**.

## The grace period and deprovision

During a grace period the user can keep using the Cloud PC for seven days. After seven days the user is logged off and loses access, and the Cloud PC is deprovisioned. One way into a grace period is a group-based resize that you leave half done, as described above.

A grace period is not an instant lock. The user keeps using the Cloud PC until the seven days end or you end the grace period yourself.

### Ending the grace period early

You do not have to wait seven days. Ending a grace period is destructive, so tell the user first. In the Intune admin center, select **Devices > All Cloud PCs**. In the **Status** column, select **In grace period**, then **Deprovision now**, then **Yes**. These steps follow automatically:

1. The Cloud PC starts deprovisioning.
2. The user loses access.
3. The operating system and data are deleted. The Cloud PC is no longer available.
4. If the original provisioning policy was replaced with a different one, the Cloud PC is reprovisioned with the settings in the new policy.

So deprovision is not always the end. When a different provisioning policy now applies, a new Cloud PC is built from it. The old data is still deleted.

### Deprovision many Cloud PCs

Select **Devices > All devices > Bulk device actions**. On the Basics tab, select **Windows** as the OS, **Cloud PCs** as the device type and **Deprovision** as the action. Add the devices, then go to the **Review + Create** tab. When you select **Create**, the Cloud PCs are deprovisioned, all data is lost and this cannot be undone. Select only Cloud PCs that are in a grace period. The action can be blocked if you select a Cloud PC that is still provisioned.

## Common mistakes

- **Reprovisioning to change the size.** Resize keeps the data. Reprovision deletes it.
- **Expecting a policy edit to change existing Cloud PCs.** It affects only new or reprovisioned Cloud PCs.
- **Starting a resize without an available license of the new size.** Check the license inventory first.
- **Leaving a group-based resize half done.** Remove the old license and assign the new one within 48 hours.
- **Assigning the wrong target license.** The Cloud PC is provisioned to match that license.
- **Forgetting the second IP address on a hybrid join network.** Resize can fail.
- **Treating the grace period as a safe place to keep data.** After seven days, or after Deprovision now, the data is deleted.
- **Using a grace period to cut off access at once.** The user keeps using the Cloud PC during it.

## How to validate this in your environment

Use a test user and a test Cloud PC, never the only working Cloud PC of a real user.

1. In the Intune admin center, open **Devices > All Cloud PCs** and note the status of your test Cloud PC. It must be **Provisioned** before a resize, and **Failed** or **Provisioned** before a reprovision.
2. Check which kind of license the user has, direct or group-based. This decides which resize steps apply.
3. Check the license inventory for an available license of the target size.
4. Check your role against the list in the resize section.
5. Save a test file on the Cloud PC. Resize it. When it is back, confirm the file is still there and the status is **Provisioned**.
6. For a group-based resize, check that the status shows **Resize pending license** after you select **Resize**, and that the status changes after you remove the old license and assign the new one.
7. To check a grace period, open **Devices > All Cloud PCs** and look for a test Cloud PC whose **Status** column shows **In grace period**. Confirm the user can still use it.
8. Only if you want to test deletion, use **Deprovision now** on a test Cloud PC in a grace period. Confirm the Cloud PC is no longer available.

## Sources

- [Resize a single Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/resize-cloud-pc-single)
- [Reprovision a Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/reprovision-cloud-pc)
- [Deprovision or end grace period for Cloud PCs](https://learn.microsoft.com/en-us/windows-365/enterprise/end-grace-period)
