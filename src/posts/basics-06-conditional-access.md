---
title: "Conditional Access: A Safe First Policy That Asks for MFA"
seoTitle: "Conditional Access for Beginners: Safe Report-only MFA Policy"
layout: post.njk
permalink: "/azure-basics-labs/conditional-access/"
order: 316
tags: [azure-basics-lab]
deck: "You build one Conditional Access policy that asks the test group for MFA when they use Azure Virtual Desktop, you test it in report-only mode first, and you delete it at the end."
description: "Beginner Azure lab: build a safe Conditional Access policy in report-only mode for a test group and the two AVD apps, test it with What If, then delete it."
---

By the end of this lab you will have created one Conditional Access policy for a test group, checked it with the What If tool and the sign-in log in report-only mode, switched it on for that group only, switched it off again, and deleted it.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

Conditional Access is a set of rules in Microsoft Entra ID. A rule reads like an if-then sentence: if this user wants to use this app, then they must do this first. Learn gives the example "if a user wants to access Microsoft 365, then they must do multifactor authentication". Multifactor authentication (MFA) was the topic of [Lab 5: Multifactor authentication (MFA)](/azure-basics-labs/mfa/).

A bad Conditional Access rule can lock every admin out of a tenant. That is why this lab has more safety steps than most. Do them in order. Do not skip any.

