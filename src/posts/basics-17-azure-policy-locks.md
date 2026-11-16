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

By the end of this lab you will have a resource group called `rg-azb-sandbox` with two Azure Policy rules on it. One allows only your region. The other requires a tag called `env`. You will have seen a storage account blocked by each rule and read the error. You will have put a CanNotDelete lock on a storage account, tried to delete it, and removed the lock before you delete the sandbox. Everything you create here is deleted at the end.

Everything in this lab happens inside one resource group that you create for it. Nothing here touches `rg-azb-core` or any other group.

## What you need

- [Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): a throwaway subscription.
- [Azure Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/): only for the CLI part. Azure CLI 2.76 or newer.
- [Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): you already know what a resource group and a tag are.
- [Azure RBAC roles](/azure-basics-labs/rbac-roles/): permissions are a different thing from policy and locks. This lab shows the difference.
- A role that can create policy assignments and locks. To create or delete locks you need access to `Microsoft.Authorization/*` or `Microsoft.Authorization/locks/*` actions. Owner and User Access Administrator have it. Use Owner on your own throwaway subscription.
- The one region you use for the whole series (the region on your notes sheet from [the account lab](/azure-basics-labs/start-azure-account-tenant-subscription/)), and a second region that is different from it. You will try to deploy into the second region and be refused. For example, if your region is East US 2, use West US 3. If the portal says a region is not available for storage accounts, pick another one.
- Time: about 60 minutes of work, plus waiting of 5 to 15 minutes at a few points. Use the waits: while you wait, read the section on locks.
- Cost: empty storage accounts cost almost nothing, but delete them the same day. You never have more than two at a time. Nothing here uses the VM.

**State of your resources**

| | At the start | At the end |
|---|---|---|
| VM `vm-azb-win01` | Stopped (deallocated). This lab does not use it. | Stopped (deallocated) |
| Rule `allow-rdp-my-ip` in `nsg-azb-vm` | Not there | Not there |
| Public IP `pip-azb-win01` | Exists. It stays. | Exists |
| New in this lab | Nothing | Nothing. `rg-azb-sandbox`, its policies, lock and storage accounts are all deleted. |

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top of the portal before you assign anything.
- Assign every policy in this lab to the resource group `rg-azb-sandbox`. Never assign a Deny policy at subscription scope in this series. A policy assignment applies to all resources contained within its scope, so a Deny rule on the subscription would also block what you build in the other labs.
- Check the scope field on every assignment page before you select **Create**. It must end in `rg-azb-sandbox`.
- A lock can stop you from cleaning up. Remove the locks first, then the assignments, then delete the resource group. The order is in "Clean up".
- Do not use a ReadOnly lock on a resource group. It blocks actions that do not look like changes, such as starting a VM. This lab only tries it, once, on one storage account.
- Azure already requires multifactor authentication (MFA) for Azure management work. If you are asked for it, that is expected.

## What the lab builds

![In rg-azb-sandbox, Allowed locations refuses a storage account in the wrong region (403) and Require tag env refuses one without the tag. A valid account is created and protected by a CanNotDelete lock. Clean up: remove the lock, then the assignments, then the group.](/img/basics/azure-policy-locks.svg)

*Source: Microsoft Learn pages listed under Sources.*

## Steps in the Azure portal

### Create the sandbox

