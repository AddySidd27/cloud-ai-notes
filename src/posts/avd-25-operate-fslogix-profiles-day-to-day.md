---
title: "Operate FSLogix Profiles Day to Day: Cloud Cache, Size, Locks and Corruption"
seoTitle: "FSLogix Operations: Cloud Cache, Compaction, Locks, Corruption"
layout: post.njk
permalink: "/azure-virtual-desktop/operate-fslogix-profiles-day-to-day/"
order: 125
part: 25
tags: [avd-series]
deck: "Decide if you need Cloud Cache, keep containers small with compaction, clear stuck sessions, and avoid the usual causes of corruption."
description: "How to run FSLogix profile containers in Azure Virtual Desktop: Cloud Cache, container size and compaction, locked containers, and corruption."
---

The profile design is done. Users sign in and their profile loads. Now you have to keep it healthy. Containers (the virtual disk files that hold each user's profile) grow. A session ends badly and leaves a container locked (in use, so the next sign-in cannot open it). A virus scanner damages a file. A storage problem slows every sign-out.

This article covers that daily work. It starts with Cloud Cache, an optional FSLogix feature that you may or may not need. Then it covers container size and compaction (making a container file smaller), locked containers, and corruption.

The basics are in two earlier articles. [How FSLogix profile containers work](/azure-virtual-desktop/how-fslogix-profile-containers-work/) explains the sign-in steps, the main settings and the default one-session-per-container lock. [The storage and access article](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/) covers where to store containers, permissions, and what the storage survives. This article does not repeat them.

One notice matters here: the April 2026 Windows Server update. It changes the default Kerberos encryption type from RC4 to AES-SHA1. Kerberos is the sign-in protocol Windows uses for file shares. RC4 and AES-SHA1 are two ways it encrypts tickets. File shares that host containers and are not upgraded might have access problems. Complete the upgrade to AES-SHA1 before you install the update. Check the current state on the storage that hosts your containers, such as Windows file servers.

## Key terms

| Term | Meaning |
|---|---|
| Session host | A virtual machine that runs users' desktops or apps. |
| Host pool (pooled) | A group of session hosts that many users share. A user can land on a different host at each sign-in. |
| Registry and `HKLM` | The Windows settings store. `HKLM` is its machine-wide section. |
| Local profile | A profile stored on the session host's own disk. |
| ODFC | Office container, a second, optional container for Microsoft 365 app data. |
| Container | The virtual disk file (VHD or VHDX) that holds a user's profile data. |
| SMB | The network file-share protocol that Windows uses. Azure Files shares use it. |
| Storage provider | The place that stores containers. This is an SMB file share, or, with Cloud Cache only, an Azure page blob (a type of Azure blob storage made for disk files). |
| Mount (attach) | Make the container file appear to Windows as a disk. |
| Cloud Cache | An optional FSLogix setup. The session host keeps a local copy of the container and sends every change to one or more storage providers. |
| `CCDLocations` | The FSLogix setting that lists the storage providers for Cloud Cache. A standard setup uses `VHDLocations` instead. |
| Local cache | The local copy of the container that Cloud Cache keeps on the session host. |
| Proxy file | A small stand-in file that Cloud Cache mounts as the user's container. It uses no disk space itself. |
| Hydrate | Cloud Cache reads missing data from a provider and copies it to the local cache. |
| Flush | Cloud Cache writes changes from the local cache to the providers. |
| Healthy and unhealthy provider | Healthy means the provider works. Unhealthy means it does not (for example, no connection or no permission). |
| Dynamic disk | A virtual disk that starts small and grows as the user adds data, up to a maximum size. A fixed disk always takes its full size. |
| `SizeInMBs` | The FSLogix setting for the maximum size of a container, in megabytes. |
| Compaction | Making a container file smaller on disk by giving back unused space. |
| Temporary profile | A blank profile that Windows gives a user when the container does not attach. |
| Event ID | The number of an entry in a Windows event log. |
| Event Viewer | The Windows tool that shows event logs. |
| Forced sign-out | A sign-out that FSLogix ends after the timeout, even though the providers are not all up to date. |
| Failover | Moving users to the second storage or region when the first one fails. |
| High availability | Keeping a service working when one part fails. |
| Disaster recovery | Getting back to work after a large failure, such as a whole region going down. |
| `ProfileType` | The FSLogix setting that says whether several sessions may use one container at the same time. 0 is the normal one-connection setting. |
| CU1 | Cumulative update 1, a bundle of fixes released after a version. |

## Do you need Cloud Cache?

Start with this question, because Cloud Cache adds disk work and local storage on the virtual machine. It also means paying for more than one storage provider.

The [Cloud Cache overview](https://learn.microsoft.com/en-us/fslogix/concepts-fslogix-cloud-cache) says its job is to protect users from short-term or intermittent storage problems close to the session host. It can also be part of a disaster recovery plan when the providers are in different regions. It puts a performance and storage need on the virtual machine, because of the extra disk work and the local cache.

The FSLogix FAQ asks the same question, "Do I need to use Cloud Cache for high availability?", and answers no. A standard container on highly available storage is acceptable. It names Azure Files with zone-redundant storage (ZRS, which keeps copies in several zones of one region) as a recommended provider.

| | Standard container | Cloud Cache |
|---|---|---|
| Setting that names the storage | `VHDLocations` | `CCDLocations` |
| Where the user works | On the container on the share | On a local copy on the session host |
| Storage needs | One provider | One to four providers (SMB or Azure page blob) |
| Extra load on the session host | None | More disk work and disk space for the local cache |
| Sign-out | Normal (compaction can add a short wait) | Can be slower, because the host waits for the providers |

Pick standard containers first. Choose Cloud Cache only if you have a clear reason, such as a plan to keep copies in two regions. For the failover and recovery side, read the storage article. Plan for a manual failover until you have tested it.

## How Cloud Cache works

If you use standard containers, you can skip to "Keep containers from filling up". The picture below shows the parts. Then the steps in words:

![Cloud Cache keeps a local copy of the container on the session host. The user works on the local copy. FSLogix reads from the first healthy storage provider when data is missing, and writes every change to all providers. At sign-out, if a provider is behind, sign-out waits until the providers match, for as long as the timeout setting allows. If all providers are down, the user keeps working on the local cache, but data that is not in it cannot be read, which can hang the session.](/img/avd/AVD-FSLogix-Cloud-Cache.svg)

*Source: [Cloud Cache overview](https://learn.microsoft.com/en-us/fslogix/concepts-fslogix-cloud-cache). The picture is simplified. Its steps 4, 5 and 6 match steps 4, 5 and 6 in the list below. Its steps 1 to 3 combine list steps 1 to 3, and list step 7 is not drawn. `CcdUnregisterTimeout` is explained in "Set up Cloud Cache".*

1. **First sign-in.** FSLogix creates a local container in `C:\ProgramData\FSLogix\Cache`. It copies data from a provider into it as Windows asks for it.
2. **Later sign-ins.** By default FSLogix looks for the old local cache and mounts it. The Cloud Cache overview says this default can lead to low disk space events on the host.
3. **During the session.** The user works on the local copy. A proxy file (`Profile_%username%.vhd`) is mounted as the container. It is not a true VHD, and its size on disk is zero.
4. **Reads.** If the local copy lacks the data, Cloud Cache hydrates it from one provider. That is the first provider in `CCDLocations`, unless it is unhealthy.
5. **Writes.** Changes are written to the local copy first. Cloud Cache then flushes them to all providers in the background. Each provider is flushed on its own thread (its own stream of work).
6. **Sign-out.** If a provider does not have all the changes, the sign-out waits until all providers match.
7. **Out of sync.** If a provider is behind at sign-in, Cloud Cache clones a full copy to it. New changes stay in the local cache until the providers are equal.

Two helper files exist. The lock file lives only on the remote providers. Cloud Cache uses it to know which VM holds the container. The meta file tracks the container state with a sequence number, so Cloud Cache knows which provider has the newest data. The Cloud Cache overview says these files are for FSLogix only and are not meant to be opened.

Things to know from the Cloud Cache overview:

- If all providers go unhealthy during a session, the local cache keeps working and grows, up to the `SizeInMBs` limit.
- If Cloud Cache needs data it cannot hydrate from any provider, the Cloud Cache overview warns of a session hang, or worse, a system crash (a blue screen).
- List providers by closeness first, then by preference.
- `Ping` and `Test-NetConnection` are bad ways to judge a provider. They do not measure real disk work.
- A provider that is often behind may be a slow provider.
- Cloud Cache puts more load on the session host. Published starting ratios differ a lot, so test with real users to find the right number of users for each vCPU (virtual CPU). [The VM sizing article](/azure-virtual-desktop/choose-session-host-vm-sizes/) covers sizing.

## Set up Cloud Cache

The Cloud Cache tutorial covers setup. These are the points that matter.

**Use `CCDLocations` instead of `VHDLocations`.** Do not set both. `CCDLocations` accepts SMB and Azure page blob providers, up to four. The first one is the primary. Separate several providers with a semicolon (`;`), as in the tutorial.

**Mind the format.** The page gives these tips: no spaces around the commas and equals signs (spaces inside quotes are fine), and parameter names and values are case sensitive (`type=smb` is right, `type=SMB` is wrong). An example with an SMB provider:

```text
type=smb,name="SMB PROVIDER 1",connectionString=\\<server-name>\<share-name>
```

For an Azure page blob provider, use the name of a protected key in the connection string. Never put the plain-text connection string in the setting. Protect the connection string with a key instead; the FSLogix guide on protecting connection strings shows how.

**Use the recommended values.** The tutorial table lists these values for a Cloud Cache profile container (all but `ProfileType` are marked as recommended):

| Value | Setting | Why the tutorial uses it |
|---|---|---|
| 1 | `ClearCacheOnLogoff` | Saves local disk space and reduces the risk of data loss with pooled host pools. |
| 1 | `HealthyProvidersRequiredForRegister` | Tutorial: stops users from creating a local cache when a provider is not healthy. The settings reference adds that sign-in then fails when no provider is healthy, and says to set `PreventLoginWithFailure` or `PreventLoginWithTempProfile` for the behaviour you want (see below). |
| 1 | `DeleteLocalProfileWhenVHDShouldApply` | Users do not lose data in a local profile by accident. |
| 0 | `ProfileType` | One connection at a time. This is the default. The tutorial says it is simpler and faster. |

The tutorial also sets `Enabled`, `FlipFlopProfileDirectoryName`, `LockedRetryCount`, `LockedRetryInterval`, `ReAttachIntervalSeconds`, `ReAttachRetryCount`, `SizeInMBs` and `VolumeType`, as in a standard setup.

Three settings in the table differ from the defaults in the settings reference:

- `HealthyProvidersRequiredForRegister` defaults to 0, so users can sign in even when no provider is available.
- `ClearCacheOnLogoff` defaults to 0, so the local cache stays after sign-out.
- `DeleteLocalProfileWhenVHDShouldApply` defaults to 0.

The tutorial sets all three to 1. I suggest the same values for pooled hosts. Read the data loss warning below before you change the sign-out settings.

If you set `HealthyProvidersRequiredForRegister` above 0, also set `PreventLoginWithFailure` or `PreventLoginWithTempProfile`. These two settings stop the sign-in when the container does not attach. The [settings reference](https://learn.microsoft.com/en-us/fslogix/reference-configuration-settings) says to use them to get the sign-in behaviour you want. By default, a profile that cannot attach can end in a temporary profile ([old, temporary or local profiles page](https://learn.microsoft.com/en-us/fslogix/troubleshooting-old-temp-local-profiles)).

The tutorial's retry values also differ from the defaults. They set how often and how long FSLogix retries a locked or detached container:

| Setting | Tutorial value | Default |
|---|---|---|
| `LockedRetryCount` | 3 | 12 |
| `LockedRetryInterval` | 15 | 5 |
| `ReAttachRetryCount` | 3 | 60 |
| `ReAttachIntervalSeconds` | 15 | 10 |

**Control what happens at sign-out.** Two settings decide this:

| Setting | Default | What it does |
|---|---|---|
| `HealthyProvidersRequiredForUnregister` | 1 | The number of healthy providers needed for a sign-out to finish. |
| `CcdUnregisterTimeout` | 0 | How many seconds a sign-out waits for the providers. The value 0 holds the sign-out until the required providers are back. The page warns this can be forever. |

Be careful here. The settings reference gives these warnings:

- Setting `HealthyProvidersRequiredForUnregister` to 0 is not recommended. It can permanently delete local cache data from a session. It also makes `CcdUnregisterTimeout` and `ClearCacheOnForcedUnregister` have no effect.
- `ClearCacheOnForcedUnregister` decides what happens to the local cache after a forced sign-out (a sign-out FSLogix ends when `CcdUnregisterTimeout` runs out before the providers are up to date). It defaults to 0, which keeps the local cache.
- Setting `ClearCacheOnForcedUnregister` to 1 may lose user data that was saved in the registry during the session. If a cache is kept, delete it by hand after you have recovered the user's data.

Read the full warning before you change these settings.

**Avoid a retired setting.** `CcdMaxCacheSizeInMBs` was retired on February 11, 2025 and is no longer supported.

**Check that it works.** On a session host, open Event Viewer (the Windows tool that shows event logs) and go to Applications and Services Logs, then Microsoft, FSLogix, CloudCache, Operational. Event ID 56 shows which providers are online. Event ID 5 shows the lock on the proxy file. In File Explorer, the local cache is in `C:\ProgramData\FSLogix\Cache\<username>_<sid>` (the SID is the user's security ID).

## Watch the providers

Microsoft provides a PowerShell module for Cloud Cache problems. It is called Microsoft.FSLogix. It loads by itself when you call it, and its commands (cmdlets) do not need administrator rights.

```powershell
Get-CloudCacheDisk
Get-CloudCacheProvider
```

[`Get-CloudCacheDisk`](https://learn.microsoft.com/en-us/fslogix/utilities/powershell/get-cloudcachedisk) lists the Cloud Cache disks for each signed-in user. Its State value can show that a sign-out is being held. For example, `WaitingForWriteQueueFlush` means the Cloud Cache service is waiting for all changes to reach the providers. Other states are `WaitingForSync`, `WaitingForZeroHandleCount` and `WaitingForUnhealthyProviders`.

`Get-CloudCacheProvider` shows each provider. Look at these values:

- **WriteQueueLength.** The number of changes waiting for that provider. Zero means the provider is in sync.
- **State.** `Valid` means in sync, `Invalid` means different from the local copy and will be synced, and `Replicating` means it is copying from a valid provider.
- **Connected.** Whether the service is connected to the provider.
- **AccessMode.** `NoAccess` can mean a problem with the provider, or that another machine holds the lock file.
- **LastLockOperation.** The result of the last test of the lock file. It is tested every 60 seconds by default ([Get-CloudCacheProvider](https://learn.microsoft.com/en-us/fslogix/utilities/powershell/get-cloudcacheprovider)).

A provider with a long write queue, or one that keeps going `Invalid`, is the first suspect for slow sign-outs.

## Keep containers from filling up

A full container causes odd problems. Users may see strange behavior in apps or when they open files. A container must have more than 200 MB free to attach.

What to know:

- **Watch the free space inside the container.** The default `SizeInMBs` is 30000 (30 GB), as [the first FSLogix article](/azure-virtual-desktop/how-fslogix-profile-containers-work/) shows. The FAQ says container size does not change sign-in time, and to plan for at least 30% free space. It also says to watch the logs for warnings at less than 2 GB free and less than 500 MB free.
- **Raise the limit if you must.** A larger `SizeInMBs` lets a dynamic container grow bigger, from the next sign-in. The change affects all users with dynamic disks. You can raise `SizeInMBs` but not lower it, and lowering it would not shrink existing containers anyway.
- **Check the real size.** On the share, right-click the container file, choose Properties, and compare Size on disk with `SizeInMBs`.
- **Watch the share too.** If the share itself is full, users may get a temporary profile, a hung session, or a container that fails to attach or detach, even when each container is fine. Alert when less than 20% of the share is free. The fix is more capacity.
- **Find the big data.** After the container grows, you can mount it off-hours and look for what uses the space. Deleting the wrong data can cause data loss or corruption, so be careful.
- **A `redirections.xml` file does not shrink an old container.** (This file lists folders to leave out of the container.) Excluding folders later does not remove data that is already in the container. FSLogix has no tool to remove it. You can delete the container and let FSLogix create a new one, or use a sign-in script that deletes the data (test it first).
- **Local profiles.** FSLogix does not remove existing local profiles when you start using it. `DeleteLocalProfileWhenVHDShouldApply` does, but users must save their data elsewhere first.

## Compaction gives space back

Deleting files in a dynamic disk does not make the file on the share smaller. Compaction does that. It is a built-in FSLogix feature.

**How it works.** At every sign-out, FSLogix checks if compaction is worth doing. It is on by default in FSLogix version 2210 and later. The setting is `VHDCompactDisk` under `HKLM\SOFTWARE\FSLogix\Apps`, and its default is 1.

It runs only when both of these are true:

- The container is bigger than 1 GB on disk.
- The space it can give back is at least 20% of the size on disk (explained below).

Call the size on disk A, and the smallest size the disk can shrink to B. C is A minus B, the space compaction can give back. Compaction runs when C is at least 20% of A. Here are two examples:

- A of 6 GB and B of 2.5 GB: C is 3.5 GB. That is more than 20% of 6 GB (1.2 GB), so it compacts.
- A of 12 GB and B of 10 GB: C is 2 GB. That is less than 20% of 12 GB (2.4 GB), so it does not.

**Rules and limits:**

- The disk must be dynamic. A fixed disk cannot be compacted.
- The Optimize Drives service (`defragsvc`) and the Microsoft Storage Spaces SMP service (`smphost`) must not be set to Disabled. Manual or Automatic is fine, running or stopped. If either is Disabled, compaction fails.
- The threshold is not configurable (FAQ).
- Compaction runs for at most 5 minutes ([VHD Disk Compaction](https://learn.microsoft.com/en-us/fslogix/concepts-vhd-disk-compaction#user-experience)). If it hits the limit, the sign-out continues and the next sign-out resumes.

**What users see.** The message "Waiting for FSLogix Apps Services" shows during sign-out. The [compaction page](https://learn.microsoft.com/en-us/fslogix/concepts-vhd-disk-compaction#user-experience) says an average run takes 20 to 30 seconds. The first run is the longest. Windows logs a Winlogon (Windows sign-in process) warning when a sign-out passes 60 seconds. The page calls these warnings normal and expected.

**A reconnect problem.** If a user disconnects during sign-out and signs in again before compaction ends, the disk is still in use. In a default setup the user gets a temporary profile.

**With Cloud Cache.** At sign-out, FSLogix downloads the disk from a provider, compacts it, and uploads it to the providers. This makes sign-out slower. The FAQ lists "Disable VHDCompactDisk" among its fixes for slow Cloud Cache sign-outs. Its other fixes: check the latency to all providers, move the storage to a higher tier, and do not use `ProfileType` 3 or `VHDAccessMode` 1, 2 or 3 (settings that let several sessions use one container, by creating differencing disks, small extra disks that hold the changes).

**If it does not run.** Look in three places.

- **The profile log.** It is in `C:\ProgramData\FSLogix\Logs\Profile`. By default FSLogix keeps about 2 days of logs (`LogFileKeepingPeriod`, [settings reference](https://learn.microsoft.com/en-us/fslogix/reference-configuration-settings#fslogix-settings-profile,-odfc,-cloud-cache,-logging)), so look soon after a problem. The default `LoggingLevel` is 1, which logs info, warnings and errors. Search for `[ERROR:`. The [Troubleshooting VHD Disk Compaction](https://learn.microsoft.com/en-us/fslogix/troubleshooting-vhd-disk-compaction) page lists `ERROR:00000422` ("The defragsvc is disabled") and `ERROR:00000102` ("Failed to query minimum supported size") under one heading. Its fix is to set the Optimize Drives (`defragsvc`) and Microsoft Storage Spaces SMP (`smphost`) services to Manual or Automatic.
- **The result line.** Search the log for `Disk size results`. A line with `WasCompacted: true` shows a compaction that ran. A line with `WasCompacted: false` is followed by a line that gives the reason.
- **The event logs.** In Event Viewer, go to Applications and Services Logs, Microsoft, FSLogix, Apps.

| Log | Event | Meaning |
|---|---|---|
| Operational | 57 | Says if a disk was compacted. |
| Operational | 61 | The disk is fixed size. |
| Admin | 60 | The compaction service is disabled. |

To set both services back to Manual, run these in an elevated PowerShell (as administrator):

```powershell
Set-Service defragsvc -StartupType Manual
Set-Service smphost -StartupType Manual
```

## Locked and stuck containers

A lock is normal. FSLogix keeps an exclusive lock on a container while the user is signed in. The first FSLogix article covers that.

The problem is a lock that should be gone. There are two causes.

- **An abrupt end.** A session ended abruptly, or a process blocked a proper sign-out. This can leave leftover data in the file system or registry. The container is not properly detached, and new sign-ins may be blocked.
- **More than one connection.** With the default exclusive lock, the second connection cannot get the container. By default it gets a temporary profile (see the old, temporary or local profiles page, linked above). With `PreventLoginWithFailure` set, the user cannot sign in. The locked-container page spells that setting `PreventLogonWithFailure`; see the differences table.

| What to try | Why |
|---|---|
| Find the root cause first | Fix environment or system problems before you treat the symptom. |
| Turn on `CleanupInvalidSessions` | The locked-container page recommends it. The settings reference says it lives under `HKLM\SOFTWARE\FSLogix\Apps`, its default is 0 (off), and it affects both profile containers and Office containers (ODFC). When on, FSLogix tries to clean up sessions that ended abruptly, so the next sign-in can work. |
| Use short retry values (from the tutorial, not the locked page) | The Cloud Cache tutorial sets `LockedRetryCount` 3, `LockedRetryInterval` 15, `ReAttachRetryCount` 3 and `ReAttachIntervalSeconds` 15 for a faster failure. These values make a failure show sooner. |
| Check Cloud Cache state (from the PowerShell page) | In a Cloud Cache setup, `Get-CloudCacheProvider` can show `AccessMode` as `NoAccess`. That means a problem with the provider, or that another machine holds the lock file. |

Run `frx.exe version` (in `C:\Program Files\FSLogix\Apps`) to see your FSLogix version. If you need help from Microsoft support, the FSLogix Support Tool collects the logs and settings for you. Check the known issues page and the release notes before you roll out a new FSLogix version.

One example: with profile containers and Office containers both turned on, `CleanupInvalidSessions` broke Office container create and mount in version 26.01. Version 26.01 CU1 (cumulative update 1) fixed it. The release notes also list fixes in FSLogix 26.08 for a sign-out deadlock with `CleanupInvalidSessions` and Office containers, and for a stuck container or storage provider that could block sign-ins and sign-outs.

One more case from the Azure architecture page about two-region designs. Only one process can open a profile file in read and write mode. If a user starts sessions in both regions at the same time, the second session cannot mount the profile disk, so the user cannot sign in, and FSLogix logs `ERROR_LOCK_VIOLATION` 33 (0x21). Keep users from connecting to both host pools at once.

The FSLogix disaster recovery page also says to make sure all users have signed out of the failover location before you fail back, because replication after a recovery can take a long time.

There is no published procedure for deleting a stuck lock by hand, so do not delete lock or meta files yourself. Use the supported setting and the troubleshooting pages, and open a support request if that is not enough.

## Corruption and missing data

Corruption has two main causes.

**Antivirus.** The page calls antivirus software one of the most common causes of container corruption. If a scanner works on data going into or out of a container, it can damage it. The FSLogix prerequisites page has an exclusion list. [The first FSLogix article](/azure-virtual-desktop/how-fslogix-profile-containers-work/) lists antivirus as a common mistake. These are the main groups:

- The FSLogix programs and drivers: `frxsvc.exe`, `frxccds.exe`, `frxdrv.sys`, `frxdrvvt.sys` and `frxccd.sys`.
- The folders `C:\Program Files\FSLogix\Apps` and `C:\ProgramData\FSLogix`, plus the per-user folder under `AppData\Local\FSLogix`.
- The Cloud Cache folders `%ProgramData%\FSLogix\Cache` and `%ProgramData%\FSLogix\Proxy`.
- The container files on the share (`*.VHD`, `*.VHDX`) and their `.lock`, `.meta` and `.metadata` files, and the temporary differencing disks in `%TEMP%` and `%WINDIR%\TEMP`.
- The FSLogix registry keys, and the container mount points.

Apply the exclusions in all layers of security, and check them after you roll out the policy. If you changed the cache or proxy folder, change the exclusions too.

**A bad `redirections.xml`.** It is tempting to exclude folders to save space. Be careful, and keep the file simple. [The first FSLogix article](/azure-virtual-desktop/how-fslogix-profile-containers-work/) covers what is safe to exclude.

Other points:

- A regional failure is never graceful, and users may lose data or meet corruption. [The storage article](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/) covers recovery.
- Microsoft supports only the latest FSLogix version, and gives hotfixes for known bugs. Keep the version current. [The golden image article](/azure-virtual-desktop/build-and-maintain-a-golden-image/) covers updating the agent software in the image.

There is no published procedure to repair a corrupted container. What you can do is prevent it and recover from storage snapshots, which the storage article covers. Treat restore as the plan, not repair.

## Details to check before you roll out

- **Version for compaction.** Use FSLogix 2210 or later, and preferably the latest version.
- **Setting name.** The sign-in blocking setting is `PreventLoginWithFailure`. Check the spelling before you set it.
- **Compaction with `ProfileType` 3 or `VHDAccessMode` 1, 2 or 3.** Install the latest version and test compaction if you use these modes.
- **Cloud Cache failover.** Plan for a manual failover until you have tested it. The storage article covers recovery.
- **Log file name.** Look in `C:\ProgramData\FSLogix\Logs\Profile` and open the newest file.

## Common mistakes

- **Using Cloud Cache for high availability when a ZRS Azure Files share is enough.** The FAQ says it is acceptable.
- **Putting both `VHDLocations` and `CCDLocations` in the registry.** Do not use both.
- **Leaving `CcdUnregisterTimeout` at 0 without knowing the risk.** A sign-out can be held forever.
- **Judging a provider with `ping`.** Use `Get-CloudCacheProvider` and its write queue.
- **Excluding folders in `redirections.xml` and expecting a smaller container.** The data stays.
- **Using fixed-size disks and expecting compaction.** Only dynamic disks compact.
- **Disabling the Optimize Drives or Storage Spaces SMP service.** Compaction then fails.
- **Skipping antivirus exclusions.** It is one of the most common causes of corruption.
- **Deleting container data by hand without a backup.** It can cause data loss or corruption.
- **Changing name settings after containers exist.** If you change `FlipFlopProfileDirectoryName`, `SIDDirNameMatch`, `SIDDirNamePattern`, `VHDNameMatch` or `VHDNamePattern`, users get an empty or new profile. The old data stays on the share. Revert the setting or rename the folders (old, temporary or local profiles page).
- **Ignoring a full file share.** The container may be fine and the share still full.

## How to check a setup

1. On a test session host, open the FSLogix registry key and confirm there is either `VHDLocations` or `CCDLocations`, and not both.
2. Sign in as a test user. In Cloud Cache setups, open the CloudCache Operational log and look for Event ID 56 and Event ID 5. Run `Get-CloudCacheProvider` and confirm `WriteQueueLength` returns to 0.
3. Sign out, then check that the sign-out did not hang. Look at `Get-CloudCacheDisk` while it runs.
4. Check the size of the user's container on the share against `SizeInMBs`, and the free space on the share (alert at 20%).
5. Check that compaction ran, using the log lines in "If it does not run" above.
6. Confirm the antivirus exclusions in the policy and on one test host.
7. End one test session abruptly on a test host, then sign in again. If the container stays locked, test `CleanupInvalidSessions`.
8. Write down the settings you changed, and why.

Next: [Troubleshoot AVD: Turn On the Logs and Learn to Read Them](/azure-virtual-desktop/troubleshoot-avd-start-here/).

## Sources

- [Cloud Cache overview](https://learn.microsoft.com/en-us/fslogix/concepts-fslogix-cloud-cache)
- [VHD disk compaction](https://learn.microsoft.com/en-us/fslogix/concepts-vhd-disk-compaction)
- [Troubleshooting container corruption or missing data](https://learn.microsoft.com/en-us/fslogix/troubleshooting-container-corruption)
