---
title: "Windows VM with Microsoft Entra Sign-In"
seoTitle: "Azure Windows VM with Entra ID Sign-In: Beginner Lab"
layout: post.njk
permalink: "/azure-basics-labs/windows-vm-entra-sign-in/"
order: 322
tags: [azure-basics-lab]
deck: "You create a small Windows Server VM in your own subnet, give the TestUsers group the right to sign in, and connect with your test user's Microsoft Entra account. Then you leave the VM safely stopped."
description: "Beginner Azure lab: create a Windows Server 2025 VM, turn on Microsoft Entra sign-in, give a group the Virtual Machine User Login role and connect with RDP."
---

By the end of this lab you will have a small Windows Server VM named `vm-azb-win01` in `snet-vm`. Your test user `testuser1` will sign in to it over Remote Desktop with a Microsoft Entra account, not with a local password. You will then remove the temporary RDP rule and stop the VM so it does not bill for compute.

A virtual machine (VM) is a computer that runs inside Azure. You rent it by the hour, and you pay for it while it exists in a running state. This is the first lab in the series that costs real money, so read "Safety first" before you click anything.

Anything in `<angle brackets>` or ALL CAPS in a command or a step is a placeholder. Replace it, brackets included. Example: `<account>` becomes `stazb48213`.

## What you need

- [Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/): the throwaway account. A free account has a $200 credit for 30 days.
- [Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): the budget from that lab sends alerts. It does not stop anything.
- [Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/): the user `testuser1` and the group `TestUsers`, with `testuser1` as a member. Write down testuser1's full sign-in name (the user principal name). It ends in `.onmicrosoft.com`. In this lab, `testuser1@yourtenant.onmicrosoft.com` stands for that name. You also need the password.
- [Multifactor authentication (MFA)](/azure-basics-labs/mfa/): per-user MFA must still show **Disabled** for every user. You looked at that page in the MFA lab.
- [Conditional Access](/azure-basics-labs/conditional-access/): the policy from that lab targets other apps and should be off or deleted. If any other Conditional Access policy that requires MFA is on, read the error table under "The most common mistake" first.
- [Azure RBAC roles](/azure-basics-labs/rbac-roles/): how a role, a scope and a person fit together.
- [Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/) and [Network security group](/azure-basics-labs/network-security-group/): `vnet-azb`, `snet-vm` and `nsg-azb-vm` in `rg-azb-lab`. A network security group (NSG) is the list of allow and deny rules on the subnet. The network security group lab told you to delete its RDP rule. You add it again in this lab. If `allow-rdp-my-ip` is still listed in `nsg-azb-vm`, check that its source is your current IP and skip the section "Open RDP for your own IP, for now".
- [Your PC and Remote Desktop clients](/azure-basics-labs/your-pc-and-remote-desktop-clients/): a Windows 10 or Windows 11 PC (a Mac cannot do the sign-in steps) and the route you wrote down there: A (PC already known to your tenant), B (personal PC that you register) or C (any other PC, web account setting). The section "Connect as the test user" uses it.
- [Azure Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) if you use the CLI steps. Azure CLI 2.76 or newer.
- Time: about 90 minutes. You can stop safely after the section "Let the group sign in". Cost: a VM, a disk and a public IP address, billed while they exist. Open the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) now, look up the hourly price for your region and size, and write it in your notes.
- Role: Owner on the subscription of your throwaway account. Creating the VM needs it, and so does assigning a role.
- Billing right now: nothing yet. New in this lab: a VM, its disk and a public IP.

State at the start: no VM exists. At the end: the VM exists and is **Stopped (deallocated)**, `pip-azb-win01` is kept, and the RDP rule is removed. The next lab starts from there.

## Safety first

