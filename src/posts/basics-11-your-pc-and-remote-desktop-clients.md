---
title: "Your PC and the Remote Desktop Clients: Get Ready to Connect to a Windows VM"
seoTitle: "Azure Windows VM: Check Your PC and RDP Clients"
layout: post.njk
permalink: "/azure-basics-labs/your-pc-and-remote-desktop-clients/"
order: 321
tags: [azure-basics-lab]
deck: "You check your Windows version and whether your PC is known to Microsoft Entra ID, install Windows App, and prove that Remote Desktop Connection opens an .rdp file."
description: "Beginner Azure lab: check your Windows version, read dsregcmd /status, compare the three Remote Desktop clients and test an .rdp file safely."
---

By the end of this lab you will know which Windows version your PC runs and whether your PC is registered, joined or hybrid joined to Microsoft Entra ID. You will have Windows App installed, and you will have seen Remote Desktop Connection open a saved `.rdp` file. You will also have a checklist for the day a connection to a Windows VM does not work.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

Remote Desktop Protocol (RDP) is the way Windows shows you another computer's screen over a network. An `.rdp` file is a small saved connection that tells a Remote Desktop client where to connect.

You create nothing in Azure in this lab. The virtual machine (VM) comes in [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/). This lab makes sure the PC in front of you is ready for it. A PC that cannot sign in is the most common reason a new VM looks broken.

## What you need

- A Windows PC that you are allowed to install an app on. Windows 10 or Windows 11. Learn says Windows App needs Windows 11, Windows 10 version 1809 or later, or Windows Server 2019 or later. A device that runs a Windows 10 version out of mainstream support must be in the Extended Security Updates programme, says Learn.
- Internet access to the Microsoft Store, or to the download link on Learn's "What's new in Windows App" page. Learn also says the device must be actively supported by its manufacturer.
- Time: about 20 minutes. Cost: nothing.
- No Azure sign-in is needed for the steps in this lab. A Microsoft work or school account is needed only for later labs. A personal Microsoft account does not work for Windows App sign-in.
- The earlier labs matter for Lab 12, not for this one. Lab 12 asks for the result you write down in Part 2 (A or B): [Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/) for `testuser1`, [Lab 7: RBAC roles](/azure-basics-labs/rbac-roles/) for the sign-in roles, and [Lab 9: Network security group](/azure-basics-labs/network-security-group/) for the RDP rule.

## Safety first

- Do not open an `.rdp` file that you did not expect, even if the email looks right. Learn says attackers send `.rdp` files in phishing emails, and that such a file can share your clipboard, drives and camera with the remote computer.
- In this lab you only open a file you made yourself, and you cancel before connecting.
- Do not register or join your work PC to the throwaway tenant. Do not change any join setting on a PC that belongs to your employer. In this lab you only read the state.
- Do not turn on Remote Desktop on your own PC, and do not open port 3389 on your home router. This lab is about connecting out to a VM, not letting people in.
- Do not sign in to Windows App with a personal Microsoft account. It does not work, and you do not need to sign in for this lab.

## What the lab builds

![A left-to-right diagram. A Windows PC at the left has three ways to reach a Windows virtual machine in Azure: Remote Desktop Connection (mstsc), Windows App, and a web browser. The first two arrows go to the VM, which is drawn with a dashed outline and the note "created in Lab 12". The browser arrow is marked as working for Azure Virtual Desktop and Windows 365, not for a plain VM. A box beside the PC says dsregcmd and winver check the PC before you connect.](/img/basics/your-pc-and-remote-desktop-clients.svg)

