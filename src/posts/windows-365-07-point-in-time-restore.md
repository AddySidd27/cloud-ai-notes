---
title: "Windows 365 Enterprise: Point-in-Time Restore"
layout: post.njk
permalink: /windows-365/point-in-time-restore/
order: 206.5
part: 7
tags: w365-series
deck: "Read the restore points, plan the data window, and validate recovery without risking the only working Cloud PC."
---

A Cloud PC restore returns its disk to an earlier point. It can help after a bad configuration or damaged installation. It also removes local changes made after the chosen point. In this chapter, we plan the action, inspect the available points and show the exact admin and user paths. **The pilot Cloud PC was not restored.**

## Before you begin

You need a Windows 365 Enterprise Cloud PC managed in Intune, a suitable admin role, and a test user or group for restore settings. Use a disposable Cloud PC for the actual restore exercise. Save important work to an approved external service, record the device state and agree on the restore point with the user. Keep the only working production or demonstration device out of this test.

| Check | Why it matters |
| --- | --- |
| User and device | Make sure the selected Cloud PC belongs to the intended test user. |
| Restore point time | Local files, installed apps, updates and settings changed afterward may be lost. |
| Cloud data | OneDrive data is outside the restored disk, but verify sync before taking action. |
| Identity and agents | Older machine secrets, certificates or keys may break sign-in or management. |
| Recovery path | Know who can help if the restored device does not connect. |

The [lifecycle decision diagram](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/exported/10-cloud-pc-lifecycle-operations.svg) and its [draw.io source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/source/10-cloud-pc-lifecycle-operations.drawio) show where restore fits alongside restart, resize, move and reprovision. It is a decision diagram, not a portal screenshot.

## Step 1: understand the restore points

Microsoft lists three types for Enterprise: ten configurable short-term points, four long-term points created every seven days, and one on-demand manual point per Cloud PC. The short-term interval can be 4, 6, 12, 16 or 24 hours. A new manual point replaces the existing manual point and normally expires after about 28 days. These are service rules; your actual device list depends on its history and settings.

In the current pilot, the Intune **Restore points** view showed 14 automatic points before the manual-point request. The [dated lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-16-restore-pilot.md) and original, sanitized captures below show the actual result. A point inventory does not prove that a disk restore worked.

## Step 2: configure the user setting on a test group

1. In the Intune admin center, go to **Devices > Cloud PC Settings > Create > User settings**. Portal labels can change; confirm them in your tenant.
2. Name the setting. Choose whether to allow the user to initiate restore and select the short-term restore-point frequency. Review the separate **Local admin** choice; do not enable it just to test restore.
3. Select **Next**, assign the intended pilot group, and review the settings before **Create**.
4. Record the group, interval, self-service permission and creation time. Later, check the actual restore-point list on the test Cloud PC. A saved setting alone is not proof that a new point exists.

This is the current [Microsoft configuration sequence](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-configure). The setting grants assigned users access to the restore feature; the user-initiated option controls whether they can start the restore themselves.

## Step 3: inspect and choose a single Cloud PC point

1. In Intune, open **Devices > All Cloud PCs** and select the disposable test Cloud PC. Record its status, user, current configuration and visible restore points.
2. Choose the closest healthy point that solves the test problem. Note its timestamp and the local changes that will be lost. A triangle warning icon marks an unhealthy point. You can still restore from it, but it has a lower probability of a successful restore.
3. Confirm externally stored user data and the recovery contact. Save a before-state screenshot, a timestamped disposable local test file, installed app and policy state. The test file makes the rollback visible; never use real user data as the marker.
4. Select **Restore**, choose the point, and read the final confirmation. Stop before this step on the sole working Cloud PC. On an approved disposable lab, submit the action and capture the **Restoring** state.
5. After completion, connect and compare the local test file, sign-in, Intune check-in, compliance, required apps, update history and user data with the before-state. Preserve both success and failure details.

