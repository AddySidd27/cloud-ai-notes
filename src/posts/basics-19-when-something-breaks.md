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

By the end of this lab you will know where to look first when an Azure step fails, and you will have deleted everything you built in Labs 1 to 18 except what the next series needs. Then you check Cost analysis the next day.

This page does two jobs. **Part A** (about 30 minutes) is a short tour of the places to look. **Part B** (about 30 minutes) deletes the whole series. If you only want to stop spending money, go straight to [Clean up](#clean-up). If you stopped after Lab 12, you can safely stop by deleting `rg-azb-lab`.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

Most Azure problems in this series come from a short list: a missing permission, a rule that blocks traffic, a limit on your subscription, or something that was not ready yet. Azure keeps a record of nearly everything it does. The skill is knowing which record to open.

## Start here: symptom to first place to look

| Symptom | First place to look | Lab |
|---|---|---|
| A create ended with "Deployment failed" | Resource group **Overview** > **Deployments** > the failed deployment > **Operation details** | This lab, Part 2 |
| You do not know who changed or deleted something | **Monitor** > **Activity log**, filter by resource group | This lab, Part 1 |
| `MissingSubscriptionRegistration` or `NoRegisteredProviderFound` | Subscription > **Resource providers** > **Register** | [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/) |
| `QuotaExceeded` or "exceeding approved cores quota" | Subscription > **Usage + quotas**, or `az vm list-usage` | [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/) |
| "Not authorized" right after you assigned a role | Wait up to 10 minutes, sign out and in, then **Access control (IAM)** > **Check access** | [Lab 7](/azure-basics-labs/rbac-roles/) |
| VM is Running but RDP will not connect | Network Watcher **IP flow verify**, then **Effective security rules** | [Lab 9](/azure-basics-labs/network-security-group/) and [Lab 11](/azure-basics-labs/your-pc-and-remote-desktop-clients/) |
| VM will not start, shows a black screen, or its health says **Unknown** | VM > **Resource health**, then **Help** > **Boot diagnostics**. **Unknown** is normal for a deallocated VM | [Lab 13](/azure-basics-labs/vm-size-disk-stop-deallocate/) |
| A user cannot sign in, gets an unexpected MFA prompt, or fails to sign in to the VM | Entra admin center > **Monitoring & health** > **Sign-in logs**, then the VM settings | [Lab 5](/azure-basics-labs/mfa/), [Lab 6](/azure-basics-labs/conditional-access/) and [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/) |
| The Connect page offers **Request access**, or RDP times out on a VM with a just-in-time (JIT) policy | Select **Request access** on the VM's **Connect** page first, then download and open the RDP file. Learn says this is needed when the VM has a JIT policy | [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/) |
| AADSTS293004 (target-device identifier not found) | You typed a full domain name. Use the short VM name `vm-azb-win01` | [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/) |
| "Your credentials didn't work" on the first Entra sign-in | The user still has a temporary password. Sign in as the user in a private window, set the new password, then try RDP again | [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/) |
| RDP times out even though the NSG rule and IP flow verify say allowed | Some office and hotel networks block outbound TCP 3389. Try another network | [Lab 11](/azure-basics-labs/your-pc-and-remote-desktop-clients/) |
| "The sign-in method you're trying to use isn't allowed" | A Conditional Access policy that requires MFA covers the app **Microsoft Azure Windows Virtual Machine Sign-in** and your PC does not use strong authentication. In the throwaway tenant, turn that policy off or exclude that app. Also check that per-user MFA shows **Disabled** | [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/) and [Lab 6](/azure-basics-labs/conditional-access/) |
| `net use` to the file share fails with "System error 1327" | A Conditional Access policy that requires MFA covers the storage account's Entra app | [Lab 14](/azure-basics-labs/storage-azure-files/) |
| A key vault call returns 403 Forbidden after you assigned a role | Wait a few minutes. A management role such as Owner does not read secrets. Check the data role | [Lab 15](/azure-basics-labs/key-vault-managed-identity/) |
| The heartbeat alert never sends an email, or "Workspace name already in use" | Check **Override query time range** on the rule, then `ag-azb-email`. A deleted workspace keeps its name for 14 days (**Open recycle bin**) | [Lab 16](/azure-basics-labs/log-analytics-alert/) |
| A create is refused with `RequestDisallowedByPolicy`, or a resource group will not delete | The error names the policy assignment (**Policy** > **Assignments**). For the delete, look for a lock on the group or on one resource in it | [Lab 17](/azure-basics-labs/azure-policy-locks/) |
| The share name still resolves to a public address, or the share stops working after you turn off public access | `nslookup` from the VM, the private DNS zone link, then the storage account **Networking** page | [Lab 18](/azure-basics-labs/private-endpoint-dns/) |
| The budget email never came | Wait. Cost data arrives 8 to 24 hours late, and budgets are checked every 24 hours | [Lab 3](/azure-basics-labs/resource-group-tags-budget/) |

## What you need

- The earlier labs, as far as you did them. Each lab you did left something behind, and Part B deletes it. If you only did some labs, skip the steps for the labs you did not do.
- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/) and [Lab 2: Azure Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/), for the sign-in and the command line.
- Owner or Contributor on the subscription, and Global Administrator in the tenant. You need these to delete resources and to delete the Conditional Access policy.
- Time: about 60 minutes, plus a five-minute look the next day. Cost: nothing for the looking. The Network Watcher checks may have a price, see Part 6. The clean up stops the cost of everything you left running.

