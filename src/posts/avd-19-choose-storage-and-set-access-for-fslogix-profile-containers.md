---
title: "Choose Storage and Set Access for FSLogix Profile Containers"
seoTitle: "FSLogix Profile Storage on Azure: Pick the Service, Set Access"
layout: post.njk
permalink: "/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/"
order: 119
part: 19
tags: [avd-series]
deck: "Choose between Azure Files and Azure NetApp Files for FSLogix profiles, then set the Azure role and Windows permissions that let each user open only their own folder."
description: "Azure Files or Azure NetApp Files for FSLogix profile containers in Azure Virtual Desktop: tiers, sizes, redundancy, storage recovery, Azure roles, Windows ACLs and what to check for cloud-only users."
---

FSLogix keeps each user's profile in one container file on a file share. If the share is slow, or far from the session hosts, the user experience suffers. If users cannot open their own folder, their profiles cannot load from the share. If they can open other people's folders, profile data is exposed. Two decisions therefore sit side by side: which Azure service holds the share, and who is allowed to open what on it.

Access has two layers. The first is an Azure role: a set of permissions that Azure gives to a user or group on the share. The second is a set of Windows permissions on the folders inside it. Both are explained in the Key terms table below. A "cloud-only user" is a user who exists only in Microsoft Entra ID, with no on-premises Active Directory account.

[Choose the Right Identity Model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/) covers the identity sources table, the Microsoft Entra Kerberos requirements, the multifactor authentication exclusion, the ticket-retrieval client setting and the limits for external (guest) users, so this article does not repeat them. The storage network path (private endpoint, private DNS, TCP 445) is in [Plan Azure Virtual Desktop Networking](/azure-virtual-desktop/plan-avd-networking/).

## Key terms

The identity model article defines Kerberos, SID, ACL, MFA, SMB, Entra joined, hybrid joined, AD DS and Microsoft Entra Domain Services. The table below adds the terms this article needs.

| Term | Meaning |
|---|---|
| Profile container | One virtual disk file (VHD or VHDX) that holds all the data of a user's profile. FSLogix attaches it when the user signs in. |
| Azure Files and storage account | Azure Files is an Azure service that offers file shares. SMB shares are created inside a storage account, a shared pool of storage. |
| Azure NetApp Files | An Azure service that provides SMB volumes. A volume sits in a capacity pool, and the pool decides the volume's performance level. |
| Premium and standard file shares | Premium shares use solid-state drives (SSD). Standard shares use hard disk drives (HDD). |
| Availability zone | A separate physical location inside an Azure region, with its own power, cooling and networking. |
| LRS, ZRS, GRS, GZRS | Locally redundant storage (LRS) keeps copies inside the primary region. Zone-redundant storage (ZRS) copies data across three availability zones there. Geo-redundant storage (GRS) and geo-zone-redundant storage (GZRS) also copy it to a second region far away. |
| Azure role-based access control (Azure RBAC) | The system that controls who can do what to Azure resources. A role (a set of permissions) is attached to a user or group at a scope (the resources it applies to). |
| Windows ACL (NTFS permissions) | The list of entries on a folder or file. Each entry names a user or group and says which access is allowed or denied. |
| Microsoft Entra Kerberos, hybrid identity, cloud-only identity | Microsoft Entra Kerberos is a setup where Microsoft Entra ID issues the Kerberos tickets itself. A hybrid identity exists in both on-premises AD DS and Microsoft Entra ID. A cloud-only identity exists only in Microsoft Entra ID. |
| GiB, TiB, PiB | Storage sizes. 1 TiB is 1,024 GiB. 1 PiB is 1,024 TiB. |
| IOPS and GBps | IOPS is input/output operations per second. GBps is gigabytes per second. |
| Open handle | An open connection to a file or folder. A share has a limit on how many it can hold at once. |
| Classic file share and NFS | A classic file share is the usual Azure Files share inside a storage account. NFS is a file-sharing protocol used mostly by Linux. FSLogix on Windows uses SMB. |
| Share snapshot and soft delete | A share snapshot is a read-only, point-in-time copy of a share. Soft delete keeps a deleted share for a set time so that it can be undeleted. |
| Account failover | Switching a geo-redundant storage account so that its secondary region becomes the primary region. |
| Last Sync Time | A property of a geo-redundant account that shows when data was last copied to the second region. |
| FSLogix Cloud Cache | An FSLogix feature that runs a user's container from a local copy on the session host and writes the changes to one or more remote storage providers listed in `CCDLocations`. |

