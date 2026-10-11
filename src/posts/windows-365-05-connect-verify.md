---
title: "Windows 365 Enterprise: Connect and Verify the Cloud PC"
layout: post.njk
permalink: /windows-365/connect-verify/
order: 205
part: 5
tags: w365-series
deck: "Test the user session, Microsoft Entra join and Intune enrollment as separate checkpoints."
---

The portal's **Provisioned** status is an important milestone, but the pilot is not finished until the assigned user can use the desktop. A connection test and a management test answer different questions. Record both.

## User connection test

Ask the assigned user to open [windows365.microsoft.com](https://windows365.microsoft.com/) and sign in with the account that received the Enterprise license. Confirm that the expected Cloud PC appears. Start the browser session, complete sign-in, open a basic application, disconnect and reconnect. Note the client or browser used and the date. A session that reconnects is stronger evidence than a Cloud PC tile alone.

If the Cloud PC does not appear, recheck license, group and provisioning status. If it appears but cannot connect, capture the full connection error and test again after checking the [Windows 365 troubleshooting guide](https://learn.microsoft.com/en-us/windows-365/enterprise/troubleshooting). Do not reset or reprovision a working pilot just to clear an unexplained error.

## Administrator verification

In Intune, compare the Cloud PC entry with the intended user, provisioning policy, join type and device enrollment. Check the device's recent check-in separately from provisioning status. In Microsoft Entra, check the device identity if you need to verify the join. Inside the session, confirm the signed-in account and the expected network or application reachability.

| Checkpoint | What it establishes | What it does not establish |
| --- | --- | --- |
| Provisioned status | Windows 365 created the Cloud PC | User can open a usable session |
| Cloud PC tile | User can see an assigned resource | Desktop sign-in succeeds |
| Browser session | User can reach and use the desktop | Intune policies have applied |
| Intune device and check-in | Management record exists and reports | Every assigned setting is effective |

My existing Enterprise pilot was observed as provisioned, Microsoft Entra joined, enrolled in Intune and accessible by web. The repository's [live validation status](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) gives the exact scope. There is no continuous screenshot sequence of a new license assignment through initial provisioning; that gap remains open.

## Capture the outcome

Save a sanitized tile or provisioning status view, an authenticated desktop view, and the device management view. Record their timestamps and which pilot account each corresponds to without publishing the account identifier. A reader should be able to see why you called the user test and the management test successful.

Next: [manage settings, applications and updates](/windows-365/manage-intune/).

### Microsoft Learn

- [What is Windows 365 Enterprise?](https://learn.microsoft.com/en-us/windows-365/enterprise/overview)
- [Troubleshooting Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/troubleshooting)
