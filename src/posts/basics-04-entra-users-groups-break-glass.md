---
title: "Microsoft Entra Users, Groups and Break-Glass Accounts"
seoTitle: "Entra Users, Groups and Break-Glass Accounts for Beginners"
layout: post.njk
permalink: "/azure-basics-labs/entra-users-groups-break-glass/"
order: 314
tags: [azure-basics-lab]
deck: "A test user, a security group, and two emergency-access admin accounts in a throwaway Entra tenant."
description: "Create a standard Entra test user, a security group, and two cloud-only emergency access accounts, and learn why they matter before you set up Conditional Access."
---
By the end of this lab you will have one standard test user, one security group with that user in it, two emergency-access (break-glass) Global Administrator accounts, and a second group named EmergencyAccess that holds those two accounts.

I have not run these steps in a live tenant for this article. Each step is checked against Microsoft Learn.

## What you need

- A throwaway tenant from [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/). Never use your employer's tenant or a real one.
- Your own admin account in that tenant. By default, the person who creates a tenant gets the Global Administrator role.
- Optional for the CLI part: [Lab 2: Cloud Shell and the Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/). The CLI part needs the User Administrator role (and Groups Administrator or User Administrator for groups). As the creator of the tenant you are Global Administrator, which is enough.
- A password manager, or paper and a safe place, for two long passwords.
- Time: about 30 minutes.
- Cost: nothing. Users and groups are included with the free tier of Microsoft Entra ID.

## Safety first

- Check the tenant name in the top right corner of the portal before you change anything. If it is not your throwaway tenant, stop.
- Do not use your daily admin account as the test user. Do not use a personal Microsoft account either. The reasons are in the steps.
- Do not sign in to a break-glass account just to see what happens. A sign-in on that account should always be a planned test or a real emergency.
- Do not use `az login --use-device-code`.
- Write the two break-glass passwords down before you close the page that shows them. You cannot read them again.
- Azure already requires multifactor authentication (MFA) when you manage Azure. This includes break-glass accounts. Do not plan on turning MFA off for them.

## What the lab builds

![Diagram of one Microsoft Entra tenant. A standard test user is a member of a security group named TestUsers. Two cloud-only emergency access accounts, each with the Global Administrator role, are members of a security group named EmergencyAccess.](/img/basics/entra-users-groups-break-glass.svg)

*Source: [Create, invite, and delete users](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users), [Manage groups](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-manage-groups), [Manage emergency access accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

Learn writes these steps for the Microsoft Entra admin center at `https://entra.microsoft.com`. I use that site below. Sign in there with your admin account from Lab 1. The menu names are the ones Learn uses: **Entra ID** > **Users**, and so on.

**Idea 1: every user has a sign-in name that ends in your tenant domain.**
Your tenant came with a domain that ends in `.onmicrosoft.com`. A sign-in name (the user principal name, or UPN) looks like `testuser1@yourtenant.onmicrosoft.com`. Find your domain name first. Open **Entra ID** > **Users** and select your own account. Your own sign-in name may look long and odd, for example with `#EXT#` in the middle. That is fine. The part after the last `@` is your `.onmicrosoft.com` domain. Write it down. In the steps below, `yourtenant.onmicrosoft.com` stands for your own domain.

### Part A: a standard test user

Why a separate test user? Later labs need to show what a normal person sees. An admin account sees and can do far more, so it tells you the wrong story. Learn also says to test with a non-administrator account when you test password reset, because admins get a different reset policy.

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) as your admin account.
2. Browse to **Entra ID** > **Users**.
3. Select **New user** > **Create new user**.
4. On the **Basics** tab:
   - **User principal name**: type `testuser1` and pick your `.onmicrosoft.com` domain.
   - **Display name**: `Test User 1`.
   - **Password**: leave **Auto-generate password** on. Copy the password when it is shown.
   - Leave **Account enabled** checked.
5. Select **Next: Properties**. Under **Settings**, set the user's location to your country. Learn calls this the global location. The field may be labelled **Usage location**.

   Learn says to check that users have a location assigned before you assign licences. Setting it now saves you a surprise later.