- Use the throwaway tenant only. Use a separate browser profile or a private window for it. Read the tenant and subscription name at the top right of the portal before you change anything. If you can see your employer's name anywhere in the top right, stop.
- A running VM costs money. **Running** and **Stopped** are billed. **Stopped (deallocated)** is not billed for compute, but disks and networking still are.
- Set a phone alarm for two hours from now with the text "Stop the VM". Before you close the laptop, deallocate the VM. Do the connect steps ("Open RDP for your own IP" and "Connect as the test user") in one sitting.
- A budget only sends an alert. It never stops a VM. You have to stop it.
- Never use `Any` or `*` as the source for port 3389. The rule you add is for your own IP address only, and you remove it before you finish.
- A public IP with the RDP rule removed is fine overnight. A public IP with the rule open is not.
- Give `testuser1` the role **Virtual Machine User Login**, not Owner and not Virtual Machine Administrator Login. Owner or Contributor alone does not allow sign-in anyway.
- Do not turn on any option that enrols the VM in Intune or mobile device management (MDM). Windows Server VMs do not support MDM enrolment.
- Leave per-user MFA at **Disabled**. A per-user **Enabled** or **Enforced** setting can make the sign-in to an Entra VM fail.
- Use the region on your notes sheet from [the account lab](/azure-basics-labs/start-azure-account-tenant-subscription/) everywhere. The VM must be in the same region as `vnet-azb`.

## What the lab builds

![Four numbered steps. 1: your PC connects over RDP, TCP 3389, to the temporary public IP pip-azb-win01. 2: the network security group nsg-azb-vm on the subnet snet-vm allows 3389 from your IP only. 3: the Windows Server VM vm-azb-win01 in snet-vm, which has a system-assigned managed identity and the Microsoft Entra sign-in extension, checks the sign-in with Microsoft Entra ID over port 443. 4: the group TestUsers, with testuser1, holds the role Virtual Machine User Login on the resource group rg-azb-lab, so the check passes.](/img/basics/windows-vm-entra-sign-in.svg)

*Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Check quota, size and image

Before you create a VM, check that your subscription is allowed to. vCPU quota has two tiers for each region: a total regional limit, and a limit for each VM size family. A new VM must fit inside both. Quota counts cores in use whether the VM is running or deallocated.

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name at the top right.
2. In the search box at the top of the portal, enter **Quotas** and select **Quotas**. Select **My quotas**. Set the provider filter to **Compute**, and filter to your region and your subscription.
3. Find the row **Total Regional vCPUs** and the row for the B-series family (the name differs a little between regions). Read the usage and the limit. You need 2 free vCPUs in both. If either row has no room, pick another size with 2 vCPUs when you create the VM, or try again tomorrow. Do not change region: the VM has to sit next to `vnet-azb`.

Check: both rows show room for at least 2 vCPUs.

**The size.** This lab uses `Standard_B2s_v2`: 2 vCPUs and 8 GiB of memory, from the burstable B-series for small test servers. If the portal does not offer it for your region, choose another size with 2 vCPUs and at least 4 GiB of memory.

**The image.** Use **Windows Server 2025 Datacenter: Azure Edition**, not the one with **Core** in its name. Entra sign-in works on Windows Server 2022 or 2025 installed with Desktop Experience. This lab uses 2025 on purpose: the [Azure Files lab](/azure-basics-labs/storage-azure-files/) needs it.

The Windows Server license is included in the VM price, so you need nothing extra. Leave the Azure Hybrid Benefit box unticked: it is only for licenses you already own.

### Create the VM

**Background: two separate things must be true.** To sign in with Entra, the VM has to trust Entra, and Azure has to say you may. The first part is a small add-on to the VM, the Microsoft Entra sign-in extension (`AADLoginForWindows`). Installing it joins the VM to Entra. It needs a system-assigned managed identity first: an Azure-managed account that belongs to the VM itself. The second part is a role: **Virtual Machine User Login** (a normal user) or **Virtual Machine Administrator Login** (an admin). Owner or Contributor does not give sign-in rights, on purpose. Once the VM is Entra joined, you cannot join it to a normal domain.

4. In the search box, enter **Virtual machines** and select **Virtual machines**. Select **Create**, then **Azure virtual machine**.
5. On the **Basics** tab, set:
   - Subscription: your throwaway subscription.
   - Resource group: `rg-azb-lab`.
   - Virtual machine name: `vm-azb-win01`. The portal uses it for the Azure resource name and the Windows computer name. A Windows computer name can be at most 15 characters. This one has 12.
   - Region: the same region as `vnet-azb`.
   - Image: **Windows Server 2025 Datacenter: Azure Edition** (select **See all images** if it is not in the list).
   - Size: select **See all sizes** and choose `Standard_B2s_v2`, or the small size you picked in the quota check.