**State of your resources**

| | At the start | At the end |
| --- | --- | --- |
| VM `vm-azb-win01` | Stopped (deallocated). Parts 3 and 6 need it running, so start it there (**Virtual machines** > `vm-azb-win01` > **Start**). | Stopped (deallocated) at the end of Part A (step 25), then deleted with `rg-azb-lab` in Part B |
| Rule `allow-rdp-my-ip` in `nsg-azb-vm` | Not there. Part 6 expects that. | Deleted with `rg-azb-lab` |
| Public IP `pip-azb-win01` | Exists | Deleted with `rg-azb-lab` |
| Kept | `rg-azb-core`, `ag-azb-email`, `budget-azb-core`, `testuser1`, `TestUsers`, the emergency accounts | Same |

## Safety first

- Use the throwaway tenant only. Read the tenant name and the subscription name before you delete anything.
- Deleting a resource group deletes everything inside it. It cannot be undone. Read each name twice. Never run a delete on `rg-azb-core` unless you are finished with the whole series.
- `az group delete` without `--yes` asks you to confirm. Keep it that way.
- Do not use `az login --use-device-code`. Cloud Shell is already signed in.
- A budget only sends emails. It does not stop anything. The clean up is what stops the cost.
- In Part A you only look. Do not turn on anything new to investigate a problem.

## What the lab builds

![A diagram with two jobs. Part A, left and middle: six symptoms each point to one place to look. Create failed points to Deployments, who changed it points to the Activity log, VM black screen or Unknown points to Resource health and boot diagnostics, cannot sign in points to the Microsoft Entra sign-in logs, quota or provider error points to Usage and quotas, and RDP will not connect points to Network Watcher IP flow verify. Part B, right: the clean up in the order of the Clean up steps. Steps 2 and 3 remove locks and policy assignments. Steps 4 and 5 check role assignments and destroy the Terraform project in rg-azb-tf. Steps 6 to 8 delete rg-azb-sandbox and rg-azb-lab and wait until they are gone. Step 9 purges the soft-deleted key vault. Step 10 removes the Microsoft Entra leftovers: the device vm-azb-win01, the storage account app and any Conditional Access policy. The last box is Cost analysis the next day. A green box keeps rg-azb-core, testuser1, TestUsers and the emergency accounts.](/img/basics/when-something-breaks.svg)

