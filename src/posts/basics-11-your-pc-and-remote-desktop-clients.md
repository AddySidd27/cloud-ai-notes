---
title: "Your PC and the Remote Desktop Clients: Get Ready to Connect to a Windows VM"
seoTitle: "Azure Windows VM: Check Your PC and RDP Clients"
layout: post.njk
permalink: "/azure-basics-labs/your-pc-and-remote-desktop-clients/"
order: 321
tags: [azure-basics-lab]
deck: "You check that your Windows PC can sign in to an Azure VM with a Microsoft Entra account, pick route A, B or C for Lab 12, install Windows App and test an .rdp file safely."
description: "Beginner Azure lab: check your Windows version, read dsregcmd /status, compare the three Remote Desktop clients and test an .rdp file safely."
---

By the end of this lab you will know whether your PC can sign in to an Azure VM with a Microsoft Entra account, and which of three routes (A, B or C) you will use in Lab 12. You will also have Windows App installed and will have seen Remote Desktop Connection open a saved `.rdp` file. Nothing is created in Azure and nothing costs money.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

You need a Windows 10 or Windows 11 PC for Labs 12, 14, 15 and 18. On a Mac you can still do Labs 11 to 13, 16, 17 and 19, but not the sign-in steps. Windows App also exists for macOS, but this series does not test it.

Labs 11 to 19 take about eight hours in total, plus waiting time. Plan five sessions: (1) Labs 11 and 12, (2) Lab 13 and the first half of Lab 14, (3) the second half of Lab 14 and Lab 15, (4) Labs 16 and 17, (5) Lab 18 and Lab 19. Each lab says where it is safe to stop.

Remote Desktop Protocol (RDP) is the way Windows shows you another computer's screen over a network. An `.rdp` file is a small saved connection that tells a Remote Desktop client where to connect.

The virtual machine (VM) comes in [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/). This lab makes sure the PC in front of you is ready for it. A PC that cannot sign in is the most common reason a new VM looks broken.

## What you need

- A Windows 10 or Windows 11 PC that you are allowed to install an app on. Check the current requirements on Learn's [What is Windows App?](https://learn.microsoft.com/en-us/windows-app/overview) page before you install.
- Internet access to the Microsoft Store, or to the download link on Learn's "What's new in Windows App" page.
- Time: about 20 minutes. Cost: nothing.
- The name of the throwaway tenant from [Lab 1: Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/). You compare it with what your PC shows in Part 2.
- No Azure sign-in is needed. A personal Microsoft account does not work for Windows App sign-in.
- Nothing from Labs 2 to 10 is used in this lab. Lab 12 uses them.

## Safety first

- Do not open an `.rdp` file that you did not expect, even if the email looks right. Learn says attackers send `.rdp` files in phishing emails, and that such a file can share your clipboard, drives and camera with the remote computer. In this lab you only open a file you made yourself, and you cancel before connecting.
- Do not register or join your work PC to the throwaway tenant. Do not change any join setting on a PC that belongs to your employer. In this lab you only read the state.
- Do not turn on Remote Desktop on your own PC, and do not open port 3389 on your home router. This lab is about connecting out to a VM, not letting people in.
- Do not sign in to Windows App with a personal Microsoft account. It does not work, and you do not need to sign in for this lab.

## What the lab builds

![A diagram with one idea: check your PC, then pick a client. The Windows PC card is numbered 1 winver, 2 dsregcmd /status, 3 pick a client. Three clients follow. Remote Desktop Connection (mstsc.exe) and Windows App both reach the Windows VM vm-azb-win01 over RDP on TCP port 3389; the VM is drawn dashed because you create it in Lab 12. The web browser client is crossed out because it only works for Azure Virtual Desktop and Windows 365. Below, a Microsoft Entra ID box says your PC and the VM must be in the same directory.](/img/basics/your-pc-and-remote-desktop-clients.svg)

