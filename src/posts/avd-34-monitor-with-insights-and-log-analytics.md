---
title: "Monitor Azure Virtual Desktop: Insights, Log Analytics and Diagnostics"
seoTitle: "Monitor Azure Virtual Desktop: Insights and Log Analytics"
layout: post.njk
permalink: "/azure-virtual-desktop/monitor-with-insights-and-log-analytics/"
order: 134
part: 34
tags: [avd-series]
deck: "Decide what to turn on, what Azure Virtual Desktop Insights needs, which log tables answer which question, and what each level of setup collects."
description: "Set up Azure Virtual Desktop monitoring: diagnostic settings, Log Analytics, the Azure Monitor Agent and a data collection rule, Insights, key tables, queries and alerts."
---

Monitoring Azure Virtual Desktop (AVD) is not one switch. There are three separate pieces of data, and each one is turned on in a different place. If you miss one, a part of your picture stays empty.

This article is for the person who has to decide what to turn on. It explains the three pieces, what AVD Insights (a dashboard built on Azure Monitor Workbooks that helps you understand your AVD environment) needs before it shows anything, which log table answers which question, and a few ready-made queries. It also explains where alerts fit, what each setup collects and the cost points to know. Terms such as diagnostic settings and Log Analytics workspace are explained in Key terms.

This article covers Azure Virtual Desktop. It does not cover Windows 365. Related articles:

- Turning diagnostics on for a ticket and the first troubleshooting queries: [Troubleshoot AVD: Turn On the Logs and Learn to Read Them](/azure-virtual-desktop/troubleshoot-avd-start-here/). The problem-specific articles that follow it start at [Troubleshoot an AVD Black Screen After Sign-in](/azure-virtual-desktop/troubleshoot-black-screen/) and end at [Troubleshoot AVD Session Hosts That Do Not Register to the Host Pool](/azure-virtual-desktop/troubleshoot-host-pool-registration-failures/). This article does not repeat them.
- The connection path that the logs describe: [Follow a Connection Step by Step](/azure-virtual-desktop/follow-a-connection-step-by-step/).
- The network numbers that Insights reports: [Plan Bandwidth, Latency and Quality of Service for Azure Virtual Desktop](/azure-virtual-desktop/plan-bandwidth-latency-and-quality-of-service/).

## Key terms

| Term | Meaning |
|---|---|
| Azure Monitor | The Azure service for monitoring and alerts. AVD uses it like many other Azure services. |
| Log Analytics workspace | A place in Azure where log and performance data is stored so you can search it. Do not confuse it with an AVD workspace. |
| AVD workspace | The AVD object that groups application groups. It is what users see in their client. |
| Host pool | A collection of Azure virtual machines that are registered to AVD as session hosts. |
| Pooled host pool | A host pool where user sessions are load balanced to any session host in it, so several users can share a session host. |
| Application group | The object that controls access to a full desktop or a group of apps on the session hosts of one host pool. |
| RemoteApp | An application group type where users open individual apps that you publish, instead of a full desktop. |
| Session host | A virtual machine (VM) that runs users' desktops or apps. |
| Diagnostic setting | A setting on an Azure resource that sends its logs to a place you choose. |
| Log category | One kind of log, such as Connections or Errors. You tick the categories you want in a diagnostic setting. |
| Azure Monitor Agent | Software installed on a session host. It collects performance data and Windows event logs and sends them to a Log Analytics workspace. |
| Data collection rule (DCR) | A rule that says what the Azure Monitor Agent collects and where it sends it. |
| Performance counter | A measured value from a VM, such as processor time or disk queue length. |
| Windows Event Log | A log on a Windows VM, such as Application or System. |
| FSLogix | Software that gives Windows user profiles a consistent experience in virtual desktop environments. |
| Stack (RDStack) | A software component installed on your VMs so they can communicate with the AVD service. |
| Shell | The program that loads when a session starts, usually explorer.exe. Insights uses it to time how long a desktop takes to be ready. |
| AVD Insights | A dashboard built on Azure Monitor Workbooks that helps you understand your AVD environment. |
| Azure Monitor Workbook | A report page in the Azure portal that draws charts from your data. |
| Azure Monitor alert | A rule that notifies you when something in your monitoring data matches a condition you set. |
| CorrelationId | The ID of one activity, such as one connection attempt. |
| UPN | The sign-in name of a user, written like someone@example.com. |
| Event hub | An Azure Event Hubs resource. Azure Event Hubs is a real-time data streaming platform. |
| Storage account | An Azure resource that holds your Azure Storage data: blobs, files, queues and tables. |
| Azure Resource Manager | The deployment and management service for Azure. |
| ARM template | A JSON file that defines one or more resources to deploy to Azure. |
| Managed identity | An identity that you can assign to an Azure resource, such as a VM, so that it can reach other resources without you managing credentials. |

