---
title: "Windows 365 Enterprise: Point-in-Time Restore"
layout: post.njk
permalink: /windows-365/point-in-time-restore/
order: 206.5
part: 7
tags: w365-series
deck: "Read the restore points, plan the data window, and validate recovery without risking the only working Cloud PC."
---

A Cloud PC restore returns its disk to an earlier point. It can help after a bad configuration or damaged installation. It also removes local changes made after the chosen point. In this chapter I plan the action, look at the available restore points in Microsoft Intune (the Microsoft device management service) and show the admin path and the user path. A restore point is a saved copy of the Cloud PC disk at one moment. **I have not restored my pilot Cloud PC.**

## Before you begin

You need a Windows 365 Enterprise Cloud PC managed in Intune, an admin role that can manage Cloud PCs in Intune (the exact permissions are listed in [Configure restore settings](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-configure)), and a test user or group for restore settings. Use a disposable Cloud PC for the actual restore exercise (judgement). Save important work to an approved external service, record the device state and agree on the restore point with the user. Do not use your only working Cloud PC for this test.

| Check | Why it matters |
|---|---|
| User and device | Make sure the selected Cloud PC belongs to the intended test user. |
| Restore point time | Local files, installed apps, updates and settings changed afterward may be lost. |
| Cloud data | OneDrive data is outside the restored disk, but verify sync before taking action. |
| Identity and agents | Older machine secrets, certificates or keys may break sign-in or management. |
| Recovery path | Know who can help if the restored device does not connect. |

The [lifecycle decision diagram](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/exported/10-cloud-pc-lifecycle-operations.svg) and its [draw.io source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/source/10-cloud-pc-lifecycle-operations.drawio) show where restore fits among the other Cloud PC actions (restart, resize, move to another region, and reprovision, which means building the Cloud PC again). It opens on GitHub. It is a decision diagram, not a portal screenshot.

## Step 1: understand the restore points

Microsoft lists three types of restore point for Enterprise:

