---
title: "Windows 365 Enterprise: Secure Access and Plan Recovery"
layout: post.njk
permalink: /windows-365/security-recovery/
order: 207
part: 7
tags: w365-series
deck: "A safe sequence for Conditional Access, device security and Cloud PC recovery decisions."
---

Security controls need a test plan because a policy can block the administrator and the pilot user at the same time. Use a small group, preserve an emergency access path under your organization's policy, and compare sign-in logs with the intended rule before enforcement.

## Conditional Access lab

1. Define the exact users, cloud apps and condition you intend to test. Read Microsoft's [Windows 365 Conditional Access guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/set-conditional-access-policies) for the relevant service apps.
2. Exclude the organization's designated emergency access accounts according to its established process. Start a new policy in **report-only** mode and target the pilot group.
3. Have the pilot user perform an ordinary sign-in and inspect the Microsoft Entra sign-in log's report-only result. Check both an expected allowed and an expected challenged scenario when the design calls for it.
4. Review the impact with the identity owner before enabling the policy. After enforcement, test a real session and record the result.

A report-only prediction is evidence about the proposed rule, not proof that enforcement worked. Likewise, a configured compliance policy is not proof that the Cloud PC is compliant. Check the device's actual compliance state and the sign-in decision independently. Microsoft's [security overview](https://learn.microsoft.com/en-us/windows-365/enterprise/security-guidelines) covers Defender, compliance and endpoint controls.

My October 6 record contains three resource simulations and one gateway sign-in with a sanitized report-only result. The screenshot below shows that report-only evaluation. It does **not** demonstrate a user being blocked by an enforced rule. Read the [validation record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-09-2026-10-06-conditional-access-validation.md) before drawing a broader conclusion.

![Sanitized Conditional Access report-only result](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-09-2026-10-06-report-only-result.jpg)

## Inspect device security separately

Open the Cloud PC in Intune and check its compliance rule results. Then connect to the device and compare Windows Security's firewall, Defender and real-time protection views. A local security screen and a compliance decision have different meanings; note both. My September 24 captures show the displayed device security and protection states, while the [device security check](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-06-2026-09-24-device-security-check.md) identifies policy freshness and other open checks.

![Intune compliance view in the pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-06-2026-09-24-compliance.jpg)

![Windows Security firewall view on the Cloud PC](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-06-2026-09-24-device-firewall.jpg)

![Windows Security real-time protection view on the Cloud PC](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-06-2026-09-24-real-time-protection.jpg)

## Choose the least disruptive support action

| Action | Before you use it |
| --- | --- |
| Disconnect and reconnect | Capture the error and test user connectivity. |
| Restart | Warn the user and save work; check whether the session returns. |
| Restore | Inspect available restore points and the data impact; agree on the chosen point. |
| Resize | Confirm the licensing path, target size and user impact. |
| Reprovision | Treat as a rebuild and plan for data and application consequences. |

Read [restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview), [resize guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/resize-cloud-pc) and [reprovision guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/reprovision-cloud-pc) before taking these actions. Preserve user data through the organization's approved storage and backup practices. Never experiment with reset or reprovision on the only working demonstration Cloud PC.

The [security](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-09-conditional-access.md) and [lifecycle](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-10-cloud-pc-lifecycle-operations.md) use cases in my repository are procedures with explicitly limited live validation. A sanitized report-only result was recorded, but there is no evidence of an enforced Conditional Access block or a completed restore.

A controlled restart and reconnect were observed on October 7; that is a narrower result than a restore. The [restart record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-10-2026-10-07-controlled-restart.md) describes what was checked and what still needs a post-action report.

Next: [read the ANC failure as a troubleshooting case](/windows-365/anc-troubleshooting/).

### Microsoft Learn

- [Set Conditional Access policies for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/set-conditional-access-policies)
- [Restore overview](https://learn.microsoft.com/en-us/windows-365/enterprise/restore-overview)
- [Reprovision a Cloud PC](https://learn.microsoft.com/en-us/windows-365/enterprise/reprovision-cloud-pc)