1. Sign in to the [Azure portal](https://portal.azure.com). Read the tenant and subscription name.
2. Search for and open **Resource groups**, then select **Create**.
3. Set **Resource group** to `rg-azb-sandbox` and **Region** to your chosen region. Select **Review + Create**, then **Create**.

Check: `rg-azb-sandbox` is in the Resource groups list and is empty.

### Allowed locations, first with Audit

**Idea 1: a policy assignment is a rule, a place and an effect.** Azure Policy checks resources against rules. A *policy definition* is the rule. A *policy assignment* applies a rule to a *scope*, which is a subscription, a resource group or a resource. An assignment applies to all resources contained in its scope. The *effect* says what happens when a resource breaks the rule. Two effects matter here. **Audit** lets the resource be created and marks it non-compliant in a report. **Deny** stops the request. A Deny returns the request as `403 (Forbidden)` before it reaches the resource provider.

**Idea 2: policy is not instant.** A new assignment takes about five minutes to be applied to its scope. The compliance report takes about 15 minutes to show a result. So wait five minutes after each assignment or change before you test. A test that runs too early can pass when it should not.

The rule is the built-in policy **Allowed locations**. It restricts the locations you can specify when you deploy resources. It does not apply to resource groups or to resources that use the `global` region. You start with Audit so you can see what the rule would catch before it blocks anything.

4. Search for and open **Policy**. Under **Authoring**, select **Assignments**, then **Assign policy**.
5. On the **Basics** tab, next to **Scope**, select the ellipsis (`...`). Choose your subscription and the resource group `rg-azb-sandbox`, then **Select**.
6. Next to **Policy definition**, select the ellipsis. Search for `Allowed locations`. Pick the one named exactly **Allowed locations**, not **Allowed locations for resource groups**, then select **Add**.
7. Leave **Policy enforcement** on **Enabled**. Set the **Assignment name** to something clear, such as `Allowed locations (sandbox)`.
8. Select **Next** to open the **Parameters** tab. Set **Allowed locations** to your one chosen region only. Set **Effect** to **Audit**. If you do not see the Effect field, look for a checkbox on that tab that hides parameters with default values and clear it.
9. Skip **Remediation**. It is only needed for effects that change resources.
10. On the **Non-compliance messages** tab, write `Resources in this sandbox must be in my chosen region.` This message is shown when a resource is denied or non-compliant.
11. Select **Review + create**, then **Create**. Check that the scope on the review page ends in `rg-azb-sandbox`.
12. Wait five minutes.

Check: under **Policy** > **Assignments**, `Allowed locations (sandbox)` is listed with the scope `rg-azb-sandbox`.

### Break the rule while it only audits

The storage accounts are named by what they test, so you do not mix them up: the audit-test account, the no-tag account and the tagged account. A Deny test account never gets created. Storage account names must be 3 to 24 characters, lowercase letters and digits only, and unique across Azure. Pick five digits and use them in every name, for example `azbsbaudit48213`. Write the names in your notes as you create them.

13. Search for **Storage accounts**, then select **Create**.
14. Set **Resource group** to `rg-azb-sandbox`. Set **Storage account name** to `azbsbaudit` plus your five digits. Set **Region** to your **second** region, the one that is not allowed.
15. Select **Review + create**, then **Create**. With Audit, the deployment should succeed. This is the audit-test account.
16. Optional compliance report: wait about 15 minutes, then open **Policy** > **Compliance** and open `Allowed locations (sandbox)`. The audit-test account should show as **Non-compliant**. If you do not want to wait, go on to the next section and look at the report at the end of the lab.

Check: the storage account exists in the wrong region. It was not stopped. That is what Audit does.

### Switch the same rule to Deny

17. Open **Policy** > **Assignments**, select `Allowed locations (sandbox)`, then select **Edit assignment**.
18. On the **Parameters** tab, change **Effect** to **Deny**. Select **Review + save**, then **Save**. Wait five minutes.
19. Search for **Storage accounts** and select **Create** again. Use the name `azbsbdeny` plus your digits, the resource group `rg-azb-sandbox` and your **second** region.
20. Select **Review + create**, then **Create**. Expect it to fail. Look for a red banner on **Review + create**, or for the notification bell, or a failed deployment. If you land on a failed deployment, open `rg-azb-sandbox`, select **Deployments**, then the failed deployment, then the error details.
21. Read the error. It looks like "Resource ... was disallowed by policy", with the code **RequestDisallowedByPolicy**, the name of the policy assignment and your non-compliance message.
22. The audit-test account is still there. Deny does not delete what already exists. Delete it now: open it, select **Delete**, and type its name to confirm.

Check: the create in the second region is refused with `RequestDisallowedByPolicy`, and the same create in your chosen region would work (you try that in the next section).

### Require a tag, with enforcement switched off first

Azure has built-in rules for tags. You use **Require a tag on resources**. It has no Audit setting, so you use a different switch for the same purpose: the **enforcement mode** of the assignment. In the portal the field is called **Policy enforcement**, with the values **Enabled** and **Disabled**. Disabled means the rule is checked but not enforced. It does not mean the assignment is deleted.

23. Open **Policy** > **Assignments** > **Assign policy**. Set the scope to `rg-azb-sandbox`.
24. Pick the definition **Require a tag on resources**.
25. Set **Policy enforcement** to **Disabled**. Name the assignment `Require env tag (sandbox)`.
26. On **Parameters**, set **Tag Name** to `env`.
27. On **Non-compliance messages**, write `Add the tag env.` Select **Review + create**, check the scope, then **Create**. Wait five minutes.
28. Create a storage account named `azbsbnotag` plus your digits in your **chosen** region, in `rg-azb-sandbox`, with **no tags**. It should succeed. The location rule is happy, and the tag rule is switched off. This is the no-tag account.
29. Switch the tag rule on: open the assignment, select **Edit assignment**, set **Policy enforcement** to **Enabled**, then **Save**. Wait five minutes.
30. Try to create another storage account named `azbsbtagged` plus your digits in your chosen region with **no tags**. It should be refused with `RequestDisallowedByPolicy` and your message `Add the tag env.`
31. Create the same account again, this time with a tag: on the **Tags** tab add the name `env` and the value `sandbox`. It should succeed. This is the tagged account.
32. Delete the no-tag account.

Check: an untagged create is refused, a tagged create in the right region works. Both rules are now being enforced at the same time. If one create fails, read which assignment name the error gives.

### Lock one resource

**Idea 3: a lock is not a permission and not a policy.** A lock is a flag on a subscription, resource group or resource. It protects from accidental deletions and modifications, and **the lock overrides any user permissions**. It applies across all users and roles, which is not how Azure RBAC works. Two levels exist. In the portal they are called **Delete** and **Read-only**. In the CLI they are **CanNotDelete** and **ReadOnly**.

- **CanNotDelete**: authorized users can read and modify the resource but cannot delete it.
- **ReadOnly**: authorized users can read but cannot delete or update.

A lock on a parent scope is inherited by everything inside it, and the most restrictive lock wins. Locks apply to control plane operations only. A lock on a storage account does not protect the data inside it.

33. Open the tagged account. In the left menu, under **Settings**, select **Locks**. (For a subscription the menu item is called **Resource locks**.)
34. Select **Add**. Set **Lock name** to `lock-azb-nodelete`, **Lock type** to **Delete**, and add a note: `Test lock. Remove before cleanup.` Select **OK**.
35. On the tagged account, select **Delete** and confirm. Expect an error that says the scope is locked and cannot perform the delete operation, and to remove the lock and try again.
36. Prove that CanNotDelete still lets you change things. Open the **Tags** page of the tagged account, change the value of `env` to `sandbox2`, and save. It should work.

Check: delete is blocked, a tag edit is not.

**Optional, one step.** To see ReadOnly, change the lock type on `lock-azb-nodelete` to **Read-only**, then try the same tag edit. It should fail with a message that says the scope is locked. Change the lock back to **Delete** right after.

A ReadOnly lock can block actions that do not look like changes, such as listing the account keys of a storage account or starting a VM. Use Delete locks, and never put ReadOnly on a resource group. A Delete lock on one resource also makes the delete of its whole resource group fail. That is why "Clean up" starts with the locks.

## Steps with the Azure CLI

Do either the portal steps or these, not both on the same names. If you did the portal steps, skip to "Clean up". Run these in Cloud Shell (Bash) or a local shell. Check the subscription first. Anything in ALL CAPS after a `#` comment is yours to change. Run `echo` on a variable before you use it. If Cloud Shell restarts, set the variables again.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
LOCATION=$(az network vnet show --resource-group rg-azb-lab --name vnet-azb --query location -o tsv)   # your chosen region
OTHER=westus3             # any other region that allows storage accounts
RG=rg-azb-sandbox
DIGITS=48213              # replace with five digits of your own
STG_AUDIT=azbsbaudit$DIGITS    # wrong region, audit
STG_DENY=azbsbdeny$DIGITS      # wrong region, deny (never created)
STG_NOTAG=azbsbnotag$DIGITS    # no tag, enforcement off
STG_TAGGED=azbsbtagged$DIGITS  # tagged, gets the lock
echo "$LOCATION $OTHER $STG_AUDIT"
```

If `LOCATION` is empty, set it by hand to your region name, for example `LOCATION=eastus2`. `OTHER` must be a different region from `LOCATION`.

Create the sandbox and read its ID, which you use as the scope.

```bash
az group create --name $RG --location $LOCATION
RG_ID=$(az group show --name $RG --query id -o tsv)
echo $RG_ID
```

Check: the ID ends in `/resourceGroups/rg-azb-sandbox`.

Assign **Allowed locations** with Audit. `--policy` takes the name or ID of the definition. The name of the built-in policy is the GUID in its ID: `e56962a6-4747-49cd-b67b-bf8b01975c4c`. Check the parameter names before you run the assignment. This prints them from the definition:

```bash
az policy definition show --name e56962a6-4747-49cd-b67b-bf8b01975c4c --query "parameters" -o json
```

Look for the list of allowed locations (`listOfAllowedLocations`) and the effect. If your output names them differently, use your names in the `-p` text below. Quote the JSON the way the example does.

```bash
az policy assignment create \
  --name allowed-locations-azb \
  --display-name "Allowed locations (sandbox)" \
  --scope $RG_ID \
  --policy e56962a6-4747-49cd-b67b-bf8b01975c4c \
  -p "{ 'listOfAllowedLocations': { 'value': [ '$LOCATION' ] }, 'effect': { 'value': 'Audit' } }"
az policy assignment list --resource-group $RG --query "[].name" -o tsv
```

Check: the list prints `allowed-locations-azb`. Wait five minutes. Then create the audit-test account in the wrong region. It should succeed.

```bash
az storage account create --name $STG_AUDIT --resource-group $RG --location $OTHER --sku Standard_LRS --kind StorageV2
```

About 15 minutes later, look at the compliance data (optional).

```bash
az policy state list --resource-group $RG -o table
```

Check: the audit-test account shows as non-compliant. If the table is empty, wait longer. An on-demand scan, `az policy state trigger-scan --resource-group $RG`, is possible, but it is asynchronous and takes a long time.

Switch the effect to Deny. Give the whole parameter set again, so nothing is lost. Wait five minutes.

```bash
az policy assignment update \
  --name allowed-locations-azb \
  --scope $RG_ID \
  -p "{ 'listOfAllowedLocations': { 'value': [ '$LOCATION' ] }, 'effect': { 'value': 'Deny' } }"
az storage account create --name $STG_DENY --resource-group $RG --location $OTHER --sku Standard_LRS --kind StorageV2
```

Check: the second command fails and the error contains `RequestDisallowedByPolicy` and the assignment name `allowed-locations-azb`. Then delete the audit-test account:

```bash
az storage account delete --name $STG_AUDIT --resource-group $RG
```

Assign **Require a tag on resources** with the enforcement mode off. Find the definition name by its display name, and check the parameter name in the output (`tagName`). `--enforcement-mode` takes `Default` or `DoNotEnforce`.

```bash
TAG_DEF=$(az policy definition list --query "[?displayName=='Require a tag on resources'].name | [0]" -o tsv)
echo $TAG_DEF
az policy definition show --name $TAG_DEF --query "parameters" -o json
az policy assignment create \
  --name require-tag-env-azb \
  --display-name "Require env tag (sandbox)" \
  --scope $RG_ID \
  --policy $TAG_DEF \
  -p "{ 'tagName': { 'value': 'env' } }" \
  --enforcement-mode DoNotEnforce
```

Wait five minutes. Create the no-tag account. It should work.

```bash
az storage account create --name $STG_NOTAG --resource-group $RG --location $LOCATION --sku Standard_LRS --kind StorageV2
```

Switch enforcement on. Wait five minutes. Then try an untagged account again, and a tagged one.

```bash
az policy assignment update --name require-tag-env-azb --scope $RG_ID --enforcement-mode Default
az storage account create --name azbsbx$DIGITS --resource-group $RG --location $LOCATION --sku Standard_LRS --kind StorageV2
az storage account create --name $STG_TAGGED --resource-group $RG --location $LOCATION --sku Standard_LRS --kind StorageV2 --tags env=sandbox
az storage account delete --name $STG_NOTAG --resource-group $RG
```

Check: the first create is refused with `RequestDisallowedByPolicy`, the second works, and the no-tag account is gone.

Add the lock to the tagged account and try to delete it. `--lock-type` is `CanNotDelete` or `ReadOnly`.

```bash
az lock create --name lock-azb-nodelete --lock-type CanNotDelete \
  --resource-group $RG --resource-name $STG_TAGGED \
  --resource-type Microsoft.Storage/storageAccounts \
  --notes "Test lock. Remove before cleanup."
az lock list --resource-group $RG -o table
az storage account delete --name $STG_TAGGED --resource-group $RG
```

Check: the delete fails with an error that says the scope is locked.

## Terraform

No Terraform in this lab. The portal and CLI steps are enough to learn the idea.

## Check that it works

- With the Allowed locations rule on Deny, a storage account in the second region is refused with `RequestDisallowedByPolicy`.
- The same rule in Audit let the audit-test account through. After you switched to Deny, that account stayed until you deleted it.
- With the tag rule enforced, an untagged account is refused and a tagged one is created.
- A CanNotDelete lock on a storage account refuses the delete but allows a tag edit.
- You can say in one sentence what a role, a policy and a lock each do. A role says what a person may do. A policy says what a resource may look like. A lock stops a delete or a change, whoever the person is.

## The most common mistake

Locking something and forgetting about it, then trying to clean up. A Delete lock on any one resource makes the delete of the whole resource group fail, and a ReadOnly lock blocks deletes as well. The error says the scope is locked. The fix is always the same: list the locks, remove them, then delete.

The second most common mistake is the scope. A Deny assignment made on the subscription instead of on `rg-azb-sandbox` blocks the same kind of deployment everywhere in that subscription, including the resources from your earlier labs. If you made that mistake, open **Policy** > **Assignments**, find the assignment, and delete it. Then wait five minutes before you test again.

A smaller one: testing too early. An assignment takes about five minutes to apply and compliance results can take 15 minutes, so a test right after you save can give a wrong answer.

## Clean up

Do it in this order. The order matters because of the locks. The CLI commands use these variables. Set them first, because Cloud Shell may have restarted, and replace the name with the real name of your tagged account:

```bash
RG=rg-azb-sandbox
RG_ID=$(az group show --name $RG --query id -o tsv)
STG_TAGGED=azbsbtagged48213   # replace with the real name of your tagged account
echo "$RG_ID $STG_TAGGED"
```

1. Remove the lock. Portal: open the tagged account, **Settings** > **Locks**, then select **Delete** next to `lock-azb-nodelete`. CLI:

   ```bash
   az lock delete --name lock-azb-nodelete --resource-group $RG --resource-name $STG_TAGGED --resource-type Microsoft.Storage/storageAccounts
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

End state: `rg-azb-sandbox` is gone with its assignments, lock and storage accounts. The VM is still Stopped (deallocated), no `allow-rdp-my-ip` rule, and the public IP `pip-azb-win01` still exists. Keep for later labs: `rg-azb-core`, `rg-azb-lab` and everything in them. `rg-azb-lab` never had a policy assignment or lock from this lab, so it is not affected. Safe stopping points: after "Switch the same rule to Deny" (delete the audit-test account and leave the assignment for now) and after "Lock one resource" (run "Clean up" now).

## Where this is used in AVD

Before you build an AVD environment you read the policy assignments that already exist, because a Deny rule on region, tag or resource type can stop a host pool or session host deployment. The first symptom is the error you saw when you switched the rule to Deny: `RequestDisallowedByPolicy`. The section on policy checks in [Prepare Your Azure Environment](/azure-virtual-desktop/prepare-your-azure-environment/) lists what to read and record: scope, excluded scopes, enforcement mode, parameters and exemptions.

## Next lab

[Private endpoint and private DNS](/azure-basics-labs/private-endpoint-dns/) adds a private endpoint and the private DNS that goes with it.

## Sources

- [Quickstart: Create a policy assignment to identify non-compliant resources using Azure portal](https://learn.microsoft.com/en-us/azure/governance/policy/assign-policy-portal)
- [Azure Policy definitions deny effect](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-deny)
- [Lock your Azure resources to protect your infrastructure](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources)