6. Leave the **Assignments** tab alone. Select **Review + create**, then **Create**.
7. Open a new private window (InPrivate in Edge, Incognito in Chrome). Go to `https://portal.azure.com` and sign in as the test user with the temporary password.
8. Learn says a new user might be asked to change the password at the next sign-in. If you see that prompt, choose a new password and write it down. Learn also says security defaults are being rolled out to all new tenants at creation, with a 24-hour grace period before protections are enforced. If they are on, the test user may be asked to set up the Microsoft Authenticator app now. You can follow the screens, or close the window and do it in [Lab 5: Multifactor authentication](/azure-basics-labs/mfa/), which walks through it.
9. Sign out and close the private window.

Check: In **Entra ID** > **Users**, `Test User 1` is listed as a **Member**, and the properties page shows the usage location you set.

**Why not a personal Microsoft account?** A personal account such as `name@outlook.com` does not live in your tenant. If you add one, it comes in as an external guest. Learn says external guests sign in with an external method and have guest-level privileges. Azure Virtual Desktop also lists extra requirements and limits for external identities. For learning the basics, a normal member account in your own tenant is the plain case.

### Part B: a security group with the user in it

**Idea 2: use groups for access, not single users.** A group lets you give access once and then add or remove people. You will use groups for Conditional Access, roles and Azure Virtual Desktop later. A **security group** is the type used to manage access to shared resources. **Assigned** membership means you add members by hand. The other kind, **dynamic**, adds them by rule.

1. Browse to **Entra ID** > **Groups** > **All groups**.
2. Select **New group**.
3. **Group type**: **Security**.
4. **Group name**: `TestUsers`. Add a short description if you like.
5. **Membership type**: **Assigned**.
6. Leave **Microsoft Entra roles can be assigned to the group** on **No**. Learn says this option needs a Microsoft Entra ID P1 or P2 licence, so you may not see it at all.
7. Under **Members**, select the link, tick `Test User 1`, then choose **Select**. If it asks for owners, you can leave them empty.
8. Select **Create**.

Check: Open `TestUsers` > **Members**. `Test User 1` is listed. The group overview shows 1 member.

### Part C: two emergency-access accounts

**Idea 3: a break-glass account is your way back in when everything else fails.** Learn gives these examples: your identity provider is down, all your admins' phones are unavailable, or the last Global Administrator left. Learn asks for at least two accounts. They should be cloud-only, use the `*.onmicrosoft.com` domain, not be federated or synced from on-premises, and hold the Global Administrator role. They are not tied to one person. You use them only in a real emergency or a planned test.

Give the accounts plain names that say what they are, so no one deletes them by mistake. I use `emergency-access-01` and `emergency-access-02` below. Learn's security benchmark uses names like EmergencyAccess01 for the same reason. The emergency access page itself gives no naming rule.

1. Browse to **Entra ID** > **Users** > **New user** > **Create new user**.
2. **User principal name**: `emergency-access-01`, with your `.onmicrosoft.com` domain. **Display name**: `Emergency Access 01`.
3. **Password**: untick **Auto-generate password** and enter a long random password. Learn's Microsoft 365 guidance says 16 or more characters, and longer is fine. Entra accepts up to 256. Make it fully random, with upper case, lower case, numbers and symbols. A password manager can generate it. Save it before you continue. Learn says the default is no password expiry, but a tenant created before 2021 can have a 90-day expiry. Learn also says an emergency credential must not expire, so check this setting if your tenant is old.
4. Select **Review + create**, then **Create**.
5. Repeat for the second account: `emergency-access-02`, display name `Emergency Access 02`, and a different password.
6. Give each account the Global Administrator role. Learn says you need at least the Privileged Role Administrator role to do this. The account that created the tenant is a Global Administrator by default.
   1. Open **Entra ID** > **Users** and select the account.
   2. Select **Assigned roles**, then **Add assignments**.
   3. Pick **Global Administrator**, then **Next**.
   4. Choose an **Assignment type** of **Active**. With the free tier you can only assign roles as active. If you see a time-limit option, leave the assignment permanent. If your tenant has Privileged Identity Management, Learn says to make the assignment active and permanent, not eligible.
   5. Select **Assign**.