6. Under **Administrator account**, enter the user name `azureuser` and a password of at least 12 characters that meets the complexity rules. This is a local administrator account. Save it somewhere you can find it (a password manager, or a note on your own PC). You need it in the Azure Files lab. This lab uses it once, in "Connect as the test user", to test the network path.
7. Under **Inbound port rules**, set **Public inbound ports** to **None**. The RDP rule goes on your subnet's NSG later in this lab, not on the VM.
8. Select **Next: Disks**. Leave the defaults. The OS disk is set to **Delete with VM** by default. Keep that.

### Networking and Management tabs

**Background: the public IP does two jobs.** You use it to reach the VM for a short time. It also lets the VM reach the internet (Windows updates, and Entra sign-in on port 443). A new subnet has no outbound path of its own (see the virtual network lab), so without the public IP the sign-in extension fails. A Standard public IP accepts nothing inbound until an NSG allows it.

9. Select **Next: Networking**. Set:
   - Virtual network: `vnet-azb`.
   - Subnet: `snet-vm`.
   - Public IP: **Create new**. If the form asks for an SKU, choose **Standard**. Name it `pip-azb-win01`.
   - NIC network security group: **None**. The subnet already has `nsg-azb-vm`. One NSG at the subnet keeps the rules in one place, as in the network security group lab.
   - Tick **Delete public IP and NIC when VM is deleted**.
10. Select **Next: Management**. Set:
    - Under **Identity**, tick **Enable system assigned managed identity**.
    - Under the Microsoft Entra ID heading on the **Management** tab, tick **Login with Microsoft Entra ID**. It installs the extension. If you cannot find it, skip it. The Check below shows how to add the extension afterwards.
    - If you see any option to enroll the VM in Intune or MDM, leave it off.
    - Auto-shutdown: tick **Enable auto-shutdown**, choose a time later today and your time zone. It is a safety net, not a replacement for stopping the VM yourself. The next day check the status. If it says **Stopped** and not **Stopped (deallocated)**, select **Stop**.
11. Select **Review + create**. Write the hourly price shown for the VM in your notes. When you see **Validation passed**, select **Create**. Wait for the deployment, then select **Go to resource**.

Check: on the VM page, open **Identity** and see that **System assigned** is **On**. Open **Extensions + applications** and see `AADLoginForWindows` with **Provisioning succeeded**. If the extension is missing, add it: **+ Add**, search for **AADLoginForWindows**, then **Review + create** and **Create**. If it failed, see the error table under "The most common mistake".

### Let the group sign in

12. Open the resource group `rg-azb-lab`. Select **Access control (IAM)**.
13. Select **Add**, then **Add role assignment**.
14. On the **Role** tab, search for **Virtual Machine User Login** and select it. Select **Next**.
15. On **Members**, set **Assign access to** to **User, group, or service principal**. Select **+ Select members**, search for `TestUsers`, select the group and choose **Select**.
16. Select **Review + assign**, then **Review + assign** again.

Now both things are true: the VM trusts Entra (the extension) and Azure says `TestUsers` may sign in (the role). If a later sign-in fails, ask which of the two is missing.

The roles lab says to give roles to groups, not people, and at the smallest scope that works. The resource group holds only the VM and its network parts for this series, so it is a small scope. A new role takes a few minutes to apply. Wait before you test.

Check: on the resource group's **Access control (IAM)**, open **Role assignments** and find `TestUsers` with **Virtual Machine User Login**. If `testuser1` is not in `TestUsers`, add the user now (the users and groups lab).

**Safe to stop here.** Open the VM, select **Stop**, and check that the status says **Stopped (deallocated)**. Nothing is open to the internet yet. When you come back, select **Start** and wait for **Running** before the next section.

### Open RDP for your own IP, for now

RDP is Remote Desktop Protocol. It listens on TCP port 3389.

