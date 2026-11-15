---
title: "VM Size, Disk Type and Power States: Stop, Deallocate and What You Pay"
seoTitle: "Azure VM Size, Disk Type and Deallocate: Beginner Lab"
layout: post.njk
permalink: "/azure-basics-labs/vm-size-disk-stop-deallocate/"
order: 323
tags: [azure-basics-lab]
deck: "You resize your lab VM, change its OS disk type, deallocate it, and see which parts of a VM still cost money when it is off."
description: "Beginner Azure lab: read VM size names, resize a VM, change the OS disk type, tell Stopped from Deallocated, and check what a VM costs when it is off."
---

By the end of this lab you will have started the VM from Lab 12, changed its size, changed the type of its OS disk, and seen the difference between a VM that is stopped and one that is deallocated. You will leave the VM deallocated, and you will know which parts of it still show up on the bill.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn. Where Learn does not give an exact menu name, I say what to look for.

## What you need

- [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the VM `vm-azb-win01` (size `Standard_B2s_v2`) in the resource group `rg-azb-lab`, with its public IP address `pip-azb-win01`.
- The state Lab 12 left: the VM is **Stopped (deallocated)** and there is no RDP rule. This lab starts with one extra step: you start the VM. You do not connect to it with RDP, so you do not add any rule.
- [Lab 3: Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): the budget that warns you about cost. Budgets only warn.
- For the CLI part only: Cloud Shell or the Azure CLI from [Lab 2: Azure Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/). Azure CLI 2.76 or newer.
- A role that can change the VM and its disk, for example Contributor on `rg-azb-lab` (see [Lab 7: Azure RBAC roles](/azure-basics-labs/rbac-roles/)).
- Time: about 20 minutes for the steps, plus an optional 5 minute check the next day.
- Billing right now: the disk and the public IP bill all the time. The VM bills while it runs. New in this lab: nothing new. You use the VM for about an hour.

State at the start: VM Stopped (deallocated), no RDP rule. At the end: VM Stopped (deallocated) again, size `Standard_B2ls_v2`, no RDP rule.

## Safety first

- Use the throwaway tenant. Read the tenant and subscription name at the top of the portal before you change anything.
- Only touch the VM from Lab 12 and its own disk. Do not change anything in `rg-azb-core`.
- Resizing restarts a running VM, and a deallocate or restart ends any session on it. Nobody else uses this VM, so that is fine here.
- Pick a small size. A bigger size costs more for every hour it runs.
- A budget only sends emails. It does not stop or deallocate anything. You have to do that yourself.
- Never shut the VM down from inside Windows to save money. Use **Stop** in the portal and read the status.

## What the lab builds

![The VM vm-azb-win01 in the resource group rg-azb-lab moves through numbered steps. It starts Running as Standard_B2s_v2. Step 1, Stop, makes it Stopped (deallocated), where compute is not billed. While it is deallocated, step 2 changes the size and step 3 changes the OS disk type. Step 4, Start, makes it Running again as Standard_B2ls_v2. A red box shows that shutting down inside Windows leaves the VM only Stopped, and compute is still billed. A group at the bottom shows that the OS disk and the static public IP pip-azb-win01 are billed in every state.](/img/basics/vm-size-disk-stop-deallocate.svg)

*Source: [States and billing status of Azure Virtual Machines](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing), [Change the size of a virtual machine](https://learn.microsoft.com/en-us/azure/virtual-machines/resize-vm), [Convert the disk type of an Azure managed disk](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-convert-types) and [FinOps best practices for compute](https://learn.microsoft.com/en-us/cloud-computing/finops/best-practices/compute). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Background: a VM size is a name you can read.** A size sets the number of virtual CPUs (vCPUs) and the memory, and so the price per hour. Take `Standard_B2s_v2`: B is the family (burstable, cheap, for light use), 2 is the vCPU count, v2 is the version. A bigger size costs more every hour it runs. Open the size page on Learn if you want the exact numbers.

### Part 1: Start the VM and look at it

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name at the top right.
2. Search for **Virtual machines** and open `vm-azb-win01` in `rg-azb-lab`.
3. The status is **Stopped (deallocated)** from Lab 12. Select **Start** and wait until **Overview** says **Running** (2 to 3 minutes). You need a running VM to see all the states.
4. On **Overview**, write down: **Size**, the status, and the **Public IP address**.
5. In the left menu open **Disks**. Write down the OS disk name and its **Storage type** (the column may be called **Disk type**).
6. Open the public IP resource `pip-azb-win01` from **Networking** or the Overview link. Write down the address and whether the assignment is **Dynamic** or **Static**. A Standard public IPv4 address is always static, so you should see **Static**.

Check: the status says **Running**, and you have the size, the disk type and the address in your notes.

**Background: power states and what they cost.** An Azure VM has two kinds of "off". Learn's states and billing page gives them like this:

| State | What it means | Compute billed? |
|---|---|---|
| Running | Fully up. | Yes |
| **Stopped** | Allocated on a host but not running. This is the result of the `PowerOff` operation **or of shutting down from inside Windows**. | **Yes** |
| **Stopped (deallocated)** | The VM has released its hold on the underlying hardware. | **No** |

A stopped VM is powered off, but Azure still keeps the CPU and memory for it. A deallocated VM is stopped through the portal, CLI or PowerShell, and Azure releases the compute. For a deallocated VM, some resources such as **disks** and **networking** continue to incur charges.

So: shutting down inside Windows does not stop the compute bill. Use **Stop** in the portal (or `az vm deallocate`) and check that the status reads **Stopped (deallocated)**.

### Part 2: Deallocate the VM

**Optional: see the billed state (5 minutes).** While the VM is **Running**, open **Operations** > **Run command** > **RunPowerShellScript**, type `shutdown /s /t 5` and select **Run**. The command may show an error or time out, because the VM shuts down while it runs. Ignore that. Wait two minutes and refresh the Overview. The status reads **Stopped**, not **Stopped (deallocated)**. That is the billed state. Go on to step 7.

7. On the VM **Overview**, select **Stop**. Wait until the status changes.
8. Read the status. It must say **Stopped (deallocated)**. If it only says **Stopped**, compute is still billed. Select **Stop** again from the portal.
9. Look at the public IP address on the Overview again. Deallocating releases dynamic addresses and leaves the disks alone. Yours is static, so the address stays and still belongs to you, and it is still a billed resource.

Check: the status says **Stopped (deallocated)**.

### Part 3: Change the VM size

10. In the VM menu, under **Availability + scale**, select **Size**.
11. Pick `Standard_B2ls_v2`: 2 vCPUs and 4 GiB of memory, half the memory of the old size. Use the search box in the size list. If it is not offered, pick another size with 2 vCPUs. Do not pick a large one.
12. Select **Resize**.

If a size says **Insufficient quota** or the resize is refused, pick another size with 2 vCPUs. Do not request more quota. If a resize fails, the portal can still show the size you asked for while the VM keeps its old size, so check the size again after you start the VM.

The VM now has 4 GiB of memory. Windows Server may feel slower. That is fine for the next labs. To go back, repeat this part with `Standard_B2s_v2`.

Check: on **Overview**, **Size** shows `Standard_B2ls_v2`.

### Part 4: Change the OS disk type

**Background: the disk bills even when the VM does not.** A managed disk is billed by its size and type, by the hour, whether or not the VM is running. Premium SSD is the fastest and costs the most. Standard SSD is cheaper. Do not choose Standard HDD for an OS disk. Premium SSD needs a VM size with Premium storage support. Learn lists Premium storage as supported for the Bsv2-series.

13. In the VM menu select **Disks**, then select the OS disk.
14. Select **Size + performance**.
15. Lab 12 created the disk with the portal default. Change **Account type** to **Standard SSD** (cheaper). If it already says Standard SSD, change it to **Premium SSD**. Select **Save**, then close the disk pane.

Check: the **Disks** page shows the new storage type for the OS disk.

### Part 5: Start the VM and check

16. On the VM **Overview**, select **Start**. Wait for **Running**.
17. Check three things: the **Size**, the OS disk type, and the **Public IP address** (it should be the same address as before).
18. Optional: under **Operations** > **Run command** > **RunPowerShellScript**, run `hostname`. The output `vm-azb-win01` proves Windows booted after the resize. No RDP is needed.
19. Select **Stop** again. Check that the status says **Stopped (deallocated)**.

Check: the VM is **Stopped (deallocated)**.

## Steps with the Azure CLI

If Cloud Shell was closed or timed out, run the variables again before the Clean up commands. Variables first. This is the VM from Lab 12.

```bash
RG=rg-azb-lab
VM=vm-azb-win01
```

Start the VM and look at it.

```bash
az vm start --resource-group $RG --name $VM
az vm show --resource-group $RG --name $VM --show-details --query "{size:hardwareProfile.vmSize, power:powerState, ip:publicIps}" --output table
```

`--show-details` adds the public IP and the power state. The power state should contain `running`.

Deallocate the VM and check it.

```bash
az vm deallocate --resource-group $RG --name $VM
az vm show --resource-group $RG --name $VM --show-details --query powerState --output tsv
```

The value should contain the word deallocated (for example `VM deallocated`).

List the sizes the VM can move to. Run this after the VM is deallocated, because more sizes are allowed then. Then resize.

```bash
az vm list-vm-resize-options --resource-group $RG --name $VM --query "[].name" --output tsv
NEWSIZE=Standard_B2ls_v2     # must be in the list above; pick another name from it if not
az vm resize --resource-group $RG --name $VM --size $NEWSIZE
```

Change the OS disk type. Get the disk name from the VM, then update it.

```bash
DISK=$(az vm show --resource-group $RG --name $VM --query storageProfile.osDisk.name --output tsv)
az disk update --resource-group $RG --name $DISK --sku StandardSSD_LRS
```

`Standard_LRS`, `StandardSSD_LRS` and `Premium_LRS` are the names for HDD, Standard SSD and Premium SSD. If the disk is already Standard SSD, use `Premium_LRS` instead.

Start, check, and deallocate again.

```bash
az vm start --resource-group $RG --name $VM
az vm show --resource-group $RG --name $VM --show-details --query "{size:hardwareProfile.vmSize, power:powerState, ip:publicIps}" --output table
az disk show --resource-group $RG --name $DISK --query sku.name --output tsv
az vm deallocate --resource-group $RG --name $VM
```

Check: the size is the new one, the disk SKU is the new one, and the last power state says deallocated.

## Terraform

No Terraform in this lab. The VM was created by hand in Lab 12.

## Check that it works

- The VM showed the new size on **Overview** after you started it.
- The OS disk shows the new type on the **Disks** page.
- The VM ended **Stopped (deallocated)**, not only **Stopped**.

## The most common mistake

Shutting down Windows from the Start menu (or `shutdown`) and thinking the bill stopped. A shutdown from inside the guest OS leaves the VM in the **Stopped** state, and that state is still billed for compute. Only a deallocate, from the portal or the CLI, releases the compute. Look at the status line: it must say **Stopped (deallocated)**.

Second most common: forgetting that the disk and the static public IP keep billing. A deallocated VM is cheap, not free.

## Clean up

- The VM must end this lab **Stopped (deallocated)**. Check the status once more.
- No RDP rule was added in this lab, so there is nothing to remove.
- Do not delete anything yet. Keep the VM, its OS disk, its network interface, `pip-azb-win01` and the NSG. Labs 14 to 18 use them.
- Pausing the series for more than a week? A deallocated VM still bills for its disk and the static public IP. Delete the VM and the public IP with "Delete the VM and the public IP" in the Clean up of [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/), and rebuild the VM with Lab 12 when you come back. Keep `vnet-azb` and `nsg-azb-vm`. If you want to remove the whole lab group instead, Lab 19 shows how. Deleting a resource group deletes everything in it and cannot be undone.

Keep for later labs:

- `rg-azb-lab` with the VM `vm-azb-win01` (now `Standard_B2ls_v2`, Stopped (deallocated)), `pip-azb-win01`, `vnet-azb` and `nsg-azb-vm`, with no RDP rule.
- `rg-azb-core` with the action group `ag-azb-email`, and the budget `budget-azb-core` on the subscription (Lab 3).

Hand-off to Lab 14: the VM is Stopped (deallocated) and there is no RDP rule. Lab 14 starts by following "Connect again later" in [Lab 12](/azure-basics-labs/windows-vm-entra-sign-in/): start the VM, add the rule, connect.

### Optional next-day check: cost by resource (5 minutes)

Cost data can take many hours to appear, so set a reminder for tomorrow. [Lab 19](/azure-basics-labs/when-something-breaks/) also checks cost.

1. In the Azure portal search for **Cost Management + Billing**. Under **Cost Management** select **Cost analysis**.
2. Set the scope to your subscription or to `rg-azb-lab`.
3. Select the view **Cost by resource** (it is only available for subscription and resource group scopes). Change the view to **Table**.
4. Success: you see rows for `vm-azb-win01`, its OS disk and `pip-azb-win01`. On days the VM was deallocated, the VM row is missing or near 0. The disk and IP rows are not.

## Where this is used in AVD

AVD session hosts are VMs, so size, disk type and deallocate rules decide most of an AVD bill. A host pool left running overnight costs the same as a host pool in use. That is why Autoscale exists. The size choices are covered in [Choose Session Host VM Sizes](/azure-virtual-desktop/choose-session-host-vm-sizes/). Turning hosts off when nobody uses them is shown with real Terraform in [AVD Autoscale Cost Lab](/terraform-labs/avd-autoscale-cost-lab/).

## Next lab

[Lab 14: Storage and Azure Files](/azure-basics-labs/storage-azure-files/) adds a storage account and a file share, the same kind of storage AVD uses for user profiles.

## Sources

- [States and billing status of Azure Virtual Machines](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing)
- [FinOps best practices for compute](https://learn.microsoft.com/en-us/cloud-computing/finops/best-practices/compute)
- [Sizes for virtual machines in Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview)
- [B family general purpose VM size series](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/b-family)
- [Change the size of a virtual machine](https://learn.microsoft.com/en-us/azure/virtual-machines/resize-vm)
- [Check vCPU quotas](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas)
- [Increase VM-family vCPU quotas](https://learn.microsoft.com/en-us/azure/quotas/per-vm-quota-requests)
- [Azure managed disk types](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types)
- [Convert the disk type of an Azure managed disk](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-convert-types)
- [Public IP addresses](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/public-ip-addresses)
- [Common cost analysis uses](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-analysis-common-uses)
- [Monitor costs for virtual machines](https://learn.microsoft.com/en-us/azure/virtual-machines/cost-optimization-monitor-costs)
- [az vm show](https://learn.microsoft.com/en-us/cli/azure/vm#az-vm-show) and [az vm resize](https://learn.microsoft.com/en-us/cli/azure/vm#az-vm-resize)
