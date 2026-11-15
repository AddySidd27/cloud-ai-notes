---
title: "Azure Policy and Resource Locks in a Sandbox Resource Group"
seoTitle: "Azure Policy and Resource Locks for Beginners: Sandbox Lab"
layout: post.njk
permalink: "/azure-basics-labs/azure-policy-locks/"
order: 327
tags: [azure-basics-lab]
deck: "In a throwaway resource group you block a storage account in the wrong region, require a tag, go from Audit to Deny, and see a CanNotDelete lock stop a delete."
description: "Beginner Azure lab: assign Allowed locations and a required tag in a sandbox resource group, move from Audit to Deny, then test CanNotDelete and ReadOnly locks."
---

By the end of this lab you will have a resource group called `rg-azb-sandbox` with two Azure Policy rules on it. One allows only your region. The other requires a tag called `env`. You will have seen a storage account blocked by each rule and read the error. You will have put a CanNotDelete lock on a storage account, tried to delete it, and removed the lock before you delete the sandbox.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

Everything in this lab happens inside one resource group that you create for it. Nothing here touches `rg-azb-core` or any other group.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway subscription.
- [Lab 2: Cloud Shell and the Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/): only for the CLI part. Azure CLI 2.76 or newer.
- [Lab 3: Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): you already know what a resource group and a tag are.
- [Lab 7: Azure RBAC roles](/azure-basics-labs/rbac-roles/): permissions are a different thing from policy and locks. This lab shows the difference.
- A role that can create policy assignments and locks. Learn says that to create or delete locks you need access to `Microsoft.Authorization/*` or `Microsoft.Authorization/locks/*` actions, and that Owner and User Access Administrator have it. Use Owner on your own throwaway subscription.
- The one region you use for the whole series (you picked it in [Lab 8](/azure-basics-labs/virtual-network-subnet/)), and a second region that is different from it. You will try to deploy into the second region and be refused.
- Time: about 60 minutes of work, plus waiting of 5 to 15 minutes at three points. Cost: storage accounts are the only billable resource, you create at most three at a time, and you delete them in this lab. I did not find a Learn page with the price of an empty storage account, so do the clean up the same day.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top of the portal before you assign anything.
- Assign every policy in this lab to the resource group `rg-azb-sandbox`. Never assign a Deny policy at subscription scope in this series. Learn says a policy assignment applies to all resources contained within its scope, so a Deny rule on the subscription would also block what you build in Labs 8 to 16.
- Check the scope field on every assignment page before you select **Create**. It must end in `rg-azb-sandbox`.
- A lock can stop you from cleaning up. Remove the locks first, then the assignments, then delete the resource group. The order is in "Clean up".
- Do not use a ReadOnly lock on the resource group. Learn lists many things it blocks. This lab only describes it.
- Azure already requires multifactor authentication (MFA) for Azure management work. If you are asked for it, that is expected.

## What the lab builds

![A left-to-right diagram. Inside one subscription is the resource group rg-azb-sandbox. Two policy assignments are attached to it: Allowed locations, which goes from Audit to Deny, and Require a tag on resources, which goes from DoNotEnforce to Enabled. Storage accounts created in a wrong region or without the env tag are refused with a Forbidden error. A CanNotDelete lock sits on one storage account and blocks its delete. At the end the locks are removed, the assignments are deleted and the resource group is deleted.](/img/basics/azure-policy-locks.svg)

