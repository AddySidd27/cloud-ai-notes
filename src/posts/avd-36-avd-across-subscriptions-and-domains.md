---
title: "Azure Virtual Desktop Across Several Subscriptions and Domains"
seoTitle: "AVD Across Several Subscriptions and AD Domains"
layout: post.njk
permalink: "/azure-virtual-desktop/multiple-subscriptions-and-domains/"
order: 136
part: 36
tags: [avd-series]
deck: "See which parts of an Azure Virtual Desktop design sit in the tenant, the subscriptions and the domains, and what must be true for sign-in and profiles when you have more than one of each."
description: "How Azure Virtual Desktop uses one Microsoft Entra tenant, several Azure subscriptions and more than one Active Directory domain: identity scenarios, join accounts, the two-way trust for single sign-on, and profile requirements."
---

Large organizations rarely have one subscription and one domain. The network may sit in one Azure subscription, the domain controllers in another, and the host pools in a third. Session hosts may be in a different Active Directory (AD) domain from the users.

This article is for the person who has to draw that design and check it. The terms are explained in the Key terms table just below. It shows which parts of Azure Virtual Desktop (AVD) belong to the Microsoft Entra tenant, which belong to a subscription and which belong to a domain. It also lists what must be true for single sign-on and for profiles. It builds on three earlier articles and links to them instead of repeating them: [Prepare Your Azure Environment](/azure-virtual-desktop/prepare-your-azure-environment/), [Choose the Right Identity Model](/azure-virtual-desktop/choose-the-right-identity-model/) and [Who Can Administer Azure Virtual Desktop](/azure-virtual-desktop/who-can-administer-azure-virtual-desktop/).

## Key terms

| Term | Meaning |
|---|---|
| Microsoft Entra tenant | The organization's cloud directory. It holds user accounts and groups. |
| Subscription | The Azure container where resources are created and billed. |
| Active Directory Domain Services (AD DS) | The Windows directory service that you run yourself, with domain controllers. A domain is one directory of users and computers inside it. |
| Domain controller | A server that checks sign-ins for a domain. |
| Microsoft Entra Domain Services | A managed domain in Azure. Microsoft runs the domain controllers. |
| Session host, host pool, workspace, application group | The main Azure Virtual Desktop resources. They are explained in [Azure Virtual Desktop Architecture](/azure-virtual-desktop/azure-virtual-desktop-architecture/). A session host is a virtual machine that provides desktops and applications. |
| Hybrid identity | A user account that exists in AD DS and is synchronized to Microsoft Entra ID. |
| Microsoft Entra Connect | The tool that synchronizes user data between AD DS and Microsoft Entra ID. |
| Microsoft Entra joined | A computer that is joined directly to Microsoft Entra ID instead of to an AD domain. |
| Microsoft Entra hybrid joined | A computer that is joined to an AD domain and also known to Microsoft Entra ID. |
| UPN | User principal name: the sign-in name of an account, written like an email address. |
| SID | Security identifier: a unique number that Windows gives to every account. |
| Two-way trust | An agreement between two AD domains in which each domain accepts the accounts of the other. |
| Single sign-on (SSO) | Signing in to Windows through Microsoft Entra authentication so the user does not get a second credential prompt. |
| Kerberos server object | An object that hosts need to complete authentication to a domain controller or to reach on-premises resources. The cases are listed in the single sign-on section. |
| Read-only domain controller and Password Replication Policy | The Password Replication Policy on a read-only domain controller sets whose passwords replicate to it. By default it denies this for members of the *Domain Admins* and *Administrators* groups. |
| Intune | A cloud-based service that manages and secures an organization's devices and apps. |
| Azure service names | The subscription table names many Azure services, such as Azure Files and Azure Firewall. Each is a separate service. They show what kind of resource sits in each subscription, and you do not need to know them to follow this article. |
| Resource provider | The service behind a type of Azure resource. AVD uses Microsoft.DesktopVirtualization. |
| Landing zone | An Azure environment that follows a set of design rules and uses subscriptions to separate resources. A platform landing zone holds shared services. A workload landing zone holds one workload such as AVD. |
| FSLogix profile container | Software that keeps a user's Windows profile in a file on a share so the profile follows the user between session hosts. |

## What stays the same

More subscriptions and more domains do not change these rules:

