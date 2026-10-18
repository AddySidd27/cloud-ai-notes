---
title: "Choose the Client: Windows App, Remote Desktop and the Web"
layout: post.njk
permalink: "/azure-virtual-desktop/choose-the-avd-client/"
order: 112
part: 12
tags: [avd-series]
deck: "Match user devices to the supported client, understand what the retirement of the older Remote Desktop clients means and plan a client change."
description: "Choose the right client for Azure Virtual Desktop: Windows App, the older Remote Desktop clients, the browser, feature gaps and how to plan a migration."
---

The client is the one part of the service your users touch. It is also the part that changes most often and is least under your control, because it runs on devices you may not manage. Most AVD designs spend pages on session hosts and a sentence on the client. That is a risk (the author's judgement), because a client that is out of support is no longer covered by support, and a whole group of users may depend on it.

This article lists the clients the documentation names, what has changed about them, the feature gaps that matter for design, and how to plan a move from an older client.

## Key terms

| Term | Meaning |
|---|---|
| Client | The app on the user's device that signs in, shows the feed and opens the remote session. |
| Windows App | Microsoft's current client for Azure Virtual Desktop, Windows 365, Microsoft Dev Box, Remote Desktop Services and remote PCs. |
| Remote Desktop client | The older family of clients. The documentation says Windows App replaces it. |
| MSI client | The Remote Desktop client for Windows, installed from a standalone installer. |
| Store app | The Remote Desktop app for Windows, once available from the Microsoft Store. |
| Web client | A client that runs in a browser, with nothing to install on a desktop or laptop. |
| Redirection | Passing a local device or feature, such as a printer, camera or clipboard, into the remote session. |
| RDP Shortpath | An optional direct UDP path between the client and the session host. The [connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/) explains it. |
| Teams media optimizations | An optimized Microsoft Teams calling and meeting experience inside a remote session. |
| WebAuthn redirection | Passes sign-in requests made inside the remote session to the local device, so security keys and Windows Hello for Business can be used. |
| Private Link | A way to connect a remote session over a private connection. |
| Microsoft Intune | Microsoft's cloud service for managing devices with policies. |
| Public cloud, Azure Government, Azure operated by 21Vianet | Azure for US Government and Azure operated by 21Vianet (in China) are sovereign clouds, separate from the public cloud. |
| AVD Classic | The older, non-Azure Resource Manager version of the service. The [fit article](/azure-virtual-desktop/decide-whether-azure-virtual-desktop-fits/) covers its retirement. |
| Feed | The list of desktops and apps a user may open. |

## The clients and where they stand

The documentation describes Windows App as the new way to connect to cloud and remote resources, and says it replaces the Remote Desktop client. These facts are from the documentation at the time of checking, and they have dates in them, so check the pages before you rely on them.

| Client | Platforms | Status in the documentation |
|---|---|---|
| Windows App | Windows, macOS, iOS and iPadOS, Android and Chrome OS, web browsers, Meta Quest | The current client. Sign-in needs a work or school account. A personal Microsoft account does not work. The overview lists Meta Quest as a platform, but the get-started page labels Meta Quest as preview, so treat it as preview. |
| Remote Desktop client for Windows (MSI) | Windows | No longer supported for public cloud customers from March 27, 2026. Support was extended to September 28, 2026 for Azure Government, Azure operated by 21Vianet and AVD Classic. That date has passed at the time of writing, so check the page for the current position. |
| Remote Desktop app for Windows (Store) | Windows | No longer supported and no longer available to install. Support ended September 2025. |
| Remote Desktop clients for macOS and iOS/iPadOS | macOS, iOS, iPadOS | Not available to download. Replaced by Windows App. |
| Remote Desktop client for Android and Chrome OS | Android, Chrome OS | Listed as available from Google Play. |
| Remote Desktop web client | Browser | No longer supported for public cloud customers from March 27, 2026. No end-of-support date is announced for Azure Government or Azure operated by 21Vianet. |

Two clients are not supported for AVD at all: the RemoteApp and Desktop Connections client, and the Remote Desktop Connection client (`mstsc.exe`). This comes from the prerequisites page for AVD, not from the client overview.

![A table-like drawing with three columns: device, client, and what to watch for. Windows PC, macOS, iPhone and iPad, Android and Chrome OS, and Meta Quest all point to Windows App. Web browser points to Windows App in the browser. Notes beside each row say what to watch for: the Windows row gives the retirement dates of the older Remote Desktop clients for Windows, and the Meta Quest row says one page labels it preview. A red box at the bottom says the RemoteApp and Desktop Connections client and the Remote Desktop Connection client are not supported for Azure Virtual Desktop.](/img/avd/AVD-Post-12-Client-By-Device.png)

*Drawn by the author from [Remote Desktop client overview](https://learn.microsoft.com/en-us/azure/virtual-desktop/users/remote-desktop-clients-overview), the statement about unsupported clients in [Prerequisites for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites), [What is Windows App?](https://learn.microsoft.com/en-us/windows-app/overview) and [Get started with Windows App](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps). Not an official Microsoft diagram. The documentation has a status table, not a diagram, so the layout is the author's. The drawing leaves out the Remote Desktop Services and remote PC columns, and feature differences between clients.*

**Recommendation (judgement):** standardize on Windows App for every platform you support, and treat any user still on an older client as a migration item with a date.

## What each choice changes

Documented facts first.

- **Windows App needs a work or school sign-in.** You cannot sign in with a personal Microsoft account. For AVD, Windows 365, Dev Box and Remote Desktop Services you must sign in. For remote PC connections on supported platforms you can use Windows App without signing in.
- **In a browser, nothing is installed.** The documentation describes this for desktops and laptops. It is the lowest-effort option for a device you do not manage.
- **Windows App on Windows connects to AVD but not to Remote Desktop Services.** For Remote Desktop Services on Windows, the documentation says to keep using the Remote Desktop app on Windows. If you have both services, plan for two clients on Windows.
- **Features differ by platform.** The next section gives examples.

Judgement: a browser is a good fallback for contractors and kiosks. It is a poor primary client if users need local devices, several monitors or heavy media. The feature table below is the reason.

## Feature gaps that affect design

The documentation has a long comparison of Remote Desktop client features across platforms. It is organised by the Remote Desktop client platforms, and it is the main published comparison. It does not describe Windows App feature by feature, so use it to see where gaps tend to appear, and check the Windows App documentation for the exact current behaviour on your platforms. The examples below are from the comparison page, for AVD.

| Feature | Where the comparison shows support |
|---|---|
| RDP Shortpath (managed and public networks) | Windows (MSI), macOS and iOS/iPadOS. Not Android, Chrome OS or the web client. The Shortpath configuration page lists the Windows App platforms differently (Windows, a macOS beta, Android and Chrome OS in preview), so test the platform you plan to allow. |
| Multiple monitors | Windows (MSI) and macOS. |
| USB and serial port redirection | Windows (MSI) only. |
| Scanner redirection | Windows (MSI) only. |
| Multimedia redirection | Windows (MSI) only. |
| Teams media optimizations | Windows (MSI) and macOS. Some pages label the macOS optimization preview, so confirm before relying on it. |
| WebAuthn redirection | Windows (MSI) only. |
| Smart card redirection | Windows (MSI) and macOS. |
| Printer redirection | Windows (MSI), macOS (limited drivers) and the web client (PDF printing only). |
| Screen capture protection | Windows (MSI), macOS, and iOS and Android with Intune settings. Not the web client. |
| Watermarking | All listed platforms except the Store app. |
| Connection information (shows the transport in use) | Windows (MSI), macOS and the web client. |
| Private Link | All listed platforms. Other pages disagree about which clients support it, so test it (the [connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) has the conflict). |

The comparison page marks a feature as present or absent on a platform. It mostly gives no version numbers and does not say how well the feature works, so treat a tick as a reason to test, not a guarantee.

Two lessons follow.

1. **The browser and mobile clients have the largest gaps.** If your design needs Teams optimization, several monitors, USB devices or Shortpath, test the platform you plan to allow.
2. **Most of the strongest features are listed for the Windows MSI client, which is no longer supported in public cloud.** Whether Windows App on Windows matches each one is not something this article can confirm. Check the Windows App documentation for each feature your design depends on.

The [connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/) explains why Shortpath support in the client matters: without it, sessions use the gateway relay.

## Plan a client change

This is a recommended order. It is judgement, not a documented procedure.

1. **Inventory the clients in use.** Count users by platform and by client. Do not assume everyone is on the client you deployed.
2. **Pick the target client per platform.** Windows App on Windows, macOS, iOS and iPadOS and Android and Chrome OS. The browser as a fallback.
3. **Check the features you depend on** against the Windows App documentation for each platform, using the list in the previous section as a starting point.
4. **Pilot with a small group** that includes your hardest case: multiple monitors, a smart card or a headset.
5. **Check what the firewall allows.** The documentation has a required URL list that includes the addresses clients use. Test the new client from your most locked-down network.
6. **Set a date and communicate it.** Publish the dates in the documentation, because they are not yours to move.
7. **Remove the old client** where you can. Keeping both invites support calls.

## Common mistakes

- **Assuming the Remote Desktop client still works because it still launches.** Support has ended for some of them, so do not expect support for problems with them.
- **Using the built-in Remote Desktop Connection (`mstsc.exe`).** It is not supported for AVD.
- **Forgetting that users need a work or school account.** A personal Microsoft account cannot sign in to Windows App.
- **Allowing every platform without testing the one with the fewest features.** Users on that platform will report the gaps.
- **Treating the browser as equal to a native client.** The comparison shows it has fewer redirection options.
- **Leaving client choice out of the design.** The client decides which transport, redirection and sign-in options a user gets.

## How to validate your client plan

These are recommended checks.

1. On one device per platform, sign in with a test account and confirm the expected desktops and apps appear.
2. Open the connection information on a client that has it, and note the transport. Do this from an office network and from a home network.
3. Test the redirections your users need, one at a time, on every allowed platform.
4. Remove the old client from a test group and confirm that nothing in your design still depends on it.

## Related book chapter and project

[Chapter 6](https://github.com/AddySidd27/azure-virtual-desktop-architect/blob/main/chapters/ch06-clients-and-the-endpoint-story.md) of the book covers clients and the endpoint story. There is no lab for this topic. [Project 06](https://github.com/AddySidd27/azure-virtual-desktop-architect/blob/main/scenarios/project-06-byod-remote-workforce.md) is a fictional case study about personal devices and has not been run against a real environment.

Next: [How Sign-in Works: Three Authentications and Single Sign-on](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/).

## Sources

[Remote Desktop client overview](https://learn.microsoft.com/en-us/azure/virtual-desktop/users/remote-desktop-clients-overview), [Compare Remote Desktop client features](https://learn.microsoft.com/en-us/azure/virtual-desktop/compare-remote-desktop-clients) and [What is Windows App?](https://learn.microsoft.com/en-us/windows-app/overview).
