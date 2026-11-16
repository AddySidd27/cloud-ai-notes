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

By the end of this lab you will have a Log Analytics workspace named `log-azb-lab`, your Windows VM sending data to it, a query that shows when the VM last reported, and an alert that emails you when the VM goes quiet. You test the alert by stopping the VM. Then you delete everything you built here and leave the VM stopped.

A Log Analytics workspace is a place in Azure where logs and performance data are stored, and where you search them with queries. Azure Monitor is the Azure service that collects that data and raises alerts on it. Almost everything you do to watch an Azure Virtual Desktop (AVD) environment later ends up in a workspace like this one.

## What you need

- [Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/): the action group `ag-azb-email`, with your email address already verified.
- [Windows VM with Entra sign-in](/azure-basics-labs/windows-vm-entra-sign-in/): the Windows VM `vm-azb-win01` in `rg-azb-lab`, with its system-assigned managed identity. You do not sign in to it in this lab, so you do not need the RDP rule. The VM must be running while you create the rule and read the heartbeat, and the first step tells you to start it.
- [VM size, disk and power states](/azure-basics-labs/vm-size-disk-stop-deallocate/): you use its stop (deallocate) step to test the alert.
- Time: about 45 minutes of work, plus waiting. Data takes a few minutes to arrive. The alert test takes 15 to 30 minutes.
- Cost: a Log Analytics workspace uses a pay-as-you-go price. No charges build up until data collection begins, and then you pay per GB of data you send. The `Heartbeat` table is one of the tables that is free from ingestion charges. The performance data in this lab is billed per GB, so the lab collects one counter only. Alert rules and email notifications can have their own small charges. Open [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/) and read the Log Analytics and alert rule rows for your region before you start. Delete everything the same day. The VM bills for compute while it runs, and this lab ends with it stopped.
- Which parts are optional: the CLI section is a second way to create the workspace and the data collection rule. Do the portal steps or the CLI, not both. The alert is always created in the portal.
- Role: owner of your own test subscription covers everything here. The narrower roles are Log Analytics Contributor for creating a workspace, Monitoring Contributor for creating data collection rules, and Virtual Machine Contributor for installing the agent.

## Safety first

- Use the throwaway tenant only. Read the tenant and subscription name at the top right of the portal before you change anything.
- The workspace costs money only when data goes in. Do not add more data sources than this lab says. Do not leave the lab running for weeks.
- Do not connect any other VM to this workspace.
- The alert test stops your VM. A stopped (deallocated) VM does not lose its disk. You start it again after the test, and stop it for good in "Clean up".
- If you set auto-shutdown for the VM in the Windows VM lab, the alert fires the night it runs. Delete the alert rule in "Clean up", not later.
- Do not delete `ag-azb-email`. Later labs use it.
- Deleting the workspace also deletes the data in it. That is fine here.

**State of your resources**

| | At the start | At the end |
|---|---|---|
| VM `vm-azb-win01` | Stopped (deallocated). The first step starts it. | Stopped (deallocated) |
| Rule `allow-rdp-my-ip` in `nsg-azb-vm` | Not there. You do not need it. | Not there |
| Public IP `pip-azb-win01` | Exists. It stays. | Exists |
| New in this lab | Nothing | Nothing. The alert rule, DCR, agent and workspace are deleted in "Clean up". |

## What the lab builds

![In rg-azb-lab, the data collection rule dcr-azb-lab is linked to the VM, whose agent sends data to the Log Analytics workspace. An alert rule queries the workspace every 5 minutes and, if the heartbeat stops, fires the action group in rg-azb-core, which emails you.](/img/basics/log-analytics-alert.svg)

*Source: Microsoft Learn pages listed under Sources.*

## Steps in the Azure portal

**Idea 1: three parts that work together.** The workspace stores the data. The Azure Monitor Agent is a small program that runs on the VM and sends data. A data collection rule (DCR) tells the agent what to collect and where to send it. The agent starts collecting only after the VM is linked to a DCR. That link is called an association.

### Start the VM and create the workspace

