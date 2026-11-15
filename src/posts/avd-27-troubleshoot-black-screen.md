---
title: "Troubleshoot an AVD Black Screen After Sign-in"
seoTitle: "Troubleshoot an AVD Black Screen After Sign-in"
layout: post.njk
permalink: "/azure-virtual-desktop/troubleshoot-black-screen/"
order: 127
part: 27
tags: [avd-series]
deck: "Sort a black screen into connection, profile, Windows shell or screen sharing, and check each in a fixed order."
description: "Troubleshoot a black screen after sign-in to Azure Virtual Desktop: connection state, FSLogix profile logs, explorer.exe, Winlogon Shell and Teams screen sharing."
---

A user signs in to Azure Virtual Desktop (AVD). The credentials are accepted, and then the session shows only black. Sometimes a mouse pointer is visible. No desktop draws.

This article gives you an order for checking. It first separates a black screen from a connection that never finished, then checks the user's profile, the Windows shell on the session host, and one case where only screen sharing is black. You need to sign in to the affected session host as an administrator, the way you normally manage a VM (for example over Azure Bastion or RDP), because most of the evidence is on the host. Diagnostics must already be on. If they are not, start with [Turn on the logs and learn to read them](/azure-virtual-desktop/troubleshoot-avd-start-here/).

## Key terms

| Term | Meaning |
|---|---|
| Session host | A virtual machine that runs users' desktops or apps. |
| Shell | The program that draws the Windows desktop after sign-in. It is `explorer.exe` by default. |
| `userinit.exe` | The Windows program that runs when a user signs in and starts the shell. |
| FSLogix profile container | A virtual disk file that holds a user's profile. FSLogix attaches it at sign-in. |
| CorrelationId | The ID of one connection attempt. Every log row for that attempt carries it. |
| Event Viewer | The Windows tool that shows event logs. |
| Process dump | A file that saves the memory of a process, so someone can find out why it failed. |
| Winlogon | The Windows component that handles sign-in. Its registry key holds the `Shell` setting. |
| ProcDump and Process Monitor (ProcMon) | Free Microsoft Sysinternals tools. ProcDump saves process dumps. ProcMon records what programs do, including when they exit. |
| Registry and `regedit` | The registry is the Windows settings store. `regedit` is the Registry Editor. Search for it in the Start menu. |
| Screen capture protection | An AVD setting that blocks screenshots and screen sharing of remote content. |

## What the user sees

Three versions of "black screen" have different causes:

1. **Black right after the credentials, and it stays black.** This is the case the Windows black-screen guide covers: the system fails to load the user profile and desktop. Most of this article is about it.
2. **Black for a few minutes, then the desktop loads.** The standard black-screen steps do not cover this case. A slow profile load is one possible cause. The FSLogix profile log shows how long the load took.
3. **Black only when sharing the screen in Microsoft Teams.** See Check 1.

The Windows guide also does not cover a black screen that appears right after boot, before credentials are asked for.

## Quick map

Ask in this order. The first checks are the cheapest, and each one rules out a whole group of causes.

| Check | Question | If yes |
|---|---|---|
| 1 | Is it black only in a Teams screen share? | Screen capture protection. |
| 2 | Did the connection never reach `Connected`? | Not a black screen. Use the host or sign-in articles. |
| 3 | Are many users hit, starting after a Windows update? | Known issue for update KB5124008. |
| 4 | Does the FSLogix profile log show an error or a long load? | Profile problem. |
| 5 | Is FSLogix 2210 (2.9.8361.52326) installed? | Known fixed issue. Update FSLogix. |
| 6 | Are `explorer.exe` or `userinit.exe` not running? | Shell check, Event ID 1000, process exit codes. |

![Diagram: Black screen after sign-in: decision tree.](/img/avd/troubleshoot-black-screen.svg)

