---
title: "Windows 365 Daily Operations: Updates, Remediation and a Review Routine"
seoTitle: "Windows 365 Daily Operations and Remediation"
layout: post.njk
permalink: /windows-365/daily-operations-and-remediation/
order: 220
part: 21
tags: w365-series
deck: "Set up a review routine for Windows 365 Cloud PCs, fix problems in the right order, and know which remote actions lose data."
---

After go-live, a Cloud PC estate needs regular care. Someone has to check for problems, keep Windows up to date, and fix what breaks without making it worse. A Cloud PC is the Windows desktop that Windows 365 runs in the cloud for a user. This article is for administrators and operations teams who run Cloud PCs. It shows the order in which to try fixes, which remote actions can run in bulk, what Intune Remediations (script packages that detect and fix common issues) can do for you, and how often to review each area.

**Scope.** The article covers Windows 365 Enterprise and Windows 365 Flex in Dedicated mode. Flex in Shared mode differs in a few places, and the text says where. Flex Cloud PCs run in Dedicated mode or Shared mode (see Key terms). The routines here are suggested starting points. They are not product requirements. Adapt them to your own processes.

Other articles cover the neighbouring topics:

- Where to find reports, alerts and alert rules: [Monitor Windows 365](/windows-365/monitoring/).
- Disaster recovery, outage awareness and the regional outage runbook: [Windows 365 Disaster Recovery and Outages](/windows-365/disaster-recovery-and-outages/).
- The grace period and unused licenses: [Grace Period and Unused Licenses](/windows-365/grace-period-unused-licenses/).
- Checking settings, apps, updates and restart on a Cloud PC: [Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/).
- Naming owners and rolling out: [Operate, Roll Out and Extend](/windows-365/operate-and-extend/).

This article does not cover Message center planning, capacity and cost reviews, or automation with Microsoft Graph and Power Platform.

## Key terms

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop that Windows 365 runs in the cloud for a user. |
| Windows 365 Enterprise | The main edition this article covers. |
| Windows 365 Flex | Its Cloud PCs run in Dedicated mode or Shared mode. |
| Dedicated mode (Flex) | A Flex mode in which Cloud PCs power off when inactive, and a powered-on Cloud PC uses a license. A Dedicated mode Cloud PC is resized through its provisioning policy. |
| Shared mode (Flex) | A Flex mode in which shared Cloud PCs do not keep user data between sessions. Reprovision is routine here and can be scheduled. |
| Microsoft Intune admin center | The web portal where you manage Cloud PCs. |
| Provisioning policy | The settings Windows 365 uses to build Cloud PCs. |
| Remote action | A task an administrator starts on a Cloud PC from the portal, such as Restart or Resize. |
| Bulk action | A remote action started on many Cloud PCs at once. |
| Preview | A feature that can still change. Items marked preview in this article are preview features. |
| Maintenance window | A scheduled time when bulk resize actions run. It is a preview feature. |
| Resize | Change the size of an existing Cloud PC, which changes its CPU and RAM. |
| Restore point | A saved state of a Cloud PC that you can restore to. |
| Manual restore point | A restore point an administrator creates on demand for a Cloud PC. A Cloud PC can have one. A new one replaces the existing one, and it expires after about 28 days if it is not replaced. |
| Reprovision | Delete a Cloud PC and build a new one from the current provisioning policy. |
| Grace period | A 7-day period that a Cloud PC can be in before it is removed. The **Deprovision (end grace period)** action ends it early. |
| Update ring | A kind of Intune update policy for Windows devices. |
| Gallery image | A released Windows image, such as Windows 11 Enterprise 26H2, that a provisioning policy can use. |
| Admin Insights | A ranked list of items that Windows 365 finds and that need attention or offer optimization. It is under **Devices** > **Manage Windows 365 Cloud PCs** > **Cloud PC Overview**. |
| Alert | A notification Windows 365 raises when a specific event occurs, such as a failed connection. Alerts and their rules are under **Tenant administration** > **Cloud PC Alerts**. |
| Windows 365 admin assistant (preview) | An AI-assisted tool in the Intune admin center, under **Windows 365** > **Windows 365 Admin Assistant**. You describe a problem in plain words. In the preview it focuses on connectivity. Check its supporting data before you act, because a pattern does not always identify the cause. |
| Resource performance report | A report under **Reports** > **Endpoint analytics** > **Resource performance**. It gives a 0 to 100 score based on CPU and RAM spike time. |
| Connection quality report | A report under **Reports** > **Cloud PC overview** > **Connection quality**. It shows round-trip time, bandwidth, gateway and protocol and UDP use per Cloud PC. |
| UDP | A network protocol. The Connection quality report shows how much UDP your connections use. |
| DS Shortpath for public networks | A connection option. Its requirements are worth reviewing when connections are not using UDP. This article does not explain how to set it up. |
| TLS inspection | Inspection of network traffic by a network device. Inspection of the traffic of Windows 365 connections is not supported. |
| Service health | A page in the Microsoft 365 admin center that shows the health of Microsoft cloud services for your tenant, including active incidents and advisories. |
| Message center | A page in the Microsoft 365 admin center that announces planned changes, new features, planned maintenance and deprecations. |
| Intune Remediations | Script packages that detect and fix common support issues on devices before users notice them. Formerly called Proactive Remediations. |
| Detection script | The part of a script package that checks for a problem. |
| Remediation script | The part of a script package that fixes the problem. It runs only after the detection script reports the problem. |
| Exit code | The number a script returns when it ends. A detection script returns `exit 1` when it finds the issue. |
| MDM (Mobile Device Management) | Enrollment of a device in Intune so Intune can manage it. |
| Azure Network Connection (ANC) | A connection setting used for Cloud PCs on your own network. It is explained in [ANC troubleshooting](/windows-365/anc-troubleshooting/). |

