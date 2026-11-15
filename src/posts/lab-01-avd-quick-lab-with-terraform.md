---
title: "Deploy an AVD Quick Lab with Terraform: Host Pool, Two Session Hosts and FSLogix Profiles"
seoTitle: "Azure Virtual Desktop Terraform Lab: Host Pool, Entra Join, FSLogix"
layout: post.njk
permalink: "/terraform-labs/avd-quick-lab/"
order: 301
tags: [terraform-lab]
deck: "What a small Terraform project builds for Azure Virtual Desktop, how to run it, and the manual steps that Terraform does not do for you."
description: "A walk through a Terraform quick lab for Azure Virtual Desktop: a pooled host pool, two Microsoft Entra joined session hosts and an Azure Files share for FSLogix profiles, with the steps to run it and the checks to make afterwards."
---

This article walks through a small Terraform project that builds an Azure Virtual Desktop (AVD) lab from code. You run a few commands, and Terraform creates the host pool, two session hosts, the network and a file share for user profiles. You finish a few steps by hand in the Azure portal, then sign in to a desktop.

The code is in a public repository: [terraform-azure-avd](https://github.com/AddySidd27/terraform-azure-avd). This article explains what it builds and why, in the order you would meet it. It is a lab, not a production design, and the last section lists what you would change before real use.

Everything below describes what the code does. It is a lab, not a production design.

## Key terms

| Term | Meaning |
|---|---|
| Azure subscription | The billing and access boundary in Azure. Everything the lab creates goes into one subscription. |
| Microsoft Entra ID | Microsoft's cloud identity service, where users and groups live. |
| Terraform | A tool that builds cloud resources from text files. You describe what you want, run `terraform plan` to see the changes, and run `terraform apply` to make them. |
| Provider | A plug-in that lets Terraform talk to one service. This project uses the `azurerm` provider for Azure. |
| Terraform state | The file where Terraform records what it built. It can contain secrets, so protect it. |
| Module | A folder of Terraform files for one job, such as the network. The top-level files call each module. |
| Resource group | A container in Azure that holds related resources. Deleting it deletes everything inside. |
| Host pool | A group of session hosts that users share. |
| Session host | A virtual machine (VM) that runs the users' desktops. |
| Pooled | A host pool type where many users share each session host. |
| Multi-session | A Windows 11 edition where several users sign in to the same VM at the same time. |
| Breadth First | A load-balancing method that spreads new sessions across the hosts. |
| Application group | The set of apps or desktops that users get from a host pool. A Desktop application group gives users a full desktop. |
| Workspace | What users see in their feed. It lists the application groups they can use. |
| Registration key | A secret that lets a session host join a host pool. It expires. |
| RDP property | A setting for the Remote Desktop Protocol (RDP), the protocol that carries the desktop to the user. |
| Microsoft Entra join | The VM is joined to Microsoft Entra ID directly, with no domain controller (a server that runs on-premises Active Directory). |
| VM extension | A small add-on that Azure installs on a VM. |
| Run command | An Azure feature that runs a PowerShell script on a VM. |
| FSLogix profile container | A virtual disk file (VHDX) that holds a user's profile. FSLogix attaches it at sign-in so the profile follows the user to any host. |
| SID | A security ID, the unique number Windows gives each user. |
| Azure Files | Azure's managed file shares. They use SMB, the Windows file-sharing protocol, on port 445. |
| ZRS | Zone-redundant storage. Azure keeps copies of the data in three zones of the region. |
| Microsoft Entra Kerberos | A way for Microsoft Entra ID to issue the Kerberos tickets (sign-in proofs) that SMB needs. It lets Entra joined VMs sign in to Azure Files without a domain controller. |
| Cloud-only user | A user created in Microsoft Entra ID, not synced from on-premises Active Directory. |
| Conditional Access | Microsoft Entra rules that decide when a sign-in is allowed, for example when it requires multifactor authentication (MFA). |
| RBAC | Role-based access control: you give a user or group a role on a resource. |

## What the lab builds

![Diagram: What the Terraform quick lab deploys: one resource group with an AVD workspace, desktop application group, host pool, two session hosts and an Azure Files profile share.](/img/avd/AVD-Terraform-Quick-Lab.svg)

*Source: the lab's Terraform code, in the [terraform-azure-avd](https://github.com/AddySidd27/terraform-azure-avd).*

With the default settings, one `terraform apply` creates these things in one Azure region (default `eastus`):

- A resource group, `rg-avd-dev`.
- A pooled host pool that uses the Breadth First method and allows 10 sessions per host, a Desktop application group, and a workspace linked to the application group.
- A virtual network `10.20.0.0/16` with one subnet `10.20.1.0/24` and a network security group (NSG) that denies inbound traffic from the internet. The session hosts get no public IP address.
- Two session hosts, `avdsh-01` and `avdsh-02`. Each runs Windows 11 multi-session with Microsoft 365 apps (image `win11-24h2-avd-m365`) on size `Standard_D4s_v5`.
- A storage account (StorageV2, ZRS) with Microsoft Entra Kerberos turned on, and a file share named `profiles` with a 1,024 GiB quota.
- Role assignments for a Microsoft Entra group that you supply: three roles, assigned four times with two hosts, because the VM login role is assigned once per host.

Names follow the pattern `<type>-<project_name>-<environment>`, so the host pool is `avd-hp-avd-dev`. You can change `project_name` (default `avd`) and `environment` (default `dev`).

Microsoft's own Terraform example, [Configure Azure Virtual Desktop with Terraform](https://learn.microsoft.com/en-us/azure/developer/terraform/configure-azure-virtual-desktop), builds only the workspace, host pool and application group. It was tested with Terraform 1.1.7 and `azurerm` 2.99.0. This lab adds the session hosts, the network, the storage and the roles, and uses newer versions.

## Before you start

You need:

- An Azure subscription where you can create resources and role assignments (for example, the Owner role).
- Free quota for 8 vCPUs of the `Standard_Dv5` VM family in your region. Two `Standard_D4s_v5` VMs use 4 vCPUs each.
- A Microsoft Entra security group for your test users, and a test user in it. In the Azure portal, open Microsoft Entra ID, then Groups. The group's **Object ID** is on its Overview page.
- Permission to grant admin consent in Microsoft Entra ID (a later step needs it).
- The Azure CLI, Git and Terraform 1.9 or newer on your computer.

The lab costs money while it exists. Two VMs, their disks and the storage account are all billed. Delete the lab when you finish (see "Clean up" below). Use the [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/) with your region and the sizes above.

## How the code is organized

The top-level files are `main.tf` (it calls the modules), `variables.tf` (the settings), `locals.tf` (the names), `outputs.tf` (what Terraform prints at the end), `versions.tf` (it pins the Terraform and provider versions) and `providers.tf` (it configures the Azure provider). Each module has its own folder under `modules/`:

| Module | What it creates |
|---|---|
| `resource-group` | The resource group |
| `networking` | The virtual network and subnet |
| `network-security-group` | The NSG, linked to the subnet |
| `storage` | The storage account and the `profiles` file share |
| `avd` | The host pool, application group, workspace and the link between them, plus the registration key |
| `session-hosts` | The network cards, the VMs, and the setup steps that run on each VM |
| `rbac` | The role assignments |

## What the code does

The numbered parts below are in reading order. Terraform works out the build order by itself.

### 1. The host pool, application group and workspace

The `avd` module creates the host pool, the Desktop application group and the workspace, then links the workspace to the application group.

The host pool sets one RDP property, `enablerdsaadauth:i:1`. It makes the connection use Microsoft Entra authentication, which gives single sign-on, if the session host supports it. Single sign-on also needs steps in your tenant that the lab does not do, described on the page [Configure single sign-on for Azure Virtual Desktop using Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-single-sign-on). Until you do them, users may see an extra prompt when they connect.

A new session host needs a registration key to join the host pool. Terraform creates the key and passes it to each VM. The key expires 23 hours after Terraform last created or rotated it. A `time_rotating` resource in `registration.tf` rotates it every 24 hours. So the next `terraform apply` after the 24 hours makes a new key and gives it to the VMs again. Hosts that have already joined keep working when the key expires. You need a valid key only to add or repair hosts.

### 2. The network

The networking module creates the virtual network and one subnet. The NSG has one rule, which denies inbound traffic from the internet. Outbound traffic is not restricted. The session hosts need outbound access to reach AVD and to download the agent, so the lab leaves it open.

### 3. The storage account

The storage account is Standard tier with ZRS. It requires TLS 1.2 or newer, and its blobs cannot be public. Its directory type is `AADKERB`, the Terraform name for Microsoft Entra Kerberos. The default share-level permission is `None`, so nobody gets in until a role assignment (see "The access roles" below) gives their group access.

### 4. The session hosts

For each session host, the `session-hosts` module creates a network card and a Windows VM from the Marketplace image. Each VM uses Secure Boot and a virtual TPM, the Windows client license that Windows 11 needs, and a system-assigned managed identity (an identity that Azure creates and manages for the VM). Three steps then run on each VM, in this order:

1. **The `AADLoginForWindows` extension** joins the VM to Microsoft Entra ID. Microsoft Entra joined VMs do not need line of sight to a domain controller. A host pool should hold VMs of one join type only.
2. **A run command installs the AVD agent.** The script `install-avd-agent.ps1` downloads the AVD agent and the boot loader (the second installer, which starts the agent). It installs the agent with the registration key. If the boot loader service already exists, the script instead sets `IsRegistered` to 0, writes the new key into the agent's registry settings and restarts the service.
3. **A run command configures FSLogix.** The script `configure-fslogix.ps1` stops with an error if the FSLogix service (`frxsvc`) is missing, because it expects an image that already has FSLogix installed. [FSLogix comes pre-installed on all available Windows Enterprise multi-session images](https://learn.microsoft.com/en-us/azure/virtual-desktop/windows-multisession-faq). The script then sets the registry values below.

The FSLogix values are under `HKLM:\SOFTWARE\FSLogix\Profiles`:

| Setting | Value | What it does |
|---|---|---|
| `Enabled` | 1 | Turns FSLogix profile containers on. |
| `VHDLocations` | `\\<storage-account>.file.core.windows.net\profiles` | Where the containers are stored. |
| `VolumeType` | `VHDX` | The container file format. |
| `FlipFlopProfileDirectoryName` | 1 | Names the profile folder `username_SID` instead of the default `SID_username`. |
| `DeleteLocalProfileWhenVHDShouldApply` | 1 | Deletes any local profile the user already has on the VM, so the container is used instead. This can lose data. It is fine for a lab, and the documentation suggests it for tests. |

Two more values make Microsoft Entra Kerberos work:

| Setting | Where | Value | What it does |
|---|---|---|---|
| `CloudKerberosTicketRetrievalEnabled` | `HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\Kerberos\Parameters` | 1 | Lets the host get a Microsoft Entra Kerberos ticket at sign-in. |
| `LoadCredKeyFromProfile` | `HKLM:\SOFTWARE\Policies\Microsoft\AzureADAccount` | 1 | Lets a user's profile load on a different VM from the one that created it. |

Both match the client settings on the pages [Enable Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable) and [Store FSLogix profile containers on Azure Files using Microsoft Entra ID](https://learn.microsoft.com/en-us/fslogix/how-to-configure-profile-container-entra-id-hybrid). They need a policy refresh or a restart to take effect, and the script prints the same warning.

### 5. The access roles

The `rbac` module gives the Entra group you supply three roles:

| Role | Scope | What it allows |
|---|---|---|
| Desktop Virtualization User | The application group | Seeing and launching the desktop. |
| Virtual Machine User Login | Each session host | Signing in to the Entra joined VM. |
| Storage File Data SMB Share Contributor | The `profiles` file share | Share-level read, write and delete access. |

Terraform assigns these roles to your group. It does not create the group. Create the group first, then put its Object ID in `avd_user_group_object_id`, and add your test users to it yourself.

## Run it

1. Clone the repository and open the folder. Run every command below from there.

   ```bash
   git clone https://github.com/AddySidd27/terraform-azure-avd
   cd terraform-azure-avd
   ```

2. Copy `terraform.tfvars.example` to `terraform.tfvars` and fill in these values:
   - `subscription_id`: your Azure subscription ID.
   - `windows_image_version`: an exact image version that exists in your region. The file warns against `latest`. Find versions with `az vm image list --publisher MicrosoftWindowsDesktop --offer office-365 --sku win11-24h2-avd-m365 --location eastus --all --output table`.
   - `admin_password`: the local administrator password for the VMs, at least 12 characters.
   - `avd_user_group_object_id`: the Object ID of your Entra group.
   - `storage_account_name`: 3 to 24 lowercase letters and numbers, unique across Azure. Change the example value.

   If you leave the placeholder subscription ID, password or group ID in place, `terraform plan` stops with an error that says which value to fix. Do not commit `terraform.tfvars`, because it holds the VM password. The repository has no `.gitignore` file, so keep this file out of any copy you push.

3. Sign in with `az login`.
4. Run `terraform init` to download the provider, then `terraform validate` to check the files for mistakes.
5. Run `terraform plan -out main.tfplan` and read the plan. Then run `terraform apply main.tfplan`. Saving the plan to a file means the plan you reviewed is exactly the plan that runs. The apply takes several minutes.

The exact Terraform and provider versions are pinned in `versions.tf`.

## Steps Terraform does not do

After `terraform apply`, the repository's post-deployment guide lists steps for the Azure portal. They are manual because they change Microsoft Entra settings that this project does not manage. In order:

1. **Restart both session hosts** so the Kerberos setting applies. Then check that both show **Available** in the host pool.
2. **Add your test users to the Entra group.**
3. **Check that Microsoft Entra Kerberos is on.** In the storage account, open File shares, then Identity-based access.
4. **Grant admin consent** to the storage account's Entra application. In Microsoft Entra ID, open App registrations, then All applications, and search for `[Storage Account] <name>.file.core.windows.net`. Open it, select API permissions, and select **Grant admin consent**.
5. **Check Conditional Access.** Microsoft Entra Kerberos does not support MFA when it gets the ticket for the file share. If a Conditional Access policy requires MFA for all apps, exclude the storage account's application from it. If you do not, mapping the share fails.
6. **Add the `kdc_enable_cloud_group_sids` tag** if your users are cloud-only. On the same application, open Manifest and add the value to the existing `tags` array. This is mandatory for cloud-only identities, and authentication fails without it.
7. **Give yourself admin access to the share.** On the share's Access Control (IAM) page, give the administrator doing the setup the roles Storage File Data SMB Share Elevated Contributor and Storage File Data Privileged Contributor. Without them you cannot do the next step. Remove them after testing.
8. **Set the folder permissions on the share.** On the share, open Browse, then **Manage access**. For cloud-only users, this is the page the documentation points to. Give the Entra group Modify on "This folder only". Then add the security ID `S-1-3-0`, which shows as `CREATOR OWNER`, with Modify on "Subfolders and files only". `CREATOR OWNER` is a built-in Windows identity that owns whatever it creates. These two permissions let each user create a profile folder and use it, without opening other people's profiles.

## Check that it works

The session hosts have no public IP address, so run these commands from the Azure portal: open the VM, select Run command, then RunPowerShellScript. Run them on each host:

```powershell
dsregcmd /status
Get-Service RDAgentBootLoader, RdAgent, frxsvc
Get-Service WinHttpAutoProxySvc, iphlpsvc
Get-ItemProperty 'HKLM:\SOFTWARE\FSLogix\Profiles'
Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\Kerberos\Parameters'
Get-ItemProperty 'HKLM:\SOFTWARE\Policies\Microsoft\AzureADAccount'
```

- `dsregcmd /status` should show `AzureAdJoined : YES`.
- `RDAgentBootLoader`, `RdAgent` and `frxsvc` should exist and run.
- `WinHttpAutoProxySvc` and `iphlpsvc` must be running. Both are required for Microsoft Entra Kerberos.
- FSLogix should show `Enabled = 1` and the right `VHDLocations`. `CloudKerberosTicketRetrievalEnabled` and `LoadCredKeyFromProfile` should both be 1.

Then test as a user:

1. Sign in to the [web client](https://windows.cloud.microsoft/) as a test user from the group, and open the desktop.
2. Create a folder and a text file on the desktop.
3. In the Azure portal, open the `profiles` file share. A folder for the user should appear, named like `jdoe_S-1-12-1-...`, with a `.vhdx` file inside.
4. Sign out fully (Start, then the user icon, then Sign out). Closing the browser tab is not a sign-out.
5. Sign in again and check that the folder and file are still there.

The lab works if both hosts are Available, the user gets a desktop, a profile file appears on the share, and the test file survives a full sign-out and sign-in.

## If something fails

- **`INVALID_REGISTRATION_TOKEN` or `EXPIRED_MACHINE_TOKEN`:** the host does not accept its registration key. The documentation's fix is to create a new key, set `IsRegistered` to 0 and write the new key into the agent's registry settings, then restart the `RDAgentBootLoader` service. See the [agent troubleshooting page](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-agent). After the 24 hours, `terraform apply` makes a new key and passes it to the install script, which is written to do these steps on a host that already has the boot loader.
- **Entra join fails:** read the logs in `C:\WindowsAzure\Logs\Plugins\Microsoft.Azure.ActiveDirectory.AADLoginForWindows`.
- **The profile does not mount:** run the `Get-ItemProperty` commands from the check section again, and run `Get-SmbConnection`. Port 445 must be reachable from the session host to the storage account.

## Clean up

Shut down the session hosts from the Azure portal when you are not using them, so the status says Stopped (deallocated). A VM stopped from inside Windows still costs money. When you are finished, run `terraform destroy`. It also deletes the storage account, so it deletes every profile on the share.

## Before you use this design for real work

The lab leaves out things that production needs. Each of these is a choice in the code that you would change:

- **Public network access to the storage account is on** (`public_network_access_enabled = true`), and the session hosts reach it over the Azure network with no private endpoint. Production usually adds a private endpoint and private DNS. With a private endpoint and Microsoft Entra Kerberos, add the private link FQDN to the storage account's Entra application.
- **The host pool allows public network access** (`public_network_access = "Enabled"`).
- **Outbound traffic is open.** Production usually adds a controlled path out, such as a firewall.
- **The VM password is a variable.** Keep it out of the repository, and use a secret store.
- **The storage account keeps shared key access on** (`shared_key_access_enabled = true`).
- **The Terraform state file holds secrets**, including the VM password and the registration key. Keep it in a protected location.
- **There is no monitoring, backup or image process.** The image is a Marketplace image with a fixed version, and the lab has no plan for updating it.

One more thing to read before you rely on it: the FSLogix page in the documentation carries a warning about an April 2026 Windows Server update that changes the default Kerberos encryption type from RC4 to AES-SHA1. The Azure Files page says that with Microsoft Entra Kerberos the ticket encryption is always AES-256, so this lab should not be affected. Read both pages before you deploy.

For the design behind these choices, read [How FSLogix profile containers work](/azure-virtual-desktop/how-fslogix-profile-containers-work/).

To cut the compute cost of this lab, see [Cut AVD Compute Cost with Autoscale](/terraform-labs/avd-autoscale-cost-lab/). It adds a scaling plan to this same environment.

## Sources

- [Configure Azure Virtual Desktop with Terraform](https://learn.microsoft.com/en-us/azure/developer/terraform/configure-azure-virtual-desktop)
- [Microsoft Entra joined session hosts in Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/azure-ad-joined-session-hosts)
- [Enable Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable)

