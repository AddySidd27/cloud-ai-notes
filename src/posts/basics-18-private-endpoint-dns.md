---
title: "Private Endpoint and Private DNS for Azure Files (Optional)"
seoTitle: "Azure Private Endpoint and Private DNS for Azure Files Lab"
layout: post.njk
permalink: "/azure-basics-labs/private-endpoint-dns/"
order: 328
tags: [azure-basics-lab]
deck: "Give your Azure Files storage account a private address in your virtual network, watch the file share name resolve to it, and then close the public door."
description: "Beginner Azure lab: create a private endpoint and the privatelink.file.core.windows.net private DNS zone, check nslookup from a VM, then disable public access."
---

By the end of this lab the file share from Lab 14 will be reachable from your VM through a private address in `vnet-azb`. You will have seen the share's name resolve to that address with `nslookup`, mounted the share over it, and then turned off public network access on the storage account and shown that the VM still works.

This lab is optional. Nothing later depends on it. It is the one lab in this series that can lock you out of your own storage account, so read "Safety first" before you start.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn. I did not write a Terraform block for this lab, and I say why in the Terraform section.

## What you need

- [Lab 8: Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/): `vnet-azb` in `rg-azb-lab`. The virtual network's DNS servers must still read **Default (Azure-provided)**.
- [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the VM `vm-azb-win01` in `vnet-azb`, and a way to sign in to it. The VM must be running. Lab 12 told you to remove the RDP rule (`allow-rdp-my-ip`) from `nsg-azb-vm` at the end, so add it again for your current public IP address, as Lab 12 showed, and remove it again in "Clean up".
- [Lab 14: Storage account and Azure Files](/azure-basics-labs/storage-azure-files/): the storage account (named `stazb` and five digits) and the file share `azbshare`, mounted from the VM as `testuser1` with Microsoft Entra Kerberos. Keep the account name to hand. This lab calls it `<account>`.
- For the CLI part only: Cloud Shell or the Azure CLI from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Azure CLI 2.76 or newer.
- The same region as the virtual network. Learn says a private endpoint must be in the same region as its virtual network.
- A role that can create network resources and change the storage account. Owner or Contributor on the test subscription is enough.
- Time: about 45 minutes. Cost: this lab creates two things that are billed while they exist, a private endpoint and a private DNS zone. See "Safety first". Delete them the same day.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top of the portal before you change anything.
- Cost. Learn lists a private endpoint as billed per endpoint per hour, plus the data processed through it. Learn also says DNS zones are billed, by the number of zones and the number of DNS queries. I am not giving prices, because they change. Use the pricing pages in "Sources", and delete both resources when you finish. Budgets from Lab 3 only send alerts. They do not stop anything.
- Lockout. Part 6 turns off public network access on the storage account. After that, nothing on the public internet can reach the share, including your own PC. Only clients that use the private endpoint can. Do not start Part 6 until the VM has mounted the share over the private address (steps 17 and 18). If something goes wrong, the way back is in "The most common mistake".
- Use only the storage account from Lab 14. Do not do this on an account that holds anything you need.
- If you ever do this in a real tenant, ask the team that owns DNS first. A private DNS zone changes how a name resolves for everything in the linked network.
- Azure already requires multifactor authentication (MFA) for Azure management work. If you are asked for it, that is expected.

## What the lab builds

![A left-to-right diagram. Inside the resource group rg-azb-lab, a Windows VM in the subnet snet-vm of the virtual network vnet-azb asks the private DNS zone privatelink.file.core.windows.net for the name of the storage account. The zone answers with a 10.10.2.x address. That address belongs to the private endpoint pe-azb-file in the second subnet snet-pe, which connects to the file service of the storage account from Lab 14. A separate arrow from the public internet to the storage account is marked closed once public network access is disabled.](/img/basics/private-endpoint-dns.svg)

*Source: [Configure network endpoints for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-networking-endpoints), [Azure Private Endpoint private DNS zone values](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns) and [Quickstart: Create a private endpoint by using the Azure CLI](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-cli). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Part 1: See what the name resolves to today

DNS (the Domain Name System) turns a name into an IP address. Your storage account has a name like `<account>.file.core.windows.net`. Before you change anything, look at what that name gives you from inside the VM.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the subscription name.
2. Sign in to the VM `vm-azb-win01` the way you did in Lab 12.
3. On the VM, open PowerShell and run this. Replace `<account>` with your storage account name (`stazb` and five digits).

```powershell
nslookup <account>.file.core.windows.net
```

4. Write down the address in the answer. It is a public address, not one that starts with `10.`. This is the baseline.

### Part 2: A second subnet for the private endpoint

**Idea 1: a private endpoint is a network card with a private address.** A private endpoint is a network interface that Azure places in your subnet. It gets an address from the subnet's range (for example `10.10.2.4`), and it is linked to one service, here the file service of your storage account. A VM that talks to that address reaches the service over Azure's network and not over the public internet. Learn says the private endpoint must be in the same region as the virtual network, and the storage account itself can be in a different region.

Learn does not say the private endpoint needs a subnet of its own. It says several private endpoints can sit in the same or in different subnets. I use a second subnet, `snet-pe`, for one practical reason. Learn says the network policy setting for private endpoints applies to every private endpoint in the subnet. A separate subnet keeps that setting away from the VM's subnet. Learn also says network policies for private endpoints are off by default, and this lab leaves them off. So the network security group you attached to `snet-vm` in Lab 9 does not apply to the private endpoint.

5. In the portal search box, enter **Virtual networks** and open `vnet-azb`.
6. Under **Settings**, select **Subnets**, then select **+ Subnet** (the button may read **+ Add subnet**).
7. Set **Name** to `snet-pe`. Set the starting address to `10.10.2.0` and the size to `/24`. Leave everything else as offered. Select **Save** (or **Add**).

Check: **Subnets** now lists `snet-vm` (`10.10.1.0/24`) and `snet-pe` (`10.10.2.0/24`).

### Part 3: The private endpoint, with its DNS zone

**Idea 2: the name stays the same, the answer changes.** You will not point the VM at a new name. You keep using `<account>.file.core.windows.net`. Here is how that works, as Learn describes it.

- When a private endpoint exists for the storage account, Azure's public DNS adds an alias (a CNAME record) that sends `<account>.file.core.windows.net` on to `<account>.privatelink.file.core.windows.net`. A CNAME says "this name is another name for that one".
- Inside your virtual network, a private DNS zone called `privatelink.file.core.windows.net` answers for that second name with the private address of the endpoint.
- A private DNS zone is a DNS zone that only the virtual networks linked to it can see. Learn says the zone name must follow the recommended name for the service. For the `file` sub-resource of a storage account, that name is `privatelink.file.core.windows.net`.
- Learn says the connection URL of your application does not change, and you mount the share with the original name, not the `privatelink` name.

A machine outside the linked network still gets the alias, but it has no private zone to answer the second name, so it ends up with the public address. That is how one name can give two different answers.

The portal wizard sets all of this up for you. Learn describes it as "automatic DNS integration": the wizard creates the zone (or reuses a matching one), links it to the virtual network and adds the record.

8. In the portal search box, enter **Private endpoints**. Select **Private endpoints**, then **+ Create**. (Learn also describes starting from the resource group: open it, select **+ Create**, search for **Private Endpoint**.)
9. **Basics** tab: choose your subscription and set **Resource group** to `rg-azb-lab`. Set **Name** to `pe-azb-file`. Leave the network interface name as offered. Set **Region** to the same region as `vnet-azb`. Select **Next: Resource**.
10. **Resource** tab: set **Resource type** to `Microsoft.Storage/storageAccounts`. Set **Resource** to your Lab 14 storage account. Set **Target sub-resource** to `file`. Select **Next: Virtual Network**. If the tab asks for a connection method first, choose the option that connects to an Azure resource in your directory.
11. **Virtual Network** tab: set **Virtual network** to `vnet-azb` and **Subnet** to `snet-pe`. Leave the IP address on dynamic. Leave the network policy and application security group settings as they are. Select **Next: DNS**.
12. **DNS** tab: check that integration with a private DNS zone is turned on, and that the zone listed is `privatelink.file.core.windows.net`, in subscription and resource group `rg-azb-lab`. Select **Next: Tags**, then **Next: Review + create**, then **Create**.

Check: when the deployment finishes, open `pe-azb-file`. Its connection status is **Approved**. Open the private DNS zone `privatelink.file.core.windows.net` in `rg-azb-lab`. Under **DNS Management** > **Recordsets** you see an A record named after your storage account, with a `10.10.2.x` address. Under **Virtual network links** you see `vnet-azb`. I could not confirm the exact menu names on Learn, so look for the record list and the links list.

### Part 4: See the private address from the VM

13. Back on the VM, run the same command as in step 3.

```powershell
nslookup <account>.file.core.windows.net
```

You should now see something like this. This is Learn's example, with its own sample names and address.

```output
Server:  UnKnown
Address:  168.63.129.16

Non-authoritative answer:
Name:    <account>.privatelink.file.core.windows.net
Address:  10.10.2.4
Aliases:  <account>.file.core.windows.net
```

Read it from the bottom. You asked for `<account>.file.core.windows.net`. That is listed under `Aliases`, which is the CNAME. The name it points to is `<account>.privatelink.file.core.windows.net`, and the private zone answered that with a `10.10.2.x` address from `snet-pe`. The `168.63.129.16` line is Azure's own DNS service, which every VM in a virtual network with default DNS uses.

If you still see the public address from step 4, do not go on. Read "The most common mistake".

14. Run `nslookup` for the same name on your own PC, outside Azure. You get the public address, and your PC is not on the private network. That is the second answer from Idea 2. Do not worry about it. It is the reason the next part exists.

### Part 5: Mount the share over the private address

Mounting needs the same sign-in as in Lab 14: you sign in to the VM as `testuser1` and the share is reached with Microsoft Entra Kerberos. Read the next box first.

**Microsoft Entra Kerberos over a private endpoint.** Because Lab 14 used Microsoft Entra Kerberos, there is one extra step. Learn says that when you connect through a private endpoint with Microsoft Entra Kerberos, you must add the private link name to the storage account's Microsoft Entra application. Without it, the mount asks for credentials and then rejects them (Learn lists this as error 1326), because the Kerberos ticket cannot be issued for the private link name. The steps from Learn:

- In the Microsoft Entra admin center, go to **App registrations** > **All applications**, and open the application named `[Storage Account] <account>.file.core.windows.net`.
- Select **Manifest**. Copy the existing text somewhere safe as a backup.
- In `identifierUris`, for every `<account>.file.core.windows.net` entry add a matching `<account>.privatelink.file.core.windows.net` entry. Select **Save**.
- Retry the mount.

Both Learn pages are in "Sources". Do the manifest step as an administrator, not as `testuser1`.

15. On the VM, check that the SMB port answers. SMB (Server Message Block) is the protocol Windows uses for file shares, and it uses TCP port 445. Learn lists `Test-NetConnection` for this check.

```powershell
Test-NetConnection -ComputerName <account>.file.core.windows.net -Port 445
```

`TcpTestSucceeded : True` and a `RemoteAddress` of `10.10.2.x` mean the VM reached the private endpoint.

16. If the share is still mounted from Lab 14, disconnect it first. Learn says file shares connected through the public endpoint must be remounted. In File Explorer, right-click the drive and select **Disconnect**, or run `net use Z: /delete` (use your drive letter).
17. Mount the share again the way you did in Lab 14, as `testuser1`. Use `\\<account>.file.core.windows.net\azbshare`, with the original name and not the `privatelink` name.
18. Create a small test file in the share, for example `private-test.txt`.

Check: the share opens and the test file is there.

### Part 6: Close the public door

**Idea 3: two doors.** A storage account has a public door and, now, a private one. They are separate. Learn says disabling public network access means clients cannot connect through the public endpoint, including through service endpoints, and that clients can still connect through private endpoints. It also says the setting does not restrict outbound traffic from the clients. Turning off the public door does not touch the private one.

Stop here and look at this checklist before you go on.

- You saw a `10.10.2.x` answer from the VM in step 13.
- The VM mounted the share and wrote a file in steps 17 and 18.
- You know the way back (see "The most common mistake").

19. In the portal, open your storage account.
20. In the left menu, under **Security + networking**, select **Networking**.
21. Under **Public network access**, select **Manage**.
22. Select **Disable**, then **Proceed**, then **Save**.
23. On the VM, open the share again, read the test file and write a second file, `private-test-2.txt`. Both should work. If the share was already open, disconnect and mount it again to be sure.
24. On your own PC, try to open the same share, or open the storage account's file share in the portal. It should fail or show an access error. The exact message depends on the client.

Check: the VM can read and write, and your PC cannot reach the share.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from Lab 2. Skip them if you did the portal steps. Check the subscription, then set the variables. Use your own region and your own storage account name.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
RG=rg-azb-lab
VNET=vnet-azb
SUBNET_PE=snet-pe
PE=pe-azb-file
ZONE=privatelink.file.core.windows.net
SA=stazb<5 digits>         # the Lab 14 account
LOCATION=$(az network vnet show --resource-group $RG --name $VNET --query location --output tsv)   # the region of vnet-azb
```

Create the second subnet.

```bash
az network vnet subnet create \
  --resource-group $RG \
  --vnet-name $VNET \
  --name $SUBNET_PE \
  --address-prefixes 10.10.2.0/24
```

Create the private endpoint for the `file` sub-resource. Learn calls the sub-resource the group ID.

```bash
SA_ID=$(az storage account show --resource-group $RG --name $SA --query id --output tsv)

az network private-endpoint create \
  --resource-group $RG \
  --name $PE \
  --location $LOCATION \
  --vnet-name $VNET \
  --subnet $SUBNET_PE \
  --private-connection-resource-id $SA_ID \
  --group-id file \
  --connection-name conn-azb-file
```

Create the private DNS zone, link it to the virtual network, and attach it to the private endpoint with a DNS zone group. The zone group is what makes the A record appear and disappear with the endpoint. `--registration-enabled false` is correct here: this zone is only for answering, not for registering VM names.

```bash
az network private-dns zone create \
  --resource-group $RG \
  --name $ZONE

az network private-dns link vnet create \
  --resource-group $RG \
  --zone-name $ZONE \
  --name link-vnet-azb \
  --virtual-network $VNET \
  --registration-enabled false

az network private-endpoint dns-zone-group create \
  --resource-group $RG \
  --endpoint-name $PE \
  --name zg-azb-file \
  --private-dns-zone $ZONE \
  --zone-name file
```

Check: this shows the endpoint connection state, the zone link and the A record.

```bash
az network private-endpoint show --resource-group $RG --name $PE \
  --query "privateLinkServiceConnections[0].privateLinkServiceConnectionState.status" -o tsv
az network private-dns link vnet list --resource-group $RG --zone-name $ZONE -o table
az network private-dns record-set a list --resource-group $RG --zone-name $ZONE -o table
```

You should see `Approved`, the link `link-vnet-azb`, and an A record named after the storage account. Then do Parts 4 and 5 from the portal steps on the VM (steps 13 to 18).

Only when the VM has mounted the share over the private address, turn off public network access.

```bash
az storage account update \
  --resource-group $RG \
  --name $SA \
  --public-network-access Disabled \
  --output none

az storage account show --resource-group $RG --name $SA --query publicNetworkAccess -o tsv
```

The last command should print `Disabled`. Then repeat steps 23 and 24 from the portal steps.

## Terraform

No Terraform in this lab, because I could not check the resource names and arguments for a private endpoint, a private DNS zone link and a DNS zone group against Learn, and I do not want to give you code I have not checked. Use the portal or the CLI here. If you want the Terraform version later, take the Terraform introduction in [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/) and the provider documentation for the private endpoint resource.

## Check that it works

- From the VM, `nslookup <account>.file.core.windows.net` shows a `10.10.2.x` address, and lists the `privatelink` name.
- From your own PC, the same command shows a public address.
- `pe-azb-file` shows a connection status of **Approved**.
- The private DNS zone `privatelink.file.core.windows.net` has a link to `vnet-azb` and an A record for the storage account.
- With public network access disabled, the VM can still read and write the share, and your PC cannot reach it.

## The most common mistake

Two mistakes, in the order you are likely to hit them.

**The name still resolves to the public address.** The usual causes, from Learn and from this lab's setup:

- The private DNS zone is not linked to `vnet-azb`. Check **Virtual network links** on the zone.
- The zone name is wrong. Learn says the automatic DNS records are created only if you use the recommended zone name. For Azure Files it is exactly `privatelink.file.core.windows.net`.
- The VM does not use Azure's DNS. If someone changed the DNS servers of `vnet-azb` away from **Default (Azure-provided)**, the VM asks another server, and that server does not know the private zone. Lab 8 left this setting alone.
- You tested from your own PC and not from the VM. Run `nslookup` on the VM.

If you turned off public access while the name still pointed to the public address, the VM now fails to mount the share. Do not panic. Nothing is deleted.

**Locking yourself out.** Public network access is off, the VM cannot reach the share, and you cannot browse it from your PC either. The setting is a property of the storage account, so you can change it back from the portal or the CLI. In the portal, go to the storage account, **Security + networking** > **Networking**, and under **Public network access** select **Manage**, then choose the option that allows access from all networks (the wording may read **Enable** or **Enabled from all networks**). With the CLI:

```bash
az storage account update --resource-group rg-azb-lab --name <account> --public-network-access Enabled
```

Then fix the DNS problem and try again.

## Clean up

Delete in this order. The private endpoint and the DNS zone cost money while they exist, so do not leave them running.

1. Re-enable public network access on the storage account, so the later labs and your own PC can reach it again (the portal steps or the CLI command in the section above). You can skip this step if you want to keep it closed, but then you can only reach the share from inside `vnet-azb`.
2. Delete the private endpoint `pe-azb-file`. Portal: open the private endpoint, select **Delete**. Learn says that when you delete a private endpoint, the DNS records in its DNS zone group are deleted too.
3. Delete the virtual network link from the private DNS zone. Portal: open the zone, **Virtual network links**, select the link, **Delete**.
4. Delete the private DNS zone `privatelink.file.core.windows.net`.
5. Optional: delete the subnet `snet-pe` from `vnet-azb`. It is empty now, and an empty subnet costs nothing, so you can keep it.

The same in the CLI:

```bash
az storage account update --resource-group $RG --name $SA --public-network-access Enabled --output none
az network private-endpoint delete --resource-group $RG --name $PE
az network private-dns link vnet delete --resource-group $RG --zone-name $ZONE --name link-vnet-azb --yes
az network private-dns zone delete --resource-group $RG --name $ZONE --yes
az network vnet subnet delete --resource-group $RG --vnet-name $VNET --name $SUBNET_PE
```

If you made the zone link in the portal, the link may have a different name. List the links with `az network private-dns link vnet list --resource-group $RG --zone-name $ZONE -o table` first.

Check: `az network private-endpoint list --resource-group $RG -o table` is empty, and `az network private-dns zone list --resource-group $RG -o table` no longer lists the zone.

Also remove the RDP rule again, as in Lab 12: open `nsg-azb-vm`, **Inbound security rules**, tick `allow-rdp-my-ip`, **Delete**. Sign out of the VM first.

Keep for later labs: `rg-azb-lab`, `vnet-azb`, `snet-vm`, the VM `vm-azb-win01` and the storage account with its file share `azbshare`. Remount the share on the VM if it was mounted over the private address, because the name now resolves to the public address again. If you added `privatelink` names to the storage account's Microsoft Entra app, they do no harm. [Lab 19](/azure-basics-labs/when-something-breaks/) deletes the storage account and tells you to check that app.

## Where this is used in AVD

Azure Virtual Desktop session hosts usually keep user profiles (FSLogix profile containers) on an Azure Files share, and many companies close that storage account to the public internet and reach it through a private endpoint and a private DNS zone, exactly as you did here. See [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/) for the storage choices, and [Required Connectivity for Azure Virtual Desktop: Endpoints, Proxies, DNS and Private Link](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) for how DNS and Private Link fit into the wider network.

## Next lab

[Lab 19: When something breaks](/azure-basics-labs/when-something-breaks/) puts the checks from this series together, so you can work out what went wrong when a step fails.

## Sources

- [Configure network endpoints for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-networking-endpoints)
- [Azure Private Endpoint private DNS zone values](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns)
- [Azure Private Endpoint DNS integration scenarios](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns-integration)
- [What is a private endpoint?](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
- [Manage network policies for private endpoints](https://learn.microsoft.com/en-us/azure/private-link/disable-private-endpoint-network-policy)
- [Quickstart: Create a private endpoint by using the Azure CLI](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-cli)
- [Tutorial: Connect to a storage account using an Azure private endpoint](https://learn.microsoft.com/en-us/azure/private-link/tutorial-private-endpoint-storage-portal)
- [Mount SMB Azure file share on Windows](https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-windows)
- [Troubleshoot Azure Files connectivity and access problems (SMB)](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-storage/files/connectivity/files-troubleshoot-smb-connectivity)
- [Enable Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable)
- [Troubleshoot Azure Files identity-based authentication and authorization issues (SMB)](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-storage/files/security/files-troubleshoot-smb-authentication)
- [Azure Private Link cost optimization principles](https://learn.microsoft.com/en-us/azure/private-link/private-link-cost-optimization)
- [What is Azure Private DNS?](https://learn.microsoft.com/en-us/azure/dns/private-dns-overview)
- [az network private-endpoint dns-zone-group](https://learn.microsoft.com/en-us/cli/azure/network/private-endpoint/dns-zone-group)
- [az network private-dns zone](https://learn.microsoft.com/en-us/cli/azure/network/private-dns/zone)
