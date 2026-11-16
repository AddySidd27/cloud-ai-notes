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

By the end of this lab the file share from the Azure Files lab will be reachable from your VM through a private address in `vnet-azb`. You will have seen the share's name resolve to that address with `nslookup`, mounted the share over it, and then turned off public network access on the storage account and shown that the VM still works.

This lab is optional. Nothing later depends on it. It is the one lab in this series that can lock you out of your own storage account, so read "Safety first" before you start.

## What you need

- [Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/): `vnet-azb` in `rg-azb-lab`. The virtual network's DNS servers must still read **Default (Azure-provided)**.
- [Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the VM `vm-azb-win01` in `vnet-azb`, and a way to sign in to it. The VM is stopped now, so the first section starts it and connects you.
- [Storage and Azure Files](/azure-basics-labs/storage-azure-files/): the storage account (named `stazb` and five digits) and the file share `azbshare`, mounted from the VM as `testuser1` with Microsoft Entra Kerberos. Keep the account name to hand. This lab calls it `<account>`.
- For the CLI part only: Cloud Shell or the Azure CLI (see the [Cloud Shell lab](/azure-basics-labs/cloud-shell-and-azure-cli/)). Azure CLI 2.76 or newer.
- Your region from the notes sheet in [the account lab](/azure-basics-labs/start-azure-account-tenant-subscription/), the same one as the virtual network. A private endpoint must be in the same region as its virtual network.
- A role that can create network resources and change the storage account. Owner or Contributor on the test subscription is enough.
- Time: about 60 minutes. Cost: this lab creates two things that are billed while they exist, a private endpoint and a private DNS zone. See "Safety first". Delete them the same day. The VM bills for compute while it runs, and this lab ends with it stopped.

**State of your resources**

| | At the start | At the end |
|---|---|---|
| VM `vm-azb-win01` | Stopped (deallocated), as the Azure Files lab leaves it. Step 2 starts it. | Stopped (deallocated) |
| Rule `allow-rdp-my-ip` in `nsg-azb-vm` | Not there. Step 3 adds it. | Not there. "Clean up" deletes it. |
| Public IP `pip-azb-win01` | Exists. It stays. | Exists |
| Storage account `stazb<digits>` | Public network access enabled | Enabled again in "Clean up" |
| New in this lab | Nothing | Nothing. The endpoint `pe-azb-file`, the DNS zone and its link are deleted. The subnet `snet-pe` is deleted too. |

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top of the portal before you change anything.
- Cost. A private endpoint is billed per endpoint per hour, plus the data processed through it. A private DNS zone is billed by the number of zones and the number of DNS queries. Prices change, so use the pricing pages in "Sources". Do the lab in one sitting and delete both resources in "Clean up". If you must stop halfway, delete the endpoint first. The budget you created earlier only sends alerts. They do not stop anything.
- Lockout. The last section turns off public network access on the storage account. After that, nothing on the public internet can reach the share, including your own PC. Only clients that use the private endpoint can. Do not start the last section until the VM has mounted the share over the private address (the mount and test-file steps). If something goes wrong, the way back is: **Storage account** > **Networking** > **Public network access** > **Manage** > **Enabled from all networks**. Nothing is deleted. More in "The most common mistake".
- Use only the storage account from the Azure Files lab. Do not do this on an account that holds anything you need.
- If you ever do this in a real tenant, ask the team that owns DNS first. A private DNS zone changes how a name resolves for everything in the linked network.
- Azure already requires multifactor authentication (MFA) for Azure management work. If you are asked for it, that is expected.

## What the lab builds

![The VM in snet-vm asks the private DNS zone for the file share name, and the zone answers with a 10.10.2.x address. The VM mounts the share over SMB port 445 through the private endpoint in snet-pe, which links to the storage account. Public internet access is blocked.](/img/basics/private-endpoint-dns.svg)

*Source: Microsoft Learn pages listed under Sources.*

## Steps in the Azure portal

### See what the name resolves to today

DNS (the Domain Name System) turns a name into an IP address. Your storage account has a name like `<account>.file.core.windows.net`. Before you change anything, look at what that name gives you from inside the VM.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the subscription name.
2. Start the VM: **Virtual machines** > `vm-azb-win01` > **Start**. Wait until the status says **Running** (two to three minutes).
3. Connect to the VM. Follow "Connect again later" in the [Windows VM lab](/azure-basics-labs/windows-vm-entra-sign-in/): look up your public IP address again, add `allow-rdp-my-ip` to `nsg-azb-vm` for that address only, connect with your route from the [Remote Desktop clients lab](/azure-basics-labs/your-pc-and-remote-desktop-clients/) (A: PC already in your tenant, B: personal PC that you registered, C: web account setting and the `hosts` line), and sign in as `testuser1`. You need `testuser1` here because the mount step later uses that user.
4. On the VM, open PowerShell and run this. Replace `<account>` with your storage account name (`stazb` and five digits).

```powershell
nslookup <account>.file.core.windows.net
```

5. Write down the address in the answer. It is a public address, not one that starts with `10.`, and the name in the answer does not contain `privatelink`. This is the baseline.

### A second subnet for the private endpoint

**Idea 1: a private endpoint is a network card with a private address.** A private endpoint is a network interface that Azure places in your subnet. It gets an address from the subnet's range (for example `10.10.2.4`), and it is linked to one service, here the file service of your storage account. A VM that talks to that address reaches the service over Azure's network and not over the public internet. The private endpoint must be in the same region as the virtual network. The storage account itself can be in a different region.

Put the endpoint in its own subnet, `snet-pe`. It keeps the endpoint's network policy setting away from the VM's subnet. Network policy for private endpoints is a subnet setting, and this lab leaves it as it is. Network security group rules apply to a private endpoint only when that setting is enabled on the endpoint's subnet. The network security group you attached to `snet-vm` is on a different subnet, so it is not involved.

6. In the portal search box, enter **Virtual networks** and open `vnet-azb`.
7. Under **Settings**, select **Subnets**, then select **+ Subnet** (the button may read **+ Add subnet**).
8. Set **Name** to `snet-pe`. Set the starting address to `10.10.2.0` and the size to `/24`. Leave everything else as offered. Select **Save** (or **Add**).

Check: **Subnets** now lists `snet-vm` (`10.10.1.0/24`) and `snet-pe` (`10.10.2.0/24`).

### The private endpoint, with its DNS zone

**Idea 2: the name stays the same, the answer changes.** You keep using `<account>.file.core.windows.net`. Inside your virtual network, a private DNS zone called `privatelink.file.core.windows.net` answers that name with the private address of the endpoint. Outside, the same name gives the public address. A private DNS zone is a DNS zone that only the virtual networks linked to it can see. You mount the share with the original name, not the `privatelink` name. The portal wizard creates the zone (or reuses a matching one), links it to the virtual network and adds the record. This is called automatic DNS integration.

9. In the portal search box, enter **Private endpoints**. Select **Private endpoints**, then **+ Create**.
10. **Basics** tab: choose your subscription and set **Resource group** to `rg-azb-lab`. Set **Name** to `pe-azb-file`. Leave the network interface name as offered. Set **Region** to the same region as `vnet-azb`. Select **Next: Resource**.
11. **Resource** tab: set **Resource type** to `Microsoft.Storage/storageAccounts`. Set **Resource** to your storage account from the Azure Files lab. Set **Target sub-resource** to `file`. This picks the file service of the account. Select **Next: Virtual Network**. If the tab asks for a connection method first, choose the option that connects to an Azure resource in your directory.
12. **Virtual Network** tab: set **Virtual network** to `vnet-azb` and **Subnet** to `snet-pe`. Leave the IP address on dynamic. Leave the network policy and application security group settings as they are. Select **Next: DNS**.
13. **DNS** tab: check that integration with a private DNS zone is turned on, and that the zone listed is `privatelink.file.core.windows.net`, in subscription and resource group `rg-azb-lab`. Select **Next: Tags**, then **Next: Review + create**, then **Create**.

Check: when the deployment finishes, open `pe-azb-file`. Its connection status is **Approved**. Open the private DNS zone `privatelink.file.core.windows.net` in `rg-azb-lab`. Find the list of records (it can be called **Recordsets** or sit under **DNS Management**): you see an A record named after your storage account, with a `10.10.2.x` address. Find the list of virtual network links: you see `vnet-azb`.

### See the private address from the VM

14. Back on the VM, run the same command as before.

```powershell
nslookup <account>.file.core.windows.net
```

You should now see something like this. This is an example with sample names and an address.

```output
Server:  UnKnown
Address:  168.63.129.16

Non-authoritative answer:
Name:    <account>.privatelink.file.core.windows.net
Address:  10.10.2.4
Aliases:  <account>.file.core.windows.net
```

Read it from the bottom. You asked for `<account>.file.core.windows.net`. That is listed under `Aliases`. It is another name (a CNAME) for `<account>.privatelink.file.core.windows.net`, and the private zone answered that with a `10.10.2.x` address from `snet-pe`. The `168.63.129.16` line is Azure's own DNS service, which every VM in a virtual network with default DNS uses.

If you see `Address: 20.x.x.x` (a public address) and no `Aliases` line, the zone link or the zone name is wrong. Do not go on. Read "The most common mistake".

15. Run `nslookup` for the same name on your own PC, outside Azure. You get the public address, because your PC is not on the private network. That is the second answer from Idea 2.

### Mount the share over the private address

Mounting needs the same sign-in as in the Azure Files lab: you are signed in to the VM as `testuser1` and the share is reached with Microsoft Entra Kerberos. Because that lab used Microsoft Entra Kerberos, the manifest change in the next step is required. Without it the mount asks for credentials and then rejects them (error 1326), because a Kerberos ticket cannot be issued for the private link name.

16. Add the private link name to the storage account's Microsoft Entra application. Do this as an administrator, in the Microsoft Entra admin center on your own PC, not as `testuser1` on the VM.
    1. Go to **App registrations** > **All applications**, and open the application named `[Storage Account] <account>.file.core.windows.net`.
    2. Select **Manifest**. Copy the existing text somewhere safe as a backup.
    3. In `identifierUris`, for every `<account>.file.core.windows.net` entry add a matching `<account>.privatelink.file.core.windows.net` entry. Select **Save**.

    Check: the manifest saves with no error, and `identifierUris` now holds both names.
17. On the VM, check that the SMB port answers. SMB (Server Message Block) is the protocol Windows uses for file shares, and it uses TCP port 445. `Test-NetConnection` is the check.

```powershell
Test-NetConnection -ComputerName <account>.file.core.windows.net -Port 445
```

`TcpTestSucceeded : True` and a `RemoteAddress` of `10.10.2.x` mean the VM reached the private endpoint.

18. If the share is still mounted from the Azure Files lab, disconnect it first. File shares connected through the public endpoint must be remounted. In File Explorer, right-click the drive and select **Disconnect**, or run `net use Z: /delete` (use your drive letter).
19. Mount the share again the way you did in the Azure Files lab, as `testuser1`. Use `\\<account>.file.core.windows.net\azbshare`, with the original name and not the `privatelink` name. If you get error 1326, the manifest change is missing or not saved.
20. Create a small test file in the share, for example `private-test.txt`.

Check: the share opens and the test file is there.

### Close the public door

**Idea 3: two doors.** A storage account has a public door and, now, a private one. They are separate. Disabling public network access means clients cannot connect through the public endpoint, and clients can still connect through private endpoints. It does not restrict outbound traffic from the clients.

Stop here and look at this checklist before you go on.

- You saw a `10.10.2.x` answer from the VM.
- The VM mounted the share and wrote a test file.
- You know the way back: **Storage account** > **Networking** > **Public network access** > **Manage** > **Enabled from all networks**. Nothing is deleted.

21. In the portal, open your storage account.
22. In the left menu, under **Security + networking**, select **Networking**.
23. Under **Public network access**, select **Manage**.
24. Choose **Disabled** (the wording may differ), confirm any prompt, then **Save**. Success: the page says **Disabled**. If you cannot find this setting in your portal version, use the CLI command in the CLI section instead.
25. On the VM, open the share again, read the test file and write a second file, `private-test-2.txt`. Both should work. If the share was already open, disconnect and mount it again to be sure.
26. On your own PC, run `nslookup <account>.file.core.windows.net`. It still gives a public address. Then open the storage account in the portal and go to **Classic file shares** > `azbshare`. You should see an access or network error. A failure here is expected. Your PC could never have mounted this share, and many home networks block port 445 anyway, so do not use the PC as the real test. The VM test above is the real test.

Check: the VM can read and write, and the portal cannot browse the share from your PC.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash). Skip them if you did the portal steps. Do the first five portal steps (in "See what the name resolves to today") first: start the VM, connect, and run `nslookup` on the VM. Check the subscription, then set the variables. Run `echo "$SA"` before you use it. If Cloud Shell restarts, set the variables again.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
RG=rg-azb-lab
VNET=vnet-azb
SUBNET_PE=snet-pe
PE=pe-azb-file
ZONE=privatelink.file.core.windows.net
SA=stazb48213              # replace 48213 with the five digits of your storage account
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

