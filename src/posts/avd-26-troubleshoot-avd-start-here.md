---
title: "Troubleshoot AVD: Turn On the Logs and Learn to Read Them"
seoTitle: "Troubleshoot AVD: Turn On Diagnostics and Read the Logs"
layout: post.njk
permalink: "/azure-virtual-desktop/troubleshoot-avd-start-here/"
order: 126
part: 26
tags: [avd-series]
deck: "Switch on diagnostics, learn which table holds what, and run the first three queries on any Azure Virtual Desktop ticket."
description: "Turn on Azure Virtual Desktop diagnostics, learn the WVD tables and the CorrelationId, and run the first queries for any user who cannot connect."
---

A user says "AVD does not work". Before you change anything, you need to see what the service recorded. That only works if diagnostics were switched on before the problem happened. Azure Virtual Desktop (AVD) does not keep a history for you to read later.

This article sets that up. It shows how to turn diagnostics on, what each log table holds, and how one connection is tied together across tables. It ends with the first queries to run for any ticket. The troubleshooting articles that follow each link back here for the setup.

The method is the same in every article. First ask how wide the problem is: one user, one host or everyone. Then ask how far the connection got. Then read the error. Check the cheapest and most likely cause first, and change something only when the evidence points to it.

For the bigger picture of what can fail, read [How Azure Virtual Desktop fails](/azure-virtual-desktop/how-azure-virtual-desktop-fails/) first. For the connection steps, see [Follow a connection step by step](/azure-virtual-desktop/follow-a-connection-step-by-step/).

## Key terms

| Term | Meaning |
|---|---|
| Session host | A virtual machine that runs users' desktops or apps. |
| Host pool | A group of session hosts that serve the same kind of desktop or app. |
| Application group | The object that decides which desktop or apps from one host pool a user can open. |
| Workspace | The AVD object that groups application groups. It is what users see in their client. Do not confuse it with a Log Analytics workspace. |
| Log Analytics workspace | An Azure Monitor store where logs are kept so you can search them. |
| Diagnostic setting | A setting on an Azure resource that sends its logs to a place you choose, such as a Log Analytics workspace. |
| Kusto Query Language (KQL) | The language you use to search logs in a Log Analytics workspace. |
| CorrelationId | The ID of one connection attempt. Every log row that belongs to that connection carries the same value. |
| UPN | User principal name, the user's sign-in name. It looks like an email address. |
| AVD agent | Software on each session host. It talks to the AVD service and reports the host's health. |
| Health check | A test the AVD agent runs on a session host. |
| Azure Monitor workbook | A report page in the Azure portal that draws charts from logs. |
| FSLogix profile container | The virtual disk file that holds a user's profile. |

## Turn on diagnostics first

Diagnostics are off until you turn them on, and each AVD object (each host pool, application group and workspace) has its own setting. Enable diagnostics for each object you want to monitor. Data is available only for activity after you enable it, and it might take a few hours after the first set-up.

You need a Log Analytics workspace before you start. If you do not have one, create one in the Azure portal first (search for **Log Analytics workspaces**, then **Create**). Then repeat these steps for each host pool, application group and workspace:

1. In the Azure portal, search for **Azure Virtual Desktop** and open it. In its left menu, pick **Host pools**, **Application groups** or **Workspaces**, then open the object.
2. Select **Diagnostic settings** in the object's left menu.
3. Select **Add diagnostic setting**. The options differ by object type.
4. Enter a name. It should not contain spaces.
5. Select **Send to Log Analytics** and choose your Log Analytics workspace when the portal asks. Then tick the categories you want. A category is one kind of log, such as Connections or Errors.
6. Select **Save**.

You are done with an object when its **Diagnostic settings** page lists your new setting.

AVD Insights, the Azure Monitor workbook described below, lists the categories it needs. On a host pool they are Management Activities, Feed, Connections, Errors, Checkpoints, HostRegistration and AgentHealthStatus. On the AVD workspace they are Management Activities, Feed, Errors and Checkpoints. The diagnostics page also lists a Network category (connection network data) and a Connection Graphics category. Tick everything you may want to query later.