![Windows 365 Enterprise remediation ladder. Intune Remediations script packages detect and fix common issues on Cloud PCs before users notice. When a problem is reported, five escalating steps run from triage to reprovision. Most remote actions support bulk, up to 5,000 Cloud PCs per operation.](/img/windows-365/windows-365-daily-operations.svg)

*Source: [Windows 365 operations guide](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-operations-guide) and [Remediations](https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations).*

## Maintenance windows (preview)

A maintenance window lets you pick the times when bulk resize actions run, and tells users in advance. A bulk resize is a Resize remote action started on many Cloud PCs at once. The Resize action is for Enterprise Cloud PCs. Flex in Dedicated mode is resized through its provisioning policy, and Flex in Shared mode cannot be resized.

What you can set:

- The schedule: daily, weekly or weekends, and the hours within the day. Times are the Cloud PC's local time.
- Each window must be at least two hours long.
- Which Microsoft Entra user groups the window applies to.
- How far ahead users are told about the coming change. The user is told in the session and cannot override or postpone the window.

You find it in the Intune admin center under **Tenant administration** > **Cloud PC maintenance windows (preview)**. After you create a window, follow the steps to bulk resize Cloud PCs and select **Use Cloud PC maintenance windows** on the **Basics** page.

What it does not do:

- It applies to bulk resize actions only.
- It is not responsible for the success or failure of the remote actions.
- It does not cover service maintenance, Windows updates, Intune payloads, OS updates or other activities. It does not schedule updates.

For an urgent fix, do not select **Use Cloud PC maintenance windows**. The action then runs at once.

## Updates for Cloud PCs

Cloud PCs are managed through Intune update policies in the same way as physical Windows devices. Choosing update rings is a deployment decision. Day to day, four practices keep Cloud PCs current:

1. After feature updates, check the Resource performance report for slowdowns.
2. Check the Windows Update compliance reports in Intune to find Cloud PCs that are missing patches.
3. When new gallery images are released, update your provisioning policies so that new and reprovisioned Cloud PCs start from a current baseline.
4. Open the update ring policies that target Cloud PCs and confirm they enforce automatic installation and automatic restart.

To look at updates on one Cloud PC, see [Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/).

### Update points that apply only to Flex

- **Dedicated mode:** a Cloud PC that has not been powered on in the previous seven days is powered on automatically so that Windows Update can check for and install updates.
- **Dedicated mode:** the service cancels deallocation while a Windows Update is in progress, so the update can finish.
- **Shared mode:** when a shared Cloud PC is provisioned or reprovisioned, Windows Update scans for and installs updates before the first user signs in. To keep the whole shared pool current and consistent, schedule a bulk reprovision.

## Remote actions

Windows 365 has remote actions for working on Cloud PCs at scale.