*Source: [Black screen after you sign in](https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/scenario-guide-black-screen-after-sign-in), [FSLogix known issues](https://learn.microsoft.com/en-us/fslogix/troubleshooting-known-issues) and [Screen capture protection](https://learn.microsoft.com/en-us/azure/virtual-desktop/screen-capture-protection).*

## Check 1: Only the Teams screen share

Screen capture protection blocks remote content in screenshots and screen sharing on the client. Teams sharing depends on supported client configurations. With an unsupported configuration, protected content might appear as a black screen during sharing. Check the Teams compatibility requirements for the current list.

A sign of this cause is that the session looks normal to the user and only the shared view is black. To check, look for the policy setting **Enable screen capture protection** on the session host. In Intune it is under **Administrative templates** > **Windows Components** > **Remote Desktop Services** > **Remote Desktop Session Host** > **Azure Virtual Desktop**. In Group Policy the same path starts at **Computer Configuration** > **Policies** > **Administrative Templates**. The options are **Block screen capture on client** and **Block screen capture on client and server**.

On macOS, enabling screen capture protection might interfere with Teams sharing, so shared windows can appear blank.

## Check 2: One user or many, and did the connection finish

In the Log Analytics workspace, select **Logs** and run the queries below. They are Log Analytics samples. Replace `userupn` with the user's UPN. Setup and table meanings are in [the start article](/azure-virtual-desktop/troubleshoot-avd-start-here/).

All connections for one user:

```kusto
WVDConnections
|where UserName == "userupn"
|take 100
|sort by TimeGenerated asc, CorrelationId
```

Errors for one user:

```kusto
WVDErrors
| where UserName == "userupn"
|take 100
```

The first query lists every connection row for the user, oldest first. The second lists the user's error rows. Read the first one like this: a healthy attempt has rows with the same `CorrelationId` and `State` values Started, then Connected, then Completed once the user signs out. A black screen sits in between: Connected is present and the user is still looking at black. If the second query shows a row near the time of the problem, read its `CodeSymbolic` and `Message`. If it shows nothing, that rules nothing out. Carry on with the host checks below. The start article explains each line of these queries.

For each attempt, look at the `State` column. A black screen after sign-in should have reached `Connected`. That state is written when the user connects to the VM that hosts the desktop. If you only see `Started`, the connection never reached a session host. That is a connection failure, not a black screen. Use [Troubleshoot an AVD Session Host That Is Unavailable or Needs Assistance](/azure-virtual-desktop/troubleshoot-session-host-unavailable-health-checks/) or [Troubleshoot AVD Sign-in Failures](/azure-virtual-desktop/troubleshoot-sign-in-and-conditional-access/).

If there are no rows at all, the connection did not reach the AVD service. Diagnostics cannot show it. Look at the client and the network instead.

To see errors and checkpoints for every attempt in one result, use the **Connection Errors** sample on the [WVDConnections sample queries page](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/queries/wvdconnections). Uncomment its user filter to look at one user.

To learn whether other users hit the same error, take `CodeSymbolic` from the error row:

```kusto
WVDErrors
| where CodeSymbolic =="ErrorSymbolicCode"
| summarize count(UserName) by CodeSymbolic
```

This counts how many users had that same error. One user means the problem follows that user. Many users mean a shared cause.

If `ServiceError` is `true` on the error, it is for Microsoft to fix. Open a support case and give the `CorrelationId`.

Many users on one host point to the host. One user points to the profile or the client.

## Check 3: A known Windows update issue

Known issue: users can see a black screen during sign-in after Windows update KB5124008. The black screen results from `explorer.exe` crashing during shell start-up. It affects FSLogix 2210 hotfix 4 (2.9.8884.27471) or later. The fix is still in progress, with no workaround, and is planned for a future release or a coordinated release with Windows. Check the FSLogix known issues page for the current state.

If many users broke after that update, treat it as this issue. Collect the evidence in Check 6 and open a support case.

## Check 4: The FSLogix profile log

On the session host, open the newest `Profile_%date%.log` in `C:\ProgramData\FSLogix\Logs\Profile`. Logging must be configured for this file to exist.

1. Search for `LoadProfile: <samaccountname>` for the user (the sign-in name without the domain).
2. Check the time matches the problem.
3. Note the process ID. It stays the same for the whole sign-in.
4. Look at `Begin Session: Logon`, `loadProfile time:` and any `[WARN:xxxxxx]` or `[ERROR:xxxxxx]` line.

Each line starts with `[INFO]`, `[WARN:xxxxxx]` or `[ERROR:xxxxxx]`. Warnings and errors have an error code. An example error, for a share the user cannot read:

```text
[ERROR:00000005]   LoadProfile failed. Version: 2.9.8440.42104 User: %username%. SID: %sid%. SessionId: 10. FrxStatus: 31 (Access is denied.)
```

A `LoadProfile failed` line means the profile did not load. The FSLogix profile article covers the causes and fixes: [Troubleshoot FSLogix: Profile Does Not Load or Is Temporary](/azure-virtual-desktop/troubleshoot-fslogix-profile-fails-to-load/).

FSLogix can also block sign-in on purpose. When `PreventLoginWithFailure` or `PreventLoginWithTempProfile` is enabled, FSLogix uses `frxshell.exe` in place of the normal shell, to stop a user from signing in when the profile fails to attach or Windows gives a temporary profile. Users of a RemoteApp are not blocked this way. If a user is blocked, the cause is still the profile, so use the profile article.

## Check 5: The RoamRecycleBin issue in FSLogix 2210

FSLogix 2210 (2.9.8361.52326) can cause a black screen at sign-in, or `sihost.exe` hanging. It happened with the `RoamRecycleBin` setting on, which is the default. It is fixed, so install the latest FSLogix version. The profile log notes the FSLogix version near the top.

## Check 6: The Windows shell on the session host

This part follows the Windows guide for a black screen after sign-in. Its first step is to press the Windows logo key + Ctrl + Shift + B, which resets the graphics driver. The guide is written for any Windows device and does not say whether this works inside a remote session.

**Check the shell setting.** Back up the registry first: in `regedit`, select the key, then **File** > **Export** and save the file. Then go to:

`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon`

The `Shell` value must be `explorer.exe`. Also check the key's permissions. They must match a device that works.

**Check what is running.** In the remote session, press Ctrl+Alt+End (not Ctrl+Alt+Del) and select **Task Manager**. On the **Details** tab, look for `explorer.exe` and `userinit.exe`.

- If they are running, capture dumps from an elevated command prompt with [ProcDump](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump):

  ```console
  procdump -ma explorer.exe explorer.dmp
  procdump -ma userinit.exe userinit.dmp
  ```

  Then analyze them, or give them to Microsoft Support.
- If they are not running, they stopped responding, exited, or `explorer.exe` is not the shell.

**Did they stop responding?** In **Event Viewer** > **Windows Logs** > **Application**, search for Event ID 1000. It indicates an application that stops responding. See whether it names `explorer.exe` or `userinit.exe` at the time of the problem. If so, turn on Windows Error Reporting dumps. Create a folder such as `C:\dumps`, then under `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Windows Error Reporting` (create the key if it is missing) add these values:

| Value name | Type | Data |
|---|---|---|
| `DumpCount` | `REG_DWORD` | `10` |
| `DumpType` | `REG_DWORD` | `2` |
| `DumpFolder` | `REG_EXPAND_SZ` | `C:\dumps` |

Sign in again to reproduce the problem. A dump is written to that folder when the process stops responding.

**Did they exit?** Use Process Monitor (ProcMon) to record the sign-in, then look for `explorer.exe` or `userinit.exe` exiting with a non-zero exit code. For a host that several users share, the guide has a procedure with a first user signed in and ProcMon running while a second user reproduces the problem. If you find a non-zero exit, the guide has you capture a dump with ProcDump:

```console
Procdump -e 1 -x C:\Temp explorer.exe
```

**A clean boot.** In the guide, a clean boot comes right after the shell check and before the dump steps above. It helps find a start-up app or service that causes the problem. Use it early if you can take the host out of service, and fall back to the dump steps if the clean boot finds nothing.

## Fix by cause

| Cause | How you know | Fix |
|---|---|---|
| Windows update KB5124008 | Many users, black screen after the update, `explorer.exe` crashes at shell start | No workaround is listed. Collect dumps and open a support case. Check the known issues page for changes. |
| FSLogix 2210 `RoamRecycleBin` | FSLogix version 2.9.8361.52326 | Install the latest FSLogix version. |
| Profile does not load | `LoadProfile failed` or an `[ERROR:xxxxxx]` line in the profile log | Use the FSLogix profile article. |
| `Shell` value is wrong | `Winlogon` `Shell` is not `explorer.exe` | Back up the registry, set it to `explorer.exe`, and match key permissions to a working device. |
| `explorer.exe` or `userinit.exe` stops responding | Event ID 1000 for either process | Collect dumps with Windows Error Reporting and give them to Microsoft Support. |
| `explorer.exe` or `userinit.exe` exits | Non-zero exit code in ProcMon | Capture a dump with ProcDump and analyze it or send it to Microsoft Support. |
| A start-up app or service | The problem goes away in a clean boot | Find the app or service and remove or fix it. |
| Screen capture protection with Teams | Only the shared view is black | Use a supported client setup for Teams sharing. |

## If it is still black

Collect these before you open a support case:

- The `CorrelationId` and the time of the failing attempt, and whether `ServiceError` is `true`.
- The FSLogix version and the profile log lines for the user's `LoadProfile`.
- The Application log entries around the time, including Event ID 1000.
- Process dumps of `explorer.exe` and `userinit.exe` if you could capture them.
- Whether KB5124008 is installed on the host.

The FSLogix Support Tool collects the FSLogix logs into one zipped archive. Collect logs before you open a support case.

## Common mistakes

- **Calling a failed connection a black screen.** Check for the `Connected` state first.
- **Editing the registry without a backup.** The Windows guide tells you to back it up first.
- **Using Ctrl+Alt+Del inside a remote session.** Use Ctrl+Alt+End.
- **Waiting for a fix to a known issue without collecting evidence.** Collect dumps while the problem is reproducible.
- **Treating FSLogix blocking as a bug.** It can be a deliberate setting.

Next: [Troubleshoot FSLogix: Profile Does Not Load or Is Temporary](/azure-virtual-desktop/troubleshoot-fslogix-profile-fails-to-load/).

## Sources

- [Black screen after you sign in](https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/scenario-guide-black-screen-after-sign-in)
- [FSLogix known issues](https://learn.microsoft.com/en-us/fslogix/troubleshooting-known-issues)
- [FSLogix logging and diagnostics](https://learn.microsoft.com/en-us/fslogix/troubleshooting-events-logs-diagnostics)
