---
title: "Microsoft Entra Users, Groups and Break-Glass Accounts"
seoTitle: "Entra Users, Groups and Break-Glass Accounts for Beginners"
layout: post.njk
permalink: "/azure-basics-labs/entra-users-groups-break-glass/"
order: 314
tags: [azure-basics-lab]
deck: "A test user, a security group, and two emergency-access admin accounts in a throwaway Entra tenant."
description: "Create a standard Entra test user, a security group and two cloud-only emergency access accounts, and learn why they matter before Conditional Access."
---

By the end of this lab you will have one standard test user, one security group with that user in it, two emergency-access (break-glass) Global Administrator accounts, and a second group named EmergencyAccess that holds those two accounts. Global Administrator is the most powerful role in Microsoft Entra. A break-glass account is a spare admin account that you keep for emergencies.

## What you need

- A throwaway tenant from [Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/). Never use your employer's tenant or a real one.
- Your own admin account in that tenant. By default, the person who creates a tenant gets the Global Administrator role.
- The notes sheet from that first lab, with your `.onmicrosoft.com` domain on it.
- A password manager, or paper and a safe place, for two long passwords.
- Time: about 50 minutes.
- Cost: nothing. Users and groups are included with the free tier of Microsoft Entra ID.

## Safety first

- Check the tenant name in the top right corner of the portal before you change anything. If it is not your throwaway tenant, stop.
- Do not use your daily admin account as the test user. Do not use a personal Microsoft account either. The reasons are in the steps.
- Do not sign in to a break-glass account just to see what happens. A sign-in on that account should always be a planned test or a real emergency. The planned test for this series is in the Conditional Access lab.
- Do not use `az login --use-device-code`.
- Write each password in a safe place before you select **Create**. For the test user, put it in a text note. For the two emergency accounts, save each one in your password manager.
- Azure already requires multifactor authentication (MFA) when you manage Azure. This includes break-glass accounts. Do not plan on turning MFA off for them.

## What the lab builds

![Diagram of one Microsoft Entra tenant, in two rows. Row 1: the standard test user testuser1 is a member of the security group TestUsers. Row 2: two cloud-only emergency access accounts, each with the Global Administrator role, are members of the security group EmergencyAccess. The admin account you work from is in neither group, and EmergencyAccess is excluded from the sign-in rule you build in the Conditional Access lab.](/img/basics/entra-users-groups-break-glass.svg)

*Based on the pages listed under Sources. Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

This lab uses a second website, the Microsoft Entra admin center (`https://entra.microsoft.com`), not portal.azure.com. Open it in a new tab. Use the same admin account as in the first lab. The menu names are the ones the Entra admin center uses: **Entra ID** > **Users**, and so on. Step numbers run on from one section to the next.

**Idea 1: every user has a sign-in name that ends in your tenant domain.**
Your tenant came with a domain that ends in `.onmicrosoft.com`. A sign-in name (the user principal name, or UPN) looks like `testuser1@yourtenant.onmicrosoft.com`. Easiest way to find your domain: open **Entra ID** > **Overview** and read **Primary domain**. It is also on your notes sheet from the first lab. In the steps below, `yourtenant.onmicrosoft.com` stands for your own domain. Do not copy your own sign-in name from the Users list: it may look long and odd, for example with `#EXT#` in the middle. You only need the part after the last `@`.

### A standard test user

Why a separate test user? Later labs need to show what a normal person sees. An admin account sees and can do far more, so it tells you the wrong story. Test with a non-administrator account when you test password reset, because admins get a different reset policy.

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) as your admin account.
2. Browse to **Entra ID** > **Users**.
3. Select **New user** > **Create new user**.
4. On the **Basics** tab:
   - **User principal name**: type `testuser1` and pick your `.onmicrosoft.com` domain in the drop-down next to the name.
   - **Display name**: `Test User 1`.
   - **Password**: untick **Auto-generate password** and type a long temporary password of your own. Copy it into a text note now.
   - Leave **Account enabled** checked.
5. Select **Next: Properties**. Under **Settings**, set the location (**Usage location**, a country) to your country. If the label differs, use the country or location setting on that tab.

   A user needs a location before you can assign a licence. Setting it now saves you a surprise in the Conditional Access lab.