17. On the same PC you will connect from, search the web for "what is my IP". Use the IPv4 address (four numbers with dots). If you use a VPN, the VPN's address is the one that counts. Check it again just before you add the rule, because home addresses change.
18. Open `nsg-azb-vm`, select **Inbound security rules**, then **+ Add**. Set:
    - Source: **IP Addresses**
    - Source IP addresses: your own address
    - Source port ranges: `*`
    - Destination: **Any**
    - Service: **RDP**
    - Action: **Allow**
    - Priority: `1000`
    - Name: `allow-rdp-my-ip`

    Select **Add**. The source must be your IP. Destination **Any** is correct here: it means any address in the subnet.

Check: the rule shows your single IP address as the source. It does not say `Any`.

### Connect as the test user

Do this part in one sitting. Make sure the VM status says **Running**.

**Background: not every PC can connect.** Remote connections to an Entra-joined VM are allowed only from Windows 10 or later PCs that are Entra registered (build 20H1 or later), joined or hybrid joined to the same directory as the VM. A registered PC must type the user name as `AzureAD\` plus the full sign-in name. Any other PC can use the setting **Use a web account to sign in to the remote computer**. Use the route you chose in the Remote Desktop clients lab.

19. Routes A and B: open **Settings** > **Accounts** > **Access work or school**. The throwaway account must be listed. If it is not, go back to the Remote Desktop clients lab and register it. Do not choose **Join this device to Microsoft Entra ID**.
20. Open a private browser window (InPrivate in Edge, Incognito in Chrome). Go to `https://portal.azure.com` and sign in as `testuser1`. The first sign-in asks for a new password and to register Microsoft Authenticator. Do both. This is expected, not an error. A temporary password cannot be used for a remote desktop sign-in. Close the private window. Your normal browser window, signed in as your admin, is the admin window.
21. In your admin window, open the VM. Select **Connect**, then **Native RDP**. You may need **More ways to connect** first. Keep the default IP address and port 3389, then select **Download RDP File**. Ignore the generic warning that the file might harm your device. This file comes from your own portal, so opening it is right.
22. **First prove the network path.** Open the downloaded file and select **Connect**. An "unknown publisher" warning is expected. Check that the address shown is your VM's public IP address and leave every resource box unticked. When Windows asks for credentials, select **More choices**, then **Use a different account**. Enter `vm-azb-win01\azureuser` and the password you set when you created the VM. If the desktop appears, the public IP, the rule and RDP all work. Sign out from the Start menu. If it does not, fix the rule or your IP now, not the Entra settings.
23. **Now sign in with Entra.**
    - **Routes A and B.** Open the same RDP file again, select **Connect**, then **More choices** and **Use a different account**. A Windows Security box asks for credentials. Enter `AzureAD\testuser1@yourtenant.onmicrosoft.com` and the new password. Use your real domain. Select **Yes** if Windows asks you to confirm the VM's identity.
    - **Route C.** The web account setting needs the VM's name, not its IP address, and the name must resolve to the VM's IP address. A line in the `hosts` file of your PC does that. It needs administrator rights. If you cannot change that file (for example on an employer PC), stop here and do this lab from a personal PC.
      1. Find the VM's public IP: VM **Overview** > **Public IP address**.
      2. On your PC, search for **Notepad**, right-click it and select **Run as administrator**.
      3. Select **File** > **Open**, go to `C:\Windows\System32\drivers\etc`, change the file type filter to **All files** and open `hosts`.
      4. Add a new last line: your VM's IP, one space, then `vm-azb-win01`. Example: `20.1.2.3 vm-azb-win01`. Use your own IP.
      5. Save the file. Keep this line until you delete the public IP in the cleanup lab, because the address stays the same.
      6. Open **Remote Desktop Connection**, select **Show Options**, open the **Advanced** tab and tick **Use a web account to sign in to the remote computer**.
      7. On the **General** tab type `vm-azb-win01` as the computer and select **Connect**.
      8. When asked for credentials, enter `testuser1@yourtenant.onmicrosoft.com`. When asked to allow the connection to a new PC, select **Yes**.