## The choices at a glance

The decision has five checks, in this order:

1. Identity. Azure Files accepts three identity sources. Azure NetApp Files supports two, with a third, Microsoft Entra Kerberos (see Key terms), still in preview. A preview is a feature that is not yet generally available. See "Points to watch" near the end.
2. Region. Azure NetApp Files is available only in select regions.
3. Size and performance. Compare the ceilings and tier guidance with the user count and workload type.
4. What the storage must survive. Redundancy options differ, and Azure Files premium shares cannot be geo-redundant.
5. Access. On Azure Files, a profile folder is reached through an identity source (who the user is), then an Azure role on the share (whether the user can reach it), then a Windows ACL on the folder and file (what the user can do inside it). If the two permission checks differ, the more restrictive one applies. For cloud-only users, do not assume the Windows ACL is enforced; test it (see "Cloud-only users and folder permissions").

Three limits on scope. The recovery section covers the Azure Files share and FSLogix Cloud Cache. It is not a runbook and gives no recovery time or data-loss figures. Cross-region disaster recovery is not covered in full here, and session-host recovery is not covered at all. For cloud-only users, the article lists what works for folder permissions and gives no full procedure.

The sections follow the checks in this order: service comparison (checks 2 and 3), identity (check 1), recovery (check 4), then access (check 5). The last two sections show common permission mistakes and how to test a setup.

## What the storage has to do

At sign-in, FSLogix attaches the user's container from a file share that supports SMB. The FSLogix [prerequisites page](https://learn.microsoft.com/en-us/fslogix/overview-prerequisites) says FSLogix itself gives no storage design guidance, so the decision rests on the Azure pages for each storage service.

