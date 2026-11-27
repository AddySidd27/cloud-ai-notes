---
title: "Windows 365 Disaster Recovery and Outages: What Protects a Cloud PC and What You Do"
seoTitle: "Windows 365 Disaster Recovery and Outages"
layout: post.njk
permalink: /windows-365/disaster-recovery-and-outages/
order: 219
part: 20
tags: w365-series
deck: "Know which protection covers which failure, and follow a plain set of steps when a whole region has an outage."
---

A Cloud PC can fail in small ways, such as a failed host, or in a big way, such as a whole Azure region going down. Windows 365 has a different protection for each. This article is for administrators of Windows 365 Enterprise. After reading it you can say which protection applies to which failure, find out whether Microsoft already knows about an outage, and follow an example runbook for a regional outage.

Windows 365 Flex has its own pages, so this article covers Enterprise. Cross region disaster recovery is also available for Windows 365 Flex in Dedicated mode.

Restoring a Cloud PC to an earlier point is covered in [Point-in-Time Restore](/windows-365/point-in-time-restore/), so it is only summarised here. Moving a Cloud PC to another region is covered in [The Life of a Cloud PC](/windows-365/cloud-pc-lifecycle/). Daily and weekly checks are in [Daily Operations and Remediation](/windows-365/daily-operations-and-remediation/).

## Key terms

| Term | Meaning |
|---|---|
| Region | An Azure location where Cloud PCs run. A regional outage is a problem with a whole region. |
| Availability zone | A separate location inside a region. Availability zones do not protect against an outage of the whole region. |
| RPO (restore point objective) | The target for how much data you can lose, measured as time. An RPO under 4 hours means the recovered copy can be up to 4 hours old. |
| RTO (restore time objective) | The target for how long recovery takes. An RTO under 4 hours means users get a working Cloud PC within 4 hours. |
| Restore point | A saved copy of a Cloud PC as it was at one point in time. |
| Primary Cloud PC | The user's normal Cloud PC, in its normal (primary) region. |
| Cross region disaster recovery (cross region DR) | An optional service that makes temporary copies of Cloud PCs in a backup region, far from the primary one. |
| Cross region DR user setting | The setting that includes users in cross region DR. A Cloud PC takes part only if its user is in one. |
| Disaster Recovery Plus (DR Plus) | A separate optional service that reserves capacity in an alternate region and has a shorter RTO. |
| Temporary Cloud PC | The copy a user works on while cross region DR is active. |
| Activate, deactivate | The admin actions that start and end cross region DR. |
| Failback | Going back from the temporary Cloud PC to the primary Cloud PC. |
| Provisioning policy | The Intune policy that sets where new Cloud PCs are created, such as the region or network. |
| Azure network connection (ANC) | A network connection you provide, instead of using a Microsoft hosted network. |
| Service health | The page in the Microsoft 365 admin center that lists incidents and advisories. |
| Message center | The page in the Microsoft 365 admin center for planned changes and planned maintenance. |

## What protects a Cloud PC

![Left: four protections for a Windows 365 Enterprise Cloud PC. In-zone recovery is automatic. Point-in-time restore is started by an admin. Cross region DR has an RPO under 4 hours and an RTO under 4 hours when fewer than 50,000 Cloud PCs are DR-licensed. DR Plus reserves capacity with an RTO under 31 minutes. Right: a short version of the outage steps in five steps, from checking Service health to deactivating or waiting for automatic failback.](/img/windows-365/windows-365-disaster-recovery.svg)