**Before you start:** this lab needs a Microsoft Entra ID P1 or P2 licence. The free tenant does not have it. Part 0 shows how to start a trial and read its terms first. If no trial is available to you, skip to [Lab 7](/azure-basics-labs/rbac-roles/). No later lab needs this one.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway tenant and a Global Administrator sign-in for it.
- [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the test user `testuser1` (with a usage location set), the group `TestUsers` (with `testuser1` in it), the two emergency accounts `emergency-access-01` and `emergency-access-02` with the passwords you saved, and the group `EmergencyAccess` (with both accounts in it).
- [Lab 5: Multifactor authentication (MFA)](/azure-basics-labs/mfa/): `testuser1` registered for the Authenticator app, per-user MFA left at **Disabled**, and your note of what security defaults showed.
- A Microsoft Entra ID P1 or P2 licence. This is the part most people do not have yet. Part 0 below shows how to get a trial and how to assign it.
- A phone with the Microsoft Authenticator app, the same one you used in Lab 5.
- A private browser window (InPrivate in Edge, Incognito in Chrome).
- Role: Learn says at least the Conditional Access Administrator role to create policies. Global Administrator covers it.
- Time: about 90 minutes. Do it in two sittings: Parts 0 to 5, then Parts 6 and 7. Cost: nothing from Azure. A trial or licence has its own terms, see Part 0.

## Safety first

- Throwaway test tenant only. Never an employer tenant, never a real one. Read the tenant name at the top right before you change anything.
- Write on your notes sheet: "security defaults were ON" or "security defaults were OFF". You need it in Clean up.
- Stop check. Before you create the policy, every line in the "Stop check" list below must be true. If one is not true, stop. Do not create the policy.
- The emergency account `emergency-access-01` must be proven to sign in, and both emergency accounts must be excluded through the group `EmergencyAccess`.
- Create the policy in **Report-only** first. Learn says report-only policies are evaluated but not enforced.
- Scope: the group `TestUsers` only. Never **All users**.
- Exclude the admin account you work from, and the group `EmergencyAccess`.
- Target only two apps: Azure Virtual Desktop and Windows Cloud Login. Never **All resources** (older name: **All cloud apps**). Do not add the Azure Virtual Desktop Azure Resource Manager Provider app or the Windows 365 app to this policy.
- Grant control: **Require multifactor authentication**. Never **Block access**.
- Turning security defaults off lowers the protection of the whole tenant. Learn says you must do it before you can use Conditional Access. Read "Idea 1" before you do it.
- At the end, delete the policy. Learn says that when the licence expires, policies are not removed, and you can view and delete them but you cannot update them. A policy you cannot edit is a policy you cannot fix.

## What the lab builds

![The group TestUsers is included in one Conditional Access policy. The group EmergencyAccess and your admin account are excluded, and exclude wins. The policy reads as a rule: if the user is in TestUsers and opens Azure Virtual Desktop or Windows Cloud Login, then require multifactor authentication. Its state goes Report-only, On, Off, then Delete. The What If tool simulates a sign-in against the policy, and the policy's report-only result shows in the sign-in log. Never use All users or All resources.](/img/basics/conditional-access.svg)

*Source: [Require multifactor authentication for Azure Virtual Desktop using Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa), [Build a Conditional Access policy](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-policies), [Analyze Conditional Access policy impact](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-report-only) and [What If tool](https://learn.microsoft.com/en-us/entra/identity/conditional-access/what-if-tool). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

This lab uses the Microsoft Entra admin center at `https://entra.microsoft.com`, not the Azure portal. Learn writes the Conditional Access steps for that site. The title "Steps in the Azure portal" is the same for every lab. Learn's menu path is **Entra ID** > **Conditional Access** > **Policies**. Some older Learn pages say **Protection** > **Conditional Access**. It is the same place.

### Part 0: Get the licence

The free Entra tier does not include Conditional Access. You need Microsoft Entra ID P1 or P2 in your tenant, and `testuser1` needs the licence assigned.

1. Learn's page [Sign up for Microsoft Entra ID P1 or P2 editions](https://learn.microsoft.com/en-us/entra/fundamentals/get-started-premium) links to the **Microsoft Entra ID P2 Trial**. Open that link from the Learn page and sign in with your Global Administrator account from Lab 1. Read what the sign-up page says before you accept anything: how long the trial lasts, whether it asks for a card, whether it renews. Write the end date on your notes sheet. I did not run the sign-up, so I cannot show you its screens.
2. If no trial is offered to you, or the page asks for something you do not have, stop here and go to [Lab 7: Azure RBAC roles](/azure-basics-labs/rbac-roles/). No later lab needs this one.
3. After the trial starts, go to `https://entra.microsoft.com` and sign in again. Check the tenant name at the top right: it must be your throwaway tenant. Open **Billing** > **Licenses** > **All products**. Learn says this page lists the product licences in the tenant. You should see **Microsoft Entra ID P2**.
4. Assign the licence to `testuser1`. Learn says licences are assigned in the Microsoft 365 admin center, at `https://admin.microsoft.com`. Go to **Users** > **Active users**, select `testuser1`, select **Licenses and Apps** in the pane on the right, expand **Licenses**, tick **Microsoft Entra ID P2** and select **Save changes**. If the save fails, the most likely reason is a missing usage location. Learn lists an invalid usage location as a common reason. Set it on the user (Lab 4, step 5) and try again.

Check: back in the Entra admin center, open **Entra ID** > **Users** > **All users** > `testuser1` > **Licenses**. It lists **Microsoft Entra ID P2**.

### Part 1: Stop check

5. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) as your Global Administrator. Read the tenant name at the top right.
6. Check the licence. Open **Entra ID** > **Conditional Access** > **Policies**. If the page opens and offers **New policy**, the tenant has the licence for it. If **New policy** is missing or greyed out, or the page offers a trial or a purchase link, go back to Part 0. If it still does not show after you assigned the licence, sign out, sign in again and look again.
7. Check the groups. Go to **Entra ID** > **Groups** > **All groups**. Open `TestUsers`: it must hold `testuser1` and must not hold your admin account. Open `EmergencyAccess`: it must hold both emergency accounts.
8. Prove that `emergency-access-01` can sign in with MFA. This is a planned test, so it is allowed. Lab 4 left this test to this lab. This is the check that tells you the exclusion works before you need it. Do these sub-steps:
    - Open a private window. Go to `https://aka.ms/mysecurityinfo`. This is the Security info page, where a user manages their sign-in methods. Sign in as `emergency-access-01` (full name ending in `.onmicrosoft.com`) with the password you saved in Lab 4.
    - If the account already has a method from Lab 4 (a passkey or the Authenticator app), use it and go on to the last sub-step.
    - If the page asks you to set up MFA, follow its prompts. If it opens Security info without asking, select **Add sign-in method** (the button may read **Add method**), choose **Authenticator app** and select **Add**. Install Microsoft Authenticator on your phone if you have not. In the app, add a **Work or school account** and follow the page to link it, usually by scanning a QR code. These are the same steps as Lab 5, Part 2, for a different account. Select **Done**.
    - Sign out, close the private window, and open a new one. Go to `https://portal.azure.com`, sign in as `emergency-access-01`, approve the prompt on your phone, and sign out.
    - In your admin window, open **Entra ID** > **Monitoring & health** > **Sign-in logs**, and find that sign-in. It must show **Success**.
9. If the sign-in does not work, fix it first. Do not go on. Return to [Lab 4](/azure-basics-labs/entra-users-groups-break-glass/) and check the password and the Global Administrator role of the account.

My judgement, not Learn: Learn tells you to keep emergency accounts off a personal phone. In a throwaway tenant I accept it, so that you can test the account. Do not do this in a real tenant. Use a passkey on a security key there, as Lab 4 describes.

**Stop check.** All of these must be true before you go on:

- You are in the throwaway tenant, and you read its name.
- Conditional Access shows **New policy** (the licence works).
- `testuser1` is in `TestUsers`. Your admin account is not.
- Both emergency accounts are in `EmergencyAccess`.
- `emergency-access-01` signed in successfully today, and the sign-in log shows it.
- You know how to turn a policy off (Part 6) and how to delete it (Part 7).

If any line is false, stop. Nothing in this lab is worth a lockout.

### Part 2: Security defaults must be off

**Idea 1: security defaults and Conditional Access cannot be on together.** Security defaults are one on/off bundle of MFA rules from Microsoft. Conditional Access replaces it with rules you write yourself, so Learn says you turn the bundle off first, and the Azure Virtual Desktop page says Conditional Access policies cannot be used while security defaults are on.

What turning them off means for you: the bundle stops, and nothing replaces it until you add policies. Learn says to enable Conditional Access policies straight after disabling, and that Microsoft-managed Conditional Access policies exist that keep the same protections. Azure's own mandatory MFA from Lab 5 is a separate rule with no opt-out, so your admin sign-in still asks for MFA. The policy in this lab protects only the test group and only two apps. For a throwaway tenant that is acceptable. In a real tenant you would not do this without a plan and the security owner's agreement.

10. Go to **Entra ID** > **Overview** > **Properties**, then select **Manage security defaults**.
11. Read the setting. If it already says **Disabled (not recommended)**, write "security defaults were OFF" on your notes sheet, close the pane and go on. If it says **Enabled**, write "security defaults were ON", set **Security defaults** to **Disabled (not recommended)**, and select **Save**. If the portal asks you to choose a reason, pick the one that says you use Conditional Access, if there is one. These are the words and steps on Learn's security defaults page.
12. Open **Entra ID** > **Conditional Access** > **Policies**. Learn says Microsoft-managed Conditional Access policies are available to keep the same protections after you disable security defaults. If any appear in the list, leave them alone. Learn says you cannot rename or delete Microsoft-managed policies. Do not change them in this lab.

Check: **Manage security defaults** shows **Disabled (not recommended)**.

**Checkpoint 1.** Security defaults are off and nothing else has changed. You can stop here and come back later. If you stop for a long time, turn security defaults back on (Clean up, step 2) and start again from Part 2.

### Part 3: Create the policy in report-only mode

**Idea 2: exclude beats include.** Learn says that when a user or group is both included and excluded, the user is excluded: the exclude action overrides the include. That is why your admin account and `EmergencyAccess` go in the exclude list, even though neither is in `TestUsers`. It is a second lock on the same door.

**Idea 3: which apps.** AVD sign-in goes through two Entra apps. Pick these two and nothing else:

| App to pick | App ID | What it covers |
|---|---|---|
| **Azure Virtual Desktop** | `9cdead84-a844-4324-93f2-b2e6bb768d07` | Signing in to the AVD service. |
| **Windows Cloud Login** | `270efc09-cd0d-444b-a71f-39af4910ec45` | Signing in to the VM itself, when single sign-on is on. |

Learn says do not pick **Azure Virtual Desktop Azure Resource Manager Provider** (app ID `50e95039-b200-4007-bc97-8d5790743a63`): it only fetches the feed and must not have MFA. Learn also warns that a policy that blocks the **Windows 365** app (app ID `0af06dc6-e4b5-4f28-818e-e78e62d137a5`) breaks sign-in for AVD users, so leave that app out too. Learn recommends one policy per app in a real deployment, so that sign-in frequency can differ. This lab sets no sign-in frequency, so one policy with both apps keeps it short. The two-policy layout is in [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/).

13. In **Entra ID** > **Conditional Access** > **Policies**, select **New policy**.
14. **Name**: `CA-Lab6-AVD-RequireMFA-TestUsers`. A name that says what it does and who it is for helps when you come back later.
15. Under **Assignments**, open the users section (**Users or workload identities**, or **Users**; the label depends on the page).
16. Under **Include**, choose **Select users and groups**, tick **Users and groups**, and select the group `TestUsers`. Do not choose **All users**. Select **Select**.
17. Under **Exclude**, choose **Users and groups**. Select your own admin account and the group `EmergencyAccess`. Select **Select**.
18. Open **Target resources**. Leave the first drop-down on **Resources (formerly cloud apps)**. Under **Include**, choose **Select resources**.
19. Search for the apps. Learn says to type the start of the app name in order. Type `Azure Virtual` and select **Azure Virtual Desktop**. Check that the app ID shows `9cdead84-a844-4324-93f2-b2e6bb768d07`. Then search `Windows Cloud` and select **Windows Cloud Login**. Check the ID `270efc09-cd0d-444b-a71f-39af4910ec45`. Select **Select**.
20. If **Azure Virtual Desktop** is not in the list, also search `Windows Virtual Desktop`. Learn says that is the app's old name, with the same app ID. If either app is still missing, stop here. Learn says a Microsoft cloud app appears in the list only when its service principal exists in your tenant, and Learn's AVD page tells you to confirm both apps exist in your tenant before you use them. Do not switch to **All resources** to get around it. Read "The most common mistake".
21. Leave **Conditions** and **Network** alone. Learn says a new policy applies to all client app types by default.
22. Under **Access controls** > **Grant**, choose **Grant access**, tick **Require multifactor authentication**, and select **Select**. Do not choose **Block access**.
23. At the bottom, set **Enable policy** to **Report-only**. Select **Create**. (Learn's AVD page shows **On** here. This lab uses **Report-only** on purpose, as other Learn pages do.)

Check: the policy appears in the list with the state **Report-only**. Open it and read the settings back, top to bottom, against steps 16 to 23. Read slowly. Wrong scope is the mistake that matters.

### Part 4: Ask the What If tool

The What If tool simulates a sign-in and tells you which policies would apply. It does not change the policy. Learn says only policies that are enabled or in report-only mode are included. Learn also says the What If tool needs four conditions: identity, target resource, device platform and client app. Without all four it cannot give a complete answer.

24. On **Policies**, select **What If** in the toolbar.
25. Set the user to `testuser1`.
26. Set the target resource to **Azure Virtual Desktop**. Learn says to provide the App ID for the application and that groups of apps such as **Office 365** do not match. If searching by name finds nothing, enter the app ID `9cdead84-a844-4324-93f2-b2e6bb768d07`. For **Windows Cloud Login** use `270efc09-cd0d-444b-a71f-39af4910ec45`.
27. Set the device platform to **Windows**. The field label may read **Device platforms**.
28. Set the client app to **Mobile apps and desktop clients**.
29. Leave the optional conditions empty. Learn says they are treated as none.
30. Select **What If**. Look at the two lists. Your policy should be under policies that apply, with **Require multifactor authentication** as the grant control.
31. Run the tool again for each of these, and write down what you see:
    - `testuser1`, target **Windows Cloud Login**: the policy should apply.
    - `testuser1`, target **Azure Virtual Desktop**, client app **Browser**: the policy should apply.
    - `emergency-access-01`, target **Azure Virtual Desktop**: the policy should be under policies that do not apply. Learn says the list gives the reason, the first condition that was not satisfied. Read the reason. It should point at the user or group exclusion. If it points at something else, stop and read the policy settings back.
    - Your admin account, target **Azure Virtual Desktop**: same, not applied.

Check: the policy applies to `testuser1` on both apps and does not apply to the emergency account or to your admin.

### Part 5: Look at the sign-in log, Report-only tab

Learn says that during sign-in the system evaluates report-only policies without enforcing them, and that the results show in the **Conditional Access** and **Report-only** tabs of the sign-in log details.

32. In a private window, sign in as `testuser1` at `https://portal.azure.com`. Approve the MFA prompt if you get one, as in Lab 5. This is an ordinary sign-in, not an AVD sign-in.
33. In your admin window, go to **Entra ID** > **Monitoring & health** > **Sign-in logs**. Find that sign-in and open it. Learn says each event shows which policies were enabled, in report-only mode, applied or not applied.
34. Open the **Report-only** tab. Look for `CA-Lab6-AVD-RequireMFA-TestUsers`. You should see it listed with **Report-only: Not applied**. That is the expected result. This sign-in was to the Azure portal and not to AVD, so the policy should not have applied. Learn defines **Report-only: Not applied** as "Not all configured policy conditions were satisfied", which fits, because the policy is for the two AVD apps. If the policy is not listed, check that you opened a sign-in made after you created the policy.

In the same tab, **Report-only: Failure** means the policy would have blocked the sign-in or required something that was not met. Learn lists **Report-only: User action required** for a policy that would need the user to do MFA, and says that in report-only mode the user is not prompted.

**The honest limit.** Without an AVD deployment, you cannot see a real AVD sign-in and its MFA prompt. What you have is the What If result and a log that shows the policy was seen and did not apply to a portal sign-in. The AVD articles [How Sign-in Works: Three Authentications and Single Sign-on](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/) and [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/) show the full flow.

Check: the policy is listed on the **Report-only** tab with **Not applied**, and the emergency account's earlier sign-in still shows **Success**.

**Checkpoint 2.** The policy exists in Report-only, and nothing is enforced. You can stop here. Do not leave the policy overnight: do Parts 6 and 7 next, or at least Part 7. Part 6 is optional if you are short of time. Part 7 is not optional.

### Part 6: Enable it for the test group only, then roll back

35. Open the policy. Check once more: Include is `TestUsers` only, Exclude is your admin and `EmergencyAccess`, apps are the two AVD apps, Grant is **Require multifactor authentication**.
36. Learn says to move the **Enable policy** toggle from **Report-only** to **On** after you have confirmed the settings with report-only mode. Set it to **On**. Select **Save**.
37. Run the What If tool again for `testuser1` on **Azure Virtual Desktop**. The policy should still apply, now enforced. Run it for `emergency-access-01`. It should still not apply.
38. Close all private windows first. Then open a new private window and sign in as `emergency-access-01` once more at `https://portal.azure.com`. It must succeed. This is the proof that the policy did not lock out the emergency account. Sign out.
39. Rollback. Open the policy and look at **Enable policy**. The switch has three positions: **Report-only**, **On** and **Off**. Set it to **Off** and select **Save**. If you do not see **Off**, go straight to Part 7 and delete the policy. Check that the list shows the policy as off, or that it is gone.

Check: the policy went **Report-only**, **On**, then off, and each time you read the state in the list.

### Part 7: Delete the policy

40. Go back to the policy list. Select the policy name, then select **Delete** in the toolbar and confirm. If you cannot find **Delete**, look in the **...** menu on the policy's row.
41. Check that the list no longer shows it. If Microsoft-managed policies were there before, they should still be there.

Check: no policy named `CA-Lab6-AVD-RequireMFA-TestUsers` remains.

## Steps with the Azure CLI

No CLI in this lab, on purpose. Conditional Access lives in Microsoft Entra, and the safe way to do it the first time is in the portal. The portal shows the warnings (for example, "Don't lock yourself out"), lets you read the scope back on screen, and has the What If tool. A script would create the policy in one step with no one reading the scope. I did not find a Learn page that creates a Conditional Access policy with `az`.

There are other ways. Microsoft Graph has Conditional Access APIs, and Learn's What If page links to one of them (the What If evaluation API). They are out of scope here.

## Terraform

No Terraform in this lab, because a Conditional Access policy is a tenant-wide change that needs a human to check the scope first, and I have not checked any Terraform for this on Learn. Terraform is covered in [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/) with ordinary Azure resources.

## Check that it works

- Security defaults show **Disabled (not recommended)** and you know why.
- You proved that `emergency-access-01` can sign in, and you did it again with the policy **On**.
- The What If tool shows the policy applying to `testuser1` on both AVD apps, and not applying to the emergency account or your admin.
- The sign-in log shows the policy on the **Report-only** tab, with **Not applied** for a portal sign-in.
- You set the policy to **Off** (or went straight to delete), then deleted it.

## The most common mistake

Choosing **All users** and **All resources** because the picker did not show the AVD apps, or because it was faster. A policy like that, with MFA, hits every user on every app. If the emergency accounts are not excluded, it can lock out everyone. Learn shows a warning for exactly this: "Don't lock yourself out! Apply a policy to a small set of users first to verify it behaves as expected. Also exclude at least one admin from this policy."

If the AVD apps are not in the list, stop. Learn says some apps do not appear in the picker at all, and that the only ways around it are **All resources** or adding the missing service principal with PowerShell or Graph. This lab takes neither way. Leave the lab for when you have an AVD deployment.

A second mistake: leaving the policy behind. If the licence ends, Learn says the policy stays, and you can view and delete it but not update it.

## Clean up

1. Delete the policy (Part 7).
2. Look at your notes sheet. If security defaults were ON when you started, turn them back on now: **Entra ID** > **Overview** > **Properties** > **Manage security defaults** > **Enabled** > **Save**. Learn says the two cannot be used together, so do this only after the delete. If they were already OFF, leave them off.
3. If you started a trial or bought a licence only for this lab, write its end date on your notes sheet and set a reminder two days before it. Check on the sign-up page whether the trial renews or asks for a card. I did not check the cancel steps on Learn. To end it early, look in the Microsoft 365 admin center under **Billing** > **Your products** for the trial and a cancel option. Learn's sign-up page is the place to confirm what you accepted.

Check: **Manage security defaults** shows the same state as at the start (or you decided to leave it off in this throwaway tenant), and the policy list no longer shows your policy.

Keep for later labs: `testuser1`, `TestUsers`, `emergency-access-01`, `emergency-access-02` and `EmergencyAccess`.

## Where this is used in AVD

AVD asks for MFA through exactly this kind of policy, aimed at the Azure Virtual Desktop and Windows Cloud Login apps. How the three sign-ins work is in [How Sign-in Works: Three Authentications and Single Sign-on](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/), and the full policy set-up, with sign-in frequency and prompt loops, is in [Secure Access with Conditional Access and Multifactor Authentication](/azure-virtual-desktop/conditional-access-and-mfa-for-avd/).

## Next lab

[Lab 7: Azure RBAC roles](/azure-basics-labs/rbac-roles/) controls what a signed-in user is allowed to do in Azure. Conditional Access decides whether they get in. RBAC decides what they can do.

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
