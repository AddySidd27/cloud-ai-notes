---
title: "Log Analytics, Azure Monitor Agent and a Heartbeat Alert for Your VM"
seoTitle: "Azure Log Analytics and VM Heartbeat Alert for Beginners"
layout: post.njk
permalink: "/azure-basics-labs/log-analytics-alert/"
order: 326
tags: [azure-basics-lab]
deck: "You send data from your lab VM to a Log Analytics workspace, read its heartbeat with a query, and get an email when the VM stops reporting."
description: "Beginner Azure lab: create a Log Analytics workspace, connect a VM with a data collection rule and Azure Monitor Agent, query Heartbeat and set an email alert."
---

By the end of this lab you will have a Log Analytics workspace named `log-azb-lab`, your Lab 12 VM sending data to it, a query that shows when the VM last reported, and an alert that emails you when the VM goes quiet. You test the alert by stopping the VM.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

A Log Analytics workspace is a place in Azure where logs and performance data are stored, and where you search them with queries. Azure Monitor is the Azure service that collects that data and raises alerts on it. Almost everything you do to watch an Azure Virtual Desktop (AVD) environment later ends up in a workspace like this one.

## What you need

- [Lab 3: Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): the action group `ag-azb-email`, with your email address already verified.
- [Lab 12: Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the Windows VM `vm-azb-win01` in `rg-azb-lab`, with its system-assigned managed identity. The VM must be running when you start. You do not sign in to it in this lab, so you do not need the RDP rule.
- [Lab 13: VM size, disk type and power states](/azure-basics-labs/vm-size-disk-stop-deallocate/): you use its stop (deallocate) step to test the alert.
- Time: about 45 minutes of work, plus waiting. Data takes a few minutes to arrive. The alert test takes longer, see the test part below.
- Cost: a Log Analytics workspace uses a pay-as-you-go price. Alert rules and email notifications can have their own small charges, so read the pricing page below. Learn says no charges build up until data collection begins, and then you pay per GB of data you send. The `Heartbeat` table is one of the tables Learn lists as free from ingestion charges. The performance and event data in this lab is billed per GB, so the lab keeps it small. See "Safety first" and "Clean up". I have no price to give you, so check [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/) for your region.
- Role: owner of your own test subscription covers everything here. Learn names Log Analytics Contributor for creating a workspace, Monitoring Contributor for creating data collection rules, and Virtual Machine Contributor for installing the agent.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top right of the portal before you change anything.
- The workspace costs money only when data goes in. Do not add more data sources than this lab says. Do not leave the lab running for weeks.
- Do not connect any other VM to this workspace.
- The alert test stops your VM. A stopped (deallocated) VM does not lose its disk. Start it again when the test is done.
- Do not delete `ag-azb-email`. Later labs use it.
- Deleting the workspace also deletes the data in it. That is fine here.

## What the lab builds

![A left-to-right diagram inside the resource group rg-azb-lab. The Windows VM from Lab 12 runs the Azure Monitor Agent. A data collection rule tells the agent what to collect and sends it to the Log Analytics workspace log-azb-lab. A log search alert rule named VM not sending heartbeat checks the workspace and notifies the action group ag-azb-email, which emails you.](/img/basics/log-analytics-alert.svg)

*Source: Learn pages [Create a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/quick-create-workspace), [Collect guest log data from virtual machines with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection), [Install and manage the Azure Monitor Agent](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-manage), [Log data ingestion time in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-ingestion-time) and [Create or edit a log search alert rule](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-log-alert-rule). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

**Idea 1: three parts that work together.** The workspace stores the data. The Azure Monitor Agent is a small program that runs on the VM and sends data. A data collection rule (DCR) tells the agent what to collect and where to send it. Learn says the agent starts collecting only after the VM is linked to a DCR. That link is called an association.

### Part 1: Create the workspace

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name.
2. Search for **Log Analytics workspaces** and open it. Select **Create**.
3. Set **Subscription** to your test subscription and **Resource group** to `rg-azb-lab`.
4. Set **Name** to `log-azb-lab`. Learn says the name must be unique per resource group.
5. Set **Region** to the same region as your VM. Pick one region for the whole series. Learn says the DCR must be in the same region as the workspace, so keeping everything in one region avoids a problem in Part 2.
6. Select **Review + Create**, then **Create**. Learn says a default pay-as-you-go pricing tier is applied and no charges accrue until data collection begins.

**Retention.** Retention is how many days the workspace keeps data. Learn says the default for tables in a workspace is 30 days. You can lower it to as little as four days with the API or CLI, but Learn also says 31 days of retention are included in the ingestion price, so lowering it below 31 days does not reduce cost. So leave retention at the default. There is nothing to save by changing it. If you want to see the setting, open the workspace, then **Settings** > **Usage and estimated costs** > **Data Retention**. Close it without changing anything.

Check: `log-azb-lab` appears in the **Log Analytics workspaces** list with status Succeeded or similar, in `rg-azb-lab`.

### Part 2: Create the data collection rule and connect the VM

**Idea 2: the DCR installs the agent for you.** Learn says that creating a DCR in the Azure portal is the recommended way to install the Azure Monitor Agent through the portal. The agent is installed automatically if it is needed, and an association is created between the DCR and each VM you select. Learn also says the agent needs a managed identity on the VM. A managed identity is an identity Azure gives to a resource so it can sign in to other Azure services without a password. When you add a VM to a DCR in the portal, Learn says the default is to enable a system-assigned managed identity for it. Your Lab 12 VM already has one, so the portal keeps it.

7. Search for **Monitor** and open it. In the left menu, select **Data Collection Rules**, then **Create**.
8. On **Basics**, set **Rule Name** to `dcr-azb-lab`, **Subscription** to your test subscription, **Resource group** to `rg-azb-lab`, and **Region** to the same region as the workspace.
9. Look at **Type of telemetry** (Learn's wording for the default portal experience). It decides which data sources you can add. Choose the option that offers Windows event logs and performance counters. If you are unsure which one, select **Help me choose** next to it. If your portal shows the classic experience instead, Learn says to set **Platform Type** to **Windows**. Leave **Data Collection Endpoint** empty. Learn says an endpoint is needed only for some data sources, and **Help me choose** shows which. Select **Next**.
10. On **Resources**, select **Add resources** and tick your Lab 12 VM. Learn says the portal turns on a system-assigned managed identity for it by default. Keep that default. Select **Next**.
11. On **Collect and deliver**, select **Add new dataflow** (the classic experience says **Add data source**).
    - Data source type **Windows Event Logs**. Learn describes a basic choice of logs and severity levels. Choose only the **System** log and only the **Critical** and **Error** levels. Set the destination to **Azure Monitor Logs** and select `log-azb-lab`. Learn says the events land in the **Event** table.
    - Add a second data source of type **Performance Counters**. Choose the basic set, and pick the smallest selection you are offered and the slowest collection setting. Learn says performance counters land in the **Perf** table in the workspace. Use the same destination, `log-azb-lab`.
    - Learn warns that adding more than one destination of the same type sends the data twice and raises cost. Add the workspace once only.
12. Select **Review + create**, then **Create**.

Why so little? Learn says `Event` and `Perf` data is billed per GB. You do not need much of either for this lab. The heartbeat that the alert uses is a separate table.

13. Wait. Learn says it can take up to 5 minutes for data to reach the destination after you create a DCR, and several minutes after installation for the first heartbeat.

Check: open your VM, then **Settings** > **Extensions + applications**. `AzureMonitorWindowsAgent` should show **Provisioning succeeded**. Open the DCR `dcr-azb-lab`, then **Configuration** > **Resources**: your VM is listed.

### Part 3: Read the heartbeat with a query

The Azure Monitor Agent sends a small record to a table called `Heartbeat` about once a minute to show it is alive. Learn says the table holds records logged by the agent once per minute to report on agent health.

14. Open the workspace `log-azb-lab`, then select **Logs** in the left menu. If a window with example queries opens, close it.
15. Paste this query and select **Run**:

    ```kusto
    Heartbeat
    | summarize arg_max(TimeGenerated, *) by Computer
    ```

    `arg_max(TimeGenerated, *)` means: for each computer, keep the whole row with the newest `TimeGenerated`. Learn lists `Computer` (the computer name) and `TimeGenerated` (when the record was created) as columns of the `Heartbeat` table.
16. Look at the result. You should see one row for your VM. The `Computer` value is the Windows computer name, which can differ from the VM name in the portal. `TimeGenerated` should be within the last few minutes.
17. If the table does not exist or the result is empty, wait a few more minutes and run it again. Learn says the first heartbeat can take several minutes after installation.

Check: one row for your VM, with a recent `TimeGenerated`. Also run `Event | take 10` and `Perf | take 10`. `Perf` should show rows after a few minutes. `Event` can stay empty on a healthy VM, because you only collect critical and error events from the System log.

### Part 4: Create the alert

**Idea 3: an alert cannot easily see "nothing".** A log search alert rule runs a query on a schedule and fires when the result meets a condition. Learn warns that log search alerts work best for finding specific data in logs, and less well for finding a lack of data. Logs are inherently more latent than metric data, such as a VM heartbeat, so a missing heartbeat can cause false alarms. Learn suggests metric alerts if you need to avoid misfires. This lab still uses a log alert, because the workspace is the thing you are learning, and it uses the approach Learn itself shows for finding silent computers: look back over a longer period, find each computer's newest heartbeat, and check how old it is. Learn's page on ingestion time has a query for this, using a one-day look back. The alert below adapts it.

There is one more catch. A VM that never sent a heartbeat is not in the table, so this alert cannot catch it. It catches a VM that was reporting and then stopped.

18. In the portal, select **Monitor**, then **Alerts** in the left pane, then **Create** > **Alert rule**. On the **Select a resource** pane, set the scope to your workspace `log-azb-lab` (filter by resource type if the list is long) and select **Apply**.
19. On the **Condition** tab, select the **Signal name** field and choose **Custom log search**.
20. In the **Logs** pane, paste this query:

    ```kusto
    Heartbeat
    | summarize LastHeartbeat = max(TimeGenerated) by Computer
    | where LastHeartbeat < ago(10m)
    ```

    Learn says log search alert queries support `ago()` with timespan literals only, such as `10m`. This query returns a row for each computer whose newest heartbeat is older than 10 minutes. It returns nothing while the VM reports.
21. Select **Run**, then **Continue Editing Alert**. Today the VM is running, so the result should be empty.
22. In **Measurement**, set **Measure** to **Table rows** and **Aggregation type** to **Count**. If the page shows **Aggregation granularity**, set it to 5 minutes. Learn says the rule counts the number of results in the last five minutes by default. In **Alert logic**, set **Operator** to **Greater than**, **Threshold value** to `0`, and **Frequency of evaluation** to `5 minutes`. Learn says the frequency can be anything from one minute to one day.
23. Open **Advanced options**. Find **Override query time range** and set it to 1 day. Learn says this setting exists for when the alert evaluation period differs from the query time range, and that the maximum is two days. Without it, the query would only look at the last few minutes and would never find a heartbeat older than 10 minutes. Do not skip this step.
24. On the **Actions** tab, select **Select action groups** and pick `ag-azb-email` from Lab 3.
25. On the **Details** tab, set **Subscription** and **Resource group** to your test subscription and `rg-azb-lab`. Set **Severity** to **2 - Warning** (or any level you like). Set **Alert rule name** to `VM not sending heartbeat`. Set **Region** to your lab region.
26. In **Advanced options** on this tab, keep **Enable upon creation** ticked. Tick **Automatically resolve alerts** so that the alert closes by itself when the heartbeat returns. Learn says this makes the alert stateful, and that it resolves when the condition is no longer met for a number of evaluation periods that depends on the frequency.
27. Select **Review + create**, then **Create**.

Check: the rule `VM not sending heartbeat` appears under **Monitor** > **Alerts** > **Alert rules**, with status Enabled.

### Part 5: Test it by stopping the VM

28. Go to your VM and select **Stop**, the same way as in Lab 13. Wait for the status to read **Stopped (deallocated)**. Note the time.
29. Wait. This takes a while, and you cannot speed it up. Here is why, step by step:
    - The query only returns the VM after its newest heartbeat is more than 10 minutes old.
    - The rule runs every 5 minutes, so it can take up to 5 more minutes before a run sees that.
    - Learn says the average delay from creating a log record to being able to query it is under 10 seconds, so ingestion is not the main delay.
    - Learn gives no figure for how long the email takes after the alert fires. I did not find one.

    So expect the email at roughly 15 minutes after the VM stops at the earliest, and plan for 20 to 30 minutes. That is my estimate from the settings above, not a number from Learn. If nothing arrives after 30 minutes, check your spam folder, then read "The most common mistake".
30. When the email arrives, open the alert in **Monitor** > **Alerts**. You should see the alert with the rule name and the VM's computer name.
31. Select **Start** on the VM. After a few minutes the heartbeat returns. With **Automatically resolve alerts** on, the alert should resolve itself. Learn says this takes more than one evaluation period, so give it some time.

Check: you got an email from the `ag-azb-email` action group after stopping the VM, and the alert shows as resolved after you started the VM again.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Check the tenant and subscription first. If you already did the portal steps, skip this section, because the names below match the portal steps and would clash.

The CLI covers the workspace, the rule, the agent and the association. It does not cover the alert. The `az monitor scheduled-query create` command on Learn lists no option for **Override query time range**, and the alert in Part 4 needs it. Create the alert in the portal.

Set the variables:

```bash
az account show --query "{tenant:tenantId, subscription:name}" -o table

LOCATION="<your-region>"   # the one region you use for the whole series, for example eastus
RG="rg-azb-lab"
VM="vm-azb-win01"
WS="log-azb-lab"
DCR="dcr-azb-lab"
```

Create the workspace. Learn says the default retention is 30 days and the default pricing tier is `PerGB2018`, so you do not set either:

```bash
az monitor log-analytics workspace create --resource-group $RG --workspace-name $WS --location $LOCATION
WS_ID=$(az monitor log-analytics workspace show --resource-group $RG --workspace-name $WS --query id --output tsv)
echo $WS_ID
```

Check: `az monitor log-analytics workspace show` prints the workspace and `$WS_ID` is not empty.

Create the rule. A DCR created from the CLI needs a JSON file. This one follows the sample DCRs on Learn: critical and error events from the System log, and one performance counter once a minute, both sent to the workspace. The first command writes the file, the second puts your workspace ID in it:

```bash
cat > dcr-azb-lab.json <<'EOF'
{
  "location": "LOCATION_HERE",
  "properties": {
    "dataSources": {
      "windowsEventLogs": [
        {
          "name": "systemErrors",
          "streams": ["Microsoft-Event"],
          "xPathQueries": ["System!*[System[(Level = 1 or Level = 2)]]"]
        }
      ],
      "performanceCounters": [
        {
          "name": "cpuOnly",
          "streams": ["Microsoft-Perf"],
          "samplingFrequencyInSeconds": 60,
          "counterSpecifiers": ["\\Processor(_Total)\\% Processor Time"]
        }
      ]
    },
    "destinations": {
      "logAnalytics": [
        { "workspaceResourceId": "WORKSPACE_ID_HERE", "name": "logazblab" }
      ]
    },
    "dataFlows": [
      {
        "streams": ["Microsoft-Event"],
        "destinations": ["logazblab"],
        "transformKql": "source",
        "outputStream": "Microsoft-Event"
      },
      {
        "streams": ["Microsoft-Perf"],
        "destinations": ["logazblab"],
        "transformKql": "source",
        "outputStream": "Microsoft-Perf"
      }
    ]
  }
}
EOF
sed -i "s|WORKSPACE_ID_HERE|$WS_ID|; s|LOCATION_HERE|$LOCATION|" dcr-azb-lab.json
az monitor data-collection rule create --resource-group $RG --location $LOCATION --name $DCR --rule-file dcr-azb-lab.json
DCR_ID=$(az monitor data-collection rule show --resource-group $RG --name $DCR --query id --output tsv)
```

The first run of `az monitor data-collection rule` may ask to install an extension. Say yes. Learn says it installs the first time you use the command. Learn also says the CLI gives a generic error if the JSON is wrong. If the command fails, look at the file again. The file follows the sample rules on Learn, one data flow for each stream.

Check: `az monitor data-collection rule show --resource-group $RG --name $DCR` prints the rule and `$DCR_ID` is not empty.

Install the agent and link the rule. Learn says the agent needs a managed identity on the VM, and that a CLI install does not create a DCR, so you must create the association yourself. The VM from Lab 12 already has a system-assigned identity, so the commands below do not turn it on. They check that it is there, install the agent and link the rule:

```bash
az vm show --resource-group $RG --name $VM --query identity
VM_ID=$(az vm show --resource-group $RG --name $VM --query id --output tsv)
az vm extension set --name AzureMonitorWindowsAgent --publisher Microsoft.Azure.Monitor --ids $VM_ID --enable-auto-upgrade true
az monitor data-collection rule association create --name dcra-azb-lab --rule-id $DCR_ID --resource $VM_ID
```

The first command should show a `SystemAssigned` identity. If it shows nothing, run `az vm identity assign --resource-group $RG --name $VM` (Learn's command for an existing VM) and then carry on.

Check: `az vm extension list --resource-group $RG --vm-name $VM --output table` lists `AzureMonitorWindowsAgent` with `Succeeded`. After a few minutes, run the `Heartbeat` query from Part 3 in the portal, in the workspace's **Logs** page.

To read the data without the portal you would need more CLI commands that I have not checked on Learn, so this lab does the query in the portal. Then create the alert in the portal as in Part 4.

## Terraform

No Terraform in this lab, because the same setup is already written as Terraform for AVD session hosts. The same pieces (workspace, data collection rule, Azure Monitor Agent extension, association, action group and a heartbeat alert) are written as Terraform for AVD session hosts in [AVD Monitoring Starter Lab with Terraform](/terraform-labs/avd-monitoring-lab/). It also says its code was not run through `terraform validate`, so read it as a reference. Come back to it after [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/).

## Check that it works

- The workspace `log-azb-lab` exists in `rg-azb-lab`.
- The VM shows `AzureMonitorWindowsAgent` as Provisioning succeeded, and `dcr-azb-lab` lists the VM under Resources.
- `Heartbeat | summarize arg_max(TimeGenerated, *) by Computer` returns one row for the VM with a recent `TimeGenerated`.
- The alert query from Part 4 returns no rows while the VM is running.
- After the VM was stopped, an email from `ag-azb-email` arrived, and the alert resolved after the VM was started again.

## The most common mistake

Forgetting **Override query time range** (step 23). Without it, the alert query only looks at a short window. A stopped VM has no rows in that window, so the query finds no computer to compare, returns nothing and the alert never fires. You see a healthy rule and no email, which looks like the alert is broken when the setting is missing. Learn says the override can go up to two days.

Two close seconds. First, using the alert on a VM that you stop on purpose every night: it will fire every time, because a stopped VM sends no heartbeat. Learn's guidance on activity log alerts says they are the type for events such as a VM restart or shutdown. If you want to know "someone stopped the VM", that is a different alert type. Second, expecting the alert on a VM that never sent a heartbeat. It is not in the table, so the query cannot see it.

## Clean up

Do the test cleanup first: start the VM again from the portal (**Start**) or with `az vm start --resource-group $RG --name $VM`. If you want it stopped to save compute cost, follow the stop step in Lab 13 after the cleanup below.

Then remove the monitoring pieces in this order. Portal:

1. **Monitor** > **Alerts** > **Alert rules**. Select `VM not sending heartbeat` and select **Delete**.
2. **Monitor** > **Data Collection Rules**. Select `dcr-azb-lab` and select **Delete**. If it warns about associations, remove them as well.
3. On the VM, open **Extensions + applications**, select `AzureMonitorWindowsAgent` and select **Uninstall** (Learn describes it on the **Extensions** tab). The VM does not need the agent without a rule.
4. **Log Analytics workspaces** > `log-azb-lab` > **Delete**. Type the name to confirm. Learn says a normal delete is a soft delete: the name stays reserved for 14 days and you can recover the workspace in that time. If you plan to repeat this lab with the same name, tick **Delete the workspace permanently** in the same dialog. That cannot be undone.

CLI:

```bash
az monitor scheduled-query delete --resource-group $RG --name "VM not sending heartbeat" --yes
az monitor data-collection rule delete --resource-group $RG --name $DCR --delete-associations true --yes
az vm extension delete --resource-group $RG --vm-name $VM --name AzureMonitorWindowsAgent
az monitor log-analytics workspace delete --resource-group $RG --workspace-name $WS --force true --yes
```

The last command deletes the workspace permanently (Learn: `--force` releases the name). Leave off `--force true` for a recoverable soft delete.

Keep for later labs:

- `ag-azb-email` and `rg-azb-core` (Lab 3).
- `rg-azb-lab` and the VM `vm-azb-win01` from Lab 12.

## Where this is used in AVD

AVD monitoring is this same pattern: a workspace, a data collection rule on the session hosts, and alerts on what lands in the tables. The AVD article on [how Azure Virtual Desktop fails](/azure-virtual-desktop/how-azure-virtual-desktop-fails/) explains that service events reach Log Analytics only after you turn on diagnostic settings on each AVD object. The full Terraform version for session hosts is in [AVD Monitoring Starter Lab with Terraform](/terraform-labs/avd-monitoring-lab/).

## Next lab

[Lab 17: Azure Policy and resource locks](/azure-basics-labs/azure-policy-locks/) adds guardrails, so a rule can stop a mistake before it happens.

## Sources

- [Create a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/quick-create-workspace)
- [Manage data retention in a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-retention-configure)
- [Azure Monitor Logs cost calculations and options](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/cost-logs)
- [Collect guest log data from virtual machines with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection)
- [Collect Windows events from virtual machine with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection-windows-events)
- [Collect performance counters from virtual machines with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection-performance)
- [Install and manage the Azure Monitor Agent](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-manage)
- [Enable VM monitoring in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/vm-enable-monitoring)
- [Create data collection rules (DCRs) using JSON](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-rule-create-edit)
- [Data collection rule (DCR) samples in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/data-collection-rule-samples)
- [Heartbeat table reference](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/heartbeat)
- [Log data ingestion time in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-ingestion-time)
- [Choose the right type of alert rule](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-types)
- [Create or edit a log search alert rule](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-log-alert-rule)
- [Delete and recover a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/delete-workspace)
- [az monitor scheduled-query](https://learn.microsoft.com/en-us/cli/azure/monitor/scheduled-query)
- [az monitor data-collection rule](https://learn.microsoft.com/en-us/cli/azure/monitor/data-collection/rule)
- [az vm identity assign](https://learn.microsoft.com/en-us/cli/azure/vm/identity)
- [Azure Monitor Agent requirements](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-requirements)
