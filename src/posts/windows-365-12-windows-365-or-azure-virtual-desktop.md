---
title: "Windows 365 or Azure Virtual Desktop: How to Choose"
layout: post.njk
permalink: /windows-365/windows-365-or-avd/
order: 211
part: 12
tags: w365-series
deck: "Compare the two services on who manages what, price model, scaling, sharing, management and networking, then work through a decision checklist."
---

Microsoft offers two ways to give people a Windows desktop that runs in the cloud: Windows 365 and Azure Virtual Desktop (AVD). Users open either one from an app or a web browser. At that level the two are similar, but they differ in how they are set up and run. This article is for IT staff and architects who must pick one, or pick both. By the end you will be able to say what each service leaves to you, how each is priced, and which one your situation points to.

This article compares Windows 365 Enterprise with AVD running in Azure. Windows 365 Business, Government and Flex are mentioned where they differ. For a closer look at AVD alone, read [Decide Whether Azure Virtual Desktop Fits](/azure-virtual-desktop/decide-whether-azure-virtual-desktop-fits/). For Windows 365 alone, start with [Start Here](/windows-365/start-here/). For the editions side by side, see [Windows 365 Editions](/windows-365/editions/).

## Key terms

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop that Windows 365 creates and hosts for a user. In Windows 365 Enterprise, Business and Government it is that one user's own PC in the cloud. |
| Windows 365 Enterprise | The edition for larger companies. It has unlimited seats, lets you build Cloud PCs from images you create, and is fully integrated with Microsoft Intune. |
| Windows 365 Business | The edition for smaller companies, up to 300 seats, with ready-to-use Cloud PCs and simple management. |
| Windows 365 Government | A Windows 365 service that spans a regulated US Government Community Cloud (GCC) and a public-facing cloud. |
| Windows 365 Flex | A Windows 365 edition for people who need a Cloud PC for a limited time each day. It has two modes. In Dedicated mode, one license provisions up to three Cloud PCs, each for one user, and only one of them can be active at a time. In Shared mode, one license provisions one Cloud PC that a group of users shares, one user at a time. |
| Azure Virtual Desktop (AVD) | A desktop and app virtualization service that runs on Azure. |
| Software as a service (SaaS) | A complete service that the provider delivers end to end. Windows 365 is described this way. |
| Platform as a service (PaaS) | A service that gives you granular control over configuration and management, and asks for more hands-on work in return. AVD is described this way. |
| Control plane | The Azure Virtual Desktop services that connect users to their desktops. They include the gateway, broker and web client services. Windows 365 and AVD both use them. |
| Session host | A virtual machine in AVD that runs the users' desktops or apps. In the standard setup you create and manage it in your Azure subscription. |
| Host pool | A group of AVD session hosts that serve the same kind of desktop or app. |
| Single-session and multi-session | Single-session gives one user a machine. Multi-session lets several users share one machine, which is why it can greatly reduce the number of virtual machines. Windows 11 and Windows 10 Enterprise multi-session is a version of Windows built for this. |
| RemoteApp | A way to publish one app to users instead of a full desktop. |
| Autoscale | An AVD feature that adds or removes capacity by time of day, day of the week, or demand. |
| FSLogix | A tool that keeps a user's profile (settings and files) in a container so it follows the user between machines. |
| Microsoft Intune | Microsoft's cloud service for managing devices. Windows 365 Enterprise Cloud PCs are managed in it. |
| Microsoft Entra ID | Microsoft's cloud-based identity and access management service. Windows 365 uses it for identity and access control. |
| Azure subscription | Where you create and manage Azure resources. The cost of those resources is billed to it. |
| Virtual network | A private network in Azure. It lets Azure resources such as virtual machines talk to each other, the internet and on-premises networks. |
| VPN and ExpressRoute | Two ways to connect your on-premises network to Azure. ExpressRoute is a private connection that does not go over the public internet. |
| Microsoft-hosted network | A Windows 365 network option. Microsoft runs the network for the Cloud PCs, so you do not need your own Azure subscription or virtual network. |
| Azure network connection (ANC) | A Windows 365 network option. The Cloud PC's network interface goes into a virtual network that you own and manage in your Azure subscription. |
| Microsoft Entra join and hybrid join | Entra join: the machine joins Microsoft Entra ID only. Hybrid join: the machine joins your on-premises Active Directory and Microsoft Entra ID, and needs line of sight (a network path) to your domain controllers. |
| Provisioning policy | A Windows 365 setting in the Microsoft Intune admin center that controls how Cloud PCs are created: the network, the image, and the Microsoft Entra user groups that get Cloud PCs. |
| Image | The Windows image a machine is built from. Windows 365 offers gallery images or your own. AVD lets you bring your own image or start from the Azure Gallery. |
| AVD Hybrid and AVD for Azure Local | Ways to host AVD desktops and apps on-premises, on the hypervisor of your choice. |
| Per-user licensing | You buy a license per user for a fixed monthly fee, whatever their use. Windows 365 licenses work this way. Flex licenses are pooled at the tenant level instead. |
| Consumption-based pricing | You pay for what you use, so the bill changes with use. |

