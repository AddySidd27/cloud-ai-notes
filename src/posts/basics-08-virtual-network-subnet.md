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

I have not run these steps in a live tenant for this article, and I have not run `terraform validate` on the Terraform block. The steps follow Microsoft Learn (Microsoft's documentation site).

## What you need

- An Azure subscription from [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/). The Azure free account gives $200 of credit for 30 days.
- For the CLI part only: Cloud Shell or the Azure CLI from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Azure CLI 2.76 or newer.
- A role that can create resources in the subscription. Learn says the Network contributor role (or a custom role with the right actions) is what you need for subnet tasks. Owner or Contributor on a test subscription also works.
- One Azure region. Use the region you used for `rg-azb-core` in [Lab 3: Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/), and keep using it for every later lab.
- About 30 minutes. Learn says there is no charge for using Azure Virtual Network. It is free. Standard charges apply for resources you put in it, such as VMs. This lab creates none.

## Safety first

- Use a test tenant, not your employer's. Read the tenant and subscription name at the top of the portal before you change anything.
- Pick ONE region and use it for every lab in this series. Write it down. You will need it again for the virtual machine.
- Do not copy address ranges from a real company network. In this lab you invent a range, and nothing here connects to anything.
- You create no virtual machine and no public IP address, so nothing here can be reached from the internet and nothing costs money.
- Azure already requires multifactor authentication (MFA) for Azure management work. If you are asked for it, that is expected.

## What the lab builds

![Inside one resource group named rg-azb-lab sits a virtual network named vnet-azb with the address space 10.10.0.0/16. Inside the virtual network sits one subnet named snet-vm with the range 10.10.1.0/24.](/img/basics/virtual-network-subnet.svg)

*Source: Learn pages [Quickstart: Create a virtual network](https://learn.microsoft.com/en-us/azure/virtual-network/quickstart-create-virtual-network), [Create, change, or delete a virtual network](https://learn.microsoft.com/en-us/azure/virtual-network/manage-virtual-network) and [Add, change, or delete a virtual network subnet](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-subnet). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Part 1: Read the numbers first

A virtual network is your own private network inside Azure. Resources such as virtual machines (VMs) connect to it and talk to each other over private addresses. A virtual network lives in exactly one region. Learn says any Azure resource you connect to it must be in the same region, so the VM you create in a later lab has to be in the region you pick now.

You give the network a block of addresses. The block is written in CIDR notation (Classless Inter-Domain Routing). It looks like `10.10.0.0/16`. Read it in two parts:

- `10.10.0.0` is where the block starts.
- `/16` says how many of the 32 bits in an IPv4 address are fixed. The smaller the number after the slash, the bigger the block. A `/16` holds 65,536 addresses. A `/24` holds 256. Each step of 1 in the number halves or doubles the size.

So `10.10.0.0/16` is every address from `10.10.0.0` to `10.10.255.255`, and `10.10.1.0/24` is every address from `10.10.1.0` to `10.10.1.255`. The subnet is a slice of the network, and its range must sit inside the network's range.

Two more facts from Learn that you need for the first step:

- **Use private ranges.** Learn recommends the ranges set aside for private networks in RFC 1918: `10.0.0.0/8`, `172.16.0.0/12` and `192.168.0.0/16`. Azure also accepts `100.64.0.0/10`. The range `10.10.0.0/16` is inside the first one. Learn also lists ranges you cannot add, for example `127.0.0.0/8` (loopback) and `169.254.0.0/16` (link local).
- **Azure keeps five addresses in every subnet.** Learn says Azure reserves the first four addresses and the last one. In `10.10.1.0/24` that is `10.10.1.0` (network address), `10.10.1.1` (default gateway), `10.10.1.2` and `10.10.1.3` (Azure DNS), and `10.10.1.255` (broadcast). That leaves 251 usable addresses. The first free one, and so the first one a VM can get, is `10.10.1.4`.

### Part 2: The resource group

This lab puts its resources in a new resource group, `rg-azb-lab`. Later labs add the VM, storage and other things to the same group.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the subscription name.
2. Search for and open **Resource groups**, then select **Create**.
3. Set **Resource group** to `rg-azb-lab` and **Region** to your chosen region.
4. Select **Review + Create**, then **Create**.

Check: `rg-azb-lab` is in the list of resource groups.

### Part 3: The virtual network and the subnet

5. In the search box at the top of the portal, enter **Virtual networks** and select it in the results. Select **+ Create**.
6. On the **Basics** tab, set **Subscription** to your test subscription, **Resource group** to `rg-azb-lab`, **Name** to `vnet-azb`, and **Region** to the region you chose. Learn says you cannot change the name of a virtual network after you create it, so check it now.
7. Select **Next** to go to the **Security** tab, and leave it as it is. Select **Next** to go to the **IP addresses** tab.
8. Find the address space on this tab. Learn's quickstart keeps the offered `10.0.0.0` range, so its steps do not show how to change it. Look for the box that holds the existing address range, and change it to `10.10.0.0/16`. If you cannot edit it in place, delete the offered range and add yours.
9. Under **Subnets**, select the existing **default** subnet. In **Edit subnet**, leave **Subnet template** as **Default**, set **Name** to `snet-vm`, **Starting address** to `10.10.1.0` and **Subnet size** to `/24 (256 addresses)`. Select **Save**. If the subnet still shows an address from the old range, check step 8 again.
10. Look at the other settings on the subnet page. If you see a setting about private subnets or default outbound access, read the next section before you change it. Leaving it as offered is fine for this lab.
11. Select **Review + create**. When validation passes, select **Create**.

Learn says the Azure portal defaults to private subnets. Here is what that means. A subnet is "private" when Azure does not give its VMs the automatic outbound internet access described below. For now, leave the portal's default alone.

**Default outbound access, in plain words.** If a VM has no explicit way to reach the internet (a NAT gateway, a public IP on the VM, or a load balancer with outbound rules), Azure can give it an outbound public IP address automatically. Learn calls this default outbound access. That address belongs to Microsoft and can change without notice. Learn also says that for the API version released after March 31, 2026, subnets in new virtual networks are private by default, and a VM in a private subnet needs an explicit outbound method to reach the internet. Examples Learn gives are Windows activation and Windows updates. Existing virtual networks are not changed. The lab that creates the VM tells you what to do about this.

12. When the deployment finishes, select **Go to resource**.
13. On the virtual network page, open **Overview** and look at the address space and **DNS servers**. Learn says that a virtual network created in the portal uses Azure's DNS servers by default. To see the setting, select **DNS servers** under **Settings**. It should read **Default (Azure-provided)**. Do not change it. With this option, resources in the same virtual network can find each other by name. It does not resolve names across virtual networks.
14. Select **Subnets** and open `snet-vm`. Note the address range.

Check: under **Subnets**, `snet-vm` shows `10.10.1.0/24`, and **Address space** shows `10.10.0.0/16`.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from Lab 2. If you did the portal steps, skip to the checks, or delete `rg-azb-lab` first. Check the subscription, then set the variables. Use your own region.

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

Create the virtual network and the first subnet in one command. `--address-prefixes` is the whole network. `--subnet-prefixes` is the range of the first subnet. Learn's `az network vnet create` page shows this pattern.

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

Learn also shows that the setting `--default-outbound false` on `az network vnet subnet update` makes an existing subnet private. Do not run it in this lab.

## Terraform

The same two resources in Terraform. I have not run `terraform validate` on this block. The resource and argument names match Learn's Terraform quickstart for a virtual network, and `azurerm_resource_group` as a data source takes a `name`. It reads `rg-azb-lab` as an existing group, so create the group first (portal or CLI). It needs the same `versions.tf`, `providers.tf` and `terraform.tfvars` setup as [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/), so skip this section until you have done Lab 10.

```hcl
data "azurerm_resource_group" "lab" {
  name = "rg-azb-lab"
}

resource "azurerm_virtual_network" "azb" {
  name                = "vnet-azb"
  address_space       = ["10.10.0.0/16"]
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
}

resource "azurerm_subnet" "vm" {
  name                 = "snet-vm"
  resource_group_name  = data.azurerm_resource_group.lab.name
  virtual_network_name = azurerm_virtual_network.azb.name
  address_prefixes     = ["10.10.1.0/24"]
}
```

Learn says Terraform deployments that use an earlier API version keep the old default for outbound access, so a subnet made this way may not be private. The provider documentation (version 4.81.0) says the `azurerm_subnet` argument `default_outbound_access_enabled` defaults to `true`, so this subnet is not private. This matters later, when a VM needs a predictable outbound path. Do not create the network twice: use either the portal, the CLI or Terraform, not more than one.

## Check that it works

- `rg-azb-lab` exists in your chosen region.
- `vnet-azb` is in `rg-azb-lab`, in the same region, with the address space `10.10.0.0/16`.
- `snet-vm` is in `vnet-azb` with the range `10.10.1.0/24`.
- **DNS servers** on the virtual network reads **Default (Azure-provided)**.
- **Connected devices** on the virtual network is empty. Nothing is attached yet. That is expected.

## The most common mistake

Choosing an address range without checking the other networks you may join later. Two things from Learn:

- Learn says you can connect virtual networks to each other and to on-premises networks only if their ranges do not overlap. Two ranges overlap if any part of them is the same. For example, `10.0.0.0/16` and `10.0.1.0/24` overlap, because the second sits inside the first. Azure refuses to peer (link) two virtual networks that overlap. The portal and many tutorials offer `10.0.0.0/16`, so that range is easy to clash with. This lab uses `10.10.0.0/16` instead. In a real company, ask whoever manages the network which ranges are taken before you pick one.
- Changing a subnet later is not always possible. Learn says you can change a subnet's address range only if no resources are deployed in it. If any exist, you must first move them to another subnet or delete them. You can delete a subnet only when it is empty. Also, once a VM exists you can change its subnet, but not its virtual network.

You can add or resize the address space of a virtual network later. Learn says you can shrink a range only while it still covers the subnets inside it, and that a range holding a subnet cannot be removed. If the network is peered, the peering has to be synced after the change. It is still cheaper to choose well the first time.

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

`rg-azb-core` from Lab 3 is not touched by this lab.

## Where this is used in AVD

Azure Virtual Desktop session hosts are VMs, and they sit in a subnet of a virtual network just like the one you made. The size of that subnet, the DNS it uses and how it reaches the internet are decided before you build. See [Plan Azure Virtual Desktop networking](/azure-virtual-desktop/plan-avd-networking/) and [Network topology and IP planning for AVD](/azure-virtual-desktop/network-topology-and-ip-planning-for-avd/).

## Next lab

[Lab 9: Network security group](/azure-basics-labs/network-security-group/) adds a set of allow and deny rules and attaches it to `snet-vm`, so you control what can reach the subnet.

## Sources

- [What is Azure Virtual Network?](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)
- [Quickstart: Create a virtual network](https://learn.microsoft.com/en-us/azure/virtual-network/quickstart-create-virtual-network)
- [Create, change, or delete a virtual network](https://learn.microsoft.com/en-us/azure/virtual-network/manage-virtual-network)
- [Add, change, or delete a virtual network subnet](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-manage-subnet)
- [Azure Virtual Network frequently asked questions](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-faq)
- [Virtual networks and virtual machines in Azure](https://learn.microsoft.com/en-us/azure/virtual-network/network-overview)
- [Default outbound access in Azure](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/default-outbound-access)
- [Troubleshoot virtual network peering problems](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-network/virtual-network-troubleshoot-peering-issues)
- [az network vnet](https://learn.microsoft.com/en-us/cli/azure/network/vnet)