7. Create the group that you will use to exclude both accounts from Conditional Access in a later lab. Go to **Entra ID** > **Groups** > **All groups** > **New group**. Use **Security**, name `EmergencyAccess`, membership type **Assigned**. Under **Members**, add both emergency accounts. Select **Create**. Do not add `Test User 1` or your own admin account.

Check: Both emergency accounts show **Global Administrator** under **Assigned roles** > **Active assignments**. The group `EmergencyAccess` has 2 members.

**Where to keep the passwords.** Learn says to store the credentials in a known secure place that more than one authorised admin can reach, and not on one person's device. Its example is a fireproof safe. For your lab, a password manager entry that is not your daily vault, or a sealed printout, is enough. Do not store both in the same place as your own admin password.

### The MFA problem, said plainly

This part matters, so I will not hide it.

Learn says break-glass accounts must also sign in with MFA once enforcement starts, and the FAQ says there is no exception for them, not even in a test tenant. Learn's answer is: register a passkey (FIDO2) on each account, or use certificate-based authentication if you already have a public key infrastructure. Learn names passkey as the recommended choice. It also says the method should differ from the one your normal admin accounts use, and should not be tied to an employee's own phone.

Most beginners have no hardware security key and no certificate infrastructure. So here are your options.

- **If you have a FIDO2 security key** (or two), follow Learn: [enable passkeys (FIDO2)](https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-authentication-passkeys-fido2) in the tenant, then [register a passkey on each emergency account](https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-register-passkey-with-security-key). Keep the keys in different places.
- **If you have no key,** you can still finish this lab. The accounts exist, hold the role and are in the group. What you cannot do is count on them as a real way in.

**My judgement, not Learn:** in a throwaway test tenant with nothing in it, I would register the Microsoft Authenticator app on a phone I own for each emergency account, so I can run the one sign-in test below. This goes against Learn's advice to keep emergency accounts off personal phones, and I would never do it in a real tenant. It is only so that you can practise. Delete the accounts when you finish the series, or move them to a key. If you would rather not, skip the sign-in test. The accounts still exist and still do their job in later labs.

Learn also says to test emergency accounts at least every 90 days, and to alert on every sign-in with them. In a real tenant, set that up. The Azure Monitor alert steps are on [Manage emergency access accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access). This lab does not build the alert.

## Steps with the Azure CLI

The CLI covers Parts A and B, and adding members to a group. It cannot finish the rest, for these reasons:

- The `az ad user create` reference lists no option for usage location. Set it in the portal (Part A, step 5).
- The `az ad` commands I checked have no command to assign a Microsoft Entra role. Do the Global Administrator assignment in the portal (Part C, step 6).
- Your CLI sign-in needs a role that can create users and groups. Learn lists User Administrator to create users, and Groups Administrator or User Administrator for groups.

Azure CLI 2.76 or newer is the Learn-recommended version for MFA. In Cloud Shell you are already signed in, so skip `az login`. On your own PC, run `az login` and sign in as yourself in the browser. Do not use device code.

```bash
az account show --query "{tenant:tenantId, user:user.name}" -o table
```

Check: The tenant ID and user name are the throwaway tenant and your admin account. If not, stop.

Set variables. Replace `yourtenant.onmicrosoft.com` with the domain you wrote down. Type the password at the prompt so it does not stay in your shell history. It needs 8 or more characters and three of the four types: lower case, upper case, numbers, symbols.

```bash
DOMAIN="yourtenant.onmicrosoft.com"
TEST_UPN="testuser2@$DOMAIN"
read -rs -p "Temporary password: " TEST_PW; echo
```

Create the test user. The `--force-change-password-next-sign-in` flag marks the user as needing to update the password at the next sign-in.

```bash
az ad user create \
  --display-name "Test User 2" \
  --user-principal-name "$TEST_UPN" \
  --password "$TEST_PW" \
  --force-change-password-next-sign-in true
```

Check: The command prints JSON that includes the `userPrincipalName` you gave.

Create a security group and add the user. `--member-id` takes the user's object ID.

