---
title: "Windows 365 Enterprise: Manage Settings, Apps and Updates"
layout: post.njk
permalink: /windows-365/manage-intune/
order: 206
part: 6
tags: w365-series
deck: "A three-step Intune lab that checks assignment, device reporting and the visible result inside the Cloud PC."
---

After the Cloud PC works, manage it like a Windows endpoint through Microsoft Intune. Test one change at a time. This makes a mismatch between the Intune report and the desktop easier to diagnose.

## Lab A: a visible setting

1. Open **Devices > Configuration** in Intune and select the pilot settings catalog profile. Record the target group and configured Edge setting.
2. Open **Device status**. Find the pilot Cloud PC and record the status and last check-in. A success result in a report is a service-side result.
3. Connect to the Cloud PC, open Edge's relevant policy or settings view, and compare the effective value. If it differs, record both values and the time instead of declaring success.

This is the sanitized Intune report from my September 24 pilot. It is paired with the device-side Edge capture below; check the [dated follow-up](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-05-2026-10-04-edge-policy-review.md) for the limits of the comparison.

![Intune Edge profile report on the Enterprise pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-05-2026-09-24-edge-report.jpg)

My [sanitized Edge setting capture](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-05-2026-09-24-edge-settings.jpg) records a setting observed on the Enterprise pilot. Consult the [configuration use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-05-configuration-management.md) for its limited evidence scope. The image alone does not establish every policy assignment step.

![Observed Edge setting on the pilot Cloud PC](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-05-2026-09-24-edge-settings.jpg)

## Lab B: an application

1. In **Apps > All apps**, choose an approved app and inspect its assignments. Distinguish **Required** from **Available for enrolled devices** before describing user choice.
2. Open the application's device or user installation status and find the Cloud PC. In my pilot, two **Required** applications appeared in the Intune status view.
3. Inside the Cloud PC, open Company Portal, inspect the catalog and **Installed** view, then launch the app you intend to test. Record the result of each action separately.

![Intune application installation status from my pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-app-status.jpg)

The Company Portal catalog was empty in this captured session. That does not imply Company Portal was broken: Required apps can be installed without appearing as user-initiated Available apps.

![Company Portal catalog in the pilot session](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-catalog.jpg)

The [Company Portal screenshot](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg) in my repository shows an installed view. It does not prove a new Available assignment or uninstall. The [application use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-07-application-lifecycle.md) retains that distinction.

![Installed application view in Company Portal](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg)

An app launch view was also captured, but a full Available assignment and controlled uninstall were not. See the [Company Portal lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-07-2026-09-24-company-portal-check.md).

![Application launched from the pilot Company Portal session](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-launch.jpg)

## Lab C: updates

1. Review the update ring and its pilot assignment in Intune. Record its settings and device reporting.
2. In the Cloud PC, open **Settings > Windows Update > Update history** and record the installed updates, build and time.
3. Compare the two views. Coordinate a restart before it occurs; capture before and after builds if claiming that an update completed during the test.

This screenshot establishes the installed update history visible on September 24. The [October 6 ring review](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-08-2026-10-06-update-ring-review.md) does not demonstrate a controlled ring deployment and restart.

![Windows Update history on the Enterprise pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-08-2026-09-24-update-history.jpg)

Use Microsoft's [Windows 365 management guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management) to check current Intune options. The [engineering use cases](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/use-cases) provide the project-specific records. In your evidence log, preserve a failure with its timestamp rather than replacing it with a later success screenshot without explanation.

Next: [secure access and plan recovery](/windows-365/security-recovery/).

### Microsoft Learn

- [Intune as the management plane for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management)
- [Security overview](https://learn.microsoft.com/en-us/windows-365/enterprise/security-guidelines)