## The three pieces of data

![Diagnostic settings on the host pool, application group and AVD workspace send logs to a Log Analytics workspace. Session hosts send performance counters and Windows Event Logs through the Azure Monitor Agent and a data collection rule to a Log Analytics workspace, which can be the same one or a different one. Either workspace can be read in Logs and in AVD Insights. Azure Monitor alerts are optional, set up separately, and shown in Insights.](/img/avd/avd-monitoring-insights.svg)

*Source: [Send diagnostic data to Log Analytics for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics), [Enable Insights to monitor Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights) and [Azure Virtual Desktop Insights glossary](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights-glossary).*

| Piece | What it tells you | Where you turn it on |
|---|---|---|
| Service logs (diagnostics) | What users and admins did and what the AVD service recorded: connections, errors, feed, host registration, agent health. | **Diagnostic settings** on each host pool, application group and AVD workspace. |
| Session host performance data | How the VMs behave: processor, memory, disk, sessions, round-trip time. | The Azure Monitor Agent and a data collection rule on the session hosts. |
| Session host Windows Event Logs | Errors and warnings inside the VM, including FSLogix events. | The same data collection rule. |

AVD Insights needs data collection for all three: diagnostics, the recommended performance counters and the recommended Windows Event Logs.

## What you must turn on

### Diagnostic settings

Each AVD object (each host pool, application group and AVD workspace) has its own diagnostic setting. Turn it on for each object you want to monitor. Data is available only for activity after you turn it on, and it might take a few hours after first set-up.

These are the log categories:

| Category | What it records |
|---|---|
| Management Activities | Whether attempts to change AVD objects using APIs or PowerShell succeed. |
| Feed | Whether users can subscribe to workspaces. |
| Connections | When users start and finish connections to the service. |
| Host registration | Whether a session host registered with the service. |
| Errors | Where users hit problems with specific activities. |
| Checkpoints | Specific steps in the life of an activity that were reached. |
| Agent Health Status | The health and status of the AVD agent on each session host. |
| Network | Average network data for user sessions, including the estimated round-trip time. |
| Connection Graphics | Performance data from the AVD graphics stream. |
| Session Host Management Activity | Management activity of session hosts. |
| Autoscale | Scaling operations. |

Which categories you can pick depends on the object. For an application group the options are checkpoints, errors and management. For a workspace, the categories configure a feed that tracks when users subscribe to their list of apps. The next table lists the ones Insights needs.

The set that AVD Insights lists as required is below, named as Insights writes them:

| Object | Categories Insights needs |
|---|---|
| Host pool | Management Activities, Feed, Connections, Errors, Checkpoints, HostRegistration, AgentHealthStatus |
| AVD workspace | Management Activities, Feed, Errors, Checkpoints |

Insights lists no required categories for the application group. You can still turn them on to query them.

To set the host pool and workspace settings from the configuration workbook (opened as described in the next section), select the **Resource diagnostic settings** tab. If the workbook shows **No existing diagnostic configuration was found**, select **Configure host pool** or **Configure workspace**, then **Deploy**.

Where the data goes: the setup sends it to a Log Analytics workspace. You can also stream it to an event hub or archive it in a storage account (both are explained in Key terms). The Insights dashboard reads from Log Analytics.

