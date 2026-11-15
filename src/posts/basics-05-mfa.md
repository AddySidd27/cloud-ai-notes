---
title: "Multifactor authentication (MFA): See What Is On and Register Your Phone"
seoTitle: "Azure MFA for Beginners: Check, Register, Sign In"
layout: post.njk
permalink: "/azure-basics-labs/mfa/"
order: 315
tags: [azure-basics-lab]
deck: "You see which MFA protection your tenant already has, leave per-user MFA off, and sign in as your test user with the Microsoft Authenticator app."
description: "Beginner Azure lab: check mandatory MFA and security defaults, leave per-user MFA Disabled, register Microsoft Authenticator for a test user and sign in with MFA."
---

By the end of this lab you will know which MFA protection your tenant already has, you will have looked at the per-user MFA page and left everyone on **Disabled**, and your test user will be registered for the Microsoft Authenticator app and will have signed in with MFA.

I have not run these steps in a live tenant for this article. Each step is checked against Microsoft Learn.

Multifactor authentication (MFA) means you prove who you are with more than a password. A password is something you know. A phone with an approval prompt is something you have. Together they are much harder to steal than a password alone.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway Azure account and tenant, and a Global Administrator sign-in for it.
- [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the test user `testuser1` you created there. Keep its sign-in name and password to hand.
- A phone (iPhone or Android) where you can install the Microsoft Authenticator app. It is free.
- A private browser window (InPrivate in Edge, Incognito in Chrome). It keeps the test user separate from your admin sign-in.
- Time: about 25 minutes. Cost: nothing. Nothing in this lab creates a billable resource.
- Role: Global Administrator is enough for everything here. Learn lists these lower roles for the individual pages: Conditional Access Administrator for security defaults, Authentication Policy Administrator for the per-user MFA page.

## Safety first

- Use the throwaway tenant only. Read the tenant name at the top right of the portal before you change anything.
- Do not turn on security defaults in this lab. You only look at the setting. [Lab 6: Conditional Access](/azure-basics-labs/conditional-access/) deals with it.
- Do not set any user to **Enabled** or **Enforced** on the per-user MFA page. You only look.
- Do not remove your own MFA method, and do not delete the emergency accounts from Lab 4.
- Azure already requires MFA when you manage Azure. Treat MFA as required for admin work, not as an option.

## What the lab builds

![A left-to-right diagram. A Global Administrator opens the Microsoft Entra admin center and checks three things: mandatory MFA, security defaults and per-user MFA. In a private window, the test user opens the Security info page, registers the Microsoft Authenticator app on a phone, and then signs in to the Azure portal with MFA.](/img/basics/mfa.svg)

*Source: [Mandatory multifactor authentication for Azure and admin portals](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mandatory-multifactor-authentication), [Security defaults in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults), [Enable per-user Microsoft Entra multifactor authentication](https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userstates) and [Microsoft Authenticator app](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-authenticator-app). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: three ways MFA is switched on.**

There are three ways, and they are separate from each other:

| Way | What it is | Licence |
|---|---|---|
| Security defaults | A ready-made bundle from Microsoft: MFA for everyone, MFA for admins, legacy sign-in blocked. It is on or off, nothing in between. | None |
| Per-user MFA | The older way. An admin marks each user account, and that user must do MFA at every sign-in. | None |
| Conditional Access | Rules you write: who, which app, what must happen. MFA is one of the things a rule can ask for. | Microsoft Entra ID P1 or P2 |

Learn says the best way to protect users with MFA is a Conditional Access policy. For tenants without that licence, it points to security defaults. It says changing per-user states is not recommended unless your licences do not include Conditional Access and you do not want security defaults. It also says not to enable per-user MFA if you use Conditional Access policies. Security defaults and Conditional Access cannot be used together, and Learn says you must disable security defaults before you can use Conditional Access policies. That is what Lab 6 is about.

On top of these three, Azure has its own rule that you cannot opt out of. Step 2 shows it.

### Part 1: See what protection is already on

1. Sign in to the [Azure portal](https://portal.azure.com) as your Global Administrator. Check the tenant name at the top right.
2. Mandatory MFA. Learn says that starting October 2024, MFA is required to sign in to the Azure portal, the Microsoft Entra admin center and the Intune admin center for any create, read, update or delete action (phase 1). Starting October 1, 2025, it is required for Azure CLI, Azure PowerShell, the Azure mobile app, infrastructure-as-code tools and REST API calls that create, update or delete (phase 2). Read actions do not need MFA in phase 2. Learn also says there is no opt-out, and that a tenant used only for testing is not an exception. Postponing was possible only until July 1, 2026.
3. To see whether it applies to your tenant, open `https://aka.ms/managemfaforazure` while signed in as Global Administrator. Look for a banner on the **Multifactor authentication (Phase 1)** page that says enforcement began for your tenant. Then open `https://aka.ms/postponePhase2MFA` and look for the same kind of banner on the **Multifactor authentication (Phase 2)** page. Write down what you see. If you do not see a banner, do not change anything on those pages. Both pages can postpone enforcement, and you do not want that.
4. Security defaults. Go to the [Microsoft Entra admin center](https://entra.microsoft.com). Browse to **Entra ID** > **Overview** > **Properties**, then select **Manage security defaults**. Read the setting: **Enabled**, or **Disabled (not recommended)**. Write down what you see. Close the pane without saving. Learn says tenants created on or after October 22, 2019 might already have security defaults on, so either answer is normal.
5. Per-user MFA. Browse to **Identity** > **Users** > **All users**, then select **Per-user MFA** in the toolbar. Some Learn pages call the top menu group **Entra ID** instead of **Identity**. It is the same place. You see a list of users with a status for each one. Check that every user shows **Disabled**. If a user shows **Enabled** or **Enforced**, read "The most common mistake" below before you touch it.

**Why leave per-user MFA at Disabled?** Learn says all users start as Disabled, and that Disabled is the right status for users covered by security defaults or Conditional Access. A user who shows Disabled here can still be asked for MFA by those two. There is also a harder reason that matters for Azure Virtual Desktop. Learn says that if per-user MFA is on together with Conditional Access, users on Microsoft Entra joined session hosts see the error "The sign-in method you're trying to use isn't allowed". The same Learn page tells you to disable per-user MFA and use Conditional Access only. The Entra-joined VM sign-in in [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/) hits the same rule. So the habit starts here: leave the page alone.

### Part 2: Register the test user for the Authenticator app

**Idea 2: authentication methods.** An authentication method is one way to prove it is you. In plain words, the ones Learn lists for MFA are:

- **Microsoft Authenticator, approval prompt.** A message on your phone. You tap approve, or type a number shown on the sign-in screen. Learn says the number step helps against people who keep sending prompts hoping you tap yes.
- **Verification code.** A six-digit code that changes. The Authenticator app can show it, and so can other apps that follow the OATH standard. Learn says a user can have up to five such apps or hardware tokens.
- **Text message or phone call.** A code sent to a phone number, or a call you answer. Easy, but easier to trick than the others.
- **Passkey, FIDO2 security key, Windows Hello for Business.** Sign-in tied to a device, a key or your face or fingerprint. Learn calls these phishing-resistant, which means a fake sign-in page cannot trick you into giving them away. Learn recommends them where you can use them.

Security defaults ask users to register the Authenticator app with notifications. Learn says users can also use codes from it or from any OATH app.


6. Open a private browser window. Do not use your admin window for this part.
7. Go to `https://mysignins.microsoft.com/security-info`. Learn lists the same page as `https://aka.ms/MySecurityInfo` for the commercial Azure cloud. Sign in as `testuser1` from Lab 4. If the tenant asks the user to change the password or to register for MFA first, follow the prompts.
8. On the **Security info** page, select **Add sign-in method** (the button may read **Add method**), then choose **Authenticator app** (or **Microsoft Authenticator**) and select **Add**. Learn describes the flow this way: install and set up the app, then select **Done**. The exact wording on the page can differ a little, so pick the option that names the Authenticator app, not a passkey.
9. On your phone, install Microsoft Authenticator from the App Store or Google Play. Open it. When it asks, add a **Work or school account**. Learn also describes a **Sign in** option on that screen. The page then guides you to link the app, usually with a QR code that you scan in the app. Select **Next**.
10. The page shows a test: it sends an approval request to the app. Approve it on the phone. If you see a number on the screen, type that number into the app. Select **Done** (or **Next**, then **Done**).
11. Back on **Security info**, the list now shows **Microsoft Authenticator**. Add a second method so a single lost phone does not lock this user out. Select **Add sign-in method** again and add one more option the page offers, for example a phone number if the page lists it. If the page offers nothing else, skip this step and read "What if you lose the phone" below.

### Part 3: Sign in with MFA

12. Still in the private window, sign out of the test user, or close the window and open a new private one.
13. Go to `https://portal.azure.com` and sign in as the test user. Learn says MFA is required for Azure portal sign-in to do create, read, update or delete actions. Enter the password. The Authenticator app should now ask you to approve. Approve it, typing the number if one is shown.
14. If the portal opens, you signed in with MFA. If the test user has no role yet ([Lab 7: RBAC roles](/azure-basics-labs/rbac-roles/) covers roles), the portal may show little or nothing. That is fine. You are checking the sign-in, not the content.

Check: in your admin window, go to the Entra admin center and open **Monitoring & health** > **Sign-in logs** in the left menu. It sits under **Identity** or **Entra ID**, depending on the page. Find the test user's latest sign-in to the Azure portal. Open it and look at the **Authentication Details** tab. It should list a step that used the Microsoft Authenticator app. Learn says the sign-in logs show which application enforced MFA.

## What if you lose the phone

This is the reason for the second method in step 11 and for the emergency accounts from Lab 4.

- If the user has another method registered, they choose another way to sign in on the sign-in page and use it. Then they open Security info, add the new phone, and remove the old one.
- If the user has no other method, an administrator has to help. Learn says an Authentication Administrator can open the user in the Entra admin center (**Entra ID** > **Users**, pick the user, **Authentication methods**) and select **Require re-register MFA**. That removes the user's phone numbers, Microsoft Authenticator apps and software OATH tokens, and deactivates hardware OATH tokens. At the next sign-in the user is asked to set up MFA again.
- A new phone with a backup. Learn says Authenticator can back up and restore account entries. For a work or school account only the account name comes back, and you must sign in again on the new phone. Keep the old phone until the new one works.
- If you are the only admin and you lose your phone, nobody can run the reset. Learn says break-glass accounts must also sign in with MFA once enforcement begins, and recommends a passkey (FIDO2) or certificate-based authentication for them. That is a decision for your real tenant. In this throwaway tenant, write down that you have two emergency accounts (`emergency-access-01` and `emergency-access-02`). Do not sign in with them just to look. Lab 4 explains why they need a passkey or similar before they are useful.

## Steps with the Azure CLI

No CLI in this lab, on purpose. The work is the user registering a phone and approving a prompt, and that only happens in a browser and on the phone. The per-user MFA state can only be changed through Microsoft Graph beta calls (Learn documents them), not through a stable `az` command, and this lab only looks at that page and changes nothing. Also, the CLI sign-in is itself covered by mandatory MFA for create, update and delete, so a script can not skip the step this lab teaches.

## Terraform

No Terraform in this lab, because nothing is deployed. The steps are a phone registration and a sign-in.

## Check that it works

- Security info for the test user lists Microsoft Authenticator, and you approved a test request from it.
- The test user signed in to the Azure portal and was asked to approve in the app.
- The sign-in log for that sign-in shows an Authenticator step under Authentication Details.
- The per-user MFA page still shows **Disabled** for every user.
- The security defaults setting is the same as when you started.

## The most common mistake

Setting a user to **Enabled** or **Enforced** on the per-user MFA page because it looks like "the MFA switch". It is the older switch. Learn says Enabled users move to Enforced after they register, that Enforced users must do MFA at every sign-in, and that legacy sign-in with passwords for old apps then needs app passwords. It also says not to use per-user MFA with Conditional Access, and the Azure Virtual Desktop article says it breaks sign-in on Entra-joined session hosts. If you set one by mistake, go back to the page, select the user, then select **User MFA settings**, and set the status back to Disabled. Learn says admins can move users between states, including to Disabled. If you set it on a user who already registered, check that the user can still sign in afterwards.

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
