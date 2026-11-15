---
title: "AVD Monitoring Starter Lab with Terraform: Log Analytics, Insights Data and One Alert"
seoTitle: "Azure Virtual Desktop Monitoring with Terraform: Log Analytics, Azure Monitor Agent, Alert"
layout: post.njk
permalink: "/terraform-labs/avd-monitoring-lab/"
order: 304
tags: [terraform-lab]
deck: "A Terraform lab that adds monitoring to the AVD quick lab: a Log Analytics workspace, service logs, performance counters and Windows events from the session hosts, and one email alert."
description: "A walk through a Terraform lab that sends Azure Virtual Desktop logs, session host performance counters and Windows events to a Log Analytics workspace, so Azure Virtual Desktop Insights has data, and adds an alert for a session host that stops reporting."
---

When something goes wrong in a virtual desktop environment, you need data to find out why. Azure Virtual Desktop (AVD) can send its logs and the session hosts' performance data to one place, where you can query them and build alerts on them. This article walks through a Terraform lab that sets that up for the [AVD quick lab](/terraform-labs/avd-quick-lab/).

Below is what the code does, how Microsoft describes the features it uses, and a test plan. Run `terraform validate` and `terraform plan` before you apply it.

## Key terms

| Term | Meaning |
|---|---|
| Log Analytics workspace | A place in Azure where logs and performance data are stored and queried. |
| Diagnostic setting | A setting on an Azure resource that sends its logs to a place such as a Log Analytics workspace. Each resource needs its own. |
| Resource log category | One kind of log that a resource can send, such as errors or connections. |
| Azure Monitor Agent | A program that runs on a VM and sends its performance data and event logs to Azure. |
| Data collection rule | A rule that says what the Azure Monitor Agent collects and where it sends the data. |
| Performance counter | A Windows measurement, such as processor use or user input delay. |
| Windows event log | The log where Windows and apps record events and errors. |
| Managed identity | An identity that Azure gives to a resource, so it can sign in to other Azure services without a password. |
| Azure Virtual Desktop Insights | A dashboard in the Azure portal, built on Azure Monitor Workbooks, that shows the health and use of an AVD environment. |
| Alert rule | A rule that runs a query on a schedule and fires when the query finds a result. |
| Action group | A list of people or actions that an alert notifies, such as an email address. |
| Session host, host pool | A session host is a VM that runs users' desktops. A host pool is a group of session hosts that users share. |
| FSLogix | Software that keeps each user's profile on a file share, so it follows them to any host. |
| Stream | The name of a kind of data in a data collection rule, such as `Microsoft-Perf`. It decides which Log Analytics table receives the data. |
| Heartbeat | A record that the Azure Monitor Agent writes to the `Heartbeat` table at regular intervals to show that it is running. |
| Deallocated | A VM that Azure has shut down and released the hardware for, so Azure no longer charges for its compute. |
| Precondition | A check in the Terraform code that stops the plan with a message if a condition is false. |
| Terraform | A tool that creates cloud resources from code files. |

## What the lab builds

![The host pool, AVD workspace and application group send logs to a Log Analytics workspace through diagnostic settings. A data collection rule, applied to each session host with the Azure Monitor Agent, sends performance counters and Windows events to the same workspace. An alert rule on the workspace checks every 15 minutes whether a session host has stopped sending heartbeats and notifies an action group that sends an email.](/img/avd/AVD-Terraform-Monitoring-Lab.svg)

*Source: the lab's Terraform code and the pages [Enable Insights to monitor Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights) and [Send diagnostic data to Log Analytics for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

The lab does not create any AVD resource. It reads the resources that the quick lab made (the resource group, host pool, workspace, application group and two session hosts) and adds monitoring to them. Azure Virtual Desktop Insights needs three kinds of data, and the lab covers all three:

1. **Diagnostics from the AVD environment.** The host pool, the AVD workspace and the application group send their logs to Log Analytics.
2. **Performance counters from the session hosts.**
3. **Windows event logs from the session hosts.**