Diagnostics also need the session hosts to reach the URLs listed under **Diagnostic output** in the required URLs list. See [Required connectivity for Azure Virtual Desktop](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/).

## Open the logs

1. In the Azure portal, search for **Log Analytics workspaces** and open the workspace you chose.
2. Select **Logs**.
3. A window of example queries may open first. Close it to get an empty query editor. Paste a query into the editor and select **Run**. The results appear below it.

All AVD diagnostic tables start with `WVD`. A table is a list of rows, one row per logged event, and each row has named columns.

You can also use **Monitor** > **Logs** and set the scope there. In the example queries screen, set the filter to **Category** and choose **Azure Virtual Desktop** to see ready-made queries.

Log data can arrive late. Azure Monitor can take up to 15 minutes to show log data, so Insights can be that far behind. If you see nothing from the last few minutes, wait and refresh.

## What each table holds

![Left to right, the user and client connect to the Azure Virtual Desktop service, which connects them to a session host. The service writes connection, checkpoint, error, registration and network tables to a Log Analytics workspace once diagnostic settings are on, and AVD Insights reads that workspace. The session host sends agent health to the workspace and keeps its own Windows event logs and FSLogix logs.](/img/avd/troubleshoot-avd-start-here.svg)

*Source: [Send diagnostics to Log Analytics](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics) and the Azure Monitor reference pages for each table.*

| Table | What a row records | Columns you will use first | Comes from |
|---|---|---|---|
| `WVDConnections` | One state of one connection: Started, Connected or Completed. | `UserName`, `State`, `CorrelationId`, `SessionHostName`, `ClientType`, `ClientVersion`, `GatewayRegion`, `TransportType` | Host pool |
| `WVDErrors` | An error in an activity such as a connection, a feed subscription, a management action or a host registration. | `UserName`, `Code`, `CodeSymbolic`, `Message`, `ServiceError`, `Source`, `ActivityType`, `CorrelationId` | Host pool, application group, workspace |
| `WVDCheckpoints` | A step that a connection or other activity reached. | `Name`, `Parameters`, `Source`, `CorrelationId` | Host pool, application group, workspace |
| `WVDAgentHealthStatus` | The health of the AVD agent on one session host. | `SessionHostName`, `Status`, `SessionHostHealthCheckResult`, `AgentVersion`, `SxSStackVersion`, `UpgradeState`, `UpgradeErrorMsg`, `LastHeartBeat` | Host pool |
| `WVDHostRegistrations` | A session host registering with the service. | `SessionHostName`, `SessionHostIPAddress` | Host pool |
| `WVDConnectionNetworkData` | Estimated round-trip time and bandwidth for a connection. | `EstRoundTripTimeInMs`, `EstAvailableBandwidthKBps`, `CorrelationId` | Host pool |

The "Comes from" column is the resource type listed on each table's reference page. It tells you which object needs the diagnostic setting. The network data table is written every two minutes during an active session.

A few details from the table pages:

- In `WVDConnections`, `TransportType` is Shortpath, TURN or Websocket. `SessionHostJoinType` is DomainJoined, HybridAzureADJoined or AzureADJoined.
- In `WVDConnections`, the `ResourceAlias` column shows whether the user connected to a full desktop or a published app. It shows only the first app they open in the connection.
- `WVDErrors` also records management errors, host registration issues and problems while a user subscribes to a feed.
- When a user opens a full desktop, their app use inside the session is not tracked in `WVDCheckpoints`.

## One connection, one CorrelationId

Each connection attempt has a `CorrelationId`. It is the ID of that activity, and it is assigned to every diagnostic within the connection. So you find the failing attempt in `WVDConnections`, copy its `CorrelationId`, and look for the same value in `WVDErrors`, `WVDCheckpoints` and `WVDConnectionNetworkData`.

`WVDConnections` reports a connection in three states:

| State | When it is written |
|---|---|
| Started | The user selects an app or desktop in the client. |
| Connected | The user connects to the VM that hosts the app or desktop. |
| Completed | The user or the server disconnects the session. |

