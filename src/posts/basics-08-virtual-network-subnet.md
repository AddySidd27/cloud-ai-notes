---
title: "Virtual Network and Subnet"
seoTitle: "Azure Virtual Network and Subnet for Beginners: CIDR Lab"
layout: post.njk
permalink: "/azure-basics-labs/virtual-network-subnet/"
order: 318
tags: [azure-basics-lab]
deck: "Create the virtual network vnet-azb and the subnet snet-vm in a new resource group, and learn to read an address range like 10.10.1.0/24."
description: "Create an Azure virtual network (10.10.0.0/16) and a subnet (10.10.1.0/24) with the portal, Azure CLI or Terraform, and learn CIDR, private ranges and overlap."
---

By the end you will have a resource group called `rg-azb-lab`, a virtual network called `vnet-azb` with the address range `10.10.0.0/16`, and one subnet called `snet-vm` with the range `10.10.1.0/24`. You will also be able to read those numbers and know how many addresses they hold.

## What you need

- An Azure subscription from [the free account lab](/azure-basics-labs/start-azure-account-tenant-subscription/). The Azure free account gives $200 of credit for 30 days.
- For the CLI part only: Cloud Shell or the Azure CLI from [the Cloud Shell lab](/azure-basics-labs/cloud-shell-and-azure-cli/). Azure CLI 2.76 or newer.
- A role that can create resources in the subscription. Owner or Contributor on a test subscription works. (The Network Contributor role also covers subnet tasks.)
- One Azure region. Use the region on your notes sheet from [the free account lab](/azure-basics-labs/start-azure-account-tenant-subscription/), and keep using it for every later lab. If `rg-azb-core` from [the resource group lab](/azure-basics-labs/resource-group-tags-budget/) is in a different region, that is fine. Only this network and the VM in the Windows VM lab must match.
- About 30 minutes. There is no charge for using Azure Virtual Network. It is free. Standard charges apply for resources you put in it, such as VMs. This lab creates none.

## Safety first

- Use a test tenant, not your employer's. Read the tenant and subscription name at the top of the portal before you change anything.
- Use ONE region for every lab in this series: the region on your notes sheet from [the free account lab](/azure-basics-labs/start-azure-account-tenant-subscription/). You will need it again for the virtual machine.
- Do not copy address ranges from a real company network. In this lab you invent a range, and nothing here connects to anything.
- You create no virtual machine and no public IP address, so nothing here can be reached from the internet and nothing costs money.
- Azure already requires multifactor authentication (MFA) for Azure management work. If you are asked for it, that is expected.

## What the lab builds

![Nested boxes in resource group rg-azb-lab: the virtual network vnet-azb, 10.10.0.0/16 with 65,536 addresses, contains the subnet snet-vm, 10.10.1.0/24 with 251 usable addresses. A VM comes in a later lab and gets 10.10.1.4.](/img/basics/virtual-network-subnet.svg)

*Source: Microsoft Learn pages listed under Sources.*

## Steps in the Azure portal

### Read the numbers first

A virtual network is your own private network inside Azure. Resources such as virtual machines (VMs) connect to it and talk to each other over private addresses. A virtual network lives in exactly one region. Any Azure resource you connect to it must be in the same region, so the VM you create in a later lab has to be in the region you pick now.

You give the network a block of addresses. The block is written in CIDR notation (Classless Inter-Domain Routing). It looks like `10.10.0.0/16`. Read it in two parts:

- `10.10.0.0` is where the block starts.
- `/16` says how big the block is. The smaller the number after the slash, the bigger the block.

| Block size | Addresses |
|---|---|
| `/16` | 65,536 |
| `/24` | 256 |
| `/27` | 32 |

So `10.10.0.0/16` is every address from `10.10.0.0` to `10.10.255.255`, and `10.10.1.0/24` is every address from `10.10.1.0` to `10.10.1.255`. The subnet is a slice of the network, and its range must sit inside the network's range.

Two more facts you need for the first step:

- **Use private ranges.** Use `10.x.x.x`, `172.16` to `172.31.x.x` or `192.168.x.x`. Use the ranges set aside for private networks. `10.10.0.0/16` is inside the first one.
- **Azure keeps five addresses in every subnet.** Azure reserves the first four addresses and the last one. That leaves 251 you can use in a `/24`. The first address a VM gets is `10.10.1.4`.

Check yourself: how many addresses does `10.10.5.0/27` hold? Answer: 32. Which is bigger, `/20` or `/26`? Answer: `/20`.

### The resource group

This lab puts its resources in a new resource group, `rg-azb-lab`. Later labs add the VM, storage and other things to the same group.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the subscription name.
2. Search for and open **Resource groups**, then select **Create**.
3. Set **Resource group** to `rg-azb-lab` and **Region** to your chosen region.
4. Select **Review + Create**, then **Create**.

Check: `rg-azb-lab` is in the list of resource groups.

### The virtual network and the subnet

5. In the search box at the top of the portal, enter **Virtual networks** and select it in the results. Select **+ Create**.
6. On the **Basics** tab, set **Subscription** to your test subscription, **Resource group** to `rg-azb-lab`, **Name** to `vnet-azb`, and **Region** to the region you chose. You cannot change the name of a virtual network after you create it, so check it now.
7. Select **Next** to go to the **Security** tab, and leave it as it is. Select **Next** to go to the **IP addresses** tab.
8. On the **IP addresses** tab you see an offered address space (often `10.0.0.0/16`) and a subnet named **default**. Select the existing address space and change it to `10.10.0.0/16`. If your portal shows a different layout and you cannot change it, select **Cancel**, use the CLI steps below in Cloud Shell, then open `vnet-azb` in the portal and continue at step 13.
9. Under **Subnets**, select the existing **default** subnet. In **Edit subnet**, leave **Subnet template** as **Default**, set **Name** to `snet-vm`, **Starting address** to `10.10.1.0` and **Subnet size** to `/24 (256 addresses)`. Select **Save**. If the subnet still shows an address from the old range, check step 8 again.
10. Leave the other subnet settings as they are. If you see a setting named **Private subnet** or **Default outbound access**, leave it as offered. The portal already makes new subnets private. A VM in a private subnet has no automatic internet access. It needs an explicit outbound method, such as the public IP address that the Windows VM lab adds.
11. Select **Review + create**. When validation passes, select **Create**.

12. When the deployment finishes, select **Go to resource**.
13. On the virtual network page, open **Overview** and look at the address space and **DNS servers**. A virtual network created in the portal uses Azure's DNS servers by default. To see the setting, select **DNS servers** under **Settings**. It should read **Default (Azure-provided)**. Do not change it. With this option, resources in the same virtual network can find each other by name.
14. Select **Subnets** and open `snet-vm`. Note the address range. Read the **Default outbound access** setting and write down what it says. Do not change it. A private subnet shows **Disabled** there.

Check: under **Subnets**, `snet-vm` shows `10.10.1.0/24`, and **Address space** shows `10.10.0.0/16`.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from the Cloud Shell lab. Do either the portal steps or the CLI steps, not both. If you did the portal steps, skip to the Check. Check the subscription, then set the variables. Use your own region.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
LOCATION=eastus2     # use the region you chose
RG=rg-azb-lab
VNET=vnet-azb
SUBNET=snet-vm
```

Create the resource group.

```bash
az group create --name $RG --location $LOCATION
```

Create the virtual network and the first subnet in one command. `--address-prefixes` is the whole network. `--subnet-prefixes` is the range of the first subnet. The `az network vnet create` reference shows this pattern.

```bash
az network vnet create \
  --name $VNET \
  --resource-group $RG \
  --location $LOCATION \
  --address-prefixes 10.10.0.0/16 \
  --subnet-name $SUBNET \
  --subnet-prefixes 10.10.1.0/24