- **Short-term:** ten points that the service creates on its own. You choose the interval: 4, 6, 12, 16 or 24 hours. A shorter interval means a shorter history, because ten points always cover ten intervals.
- **Long-term:** four points that the service creates on its own every seven days. You cannot change them.
- **Manual:** one on-demand point per Cloud PC that an administrator creates. A new manual point replaces the existing one. If it is not replaced, it expires in approximately 28 days (Microsoft Learn). Microsoft Learn also says a new manual point can take up to an hour or more to appear in the list. See [Create on-demand manual restore points](https://learn.microsoft.com/en-us/windows-365/enterprise/create-manual-restore-point).

These are service rules. Your actual device list depends on its history and settings.

In my pilot, the Intune **Restore points** view showed 14 automatic points (10 short-term plus 4 long-term, the ones the service creates on its own) before I requested a manual point. My [lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-16-restore-pilot.md) and the sanitized screenshots show the result. Figure 1 is below and Figure 2 is in the section on my lab. A list of restore points does not show that a disk restore works.

![Sanitized Intune list of 14 automatic restore points on the Enterprise pilot](https://github.com/AddySidd27/Windows365-enterprise-engineering/raw/refs/heads/main/evidence/w365-restore-points-public-20261016.jpg)

*Figure 1: Sanitized Intune list of restore points. The crop leaves out tenant and device identifiers.*

## Step 2: configure the user setting on a test group

1. In the Intune admin center, go to **Devices > Cloud PC Settings > Create > User settings**. Portal labels can change; confirm them in your tenant. Learn describes the same path as **Devices > Cloud PC Settings > Add**.
2. Name the setting. Choose whether to allow the user to initiate restore and select the short-term restore-point frequency. The page also has a separate **Local admin** choice, which gives the user local administrator rights on the Cloud PC. Do not enable it just to test restore. Learn names the other two options **Allow user to initiate restore service** and **Frequency of restore-point service**. Your tenant may also show switches for user reset and user-initiated disaster recovery. They are not part of restore, so leave them off here.
3. Select **Next**, assign the intended pilot group, and review the settings before **Create**.
4. Record the group, interval, self-service permission and creation time. Later, check the actual restore-point list on the test Cloud PC. A saved setting does not show that a new point exists.

This is the current [Microsoft configuration sequence](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-configure). The setting gives assigned users access to the restore feature. The user-initiated option controls whether they can start the restore themselves.

## Step 3: inspect and choose a single Cloud PC point

1. In Intune, open **Devices > All Cloud PCs** and select the disposable test Cloud PC. Record its status, user, current configuration and visible restore points.
2. Choose the closest healthy point that solves the test problem. Note its timestamp and the local changes that will be lost. A point is unhealthy when the service has flagged it with a triangle warning icon. You can still restore from it, but it has a lower probability of a successful restore.
3. Confirm externally stored user data and the recovery contact. Save a screenshot of the current state, a timestamped local test file you can throw away, and the installed app and policy state. The test file makes the rollback visible. Never use real user data as the marker.
4. Select **Restore**, choose the point and read the confirmation. On the only working Cloud PC, stop here and do not confirm. On an approved disposable test Cloud PC, confirm and capture the **Restoring** status.
5. After completion, connect and compare the local test file, sign-in, Intune check-in, compliance, required apps, update history and user data with the before-state. Keep the details of both successes and failures.

The [single-device restore procedure](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-single-cloud-pc) specifies the Intune action and the **Restoring** status. It does not promise that every application or credential will work after a disk rollback. If the user cannot connect after a restore, Learn advises a second restore to a more recent point. On rare occasions you may need to reprovision the Cloud PC, when every point holds obsolete credentials ([overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview#best-practices)).

## Bulk and user-initiated paths

Bulk restore is a separate admin workflow. First test one disposable Cloud PC (judgement). Then follow the [bulk restore procedure](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-bulk): in Intune, go to **Devices > All devices > Bulk Device Actions** and choose the device action **Restore**. You pick one date and time and a range: before, after, or whichever is closest. You can also skip unhealthy snapshots unless all of them are unhealthy. Then you select the Cloud PCs. Each Cloud PC is restored to its own closest point, so record every device and the point it used. Results may differ between devices. I have not tested bulk restore yet.

If the user setting allows self-service, a user can start the restore on the Windows 365 website (windows365.microsoft.com). Per [Learn](https://learn.microsoft.com/en-us/troubleshoot/windows-365/manage-windows-365-cloud-pcs#restore-your-cloud-pc):

1. Under **Your Cloud PCs**, select the three dots (**...**) on the Cloud PC and select **Restore**.
2. Tick **Yes, I want to restore this Cloud PC**, choose a restore point from the drop-down list and select **Restore**.
3. When it finishes, a green **Restored** message means success. A red **wasn't restored. Try restoring again** message means it failed.

The Cloud PC is unavailable until the restore finishes, and the user cannot undo it. Agree on the data-loss window and save the service and desktop result, as you would for an admin action. Turning on the permission does not mean a user has restored a device.

## What I tested and what I have not

| Check | What I saw on 16 October 2026 | Still to do |
|---|---|---|
| List of restore points | 14 automatic points and one later manual point, with sanitized portal captures | Restore a device and record whether the point was healthy. |
| Settings and assignment | 12-hour user setting saved; pilot group assigned; self-service restore off | Check later that the 12-hour schedule creates new points. |
| Manual point creation | Device action Completed and Manual point listed | This does not show a disk rollback. |
| Single-device restore | Not tested yet | Use a test Cloud PC and record the state before, the action status and the state after. |
| Bulk restore | Not tested yet | Run a separate multi-device lab. |
| User-initiated restore | Not tested yet; disabled in my pilot setting | Give the permission to a small group and record the result. |

My [October 7 restart](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-07-controlled-restart.md) is a different operation. It tells you nothing about restore. Choose a recent point to reduce data loss and the risk from rolling credentials. Rolling credentials are passwords, secrets, certificates and keys that Windows and agents change on a schedule. A restored disk may hold older ones that no longer match. Keep error text and timestamps in your lab log.

## Cleanup and next step

After a disposable restore test, remove the test assignment and the Cloud PC through the supported lifecycle, check what data is kept and remove any paid lab resources. Do not delete your existing Enterprise pilot for this test. The next chapter, [Secure Access and Plan Recovery](/windows-365/security-recovery/), covers Conditional Access, device security and the wider recovery plan. Windows Autopatch is not covered in this series yet.

## Microsoft Learn

- [Point-in-time restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview)
- [Configure restore settings](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-configure)
- [Restore a single Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-single-cloud-pc)
- [Restore multiple Cloud PCs](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-bulk)
- [Create on-demand manual restore points](https://learn.microsoft.com/en-us/windows-365/enterprise/create-manual-restore-point)
- [Rename, restart, restore and reset Cloud PCs (user steps)](https://learn.microsoft.com/en-us/troubleshoot/windows-365/manage-windows-365-cloud-pcs#restore-your-cloud-pc)

## My lab on 16 October 2026

I checked my only Enterprise Cloud PC in Intune. It was still **Provisioned** and compliant. Its **Restore points** view showed 14 automatic points; the newest was dated 16 October 2026 at 8:07:18 AM in the portal display. That is the list of restore points in Figure 1 (Step 1). It is not a completed rollback. That newest point was made before I created the 12-hour setting below.

I created **W365 Restore Pilot - 2026-10-16** in **Devices > Cloud PC Settings > Create > User settings** and assigned it to **Windows365-Group**, whose single direct member was the pilot user. The review screen showed a 12-hour frequency. Local admin, user reset, user-initiated restore and user-initiated disaster recovery were all **No** (the last two switches are not part of the restore steps above). Intune confirmed the setting was added; the list showed **Assigned: Yes**. That confirms the setting and the assignment. It does not show that a new scheduled point was made.

Next I selected **Create Restore Points** (Intune: **Devices > All devices >** the device **> Restore points > Create restore points**) for the Cloud PC and left the optional sharing choice off. The action initially showed **TakeSnapshot: Pending** (TakeSnapshot is the name of the device action). On the later check it showed **TakeSnapshot: Completed**, and the list contained a **Manual** point created at 12:58:24 PM, with an expiration shown for 15 November 2026. That date is about 30 days after creation, while Learn says approximately 28 days. I did not check why. I also did not check the portal's time zone, so the times above are as the portal showed them.

![Sanitized Intune view with the new manual restore point](https://github.com/AddySidd27/Windows365-enterprise-engineering/raw/refs/heads/main/evidence/w365-manual-restore-point-public-20261016.jpg)

*Figure 2: Sanitized Intune screenshot showing the manual point after the device action completed. The [lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-16-restore-pilot.md) has the action timeline.*

**Result:** The manual point was created. I have not tested a single-device, bulk or user-initiated restore yet, and I did not roll back my only working Cloud PC. A full recovery test needs a test Cloud PC, a marker file, a completed restore, a reconnect, and device and user checks.
