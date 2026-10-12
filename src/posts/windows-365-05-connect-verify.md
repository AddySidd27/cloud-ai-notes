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

1. Ask the assigned user to open [windows365.microsoft.com](https://windows365.microsoft.com/) and sign in with the account that received the Enterprise license.
2. Confirm the expected Cloud PC tile appears. Record its displayed state and the connection method. A tile is an assignment check, not a successful desktop test.
3. Select **Open in browser**, complete the Windows sign-in, and open a basic application. Record whether the desktop is responsive. Keep the user name and tenant details out of a public capture.
4. Disconnect, return to the portal and reconnect. Record the browser or Windows App version and the result. A reconnect test detects a problem the initial tile cannot show.

If the Cloud PC does not appear, recheck license, group and provisioning status. If it appears but cannot connect, capture the full connection error and test again after checking the [Windows 365 troubleshooting guide](https://learn.microsoft.com/en-us/windows-365/enterprise/troubleshooting). Do not reset or reprovision a working pilot just to clear an unexplained error.

## Administrator verification

1. In Intune, open **Devices > Provision Cloud PCs > All Cloud PCs** and inspect the expected user's Cloud PC. Record its status, policy and device name privately.
2. Open the matching device under **Devices > All devices**. Compare the primary user, Microsoft Entra join and last check-in. A stale management check-in needs investigation even if the session opens.
3. In Microsoft Entra, locate the device if you need to corroborate its identity and join. In the Cloud PC session, verify the signed-in account and one required application or destination.
4. Save a timestamped service-side view and a separate user-side view. Add a one-sentence caption to each saying exactly what it proves.

| Checkpoint | What it establishes | What it does not establish |
| --- | --- | --- |
| Provisioned status | Windows 365 created the Cloud PC | User can open a usable session |
| Cloud PC tile | User can see an assigned resource | Desktop sign-in succeeds |
| Browser session | User can reach and use the desktop | Intune policies have applied |
| Intune device and check-in | Management record exists and reports | Every assigned setting is effective |

My existing Enterprise pilot was observed as provisioned, Microsoft Entra joined, enrolled in Intune and accessible by web. The repository's [live validation status](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) gives the exact scope. There is no continuous screenshot sequence of a new license assignment through initial provisioning; that gap remains open.

The [September 24 portal check](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-09-24-portal-check.md) records the observed Cloud PC state, web session, Intune device and sanitized join output. Its public evidence is a dated text record, not a publishable screenshot of every portal screen. I have not filled the gap with a simulated Windows 365 page or another writer's image.

## When one checkpoint fails

| Symptom | What to inspect next |
| --- | --- |
| No Cloud PC tile | License assignment, group membership, policy target and provisioning status |
| Tile appears, desktop does not open | Exact connection error, user sign-in and client or browser |
| Desktop opens, Intune looks stale | Last check-in, network reachability and enrollment state |
| Unexpected join type | Policy configuration and matching Entra device object |

Capture the exact error before restarting or taking a more disruptive action. A support ticket that names the failing checkpoint is easier to reproduce than one that says only “Cloud PC is broken.”

## Capture the outcome

Save a sanitized tile or provisioning status view, an authenticated desktop view, and the device management view. Record their timestamps and which pilot account each corresponds to without publishing the account identifier. A reader should be able to see why you called the user test and the management test successful.

Next: [manage settings, applications and updates](/windows-365/manage-intune/).

### Microsoft Learn

- [What is Windows 365 Enterprise?](https://learn.microsoft.com/en-us/windows-365/enterprise/overview)
- [Troubleshooting Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/troubleshooting)
