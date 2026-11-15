---
title: "Windows 365 Enterprise: Point-in-Time Restore"
layout: post.njk
permalink: /windows-365/point-in-time-restore/
order: 206.5
part: 7
tags: w365-series
deck: "Read the restore points, plan the data window, and validate recovery without risking the only working Cloud PC."
---

A Cloud PC restore returns its disk to an earlier point. It can help after a bad configuration or damaged installation. It also removes local changes made after the chosen point. This article covers how to plan the action, look at the available restore points in Microsoft Intune (the Microsoft device management service) and use the admin path and the user path. A restore point is a saved copy of the Cloud PC disk at one moment.

## Before you begin

You need a Windows 365 Enterprise Cloud PC managed in Intune, an admin role that can manage Cloud PCs in Intune (the exact permissions are listed in [Configure restore settings](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-configure)), and a test user or group for restore settings. Use a disposable Cloud PC for the actual restore exercise. Save important work to an approved external service, record the device state and agree on the restore point with the user. Do not use your only working Cloud PC for this test.

| Check | Why it matters |
|---|---|
| User and device | Make sure the selected Cloud PC belongs to the intended test user. |
| Restore point time | Local files, installed apps, updates and settings changed afterward may be lost. |
| Cloud data | OneDrive data is outside the restored disk, but verify sync before taking action. |
| Identity and agents | Older machine secrets, certificates or keys may break sign-in or management. |
| Recovery path | Know who can help if the restored device does not connect. |

Restore is one of several Cloud PC actions. The others are restart, resize, move to another region, and reprovision, which means building the Cloud PC again.

![A Cloud PC has restore points. The service makes 10 short-term points at an interval set in the Cloud PC user setting in Intune, of 4, 6, 12, 16 or 24 hours. The service makes 4 long-term points, one every 7 days, which cannot be changed. An administrator can make one manual point on demand, which a newer manual point replaces and which expires after about 28 days. You choose the closest healthy point. A point with a triangle warning is unhealthy and less likely to restore. An administrator starts the restore in Intune for one Cloud PC or in bulk, and a user can start it only if the user setting allows it. The Cloud PC returns to the chosen point. Everything saved on it after that point is lost, but data in external services such as OneDrive is kept. After the restore the user signs in to check it. If the user cannot connect, restore to a more recent point.](/img/windows-365/windows-365-point-in-time-restore.svg)

