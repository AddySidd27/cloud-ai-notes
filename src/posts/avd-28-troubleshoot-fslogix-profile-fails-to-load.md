---
title: "Troubleshoot FSLogix: Profile Does Not Load or Is Temporary"
seoTitle: "FSLogix Profile Not Loading or Temporary: Troubleshooting"
layout: post.njk
permalink: "/azure-virtual-desktop/troubleshoot-fslogix-profile-fails-to-load/"
order: 128
part: 28
tags: [avd-series]
deck: "Find out why a user gets a temporary, empty or slow profile, read the FSLogix profile log, and fix the usual causes in order."
description: "Troubleshoot an FSLogix profile that does not load in Azure Virtual Desktop: temporary or empty profile, slow sign-in, access denied, locked or full container."
---

A user signs in to Azure Virtual Desktop and something is wrong with their profile. The desktop is empty. Their files are missing. Windows says it signed them in with a temporary profile. The "Please wait" screen runs for minutes. Or FSLogix blocks the sign-in with a message. This article gives you an order of checks to find out why.

FSLogix is the software that stores each user's profile in a container and attaches it at sign-in. The sign-in steps and the main settings are in [How FSLogix profile containers work](/azure-virtual-desktop/how-fslogix-profile-containers-work/). Permissions and storage choices are in [the storage and access article](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/). Daily care of containers (size, locks, corruption) is in [Operate FSLogix profiles day to day](/azure-virtual-desktop/operate-fslogix-profiles-day-to-day/). This article starts from the symptom and works backwards to the cause.

One notice matters here: the April 2026 Windows Server update. Kerberos is the way Windows proves to a file share who a user is, and the update changes the default encryption type it uses from RC4 to AES-SHA1. File shares that hold containers and are not upgraded to AES-SHA1 might have access problems after the change. If access started failing after Windows Server updates, check the storage side first. The notice is explained in the daily operations article linked above.

## Key terms

| Term | Meaning |
|---|---|
| Session host | A virtual machine that runs users' desktops or apps. |
| FSLogix profile container | A virtual disk file (VHD or VHDX, written VHD(x)) that holds one user's profile. FSLogix attaches it at sign-in so Windows sees it as the user's profile folder. |
| Temporary profile | A blank profile that Windows gives a user when the real profile cannot be loaded. It is deleted at sign-out. |
| Local profile | A profile stored on the session host's own disk. |
| SMB share and UNC path | An SMB share is a network file share. A UNC path is its address, such as `\\server\share`. Azure Files shares use SMB. |
| `VHDLocations` | The FSLogix setting that lists where containers are stored. Cloud Cache setups use `CCDLocations` instead. |
| Profile log | A text file FSLogix writes on the session host. It records each step of a user's sign-in and sign-out. |
| SID | Security identifier. The unique ID Windows gives a user. It appears in FSLogix log lines and in the container folder name. |
| Registry | The Windows settings store. `HKLM` is its machine-wide section. |
| Log Analytics workspace | An Azure place where logs are stored and queried. |
| KQL | Kusto Query Language, the language used to query a Log Analytics workspace. |
| CorrelationId | An ID that ties together every log row for one connection. |

## Before you start

You need to sign in to the affected session host as an administrator, the way you normally manage a VM (for example over Azure Bastion or RDP), and have read access to the Log Analytics workspace if you want to run the queries below. The queries only return data if diagnostics were switched on before the problem happened. [Turn on the logs and learn to read them](/azure-virtual-desktop/troubleshoot-avd-start-here/) shows how.

The AVD logs tell you whether the user connected and how long sign-in took. The reason a profile failed is almost always in the FSLogix logs on the session host. Plan to work on the host.

## What to check first

