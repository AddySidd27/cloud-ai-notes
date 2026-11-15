---
title: "Azure RBAC: Give a Group Reader and Contributor, Then Test It"
seoTitle: "Azure RBAC for Beginners: Reader, Contributor, Scope"
layout: post.njk
permalink: "/azure-basics-labs/rbac-roles/"
order: 317
tags: [azure-basics-lab]
deck: "You give the TestUsers group Reader on the subscription and Contributor on one resource group, then sign in as the test user and see exactly what that allows."
description: "Beginner Azure lab: assign Reader and Contributor to a group at two scopes, check inherited access, test as a user, and learn why Owner is not Contributor."
---

By the end of this lab the group `TestUsers` will have Reader on your subscription and Contributor on the resource group `rg-azb-core`. You will have looked at that access in **Check access**, signed in as `testuser1` and seen what the user can and cannot do, and then removed both assignments again.

## What you need

- [Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway subscription.
- [Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): the resource group `rg-azb-core`.
- [Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the user `testuser1` and the group `TestUsers` with `testuser1` as a member.
- [Multifactor authentication (MFA)](/azure-basics-labs/mfa/): `testuser1` is registered for the Authenticator app, so the private-window sign-in works.
- For the CLI part: Cloud Shell or the Azure CLI from the [Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) lab, version 2.76 or newer.
- A private browser window (InPrivate in Edge, Incognito in Chrome).
- A role that can assign roles: Owner or User Access Administrator on the subscription. As the creator of the free account you are already Owner. If **Add role assignment** is grayed out for you, you do not have it. Stop and fix that first.
- Time: about 50 minutes. Cost: nothing. Role assignments are free.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top of the portal before you assign anything.
- Do not assign Owner to anyone at subscription scope. Owner can do everything, including give access to others. Keep subscription owners to a maximum of 3, avoid privileged roles where a normal job role is enough, and use a narrow scope if you must.
- Assign to the group `TestUsers`, not to the user. Groups are better than single users.
- The subscription-level Reader assignment is temporary. You remove it at the end.
- Do not give `testuser1` any role on `rg-azb-core` other than the ones in this lab.
- Contributor on `rg-azb-core` can change or delete things in it, including the action group `ag-azb-email` from the resource group lab. The budget `budget-azb-core` is on the subscription, not in this group, so this role does not cover it. You remove the Contributor assignment at the end anyway.
- Azure already requires MFA for Azure management work. If `testuser1` is asked for it, that is expected.

## What the lab builds

![The group TestUsers, with member testuser1, gets two roles. First: Reader at the subscription, which is inherited by the resource group rg-azb-core inside it. Second: Contributor on rg-azb-core. As a result testuser1 can change a tag in rg-azb-core but cannot add a role assignment there, and cannot create a new resource group.](/img/basics/rbac-roles.svg)

*Based on the pages listed under Sources. Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: a role assignment has three parts.** Azure role-based access control (Azure RBAC) decides who can do what in Azure. Every role assignment has three elements:

- **Who.** A user, a group, a service principal (an identity for an app) or a managed identity (an identity Azure manages for a resource). Here it is the group `TestUsers`.
- **Which role.** A role is a named set of permissions, such as read, write and delete. Reader and Contributor are built-in roles, which means Microsoft already made them.
- **Where.** The scope. There are four levels, from wide to narrow: management group, subscription, resource group, resource. In this lab you use two of them: the subscription and one resource group.

Access is granted by creating a role assignment and taken away by removing it. Owner or Contributor on a virtual machine does not let you sign in to it. The Windows VM sign-in lab uses the role Virtual Machine User Login for that.

**The roles you use here:**

- **Reader**: "View all resources, but does not allow you to make any changes."
- **Contributor**: "Grants full access to manage all resources, but does not allow you to assign roles in Azure RBAC".
- **Owner**: "Grants full access to manage all resources, including the ability to assign roles in Azure RBAC."

The difference between Contributor and Owner is one thing: Contributor cannot give other people access, and Owner can. That is why the lab uses Contributor and never Owner. Owner and User Access Administrator are privileged administrator roles.

`rg-azb-core` is used for the Contributor assignment because it already exists from the resource group lab. `rg-azb-lab` is created later, in the [virtual network lab](/azure-basics-labs/virtual-network-subnet/). `rg-azb-core` holds only the action group, so the damage a Contributor could do is small, but it is not zero. Do not put anything else you care about in it.

### Reader on the subscription

1. Sign in to the [Azure portal](https://portal.azure.com) as your admin account. Check the tenant name at the top right.
2. Search for **Subscriptions** and open your test subscription.
3. Select **Access control (IAM)**. IAM means identity and access management. It is the page where you give people roles.
4. Select **Add** > **Add role assignment**.
5. On the **Role** tab, stay on **Job function roles**, search for `Reader` and select **Reader**. (**Job function roles** are roles for general Azure resource management. If you do not find Reader there, use the search box.) Select **Next**. Do not use the **Privileged administrator roles** tab for this step.
6. On the **Members** tab, leave **Assign access to** on **User, group, or service principal**. Select **Select members**, type `TestUsers`, select the group, then select **Select**.
7. Optional: in **Description** type `temporary`. It helps when you clean up. Select **Next**.
8. If you see a **Conditions** or **Assignment type** tab, leave the defaults. An **Assignment type** tab only appears with a Microsoft Entra ID P2 or Governance license. If it appears, keep **Active** and **Permanent**.
9. Select **Review + assign**, then **Review + assign** again.

Check: on the **Role assignments** tab for the subscription, `TestUsers` is listed under **Reader**. It can take a few moments to show.

### Contributor on rg-azb-core

**Idea 2: inheritance.** Scopes are parent and child, and lower levels inherit role permissions from higher levels. A subscription holds resource groups, so a role you give on the subscription also applies in `rg-azb-core`. A role given on `rg-azb-core` does not go up to the subscription.

10. Search for **Resource groups** and open `rg-azb-core`.
11. Select **Access control (IAM)**, then **Add** > **Add role assignment**.
12. On the **Role** tab, select the **Privileged administrator roles** tab. Despite the name, Contributor is listed there. Select **Contributor**, then **Next**.
13. On **Members**, choose **User, group, or service principal**, select `TestUsers`, then **Select**. Add the description `RBAC test`. Select **Next**.
14. Select **Review + assign**, then **Review + assign** again.

Check: `rg-azb-core` > **Access control (IAM)** > **Role assignments** lists `TestUsers` twice. Contributor has **This resource** in the **Scope** column. Reader has **(Inherited)** next to the subscription.

### See the access in Check access

**Idea 3: access adds up.** Azure RBAC is an additive model, so the effective permissions are the sum of all the role assignments. Roles add up: if a user gets Reader from one assignment and Contributor from another, they have both. Assign at the smallest scope that works. Reader above plus Contributor below gives Contributor on `rg-azb-core`, and only Reader everywhere else in the subscription. The mirror example: Contributor on the subscription plus Reader on a resource group is still Contributor, and the Reader assignment changes nothing. A narrower scope cannot take access away. There is no "less than inherited".

15. On `rg-azb-core` > **Access control (IAM)**, open the **Check access** tab and select **Check access**.
16. Choose **User, group, or service principal**. Search for `TestUsers` and select it.
17. Read the pane that opens. It shows the access at this scope and inherited to this scope.
18. Do the same for the user `testuser1`. The user gets the same two roles through the group.

Check: the pane for `TestUsers` shows Reader inherited from the subscription and Contributor on this resource group.

If you want to see which assignments the group has in the whole subscription, open **Microsoft Entra ID** > **Groups**, select `TestUsers`, then **Azure role assignments**. That pane lists the roles at several scopes.

The **Check access** pane also lists deny assignments. These come from Azure Blueprints or managed applications. If a deny assignment applies, access is blocked even when a role allows it. You have none in this lab.

### Sign in as testuser1 and test

Tip: role changes only show up after a fresh sign-in. Use one private window for `testuser1`. After each role change, select the profile picture, **Sign out**, and sign in again. If a tag change still fails right after a role change, wait 2 minutes, sign out, sign in. This is normal.

19. Open a private window. Go to `https://portal.azure.com` and sign in as `testuser1`. Approve the MFA prompt from the MFA lab. If the portal looks empty or the role does not seem to apply, sign out and sign in again. The sign-in token carries the user's group memberships, so a fresh sign-in is the safe way to pick up changes.
20. Search for **Subscriptions**. Your subscription is listed. That is the subscription-level Reader.
21. Search for **Resource groups**. `rg-azb-core` is listed.
22. Open `rg-azb-core` > **Tags**. Add a tag `rbac-test` with the value `testuser1` and select **Apply** (or **Save**, depending on the page). Contributor can change the group, so this should work.
23. Open `rg-azb-core` > **Access control (IAM)**. Select **Add**. If you do not have permission to assign roles, **Add role assignment** is disabled. Contributor cannot assign roles, so expect it to be disabled or to fail.
24. Search for **Resource groups** and select **Create**. Try to create a group named `rg-azb-denied` in the same region as `rg-azb-core`. Creating a resource group is a change at subscription level, and the user only has Reader there. Expected result: a red message that says you do not have authorization to perform the action. The wording can differ. If the group is created, delete it and re-check the Reader assignment on the subscription. The usual causes are a role given at the wrong scope, or being signed in as the wrong user: check the user name at the top right.

Check: step 22 worked. Steps 23 and 24 were refused. Same user, same group, two different results, because of scope.

**Try removing Contributor.**

25. Close the private window. In the admin window, go to `rg-azb-core` > **Access control (IAM)** > **Role assignments**, tick the Contributor assignment for `TestUsers` and select **Remove**. Confirm with **Yes**.
26. Wait a minute. Sign in as `testuser1` in a fresh private window and try to add a second tag to `rg-azb-core`, with the name `owner` and the value `you`. With Reader only, the tag change should be refused.
27. Add Contributor again (steps 11 to 14), sign in as `testuser1` again, and add the same second tag (`owner` = `you`). It should work.

Check: with Reader only, the tag change is refused. With Contributor added again, it works. Contributor gave the change access. Reader inherited from the subscription is not enough.

### What Owner would have done

Do not do this step. It is here so you understand the choice. If `TestUsers` had Owner on the subscription, `testuser1` could create or delete anything in the whole subscription and give access to anyone else. The rule to keep is least privilege: the smallest role, at the smallest scope, that does the job.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from the Cloud Shell lab. The commands do the same as the portal steps. Do either the portal steps or the CLI steps, not both. If you already did the portal steps, do not run the `create` commands again, because the assignments exist. Use the `list` commands to see them. Check the subscription first.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
SUB_ID=$(az account show --query id -o tsv)
RG=rg-azb-core
TESTUSERS_ID=$(az ad group show --group "TestUsers" --query id -o tsv)
echo "$TESTUSERS_ID"
```

A role assignment to a group needs the group's object ID, and `az ad group show --query id` returns it. `--assignee-principal-type` tells Azure what kind of identity the ID belongs to. Use it together with `--assignee-object-id` to avoid errors caused by propagation latency in Microsoft Graph. `Group` is an accepted value.

Create the two assignments. `--scope` is the long path of the scope: `/subscriptions/{id}` for the subscription and `/subscriptions/{id}/resourceGroups/{name}` for a resource group.

```bash
az role assignment create \
  --assignee-object-id "$TESTUSERS_ID" \
  --assignee-principal-type Group \
  --role "Reader" \
  --scope "/subscriptions/$SUB_ID"

az role assignment create \
  --assignee-object-id "$TESTUSERS_ID" \
  --assignee-principal-type Group \
  --role "Contributor" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG"
```

Check: list everything the group has in this subscription. By default `az role assignment list` shows only assignments at subscription scope, so `--all` is needed to see the one on the resource group.

```bash
az role assignment list --assignee "$TESTUSERS_ID" --all \
  --query "[].{role:roleDefinitionName, scope:scope}" -o table
```

You should see two rows: Reader with the subscription path, and Contributor with the path that ends in `rg-azb-core`.

To see what applies at the resource group, including what comes from the parent scope, give the scope and add `--include-inherited`. That flag includes assignments applied on parent scopes.

```bash
az role assignment list --assignee "$TESTUSERS_ID" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG" --include-inherited \
  --query "[].{role:roleDefinitionName, scope:scope}" -o table
```

A tip for scripts: use the role's ID instead of its name, because a name can change and an ID does not. The Contributor ID is `b24988ac-6180-42a0-ab88-20f7382dd24c`. This lab uses names so you can read the commands.

## Terraform

No Terraform in this lab, because Terraform is only taught in [Terraform basics](/azure-basics-labs/terraform-basics/). The `azurerm_role_assignment` resource does this lab's work. A ready block for it is at the end of that lab, in "Try it yourself".

## Check that it works

- `rg-azb-core` > **Access control (IAM)** > **Check access** for `TestUsers` shows Reader inherited from the subscription and Contributor at the resource group.
- As `testuser1` in a private window, the subscription and `rg-azb-core` are visible.
- As `testuser1`, changing a tag on `rg-azb-core` works.
- As `testuser1`, **Add role assignment** on `rg-azb-core` is disabled or refused.
- As `testuser1`, creating a new resource group is refused.
- With the Contributor assignment removed, the tag change is refused. With it added back, it works again.

## The most common mistake

Assigning a role to the wrong scope, usually the subscription when you meant one resource group. Everything inherits from the subscription, so a Contributor given there reaches every resource group in it, and this lab would give `TestUsers` Contributor in every resource group. The second mistake is the same thing with Owner. Before you select **Review + assign**, read the scope line on the review tab. If you gave the wrong scope, remove the assignment at that scope and add the right one. You cannot remove an inherited assignment from a child scope. If you see that message, use the link next to **(Inherited)** in the **Scope** column to open the scope where it was assigned.

A third one: expecting a role to take effect to the second. If a user still lacks access right after you assign, wait a little and have the user sign in again.

## Clean up

Remove the subscription-level Reader first. It is the broader of the two, and you do not need it again.

In the portal: open the subscription > **Access control (IAM)** > **Role assignments**, tick `TestUsers` under **Reader**, select **Remove**, then **Yes**.

With the CLI:

```bash
az role assignment delete --assignee "$TESTUSERS_ID" --role "Reader" \
  --scope "/subscriptions/$SUB_ID"
```

Check: `az role assignment list --assignee "$TESTUSERS_ID" --all -o table` no longer lists the subscription scope.

Then remove Contributor on `rg-azb-core` as well. If a later lab needs it, that lab will tell you to add it.

In the portal: open `rg-azb-core` > **Access control (IAM)** > **Role assignments**, tick `TestUsers` under **Contributor**, select **Remove**, then **Yes**.

With the CLI:

```bash
az role assignment delete --assignee "$TESTUSERS_ID" --role "Contributor" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG"
```

Check: `az role assignment list --assignee "$TESTUSERS_ID" --all -o table` lists no rows. If you opened a new Cloud Shell, set `SUB_ID`, `RG` and `TESTUSERS_ID` again first (see the CLI section).

Also remove the test tags: in the portal, open `rg-azb-core` > **Tags**, delete `rbac-test` and `owner`, and apply.

Keep for later labs:

- The group `TestUsers` with `testuser1`, from the users and groups lab.
- `rg-azb-core`, with its action group, and the budget `budget-azb-core` on the subscription.
- A note that nobody has Owner at subscription scope except your own admin account. If you gave Owner to anyone else, remove it now.

Nothing in this lab costs money.

## Where this is used in AVD

In AVD, a user sees a desktop only after a group has the role Desktop Virtualization User on the application group. You assign it to a group, at the application group scope, in the AVD series. The habit from this lab (small role, small scope, assign to groups) is what keeps an AVD estate safe. The full list of AVD roles is in [Who Can Administer Azure Virtual Desktop: Roles, Scopes and Delegation](/azure-virtual-desktop/who-can-administer-azure-virtual-desktop/).

## Next lab

[Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/) creates the resource group `rg-azb-lab` and the network that your virtual machines will sit in.

## Sources

- [What is Azure role-based access control (Azure RBAC)?](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview)
- [Assign Azure roles using the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal)
- [Assign Azure roles using Azure CLI](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-cli)