The [FSLogix storage page](https://learn.microsoft.com/en-us/fslogix/concepts-container-storage-options) gives an example of one user: about 10 IOPS (input/output operations per second) in steady state and about 50 IOPS at sign-in and sign-out. It says this can be scaled to your user count, for example about 1,000 IOPS for 100 users in steady state and about 5,000 IOPS when 100 users sign in or out. These are an example, not a guarantee. Measure your own workload.

Distance also matters. The prerequisites page says network latency, bandwidth and proximity to the storage provider are pivotal to the user's experience. The Azure Virtual Desktop [page on profile containers](https://learn.microsoft.com/en-us/azure/virtual-desktop/fslogix-profile-containers) says the storage account must be in the same region as the session host virtual machines, and that for best performance the storage and the profile container should be in the same data center location.

## Azure Files or Azure NetApp Files

Both are Azure-native services and both offer SMB shares that FSLogix can use. The [storage options page](https://learn.microsoft.com/en-us/azure/virtual-desktop/store-fslogix-profile) states a default: Azure Files is recommended for most customers. The table lists what that page and the service pages document.

| | Azure Files | Azure NetApp Files |
|---|---|---|
| Regions | All regions | Select regions only |
| Performance ceiling (storage options page) | Up to 100,000 IOPS per share, 10 GBps per share, about 3 ms latency | Up to 460,000 IOPS per volume, 4.5 GBps per volume, about 1 ms latency |
| Performance levels | Premium and standard | Standard, Premium and Ultra |
| Largest share or volume | 100 TiB per share on the storage options page (the [Azure Files limits page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-scale-targets) lists up to 256 TiB for provisioned v2 shares) | 100 TiB per regular volume ([limits page](https://learn.microsoft.com/en-us/azure/azure-netapp-files/azure-netapp-files-resource-limits)) |
| Smallest size | 1 GiB share on the storage options page (the Azure Files limits page gives a minimum that depends on the billing model) | 1 TiB capacity pool (4 TiB if any volume uses Basic network features) and 50 GiB volume |
| Redundancy | LRS, ZRS, GRS, GZRS | Locally redundant, zone-redundant with cross-zone replication, geo-redundant with cross-region replication (another FSLogix page lists locally redundant and cross-region replication only) |
| Backup | Azure Backup snapshot integration | Azure NetApp Files snapshots and backup |

The ceilings are the top of what the services allow, not what one profile share will deliver. The Azure Files limits page says other variables can affect these targets, so test your own usage pattern. Standard (HDD) Azure Files shares have lower limits: a standard pay-as-you-go storage account is limited to 20,000 IOPS by default, or 40,000 in select regions, according to the Azure Files limits page.

### Azure Files tiers

The storage options page gives this guidance, based on the example scenarios in the Remote Desktop workload types.

| Workload type | Recommended file share |
|---|---|
| Light, fewer than 200 users | Standard |
| Light, more than 200 users | Premium, or standard with multiple file shares |
| Medium, Heavy, Power | Premium |

The tiers bill differently. Premium shares use a provisioned billing model: you pay for the storage you set up, whether you use it or not. The storage options page describes standard shares as pay-as-you-go: you pay for what you use, including data stored and transactions. The [Azure Files limits page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-scale-targets) also lists a provisioned v2 model for standard shares, so check the billing model when you create the account.

A share allows [10,000 open handles on its root folder (see Key terms)](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-scale-targets). A [release note](https://learn.microsoft.com/en-us/azure/storage/files/files-whats-new) says that after the root-folder handle limit was raised to 10,000, FSLogix on Azure Files supports 10,000 active users per share, and that the real number depends on what the applications do.

FSLogix profiles on Azure Files use a classic file share in a storage account, because new shares created with the `Microsoft.FileShares` resource provider currently offer NFS only (see Key terms), according to the Azure Files FAQ and release notes.

### Azure NetApp Files tiers

Performance depends on the service level and the size you provision. The storage options page says more provisioned capacity gives a higher performance budget, which "likely" lets you use a lower level, and that this gives a more optimal total cost of ownership. It points to a calculator to choose the level and volume size.

The tier guidance by workload type:

| Workload | Small number of users | Medium number | Large number |
|---|---|---|---|
| Light | Standard | Standard | Standard |
| Medium and Heavy | Premium | Premium | Standard |
| Power | Ultra | Premium | Standard |

Two limits shape larger designs. The [FSLogix page for Azure NetApp Files](https://learn.microsoft.com/en-us/fslogix/how-to-configure-profile-container-netapp) says to keep the number of profiles in active use on one regular volume to 3,000 or fewer, because going above that can significantly increase latency. For more than 3,000 concurrent users it suggests spreading users over several volumes, each in a different availability zone. The same page recommends turning on Continuous Availability (a setting that keeps SMB connections alive during maintenance events) for the SMB volume when it holds FSLogix profiles.

### Which to start with

There is no single rule for choosing. Without a reason to leave it, the default is Azure Files. Another [FSLogix page](https://learn.microsoft.com/en-us/fslogix/concepts-container-storage-options) describes Azure NetApp Files as for ultra performance or for migration from NetApp on-premises. Work through the five checks in order, because the identity check can narrow the choice before speed or price matters.

## Identity can rule out a storage choice

Azure Files accepts three identity sources: AD DS, Microsoft Entra Domain Services and Microsoft Entra Kerberos. A storage account can use only one at a time, and all shares in the account share that choice, according to the [Azure Files identity page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-active-directory-overview). The storage options page lists only the first two for Azure Files, but the identity page lists three, and this article follows that page. Changing the source later interrupts identity-based access to all shares in the account for a while.

### Azure NetApp Files and identity

The FSLogix page for Azure NetApp Files says profile containers on Azure NetApp Files need Kerberos authentication and can be reached only by users who authenticate from AD DS or Microsoft Entra Domain Services. It works with Microsoft Entra joined or hybrid joined session hosts when the user identities are backed by AD DS, for example hybrid identities.

The [SMB FAQ](https://learn.microsoft.com/en-us/azure/azure-netapp-files/faq-smb) says an SMB volume needs an Active Directory connection first, that the domain controllers must be reachable from the subnet Azure NetApp Files uses, and that one NetApp account supports one Active Directory connection. Its answer on Microsoft Entra ID is about AD join and does not mention Microsoft Entra Kerberos. For cloud-only users, see "Azure NetApp Files and Microsoft Entra Kerberos" under "Points to watch".

## What the storage survives

Azure Files always keeps three copies of the data in the primary region, according to the [redundancy page](https://learn.microsoft.com/en-us/azure/storage/files/files-redundancy). LRS keeps them in one or more availability zones and is the least expensive option, but a disaster such as fire or flood in the data center could lose all the copies, so the page recommends ZRS, GRS or GZRS for protection.

The page recommends ZRS for scenarios that need high availability, and GZRS for applications that need high availability or maximum durability; GZRS is not available for premium shares (see below). With ZRS, a zone failure needs no remounting of the share by clients, though the DNS updates Azure makes in that case can affect access until they finish, so users may briefly be unable to connect.

| What fails | LRS | ZRS | GRS | GZRS |
|---|---|---|---|---|
| One server in a data center | Data stays available | Data stays available | Data stays available | Data stays available |
| A whole data center | Not available | Available | Available. An account failover is needed to make the share writable again if the primary region is unavailable | Available |
| The whole primary region | Not available | Not available | Available after an account failover | Available after an account failover |

These two decisions affect each other: geo-redundancy (GRS or GZRS) is supported only for standard (HDD) file shares. Premium (SSD) shares must use LRS or ZRS, and ZRS support for premium shares depends on the region, so check the [region list](https://learn.microsoft.com/en-us/azure/storage/files/redundancy-premium-file-shares). The tier guidance above recommends premium shares for medium, heavy and power workloads. If you follow that recommendation, geo-redundancy is not available for that share.

Redundancy is set per storage account and applies to every share in it. Use separate storage accounts for shares with different needs. With GRS or GZRS the shares cannot be reached in the second region unless a failover happens. During a failover the data is inaccessible, and afterward clients must disconnect the share and connect it again.

## Storage recovery

Redundancy keeps copies for availability. It is not a backup.

For geo-redundant accounts (standard HDD shares only), the [disaster recovery page](https://learn.microsoft.com/en-us/azure/storage/files/files-disaster-recovery) describes account failover: DNS is updated so the secondary endpoint becomes the primary, file handles and leases are not retained, and the account is then locally redundant until geo-redundancy is configured again.

An unplanned (forced) account failover usually involves some data loss because copying to the secondary region is asynchronous (see Last Sync Time in Key terms). The [redundancy page](https://learn.microsoft.com/en-us/azure/storage/files/files-redundancy) says it is blocked if no system snapshot exists in the secondary region. The page also describes customer-managed planned failover and Microsoft-managed failover.

For premium shares, which have no geo-redundant option, the [multiregion page](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr) says that if you require Premium performance for FSLogix profile storage, you should rely on FSLogix Cloud Cache for cross-region replication rather than storage built-in geo-replication.

A [share snapshot](https://learn.microsoft.com/en-us/azure/storage/files/storage-snapshots-files) is a read-only, point-in-time copy taken at share level; a share can hold up to 200, and snapshots follow the share's redundancy. They let you restore earlier versions of files, or copy a whole share back from a snapshot. They do not protect against deleting the share or the storage account.

[Azure Backup for Azure Files](https://learn.microsoft.com/en-us/azure/backup/azure-file-share-backup-overview) has two tiers:

- **Snapshot tier.** The snapshots stay in the same storage account. Deleting the account loses them, and Azure Backup takes a delete lock on the account, according to the [backup FAQ](https://learn.microsoft.com/en-us/azure/backup/backup-azure-files-faq). According to the [support matrix](https://learn.microsoft.com/en-us/azure/backup/azure-file-share-support-matrix), it supports full-share and item-level restore.
- **Vault-standard tier.** It also transfers changed data to a backup vault. It supports full-share restore only ("File-level recovery is not supported"), shares up to 10 TB and 10 million files, and only the regions the matrix lists. The [release notes](https://learn.microsoft.com/en-us/azure/storage/files/files-whats-new) list vaulted backup as generally available for HDD (2025 quarter 1) and SSD (2025 quarter 3) shares and recommend it over snapshot backups.

Azure Backup uses key-based access, so key access must be enabled on source and target storage accounts even if identity-based access is configured. After a customer-managed unplanned failover, backups are not supported and only cross-region restore from the vault is. The multiregion page recommends Azure Backup for user profile data; the snapshot, soft delete and backup pages do not mention FSLogix.

[Soft delete](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-prevent-file-share-deletion) keeps a deleted classic file share and its snapshots for a retention period so that it can be undeleted. It works only at share level (for deleted files, the page points to share snapshots or Azure Backup), applies to the whole storage account, and is on by default for new accounts. The backup FAQ says a soft-deleted share must be undeleted before a restore, and a permanently deleted share cannot be restored.

The Cloud Cache [overview](https://learn.microsoft.com/en-us/fslogix/concepts-fslogix-cloud-cache) says it provides resiliency and high availability and, with providers in different regions, can support a business continuity and disaster recovery plan, at the cost of a performance and storage requirement on the session host. Two more points from the overview:

- Sign-out is delayed until all providers are at the same sequence. How long depends on two Cloud Cache registry settings, `HealthyProvidersRequiredForUnregister` and `CcdUnregisterTimeout`.
- A read that no provider can fill can cause a session hang or system crash.

The [FSLogix FAQ](https://learn.microsoft.com/en-us/fslogix/overview-faq) says Cloud Cache is not required for high availability: standard containers on a highly available provider such as Azure Files with ZRS are acceptable. The [FSLogix business continuity page](https://learn.microsoft.com/en-us/fslogix/concepts-container-recovery-business-continuity) describes designs with two providers in different locations, says disaster recovery events are rarely graceful and users could see data loss or container corruption, and says critical data belongs on platforms such as OneDrive or SharePoint.

The automatic or manual failover wording is compared in "Cloud Cache failover: automatic or manual" below, and [Operate FSLogix Profiles Day to Day](/azure-virtual-desktop/operate-fslogix-profiles-day-to-day/) covers the same point for daily operations.

See "Points to watch" for the soft delete retention and Cloud Cache failover.

## Share-level permissions: Azure roles

For Azure Files, the first access check is an Azure role on the share (a share-level permission), and the scope can be the single file share. The [share-level permissions page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions) lists the roles. The SMB Admin row below uses the wording of the file-level permissions page; the share-level page describes the role differently (see "Smaller differences").

| Built-in role | What it allows on files and folders |
|---|---|
| Storage File Data SMB Share Reader | Read |
| Storage File Data SMB Share Contributor | Read, write and delete |
| Storage File Data SMB Share Elevated Contributor | Read, write, delete and change permissions (ACLs) |
| Storage File Data SMB Admin | Share-level access plus the right to take ownership (with `takeown`) of any file or folder and then change its ACL. Existing ACLs still apply for normal file access. |

Other built-in roles exist, for example Storage File Data Privileged Contributor and Storage File Data Privileged Reader, which override existing ACLs.

There are two ways to give share-level permission:

- **To specific users or groups.** The share-level page says most people do this and that it is the most secure option. Hybrid users and groups must be synced from AD to Microsoft Entra ID first. With AD DS, a user who is not synced still gets the role of a synced on-premises group the user belongs to, because Azure Files reads the group identifiers in the Kerberos ticket. With Microsoft Entra Domain Services and scoped synchronization, [role assignments for identities that are not synchronized to the managed domain are ignored](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-domain-services-enable).
- **A default share-level permission for all authenticated identities.** It applies to every share in the storage account. It starts as None, which means no access. It is meant for cases where you cannot sync AD DS to Microsoft Entra ID, or where you prefer to enforce access only with Windows ACLs.

If both are set, a user gets the higher of the two. The [FSLogix permissions page](https://learn.microsoft.com/en-us/fslogix/how-to-configure-storage-permissions) recommends the default share-level permission set to Storage File Data SMB Share Contributor for all authenticated identities, plus Storage File Data SMB Share Elevated Contributor for the specific users or groups who set the Windows ACLs. The two pages stress different options, so decide on purpose which one you follow.

A change to a share-level permission usually takes effect within 30 minutes and can take longer ([Assign share-level permissions for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions)). Wait before testing.

## Folder and file permissions: Windows ACLs

The second check is the Windows ACL on the folder and file. The [file-level permissions page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-configure-file-level-permissions) describes the split: share-level permissions act as a high-level gatekeeper that decides whether a user can reach the share, and Windows ACLs decide what the user can do inside it.

When both apply and differ, only the most restrictive one counts, according to the page. Some examples from the page:

- No Azure role: access is denied, whatever the ACL says.
- Reader role and an ACL that allows Modify: the user can only read.
- Any role and an ACL of None: access is denied.

### The recommended ACLs for a profile share

The FSLogix permissions page recommends a user-based setup. Each user has access only to their own profile folder or container file, and administrative groups have Full Control for operations. These are its recommended entries.

| Who | Access | Applies to | Why |
|---|---|---|---|
| CREATOR OWNER (a built-in Windows name that means whoever created the item) | Modify | Subfolders and files only | The folder a user creates gets permissions for that user only. |
| Your administrator group (the page uses Domain Admins as the example) | Full Control | This folder, subfolders and files | Lets administrators manage the share. |
| Your users group (the page uses Domain Users as the example) | Modify | This folder only | Lets users create their own profile folder. |

The page shows how to apply these with icacls or File Explorer. FSLogix also has a setting, `SIDDirSDDL`, that sets the ACLs (written in SDDL, a text format for permissions) on each user's folder when the folder is created.

### Who can set ACLs on Azure Files, and with what

Setting ACLs (icacls is the Windows command-line tool for ACLs) with File Explorer or icacls on Azure Files needs extra rights, because there are two checks. The file-level page says to skip the admin-level mount for the Azure portal and `RestSetAcls` (an Azure Files PowerShell module that sets ACLs through the REST API). The ways to mount with admin-level access are:

- Give the person the Storage File Data SMB Share Elevated Contributor role. The FSLogix page names this role for setting ACLs without the account key. The file-level page adds that the person also needs a Full Control ACL, or the Storage File Data SMB Admin role, which lets an administrator mount the share with their own identity and take ownership where needed. It calls the SMB Admin approach more secure than the next one.
- Mount the share with the storage account key. The file-level page calls this less secure and advises it only when identity-based access cannot be used.

The tool depends on the identity source. This table is from the file-level page.

| Tool | AD DS | Microsoft Entra Domain Services | Microsoft Entra Kerberos, hybrid users | Microsoft Entra Kerberos, cloud-only users |
|---|---|---|---|---|
| Windows File Explorer | Yes | Yes | Yes | No |
| icacls | Yes | Yes | Yes | No |
| Azure portal | No | No | Yes | Yes |
| PowerShell, RestSetAcls module | No | No | Yes | Yes |

With Microsoft Entra Kerberos and hybrid users, the users must be synced to Microsoft Entra ID for the ACLs to be enforced. ACLs set for users that are not synced are not enforced. With AD DS as the identity source, ACLs for users that are not synced do work. Setting ACLs with File Explorer or icacls needs a Windows client with unimpeded network connectivity to the domain controllers; the portal and `RestSetAcls` do not depend on domain controllers. Cloud-only identities on Azure Files are supported in the Azure public cloud only (see "Points to watch").

### Cloud-only users and folder permissions

For Azure Files with Microsoft Entra Kerberos and cloud-only users:

- The Azure portal (the Manage access action) and the `RestSetAcls` PowerShell module are the two tools that work. File Explorer and icacls are not supported for cloud-only identities.
- Neither tool depends on domain controllers. The `RestSetAcls` example on the file-level page authenticates with the storage account key, and the module needs a Windows client.
- In the portal, Deny takes precedence over Allow when both are set, and when neither is set, default permissions are inherited.
- The FSLogix recommended entries (the table above) are written with domain principals and applied with icacls or File Explorer. Those are the two tools that do not work for cloud-only identities, so the entries need to be rebuilt with Microsoft Entra groups in the portal or with `RestSetAcls`. Check whether CREATOR OWNER with "subfolders and files only" and the FSLogix `SIDDirSDDL` setting work in your setup before you rely on them.

Do not assume that Windows ACLs keep cloud-only users out of each other's folders. The Microsoft Entra Kerberos introduction says authorization for cloud-only users is enforced by Azure roles and lists "no NTFS ACL enforcement", while the file-level permissions page says share-level, file-level and directory-level permissions are all enforced. Before rollout, test with two cloud-only users that one cannot open the other's profile folder.

### Azure NetApp Files

The FSLogix permissions page says Azure NetApp Files relies solely on Windows ACLs, and it points to the same recommended list. The FSLogix page for Azure NetApp Files warns that without proper permissions on the folders, a user can delete their profile or read another user's personal information.

## More Microsoft Entra Kerberos requirements for Azure Files

Three requirements on the Azure Files [setup page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable) are not in the identity model article, which covers the rest of the Microsoft Entra Kerberos requirements:

- Two Windows services must be running on the clients: WinHTTP Web Proxy Auto-Discovery (`WinHttpAutoProxySvc`) and IP Helper (`iphlpsvc`).
- A Kerberos ticket can hold at most 1,010 group identifiers (SIDs, the unique IDs of groups). The tag in the storage account's app manifest (the app's settings file in Microsoft Entra ID) is `kdc_enable_cloud_group_sids`.
  - The setup page says that for cloud-only identities the ticket must include both on-premises and cloud group SIDs. It says updating the tag is mandatory for cloud-only identities, or authentication fails.
  - The Microsoft Entra Kerberos introduction page describes the tag as a short-term solution. It does not say that leaving it out causes authentication to fail.
  - Exceeding 1,010 groups can make authentication fail (see "Points to watch").
- Kerberos ticket encryption with Microsoft Entra Kerberos is always AES-256.

The setup page also says an administrator must grant admin consent (approve the app's permissions for the whole organization) for the storage account's app. It also says that without the multifactor authentication exclusion (covered in the identity model article) mapping the share with `net use` returns system error 1327. The [Microsoft Entra Kerberos introduction page](https://learn.microsoft.com/en-us/entra/identity/authentication/kerberos) says "Microsoft Entra Kerberos authentication for Azure file shares doesn't support MFA" and that Conditional Access policies that enforce MFA must exclude the storage account application, or users experience authentication failures.

## Points to watch

### Cloud-only identities on Azure Files

FSLogix profile containers for cloud-only and external identities on Azure Files are generally available (May 2026 for Azure Virtual Desktop, 2026 quarter 2 for Azure Files). They are supported only in the Azure public cloud, not in Azure US Government or Azure operated by 21Vianet. Some Microsoft Entra Kerberos pages still carry "Preview" in their headings, so check the current state for your cloud before you plan for cloud-only users.

The FSLogix FAQ allows cloud-only identities but asks you to understand the risks. Password changes during an active session are not supported on Microsoft Entra joined hosts or with Entra-only identities, and object-specific settings and application rule sets need traditional Active Directory identifiers.

### Azure NetApp Files and Microsoft Entra Kerberos

Azure NetApp Files does not support FSLogix profile access with cloud-only identities: Kerberos authentication without AD DS is not supported, and the SMB FAQ says it does not support AD join for Microsoft Entra ID. A Microsoft Entra Kerberos feature for hybrid and cloud-only identities on SMB volumes is in preview ([understand](https://learn.microsoft.com/en-us/azure/azure-netapp-files/understand-entra-id) and [configure](https://learn.microsoft.com/en-us/azure/azure-netapp-files/configure-entra-kerberos-authentication-for-hybrid-cloud-identities)). It needs a feature registration step, a Standard SKU NAT gateway for outbound access to Microsoft Graph and an Entra ID connection on the NetApp account. A NetApp account supports either Microsoft Entra ID or AD DS authentication, not both. Windows ACLs can be set only with icacls (File Explorer is not supported, and icacls for groups is not supported for Entra-only identities). The preview does not mention FSLogix, so do not plan profile storage on it without testing.

### Cloud Cache failover

The [multiregion architecture](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr) says Cloud Cache fails over to the secondary region automatically when the first storage location cannot be reached. The FSLogix business continuity designs describe starting a failover manually, with approval from business stakeholders. Test what happens in your own design before you promise a recovery behavior.

### Soft delete retention

Soft delete for Azure Files shares keeps deleted shares for 7 days by default and allows 1 to 365 days. Azure Backup enables soft delete on the storage account with a retention period of 14 days. Check the retention that is actually set on your account.

### Smaller points

- **Service principal password expiry.** If you enabled Microsoft Entra Kerberos through the earlier manual limited-preview steps, the storage account's service principal password expires every six months and must be rotated.
- **Storage File Data SMB Admin role.** Treat it as powerful: the share-level page equates it to a storage account key. The file-level page notes that existing ACLs still apply and that the role adds the right to take ownership.
- **Group limit.** A Kerberos ticket holds at most 1,010 group SIDs. Beyond that, authentication can fail, and heavily grouped users can fail intermittently. Test with a user who belongs to many groups.
- **A Kerberos change.** The default Kerberos encryption type in Windows is changing from RC4 to AES-SHA1 with the April 2026 Windows Server update. RC4 and AES are two encryption types Kerberos can use. File shares that are not upgraded might have access problems afterward, so read the FSLogix blog post about it and check the current state before you deploy. Microsoft Entra Kerberos always uses AES-256, and Microsoft Entra Domain Services recommends AES-256.
- **Azure NetApp Files limits.** The default quota is 25 TiB per subscription on one FSLogix page, and the limits page gives a regional capacity quota of 100 TiB per subscription. Check the limits page for your region and request an increase if you need more.

## Permission mistakes to avoid

- **Setting only one permission layer.** Access needs both a share-level permission and a matching Windows ACL. With only the Azure role, the default ACLs stay in place. The file-level page lists default root permissions that include Modify for authenticated users, so users would not be limited to their own folders. With only the ACLs and no Azure role, access is denied, and so it is with the default share-level permission left at None and no roles assigned. For cloud-only users, test that ACLs are enforced (see "Cloud-only users and folder permissions").
- **Expecting a portal ACL change to reach existing folders.** The file-level page says inheritable permissions edited in the portal apply only to new items, and names the `Restore-AzFileAclInheritance` command from the RestSetAcls module for existing ones.
- **Mounting with PowerShell when setting ACLs with File Explorer.** Use `net use` (for example `net use Z: \\<storage-account>.file.core.windows.net\<share>`). A share mounted with PowerShell is not visible to File Explorer or cmd.exe.

## How to check a setup

The checks for the host join state, the host pool sign-in setting and the storage identity source are in the identity model article. These checks cover the profile itself; run them in a test environment.

1. Sign in as a test user who has never had a local profile on the session host. A user who has signed in before already has a local profile, and FSLogix keeps using it unless you set `DeleteLocalProfileWhenVHDShouldApply`. A local profile is the profile folder stored on the session host's own disk. The Azure NetApp Files page says that setting makes FSLogix permanently delete the local profile when a user should have an FSLogix profile.
2. On Azure Files, open the share in the Azure portal. A folder named `<user SID>_<username>` should appear, according to the Azure Virtual Desktop setup page.
3. On Azure NetApp Files, open the volume in the Azure portal and confirm that space is in use. Then open the mount path in File Explorer and confirm that a profile VHD or VHDX file exists.
4. Sign in as a second test user and confirm that the first user's profile folder cannot be opened, especially for cloud-only users.

Next: [Build and Maintain a Golden Image](/azure-virtual-desktop/build-and-maintain-a-golden-image/).

## Sources

- [Storage options for FSLogix profile containers](https://learn.microsoft.com/en-us/azure/virtual-desktop/store-fslogix-profile)
- [Directory and file-level permissions for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-configure-file-level-permissions)
- [Configure SMB storage permissions for FSLogix](https://learn.microsoft.com/en-us/fslogix/how-to-configure-storage-permissions)
