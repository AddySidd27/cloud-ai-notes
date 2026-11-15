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

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn (Microsoft's documentation site).

A network security group (NSG) is a list of allow and deny rules for network traffic. It works like a door list for a subnet: it decides which traffic may come in and which may go out.

## What you need

- [Lab 8: Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/): the virtual network `vnet-azb` with the subnet `snet-vm`, in the resource group `rg-azb-lab`.
- [Lab 2: Azure Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) if you want to use the CLI steps. Azure CLI 2.76 or newer.
- Time: about 30 minutes. Cost: nothing for this lab. No VM, no public IP. (Learn lists a charge for NSG flow logs. This lab does not turn those on.)
- Role: Learn says to use the Network Contributor role or a custom role with the right permissions. Owner on the subscription of your throwaway account is enough.
- A way to find your own public IP address. Step 10 shows how.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top right of the portal before you change anything.
- Never use `Any` or `*` as the source for port 3389. That opens RDP to the whole internet.
- The RDP rule is temporary. You remove it in the clean-up, and you do not leave it in place "for later".
- This lab has no VM, so nothing can answer on port 3389 yet. The rule is for learning the rule format.
- Use the region on your notes sheet from [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/) everywhere. It is the same region as Lab 8. Learn says the NSG must be in the same subscription and location as the virtual network.

## What the lab builds

![Your PC, with your own public IP address, sends TCP 3389 toward the subnet snet-vm, and the temporary rule allows it. Anyone else on the internet is denied by the default rule DenyAllInBound. The network security group nsg-azb-vm is its own resource in the resource group rg-azb-lab, outside the virtual network. Part 1 creates it and Part 2 attaches it to the subnet. Part 3 reads the default rules, and Part 4 adds the temporary rule above them. No VM exists yet.](/img/basics/network-security-group.svg)

*Source: [Azure network security groups overview](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) and [Create, change, or delete a network security group](https://learn.microsoft.com/en-us/azure/virtual-network/manage-network-security-group). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: a rule has five parts.**

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
   - Region: the same region as `vnet-azb`. The NSG must be in the same region and subscription as the virtual network.
5. Select **Review + create**. When you see **Validation passed**, select **Create**.

Check: `nsg-azb-vm` is listed under **Network security groups**.

### Part 2: Attach it to the subnet

**Idea 3: subnet or network card.** You can attach an NSG to a subnet, to a VM's network interface (its virtual network card, or NIC), or to both. Learn advises against attaching an NSG to both, because the rules can conflict and are hard to troubleshoot. In this series you attach the NSG to the subnet only, so there is one list of rules to read.

6. Open `nsg-azb-vm`. Under **Settings**, select **Subnets**.
7. Select **+ Associate**. Choose the virtual network `vnet-azb` and the subnet `snet-vm`. Select **OK**.

Check: the **Subnets** page of `nsg-azb-vm` lists `vnet-azb / snet-vm`.

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

The outbound rule `AllowInternetOutBound` only says that the NSG does not block outbound internet traffic. Whether a VM can reach the internet also depends on the subnet (see [Lab 8](/azure-basics-labs/virtual-network-subnet/): new subnets in the portal are private) and on having an outbound method, such as the public IP address in Lab 12.

### Part 4: Add one RDP rule for your own IP only

10. Find your public IP address. This is the address the internet sees when you connect from home or work. Open a browser and search for "what is my IP". Learn's own RDP troubleshooting page also points to a "what is my IP" website for this. Use the IPv4 address (four numbers separated by dots). If you only see a long address with colons, search "what is my IPv4 address". `203.0.113.25` is only an example address from the documentation, not yours. Write your address on your notes sheet with today's date. If you use a VPN or a company proxy, the address is the one the VPN or proxy shows, and it can change. In Lab 12, check it again before you add the rule.
11. In `nsg-azb-vm`, select **Inbound security rules**, then **+ Add**.
12. Set:
    - Source: **IP Addresses**.
    - Source IP addresses/CIDR ranges: your IP address from step 10.
    - Source port ranges: `*`.
    - Destination: **Any**. This is fine here: the rule is on the subnet, and the source is your own IP.
    - Service: **RDP**. Learn says you can pick a predefined service such as RDP. After you pick it, check that the destination port range reads `3389` and the protocol reads TCP.
    - Action: **Allow**.
    - Priority: `1000`.
    - Name: `allow-rdp-my-ip`.
13. Select **Add**.

**Warning about "My IP address".** The Source list in the portal also has **My IP address**. Learn lists it as a source option. Do not rely on it blindly. It uses the address the portal sees from your browser, which may not be the address your RDP client will use, for example if you use a VPN or a proxy. Type the address yourself and check it. Never choose **Any** as the source for 3389.

Check: the **Inbound security rules** list shows `allow-rdp-my-ip` at priority 1000, source your IP address, port 3389, action Allow, above the default rules. Select the rule and read its source once more.

**Predict the result.** There is no VM yet, so you cannot connect. But you can say what the NSG would do. Write your answer for each row, then compare.

| Traffic arriving at `snet-vm` | Allow or deny? Which rule? |
| --- | --- |
| Your PC, TCP 3389 | ? |
| Another PC on the internet, TCP 3389 | ? |
| A VM in the same virtual network, any port | ? |
| Your PC, TCP 80 | ? |

Check: row 1 is allowed by `allow-rdp-my-ip` (1000). Row 2 is denied by `DenyAllInBound` (65500). Row 3 is allowed by `AllowVnetInBound` (65000). Row 4 is denied by `DenyAllInBound` (65500). You will see rule 1000 work in Lab 12.

## Steps with the Azure CLI

Do either the portal steps or these commands, not both. These are Bash commands for Cloud Shell, not PowerShell. Set the variables first. Replace the values with yours.

```bash
LOCATION=eastus2                 # the region you used in Lab 8
RG=rg-azb-lab
VNET=vnet-azb
SUBNET=snet-vm
NSG=nsg-azb-vm
MYIP=YOUR.PUBLIC.IP.HERE         # replace with your real IPv4 address from step 10, no spaces
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

Add the temporary RDP rule for your own IP only. First print the value, and check that it is your real address and not the placeholder text. If it is the placeholder, set `MYIP` again before you go on. If you ran the create command with a wrong address, delete the rule and create it again.

```bash
echo "The rule will allow: $MYIP"
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

No Terraform in this lab, because Terraform is taught in [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/). At the end of Lab 10, "Try it yourself" has a block that creates an NSG and attaches it to a subnet in code.

## Check that it works

- `nsg-azb-vm` exists in `rg-azb-lab`, and its **Subnets** page lists `vnet-azb / snet-vm`.
- The default rules match the table above. Learn lists these default rules, so the priorities and names should be the same. `DenyAllInBound` is at 65500 and your rule is at 1000, above it.
- While the rule exists, `allow-rdp-my-ip` shows your own address as the only source, never `Any` or `*`.
- You cannot test a real RDP connection yet, because there is no VM. Lab 12 adds one.

## The most common mistake

Setting the source of the RDP rule to **Any**, or to the **Internet** tag, to "make it work". Learn says the Internet tag means all public IP addresses. Anyone on the internet can then try to sign in to your VM. Use your own address, and take the rule away when you finish.

A close second: a rule that never matches because a deny rule has a lower number. Azure stops at the first match, so check the numbers first.

## Clean up

Remove the RDP rule. You can do this in the portal or the CLI. If you opened a new Cloud Shell, set `RG=rg-azb-lab` and `NSG=nsg-azb-vm` again first.

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

AVD does not need an inbound RDP rule from the internet. Learn says AVD uses reverse connect: the session host and the user's client both connect outward over HTTPS to the AVD service, and there is no TCP listener waiting for incoming RDP. So an AVD subnet keeps the default deny for inbound traffic and needs outbound access to the AVD service. Lab 12 opens RDP only because a plain VM needs it for the test. AVD does not. Read [Required connectivity for Azure Virtual Desktop](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) for the outbound list, and [Plan Azure Virtual Desktop networking](/azure-virtual-desktop/plan-avd-networking/) for NSG review in a real design.

## Next lab

[Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/) introduces Terraform, so you can describe a network like this one in code.

## Sources

- [Azure network security groups overview](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)
- [Create, change, or delete a network security group](https://learn.microsoft.com/en-us/azure/virtual-network/manage-network-security-group)
- [Azure service tags overview](https://learn.microsoft.com/en-us/azure/virtual-network/service-tags-overview)
- [Troubleshoot network security group misconfigurations blocking traffic](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-network/virtual-network-troubleshoot-nsg-blocking-traffic)
- [Troubleshoot RDP blocked by NSG rules on Azure Windows VMs](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/troubleshoot-rdp-nsg-problem)
- [Understanding Azure Virtual Desktop network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity)