*Source: [Activity log in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log), [View deployment history with Azure Resource Manager](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deployment-history), [Resource Health overview](https://learn.microsoft.com/en-us/azure/service-health/resource-health-overview), [Microsoft Entra sign-in logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins) and [What is Azure Network Watcher?](https://learn.microsoft.com/en-us/azure/network-watcher/network-watcher-overview). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Part A: Where to look

#### Part 1: The Activity log, who did what

**Idea 1: Azure writes down every change.** The Activity log records management operations on your resources: creating a VM, deleting a group, a deployment that failed. It is on by default, you cannot edit it, and Azure keeps entries for 90 days. Entries show up 3 to 20 minutes after the event. It is not an audit log of rejected requests, so an empty log does not prove nobody tried.

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant and subscription name.
2. Search for and open **Monitor**, then select **Activity log**.
3. Set the time range to the last 7 days. Use **Add Filter** to filter by **Resource group**, **Operation**, **Event initiated by** or **Event category**.
4. Open the Activity log of `rg-azb-lab` and open the newest event, which comes from your last lab. Read three things: what operation it was, who started it (the **Event initiated by** value), and whether it succeeded. For an older event, look for the resource group `rg-azb-practice` that you deleted in Lab 3 (it may be past the filter).
5. Open the **Change history** tab on an event that has one. It shows what changed on the resource. Not every event has changes.
6. Open the Activity log from a single resource: open `rg-azb-core`, then **Activity log** in its menu. It starts filtered to that resource.

Check: you found one event from an earlier lab, and you can say who did it and when. A failed create shows up here with a failed status. The full message is on the Deployments page in Part 2.

#### Part 2: The Deployments page, why a create failed

**Idea 2: every create is a deployment.** Azure keeps a record of each deployment, with errors, a correlation ID and the operations inside it. Copy the correlation ID if you ever open a support request.

7. Open `rg-azb-lab`. On the **Overview** page, select the link under **Deployments**.
8. Select a deployment. Read the summary, including the **Correlation ID**.
9. If a deployment shows **Failed**, select **Operation details**. The failed step shows the error message.
10. Read the error in two parts: the **code** (a short name such as `QuotaExceeded`) and the **message**. Search for the code, not the whole message.

Check: you opened one deployment and found its correlation ID. If you have no failed deployment, that is fine. Do not make one to practise.

Optional, if `rg-azb-sandbox` from Lab 17 still exists: its **Deployments** page shows the deployment that policy refused. Find the code `RequestDisallowedByPolicy` and the name of the policy assignment in it. If Lab 17 is already cleaned up, skip this.

#### Part 3: Resource health and boot diagnostics, is the VM itself okay

**Idea 3: Azure tells you if the problem is on its side.** Resource Health answers one question first: is Azure having a problem, or is my configuration the problem?

11. Open your VM `vm-azb-win01` (if it still exists). In the left menu, select **Resource health**.
12. Read the status. Learn names four: **Available**, **Unavailable**, **Degraded** and **Unknown**. Your VM is deallocated now, so you should see **Unknown**. That is the normal state of a deallocated VM, not a fault. **Available** does not promise that RDP works.
13. Open the **Health history** to see past events for the resource.
14. Start the VM and wait for **Running**. In the VM menu, under **Help**, select **Boot diagnostics**. It shows a screenshot and the serial log of the VM. For Windows the screenshot normally shows the desktop background. If it shows an error screen or stays black, the VM is not booting properly, and the cause is inside the VM, not in the network. If the page says boot diagnostics is off, do not turn it on now.

Check: you read the health status of the VM and you know why it said Unknown.

#### Part 4: Microsoft Entra sign-in logs, why a sign-in failed

**Idea 4: sign-in problems live in Entra, not in Azure.** The Activity log does not show failed sign-ins. Microsoft Entra keeps its own log. On the free tier it holds the last 7 days, and collection starts the first time you open Microsoft Entra ID, so an empty log on your first visit can be why.

15. Go to the [Microsoft Entra admin center](https://entra.microsoft.com). You need at least the Reports Reader role. Global Administrator is enough.
16. Browse to **Entra ID** > **Monitoring & health** > **Sign-in logs**. The menu group may read **Identity** instead of **Entra ID**.
17. Filter to the user `testuser1` and the last 24 hours. The first tab, interactive sign-ins, is the one for a person typing a password.
18. Open one sign-in. Read the **Status** or result and the failure reason if there is one. Open the **Authentication Details** tab, and the **Conditional Access** tab, which tells you which policy applied.
19. Most sign-in problems in this series come from four causes: MFA was asked for and not completed ([Lab 5](/azure-basics-labs/mfa/)); a Conditional Access policy applied to the user ([Lab 6](/azure-basics-labs/conditional-access/)); per-user MFA was set to **Enabled** or **Enforced** on top of Conditional Access (the error "The sign-in method you're trying to use isn't allowed", see Lab 5); or the sign-in role or extension on the VM was missing ("Your account is configured to prevent you from using this device" points to a missing role, see [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/)).

Check: you opened the last sign-in of `testuser1` and can say what the result was.

#### Part 5: Three quick checks for the errors beginners hit most

You can meet these three errors in any lab. Read them now so you know the fix before you need it.

**A. Provider not registered.** The error code is `MissingSubscriptionRegistration` or `NoRegisteredProviderFound`. It looks like "The subscription is not registered to use namespace 'Microsoft.Xyz'". Most providers are registered for you by the portal and the CLI, but not all. Do this: open **Subscriptions**, select your subscription, then under **Settings** select **Resource providers**. Find the provider named in the error, select **Register**, and wait until it shows **Registered**. Then run the step again.

**B. Quota exceeded.** Each subscription has a vCPU limit for each region and for each VM family, and a new VM must fit inside both. A deallocated VM still uses quota. Do this: in the subscription menu, select **Usage + quotas**, filter to your region and read the usage and limit for the VM family in the error. If you cannot raise the limit, pick a smaller size ([Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/) Part 1 covers quota, [Lab 13](/azure-basics-labs/vm-size-disk-stop-deallocate/) covers sizes) or a different region.

**C. Role not applied yet.** You gave a role and the next step still says you have no access. A role change can take up to 10 minutes to take effect. Do this: wait a few minutes, sign out and sign in again, then open the resource, select **Access control (IAM)** > **Check access** and look up the user ([Lab 7](/azure-basics-labs/rbac-roles/) shows how to read the result). If the role is not listed, the assignment was not made or was made at the wrong scope.

#### Part 6: Network Watcher, which network rule is blocking

When a VM is running but you cannot connect, the cause is often a network security group (NSG) rule ([Lab 9](/azure-basics-labs/network-security-group/)). Network Watcher has two tools that name the rule for you. It is turned on automatically when you create a virtual network in a region. I did not find a price for the individual tools on the Learn pages I read, so open the [Network Watcher pricing page](https://azure.microsoft.com/pricing/details/network-watcher/) first and run each tool once.

**Predict, then check.** You deleted the RDP rule at the end of Labs 12, 14, 15 and 18. So what should IP flow verify say for port 3389 from your PC? Write down your guess, then run it.

20. Make sure `vm-azb-win01` is running (you started it in Part 3). Stopped VMs are not offered in the IP flow verify list. Open **Network Watcher**, then under **Network diagnostic tools** select **IP flow verify**.
21. Fill in the test: choose the VM, set **Direction** to **Inbound**, **Protocol** to **TCP**, **Local port** to `3389`, **Remote IP address** to your own public IP (look it up on your PC), and any **Remote port**, such as `60000`. The local IP fills in with the VM's private IP.
22. Select **Check**. Expected result now: **Access denied**, by the default rule that denies all inbound traffic (its name ends in `DenyAllInBound`). That is correct. It proves the RDP rule is gone. Read the rule name in the result.
23. Optional: to see **Access allowed**, add `allow-rdp-my-ip` again (follow "Connect again later" in [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/), step 3 only), run the test again, and then delete the rule. The result now names your rule.
24. Check the NSGs together. Open the VM, then **Networking** > **Network settings**, select the network interface, and select **Effective security rules**. It shows the combined rules from the subnet NSG and the NIC NSG, and traffic must pass both.

25. Stop the VM so nothing bills while you read on: **Virtual machines** > `vm-azb-win01` > **Stop**. Check that the status says **Stopped (deallocated)**. If you added `allow-rdp-my-ip` in step 23, make sure you deleted it again.

Check: you got **Access denied** with a rule name, and you can say why. If IP flow verify says allowed and you still cannot connect, the block is not the NSG. Look at the VM (Part 3), then at the client ([Lab 11](/azure-basics-labs/your-pc-and-remote-desktop-clients/)).

#### Self-test

Answer without scrolling up. A user cannot sign in: which log? A create failed: which page? RDP does not work but the VM is Running: which tool? (Entra sign-in logs, the Deployments page, IP flow verify.)

## Steps with the Azure CLI

The CLI does the same looking. The clean up commands are in Part B. Open Cloud Shell (Bash) from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Read the subscription first, and set the names once. Anything in ALL CAPS after a `#` comment is yours to change. Run `echo` on a variable before you use it. If Cloud Shell restarts, set them again.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
RG=rg-azb-lab
VM=vm-azb-win01
LOCATION=$(az vm show --resource-group $RG --name $VM --query location -o tsv)   # the region of your VM
echo "$LOCATION"
```

Read the Activity log for a resource group, then the deployments in it. `--offset` takes values like `7d`.

```bash
az monitor activity-log list --resource-group $RG --offset 7d --max-events 20 \
  --select eventName operationName status eventTimestamp -o table
az deployment group list --resource-group $RG -o table
```

For one failed deployment, print the failed operations with their error messages, and the correlation ID. Set `DEPLOYMENT` to a name from the list above.

```bash
DEPLOYMENT=NAME_FROM_THE_LIST   # replace with a deployment name
az deployment operation group list --resource-group $RG --name $DEPLOYMENT \
  --query "[?properties.provisioningState=='Failed'].properties.statusMessage.error"
az deployment group show --resource-group $RG --name $DEPLOYMENT \
  --query properties.correlationId
```

Check quota and provider registration.

```bash
az vm list-usage --location $LOCATION -o table
az provider list --query "[?registrationState=='NotRegistered'].namespace" -o tsv
az provider show --namespace Microsoft.Compute --query registrationState -o tsv
```

Read the VM boot log, and test the NSG. The VM must be running. Set `MYIP` to your own public IP: look it up on your PC, because Cloud Shell shows Cloud Shell's address, not yours.

```bash
MYIP=198.51.100.25   # replace with your own public IP
case "$MYIP" in 198.51.100.*|"") echo "STOP: set MYIP to your own public IP";; esac
VM_IP=$(az vm list-ip-addresses --resource-group $RG --name $VM --query "[0].virtualMachine.network.privateIpAddresses[0]" -o tsv)
NIC=$(az vm show --resource-group $RG --name $VM --query "networkProfile.networkInterfaces[0].id" -o tsv | sed 's|.*/||')
echo "$VM_IP $NIC"
az vm boot-diagnostics get-boot-log --name $VM --resource-group $RG
az network watcher test-ip-flow --direction Inbound --protocol TCP \
  --local $VM_IP:3389 --remote $MYIP:60000 \
  --vm $VM --resource-group $RG --out table
az network nic list-effective-nsg --name $NIC --resource-group $RG --output table
```

When you are done, stop the VM: `az vm deallocate --resource-group $RG --name $VM`.

Check: each command prints a table or text and no error. With no RDP rule, `test-ip-flow` prints `Deny` and a rule name ending in `DenyAllInBound`. If a command says the VM or NIC does not exist, you already deleted it, which is fine. Sign-in logs have no stable `az` command that I could confirm on Learn, so use the Entra admin center for those.

## Terraform

No Terraform in this lab, because reading a log is not something you describe in code. Terraform also only deletes what is in its own state file, and most of what you now need to remove was made by hand in the portal. The one Terraform project, from [Lab 10](/azure-basics-labs/terraform-basics/), is destroyed in step 5 of the clean up with `terraform destroy`.

## Check that it works

- You opened the Activity log, a deployment with its correlation ID, the health of a VM, boot diagnostics, the sign-in log of `testuser1`, and IP flow verify.
- `az group list -o table` shows `rg-azb-core` and no `rg-azb-lab`, `rg-azb-sandbox` or `rg-azb-tf`.
- No Conditional Access policy from Lab 6, no device `vm-azb-win01` and no `[Storage Account]` app are left, and the soft-deleted key vault is purged.
- Cost analysis, a day later, shows no cost from the deleted resources.

## The most common mistake

Deleting the resource groups and stopping there. Things that survive a group delete live outside the group: a Conditional Access policy you forgot to remove in Lab 6 (it lives in the tenant), the Microsoft Entra app for the storage account from Lab 14, the Entra device record `vm-azb-win01` from Lab 12, a soft-deleted key vault (it keeps its name until purged) and a soft-deleted Log Analytics workspace (14 days). The Conditional Access policy is the one that bites, because it can block a sign-in weeks later and nothing in a resource group points to it.

The second mistake is looking in the wrong log. A failed sign-in is in the Entra sign-in log, not in the Activity log. A failed create is on the Deployments page, not in the sign-in log. The table at the top is there for that.

## Clean up

This is Part B. The order matters. Locks and policy first, because they can block a delete. Then roles, the Terraform project and the resource groups. After that come the leftovers that hide once a group is gone: a soft-deleted key vault and the items in Microsoft Entra.

If you did only some labs, skip the steps for the labs you did not do. If you already cleaned up at the end of a lab, the check in that step simply shows nothing. If you stopped after Lab 12, you only need steps 1, 7, 8 and 10. Use this table to see what each lab left behind:

| If you did | Delete this | Step |
|---|---|---|
| Lab 17 | Lock `lock-azb-nodelete`, two policy assignments, `rg-azb-sandbox` | 2, 3, 6 |
| Lab 7 | Role assignments for `TestUsers` (Lab 7 removes them itself) | 4 |
| Lab 10 | `rg-azb-tf` | 5 |
| Labs 8 to 16 and 18 | Everything in `rg-azb-lab` (VM, disk, NIC, `pip-azb-win01`, `nsg-azb-vm`, `vnet-azb`, storage account, private endpoint, DNS zone, workspace) | 7 |
| Lab 15 | Soft-deleted key vault `kv-azb-<digits>` (Lab 15 purges it itself) | 9 |
| Lab 12 | Device `vm-azb-win01` in Entra, the `hosts` line (route C), `test.rdp` | 10 |
| Lab 11 | The registered PC (route B), `test.rdp` | 10 |
| Lab 14 | The `[Storage Account]` app in Entra | 10 |
| Lab 6 | The Conditional Access policy, if you did not delete it | 10 |

Read the tenant and subscription name again before you start. Then in Cloud Shell:

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
SUB_ID=$(az account show --query id -o tsv)
```

1. **List what exists.**

   ```bash
   az group list -o table
   az resource list -g rg-azb-lab -o table
   az resource list -g rg-azb-core -o table
   ```

   Write down every group name. Expect `rg-azb-core` and `rg-azb-lab`. You may also see `rg-azb-sandbox` and `rg-azb-tf`. A group you did not create stays: it can be one Azure made for Network Watcher (`NetworkWatcherRG`), or, if you chose a Cloud Shell storage account in Lab 2, a group with a name like `cloud-shell-storage-<region>`. `rg-azb-core` should hold only `ag-azb-email`.

2. **Remove locks.** A Delete lock on one resource blocks the delete of the whole resource group. Lab 17 made one lock, `lock-azb-nodelete`, in `rg-azb-sandbox`. This removes every lock it finds in the two groups. If a group does not exist, the command prints an error and you can ignore it.

   ```bash
   for L in $(az lock list --resource-group rg-azb-sandbox --query "[].id" -o tsv); do az lock delete --ids "$L"; done
   for L in $(az lock list --resource-group rg-azb-lab --query "[].id" -o tsv); do az lock delete --ids "$L"; done
   az lock list --resource-group rg-azb-sandbox -o table
   az lock list --resource-group rg-azb-lab -o table
   ```

   Check: the last two lists print nothing. A lock on a resource group or on the subscription is removed with `az lock delete --name LOCK_NAME --resource-group GROUP` or `az lock delete --name LOCK_NAME`. In the portal you can also open each resource group and storage account and select **Locks**.

3. **Remove policy assignments.** Lab 17 made two assignments on `rg-azb-sandbox`. This deletes every assignment at that scope:

   ```bash
   SANDBOX_ID=$(az group show --name rg-azb-sandbox --query id -o tsv)
   for A in $(az policy assignment list --resource-group rg-azb-sandbox --query "[].name" -o tsv); do az policy assignment delete --name "$A" --scope "$SANDBOX_ID"; done
   az policy assignment list --resource-group rg-azb-sandbox --query "[].name" -o tsv
   ```

   Check: the last command prints nothing. In the portal: **Policy** > **Assignments**, open the ellipsis of each assignment, then **Delete assignment**. If `rg-azb-sandbox` is already gone, there is nothing to do here.

4. **Check role assignments.** Lab 7 gave the group `TestUsers` Reader on the subscription and Contributor on `rg-azb-core`, and its clean up removes them. Check that nothing is left:

   ```bash
   GROUP_ID=$(az ad group show --group TestUsers --query id -o tsv)
   az role assignment list --assignee "$GROUP_ID" --all -o table
   ```

   If a role still shows, remove it: `az role assignment delete --assignee "$GROUP_ID" --role "Reader" --scope "/subscriptions/$SUB_ID"` for the subscription Reader, and the same with `--role "Contributor" --scope "/subscriptions/$SUB_ID/resourceGroups/rg-azb-core"` for the Contributor. Other assignments sit on resources you are about to delete and go with them: **Virtual Machine User Login** on `rg-azb-lab` (Lab 12), **Storage File Data SMB Share Contributor** on the share (Lab 14) and the Key Vault roles (Lab 15).

5. **Destroy the Terraform project.** If you did Lab 10 and did not destroy it yet, go to that project folder and run `terraform destroy`. Read the plan. Type `yes` only if every name starts with `rg-azb-tf`, `vnet-azb-tf`, `snet-azb-tf` or `nsg-azb-tf`. Then:

   ```bash
   az group exists --name rg-azb-tf
   ```

   Check: it prints `false`.

6. **Delete the sandbox group.** This is `rg-azb-sandbox` from Lab 17. Skip this step if it is already gone. Read the name, then run:

   ```bash
   az group delete --name rg-azb-sandbox --no-wait   # only rg-azb-sandbox
   ```

   The command asks you to confirm. Type `y` only after you read the name. `--no-wait` returns at once and the delete continues in Azure.

7. **Delete the lab group.** Look at what is inside first, so you know what goes:

   ```bash
   az resource list -g rg-azb-lab -o table
   ```

   You should see some or all of: the VM `vm-azb-win01`, its OS disk, its network interface and `pip-azb-win01`; `nsg-azb-vm` and `vnet-azb` with `snet-vm` and `snet-pe`; the storage account `stazb<digits>` with the share `azbshare`; the private endpoint `pe-azb-file` and the DNS zone `privatelink.file.core.windows.net`; the key vault `kv-azb-<digits>` unless Lab 15 already purged it; and `log-azb-lab`, `dcr-azb-lab` and the alert rule `VM not sending heartbeat` unless Lab 16 already removed them. Deleting the group removes all of them in one go.

   A deleted Log Analytics workspace keeps its name for 14 days and can be recovered. If you want to reuse the name `log-azb-lab`, delete it permanently first (this cannot be undone). Otherwise skip this command:

   ```bash
   az monitor log-analytics workspace delete --resource-group rg-azb-lab --workspace-name log-azb-lab --force true --yes
   ```

   Then delete the group:

   ```bash
   az group delete --name rg-azb-lab --no-wait   # only rg-azb-lab
   ```

   If the delete fails and the message mentions a lock, go back to step 2. Removing resources one by one in the portal also works (VM first, then its disk, network interface and public IP, then the rest, the virtual network last), but deleting the group is simpler.

8. **Wait for the deletes.** They take a few minutes. Run this until both print `false`. Do not go to step 9 before that:

   ```bash
   az group exists --name rg-azb-lab
   az group exists --name rg-azb-sandbox
   ```

9. **Purge the soft-deleted key vault.** Deleting the group soft-deleted the vault if Lab 15 had not purged it. Purging frees the name and removes it for good. First list what is there:

   ```bash
   az keyvault list-deleted --resource-type vault -o table
   ```

   If the list is empty, you purged it in Lab 15. Done. If it lists your vault, copy the name from the list and purge it. For example, if the list shows `kv-azb-48213`:

   ```bash
   az keyvault purge --name kv-azb-48213   # replace with the name from the list
   ```

   If the purge is refused, read the message. If purge protection is on, you cannot purge until the retention period ends. Lab 15 told you not to turn it on, so this should not happen. The vault then stays in the deleted list until its retention time ends.

10. **Check the Microsoft Entra leftovers.** These are not in any resource group, so deleting the groups does not remove them. Go to the [Microsoft Entra admin center](https://entra.microsoft.com) and check the tenant name. Then:
    1. **Conditional Access.** Browse to **Entra ID** > **Conditional Access** > **Policies**. You deleted the Conditional Access policy in Lab 6 Part 7. Check that no policy named like `CA-Lab6-AVD-RequireMFA-TestUsers` is still in the list. If it is, select it, select **Delete** and confirm. A policy left on can ask `testuser1` for MFA the next time you build an AVD lab, which looks like a sign-in fault you made yourself. Microsoft-managed policies that were there before you started stay.
    2. **Device.** Browse to **Entra ID** > **Devices** > **All devices**. If a device named `vm-azb-win01` is still there, delete it. A leftover device can make a later join with the same name fail.
    3. **Storage account app.** Browse to **Entra ID** > **App registrations** > **All applications** and search for `[Storage Account]`. Lab 14 turned on Microsoft Entra Kerberos for the account, and Azure created an app for it. The account is gone now. If an app named for it is still listed, open it and delete it.
    4. **Your PC and notes.** If you registered your PC in Lab 11 (route B): **Settings** > **Accounts** > **Access work or school**, select the account and select **Disconnect**. If you used route C in Lab 12: delete the `hosts` line that names `vm-azb-win01` (open Notepad as administrator, open `C:\Windows\System32\drivers\etc\hosts`, delete the line, save). It points at `pip-azb-win01`, which is gone now. Delete `test.rdp` from your PC.
    5. **Security defaults.** If security defaults were **Enabled** when you started Lab 6 (your note from Lab 6), turn them back on under **Entra ID** > **Overview** > **Properties** > **Manage security defaults**. They cannot be used together with Conditional Access, so do this only after the policy is gone.
    6. If you started a trial or bought a licence for Lab 6, end it where you got it. If you added the storage app to the excluded apps of an all-resources MFA policy in Lab 14, leave that policy as it is. The exclusion is harmless once the account is gone.

11. **Final check.**

    ```bash
    az group list -o table
    ```

    You expect `rg-azb-core` and any group you did not create. Set a reminder for tomorrow: open Cost analysis (see "Cost check the next day" below). If any line is not zero, open it by name.

### What to keep, and what to delete

Keep these. They cost nothing and the AVD labs use them:

- `rg-azb-core`, with `ag-azb-email`, and the budget `budget-azb-core` on the subscription. The budget warns you when the AVD labs start to spend.
- The test user `testuser1`, the group `TestUsers`, and their MFA registration from Lab 5.
- The emergency accounts `emergency-access-01` and `emergency-access-02`, and the group `EmergencyAccess`. Do not delete them while the tenant exists.
- The registered resource providers from Lab 1.
- Your Azure free account. It gives $200 of credit for 30 days, and the credit is a limit, not a plan to spend it.
- The Cloud Shell storage group, if you chose one in Lab 2 and still use Cloud Shell. Deleting it erases your `$HOME` files.

#### Only if you are finished with the whole series

These are separate and optional. Read each name twice before you run it.

- The budget and `rg-azb-core`. Deleting `rg-azb-core` does not delete the budget, because the budget is on the subscription, not in the group. Delete the budget separately: **Subscriptions** > your subscription > **Budgets** (it may sit under **Cost Management**) > `budget-azb-core` > **Delete**. Then delete the group, which holds only `ag-azb-email`:

  ```bash
  az group delete --name rg-azb-core   # only rg-azb-core, only when finished with the series
  ```

- The Terraform project folder from Lab 10, once you have copied what you want. Delete `terraform.tfstate` and `main.tfplan`, or keep the folder out of Git.
- `testuser1` and `TestUsers`, only if you will not build the AVD labs. They are easy to create again from [Lab 4](/azure-basics-labs/entra-users-groups-break-glass/).
- The whole test tenant. To remove the test tenant itself, follow Microsoft's [Delete a tenant in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/users/directory-delete-howto) page. Do that only for the test tenant, after reading its name. Learn says a Global Administrator must do it, and that the tenant must pass several checks first: no users except that one Global Administrator, no applications, and no subscription that still uses the tenant, so your Azure subscription has to be cancelled and deleted first.

### Cost check the next day

A delete in the middle of a day still shows some cost for that day. Cost data also arrives 8 to 24 hours late. So check tomorrow, then again the day after.

1. In the portal, open **Cost Management** and select **Cost analysis**. Set the scope to your subscription.
2. Set the date range to this month. Change the view to **Daily costs**.
3. Group by **Resource** (**View** > **Cost by resource**, or change **Group by**). Look at the last two days.
4. You expect some cost on the day you deleted things, and zero or close to zero the day after. If a resource still shows cost, open it by name. It is a leftover that the group delete did not cover, or a resource in a group you did not list in step 1.

Check: the day after the clean up shows 0.00 or a few cents for `rg-azb-core` items only, and no resource from Labs 8 to 18 appears in the list.

## Where this is used in AVD

Every AVD problem starts with the same question: which of the steps failed? The article [How Azure Virtual Desktop Fails](/azure-virtual-desktop/how-azure-virtual-desktop-fails/) sorts the failures by where they happen, and [Follow a Connection Step by Step](/azure-virtual-desktop/follow-a-connection-step-by-step/) walks the path a user takes so you know which log to open at each step. The logs in this lab are the ones you will open there.

## Next lab

There is no Lab 20. You have built the small parts: an account and a tenant, a resource group with a budget, people and roles, a network, a virtual machine, storage, a vault, logging, policy and a private endpoint. You have also deleted all of it. Next, build the real thing once, in code, so you can build it again and delete it again. [Quick AVD Lab with Terraform](/terraform-labs/avd-quick-lab/) builds a small Azure Virtual Desktop environment. It makes its own resource group, and you need a test user and a group for it: you kept `testuser1` and `TestUsers`. If you want the theory first, the AVD series starts at [What Is Azure Virtual Desktop](/azure-virtual-desktop/what-is-azure-virtual-desktop/). Keep the budget on, read the cost after every lab, and delete when you are done.

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
- [Delete a tenant in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/users/directory-delete-howto)
- [How to connect using Remote Desktop and sign on to an Azure virtual machine running Windows](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/connect-rdp)
- [Lock your Azure resources to protect your infrastructure](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources)
- [az lock](https://learn.microsoft.com/en-us/cli/azure/lock)
- [az group](https://learn.microsoft.com/en-us/cli/azure/group)
- [az policy assignment](https://learn.microsoft.com/en-us/cli/azure/policy/assignment)
- [Delete and recover a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/delete-workspace)
- [Azure Key Vault recovery management with soft delete and purge protection](https://learn.microsoft.com/en-us/azure/key-vault/general/key-vault-recovery)
- [Manage stale devices in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/devices/manage-stale-devices)
- [Quickstart: Start using Cost Analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/quick-acm-cost-analysis)
- [Customize views in Cost Analysis](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/customize-cost-analysis-views)
- [Identify anomalies and unexpected changes in cost](https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/analyze-unexpected-charges)