- Microsoft Entra ID is always used to authenticate users for AVD.
- The user account must exist in the Microsoft Entra tenant that you use for AVD. Personal Microsoft accounts are not supported.
- Session hosts must join the same Microsoft Entra tenant as the users, or an Active Directory domain. The domain can be AD DS or Microsoft Entra Domain Services.
- When you use AD DS or Microsoft Entra Domain Services, the user accounts must be hybrid identities. With AD DS you set up Microsoft Entra Connect. With Microsoft Entra Domain Services the synchronization runs one way from Microsoft Entra ID, and it is automatic.
- When you use hybrid identities, either the UPN or the SID must match between AD DS and Microsoft Entra ID.

For how to choose between these join options, see [Choose the Right Identity Model](/azure-virtual-desktop/choose-the-right-identity-model/).

## Identity scenarios

The supported scenarios are listed as rows. Each row has one kind of session host join and one place where the user accounts live.

| Identity scenario | Session hosts | User accounts |
|---|---|---|
| Microsoft Entra ID + AD DS | Joined to AD DS | In Microsoft Entra ID and AD DS, synchronized |
| Microsoft Entra ID + AD DS | Joined to Microsoft Entra ID | In Microsoft Entra ID and AD DS, synchronized |
| Microsoft Entra ID + Microsoft Entra Domain Services | Joined to Microsoft Entra Domain Services | In Microsoft Entra ID and Microsoft Entra Domain Services, synchronized |
| Microsoft Entra ID + Microsoft Entra Domain Services + AD DS | Joined to Microsoft Entra Domain Services | In Microsoft Entra ID and AD DS, synchronized |
| Microsoft Entra ID + Microsoft Entra Domain Services | Joined to Microsoft Entra ID | In Microsoft Entra ID and Microsoft Entra Domain Services, synchronized |
| Microsoft Entra-only | Joined to Microsoft Entra ID | In Microsoft Entra ID, including external identities |

In the fourth row the hosts join Microsoft Entra Domain Services, but the user accounts come from AD DS and are synchronized. Single sign-on has its own host requirements, described below.

The table has no row that describes more than one AD domain for the session hosts. If your design has several domains, do not assume it fits a row. Write down which row each group of users and hosts matches, and test the sign-in before you build more.

## What to check for each domain

Use these facts as a checklist for each domain in your design.

**Where the user accounts live.** Users must be discoverable through Microsoft Entra ID. Identities that exist only in AD DS are not supported.

**How the account is matched.** When you use hybrid identities, either the UPN or the SID must match across AD DS and Microsoft Entra ID. 

**The join details.** When you deploy session hosts into a domain, you enter the domain name and the credentials to join the hosts. You can also enter an organizational unit (OU), which is optional. The account that joins the hosts cannot have multifactor authentication (MFA) turned on. For Microsoft Entra Domain Services, the joining account must be a member of the *AAD DC Administrators* group.

**The network path.** The virtual network of the session hosts must be able to reach the domain controllers and the DNS servers, because the hosts have to join the domain. The virtual network must be in the same Azure region as the session host. In the reference design the domain services sit in the Identity subscription, so the network of the session hosts must be able to reach that subscription. See [Network Topology and IP Planning for AVD](/azure-virtual-desktop/network-topology-and-ip-planning-for-avd/).

**Management with Intune.** If you join session hosts to AD DS and want to manage them with Intune, set up Microsoft Entra Connect for Microsoft Entra hybrid join. Session hosts joined to Microsoft Entra Domain Services cannot be managed with Intune.

## Single sign-on when users and hosts are in different domains

SSO using Microsoft Entra authentication needs hosts that are Microsoft Entra joined or Microsoft Entra hybrid joined. Hosts that are joined only to AD DS, or only to Microsoft Entra Domain Services, are not supported for it.

This is the rule that matters most when there is more than one domain:

> If your Microsoft Entra hybrid joined session hosts are in a different Active Directory domain than your user accounts, there must be a two-way trust between the two domains. Without the two-way trust, connections fall back to older authentication protocols.

Other SSO requirements that depend on the domain setup:

- **Kerberos server object.** The steps are in Microsoft's article on passwordless security key sign-in to on-premises resources. You must create it if the session hosts are Microsoft Entra hybrid joined. You must also create it if the hosts are Microsoft Entra joined and your environment has AD domain controllers, so that users can reach on-premises resources such as SMB shares and sites that use Windows-integrated authentication. Without it on hybrid joined hosts, users may get an error that the session does not exist, or SSO is skipped and they see a standard sign-in dialog.
- **Domain administrator accounts.** On read-only domain controllers, the default Password Replication Policy denies replication for members of *Domain Admins* and *Administrators*. These accounts may be unable to sign in to hybrid joined hosts and may be prompted again and again. The same policy also stops them from reaching on-premises resources that use Kerberos from Microsoft Entra joined hosts. Connecting with a domain administrator account is not recommended.
- **Tenant role.** Whoever configures SSO needs the Application Administrator or Cloud Application Administrator role in Microsoft Entra ID, or an equivalent role.

The steps to turn SSO on are in [How Sign-in Works](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/).

## More than one subscription

In the reference design, AVD is spread over several subscriptions, each with one job. The diagram shows the subscriptions that hold or support AVD. The Management and Security subscriptions are in the table below. The diagram adds the tenant and the domain rule.

![One Microsoft Entra tenant holds the user accounts, synchronized from on-premises AD DS. Identity and Connectivity platform subscriptions support the Azure Virtual Desktop subscription, and a shared services subscription supplies images, monitoring and automation. A bottom panel shows the two-way trust needed for single sign-on between domains.](/img/avd/avd-subscriptions-and-domains.svg)

*Source: [Azure Virtual Desktop landing zone design guide](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/azure-virtual-desktop/design-guide), [Configure single sign-on for Azure Virtual Desktop using Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-single-sign-on) and [Prerequisites for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites).*

In the reference design, AVD uses these subscriptions:

| Subscription | Kind | What it holds |
|---|---|---|
| Azure Virtual Desktop | Workload | Workspaces, application groups, host pools, session hosts, scaling plans, profile storage such as Azure Files, Azure Key Vault and workload-specific networking. |
| Azure Virtual Desktop shared services | Workload | Services shared across several AVD workloads: Azure Automation accounts, data collection rules, Log Analytics workspaces, Azure compute galleries and image management such as Azure VM Image Builder. |
| Identity | Platform | Domain services for domain-joined session hosts: Microsoft Entra Domain Services or self-managed AD domain controllers hosted in Azure. |
| Connectivity | Platform | Virtual networks, network security groups, Azure Firewall, and ExpressRoute or VPN gateways. |
| Management | Platform | Shared management resources. In the reference design it is not an active dependency for AVD, so the workload team builds its own automation, monitoring and management in its own subscription. |
| Security (optional) | Platform | Shared security services such as Microsoft Sentinel and Microsoft Defender for Cloud settings. |

The work is also split into two kinds of landing zones. The platform landing zone supplies shared services such as hub connectivity, Microsoft Entra ID integration, shared firewalls and policy enforcement. The workload landing zone holds the AVD resources: host pools, session hosts, workspaces, application groups, autoscale, FSLogix profile storage, application delivery, App Attach and custom images. Resource placement and responsibilities can vary with an organization's rules, so treat this as a common pattern and not a fixed rule. The reference implementation needs a platform landing zone deployed first.

## Where each setting is made

When several subscriptions and domains are involved, one task can be done in three different places. This table sorts them.

| Task | Where or by whom |
|---|---|
| Register the Microsoft.DesktopVirtualization resource provider | On the subscription: **Subscriptions**, the subscription name, then **Resource providers**. It needs the `*/register/action` permission, which the Contributor and Owner roles include. |
| Azure roles for deploying AVD | Azure role-based access control (RBAC). The roles needed are listed in each deployment article. |
| Join a session host to Microsoft Entra ID | An account that can join computers to the tenant. |
| Join a session host to an AD domain | A domain account that can join computers to that domain. |
| Join a session host to Microsoft Entra Domain Services | A member of the *AAD DC Administrators* group. |
| Configure SSO | A Microsoft Entra role in the tenant: Application Administrator or Cloud Application Administrator. |
| Create the Kerberos server object | Follow the Kerberos server object steps in Microsoft's article on passwordless security key sign-in to on-premises resources. It is needed when the hosts are hybrid joined, or Microsoft Entra joined with domain controllers present. |

