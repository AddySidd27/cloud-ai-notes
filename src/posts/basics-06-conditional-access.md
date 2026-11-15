---
title: "Conditional Access: A Safe First Policy That Asks for MFA"
seoTitle: "Conditional Access for Beginners: Safe Report-only MFA Policy"
layout: post.njk
permalink: "/azure-basics-labs/conditional-access/"
order: 316
tags: [azure-basics-lab]
deck: "You build one Conditional Access policy that asks the test group for MFA when they use Azure Virtual Desktop, you test it in report-only mode first, and you delete it at the end."
description: "Beginner Azure lab: create a safe Conditional Access policy in report-only mode, scoped to a test group and the two AVD apps, check it with What If, then enable and delete it."
---

By the end of this lab you will have created one Conditional Access policy for a test group, checked it with the What If tool and the sign-in log in report-only mode, switched it on for that group only, switched it off again, and deleted it.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

Conditional Access is a set of rules in Microsoft Entra ID. A rule reads like an if-then sentence: if this user wants to use this app, then they must do this first. Learn gives the example "if a user wants to access Microsoft 365, then they must do multifactor authentication". Multifactor authentication (MFA) was the topic of [Lab 5: Multifactor authentication](/azure-basics-labs/mfa/).

A bad Conditional Access rule can lock every admin out of a tenant. That is why this lab has more safety steps than most. Do them in order. Do not skip any.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway tenant and a Global Administrator sign-in for it.
- [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the test user `testuser1`, the group `TestUsers` (with `testuser1` in it), the two emergency accounts `emergency-access-01` and `emergency-access-02`, and the group `EmergencyAccess` (with both accounts in it).
- [Lab 5: Multifactor authentication](/azure-basics-labs/mfa/): `testuser1` registered for the Authenticator app, per-user MFA left at **Disabled**, and your note of what security defaults showed.
- A Microsoft Entra ID P1 licence (or P2, which includes it). Learn says Conditional Access needs P1, and that the users the policy applies to need a licence that includes P1 or P2. Learn also says customers with Microsoft 365 Business Premium licences can use Conditional Access. The free Entra tier does not include it.
  - How to get one for a test tenant: Learn's sign-up page points to a free trial of Microsoft Entra ID P2, and to a Microsoft 365 Developer Program sandbox "if qualified". I do not state a trial length or a price, because that Learn page does not. Read the terms on the sign-up page before you start it.
  - Assign the licence to `testuser1`. Learn says to assign users a licence that includes P1 or P2. Learn says licences are managed in the Microsoft 365 admin center (**Users** > **Active users** > select the user > **Licenses and apps**), and that a user needs a usage location (a country or region) before a licence can be assigned. The Entra admin center can show a user's licences under **Users** > **All users** > the user > **Licenses**.
- A private browser window (InPrivate in Edge, Incognito in Chrome).
- Role: Learn says at least the Conditional Access Administrator role to create policies. Global Administrator covers it.
- Time: about 45 minutes. Cost: nothing from Azure. A trial or licence has its own terms, see above.

## Safety first

- Throwaway test tenant only. Never an employer tenant, never a real one. Read the tenant name at the top right before you change anything.
- Stop check. Before you create the policy, every line in the "Stop check" list below must be true. If one is not true, stop. Do not create the policy.
- The two emergency accounts must be proven to sign in, and must be excluded through the group `EmergencyAccess`.
- Create the policy in **Report-only** first. Learn says report-only policies are evaluated but not enforced.
- Scope: the group `TestUsers` only. Never **All users**.
- Exclude the admin account you work from, and the group `EmergencyAccess`.
- Target only two apps: Azure Virtual Desktop and Windows Cloud Login. Never **All resources** (older name: **All cloud apps**).
- Grant control: **Require multifactor authentication**. Never **Block access**.
- Turning security defaults off lowers the protection of the whole tenant. Learn says you must do it before you can use Conditional Access. Read "Idea 1" before you do it.
- At the end, delete the policy. Learn says that when the licence expires, policies are not removed, and you can view and delete them but you cannot update them. A policy you cannot edit is a policy you cannot fix.

## What the lab builds

![A left-to-right diagram. A Global Administrator creates one Conditional Access policy in the Microsoft Entra admin center. The policy includes the group TestUsers, excludes the admin account and the group EmergencyAccess, targets the Azure Virtual Desktop and Windows Cloud Login apps, and requires multifactor authentication. The policy starts in report-only mode. The What If tool and the sign-in log show what the policy would do.](/img/basics/conditional-access.svg)

*Source: [Require multifactor authentication for Azure Virtual Desktop using Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa), [Build a Conditional Access policy](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-policies), [Analyze Conditional Access policy impact](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-report-only) and [What If tool](https://learn.microsoft.com/en-us/entra/identity/conditional-access/what-if-tool). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

This lab uses the Microsoft Entra admin center at `https://entra.microsoft.com`, not the Azure portal. Learn writes the Conditional Access steps for that site. The title "Steps in the Azure portal" is the same for every lab. Learn's menu path is **Entra ID** > **Conditional Access** > **Policies**. Some older Learn pages say **Protection** > **Conditional Access**. It is the same place.

### Part 1: Stop check

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) as your Global Administrator. Read the tenant name at the top right.
2. Check the licence. In the Entra admin center, open **Entra ID** > **Conditional Access** > **Policies**. If the page opens and offers **New policy**, the tenant has the licence for it. If it asks you to get a licence, stop and get one first (see "What you need"). Then assign it to `testuser1` as described in "What you need", and check it under **Entra ID** > **Users** > **All users** > `testuser1` > **Licenses**.
3. Check the groups. Go to **Entra ID** > **Groups** > **All groups**. Open `TestUsers`: it must hold `testuser1` and must not hold your admin account. Open `EmergencyAccess`: it must hold both emergency accounts.
4. Prove that an emergency account can sign in. This is a planned test, so it is allowed. Open a private window. Go to `https://portal.azure.com`. Sign in as `emergency-access-01` with the method you registered in Lab 4 (a passkey on a security key, or, in a throwaway tenant only, the Authenticator app as Lab 4 describes). Sign out. In your admin window, open **Entra ID** > **Monitoring & health** > **Sign-in logs** and find that sign-in. It must show **Success**.
5. If you did not register a method on the emergency accounts in Lab 4, you cannot do step 4. Azure requires MFA for these accounts too, as Lab 5 explains. Go back to Lab 4 and finish that part, or stop here.

**Stop check.** All of these must be true before you go on:

- You are in the throwaway tenant, and you read its name.
- Conditional Access shows **New policy** (the licence works).
- `testuser1` is in `TestUsers`. Your admin account is not.
- Both emergency accounts are in `EmergencyAccess`.
- At least one emergency account signed in successfully today, and the sign-in log shows it.
- You know how to turn a policy off (Part 6) and how to delete it (Part 7).

If any line is false, stop. Nothing in this lab is worth a lockout.

### Part 2: Security defaults must be off

**Idea 1: security defaults and Conditional Access do not work together.** Security defaults are a ready-made bundle from Microsoft. Learn lists what it does: all users register for MFA, administrators do MFA, users do MFA when needed, old sign-in protocols are blocked, device code flow is blocked, and Azure management such as the portal, CLI and PowerShell needs MFA. It is one switch, on or off. Conditional Access is the custom version of the same idea. Learn says that organisations that choose Conditional Access policies to replace security defaults must disable security defaults, and the Azure Virtual Desktop page says Conditional Access policies cannot be used when security defaults are on.

What turning them off means for you: the bundle stops. Nothing replaces it until you add policies. Learn says to enable Conditional Access policies straight after disabling, and that Microsoft-managed Conditional Access policies exist that keep the same protections (block legacy authentication, MFA for Azure management, MFA for admins, MFA for all users). Azure's own mandatory MFA from Lab 5 is a separate rule with no opt-out, so your admin sign-in still asks for MFA. The policy in this lab protects only the test group and only two apps. For a throwaway tenant that is acceptable. In a real tenant you would not do this without a plan and the security owner's agreement.

6. Go to **Entra ID** > **Overview** > **Properties**, then select **Manage security defaults**.
7. Read the setting. If it already says **Disabled (not recommended)**, close the pane and go on. If it says **Enabled**, write that down (you may want to turn it back on in the clean up), set **Security defaults** to **Disabled (not recommended)**, and select **Save**. These are the words and steps on Learn's security defaults page.
8. Open **Entra ID** > **Conditional Access** > **Policies**. Learn says Microsoft-managed Conditional Access policies are available to keep the same protections after you disable security defaults. If any appear in the list, leave them alone. Learn says you cannot rename or delete Microsoft-managed policies. Do not change them in this lab.

Check: **Manage security defaults** shows **Disabled (not recommended)**.

### Part 3: Create the policy in report-only mode

**Idea 2: exclude beats include.** Learn says that when a user or group is both included and excluded, the user is excluded: the exclude action overrides the include. That is why your admin account and `EmergencyAccess` go in the exclude list, even though neither is in `TestUsers`. It is a second lock on the same door.

**Idea 3: which apps.** Learn lists two apps for AVD with MFA. **Azure Virtual Desktop** (app ID `9cdead84-a844-4324-93f2-b2e6bb768d07`) covers subscribing to AVD, signing in to the gateway and sending diagnostics. **Windows Cloud Login** (app ID `270efc09-cd0d-444b-a71f-39af4910ec45`) covers signing in to the session host when single sign-on is on. Learn says do not pick **Azure Virtual Desktop Azure Resource Manager Provider** (app ID `50e95039-b200-4007-bc97-8d5790743a63`): it only fetches the feed and must not have MFA. Learn also recommends two policies, one per app, so that sign-in frequency can differ. This lab sets no sign-in frequency, so one policy with both apps keeps it short. Learn's own basic steps also pick both apps in one policy. The two-policy layout is in [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/).

9. In **Entra ID** > **Conditional Access** > **Policies**, select **New policy**.
10. **Name**: `CA-AVD-RequireMFA-TestUsers-REPORTONLY`. A name that says what it does and who it is for helps when you come back later.
11. Under **Assignments**, open the users section (**Users or workload identities**, or **Users**; the label depends on the page).
12. Under **Include**, choose **Select users and groups**, tick **Users and groups**, and select the group `TestUsers`. Do not choose **All users**. Select **Select**.
13. Under **Exclude**, choose **Users and groups**. Select your own admin account and the group `EmergencyAccess`. Select **Select**.
14. Under **Target resources** > **Resources (formerly cloud apps)**, keep the default **Resources (formerly cloud apps)**. Under **Include**, choose **Select resources**.
15. Search for the apps. Learn says to type the start of the app name in order. Type `Azure Virtual` and select **Azure Virtual Desktop**. Check the app ID shows `9cdead84-a844-4324-93f2-b2e6bb768d07`. Then search `Windows Cloud` and select **Windows Cloud Login**. Check the ID `270efc09-cd0d-444b-a71f-39af4910ec45`. Select **Select**.
16. If **Azure Virtual Desktop** is not in the list, also search `Windows Virtual Desktop`. Learn says that is the app's old name, with the same app ID. If either app is still missing, stop here. Learn says a Microsoft cloud app appears in the list only when its service principal exists in your tenant. Learn's AVD page tells you to confirm both apps exist in your tenant before you use them. Do not switch to **All resources** to get around it. Read "The most common mistake".
17. Leave **Conditions** and **Network** alone. Learn says a new policy applies to all client app types by default.
18. Under **Access controls** > **Grant**, choose **Grant access**, tick **Require multifactor authentication**, and select **Select**. Do not choose **Block access**.
19. At the bottom, set **Enable policy** to **Report-only**. Select **Create**. (Learn's AVD page shows **On** here. This lab uses **Report-only** on purpose, as other Learn pages do.)

Check: the policy appears in the list with the state **Report-only**. Open it and read the settings back, top to bottom, against steps 12 to 19. Read slowly. Wrong scope is the mistake that matters.

### Part 4: Ask the What If tool

The What If tool simulates a sign-in and tells you which policies would apply. Learn says only policies that are enabled or in report-only mode are included. Learn also says the What If tool needs four conditions: identity, target resource, device platform and client app. Without all four it cannot give a complete answer.

20. On **Policies**, select **What If** in the toolbar.
21. Set the user to `testuser1`.
22. Set the target resource to **Azure Virtual Desktop**. Learn says to provide the App ID for the application and that groups of apps such as **Office 365** do not match. If searching by name finds nothing, enter the app ID `9cdead84-a844-4324-93f2-b2e6bb768d07`. For **Windows Cloud Login** use `270efc09-cd0d-444b-a71f-39af4910ec45`.
23. Set the device platform to **Windows**. The field label may read **Device platforms**.
24. Set the client app to **Mobile apps and desktop clients**.
25. Leave the optional conditions empty. Learn says they are treated as none.
26. Select **What If**. Look at the two lists. Your policy should be under policies that apply, with **Require multifactor authentication** as the grant control.
27. Run the tool again for each of these, and write down what you see:
    - `testuser1`, target **Windows Cloud Login**: the policy should apply.
    - `testuser1`, target **Azure Virtual Desktop**, client app **Browser**: the policy should apply.
    - `emergency-access-01`, target **Azure Virtual Desktop**: the policy should be under policies that do not apply. Learn says the list gives the reason, the first condition that was not satisfied. Read the reason and check that it points at the user or group exclusion. I do not quote the wording, because Learn does not.
    - Your admin account, target **Azure Virtual Desktop**: same, not applied.

Check: the policy applies to `testuser1` on both apps and does not apply to the emergency account or to your admin.

### Part 5: Look at the sign-in log, Report-only tab

Learn says that during sign-in the system evaluates report-only policies without enforcing them, and that the results show in the **Conditional Access** and **Report-only** tabs of the sign-in log details.

28. In a private window, sign in as `testuser1` at `https://portal.azure.com`. Approve the MFA prompt if you get one, as in Lab 5. This is an ordinary sign-in, not an AVD sign-in.
29. In your admin window, go to **Entra ID** > **Monitoring & health** > **Sign-in logs**. Find that sign-in and open it. Learn says each event shows which policies were enabled, in report-only mode, applied or not applied.
30. Open the **Report-only** tab. Look for `CA-AVD-RequireMFA-TestUsers-REPORTONLY` and read the result next to it. This sign-in was to the Azure portal and not to AVD, so the policy should not have applied. Learn defines **Report-only: Not applied** as "Not all configured policy conditions were satisfied", which fits, because the policy is for the two AVD apps. If the policy is not listed at all, that is also a sign it did not apply to this sign-in.

**The honest limit.** Without an AVD deployment, you cannot see the real AVD sign-in and the real MFA prompt. There is no host pool for the user to connect to, so the two AVD apps are never used. What you have is the What If result and a report-only log that shows the policy was seen and did not apply to a portal sign-in. If you later have an AVD deployment, the same tab would show a result for the two AVD apps. Learn lists **Report-only: User action required** for a policy that would need the user to do MFA, and says that in report-only mode the user is not prompted. The AVD articles [How Sign-in Works: Three Authentications and Single Sign-on](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/) and [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/) show the full flow. [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/) is the next lab where you sign in to something Entra protects.

Check: the policy shows on the **Report-only** tab for the sign-in, and the emergency account's earlier sign-in still shows **Success**.

### Part 6: Enable it for the test group only, then roll back

31. Open the policy. Check once more: Include is `TestUsers` only, Exclude is your admin and `EmergencyAccess`, apps are the two AVD apps, Grant is **Require multifactor authentication**.
32. Learn says to move the **Enable policy** toggle from **Report-only** to **On** after you have confirmed the settings with report-only mode. Set it to **On**. Select **Save**. You may rename the policy to drop `-REPORTONLY`, but that is not needed.
33. Run the What If tool again for `testuser1` on **Azure Virtual Desktop**. The policy should still apply, now enforced. Run it for `emergency-access-01`. It should still not apply.
34. Before you sign out of your admin session, open another private window and sign in as `emergency-access-01` once more. It must succeed. This is the proof that the policy did not lock out the emergency account.
35. Rollback. Open the policy, set **Enable policy** to **Off**, and select **Save**. Learn names **Report-only** and **On** for this toggle. If your toggle shows no **Off**, skip to Part 7 and delete the policy now. Check that the list shows the policy as off (or that it is gone).

Check: the policy went **Report-only**, **On**, then off, and each time you read the state in the list.

### Part 7: Delete the policy

36. Go back to the policy list. Select the policy and look for a **Delete** option (in the toolbar, or in the **...** menu on the row, or inside the policy's own page). Confirm.
37. Check that the list no longer shows it. If Microsoft-managed policies were there before, they should still be there.

Check: no policy named `CA-AVD-RequireMFA-TestUsers-...` remains.

## Steps with the Azure CLI

No CLI in this lab, on purpose. Conditional Access lives in Microsoft Entra, and the safe way to do it the first time is in the portal. The portal shows the warnings (for example, "Don't lock yourself out"), lets you read the scope back on screen, and has the What If tool. A script would create the policy in one step with no one reading the scope. I did not find a Learn page that creates a Conditional Access policy with `az`.

There are other ways. Microsoft Graph has Conditional Access APIs, and Learn's What If page links to one of them (the What If evaluation API). They are out of scope here.

## Terraform

No Terraform in this lab, because a Conditional Access policy is a tenant-wide change that needs a human to check the scope first, and I have not checked any Terraform for this on Learn. Terraform is covered in [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/) with ordinary Azure resources.

## Check that it works

- Security defaults show **Disabled (not recommended)** and you know why.
- You proved that an emergency account can sign in, and you did it again with the policy **On**.
- The What If tool shows the policy applying to `testuser1` on both AVD apps, and not applying to the emergency account or your admin.
- The sign-in log shows the policy on the **Report-only** tab.
- You set the policy to **Off**, then deleted it.

## The most common mistake

Choosing **All users** and **All resources** because the picker did not show the AVD apps, or because it was faster. A policy like that, with MFA, hits every user on every app. If the emergency accounts are not excluded, it can lock out everyone. Learn shows a warning for exactly this: "Don't lock yourself out! Apply a policy to a small set of users first to verify it behaves as expected. Also exclude at least one admin from this policy."

If the AVD apps are not in the list, stop. Learn says some apps do not appear in the picker at all, and that the only ways around it are **All resources** or adding the missing service principal with PowerShell or Graph. This lab takes neither way. Leave the lab for when you have an AVD deployment.

A second mistake: leaving the policy behind. If the licence ends, Learn says the policy stays, and you can view and delete it but not update it.

## Clean up

1. Delete the policy (Part 7).
2. If security defaults were **Enabled** when you started, you can set them back to **Enabled** now: **Entra ID** > **Overview** > **Properties** > **Manage security defaults**. Learn says the two cannot be used together, so do this only after the delete.
3. If you started a trial or bought a licence only for this lab, remove it in the place you got it. I did not check the cancel steps on Learn. Check the terms you accepted.

Keep for later labs: `testuser1`, `TestUsers`, `emergency-access-01`, `emergency-access-02` and `EmergencyAccess`.

## Where this is used in AVD

AVD asks for MFA through exactly this kind of policy, aimed at the Azure Virtual Desktop and Windows Cloud Login apps. How the three sign-ins work is in [How Sign-in Works: Three Authentications and Single Sign-on](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/), and the full policy set-up, with sign-in frequency and prompt loops, is in [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/).

## Next lab

[Lab 7: RBAC roles](/azure-basics-labs/rbac-roles/) controls what a signed-in user is allowed to do in Azure. Conditional Access decides whether they get in. RBAC decides what they can do.

## Sources

- [What is Conditional Access?](https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview)
- [Build a Conditional Access policy](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-policies)
- [Conditional Access: Users, groups, agents, and workload identities](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-users-groups)
- [Conditional Access: Target resources](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-cloud-apps)
- [Analyze Conditional Access policy impact (report-only mode)](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-report-only)
- [Troubleshoot Conditional Access policies with the What If tool](https://learn.microsoft.com/en-us/entra/identity/conditional-access/what-if-tool)
- [Enforce Microsoft Entra multifactor authentication for Azure Virtual Desktop using Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa)
- [Security defaults in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults)
- [Manage emergency access accounts in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access)
- [Sign up for Microsoft Entra ID P1 or P2 editions](https://learn.microsoft.com/en-us/entra/fundamentals/get-started-premium)
- [Require multifactor authentication for all users](https://learn.microsoft.com/en-us/entra/identity/conditional-access/howto-conditional-access-policy-all-users-mfa)