The documentation also says to use a Log Analytics workspace just for your AVD session hosts, so that only AVD data is collected. The lab creates its own for that reason.

## What it costs

Log Analytics charges for the data you send to it. The documentation's page [Estimate Azure Virtual Desktop monitoring costs](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights-costs) says performance counters are probably your largest source of data, and gives an estimate of roughly 90 megabytes of counter data per VM per day for a light workload. That is the documentation's example, not a measurement of this lab. The page also suggests lowering the retention period and setting limits on how much data can be ingested. The lab does both: `retention_in_days` defaults to 30, the lowest value the provider accepts, and `daily_quota_gb` caps daily ingestion at 1 GB. Change them if they do not fit.

## Before you start

- The [AVD quick lab](/terraform-labs/avd-quick-lab/) deployed with its default names (`rg-avd-dev`, `avd-hp-avd-dev`, `avd-ws-avd-dev`, `avd-dag-avd-dev`, `avdsh-01` and `avdsh-02`). If your names differ, change the matching settings.
- Both session hosts powered on when you apply, because the lab installs an agent on them. If you also use the [autoscale lab](/terraform-labs/avd-autoscale-cost-lab/), start the hosts in the portal first.
- Permissions to create resources in the resource group. Installing the Azure Monitor Agent needs the Virtual Machine Contributor role on the VMs. Contributor on the resource group covers both.
- An email address for the alert.
- The Azure CLI, Git and Terraform 1.9 or newer.
- The people who will look at the dashboard need the Desktop Virtualization Reader role on the resource group and the Log Analytics Reader role on the workspace. These are the minimum roles.

## The code

You need five files in one folder. The first two are the same as in the [budget lab](/terraform-labs/avd-budget-alert-lab/).

`versions.tf`:

```hcl
terraform {
  required_version = ">= 1.9.0, < 2.0.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.81.0"
    }
  }
}
```

`providers.tf`:

```hcl
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
```

### The settings

`variables.tf` has these settings. All of them except `subscription_id` and `alert_email` have defaults that match the quick lab.

| Setting | Default | Meaning |
|---|---|---|
| `subscription_id` | none | The subscription that contains the quick lab. |
| `alert_email` | none | The address that receives the alert. |
| `resource_group_name` | `rg-avd-dev` | The quick lab's resource group. The monitoring resources go here too. |
| `host_pool_name`, `workspace_name`, `application_group_name` | `avd-hp-avd-dev`, `avd-ws-avd-dev`, `avd-dag-avd-dev` | The existing AVD resources. |
| `session_host_names` | `["avdsh-01", "avdsh-02"]` | The existing session host VMs. |
| `log_analytics_workspace_name` | `log-avd-dev` | The workspace to create. |
| `retention_in_days` | `30` | How long to keep data (30 to 730). |
| `daily_quota_gb` | `1` | The daily ingestion cap. `-1` means no cap. |
| `host_pool_log_categories` | Checkpoint, Error, Management, Connection, HostRegistration, AgentHealthStatus | Logs to send from the host pool. |
| `workspace_log_categories` | Checkpoint, Error, Management, Feed | Logs to send from the AVD workspace. |
| `application_group_log_categories` | Checkpoint, Error, Management | Logs to send from the application group. |

The full file:

