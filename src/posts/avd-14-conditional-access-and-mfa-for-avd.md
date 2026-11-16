---
title: "Secure Access with Conditional Access and Multifactor Authentication"
seoTitle: "AVD Conditional Access and MFA"
layout: post.njk
permalink: "/azure-virtual-desktop/conditional-access-and-mfa-for-avd/"
order: 114
part: 14
tags: [avd-series]
deck: "Target the right Microsoft Entra applications, set sign-in frequency without causing prompt loops and know what to check when users are asked again and again."
description: "Set up Conditional Access and multifactor authentication for Azure Virtual Desktop: which apps to target, two policies, sign-in frequency and prompt loops."
---

Multifactor authentication (MFA) for Azure Virtual Desktop (AVD) looks like one policy. It turns out to be two applications, two policies and a few ways to create a loop of prompts. It is easy to apply a policy to "all cloud apps", turn on single sign-on (SSO), and then lose time finding out why users are asked for a code again and again.

This article explains which Microsoft Entra applications take part in an AVD sign-in, the two-policy structure Microsoft recommends, how sign-in frequency behaves, and a set of checks for repeated prompts. The [sign-in article](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/) explains the three authentications that these policies sit on.

## Key terms

| Term | Meaning |
|---|---|
| Conditional Access | Microsoft Entra rules that decide whether a sign-in is allowed, and what must happen first, such as multifactor authentication. |
| Multifactor authentication (MFA) | Asking for a second proof of identity in addition to a password. |
| Target resource | The application a policy applies to. |
| Grant control | What the policy requires before it allows access, for example MFA. |
| Access token | A credential from Microsoft Entra ID that lets an app reach a resource. A new one is requested when an app needs access and does not hold a valid one. |
| Sign-in frequency | How often a user must sign in again. It is a session control. |
| Azure Virtual Desktop application | The Microsoft Entra application for the AVD service. It covers subscribing to the feed, signing in to the gateway and sending diagnostics. |
| Windows Cloud Login application | The Microsoft Entra application used to sign in to the session host when single sign-on is on. |
| Single sign-on (SSO) | One sign-in that also signs the user in to the session host, so there is no second password prompt. |
| Session host | The virtual machine that runs the user's Windows desktop or apps. |
| Windows App | Microsoft's current client for Azure Virtual Desktop. The [client article](/azure-virtual-desktop/choose-the-avd-client/) covers it. |
| Feed | The list of desktops and apps a user may open. |
| Gateway | The Microsoft-run AVD service that the client connects through to reach the session host. |
| Periodic reauthentication | A sign-in frequency setting with a time value, such as one hour. |
| Every time | A sign-in frequency setting. It asks the user to sign in again when a new connection starts, after about 5 to 10 minutes since the last sign-in. Supported only on Windows Cloud Login. |
| Per-user MFA | The older way to require MFA, set on each user account. It is separate from Conditional Access. |
| Security Defaults | A set of baseline settings in Microsoft Entra ID. Conditional Access policies cannot be used while they are on. |

## What you need first

Prerequisites:

- A license that includes Microsoft Entra ID P1 or P2 for the users.
- A Microsoft Entra group that holds your AVD users.
- Microsoft Entra multifactor authentication enabled.

To create the policy you also need at least the Conditional Access Administrator role.

Conditional Access cannot be used when Security Defaults are on. If your tenant uses them, you must turn them off before you create the policies. Turn them off deliberately, and tell the security owner. This changes baseline protection for the whole tenant.

## Which applications to target

