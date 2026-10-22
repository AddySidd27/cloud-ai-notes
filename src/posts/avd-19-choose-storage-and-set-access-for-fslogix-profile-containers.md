---
title: "Choose Storage and Set Access for FSLogix Profile Containers"
seoTitle: "FSLogix Profile Storage on Azure: Pick the Service, Then Set Access"
layout: post.njk
permalink: "/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/"
order: 119
part: 19
tags: [avd-series]
# PENDING: publication date and final slug/order approval; the date lives in src/_data/articleMeta.js
deck: "Choose between Azure Files and Azure NetApp Files for FSLogix profiles, then set the Azure role and Windows permissions that let each user open only their own folder."
description: "Azure Files or Azure NetApp Files for FSLogix profile containers in Azure Virtual Desktop: tiers, sizes, redundancy, storage recovery as the documentation describes it, Azure roles, Windows ACLs, and the places where the documentation pages differ about cloud-only users."
---

FSLogix keeps each user's profile in one container file on a file share. If the share is slow, or far from the session hosts, the user experience suffers. If users cannot open their own folder, their profiles cannot load from the share. If they can open other people's folders, profile data is exposed. Two decisions therefore sit side by side: which Azure service holds the share, and who is allowed to open what on it.

Three limits on scope. The recovery section reports only what the cited documentation pages say about the Azure Files share and FSLogix Cloud Cache. It is not a runbook, it was not tested, and it gives no recovery time or data-loss figures. Cross-region disaster recovery is not covered in full in this article, and session-host recovery is not covered at all. For cloud-only users, the article lists what the documentation covers about folder permissions and gives no procedure (see "Cloud-only users: what the documentation covers about folder permissions"). The pages also label cloud-only identity support differently (see "Cloud-only identities on Azure Files: generally available or preview").

[Choose the Right Identity Model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/) covers the identity sources table, the Microsoft Entra Kerberos requirements, the multifactor authentication exclusion, the ticket-retrieval client setting and the limits for external (guest) users, so this article does not repeat them. The storage network path (private endpoint, private DNS, TCP 445) is in [Plan Azure Virtual Desktop Networking](/azure-virtual-desktop/plan-avd-networking/).

## Key terms

The identity model article defines Kerberos, SID, ACL, MFA, SMB, Entra joined, hybrid joined, AD DS and Microsoft Entra Domain Services. These terms are new here.

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
| Account failover | Switching a geo-redundant storage account so that its secondary region becomes the primary region. |
| FSLogix Cloud Cache | An FSLogix feature that runs a user's container from a local copy on the session host and writes the changes to one or more remote storage providers listed in `CCDLocations`. |

## The choices at a glance

The decision has five checks, in this order:

1. Identity. Azure Files accepts three identity sources. Azure NetApp Files documents two, and two preview pages describe a third, Microsoft Entra Kerberos, as a preview (see the caveats near the end).
2. Region. Azure NetApp Files is available only in select regions.
3. Size and performance. Compare the documented ceilings and tier guidance with the user count and workload type.
4. What the storage must survive. Redundancy options differ, and Azure Files premium shares cannot be geo-redundant.
5. Access. On Azure Files, a profile folder is reached through an identity source (who the user is), then an Azure role on the share (whether the user can reach it), then a Windows ACL on the folder and file (what the user can do inside it). If the two permission checks differ, the more restrictive one applies. For cloud-only users the pages differ on whether the Windows ACL is enforced (see the first caveat under "Where the pages differ").

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

The ceilings are the top of what the services allow, not what one profile share will deliver. Standard (HDD) Azure Files shares have lower limits: a standard pay-as-you-go storage account is limited to 20,000 IOPS by default, or 40,000 in select regions, according to the Azure Files limits page.

### Azure Files tiers

The storage options page gives this guidance, based on the example scenarios in the Remote Desktop workload types.

| Workload type | Recommended file share |
|---|---|
| Light, fewer than 200 users | Standard |
| Light, more than 200 users | Premium, or standard with multiple file shares |
| Medium, Heavy, Power | Premium |

