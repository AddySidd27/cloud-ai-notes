---
title: "Troubleshoot an AVD Session Host That Is Unavailable or Needs Assistance"
seoTitle: "AVD Session Host Unavailable or Needs Assistance: Fixes"
layout: post.njk
permalink: "/azure-virtual-desktop/troubleshoot-session-host-unavailable-health-checks/"
order: 129
part: 29
tags: [avd-series]
deck: "Read the session host status, find the health check that failed, and fix the agent, stack, URL or domain problem behind it."
description: "Fix an Azure Virtual Desktop session host that is Unavailable, Needs Assistance, Upgrading or Upgrade Failed: health checks, agent events and fixes."
---

You open the host pool in the Azure portal and a session host does not say Available. It says Unavailable, Needs Assistance, Upgrading or Upgrade Failed. Users may get "no resources available", or the host stops getting new sessions. This article shows how to read the status, find the health check that failed, and fix the usual causes.

For how a connection reaches a session host, see [Follow a connection step by step](/azure-virtual-desktop/follow-a-connection-step-by-step/). For the network addresses and ports the host must reach, see [Required connectivity](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/).

## Key terms

| Term | Meaning |
|---|---|
| Session host | A virtual machine that runs users' desktops or apps. |
| Host pool | A group of session hosts that users share. |
| Azure Virtual Desktop Agent | Software on the session host. It talks to the Azure Virtual Desktop service, reports the host's status and receives connections. |
| Boot loader | A small service on the host (service name `RDAgentBootLoader`, shown as Remote Desktop Agent Loader) that starts the agent. |
| Broker | The Azure Virtual Desktop service part that decides which session host gets a connection. |
| Health check | A test the agent runs on the host. The result sets the host's status. |
| Fatal and non-fatal | A fatal problem stops users from using the host. A non-fatal one lets the service run, but you should still fix it. |
| Side-by-side (SxS) stack | The component on the host that accepts incoming Azure Virtual Desktop connections. Its "listener" waits for them. |
| IMDS | Azure Instance Metadata Service. A VM reads information about itself from the address 169.254.169.254. |
| Geneva Monitoring Agent | A monitoring component that the Azure Virtual Desktop agent installs. It sends connection logging data. |
| Registration key | A key you create on the host pool, with an expiry date. A session host uses it to register with the host pool. |
| Event Viewer | The Windows tool that shows event logs. The Application log holds the agent's events. |
| Log Analytics workspace | An Azure place where logs are stored and queried. |
| KQL | Kusto Query Language, the language used to query a Log Analytics workspace. |
| Diagnostic setting | A setting on an Azure resource that sends its logs to a workspace. |

## Before you start

To read statuses you need access to the host pool in the Azure portal. To fix most causes you need administrator rights on the session host. For the queries, you need read access to the Log Analytics workspace, and a diagnostic setting on the host pool that includes the Agent Health Status category. [Turn on the logs and learn to read them](/azure-virtual-desktop/troubleshoot-avd-start-here/) shows how. Data can take a few hours to appear after you first switch diagnostics on.

## What the status means

Open the host pool, select Session hosts, and read the Status column. The table below explains each status.

| Status | What it means | New sessions go to it? |
|---|---|---|
| Available | The host passed all health checks and can take connections. A host at its maximum session limit still shows Available if it passed. | Yes |
| Needs Assistance | The host failed a non-fatal check: Geneva Monitoring Agent, IMDS, or URL. Users can connect, but their experience may be worse. | Yes |
| Shutdown | The host was shut down. | No |
| Unavailable | The VM is off, or the host failed a fatal health check. | No |
| Upgrade Failed | The agent could not update or upgrade. This does not affect new or existing sessions. | Yes |
| Upgrading | An agent upgrade is in progress. The status changes to Available when it is done. | Yes |

A VM that shut down before its agent could report may show Unavailable instead of Shutdown. That does not mean there is a fault. To know the real power state, read the status together with the VM's instance view.

The picture shows the order of checks as a decision tree.

![Six checks: is the VM running, status Needs Assistance, a failed domain, trust or stack check, agent errors in the Application log, stuck in Upgrading. Each yes names a fix; the last step is reinstalling, re-registering and opening a case.](/img/avd/troubleshoot-session-host-unavailable-health-checks.svg)

