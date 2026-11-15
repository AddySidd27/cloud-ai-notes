---
title: "Choose the Client: Windows App, Remote Desktop and the Web"
seoTitle: "Choose an AVD Client: Windows App or Web"
layout: post.njk
permalink: "/azure-virtual-desktop/choose-the-avd-client/"
order: 112
part: 12
tags: [avd-series]
deck: "Match user devices to the supported client, see what the retirement of the older Remote Desktop clients means and plan a client change."
description: "Choose the right client for Azure Virtual Desktop: Windows App, the older Remote Desktop clients, the browser, feature gaps and how to plan a migration."
---

The client is the one part of the service your users touch. It is also the part that changes most often and is least under your control, because it runs on devices you may not manage. Most AVD designs spend pages on session hosts and a sentence on the client. That is a risk. If a client is out of support, Microsoft will not help with problems in it, and a whole group of users may still depend on it.

This article lists the clients Microsoft names, what has changed about them, the feature gaps that matter for design, and how to plan a move from an older client.

## Key terms

| Term | Meaning |
|---|---|
| Client | The app on the user's device that signs in, shows the feed and opens the remote session. |
| Windows App | Microsoft's current client for Azure Virtual Desktop, Windows 365, Microsoft Dev Box, Remote Desktop Services and remote PCs. |
| Remote Desktop Services | A separate Microsoft service for server-based remote desktops. It is not Azure Virtual Desktop. |
| Remote PC | A physical computer, such as an office PC, that you reach from far away. |
| Remote Desktop client | The older family of clients. Windows App replaces it. |
| MSI client | The Remote Desktop client for Windows, installed from a standalone installer. |
| Store app | The Remote Desktop app for Windows, once available from the Microsoft Store. |
| Web client | A client that runs in a browser, with nothing to install on a desktop or laptop. |
| Redirection | Passing a local device or feature, such as a printer, camera or clipboard, into the remote session. |
| RDP Shortpath | An optional direct UDP path between the client and the session host. The [connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/) explains it. |
| Teams media optimizations | An optimized Microsoft Teams calling and meeting experience inside a remote session. |
| WebAuthn redirection | Passes sign-in requests made inside the remote session to the local device, so security keys and Windows Hello for Business can be used. |
| Private Link | A way to connect a remote session over a private connection. |
| Transport | The network path a session uses, for example UDP (RDP Shortpath) or TCP through the Azure gateway. The [connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/) explains it. |
| Mobile application management | Intune rules that protect company data inside apps on a phone or tablet. |
| Microsoft Intune | Microsoft's cloud service for managing devices with policies. |
| Public cloud | The standard Azure cloud that most customers use. |
| Sovereign cloud | A separate Azure cloud for a government or country. Azure Government (Azure for US Government) and Azure operated by 21Vianet (in China) are examples. |
| AVD Classic | The older, non-Azure Resource Manager version of the service. The [fit article](/azure-virtual-desktop/decide-whether-azure-virtual-desktop-fits/) covers its retirement. |
| Feed | The list of desktops and apps a user may open. |

## The clients and where they stand

Windows App is the new way to connect to cloud and remote resources, and it replaces the Remote Desktop client. These facts have dates in them, so check the linked pages before you rely on them.

