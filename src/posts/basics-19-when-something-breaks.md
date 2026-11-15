---
title: "When Something Breaks: Where to Look, and How to Clean Up the Whole Series"
seoTitle: "Azure Troubleshooting for Beginners and Full Lab Cleanup"
layout: post.njk
permalink: "/azure-basics-labs/when-something-breaks/"
order: 329
tags: [azure-basics-lab]
deck: "You learn the first place to look for the common Azure errors from this series, then delete everything from Labs 1 to 18 in a safe order and check the cost the next day."
description: "Beginner Azure lab: read the activity log, deployments, resource health, sign-in logs, quota and NSG checks, then delete every lab resource and check cost."
---

By the end of this lab you will know where to look first when an Azure step fails. You will have opened the Activity log, the Deployments page, Resource health, boot diagnostics, the Microsoft Entra sign-in logs and the Network Watcher checks for a network security group. Then you will delete everything you built in Labs 1 to 18, keep only what the next series needs, and check Cost analysis the next day.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

Most Azure problems in this series come from a short list: a missing permission, a rule that blocks traffic, a limit on your subscription, or something that was not ready yet. Azure keeps a record of nearly everything it does. The skill is knowing which record to open.

## What you need

- The earlier labs, as far as you did them. Each lab you did left something behind, and the second half of this article deletes it. If you only did some labs, skip the steps for the labs you did not do.
- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/) and [Lab 2: Cloud Shell and the Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/), for the sign-in and the command line.
- Owner or Contributor on the subscription, and Global Administrator in the tenant. You need these to delete resources and to delete the Conditional Access policy.
- Time: about 60 minutes, plus a five-minute look the next day. Cost: nothing for the looking. The Network Watcher checks may have a price, see Part 6. The cleanup stops the cost of everything you left running.

## Safety first

- Use the throwaway tenant only. Read the tenant name and the subscription name before you delete anything.
- Deleting a resource group deletes everything inside it. It cannot be undone. Read each name twice. Never run a delete on `rg-azb-core` by accident.
- `az group delete` without `--yes` asks you to confirm. Keep it that way.
- Do not use `az login --use-device-code`. Cloud Shell is already signed in.
- A budget only sends emails. It does not stop anything. The cleanup is what stops the cost.
- Do not turn on anything new to investigate a problem. In this lab you only look.

## What the lab builds

![A left-to-right diagram. On the left, a box named Something broke. In the middle, six places to look: Activity log, Deployments page, Resource health with boot diagnostics, Microsoft Entra sign-in logs, quota check and Network Watcher. On the right, a clean up path that removes locks, policy assignments and role assignments, deletes rg-azb-sandbox and rg-azb-lab, purges the key vault, checks that the Conditional Access policy is gone, keeps rg-azb-core, and ends with a cost check in Cost analysis the next day.](/img/basics/when-something-breaks.svg)