| Action | Bulk | What it is for |
|---|---|---|
| Restart | Yes | Resolve performance issues, apply pending updates |
| Restore | Yes | Roll back to a known-good state. Changes made after the restore point are lost |
| Resize | Yes | Address performance issues by scaling CPU and RAM. Enterprise only. Flex in Dedicated mode is resized through the provisioning policy. Flex in Shared mode cannot be resized |
| Reprovision | Yes | Enterprise and Flex in Dedicated mode: last resort only. Deletes the Cloud PC, including all user data, apps and settings, and builds a new one from the current provisioning policy. Flex in Shared mode: routine maintenance that can be scheduled |
| Collect diagnostics | Yes | Gather logs for troubleshooting |
| Place under review | Yes | Preserve the Cloud PC state for investigation or compliance |
| Troubleshoot | Yes | Run connectivity health checks |
| Rename | No | Update the Cloud PC display name |
| Create manual restore point | Yes | Back up before administrative changes such as resize or reprovision |
| Share restore point to storage | Yes | Export to Azure Storage for archival |
| Power on/off (Flex) | Yes | Manage Flex Cloud PC availability. Powering off signs out any signed-in user, and unsaved data is lost |
| Sync | Yes | Force an Intune policy sync |
| Update Windows Defender | No | Trigger a signature update |
| Deprovision (end grace period) | Yes | Remove Cloud PCs in the grace period without waiting for the 7-day period to expire |
| Move (preview) | Yes, up to 100 | Relocate selected Enterprise Cloud PCs to another region or Azure Network Connection without changing the provisioning policy |

Bulk actions support up to 5,000 Cloud PCs per operation, except where noted. You can also start bulk actions from a provisioning policy's **Devices** tab and follow progress on its **Action Status** tab.

Flex Cloud PCs support remote actions like Enterprise Cloud PCs, with one difference: if a Flex Cloud PC is powered off, remote actions start when it is next powered on.

## The remediation workflow

Work through these steps in order, and stop when the issue is solved. Each step is more disruptive than the one before. The data impact column is for Enterprise and Flex in Dedicated mode.

| Step | When | Action | Data impact |
|---|---|---|---|
| 1 | An alert, Admin Insights item or user report points to a problem | Triage severity and find the affected Cloud PCs | None |
| 2 | Users cannot connect, or connections fail | Describe the issue to Windows 365 admin assistant (preview) to find the likely cause and whether other Cloud PCs are affected. Run the **Troubleshoot** action, which runs connectivity health checks, and review the results | None |
| 3 | Cloud PCs are slow | Check the **Resource performance** report. If Cloud PCs are resource-constrained, resize them: use the **Resize** action for Enterprise, or change the Cloud PC size in the provisioning policy for Flex in Dedicated mode | None |
| 4 | The issue persists | Create a manual restore point to keep the current state, then restore to a known-good restore point | Changes made after the selected restore point are lost |
| 5 | The earlier steps did not solve it | Reprovision the Cloud PC | All user data, apps and settings on the Cloud PC are deleted. For Flex in Shared mode, reprovision is routine because no user data is kept between sessions |

Before you restore (step 4):

- A Cloud PC can have one manual restore point. Creating a new one replaces the existing one, so check whether someone made one before a resize or reprovision.
- Check the restore point list for the unhealthy snapshot indicator (a triangle icon). An unhealthy snapshot has a low probability of a successful restore.
- Store critical user data in OneDrive to avoid data loss between restore points.

Reprovision permanently deletes the user's Cloud PC, including all local data, apps and customizations. The user gets a new Cloud PC, often with a new device name. Data stored in OneDrive or other cloud services is not affected. Tell the user, confirm that critical data is backed up, and keep reprovision for problems that less disruptive actions cannot solve. This warning applies to Enterprise and Flex in Dedicated mode. Flex Cloud PCs in Shared mode do not keep user data between sessions, so reprovisioning is the standard way to return them to a known state.

What each action keeps and deletes is in [The life of a Cloud PC](/windows-365/cloud-pc-lifecycle/). Restore is in [Point-in-Time Restore](/windows-365/point-in-time-restore/).

## Proactive fixing with Intune Remediations

Intune Remediations are script packages that detect and fix common support issues before users notice them. Each package has a detection script, a remediation script and metadata. You find them in the Intune admin center under **Devices** > **Manage devices** > **Scripts and remediations**. Start with the built-in packages, such as:

- **Update stale Group Policies**
- **Restart Office Click-to-run service**