A connection with Started but no Connected never reached a session host. A connection with Connected but no Completed is still running, or its end was not recorded.

## Two limits to know before you trust a result

**Connections that never reach AVD leave no rows.** The diagnostics service is part of AVD. If the user's network, DNS or client stops the connection before it reaches the service, nothing is logged. "The user says it failed and the logs are empty" points to the client side or the network, not to a missing log. See [Required connectivity](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/).

**`ServiceError` tells you who can fix it.** In `WVDErrors`, `ServiceError` equal to `false` means the issue can be resolved by an admin task. `true` means you need to escalate to Microsoft, and give them the CorrelationId when you do.

## How to read a KQL query

A query starts with a table name. Each following line starts with `|` (a pipe). The pipe takes the rows from the line above, changes them and passes the result to the next line. You read a query from top to bottom. These are the keywords used in this series:

| Keyword | What it does |
|---|---|
| `where` | Keeps only the rows that match the test. `==` means "is equal to". |
| `take 100` | Returns at most 100 rows. They are not necessarily the newest. |
| `sort by` | Orders the rows. `asc` is smallest first, `desc` is largest first. |
| `project` | Keeps only the columns you name. |
| `summarize` | Groups rows and calculates a number for each group, such as `count()`. |
| `join` | Puts rows from two tables side by side where a column matches, such as `CorrelationId`. |
| `ago(1d)` | The time one day before now. `7d` is seven days, `2h` is two hours. |
| `//` | The rest of the line is a comment. It is ignored. |

Log Analytics stores times in UTC (`TimeGenerated`). Convert the user's local time before you look for their attempt. The time range picker above the editor also limits how far back a query looks. If a query has its own `where TimeGenerated > ago(...)` line, the picker shows **Set in query**.

## The first queries to run

Run these in the workspace under **Logs**. They are the Log Analytics samples from the diagnostics page. Replace `userupn` with the user's UPN, such as `alex@contoso.com`. Keep the double quotes.

All connections for one user:

```kusto
WVDConnections
|where UserName == "userupn"
|take 100
|sort by TimeGenerated asc, CorrelationId
```

- Line 1 chooses the connections table.
- Line 2 keeps only this user's rows.
- Line 3 limits the result to 100 rows.
- Line 4 puts the rows in time order, oldest first, and keeps the rows of one connection together.

`take 100` runs before `sort`, so if the user has a long history you get 100 rows picked first and then sorted. If the attempt you want is missing, add `| where TimeGenerated > ago(1d)` after line 2.

What a healthy result looks like: each attempt has up to three rows with the same `CorrelationId`, with `State` going Started, then Connected, then Completed. What a bad result looks like: an attempt with Started and nothing after it, or no rows at all for the time of the problem.

Errors for one user:

```kusto
WVDErrors
| where UserName == "userupn"
|take 100
```

This returns the error rows for the user. An empty result means AVD logged no error for that user in the time range. It does not prove the user had no problem, because a connection that never reached AVD logs nothing. A bad result is a row with a `CodeSymbolic` and a `Message`. Read both, and note `ServiceError`.

Did the same error hit other users? Copy the `CodeSymbolic` from the previous result and put it in place of `ErrorSymbolicCode`:

```kusto
WVDErrors
| where CodeSymbolic =="ErrorSymbolicCode"
| summarize count(UserName) by CodeSymbolic
```

- Line 2 keeps only rows with that error.
- Line 3 counts the user names in those rows and shows one result row for the error.

If the count is only the one user you started with, the problem is probably tied to that user, their device or their profile. If the count is large, many users hit the same error, so look at something shared, such as a session host, a policy or the network. These readings are a rule of thumb, not an official threshold.

To see each connection attempt with its errors and checkpoints together, use the **Connection Errors** sample for `WVDConnections`. It joins the three tables on `CorrelationId`. Its comment says you can uncomment the user filter to look at one user. It is on the [WVDConnections sample queries page](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/queries/wvdconnections).