*Source: [Activity log in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log), [View deployment history with Azure Resource Manager](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deployment-history), [Resource Health overview](https://learn.microsoft.com/en-us/azure/service-health/resource-health-overview), [Microsoft Entra sign-in logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins) and [What is Azure Network Watcher?](https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-overview). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Part 1: The Activity log, who did what

**Idea 1: Azure writes down every change.** The Activity log records management operations on your resources: creating a virtual machine, deleting a group, a deployment that failed. Learn says entries are collected by default with no setup, that you cannot change or delete them, and that Azure keeps them for 90 days. Entries are usually available 3 to 20 minutes after the event. The log does not usually record read operations.

One limit matters for beginners. Learn says the Activity log is not an authentication or authorization audit log. A request that Azure Resource Manager rejects before an operation starts, for example because you have no permission, does not create an entry. So an empty Activity log does not prove nobody tried.

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant and subscription name.
2. Search for and open **Monitor**, then select **Activity log**. Learn says this view starts with only the subscription as a filter.
3. Set the time range to the last 24 hours. Use **Add Filter** to filter by **Resource group** if you see that option, or by **Operation**, **Event initiated by** or **Event category**. Learn lists those last three as filters.
4. Find an event you know about, for example the group you deleted in Lab 3 or the role assignment from Lab 7. Open it. Read three things: what operation it was, who started it (the **Event initiated by** value), and whether it succeeded.
5. Open the **Change history** tab on an event that has one. Learn says it shows what changed on the resource up to 30 minutes before and after the operation. Not every event has changes.
6. Now open the Activity log from a single resource instead: open `rg-azb-core`, then **Activity log** in its menu. Learn says the menu you open it from sets the first filter. From a resource, it starts filtered to that resource.

Check: you found one event from an earlier lab, and you can say who did it and when.

**Failed deployment details.** When a create fails, the Activity log has an event with a failed status for it. Open that event and look for the error code and the error message in its details. The better place for the full message is the Deployments page in Part 2.

### Part 2: The Deployments page, why a create failed

**Idea 2: every create is a deployment.** When you create resources, Azure Resource Manager keeps a record of the deployment. Learn says that record includes errors, a correlation ID, and the operations inside the deployment. Support can use the correlation ID to find a failed deployment, so copy it if you ever open a support request. A resource group keeps up to 800 deployments, and the oldest are deleted as it fills.

7. Open `rg-azb-lab` (or any resource group where you created something). On the **Overview** page, select the link under **Deployments**.
8. Select a deployment from the list. Read the summary, including the **Correlation ID**.
9. If a deployment shows **Failed**, select **Operation details** on the summary. Learn says each step of the deployment is listed, and the failed step shows the error message.
10. Read the error in two parts: the **code** (a short name such as `QuotaExceeded`) and the **message** (the sentence that explains it). Search for the code, not the whole message.

Check: you opened one deployment, found its correlation ID, and opened **Operation details**. If you have no failed deployment, that is fine. Do not make one to practise.

### Part 3: Resource health and boot diagnostics, is the VM itself okay

**Idea 3: Azure tells you if the problem is on its side.** Resource Health reports the current and past health of a resource. For a virtual machine it answers one question first: is Azure having a problem, or is my configuration the problem?

11. Open your virtual machine `vm-azb-win01` from Lab 12 (if it still exists). In the left menu, select **Resource health**.
12. Read the status. Learn names four: **Available**, **Unavailable**, **Degraded** and **Unknown**.
    - **Available**: Azure sees no event that affects the resource. It does not say your RDP will work.
    - **Unavailable**: Azure sees a problem. Learn splits these into platform events (planned maintenance, an unplanned host reboot) and non-platform events caused by users, such as stopping a VM.
    - **Unknown**: Resource Health has had no information for more than 10 minutes. Learn says this commonly happens when VMs are deallocated. After Lab 13 this is the normal state of a stopped VM, not a fault.
    - **Degraded**: still up, but slower than it should be.
13. Open the **Health history**. Learn says the portal keeps up to 30 days.
14. Back in the VM menu, under **Help**, select **Boot diagnostics**. Learn says this shows a screenshot and the serial log of the VM as it boots. For Windows the screenshot normally shows the desktop background. If it shows an error screen or stays black, the VM is not booting properly, and the cause is inside the VM, not in the network.

Learn says boot diagnostics is on by default for VMs created in the portal, using a managed storage account, and that the data in the managed account is not currently billed. If the page says boot diagnostics is off, do not turn it on now. Note it for the next VM you build.

Check: you read the health status of the VM, and you know whether it is Unknown because it is deallocated.

### Part 4: Microsoft Entra sign-in logs, why a sign-in failed

**Idea 4: sign-in problems live in Entra, not in Azure.** The Activity log does not show failed sign-ins. Microsoft Entra keeps its own log for that. Learn says the sign-in logs answer who signed in, with which app, to which resource, and whether it worked.

Licence: Learn's retention table lists sign-in logs for **Microsoft Entra ID Free** with seven days of history, and 30 days for P1 and P2. So the free tenant from Lab 1 has sign-in logs, but only the last week. Learn also says that for Free, collection starts the first time you open Microsoft Entra ID. If the log is empty on your first visit, that can be why.

15. Go to the [Microsoft Entra admin center](https://entra.microsoft.com). Learn says you need at least the Reports Reader role. Global Administrator is enough.
16. Browse to **Entra ID** > **Monitoring & health** > **Sign-in logs**. The menu group may read **Identity** instead of **Entra ID**.
17. Filter to the user `testuser1` and the last 24 hours. Learn describes four log types: interactive user sign-ins, non-interactive user sign-ins, service principal sign-ins and managed identity sign-ins. The first tab, interactive, is the one you want for a person typing a password.
18. Open one sign-in. Read the **Status** or result, and the failure reason if there is one. Open the **Authentication Details** tab, which showed the Authenticator step in Lab 5. Look for a **Conditional Access** tab on the same record too. It tells you which policy applied.
19. Compare the time of the failed sign-in with what you did in the labs. Most sign-in problems in this series come from four causes:
    - MFA was asked for and not completed ([Lab 5: MFA](/azure-basics-labs/mfa/)).
    - A Conditional Access policy applied to the user ([Lab 6: Conditional Access](/azure-basics-labs/conditional-access/)).
    - Per-user MFA was set to **Enabled** or **Enforced** on top of Conditional Access. Lab 5 explains the error "The sign-in method you're trying to use isn't allowed" that comes from it.
    - The user signed in to a virtual machine with Entra, and the sign-in role or the sign-in extension on the VM was missing. "Your account is configured to prevent you from using this device" points to a missing role. "Your credentials didn't work" can come from a temporary password or from per-user MFA ([Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/)).

Check: you opened the last sign-in of `testuser1` and can say what the result was and which tab told you.

### Part 5: Three quick checks for the errors beginners hit most

These are three errors you can meet in any lab. Read them now so you know the fix before you need it.

**A. Provider not registered.** The error code is `MissingSubscriptionRegistration` or `NoRegisteredProviderFound`. Learn says it happens when you use a resource provider your subscription has not used before, and that most providers are registered for you by the portal and the CLI, but not all. The fix is in [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/):

20. Open **Subscriptions**, select your subscription, then under **Settings** select **Resource providers**. Find the provider named in the error message, select it, and select **Register**. Wait until it shows **Registered**, then run the step again.

**B. Quota exceeded.** Learn says each subscription has a vCPU limit in two levels for each region: Total Regional vCPUs, and a limit for each VM family. A new VM must fit inside both. Learn also says quota counts cores that are in use, allocated and deallocated, so a stopped VM still uses quota. Quota is also separate from capacity: Azure can lack room for a size in a region even when your quota is fine, and then a different size, zone or region can work.

21. In the subscription menu, select **Usage + quotas**. Filter to your region. Read the current usage and limit for the VM family in the error. Learn describes requesting more under the Quotas page. If a request is not possible for your account, pick a smaller VM size from [Lab 13: VM size, disk, stop and deallocate](/azure-basics-labs/vm-size-disk-stop-deallocate/) or a different region.

**C. Role not applied yet.** You gave a role and the next step still says you have no access. Learn says role assignment changes can take up to 10 minutes to take effect, and that you can force a refresh by signing out and signing in again (REST callers refresh the token).

22. Wait a few minutes. Sign out and sign in again. Then open the resource, select **Access control (IAM)** and **Check access**, and look up the user. [Lab 7: RBAC roles](/azure-basics-labs/rbac-roles/) shows how to read the result. If the role is not listed, the assignment was not made or was made at the wrong scope. If it is listed, wait and try again.

Check: you can say, for each of the three, where you look and what you do.

### Part 6: Network Watcher, which network rule is blocking

When a VM is running but you cannot connect, the cause is often a network security group (NSG) rule. [Lab 9: Network security group](/azure-basics-labs/network-security-group/) explains the rules. Network Watcher has two tools that name the rule for you. Learn says Network Watcher is turned on automatically in a region when you create or update a virtual network there, and that the automatic turn-on does not change your resources or add a charge.

**Cost.** I did not find a price for the individual tools on the Learn pages I read. Learn sends you to the [Network Watcher pricing page](https://azure.microsoft.com/pricing/details/network-watcher/). Read it before you run the tools, and run each one once.

23. First make sure `vm-azb-win01` is running: start it if it is deallocated. Learn says stopped virtual machines are not offered in the IP flow verify list. Then open **Network Watcher** (search for it in the portal). Under **Network diagnostic tools**, select **IP flow verify**.
24. Fill in the test. Learn's example for an inbound test: choose the VM, set **Direction** to **Inbound**, **Protocol** to **TCP**, **Local port** to the port you tried (3389 for RDP), **Remote IP address** to your own public IP, and any **Remote port**, such as 60000. The local IP address fills in with the VM's private IP.
25. Select **Check**. Learn says the result is **Access allowed** or **Access denied**, and it names the security rule that decided it.
26. If the result is **Access denied**, note the rule name. Open the NSG and compare it with what you built in Lab 9. The usual causes are no allow rule for your IP, a rule with the wrong priority, or an old public IP because your home address changed.
27. Next, check the NSGs together. Open the VM, then **Networking** > **Network settings**, select the network interface, and select **Effective security rules**. Learn says this shows the combined rules from the subnet NSG and the NIC NSG, and that traffic must pass both.

Check: IP flow verify says **Access allowed** for the port and address that should work, and you can name the rule that allows it.

If IP flow verify says allowed and you still cannot connect, the block is not the NSG. Look at the VM next (Part 3), then at the client ([Lab 11: Your PC and Remote Desktop clients](/azure-basics-labs/your-pc-and-remote-desktop-clients/)).

## Symptom to first place to look

| Symptom | First place to look | Lab that covers it |
|---|---|---|
| A create ended with "Deployment failed" | The resource group **Overview**, **Deployments**, the failed deployment, **Operation details** | This lab, Part 2 |
| You do not know who changed or deleted something | **Monitor** > **Activity log**, filter by resource group | This lab, Part 1 |
| `MissingSubscriptionRegistration` or `NoRegisteredProviderFound` | Subscription > **Resource providers** > **Register** | [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/) |
| `QuotaExceeded` or "exceeding approved cores quota" | Subscription > **Usage + quotas**, or `az vm list-usage` | [Lab 13](/azure-basics-labs/vm-size-disk-stop-deallocate/) |
| "Not authorized" right after you assigned a role | Wait up to 10 minutes, sign out and in, then **Access control (IAM)** > **Check access** | [Lab 7](/azure-basics-labs/rbac-roles/) |
| VM is Running but RDP will not connect | Network Watcher **IP flow verify**, then **Effective security rules** | [Lab 9](/azure-basics-labs/network-security-group/) and [Lab 11](/azure-basics-labs/your-pc-and-remote-desktop-clients/) |
| VM will not start, or shows a black screen | VM > **Resource health**, then **Help** > **Boot diagnostics** | [Lab 13](/azure-basics-labs/vm-size-disk-stop-deallocate/) |
| VM health says **Unknown** | Check whether the VM is deallocated. Learn says that is the common cause | [Lab 13](/azure-basics-labs/vm-size-disk-stop-deallocate/) |
| `net use` to the file share fails with "System error 1327" | A Conditional Access policy that requires MFA covers the storage account's Entra app | [Lab 14](/azure-basics-labs/storage-azure-files/) |
| A VM or key vault call returns 403 Forbidden right after you assigned a role | Wait a few minutes. A management role such as Owner does not read secrets. Check the data role | [Lab 15](/azure-basics-labs/key-vault-managed-identity/) |
| The heartbeat alert never sends an email | Check **Override query time range** on the rule, then the action group `ag-azb-email` | [Lab 16](/azure-basics-labs/log-analytics-alert/) |
| A create is refused with `RequestDisallowedByPolicy` | The error names the policy assignment. Read its scope and effect under **Policy** > **Assignments** | [Lab 17](/azure-basics-labs/azure-policy-locks/) |
| The share name still resolves to a public address, or the share stops working after you turn off public access | `nslookup` from the VM, the private DNS zone link, then the storage account **Networking** page | [Lab 18](/azure-basics-labs/private-endpoint-dns/) |
| A user cannot sign in, or gets an unexpected MFA prompt | Entra admin center > **Monitoring & health** > **Sign-in logs** | [Lab 5](/azure-basics-labs/mfa/) and [Lab 6](/azure-basics-labs/conditional-access/) |
| Sign-in fails on a VM that uses Entra sign-in | Sign-in logs for the user, then the VM settings | [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/) |
| "Workspace name already in use" when you create a workspace | **Log Analytics workspaces** > **Open recycle bin**. A deleted workspace keeps its name for 14 days | [Lab 16](/azure-basics-labs/log-analytics-alert/) |
| A resource group will not delete | A delete lock on the group or on one resource in it. A lock on one resource blocks the whole group delete | [Lab 17](/azure-basics-labs/azure-policy-locks/) |
| The budget email never came | Wait. Cost data arrives 8 to 24 hours late, and budgets are checked every 24 hours | [Lab 3](/azure-basics-labs/resource-group-tags-budget/) |

## Steps with the Azure CLI

The CLI does the same looking, and it does the cleanup in fewer clicks. Open Cloud Shell (Bash) from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Read the subscription first, and set the names once.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
LOCATION=<your-region>   # the one region you used in the series, for example eastus2
RG=rg-azb-lab
VM=vm-azb-win01
```

Read the Activity log for a resource group, then the deployments in it. `--offset` takes values like `7d`.

```bash
az monitor activity-log list --resource-group $RG --offset 7d --max-events 20 \
  --select eventName operationName status eventTimestamp -o table
az deployment group list --resource-group $RG -o table
```

For one failed deployment, print the failed operations and their error messages, and the correlation ID. Replace `DEPLOYMENT` with the name from the list above.

```bash
az deployment operation group list --resource-group $RG --name DEPLOYMENT \
  --query "[?properties.provisioningState=='Failed'].properties.statusMessage.error"
az deployment group show --resource-group $RG --name DEPLOYMENT \
  --query properties.correlationId
```

Check quota and provider registration.

```bash
az vm list-usage --location $LOCATION -o table
az provider list --query "[?registrationState=='NotRegistered'].namespace" -o tsv
az provider show --namespace Microsoft.Compute --query registrationState -o tsv
```

Read the VM boot log, and test the NSG. Replace the values in angle brackets. `10.10.1.4` is only an example from the range `10.10.1.0/24` in Lab 8. Use the private IP of your VM. The VM must be running.

```bash
az vm boot-diagnostics get-boot-log --name $VM --resource-group $RG
az network watcher test-ip-flow --direction Inbound --protocol TCP \
  --local 10.10.1.4:3389 --remote <your-public-ip>:60000 \
  --vm $VM --resource-group $RG --out table
az network nic list-effective-nsg --name <nic-name> --resource-group $RG --output table
```

Check: each command prints a table or text and no error. If a command says the VM or NIC does not exist, you already deleted it, which is fine.

Sign-in logs have no stable `az` command that I could confirm on Learn, so use the Entra admin center for those.

## Terraform

No Terraform in this lab, because reading a log is not something you describe in code. Terraform also only deletes what is in its own state file, and most of what you now need to remove was made by hand in the portal. The one Terraform project, from [Lab 10](/azure-basics-labs/terraform-basics/), is destroyed in step 5 of the clean up with `terraform destroy`.

## Check that it works

- You opened the Activity log, a deployment with its correlation ID, the health of a VM, boot diagnostics, the sign-in log of `testuser1`, and IP flow verify.
- `az group list -o table` shows `rg-azb-core` and no `rg-azb-lab`, `rg-azb-sandbox` or `rg-azb-tf`.
- The Conditional Access policy from Lab 6 is gone, and the soft-deleted key vault is purged or you know its name.
- Cost analysis, a day later, shows no cost from the deleted resources.

## The most common mistake

Deleting the resource groups and stopping there. Four things survive a group delete: a Conditional Access policy you forgot to remove in Lab 6 (it lives in the tenant), the Microsoft Entra app for the storage account from Lab 14, a soft-deleted key vault (it keeps its name until purged or until its retention ends) and a soft-deleted Log Analytics workspace (14 days). The Conditional Access policy is the one that bites, because it can block a sign-in weeks later and nothing in a resource group points to it.

The second mistake is looking in the wrong log. A failed sign-in is in the Entra sign-in log, not in the Activity log. A failed create is in the Deployments page, not in the sign-in log. The table above is there for that.

## Clean up

This is the last lab, so the clean up is the main job. The order matters. Locks and policy first, because they can block a delete. Then roles, the Terraform project and the resource groups. After that come the leftovers that hide once a group is gone: a soft-deleted key vault and a Conditional Access policy.

If you did only some labs, skip the steps for the labs you did not do. If you already cleaned up at the end of a lab, the check in that step will simply show nothing.

Read the tenant and subscription name again before you start. Then set the names once in Cloud Shell:

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
SUB_ID=$(az account show --query id -o tsv)
```

**Step 1: list what exists.**

```bash
az group list -o table
az resource list -g rg-azb-lab -o table
az resource list -g rg-azb-core -o table
```

Write down every group name. You can expect `rg-azb-core` and `rg-azb-lab`. You may also see `rg-azb-sandbox` (Lab 17 deletes it at its end) and `rg-azb-tf` (Lab 10 destroys it at its end). A group you did not create stays. That can be one Azure made for Network Watcher, or, if you chose a Cloud Shell storage account in Lab 2, a group with a name like `cloud-shell-storage-<region>`. Do not delete groups you did not create.

`rg-azb-core` should hold only the action group `ag-azb-email`. The alert rule, the data collection rule and the workspace from Lab 16 are in `rg-azb-lab`.

**Step 2: remove locks.** Learn says a Delete lock on one resource blocks the delete of the whole resource group, even when everything else is unlocked. Lab 17 made one lock, `lock-azb-nodelete`, on a storage account in `rg-azb-sandbox`. Find any lock and remove it.

```bash
az lock list --resource-group rg-azb-sandbox -o table
az lock list --resource-group rg-azb-lab -o table
```

In the portal you can also open each resource group and each storage account and select **Locks**. To remove the Lab 17 lock, use the name of the storage account it sits on:

```bash
az lock delete --name lock-azb-nodelete --resource-group rg-azb-sandbox \
  --resource <storage-account-name> --resource-type Microsoft.Storage/storageAccounts
```

For a lock on a resource group, use `az lock delete --name <lock-name> --resource-group <group-name>`. A lock set on the subscription is removed with `az lock delete --name <lock-name>`.

Check: the lock lists print nothing.

**Step 3: remove policy assignments.** Lab 17 made two assignments on `rg-azb-sandbox`. If you ran the CLI part they are named `allowed-locations-azb` and `require-tag-env-azb`. If you used the portal, the name can be different from the display names `Allowed locations (sandbox)` and `Require env tag (sandbox)`, so list them first.

```bash
SANDBOX_ID=$(az group show --name rg-azb-sandbox --query id -o tsv)
az policy assignment list --resource-group rg-azb-sandbox --query "[].name" -o tsv
az policy assignment delete --name <assignment-name> --scope "$SANDBOX_ID"
```

Run the last command once for each name the list prints. In the portal: **Policy** > **Assignments**, open the ellipsis of each assignment, then **Delete assignment**. If `rg-azb-sandbox` is already gone, there is nothing to do here.

**Step 4: remove role assignments.** Lab 7 gave the group `TestUsers` Reader on the subscription and Contributor on `rg-azb-core`. Lab 7's clean up removes them. Check that nothing is left.

```bash
GROUP_ID=$(az ad group show --group TestUsers --query id -o tsv)
az role assignment list --assignee "$GROUP_ID" --all -o table
```

Remove the subscription-level Reader first, then the Contributor, if they still show:

```bash
az role assignment delete --assignee "$GROUP_ID" --role "Reader" --scope "/subscriptions/$SUB_ID"
az role assignment delete --assignee "$GROUP_ID" --role "Contributor" --scope "/subscriptions/$SUB_ID/resourceGroups/rg-azb-core"
```

Other assignments from the labs sit on resources that you are about to delete, and they go with them: **Virtual Machine User Login** on `rg-azb-lab` (Lab 12), **Storage File Data SMB Share Contributor** on the share (Lab 14), and the two Key Vault roles on the vault (Lab 15). Learn says role assignments on a soft-deleted vault are deleted.

**Step 5: destroy the Terraform project.** If you did Lab 10 and did not destroy it yet, go to that project folder and run `terraform destroy`. Read the plan. Type `yes` only if every name starts with `rg-azb-tf`, `vnet-azb-tf`, `snet-azb-tf` or `nsg-azb-tf`. Then check:

```bash
az group exists --name rg-azb-tf
```

Check: it prints `false`.

**Step 6: delete the sandbox group.** This is `rg-azb-sandbox` from Lab 17. Skip this step if it is already gone.

```bash
az group delete --name rg-azb-sandbox --no-wait
```

The command asks you to confirm. Type `y` only after you read the name. `--no-wait` returns at once and the delete continues in Azure.

**Step 7: delete the lab group.** `rg-azb-lab` holds the main lab resources. Before you delete it, look at what is inside, so you know what goes.

```bash
az resource list -g rg-azb-lab -o table
```

You should see some or all of these:

- The virtual machine `vm-azb-win01`, its OS disk, its network interface and the public IP address `pip-azb-win01`, plus the auto-shutdown schedule if you set one in Lab 12.
- The network security group `nsg-azb-vm` and the virtual network `vnet-azb` with its subnets `snet-vm` and `snet-pe`.
- The storage account `stazb` and five digits, with the file share `azbshare`.
- The private endpoint `pe-azb-file` with its network interface, and the private DNS zone `privatelink.file.core.windows.net` with its link to `vnet-azb`.
- The key vault `kv-azb-` and five digits, unless you already deleted it in Lab 15.
- The Log Analytics workspace `log-azb-lab`, the data collection rule `dcr-azb-lab` and the alert rule `VM not sending heartbeat`, unless you already removed them in Lab 16.

Deleting the group removes all of them in one go, which is why the labs put them in one group.

Do the workspace first. Learn says a deleted workspace keeps its name for 14 days and can be recovered, and that to free the name at once you delete it permanently. If you do not plan to reuse the name `log-azb-lab`, skip this and let the 14 days pass. If you do:

```bash
az monitor log-analytics workspace delete --resource-group rg-azb-lab \
  --workspace-name log-azb-lab --force true --yes
```

This cannot be undone. Then delete the group:

```bash
az group delete --name rg-azb-lab --no-wait
```

If you prefer to remove the resources one by one in the portal, do the VM first, then its disk, network interface and public IP, then the private endpoint, the storage account, the key vault and the workspace, then the NSG, and the virtual network last. Azure can refuse to delete something that another resource still uses. Deleting the whole group is simpler and leaves nothing behind.

If the delete fails and the message mentions a lock, go back to step 2.

**Step 8: purge the soft-deleted key vault.** Learn says a deleted key vault is kept in a soft-deleted state and can be recovered or purged. If you deleted `rg-azb-lab` with the vault inside, the vault is now soft-deleted too. Purging deletes it for good and frees the name. You only need this if you want to reuse the vault name or want nothing left.

```bash
az keyvault list-deleted --resource-type vault -o table
az keyvault purge --name kv-azb-<5 digits>
```

If the purge is refused, read the message. Learn says that when purge protection is on, you cannot purge a vault until the retention period ends. Lab 15 told you not to turn it on, so this should not happen. In that case the vault stays in the deleted list until its retention time ends.

**Step 9: check the Microsoft Entra leftovers.** These are not in any resource group, so deleting the groups does not remove them.

1. Go to the [Microsoft Entra admin center](https://entra.microsoft.com). Check the tenant name.
2. Browse to **Entra ID** > **Conditional Access** > **Policies**.
3. Lab 6 told you to delete its policy in Part 7. Check that no policy named like `CA-AVD-RequireMFA-TestUsers-REPORTONLY` is still in the list. If it is, select it and select **Delete**, then confirm. A policy left on can still ask `testuser1` for MFA the next time you build an AVD lab, which looks like a sign-in fault you made yourself. Microsoft-managed policies that were there before you started stay.
4. If you added `[Storage Account] stazb<5 digits>.file.core.windows.net` to the excluded apps of an all-resources MFA policy in Lab 14, that exclusion is harmless once the account is gone. Leave the policy as it is.
5. Browse to **Entra ID** > **App registrations** > **All applications** and search for `[Storage Account]`. Lab 14 turned on Microsoft Entra Kerberos for the account, and Azure created an app for it. Once the storage account is gone, if an app named for it is still listed, open it and delete it. I did not find a Learn page that says what happens to this app when the account is deleted, so look.
6. If security defaults were **Enabled** when you started Lab 6, you can turn them back on now, under **Entra ID** > **Overview** > **Properties** > **Manage security defaults**. Learn says they cannot be used together with Conditional Access, so do this only after the policy is gone.

If you started a trial or bought a licence for Lab 6, end it where you got it. Check the terms you accepted.

**Step 10: check what is left.**

```bash
az group list -o table
az group exists --name rg-azb-lab
az group exists --name rg-azb-sandbox
```

The deletes take a few minutes. Run the commands again until `rg-azb-lab` and `rg-azb-sandbox` print `false`. In the portal, **Resource groups** > **Refresh** shows the same.

### What to keep, and what to delete

Keep these. They cost nothing and the AVD labs use them:

- `rg-azb-core`, with `ag-azb-email` and the budget `budget-azb-core`. The budget will warn you when the AVD labs start to spend.
- The test user `testuser1`, the group `TestUsers`, and their MFA registration from Lab 5.
- The emergency accounts `emergency-access-01` and `emergency-access-02`, and the group `EmergencyAccess`. Do not delete them while the tenant exists.
- The registered resource providers from Lab 1.
- Your Azure free account. It gives $200 of credit for 30 days, and the credit is a limit, not a plan to spend it.
- The Cloud Shell storage group, if you chose one in Lab 2 and still use Cloud Shell. Learn warns that deleting it erases your `$HOME` files.

Delete these if you are done with them:

- The budget and `rg-azb-core`, if you are finished with the whole series and will not build the AVD labs. Open **Cost Management** > **Budgets**, open `budget-azb-core` and delete it. Then run `az group delete --name rg-azb-core`, after you read the name twice.
- The Terraform project folder from Lab 10, once you have copied what you want. Delete `terraform.tfstate` and `main.tfplan`, or keep the folder out of Git.
- `testuser1` and `TestUsers`, only if you will not build the AVD labs. They are easy to create again from [Lab 4](/azure-basics-labs/entra-users-groups-break-glass/).
- The whole test tenant, only when you are finished with the series. [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/) says how: open Microsoft Entra ID in that tenant and select **Delete directory**. Azure may refuse and tell you why. Read the tenant name first.

### Cost check the next day

A delete in the middle of a day still shows some cost for that day, and Learn says the full effect of a change is not visible until the next full day. Cost data also arrives 8 to 24 hours late. So check tomorrow, then again the day after.

1. In the portal, open **Cost Management** and select **Cost analysis**. Set the scope to your subscription.
2. Set the date range to this month. Change the view to **Daily costs**, and set **Granularity** to **Daily**. Learn says daily view works for a range of up to three months.
3. Group by **Resource** (Learn's menu is **View** > **Cost by resource**, and you can also change **Group by**). Look at the last two days.
4. You expect: some cost on the day you deleted things, and zero or close to zero the day after. If a resource still shows cost the day after, open it by name. It is a leftover that the group delete did not cover, or a resource in a group you did not list in step 1.

Check: the daily cost for the day after the clean up is zero or close to it, and no resource from Labs 8 to 18 appears in the list.

## Where this is used in AVD

Every AVD problem starts with the same question: which of the steps failed? The article [How Azure Virtual Desktop Fails](/azure-virtual-desktop/how-azure-virtual-desktop-fails/) sorts the failures by where they happen, and [Follow a Connection Step by Step](/azure-virtual-desktop/follow-a-connection-step-by-step/) walks the path a user takes so you know which log to open at each step. The logs in this lab are the ones you will open there.

## Next lab

There is no Lab 20. You have now built the small parts: an account and a tenant, a resource group with a budget, people and roles, a network, a virtual machine, storage, a vault, logging, policy and a private endpoint. You have also deleted all of it. Next, build the real thing once, in code, so you can build it again and delete it again. [Quick AVD Lab with Terraform](/terraform-labs/avd-quick-lab/) builds a small Azure Virtual Desktop environment on top of what you kept. If you want the theory first, the AVD series starts at [What Is Azure Virtual Desktop](/azure-virtual-desktop/what-is-azure-virtual-desktop/). Keep the budget on, read the cost after every lab, and delete when you are done.

## Sources

- [Activity log in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log)
- [View deployment history with Azure Resource Manager](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deployment-history)
- [Resource Health overview](https://learn.microsoft.com/en-us/azure/service-health/resource-health-overview)
- [Azure boot diagnostics](https://learn.microsoft.com/en-us/azure/virtual-machines/boot-diagnostics)
- [az vm boot-diagnostics](https://learn.microsoft.com/en-us/cli/azure/vm/boot-diagnostics)
- [What are Microsoft Entra sign-in logs?](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins)
- [Microsoft Entra data retention](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-reports-data-retention)
- [Resolve errors for resource provider registration](https://learn.microsoft.com/en-us/azure/azure-resource-manager/troubleshooting/error-register-resource-provider)
- [Check vCPU quotas](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas)
- [Troubleshoot Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshooting)
- [What is Azure Network Watcher?](https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-overview)
- [Enable or disable Azure Network Watcher](https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-create)
- [Diagnose a virtual machine network traffic filter problem](https://learn.microsoft.com/en-us/azure/network-watcher/diagnose-vm-network-traffic-filtering-problem)
- [Lock your Azure resources to protect your infrastructure](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources)
- [az lock](https://learn.microsoft.com/en-us/cli/azure/lock)
- [az group](https://learn.microsoft.com/en-us/cli/azure/group)
- [az policy assignment](https://learn.microsoft.com/en-us/cli/azure/policy/assignment)
- [Delete and recover a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/delete-workspace)
- [Azure Key Vault recovery management with soft delete and purge protection](https://learn.microsoft.com/en-us/azure/key-vault/general/key-vault-recovery)
- [Quickstart: Start using Cost Analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis)
- [Customize views in Cost Analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/customize-cost-analysis-views)
- [Identify anomalies and unexpected changes in cost](https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/analyze-unexpected-charges)
