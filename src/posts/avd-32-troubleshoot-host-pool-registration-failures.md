---
title: "Troubleshoot AVD Session Hosts That Do Not Register to the Host Pool"
seoTitle: "Fix AVD Session Hosts That Will Not Register to a Host Pool"
layout: post.njk
permalink: "/azure-virtual-desktop/troubleshoot-host-pool-registration-failures/"
order: 132
part: 32
tags: [avd-series]
deck: "Work through deployment, domain join, agent install, registration key, name, network and stack checks in order, with the queries and fixes for each."
description: "Find why an Azure Virtual Desktop session host is missing from the host pool or never turns Available: deployment, domain join, token, name, network, stack."
---

You built a new session host, or rebuilt an old one, and it does not show up as a working host. Maybe it is missing from the **Session hosts** list in the host pool. Maybe it is listed as **Unavailable** and never changes to **Available**. Maybe the deployment failed halfway, at a step called `joindomain` or `dscextension`. Or the agent installer complained about a token, or said the name is already registered.

A session host is a virtual machine (VM) that runs users' desktops or apps. A host pool is the group of session hosts that users are connected to. A session host is only useful once it is *registered*: it has told the Azure Virtual Desktop service "I belong to this host pool". This article walks through the reasons that registration fails, in the order that is cheapest to check.

Set up the logs first. The queries below return nothing until diagnostics are switched on for the host pool. [Turn on the logs and learn to read them](/azure-virtual-desktop/troubleshoot-avd-start-here/) shows how. For the bigger picture of how Azure Virtual Desktop fails, see [How Azure Virtual Desktop fails](/azure-virtual-desktop/how-azure-virtual-desktop-fails/).

## Key terms

| Term | Meaning |
|---|---|
| Registration key (token) | A secret that the host pool creates. It authorizes a VM to join that host pool, and it is valid only until the expiry time you choose. |
| Agent | The Remote Desktop Services Infrastructure Agent. A program on the session host that registers it with the service and reports its health. |
| Boot loader | The Remote Desktop Agent Boot Loader. It starts the agent. Its Windows service is called `RDAgentBootLoader`. |
| Broker | The part of the Azure Virtual Desktop service that the agent talks to. It keeps track of which hosts are in which pool. |
| Side-by-side (SxS) stack | A component on the session host that listens for connections. `qwinsta` lists it as `rdp-sxs`. |
| DSC | PowerShell Desired State Configuration. A deployment template uses it to install the agent on the new VM. |
| Domain join | Making the VM a member of an Active Directory domain. |
| Drain mode | A host setting that stops new sessions from starting on it. |
| Event Viewer | The Windows tool that shows event logs on the VM. |
| Diagnostic setting | An Azure setting that sends a resource's logs to a Log Analytics workspace (a store you query). |
| KQL | Kusto Query Language, the language you use to query a Log Analytics workspace. |
| CorrelationId | An ID for one activity in the logs. Support asks for it. |

## What you need before you start

To generate a registration key you need the **Desktop Virtualization Host Pool Contributor** role on the resource group. To create and add session hosts in the portal you also need **Virtual Machine Contributor**. On the session host you need local administrator rights.

If you add hosts through the portal, do not turn off Windows Remote Management (WinRM). DSC needs it.

## Quick map

Work from the top. Stop at the first check that fails.

1. Did the VM deployment succeed? Look at the deployment operations in Azure.
2. Did the host join the domain? Check the join errors and DNS.
3. Are the agent and boot loader installed on the VM?
4. Is the registration key valid? Look for event 3277 in Event Viewer.
5. Is the VM name unique in the host pool?
6. Can the VM reach the broker on port 443 and open the required URLs?
7. Is the side-by-side stack listening?
8. If all that passes and the host is still not **Available**, uninstall, remove the host, and register it again.

![The first question is whether the VM deployment succeeded; if it did not, read the deployment error. The tree then asks, in order, whether the host joined the domain, whether the agent and boot loader are installed, whether the registration token is valid, whether the VM name is unique, whether the host can reach the broker on port 443 and whether the stack is listening, and ends with uninstalling and registering the host again.](/img/avd/troubleshoot-host-pool-registration-failures.svg)

