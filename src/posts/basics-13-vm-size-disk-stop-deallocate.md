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

By the end of this lab you will have changed the size of the VM from Lab 12, changed the type of its OS disk, and seen the difference between a VM that is stopped and one that is deallocated. You will leave the VM deallocated, and you will know which parts of it still show up on the bill.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn. Where Learn does not give an exact menu name, I say what to look for.

## What you need

- [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the VM `vm-azb-win01` (size `Standard_B2s_v2`) in the resource group `rg-azb-lab`, with its public IP address `pip-azb-win01`.
- [Lab 3: Resource group, tags and budget](/azure-basics-labs/resource-group-tags-budget/): the budget that warns you about cost. Lab 3 is also where the 8 to 24 hour data delay in cost reports comes from.
- For the CLI part only: Cloud Shell or the Azure CLI from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Azure CLI 2.76 or newer.
- A role that can change the VM and its disk, for example Contributor on `rg-azb-lab` (see [Lab 7: RBAC roles](/azure-basics-labs/rbac-roles/)).
- Time: about 15 minutes for the steps. The cost report needs a second visit a day later.
- Cost: the VM and its disk bill while they exist. Only a few hours of VM time are used here. The disk keeps billing until you delete it in the cleanup of [Lab 19: When something breaks](/azure-basics-labs/when-something-breaks/).

## Safety first

- Use the throwaway tenant. Read the tenant and subscription name at the top of the portal before you change anything.
- Only touch the VM from Lab 12 and its own disk. Do not change anything in `rg-azb-core`.
- Resizing restarts a running VM, and a deallocate or restart ends any session on it. Nobody else uses this VM, so that is fine here. On a real VM it is a planned change.
- Pick a small size. Do not choose a size just because it looks fast. A bigger size costs more for every hour it runs.
- A budget only sends emails. It does not stop or deallocate anything. You have to do that yourself.

## What the lab builds

![A left-to-right diagram in the resource group rg-azb-lab. A Windows virtual machine moves through three power states: Running, Stopped (deallocated), and Running again after a start. Between the second and third state the size is changed and the OS disk type is changed. Under the VM, a managed OS disk and a public IP address stay in place while the VM is deallocated.](/img/basics/vm-size-disk-stop-deallocate.svg)

*Source: [States and billing status of Azure Virtual Machines](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing), [Change the size of a virtual machine](https://learn.microsoft.com/en-us/azure/virtual-machines/resize-vm), [Convert the disk type of an Azure managed disk](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-convert-types) and [FinOps best practices for compute](https://learn.microsoft.com/en-us/cloud-computing/finops/best-practices/compute). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: a VM size is a name you can read.**

A VM size sets how many virtual CPUs (vCPUs) and how much memory the VM gets. Learn groups sizes by purpose:

- **General purpose.** A balanced mix of CPU and memory. Learn lists testing and development, small to medium databases and low to medium traffic web servers as typical uses.
- **Compute optimized.** More CPU for each GiB of memory. For example medium traffic web servers and batch jobs.
- **Memory optimized.** More memory for each CPU. For example relational databases and in-memory caches.

Learn also describes the name. The first letter is the family: **B** is the burstable family and **D** is the general purpose family used for enterprise applications. Later letters and the `v5`-style ending give extra features and the version. Learn says a lowercase **s** in the name means the size supports Premium SSD disks, and gives `Standard_E4s_v3` against `Standard_E4_v3` as the example. The number in the name is the vCPU count. Read the name left to right. Take `Standard_B2s_v2`, the size from Lab 12. B is the family (burstable), 2 is the vCPU count, **s** means it works with any Premium SSD, and v2 is the version. Open the size page on Learn to see the exact numbers. B-series VMs only get full CPU speed when they have saved up CPU credits, and Learn says they are throttled back to a base level when the credits run out.

### Part 1: Look at the VM as it is now

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name at the top right.
2. Search for **Virtual machines** and open `vm-azb-win01` in `rg-azb-lab`.
3. On **Overview**, write down: **Size**, the status line (for example **Running**), and the **Public IP address**.
4. In the left menu open **Disks**. Write down the OS disk name and its **Storage type** (the column may be called **Disk type** or similar).
5. Open the public IP resource `pip-azb-win01` from the **Networking** page or the Overview link. Write down the address and whether the assignment is **Dynamic** or **Static**. Learn says Standard SKU public IPv4 addresses are always static, and that Basic ones can be either. The one from Lab 12 is Standard, so you should see **Static**.

**Idea 2: power states and what they cost.**

An Azure VM has two kinds of "off". Learn's states and billing page gives them like this:

| State | What it means | Compute billed? |
|---|---|---|
| Running | Fully up. | Yes |
| **Stopped** | Allocated on a host but not running. Learn says this is the result of the `PowerOff` operation **or of shutting down from inside the guest OS**. The portal can show it as *Stopped*. | **Yes** |
| **Stopped (deallocated)** | The VM has released its hold on the underlying hardware. | **No** |

Learn's FinOps page says the same thing in plain words. A stopped VM is powered off, but Azure still keeps the CPU and memory for it, so it keeps costing compute. A deallocated VM is stopped through the portal, CLI, PowerShell or another client tool, and Azure releases the compute, so there is no compute charge. It also says to avoid stopping VMs without deallocating them.

The states page adds one more line you should remember: for a deallocated VM, some resources such as **disks** and **networking** continue to incur charges.

So: shutting down inside Windows does not stop the compute bill. Use **Stop** in the portal (or `az vm deallocate`) and check that the status reads **Stopped (deallocated)**.

### Part 2: Deallocate the VM

6. On the VM **Overview**, select **Stop**. Wait until the status changes.
7. Read the status. It must say **Stopped (deallocated)**. If it only says **Stopped**, the compute is still billed. Select **Stop** again from the portal, not from inside Windows.
8. Look at the public IP address on the Overview again. Learn says deallocating releases any dynamic IP addresses assigned to the VM, and that the OS and data disks are not affected. Yours is static, so the address stays and still belongs to you, and it is still a billed resource.

Check: the status says **Stopped (deallocated)**.

### Part 3: Change the VM size

9. In the VM menu, under **Availability + scale**, select **Size**.
10. Pick `Standard_B2ls_v2`. It is in the same family as `Standard_B2s_v2`, with 2 vCPUs and 4 GiB of memory instead of 8, according to Learn's Bsv2-series page. If it is not offered, pick another small size with 2 vCPUs. Do not pick a large one. Learn says that if the VM is running and the size you want is missing, stopping it may show more sizes. Yours is already deallocated, so you see the full list for your region.
11. Select **Resize**.

Two limits from Learn that can stop you:

- **Quota.** Each subscription has a vCPU limit per region and a second limit per VM family, and a deployment cannot exceed either one. Learn says quota counts both allocated and deallocated cores, so a deallocated VM still uses its share. If a size shows **Insufficient quota - family limit** in the list, pick another size. Learn says you can use the **Request quota** link, but for a lab it is simpler to pick another size.
- **Temp disk.** For Windows VMs Learn only allows a resize from a size with a local temp disk to another size with a temp disk, and from a size without one to another without one. Learn says the Bsv2-series has no local temp storage, so a move between two Bsv2 sizes is fine. If a different size is refused, check this first.

Learn also says that if a resize fails, the portal can still show the size you asked for while the VM keeps its old size. After you start the VM, check the size again.

Check: on **Overview**, **Size** shows the new size.

### Part 4: Change the OS disk type

**Idea 3: the disk bills even when the VM does not.**

A managed disk is billed by its provisioned size and type, prorated by the hour, whether or not the VM is running (Learn's disk types page). Learn lists five managed disk types: Ultra Disk, Premium SSD v2, Premium SSD, Standard SSD and Standard HDD. Three of them can be used as an OS disk and can be switched between: **Premium SSD** (production workloads that need high performance), **Standard SSD** (web servers, lightly used applications, development and test) and **Standard HDD** (backup and other infrequent, non-critical use). Learn says Standard HDD as an OS disk is retiring on September 8, 2028, so do not choose it for the OS disk here. Premium SSD v2 and Ultra cannot be OS disks.

Learn's rules for switching:

- You can only change the disk type twice per day.
- To use Premium SSD, the VM size must support Premium storage (the **s** in the name).
- Learn's portal steps tell you to stop the VM first, and its CLI example deallocates the VM before the change. The page also says conversion needs a restart, and that the portal change itself is instant.

12. In the VM menu select **Disks**, then select the OS disk.
13. Select **Size + performance**.
14. Change **Account type** to the other type: from Premium SSD to **Standard SSD**, or from Standard SSD to **Premium SSD**. `Standard_B2ls_v2` has an **s** in its name, so both work. Learn lists Premium Storage as supported for the Bsv2-series. Select **Save**, then close the disk pane.

Check: the **Disks** page shows the new storage type for the OS disk.

### Part 5: Start the VM and check

15. On the VM **Overview**, select **Start**. Wait for **Running**.
16. Check three things: the **Size**, the OS disk type, and the **Public IP address** (it should be the same address as before).
17. If you want to, connect with the method from Lab 12 to confirm Windows still works. This is optional. You would need to add the RDP rule again as in Lab 12 and remove it afterwards.
18. When you are done, select **Stop** again. Check that the status says **Stopped (deallocated)**.

Check: the VM is **Stopped (deallocated)**.

### Part 6: See the cost by resource (do this a day later)

Cost reports are delayed. Learn says cost and usage data is typically available within 8 to 24 hours. Come back to this part the next day.

19. In the Azure portal search for **Cost Management + Billing**. Under **Cost Management** select **Cost analysis**.
20. Set the scope to your subscription or to `rg-azb-lab`.
21. Select the view **Cost by resource** (the page lists it among the views, and Learn says it is only available for subscription and resource group scopes). Change the view to **Table**.
22. Find the VM, its OS disk, and the public IP address. Look at the cost on the days the VM was deallocated. Compute should be missing, but the disk and the public IP address should still show up. Learn says a deallocated VM still pays for disks and networking.

One more sentence for later: Learn's FinOps page says commitment discounts (reservations and savings plans, for one or three years) can save up to 72 percent compared to list prices, and that Spot VMs use spare Azure capacity at a lower price but can be taken away when Azure needs the capacity back. Do not use either in this lab.

## Steps with the Azure CLI

Set variables first. This is the VM from Lab 12.

```bash
RG=rg-azb-lab
VM=vm-azb-win01
```

Look at the VM, its power state and its sizes.

```bash
az vm show --resource-group $RG --name $VM --show-details --query "{size:hardwareProfile.vmSize, power:powerState, ip:publicIps}" --output table
az vm list-vm-resize-options --resource-group $RG --name $VM --query "[].name" --output tsv
```

`--show-details` is the option that adds the public IP and the power state. The second command lists the sizes this VM can move to on its current hardware cluster. Learn says to check the list first.

Deallocate the VM and check it.

```bash
az vm deallocate --resource-group $RG --name $VM
az vm show --resource-group $RG --name $VM --show-details --query powerState --output tsv
```

The value should contain the word deallocated (for example `VM deallocated`).

Resize.

```bash
NEWSIZE=Standard_B2ls_v2     # must be in the list above; pick another name from it if not
az vm resize --resource-group $RG --name $VM --size $NEWSIZE
```

Change the OS disk type. Get the disk name from the VM, then update it.

```bash
DISK=$(az vm show --resource-group $RG --name $VM --query storageProfile.osDisk.name --output tsv)
az disk update --resource-group $RG --name $DISK --sku StandardSSD_LRS
```

Learn lists `Standard_LRS`, `StandardSSD_LRS` and `Premium_LRS` as the disk type names for HDD, Standard SSD and Premium SSD. Use `Premium_LRS` only if the VM size supports Premium storage.

Start, check, and deallocate again.

```bash
az vm start --resource-group $RG --name $VM
az vm show --resource-group $RG --name $VM --show-details --query "{size:hardwareProfile.vmSize, power:powerState, ip:publicIps}" --output table
az disk show --resource-group $RG --name $DISK --query sku.name --output tsv
az vm deallocate --resource-group $RG --name $VM
```

Check: the size is the new one, the disk SKU is the new one, and the last power state says deallocated.

## Terraform

No Terraform in this lab, because the VM from Lab 12 was not built with Terraform. If you changed its size or disk by hand and it were also in a Terraform state file, the next `terraform plan` would try to change it back, as Lab 10 showed. Learn says that in Terraform a resize is just a change to the `size` argument and a new `plan` and `apply`. Deallocating and starting are actions, not settings, so Terraform does not do them.

## Check that it works

- The VM shows the new size on **Overview** after you started it.
- The OS disk shows the new type on the **Disks** page.
- The VM ended **Stopped (deallocated)**, not only **Stopped**.
- The portal Overview or `az vm show --show-details` shows the power state you expect at each step.
- The next day, Cost analysis lists the VM, the OS disk and the public IP as separate lines.

## The most common mistake

Shutting down Windows from the Start menu (or `shutdown`) and thinking the bill stopped. Learn says a shutdown from inside the guest OS leaves the VM in the **Stopped** state, and that state is still billed for compute. Only a deallocate, from the portal or the CLI, releases the compute. Look at the status line: it must say **Stopped (deallocated)**.

Second most common: forgetting that the disk and the static public IP keep billing. A deallocated VM is cheap, not free. Delete the resources when you are done with the series.

## Clean up

- The VM must end this lab **Stopped (deallocated)**. Check the status once more.
- Do not delete anything yet. Keep the VM, its OS disk, its network interface, the public IP address `pip-azb-win01` and the NSG. Labs 14 to 18 use them.
- Delete everything in `rg-azb-lab` only in the cleanup of [Lab 19: When something breaks](/azure-basics-labs/when-something-breaks/). Deleting a resource group deletes all resources in it and cannot be undone. Lab 16 does not delete the group.

Keep for later labs:

- `rg-azb-lab` with the VM `vm-azb-win01` (now `Standard_B2ls_v2`, deallocated), `pip-azb-win01`, `vnet-azb` and `nsg-azb-vm`.
- `rg-azb-core` with the budget from Lab 3.

## Where this is used in AVD

AVD session hosts are VMs, so size, disk type and deallocate rules decide most of an AVD bill. The size choices are covered in [Choose Session Host VM Sizes](/azure-virtual-desktop/choose-session-host-vm-sizes/). Turning hosts off when nobody uses them is shown with real Terraform in [AVD Autoscale Cost Lab](/terraform-labs/avd-autoscale-cost-lab/).

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