*Source: [Quickstart: Create a policy assignment to identify non-compliant resources](https://learn.microsoft.com/en-us/azure/governance/policy/assign-policy-portal), [Azure Policy assignment structure](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/assignment-structure), [Azure Policy definitions deny effect](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-deny), [Get compliance data of Azure resources](https://learn.microsoft.com/en-us/azure/governance/policy/how-to/get-compliance-data) and [Lock your Azure resources to protect your infrastructure](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Part 1: Create the sandbox

1. Sign in to the [Azure portal](https://portal.azure.com). Read the tenant and subscription name.
2. Search for and open **Resource groups**, then select **Create**.
3. Set **Resource group** to `rg-azb-sandbox` and **Region** to your chosen region. Select **Review + Create**, then **Create**.

Check: `rg-azb-sandbox` is in the Resource groups list and is empty.

### Part 2: Allowed locations, first with Audit

**Idea 1: a policy assignment is a rule, a place and an effect.** Azure Policy checks resources against rules. A *policy definition* is the rule. A *policy assignment* applies a rule to a *scope*, which is a subscription, a resource group or a resource. Learn says an assignment applies to all resources contained in its scope. The *effect* says what happens when a resource breaks the rule. Two effects matter here. **Audit** lets the resource be created and marks it non-compliant in a report. **Deny** stops the request. Learn says Deny returns the request as `403 (Forbidden)` before it reaches the resource provider, and that in the portal you can see it as a deployment status that the policy assignment prevented.

The rule is the built-in policy **Allowed locations**. Learn's list of built-in policies describes it as restricting the locations your organization can specify when deploying resources, and says it **excludes resource groups, `Microsoft.AzureActiveDirectory/b2cDirectories`, and resources that use the `global` region**. So it does not stop you from creating a resource group in another region, and it does not touch global resources. It lists the allowed effects as Audit, Deny and Disabled. You start with Audit so you can see what the rule would catch before it blocks anything.

4. Search for and open **Policy**. Under **Authoring**, select **Assignments**, then **Assign policy**.
5. On the **Basics** tab, next to **Scope**, select the ellipsis (`...`). Choose your subscription and the resource group `rg-azb-sandbox`, then **Select**. Learn describes this step the same way.
6. Next to **Policy definition**, select the ellipsis. Search for `Allowed locations`. Pick the one named exactly **Allowed locations**, not **Allowed locations for resource groups**, then select **Add**.
7. Leave **Policy enforcement** on **Enabled**. Set the **Assignment name** to something clear, such as `Allowed locations (sandbox)`.
8. Select **Next** to open the **Parameters** tab. Set **Allowed locations** to your one chosen region only. Set **Effect** to **Audit**. If you do not see the Effect field, look for a checkbox on that tab that hides parameters with default values and clear it.
9. Skip **Remediation**. Learn says the managed identity is only needed for the deployIfNotExists and modify effects.
10. On the **Non-compliance messages** tab, write `Resources in this sandbox must be in my chosen region.` Learn says this message is shown when a resource is denied or non-compliant.
11. Select **Review + create**, then **Create**. Check that the scope on the review page ends in `rg-azb-sandbox`.

**Idea 2: policy is not instant.** Learn gives these times:

- A new assignment takes about five minutes to be applied to its scope, and then the evaluation of the resources begins.
- When you deploy or update a resource in a scope that has an assignment, the effect event and the compliance result for that resource appear in the portal around 15 minutes later.
- Every 24 hours all assignments are evaluated again.
- You can also start an on-demand scan, but Learn says it is asynchronous and takes a long time to run.

So wait at least five minutes after each assignment or change before you test. A test that runs too early can pass when it should not.

12. Wait five minutes.

Check: under **Policy** > **Assignments**, `Allowed locations (sandbox)` is listed with the scope `rg-azb-sandbox`.

### Part 3: Break the rule while it only audits

13. Search for **Storage accounts**, then select **Create**.
14. Set **Resource group** to `rg-azb-sandbox`. Set **Storage account name** to a name that is new to you. Learn says it must be between 3 and 24 characters and use only numbers and lowercase letters. A name like `azbsbaa` plus six digits works. Set **Region** to your **second** region, the one that is not allowed.
15. Select **Review + create**, then **Create**. With Audit, the deployment should succeed. This is the first account. Call it account A.
16. Wait about 15 minutes. Then open **Policy** > **Compliance** and open `Allowed locations (sandbox)`. Learn says compliance results for a new or updated resource show up around 15 minutes after the deployment. Account A should show as **Non-compliant**.

Check: the storage account exists in the wrong region and the policy reports it as non-compliant. It was not stopped. That is what Audit does.

### Part 4: Switch the same rule to Deny

17. Open **Policy** > **Assignments**, select `Allowed locations (sandbox)`, then select **Edit assignment**. Learn describes this path for changing an assignment's parameters.
18. On the **Parameters** tab, change **Effect** to **Deny**. Select **Review + save**, then **Save**. Learn says an updated assignment goes through the same timing as a new one, so wait five minutes.
19. Search for **Storage accounts** and select **Create** again. Use a new name (account B), the resource group `rg-azb-sandbox` and your **second** region.
20. Select **Review + create**, then **Create**. Expect it to fail. Either the validation step shows an error, or the deployment starts and fails. If you land on a failed deployment, open `rg-azb-sandbox`, select **Deployments**, then the failed deployment, then the error details. Learn says a denied deployment shows with a status of **Forbidden**.
21. Read the error. Look for the code **RequestDisallowedByPolicy**, the name of the policy assignment, and your non-compliance message. Learn says the error names the policy definition and the policy assignment, and that the last segment of each `id` is its name.
22. Account A is still there. Deny does not delete what already exists. Learn says existing resources that match a deny policy are marked non-compliant. Delete account A now: open it, select **Delete**, and type its name to confirm.

Check: the create in the second region is refused with `RequestDisallowedByPolicy`, and the same create in your chosen region would work (you try that in Part 5).

### Part 5: Require a tag, with the enforcement switch off first

Learn's list of built-in policies has four tag rules that fit here:

- **Require a tag on resources**: the resource must have a tag with the name you give. It does not apply to resource groups.
- **Require a tag and its value on resources**: the tag must exist and have the value you give. It does not apply to resource groups.
- **Require a tag on resource groups** and **Require a tag and its value on resource groups**: the same two rules, but for resource groups.

All four list only `deny` as their effect, so there is no Audit setting to start with. You use a different switch for the same purpose: the **enforcement mode** of the assignment. Learn says `DoNotEnforce` evaluates compliance without enforcing the effect and without writing deny entries to the activity log, and describes it as a way to test a new assignment before it is enforced. In the portal the field is called **Policy enforcement**, with the values **Enabled** and **Disabled**. The Learn table maps Enabled to `Default` and Disabled to `DoNotEnforce`.

23. Open **Policy** > **Assignments** > **Assign policy**. Set the scope to `rg-azb-sandbox`.
24. Pick the definition **Require a tag on resources**.
25. Set **Policy enforcement** to **Disabled**. Name the assignment `Require env tag (sandbox)`.
26. On **Parameters**, set **Tag Name** to `env`.
27. On **Non-compliance messages**, write `Add the tag env.` Select **Review + create**, check the scope, then **Create**. Wait five minutes.
28. Create a storage account (account C) in your **chosen** region, in `rg-azb-sandbox`, with **no tags**. It should succeed. The Location rule is happy, and the tag rule is switched off.
29. Switch the tag rule on: open the assignment, select **Edit assignment**, set **Policy enforcement** to **Enabled**, then **Save**. Wait five minutes.
30. Try to create another storage account (account D) in your chosen region with **no tags**. It should be refused with `RequestDisallowedByPolicy` and your message `Add the tag env.`
31. Create account D again, this time with a tag: on the **Tags** tab add the name `env` and the value `sandbox`. It should succeed.
32. Delete account C, the one without a tag.

Check: an untagged create is refused, a tagged create in the right region works. Both rules are now being enforced at the same time. If one create fails, read which assignment name the error gives. Learn says the error includes it.

### Part 6: Lock one resource

**Idea 3: a lock is not a permission and not a policy.** A lock is a flag on a subscription, resource group or resource. Learn says it protects from accidental deletions and modifications, and that **the lock overrides any user permissions**. It applies across all users and roles, which is not how Azure RBAC works. Two levels exist. In the portal they are called **Delete** and **Read-only**. In the CLI they are **CanNotDelete** and **ReadOnly**.

- **CanNotDelete**: authorized users can read and modify the resource but cannot delete it.
- **ReadOnly**: authorized users can read but cannot delete or update. Learn says it is similar to giving everyone only the Reader role.

Learn also says: a lock on a parent scope is inherited by everything inside it, including resources you add later, and the most restrictive lock wins. And locks apply only to control plane operations (the calls to `management.azure.com`), not to data plane operations. A lock on a storage account does not protect the data inside it.

33. Open account D. In the left menu, under **Settings**, select **Locks**. (For a subscription the menu item is called **Resource locks**.)
34. Select **Add**. Set **Lock name** to `lock-azb-nodelete`, **Lock type** to **Delete**, and add a note: `Lab 17 test. Remove before cleanup.` Select **OK**.
35. On account D, select **Delete** and confirm. Expect an error. Learn's troubleshooting pages show the error code as `ScopeLocked`, with text that says the scope cannot perform the delete operation because it is locked, and to remove the lock and try again.
36. Prove that CanNotDelete still lets you change things. Open the **Tags** page of account D, change the value of `env` to `sandbox2`, and save. It should work, because Learn says CanNotDelete allows read and modify.

Check: delete is blocked, a tag edit is not.

**Optional, one step.** To see ReadOnly, change the lock type on `lock-azb-nodelete` to **Read-only**, then try the same tag edit. It should fail with a message that says the scope is locked, probably for a write operation. Change the lock back to **Delete** or remove it right after.

**What ReadOnly can break.** Learn warns that applying locks can have unexpected results, because some operations that do not look like changes use the POST method, which a ReadOnly lock blocks. Examples from the Learn page:

- A ReadOnly lock on a storage account stops you listing the account keys. It also blocks creating a blob container and assigning RBAC roles scoped to that account.
- A ReadOnly lock on a resource group that contains a virtual machine stops all users from starting or restarting the VM.
- A ReadOnly lock on a resource group stops you moving resources in or out of the group.
- A ReadOnly lock on a resource group with an Automation account stops runbooks from starting.
- A CanNotDelete lock on a resource group stops Resource Manager from automatically deleting old deployments from the history. Learn says when you reach 800 deployments, your deployments fail.

Also, a ReadOnly lock stops deletion too. So it can block your own cleanup. Learn also says that if a Delete lock exists on one resource and you try to delete its resource group, the whole delete is refused. A partial delete is not possible.

## Steps with the Azure CLI

Do either the portal steps or these, not both at the same time on the same names. If you did the portal steps, skip to "Clean up". Run these in Cloud Shell (Bash) or a local shell. Check the subscription first.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
LOCATION=eastus2          # your chosen region
OTHER=westus3             # a different region
RG=rg-azb-sandbox
SUFFIX=$RANDOM$RANDOM
STG_A=azbsba$SUFFIX       # wrong region, audit
STG_B=azbsbb$SUFFIX       # wrong region, deny (never created)
STG_C=azbsbc$SUFFIX       # no tag, enforcement off
STG_D=azbsbd$SUFFIX       # tagged, gets the lock
```

Storage account names must be 3 to 24 characters, numbers and lowercase letters only. These names are short enough.

Create the sandbox and read its ID, which you use as the scope.

```bash
az group create --name $RG --location $LOCATION
RG_ID=$(az group show --name $RG --query id -o tsv)
echo $RG_ID
```

Check: the ID ends in `/resourceGroups/rg-azb-sandbox`.

Assign **Allowed locations** with Audit. `--policy` takes the name or ID of the definition. The name of the built-in policy is the GUID in its ID: `e56962a6-4747-49cd-b67b-bf8b01975c4c`. The parameters are `listOfAllowedLocations` and `effect`. Quote the JSON the way the Learn example does.

```bash
az policy assignment create \
  --name allowed-locations-azb \
  --display-name "Allowed locations (sandbox)" \
  --scope $RG_ID \
  --policy e56962a6-4747-49cd-b67b-bf8b01975c4c \
  -p "{ 'listOfAllowedLocations': { 'value': [ '$LOCATION' ] }, 'effect': { 'value': 'Audit' } }"
az policy assignment list --resource-group $RG --query "[].name" -o tsv
```

Check: the list prints `allowed-locations-azb`. Wait five minutes. Then create account A in the wrong region. It should succeed.

```bash
az storage account create --name $STG_A --resource-group $RG --location $OTHER --sku Standard_LRS --kind StorageV2
```

About 15 minutes later, look at the compliance data.

```bash
az policy state list --resource-group $RG -o table
```

Check: account A shows as non-compliant. If the table is empty, wait longer. Learn says an on-demand scan, `az policy state trigger-scan --resource-group $RG`, is possible, but it is asynchronous and takes a long time.

Switch the effect to Deny. Give the whole parameter set again, so nothing is lost. Wait five minutes.

```bash
az policy assignment update \
  --name allowed-locations-azb \
  --scope $RG_ID \
  -p "{ 'listOfAllowedLocations': { 'value': [ '$LOCATION' ] }, 'effect': { 'value': 'Deny' } }"
az storage account create --name $STG_B --resource-group $RG --location $OTHER --sku Standard_LRS --kind StorageV2
```

Check: the second command fails and the error contains `RequestDisallowedByPolicy` and the assignment name `allowed-locations-azb`. Then delete account A:

```bash
az storage account delete --name $STG_A --resource-group $RG
```

Assign **Require a tag on resources** (definition name `871b6d14-10aa-478d-b590-94f262ecfa99`, parameter `tagName`) with the enforcement mode off. `--enforcement-mode` takes `Default` or `DoNotEnforce`.

```bash
az policy assignment create \
  --name require-tag-env-azb \
  --display-name "Require env tag (sandbox)" \
  --scope $RG_ID \
  --policy 871b6d14-10aa-478d-b590-94f262ecfa99 \
  -p "{ 'tagName': { 'value': 'env' } }" \
  --enforcement-mode DoNotEnforce
```

Wait five minutes. Create account C with no tag. It should work.

```bash
az storage account create --name $STG_C --resource-group $RG --location $LOCATION --sku Standard_LRS --kind StorageV2
```

Switch enforcement on. Wait five minutes. Then try an untagged account again, and a tagged one. The tagged one is account D.

```bash
az policy assignment update --name require-tag-env-azb --scope $RG_ID --enforcement-mode Default
az storage account create --name azbsbx$SUFFIX --resource-group $RG --location $LOCATION --sku Standard_LRS --kind StorageV2
az storage account create --name $STG_D --resource-group $RG --location $LOCATION --sku Standard_LRS --kind StorageV2 --tags env=sandbox
az storage account delete --name $STG_C --resource-group $RG
```

Check: the first create is refused with `RequestDisallowedByPolicy`, the second works, and account C is gone.

Add the lock to account D and try to delete it. `--lock-type` is `CanNotDelete` or `ReadOnly`.

```bash
az lock create --name lock-azb-nodelete --lock-type CanNotDelete \
  --resource-group $RG --resource-name $STG_D \
  --resource-type Microsoft.Storage/storageAccounts \
  --notes "Lab 17 test. Remove before cleanup."
az lock list --resource-group $RG -o table
az storage account delete --name $STG_D --resource-group $RG
```

Check: the delete fails with `ScopeLocked`.

## Terraform

No Terraform in this lab, because I could not check the Terraform resources for policy assignments and locks against Learn, and I do not want to give you code I have not checked. The portal and CLI steps are enough to learn the idea.

## Check that it works

- With the Allowed locations rule on Deny, a storage account in the second region is refused with `RequestDisallowedByPolicy`.
- The same rule in Audit let the account through and reported it as non-compliant. After you switched to Deny, the old account stayed until you deleted it.
- With the tag rule enforced, an untagged account is refused and a tagged one is created.
- A CanNotDelete lock on a storage account refuses the delete but allows a tag edit.
- You can say in one sentence what a role, a policy and a lock each do. A role says what a person may do. A policy says what a resource may look like. A lock stops a delete or a change, whoever the person is.

## The most common mistake

Locking something and forgetting about it, then trying to clean up. A Delete lock on any one resource makes the delete of the whole resource group fail, and a ReadOnly lock blocks deletes as well. The error is `ScopeLocked`. The fix is always the same: list the locks, remove them, then delete.

The second most common mistake is the scope. A Deny assignment made on the subscription instead of on `rg-azb-sandbox` blocks the same kind of deployment everywhere in that subscription, including the resources from your earlier labs. If you made that mistake, open **Policy** > **Assignments**, find the assignment, and delete it. Then wait five minutes before you test again.

A smaller one: testing too early. Learn says an assignment takes about five minutes to apply and compliance results can take 15 minutes, so a test right after you save can give a wrong answer.

## Clean up

Do it in this order. The order matters because of the locks. The CLI commands use the variables from the CLI part. If you used the portal, set them first:

```bash
RG=rg-azb-sandbox
RG_ID=$(az group show --name $RG --query id -o tsv)
STG_D=<the name of account D>
```

1. Remove the lock. Portal: open the storage account, **Settings** > **Locks**, then select **Delete** next to `lock-azb-nodelete`. CLI:

   ```bash
   az lock delete --name lock-azb-nodelete --resource-group $RG --resource $STG_D --resource-type Microsoft.Storage/storageAccounts
   az lock list --resource-group $RG -o table
   ```

   The list should be empty. If you made any other lock, remove that too.

2. Delete the policy assignments. Portal: **Policy** > **Assignments**, open the ellipsis of each assignment, then **Delete assignment**. CLI:

   ```bash
   az policy assignment delete --name allowed-locations-azb --scope $RG_ID
   az policy assignment delete --name require-tag-env-azb --scope $RG_ID
   az policy assignment list --resource-group $RG --query "[].name" -o tsv
   ```

   The last command should print nothing.

3. Delete the resource group. Read the name twice. Portal: **Resource groups** > `rg-azb-sandbox` > **Delete resource group**, type the name. CLI:

   ```bash
   az group delete --name rg-azb-sandbox
   az group exists --name rg-azb-sandbox
   ```

   The last command should print `false`.

Keep for later labs: `rg-azb-core`, `rg-azb-lab` and everything in them. Nothing from this lab stays. `rg-azb-lab` never had a policy assignment or lock from this lab, so it is not affected.

## Where this is used in AVD

Before you build an AVD environment you read the policy assignments that already exist, because a Deny rule on region, tag or resource type can stop a host pool or session host deployment. The section on policy checks in [Prepare Your Azure Environment](/azure-virtual-desktop/prepare-your-azure-environment/) lists what to read and record: scope, excluded scopes, enforcement mode, parameters and exemptions.

## Next lab

[Lab 18: Private endpoint and private DNS](/azure-basics-labs/private-endpoint-dns/) adds a private endpoint and the private DNS that goes with it.

## Sources

- [Quickstart: Create a policy assignment to identify non-compliant resources using Azure portal](https://learn.microsoft.com/en-us/azure/governance/policy/assign-policy-portal)
- [Azure Policy assignment structure](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/assignment-structure)
- [Azure Policy definitions deny effect](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-deny)
- [Get compliance data of Azure resources](https://learn.microsoft.com/en-us/azure/governance/policy/how-to/get-compliance-data)
- [Azure Policy built-in policy definitions](https://learn.microsoft.com/en-us/azure/governance/policy/samples/built-in-policies)
- [Understand scope in Azure Policy](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/scope)
- [Resolve errors for request disallowed by policy](https://learn.microsoft.com/en-us/azure/azure-resource-manager/troubleshooting/error-policy-requestdisallowedbypolicy)
- [Tutorial: Create and manage policies to enforce compliance](https://learn.microsoft.com/en-us/azure/governance/policy/tutorials/create-and-manage)
- [Lock your Azure resources to protect your infrastructure](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources)
- [Create an Azure storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create)
- [az policy assignment](https://learn.microsoft.com/en-us/cli/azure/policy/assignment)
- [az lock](https://learn.microsoft.com/en-us/cli/azure/lock)
- [Troubleshoot an Azure Load Balancer that can't be deleted](https://learn.microsoft.com/en-us/troubleshoot/azure/load-balancer/troubleshoot-cannot-delete-load-balancer) (the ScopeLocked error text)