Two limits to know:

- Diagnostic events are sent when the activity completes. For a connection, Log Analytics reports three states: Started (the user selects and connects to an app or desktop in the Remote Desktop client), Connected (the user connects to the VM) and Completed (the user or the server disconnects the session).
- Connections that do not reach AVD do not appear in the results, because the diagnostics service is part of AVD. A user with a network problem may leave no rows at all.

The session hosts also need to reach the URLs listed as **Diagnostic output** in the required URLs list. See [Required Connectivity for Azure Virtual Desktop](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/).

### The Azure Monitor Agent and a data collection rule

To collect data from session hosts you must do four things: configure a data collection rule for performance data and Windows Event Logs, associate the session hosts with the rule, install the Azure Monitor Agent on all session hosts in the host pools you collect from, and make sure the hosts send data to a Log Analytics workspace.

The workspace that receives session host data does not have to be the same one that receives the diagnostics.

Insights has a configuration workbook that does most of this for you. Open Insights at `aka.ms/avdi`, select **Workbooks**, then **Check Configuration**. To set up the data collection rule from a host pool:

1. In AVD, select **Host pools** and then the pooled host pool you want to monitor (a host pool where sessions are load balanced across session hosts).
2. Select **Insights**, then **Open Configuration Workbook**.
3. Open the **Session host data settings** tab.
4. Pick the **Workspace destination** (a Log Analytics workspace) and the **DCR resource group**.
5. Select **Create data collection rule**.

Then, for hosts that are not yet set up, select the rule and use **Deploy association** (creates the link between the rule and the hosts), **Add extension** (installs the Azure Monitor Agent on the hosts) and **Add system managed identity** (configures the managed identity the agent requires). The automated deployment is limited to 1,000 session hosts or fewer. For larger host pools, or if the deployment has problems, install the agent when you create the session host by using an ARM template (an Azure Resource Manager template).

The workbook also has sections for performance counters and Windows Event Logs. They list what is configured and what is missing, and a button to add the missing items.

## What AVD Insights needs before it works

| Requirement | Detail |
|---|---|
| AVD release | Every environment you monitor must be based on the latest AVD release that is compatible with Azure Resource Manager. |
| A designated Log Analytics workspace | Use a workspace dedicated to your AVD session hosts, so counters and events come only from AVD session hosts. |
| Data collection enabled | Diagnostics from AVD, the recommended performance counters and the recommended Windows Event Logs. |
| Roles for anyone who reads Insights | At minimum, Desktop Virtualization Reader on the resource group or subscription that holds the host pools, workspaces and session hosts, and Log Analytics Reader on each Log Analytics workspace used. |

Read access only lets people view data. They need other permissions to manage AVD resources.

The recommended performance counters include these (with the interval at which they are sampled). The full recommended list is longer. If counters are missing, the configuration workbook can configure them.

| Counter | Interval |
|---|---|
| Processor Information(_Total)\% Processor Time | 30 seconds |
| Memory(\*)\Available Mbytes | 30 seconds |
| Logical Disk(C:)\Avg. Disk sec/Transfer | 60 seconds |
| Terminal Services(\*)\Total Sessions | 60 seconds |
| User Input Delay per Session(\*)\Max Input Delay | 30 seconds |
| RemoteFX Network(\*)\Current TCP RTT | 30 seconds |

The required Windows Event Logs are:

| Event log | Types collected |
|---|---|
| Application | Error and Warning |
| System | Error and Warning |
| Microsoft-Windows-TerminalServices-RemoteConnectionManager/Admin | Error, Warning and Information |
| Microsoft-Windows-TerminalServices-LocalSessionManager/Operational | Error, Warning and Information |
| Microsoft-FSLogix-Apps/Operational | Error, Warning and Information |
| Microsoft-FSLogix-Apps/Admin | Error, Warning and Information |

## What Insights shows

Insights turns the data into named measures. These are the ones to learn first.