1. Sign in to the [Azure portal](https://portal.azure.com). Check the tenant name. Open **Virtual machines** > `vm-azb-win01` > **Start**. Wait until the status says **Running** (two to three minutes). The agent installs only on a running VM.
2. Search for **Log Analytics workspaces** and open it. Select **Create**.
3. Set **Subscription** to your test subscription and **Resource group** to `rg-azb-lab`.
4. Set **Name** to `log-azb-lab`. The name must be unique per resource group.
5. Set **Region** to the same region as your VM. Use the region on your notes sheet from [the account lab](/azure-basics-labs/start-azure-account-tenant-subscription/) for the whole series. The data collection rule must be in the same region as the workspace, so keeping everything in one region avoids a problem later.
6. Select **Review + Create**, then **Create**. A default pay-as-you-go pricing tier is applied and no charges accrue until data collection begins.

Retention is how many days the workspace keeps data. The default for tables in a workspace is 30 days. Leave it at 30. You can change retention per table, and you do not need to in this lab.

Check: `log-azb-lab` appears in the **Log Analytics workspaces** list with status Succeeded or similar, in `rg-azb-lab`.

### Create the data collection rule and connect the VM

**Idea 2: the DCR installs the agent for you.** Creating a DCR in the Azure portal is the recommended way to install the Azure Monitor Agent through the portal. The agent is installed automatically if it is needed, and an association is created between the DCR and each VM you select. The agent needs a managed identity on the VM (the Key Vault lab explains what that is). When you add a VM to a DCR in the portal, the default is to enable a system-assigned managed identity for it. Your VM already has one, so the portal keeps it.

7. Search for **Monitor** and open it. In the left menu, select **Data Collection Rules**, then **Create**.
8. On **Basics**, set **Rule Name** to `dcr-azb-lab`, **Subscription** to your test subscription, **Resource group** to `rg-azb-lab`, and **Region** to the same region as the workspace.
9. Set the type of data this rule is for to Windows. Your page shows one of two things. The default experience shows **Type of telemetry**: open its drop-down, read the short descriptions and choose the option for data collected from the agent on a virtual machine. Select **Help me choose** if you are unsure. The classic experience shows **Platform Type**: set it to **Windows**. Leave **Data Collection Endpoint** empty. An endpoint is needed only for some data sources. Select **Next**.
10. On **Resources**, select **Add resources** and tick your VM `vm-azb-win01`. The portal turns on a system-assigned managed identity for it by default. Keep that default. Select **Next**.
11. On **Collect and deliver**, select **Add new dataflow**. (The classic experience calls it **Add data source**.) Add one data source only:
    - Set **Data source type** to **Performance Counters**. Choose **Custom** and enter `\Processor(_Total)\% Processor Time`. If the page shows a sample rate, set it to 60 seconds. This is the same counter as in the CLI section.
    - Set the destination to **Azure Monitor Logs** and select `log-azb-lab`. Performance counters land in the **Perf** table. Add the workspace once only: a second destination of the same type sends the data twice and raises cost.
12. Select **Review + create**, then **Create**.

Why so little? `Perf` data is billed per GB, and the alert does not use it. The heartbeat that the alert uses is a separate table that the agent writes by itself once the VM is linked to a rule.

13. Wait. It can take up to 5 minutes for data to reach the workspace after you create a DCR, and several minutes after installation for the first heartbeat.

Check: open your VM, then **Settings** > **Extensions + applications**. `AzureMonitorWindowsAgent` should show **Provisioning succeeded**. Open the DCR `dcr-azb-lab`, then **Configuration** > **Resources**: your VM is listed. If the extension shows a failure, check that the VM is **Running**.

### Read the heartbeat with a query

The Azure Monitor Agent sends a small record to a table called `Heartbeat` about once a minute to show it is alive.

14. Open the workspace `log-azb-lab`, then select **Logs** in the left menu. If a window with example queries opens, close it.
15. Queries in Azure Monitor use the Kusto Query Language (KQL). Copy and paste; you do not need to learn it now. Paste this query and select **Run**:

    ```kusto
    Heartbeat
    | summarize arg_max(TimeGenerated, *) by Computer
    ```

    `arg_max(TimeGenerated, *)` means: for each computer, keep the whole row with the newest `TimeGenerated`. `Computer` is the computer name and `TimeGenerated` is when the record was created.
16. Look at the result. You should see one row for your VM, like this (the values differ):

    | Computer | TimeGenerated | Category |
    |---|---|---|
    | vm-azb-win01 | a time within the last few minutes | Azure Monitor Agent |

    The `Computer` value is the Windows computer name, which can differ from the VM name in the portal.
17. If the table does not exist or the result is empty, that is normal for the first 5 to 10 minutes. Wait and run it again.

Check: one row for your VM, with a recent `TimeGenerated`. Also run `Perf | take 10`. It should show rows after a few minutes.

### Create the alert

**Idea 3: an alert cannot easily see "nothing".** Log alerts are slow and can miss silence, so a metric alert is often a better fit when you must avoid false alarms. This lab still uses a log alert because the workspace is the point. The alert looks back over a long period, finds each computer's newest heartbeat and checks how old it is. It cannot catch a VM that never reported, because that VM is not in the table.

18. In the portal, select **Monitor**, then **Alerts** in the left pane, then **Create** > **Alert rule**. On the **Select a resource** pane, set the scope to your workspace `log-azb-lab` (filter by resource type if the list is long) and select **Apply**.
19. On the **Condition** tab, select the **Signal name** field and choose **Custom log search**.
20. In the **Logs** pane, paste this query:

    ```kusto
    Heartbeat
    | summarize LastHeartbeat = max(TimeGenerated) by Computer
    | where LastHeartbeat < ago(10m)
    ```

    The query uses `ago()` with a timespan such as `10m`. This query returns a row for each computer whose newest heartbeat is older than 10 minutes. It returns nothing while the VM reports.
21. Select **Run**, then **Continue Editing Alert**. While the VM is running the result is empty. That is correct.
22. In **Measurement**, set **Measure** to **Table rows** and **Aggregation type** to **Count**. If the page shows **Aggregation granularity**, set it to 5 minutes. In **Alert logic**, set **Operator** to **Greater than**, **Threshold value** to `0`, and **Frequency of evaluation** to `5 minutes`.
23. Still on the **Condition** tab, scroll down to **Advanced options** and set **Override query time range** to 1 day (the maximum is two days). Without it, the query would only look at the last few minutes and would never find a heartbeat older than 10 minutes. Do not skip this step.
24. On the **Actions** tab, select **Select action groups** and pick `ag-azb-email`, the action group you created in the budget lab.
25. On the **Details** tab, set **Subscription** and **Resource group** to your test subscription and `rg-azb-lab`. Set **Severity** to **2 - Warning** (or any level you like). Set **Alert rule name** to `VM not sending heartbeat`. Set **Region** to your lab region.
26. In **Advanced options** on this tab, keep **Enable upon creation** ticked. Tick **Automatically resolve alerts** so that the alert closes by itself when the heartbeat returns. It resolves when the condition is no longer met for a few evaluation periods.
27. Select **Review + create**, then **Create**.

Check: the rule `VM not sending heartbeat` appears under **Monitor** > **Alerts** > **Alert rules**, with status Enabled.

### Test it by stopping the VM

28. Go to your VM and select **Stop**, the same way as in the VM size lab. Wait for the status to read **Stopped (deallocated)**. Note the time.
29. Wait 15 to 30 minutes. You cannot speed it up. The query only returns the VM after its newest heartbeat is more than 10 minutes old, and the rule runs every 5 minutes, so it can take up to 5 more minutes before a run sees that. The email then follows. While you wait, run the heartbeat query from the earlier section again and watch the newest `TimeGenerated` stop moving. That is the signal the alert is looking for. If nothing arrives after 30 minutes, check your spam folder, then read "The most common mistake".
30. When the email arrives, open the alert in **Monitor** > **Alerts**. You should see the alert with the rule name and the VM's computer name.
31. Select **Start** on the VM. After a few minutes the heartbeat returns. With **Automatically resolve alerts** on, the alert should resolve itself. Give it some time, because it needs more than one evaluation period.

Check: you got an email from the `ag-azb-email` action group after stopping the VM, and the alert shows as resolved after you started the VM again. Now go to "Clean up".

## Steps with the Azure CLI

Optional. The portal steps above are the main path. Skip this section if you used them, because the names below match the portal steps and would clash. Start the VM first (the first portal step), because the agent installs only on a running VM.

Run these in Cloud Shell (Bash). Check the tenant and subscription first. The CLI covers the workspace, the rule, the agent and the association. It does not cover the alert: the alert needs the **Override query time range** setting, so create the alert in the portal.

Set the variables. If Cloud Shell restarts, set them again before you carry on:

```bash
az account show --query "{tenant:tenantId, subscription:name}" -o table

RG="rg-azb-lab"
VM="vm-azb-win01"
WS="log-azb-lab"
DCR="dcr-azb-lab"
LOCATION=$(az vm show --resource-group "$RG" --name "$VM" --query location -o tsv)   # same region as the VM
echo "$LOCATION"
```

Create the workspace. The default retention is 30 days and the default pricing tier is `PerGB2018`, so you do not set either:

```bash
az monitor log-analytics workspace create --resource-group $RG --workspace-name $WS --location $LOCATION
WS_ID=$(az monitor log-analytics workspace show --resource-group $RG --workspace-name $WS --query id --output tsv)
echo $WS_ID
```

Check: `az monitor log-analytics workspace show` prints the workspace and `$WS_ID` is not empty.

Create the rule. A DCR created from the CLI needs a JSON file. This one uses one performance counter once a minute, sent to the workspace. The `kind` line sets the platform to Windows. The first command writes the file, the second puts your workspace ID and region in it, the third stops you if a placeholder is left:

```bash
cat > dcr-azb-lab.json <<'EOF'
{
  "location": "LOCATION_HERE",
  "kind": "Windows",
  "properties": {
    "dataSources": {
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
grep -E "LOCATION_HERE|WORKSPACE_ID_HERE" dcr-azb-lab.json && echo "STOP: placeholders left"
az monitor data-collection rule create --resource-group $RG --location $LOCATION --name $DCR --rule-file dcr-azb-lab.json
DCR_ID=$(az monitor data-collection rule show --resource-group $RG --name $DCR --query id --output tsv)
```

The first run of `az monitor data-collection rule` may ask to install an extension. Say yes. The CLI gives a generic error if the JSON is wrong. If the command fails, look at the file again.

Check: `az monitor data-collection rule show --resource-group $RG --name $DCR` prints the rule and `$DCR_ID` is not empty.

Install the agent and link the rule. A CLI install does not create a DCR, so you create the association yourself. The VM already has a system-assigned identity, so the commands below do not turn it on. They check that it is there, install the agent and link the rule:

```bash
az vm show --resource-group $RG --name $VM --query identity
VM_ID=$(az vm show --resource-group $RG --name $VM --query id --output tsv)
az vm extension set --name AzureMonitorWindowsAgent --publisher Microsoft.Azure.Monitor --ids $VM_ID --enable-auto-upgrade true
az monitor data-collection rule association create --name dcra-azb-lab --rule-id $DCR_ID --resource $VM_ID
```

The first command should show a `SystemAssigned` identity. If it shows nothing, run `az vm identity assign --resource-group $RG --name $VM` (this turns it on for an existing VM) and then carry on.

Check: `az vm extension list --resource-group $RG --vm-name $VM --output table` lists `AzureMonitorWindowsAgent` with `Succeeded`. After a few minutes, run the `Heartbeat` query in the portal, in the workspace's **Logs** page. Then create the alert in the portal as in "Create the alert".

## Terraform

No Terraform in this lab. The same pieces (workspace, data collection rule, Azure Monitor Agent extension, association, action group and a heartbeat alert) are written as Terraform for AVD session hosts in [AVD Monitoring Starter Lab with Terraform](/terraform-labs/avd-monitoring-lab/). Come back to it after the [Terraform basics lab](/azure-basics-labs/terraform-basics/).

## Check that it works

- The workspace `log-azb-lab` exists in `rg-azb-lab`.
- The VM shows `AzureMonitorWindowsAgent` as Provisioning succeeded, and `dcr-azb-lab` lists the VM under Resources.
- `Heartbeat | summarize arg_max(TimeGenerated, *) by Computer` returns one row for the VM with a recent `TimeGenerated`.
- The alert query returns no rows while the VM is running.
- After the VM was stopped, an email from `ag-azb-email` arrived, and the alert resolved after the VM was started again.

## The most common mistake

Forgetting **Override query time range**. Without it, the alert query only looks at a short window. A stopped VM has no rows in that window, so the query finds no computer to compare, returns nothing and the alert never fires. You see a healthy rule and no email, which looks like the alert is broken when the setting is missing.

Two close seconds. First, using the alert on a VM that you stop on purpose every night: it will fire every time, because a stopped VM sends no heartbeat. If you want to know "someone stopped the VM", that is a different alert type: an activity log alert. Second, expecting the alert on a VM that never sent a heartbeat. It is not in the table, so the query cannot see it.

## Clean up

Order matters. First delete the monitoring pieces, then stop the VM. Do not skip the last step.

1. Start the VM again if it is stopped (the alert test is over). In the portal: VM > **Start**. You need it running so the agent can be removed.
2. Portal, in this order:
   1. **Monitor** > **Alerts** > **Alert rules**. Select `VM not sending heartbeat` and select **Delete**.
   2. **Monitor** > **Data Collection Rules**. Select `dcr-azb-lab` and select **Delete**. If it warns about associations, remove them as well.
   3. On the VM, open **Extensions + applications**, select `AzureMonitorWindowsAgent` and select **Uninstall**. The VM does not need the agent without a rule.
   4. **Log Analytics workspaces** > `log-azb-lab` > **Delete**. Type the name to confirm. A normal delete is a soft delete: the name stays reserved for 14 days and you can recover the workspace in that time. If you plan to repeat this lab with the same name, tick **Delete the workspace permanently** in the same dialog. That cannot be undone.
3. Or the same in the CLI. Set the variables from the CLI section again first (`RG`, `VM`, `WS`, `DCR`):

   ```bash
   az monitor scheduled-query delete --resource-group $RG --name "VM not sending heartbeat" --yes
   az monitor data-collection rule delete --resource-group $RG --name $DCR --delete-associations true --yes
   az vm extension delete --resource-group $RG --vm-name $VM --name AzureMonitorWindowsAgent
   az monitor log-analytics workspace delete --resource-group $RG --workspace-name $WS --force true --yes
   ```

   The last command deletes the workspace permanently (`--force` releases the name). Leave off `--force true` for a recoverable soft delete.
4. Stop the VM: **Virtual machines** > `vm-azb-win01` > **Stop**. Read the status. It must say **Stopped (deallocated)**.

End state: VM Stopped (deallocated), no `allow-rdp-my-ip` rule. The workspace, the data collection rule, the agent and the alert rule are deleted. The action group `ag-azb-email` still exists.

The public IP `pip-azb-win01` is still there. Keep for later labs: `ag-azb-email` and `rg-azb-core`, and `rg-azb-lab` with the VM `vm-azb-win01`.

## Where this is used in AVD

AVD monitoring is this same pattern: a workspace, a data collection rule on the session hosts, and alerts on what lands in the tables. The AVD article on [how Azure Virtual Desktop fails](/azure-virtual-desktop/how-azure-virtual-desktop-fails/) explains that service events reach Log Analytics only after you turn on diagnostic settings on each AVD object. The full Terraform version for session hosts is in [AVD Monitoring Starter Lab with Terraform](/terraform-labs/avd-monitoring-lab/).

## Next lab

[Azure Policy and resource locks](/azure-basics-labs/azure-policy-locks/) adds guardrails, so a rule can stop a mistake before it happens.

## Sources

- [Create a Log Analytics workspace](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/quick-create-workspace)
- [Collect guest log data from virtual machines with Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection)
- [Create or edit a log search alert rule](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-log-alert-rule)