Create the private endpoint for the `file` sub-resource. The sub-resource is called the group ID.

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

You should see `Approved`, the link `link-vnet-azb`, and an A record named after the storage account. Then do "See the private address from the VM" and "Mount the share over the private address" from the portal steps on the VM, including the Microsoft Entra manifest change.

Only when the VM has mounted the share over the private address, turn off public network access.

```bash
az storage account update \
  --resource-group $RG \
  --name $SA \
  --public-network-access Disabled \
  --output none

az storage account show --resource-group $RG --name $SA --query publicNetworkAccess -o tsv
```

The last command should print `Disabled`. Then repeat the VM test and the PC test from the portal steps.

## Terraform

No Terraform in this lab. Use the portal or the CLI here. If you want the Terraform version later, take the introduction in the [Terraform basics lab](/azure-basics-labs/terraform-basics/) and the provider documentation for the private endpoint resource.

## Check that it works

- From the VM, `nslookup <account>.file.core.windows.net` shows a `10.10.2.x` address, and lists the `privatelink` name.
- From your own PC, the same command shows a public address.
- `pe-azb-file` shows a connection status of **Approved**.
- The private DNS zone `privatelink.file.core.windows.net` has a link to `vnet-azb` and an A record for the storage account.
- With public network access disabled, the VM can still read and write the share, and your PC cannot reach it.

