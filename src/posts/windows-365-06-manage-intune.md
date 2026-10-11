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

Choose a harmless setting that you can read inside the Cloud PC. Create an Intune settings catalog profile, assign it to the small Cloud PC device group, and record the desired value. Wait for the device to check in, inspect the profile's device status, then open the Cloud PC and read the effective setting. Record **assigned**, **reported** and **observed** as three separate columns.

My [sanitized Edge setting capture](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-05-2026-09-24-edge-settings.jpg) records a setting observed on the Enterprise pilot. Consult the [configuration use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-05-configuration-management.md) for its limited evidence scope. The image alone does not establish every policy assignment step.

![Observed Edge setting on the pilot Cloud PC](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-05-2026-09-24-edge-settings.jpg)

## Lab B: an application

Select an approved test application and decide whether it should be **Required** or **Available**. Assign it to the pilot group. In Intune, read the installation status; in the Cloud PC, check the installed application or Company Portal view and launch it. If the app is Available, have the user initiate installation and capture that event. Record a failed installation separately from a missing assignment.

The [Company Portal screenshot](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg) in my repository shows an installed view. It does not prove a new Available assignment or uninstall. The [application use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-07-application-lifecycle.md) retains that distinction.

![Installed application view in Company Portal](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg)

## Lab C: updates

Choose a small update ring pilot and confirm the Cloud PC is in its target group. Record the assigned policy, device reporting, Windows Update status and any restart requirement. Avoid asserting that a feature update completed merely because a ring was created. Coordinate restarts with the test user and document the before and after OS build when an update is the claim.

Use Microsoft's [Windows 365 management guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management) to check current Intune options. The [engineering use cases](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/use-cases) provide the project-specific records. In your evidence log, preserve a failure with its timestamp rather than replacing it with a later success screenshot without explanation.

Next: [secure access and plan recovery](/windows-365/security-recovery/).

### Microsoft Learn

- [Intune as the management plane for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-management)
- [Security overview](https://learn.microsoft.com/en-us/windows-365/enterprise/security-guidelines)
