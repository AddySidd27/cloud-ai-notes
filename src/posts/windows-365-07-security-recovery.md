---
title: "Windows 365 Enterprise: Secure Access and Plan Recovery"
seoTitle: "Windows 365: Secure Access and Plan Recovery"
layout: post.njk
permalink: /windows-365/security-recovery/
order: 207
part: 8
tags: w365-series
deck: "A safe sequence for Conditional Access, device security and Cloud PC recovery decisions."
---

Test security controls before you turn them on, because a policy can lock out the administrator and the pilot user at the same time. Use a small group, keep your emergency access accounts outside the policy, and compare sign-in logs with the rule you intended before you enforce it. (The log comparison step is my judgement.)

**Terms used here.** *Conditional Access* is a set of Microsoft Entra rules that decide who can sign in and under which conditions. *Report-only* mode logs what a rule would do, but does not block anyone. *Emergency access accounts* are special administrator accounts that Conditional Access never blocks, so you can still sign in if a policy locks everyone out; see Microsoft's [emergency access guidance](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access). The series glossary is in [Start here](/windows-365/start-here/).

## Conditional Access lab

1. Define the exact users, cloud apps and condition you intend to test. Read Microsoft's [Windows 365 Conditional Access guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/set-conditional-access-policies) and choose the apps: **Windows 365** (it may show as **Cloud PC**), **Azure Virtual Desktop** (it may show as **Windows Virtual Desktop**) and, if you use single sign-on, **Windows Cloud Login**. Microsoft recommends matching the policy across these apps. A policy on Windows 365 can also affect sign-in to the Azure portal, the Intune admin center and the Microsoft 365 admin center, so scope it with care.
2. Exclude your emergency access accounts. Report-only policies do not block anyone, but add the exclusion now so it is already in place when you enforce. Start a new policy in **report-only** mode and target the pilot group.
3. Have the pilot user perform an ordinary sign-in and inspect the report-only result for that sign-in (when you download sign-in logs, choose JSON format to include the report-only data). Check an expected allowed case and an expected controlled case. Report-only policies do not enforce interactive grant controls such as multifactor authentication, so for those sign-ins the Conditional Access insights and reporting workbook counts the result as **Report-only: User action required**: success or failure cannot be determined. See [Conditional Access insights and reporting](https://learn.microsoft.com/en-us/entra/identity/conditional-access/howto-conditional-access-insights-reporting).
4. Review the impact with the person who owns Microsoft Entra in your organization before enabling the policy. After enforcement, test a real session and record the result.

A report-only result shows what the rule would do. It does not show that enforcement works. Likewise, a compliance policy is the rule, and the compliance state is the result Intune records for each device. A configured policy does not mean the Cloud PC is compliant. Check the device's compliance state and the sign-in decision separately. Microsoft's [Security guidelines](https://learn.microsoft.com/en-us/windows-365/enterprise/security-guidelines) cover Defender, compliance and endpoint controls.

On October 6 I recorded three simulated resource sign-ins and one sign-in through the Azure Virtual Desktop Gateway (the service the client connects through), with a sanitized report-only result. "Sanitized" means private details were removed. The screenshot below shows that report-only result. It does **not** show a user being blocked by an enforced rule. I have not tested an enforced block yet. My [October 6 lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-09-2026-10-06-conditional-access-validation.md) has the details.

![Sanitized Conditional Access report-only result](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-09-2026-10-06-report-only-result.jpg)

*October 6: the sanitized report-only result from my pilot. It shows what the policy would do. It is not an enforced block.*

## Inspect device security separately

Open the Cloud PC in Intune and check the device's compliance status page. Then connect to the device and compare Windows Security's firewall, Defender and real-time protection views. A local security screen and a compliance decision mean different things, so note both. My September 24 screenshots show the device security and protection states. My [device security lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-06-2026-09-24-device-security-check.md) covers policy freshness (how recently the device received policy) and lists checks I have not finished.

![Intune compliance view in the pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-06-2026-09-24-compliance.jpg)

*September 24: the Intune compliance view for my pilot Cloud PC. It shows what Intune displayed that day.*

![Windows Security firewall view on the Cloud PC](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-06-2026-09-24-device-firewall.jpg)

*September 24: the Windows Security firewall view on the Cloud PC.*

![Windows Security real-time protection view on the Cloud PC](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-06-2026-09-24-real-time-protection.jpg)

*September 24: the Windows Security real-time protection view on the Cloud PC. None of the three screenshots shows compliance on its own.*

### Cloud PC policy exceptions to check

Microsoft's [Security guidelines](https://learn.microsoft.com/en-us/windows-365/enterprise/security-guidelines) state that Cloud PCs do not support BitLocker, and Microsoft recommends excluding that setting from compliance policies that target Cloud PCs. The same page says **Administrator protection** (a Windows feature that requires approval for admin tasks) is unsupported on Cloud PCs; use an Intune assignment filter (a rule that includes or excludes devices from a policy assignment) to exclude them from a policy that enables it.

Check this before applying a security baseline (a ready-made group of security settings) unchanged. The Security Compliance Toolkit baselines applied through Group Policy turn Administrator protection on from the October 2026 Windows security update. Microsoft's fix is to set **User Account Control: Configure type of Admin Approval Mode** to **Legacy Admin Approval Mode** and restart the Cloud PCs. These are design checks. I did not deploy these controls in my pilot.

## Choose the support action, from least to most disruptive

| Action | What it does | Before you use it |
| --- | --- | --- |
| Disconnect and reconnect | Ends the session and starts a new one. | Note the error and test user connectivity. (judgement) |
| Restart | Reboots the Cloud PC; no data loss. | Warn the user and save work; check whether the session returns. (judgement) |
| Restore | Returns the Cloud PC to an earlier saved point. | Inspect available restore points and the data impact; agree on the chosen point. |
| Resize | Changes the Cloud PC to a different size license. | Confirm the licensing path, target size and user impact. It disconnects the user, unsaved work can be lost, and it takes about 15 to 20 minutes. The disk cannot shrink and GPU Cloud PCs are not supported. With group-based licensing the Cloud PC waits up to 48 hours in **Resize pending license** until the old license is removed and the new one assigned. |
| Reset (end user) | Reinstalls the operating system on the same Cloud PC. | Treat as a wipe: data and settings are deleted. |
| Reprovision | Deletes the Cloud PC and builds a new one from the current provisioning policy. | Treat as a rebuild: all data, apps and customizations are deleted. The status must be **Failed** or **Provisioned**. |

Read [restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview), [resize overview](https://learn.microsoft.com/en-us/windows-365/enterprise/resize-cloud-pc) and [reprovision guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/reprovision-cloud-pc) before taking these actions. Keep user files in your organization's approved backup or file storage, for example OneDrive. Do not try reset or reprovision on your only working Cloud PC.

### Plan a point-in-time restore before you need one

A restore returns the Cloud PC to an earlier point and loses later local changes. The administrator can set the short-term interval (4, 6, 12, 16 or 24 hours); the long-term points are not configurable. Choose the most recent healthy point, tell the user which period of changes will be lost, and check sign-in afterwards. The [Point-in-Time Restore chapter](/windows-365/point-in-time-restore/) covers the point types, data impact and credential risks. Microsoft's [restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview) is the source.

## What I tested

I have not restored my Enterprise Cloud PC. On 16 October 2026 I listed its restore points and created a manual point (see [Point-in-Time Restore](/windows-365/point-in-time-restore/)). On October 7 I restarted it and reconnected, which is a smaller test than a restore. My [restart lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-07-controlled-restart.md) says what I checked and what I did not.

The [Conditional Access](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-09-conditional-access.md) and [lifecycle](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-10-cloud-pc-lifecycle-operations.md) records in my repository are mostly procedures. My live testing was limited. I recorded a sanitized report-only result. I have not tested an enforced Conditional Access block or a restore yet.

Next: [read the ANC failure as a troubleshooting case](/windows-365/anc-troubleshooting/).

### Microsoft Learn

- [Set Conditional Access policies for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/set-conditional-access-policies)
- [Security guidelines](https://learn.microsoft.com/en-us/windows-365/enterprise/security-guidelines)
- [Manage emergency access accounts in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access)
- [Conditional Access insights and reporting](https://learn.microsoft.com/en-us/entra/identity/conditional-access/howto-conditional-access-insights-reporting)
- [Restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview)
- [Resize overview](https://learn.microsoft.com/en-us/windows-365/enterprise/resize-cloud-pc)
- [Reprovision a Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/reprovision-cloud-pc)