```hcl
variable "subscription_id" {
  description = "ID of the Azure subscription that contains the AVD quick lab."
  type        = string
}

variable "resource_group_name" {
  description = "Resource group of the existing AVD quick lab. The monitoring resources are created here too."
  type        = string
  default     = "rg-avd-dev"
}

variable "host_pool_name" {
  description = "Name of the existing host pool."
  type        = string
  default     = "avd-hp-avd-dev"
}

variable "workspace_name" {
  description = "Name of the existing AVD workspace (not a Log Analytics workspace)."
  type        = string
  default     = "avd-ws-avd-dev"
}

variable "application_group_name" {
  description = "Name of the existing desktop application group."
  type        = string
  default     = "avd-dag-avd-dev"
}

variable "session_host_names" {
  description = "Names of the existing session host VMs."
  type        = list(string)
  default     = ["avdsh-01", "avdsh-02"]
}

variable "log_analytics_workspace_name" {
  description = "Name of the Log Analytics workspace to create."
  type        = string
  default     = "log-avd-dev"
}

variable "retention_in_days" {
  description = "How long the workspace keeps data, from 30 to 730 days."
  type        = number
  default     = 30

  validation {
    condition     = var.retention_in_days >= 30 && var.retention_in_days <= 730
    error_message = "retention_in_days must be between 30 and 730."
  }
}

variable "daily_quota_gb" {
  description = "Daily ingestion cap in GB. Use -1 for no cap."
  type        = number
  default     = 1
}

variable "alert_email" {
  description = "Email address that receives the alert."
  type        = string
}

variable "host_pool_log_categories" {
  description = "Resource log categories to send from the host pool. These are the categories AVD Insights uses for a host pool."
  type        = list(string)
  default = [
    "Checkpoint",
    "Error",
    "Management",
    "Connection",
    "HostRegistration",
    "AgentHealthStatus",
  ]
}

variable "workspace_log_categories" {
  description = "Resource log categories to send from the AVD workspace."
  type        = list(string)
  default     = ["Checkpoint", "Error", "Management", "Feed"]
}

variable "application_group_log_categories" {
  description = "Resource log categories to send from the application group."
  type        = list(string)
  default     = ["Checkpoint", "Error", "Management"]
}
```

### Reading the existing lab and creating the workspace

The first part of `main.tf` reads the quick lab's resources with `data` blocks. A `data` block only looks a resource up, so Terraform never changes the quick lab. It then creates the Log Analytics workspace.

```hcl
data "azurerm_resource_group" "lab" {
  name = var.resource_group_name
}

data "azurerm_virtual_desktop_host_pool" "lab" {
  name                = var.host_pool_name
  resource_group_name = data.azurerm_resource_group.lab.name
}

data "azurerm_virtual_desktop_workspace" "lab" {
  name                = var.workspace_name
  resource_group_name = data.azurerm_resource_group.lab.name
}

data "azurerm_virtual_desktop_application_group" "lab" {
  name                = var.application_group_name
  resource_group_name = data.azurerm_resource_group.lab.name
}

data "azurerm_virtual_machine" "session_host" {
  for_each = toset(var.session_host_names)

  name                = each.value
  resource_group_name = data.azurerm_resource_group.lab.name
}

# The categories that each resource offers. Used to stop the plan early with a
# clear message if a category name is wrong.
data "azurerm_monitor_diagnostic_categories" "host_pool" {
  resource_id = data.azurerm_virtual_desktop_host_pool.lab.id
}

data "azurerm_monitor_diagnostic_categories" "workspace" {
  resource_id = data.azurerm_virtual_desktop_workspace.lab.id
}

data "azurerm_monitor_diagnostic_categories" "application_group" {
  resource_id = data.azurerm_virtual_desktop_application_group.lab.id
}

resource "azurerm_log_analytics_workspace" "avd" {
  name                = var.log_analytics_workspace_name
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
  sku                 = "PerGB2018"
  retention_in_days   = var.retention_in_days
  daily_quota_gb      = var.daily_quota_gb
}
```

The three `azurerm_monitor_diagnostic_categories` blocks ask Azure which log categories each resource offers. The next part uses them to stop with a clear message if a category name in your settings does not exist.

### 1. Service diagnostics

Each AVD object needs its own diagnostic setting. The documentation's page on [sending diagnostics to Log Analytics](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics) says to enable diagnostics for each object you want to monitor, and that data is available only from the time diagnostics is enabled. It can take a few hours after the first setup.