```

Check: this lists the network and the subnet.

```bash
az network vnet show --name $VNET --resource-group $RG --query "{name:name, location:location, space:addressSpace.addressPrefixes}" -o json
az network vnet subnet list --vnet-name $VNET --resource-group $RG --query "[].{name:name, prefix:addressPrefix, prefixes:addressPrefixes}" -o json
```

You should see `10.10.0.0/16` for the network and `snet-vm` with `10.10.1.0/24`. The subnet range shows under `prefix` or under `prefixes`, depending on the CLI version. One of the two can be `null`.

The CLI may follow the older outbound default, depending on the CLI version: only the API version released after March 31, 2026 makes subnets in new virtual networks private by default. After the command, open `snet-vm` in the portal and read **Default outbound access**. The setting `--default-outbound false` on `az network vnet subnet update` makes an existing subnet private. Do not run it in this lab.

## Terraform

No Terraform in this lab, because Terraform is taught in [Terraform basics](/azure-basics-labs/terraform-basics/). At the end of that lab, "Try it yourself" has a block that builds this network in code, with the same address ideas.

## Check that it works

- `rg-azb-lab` exists in your chosen region.
- `vnet-azb` is in `rg-azb-lab`, in the same region, with the address space `10.10.0.0/16`.
- `snet-vm` is in `vnet-azb` with the range `10.10.1.0/24`.
- **DNS servers** on the virtual network reads **Default (Azure-provided)**.
- Open `vnet-azb` and select **Connected devices** in the left menu. It should be empty. Nothing is attached yet. That is expected.
- Why 251? Azure reserves the first four addresses and the last one in the subnet. The first VM gets `10.10.1.4`.

## The most common mistake

Choosing an address range without checking the other networks you may join later. Three things to know:

- A validation error that says the subnet is outside the address space means you changed the network range but not the **default** subnet. Edit the subnet (step 9).
- You can connect virtual networks to each other and to on-premises networks only if their ranges do not overlap. Two ranges overlap if any part of them is the same. For example, `10.0.0.0/16` and `10.0.1.0/24` overlap, because the second sits inside the first. Azure refuses to peer (link) two virtual networks that overlap. The portal and many tutorials offer `10.0.0.0/16`, so that range is easy to clash with. This lab uses `10.10.0.0/16` instead. In a real company, ask whoever manages the network which ranges are taken before you pick one.
- Changing a subnet later is not always possible. You can change a subnet's address range only if no resources are deployed in it. If any exist, you must first move them to another subnet or delete them. You can delete a subnet only when it is empty. Also, once a VM exists you can change its subnet, but not its virtual network.

You can add or resize the address space of a virtual network later. You can shrink a range only while it still covers the subnets inside it, and that a range holding a subnet cannot be removed. If the network is peered, the peering has to be synced after the change. It is still cheaper to choose well the first time.

## Clean up

Keep everything. The virtual network is free, and the next labs need it.

**Keep these for the later labs:**

- `rg-azb-lab`
- `vnet-azb`
- `snet-vm`

`rg-azb-lab` is the group for the network, VM, storage, vault and workspace labs that follow. To remove everything at the very end of the series, delete the resource group `rg-azb-lab`. That deletes everything inside it, so do it only when you have finished with the later labs.

```bash
az group delete --name rg-azb-lab
```

`rg-azb-core` from the resource group lab is not touched by this lab.

## Where this is used in AVD

Azure Virtual Desktop session hosts are VMs, and they sit in a subnet of a virtual network just like the one you made. The size of that subnet, the DNS it uses and how it reaches the internet are decided before you build. A `/24` holds about 251 session hosts, and a subnet that is too small blocks adding hosts later. See [Plan Azure Virtual Desktop networking](/azure-virtual-desktop/plan-avd-networking/) and [Network topology and IP planning for AVD](/azure-virtual-desktop/network-topology-and-ip-planning-for-avd/).

## Next lab

[Network security group](/azure-basics-labs/network-security-group/) adds a set of allow and deny rules and attaches it to `snet-vm`, so you control what can reach the subnet.

## Sources

- [Quickstart: Create a virtual network](https://learn.microsoft.com/en-us/azure/virtual-network/quickstart-create-virtual-network)
- [Add, change, or delete a virtual network subnet](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-subnet)
- [Default outbound access in Azure](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/default-outbound-access)