*Source: [Point-in-time restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Step 1: understand the restore points

Microsoft lists three types of restore point for Enterprise:

- **Short-term:** ten points that the service creates on its own. You choose the interval: 4, 6, 12, 16 or 24 hours. A shorter interval means a shorter history, because ten points always cover ten intervals.
- **Long-term:** four points that the service creates on its own every seven days. You cannot change them.
- **Manual:** one on-demand point per Cloud PC that an administrator creates. A new manual point replaces the existing one. If it is not replaced, it expires in approximately 28 days. A new manual point can take up to an hour or more to appear in the list. See [Create on-demand manual restore points](https://learn.microsoft.com/en-us/windows-365/enterprise/create-manual-restore-point).

These are service rules. Your actual device list depends on its history and settings.

A list of restore points does not show that a disk restore works. Test it on a disposable Cloud PC.

## Step 2: configure the user setting on a test group

1. In the Intune admin center, go to **Devices > Cloud PC Settings > Create > User settings**. Portal labels can change; confirm them in your tenant. Microsoft describes the same path as **Devices > Cloud PC Settings > Add**.
2. Name the setting. Choose whether to allow the user to initiate restore and select the short-term restore-point frequency. The page also has a separate **Local admin** choice, which gives the user local administrator rights on the Cloud PC. Do not enable it just to test restore. The other two options are named **Allow user to initiate restore service** and **Frequency of restore-point service**. Your tenant may also show switches for user reset and user-initiated disaster recovery. They are not part of restore, so leave them off here.
3. Select **Next**, assign the intended pilot group, and review the settings before **Create**.
4. Record the group, interval, self-service permission and creation time. Later, check the actual restore-point list on the test Cloud PC. A saved setting does not show that a new point exists.

This is the current [Microsoft configuration sequence](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-configure). The setting gives assigned users access to the restore feature. The user-initiated option controls whether they can start the restore themselves.

## Step 3: inspect and choose a single Cloud PC point

1. In Intune, open **Devices > All Cloud PCs** and select the disposable test Cloud PC. Record its status, user, current configuration and visible restore points.
2. Choose the closest healthy point that solves the test problem. Note its timestamp and the local changes that will be lost. A point is unhealthy when the service has flagged it with a triangle warning icon. You can still restore from it, but it has a lower probability of a successful restore.
3. Confirm externally stored user data and the recovery contact. Save a screenshot of the current state, a timestamped local test file you can throw away, and the installed app and policy state. The test file makes the rollback visible. Never use real user data as the marker.
4. Select **Restore**, choose the point and read the confirmation. On the only working Cloud PC, stop here and do not confirm. On an approved disposable test Cloud PC, confirm and capture the **Restoring** status.
5. After completion, connect and compare the local test file, sign-in, Intune check-in, compliance, required apps, update history and user data with the before-state. Keep the details of both successes and failures.

The [single-device restore procedure](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-single-cloud-pc) specifies the Intune action and the **Restoring** status. It does not promise that every application or credential will work after a disk rollback. If the user cannot connect after a restore, Microsoft advises a second restore to a more recent point. On rare occasions you may need to reprovision the Cloud PC, when every point holds obsolete credentials ([overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview#best-practices)).

## Bulk and user-initiated paths

Bulk restore is a separate admin workflow. First test one disposable Cloud PC. Then follow the [bulk restore procedure](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-bulk): in Intune, go to **Devices > All devices > Bulk Device Actions** and choose the device action **Restore**. You pick one date and time and a range: before, after, or whichever is closest. You can also skip unhealthy snapshots unless all of them are unhealthy. Then you select the Cloud PCs. Each Cloud PC is restored to its own closest point, so record every device and the point it used. Results may differ between devices.

If the user setting allows self-service, a user can start the restore on the Windows 365 website (windows365.microsoft.com), as described in [Manage your Cloud PC](https://learn.microsoft.com/en-us/troubleshoot/windows-365/manage-windows-365-cloud-pcs#restore-your-cloud-pc):

1. Under **Your Cloud PCs**, select the three dots (**...**) on the Cloud PC and select **Restore**.
2. Tick **Yes, I want to restore this Cloud PC**, choose a restore point from the drop-down list and select **Restore**.
3. When it finishes, a green **Restored** message means success. A red **wasn't restored. Try restoring again** message means it failed.

The Cloud PC is unavailable until the restore finishes, and the user cannot undo it. Agree on the data-loss window and save the service and desktop result, as you would for an admin action. Turning on the permission does not mean a user has restored a device.

## What a restore does not show

A restart is a different operation and tells you nothing about restore. Choose a recent point to reduce data loss and the risk from rolling credentials. Rolling credentials are passwords, secrets, certificates and keys that Windows and agents change on a schedule. A restored disk may hold older ones that no longer match. Keep error text and timestamps in your log.

## Cleanup and next step

After a disposable restore test, remove the test assignment and the Cloud PC through the supported lifecycle, check what data is kept and remove any paid test resources. Do not delete your existing Enterprise pilot for this test. The next article, [Secure Access and Plan Recovery](/windows-365/security-recovery/), covers Conditional Access, device security and the wider recovery plan.

Next: [Windows 365 Enterprise: Secure Access and Plan Recovery](/windows-365/security-recovery/).

## Sources

- [Point-in-time restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview)
- [Configure restore settings](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-configure)
- [Restore a single Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-single-cloud-pc)