| Measure | What it means |
|---|---|
| Connection success | The connection could reach the host, as confirmed by the stack (the RDStack software) on that VM. A failed connection could not reach the host. |
| Daily active users | Users who started a session in the last 24 hours. |
| Monthly active users | Users who started a session in the last 28 days. If you store data for 30 days or less, you may see lower-than-expected values while fewer than 28 days of data are available. |
| Available sessions | VMs multiplied by the maximum sessions per VM, minus the total sessions. |
| Users per core | Users on each VM core. Tracking the maximum over time shows whether the environment runs high, low or uneven. |
| Round-trip time (RTT) | An estimate of the round trip between the user's location and the session host's Azure region. |
| Input delay | The input delay per process counter for each session, reported every 30 seconds as the worst case in that sample. Good is below 150 ms, Acceptable is 150 to 500 ms, Poor is 500 to 2,000 ms, Bad is over 2,000 ms. |
| Potential connectivity issues | Hosts, users, published resources (apps or desktops) and clients with a high connection failure rate. |
| User report | One user's connection history, usage patterns and errors. |

### Time to connect

Time to connect runs from when the user opens a resource to when the desktop is loaded and ready. Insights measures it from the service data: it begins at the `WVDConnections` state Started, and ends at the `WVDCheckpoints` name ShellReady for desktops or RdpShellAppExecuted for a RemoteApp (first app launch only). These tables are explained in the next section. The time the user spends entering credentials is subtracted.

When it is high, Insights splits it into four parts that can run in parallel, so they do not add up to the total:

| Part | What it covers |
|---|---|
| User route | From selecting the icon to the service finding a host. Look at network paths. |
| Stack connected | From the host being chosen to the connection between the host and the client. Check proxy settings and routing. |
| Logon | From the connection to the shell starting. It includes profiles, Group Policy objects (the group policies applied to a new session), shell start and FSLogix. |
| Shell start to shell ready | From the shell starting to being ready. Delay here can come from an overloaded host or configuration. |

A new session usually takes longer than reconnecting to an existing one.

## Three tables to know first

All AVD diagnostic tables start with `WVD`. These three are the ones used in the example queries and notes below:

| Table | Question it answers | Detail that matters |
|---|---|---|
| `WVDConnections` | Who connected, and did the connection start, connect and complete? | `ResourceAlias` shows desktop or published app, and only the first app opened in the connection. |
| `WVDErrors` | What went wrong, and can an admin fix it? | Also holds management errors, host registration issues and feed subscription issues. `ServiceError` equal to `false` means an admin task can resolve it. `true` means escalate to Microsoft with the CorrelationId. |
| `WVDCheckpoints` | Which steps did the activity reach? | A full desktop session does not track app use in this table. Published apps are tracked here. |

The other categories answer these questions: whether a host registered (Host registration), how healthy the AVD agent is on each host (Agent Health Status), the estimated round-trip time (Network), the graphics stream (Connection Graphics), session host management (Session Host Management Activity) and scaling operations (Autoscale). In some cases client information may be missing from `WVDConnections` and `WVDCheckpoints` even if the connection completed.

## Example queries

Run these in the workspace under **Logs**. Replace `userupn` with the user's UPN (see Key terms). In the example query screen, set the filter to **Category** and pick **Azure Virtual Desktop** to see ready-made queries.

All connections for one user:

```kusto
WVDConnections
|where UserName == "userupn"
|take 100
|sort by TimeGenerated asc, CorrelationId
```

How many times a user connected per day:

```kusto
WVDConnections
|where UserName == "userupn"
|take 100
|sort by TimeGenerated asc, CorrelationId
|summarize dcount(CorrelationId) by bin(TimeGenerated, 1d)
```

`dcount(CorrelationId)` counts the different connection attempts, and `bin(TimeGenerated, 1d)` groups them by day. As written, the query takes the first 100 rows before it counts, so a user with a long history can be undercounted.

Session duration by user:

```kusto
let Events = WVDConnections | where UserName == "userupn" ;
Events
| where State == "Connected"
| project CorrelationId , UserName, ResourceAlias , StartTime=TimeGenerated
| join (Events
| where State == "Completed"
| project EndTime=TimeGenerated, CorrelationId)
on CorrelationId
| project Duration = EndTime - StartTime, ResourceAlias
| sort by Duration asc
```