```hcl
# 1. Service diagnostics: host pool, workspace and application group send their
# logs to Log Analytics. Each object needs its own diagnostic setting.
resource "azurerm_monitor_diagnostic_setting" "host_pool" {
  name                       = "send-to-log-analytics"
  target_resource_id         = data.azurerm_virtual_desktop_host_pool.lab.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.avd.id

  dynamic "enabled_log" {
    for_each = toset(var.host_pool_log_categories)

    content {
      category = enabled_log.value
    }
  }

  lifecycle {
    precondition {
      condition     = alltrue([for c in var.host_pool_log_categories : contains(data.azurerm_monitor_diagnostic_categories.host_pool.log_category_types, c)])
      error_message = "A category in host_pool_log_categories is not offered by this host pool. Available: ${join(", ", data.azurerm_monitor_diagnostic_categories.host_pool.log_category_types)}."
    }
  }
}

resource "azurerm_monitor_diagnostic_setting" "workspace" {
  name                       = "send-to-log-analytics"
  target_resource_id         = data.azurerm_virtual_desktop_workspace.lab.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.avd.id

  dynamic "enabled_log" {
    for_each = toset(var.workspace_log_categories)

    content {
      category = enabled_log.value
    }
  }

  lifecycle {
    precondition {
      condition     = alltrue([for c in var.workspace_log_categories : contains(data.azurerm_monitor_diagnostic_categories.workspace.log_category_types, c)])
      error_message = "A category in workspace_log_categories is not offered by this workspace. Available: ${join(", ", data.azurerm_monitor_diagnostic_categories.workspace.log_category_types)}."
    }
  }
}

resource "azurerm_monitor_diagnostic_setting" "application_group" {
  name                       = "send-to-log-analytics"
  target_resource_id         = data.azurerm_virtual_desktop_application_group.lab.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.avd.id

  dynamic "enabled_log" {
    for_each = toset(var.application_group_log_categories)

    content {
      category = enabled_log.value
    }
  }

  lifecycle {
    precondition {
      condition     = alltrue([for c in var.application_group_log_categories : contains(data.azurerm_monitor_diagnostic_categories.application_group.log_category_types, c)])
      error_message = "A category in application_group_log_categories is not offered by this application group. Available: ${join(", ", data.azurerm_monitor_diagnostic_categories.application_group.log_category_types)}."
    }
  }
}
```

The `dynamic "enabled_log"` block creates one `enabled_log` for each category in the list. The `precondition` checks that every category you listed exists on that resource, and prints the available ones if it does not. The category names match the documentation's supported-logs pages for host pools, workspaces and application groups. The documentation's Insights page also lists Feed for the host pool, but that category exists only on the AVD workspace, so the lab leaves it out of the host pool list. The precondition is there to catch a wrong category name at plan time.

### 2. Session host data