24. Wait for the desktop. The first sign-in takes a while.

Check: you see the VM desktop, and inside the VM `dsregcmd /status` in PowerShell shows `AzureAdJoined : YES`. Then sign out from the Start menu. Do not lock the session: the lock screen does not support Entra tokens in a remote session, so a locked session is disconnected. Optional: in the Microsoft Entra admin center, open **Entra ID** > **Monitoring & health** > **Sign-in logs** and find the sign-in to **Microsoft Azure Windows Virtual Machine Sign-in** (some tenants show **Azure Windows VM Sign-in**).

## Steps with the Azure CLI

Run these in Cloud Shell (Bash). Check the subscription first. Azure already requires MFA for create, update and delete from the CLI, so your normal sign-in covers it. Anything in `<angle brackets>` or ALL CAPS is yours to replace. Run `echo` on a variable before you use it. If Cloud Shell was closed or timed out, run this block again before the Clean up commands.

Find your public IP on your own PC, in a browser. Do not use `curl` in Cloud Shell for this: it returns Cloud Shell's address, not your PC's.

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
MYIP=203.0.113.25        # EXAMPLE. Replace with your own IPv4 address
case "$MYIP" in 203.0.113.*|"") echo "STOP: set MYIP to your own public IP";; esac
echo "$LOCATION"
read -s -p "Local admin password for azureuser (12 or more characters): " ADMINPW; echo
```

Check the quota in your region. Look for **Total Regional vCPUs** and the B-series row, and compare `currentValue` with `limit`.

```bash
az vm list-usage --location $LOCATION --output table
```

Create the VM. The variable `ADMINPW` holds the password you typed above. `--nsg ""` means no NSG on the network card, because the subnet has one. `--assign-identity '[system]'` turns on the system-assigned managed identity.

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

Install the Microsoft Entra sign-in extension. The portal option **Login with Microsoft Entra ID** does this for you. The CLI does not, so run it here.

```bash
az vm extension set \
    --publisher Microsoft.Azure.ActiveDirectory \
    --name AADLoginForWindows \
    --resource-group $RG \
    --vm-name $VM
```

Set an auto-shutdown time as a safety net. The time is in UTC. Pick a time later today, and still stop the VM yourself.

```bash
az vm auto-shutdown --resource-group $RG --name $VM --time 2300
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

Add the temporary RDP rule for your own IP, as in the network security group lab.

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

Check: the extension is listed, the role is assigned, and the rule shows your IP.

```bash
az vm extension list --resource-group $RG --vm-name $VM --output table
az role assignment list --scope $RG_ID --role "Virtual Machine User Login" --output table
az network nsg rule list --resource-group $RG --nsg-name $NSG --output table
az vm show --resource-group $RG --name $VM --show-details --query publicIps --output tsv
```

Then connect as in "Connect as the test user" in the portal steps, using your route: download the RDP file from the portal and sign in first as `vm-azb-win01\azureuser`, then as `AzureAD\testuser1@yourtenant.onmicrosoft.com` (routes A and B), or use the web account setting (route C).

## Terraform

No Terraform in this lab. The VM lives for a few hours with a temporary rule, and a sign-in test is quicker by hand. The extension, the managed identity and the role assignment would each be separate resources. If you want a repeatable VM build with Terraform, see [the AVD quick lab](/terraform-labs/avd-quick-lab/). The Terraform basics lab covers the first steps.

## Check that it works

- `vm-azb-win01` is in `rg-azb-lab`, in the same region as `vnet-azb`, in the subnet `snet-vm`.
- **Identity** shows system assigned **On**, and `AADLoginForWindows` shows **Provisioning succeeded**.
- `TestUsers` has **Virtual Machine User Login** at the resource group, and nobody got Owner for this lab.
- `azureuser` reached the desktop (network path works).
- `testuser1` signed in over RDP with the Entra account, and `dsregcmd /status` shows `AzureAdJoined : YES`.
- Per-user MFA still shows **Disabled** for everyone.

## The most common mistake