It pairs the Connected row and the Completed row of each connection by `CorrelationId` and subtracts the times. A connection with no Completed row does not appear in the result.

Errors for one user:

```kusto
WVDErrors
| where UserName == "userupn"
|take 100
```

Whether a specific error hit other users (replace `ErrorSymbolicCode` with the code you saw):

```kusto
WVDErrors
| where CodeSymbolic =="ErrorSymbolicCode"
| summarize count(UserName) by CodeSymbolic
```

## Alerts

Alerts are optional and are set up separately from Insights. You can use the Azure Monitor alerts framework to set custom alerts on AVD events, diagnostics and resources. Insights then shows the Azure Monitor alerts in your selected subscription next to your AVD data.

Two details on how Insights shows them. Active alerts that you classified as severity 0 appear on the Overview page. Severity 0 alerts are the most urgent items. If you do not address them, they could cause your deployment to stop working. Insights also reports the number of alerts triggered each day.

Which alert rules to create is your decision. Base them on your own questions, using the tables above. For example, the Agent Health Status category holds the health and status of the AVD agent on each session host, and the `WVDErrors` table holds errors.

## What each setup collects, and the cost points

Prices are not covered here. See Azure Monitor pricing for current prices.

| Setup | What it collects |
|---|---|
| Diagnostic settings only | Service logs for the objects you enable. The data can go to a Log Analytics workspace, an event hub or a storage account. |
| Insights | The diagnostics, plus the recommended performance counters and Windows Event Logs from the session hosts. |
| Alerts | Rules you create in Azure Monitor. They are optional and set up separately. |

Cost points for the Log Analytics workspace that Insights uses:

- Standard data storage charges for Log Analytics apply.
- To start, choose the pay-as-you-go pricing model and adjust as you scale and take in more data.
- The data setup described for Insights is the only one you need to monitor AVD. You can disable all other items that send data to the workspace to save costs.
- Insights asks for a designated workspace for your session hosts, so that performance counters and events are collected only from AVD session hosts.

## Common mistakes

- **Turning on diagnostics for the host pool only.** Each object needs its own setting. Insights lists separate required categories for the host pool and the AVD workspace.
- **Turning on the logs but not the session host data.** Insights then lacks the performance counters and Windows Event Logs.
- **Skipping the roles.** Insights needs Desktop Virtualization Reader and Log Analytics Reader for the people who read it.
- **Sharing the workspace with other VMs.** Counters and events should come only from AVD session hosts.
- **Reading empty logs as no problem.** A connection that never reached AVD leaves no rows.
- **Trusting one monthly number.** If you store data for 30 days or less, monthly active users can look low.
- **Expecting alerts to appear on their own.** They are optional and set up separately.

## How to validate this in your environment

1. Open a host pool, an application group and the AVD workspace in turn. Select **Diagnostic settings** on each. Confirm a setting is listed with the categories you need.
2. Open `aka.ms/avdi`, select **Workbooks**, then **Check Configuration**. Pick the subscription, resource group and host pool. Confirm no error says **No existing diagnostic configuration was found**.
3. On the **Session host data settings** tab, confirm that the **Session hosts** warning (**Some hosts in the host pool are not sending data to the selected Log Analytics workspace**) is not shown.
4. In the configuration workbook, check that **Missing counters** and **Missing Event Logs** are empty.
5. In the Log Analytics workspace, select **Logs**, and run the first query above with your own UPN. Confirm rows appear for a test sign-in. After first set-up it might take a few hours.
6. Confirm the people who read Insights have the Desktop Virtualization Reader and Log Analytics Reader roles.
7. If you use alerts, open Insights and confirm that your severity 0 alerts show on the Overview page.

## Sources

- [Send diagnostic data to Log Analytics for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics)
- [Enable Insights to monitor Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights)
- [Azure Virtual Desktop Insights glossary](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights-glossary)