## The most common mistake

Two mistakes, in the order you are likely to hit them.

**The name still resolves to the public address.** The usual causes:

- The private DNS zone is not linked to `vnet-azb`. Check **Virtual network links** on the zone.
- The zone name is wrong. The automatic DNS records are created only if you use the recommended zone name. For Azure Files it is exactly `privatelink.file.core.windows.net`.
- The VM does not use Azure's DNS. If someone changed the DNS servers of `vnet-azb` away from **Default (Azure-provided)**, the VM asks another server, and that server does not know the private zone. The virtual network lab left this setting alone.
- You tested from your own PC and not from the VM. Run `nslookup` on the VM.

If you turned off public access while the name still pointed to the public address, the VM now fails to mount the share. Do not panic. Nothing is deleted.

**Locking yourself out.** Public network access is off, the VM cannot reach the share, and you cannot browse it from your PC either. The setting is a property of the storage account, so you can change it back from the portal or the CLI. In the portal, go to the storage account, **Security + networking** > **Networking**, and under **Public network access** select **Manage**, then choose **Enabled from all networks** (the wording may read **Enable**). With the CLI (replace `stazb48213` with the name of your own account):

```bash
az storage account update --resource-group rg-azb-lab --name stazb48213 --public-network-access Enabled
```

Then fix the DNS problem and try again.