Requirements:

- **Devices:** Microsoft Entra joined or Microsoft Entra hybrid joined, and either MDM enrolled in Intune and running Windows Enterprise, Professional or Education, or co-managed and running Windows.
- **Licenses:** users of the devices need Windows Enterprise E3 or E5 (included in Microsoft 365 F3, E3 or E5), Windows Education A3 or A5 (included in Microsoft 365 A3 or A5), or Windows Virtual Desktop Access (VDA) per user. Check that the users of your Cloud PCs have one of these licenses before you rely on Remediations.
- **Permissions:** the person needs permissions for their role under the **Device configurations** category in Intune role-based access control.
- **Before first use:** an Intune Service Administrator must confirm the licensing requirements.
- **Scripts:** up to 200 script packages. A package can hold a detection script alone, or a detection and a remediation script. The remediation script runs only if the detection script ends with `exit 1`, which means it found the issue. With any other exit code, including empty output, the result is "issue isn't found" and the remediation script does not run. Scripts must be encoded in UTF-8. The maximum output size is 2,048 characters. Do not put reboot commands, passwords or other sensitive information in scripts. Do not put personal data in scripts or use scripts to collect it.
- **Schedule:** once, hourly (every n hours, fewer than 24) or daily. Remediations run on the device's local time unless you select **Use UTC**. If a scheduled run is missed, it runs as soon as the device is online. For scripts that are not urgent or use many resources, choose a less frequent schedule.

To check the results, open the script package and select **Device status**.

## Security review tasks

Security baselines, Conditional Access and Microsoft Defender for Endpoint onboarding are Microsoft security features and deployment decisions that this article names only as review items. After go-live, these are the repeat checks:

| How often | Task |
|---|---|
| Daily | Review security alerts from Defender for Endpoint, and investigate Cloud PCs with an elevated threat level |
| Weekly | Check the compliance status of the Cloud PC fleet in Intune |
| Monthly | Review Conditional Access sign-in logs for Windows 365 and Azure Virtual Desktop for anomalies |
| Quarterly | Check for new security baseline versions in Intune, test them on a pilot group of Cloud PCs, then update. Review Conditional Access policies |
| Annually | Do a security posture review and assess new Windows 365 security features |

## Review cadence

Recurring reviews at a glance:

| How often | Activity |
|---|---|
| Real time | Alert notifications (console and email) |
| Daily | Review Admin Insights and active alerts. Check the Cloud PC monitoring dashboard. Review Microsoft 365 Service health and Message center |
| Weekly | Review the Cloud PCs not available report. Check connection quality trends. Review Cloud PCs in the grace period. Flex: review concurrency and buffer use (see [Concurrency Buffer](/windows-365/flex-concurrency-buffer/)), and confirm that scheduled Shared mode reprovisions completed (provisioning policy **Action Status** tab) |
| Monthly | Review resource performance scores. Assess utilization. Review License and utilization. Validate disaster recovery readiness. Review What's new for Windows 365. Flex Shared mode: review user storage |
| Quarterly | Test disaster recovery activation and deactivation. Review security baselines. Adjust alert thresholds. Review Cloud PC Settings assignments. Update runbooks |
| Annually | Full operational review. Evaluate new Windows 365 features. Refresh business continuity and disaster recovery documentation |

Disaster recovery checks and outage awareness are explained in [Windows 365 Disaster Recovery and Outages](/windows-365/disaster-recovery-and-outages/).

To start: name at least two people to review Admin Insights, Cloud PC alerts, Service health and Message center every day, and send alert email to a distribution list instead of one person's mailbox. Naming owners before rollout is also in [Operate, Roll Out and Extend](/windows-365/operate-and-extend/).

## Two example runbooks

These runbooks are illustrative templates, not Microsoft-published procedures. Adapt them to your change management, approval and communication processes, and test them first. Actions that remove data (Restore, Reprovision) should follow your change approval process. A third runbook, for a regional outage, is in [Windows 365 Disaster Recovery and Outages](/windows-365/disaster-recovery-and-outages/).

### Cloud PCs not available

