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

I have not run these steps in a live tenant for this article, and I have not run `terraform validate` on the Terraform block. The steps follow Microsoft Learn, and the Terraform arguments are checked against Learn's Terraform samples and provider notes.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway subscription.
- [Lab 3: Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): the resource group `rg-azb-core`.
- [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the user `testuser1` and the group `TestUsers` with `testuser1` as a member.
- [Lab 5: Multifactor authentication](/azure-basics-labs/mfa/): `testuser1` is registered for the Authenticator app, so the private-window sign-in works.
- For the CLI part: Cloud Shell or the Azure CLI from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/), version 2.76 or newer.
- A private browser window (InPrivate in Edge, Incognito in Chrome).
- A role that can assign roles. Learn says you need the `Microsoft.Authorization/roleAssignments/write` permission, which roles such as Owner, Role Based Access Control Administrator and User Access Administrator have. If **Add role assignment** is greyed out for you, you do not have it. Stop and fix that first.
- Time: about 40 minutes. Cost: nothing. Role assignments are free.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top of the portal before you assign anything.
- Do not assign Owner to anyone at subscription scope. Owner can do everything, including give access to others. Learn says to keep subscription owners to a maximum of 3, to avoid privileged roles where a normal job role is enough, and to use a narrow scope if you must.
- Assign to the group `TestUsers`, not to the user. Learn recommends groups over single users.
- The subscription-level Reader assignment is temporary. You remove it at the end.
- Do not give `testuser1` any role on `rg-azb-core` other than the ones in this lab.
- Contributor on `rg-azb-core` can change or delete things in it, including the budget and the action group from Lab 3. You remove that assignment at the end for this reason.
- Azure already requires MFA for Azure management work. If `testuser1` is asked for it, that is expected.

## What the lab builds

![A left-to-right diagram. The group TestUsers, with member testuser1, receives two role assignments. Reader is assigned at the subscription and is inherited by the resource group rg-azb-core inside it. Contributor is assigned directly on rg-azb-core. The effective access is read-only on the subscription and full management, without role assignment, on rg-azb-core.](/img/basics/rbac-roles.svg)

*Source: [What is Azure role-based access control?](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview), [Understand scope for Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview), [Assign Azure roles using the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal) and [Azure built-in roles for Privileged](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/privileged). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: a role assignment has three parts.** Azure role-based access control (Azure RBAC) decides who can do what in Azure. Learn says every role assignment has three elements:

- **Who.** A user, a group, a service principal (an identity for an app) or a managed identity (an identity Azure manages for a resource). Learn calls this the security principal. Here it is the group `TestUsers`.
- **Which role.** A role is a named set of permissions, such as read, write and delete. Reader and Contributor are built-in roles, which means Microsoft already made them.
- **Where.** The scope. Learn lists four levels, from wide to narrow: management group, subscription, resource group, resource. In this lab you use two of them: the subscription and one resource group.

Access is granted by creating a role assignment and taken away by removing it.

**The roles you use here:**

- **Reader**: "View all resources, but does not allow you to make any changes."
- **Contributor**: "Grants full access to manage all resources, but does not allow you to assign roles in Azure RBAC", and also not to manage Azure Blueprints assignments or share image galleries.
- **Owner**: "Grants full access to manage all resources, including the ability to assign roles in Azure RBAC."

The difference between Contributor and Owner is one thing: Contributor cannot give other people access, and Owner can. In the role definition Learn lists the Contributor exclusions, and creating role assignments (`Microsoft.Authorization/*/Write`) is one of them. That is why the lab uses Contributor and never Owner.

I chose `rg-azb-core` for the Contributor assignment because it already exists from Lab 3. `rg-azb-lab` is created in [Lab 8](/azure-basics-labs/virtual-network-subnet/), after this lab. `rg-azb-core` holds only the action group and the budget, so the damage a Contributor could do is small, but it is not zero. Do not put anything else you care about in it.

### Part 1: Reader on the subscription