## Clean up

Do this the same day. The private endpoint and the DNS zone cost money while they exist, so do not leave them running. Delete in this order:

1. Re-enable public network access on the storage account (the portal way back from the last section, or the CLI command in the section above). Skip this step if you are going straight to the cleanup lab, which deletes the account. You can also keep it closed, but then you can only reach the share from inside `vnet-azb`.
2. Delete the private endpoint `pe-azb-file`. Portal: open the private endpoint, select **Delete**. The DNS records in its DNS zone group are deleted too.
3. Delete the virtual network link from the private DNS zone. Portal: open the zone, find the list of virtual network links, select the link, **Delete**.
4. Delete the private DNS zone `privatelink.file.core.windows.net`.
5. Delete the subnet `snet-pe` from `vnet-azb`. It held the private endpoint and is empty now. Portal: open `vnet-azb` > **Subnets**, select `snet-pe` and select **Delete**.

The same in the CLI. Set the variables from the CLI section again first (`RG`, `VNET`, `SUBNET_PE`, `PE`, `ZONE`, `SA`):

```bash
az storage account update --resource-group $RG --name $SA --public-network-access Enabled --output none
az network private-endpoint delete --resource-group $RG --name $PE
az network private-dns link vnet delete --resource-group $RG --zone-name $ZONE --name link-vnet-azb --yes
az network private-dns zone delete --resource-group $RG --name $ZONE --yes
az network vnet subnet delete --resource-group $RG --vnet-name $VNET --name $SUBNET_PE
```