When a user connects, several Microsoft Entra applications take part. The IDs are in [Enforce Microsoft Entra multifactor authentication for Azure Virtual Desktop using Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa#create-a-conditional-access-policy). The Windows 365 ID is in the [pre-configuration checklist](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa#pre-configuration-checklist) on the same page.

| Application | What it covers | Guidance |
|---|---|---|
| Azure Virtual Desktop (ID `9cdead84-a844-4324-93f2-b2e6bb768d07`) | Subscribing to AVD, signing in to the gateway during a connection, and sending diagnostics from the device. | Target it with your MFA policy. Do not use the Every time sign-in frequency on it (see Key terms and the sign-in frequency section). |
| Windows Cloud Login (ID `270efc09-cd0d-444b-a71f-39af4910ec45`) | Signing in to the session host when single sign-on is on. | Target it with the second policy. Use the same users, grant and conditions as the first policy. Sign-in frequency can differ. Check that no policy blocks it. |
| Azure Virtual Desktop Azure Resource Manager Provider (ID `50e95039-b200-4007-bc97-8d5790743a63`) | Retrieving the feed. | Do not select it. It must not have MFA. |
| Windows 365 (ID `0af06dc6-e4b5-4f28-818e-e78e62d137a5`) | Windows App signs in to this application too, even if the user only has AVD resources. | Make sure no policy blocks it. A block causes sign-in failures for AVD users. |

If you use the older Azure Virtual Desktop (classic), a different set of applications applies.

The Azure Virtual Desktop application used to be called Windows Virtual Desktop. If you registered the `Microsoft.DesktopVirtualization` resource provider before the name changed, the application may still show the old name. The application ID is the same.

When users connect with the web client, the sign-in log lists the client app as Azure Virtual Desktop client (ID `a85cf173-4192-42f8-81fa-777a763e6e2c`, from the note under step 20 of the [policy steps](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa#create-a-conditional-access-policy)). This client app is linked internally to the server app where you set the policy.

If you connect with thin clients, ask the client's provider whether Windows Cloud Login is the right target for single sign-on connections.

The next section calls the two policies Policy 1 (service) and Policy 2 (session host).

![Three columns: the Azure Virtual Desktop app covers subscribing and gateway sign-in (policy one); Windows Cloud Login covers session host sign-in (policy two); the Resource Manager Provider app, outlined red, stays out of every policy. Windows 365 must not be blocked.](/img/avd/AVD-Post-14-Apps-And-Policies.png)

*Source: [Enforce Microsoft Entra multifactor authentication for Azure Virtual Desktop using Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa).*

## The two-policy structure

Use two separate policies rather than one combined policy. The two policies must match, or users see MFA prompts at unexpected times.

| Setting | Policy 1: service | Policy 2: session host |
|---|---|---|
| Target application | Azure Virtual Desktop | Windows Cloud Login |
| Users | The AVD user group | The same group |
| Grant | Require MFA | Require MFA |
| Sign-in frequency | Per your security needs | Match or exceed policy 1. Every time is supported only here. |
| Client apps | Browser, plus mobile apps and desktop clients | The same |

When a user connects, policy 1 is evaluated when Windows App authenticates to the Azure Virtual Desktop application. Policy 2 is evaluated later, when the gateway starts session host single sign-on through Windows Cloud Login. When both are right, the user sees one MFA prompt, if one is needed, and enters the session.

In the policy, under Conditions > Client apps, do not select the legacy authentication clients.

## Sign-in frequency

Sign-in frequency decides how often Microsoft Entra asks again. Behavior:

- A user is asked again only when a new access token is needed. After a connection is up, the user is not prompted even if the session outlasts the frequency.
- **Periodic reauthentication** takes a time value. If you set one hour, MFA is required when a connection starts more than an hour after the last sign-in.
- **Every time** is supported only on Windows Cloud Login, with SSO on. Users are then asked when starting a new connection after a period of 5 to 10 minutes since the last sign-in.
- On the Azure Virtual Desktop application, after the period ends, background feed refresh and diagnostics upload fail silently until the user signs in again interactively.
- A network disruption that forces the session to be re-established after the period also forces a new sign-in. That can mean more prompts on unstable networks.
- Some users on devices that are not registered in Microsoft Entra ID may see a "Stay signed in to all your apps" prompt. If they decline organization management of the device, they may be asked more often.

Frequent sign-in matters most on personal devices, where the local operating system might not require MFA or lock after inactivity.

**Recommendation:** begin with the same periodic value on both policies. Add Every time on Windows Cloud Login only for high-risk groups, and test reconnects on a bad network first.

## Traps to check before you enable single sign-on

The pre-configuration checklist covers most of these. Complete it before you enable single sign-on on the host pool. The last item comes from the section on Microsoft Entra joined session hosts on the same page.

- **Policies that target "All cloud apps"** apply to AVD single sign-on sessions and can block access unexpectedly. List them first. If you use Microsoft Entra Kerberos for Azure Files, the [identity article](/azure-virtual-desktop/choose-the-right-identity-model/) describes an exclusion you also need.
- **Device compliance policies.** Microsoft Entra joined session hosts may not satisfy compliance policies written for user endpoints (Intune rules that say a device is healthy enough). For connection-time policies, the compliance rule applies to the client device, so most deployments should scope connection-time compliance to client endpoints. A policy that targets an app used inside the session, such as Microsoft 365, applies to the session host instead. If an "All cloud apps" policy requires compliance, exclude Windows Cloud Login and Azure Virtual Desktop from it and create separate AVD policies.
- **Location policies.** For the Azure Virtual Desktop application they evaluate the user's client IP. For Windows Cloud Login the address Conditional Access sees may differ from the client IP, depending on network routing. Test both.
- **Per-user MFA.** If it is on at the same time as Conditional Access, users on Microsoft Entra joined session hosts get "The sign-in method you're trying to use isn't allowed". Disable per-user MFA for AVD users and use Conditional Access only.
- **Microsoft Entra joined hosts and strong methods.** If you do not want to restrict sign-in to strong methods such as Windows Hello for Business (sign-in with a PIN or biometrics tied to the device), exclude the Azure Windows VM Sign-In application from the policy. This is the Microsoft Entra application used to sign in to Microsoft Entra joined Windows VMs ([Microsoft Entra joined session host VMs](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa#microsoft-entra-joined-session-host-vms)).

## When users are prompted again and again

These are the usual causes, with the Every time cause split out of the first one.

| Cause | What to look at |
|---|---|
| Sign-in frequency differs between the two apps | Make the values equal, or have Windows Cloud Login match or exceed the other. |
| Every time is set on the Azure Virtual Desktop application | Move it to Windows Cloud Login. |
| Per-user MFA is on beside Conditional Access | Disable per-user MFA. |
| No policy covers Windows Cloud Login | The user gets MFA once at the service and again at the session host. Add a policy for it. |
| The consent prompt is not hidden | It looks like a sign-in prompt. See the [sign-in article](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/). |
| Session lock shows the remote lock screen | The default with single sign-on is to disconnect on lock. If someone changed it, users must give full credentials after a lock. Set it back to disconnect. See the [sign-in article](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/). |

For sign-in errors, the [troubleshooting page](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-sso-conditional-access#authentication-errors-at-connection-time) gives a short list of codes and what they mean. It says the sign-in log is the main tool.

| Code | Meaning |
|---|---|
| AADSTS50058 | The client has no active Microsoft Entra session. Sign out of Windows App and in again, and clear the Web Account Manager cache (the Windows store of cached sign-in tokens) on the client device if needed. |
| AADSTS50076 | MFA is required, by policy or per-user, and was not satisfied. Check the user's registered method and the policy conditions. |
| AADSTS530002 | The device is not compliant. Which device depends on which policy failed. |
| AADSTS530032 | A tenant security control blocked the sign-in. This can be Security Defaults or a policy that blocks access. |
| AADSTS65001 | Consent is required. Hide the consent prompt or give admin consent for Windows Cloud Login. |

The diagnosis steps are the same each time. In the Microsoft Entra admin center, go to Identity > Monitoring & health > Sign-in logs. Filter by the user. Look for entries for the Azure Virtual Desktop and Windows Cloud Login applications. For each failure, note the error code, open the Conditional Access tab to see which policy blocked it, and open Authentication Details to see which method was used.

## Common mistakes

- **Applying one policy to "All cloud apps" and calling it done.** It also catches the apps AVD needs and can cause failures.
- **Adding the Resource Manager Provider app to a policy.** It is only for the feed and must not have MFA.
- **Blocking the Windows 365 or Windows Cloud Login app.** Windows App signs in to the Windows 365 app as well. Check that no policy blocks either app.
- **Setting Every time on the wrong application.** It causes constant prompts on feed refresh.
- **Leaving per-user MFA on.** It collides with Conditional Access on Microsoft Entra joined hosts.
- **Applying user-device compliance rules to session hosts at connection time.** Scope compliance to client devices.

## How to validate your policies

Run these checks after you configure the policies.

1. Connect with Windows App as a test user. Confirm you authenticate once, with MFA if required, and enter without a second prompt.
2. In the sign-in logs, filter by the test user. Check that the Azure Virtual Desktop and Windows Cloud Login entries both show success and the expected policy.
3. If either shows failure, open the Conditional Access tab to see which policy blocked it.
4. Wait past your sign-in frequency and reconnect. Confirm the behavior you intended.
5. Test from an unstable network, and from a location your policies treat differently.

Next: [Who Can Administer Azure Virtual Desktop: Roles, Scopes and Delegation](/azure-virtual-desktop/who-can-administer-azure-virtual-desktop/).

## Sources

- [Enforce Microsoft Entra multifactor authentication for Azure Virtual Desktop using Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa)
- [Troubleshoot single sign-on and Conditional Access](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-sso-conditional-access)
- [Configure single sign-on](https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-single-sign-on)