A data collection rule says what to collect from the session hosts. This one collects the 20 performance counters that are listed in the [Azure Virtual Desktop Insights glossary](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights-glossary#performance-counters) and its [monitoring costs page](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights-costs), at the sample intervals Microsoft gives (30 seconds for most, 60 seconds for the rest), and the Windows event logs that are the Insights defaults.

```hcl
# 2. Session host data: a data collection rule says what to collect from the
# VMs (performance counters and Windows events) and where to send it.
resource "azurerm_monitor_data_collection_rule" "session_hosts" {
  name                = "dcr-avd-session-hosts"
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
  kind                = "Windows"
  description         = "Performance counters and Windows events for AVD Insights."

  destinations {
    log_analytics {
      name                  = "avd-log-analytics"
      workspace_resource_id = azurerm_log_analytics_workspace.avd.id
    }
  }

  data_flow {
    streams      = ["Microsoft-Perf", "Microsoft-Event"]
    destinations = ["avd-log-analytics"]
  }

  data_sources {
    performance_counter {
      name                          = "avd-counters-30s"
      streams                       = ["Microsoft-Perf"]
      sampling_frequency_in_seconds = 30
      counter_specifiers = [
        "\\LogicalDisk(C:)\\Avg. Disk Queue Length",
        "\\LogicalDisk(C:)\\Current Disk Queue Length",
        "\\Memory(*)\\Available Mbytes",
        "\\Memory(*)\\Page Faults/sec",
        "\\Memory(*)\\Pages/sec",
        "\\Memory(*)\\% Committed Bytes In Use",
        "\\PhysicalDisk(*)\\Avg. Disk Queue Length",
        "\\PhysicalDisk(*)\\Avg. Disk sec/Read",
        "\\PhysicalDisk(*)\\Avg. Disk sec/Transfer",
        "\\PhysicalDisk(*)\\Avg. Disk sec/Write",
        "\\Processor Information(_Total)\\% Processor Time",
        "\\User Input Delay per Process(*)\\Max Input Delay",
        "\\User Input Delay per Session(*)\\Max Input Delay",
        "\\RemoteFX Network(*)\\Current TCP RTT",
        "\\RemoteFX Network(*)\\Current UDP Bandwidth",
      ]
    }

    performance_counter {
      name                          = "avd-counters-60s"
      streams                       = ["Microsoft-Perf"]
      sampling_frequency_in_seconds = 60
      counter_specifiers = [
        "\\LogicalDisk(C:)\\% Free Space",
        "\\LogicalDisk(C:)\\Avg. Disk sec/Transfer",
        "\\Terminal Services(*)\\Active Sessions",
        "\\Terminal Services(*)\\Inactive Sessions",
        "\\Terminal Services(*)\\Total Sessions",
      ]
    }

    windows_event_log {
      name    = "avd-events"
      streams = ["Microsoft-Event"]
      x_path_queries = [
        "Application!*[System[(Level=2 or Level=3)]]",
        "System!*[System[(Level=2 or Level=3)]]",
        "Microsoft-Windows-TerminalServices-RemoteConnectionManager/Admin!*[System[(Level=2 or Level=3 or Level=4 or Level=0)]]",
        "Microsoft-Windows-TerminalServices-LocalSessionManager/Operational!*[System[(Level=2 or Level=3 or Level=4 or Level=0)]]",
        "Microsoft-FSLogix-Apps/Operational!*[System[(Level=2 or Level=3 or Level=4 or Level=0)]]",
        "Microsoft-FSLogix-Apps/Admin!*[System[(Level=2 or Level=3 or Level=4 or Level=0)]]",
      ]
    }
  }
}
```

The two streams, `Microsoft-Perf` and `Microsoft-Event`, decide which tables in Log Analytics the data goes into. The first `performance_counter` block holds the 30-second counters and the second holds the 60-second counters. The Windows event queries keep only errors, warnings and, for the Remote Desktop and FSLogix logs, informational events. The FSLogix logs exist only if FSLogix is installed, which the quick lab does.

The configuration workbook in Insights creates its own data collection rule. If you open the workbook after applying this lab, it checks the configuration, and it may report items as missing if this lab's rule differs from what it expects. Treat that report as the check on this part of the lab.

### 3. The agent and the association

Two things must exist before a VM sends data. The Azure Monitor Agent must be installed, and the VM must be associated with the data collection rule. The documentation describes the same two steps for session hosts.

```hcl
# 3. The Azure Monitor Agent runs on each session host. It uses the VM's
# system-assigned managed identity, which the quick lab already creates.
resource "azurerm_virtual_machine_extension" "azure_monitor_agent" {
  for_each = data.azurerm_virtual_machine.session_host

  name                       = "AzureMonitorWindowsAgent"
  virtual_machine_id         = each.value.id
  publisher                  = "Microsoft.Azure.Monitor"
  type                       = "AzureMonitorWindowsAgent"
  type_handler_version       = "1.0"
  auto_upgrade_minor_version = true
  automatic_upgrade_enabled  = true
}

# The association connects each VM to the data collection rule. The agent
# starts collecting when both the agent and the association exist.
resource "azurerm_monitor_data_collection_rule_association" "session_host" {
  for_each = data.azurerm_virtual_machine.session_host

  name                    = "dcra-${each.key}"
  target_resource_id      = each.value.id
  data_collection_rule_id = azurerm_monitor_data_collection_rule.session_hosts.id

  depends_on = [azurerm_virtual_machine_extension.azure_monitor_agent]
}
```

The agent needs a managed identity on the VM. The quick lab already gives each session host a system-assigned managed identity, so the extension needs no extra settings. The extension uses automatic upgrades, so Azure updates the agent for you. The `depends_on` makes Terraform install the agent before it creates the association.

### 4. One alert

The last part creates an action group, which holds your email address, and an alert rule that uses it.

```hcl
# 4. One alert: a session host that has stopped sending heartbeats.
resource "azurerm_monitor_action_group" "alerts" {
  name                = "ag-avd-monitoring"
  resource_group_name = data.azurerm_resource_group.lab.name
  short_name          = "avdmon"

  email_receiver {
    name                    = "avd-admin"
    email_address           = var.alert_email
    use_common_alert_schema = true
  }
}

resource "azurerm_monitor_scheduled_query_rules_alert_v2" "host_stopped_reporting" {
  name                      = "alert-avd-host-stopped-reporting"
  display_name              = "AVD session host stopped reporting"
  description               = "A session host sent heartbeats in the last day but none in the last 15 minutes."
  location                  = data.azurerm_resource_group.lab.location
  resource_group_name       = data.azurerm_resource_group.lab.name
  scopes                    = [azurerm_log_analytics_workspace.avd.id]
  severity                  = 2
  evaluation_frequency      = "PT15M"
  window_duration           = "PT30M"
  query_time_range_override = "P1D"
  enabled                   = true
  auto_mitigation_enabled   = true

  criteria {
    query = <<-QUERY
      Heartbeat
      | where Category == "Azure Monitor Agent"
      | summarize LastHeartbeat = max(TimeGenerated) by Computer
      | where LastHeartbeat < ago(15m)
    QUERY

    time_aggregation_method = "Count"
    operator                = "GreaterThan"
    threshold               = 0

    failing_periods {
      minimum_failing_periods_to_trigger_alert = 1
      number_of_evaluation_periods             = 1
    }
  }

  action {
    action_groups = [azurerm_monitor_action_group.alerts.id]
  }

  depends_on = [azurerm_monitor_data_collection_rule_association.session_host]
}
```

The agent sends heartbeats regularly. The query looks back one day (`query_time_range_override`), finds the newest heartbeat for each VM, and returns the VMs whose newest heartbeat is older than 15 minutes. If it returns any row, the alert fires and the action group emails you. The alert is checked every 15 minutes.

Two limits to know about:

- **It also fires for a VM that is deallocated on purpose.** If you use the autoscale lab, the hosts that Autoscale turns off will stop sending heartbeats and trigger this alert. The query looks back one day, so the alert stays active for up to a day after the host goes off. `auto_mitigation_enabled = true` makes the alert resolve itself when the condition clears, instead of staying open. Either skip this alert if you use Autoscale, or add a filter to the query for the VMs you care about.
- **Log alerts are not ideal for missing data.** Log search alerts are less effective at detecting a lack of data, such as a missing heartbeat, because logs arrive with some delay, and it suggests metric alerts for this. This lab uses a log alert to stay inside the Log Analytics workspace. A host that never sent a heartbeat, for example because the agent failed to install, is never in the `Heartbeat` table, so the query cannot flag it.
- **It watches the agent, not the user experience.** A host can send heartbeats and still have a broken AVD agent. For that, use the AVD health data in the `WVDAgentHealthStatus` table, which the documentation describes as the health status of the Azure Virtual Desktop agent. The alert does not use it, because the documentation does not say when it reports a host that is off.

`outputs.tf`:

```hcl
output "log_analytics_workspace_id" {
  description = "Resource ID of the Log Analytics workspace."
  value       = azurerm_log_analytics_workspace.avd.id
}

output "data_collection_rule_id" {
  description = "Resource ID of the data collection rule."
  value       = azurerm_monitor_data_collection_rule.session_hosts.id
}

output "monitored_session_hosts" {
  description = "Session hosts that have the Azure Monitor Agent and the data collection rule."
  value       = sort(keys(data.azurerm_virtual_machine.session_host))
}
```

## Run it

1. **Create the folder and the files** above, and copy the example values into `terraform.tfvars`:

   ```hcl
   subscription_id = "00000000-0000-0000-0000-000000000000"
   alert_email     = "you@example.com"

   # Optional. These are the defaults, which match the AVD quick lab.
   # resource_group_name          = "rg-avd-dev"
   # host_pool_name               = "avd-hp-avd-dev"
   # workspace_name               = "avd-ws-avd-dev"
   # application_group_name       = "avd-dag-avd-dev"
   # session_host_names           = ["avdsh-01", "avdsh-02"]
   # log_analytics_workspace_name = "log-avd-dev"
   # retention_in_days            = 30
   # daily_quota_gb               = 1
   ```

2. **Keep `terraform.tfvars` out of Git.** Add a `.gitignore` file that lists `*.tfvars` and `.terraform/`, and keep `terraform.tfstate` out of Git too.
3. **Sign in and initialize.** Run `az login`, then `terraform init`.
4. **Check and plan.** Run `terraform validate`, then `terraform plan -out main.tfplan`. The plan should show new resources only: the workspace, three diagnostic settings, the data collection rule, two extensions, two associations, the action group and the alert rule.
5. **Apply.** Run `terraform apply main.tfplan`.

## Check that it works

1. **Diagnostic settings.** In the portal, open the host pool, the AVD workspace and the application group. Under Diagnostic settings, each should show a setting that sends to `log-avd-dev`.
2. **The agent.** For each VM, open Extensions + applications. `AzureMonitorWindowsAgent` should show Provisioning succeeded.
3. **Heartbeats.** In the Log Analytics workspace, open Logs and run this query from the documentation. Both hosts should appear within a few minutes of the agent starting. The `Computer` column shows the Windows computer name, which is `avdsh01` and `avdsh02` (no hyphen), not the VM name in the portal:

   ```kusto
   Heartbeat
   | where Category == "Azure Monitor Agent"
   | where TimeGenerated > ago(5m)
   | project Computer, TimeGenerated, Category, OSType
   | order by TimeGenerated desc
   ```

4. **Performance and events.** Run `Perf | take 20` and `Event | take 20`. `Perf` should return rows after a few minutes. `Event` may stay empty on a healthy host until something is logged. Signing in with a test user generates Remote Desktop and FSLogix events.
5. **AVD logs.** Sign in to the quick lab with a test user, wait a few hours, then run `WVDConnections | take 20`. Diagnostic data can take a few hours to appear after setup.
6. **Insights.** Open Azure Virtual Desktop Insights at `aka.ms/avdi`, pick the host pool, and open Workbooks, then Check Configuration. It reports anything that is missing.
7. **The alert.** Stop one session host from the portal. The Stop button deallocates it. After the heartbeats stop, wait more than 15 minutes plus the next 15-minute check. You should receive an email. Start the host again afterwards. The alert resolves itself after the heartbeats return.

## Clean up

Run `terraform destroy`. It deletes the workspace and everything the lab added, including the logs in the workspace. The quick lab stays, but the diagnostic settings, the agent and the associations are removed from it.

Azure keeps a deleted Log Analytics workspace for 14 days and reserves its name. If you apply the lab again within that time, set `log_analytics_workspace_name` to a different name.

## Before you use this design for real work

- **Do not use one cap for everything.** A daily cap protects your bill, but data stops arriving once the cap is reached. Choose it from real volumes.
- **Alert on more than heartbeats.** Add alerts for failed connections, high user input delay and full disks. The documentation's [diagnostics page](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics) has example queries for the `WVDConnections` and `WVDErrors` tables.
- **Send alerts to a team address.** One personal email is a single point of failure.
- **Plan for private networking.** The workspace here is open to the public internet by default.

## Sources

- [Enable Insights to monitor Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights)
- [Send diagnostic data to Log Analytics for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/diagnostics-log-analytics)
- [Estimate Azure Virtual Desktop monitoring costs](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights-costs)