1. Sign in to the [Azure portal](https://portal.azure.com) as your admin account. Check the tenant name at the top right.
2. Search for **Subscriptions** and open your test subscription.
3. Select **Access control (IAM)**.
4. Select **Add** > **Add role assignment**.
5. On the **Role** tab, stay on **Job function roles**, search for `Reader` and select **Reader**. (Learn describes **Job function roles** as roles for general Azure resource management. If you do not find Reader there, use the search box.) Select **Next**. Do not pick a role from the **Privileged administrator roles** tab for this step.
6. On the **Members** tab, leave **Assign access to** on **User, group, or service principal**. Select **Select members**, type `TestUsers`, select the group, then select **Select**.
7. Optional: in **Description** type `Lab 7 temporary`. It helps when you clean up. Select **Next**.
8. If you see a **Conditions** or **Assignment type** tab, leave the defaults. Learn says an **Assignment type** tab only appears with a Microsoft Entra ID P2 or Governance licence. If it appears, keep **Active** and **Permanent**.
9. Select **Review + assign**, then **Review + assign** again.

Check: on the **Role assignments** tab for the subscription, `TestUsers` is listed under **Reader**. It can take a few moments to show.

### Part 2: Contributor on rg-azb-core

**Idea 2: inheritance.** Learn says scopes are parent and child, and lower levels inherit role permissions from higher levels. A subscription holds resource groups, so a role you give on the subscription also applies in `rg-azb-core`. A role given on `rg-azb-core` does not go up to the subscription.

10. Search for **Resource groups** and open `rg-azb-core`.
11. Select **Access control (IAM)**, then **Add** > **Add role assignment**.
12. On the **Role** tab, search for `Contributor`. Learn names Contributor as an example of a **Privileged administrator role**, so select that tab first. Select **Contributor**, then **Next**.
13. On **Members**, choose **User, group, or service principal**, select `TestUsers`, then **Select**. Add the description `Lab 7`. Select **Next**.
14. Select **Review + assign**, then **Review + assign** again.

Check: `rg-azb-core` > **Access control (IAM)** > **Role assignments** lists `TestUsers` twice. Contributor has **This resource** in the **Scope** column. Reader has **(Inherited)** next to the subscription.

### Part 3: See the access in Check access

**Idea 3: access adds up.** Learn says Azure RBAC is an additive model, so the effective permissions are the sum of all the role assignments. Reader above plus Contributor below gives Contributor on `rg-azb-core`, and only Reader everywhere else in the subscription. Learn gives the mirror example: Contributor on the subscription plus Reader on a resource group is still Contributor, and the Reader assignment changes nothing. A narrower scope cannot take access away. There is no "less than inherited".

15. On `rg-azb-core` > **Access control (IAM)**, open the **Check access** tab and select **Check access**.
16. Choose **User, group, or service principal**. Search for `TestUsers` and select it.
17. Read the pane that opens. Learn says it shows the access at this scope and inherited to this scope. Assignments at child scopes are not listed.
18. Do the same for the user `testuser1`. The user gets the same two roles through the group. If the pane for the user does not list them, rely on the group result and the sign-in test in Part 4.

Check: the pane for `TestUsers` shows Reader inherited from the subscription and Contributor on this resource group.

If you want to see which assignments the group has in the whole subscription, open **Microsoft Entra ID** > **Groups**, select `TestUsers`, then **Azure role assignments**. Learn says that pane lists the roles at several scopes.

The **Check access** pane also lists deny assignments. Learn says these come from Azure Blueprints or managed applications, and that if a deny assignment applies, access is blocked even when a role allows it. You have none in this lab.

### Part 4: Sign in as testuser1 and test

19. Open a private window. Go to `https://portal.azure.com` and sign in as `testuser1`. Approve the MFA prompt from Lab 5. If the portal looks empty or the role does not seem to apply, sign out, close the window, open a new private window and sign in again. Learn says the sign-in token carries the user's group memberships, so a fresh sign-in is the safe way to pick up changes.
20. Search for **Subscriptions**. Your subscription is listed. That is the subscription-level Reader.
21. Search for **Resource groups**. `rg-azb-core` is listed.
22. Open `rg-azb-core` > **Tags**. Add a tag `rbac-test` with the value `testuser1` and select **Apply** (or **Save**, depending on the page). Contributor can change the group, so this should work.
23. Open `rg-azb-core` > **Access control (IAM)**. Select **Add**. Learn says that if you do not have permission to assign roles, **Add role assignment** is disabled. Contributor cannot assign roles, so expect it to be disabled or to fail.
24. Search for **Resource groups** and select **Create**. Try to create a group named `rg-azb-denied` in the same region as `rg-azb-core`. Creating a resource group is a change at subscription level, and the user only has Reader there. Expect an authorization error when you validate or create. The wording of the message can differ. If the group is created anyway, delete it and check your assignments.

Check: step 22 worked. Step 23 and step 24 were refused. Same user, same group, two different results, because of scope.

**Try the additive part.** Close the private window. In the admin window, go to `rg-azb-core` > **Access control (IAM)** > **Role assignments**, tick the Contributor assignment for `TestUsers` and select **Remove**. Confirm with **Yes**. Wait a minute, then repeat step 22 as `testuser1` in a fresh private window. With Reader only, the tag change should now be refused. Then add Contributor again (steps 11 to 14) before you carry on. This shows that Contributor is what gave the change access, and that Reader inherited from the subscription is not enough.

### What Owner would have done

Do not do this step. It is here so you understand the choice. If `TestUsers` had Owner on the subscription, `testuser1` could create or delete anything in the whole subscription and give access to anyone else. Learn lists Owner as a privileged administrator role. The rule to keep is least privilege: the smallest role, at the smallest scope, that does the job.

### A note on virtual machines

Owner or Contributor on a virtual machine does not let a user sign in to it. Learn says there is an intentional, audited separation between the people who manage virtual machines and the people who can sign in. Signing in needs a separate role such as **Virtual Machine User Login**, which Learn describes as "view virtual machines in the portal and sign in as a regular user". You use that role in [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/). For now you only need to know that the name exists and that Contributor does not replace it.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from Lab 2. The commands do the same as the portal steps. If you already did the portal steps, do not run the `create` commands again, because the assignments exist. Use the `list` commands to see them. Check the subscription first.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
SUB_ID=$(az account show --query id -o tsv)
RG=rg-azb-core
GROUP_ID=$(az ad group show --group "TestUsers" --query id -o tsv)
echo "$GROUP_ID"
```

Learn says a role assignment to a group needs the group's object ID, and `az ad group show --query id` is how it gets it. `--assignee-principal-type` tells Azure what kind of identity the ID belongs to. Learn's CLI reference says to use it together with `--assignee-object-id` to avoid errors caused by propagation latency in Microsoft Graph, and lists `Group` as an accepted value.

Create the two assignments. `--scope` is the long path Learn shows: `/subscriptions/{id}` for the subscription and `/subscriptions/{id}/resourceGroups/{name}` for a resource group.

```bash
az role assignment create \
  --assignee-object-id "$GROUP_ID" \
  --assignee-principal-type Group \
  --role "Reader" \
  --scope "/subscriptions/$SUB_ID"

az role assignment create \
  --assignee-object-id "$GROUP_ID" \
  --assignee-principal-type Group \
  --role "Contributor" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG"
```

Check: list everything the group has in this subscription. By default `az role assignment list` shows only assignments at subscription scope, so `--all` is needed to see the one on the resource group.

```bash
az role assignment list --assignee "$GROUP_ID" --all \
  --query "[].{role:roleDefinitionName, scope:scope}" -o table
```

You should see two rows: Reader with the subscription path, and Contributor with the path that ends in `rg-azb-core`.

To see what applies at the resource group, including what comes from the parent scope, give the scope and add `--include-inherited`. Learn's CLI reference describes that flag as including assignments applied on parent scopes.

```bash
az role assignment list --assignee "$GROUP_ID" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG" --include-inherited \
  --query "[].{role:roleDefinitionName, scope:scope}" -o table
```

A tip from Learn for scripts: use the role's ID instead of its name, because a name can change and an ID does not. The Contributor ID Learn lists is `b24988ac-6180-42a0-ab88-20f7382dd24c`. This lab uses names so you can read the commands.

## Terraform

Terraform describes a role assignment in one block. If you have not done [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/), skip this section for now. It uses the same provider setup, so you need Lab 10's `versions.tf`, `providers.tf` and `terraform.tfvars` (with your `subscription_id`) copied into a new empty folder, for example `rbac-tf`. Keep this project separate from the Lab 10 folder, so each has its own state.

Use Terraform instead of the portal or CLI steps, not on top of them. If the assignments already exist, remove them first (see Clean up), or Terraform will report that they already exist.

I have not run `terraform validate` on this code. The arguments `scope`, `role_definition_name` and `principal_id` match Learn's Terraform samples for `azurerm_role_assignment`. `principal_type` is documented with the values `User`, `Group` and `ServicePrincipal`. The `azurerm_subscription` and `azurerm_resource_group` data sources return an `id`. The group's object ID is passed in as a variable, so this block needs no second provider. Get the value with `az ad group show --group "TestUsers" --query id -o tsv` and put it in `terraform.tfvars` as `group_object_id = "..."`.

```hcl
variable "group_object_id" {
  description = "Object ID of the group TestUsers (from az ad group show)."
  type        = string
}

data "azurerm_subscription" "current" {}

data "azurerm_resource_group" "core" {
  name = "rg-azb-core"
}

resource "azurerm_role_assignment" "reader_sub" {
  scope                = data.azurerm_subscription.current.id
  role_definition_name = "Reader"
  principal_id         = var.group_object_id
  principal_type       = "Group"
}

resource "azurerm_role_assignment" "contributor_rg" {
  scope                = data.azurerm_resource_group.core.id
  role_definition_name = "Contributor"
  principal_id         = var.group_object_id
  principal_type       = "Group"
}
```

Run `terraform init`, `terraform plan` and `terraform apply` as in Lab 10. Read the plan first: it must show two assignments to add and nothing else.

## Check that it works

- `rg-azb-core` > **Access control (IAM)** > **Check access** for `TestUsers` shows Reader inherited from the subscription and Contributor at the resource group.
- As `testuser1` in a private window, the subscription and `rg-azb-core` are visible.
- As `testuser1`, changing a tag on `rg-azb-core` works.
- As `testuser1`, **Add role assignment** on `rg-azb-core` is disabled or refused.
- As `testuser1`, creating a new resource group is refused.
- With the Contributor assignment removed, the tag change is refused. With it added back, it works again.

## The most common mistake

Assigning a role to the wrong scope, usually the subscription when you meant one resource group. Everything inherits from the subscription, so a Contributor given there reaches every resource group in it, and the Reader-above-Contributor-below picture in this lab turns into "Contributor everywhere". The second mistake is the same thing with Owner. Before you select **Review + assign**, read the scope line on the review tab. If you gave the wrong scope, remove the assignment at that scope and add the right one. Learn says you cannot remove an inherited assignment from a child scope. If you see that message, use the link next to **(Inherited)** in the **Scope** column to open the scope where it was assigned.

A third one: expecting a role to take effect to the second. If a user still lacks access right after you assign, wait a little and have the user sign in again.

## Clean up

Remove the subscription-level Reader first. It is the broader of the two, and you do not need it again.

In the portal: open the subscription > **Access control (IAM)** > **Role assignments**, tick `TestUsers` under **Reader**, select **Remove**, then **Yes**.

With the CLI:

```bash
az role assignment delete --assignee "$GROUP_ID" --role "Reader" \
  --scope "/subscriptions/$SUB_ID"
```

Learn shows `az role assignment delete` with `--assignee`, `--role` and `--scope`. It shows a group ID as the `--assignee` value, which is what the command above does.

Check: `az role assignment list --assignee "$GROUP_ID" --all -o table` no longer lists the subscription scope.

Then decide about Contributor on `rg-azb-core`. The safe choice is to remove that too, and to add it back only when a later lab needs it:

```bash
az role assignment delete --assignee "$GROUP_ID" --role "Contributor" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG"
```

Also remove the test tag: in the portal, open `rg-azb-core` > **Tags**, delete `rbac-test` and apply.

Keep for later labs:

- The group `TestUsers` with `testuser1`, from Lab 4.
- `rg-azb-core`, with its action group and budget.
- A note that nobody has Owner at subscription scope except your own admin account. If you gave Owner to anyone else, remove it now.

Nothing in this lab costs money. If you used Terraform, run `terraform destroy` in the `rbac-tf` folder instead of the portal or CLI removal above. It removes both assignments.

## Where this is used in AVD

AVD has its own roles and uses these same scopes, and the habit from this lab (small role, small scope, assign to groups) is what keeps an AVD estate safe. The full list of AVD roles is in [Who Can Administer Azure Virtual Desktop: Roles, Scopes and Delegation](/azure-virtual-desktop/who-can-administer-azure-virtual-desktop/).

## Next lab

[Lab 8: Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/) creates the resource group `rg-azb-lab` and the network that your virtual machines will sit in.

## Sources

- [What is Azure role-based access control (Azure RBAC)?](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview)
- [Understand scope for Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview)
- [Assign Azure roles using the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal)
- [Assign Azure roles using Azure CLI](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-cli)
- [List Azure role assignments using the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-list-portal)
- [List Azure role assignments using Azure CLI](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-list-cli)
- [Remove Azure role assignments](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-remove)
- [Azure built-in roles for Privileged](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/privileged)
- [Best practices for Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/best-practices)
- [Azure built-in roles for Compute (Virtual Machine User Login)](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/compute#virtual-machine-user-login)
- [Sign in to Windows virtual machine in Azure using Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-windows)
