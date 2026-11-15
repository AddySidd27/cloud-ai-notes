---
title: "Network Security Group: Control What Can Reach Your Subnet"
seoTitle: "Azure Network Security Group for Beginners: Rules and RDP"
layout: post.njk
permalink: "/azure-basics-labs/network-security-group/"
order: 319
tags: [azure-basics-lab]
deck: "You create a network security group, attach it to your subnet, read the default rules, add one RDP rule for your own IP address only, and remove it again."
description: "Beginner Azure lab: create a network security group, attach it to a subnet, read the default rules, allow RDP from your own IP only, then remove the rule."
---

By the end of this lab you will have a network security group named `nsg-azb-vm` attached to the subnet `snet-vm`. You will have read its default rules, added one rule that allows Remote Desktop (RDP) from your own public IP address only, and removed that rule again.

I have not run these steps in a live tenant for this article, and I have not run `terraform validate` on the Terraform block. The steps follow Microsoft Learn (Microsoft's documentation site).

A network security group (NSG) is a list of allow and deny rules for network traffic. It works like a door list for a subnet: it decides which traffic may come in and which may go out.

## What you need

- [Lab 8: Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/): the virtual network `vnet-azb` with the subnet `snet-vm`, in the resource group `rg-azb-lab`.
- [Lab 2: Cloud Shell and the Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) if you want to use the CLI steps. Azure CLI 2.76 or newer.
- Time: about 20 minutes. Cost: this lab creates no VM. I found no price for an NSG itself on Learn. Learn does list a charge for NSG flow logs, and this lab does not turn those on.
- Role: Learn says to use the Network Contributor role or a custom role with the right permissions. Owner on the subscription of your throwaway account is enough.
- A way to find your own public IP address. Step 5 shows how.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top right of the portal before you change anything.
- Never use `Any` or `*` as the source for port 3389. That opens RDP to the whole internet.
- The RDP rule is temporary. You remove it in the clean-up, and you do not leave it in place "for later".
- This lab has no VM, so nothing can answer on port 3389 yet. The rule is for learning the rule format.
- Pick one region and use it everywhere. Use the same region as Lab 8. Learn says the NSG must be in the same subscription and location as the virtual network.

## What the lab builds

![A left-to-right diagram. A laptop with your own public IP address sends traffic toward the virtual network vnet-azb. The network security group nsg-azb-vm is attached to the subnet snet-vm and holds the default rules plus one temporary rule that allows TCP 3389 from your IP address only.](/img/basics/network-security-group.svg)

*Source: [Azure network security groups overview](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) and [Create, change, or delete a network security group](https://learn.microsoft.com/en-us/azure/virtual-network/manage-network-security-group). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: a rule is five things plus an action.**

Each rule says which traffic it matches and what to do with it. The parts are: a priority, a source, a destination, a port and protocol, and an action (Allow or Deny). Learn says rules match on source, source port, destination, destination port and protocol. It also says an NSG is stateful: if you allow traffic in, the reply goes out without a second rule.

**Idea 2: the lowest number wins.**

Priority is a number from 100 to 4096 for your own rules. Azure checks rules from the lowest number up, and stops at the first rule that matches. Azure also adds default rules to every NSG with numbers from 65000 to 65500, so your rules are always checked first. You cannot delete the default rules, but you can override them with a rule that has a lower number.

### Part 1: Create the NSG

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name at the top right.
2. In the search box at the top, enter **Network security group** and select **Network security groups**.
3. Select **+ Create**.
4. On the **Basics** tab, set:
   - Subscription: your throwaway subscription.
   - Resource group: `rg-azb-lab`.
   - Network security group name: `nsg-azb-vm`.
   - Region: the same region as `vnet-azb`.
5. Select **Review + create**. When you see **Validation passed**, select **Create**.

### Part 2: Attach it to the subnet

**Idea 3: subnet or network card.** You can attach an NSG to a subnet, to a VM's network interface (its virtual network card, or NIC), or to both. Learn says that when both have an NSG, inbound traffic is checked by the subnet NSG first and then by the NIC NSG, and both must allow it. For outbound traffic the order is the other way round. Learn also advises against attaching an NSG to both a subnet and its network cards, because the rules can conflict and are hard to troubleshoot. In this series you attach to the subnet only.

6. Open `nsg-azb-vm`. Under **Settings**, select **Subnets**.
7. Select **+ Associate**. Choose the virtual network `vnet-azb` and the subnet `snet-vm`. Select **OK**.

### Part 3: Read the default rules

8. Under **Settings**, select **Inbound security rules**. You see three default rules. Write down their names, priorities and actions.
9. Select **Outbound security rules** and do the same.

Learn lists these defaults:

| Direction | Priority | Name | Action | What it means |
|---|---|---|---|---|
| Inbound | 65000 | AllowVnetInBound | Allow | Traffic from inside the virtual network (and connected networks) is allowed. |
| Inbound | 65001 | AllowAzureLoadBalancerInBound | Allow | Health checks from the Azure load balancer are allowed. |
| Inbound | 65500 | DenyAllInBound | Deny | Everything else coming in is denied, including the internet. |
| Outbound | 65000 | AllowVnetOutBound | Allow | Traffic to the virtual network is allowed. |
| Outbound | 65001 | AllowInternetOutBound | Allow | Traffic out to the internet is allowed. |
| Outbound | 65500 | DenyAllOutBound | Deny | Everything else going out is denied. |

The first two rules in each direction use names such as `VirtualNetwork`, `AzureLoadBalancer` and `Internet`. Learn calls these service tags. A service tag stands for a group of IP addresses that Microsoft keeps up to date, so you do not type the addresses yourself.

So by default, nothing from the internet can reach the subnet. That is why a new VM is closed until you open it.

### Part 4: Add one RDP rule for your own IP only

10. Find your public IP address. This is the address the internet sees when you connect from home or work. Open a browser and search for "what is my IP". Learn's own RDP troubleshooting page also points to a "what is my IP" website for this. Note it down, for example `203.0.113.25`. If you use a VPN or a company proxy, the address is the one the VPN or proxy shows, and it can change. Check it again right before you add the rule.
11. In `nsg-azb-vm`, select **Inbound security rules**, then **+ Add**.
12. Set:
    - Source: **IP Addresses**.
    - Source IP addresses/CIDR ranges: your IP address from step 10, for example `203.0.113.25`.
    - Source port ranges: `*`.
    - Destination: **Any**.
    - Service: **RDP**. Learn says you can pick a predefined service such as RDP. After you pick it, check that the destination port range reads `3389` and the protocol reads TCP.
    - Action: **Allow**.
    - Priority: `1000`.
    - Name: `allow-rdp-my-ip`.
13. Select **Add**.

**Warning about "My IP address".** The Source list in the portal also has **My IP address**. Learn lists it as a source option. Do not rely on it blindly. It uses the address the portal sees from your browser, which may not be the address your RDP client will use, for example if you use a VPN, a proxy or Cloud Shell. Type the address yourself and check it. Never choose **Any** as the source for 3389.

Check: the **Inbound security rules** list shows `allow-rdp-my-ip` at priority 1000, source your IP address, port 3389, action Allow, above the default rules. Select the rule and read its source once more.

## Steps with the Azure CLI

Set the variables first. Replace the values with yours.

```bash
LOCATION=eastus2                 # the region you used in Lab 8
RG=rg-azb-lab
VNET=vnet-azb
SUBNET=snet-vm
NSG=nsg-azb-vm
MYIP=203.0.113.25                # your public IP, found with a browser search
```

Create the NSG.

```bash
az network nsg create \
    --resource-group $RG \
    --name $NSG \
    --location $LOCATION
```

Attach it to the subnet.

```bash
az network vnet subnet update \
    --resource-group $RG \
    --vnet-name $VNET \
    --name $SUBNET \
    --network-security-group $NSG
```

Read the default rules. Learn's reference for `az network nsg rule list` has an `--include-default` option for this.

```bash
az network nsg rule list \
    --resource-group $RG \
    --nsg-name $NSG \
    --include-default \
    --output table
```

Add the temporary RDP rule for your own IP only.

```bash
az network nsg rule create \
    --resource-group $RG \
    --nsg-name $NSG \
    --name allow-rdp-my-ip \
    --priority 1000 \
    --direction Inbound \
    --access Allow \
    --protocol Tcp \
    --source-address-prefixes $MYIP \
    --destination-address-prefixes '*' \
    --destination-port-ranges 3389
```

Check: list the rules you created. Without `--include-default`, the list shows only your own rule, `allow-rdp-my-ip`, with your IP address as the source.

```bash
az network nsg rule list --resource-group $RG --nsg-name $NSG --output table
```

## Terraform

This block creates the NSG and attaches it to the subnet from Lab 8. It does not include the RDP rule, because that rule is temporary. I have not run `terraform validate` on it. The `azurerm_network_security_group` and `azurerm_subnet_network_security_group_association` arguments (`name`, `location`, `resource_group_name`, `subnet_id`, `network_security_group_id`) match Learn's Terraform samples, and `azurerm_resource_group` as a data source takes a `name`.

Skip this section until you have done [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/). It needs the same `versions.tf`, `providers.tf` and `terraform.tfvars` setup, in a new empty folder, for example `nsg-tf`. Get the subnet ID with this command and put it in `terraform.tfvars` as `subnet_id = "..."`:

```bash
az network vnet subnet show --resource-group rg-azb-lab --vnet-name vnet-azb --name snet-vm --query id -o tsv
```

```hcl
variable "subnet_id" {
  description = "Resource ID of snet-vm from Lab 8"
  type        = string
}

data "azurerm_resource_group" "lab" {
  name = "rg-azb-lab"
}

resource "azurerm_network_security_group" "vm" {
  name                = "nsg-azb-vm"
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
}

resource "azurerm_subnet_network_security_group_association" "vm" {
  subnet_id                 = var.subnet_id
  network_security_group_id = azurerm_network_security_group.vm.id
}
```

If you create the NSG in Terraform, do not also create it in the portal or CLI. Use one way only. Read the plan before you apply it: it must show two resources to add. Keep this folder's state: if you later run `terraform destroy` here, it removes the NSG and detaches it from the subnet.

## Check that it works

- `nsg-azb-vm` exists in `rg-azb-lab`, and its **Subnets** page lists `vnet-azb / snet-vm`.
- The default rules match the table above. Learn lists these default rules, so the priorities and names should be the same.
- While the rule exists, `allow-rdp-my-ip` shows your own address as the only source, never `Any` or `*`.
- You cannot test a real RDP connection yet, because there is no VM. Lab 12 adds one.

## The most common mistake

Setting the source of the RDP rule to **Any**, or to the **Internet** tag, to "make it work". Learn says the Internet tag means all public IP addresses. Anyone on the internet can then try to sign in to your VM. Use your own address, and take the rule away when you finish.

A close second: a rule that never matches because a deny rule has a lower number. Azure stops at the first match, so check the numbers first.

## Clean up

Remove the RDP rule. You can do this in the portal or the CLI.

Portal: open `nsg-azb-vm`, select **Inbound security rules**, tick `allow-rdp-my-ip`, select **Delete**, then **Yes**.

CLI:

```bash
az network nsg rule delete \
    --resource-group $RG \
    --nsg-name $NSG \
    --name allow-rdp-my-ip
```

Learn says that removing a rule does not cut connections that are already open. It only affects new connections.

Check: **Inbound security rules** shows only the three default rules again.

Keep for later labs:

- `nsg-azb-vm`, attached to `snet-vm`. I found no charge for an NSG on Learn, and Lab 12 uses it.
- `vnet-azb` and `rg-azb-lab`.

## Where this is used in AVD

AVD does not need an inbound RDP rule from the internet. Learn says AVD uses reverse connect: the session host and the user's client both connect outward over HTTPS to the AVD service, and there is no TCP listener waiting for incoming RDP. So an AVD subnet keeps the default deny for inbound traffic and needs outbound access to the AVD service. Read [Required connectivity for Azure Virtual Desktop](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) for the outbound list, and [Plan Azure Virtual Desktop networking](/azure-virtual-desktop/plan-avd-networking/) for NSG review in a real design.

## Next lab

[Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/) introduces Terraform, so you can describe a network like this one in code.

## Sources

- [Azure network security groups overview](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)
- [Create, change, or delete a network security group](https://learn.microsoft.com/en-us/azure/virtual-network/manage-network-security-group)
- [Azure service tags overview](https://learn.microsoft.com/en-us/azure/virtual-network/service-tags-overview)
- [Troubleshoot network security group misconfigurations blocking traffic](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-network/virtual-network-troubleshoot-nsg-blocking-traffic)
- [Troubleshoot RDP blocked by NSG rules on Azure Windows VMs](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/troubleshoot-rdp-nsg-problem)
- [Understanding Azure Virtual Desktop network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity)