| What the user sees | Start with |
|---|---|
| Temporary profile, or a profile that looks new | Checks 1 to 5 |
| Empty desktop, but the folder under `C:\Users\` has the user's normal name | Check 6 |
| Sign-in blocked with an FSLogix message | Checks 2 and 3, then "Blocked sign-in" below |
| Very long sign-in or hang at sign-out | Checks 4, 5 and 7 |

The picture shows the same order as a decision tree. Each leaf names its source.

![Six yes/no checks, from FSLogix enabled with VHDLocations set, through access denied, a locked container, SMB reachability, full storage and an empty profile. Each answer leads to a fix, or to collecting logs for a support case.](/img/avd/troubleshoot-fslogix-profile-fails-to-load.svg)

*Source: [Old, temporary or local profiles](https://learn.microsoft.com/en-us/fslogix/troubleshooting-old-temp-local-profiles), [Container attach or detach](https://learn.microsoft.com/en-us/fslogix/troubleshooting-container-attach-detach) and [FSLogix codes](https://learn.microsoft.com/en-us/fslogix/troubleshooting-error-codes).*

## Work through the checks in order

### 1. Is FSLogix switched on and pointed at storage?

After you install FSLogix, none of its features are enabled. Nothing is created for you, so a host with a half-finished setup behaves as if FSLogix is not there.

1. On the session host, search the Start menu for `regedit` and open the Registry Editor. Use the folder tree on the left to browse to each key.
2. Go to `HKEY_LOCAL_MACHINE\SOFTWARE\FSLogix\Profiles`. For Office containers (ODFC), go to `HKEY_LOCAL_MACHINE\SOFTWARE\Policies\FSLogix\ODFC`.
3. Check that `Enabled` is `1`. Its default is `0`, which means profile containers are disabled.
4. Check that `VHDLocations` (or `CCDLocations` for Cloud Cache) has a value. The type must be REG_SZ (preferred) or REG_MULTI_SZ. With REG_SZ, separate several locations with a semicolon.

If a setting is missing or wrong, fix it and have a test user sign in again. Test access to the location with a test user before you roll it out.

### 2. Read the profile log for this user

The profile log is the first place to look. It is a text file on the session host:

`C:\ProgramData\FSLogix\Logs\Profile\Profile_%date%.log`

A new file is created each day. If the folder is empty, check the logging settings. `LoggingEnabled` defaults to `2` (all logs on) and `LoggingLevel` defaults to `1` (informational, warning and error lines). Setting `LoggingEnabled` to `0` turns all log files off.

1. Open the file for the day of the problem.
2. Search for `LoadProfile: ` followed by the user's account name (the `samaccountname`, which is the sign-in name without the domain, such as `alex` for `CONTOSO\alex`). Use Ctrl+F in Notepad.
3. Make sure the time matches the time the user reports.
4. Note the process ID on that line. The same ID is used for the whole sign-in or sign-out of that user, so you can follow one user while other users sign in at the same time.
5. Look for these markers: `Begin Session: Logon`, `Begin Session: Logoff`, `loadProfile time:` and `unloadProfile time:`.

Every line starts with a type. `[INFO]` is information. `[WARN:xxxxxx]` is a warning. `[ERROR:xxxxxx]` is an error. The number after `WARN` or `ERROR` is a Windows system error code, written in hexadecimal. `00000005` is code 5.

The lines to look for are the `[ERROR:...]` line just before the final `LoadProfile failed` line. The table in check 3 shows what the common ones look like.

### 3. Match the error to a cause

These are example lines. Your lines will have your own names, paths and version numbers.

| What the log shows | What it means | Go to |
|---|---|---|
| `[ERROR:00000005] ... Failed to attach VHD. (Access is denied.)` | The user or the session host cannot read or write the container on storage. | Check 3a |
| `[ERROR:000000a7] Operation 'AcquireExclusiveLock' failed ... (Unable to lock a region of a file.)`, then `ErrorCode set to 33` | Another session already holds the container. | Check 3b |
| `[ERROR:00000021] LoadProfile failed ... FrxStatus: 33 (The process cannot access the file because another process has locked a portion of the file.)` | The same locked-container case, at the final line. | Check 3b |
| `[ERROR:0000052e] FindFile failed for path ... (The user name or password is incorrect.)` followed by `Status set to 27: Cannot find virtual disk at the provided location` | FSLogix could not sign in to the storage path to look for the container. Check how the host authenticates to the share. | Check 3a, then check 4 |
| `[ERROR:000000b7] No Create access ... (Cannot create a file when that file already exists.)` | An example of a create failure on the share. | Check permissions and the folder names on the share |

For any other code, look it up. There are three ways: the Windows System Error Codes list, the Windows Error Code Lookup tool, and the `NET HELPMSG` command.

#### 3a. Access is denied

Permissions on the storage are one of the most common mistakes in an FSLogix setup. Depending on the storage there are three layers: NTFS access control lists (ACLs), share-level permissions, and Azure role-based access control (Azure RBAC).

The recommended NTFS ACLs for an SMB share are:

| Principal | Access | Applies to |
|---|---|---|
| CREATOR OWNER | Modify | Subfolders and files only |
| Domain Admins group (or your own admin group) | Full Control | This folder, subfolders and files |
| Domain Users group (or the group of users who need profiles) | Modify | This folder only |

For Azure Files, the permissions how-to recommends giving all authenticated identities the share-level role Storage File Data SMB Share Contributor. To set the Windows ACLs on an Azure file share, you need either the Storage File Data SMB Share Elevated Contributor role or to mount the share with the storage account key. Do the full steps in [Configure SMB storage permissions](https://learn.microsoft.com/en-us/fslogix/how-to-configure-storage-permissions).

A quick test: sign in as the user, or use a test user, browse to the `VHDLocations` path and try to create a file or folder. If the user can open the path but cannot write, it is permissions. If the user cannot reach the path at all, go to check 4.

#### 3b. The container is locked by another session

By default FSLogix allows a user only one connection to a container. If the user signs in to a second session host while the first session is still open, the second one gets a temporary profile.

You have three choices, and each organization has to decide:

- Let the user work with a temporary profile.
- Block the sign-in with `PreventLoginWithTempProfile`, and teach users to sign out before they start a new connection.
- Allow multiple or concurrent connections to one container. This is a design choice, so read the concurrent connections article first.

A session that ended badly can leave a container locked as well. That case, and `CleanupInvalidSessions`, are covered in [Operate FSLogix profiles day to day](/azure-virtual-desktop/operate-fslogix-profiles-day-to-day/).

### 4. Can the host reach the share?

If the log shows the path cannot be found or reached, check name resolution and the SMB port from the session host. In PowerShell, run:

```powershell
Test-NetConnection -ComputerName <server-fully-qualified-domain-name> -CommonTCPPort SMB
```

Replace the placeholder with the fully qualified name of the file server or the Azure Files endpoint. Also test from a different virtual machine. If the path works from there but not from this host, look at that host's network settings, DNS, firewall, and any third-party firewall or intrusion prevention product. To find out if such a product is the cause, disable it on a test host and try again. Also review the FSLogix list of recommended antivirus exclusions.

### 5. Is the container or the storage full?

A container must have more than 200 MB free to attach. To check:

1. Look at the `SizeInMBs` setting on the host. Its default is 30000 (about 30 GB).
2. Find the user's container file on the share, right-click it, and open Properties.
3. Compare "Size on disk" with the `SizeInMBs` value.

If the container is full, raise `SizeInMBs`. This affects every user whose containers are dynamic disks. You can raise the value at any time but you cannot lower it, and lowering it does not shrink existing containers. FSLogix extends existing containers to the new size at sign-in. Deleting content inside the container lets it shrink at sign-out on FSLogix 2210 or later. Be careful what you delete: the wrong deletion can cause data loss or profile corruption.

Also check the storage itself. If the storage has reached its maximum size, users cannot create new containers and end up with a temporary or local profile, sessions can hang, and containers can fail to attach or detach. The fix is more capacity.

### 6. Empty or new profile, but not a temporary one

There are two causes.

**An old local profile exists.** When FSLogix is installed on a host that already has local profiles, it uses the local profile by default and does not look for a container. A user who has no local profile on this host gets an FSLogix profile that looks new. `DeleteLocalProfileWhenVHDShouldApply` set to `1` deletes the local profile at sign-in and attaches the container. FSLogix then permanently deletes the local profile. Look at which local profiles exist before you turn this on. The log reason code for this case is 3, "A local profile for this user exists on this system".

**A folder-name setting changed after containers were created.** If `FlipFlopProfileDirectoryName`, `SIDDirNameMatch`, `SIDDirNamePattern`, `VHDNameMatch` or `VHDNamePattern` was changed after containers existed, FSLogix looks for a folder name that is not on the share. It cannot find the old container, so it creates a new empty one. The user's data is not lost. It is still at the old path.

1. Check the current value of each setting under `HKLM\SOFTWARE\FSLogix\Profiles` (or the ODFC path above).
2. Browse the share and note the folder name format (`SID_username` or `username_SID`).
3. If they do not match, either revert the setting, restart the FSLogix Apps Services (`frxsvc`) and have users sign out and in again, or rename the existing folders to match (all affected users signed out first; if the VHD name setting also changed, rename the VHD(x) file as well).

To avoid this, choose these settings at the start, before profiles exist.

### 7. Slow sign-in

Long sign-ins can come from the host rather than the profile. A host with too many users, or too small for the workload, is a known cause. Reduce the number of simultaneous sessions per host, or move to a larger VM size. See [Choose session host VM sizes](/azure-virtual-desktop/choose-session-host-vm-sizes/). Cloud Cache puts more load on the VM, so size for it. Measure CPU during sign-in to check the size.

To see how long sign-in takes across a host pool, run this query. It is the "Average session logon time" sample from the Azure Monitor query reference.

```kusto
WVDConnections
| where TimeGenerated > ago(24h)
| where State == "Started"
| project CorrelationId , UserName, ConnectionType , StartTime=TimeGenerated, _ResourceId
| join kind=inner
(
    WVDConnections
    | where State == "Connected"
    | project ConnectTime=TimeGenerated, CorrelationId
) on CorrelationId
| join kind=inner
(
    WVDCheckpoints
    | where Name =~ "LoadBalancedNewConnection"
    | extend LoadBalanceOutcome=tostring(parse_json(Parameters).LoadBalanceOutcome)
) on CorrelationId
| project Duration = ConnectTime - StartTime, _ResourceId, Session=case(LoadBalanceOutcome in ("Active", "Disconnected"), "ExistingSession", LoadBalanceOutcome == "Pending", "Creating", LoadBalanceOutcome)
// Exclude connections that are happening while another connection kicked off the session creation, since results will be inconclusive
| where Session != "Creating"
| summarize AvgDuration=avg(Duration) by _ResourceId, Session
| parse _ResourceId with "/subscriptions/" subscription "/resourcegroups/" ResourceGroup "/providers/microsoft.desktopvirtualization/hostpools/" HostPool
| project ResourceGroup, HostPool, Session, AvgDuration
| sort by AvgDuration desc
```

How the query works, in short. The first block takes each connection's `Started` row and its `Connected` row (matched on `CorrelationId` with `join`) and keeps the time difference as `Duration`. The `WVDCheckpoints` part tells it whether the user reached a new session or an existing one. The last lines average the duration for each host pool and session type and put the slowest first. The result has one row per host pool and session type, with `AvgDuration` in `hh:mm:ss` form.

A healthy result is a short, steady duration, and an `ExistingSession` row (reconnecting) is normally shorter than a new session. A bad result is a host pool whose `AvgDuration` is much longer than the others, or longer than it used to be. There is no fixed number for "too long", so compare host pools and days with each other. If the query returns nothing, check that diagnostics are on for the host pool and that the Checkpoints category is ticked.

Read the result with care. The time to connect includes the time a user spends typing credentials, so a peak can be a false one. And in rare cases the "completed" event of a connection goes missing, which affects some results. For one user's slow sign-in, the better evidence is the `loadProfile time:` line in that user's profile log.

To look at one user's connections and errors, use the two samples below. Replace `userupn` with the user's UPN (the sign-in name that looks like an email address). The [start article](/azure-virtual-desktop/troubleshoot-avd-start-here/) explains each line and what healthy and bad results look like: a healthy attempt shows Started, Connected and Completed rows, and a bad one stops early or has an error row.

```kusto
WVDConnections
|where UserName == "userupn"
|take 100
|sort by TimeGenerated asc, CorrelationId
```

```kusto
WVDErrors
| where UserName == "userupn"
|take 100
```

If the user has no rows in either table, the connection never reached the Azure Virtual Desktop service. The problem is then at the client, the network, or sign-in, and not the profile. The `WVDErrors` table is for errors that happen while a user subscribes to apps or connects, and for management and host registration errors. When `ServiceError` is `false`, an administrator can fix the cause. When it is `true`, escalate with the CorrelationId.

## Event logs on the session host

FSLogix also writes to the Windows event log. In Event Viewer open Applications and Services Logs, then FSLogix. The Admin and Operational logs under Apps hold most entries. Cloud Cache has its own Admin and Operational logs under CloudCache.

One entry you can skip: a session host that is only Microsoft Entra joined (not domain joined or hybrid joined) logs two Event ID 26 errors from the Operational log. These are expected and can be ignored.

## Registry state for one user

FSLogix also records three values for each signed-in user in the host's registry, under `HKLM\Software\FSLogix\Profiles\Sessions\<SID>` for profile containers (the SID is on the `LoadProfile` line in the log). The values are `Status`, `Reason` and `Error`. These are the ones that matter most:

| Value | Code | Meaning |
|---|---|---|
| Status | 0 | Success |
| Status | 12 | Can't attach to virtual disk |
| Status | 25 | Maximum sessions reached |
| Status | 27 | Can't find virtual disk at the provided location |
| Status | 28 | No user session config found |
| Status | 100, 200 | Normal: waiting for the Windows Profile Service, and setup in progress |
| Reason | 0 | The container is attached |
| Reason | 1 | User isn't a member of the include group |
| Reason | 2 | User is a member of the exclude group |
| Reason | 3 | A local profile for this user exists on this system |
| Reason | 7 | Profile is a Windows temporary profile |
| Reason | 9 | Profile load failed |

Reason codes only explain the normal statuses, not the error statuses. The `Error` value is a Windows system error code. The full tables are in [FSLogix codes and what they mean](https://learn.microsoft.com/en-us/fslogix/troubleshooting-error-codes).

## Blocked sign-in

Two settings stop a user from signing in when the profile fails. With `PreventLoginWithFailure` set to `1`, FSLogix blocks the sign-in if it cannot attach or use an existing container. With `PreventLoginWithTempProfile` set to `1`, it blocks the sign-in if a temporary profile was created. Both default to `0`. The user gets a prompt to call support, and the only option is to sign out. FSLogix does this by replacing the Windows shell with `frxshell.exe`.

This does not apply to RemoteApp users. Remote apps do not start the standard Windows shell, so FSLogix cannot hook in, and those users are not blocked. There is no workaround, and the cause is most often storage permissions. Go to check 3a.

## Fixes by cause

| Cause | How you know | Fix |
|---|---|---|
| FSLogix profile feature is off or `VHDLocations` is wrong | `Enabled` is `0`, or the location is missing or the wrong type | Set `Enabled` to `1`. Set `VHDLocations` or `CCDLocations` as REG_SZ or REG_MULTI_SZ. |
| Users lack permission on the storage | `[ERROR:00000005]` and "Access is denied" | Set the NTFS ACLs, share-level permissions and Azure RBAC role for the storage type. |
| Container in use in another session | `[ERROR:000000a7]`, error code 33, "locked a portion of the file" | Sign out the other session, block the sign-in with `PreventLoginWithTempProfile`, or design for concurrent connections. |
| Host cannot reach or resolve the share | The path fails in `Test-NetConnection`, or works from another VM only | Fix DNS, network or firewall. Check third-party firewall or IPS. Check the antivirus exclusions. |
| Container is full | Size on disk is near `SizeInMBs`, less than 200 MB free | Raise `SizeInMBs`. Free space inside the container with care. |
| Storage is full | New containers fail, sessions hang, attach or detach fails | Increase the capacity of the storage. |
| Old local profile exists | Reason code 3, or a new-looking profile on a host with older profiles | Review the local profiles, then consider `DeleteLocalProfileWhenVHDShouldApply`. |
| Folder-name setting changed | Empty profile, no temporary profile, new container created next to the old one | Revert the setting or rename the folders. |
| Host too small or too many users | Long sign-in, slow `loadProfile time:` | Reduce sessions per host or use a larger VM size. |
| `frxsvc.exe` crash with `InstallAppxPackages` (FSLogix 2210, 2.9.8361.52326) | Default or temporary profile on that version | Install the latest FSLogix. This does not cover every case of a profile failing to load. |

## If the profile still does not load

Collect the logs before you open a support case. The FSLogix Support Tool gathers the needed logs into one zip file. Include the profile log, the FSLogix event logs, the FSLogix version, and the time of the failed sign-in. The two trace files in `C:\ProgramData\FSLogix\Logs` (`trace.etl.001` and `trace.etl.002`) are for Microsoft internal use only, so you do not need to read them.

If a user's sign-in failed and the AVD error row has `ServiceError` set to `true`, include the CorrelationId from `WVDErrors` in the case.

Next: [Troubleshoot an AVD Session Host That Is Unavailable or Needs Assistance](/azure-virtual-desktop/troubleshoot-session-host-unavailable-health-checks/).

## Sources

- [Old, temporary or local profiles](https://learn.microsoft.com/en-us/fslogix/troubleshooting-old-temp-local-profiles)
- [FSLogix codes and what they mean](https://learn.microsoft.com/en-us/fslogix/troubleshooting-error-codes)
- [Logging and diagnostics](https://learn.microsoft.com/en-us/fslogix/troubleshooting-events-logs-diagnostics)