If you made the zone link in the portal, the link may have a different name. List the links with `az network private-dns link vnet list --resource-group $RG --zone-name $ZONE -o table` first.

Check: `az network private-endpoint list --resource-group $RG -o table` is empty, and `az network private-dns zone list --resource-group $RG -o table` no longer lists the zone.

6. Sign out of the VM (do not just lock it). Then delete the RDP rule: open `nsg-azb-vm` > **Inbound security rules**, tick `allow-rdp-my-ip`, **Delete**.
7. Stop the VM: `vm-azb-win01` > **Stop**. Read the status. It must say **Stopped (deallocated)**.

End state: VM Stopped (deallocated), no `allow-rdp-my-ip` rule.

The public IP `pip-azb-win01` is still there, and no private endpoint or private DNS zone is left. Keep for later labs: `rg-azb-lab`, `vnet-azb`, `snet-vm`, the VM `vm-azb-win01` and the storage account with its file share `azbshare`. Remount the share on the VM next time, because the name resolves to the public address again. The Kerberos client setting on the VM (`CloudKerberosTicketRetrievalEnabled`) and the `[Storage Account]` app in Entra are unchanged from the Azure Files lab. If you added `privatelink` names to that app, they do no harm. [When something breaks](/azure-basics-labs/when-something-breaks/) deletes the storage account and tells you to check that app.

## Where this is used in AVD

Azure Virtual Desktop session hosts usually keep user profiles (FSLogix profile containers) on an Azure Files share, and many companies close that storage account to the public internet and reach it through a private endpoint and a private DNS zone, exactly as you did here. In AVD, a missing private DNS link looks like the wrong answer you can see in "See the private address from the VM": the name resolves to a public address.

See [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/) for the storage choices, and [Required Connectivity for Azure Virtual Desktop: Endpoints, Proxies, DNS and Private Link](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) for how DNS and Private Link fit into the wider network.

## Next lab

[When something breaks](/azure-basics-labs/when-something-breaks/) puts the checks from this series together, so you can work out what went wrong when a step fails.

## Sources

- [Configure network endpoints for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-networking-endpoints)
- [Azure Private Endpoint private DNS zone values](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns)
- [Troubleshoot Azure Files identity-based authentication and authorization issues (SMB)](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-storage/files/security/files-troubleshoot-smb-authentication)
