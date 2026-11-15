---
title: "Windows 365 Enterprise: Manage Settings, Apps, Updates and Restart"
seoTitle: "Windows 365: Manage Settings, Apps and Updates"
layout: post.njk
permalink: /windows-365/manage-intune/
order: 206
part: 6
tags: w365-series
deck: "Four practical management checks: settings, apps, updates and a controlled restart, with evidence limits."
---

After the Cloud PC works, manage it like any other Windows device through Microsoft Intune. Enterprise Cloud PCs are covered in [Start here](/windows-365/start-here/). Test one change at a time (judgement). This makes a mismatch between the Intune report and the desktop easier to diagnose.

## Before you run the labs

Use one assigned Enterprise Cloud PC and a pilot group (a small group of test users). Record the Cloud PC name and the test account in a private lab log. Remove tenant IDs, user names and other private data before you share screenshots. For each change, save the assignment, the Intune status with time, and the device-side result with time. These are three different checks; a green status in an Intune report alone does not prove the user sees the intended result (judgement).

Terms used in this post:

- **Settings catalog:** an Intune profile type that lets you pick individual Windows and Edge settings.
- **Required app:** Intune installs it on the targeted devices. **Available app:** the user chooses to install it in Company Portal.
- **Company Portal:** the Intune app where users see and install company apps. See [Start here](/windows-365/start-here/).
- **Update ring:** an Intune policy that sets when and how Windows updates install.
- **Check-in:** the time the device last contacted Intune.
- **KB:** the number of a Windows update, such as KB5xxxxxx.
- **Remote action:** a command an admin sends to the Cloud PC from Intune.
- **Cloud PC actions report:** the Intune report of actions admins have taken on Cloud PCs.

| Lab | Admin-side check | Cloud PC check | Existing pilot evidence |
| --- | --- | --- | --- |
| A: Edge setting | Settings catalog assignment and device report | Effective Edge setting | Intune report captured September 24; Edge policy page checked October 6 and 7. The home page URL matched, but no startup-action policy appeared in Edge's list. |
| B: application | Required app installation status | Company Portal Installed view and app launch | Required app status and app launch views captured; an Available assignment and uninstall were not tested. |
| C: updates | Ring assignment and reporting | Windows Update history and build | Update history captured; a controlled ring rollout and restart were not demonstrated. |
| D: restart | Action status and later Intune check-in | Reconnect, desktop and Edge policy | Restart and reconnect passed on October 7; Intune action report and new check-in were not captured. |

The steps below let a reader repeat each lab. The status in the last column describes only my existing pilot evidence.

## Lab A: a visible setting

1. Open **Devices > Configuration** in Intune and select the pilot settings catalog profile. Record the target group and configured Edge setting.
2. Open **Device status**. Find the pilot Cloud PC and record the status and last check-in (the last time the device contacted Intune). A success result in a report is a service-side result.
3. Connect to the Cloud PC, open Edge's policy or settings view (type `edge://policy` in Edge; see [Configure Microsoft Edge policy settings on Windows devices](https://learn.microsoft.com/deployedge/configure-microsoft-edge#3-test-your-policies)), and compare the effective value. If it differs, record both values and the time instead of declaring success.

This is the sanitized Intune report from my September 24 pilot. It is paired with the device-side Edge capture below; the [dated follow-up](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-05-2026-10-04-edge-policy-review.md) records what was and was not matched. In that record, the profile's **Configure the home page URL** setting (`HomepageLocation`) matched the value Edge showed in `edge://policy`. Intune reported success for a startup-action setting as well, but no startup-action policy appeared in Edge's effective list, so only the home page value is confirmed on the device.

![Intune Edge profile report on the Enterprise pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-05-2026-09-24-edge-report.jpg)

My [sanitized Edge setting capture](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-05-2026-09-24-edge-settings.jpg) records a setting observed on the Enterprise pilot. Consult the [configuration use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-05-configuration-management.md) for its limited evidence scope. The image alone does not establish every policy assignment step.