```bash
az ad group create \
  --display-name "TestUsersCli" \
  --mail-nickname "TestUsersCli"

USER_ID=$(az ad user show --id "$TEST_UPN" --query id -o tsv)
az ad group member add --group "TestUsersCli" --member-id "$USER_ID"
az ad group member list --group "TestUsersCli" --query "[].userPrincipalName" -o tsv
```

Check: The last command prints `testuser2@...`. In the portal, open the group and confirm **Group type** shows **Security**. The `az ad group create` reference does not state the type, so look.

Open `testuser2` in the portal to set the location as in Part A, step 5. The CLI part is optional, and the later labs use `testuser1`.

You could create the emergency accounts with `az ad user create` in the same way, then use the portal for the role. I do those in the portal, so you can see the passwords and roles on screen.

## Terraform

No Terraform in this lab, because Terraform comes in [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/) and these are one-off identity steps you should do by hand first.

## Check that it works

- `Test User 1` signed in once from a private window and sits in `TestUsers`.
- Both emergency accounts (`emergency-access-01` and `emergency-access-02`) are cloud-only on `.onmicrosoft.com`, hold an active, permanent Global Administrator role, and sit in `EmergencyAccess`.
- You have both passwords stored somewhere you can find them, and it is not only your own head or your own laptop.
- If you registered a key or an authenticator on an emergency account: sign in once in a private window, confirm it works, and sign out. Then open the sign-in logs in the Entra admin center (search for "sign-in logs" if you cannot find the menu) and look for your own test sign-in. That is how a real alert would look.

## The most common mistake

Making only one emergency account, or making none, and then locking yourself out with a Conditional Access policy in [Lab 6: Conditional Access](/azure-basics-labs/conditional-access/). The second most common: creating the accounts and then forgetting to add them to `EmergencyAccess`. When you build the policy, the exclusion has to use that group.

A close third is using your own admin account as the "test user" and thinking the policy works. It works for you because you are an admin, not because it is right for a normal user.

## Clean up

Keep, for later labs:

- `Test User 1` and the `TestUsers` group. Later labs use them.
- Both emergency accounts, the `EmergencyAccess` group, and the stored passwords.

Delete if you made them from the CLI:

```bash
az ad group delete --group "TestUsersCli"
az ad user delete --id "$TEST_UPN"
```

Learn says a deleted user stays in **Deleted users** for 30 days and can be restored in that time. You can clear the variable with `unset TEST_PW`.

## Where this is used in AVD

Azure Virtual Desktop needs users who exist in Microsoft Entra ID. A test user plus a group is the normal way to give people access to a desktop. See [Choose the right identity model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/).

## Next lab

[Lab 5: Multifactor authentication](/azure-basics-labs/mfa/) adds multifactor authentication for your test user and shows what Azure already requires of admins.

## Sources

- [Manage emergency access accounts in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access)
- [How to create, invite, and delete users](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users)
- [Manage Microsoft Entra groups and group membership](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-manage-groups)
- [Learn about group types, membership types, and access management](https://learn.microsoft.com/en-us/entra/fundamentals/concept-learn-about-groups)
- [Assign user roles with Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-assign-roles-to-users)
- [Problems signing in to a Microsoft application](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/application-sign-in-problem-first-party-microsoft)
- [Mandatory multifactor authentication for Azure and admin portals](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mandatory-multifactor-authentication)
- [Security defaults in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults)
- [Password policies and account restrictions in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-policy)
- [Tutorial: Enable users to unlock their account or reset passwords (SSPR)](https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-sspr)
- [Admin account security in Microsoft 365 for business](https://learn.microsoft.com/en-us/microsoft-365/admin/security-and-compliance/m365b-account-security-admins)
- [Best practices for Microsoft Entra roles](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/best-practices)
- [az ad user](https://learn.microsoft.com/en-us/cli/azure/ad/user), [az ad group](https://learn.microsoft.com/en-us/cli/azure/ad/group), [az ad group member](https://learn.microsoft.com/en-us/cli/azure/ad/group/member)
- [Zero Trust: Phase 1, secure the identity control plane (step 7, emergency accounts)](https://learn.microsoft.com/en-us/security/zero-trust/adopt/implement-privileged-access-identity#step-7-configure-emergency-accounts)
- [Supported identities and authentication methods for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/authentication)