*Source: [Sign in to a Windows virtual machine in Azure by using Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-windows), [Get started with Windows App](https://learn.microsoft.com/en-us/windows-app/get-started-connect-devices-desktops-apps) and [Troubleshoot devices by using the dsregcmd command](https://learn.microsoft.com/en-us/entra/identity/devices/troubleshoot-device-dsregcmd). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

There are no Azure portal steps in this lab, on purpose. The work happens on your PC. Part 5 is only a preview of where the `.rdp` file comes from in Lab 12. Do not look for the VM yet.

### Part 1: Check your Windows version

1. On your PC, type **winver** in the search box on the taskbar and select it. A window opens with your edition and version.
2. Write down the Windows name (Windows 10 or Windows 11), the version (for example 22H2 or 24H2) and the OS build number. The same facts are under **Start** > **Settings** > **System** > **About**.

Check: you have a Windows name (Windows 10 or 11) and a version. That is all you need here. Windows Home is fine, because it can be a client even though it cannot be the target of a Remote Desktop connection.

### Part 2: Is your PC known to Microsoft Entra ID?

Microsoft Entra ID is the sign-in service from Lab 1 and Lab 4. Your tenant is your own copy of it. Learn says remote connection to a VM that uses Entra sign-in is allowed only from a Windows 10 or later PC that is in the **same directory** (tenant) as the VM. "Known to Entra ID" means one of three states:

| State | In plain words |
|---|---|
| Microsoft Entra registered | You added a work or school account to the PC, but you still sign in to Windows with your own account. Often a personal PC. |
| Microsoft Entra joined | Windows itself signs in with a work or school account. The PC belongs to the organisation. |
| Microsoft Entra hybrid joined | The PC is joined to an on-premises Active Directory domain and is also known to Entra ID. |

An on-premises domain is a company's own server-based sign-in system inside an office. A home PC is almost never in one. A PC that is only in such a domain is not known to Entra ID.

The command that tells you is `dsregcmd /status`. Run it as yourself: Learn says one field can show an error in an elevated window (one opened with **Run as administrator**).

3. Open **Command Prompt** or **Windows PowerShell** as yourself. Do not choose **Run as administrator**.
4. Type this as one line, including the `|` character. It shows only the lines you need.

```
dsregcmd /status | findstr /i "AzureAdJoined EnterpriseJoined DomainJoined DomainName WorkplaceJoined TenantName TenantId"
```

You see lines like the ones below. Yours will differ. A plain home PC shows all NO and no tenant name.

```
AzureAdJoined : NO
EnterpriseJoined : NO
DomainJoined : NO
WorkplaceJoined : NO
```

Do not paste this output in a forum. It can contain your tenant ID.

5. Read the result with this table.

| AzureAdJoined | DomainJoined | WorkplaceJoined | Your PC is |
|---|---|---|---|
| YES | NO | any | Microsoft Entra joined |
| YES | YES | any | Microsoft Entra hybrid joined |
| NO | NO | YES | Microsoft Entra registered |
| NO | YES | NO | Domain joined only. Not known to Entra ID. |
| NO | NO | NO | Not known to Entra ID |

6. Find which tenant the PC is in. `TenantName` and `TenantId` show only for a joined or hybrid joined PC. For a registered PC, open **Start** > **Settings** > **Accounts** > **Access work or school** and read the account name. Compare it with the tenant name you wrote down in Lab 1.

7. Pick your route. Write the letter in your notes. Lab 12 asks for it.

| What you found | Route |
|---|---|
| The PC is registered, joined or hybrid joined, and the tenant is your throwaway tenant. | **A.** Lab 12 uses the normal sign-in. |
| The PC is not known to Entra ID (all NO), it is your own personal PC, and you are willing to register it. | **B.** Register it as shown below, then sign in as in route A. |
| The PC belongs to another organisation's tenant, or to an employer, or you cannot or do not want to register it. | **C.** Lab 12 uses the web account setting and one extra line in the `hosts` file of this PC. That file needs administrator rights. If you cannot change it, do Lab 12 from a personal PC and choose B. |

**Only if you chose B: register your personal PC.** Open **Settings** > **Accounts** > **Access work or school** and select **Connect**. Sign in with your admin account of the throwaway tenant. Registering adds the account to that page. It does not join the PC and does not let anyone manage it. Registration is per Windows user profile. Read every prompt: if one offers to join the PC to Microsoft Entra ID, or to let the organisation manage it, cancel and choose route C. You can undo registration on the same page with **Disconnect**. Never do this on a PC your employer manages.

Route C works because Learn describes a second way in. The setting **Use a web account to sign in to the remote computer** in Remote Desktop Connection needs no registration or join. It has two conditions: you connect by computer name, not by IP address, and the name must match the VM's host name in Entra ID and resolve to the VM's IP address. That is why route C needs the `hosts` line. You will see the setting in Part 4.

### Part 3: The three ways in

| Way | What it is | Use it for a plain Azure Windows VM? |
|---|---|---|
| Remote Desktop Connection | Built into Windows. The file is `mstsc.exe`. Start it from the Start menu. Learn's Entra sign-in steps for a VM use this one. | Yes. Lab 12 uses it. |
| Windows App | Microsoft's current client, free from the Microsoft Store. It can connect to a remote PC by name or IP address without signing in to Windows App. It is the main client for Azure Virtual Desktop (AVD). | Yes, but this series uses mstsc for the plain VM. |
| The web | Windows App in a browser at `https://windows.cloud.microsoft/`. Nothing to install. | No. Learn says the browser connects to Azure Virtual Desktop, Windows 365 and Microsoft Dev Box, and marks "Remote PC" as not supported there. |

Do not install an older "Remote Desktop" app. Use Windows App. The [article on choosing the AVD client](/azure-virtual-desktop/choose-the-avd-client/) has the dates and the status of each client.

Azure Bastion opens a VM in the browser, but it bills by the hour from the moment you create it. This series does not use it.

### Part 4: Install Windows App and test an `.rdp` file

8. Install Windows App. Open the Microsoft Store and search for **Windows App**. Check that the publisher is Microsoft. If your PC cannot use the Store, use the download link on Learn's "What's new in Windows App" page. Open it once to see the welcome page. If it shows a sign-in page, close the app. That is enough. You will use it for AVD later.
9. Make a test `.rdp` file. Open **Remote Desktop Connection** from the Start menu and select **Show Options**. On the **General** tab, type `testpc01` in **Computer**. In the box **Connection settings**, select **Save As**. Choose **Desktop**, name the file `test.rdp` and select **Save**. Close the window without connecting.
10. Double-click `test.rdp`. A warning about remote connections may appear. Learn says that since the April 2026 security update the first time you open an `.rdp` file a short dialog explains the risks. Read it and allow it.
11. A security box shows the computer name `testpc01` and tick boxes for local resources such as drives and the clipboard. Learn says they are off by default. Leave every box unticked and select **Cancel**. You may see "Unknown publisher". That is normal for a file you made yourself. Success: no connection is made.
12. Open Remote Desktop Connection again, select **Show Options**, then the **Advanced** tab. Under **User authentication**, find the box **Use a web account to sign in to the remote computer**. Do not tick it now. You only need to know where it is.

Check: you wrote down your Windows version and your route (A, B or C), `test.rdp` opened the dialogs and you cancelled, and you know where the web account box is.

### Part 5: Preview of Lab 12 (do not do this now)

When a VM exists, Lab 12 gets the `.rdp` file from the portal like this:

- In the Azure portal, open **Virtual machines** and select your VM.
- Select **Connect**, then **Native RDP**. You may need **More ways to connect** first. Keep port 3389.
- Select **Download RDP File**. Learn says to ignore the warning that the file might harm your device. You asked for this file from your own portal, so opening it is right.

## Steps with the Azure CLI

No Azure CLI in this lab, because there is no Azure resource to create or read. The only commands are the ones you ran on your PC (`winver` and `dsregcmd /status`). Lab 12 has the CLI for the VM.

## Terraform

No Terraform in this lab, because nothing is deployed.

## Check that it works

- You can say your Windows name, version and build.
- You wrote down A, B or C, and the tenant name if the output showed one.
- Windows App opens and shows its welcome page.
- Double-clicking `test.rdp` opened a Remote Desktop Connection dialog, and you cancelled it with every resource box left unticked.
- You know where the **Use a web account to sign in to the remote computer** box is.

## The most common mistake

Using the wrong client or the wrong PC. Four cases cover most of it.

- Using a browser or the web version of Windows App for a plain VM. It connects to AVD, Windows 365 and Dev Box only.
- Using a work PC from another tenant without the web account setting. The Entra sign-in works only from a PC in the same directory as the VM.
- Using an IP address together with the web account setting. Learn says an IP address cannot be used with that option.
- Believing that `mstsc.exe` works for AVD. The [AVD client article](/azure-virtual-desktop/choose-the-avd-client/) says it is not supported for AVD. For a plain VM with Entra sign-in it is the client Learn uses.

### If you cannot connect later

Go from the top. The full list is in [Lab 19: When something breaks](/azure-basics-labs/when-something-breaks/).

| What to check | Where to look |
|---|---|
| The VM is running. | VM **Overview**: the status must say **Running**. If not, select **Start**. |
| The VM has a public IP address. | VM **Overview**: **Public IP address**. |
| The network security group allows TCP 3389 from your IP address. | VM **Networking**. See [Lab 9](/azure-basics-labs/network-security-group/). |
| You have a sign-in role. | You need **Virtual Machine User Login** or **Virtual Machine Administrator Login**. Owner or Contributor does not give sign-in. See [Lab 7](/azure-basics-labs/rbac-roles/). |
| Your PC fits your route, and the user name has the right form. | Part 2. A registered PC must use `AzureAD\` plus the full sign-in name, for example `AzureAD\john@contoso.com`. Some office or hotel networks block outbound TCP 3389. |

## Clean up

Nothing in Azure to delete.

On your PC:

- Delete `test.rdp` from the Desktop.
- Keep Windows App.
- If you registered your PC (route B), keep that until Lab 12 is done. To undo it later, go to **Settings** > **Accounts** > **Access work or school**, select the account and select **Disconnect**.

Keep for later labs: your notes (Windows version, route A, B or C, tenant name) and Windows App.

State at the end of this lab: no VM exists yet. Lab 12 creates it.

## Where this is used in AVD

AVD users connect with Windows App on most platforms or with the web version, not with `mstsc.exe`, and they must sign in with a work or school account. In Lab 12 you connect straight to a VM's public IP on port 3389. In AVD the session host has no public IP and no inbound rule: Windows App connects through the AVD service. The full list of clients and retirement dates is in [Choose the Client: Windows App, Remote Desktop and the Web](/azure-virtual-desktop/choose-the-avd-client/).

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