Forgetting the role, or giving Owner instead of the sign-in role. You see this message when you connect: "Your account is configured to prevent you from using this device. For more info, contact your system administrator." Check that the user has **Virtual Machine Administrator Login** or **Virtual Machine User Login**. Owner or Contributor on the VM does not count. Add the role as in "Let the group sign in", wait a few minutes, and try again.

### Other errors you can hit

| What you see | Cause | What to do |
|---|---|---|
| "Your credentials didn't work." | A PC in another directory, a registered PC without the `AzureAD\` prefix, a temporary password, the extension removed, or a legacy per-user **Enabled** or **Enforced** MFA setting. | Sign in as the user in a private window and change the password. Check that per-user MFA shows **Disabled**. Check **Access work or school** on your PC, or use route C. Check the extension is still there. |
| "The sign-in method you're trying to use isn't allowed." | A Conditional Access policy requires MFA, and your PC does not use strong authentication such as Windows Hello. | Turn that policy off for this lab, or exclude the app **Microsoft Azure Windows Virtual Machine Sign-in** from it. Do that only in this throwaway tenant. The policy from the [Conditional Access lab](/azure-basics-labs/conditional-access/) targets other apps and should not cause this. |
| AADSTS293004 (target-device identifier not found) | The computer name you typed does not match the VM's host name in Entra. | Use the short name `vm-azb-win01`, not a full domain name. |
| The extension shows a failed state | The VM has no system-assigned identity, or it cannot reach `login.microsoftonline.com`, `enterpriseregistration.windows.net` and `pas.windows.net` on port 443, or an old device named `vm-azb-win01` exists in Entra. | Turn on the identity, install the extension again, and check **Devices** in the Entra admin center for an old entry. |
| Cannot connect even as `azureuser` | The VM is not running, the NSG rule is missing or has the wrong IP, or your IP changed. | Check the status, the rule and your current public IP. |

The rest of the checklist is in [When something breaks](/azure-basics-labs/when-something-breaks/).

## Clean up

Do the first part either way. Sign out of the VM first. Removing a rule does not cut connections that are already open.

**Remove the RDP rule.**

Portal: open `nsg-azb-vm`, select **Inbound security rules**, tick `allow-rdp-my-ip`, select **Delete**, then **Yes**.

CLI:

```bash
az network nsg rule delete \
    --resource-group $RG \
    --nsg-name $NSG \
    --name allow-rdp-my-ip