| Client | Platforms | Status |
|---|---|---|
| Windows App | Windows, macOS, iOS and iPadOS, Android and Chrome OS, web browsers, Meta Quest | The current client. Sign-in needs a work or school account. A personal Microsoft account does not work. Meta Quest support is in preview. |
| Remote Desktop client for Windows (MSI) | Windows | No longer supported for public cloud customers from March 27, 2026. Support was extended to September 28, 2026 for Azure Government, Azure operated by 21Vianet and AVD Classic. That date has passed at the time of writing, so check the [client overview](https://learn.microsoft.com/en-us/previous-versions/remote-desktop-client/overview) for the current position. |
| Remote Desktop app for Windows (Store) | Windows | No longer supported and no longer available to install. Support ended September 2025. |
| Remote Desktop clients for macOS and iOS/iPadOS | macOS, iOS, iPadOS | Not available to download. Replaced by Windows App. |
| Remote Desktop client for Android and Chrome OS | Android, Chrome OS | Available from Google Play, as listed in the [client overview connection matrix](https://learn.microsoft.com/en-us/previous-versions/remote-desktop-client/overview#connection-matrix-and-status). |
| Remote Desktop web client | Browser | No longer supported for public cloud customers from March 27, 2026. No end-of-support date is announced for Azure Government or Azure operated by 21Vianet. |

Two clients are not supported for AVD at all: the RemoteApp and Desktop Connections client, and the Remote Desktop Connection client (`mstsc.exe`).

![A diagram with three columns: device, client, and what to watch for. Windows PC, macOS, iPhone and iPad, Android and Chrome OS, and Meta Quest all point to Windows App. Web browser points to Windows App in the browser. Notes beside each row say what to watch for: the Windows row gives the retirement dates of the older Remote Desktop clients for Windows, and the Meta Quest row says it is in preview. A red box at the bottom says the RemoteApp and Desktop Connections client and the Remote Desktop Connection client are not supported for Azure Virtual Desktop.](/img/avd/AVD-Post-12-Client-By-Device.png)

*Which client each device uses. Feature differences between clients are left out. Source: [Get started with Windows App](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps).*

**Recommendation:** standardize on Windows App for every platform you support, and treat any user still on an older client as a migration item with a date.

## What each choice changes

Facts first.

- **Windows App needs a work or school sign-in for Azure Virtual Desktop.** You cannot sign in with a personal Microsoft account. For AVD, Windows 365, Dev Box and Remote Desktop Services you must sign in. For remote PC connections on supported platforms you can use Windows App without signing in.
- **In a browser, nothing is installed.** This works on desktops and laptops. Mobile browsers are not supported. The browser must be no more than 12 months old, support the AVC video codec and have WebGL turned on ([Get started with Windows App](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps?pivots=azure-virtual-desktop)). It is the lowest-effort option for a device you do not manage.
- **Windows App on Windows connects to AVD but not to Remote Desktop Services.** For Remote Desktop Services on Windows, keep using the Remote Desktop app on Windows. If you use both services, you may need two clients on Windows.
- **Features differ by platform.** The next section gives examples.

A browser is a good fallback for contractors and kiosks. It is a poor primary client if users need local devices, several monitors or heavy media. The feature table below is the reason.

## Feature gaps that affect design

Windows App has a comparison of features across platforms, with a separate view for Azure Virtual Desktop. The table follows that view, as of November 2026.

Terms used in the table. STUN and TURN are two methods RDP Shortpath uses over public networks (see the [networking article](/azure-virtual-desktop/plan-avd-networking/)). WebRTC and SlimCore are two ways Teams media optimization works. TWAIN is a standard for scanners. RAW printing sends print data to the printer without converting it first. Publisher Imagesetter is a printer driver. YubiKey is a brand of hardware security key.

RDP Multipath lets one session use several network paths at once. Input Protection protects typed keys from keyloggers on the device. Display Protection stops the session display from being captured. Screen capture protection blocks screenshots of the session. Watermarking shows a visible label over the session. Managed networks are networks you control, such as a company network. Public networks are the open internet.

| Feature | Where the Windows App comparison shows support |
|---|---|
| Multiple monitors | Windows and macOS. Android and Chrome OS is listed, but only on Chrome OS devices. Not iOS and iPadOS, the web client or Meta Quest. An external monitor is listed for Windows, macOS, iOS and iPadOS, and Android and Chrome OS (the last depends on the local device), but not the web client or Meta Quest. |
| USB and serial port redirection | Windows only. |
| Scanner redirection | Windows only, and TWAIN scanner redirection is labeled preview. |
| Multimedia redirection (video playback and calls) | Windows only. |
| Teams media optimizations | WebRTC: Windows, macOS, iOS and iPadOS, and Android and Chrome OS. SlimCore: Windows and macOS. Neither is listed for the web client or Meta Quest. |
| WebAuthn redirection | Windows. macOS, iOS and iPadOS, and Android are listed as preview with minimum client versions. On those platforms only passkey sign-ins to Microsoft Entra ID work. On Android the passkey must be stored on the device, for example in Microsoft Authenticator. Not the web client or Meta Quest. |
| Smart card redirection | Windows and macOS. iOS and iPadOS is preview and supports only YubiKey. Not Android and Chrome OS, the web client or Meta Quest. |
| Printer redirection | Windows (RAW printing is preview for Azure Virtual Desktop), macOS (only the Publisher Imagesetter driver by default) and the web client. Not iOS and iPadOS, Android and Chrome OS, or Meta Quest. |
| Screen capture protection | Windows and macOS. iOS and iPadOS and Android need Intune mobile application management, and Chrome OS is not covered. The web client is listed only with Microsoft Edge for Business on Windows, an Intune app protection policy and a Conditional Access policy that requires app protection. |
| Watermarking | Windows, macOS, iOS and iPadOS, Android and Chrome OS, and the web client. |
| Connection information (shows the transport in use) | Windows, macOS and the web client. Not iOS and iPadOS, Android and Chrome OS, or Meta Quest. |
| RDP Shortpath for managed networks | Windows, macOS, iOS and iPadOS, Android and Chrome OS, and Meta Quest. Not the web client. |
| RDP Shortpath for public networks | Windows, Android and Chrome OS, and Meta Quest, for both STUN and TURN. macOS only in a beta build. Not iOS and iPadOS or the web client. |
| RDP Multipath | UDP: Windows (version 2.0.559.0 or later) and macOS (beta build). UDP and TCP: Windows (version 2.0.1069.0 or later) ([Windows App comparison](https://learn.microsoft.com/en-us/windows-app/compare-platforms-features?pivots=azure-virtual-desktop)). |
| Input Protection and Display Protection (preview) | Windows only, with a minimum Windows App version and session host configuration. Input Protection also needs the Windows Cloud Input Protect MSI on the device. |
| Private Link | Windows, macOS, iOS and iPadOS, and Android and Chrome OS. Not the web client or Meta Quest. |

The comparison marks a feature as present or absent on a platform and labels some entries preview. It gives version numbers for only a few features and does not say how well a feature works, so treat a tick as a reason to test, not a guarantee. Redirection also depends on what your administrator allows. If the host pool setting and the session host policy differ, the most restrictive one wins.

Two lessons follow.

1. **The browser, Meta Quest, and iOS and iPadOS have the largest gaps.** If your design needs Teams optimization, several monitors, USB devices or Shortpath, test the platform you plan to allow.
2. **Windows has the widest support, and several entries on other platforms are preview or beta builds.** Check the Windows App feature comparison again before you rely on a feature, because these entries change.

The [connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/) explains why Shortpath support in the client matters. Without Shortpath, the session goes through the Azure gateway instead of directly to the session host. Test Private Link on each platform before you rely on it; [Required Connectivity](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) covers it.

## Plan a client change

This is a recommended order.

1. **Inventory the clients in use.** Count users by platform and by client. Do not assume everyone is on the client you deployed.
2. **Pick the target client per platform.** Windows App on Windows, macOS, iOS and iPadOS and Android and Chrome OS. The browser as a fallback.
3. **Check the features you depend on** against the Windows App feature comparison for each platform, using the table in the section "Feature gaps that affect design" as a starting point.
4. **Pilot with a small group** that includes your hardest case: multiple monitors, a smart card or a headset.
5. **Check what the firewall allows.** The required URL list includes the addresses clients use. The [connectivity article](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) covers it. Test the new client from your most locked-down network.
6. **Set a date and communicate it.** Publish the support end dates, because they are not yours to move.
7. **Remove the old client** where you can. Keeping both invites support calls.

## Common mistakes

- **Assuming the Remote Desktop client still works because it still launches.** Support has ended for some of them. Microsoft will not help with problems in them.
- **Using the built-in Remote Desktop Connection (`mstsc.exe`).** It is not supported for AVD.
- **Forgetting that users need a work or school account.** A personal Microsoft account cannot sign in to Windows App.
- **Allowing every platform without testing the one with the fewest features.** Users on that platform will report the gaps.
- **Treating the browser as equal to a native client.** The comparison shows it has fewer redirection options.
- **Leaving client choice out of the design.** The client decides which transport, redirection and sign-in options a user gets.

## How to validate your client plan

Run these checks.

1. On one device per platform, sign in with a test account and confirm the expected desktops and apps appear.
2. Open the connection information on a client that has it, and note the transport. Do this from an office network and from a home network.
3. Test the redirections your users need, one at a time, on every allowed platform.
4. Remove the old client from a test group and confirm that nothing in your design still depends on it.

Next: [How Sign-in Works: Three Authentications and Single Sign-on](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/).

## Sources

- [Windows App features across platforms and devices](https://learn.microsoft.com/en-us/windows-app/compare-platforms-features?pivots=azure-virtual-desktop)
- [What is Windows App?](https://learn.microsoft.com/en-us/windows-app/overview)
- [Get started with Windows App](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps?pivots=azure-virtual-desktop)