| Step | Action | Where |
|---|---|---|
| 1 | Verify the alert. Check Admin Insights for related items | **Tenant administration** > **Cloud PC Alerts**; **Cloud PC Overview** |
| 2 | Check the scope: one user or many. Describe the issue to Windows 365 admin assistant | **Cloud PCs that aren't available** report; Windows 365 admin assistant |
| 3 | Run **Troubleshoot** on the affected devices | Remote actions (bulk supported) |
| 4 | Review the health check results | Cloud PC > **Overview** > **Troubleshoot** |
| 5 | If it is related to an ANC, check the ANC health | **Devices** > **Provision Cloud PCs** > **Azure network connections** |
| 6 | If it persists, create a manual restore point to keep the current state, then restore to an earlier point. Changes made after the selected restore point are lost, so confirm with the user first | Remote actions |
| 7 | Last resort: reprovision. All user data, apps and settings are deleted and a new Cloud PC is built. First get user and change approval and confirm user data is in OneDrive or other cloud storage. Consider keeping the current state with **Share restore point to storage** or **Place under review**. For Flex in Shared mode, reprovision is routine | Remote actions |
| 8 | Record the root cause and the fix | Your IT service management (ITSM) tool |

### Performance degradation

| Step | Action | Where |
|---|---|---|
| 1 | Find the scope with connection health metrics and Admin Insights outlier cards | **Devices** > **Manage Windows 365 Cloud PCs** > **Monitor Cloud PCs** > **Connection health** |
| 2 | Check round-trip time and bandwidth for the affected group | Connection quality report |
| 3 | Check UDP use. If connections are not using UDP, review the DS Shortpath for public networks requirements | Connection quality report |
| 4 | Review CPU and RAM spike times | Resource performance report |
| 5 | If resource-constrained, start a Resize (Enterprise), or change the Cloud PC size in the provisioning policy assignment (Flex in Dedicated mode) | Remote actions; provisioning policy |
| 6 | If it looks network-related, check client location, gateway, UDP path, and whether the connection traffic is being TLS-inspected. Inspection of this traffic is not supported | Connection quality report; network configuration |
| 7 | If it is widespread, check for service incidents | Microsoft 365 admin center > **Health** > **Service health** |

## Common mistakes

- **Expecting a maintenance window to schedule Windows updates.** It covers bulk resize actions only.
- **Using Reprovision as the first fix on Enterprise or Flex Dedicated.** It deletes local data. Try steps 1 to 4 first.
- **Treating Flex Shared mode like Enterprise.** In Shared mode, reprovision is routine and Resize is not available.
- **Restoring without checking the manual restore point.** A new manual restore point replaces the old one. Changes made after the restore point you pick are lost.
- **Restoring to a snapshot marked unhealthy.** It has a low probability of a successful restore.
- **Sending alert email to one person.** Use a distribution list, and name at least two reviewers.
- **Scheduling heavy remediation scripts often.** Use a less frequent schedule for scripts that are not urgent.
- **Putting reboot commands or passwords in remediation scripts.** Do not.
- **Treating the runbooks as official procedures.** They are templates that you adapt and test.
- **Applying Flex update behavior to Enterprise.** The automatic power-on and deallocation points are for Flex Dedicated mode.

## How to validate this in your environment

Use a test Cloud PC and a test user.

1. In the Intune admin center, open **Tenant administration** and check that **Cloud PC maintenance windows (preview)** exists. If you create a test window, confirm the end time is at least two hours after the start time.
2. Start a bulk resize on one test Cloud PC with **Use Cloud PC maintenance windows** selected, then repeat without it. With the box selected the action runs in the maintenance window. Without it the action runs at once.
3. Open the provisioning policy's **Devices** tab and the **Action Status** tab, and confirm you can follow a bulk action.
4. Go to **Devices** > **Manage devices** > **Scripts and remediations** and check that the built-in packages are listed. Assign one to a small test group and look at **Device status** on the package.
5. Check the update ring policies that target Cloud PCs for automatic install and automatic restart.
6. Walk one test Cloud PC through steps 1 to 4 of the ladder. Step 4 rolls the test Cloud PC back and replaces any existing manual restore point. Do not run step 5 on a Cloud PC whose data you need.
7. Put the cadence table into your team calendar and name two reviewers for the daily review.

## Sources

- [Windows 365 operations guide](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-operations-guide)
- [Cloud PC maintenance windows (preview)](https://learn.microsoft.com/en-us/windows-365/enterprise/cloud-pc-maintenance-windows)
- [Remediations](https://learn.microsoft.com/en-us/mem/intune/fundamentals/remediations)
