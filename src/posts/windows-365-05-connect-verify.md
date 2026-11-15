---
title: "Windows 365 Enterprise: Connect and Verify the Cloud PC"
seoTitle: "Windows 365: Connect and Verify a Cloud PC"
layout: post.njk
permalink: /windows-365/connect-verify/
order: 205
part: 5
tags: w365-series
deck: "Test the user session, Microsoft Entra join and Intune enrollment as separate checkpoints."
---

The portal's **Provisioned** status is an important milestone, but the pilot is not finished until the assigned user can use the desktop. A pilot here means a small first deployment with one or a few test users. A connection test and a management test answer different questions. Record both.

There are two ways to connect to a Cloud PC. **Windows App** is Microsoft's app for connecting to a Cloud PC. The **web client** is the same kind of connection in a browser, at windows.cloud.microsoft. The next sections use these two names.

## User connection test

1. Ask the assigned user to open [windows.cloud.microsoft](https://windows.cloud.microsoft/) and sign in with the account that received the Enterprise license.
2. Confirm the expected Cloud PC card (the tile under **Your Cloud PCs**) appears. Record its displayed state and the connection method (web client or Windows App; see the next section). A tile is an assignment check, not a successful desktop test.
3. Select **Open in browser**, then select **Connect** in the **In Session Settings** window. Complete the Windows sign-in, and open a basic application. Record whether the desktop is responsive. Keep the user name and tenant details out of a public capture.
4. Disconnect, return to the portal and reconnect. Record the browser or Windows App version and the result. A reconnect test detects a problem the initial tile cannot show.

If the Cloud PC does not appear, recheck license, group and provisioning status. If it appears but cannot connect, capture the full connection error and test again after checking the [Windows 365 troubleshooting guide](https://learn.microsoft.com/en-us/windows-365/enterprise/troubleshooting). Do not reset or reprovision a working pilot just to clear an unexplained error.

## Choose a supported connection method

The current [Microsoft access guide](https://learn.microsoft.com/en-us/windows-365/end-user-access-cloud-pc) lists Windows App and the [Windows 365 web client](https://windows.cloud.microsoft/) as the current connection methods for Enterprise Cloud PCs. Microsoft Remote Desktop is the older app; its support ended in March 2026. Windows App is available on Windows, macOS, iOS/iPadOS and Android/ChromeOS; its features differ by platform. The web client is for a supported browser on a desktop or laptop, not a mobile browser. Review the [platform comparison](https://learn.microsoft.com/en-us/windows-app/compare-platforms-features) before promising a feature on every client. The classic Remote Desktop Connection tool (mstsc.exe) is not a supported connection method. Microsoft says it may work for troubleshooting, but it should not be used for daily access.

| Pilot device | Reader action | What this article proves |
| --- | --- | --- |
| Desktop or laptop browser | Sign in at [windows.cloud.microsoft](https://windows.cloud.microsoft/), select the assigned Cloud PC and open it in the browser. | The existing Enterprise pilot reached an interactive web desktop on October 12, 2026. |
| Windows or macOS with Windows App | Install Windows App from the official platform source, sign in with the assigned work account and select the Cloud PC. | Steps only. A native Windows or macOS app session was not tested in this lab. |
| iOS/iPadOS or Android/ChromeOS with Windows App | Install the official Windows App, sign in with the work account and select the Cloud PC. | Steps only. No mobile client session was tested. |

Follow Microsoft's [Windows App connection walkthrough](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps?pivots=windows-365) for your platform. It supplies the current client requirements and screens. Use a work or school account assigned the Cloud PC. You cannot sign in to Windows App with a personal Microsoft account. The same Cloud PC can be tested by different supported connection methods, but record each method as a separate result.

### A small repeatable user test

1. Before connecting, record the device platform, browser or app version, work account (privately), Cloud PC tile and start time.
2. Connect. Confirm that the Windows desktop appears, open a harmless built-in app and record whether keyboard, mouse and display respond. Test a business app only if it is part of the pilot's agreed success criteria.
3. Disconnect using the client control, return to the Cloud PC card, then reconnect. Record the second result and time. If you did not perform this step, write **reconnect: untested** in your own test notes.
4. Repeat on another client only when you have that device. Note platform-specific prompts and features separately; do not use a web result as proof of a mobile or native app result.

**My evidence:** The [October 12 connection record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-10-12-enterprise-web-connection.md) confirms the browser client reached the desktop. It does not document a completed disconnect/reconnect or native app test. A sanitized desktop capture from a separate October 15 browser connection is published in this article (see the figure under the pilot connection heading). Disconnect/reconnect and native app tests remain unverified. A separate October 7 restart-and-reconnect result is described in [Manage settings, applications and updates](/windows-365/manage-intune/); it is not a client disconnect test.

### If the user cannot connect

First separate **no Cloud PC tile** from **tile visible but connection fails**. For the first, inspect assignment, license and provisioning. For the second, record the exact error and time, check the supported client and network, then use the **Troubleshoot** option (gear icon on the Cloud PC card at windows.cloud.microsoft) or the Windows App **Inspect Connection** option where offered. Microsoft's [connection error guide](https://learn.microsoft.com/en-us/troubleshoot/windows-365/connection-errors) explains these checks. For a pattern affecting many users, inspect the Intune [Cloud PC connection quality report](https://learn.microsoft.com/en-us/windows-365/enterprise/report-cloud-pc-connection-quality) (in the Intune admin center under **Reports > Cloud PC overview > Connection quality**). These are diagnostic paths, not results I measured in this pilot.

## Administrator verification

1. In the [Microsoft Intune admin center](https://intune.microsoft.com/), open **Devices > All Cloud PCs** (under **Manage Windows 365 Cloud PCs**) and inspect the expected user's Cloud PC. Record its status, policy and device name privately.
2. Open the matching device under **Devices > All devices**. Compare the primary user, Microsoft Entra join and last check-in (the last time the device contacted Intune). Microsoft Entra join means the Cloud PC is joined to Microsoft Entra ID only; Microsoft Entra hybrid join also joins it to on-premises Active Directory. The provisioning policy decides which. A stale management check-in needs investigation even if the session opens.
3. In Microsoft Entra, locate the device if you need to corroborate its identity and join. In the Cloud PC session, verify the signed-in account and one required application or destination.
4. Save a timestamped admin portal screenshot and a separate screenshot of the user's desktop. Add a one-sentence caption to each saying exactly what it proves.

| Checkpoint | What it establishes | What it does not establish |
| --- | --- | --- |
| Provisioned status | Windows 365 created the Cloud PC | User can open a usable session |
| Cloud PC tile | User can see an assigned resource | Desktop sign-in succeeds |
| Browser session | User can reach and use the desktop | Intune policies have applied |
| Intune device and check-in | Management record exists and reports | Every assigned setting is effective |

My existing Enterprise pilot was observed as provisioned, Microsoft Entra joined, enrolled in Intune (meaning Intune can manage it) and accessible by web. The [evidence repository](https://github.com/AddySidd27/Windows365-enterprise-engineering) (AddySidd27/Windows365-enterprise-engineering) holds my records; its [live validation status](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) gives the exact scope. There is no continuous screenshot sequence of a new license assignment through initial provisioning; that gap remains open.

The [September 24 portal check](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-09-24-portal-check.md) records the observed Cloud PC state, web session, Intune device and sanitized join output. For September 24, the public evidence is a dated text record, not a publishable screenshot of every portal screen. This article uses no simulated Windows 365 pages and no third-party images.

## Verified pilot connections on October 12 and October 15, 2026

In Intune, the existing Enterprise Cloud PC showed **Provisioned** in All Cloud PCs. Its Intune device record showed the compliance state **Compliant**, meaning it met the Intune compliance rules. That is what the Intune record reported; it is not evidence from the desktop session.

On October 12, I signed in at windows.cloud.microsoft (Windows App in a web browser) as the assigned pilot user, selected the Enterprise Cloud PC card and chose **Connect**. The web client progressed through **Connecting** to **Connected**, and the Windows desktop appeared. This confirms an interactive web session for the existing pilot.

The [dated connection lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-02-2026-10-12-enterprise-web-connection.md) separates the administrator and user observations. On October 15, I connected again to the existing Enterprise Cloud PC. The web client reached the desktop and reported **Connection quality is good**.

I collapsed the toolbar before taking this capture, so account and device identifiers are outside the image. The image shows the desktop and taskbar. It does not prove Intune compliance, a fresh provisioning cycle, a complete disconnect/reconnect, every application, or the Azure network connection path.

![Existing Enterprise Cloud PC desktop opened in the Windows 365 web client](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/windows365-enterprise-desktop-20261015.jpg?raw=true)

*Figure: Sanitized October 15 browser capture of the connected Enterprise Cloud PC desktop. The client toolbar was collapsed before capture so that account and device identifiers are not shown.*

## When one checkpoint fails

| Symptom | What to inspect next |
| --- | --- |
| No Cloud PC tile | License assignment, group membership, the provisioning policy's assigned group and provisioning status |
| Tile appears, desktop does not open | Exact connection error, user sign-in and client or browser |
| Desktop opens, Intune looks stale | Last check-in, network reachability and Intune enrollment state |
| Unexpected join type | Policy configuration and matching Entra device object |

Capture the exact error before restarting or taking a more disruptive action. A support ticket that names the failing checkpoint is easier to reproduce than one that says only “Cloud PC is broken.”

## Capture the outcome

Save a sanitized tile or provisioning status view, an authenticated desktop view, and the device management view. Record their timestamps and which pilot account each corresponds to without publishing the account identifier. A reader should be able to see why you called the user test and the management test successful.

Next: [manage settings, applications and updates](/windows-365/manage-intune/).

### Microsoft Learn

- [What is Windows 365 Enterprise?](https://learn.microsoft.com/en-us/windows-365/enterprise/overview)
- [Troubleshooting Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/troubleshooting)
- [Access a Cloud PC](https://learn.microsoft.com/en-us/windows-365/end-user-access-cloud-pc)
- [Connect with Windows App](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps?pivots=windows-365)
- [Compare Windows App platforms](https://learn.microsoft.com/en-us/windows-app/compare-platforms-features)