The [single-device restore procedure](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-single-cloud-pc) specifies the Intune action and the **Restoring** status. It does not guarantee that every application or credential will work after a disk rollback.

## Bulk and user-initiated paths

Bulk restore is a separate admin workflow. First test one disposable Cloud PC, then use the [bulk restore procedure](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-bulk) for the intended group and date or restore point. Record every selected device, because their available points and results may differ. This tenant has no completed bulk restore evidence.

If the user setting allows self-service, a user can start restore from the Windows 365 user experience. Agree on the data-loss window and capture the service and desktop result just as you would for an admin action. Do not confuse permission being enabled with proof that a user actually restored a device.

## What the pilot proves

| Check | Observed on 16 October 2026 | Still needed |
| --- | --- | --- |
| Restore-point inventory | 14 automatic points and one later manual point, with sanitized portal captures | A device restore and point health outcome |
| Settings and assignment | 12-hour user setting saved; pilot group assigned; self-service restore off | Later policy and scheduled-point processing check |
| Manual point creation | Device action Completed and Manual point listed | No disk rollback implied |
| Single-device restore | Not run | Disposable device before, action status and after-state |
| Bulk restore | Not run | Separate multi-device lab |
| User-initiated restore | Not run; disabled in pilot setting | Separate scoped permission and actual result |

The [controlled restart](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-07-controlled-restart.md) is a different operation. It cannot be used as evidence for restore. Choose a recent suitable point to reduce data loss and rolling-credential risk. Keep error text and timestamps in the lab record.

## Cleanup and next step

After a disposable restore test, remove the test assignment and Cloud PC through the supported lifecycle, verify retained data and remove any paid lab infrastructure. Do not delete the existing Enterprise pilot to complete this post. The next foundation chapter covers Windows Autopatch; [security and recovery decisions](/windows-365/security-recovery/) remain a separate advanced chapter.

### Microsoft Learn

- [Point-in-time restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview)
- [Configure restore settings](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-configure)
- [Restore a single Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-single-cloud-pc)
- [Restore multiple Cloud PCs](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-bulk)


## Live pilot: 16 October 2026

I checked the sole Enterprise Cloud PC in Intune. It remained **Provisioned** and compliant. Its **Restore points** view showed 14 automatic points; the newest was dated 16 October 2026 at 8:07:18 AM in the portal display. This is an inventory result, not a completed rollback.

![Sanitized Intune list of 14 automatic restore points on the Enterprise pilot](https://github.com/AddySidd27/Windows365-enterprise-engineering/raw/refs/heads/main/evidence/w365-restore-points-public-20261016.jpg)

*Figure 1: original Intune restore-point inventory. The crop omits tenant and device identifiers.*

I created **W365 Restore Pilot - 2026-10-16** in **Devices > Cloud PC Settings > Create > User settings** and assigned it to **Windows365-Group**, whose single direct member was the pilot user. The review screen showed a 12-hour frequency. Local admin, user reset, user-initiated restore and user-initiated disaster recovery were all **No**. Intune confirmed the setting was added; the list showed **Assigned: Yes**. This confirms configuration and assignment, not a new scheduled point.

Next I selected **Create Restore Points** for the Cloud PC and left the optional sharing choice off. The action initially showed **TakeSnapshot: Pending**. On the later check it showed **TakeSnapshot: Completed**, and the list contained a **Manual** point created at 12:58:24 PM, with an expiration shown for 15 November 2026. Portal time-zone context was not independently checked.

![Sanitized Intune view with the new manual restore point](https://github.com/AddySidd27/Windows365-enterprise-engineering/raw/refs/heads/main/evidence/w365-manual-restore-point-public-20261016.jpg)

*Figure 2: original Intune capture showing the manual point after the device action completed. [Read the dated lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-16-restore-pilot.md) for the action timeline and limits.*

**Result:** Point creation completed. No single-device, bulk, or user-initiated disk restore was run. The only working Cloud PC was not rolled back. An end-to-end recovery test still needs a disposable device, a before-state marker, a completed restore, reconnection, and device and user checks.