## What the two have in common

Both run on Azure's cloud, use the same global control plane, and give users virtual Windows desktops ([Compare Windows 365 Cloud PCs to Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/examine-windows-365/3-compare-windows-365-azure-virtual-desktop)). Windows 365 uses the AVD gateway, connection broker and web client services to connect users to Cloud PCs ([Windows 365 Azure network connection](https://learn.microsoft.com/en-us/azure/architecture/virtual-desktop/windows-365-azure-network-connection)).

The difference is how much you run yourself.

## What Microsoft manages and what you manage

Windows 365 is a SaaS service. AVD is a PaaS service. In practice this means AVD gives you more control, and asks for more hands-on work in return. Windows 365 aims for simple, ready-to-use desktops that need less expertise to deploy and manage ([Compare Windows 365 Cloud PCs to Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/examine-windows-365/3-compare-windows-365-azure-virtual-desktop)).

![Side-by-side view of Windows 365 and Azure Virtual Desktop. Both use the same Azure Virtual Desktop connection services. It lists what Microsoft manages, what you manage and the price model for each.](/img/windows-365/windows-365-or-avd.svg)

*Source: [Windows 365 Azure network connection](https://learn.microsoft.com/en-us/azure/architecture/virtual-desktop/windows-365-azure-network-connection), [What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview) and [Compare Windows 365 Cloud PCs to Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/examine-windows-365/3-compare-windows-365-azure-virtual-desktop).*

The Windows 365 side of the diagram shows the recommended setup: a Microsoft-hosted network, Microsoft Entra join, and gallery images with Windows Autopatch. With that setup, Microsoft manages the Cloud PC virtual machines, the Cloud PC infrastructure, the virtual network and routing, and the Azure subscription and resource groups. These are in an Azure subscription that Microsoft owns, not yours. Microsoft also runs the Intune service itself. You manage Microsoft Entra ID, Azure DNS, the guest operating system (Windows) and your apps on the Cloud PC, and Cloud PC security. You also set the policies in Intune ([Windows 365 Azure network connection](https://learn.microsoft.com/en-us/azure/architecture/virtual-desktop/windows-365-azure-network-connection)).

If you use an Azure network connection instead, you also manage your own Azure subscription, resource groups, virtual network and routing, and any VPN or ExpressRoute connection. Microsoft still manages the Cloud PC virtual machines.

On the AVD side, you create the environment in your own Azure subscription. You manage the image and the virtual machines that run the sessions. You do not manage the supporting infrastructure such as the gateway or broker ([What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)). The AVD hosts, their disks, profile storage with FSLogix and the virtual network are customer-managed ([Compare Windows 365 Cloud PCs to Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/examine-windows-365/3-compare-windows-365-azure-virtual-desktop)). The organization that pays for an AVD deployment is also responsible for managing its Azure resources and their costs. The Windows 365 lists follow Microsoft's responsibility matrix. The AVD list shows the items that the AVD pages name as yours. For how this looks when something breaks, see [How Azure Virtual Desktop Fails](/azure-virtual-desktop/how-azure-virtual-desktop-fails/).

## The two compared

| Question | Windows 365 | Azure Virtual Desktop |
|---|---|---|
| Service model | SaaS: a complete, end-to-end Microsoft service | PaaS: granular controls over configuration and management |
| Who gets a machine | One user per Cloud PC in Enterprise, Business and Government. Flex works differently (see Multi-session and sharing) | Single-session or multi-session, with pooled desktops and RemoteApp |
| Operating systems | Windows 10 and Windows 11 | Windows 11, Windows 10 (single- or multi-session) and Windows Server |
| How machines are created | Automatic: a Cloud PC is created when you assign a license to a user who is in a Microsoft Entra user group that a provisioning policy covers | Manual provisioning: you create the session hosts and manage the host pools |
| Compute | Microsoft-managed, fixed cost, no access to the VMs. You still manage Windows and your apps inside the Cloud PC | Customer-managed, usage-based cost, flexible |
| Price model | A fixed monthly fee per licensed user, whatever the usage (Flex licenses are pooled) | Consumption-based |
| Management tools | Microsoft Intune (Enterprise) | Azure portal, Intune and PowerShell |
| Network | Microsoft-hosted network (no Azure subscription needed) or an Azure network connection (ANC) | A virtual network that you manage (for session hosts in Azure) |

## Pricing model

Prices change, so this article compares how each service is priced, not the amounts. The right comparison uses your own numbers.

Windows 365 licenses are bought per user for a fixed monthly fee. Your organization does not have to manage the variability of compute and storage costs. The price is fixed for the plan, regardless of usage. Additional costs may apply based on network usage. With a Microsoft-hosted network you do not pay to run virtual networks or bandwidth for your Cloud PCs. With an ANC you pay for your own network resources, such as bandwidth, Azure Firewall and NAT gateways. Windows 365 Flex licenses are pooled at the tenant level, and the number you buy sets how many Cloud PC sessions can be active at once.

AVD costs come from two places: Azure resource consumption and licensing. Consumption covers the session host virtual machines, their disks and network bandwidth, and also storage and identity services you add. For internal users you must also buy an eligible license for each user who accesses AVD. Internal users are people in your own organization, such as employees, students or contractors. Autoscale, Azure savings plans and reserved VM instances can lower compute costs.

Neither model is cheaper in every case. AVD's flexible pricing may be more efficient in some cases. Which one costs less depends on how you plan and forecast your usage ([Compare Windows 365 Cloud PCs to Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/examine-windows-365/3-compare-windows-365-azure-virtual-desktop)).

## Scaling

**Windows 365.** A Cloud PC is created when you assign a Windows 365 license to a user in an appropriate Microsoft Entra user group. Admins do not create Cloud PCs by hand. Windows 365 Enterprise is for larger companies and has unlimited seats. Windows 365 Business is for companies of up to 300 seats. With a Microsoft-hosted network, Microsoft manages scale, so you can add large numbers of Cloud PCs on demand without first growing network infrastructure. With an ANC, scale depends on the network infrastructure that you own and manage.

**AVD.** You can use autoscale to increase or decrease capacity based on time of day, specific days of the week, or as demand changes. This helps manage cost ([What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)).

## Multi-session and sharing

Windows 11 and Windows 10 Enterprise multi-session is available only in AVD. It lets you greatly reduce the number of virtual machines and operating system overhead while still giving users the same resources ([What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)). AVD can also give individual ownership through personal (persistent) desktops, and it can publish single apps with RemoteApp.

In Windows 365 Enterprise, Business and Government, each user has a 1:1 relationship with their Cloud PC. Windows 365 Flex is different. In Shared mode, a group of users share one Cloud PC, one at a time, and user data is deleted when each user signs out. In Dedicated mode, one license can provision up to three Cloud PCs, each for one user, and only one of them can be active at a time. In Shared mode you can also give users Cloud Apps instead of the full desktop.

For apps published one at a time in AVD, see [Deliver Applications with RemoteApp and App Attach](/azure-virtual-desktop/deliver-applications-remoteapp-app-attach/). For how AVD pools are planned, see [Plan Your Host Pools](/azure-virtual-desktop/plan-your-host-pools/).

## Management

Windows 365 Enterprise Cloud PCs are managed in Microsoft Intune like any other supported device, including configuration, apps and updates. You choose a built-in image or create your own. The series covers this in [Manage Settings, Apps, Updates and Restart](/windows-365/manage-intune/) and [Operate, Roll Out and Extend](/windows-365/operate-and-extend/).

AVD gives you more to manage. You use tools such as the Azure portal, Azure CLI and Azure PowerShell to create and configure host pools and to publish desktops and apps to users. You bring your own image for production, or start from the Azure Gallery ([What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)). See [Build and Maintain a Golden Image](/azure-virtual-desktop/build-and-maintain-a-golden-image/) for the image work this involves.

AVD can also host desktops and apps on-premises, on the hypervisor of your choice, with AVD Hybrid or AVD for Azure Local.

Citrix and VMware integration is listed as an AVD capability ([Compare Windows 365 Cloud PCs to Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/examine-windows-365/3-compare-windows-365-azure-virtual-desktop)). Windows 365 Enterprise also supports Citrix and Omnissa partner connections, so check both before you rule out Windows 365 for a Citrix or Omnissa shop.

## Networking

For Windows 365 you pick one of two network options. Microsoft recommends the Microsoft-hosted network for most scenarios. You only choose the region, and Microsoft runs the rest. It is not compatible with Microsoft Entra hybrid join and it has no direct connection to on-premises Active Directory. It needs cloud-native management with Intune rather than Group Policy. Use a VPN or a Private Access solution to reach on-premises apps.

Use an ANC when you need Microsoft Entra hybrid join, direct line of sight to on-premises resources, or privately managed connectivity. An ANC needs an Azure subscription and Azure networking skills. You then own the design and operation of addressing, routing, DNS and security controls. The two options can run side by side in one tenant, chosen per provisioning policy ([Windows 365 Azure network connection](https://learn.microsoft.com/en-us/azure/architecture/virtual-desktop/windows-365-azure-network-connection)). [Choose Identity and Network](/windows-365/identity-network/) walks through this choice.

AVD session hosts in Azure use a virtual network that you manage. Users connect through reverse connections to the service, so you do not need to open inbound ports ([What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)). The AVD planning side is in [Plan AVD Networking](/azure-virtual-desktop/plan-avd-networking/).

## Decision checklist

Answer each question for each group of users, not for the whole company. A yes in the first rows names a capability that points to AVD. A yes in the other rows is a leaning, not a rule.

| Question | If yes, this points to |
|---|---|
| Should several users share one Windows machine at the same time? | AVD (multi-session) |
| Do you need Windows Server as the desktop operating system? | AVD |
| Do you need to publish single apps (RemoteApp) rather than full desktops? | AVD. Windows 365 Flex in Shared mode can also give users Cloud Apps |
| Do you need Citrix or VMware integration? | AVD lists it as a capability. Windows 365 Enterprise also supports Citrix and Omnissa partner connections, so check both |
| Must the machines run on your own on-premises hypervisor? | AVD Hybrid or AVD for Azure Local |
| Do you want Microsoft to create each user's machine when you assign a license? | Windows 365 |
| Is one dedicated Cloud PC per user enough? | Windows 365 |
| Do you want a fixed monthly fee per user, whatever their usage? | Windows 365 Enterprise or Business |
| Do you want to avoid running a virtual network, session hosts and scaling rules, and can you use Microsoft Entra join? | Windows 365 with a Microsoft-hosted network |
| Can you manage machines with Intune and move Group Policy settings to Intune? | Windows 365 with a Microsoft-hosted network |
| Do you want to pay by consumption and tune capacity yourself? | AVD |
| Do you have no team with Azure networking skills? | Windows 365 with a Microsoft-hosted network. An ANC needs Azure networking expertise, and AVD needs more hands-on administration |
| Must the machines join on-premises Active Directory (hybrid join), or reach on-premises systems directly over the network? | Windows 365 with an ANC, or AVD |

If the answers split, you do not have to choose only one. Some organizations use both Windows 365 and AVD, because each suits particular workloads ([Compare Windows 365 Cloud PCs to Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/examine-windows-365/3-compare-windows-365-azure-virtual-desktop)).

## Common mistakes

- **Choosing on price alone.** The two price models behave differently as usage changes. Forecast your own usage first.
- **Assuming Windows 365 needs no network decision.** The Microsoft-hosted network is simple, but it cannot do hybrid join. If you need that, you need an ANC and an Azure subscription.
- **Expecting multi-session in Windows 365.** Windows Enterprise multi-session is available only in AVD. Enterprise Cloud PCs are one per user.
- **Ruling out Windows 365 for Citrix or Omnissa.** Windows 365 Enterprise supports Citrix and Omnissa partner connections. Check them before you decide.
- **Forgetting AVD licensing.** For internal users, each person who accesses AVD needs an eligible license, on top of the Azure consumption costs.
- **Treating it as one choice for everyone.** You can use both, and you can mix Windows 365 network options by provisioning policy.

## How to validate this in your environment

1. **Estimate the AVD cost with your own numbers.** Open the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/), select the **Compute** tab, then **Azure Virtual Desktop**. Enter your expected compute, storage and networking use, the number of users, total hours and concurrency (how many users are signed in at the same time). Add your license cost separately for internal users.
2. **Get the Windows 365 per-user price for the plan you need.** Use [Windows 365 plans and pricing](https://www.microsoft.com/windows-365/all-pricing?rtc=1) and multiply by your user count. Note any network usage costs.
3. **Run a small Windows 365 pilot.** Follow [Plan the Pilot](/windows-365/plan-the-pilot/) and [Provision](/windows-365/provision/) with a small group of test users. Check that assigning the license to a user in a group your provisioning policy covers creates a Cloud PC.
4. **Run a small AVD pilot.** Follow [Plan Your Host Pools](/azure-virtual-desktop/plan-your-host-pools/) with a few users. Note how many steps you did by hand.
5. **Compare what your team had to do.** List the work each pilot needed: network, image, scaling, patching, support. Match it against the "what you manage" column of the diagram.

## Sources

- [Compare Windows 365 Cloud PCs to Azure Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/examine-windows-365/3-compare-windows-365-azure-virtual-desktop)
- [Windows 365 Azure network connection](https://learn.microsoft.com/en-us/azure/architecture/virtual-desktop/windows-365-azure-network-connection)
- [What is Azure Virtual Desktop?](https://learn.microsoft.com/en-us/azure/virtual-desktop/overview)