*Source: [Sign in to a Windows virtual machine in Azure by using Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-windows), [Get started with Windows App](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps) and [Troubleshoot devices by using the dsregcmd command](https://learn.microsoft.com/en-us/entra/identity/devices/troubleshoot-device-dsregcmd). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

There are no Azure portal steps in this lab, on purpose. Nothing is created in Azure. The work happens on your PC, and the portal only matters once a VM exists. Part 5 below shows where the `.rdp` file comes from, so you know the click path before Lab 12. Do not look for the VM yet.

### Part 1: Check your Windows version

1. On your PC, type **winver** in the search box on the taskbar and select it. Learn gives this as a quick way to see your version. A window opens with your edition and version.
2. Write down the Windows name (Windows 10 or Windows 11), the version (for example 22H2 or 24H2) and the OS build number. You can also see the same facts under **Start** > **Settings** > **System** > **About**, where Learn says you see **Edition**, **Version** and **OS Build**.

Why it matters: Learn says that remote connection to a VM that uses Microsoft Entra sign-in is allowed only from a Windows 10 or later PC. If your PC is only Entra registered (see Part 2), Learn says the minimum build is Windows 10 20H1. Windows 11 is fine.

If your edition is Windows Home, you can still connect out to a VM. Learn says Home cannot be the target of a Remote Desktop connection, but it can be used as a client.

### Part 2: Is your PC known to Microsoft Entra ID?

**Idea 1: three states, plus "none".** Microsoft Entra ID is the sign-in service from Lab 1 and Lab 4. Your tenant is your own copy of it. Entra ID can know about a PC in three ways. Learn calls the PC a device, and the record in Entra ID a device identity.

| State | In plain words |
|---|---|
| Microsoft Entra registered | You added a work or school account to the PC, but you still sign in to Windows with your own account. Often a personal PC. |
| Microsoft Entra joined | Windows itself signs in with a work or school account. The PC belongs to the organisation. |
| Microsoft Entra hybrid joined | The PC is joined to an on-premises Active Directory domain and is also known to Entra ID. |

If none of these fits, the PC is not known to Entra ID. A PC that is only joined to an on-premises domain is not enough.

The command that tells you is `dsregcmd /status`. Learn says to run it in the user's own context, so do not use an elevated window (one that was opened with **Run as administrator**). Learn says one field can show an error when the command runs elevated.

3. Open **Command Prompt** or **Windows PowerShell** as yourself. Do not choose **Run as administrator**.
4. Run this. It shows only the lines you need.

```
dsregcmd /status | findstr /i "AzureAdJoined EnterpriseJoined DomainJoined DomainName WorkplaceJoined TenantName TenantId"
```

5. Read the output with this table. The field names `AzureAdJoined`, `EnterpriseJoined` and `DomainJoined` are in the **Device State** section. `WorkplaceJoined` is in the **User State** section. `TenantName` and `TenantId` are in the **Tenant Details** section.

| AzureAdJoined | DomainJoined | WorkplaceJoined | Your PC is |
|---|---|---|---|
| YES | NO | any | Microsoft Entra joined |
| YES | YES | any | Microsoft Entra hybrid joined |
| NO | NO | YES | Microsoft Entra registered |
| NO | YES | NO | Domain joined only. Not known to Entra ID. |
| NO | NO | NO | Not known to Entra ID |

Learn's table for the first two rows is the device state table (for example, AzureAdJoined YES, EnterpriseJoined NO, DomainJoined NO means Microsoft Entra joined). Learn says the registered state shows in the User State section. The last three rows follow from those fields.

6. Find out which directory (tenant) your PC is in. Learn says the tenant details show only when the PC is joined or hybrid joined, not when it is only registered. The tenant ID is a long string of letters and numbers that names your tenant. If you see `TenantName` and `TenantId`, write them down. For a registered PC, open **Start** > **Settings** > **Accounts** > **Access work or school** and read the account name. Learn lists this page for registered Windows PCs.

**Idea 2: same directory.** This is the rule Lab 12 depends on. Learn says: remote connection to a VM that is joined to Microsoft Entra ID is allowed only from Windows 10 or later PCs that are Microsoft Entra registered (minimum build 20H1), or Microsoft Entra joined, or Microsoft Entra hybrid joined, to the same directory as the VM. Your throwaway tenant is the directory of the VM. So a work PC that is joined to your employer's tenant does not count, because that is a different directory.

Learn also gives a second way, which does not need the PC to be registered or joined. It is the **Use a web account to sign in to the remote computer** setting in Remote Desktop Connection. Learn says that with this option there is no requirement for the local device to be joined to a domain or to Microsoft Entra ID. It has two conditions of its own. You must connect by computer name, not by IP address. And the name must match the VM's hostname in Microsoft Entra ID and resolve to the VM's IP address. You will see the setting in Part 4.

Write down your result as one of these. Lab 12 asks for it:

- **A.** My PC is Entra registered, joined or hybrid joined, and the tenant is the throwaway one. Lab 12 uses the normal sign-in.
- **B.** My PC is in another tenant, or in none (for example, an employer PC). Lab 12 uses the web account setting. You do not need to change the PC.
- **C.** My PC is a personal PC that I want to register to the throwaway tenant. Do the registration below, then you are in case A.

If you want to make a personal PC registered to the throwaway tenant, Learn says registration is done in **Settings** > **Accounts** > **Access work or school**, and that it is per user profile on Windows. You can undo it on the same page with **Disconnect**. This is optional. Learn does not describe every prompt that the Windows sign-in window can show, so read each one. If a prompt offers to join the PC or to let the organisation manage it, stop and use case B instead. Do not do any of this on a PC your employer manages.

### Part 3: The three ways in

**Idea 3: three ways to open a remote session.**

| Way | What it is | Use it for a plain Azure Windows VM? |
|---|---|---|
| Remote Desktop Connection (`mstsc.exe`) | The client built into Windows. Start it from the Start menu or by running `mstsc.exe`. Learn's Entra sign-in steps for a VM use this one. | Yes. This is the one Lab 12 uses. |
| Windows App | Microsoft's current client. It is free from the Microsoft Store. Learn lists it for Windows, macOS, iOS and iPadOS, Android and Chrome OS, web browsers and Meta Quest (preview). | Learn lists a "remote PC" connection by computer name or IP address, which does not need a sign-in to Windows App. It is the main client for Azure Virtual Desktop. |
| The web | Windows App in a browser at `https://windows.cloud.microsoft/`. Nothing to install. | Not for a plain VM. Learn's table says the browser connects to Azure Virtual Desktop, Windows 365 and Microsoft Dev Box, and marks "Remote PC" as not supported there. |

Two more points from Learn. First, you cannot sign in to Windows App with a personal Microsoft account. Second, the older "Remote Desktop" apps are being replaced by Windows App. Do not install an older Remote Desktop client in this series. The [article on choosing the AVD client](/azure-virtual-desktop/choose-the-avd-client/) has the dates and the status of each one.

Azure Bastion is not used in this series. It is a separate Azure service that opens a VM in the browser from the Azure portal. Learn says its hourly charge starts as soon as it is deployed (except the Developer SKU, which Learn calls free and limited to one VM at a time), so it is left out to keep the cost at zero.

### Part 4: Install Windows App and test an `.rdp` file

7. Install Windows App. Open the Microsoft Store and search for **Windows App**. Learn gives the Store listing as `https://apps.microsoft.com/detail/9N1F85V9T8BN`. If your PC cannot use the Store, Learn says you can get it from the "What's new in Windows App" page. Check that the publisher is Microsoft.
8. Open Windows App. Learn's remote PC steps start from the welcome page, where you select **Add a remote PC**. In this lab do not add any PC and do not sign in. Learn says you can connect to a remote PC without signing in to Windows App. Close the app. It is now installed for later.
9. Make a test `.rdp` file. Open **Remote Desktop Connection** from the Start menu. Select **Show Options**. On the **General** tab, type any computer name in **Computer**, for example `testpc01`. In the same tab, look for the **Save** or **Save As** button in the connection settings area, and save the file to your Desktop as `test.rdp`. Close the window without connecting.
10. Open `test.rdp` by double-clicking it. Learn says that since the April 2026 security update, the first time you open an `.rdp` file a short dialog explains the risks of such files. After you allow `.rdp` files in that dialog, it does not appear again for your account. Read it. If your PC does not have that update, you may see an older prompt about an unknown publisher instead, which Learn's connect page calls expected. The next step still applies: do not connect.
11. A security dialog then shows the remote computer's address and a check box for each local resource the file wants, such as drives or the clipboard. Learn says all of these are off by default. Because you made `test.rdp` yourself and did not sign it, Learn says the dialog shows a caution banner for an unknown remote connection with the publisher set to "Unknown publisher". That is normal here. Check that your computer name is shown. Do not tick anything. Select **Cancel** (or close the dialog) so nothing connects.
12. Open Remote Desktop Connection again, select **Show Options**, then the **Advanced** tab. Under **User authentication**, find the box **Use a web account to sign in to the remote computer**. Learn says this is the same as the `enablerdsaadauth` RDP property. Do not tick it now. You only need to know where it is.

### Part 5: Where the `.rdp` file comes from (you do this in Lab 12)

Once a VM exists, Learn gives this path (Lab 12 uses it):

1. In the Azure portal, search for **Virtual machines** and select your VM.
2. Select **Connect**.
3. On the **Connect** page, select **Native RDP**. Learn says it is the top method by default, and that you may need to select **More ways to connect** first. Keep the default IP address and port 3389.
4. Select **Download RDP File**. Learn says to ignore the warning that the file might harm your device. This file is one you asked for, from your own portal, so that is the case where opening it is right.
5. Open the file and select **Connect**. Learn says a warning that the publisher is unknown is expected.

Check: you have written down your Windows version, your Entra state (A, B or C), `test.rdp` opened the Remote Desktop Connection dialogs and you cancelled, and Windows App starts.

## Steps with the Azure CLI

No Azure CLI in this lab, because there is no Azure resource to create or read. The only commands are the ones you ran on your PC (`winver` and `dsregcmd /status`). Lab 12 has the CLI for the VM.

## Terraform

No Terraform in this lab, because nothing is deployed.

## Check that it works

- You can say your Windows name, version and build.
- You can say which of these your PC is: Entra registered, joined, hybrid joined, or none. And you wrote down the tenant if the output showed one. You wrote down A, B or C.
- Windows App opens and shows its welcome page.
- Double-clicking `test.rdp` opens a Remote Desktop Connection dialog, and you cancelled it with every resource box left unticked.
- You know where the **Use a web account to sign in to the remote computer** box is.

## The most common mistake

Using the wrong client or the wrong PC. Four cases cover most of it.

- Using a browser or Windows App's web version for a plain VM. The web version connects to Azure Virtual Desktop, Windows 365 and Dev Box. Learn marks remote PC as unsupported in a browser.
- Using a work PC from another tenant. The Entra sign-in works only from a PC in the same directory as the VM, or with the web account setting.
- Using an IP address together with the web account setting. Learn says an IP address cannot be used with that option.
- Believing that the built-in client works for Azure Virtual Desktop. The [AVD client article](/azure-virtual-desktop/choose-the-avd-client/) says `mstsc.exe` is not supported for AVD. For a plain VM with Entra sign-in, it is the one Learn uses.

### When you cannot connect: a checklist

Go from the top. Each line comes from Learn's pages on RDP to Azure VMs.

| What to check | Where to look | Source |
|---|---|---|
| The VM is running. | VM **Overview**, status should be **Running**. If not, select **Start**. | Connect to a Windows VM |
| The VM has a public IP address. | VM **Overview**, **Networking**. Learn says that without a public IP, RDP needs ExpressRoute or a site-to-site VPN (both are private links from your own network to Azure, not used in this series). | Connect to a Windows VM |
| The network security group allows TCP 3389 from your IP address. | VM **Networking** > **Network settings**. Learn says to look for a rule that allows TCP 3389 from the IP address of the computer you use. See [Lab 9](/azure-basics-labs/network-security-group/). | Connect to a Windows VM |
| Your own network lets outbound TCP 3389 out. | Some office or hotel networks block it. Learn says to check that firewalls on your side allow outbound TCP 3389. | Troubleshoot RDP connections |
| You have the right role. | You need **Virtual Machine Administrator Login** or **Virtual Machine User Login**. Learn says Owner or Contributor does not give sign-in. The error is "Your account is configured to prevent you from using this device." See [Lab 7](/azure-basics-labs/rbac-roles/). | Entra sign-in to a Windows VM |
| Your PC is in the same directory, or you use the web account setting. | Part 2. One error Learn lists for this is "Your credentials didn't work." | Entra sign-in to a Windows VM |
| The user name has the right format. | Learn says a registered PC must use `AzureAD\UPN`, for example `AzureAD\john@contoso.com`. The UPN is the sign-in name that looks like an email address. | Entra sign-in to a Windows VM |
| The password is not temporary. | Learn says a temporary password cannot be used. Sign in once in a private browser window and set a new one. | Entra sign-in to a Windows VM |
| The computer name matches the VM's name in Entra ID. | Learn's error AADSTS293004 comes from a mismatch such as a short name against a full domain name. | Entra sign-in to a Windows VM |
| A Conditional Access policy that requires MFA, or a per-user MFA setting, blocks the sign-in. | Learn gives "The sign-in method you're trying to use isn't allowed" for a Conditional Access policy that requires MFA, and "Your credentials didn't work" when a legacy per-user Enabled or Enforced setting is the cause. See [Lab 5](/azure-basics-labs/mfa/) and [Lab 6](/azure-basics-labs/conditional-access/). | Entra sign-in to a Windows VM |
| A just-in-time policy is set on the VM. | Learn says to select **Request access** first. | Connect to a Windows VM |
| The wrong client. | Part 3. | This lab |

## Clean up

Nothing in Azure to delete.

On your PC:

- Delete `test.rdp` from the Desktop.
- Keep Windows App. You need it again.
- If you registered a personal PC to the throwaway tenant (case C), keep that until Lab 12 is done. To undo it later, go to **Settings** > **Accounts** > **Access work or school**, select the account and select **Disconnect**. Learn says this removes the registered state on Windows 10 and 11.

Keep for later labs:

- Your notes: Windows version, Entra state (A, B or C), tenant name.
- Windows App.

## Where this is used in AVD

AVD users connect with Windows App on most platforms or with the web version, not with `mstsc.exe`, and they must sign in with a work or school account. The full list of clients, feature gaps and retirement dates is in [Choose the Client: Windows App, Remote Desktop and the Web](/azure-virtual-desktop/choose-the-avd-client/).

## Next lab

[Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/) creates a Windows VM, turns on Entra sign-in and connects to it with the client you checked here.

## Sources

- [Sign in to a Windows virtual machine in Azure by using Microsoft Entra ID and Azure RBAC](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-windows)
- [Troubleshoot devices by using the dsregcmd command](https://learn.microsoft.com/en-us/entra/identity/devices/troubleshoot-device-dsregcmd)
- [Microsoft Entra registered devices](https://learn.microsoft.com/en-us/entra/identity/devices/concept-device-registration)
- [Microsoft Entra device management FAQ](https://learn.microsoft.com/en-us/entra/identity/devices/faq)
- [What version of Windows am I running?](https://learn.microsoft.com/en-us/windows/client-management/client-tools/windows-version-search)
- [Get started with Windows App to connect to devices and apps](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps)
- [What is Windows App?](https://learn.microsoft.com/en-us/windows-app/overview)
- [Use the Remote Desktop Connection app to connect to a remote PC using single sign-on with Microsoft Entra authentication](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-connection-single-sign-on)
- [Understanding security warnings when opening Remote Desktop (RDP) files](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/understanding-security-warnings)
- [How to connect using Remote Desktop and sign on to an Azure virtual machine running Windows](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/connect-rdp)
- [Troubleshoot Remote Desktop connections to an Azure virtual machine](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/windows/troubleshoot-rdp-connection)
- [Enable Remote Desktop on your PC](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-allow-access)
- [Choose the right Azure Bastion SKU](https://learn.microsoft.com/en-us/azure/bastion/bastion-sku-comparison)