*Check order for a session host that does not register. Source: [Troubleshoot host pool creation](https://learn.microsoft.com/en-us/azure/virtual-desktop/troubleshoot-set-up-issues), [Troubleshoot session host VM configuration](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-vm-configuration) and [Troubleshoot common Agent issues](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-agent).*

## Where to look

| Place | What it shows |
|---|---|
| Azure portal, deployment operations for the resource group, then the Activity log | Why the VM or one of its extensions failed to deploy. |
| Host pool, **Session hosts** tab | Status of each host. Select a host name to see which health checks failed. |
| On the VM: Event Viewer, **Windows Logs**, **Application** | Agent events. Look at sources `WVD-Agent`, `WVD-Agent-Updater`, `RDAgentBootLoader` and `MsiInstaller`. Registration errors appear as event ID 3277. |
| On the VM: `C:\Windows\Temp\ScriptLog.log` | The log of the DSC step that installs the agent. If the file is missing, that step did not run. |
| Log Analytics tables `WVDHostRegistrations`, `WVDAgentHealthStatus`, `WVDErrors` | Registration activity, agent health, and errors. |

### Queries

The first query is a sample from the documentation. It lists each health check per host, for hosts that run health checks. Hosts in some states, such as Unavailable or Upgrading, do not run them, so a host that never registered may not appear here.

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

*Source: sample queries for the `WVDAgentHealthStatus` table.*

How to read it: the two `let` blocks are lookup lists that turn the numbers the agent stores into check names (such as `DomainJoin` and `URLCheck`) and results (such as `Succeeded` and `Failed`). The query then gives one row per host, check and result, with a count and the first and last time it was seen. Healthy: every check says `Succeeded`. Bad: a row with `Failed`. Its `HealthCheckDesc` tells you which check, such as `DomainJoin` (go to check 2) or `URLCheck` (go to check 6). A host that is missing from the result may not have registered at all, so use the next query.

The next three queries are written for this article. They are not documentation samples, because the documentation has no sample queries for `WVDHostRegistrations`. They use only column names listed on the table pages.

Which hosts registered, and when:

```kusto
WVDHostRegistrations
| where TimeGenerated > ago(7d)
| summarize LastRegistered=max(TimeGenerated), Registrations=count() by SessionHostName, SessionHostIPAddress
| order by LastRegistered desc
```

Line 2 keeps the last seven days. Line 3 groups the rows by host name and IP address and shows the newest registration time and how many registrations there were. Line 4 puts the most recent first. Healthy: your new host is in the list with a `LastRegistered` time after you installed the agent. Bad: the host is not in the list, which means the service never saw it register. Go to check 3 and check 4.

The latest agent report for each host:

```kusto
WVDAgentHealthStatus
| where TimeGenerated > ago(1d)
| summarize arg_max(TimeGenerated, Status, LastHeartBeat, AgentVersion) by SessionHostName
```

For each host, this keeps only the newest agent report from the last day and shows its `Status`, `LastHeartBeat` (the last time the agent reported in) and `AgentVersion`. Healthy: the host is listed and `LastHeartBeat` is recent. Bad: the host is missing (the agent has sent no report in the last day) or `LastHeartBeat` is old (the agent stopped). In both cases check that the `RDAgentBootLoader` service is running (check 6).

Errors that you can fix yourself. The documentation says `ServiceError` is `false` for problems an administrator can resolve, and that `WVDErrors` includes host registration issues. The query does not filter on `ActivityType` because the documentation does not list the value for registration.

```kusto
WVDErrors
| where TimeGenerated > ago(7d)
| where ServiceError == "false"
| project TimeGenerated, ActivityType, Source, CodeSymbolic, Code, Message, CorrelationId
| order by TimeGenerated desc
```

Line 3 keeps errors that an administrator can fix. Line 4 keeps the columns that matter. Line 5 puts the newest first. Healthy: no rows. Bad: rows around the time you installed or re-registered the host. Read `Message` and `CodeSymbolic`, and look for that text in the tables below.

## Ordered checks

### 1. Did the VM deployment succeed?

In the Azure portal, open the resource group that holds the VMs, then select **Deployments** in its left menu and open the failed deployment to see which operation failed and its error message. If the deployment shows no error, select **Activity log** in the same menu. The Activity log is Azure's record of actions on the resource group's resources. Then match the message to this table.

| What you see | Cause | Fix |
|---|---|---|
| `VMExtensionProvisioningError` on `joindomain` | Wrong domain join credentials, the domain name does not resolve, or the virtual network DNS setting is **Default**. | Check the credentials. Set the virtual network DNS servers to **Custom** and make sure they match your domain controller. See check 2. |
| `Unauthorized`: "The scale operation is not allowed for this subscription in this region" | The subscription type cannot use a required feature in that region. The documentation names MSDN, Free and Education subscriptions as examples. | Change the subscription type or the region. |
| `InvalidParameter`: "The Admin Username specified is not allowed" | The name or password contains a forbidden word: admin, administrator or root. | Use a different username. |
| `VMExtensionProvisioningError` on `dscextension`, "The SendConfigurationApply function did not succeed" | DSC could not get administrator access on the VM. | Confirm that the username and password have administrator rights on the VM, then run the template again. |
| `InvalidResourceReference` (a subnet or network card not found) | The template picked up an existing resource with a similar name, from part of the resource group name. Or a network card has the same name as another in the virtual network. | Make the first two characters of the resource group name unique in the subscription, or use a different host name prefix. |
| DSC "Error downloading ... catalogartifact.azureedge.net" | A static route, firewall rule or network security group (NSG) blocks the download of the template's zip file. | Remove the block. You can also download the zip file from the link in the template to an allowed location. |
| "Exceeding quota limit" | The deployment is over the subscription's quota for that VM size. | Deploy fewer VMs or cores, or open the link in the `statusMessage` field to request more quota. |
| The Azure region you want is not listed | The resource provider has not refreshed. | In **Subscriptions**, **Resource providers**, select `Microsoft.DesktopVirtualization` and **Re-register**. This does not affect existing environments. |
| `VMExtensionProvisioningError`, with no clear cause | The documentation lists a temporary problem with the service or the connection as the cause. | Confirm the service is healthy by signing in with PowerShell, then finish the registration by hand with the [manual registration steps](https://learn.microsoft.com/en-us/azure/virtual-desktop/add-session-hosts-host-pool#register-session-hosts-to-a-host-pool) (also described under check 3). |

If the host pool uses a *session host configuration* (a saved template that the service uses to create hosts for you), the domain join is done by the agent, not by a deployment extension. The Azure deployment can then succeed even when the domain join failed, which leaves unhealthy hosts. In that case the domain join errors are in the portal: open the session host and view the JSON for its session host health.

### 2. Did the host join the domain?

This applies to hosts that join an Active Directory domain. Try pinging the domain name from a command line on the VM. Then match the error.

| Error | Cause | Fix |
|---|---|---|
| Incorrect credentials | A typo in the credentials entered in the template. | Join the VM by hand, or redeploy with confirmed credentials. |
| "Timeout waiting for user input" | The join account may use multifactor authentication (MFA). | Remove MFA from that account for now, or use a service account. |
| The account does not have permission to complete the operation | The account may not be allowed to join computers to the domain. | Use an account in the Administrator group, or give the account the needed permissions. |
| Domain name does not resolve | The VM's virtual network is not connected to the one that holds the domain. Or, with Microsoft Entra Domain Services, the virtual network DNS does not point to the managed domain controllers. Or the network card DNS settings do not point to the right servers. | Peer the virtual networks. Update the virtual network DNS settings. Set the network card DNS to **Custom** with the DNS servers' private IP addresses, or to **Inherit from virtual network**. |
| Computer account reuse is blocked | You reuse a computer name, the Windows updates released on or after October 11, 2022 are installed, and the account lacks rights to reuse computer accounts. | Use the account that created the computer object, a Domain Administrators member, or an account covered by the policy **Domain controller: Allow computer account re-use during domain join**. That policy needs updates released on or after March 14, 2023 on all member computers and domain controllers. |

For Microsoft Entra joined hosts, the documentation says the supported way is the `AADLoginForWindows` VM extension, which the portal and the Azure Virtual Desktop templates add for you. All hosts in one pool should use the same identity provider. This article does not cover Entra join errors beyond that.

### 3. Are the agent and boot loader installed?

On the VM, open **Control Panel**, **Programs and Features**. After a normal install you see four entries:

- Remote Desktop Agent Boot Loader
- Remote Desktop Services Infrastructure Agent
- Remote Desktop Services Infrastructure Geneva Agent
- Remote Desktop Services SxS Network Stack

An older documentation page names the first two "Azure Virtual Desktop Agent" and "Azure Virtual Desktop Agent Boot Loader". Look for either.

Then open `C:\Windows\Temp\ScriptLog.log`. If it is missing, the DSC step that installs the agent could not run with the credentials it was given. If it exists, read it for errors.

| What you see | Cause | Fix |
|---|---|---|
| Agent and boot loader missing, and `ScriptLog.log` missing | Wrong credentials or too few permissions in the template. | Add the components by hand with the [manual registration steps](https://learn.microsoft.com/en-us/azure/virtual-desktop/add-session-hosts-host-pool#register-session-hosts-to-a-host-pool). |
| Agent and boot loader missing, `ScriptLog.log` missing, and DSC started but could not finish | DSC could not sign in to Azure Virtual Desktop to get what it needs. | Make sure the account has no MFA, the host pool name is right and the host pool exists, and the account has at least Contributor on the subscription or resource group. |
| "Authentication failed" in `ScriptLog.log` | DSC ran but could not connect to Azure Virtual Desktop. | Register the VM by hand. Check that the account has permission and no MFA. |
| The image already contains the agent | A golden image must not include the agent. | Install the agent only after you deploy the image. See [Build and maintain a golden image](/azure-virtual-desktop/build-and-maintain-a-golden-image/). |
| Session host runs Windows Server | The Remote Desktop Session Host role is needed before registering. | Install the role and restart the VM, then install the agent. |

If you install by hand, download the agent and the boot loader from the links on the [manual registration page](https://learn.microsoft.com/en-us/azure/virtual-desktop/add-session-hosts-host-pool#register-session-hosts-to-a-host-pool), unblock the files (right-click, **Properties**, **Unblock**), run the agent installer and paste the registration key when it asks, then run the boot loader installer. After a short time the VM is listed in the host pool, possibly as **Unavailable** at first. When it shows **Available**, restart the VM.

### 4. Is the registration key valid?

On the VM, open Event Viewer, **Windows Logs**, **Application**. Event ID 3277 with `INVALID_REGISTRATION_TOKEN` or `EXPIRED_MACHINE_TOKEN` in the description means the key is not accepted. A registry value `IsRegistered` of 0 under `HKLM:\SOFTWARE\Microsoft\RDInfraAgent` points the same way, and an expired key is the documented cause.

To fix it:

1. In the Azure portal, open the host pool, select **Registration key**, then **Generate new key**. Set an expiry time and select **OK**. Copy the key.
2. On the VM, open PowerShell as an administrator and put the new key in the registry. Replace `<RegistrationToken>` with the key.

```powershell
$newKey = '<RegistrationToken>'

Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\RDInfraAgent" -Name "IsRegistered" -Value 0 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\RDInfraAgent" -Name "RegistrationToken" -Value $newKey -Force
```

3. Restart the boot loader service:

```powershell
Restart-Service RDAgentBootLoader
```

4. Check the result. `IsRegistered` should be 1 and `RegistrationToken` should be blank:

```powershell
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\RDInfraAgent" -Name IsRegistered | FL IsRegistered
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\RDInfraAgent" -Name RegistrationToken | FL RegistrationToken
```

5. Check the host pool. If the host is not listed, read the Event Viewer entries for errors that stop the agent from starting.

How long should the key last? The documentation gives different answers, so here are both. One page says the expiry can be no less than an hour and no longer than 27 days, and says to generate a key only for as long as you need it. It suggests 1 to 4 hours for an interactive rollout, and a longer lifetime, up to 27 days, if you add hosts over several days. An older page says to confirm that the `-ExpirationTime` parameter of `New-AzWvdRegistrationInfo` is set to three days. Pick a lifetime that covers your deployment window, and generate a new key if a host fails with an expired-key error.

A related limit: VMs that are pre-provisioned and stay powered off for more than 90 days also have their machine token expire. The documentation says to power them on for at least 20 minutes every 90 days so the token refreshes.

### 5. Is the VM name unique in the host pool?

`NAME_ALREADY_REGISTERED` means a host with that name is already registered, most likely a duplicate. Remove the old entry for that host from the host pool, then use a VM with a unique name, and wait 5 to 10 minutes for the status to change to **Available**.

When you add hosts through the portal, the name prefix can be at most 11 characters, the prefix and suffix together at most 15 characters, and session host names must be unique.

When you delete a host for good, do it in this order: put the host in drain mode, sign out all users, delete the session host from the host pool, then delete the VM. If you delete the VM first, you cannot delete the host from the pool.

### 6. Can the host reach the broker?

Event ID 3277 with `INVALID_FORM` in the description means the agent cannot connect to the broker or reach one endpoint. Firewall or DNS settings are the usual causes.

1. On the VM, open Registry Editor and go to `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\RDInfraAgent`. Note the values of `BrokerResourceIdURI` and `BrokerResourceIdURIGlobal`.
2. In a browser, open each value with `/api/health` added to the end, for example `https://rdbroker-g-us-r0.wvd.microsoft.com/api/health`.
3. If your network does not block the connection, each page loads and shows **RD Broker is Healthy**.
4. If a page does not load, unblock the endpoints in the required URL list and test again. If it still fails, check for group policies that set TLS ciphers and block the agent's connection to the broker.

Other ways to check the network:

- Event ID 3703 with `RD Gateway Url: is not accessible`: the agent cannot reach the gateway URLs. Event ID 3019: the agent cannot reach the web socket transport URLs. Both mean a required URL is blocked. Ask your network team to check the firewall, proxy and DNS.
- The Agent URL Tool, `WVDAgentUrlTool.exe`, is in the agent's install folder on the host. It lists the required addresses the host cannot reach. It does not check wildcard entries, so allow those first.
- To test port 443, install [PSPing](https://learn.microsoft.com/en-us/sysinternals/downloads/psping) (a free Sysinternals network test tool) on the VM and run `psping rdbroker.wvdselfhost.microsoft.com:443` from an administrator command prompt. A reply from the broker means the port is open. The `/api/health` test above uses the addresses from the registry; this test uses one fixed address. Both are in the documentation.
- If the agent does not report a heartbeat, check that the `RDAgentBootLoader` service is running. Start it if it is stopped.

[Required connectivity for Azure Virtual Desktop](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/) explains which addresses and ports the hosts need.

### 7. Is the side-by-side stack listening?

On the VM, run `qwinsta` from a command prompt. If the stack is installed and enabled, `rdp-sxs` is listed. The `STATE` column for `rdp-tcp` and `rdp-sxs` should be `Listen`. If those entries are missing or not listening, there is a stack problem.

| What you see | Cause | Fix |
|---|---|---|
| `O_REVERSE_CONNECT_STACK_FAILURE` | The stack is not installed. | Connect to the VM as local administrator and install the stack by registering the host as in check 3. |
| `rdp-sxs` is missing even though the stack is installed | The VM runs Windows Pro or another system that is not supported. The stack installs but is not activated. | Create the hosts from a supported operating system: Windows Enterprise or a Windows Server edition. |
| Event 3277 with `InstallationHealthCheckFailedException` | The stack listener is not working because the terminal server toggled the listener's registry key. | Check the listener. If it is not working, uninstall and reinstall the stack. |
| Event 3277 with `InstallMsiException` | Another installer is running, or a group policy blocks `msiexec.exe`. | Run `rsop.msc`, go to **Computer Configuration**, **Administrative Templates**, **Windows Components**, **Windows Installer**, **Turn off Windows Installer**. If it is **Enabled**, ask your Active Directory team to allow `msiexec.exe`. |
| `InstallMsiException` and the `DisableRegistryTools` registry value is 1 | That value prevents the agent from installing the stack. The documentation lists three places to check: under `HKU\DEFAULT`, under `HKU\S-1-5-18`, and under `HKCU`, all in `SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System`. | Remove the value from all three places, uninstall the affected stack from **Apps & Features**, remove its registry keys, restart the VM, then start the agent and let it install the stack again. |
| Event 3277 with `DownloadMsiException` | Not enough disk space for the agent. | Free space or enlarge the VM disk. |

If the status stays **Unavailable** or **Upgrading**, the agent or stack did not install correctly. The documentation says to reinstall the stack first: stop `RDAgentBootLoader`, uninstall **Remote Desktop Services SxS Network Stack**, install the newest `SxSStack*.msi` from `C:\Program Files\Microsoft RDInfra\` with `msiexec /i`, restart, and run `qwinsta` again. If `rdp-tcp` and `rdp-sxs` are still not `Listen`, register the VM again as described next.

The registry settings behind the stack are worded slightly differently on two documentation pages. One gives `fEnableWinstation` under a key named `rds-sxs`, and `SessionDirectoryListener` set to `rdp-sxs`. The other, for a Windows 10 2004 host, gives `fReverseConnectMode` and `fEnableWinStation`, both 1, in the folder that matches the version `qwinsta` shows, and `SessionDirectoryListener` as `rdp-sxs` plus that version number. If you must edit the registry, use the page that matches your Windows version.

### 8. Start again: uninstall, remove, register

The documentation says to do this when the host is stuck as **Unavailable** or **Upgrading**, you see `EXPIRED_REGISTRATION_TOKEN`, the host is not in the list, the **Remote Desktop Agent Loader** service is missing, or the earlier checks did not help.

1. On the VM, sign in as administrator. In **Programs and Features** (or **Settings**, **Apps** on Windows 11), uninstall all four components listed in check 3, then restart. You may see several copies. Remove them all. If you are connected over RDP, when the SxS Network Stack uninstall asks to close Remote Desktop Services, choose **Do not close applications**. Otherwise your RDP connection drops.
2. In the Azure portal, open the host pool, **Session hosts**, tick the host and select **Remove**. This resets the registration. In a personal host pool, note which user the host is assigned to first, so you can assign it again afterwards (this is a precaution, not a step from the agent page).
3. Generate a new registration key (check 4, step 1).
4. On the VM, run the agent installer and paste the key, then run the boot loader installer. This also installs the stack and the monitoring agent. Restart the VM.
5. In the host pool, **Session hosts**, the host should show **Available**.

## Other fixes from the same pages

| What you see | Fix |
|---|---|
| A session host update (for pools with a session host configuration) fails in the first batch with an agent, domain join or health error | Make sure the image does not have the PowerShell DSC extension. If it does, remove the folder `C:\packages\plugin` from the image. If only some hosts fail, with an error such as `AgentRegistrationFailureGeneric`, retrying the update can fix it. |
| Agent not updating, **Unavailable** in `Get-AzWvdSessionHost` | Stop `RDAgentBootLoader`, run the new agent installer, remove `INVALID_TOKEN` from the token prompt (no new token needed), finish the wizard, start `RDAgentBootLoader`. |

For a host that is registered but shows **Needs Assistance** or fails a health check, use the next article.

## If you are still stuck

Open a support case. Include what you tried and what happened. Collect:

- The `CorrelationId` from `WVDErrors` or `WVDHostRegistrations` for the failure. If `ServiceError` is `true`, the documentation says to escalate to Microsoft and give the CorrelationId.
- The text of the Application log events (event ID 3277, and 3703 or 3019 if they appear) and the contents of `C:\Windows\Temp\ScriptLog.log`.
- For event ID 3019, network trace logs. The documentation says to attach them to the case.

If the host registers but is not healthy, read [Troubleshoot an AVD Session Host That Is Unavailable or Needs Assistance](/azure-virtual-desktop/troubleshoot-session-host-unavailable-health-checks/).

## Sources

- [Troubleshoot common Azure Virtual Desktop Agent issues](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-agent)
- [Troubleshoot session host virtual machine configuration](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-vm-configuration)
- [Troubleshoot host pool creation](https://learn.microsoft.com/en-us/azure/virtual-desktop/troubleshoot-set-up-issues)