## AVD Insights

AVD Insights is a dashboard built on Azure Monitor workbooks. Open it at `aka.ms/avdi`, or from a host pool by selecting **Insights**. It reads from your Log Analytics workspace, so it needs the same diagnostics. It also needs the Azure Monitor Agent, a data collection rule for performance counters and Windows event logs, and the roles Desktop Virtualization Reader and Log Analytics Reader at a minimum. The first time you open it, use **Workbooks** > **Check Configuration**.

The tabs named in the use-case pages are Connection Performance, Connection Reliability, Host Performance, Host Diagnostics, Clients and Utilization. They are useful to see whether a problem touches one user, one host or everyone.

Known limits from the Insights troubleshooting page: a connection's completion event can go missing, which skews some charts. The time to connect includes the time users spend typing their credentials, so a peak can be false.

## Logs on the session host

Some evidence is only on the session host. Sign in to the host as an administrator, the way you normally manage a VM (for example over Azure Bastion or RDP), search the Start menu for **Event Viewer** and open it. Then go to **Windows Logs** > **Application** and look for events from these sources: WVD-Agent, WVD-Agent-Updater, RDAgentBootLoader and MsiInstaller. These are the sources that log agent and connection problems. The host articles in this series use them.

FSLogix keeps its own logs. The text logs are in `C:\ProgramData\FSLogix\Logs`, and the profile log is in the `Profile` folder under it. Logging settings must be configured first. The FSLogix event logs are in Event Viewer under **Applications and Services Logs** > **FSLogix**. The FSLogix profile articles in this series cover how to read them.

## What to do in the first two minutes

This order is my suggestion.

1. Check Azure status and Azure Service Health. Do this before anything else.
2. Run the all-connections query for the user. Did a row appear for the time of the problem? If not, the connection did not reach AVD.
3. If rows appear, look at the last `State` and copy the `CorrelationId`.
4. Run the errors query. Look at `ServiceError`, `CodeSymbolic` and `Message`.
5. Run the "same error, other users" query to learn whether this is one user or many.

Then pick the article that fits what you found:

| What you found | Open |
|---|---|
| Credentials accepted, then a black screen | [Troubleshoot an AVD Black Screen After Sign-in](/azure-virtual-desktop/troubleshoot-black-screen/) |
| Temporary, empty or slow profile | [Troubleshoot FSLogix: Profile Does Not Load or Is Temporary](/azure-virtual-desktop/troubleshoot-fslogix-profile-fails-to-load/) |
| A session host that is not Available, or "no resources available" | [Troubleshoot an AVD Session Host That Is Unavailable or Needs Assistance](/azure-virtual-desktop/troubleshoot-session-host-unavailable-health-checks/) |
| Sessions that drop, lag or sign in slowly | [Troubleshoot AVD Disconnects and Slow Sessions](/azure-virtual-desktop/troubleshoot-disconnects-and-slow-sessions/) |
| Cannot sign in, repeated prompts, empty feed, AADSTS codes | [Troubleshoot AVD Sign-in Failures: Conditional Access, MFA and Single Sign-on](/azure-virtual-desktop/troubleshoot-sign-in-and-conditional-access/) |
| A new or rebuilt host that never registers | [Troubleshoot AVD Session Hosts That Do Not Register to the Host Pool](/azure-virtual-desktop/troubleshoot-host-pool-registration-failures/) |

## Common mistakes

- **Turning on diagnostics after the problem.** There is no history to read.
- **Enabling it on the host pool only.** Enable it on each object you want to monitor.
- **Reading empty logs as "no problem".** A connection that never reached the service leaves no rows.
- **Trusting one Insights peak.** Time to connect includes typing credentials.

Next: [Troubleshoot an AVD Black Screen After Sign-in](/azure-virtual-desktop/troubleshoot-black-screen/).

## Sources

- [Send diagnostics to Log Analytics](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics)
- [Analyze connection quality](https://learn.microsoft.com/en-us/azure/virtual-desktop/connection-latency)
- [Enable Insights](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights)
