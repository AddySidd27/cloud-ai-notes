---
title: "Windows VM with Microsoft Entra Sign-In"
seoTitle: "Azure Windows VM with Entra ID Sign-In: Beginner Lab"
layout: post.njk
permalink: "/azure-basics-labs/windows-vm-entra-sign-in/"
order: 322
tags: [azure-basics-lab]
deck: "You create a small Windows Server VM in your own subnet, give the TestUsers group the right to sign in, and connect with your test user's Microsoft Entra account."
description: "Beginner Azure lab: create a Windows Server 2025 VM, turn on Microsoft Entra sign-in, give a group the Virtual Machine User Login role and connect with RDP."
---

By the end of this lab you will have a small Windows Server VM named `vm-azb-win01` in `snet-vm`. Your test user `testuser1` will sign in to it over Remote Desktop with a Microsoft Entra account, not with a local password. You will then remove the temporary RDP rule and decide whether to keep the VM or delete it.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

A virtual machine (VM) is a computer that runs inside Azure. You rent it by the hour, and you pay for it while it exists in a running state. This is the first lab in the series that costs real money, so read "Safety first" before you click anything.

## What you need

- [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): the throwaway account. A free account has a $200 credit for 30 days.
- [Lab 3: Resource group, tags and budget](/azure-basics-labs/resource-group-tags-budget/): the budget from that lab sends alerts. It does not stop anything.
- [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the user `testuser1` and the group `TestUsers`, with `testuser1` as a member. You need the user's sign-in name and password.
- [Lab 5: Multifactor authentication](/azure-basics-labs/mfa/): per-user MFA must still show **Disabled** for every user.
- [Lab 6: Conditional Access](/azure-basics-labs/conditional-access/): the policy from that lab targets other apps and should be off or deleted. If you left any Conditional Access policy on that requires MFA, read the error table under "The most common mistake" first.
- [Lab 7: RBAC roles](/azure-basics-labs/rbac-roles/): how a role, a scope and a person fit together.
- [Lab 8: Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/) and [Lab 9: Network security group](/azure-basics-labs/network-security-group/): `vnet-azb`, `snet-vm` and `nsg-azb-vm` in `rg-azb-lab`. A network security group (NSG) is the list of allow and deny rules on the subnet. The RDP rule from Lab 9 is gone. You add it again in this lab.
- [Lab 11: Your PC and Remote Desktop clients](/azure-basics-labs/your-pc-and-remote-desktop-clients/): a Windows 10 or Windows 11 PC and the result you wrote down there: A (PC already known to your tenant), B (any other PC) or C (personal PC that you register). Part 6 uses it.
- [Lab 2: Cloud Shell and the Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) if you use the CLI steps. Azure CLI 2.76 or newer.
- Time: about 60 minutes in one sitting. Cost: a VM, a disk and a public IP address, billed while they exist. Look up the hourly price for your region and size in the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) and write it down before you create anything.
- Role: Owner on the subscription of your throwaway account. Creating the VM needs it, and so does assigning a role. Learn says assigning roles needs `Microsoft.Authorization/roleAssignments/write`, which Owner has.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top right of the portal before you change anything.
- A running VM costs money. Learn lists the power states: **Running** and **Stopped** are billed. **Stopped (deallocated)** is not billed for compute, but disks and networking still are.
- Time-box it. Do this lab in one sitting. Before you close the laptop, either delete the VM or deallocate it. Put a reminder in your calendar for the end of the session.
- A budget only sends an alert. It never stops a VM. You have to stop it.
- Never use `Any` or `*` as the source for port 3389. The rule you add is for your own IP address only, and you remove it before you finish.
- The public IP address is temporary. Do not leave a VM with a public IP and an open RDP rule overnight.
- Give `testuser1` the role **Virtual Machine User Login**, not Owner and not Virtual Machine Administrator Login. Learn says Owner or Contributor alone does not allow sign-in anyway.
- Do not turn on any option that enrols the VM in Intune or mobile device management (MDM). Learn says Windows Server VMs do not support MDM enrolment.
- Leave per-user MFA at **Disabled**. Learn lists a per-user **Enabled** or **Enforced** setting as a cause of a failed sign-in to an Entra VM. See "The most common mistake".
- Pick one region and use it everywhere. The VM must be in the same region as `vnet-azb`.