The tiers bill differently, the main cost lever the page documents. Premium shares use a provisioned billing model: you pay for the storage you set up, whether you use it or not. Standard shares use pay-as-you-go billing: you pay for what you use, including data stored and transactions.

A share allows [10,000 open handles on its root folder](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-scale-targets). A [release note](https://learn.microsoft.com/en-us/azure/storage/files/files-whats-new) says that after the root-folder handle limit was raised to 10,000, FSLogix on Azure Files supports 10,000 active users per share, and that the real number depends on what the applications do.

FSLogix profiles on Azure Files use a classic file share in a storage account, because new shares created with the `Microsoft.FileShares` resource provider currently offer NFS only, according to the Azure Files FAQ and release notes.

### Azure NetApp Files tiers

Performance is a function of level times capacity. The storage options page says more provisioned capacity gives a higher performance budget, which "likely" lets you use a lower level, and that this gives a more optimal total cost of ownership. It points to a calculator to choose the level and volume size.

The tier guidance by workload type is: Light, Standard. Medium and Heavy, Premium for a small or medium number of users and Standard for a large number. Power, Ultra for a small number of users, Premium for a medium number and Standard for a large number.

Two documented limits shape larger designs. The [FSLogix page for Azure NetApp Files](https://learn.microsoft.com/en-us/fslogix/how-to-configure-profile-container-netapp) says to keep the number of profiles in active use on one regular volume to 3,000 or fewer, because going above that can significantly increase latency. For more than 3,000 concurrent users it suggests spreading users over several volumes, each in a different availability zone. The same page recommends turning on Continuous Availability for the SMB volume when it holds FSLogix profiles.

### Which to start with

The pages do not give one rule for choosing. Without a reason to leave it, the documented default is Azure Files. Another [FSLogix page](https://learn.microsoft.com/en-us/fslogix/concepts-container-storage-options) describes Azure NetApp Files as for ultra performance or for migration from NetApp on-premises. Work through the five checks in order, because the identity check can narrow the choice before speed or price matters.

## Identity can rule out a storage choice

Azure Files accepts three identity sources: AD DS, Microsoft Entra Domain Services and Microsoft Entra Kerberos. A storage account can use only one at a time, and all shares in the account share that choice, according to the [Azure Files identity page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-active-directory-overview). The storage options page lists only the first two for Azure Files, so the pages differ on the count; the identity page lists three, and this article follows that page. Changing the source later interrupts identity-based access to all shares in the account for a while.

### Azure NetApp Files and identity

The FSLogix page for Azure NetApp Files says profile containers on Azure NetApp Files need Kerberos authentication and can be reached only by users who authenticate from AD DS or Microsoft Entra Domain Services. It works with Microsoft Entra joined or hybrid joined session hosts when the user identities are backed by AD DS, for example hybrid identities.

The [SMB FAQ](https://learn.microsoft.com/en-us/azure/azure-netapp-files/faq-smb) says an SMB volume needs an Active Directory connection first, that the domain controllers must be reachable from the subnet Azure NetApp Files uses, and that one NetApp account supports one Active Directory connection. Its answer on Microsoft Entra ID is about AD join and does not mention Microsoft Entra Kerberos. For cloud-only users, that FAQ and the FSLogix page differ from two preview pages; both sides are quoted in the third caveat under "Where the pages differ".

## What the storage survives

Azure Files always keeps three copies of the data in the primary region, according to the [redundancy page](https://learn.microsoft.com/en-us/azure/storage/files/files-redundancy). LRS keeps them in one or more availability zones and is the least expensive option, but a disaster such as fire or flood in the data center could lose all the copies, so the page recommends ZRS, GRS or GZRS for protection. The page recommends ZRS for scenarios that need high availability, and GZRS for applications that need high availability or maximum durability; GZRS is not available for premium shares (see below). With ZRS, a zone failure needs no remounting of the share by clients, though the DNS updates Azure makes in that case can affect access until they finish.

| What fails | LRS | ZRS | GRS | GZRS |
|---|---|---|---|---|
| One server in a data center | Data stays available | Data stays available | Data stays available | Data stays available |
| A whole data center | Not available | Available | Available. An account failover is needed to restore writes if the primary region is unavailable | Available |
| The whole primary region | Not available | Not available | Available after an account failover | Available after an account failover |

The part that links two decisions: geo-redundancy (GRS or GZRS) is supported only for standard (HDD) file shares. Premium (SSD) shares must use LRS or ZRS, and ZRS support for premium shares depends on the region, so check the [region list](https://learn.microsoft.com/en-us/azure/storage/files/redundancy-premium-file-shares). The tier guidance above recommends premium shares for medium, heavy and power workloads. If you follow that recommendation, geo-redundancy is not available for that share.

Redundancy is set per storage account and applies to every share in it. Use separate storage accounts for shares with different needs. With GRS or GZRS the shares cannot be reached in the second region unless a failover happens. During a failover the data is inaccessible, and afterward clients must unmount and remount the share.

## Storage recovery: what the documentation says

Redundancy is not a recovery copy.

For geo-redundant accounts (standard HDD shares only), the [disaster recovery page](https://learn.microsoft.com/en-us/azure/storage/files/files-disaster-recovery) describes account failover: DNS is updated so the secondary endpoint becomes the primary, file handles and leases are not retained, and the account is then locally redundant until geo-redundancy is configured again. An unplanned (forced) account failover usually involves some data loss because copying to the secondary region is asynchronous (see the Last Sync Time property), and the [redundancy page](https://learn.microsoft.com/en-us/azure/storage/files/files-redundancy) says it is blocked if no system snapshot exists in the secondary region. The page also describes customer-managed planned failover and Microsoft-managed failover. For premium shares, which have no geo-redundant option, the [multiregion page](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr) says that if you require Premium performance for FSLogix profile storage, you should rely on FSLogix Cloud Cache for cross-region replication rather than storage built-in geo-replication.

A [share snapshot](https://learn.microsoft.com/en-us/azure/storage/files/storage-snapshots-files) is a read-only, point-in-time copy taken at share level; a share can hold up to 200, and snapshots follow the share's redundancy. They give only file-level protection and do not prevent deletion of a share or storage account. [Azure Backup for Azure Files](https://learn.microsoft.com/en-us/azure/backup/azure-file-share-backup-overview) has a snapshot tier, whose snapshots stay in the same storage account (deleting the account loses them, and Azure Backup takes a delete lock on it, according to the [backup FAQ](https://learn.microsoft.com/en-us/azure/backup/backup-azure-files-faq)), and a vault-standard tier, which also transfers changed data to a backup vault. According to the [support matrix](https://learn.microsoft.com/en-us/azure/backup/azure-file-share-support-matrix), the snapshot tier supports full-share and item-level restore; the vault-standard tier supports full-share restore only ("File-level recovery is not supported"), shares up to 10 TB and 10 million files, and only the regions it lists. The [release notes](https://learn.microsoft.com/en-us/azure/storage/files/files-whats-new) list vaulted backup as generally available for HDD (2025 quarter 1) and SSD (2025 quarter 3) shares and recommend it over snapshot backups. Azure Backup uses key-based access, so key access must be enabled on source and target storage accounts even if identity-based access is configured. After a customer-managed unplanned failover, backups are not supported and only cross-region restore from the vault is. The multiregion page recommends Azure Backup for user profile data; the snapshot, soft delete and backup pages do not mention FSLogix.

[Soft delete](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-prevent-file-share-deletion) keeps a deleted classic file share and its snapshots for a retention period so that it can be undeleted. It works only at share level (for deleted files, the page points to share snapshots or Azure Backup), applies to the whole storage account, and is on by default for new accounts. The backup FAQ says a soft-deleted share must be undeleted before a restore, and a permanently deleted share cannot be restored.

The Cloud Cache [overview](https://learn.microsoft.com/en-us/fslogix/concepts-fslogix-cloud-cache) says it provides resiliency and high availability and, with providers in different regions, can support a business continuity and disaster recovery plan, at the cost of a performance and storage requirement on the session host; sign-out is delayed until all providers are at the same sequence (how long depends on the `HealthyProvidersRequiredForUnregister` and `CcdUnregisterTimeout` values), and a read that no provider can fill can cause a session hang or system crash. The [FSLogix FAQ](https://learn.microsoft.com/en-us/fslogix/overview-faq) says Cloud Cache is not required for high availability: standard containers on a highly available provider such as Azure Files with ZRS are acceptable. The [FSLogix business continuity page](https://learn.microsoft.com/en-us/fslogix/concepts-container-recovery-business-continuity) describes designs with two providers in different locations, says disaster recovery events are rarely graceful and users could see data loss or container corruption, and says critical data belongs on platforms such as OneDrive or SharePoint.

Two figures differ between pages; see the soft delete and Cloud Cache caveats below.

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

A change to a share-level permission usually takes effect within 30 minutes and can take longer. Wait before testing.

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
| CREATOR OWNER (the owner of the object) | Modify | Subfolders and files only | The folder a user creates gets permissions for that user only. |
| Your administrator group (the page uses Domain Admins as the example) | Full Control | This folder, subfolders and files | Lets administrators manage the share. |
| Your users group (the page uses Domain Users as the example) | Modify | This folder only | Lets users create their own profile folder. |

The page shows how to apply these with icacls or File Explorer. FSLogix also has a setting, `SIDDirSDDL`, that sets the ACLs on each user's folder when the folder is created.

### Who can set ACLs on Azure Files, and with what

Setting ACLs with File Explorer or icacls on Azure Files needs extra rights, because there are two checks. The file-level page says to skip the admin-level mount for the Azure portal and `RestSetAcls`. The documented ways to mount with admin-level access are:

- Give the person the Storage File Data SMB Share Elevated Contributor role. The FSLogix page names this role for setting ACLs without the account key. The file-level page adds that the person also needs a Full Control ACL, or the Storage File Data SMB Admin role, which lets an administrator mount the share with their own identity and take ownership where needed. It calls the SMB Admin approach more secure than the next one.
- Mount the share with the storage account key. The file-level page calls this less secure and advises it only when identity-based access cannot be used.

The tool depends on the identity source. This table is from the file-level page.

| Tool | AD DS | Microsoft Entra Domain Services | Microsoft Entra Kerberos, hybrid users | Microsoft Entra Kerberos, cloud-only users |
|---|---|---|---|---|
| Windows File Explorer | Yes | Yes | Yes | No |
| icacls | Yes | Yes | Yes | No |
| Azure portal | No | No | Yes | Yes |
| PowerShell, RestSetAcls module | No | No | Yes | Yes |

With Microsoft Entra Kerberos and hybrid users, the users must be synced to Microsoft Entra ID for the ACLs to be enforced. ACLs set for users that are not synced are not enforced. With AD DS as the identity source, ACLs for users that are not synced do work. Setting ACLs with File Explorer or icacls needs a Windows client with unimpeded network connectivity to the domain controllers; the portal and `RestSetAcls` do not depend on domain controllers. For the cloud-only column, the pages label cloud-only identity support differently (see "Cloud-only identities on Azure Files: generally available or preview").

### Cloud-only users: what the documentation covers about folder permissions

For Azure Files with Microsoft Entra Kerberos and cloud-only users, the pages reviewed document the following about folder and file permissions. The pages label cloud-only identity support differently (see "Cloud-only identities on Azure Files: generally available or preview").

- The Azure portal (the Manage access action) and the `RestSetAcls` PowerShell module are the two documented tools. File Explorer and icacls are documented as not supported for cloud-only identities.
- Neither documented tool depends on domain controllers. The `RestSetAcls` example on the file-level page authenticates with the storage account key, and the module needs a Windows client.
- In the portal, Deny takes precedence over Allow when both are set, and when neither is set, default permissions are inherited.
- The FSLogix recommended entries (the table above) are written with domain principals, and the FSLogix page applies them with icacls or File Explorer. Those are the two tools listed as unsupported for cloud-only identities.

The pages reviewed do not document how to apply that entry set to a cloud-only share: which Entra group stands in for the users group, whether CREATOR OWNER with "subfolders and files only" can be set with the portal or `RestSetAcls`, or which Azure role an administrator needs to use Manage access. They do not say whether the FSLogix `SIDDirSDDL` setting works with cloud-only identities. They also do not settle whether the resulting ACLs are enforced for cloud-only users (first caveat below). This article therefore gives no cloud-only folder-permission procedure.

### Azure NetApp Files

The FSLogix permissions page says Azure NetApp Files relies solely on Windows ACLs, and it points to the same recommended list. The FSLogix page for Azure NetApp Files warns that without proper permissions on the folders, a user can delete their profile or read another user's personal information.

## More Microsoft Entra Kerberos requirements for Azure Files

Three requirements on the Azure Files [setup page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable) are not in the identity model article, which covers the rest of the Microsoft Entra Kerberos requirements:

- Two Windows services must be running on the clients: WinHTTP Web Proxy Auto-Discovery (`WinHttpAutoProxySvc`) and IP Helper (`iphlpsvc`).
- A Kerberos ticket can hold at most 1,010 group identifiers (SIDs). The setup page says that for cloud-only identities the ticket must include both on-premises and cloud group SIDs, and that updating the tag (`kdc_enable_cloud_group_sids`) in the storage account's app manifest is mandatory for cloud-only identities, or authentication fails. The Microsoft Entra Kerberos introduction page describes the tag as a short-term solution and does not say that leaving it out causes authentication to fail. The pages also word the result of exceeding 1,010 differently (see "Group limit effect" under "Smaller differences"). The pages also label cloud-only identity support differently (see "Cloud-only identities on Azure Files: generally available or preview").
- Kerberos ticket encryption with Microsoft Entra Kerberos is always AES-256.

The setup page also says the storage account's app needs admin consent, and that without the multifactor authentication exclusion (covered in the identity model article) mapping the share with `net use` returns system error 1327. The [Microsoft Entra Kerberos introduction page](https://learn.microsoft.com/en-us/entra/identity/authentication/kerberos) says "Microsoft Entra Kerberos authentication for Azure file shares doesn't support MFA" and that Conditional Access policies that enforce MFA must exclude the storage account application, or users experience authentication failures.

## Where the pages differ

Some documentation pages differ on points that affect these decisions. This article does not settle them. Recheck the current status of each on the publish date.

### Cloud-only identities and Windows ACL enforcement

The pages describe permissions for cloud-only users on Azure Files in two different ways.

**Setup and identity pages.** The Azure Files file-level permissions page says "For cloud-only identities, you must use the Azure portal or PowerShell" to configure Windows ACLs, and that the portal method "works for both hybrid and cloud-only identities only when Microsoft Entra Kerberos is the identity source." The Azure Files identity page also says, in general terms, "To access a file or directory, the identity needs share-level permission and the appropriate file or directory permission." The file-level page says, also in general terms, "When a user tries to access a file or directory, share-level, file-level, and directory-level permissions are enforced." The Azure Virtual Desktop [setup page](https://learn.microsoft.com/en-us/azure/virtual-desktop/create-profile-container-azure-ad) calls the portal's Manage access tab "the recommended configuration option for cloud-only and external identity users." None of the passages quoted in this paragraph is written specifically about whether ACLs are enforced for cloud-only users.

**Microsoft Entra Kerberos introduction page.** The [introduction page](https://learn.microsoft.com/en-us/entra/identity/authentication/kerberos) describes access to Azure Files for a cloud-only user under the heading "Cloud only identities scenarios (Preview)". It says "Authorization is enforced using Azure RBAC roles", and that "No on-premises AD or NTFS ACLs are involved—authorization is fully cloud-based." Under "Key Differences from Traditional Kerberos" it lists "No NTFS ACL enforcement; uses Azure RBAC." In its group limit section it says that for Azure Files "NTFS ACL checks depend on complete group membership in the ticket."

**FSLogix permissions page.** It tells you to configure the Windows ACLs for profile containers, and it does not separate cloud-only users from others.

The pages do not settle this, so this article does not claim either result. Design recommendation, not a documented step: before rollout, test with two cloud-only users that one cannot open the other's profile folder.

### Cloud-only identities on Azure Files: generally available or preview

The pages give different status for cloud-only identities on Azure Files.

Pages that describe it as generally available: the Azure Files [release notes](https://learn.microsoft.com/en-us/azure/storage/files/files-whats-new) list "Entra-only identity support for SMB Azure file shares is now generally available" under 2026 quarter 2, after a public preview listed under 2025 quarter 4. The Azure Virtual Desktop [what's new page](https://learn.microsoft.com/en-us/azure/virtual-desktop/whats-new) lists "FSLogix support for cloud-only and external identities is now generally available" under May 2026, after a preview listed under November 2025.

Pages that label it a preview: the Microsoft Entra Kerberos introduction page carries the headings "Cloud only identity (Preview)", "Support for cloud-only user identities (Preview)" and "Group SID limit in Entra Kerberos (Preview)", and the section describing cloud-only scenarios is headed "Cloud only identities scenarios (Preview)". The page gives no quarter or month for these headings.

Pages that carry no label: the Azure Files setup page and the Azure Virtual Desktop setup page describe the cloud-only setup without a preview label and without a general availability statement.

The FSLogix FAQ answers yes to cloud-only identities, "BUT, it requires understanding of the risks". It also lists limits: password changes during an active session are not supported on Microsoft Entra joined hosts or with Entra-only identities, and object-specific settings and application rule sets need traditional Active Directory identifiers.

The labels have not been reconciled. The Azure Files setup page also says cloud-only identities are supported in Azure public cloud regions but not in Azure US Gov or Azure operated by 21Vianet. Check the current status for your cloud and design before you plan for cloud-only users.

### Azure NetApp Files and Microsoft Entra Kerberos

For cloud-only users on Azure NetApp Files, the pages give two different answers.

The FSLogix page for Azure NetApp Files says Azure NetApp Files "does not currently support FSLogix profile access using Entra-only (cloud-only) identities, as Kerberos authentication without AD DS is not supported." The SMB FAQ lists Microsoft Entra Domain Services and AD DS as supported and says Azure NetApp Files "doesn't support AD join for Microsoft Entra ID at this time."

Two other Azure NetApp Files pages, [Understand Microsoft Entra Kerberos with Azure NetApp Files (preview)](https://learn.microsoft.com/en-us/azure/azure-netapp-files/understand-entra-id) and [Configure Microsoft Entra Kerberos authentication with Azure NetApp Files (preview)](https://learn.microsoft.com/en-us/azure/azure-netapp-files/configure-entra-kerberos-authentication-for-hybrid-cloud-identities), describe Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on SMB volumes. The understand page says Azure NetApp Files "supports Microsoft Entra Kerberos authentication for SMB volumes", and the configure page says it helps you "configure Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on Azure NetApp Files". Both label it a preview, and the Azure NetApp Files [release notes](https://learn.microsoft.com/en-us/azure/azure-netapp-files/whats-new) list "Support for Microsoft Entra Kerberos authentication (preview)" under September 2026.

The preview needs a feature registration step, a Standard SKU NAT gateway for outbound access to Microsoft Graph, and an Entra ID connection on the NetApp account. A NetApp account supports either Microsoft Entra ID or AD DS authentication, not both. The configure page says Windows ACLs can be set only with icacls (File Explorer is not supported, and icacls for groups is not supported for Entra-only identities). The text of both preview pages does not mention FSLogix.

The pages do not settle whether FSLogix profiles are supported on the preview. Check all four pages and the current status before you plan Azure NetApp Files for cloud-only users. This article makes no recommendation between the two readings.

### Cloud Cache failover: automatic or manual

The [Multiregion BCDR page for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr) says "When the first storage location fails or can't be reached, cloud cache automatically fails over to the secondary region". The FSLogix business continuity page says about its primary/failover design that "you have to manually initiate the failover process, which may require the approval of the business stakeholders", and about its active/active design that it "requires a manual decision by business stakeholders before initiating a failover". The pages do not say whether the statements describe the same step. This article does not settle it.

### Soft delete retention: 7 or 14 days

The Azure Files soft delete page says "By default, the retention period for file shares is 7 days" and allows 1 to 365 days. The [About Azure Files backup page](https://learn.microsoft.com/en-us/azure/backup/azure-file-share-backup-overview) says Azure Backup "enables the soft delete feature on a storage account level with a retention period of 14 days." The pages do not say how the two figures relate. This article does not settle it.

### Smaller differences

- **Service principal password expiry.** The Microsoft Entra Kerberos introduction page says the storage account's service principal password expires every six months and must be rotated. The Azure Files setup page ties its expiry warning to accounts set up through the earlier manual limited-preview steps. The pages do not say whether other setups are affected.
- **Storage File Data SMB Admin role.** The [share-level permissions page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-assign-share-level-permissions) describes it as equivalent to a storage account key. The [file-level permissions page](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-configure-file-level-permissions) says it does not work the same way, because existing ACLs still apply and the role adds the right to take ownership. The pages differ, and they do not say which description applies in every case. Check both before you rely on the role.
- **Group limit effect.** The Microsoft Entra Kerberos introduction page says in its limits section that if the cap of 1,010 groups is exceeded, "only the first 1,010 are included", and in its group-limit section that if the combined group SIDs exceed 1,010 "the Kerberos ticket cannot be issued and authentication fails." The same page also says heavily grouped users can fail intermittently. The Azure Files setup page says the ticket "can't be issued" in that case. The pages do not reconcile the results. Design recommendation, not a documented step: test with a user who belongs to many groups.
- **A Kerberos change.** Several FSLogix pages carry a notice that the default Kerberos encryption type in Windows is changing from RC4 to AES-SHA1 with the April 2026 Windows Server update. File shares that are not upgraded might have access problems afterward. The notice is still worded as upcoming and links a blog post; read both and check the current state before you deploy. The setup page says Microsoft Entra Kerberos always uses AES-256, and the Microsoft Entra Domain Services page recommends AES-256.
- **Azure NetApp Files limits.** One FSLogix page gives 25 TiB as the default quota per subscription, and the Azure NetApp Files limits page gives a regional capacity quota of 100 TiB per subscription. The storage options page gives up to 12.5 PiB per NetApp account, which the limits page does not list, and three performance levels where the limits page also lists Flexible.

## Permission mistakes to avoid

- **Setting only one permission layer.** Access needs both a share-level permission and a matching Windows ACL. With only the Azure role, the default ACLs stay in place. The file-level page lists default root permissions that include Modify for authenticated users, so users would not be limited to their own folders. With only the ACLs and no Azure role, access is denied, and so it is with the default share-level permission left at None and no roles assigned. For cloud-only users the pages differ on whether ACLs are enforced (first caveat).
- **Expecting a portal ACL change to reach existing folders.** The file-level page says inheritable permissions edited in the portal apply only to new items, and names the `Restore-AzFileAclInheritance` command from the RestSetAcls module for existing ones.
- **Mounting with PowerShell when setting ACLs with File Explorer.** Use `net use`. A share mounted with PowerShell is not visible to File Explorer or cmd.exe.

## How to check a setup

The checks for the host join state, the host pool sign-in setting and the storage identity source are in the identity model article. These checks cover the profile itself; run them in a test environment.

1. Sign in as a test user who has never had a local profile on the session host. A user who has signed in before already has a local profile, and FSLogix keeps using it unless you set `DeleteLocalProfileWhenVHDShouldApply`. The Azure NetApp Files page says that setting makes FSLogix permanently delete the local profile when a user should have an FSLogix profile.
2. On Azure Files, open the share in the Azure portal. A folder named `<user SID>_<username>` should appear, according to the Azure Virtual Desktop setup page.
3. On Azure NetApp Files, open the volume in the Azure portal and confirm that space is in use. Then open the mount path in File Explorer and confirm that a profile VHD or VHDX file exists.
4. Design recommendation, not a documented step: sign in as a second test user and confirm that the first user's profile folder cannot be opened, especially for cloud-only users.

## Sources

[Storage options for FSLogix profile containers](https://learn.microsoft.com/en-us/azure/virtual-desktop/store-fslogix-profile), [Directory and file-level permissions for Azure file shares](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-configure-file-level-permissions) and [Configure SMB storage permissions for FSLogix](https://learn.microsoft.com/en-us/fslogix/how-to-configure-storage-permissions).
