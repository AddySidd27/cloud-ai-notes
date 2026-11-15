---
title: "Multifactor authentication (MFA): See What Is On and Register Your Phone"
seoTitle: "Azure MFA for Beginners: Check, Register, Sign In"
layout: post.njk
permalink: "/azure-basics-labs/mfa/"
order: 315
tags: [azure-basics-lab]
deck: "You see which MFA protection your tenant already has, leave per-user MFA off, and sign in as your test user with the Microsoft Authenticator app."
description: "Check mandatory MFA and security defaults, leave per-user MFA Disabled, register Microsoft Authenticator for a test user and sign in with MFA."
---

By the end of this lab you will know which multifactor authentication (MFA) protection your tenant already has, you will have looked at the per-user MFA page and left everyone on **Disabled**, and your test user will be registered for the Microsoft Authenticator app and will have signed in with MFA.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn (Microsoft's documentation site).

Multifactor authentication (MFA) means you prove who you are with more than a password. A password is something you know. A phone with an approval prompt is something you have. Together they are much harder to steal than a password alone.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway Azure account and tenant, and a Global Administrator sign-in for it.
- [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the test user `testuser1` you created there. Keep its sign-in name and password to hand.
- A phone (iPhone or Android) where you can install the Microsoft Authenticator app. It is free.
- A private browser window (InPrivate in Edge, Incognito in Chrome). It keeps the test user separate from your admin sign-in.
- Time: about 25 minutes. Cost: nothing. Nothing in this lab creates a billable resource.
- Role: Global Administrator is enough for everything here.

## Safety first

- Use the throwaway tenant only. Read the tenant name at the top right of the portal before you change anything.
- Do not turn on security defaults in this lab. You only look at the setting. [Lab 6: Conditional Access](/azure-basics-labs/conditional-access/) deals with it.
- Do not set any user to **Enabled** or **Enforced** on the per-user MFA page. You only look.
- Do not remove your own MFA method, and do not delete the emergency accounts from Lab 4.
- Azure already requires MFA when you manage Azure. Treat MFA as required for admin work, not as an option.

## What the lab builds

![A left-to-right diagram in three columns. Column 1: a Global Administrator looks at the Microsoft Entra admin center: Azure already requires MFA, security defaults are only looked at, and per-user MFA stays Disabled. Column 2: in a private window, the test user opens the Security info page, adds a method and scans a QR code in Microsoft Authenticator on a phone. Column 3: the test user signs in to the Azure portal with a password and then approves the prompt. The sign-in log then shows an Authenticator step.](/img/basics/mfa.svg)

*Source: [Mandatory multifactor authentication for Azure and admin portals](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mandatory-multifactor-authentication), [Security defaults in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults), [Enable per-user Microsoft Entra multifactor authentication](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userstates) and [Microsoft Authenticator app](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-authenticator-app). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

Part 1 and the check at the end use a second website, the Microsoft Entra admin center (`https://entra.microsoft.com`), not portal.azure.com. Open it in a new tab. Use the same admin account. The sign-in in Part 3 uses portal.azure.com.

**Idea 1: four things that can switch MFA on.**

They are separate from each other:

| Way | What it is | License |
|---|---|---|
| Security defaults | A ready-made bundle from Microsoft: MFA for everyone, MFA for admins, legacy sign-in blocked. It is on or off, nothing in between. | None |
| Per-user MFA | The older way. An admin marks each user account, and that user must do MFA at every sign-in. | None |
| Conditional Access | Rules you write: who, which app, what must happen. MFA is one of the things a rule can ask for. | Microsoft Entra ID P1 or P2 |
| Azure mandatory MFA | Always on, no opt-out, for managing Azure. You do not set it. | None |

Microsoft says the best way to protect users with MFA is a Conditional Access policy. For tenants without that license, it points to security defaults. It says changing per-user states is not recommended unless your licenses do not include Conditional Access and you do not want security defaults. It also says not to enable per-user MFA if you use Conditional Access policies. Security defaults and Conditional Access cannot be used together, and Microsoft says you must disable security defaults before you can use Conditional Access policies. That is what Lab 6 is about.

The last row is Azure's own rule, which you cannot opt out of. The note at the top of Part 1 explains it.

### Part 1: See what protection is already on

Azure already requires MFA. To sign in to the Azure portal and the Microsoft Entra admin center you need it. In the Azure CLI, PowerShell and automation tools you need it when you create, update or delete things. Reading data there does not need it. You cannot turn this off, even in a test tenant. You see it as an MFA prompt when you sign in to manage Azure.

1. Open a new tab and go to the [Microsoft Entra admin center](https://entra.microsoft.com). Sign in with your Global Administrator account. Check the tenant name at the top right.
2. Security defaults. Browse to **Entra ID** > **Overview** > **Properties**, then select **Manage security defaults**. If your menu says **Identity** instead of **Entra ID**, use that. Read the setting: **Enabled**, or **Disabled (not recommended)**. Write down what you see. Close the pane without saving. Microsoft says tenants created on or after October 22, 2019 might already have security defaults on, so either answer is normal.
3. Per-user MFA. Browse to **Entra ID** > **Users** > **All users**, then select **Per-user MFA** in the toolbar. You see a list of users with a status for each one. Check that every user shows **Disabled**. If a user shows **Enabled** or **Enforced**, read "The most common mistake" below before you touch it.

Check: you wrote down whether security defaults are Enabled or Disabled, and every user shows **Disabled** in per-user MFA.

**Why leave per-user MFA at Disabled?** Per-user MFA is the old switch. If you set it to Enabled or Enforced, people who sign in to Windows VMs with Entra (Lab 12, and AVD later) can be blocked. So leave it at **Disabled**. Security defaults and Conditional Access still ask for MFA when they should. The per-user and VM sign-in pages are in the sources if you want the exact error messages.

### Part 2: Register the test user for the Authenticator app

**Idea 2: authentication methods.** An authentication method is one way to prove it is you. You will use the Microsoft Authenticator app: a prompt on your phone that you approve (type the number if one is shown). Other methods exist, such as a code, a text message or a passkey (a security key you plug in or touch). The steps below tell you where to find them.

4. Open a private browser window. Do not use your admin window for this part.
5. Go to `https://mysignins.microsoft.com/security-info`. Sign in as `testuser1` from Lab 4. If Azure asks `testuser1` to set up MFA here, install Microsoft Authenticator on your phone and follow the screens, which are steps 7 and 8 below. If it asks for a new password first, choose one and write it down.
6. On the **Security info** page, select **Add sign-in method** (the button may read **Add method**), then choose **Authenticator app** (or **Microsoft Authenticator**) and select **Add**. The exact wording on the page can differ a little, so pick the option that names the Authenticator app, not a passkey.
7. On your phone, install Microsoft Authenticator from the App Store or Google Play. Open it, select **+** (Add account), then **Work or school account**, then **Scan QR code**. Scan the code that the browser shows. Scan it from inside the Authenticator app, not with the phone camera. If the app offers **Sign in** instead, use the QR code option. Select **Next**.
8. The page shows a test: it sends an approval request to the app. Approve it on the phone. If you see a number on the screen, type that number into the app. Select **Done** (or **Next**, then **Done**).
9. Back on **Security info**, the list now shows **Microsoft Authenticator**. Add a second method so a single lost phone does not lock this user out: select **Add sign-in method** and choose **Phone**. Enter your mobile number and the code you get. If **Phone** is not offered, skip this step and read "What if you lose the phone" below.

Check: Security info lists Microsoft Authenticator.

### Part 3: Sign in with MFA

10. Still in the private window, sign out of the test user, or close the window and open a new private one.
11. Go to `https://portal.azure.com` and sign in as the test user. Microsoft says MFA is required for Azure portal sign-in. Enter the password. The Authenticator app should now ask you to approve. Approve it, typing the number if one is shown.
12. If the portal opens, you signed in with MFA. If the test user has no role yet ([Lab 7: Azure RBAC roles](/azure-basics-labs/rbac-roles/) covers roles), the portal may show little or nothing. That is fine. You are checking the sign-in, not the content.

Check: the portal sent a prompt to your phone and you approved it. Then, in your admin window, open the Entra admin center and go to **Entra ID** > **Monitoring & health** > **Sign-in logs**. Find the test user's latest sign-in to the Azure portal. Open it and look at the **Authentication Details** tab. It should list a step that used the Microsoft Authenticator app.

## What if you lose the phone

This is the reason for the second method in step 9 in Part 2, and for the emergency accounts from Lab 4.

- If the user has another method registered, they choose another way to sign in on the sign-in page and use it. Then they open Security info, add the new phone, and remove the old one.
- If the user has no other method, an administrator selects **Require re-register MFA**. Microsoft says an Authentication Administrator can do this: open the user in the Entra admin center (**Entra ID** > **Users**, pick the user, **Authentication methods**). It removes the user's phone numbers, Authenticator apps and software OATH tokens. At the next sign-in the user is asked to set up MFA again.
- A new phone: keep the old phone until the new one works. Microsoft says Authenticator can back up and restore account entries, but for a work or school account you must sign in again on the new phone.
- If you are the only admin and you lose your phone, nobody can run the reset. Your two emergency accounts from Lab 4 are your way back in. Lab 4 only creates them. The one planned test sign-in with them is in [Lab 6](/azure-basics-labs/conditional-access/), so do not sign in with them before that unless you really need to. In a real tenant they would use a passkey instead of a phone.

## Steps with the Azure CLI

No CLI in this lab. Registering a phone only works in a browser and on the phone, and CLI sign-in is itself covered by mandatory MFA for create, update and delete.

## Terraform

No Terraform in this lab, because nothing is deployed. The steps are a phone registration and a sign-in.

## Check that it works

- Security info for the test user lists Microsoft Authenticator, and you approved a test request from it.
- The test user signed in to the Azure portal and was asked to approve in the app.
- The sign-in log for that sign-in shows an Authenticator step under Authentication Details.
- The per-user MFA page still shows **Disabled** for every user.
- The security defaults setting is the same as when you started.

## The most common mistake

Setting a user to **Enabled** or **Enforced** on the per-user MFA page because it looks like "the MFA switch". It is the older switch. Microsoft says Enabled users move to Enforced after they register, that Enforced users must do MFA at every sign-in, and that legacy sign-in with passwords for old apps then needs app passwords.

It also says not to use per-user MFA with Conditional Access, and the Azure Virtual Desktop articles say it is not supported for sign-in to Entra-joined session hosts. If you set one by mistake, go back to the page, select the user, then select **User MFA settings**, and set the status back to Disabled. Microsoft says admins can move users between states, including to Disabled. If you set it on a user who already registered, check that the user can still sign in afterwards.

A close second: registering only one method. A lost phone then means an admin has to reset the user.

## Clean up

Nothing to delete. This lab created nothing billable.

Keep for later labs:

- The test user and its Authenticator registration. Lab 6 uses it to see what a Conditional Access rule does.
- The emergency accounts from Lab 4.
- A note of what security defaults showed (Enabled or Disabled) at the start. Lab 6 starts from that.

If you want to remove the Authenticator registration from the test user, ask an administrator to select **Require re-register MFA** for that user. Then you register again next time.

## Where this is used in AVD

AVD sign-in asks for MFA through Conditional Access rules, and the per-user switch you left alone here is the one that breaks Entra-joined session hosts. The full setup is in [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/).

## Next lab

[Lab 6: Conditional Access](/azure-basics-labs/conditional-access/) turns MFA into a rule you control, and shows why security defaults have to be turned off first.

## Sources

- [Mandatory multifactor authentication for Azure and admin portals](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mandatory-multifactor-authentication)
- [Security defaults in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults)
- [Enable per-user Microsoft Entra multifactor authentication to secure sign-in events](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userstates)
- [Manage user authentication methods for Microsoft Entra multifactor authentication](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userdevicesettings)
- [Authentication methods in Microsoft Entra ID: Microsoft Authenticator app](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-authenticator-app)
- [Microsoft Entra authentication overview](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-methods)
- [Enable passwordless sign-in with Authenticator](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-passwordless-phone)
- [Transfer Microsoft Authenticator account entries to a new phone](https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-transfer-authenticator-new-phone)
- [Enforce Microsoft Entra multifactor authentication for Azure Virtual Desktop using Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa)