![Observed Edge setting on the pilot Cloud PC](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-05-2026-09-24-edge-settings.jpg)

## Lab B: an application

1. In **Apps > All apps**, choose an approved app and inspect its assignments. Distinguish **Required** from **Available for enrolled devices** before describing user choice.
2. Open the application's device or user installation status and find the Cloud PC. In my pilot, the Intune status view and Company Portal's **Installed** list showed Company Portal and Microsoft Whiteboard as **Required** and installed.
3. Inside the Cloud PC, open Company Portal, inspect the catalog and **Installed** view, then launch the app you intend to test. Record the result of each action separately.

![Intune application installation status from my pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-app-status.jpg)

The Company Portal catalog was empty in this captured session. That does not imply Company Portal was broken: Required apps can be installed without appearing as user-initiated Available apps (judgement; I did not confirm this in Learn for this tenant, so check the app's assignment list first).

![Company Portal catalog in the pilot session](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-catalog.jpg)

The [Company Portal screenshot](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg) in my repository shows an installed view. It does not prove a new Available assignment or uninstall. The [application use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-07-application-lifecycle.md) retains that distinction.

![Installed application view in Company Portal](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg)

An app launch view was also captured (Microsoft Whiteboard opened, but its own banner said it was unable to save, so I do not call the app fully working), and a full Available assignment and controlled uninstall were not. See the [Company Portal lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-07-2026-09-24-company-portal-check.md).

![Application launched from the pilot Company Portal session](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-launch.jpg)

## Lab C: updates

1. In Intune, open **Devices > By platform > Windows > Manage updates > Windows updates > Update rings**. Select the pilot ring and record its settings, its assignment and the **Device and user check-in status** report. Microsoft lists update rings as a way to keep Cloud PCs patched ([Security overview](https://learn.microsoft.com/en-us/windows-365/enterprise/security-guidelines)). Assign rings to device groups, because then no user sign-in is needed ([Manage Windows update rings](https://learn.microsoft.com/en-us/intune/device-updates/windows/manage-update-rings)).
2. In the Cloud PC, open **Settings > Windows Update > Update history** and record the installed updates, build and time.
3. Check that the updates and build in Update history fit the ring settings. If a restart is planned, tell the user first and note the build before and after. Be careful with the ring's **Pause** and **Uninstall** actions: they take effect at once, and an uninstall can restart a device without letting the user delay it.

This screenshot establishes the installed update history visible on September 24. The [October 6 ring review](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-08-2026-10-06-update-ring-review.md) does not demonstrate a controlled ring deployment and restart.

![Windows Update history on the Enterprise pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-08-2026-09-24-update-history.jpg)

## Lab D: controlled restart and remote actions

A remote action can interrupt a user's work. Read the action's impact before selecting it. In this pilot, only **Restart** was tested. Resize, Move, Restore and Reprovision are separate lifecycle tests, not a completed part of this lab. The [lifecycle decision guide](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-10-cloud-pc-lifecycle-operations.md) includes a diagram and explains the data impact of each choice.

1. Ask the user to save work. Confirm the Cloud PC, its owner and the intended action. Record the starting state and time.
2. Start the restart. My test used the user route; the admin route is listed for comparison. Admin route: in the Intune admin center, select **Devices > All devices**, select the Cloud PC, then select **Restart**. The exact menu depends on your role and the device state. User route: in Windows App, open **Devices**, select the ellipsis (...) on the Cloud PC card, select **Restart**, then confirm ([Windows App device actions](https://learn.microsoft.com/en-us/windows-app/device-actions#restart)). The web client at [windows.cloud.microsoft](https://windows.cloud.microsoft/) offers the same action; menu names can differ.
3. Watch for the restart state. Wait until **Connect** returns. Open a fresh session and check sign-in, desktop and the setting or app that matters to the user.
4. In Intune, review **Devices > Monitor > Cloud PC actions** and the device's last check-in when those views are available. Record their time separately from the user reconnect. The **Cloud PC actions** report lists actions that admins take; Learn does not say that a restart the user starts in Windows App appears there, so use the admin route if you need a report entry ([Cloud PC actions report](https://learn.microsoft.com/en-us/windows-365/enterprise/report-cloud-pc-actions)). The report shows the last 90 days. A browser reconnect by itself does not prove the Intune report or app health.

**Observed on October 7, 2026:** The existing Enterprise Cloud PC showed **Restarting**; the active session disconnected; **Connect** returned; a new web session reached the signed-in desktop. Edge's policy page still reported the `HomepageLocation` policy as OK, while Edge opened a New tab page and no startup-action policy appeared in the list. See the [dated restart record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-07-controlled-restart.md). That test did not capture the Cloud PC actions report, a new Intune check-in or post-restart app status, so the full management validation remains open. The restart was started in Windows App (**More options > Restart**), so it would not necessarily appear in the admin **Cloud PC actions** report. No screenshot of that restart sequence is published here.

**Do not test the other actions on your only working Cloud PC (judgement).** Restore returns the Cloud PC to an earlier point, and everything saved after that point is lost. Reprovision deletes the Cloud PC and creates a new one from the current provisioning policy, and all user data, apps and customizations are deleted. Neither can be undone. See [Point-in-time restore](/windows-365/point-in-time-restore/) and [Secure access and plan recovery](/windows-365/security-recovery/) for the details. A separate disposable device and a recorded recovery path are needed before those labs. See Microsoft's [remote management action reference](https://learn.microsoft.com/en-us/windows-365/enterprise/remotely-manage-cloud-pc).

## What counts as a completed test

- **Setting:** Match the exact configured Edge value to the effective value in the Cloud PC. Preserve both timestamps and the policy assignment. The screenshots here show a report and a setting; review the linked follow-up before calling the full change cycle proven.
- **Application:** Record the app's assignment type and target group, installation status, a successful launch and the time of each check. **Required** installs to its targeted devices; **Available for enrolled devices** lets the targeted user choose it in Company Portal, and the app appears only for the device's primary user. My pilot did not complete the Available or uninstall paths.
- **Update:** Record ring settings, target, reporting, installed KB number and build, restart and after-state. Update history by itself does not show which ring installed an update (judgement); Learn also notes that a rolled-back quality update still appears in Update history, so history is not proof of the current state. My pilot does not prove that full sequence.
- **Restart:** Record the starting state, the **Restarting** status, the reconnect time, the post-restart check of the setting or app, the Cloud PC actions report entry (admin route) and the next Intune check-in.

When a result differs, note the exact status, last check-in, error and time. Review assignment and device sync (select **Sync** on the device in Intune; see [Device action: sync](https://learn.microsoft.com/intune/device-management/actions/sync)) before changing the profile (judgement). Keep a failure in the log even if a later attempt works.

Microsoft's [management guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management) explains why Intune is the recommended management plane for Windows 365. It prefers Intune Win32 apps and Enterprise App Catalog apps for app delivery; the Catalog is included with Microsoft 365 E5, and other plans need separate licensing. For exact options, use the Intune pages listed below. The [engineering use cases](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/use-cases) provide the project-specific records.

Next: [secure access and plan recovery](/windows-365/security-recovery/).

### Microsoft Learn

- [Intune as the management plane for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management)
- [Assign apps to groups in Intune](https://learn.microsoft.com/en-us/intune/app-management/deployment/assign-groups)
- [Manage Windows update rings](https://learn.microsoft.com/en-us/intune/device-updates/windows/manage-update-rings)
- [Remotely manage Cloud PCs](https://learn.microsoft.com/en-us/windows-365/enterprise/remotely-manage-cloud-pc)
- [Cloud PC actions report](https://learn.microsoft.com/en-us/windows-365/enterprise/report-cloud-pc-actions)
- [Windows App device actions](https://learn.microsoft.com/en-us/windows-app/device-actions)
- [Security overview](https://learn.microsoft.com/en-us/windows-365/enterprise/security-guidelines)