6. Leave the **Assignments** tab alone. Select **Review + create**, then **Create**.
7. Open a new private window (InPrivate in Edge, Incognito in Chrome). Go to `https://portal.azure.com` and sign in as the test user with the temporary password.
8. Azure asks for MFA when you sign in to the Azure portal, so `testuser1` will probably be asked to set up MFA at this first sign-in. Close the window. You set it up properly in [Multifactor authentication (MFA)](/azure-basics-labs/mfa/). If the page asks for a new password first, choose one and write it down. What you should see otherwise: the portal opens, or the MFA setup screen opens, and no subscription or resources are shown. That is correct, because the user has no role yet (the RBAC lab gives it one). The check below does not need the sign-in to finish.
9. Sign out and close the private window.

Check: In **Entra ID** > **Users**, `Test User 1` is listed as a **Member**, the properties page shows the usage location you set, and the sign-in got as far as the password or MFA setup screen.

**Why not a personal Microsoft account?** A personal account such as `name@outlook.com` does not live in your tenant. If you add one, it comes in as an external guest. External guests sign in with an external method and have guest-level privileges. Azure Virtual Desktop also lists extra requirements and limits for external identities. For learning the basics, a normal member account in your own tenant is the plain case.

### A security group with the user in it

**Idea 2: use groups for access, not single users.** A group lets you give access once and then add or remove people. You will use groups for Conditional Access, roles and Azure Virtual Desktop later. A **security group** is the type used to manage access to shared resources. **Assigned** membership means you add members by hand. The other kind, **dynamic**, adds them by rule.

10. Browse to **Entra ID** > **Groups** > **All groups**.
11. Select **New group**.
12. **Group type**: **Security**.
13. **Group name**: `TestUsers`. Add a short description if you like.
14. **Membership type**: **Assigned**.
15. Leave **Microsoft Entra roles can be assigned to the group** on **No**. This option is only offered with a paid Entra plan, so you may not see it at all.
16. Under **Members**, select the link, tick `Test User 1`, then choose **Select**. If it asks for owners, you can leave them empty.
17. Select **Create**.

Check: Open `TestUsers` > **Members**. `Test User 1` is listed. The group overview shows 1 member.

### Two emergency-access accounts

**Idea 3: a break-glass account is your way back in when everything else fails.** It is a spare way into the tenant when normal sign-in fails. You need two. They are cloud-only (created in Entra, not copied from a company server), they use the `*.onmicrosoft.com` domain, and they hold the Global Administrator role. They are not tied to one person. You use them only in a real emergency or a planned test. Later, in [Conditional Access](/azure-basics-labs/conditional-access/), you will build sign-in rules (Conditional Access). These accounts must be excluded from those rules, so a mistake in a rule cannot lock you out.

Give the accounts plain names that say what they are, so no one deletes them by mistake. Use names like `emergency-access-01` and `emergency-access-02`, as below. There is no required naming rule.

18. Browse to **Entra ID** > **Users** > **New user** > **Create new user**.
19. **User principal name**: `emergency-access-01`, with your `.onmicrosoft.com` domain from the drop-down. **Display name**: `Emergency Access 01`.
20. **Password**: untick **Auto-generate password**. Let your password manager generate a long random password (20 characters or more is a good habit). Paste it into the field and save the entry in your password manager before you select **Create**. An emergency credential must not expire, so make sure the password is set not to expire.
21. Select **Review + create**, then **Create**.
22. Repeat for the second account: `emergency-access-02`, display name `Emergency Access 02`, and a different password.
23. Give each account the Global Administrator role. You need at least the Privileged Role Administrator role to do this. The account that created the tenant is a Global Administrator by default. Do the next five actions for `emergency-access-01`, then again for `emergency-access-02`.
24. Open **Entra ID** > **Users** and select the account.
25. Select **Assigned roles**, then **Add assignments**.
26. Pick **Global Administrator**, then **Next**.
27. Choose an **Assignment type** of **Active**. With the free tier you can only assign roles as active. If you see a time-limit option, leave the assignment permanent.
28. Select **Assign**.
29. Create the group that you will use to exclude both accounts from Conditional Access in a later lab. Go to **Entra ID** > **Groups** > **All groups** > **New group**. Use **Security**, name `EmergencyAccess`, membership type **Assigned**. Under **Members**, add both emergency accounts. Select **Create**. Do not add `Test User 1` or your own admin account.