*Source: [Session host statuses and health checks](https://learn.microsoft.com/en-us/azure/virtual-desktop/troubleshoot-statuses-checks) and [Troubleshoot common agent issues](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-agent).*

## Work through the checks in order

### 1. Is the VM running?

In the Azure portal, open the VM and read its power state. If it is stopped, start it. Wait a few minutes, then read the status in the host pool again. If the VM was off, Unavailable was expected.

### 2. Find the health check that failed

1. In the Azure portal, search for Azure Virtual Desktop and open Host pools.
2. Select the host pool, then Session hosts.
3. Select the name of the session host. The page shows which health checks failed.

Match the failed check to this table.

| Health check | If it fails | What to do |
|---|---|---|
| Domain joined | Fatal. Users cannot connect. | Join the session host to a domain. |
| Domain trust check | Fatal. The service cannot connect if the host cannot reach the authentication domain. | Fix the trust or the path to the domain. |
| Side-by-side (SxS) Stack Listener | Fatal. Users cannot connect. | Restart the VM. If that does not work, see check 5 and then contact support. |
| Geneva Monitoring Agent | Semi-fatal. Connections can work but have no logging information. | Make sure a monitoring agent is installed. If it is, contact support. See check 6. |
| App Attach health check | Not fatal, but some apps stop working for users. | Check that the app attach service works during package staging and destaging. |
| Metadata service check | Not fatal. | See check 6, the IMDS part. |

The check names differ between sources. The agent troubleshooting guidance calls the three Needs Assistance checks `UrlsAccessibleCheck`, `MetaDataServiceCheck` and `MonitoringAgentCheck`. The sample Log Analytics query below uses a list of 11 other names, such as `DomainJoin`, `SxSStack`, `URLCheck` and `GenevaAgent`. These are not one list. Use the name the portal shows for your host.

### 3. Read the agent events on the host

Sign in to the session host as an administrator, the way you normally manage a VM (for example over Azure Bastion or RDP). Search the Start menu for Event Viewer and open it, then open Windows Logs, then Application. Look for events whose source is `WVD-Agent`, `WVD-Agent-Updater`, `RDAgentBootLoader` or `MsiInstaller`, at the time the host went wrong.

Also open Services (search the Start menu for `services.msc`) and check that Remote Desktop Agent Loader is running. If it is stopped, start it. If you cannot select Start, you do not have administrator rights. If it stops again after you start it, the host may have a registration failure. A registration failure means the host's registration key is not valid. See [Troubleshoot AVD Session Hosts That Do Not Register to the Host Pool](/azure-virtual-desktop/troubleshoot-host-pool-registration-failures/).

### 4. Match the event to a cause

| Event or message | Cause | Fix |
|---|---|---|
| ID 3703, "RD Gateway Url: is not accessible" | The agent cannot reach the gateway URLs. | Allow the required URLs. Make sure no firewall or proxy blocks them. Run the Required URL Check tool (`WVDAgentUrlTool.exe`, see check 7). |
| ID 3019 | The agent cannot reach the web socket transport URLs. | Allow the required URLs. Work with your network team on firewall, proxy and DNS. A network trace can show where the service is blocked. Attach it to a support case. |
| ID 3277, `INVALID_FORM` | The agent cannot reach the broker or a specific endpoint. A firewall or DNS setting is a likely cause. | Open the `BrokerResourceIdURI` and `BrokerResourceIdURIGlobal` addresses (under `HKLM\SOFTWARE\Microsoft\RDInfraAgent`) with `/api/health` added. Both should show "RD Broker is Healthy". If not, unblock the endpoints. Also check for group policy ciphers that block the agent's connection to the broker. |
| ID 3277, `INVALID_REGISTRATION_TOKEN` or `EXPIRED_MACHINE_TOKEN` | The registration key is not valid. | Create a new key and re-register the host. See the registration article. |
| ID 3277, `InstallationHealthCheckFailedException` | The stack listener is not working because the terminal server toggled its registry key. | Check the listener (check 5). If it is not working, uninstall and reinstall the stack component by hand. |
| ID 3277, `InstallMsiException` | The installer is busy with another application, or group policy blocks `msiexec.exe`. | On the host, run `rsop.msc` and open Computer Configuration, Administrative Templates, Windows Components, Windows Installer, Turn off Windows Installer. If Enabled, ask your Active Directory team to allow `msiexec.exe`. |
| ID 3277, `Win32Exception` | A policy blocks `cmd.exe`, which the agent needs to restart its service during updates. | On the host, run `rsop.msc` and open User Configuration, Administrative Templates, System, Prevent access to the command prompt. If Enabled, ask your Active Directory team to allow `cmd.exe`. |
| ID 3277, `DownloadMsiException` | Not enough disk space for the agent. | Delete files you no longer need, or increase the disk. |
| ID 3277, `ENDPOINT_NOT_FOUND` | The broker found no endpoint. There are no hosts in the pool, the hosts are not active, all are at the session limit, or none has the agent service running. | Check the VM is on and still in the host pool, is below its session limit, runs the agent and has a working stack listener, can reach the broker, and has a valid registration key. |
| ID 3389, `MissingMethodException: Method not found` | The agent update failed and rolled back. The .NET Framework on the VM is older than 4.7.2. | Upgrade .NET Framework to 4.7.2 or later. |
| Event 7000 or 7011 (service start timeouts) | The boot loader does not start fast enough at boot. | See check 7. |
| "Connection not found: RDAgent does not have an active connection to the broker" | The host is at its connection limit. | Lower the maximum session limit, or give the VMs more resources. |
| `DisableRegistryTools` set to 1 | A registry setting stops the agent from installing the side-by-side stack, which causes an `InstallMsiException`. | Remove the key from the three places where it can be set (`HKU\DEFAULT`, `HKU\S-1-5-18` and `HKCU`, under `SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System`), remove the broken stack install, restart, and let the agent reinstall the stack. |

### 5. Check the stack listener

The side-by-side stack must be listening for the host to take connections. On the host, run this from a command prompt:

```console
qwinsta.exe
```

`qwinsta.exe` lists the sessions and listeners on the host. Note the version number next to `rdp-sxs`. In the STATE column, both `rdp-tcp` and `rdp-sxs` should say `Listen`. If they do not, or are missing, there is a stack problem.

If the listener is not working on Windows 10 version 2004, check these in the registry:

1. Under `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations`, open the folder that matches the version from `qwinsta.exe`. `fReverseConnectMode` must be `1`, and `fEnableWinStation` must be `1`. Do this for each matching folder, then restart the VM.
2. Under `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\ClusterSettings`, `SessionDirectoryListener` must be `rdp-sxs` followed by that version number. If not, use the full re-registration in "Reinstall and re-register" below.

Only Windows Enterprise and Windows Server editions support the stack. On Windows Pro, the stack installs but is not activated, so it does not show in `qwinsta.exe`. Use a supported operating system to create the host.

If the host stays Unavailable or Upgrading, reinstall the stack:

1. Sign in as an administrator. Run `Stop-Service RDAgentBootLoader` in an elevated PowerShell window.
2. In Programs and Features (or Settings, then Apps on Windows 11), uninstall the latest Remote Desktop Services SxS Network Stack.
3. Find the newest installer on the host and install it:

```powershell
$sxsMsi = (Get-ChildItem "$env:SystemDrive\Program Files\Microsoft RDInfra\" | ? Name -like SxSStack*.msi | Sort-Object CreationTime -Descending | Select-Object -First 1).FullName
$sxsMsi
msiexec /i $sxsMsi
```

4. Restart the VM. Run `qwinsta.exe` again. If `rdp-tcp` and `rdp-sxs` are not `Listen`, re-register the host (see below).

### 6. Needs Assistance: URL, IMDS and Geneva

These three checks keep a host at Needs Assistance. Users can still connect.

- **`UrlsAccessibleCheck`.** A required URL is blocked. Either an active firewall blocks most outbound traffic, or the local hosts file blocks the URLs. For a firewall, add a rule that allows outbound TCP port 80 and 443 to the blocked URLs. For the hosts file, make sure none of the required URLs are in it. Its location is in the registry at `HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters`, value `DataBasePath`.
- **`MetaDataServiceCheck`.** The host cannot reach IMDS. Unblock 169.254.169.254 in networking, firewall or proxy settings. Make sure HTTP clients in the VM bypass web proxies when they query IMDS. If a web proxy is the cause, add an exception for 169.254.169.254. In an elevated window run `netsh winhttp set proxy proxy-server="http=<customerwebproxyhere>" bypass-list="169.254.169.254"`.
- **`MonitoringAgentCheck`.** Check that Remote Desktop Services Infrastructure Geneva Agent is installed. If several versions are installed, remove the old ones. If it is not installed, read `C:\Program Files\Microsoft RDInfra\GenevaInstall.txt` for the install error. Check that the scheduled task `GenevaTask_<version>` exists, is enabled and is running. If not, reinstall from the `Microsoft.RDInfra.Geneva.Installer-x64-<version>.msi` file in `C:\Program Files\Microsoft RDInfra`.

### 7. The agent starts too late at boot

If the boot loader is stopped after a restart, or Windows logs service start timeouts (events 7000 or 7011), or users cannot connect with start on connect, the boot loader may not start quickly enough. Try these in order:

1. In Services, set Remote Desktop Agent Loader to Automatic (Delayed Start).
2. Raise the service timeout. In an administrator command prompt run `reg add "HKLM\SYSTEM\CurrentControlSet\Control" /v ServicesPipeTimeout /t REG_DWORD /d 60000 /f`. Start at 60,000 ms and tune as needed. Restart the host.
3. Check boot performance. Make sure the VM meets the recommended IOPS and that startup tasks, such as antivirus scans, heavy logon scripts or large group policies, do not starve the agent.
4. If the host still shows Needs Assistance or Unavailable, run `WVDAgentUrlTool.exe` and fix any endpoint that fails.

After a restart, the host should become Available within a few minutes.

### 8. Reinstall and re-register

Use this when the host is stuck in Upgrading or Unavailable, the stack listener does not work, the Remote Desktop Agent Loader service or the `RdAgentBootLoader` process is missing, or nothing above helped.

1. Sign in to the host as an administrator. In Programs and Features, uninstall all of these, remove every instance, then restart the VM: Remote Desktop Agent Boot Loader, Remote Desktop Services Infrastructure Agent, Remote Desktop Services Infrastructure Geneva Agent, Remote Desktop Services SxS Network Stack. If you are connected over RDP when you uninstall the SxS stack, choose "Do not close applications" when asked, or your connection drops.
2. In the host pool, select Session hosts, tick the host and select Remove. If this is a personal host pool, write down which user the host is assigned to first, so you can assign it again after it registers.
3. On the host pool Overview, select Registration key, then Generate new key. Choose an expiration date and generate the key only for as long as you need it. Copy it.
4. Download the Azure Virtual Desktop Agent installer and the Boot Loader installer from the links in [Register session hosts to a host pool](https://learn.microsoft.com/en-us/azure/virtual-desktop/add-session-hosts-host-pool#register-session-hosts-to-a-host-pool). Run the agent installer and paste the key when asked. Then run the Boot Loader installer. The agent installer also installs the side-by-side stack and the Geneva monitoring agent. You might need to unblock the downloaded files in their Properties first.
5. Restart the VM. After a few minutes the host should show Available in the host pool.

## Queries

These need the host pool's diagnostic setting for Agent Health Status to be on.

### Health checks over time

This is the "HealthChecks of SessionHost" sample from the Azure Monitor query reference. It shows, per host and per check, how many times each result happened and when it was first and last seen. In some states, such as Unavailable or Upgrading, hosts do not run health checks, so those hosts may be missing from the result.

How to read it. The two `let` blocks at the top are lookup lists. The agent stores each check and each result as a number, and these lists turn the numbers into names such as `SxSStack` and `Succeeded`. The `WVDAgentHealthStatus` part then splits the stored check results into one row per check (`mv-expand` and `bag_unpack`), adds the check name, and counts each result for each host with the first and last time it was seen.

A healthy host shows `Succeeded` for every check, with a `LastSeen` that is recent. A bad host has a row where `HealthCheckResult` is `Failed`, and the `HealthCheckDesc` on that row names the check to look up in the table in check 2. If one host shows both `Succeeded` and `Failed` for the same check, compare `FirstSeen` and `LastSeen` to see which came last.

```kusto
let HealthCheckIdToDescription = (idx:long) {
    case(
        idx == 0,  "DomainJoin",
        idx == 1,  "DomainTrust",
        idx == 2,  "FSLogix",
        idx == 3,  "SxSStack",
        idx == 4,  "URLCheck",
        idx == 5,  "GenevaAgent",
        idx == 6,  "DomainReachable",
        idx == 7,  "WebRTCRedirector",
        idx == 8,  "SxSStackEncryption",
        idx == 9,  "IMDSReachable",
        idx == 10, "MSIXPackageStaging",
        strcat("InvalidNameIndex: ", idx)
     )
};
let GetHealthCheckResult = (idx:long) {
    case(
        idx == 0, "Unknown",
        idx == 1, "Succeeded",
        idx == 2, "Failed",
        idx == 3, "SessionHostShutdown",
        strcat("InvalidResultIndex: ", idx)
    )
};
WVDAgentHealthStatus
// In some states (e.g. Unavailable, Upgrading) hosts are not running health checks
| where isnotempty(SessionHostHealthCheckResult)
| mv-expand SessionHostHealthCheckResult to typeof(dynamic)
| evaluate bag_unpack(SessionHostHealthCheckResult)
| evaluate bag_unpack(AdditionalFailureDetails)
| extend HealthCheckDesc = HealthCheckIdToDescription(HealthCheckName)
| summarize count(), FirstSeen=min(TimeGenerated), LastSeen=max(TimeGenerated) by HealthCheckDesc, SessionHostName, HealthCheckResult=GetHealthCheckResult(HealthCheckResult)
```

### Latest status for each host

This query is not a published sample. It uses only columns that the `WVDAgentHealthStatus` table lists. Try it in a test workspace first. It takes each host's newest row in the last day.

```kusto
WVDAgentHealthStatus
| where TimeGenerated > ago(1d)
| summarize arg_max(TimeGenerated, Status, LastHeartBeat, AgentVersion, SxSStackVersion, UpgradeState, UpgradeErrorMsg, AllowNewSessions) by SessionHostName
| order by Status asc
```

Line by line: line 2 keeps the last day of agent reports. Line 3 (`arg_max`) keeps, for each host, only the row with the newest `TimeGenerated` and shows the listed columns from that row. Line 4 sorts by `Status`. You get one row per host. A healthy host has a recent `LastHeartBeat` (the last time the agent reported in), an `UpgradeState` that is not a failure, and an empty `UpgradeErrorMsg`. A bad host has an old `LastHeartBeat`, which means the agent stopped reporting (go to check 3 and check 8), or an `UpgradeErrorMsg` that names an upgrade problem. A host that is missing from the result sent no report in the last day.

The table reference only describes `Status` as "the current status of the VM, whether its healthy or not", and does not list its possible values. Read the values in your own results before you filter on a word.

### Is the same error hitting other users?

This is a sample from the diagnostics reference. Take `CodeSymbolic` from a failing row in `WVDErrors` and put it in place of `ErrorSymbolicCode`.

```kusto
WVDErrors
| where CodeSymbolic =="ErrorSymbolicCode"
| summarize count(UserName) by CodeSymbolic
```

In `WVDErrors`, `ServiceError` is `false` for problems an administrator can fix. When it is `true`, escalate to Microsoft and include the CorrelationId.

## If the host is still not Available

If the host is still Unavailable after the steps above, open a support case. Put these in the case: what you changed, the Application log entries from the agent sources, the output of `qwinsta.exe`, the health check that failed, and any CorrelationId from `WVDErrors` rows with `ServiceError` set to `true`.

Next: [Troubleshoot AVD Disconnects and Slow Sessions](/azure-virtual-desktop/troubleshoot-disconnects-and-slow-sessions/).

## Sources

- [Session host statuses and health checks](https://learn.microsoft.com/en-us/azure/virtual-desktop/troubleshoot-statuses-checks)
- [Troubleshoot common Azure Virtual Desktop Agent issues](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-agent)
- [Send diagnostic data to Log Analytics](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics)