The resource provider registration is made for a subscription, so check each subscription where you plan to create AVD resources. The roles in the second row are covered in [Who Can Administer Azure Virtual Desktop](/azure-virtual-desktop/who-can-administer-azure-virtual-desktop/), and the subscription checks are in [Prepare Your Azure Environment](/azure-virtual-desktop/prepare-your-azure-environment/).

For vCPU quota and capacity checks, see [Prepare Your Azure Environment](/azure-virtual-desktop/prepare-your-azure-environment/) and [Choose Session Host VM Sizes](/azure-virtual-desktop/choose-session-host-vm-sizes/).

## What FSLogix needs

FSLogix profile storage belongs in the workload landing zone, so the storage usually sits in the same subscription as the host pools. The profile storage is one more resource to place on your map.

Which storage works with which kind of user account depends on the storage you choose. Cloud-only users, who exist only in Microsoft Entra ID, can keep profiles on Azure Files with Microsoft Entra Kerberos. Hybrid users can use it too. The details and permissions are in [Choose the Right Identity Model](/azure-virtual-desktop/choose-the-right-identity-model/) and [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/).

## Common mistakes

- **Assuming a domain-only user can connect.** Users must be in Microsoft Entra ID. An account that exists only in AD DS is not supported.
- **Mismatched accounts.** The UPN or the SID must match between AD DS and Microsoft Entra ID. If neither matches, the account does not meet the requirement.
- **Hybrid joined hosts in another domain with no trust.** Without a two-way trust, SSO connections fall back to older authentication protocols.
- **Skipping the Kerberos server object.** Hybrid joined hosts with SSO can fail with a "session does not exist" error, or skip SSO and show a standard sign-in dialog.
- **Using SSO with AD-only or Domain Services hosts.** SSO needs Microsoft Entra joined or hybrid joined hosts.
- **Using a join account with MFA.** The account that joins hosts to a domain cannot have MFA enabled.
- **Registering the resource provider in one subscription only.** The registration is made for a subscription.
- **Expecting the management subscription to do the work.** In the reference design, the workload team provides its own monitoring and automation.
- **Treating a table row as proof that several domains work.** The scenario table has no row for more than one AD domain.

## How to validate this in your environment

1. **Draw the map.** For each group of users, write down: the domain the account lives in, the Microsoft Entra tenant, the join type of its session hosts, and the subscription that holds the hosts, the network and the profile storage.
2. **Check each row.** Match every user group and host group to a row in the identity scenarios table. If a group has no row, stop and test before building.
3. **Check the accounts.** For a test user, compare the UPN and the SID in AD DS and Microsoft Entra ID. At least one must match.
4. **Check the resource provider.** In the Azure portal open **Subscriptions**, select the subscription, select **Resource providers** and search for **Microsoft.DesktopVirtualization**. The status must be *Registered*. Repeat for each subscription you use.
5. **Check the join account.** Confirm it can join computers to the domain or to the tenant, and that MFA is not enabled on a domain join account.
6. **Check the network.** From the virtual network of the session hosts, confirm that the domain controllers and DNS servers can be reached, and that the virtual network is in the same region as the session hosts.
7. **Check the SSO rules.** Confirm the hosts are Microsoft Entra joined or hybrid joined. If the hosts are in a different domain from the users, confirm that a two-way trust exists. If the hosts are hybrid joined, confirm the Kerberos server object exists.
8. **Check the SSO settings.** In the Azure portal open **Microsoft Entra ID**, then **Devices**, then **Remote connection configuration**, then **Windows Cloud Login**, and confirm that Microsoft Entra authentication is enabled. In the host pool, confirm that **Microsoft Entra single sign-on** is set to **Connections will use Microsoft Entra authentication to provide single sign-on**.
9. **Test one sign-in per row.** Sign in with a test user from each user group, and note any second credential prompt. If a host does not register, use [Troubleshoot AVD Session Hosts That Do Not Register to the Host Pool](/azure-virtual-desktop/troubleshoot-host-pool-registration-failures/).

## Sources

- [Prerequisites for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)
- [Configure single sign-on for Azure Virtual Desktop using Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-single-sign-on)
- [Azure Virtual Desktop landing zone design guide](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/azure-virtual-desktop/design-guide)