Check: Both emergency accounts show **Global Administrator** under **Assigned roles** > **Active assignments**. The group `EmergencyAccess` has 2 members.

**Where to keep the passwords.** Store the credentials in a known secure place that more than one authorised admin can reach, and not on one person's device, for example a fireproof safe. For your lab, a password manager entry that is not your daily vault, or a sealed printout, is enough. Do not store both in the same place as your own admin password.

### The MFA problem, said plainly

This part matters.

Emergency access accounts must also sign in with MFA, and there is no exception for them, not even in a test tenant. The recommended method is a passkey (a FIDO2 security key that you plug in or touch), registered on each account. These accounts should also stay off personal phones, and use a method that differs from the one your normal admin accounts use.

Most beginners have no security key. So here is the plan for this series.

- **If you have a FIDO2 security key** (or two), enable [passkeys (FIDO2)](https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-authentication-passkeys-fido2) in the tenant, then [register a passkey on each emergency account](https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-register-passkey-with-security-key). Keep the keys in different places.
- **If you have no key,** you register nothing in this lab and you do not sign in with these accounts now. The accounts exist, hold the role and are in the group, which is all that the MFA lab needs. The Conditional Access lab asks for one planned sign-in with `emergency-access-01` before you build a sign-in rule, and it walks you through it. For that test it uses an authenticator app on your own phone. That is only acceptable because this tenant is a throwaway. Do not do this in a real tenant.

In a real tenant, also test each emergency account at least every 90 days, and alert on every sign-in to them. The alert steps are in the emergency access article listed under Sources. This lab does not build the alert.

Check: you now have everything that the MFA lab and the RBAC lab need. The emergency accounts are only needed in the Conditional Access lab. You can stop here.

## Steps with the Azure CLI

No CLI in this lab. Creating a user and a group is a one-time portal task here, and the CLI would create a second user and group that you would have to delete. The commands (`az ad user create`, `az ad group create`) do exist, but the portal is simpler for the location and role steps.

## Terraform

No Terraform in this lab, because Terraform comes in [Terraform basics](/azure-basics-labs/terraform-basics/) and these are one-off identity steps you should do by hand first.

## Check that it works

- `Test User 1` sits in `TestUsers`, and its first sign-in from a private window reached the password or MFA setup screen.
- Both emergency accounts (`emergency-access-01` and `emergency-access-02`) are cloud-only on `.onmicrosoft.com`, hold an active, permanent Global Administrator role, and sit in `EmergencyAccess`.
- Open the password manager entry and confirm both emergency entries have a user name and a password saved, in a place that is not only your own head or your own laptop.
- If you registered a key on an emergency account: sign in once in a private window, confirm it works, and sign out. Then open **Entra ID** > **Monitoring & health** > **Sign-in logs** in the Entra admin center and look for your own test sign-in. If you have no key, the Conditional Access lab does this check.

## The most common mistake

Making only one emergency account, or making none, and then locking yourself out with a Conditional Access policy in the [Conditional Access lab](/azure-basics-labs/conditional-access/). The second most common: creating the accounts and then forgetting to add them to `EmergencyAccess`. When you build the policy, the exclusion has to use that group.

A third is using your own admin account as the "test user" and thinking the policy works. It works for you because you are an admin, not because it is right for a normal user.

A fourth: skipping the usage location on `testuser1`. The Conditional Access lab cannot assign a licence without it.

## Clean up

Keep, for later labs:

- `Test User 1` and the `TestUsers` group. Later labs use them.
- Both emergency accounts, the `EmergencyAccess` group, and the stored passwords.

Nothing to delete in this lab. Later labs use all of these objects.

## Where this is used in AVD

Azure Virtual Desktop needs users who exist in Microsoft Entra ID. In AVD you assign an application group to a group, not to single people. Later you will give `TestUsers` access to a desktop, then add or remove people from the group. See [Choose the right identity model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/).

## Next lab

[Multifactor authentication (MFA)](/azure-basics-labs/mfa/) adds multifactor authentication for your test user and shows what Azure already requires of admins.

## Sources

- [Manage emergency access accounts in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access)
- [How to create, invite, and delete users](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users)
- [Manage Microsoft Entra groups and group membership](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-manage-groups)