*Source: [Windows 365 operations guide](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-operations-guide), [Cross region disaster recovery in Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/cross-region-disaster-recovery) and [Activate or deactivate cross region disaster recovery](https://learn.microsoft.com/en-us/windows-365/enterprise/cross-region-disaster-recovery-activate).*

| Protection | Covers | Who acts | Recovery target |
|---|---|---|---|
| Automated in-zone recovery | Host failure, power failure, networking issues | Nobody. It is automatic. | RPO about 0 (almost no data loss) |
| Point-in-time restore | A Cloud PC that needs to go back to an earlier state | An admin. Users can also restore if you allow it. | You choose the restore point |
| Cross region DR | A regional outage | An admin activates it | RPO under 4 hours, RTO under 4 hours |
| Disaster Recovery Plus | A regional outage, with reserved capacity | Users can self-activate if you allow it. | RTO under 31 minutes |

### Automated in-zone recovery

If a compute failure happens inside an availability zone, the workload moves to healthy compute in the same zone. The triggers are host failure, power failure and networking issues. The recovery uses an up-to-date copy of the OS disk, so the RPO is about 0. The user sees a brief interruption and reconnects. You do not need to do anything. It cannot help if the whole region is down, which is why cross region DR exists.

### Point-in-time restore in one paragraph

Point-in-time restore lets an administrator return a Cloud PC to the exact state it had at an earlier time. Changes made after the chosen restore point are lost. You can also let users restore their own Cloud PCs with the Windows App setting **Allow users to initiate a Restore**. The restore point types, the steps and the risks are in [Point-in-Time Restore](/windows-365/point-in-time-restore/).

## Cross region disaster recovery

Cross region DR is an optional service. It protects Cloud PCs and data against regional outages. When it is licensed and activated, it creates temporary copies of Cloud PCs in a backup region that is far from the primary one.

You activate it yourself. It ends when you deactivate it. If you do not deactivate it, the service returns users to their primary Cloud PCs on its own after the failback period described below. So it is manual to start and can be automatic to end.

| Item | What applies |
|---|---|
| Editions | Windows 365 Enterprise, and Windows 365 Flex in Dedicated mode |
| RTO | Less than 4 hours for tenants with fewer than 50,000 DR-licensed Cloud PCs. As a general guideline, up to 50,000 DR-enabled Cloud PCs per backup region. |
| RPO | Less than 4 hours |
| Activation | Manual, by an administrator |
| Deactivation | Manual, or automatic failback up to 7 days after Microsoft declares the outage over |
| Capacity | Not guaranteed. It depends on free capacity in the backup region when the outage happens. Nothing is reserved in advance. |

If more than 50,000 Cloud PCs are enabled in the same backup region, recovery still goes ahead, but Cloud PCs may come back in stages as capacity becomes available.

### Licensing

Cross region DR applies only to a Cloud PC that meets both conditions:

- The user has a Windows 365 Cross Region Disaster Recovery add-on license.
- The user is included in a cross region DR user setting.

You can assign cross region DR to only some users. Cloud PCs without it are not affected and do not fail over. During a failover, the RPO and RTO goals depend on the number of DR-licensed Cloud PCs, not on the total number of Cloud PCs in the tenant. Assign DR licenses only to users who have a documented RTO requirement. General license planning is in [Windows 365 licensing](/windows-365/licensing/). Setting up cross region DR is not covered in this article.

### What the user sees

- When cross region DR is activated, affected users get a warning the next time they sign in.
- Users cannot reach their Cloud PCs until the move to the backup region is complete.
- After that, the user signs in to a temporary Cloud PC. It is built from the latest restore point, so it has the configuration, the data on the local disk and the user-installed apps as of that point, up to the RPO.
- Cloud PCs that are active in a temporary backup region do not receive a new Cloud PC configuration until they return to the primary region.
- When cross region DR is deactivated, the temporary Cloud PC is deleted. No apps, settings or data from it are kept. Data in cloud storage and cloud apps is not affected. Tell users to save work to OneDrive while they use the temporary Cloud PC.

### Limits and edge cases

- Once Microsoft declares the primary region healthy again, automatic failback happens after up to 7 days. The 7-day timer starts when the outage is declared over, not when you activated cross region DR.
- If you activate cross region DR without a Microsoft-declared outage, for example to test, Cloud PCs fail back 7 days after activation. This period cannot be extended.
- If the backup region has no capacity or is not healthy, the backup Cloud PC is not created. The data is still kept and remains accessible in the backup region.
- Your restore points are kept safe in the other region even if a temporary Cloud PC cannot be created right away.

## Disaster Recovery Plus

DR Plus is the option for when you need guaranteed capacity or tighter recovery times. What is different from cross region DR:

- Capacity is reserved in the alternate region. Cross region DR does not reserve capacity in advance.
- The RTO is less than 31 minutes.
- Users can self-activate it if the Windows App setting **Allow users to initiate Disaster Recovery Plus service** is on.

DR Plus has its own licensing and limits. Check them before you rely on it. This article does not cover them, and the runbook below covers cross region DR only.

## Moving a Cloud PC is not disaster recovery

Cross region DR is for unplanned outages only. For a planned or permanent region change, use Move Cloud PC. It is a controlled, permanent migration, and it avoids the automatic failback that comes with cross region DR.

- The **Move** device action (preview, so it can change) relocates selected Enterprise Cloud PCs to another region or Azure network connection without changing the provisioning policy. Bulk moves are limited to 100 Cloud PCs.
- To move all Cloud PCs in a provisioning policy, including Flex in Dedicated mode, edit the provisioning policy.

Move has its own limits. Check them before you rely on it. What happens to a Cloud PC during a move is covered in [The Life of a Cloud PC](/windows-365/cloud-pc-lifecycle/).

## Activate and deactivate in Intune

Set up cross region DR (the add-on licenses and the user setting) before an outage. When a regional outage happens, you decide whether to activate. Activating moves users to a new Cloud PC in a temporary region.

1. Sign in to the Microsoft Intune admin center.
2. Open the Cloud PC optional business continuity and disaster recovery status report. If it shows errors, correct them before you continue.
3. Select **Devices** > **All devices** > **Bulk device actions**.
4. On **Basics**, set **OS** to Windows, **Device type** to Cloud PCs and **Device action** to **Optional disaster recovery**.
5. For **Action type**, choose **Activate cross region disaster recovery** or **Deactivate cross region disaster recovery**.
6. Select **Next**. On **Devices**, pick individual Cloud PCs or a group. Only Cloud PCs that can take this action are shown. To deactivate everything that is currently activated, use the select-all box.
7. Select **Next**, then **Create** on **Review + create**.

Deactivation can take up to one hour to move the user back to the primary Cloud PC. During that time the user may keep using the temporary Cloud PC. When the transfer ends, the user signs in to the primary device within a few minutes. The temporary Cloud PC is deleted, so users should save work to OneDrive before then.

## DR readiness checklist

- [ ] The first backup is complete in the Cloud PC optional business continuity and disaster recovery status report. The first backup may take several days.
- [ ] The activation and deactivation procedure is written in your runbook.
- [ ] You run regular DR drills: activate and deactivate test devices.
- [ ] If you use an ANC (your own network connection), it passes health checks in the backup region.

As a starting point, not a product rule, validate DR readiness monthly and test activation and deactivation quarterly.

## How to find out about an outage

Windows 365 depends on Microsoft Entra ID, Intune, Azure compute and Azure networking. When one of them has a disruption, first find out whether Microsoft already knows about it and when it expects to fix it.

**Service health.** Go to the Microsoft 365 admin center > **Health** > **Service health**.

- The **Overview** tab shows all services and active incidents or advisories.
- **Issues for your organization to act on** lists issues in your own environment.
- **Active issues Microsoft is working on** lists what Microsoft is investigating or fixing.
- **Issue history** shows issues resolved in the last 7 or 30 days.
- **Report an issue** lets you tell Microsoft about a problem that is not listed.
- Updates are posted hourly unless the posting says otherwise.
- For broad-impact incidents, a preliminary post-incident review (PIR) comes within 48 hours of resolution. The final PIR follows within five business days.

Common status values:

| Status | Meaning |
|---|---|
| Investigating | Microsoft is aware of a possible issue and is gathering information |
| Service degradation | Issue confirmed. The service is slower or only sometimes available. |
| Service interruption | A significant issue affects user access to the service |
| Restoring service | The root cause is known and a fix is in progress |
| Extended recovery | A fix is in progress but will take time to reach all systems |
| Service restored | The fix is complete and the service is healthy |
| Post-incident report published | A PIR with the root cause and next steps is available |

**Message center.** Go to the Microsoft 365 admin center > **Health** > **Message center**. It carries planned changes, new features, planned maintenance and deprecations. Planned maintenance is announced here, not in Service health, and customers are notified at least five days in advance. Filter on the **Plan for change** category to find actions you must take. Use **Preferences** to get a weekly digest or major-update emails.

**If the admin center will not open.**

| Channel | Use it for |
|---|---|
| https://status.cloud.microsoft | Known issues that stop you signing in to your tenant |
| @MSFT365Status on X | Information on certain service events |
| https://azure.status.microsoft | Health of Azure services and regions |
| Microsoft 365 Admin app (mobile) | Service health and maintenance status |

Good habits: name at least two administrators to review Service health daily, set Message center email preferences for all Windows 365 administrators, and check Service health before you open a support case to see whether the issue is already known.

## Runbook: regional outage

This is an illustrative example, not a Microsoft-published procedure. Adapt it to your change process and test it before you need it.

1. Check Service health for active incidents that affect Windows 365 or Azure dependencies.
2. If the admin center cannot be opened, use https://status.cloud.microsoft, https://azure.status.microsoft and @MSFT365Status.
3. Confirm that Microsoft has declared a regional outage. Look for it in the Service health incident details, and note the incident ID and the affected services. (You can also activate without a declared outage, for example to test.)
4. Review the Message center for related planned maintenance or advisory posts.
5. Review DR readiness in the Cloud PC optional business continuity and disaster recovery status report in Intune.
6. Activate cross region DR for the affected users in the Intune admin center (see the steps above).
7. Tell users that temporary Cloud PCs are targeted within the recovery time objective (less than 4 hours). This is a target. Include the incident ID. Ask them to save work to OneDrive.
8. Watch DR activation progress in the status report, and watch Service health for updates.
9. After Microsoft declares the outage over, deactivate cross region DR, or wait for automatic failback (up to 7 days). Users keep working on the temporary Cloud PCs until then, and the temporary Cloud PC and its data are deleted at the end.
10. Check that the primary Cloud PCs are healthy after failback.
11. Read the post-incident report when it is published in the Service health issue history.
12. Hold an internal review. Record lessons learned and update the runbook.

## Common mistakes

- Treating in-zone recovery as protection against a regional outage. They are separate protections with different triggers.
- Skipping a drill. An untested DR plan is a common mistake.
- Assuming every Cloud PC fails over. Only users with the add-on license and a DR user setting do.
- Expecting guaranteed capacity from cross region DR. Capacity is not guaranteed. DR Plus reserves it.
- Using cross region DR for a planned region change. Use Move Cloud PC instead.
- Letting users save work only on the temporary Cloud PC. It is deleted at deactivation.
- Activating without checking the status report first.
- Using only the admin center for outage news. Know the backup channels.

## How to validate this in your environment

1. In Intune, open the Cloud PC optional business continuity and disaster recovery status report. Confirm the first backup is complete for your DR users.
2. Check that your DR users have the add-on license and are in a cross region DR user setting.
3. If you use an ANC, confirm it passes health checks in the backup region.
4. Run a drill with a few test devices: activate, sign in to the temporary Cloud PC, then deactivate. Note how long each step takes. A test activation fails back by itself after 7 days if you do not deactivate it.
5. In the Microsoft 365 admin center, open Service health and Message center. Confirm your administrators can see both and have set their email preferences.
6. Write the channels from the "If the admin center will not open" table into your runbook.
7. Write the runbook above with your own names, contacts and approval steps.

## Sources

- [Windows 365 operations guide](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-operations-guide)
- [Cross region disaster recovery in Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/cross-region-disaster-recovery)
- [Activate or deactivate cross region disaster recovery](https://learn.microsoft.com/en-us/windows-365/enterprise/cross-region-disaster-recovery-activate)