```

**Then pick one.**

| Your plan | What to do |
|---|---|
| Doing the VM size lab within a day, or carrying on with the series | Stop the VM (below). Keep the VM and `pip-azb-win01`. |
| Done for now and not coming back this week | Delete the VM and the public IP (below). You can rebuild the VM in about 20 minutes with the CLI block. |
| Stopping the series | Delete the VM and the public IP. The cleanup lab deletes `rg-azb-lab`. |

**Stop the VM.** Do not shut Windows down from inside: that leaves the VM in the billed **Stopped** state. In the portal, open the VM, select **Stop**, and check that the status says **Stopped (deallocated)**. With the CLI:

```bash
az vm deallocate --resource-group $RG --name $VM
az vm show --resource-group $RG --name $VM --show-details --query powerState --output tsv
```

The last command should print `VM deallocated`. The [VM size lab](/azure-basics-labs/vm-size-disk-stop-deallocate/) shows the difference between the two states.

**Delete the VM and the public IP.** Portal: open the VM, select **Delete**, and confirm. Because you ticked the delete options, the disk and the network card go with it. Open **Public IP addresses**, find `pip-azb-win01`, and delete it if it is still there. CLI:

```bash
az vm delete --resource-group $RG --name $VM --yes
az network public-ip delete --resource-group $RG --name $PIP   # if it says the IP was not found, the VM delete already removed it
az resource list --resource-group $RG --output table
```

Check: the last command lists no VM, disk, network card or public IP. You may still see `vnet-azb` and `nsg-azb-vm`. If a device named `vm-azb-win01` is still in **Devices** in the Entra admin center, delete it before you build a VM with the same name. A device with the same name makes the join fail. Route C: remove the `hosts` line too.

**The public IP while you keep the VM.** Keep `pip-azb-win01` attached, with no inbound rule. The subnet has no outbound path of its own, and the later labs need the VM to reach Azure services. A Standard public IP is billed every hour it exists, even when the VM is deallocated. Check the price in the pricing calculator now. The cleanup lab deletes it.

### Connect again later

The later labs refer to this routine. Use it whenever a lab says "connect to the VM".

1. **Start the VM.** Portal: **Virtual machines** > `vm-azb-win01` > **Start**. Wait until **Overview** says **Running** (2 to 3 minutes). CLI: `az vm start --resource-group $RG --name $VM`.
2. **Look up your public IP again.** Use the same PC you connect from. It may have changed.
3. **Add the rule `allow-rdp-my-ip`.** Priority 1000, source your IP only, as in "Open RDP for your own IP, for now". If a rule with that name is still listed, check its source and fix it. CLI: the `az network nsg rule create` command above, after you set `MYIP`.
4. **Connect.** Routes A and B: open the saved `.rdp` file (or download it again with **Connect** > **Native RDP**), select **More choices** > **Use a different account**, and sign in as `AzureAD\testuser1@yourtenant.onmicrosoft.com`. For the local administrator use `vm-azb-win01\azureuser`. Route C: open Remote Desktop Connection, tick the web account box, connect to `vm-azb-win01` (the `hosts` line must still be there) and sign in with `testuser1@yourtenant.onmicrosoft.com`.
5. **Sign out** from the Start menu. Do not lock.
6. **Delete the rule** `allow-rdp-my-ip` (steps above).
7. **Stop the VM** and check that the status says **Stopped (deallocated)**.

End state: VM Stopped (deallocated), no `allow-rdp-my-ip` rule.

Where the VM should be when each later lab starts and ends:

| Topic | At the start | At the end |
|---|---|---|
| This lab | No VM | Stopped (deallocated), no rule, `pip-azb-win01` kept |
| VM size and disk | Stopped (deallocated). You start it. No rule needed. | Stopped (deallocated), no rule |
| Azure Files | Stopped (deallocated). Needs the routine steps 1 to 4. | Stopped (deallocated), no rule |
| Key Vault | Stopped (deallocated). Needs the routine steps 1 to 4. | Stopped (deallocated), no rule |
| Log Analytics | Stopped (deallocated). You start it. No rule needed. | Stopped (deallocated) |
| Azure Policy | The VM is not used | Stays Stopped (deallocated) |
| Private endpoint | Stopped (deallocated). Needs the routine steps 1 to 4. | Stopped (deallocated), no rule |

Each lab repeats its own line under "What you need". If a lab and this table differ, follow the lab.

Keep for later labs:

- `rg-azb-lab`, `vnet-azb`, `snet-vm` and `nsg-azb-vm`, with no RDP rule.
- The VM `vm-azb-win01` (Stopped (deallocated)), its public IP `pip-azb-win01`, and the role assignment for `TestUsers`.
- `testuser1`, `TestUsers`, and the local admin password for `azureuser`.
- Your notes: route A, B or C, your tenant name, `testuser1`'s sign-in name, the region.

## Where this is used in AVD

AVD session hosts that are joined to Entra use the same extension idea and the same two roles, and the user also needs the Desktop Virtualization User role on the app group. In AVD the session host has no public IP and no inbound 3389 rule: the user connects through the AVD service. What you did here is the plain-VM version of the same sign-in.

The sign-in is one of three separate steps in AVD: [How Sign-In Works in Azure Virtual Desktop: Three Authentications and SSO](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/). The choice of image and the license it needs is in [Choose the Session Host Operating System and Licensing](/azure-virtual-desktop/session-host-operating-system-and-licensing/).

## Next lab

[VM size, disk and power states](/azure-basics-labs/vm-size-disk-stop-deallocate/) starts the VM, changes its size and OS disk type, and shows what each power state costs.

## Sources

- [Sign in to a Windows virtual machine in Azure by using Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-windows)
- [Quickstart: Create a Windows virtual machine in the Azure portal](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/quick-create-portal)
- [States and billing status of Azure Virtual Machines](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing)