## What the lab builds

![A left-to-right diagram. Your PC connects over RDP through a temporary public IP address and the network security group nsg-azb-vm to the Windows Server VM vm-azb-win01 in the subnet snet-vm. The VM has a system-assigned managed identity and the Microsoft Entra sign-in extension. The group TestUsers holds the role Virtual Machine User Login at the scope of the resource group rg-azb-lab.](/img/basics/windows-vm-entra-sign-in.svg)

*Source: [Sign in to a Windows virtual machine in Azure by using Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-windows), [Quickstart: Create a Windows virtual machine in the Azure portal](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-portal) and [Check vCPU quotas](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Part 1: Check quota, size and image

Before you create a VM, check that your subscription is allowed to. Learn says vCPU quota has two tiers for each region: a total regional limit, and a limit for each VM size family. A new VM must fit inside both. Learn also says quota counts cores in use whether the VM is running or deallocated. Quota is separate from capacity: even with quota, a region can run out of a certain size.

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name at the top right.
2. In the search box, enter **Quotas** and select **Quotas**. Select **My quotas**. Learn says you can filter by provider, location and subscription. Set the provider filter to **Compute**, and filter to your region and your subscription.
3. Find the row for **Total Regional vCPUs** and the row for the B-series family (the name differs a little between regions). For each, read the usage and the limit. You need 2 free vCPUs in both. If the limit is 0 or the room is used up, pick another size in Part 2 or ask for an increase on the same page. Do not change region: the VM has to sit next to `vnet-azb`.

**The size.** This lab uses `Standard_B2s_v2`: 2 vCPUs and 8 GiB of memory. Learn's Bsv2-series page lists it, with no local temporary disk, and says the series supports Premium SSD and Generation 2 VMs. Learn describes the B-series as burstable: it collects CPU credits while it is quiet and spends them when it is busy, and it is meant for small test and development servers. That fits a sign-in test. If the portal does not offer this size for your region or subscription, choose another size with 2 vCPUs and at least 4 GiB of memory, and keep it small.

**The image.** This lab uses **Windows Server 2025 Datacenter: Azure Edition**. Its image name is `MicrosoftWindowsServer:WindowsServer:2025-datacenter-azure-edition:latest`. Learn's own Windows VM quickstart uses the 2022 edition of the same image family. This lab uses 2025 on purpose: Learn's Azure Files page lists Windows 11 and Windows Server 2025, but not Windows Server 2022, for cloud-only users, and [Lab 14: Storage account and Azure Files](/azure-basics-labs/storage-azure-files/) needs that. Learn says Entra sign-in works on Windows Server 2022 or 2025 installed with Desktop Experience, so do not pick an image with **Core** in its name. There is a licence reason for picking a server image too:

- Windows 11 Enterprise multi-session is for Azure Virtual Desktop only. Learn says Microsoft does not allow it to run in production outside the Azure Virtual Desktop service.
- Other Windows 11 images need a qualifying licence for any production use in Azure, for example Microsoft 365 E3, E5 or Business Premium, or Windows Enterprise E3 or E5. Learn says Free Trial and Student accounts can deploy Windows 11 images for development and testing.
- A Windows Server image has no such question for a short test. Leave the box for an existing Windows Server licence (Azure Hybrid Benefit) unticked. It needs Software Assurance, and you do not have it.

The trade-off: it is a server, not the Windows 11 desktop your AVD users will see. For the question "can an Entra user sign in to this VM", it behaves the same.

### Part 2: Create the VM

**Idea 1: two separate things must be true.** To sign in with Entra, the VM has to trust Entra, and Azure has to say you may. The first part is a small add-on to the VM, the "Microsoft Entra sign-in extension" (named `AADLoginForWindows`). Installing it joins the VM to Entra. Learn says the VM needs a system-assigned managed identity first. A managed identity is an Azure-managed account that belongs to the VM itself, and the extension uses it to talk to Entra. The second part is a role. Learn names two: **Virtual Machine User Login** (a normal user) and **Virtual Machine Administrator Login** (an admin). Learn says Owner or Contributor does not give sign-in rights, on purpose: the people who manage VMs and the people who log in to them are kept apart. Learn also says that once the VM is Entra joined, you cannot join it to a normal domain. If you ever need that, you remove the extension first.

4. In the search box, enter **Virtual machines** and select **Virtual machines**. Select **Create**, then **Azure virtual machine**.
5. On the **Basics** tab, set:
   - Subscription: your throwaway subscription.
   - Resource group: `rg-azb-lab`.
   - Virtual machine name: `vm-azb-win01`. Learn says the portal uses this value for both the Azure resource name and the Windows computer name, and that a Windows computer name can be at most 15 characters. This one has 12.
   - Region: the same region as `vnet-azb`.
   - Image: **Windows Server 2025 Datacenter: Azure Edition** (select **See all images** if it is not in the list). Pick the one without **Core** in its name.
   - Size: select **See all sizes** and choose `Standard_B2s_v2`, or the small size you picked in Part 1.
6. Under **Administrator account**, enter the user name `azureuser` and a password. Learn says the password must be at least 12 characters and meet the complexity rules. This is a local emergency account. Save it in your password manager. You do not use it to sign in as `testuser1`.
7. Under **Inbound port rules**, set **Public inbound ports** to **None**. Learn's quickstart chooses **Allow selected ports** here, but you do not want that: the RDP rule goes on your subnet's NSG in Part 5, not on the VM.
8. Select **Next: Disks**. Leave the defaults. Learn says the OS disk is set to **Delete with VM** by default. Keep that.

### Part 3: Network and identity settings on the same page

**Idea 2: the public IP address is for two jobs.** First, it is the door you come in by, for a short time. Second, it gives the VM a way out to the internet. Learn says a VM with a public IP address assigned to it has an explicit outbound path. This matters here. Lab 8 told you that new subnets are private by default, so the VM has no outbound path of its own. Learn says Windows activation and Windows updates do not work in a private subnet without an explicit outbound method. The Entra extension also needs outbound HTTPS (port 443). Learn lists four endpoints: `enterpriseregistration.windows.net`, `login.microsoftonline.com`, `pas.windows.net` and the Azure metadata address `169.254.169.254`. The Standard public IP in this lab gives it that path. A Standard public IP is secure by default. It accepts no inbound traffic until an NSG allows it, and your subnet NSG allows only what you add.

9. Select **Next: Networking**. Set:
   - Virtual network: `vnet-azb`.
   - Subnet: `snet-vm`.
   - Public IP: **Create new**. If the form asks for an SKU, choose **Standard**. Give it the name `pip-azb-win01`.
   - NIC network security group: **None**. The subnet already has `nsg-azb-vm`. One NSG at the subnet keeps the rules in one place, as in Lab 9.
   - Tick **Delete public IP and NIC when VM is deleted**. Learn lists this option on the Networking tab.
10. Select **Next: Management**. Set:
    - Under **Identity**, tick **Enable system assigned managed identity**.
    - Look for the option **Login with Microsoft Entra ID** and tick it. It installs the extension. Learn's Bastion page names this option. If you cannot find it, skip it. The Check below shows how to add the extension afterwards.
    - If you see any option to enrol the VM in Intune or MDM, leave it off.
    - Auto-shutdown: tick **Enable auto-shutdown**, choose a time later today and your time zone (UTC is the default). Learn's quickstart uses this setting. It is a safety net, not a replacement for deleting the VM. Learn does not say which power state the VM ends in, so the next day check that the status reads **Stopped (deallocated)** (Lab 13 explains why).
11. Select **Review + create**. Read the price shown for the VM. When you see **Validation passed**, select **Create**. Wait for the deployment, then select **Go to resource**.

Check: on the VM page, open **Identity** and see that **System assigned** is **On**. Open **Extensions + applications** and see `AADLoginForWindows` with **Provisioning succeeded**. If the extension is missing, add it: **+ Add**, search for **AADLoginForWindows**, then **Review + create** and **Create**. If it failed, go to "The most common mistake".

### Part 4: Let the group sign in

12. Open the resource group `rg-azb-lab`. Select **Access control (IAM)**.
13. Select **Add**, then **Add role assignment**.
14. On the **Role** tab, search for **Virtual Machine User Login** and select it. Select **Next**.
15. On **Members**, set **Assign access to** to **User, group, or service principal**. Select **+ Select members**, search for `TestUsers`, select the group and choose **Select**.
16. Select **Review + assign**, then **Review + assign** again.

Why the group and why this scope: Lab 7 says to give roles to groups, not people, and to give them at the smallest scope that works. The resource group holds only the VM and its network parts for this series, so it is a small scope. A role given on the resource group applies to everything in it, including the VM. A new role assignment can take a few minutes to apply, so wait a few minutes before you test.

Check: on the resource group's **Access control (IAM)**, open **Role assignments** and find `TestUsers` with **Virtual Machine User Login**, scope **This resource**. If `testuser1` is not in `TestUsers`, add the user now (Lab 4).

### Part 5: Open RDP for your own IP, for now

RDP is Remote Desktop Protocol, the way Windows lets you use a computer's screen over a network. It listens on TCP port 3389.

17. Find your public IP address with a browser search for "what is my IP". Check it again right now. If you use a VPN, the VPN's address is the one that counts.
18. Open `nsg-azb-vm`, select **Inbound security rules**, then **+ Add**. Set Source **IP Addresses**, source IP address your own address, source port ranges `*`, Destination **Any**, Service **RDP**, Action **Allow**, Priority `1000`, Name `allow-rdp-my-ip`. Select **Add**. This is the same rule as Lab 9.

Check: the rule shows your single IP address as the source. It does not say `Any`.

### Part 6: Connect as the test user

**Idea 3: not every PC can connect.** Learn says remote connections to a VM that is joined to Entra are allowed only from Windows 10 or later PCs that are Microsoft Entra registered (build 20H1 or later), Entra joined, or Entra hybrid joined to the same directory as the VM. "Registered" is what you get when you add a work or school account on a PC in **Settings** > **Accounts** > **Access work or school**. If the PC is only registered, Learn says you must type the user name as `AzureAD\` followed by the full sign-in name, for example `AzureAD\testuser1@yourtenant.onmicrosoft.com`. Learn gives a second way for any other PC: the setting **Use a web account to sign in to the remote computer** in Remote Desktop Connection, which does not need the PC to be registered or joined. Use your result from Lab 11.

19. Check your Lab 11 result.
    - **A or C.** Open **Settings** > **Accounts** > **Access work or school** and check that the account for your throwaway tenant is listed. If you are in case C and it is not, select **Connect**, and sign in with `testuser1` or your admin account of the test tenant. Do not choose **Join this device to Microsoft Entra ID**. A registered PC is enough, and joining is a bigger change. If a prompt offers to let the organisation manage the device, stop and use the case B steps instead.
    - **B.** Do not change your PC. You use the web account setting in step 23, described there.
20. Open a private browser window (InPrivate in Edge, Incognito in Chrome). Go to `https://portal.azure.com` and sign in as `testuser1`. Learn says a temporary password cannot be used for a remote desktop sign-in. If the page asks you to change the password, set a new one and save it. If MFA is registered from Lab 5, approve the request. Close the private window.
21. (Cases A and C. In case B, go to step 23.) In your admin window, open the VM. Select **Connect**. On the **Connect** page, select **Native RDP**. Learn says it is the top method by default, and that you may need to select **More ways to connect** first. Keep the default IP address and port 3389, then select **Download RDP File**. Learn says to ignore the warning that the file might harm your device. This file comes from your own portal, so it is the case where opening it is right.
22. Open the downloaded file. If you are in case A or C, select **Connect** and go on to step 23. Learn says an "unknown publisher" warning is expected. On a PC with the April 2026 security update, the dialog may show a caution banner for an unknown remote connection instead. Check that the address shown is your VM's public IP address, leave every resource box unticked, and continue. Later, Windows may ask you to confirm the identity of the VM. Select **Yes**.
23. Sign in.
    - **A or C (registered or joined PC).** When Windows asks for credentials and does not sign you in by itself, select **More choices**, then **Use a different account**. Enter `AzureAD\testuser1@yourtenant.onmicrosoft.com` and the new password. Use your real domain.
    - **B (any other PC).** Do not use the downloaded file for this. The web account setting needs the VM's name, not its IP address, and Learn says the name must match the VM's host name in Entra ID and resolve to the VM's IP address. A simple way is a line in the `hosts` file on your PC that maps `vm-azb-win01` to the VM's public IP address. Learn mentions a HOSTS entry for a name mismatch, but gives no click path, so look up how to edit the `hosts` file on your Windows version, and remove the line when you finish. Then open **Remote Desktop Connection**, select **Show Options**, open the **Advanced** tab and tick **Use a web account to sign in to the remote computer**. On the **General** tab type `vm-azb-win01` as the computer and select **Connect**. When asked for credentials, enter your user name in the form `testuser1@yourtenant.onmicrosoft.com`. Learn says you are then asked to allow the connection to a new PC. Select **Yes**. If your employer blocks changes to the `hosts` file, stop here and do this lab from a personal PC.
24. Wait for the desktop. The first sign-in takes a while.

Check: inside the VM, open PowerShell and run `dsregcmd /status`. Learn says the goal is `AzureAdJoined : YES`, and `AzureAdPrt : YES` for the single sign-on state. Then sign out of the VM from the Start menu. Learn says the Windows lock screen does not support Entra tokens in a remote session, so a locked session is disconnected. Sign out instead of locking. In your admin window, open the Entra admin center and **Identity** > **Monitoring & health** > **Sign-in logs**. Find the sign-in to the app **Microsoft Azure Windows Virtual Machine Sign-in** (some tenants show **Azure Windows VM Sign-in**).

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from Lab 2. Check the subscription first. Azure already requires MFA for create, update and delete from the CLI, so your sign-in from Lab 2 covers it. Set the variables. Use your own values.

```bash
RG=rg-azb-lab
VNET=vnet-azb
SUBNET=snet-vm
NSG=nsg-azb-vm
VM=vm-azb-win01
PIP=pip-azb-win01
SIZE=Standard_B2s_v2
IMAGE=MicrosoftWindowsServer:WindowsServer:2025-datacenter-azure-edition:latest
LOCATION=$(az network vnet show --resource-group $RG --name $VNET --query location --output tsv)
MYIP=203.0.113.25        # your public IP, found with a browser search
echo "$LOCATION"
read -s -p "Local admin password for azureuser (12 or more characters): " ADMINPW; echo
```

Check the quota in your region. Look for **Total Regional vCPUs** and the B-series row, and compare `currentValue` with `limit`.

```bash
az vm list-usage --location $LOCATION --output table
```

Check that the size is offered in your region.

```bash
az vm list-skus --location $LOCATION --resource-type virtualMachines \
    --query "[?name=='$SIZE'].{name:name, restrictions:restrictions}" --output json
```

Create the VM. The variable `ADMINPW` holds the password you typed above, so it is not written into the command. `--nsg ""` means no NSG on the network card, because the subnet has one. `--assign-identity '[system]'` turns on the system-assigned managed identity. Learn says the computer name defaults to the VM name, so the Windows computer name is `vm-azb-win01` here too.

```bash
az vm create \
    --resource-group $RG \
    --name $VM \
    --image $IMAGE \
    --size $SIZE \
    --admin-username azureuser \
    --admin-password "$ADMINPW" \
    --vnet-name $VNET \
    --subnet $SUBNET \
    --nsg "" \
    --public-ip-address $PIP \
    --public-ip-sku Standard \
    --assign-identity '[system]' \
    --os-disk-delete-option Delete \
    --nic-delete-option Delete
```

Install the Microsoft Entra sign-in extension. The portal option in Part 3 does this for you. The CLI does not, so run it here.

```bash
az vm extension set \
    --publisher Microsoft.Azure.ActiveDirectory \
    --name AADLoginForWindows \
    --resource-group $RG \
    --vm-name $VM
```

Give the group `TestUsers` the role at the resource group scope.

```bash
GROUP_ID=$(az ad group show --group TestUsers --query id --output tsv)
RG_ID=$(az group show --name $RG --query id --output tsv)

az role assignment create \
    --assignee-object-id $GROUP_ID \
    --assignee-principal-type Group \
    --role "Virtual Machine User Login" \
    --scope $RG_ID
```

Add the temporary RDP rule for your own IP, as in Lab 9.

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

Optional safety net: switch the VM off every day at a set time (Learn's reference example uses `1730`). Learn says the time zone is UTC by default. The command does not set one, so `1900` means 19:00 UTC.

```bash
az vm auto-shutdown --resource-group $RG --name $VM --time 1900
```

Check: the extension is listed, the role is assigned, and the rule shows your IP.

```bash
az vm extension list --resource-group $RG --vm-name $VM --output table
az role assignment list --scope $RG_ID --role "Virtual Machine User Login" --output table
az network nsg rule list --resource-group $RG --nsg-name $NSG --output table
az vm show --resource-group $RG --name $VM --show-details --query publicIps --output tsv
```

Then connect as in Part 6 of the portal steps, using your Lab 11 result: download the RDP file from the portal and sign in as `AzureAD\testuser1@yourtenant.onmicrosoft.com` (cases A and C), or use the web account setting (case B).

## Terraform

No Terraform in this lab. The VM lives for about an hour, with a temporary public IP and a temporary rule, and a sign-in test is quicker by hand. The extension, the managed identity and the role assignment would each be separate resources, and I have not validated that code. If you want a repeatable VM build with Terraform, see [the AVD quick lab](/terraform-labs/avd-quick-lab/). Lab 10 has the Terraform basics.

## Check that it works

- `vm-azb-win01` is in `rg-azb-lab`, in the same region as `vnet-azb`, in the subnet `snet-vm`.
- **Identity** shows system assigned **On**, and `AADLoginForWindows` shows **Provisioning succeeded**.
- `TestUsers` has **Virtual Machine User Login** at the resource group, and nobody got Owner for this lab.
- `testuser1` signed in over RDP with the Entra account, and `dsregcmd /status` shows `AzureAdJoined : YES`.
- The sign-in log shows the sign-in to the Windows VM sign-in app.
- Per-user MFA still shows **Disabled** for everyone.

## The most common mistake

Forgetting the role, or giving Owner instead of the sign-in role. You see this message when you connect: "Your account is configured to prevent you from using this device. For more info, contact your system administrator." Learn says to check that the user has **Virtual Machine Administrator Login** or **Virtual Machine User Login**. Owner or Contributor on the VM does not count. Add the role as in Part 4, wait a few minutes, and try again.

### Other errors you can hit

| What you see | Likely cause, from Learn | What to do |
|---|---|---|
| "The sign-in method you're trying to use isn't allowed. Try a different sign-in method or contact your system administrator." | Learn's VM sign-in page puts this message under "MFA sign-in method required": a Conditional Access policy requires MFA, and the PC that starts the connection does not use strong authentication such as Windows Hello. Learn's Azure Virtual Desktop MFA page also names this message when per-user MFA is on together with Conditional Access. | Check for a Conditional Access policy that requires MFA, and check the per-user MFA page from [Lab 5](/azure-basics-labs/mfa/). The policy from [Lab 6](/azure-basics-labs/conditional-access/) targets other apps, so it should not cause this. Learn says that if Windows Hello for Business is not an option, you can exclude the app **Microsoft Azure Windows Virtual Machine Sign-in** from a policy. Do that only in this throwaway tenant. |
| "Your credentials didn't work." | Several causes, as Learn lists them. A PC that is not joined or hybrid joined to the same directory (a registered PC must use `AzureAD\` and the sign-in name). A temporary password. The extension was removed after the join. Learn also calls this an MFA-related message: if a legacy per-user **Enabled** or **Enforced** MFA setting is set, removing it is the fix. | Sign in as the user in a private window and change the password. Check that per-user MFA shows **Disabled**. Check **Access work or school** on your PC, or use the web account setting. Check the extension is still there. |
| AADSTS293004: the target-device identifier in the request was not found in the tenant | The computer name you typed in Remote Desktop Connection does not match the VM's host name in Entra. Learn's example is a short name against a full domain name. | Use the short host name, `vm-azb-win01`, not a full domain name. |
| The extension shows a failed state | Learn says the VM needs a system-assigned managed identity, and outbound HTTPS to the four Microsoft addresses. A device with the same name may already exist in Entra. | Turn on the identity, then install the extension again. Check **Devices** in the Entra admin center for an old entry with the VM's name. |
| The RDP file cannot connect at all | The NSG rule is missing, has the wrong IP, or your IP changed. | Check the rule and your current public IP. |

A close second: a per-user MFA setting left over from Lab 5. Learn's sign-in page says that if you configured a legacy per-user **Enabled/Enforced** setting and you see "Your credentials didn't work", you can resolve it by removing the per-user setting. Learn's pages do not agree on which of the two messages a per-user setting shows, so treat both as a reason to look at that page.

## Clean up

Do the first part either way.

**Remove the RDP rule.**

Portal: open `nsg-azb-vm`, select **Inbound security rules**, tick `allow-rdp-my-ip`, select **Delete**, then **Yes**.

CLI:

```bash
az network nsg rule delete \
    --resource-group $RG \
    --nsg-name $NSG \
    --name allow-rdp-my-ip
```

Learn says removing a rule does not cut connections that are already open, so sign out of the VM first.

**If you are not continuing right now, delete the VM and the public IP.**

Portal: open the VM, select **Delete**, and confirm. Because you ticked the delete options, the disk and the network card go with it. Open **Public IP addresses**, find `pip-azb-win01`, and delete it if it is still there. Learn says a public IP can be deleted only when nothing uses it.

CLI:

```bash
az vm delete --resource-group $RG --name $VM --yes
az network public-ip delete --resource-group $RG --name $PIP
az resource list --resource-group $RG --output table
```

Check: the last command lists no VM, disk, network card or public IP. You may still see `vnet-azb` and `nsg-azb-vm`. If a device named `vm-azb-win01` is still in **Devices** in the Entra admin center, delete it before you build a VM with the same name. Learn says a device with the same name makes the join fail.

**If you are continuing to Labs 13 to 19, keep the VM and stop paying for compute.** Deallocate it. Learn says deallocated VMs do not incur compute charges, and that disks and networking still do. Do not just shut Windows down from inside: that leaves the VM in the billed **Stopped** state.

```bash
az vm deallocate --resource-group $RG --name $VM
```

In the portal, open the VM and select **Stop**, then check that the status says **Stopped (deallocated)**. [Lab 13: VM size, disk, stop and deallocate](/azure-basics-labs/vm-size-disk-stop-deallocate/) covers the difference in detail. Keep the RDP rule removed. When you need to connect again, repeat Part 5, then remove the rule again.

About the public IP `pip-azb-win01` when you keep the VM: the subnet is private, and Learn says a VM in a private subnet needs an explicit outbound method for Windows activation and updates. The later labs also need the VM to reach Azure services, and this lab does not add any other outbound method. So keep the public IP attached while you work, with no inbound rule. It is a temporary item. A public IP address is a billed resource while it exists, so check its price in the pricing calculator and delete it when you delete the VM, at the latest in the cleanup in [Lab 19: When something breaks](/azure-basics-labs/when-something-breaks/).

Keep for later labs:

- `rg-azb-lab`, `vnet-azb`, `snet-vm` and `nsg-azb-vm`, with no RDP rule.
- The VM `vm-azb-win01`, deallocated, its public IP `pip-azb-win01` (no inbound rule), and the role assignment for `TestUsers`, if you are continuing.
- The test user `testuser1` and the group `TestUsers`.
- The local admin password for `azureuser`, in your password manager.

## Where this is used in AVD

AVD session hosts that are joined to Entra use the same extension idea and the same two roles, and the user also needs the Desktop Virtualization User role on the app group. The sign-in is one of three separate steps in AVD: [How Sign-In Works in Azure Virtual Desktop: Three Authentications and SSO](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/). The choice of image and the licence it needs is in [Choose the Session Host Operating System and Licensing](/azure-virtual-desktop/session-host-operating-system-and-licensing/).

## Next lab

[Lab 13: VM size, disk, stop and deallocate](/azure-basics-labs/vm-size-disk-stop-deallocate/) changes the size of this VM, adds a disk, and shows what each power state costs.

## Sources

- [Sign in to a Windows virtual machine in Azure by using Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-windows)
- [Quickstart: Create a Windows virtual machine in the Azure portal](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-portal)
- [Quickstart: Create a Windows virtual machine with the Azure CLI](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-cli)
- [Find and use Azure Marketplace VM images](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/cli-ps-findimage)
- [Check vCPU quotas](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas)
- [View quotas](https://learn.microsoft.com/en-us/azure/quotas/view-quotas)
- [B-family VM sizes: Bsv2-series](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/bsv2-series)
- [Windows Enterprise multi-session FAQ](https://learn.microsoft.com/en-us/azure/virtual-desktop/windows-multisession-faq)
- [How to deploy Windows 11 on Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/windows-desktop-multitenant-hosting-deployment)
- [Azure Hybrid Benefit for Windows VMs](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/hybrid-use-benefit-licensing)
- [Configure managed identities on Azure VMs](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-configure-managed-identities)
- [Configure Microsoft Entra ID authentication for Azure Bastion](https://learn.microsoft.com/en-us/azure/bastion/bastion-entra-id-authentication)
- [Sign in to a Linux VM with Microsoft Entra ID (role assignment steps)](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-linux)
- [az role assignment create](https://learn.microsoft.com/en-us/cli/azure/role/assignment)
- [az vm](https://learn.microsoft.com/en-us/cli/azure/vm)
- [Default outbound access in Azure](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/default-outbound-access)
- [States and billing status of Azure Virtual Machines](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing)
- [Auto-shutdown a virtual machine](https://learn.microsoft.com/en-us/azure/virtual-machines/auto-shutdown-vm)
- [Delete a VM and attached resources](https://learn.microsoft.com/en-us/azure/virtual-machines/delete)
- [Create, change, or delete an Azure public IP address](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/virtual-network-public-ip-address)
- [Microsoft Entra registered devices](https://learn.microsoft.com/en-us/entra/identity/devices/concept-device-registration)
- [Naming rules and restrictions for Azure resources](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-name-rules)
- [Public IP addresses](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/public-ip-addresses)
- [Enforce Microsoft Entra multifactor authentication for Azure Virtual Desktop using Conditional Access](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa)
- [How to connect using Remote Desktop and sign on to an Azure virtual machine running Windows](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/connect-rdp)
- [Understanding security warnings when opening Remote Desktop (RDP) files](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/understanding-security-warnings)
