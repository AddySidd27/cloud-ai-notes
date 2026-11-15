---
title: "Add a Cost Budget and Alerts to Your AVD Lab with Terraform"
seoTitle: "Azure Budget Alerts with Terraform: Resource Group Cost Budget for an AVD Lab"
layout: post.njk
permalink: "/terraform-labs/avd-budget-alert-lab/"
order: 303
tags: [terraform-lab]
deck: "A small Terraform project that puts a monthly budget on the lab's resource group and emails you when the cost, or the forecast, passes the limits you set."
description: "A walk through a small Terraform lab that creates an Azure cost budget on the resource group of an Azure Virtual Desktop lab, with alerts at 50, 80 and 100 percent of actual cost and when the forecast goes above the budget."
---

A lab that you forget to shut down keeps costing money. This article walks through a small Terraform project that puts a monthly budget on the resource group of your lab and emails you when the cost reaches the limits you choose. It is meant to sit on top of the [AVD quick lab](/terraform-labs/avd-quick-lab/), but it works on any resource group.

Below is what the code does, how Microsoft describes the features it uses, and a test you can run.

## Key terms

| Term | Meaning |
|---|---|
| Resource group | An Azure container that holds related resources. The quick lab puts everything in `rg-avd-dev`. |
| Budget | A spending limit for a scope and a time period, such as one resource group for one month. Azure compares your cost with it. |
| Scope | What the budget watches. Here it is one resource group. |
| Actual cost | What the resources have cost so far in the period. |
| Forecast | Azure's estimate of what the cost will be by the end of the period. |
| Threshold | A percentage of the budget at which Azure sends an alert. At 80% of a budget of 50, the threshold is reached at a cost of 40. |
| Subscription | The Azure billing and access boundary that contains resource groups. |
| Terraform | A tool that creates cloud resources from code files. |
| Provider | The plugin that lets Terraform talk to Azure. `versions.tf` picks it. |
| Action group | An Azure Monitor object that can send notifications or call automation. Used in "Before you use this design for real work". |
| State file | `terraform.tfstate`, where Terraform records what it created. |

## What the lab builds

![A budget named budget-avd-dev applies to the resource group rg-avd-dev. It reads the cost of the lab resources. When actual cost reaches 50, 80 and 100 percent of the budget, or the forecast goes above 100 percent, it sends an email to up to five addresses. An alert only sends a message and does not stop or change any resource.](/img/avd/AVD-Terraform-Budget-Lab.svg)

*Source: the lab's Terraform code and the page [Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

The code creates one resource: a monthly budget on an existing resource group. It does not create or change the resource group, and it does not touch anything inside it.

## What Azure budgets do and do not do

These points come from the page [Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets). They decide how you should read the alerts.

- **An alert does not stop anything.** When a threshold is exceeded, resources are not affected and consumption is not stopped. A budget tells you. It does not turn a VM off.
- **The alerts are not instant.** Cost and usage data is typically available within 8 to 24 hours, and budgets are checked against that data every 24 hours. When a threshold is met, the email is normally sent within an hour of the check. A VM that runs all weekend can cost more than you expected before the first email arrives.
- **A budget can use actual cost or the forecast.** A forecast alert warns you that spending is likely to pass the limit before it does.
- **A budget can have up to five thresholds and five email addresses.**
- **A new subscription may not allow budgets at first.** It can take up to 48 hours before you can use all Cost Management features on a new subscription.

## Before you start

- An Azure subscription and an existing resource group, for example `rg-avd-dev` from the quick lab.
- A role that lets you create budgets on the resource group. You must have contributor permission. Owner can also create budgets for a subscription.
- The Azure CLI, Git and Terraform 1.9 or newer.
- An email address for the alerts. The documentation suggests adding `azure-noreply@microsoft.com` to your approved senders so that the emails do not go to junk.

## The code

You need five `.tf` files in one folder, plus a `terraform.tfvars` file for your values. The first two tell Terraform which provider to use and which subscription to work in.

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

`variables.tf` defines what you can change:

| Setting | Default | Meaning |
|---|---|---|
| `subscription_id` | none | The subscription that contains the resource group. |
| `resource_group_name` | `rg-avd-dev` | The resource group to put the budget on. |
| `budget_name` | `budget-avd-dev` | The name of the budget. |
| `budget_amount` | `50` | The monthly amount. Check the currency on your invoice. |
| `budget_start_date` | none | The first day of the current month, in the form `2026-11-01T00:00:00Z`. Azure rejects a start date from an earlier month. |
| `alert_emails` | none | One to five email addresses. |
| `actual_cost_thresholds` | `[50, 80, 100]` | Percentages of the budget that trigger an alert on actual cost. |
| `forecast_cost_threshold` | `100` | The percentage that triggers an alert when the forecast goes above it. |

The start date has no default on purpose. Set it to the first day of the month you run the lab in. It must be the first day of a month, that a past start date must fall inside the budget period, that a future start date can be at most twelve months ahead, and that changing it later forces Terraform to replace the budget. The code checks only the format. A budget can have up to five thresholds. The forecast alert counts as one of them, so the code allows at most four actual cost thresholds.

The full file:

```hcl
variable "subscription_id" {
  description = "ID of the Azure subscription that contains the resource group."
  type        = string
}

variable "resource_group_name" {
  description = "Name of the existing resource group to put the budget on. The default matches the AVD quick lab."
  type        = string
  default     = "rg-avd-dev"
}

variable "budget_name" {
  description = "Name of the budget."
  type        = string
  default     = "budget-avd-dev"
}

variable "budget_amount" {
  description = "Monthly budget amount."
  type        = number
  default     = 50

  validation {
    condition     = var.budget_amount > 0
    error_message = "budget_amount must be greater than 0."
  }
}

variable "budget_start_date" {
  description = "First day of the current month, in the form 2026-11-01T00:00:00Z. Azure rejects a start date from an earlier month."
  type        = string

  validation {
    condition     = can(regex("^[0-9]{4}-[0-9]{2}-01T00:00:00Z$", var.budget_start_date))
    error_message = "budget_start_date must be the first day of a month, for example 2026-11-01T00:00:00Z."
  }
}

variable "alert_emails" {
  description = "Email addresses that receive the budget alerts. Azure allows up to five."
  type        = list(string)

  validation {
    condition     = length(var.alert_emails) >= 1 && length(var.alert_emails) <= 5
    error_message = "Provide between 1 and 5 email addresses."
  }
}

variable "actual_cost_thresholds" {
  description = "Percentages of the budget that trigger an alert on actual cost."
  type        = list(number)
  default     = [50, 80, 100]

  validation {
    condition     = alltrue([for t in var.actual_cost_thresholds : t >= 0.01 && t <= 1000])
    error_message = "Each threshold must be between 0.01 and 1000 percent."
  }

  validation {
    condition     = length(var.actual_cost_thresholds) >= 1 && length(var.actual_cost_thresholds) <= 4
    error_message = "Provide between 1 and 4 actual cost thresholds. Azure allows up to five thresholds in a budget, and one is used for the forecast alert."
  }
}

variable "forecast_cost_threshold" {
  description = "Percentage of the budget that triggers an alert when the forecast goes above it."
  type        = number
  default     = 100
}
```

### The budget

`main.tf` reads the resource group and creates the budget:

```hcl
data "azurerm_resource_group" "lab" {
  name = var.resource_group_name
}

resource "azurerm_consumption_budget_resource_group" "lab" {
  name              = var.budget_name
  resource_group_id = data.azurerm_resource_group.lab.id

  amount     = var.budget_amount
  time_grain = "Monthly"

  time_period {
    start_date = var.budget_start_date
  }

  dynamic "notification" {
    for_each = toset(var.actual_cost_thresholds)

    content {
      enabled        = true
      threshold      = notification.value
      threshold_type = "Actual"
      operator       = "GreaterThanOrEqualTo"
      contact_emails = var.alert_emails
    }
  }

  notification {
    enabled        = true
    threshold      = var.forecast_cost_threshold
    threshold_type = "Forecasted"
    operator       = "GreaterThan"
    contact_emails = var.alert_emails
  }
}
```

A few things to notice:

- **`data "azurerm_resource_group"`** only reads the resource group. Terraform does not manage it, so removing the budget later does not delete the resource group.
- **`time_grain = "Monthly"`** resets the budget at the start of each calendar month. With no end date, the budget ends 10 years after the start date.
- **One `notification` block per threshold.** The `dynamic` block creates one block for each value in `actual_cost_thresholds`. The last block is the forecast alert.
- **The operators.** Actual cost alerts use `GreaterThanOrEqualTo`, so the 100% alert fires when the cost reaches the budget. The forecast alert uses `GreaterThan`, so it fires when the forecast goes above the limit.

`outputs.tf`:

```hcl
output "budget_id" {
  description = "Resource ID of the budget."
  value       = azurerm_consumption_budget_resource_group.lab.id
}

output "budget_amount" {
  description = "Monthly amount the budget tracks."
  value       = var.budget_amount
}
```

## Run it

1. **Create the folder and the files** above, and copy the example values into `terraform.tfvars`:

   ```hcl
   subscription_id   = "00000000-0000-0000-0000-000000000000"
   # Use the first day of the current month.
   budget_start_date = "2026-11-01T00:00:00Z"
   alert_emails      = ["you@example.com"]

   # Optional. These are the defaults.
   # resource_group_name     = "rg-avd-dev"
   # budget_amount           = 50
   # actual_cost_thresholds  = [50, 80, 100]
   # forecast_cost_threshold = 100
   ```

2. **Keep `terraform.tfvars` out of Git.** It holds your subscription ID and email address. Add a `.gitignore` file that lists `*.tfvars`, `.terraform/` and `*.tfstate`. The state file records what Terraform created and can hold sensitive values.
3. **Sign in and initialize.** Run `az login`, then `terraform init`.
4. **Check and plan.** Run `terraform validate`, then `terraform plan -out main.tfplan`. The plan should show one budget to add.
5. **Apply.** Run `terraform apply main.tfplan`.

## Check that it works

1. In the Azure portal, open the resource group and select **Budgets**. `budget-avd-dev` should be listed with the amount you set.
2. Open the budget. The alert conditions should show the thresholds you chose, with the email addresses.
3. To see an alert arrive, you have to wait for cost data. Run the lab for a day, then lower `budget_amount` to a small number such as `1` and apply again. If the cost is already above the new limit, the actual cost alerts should fire at the next daily check. Cost data can lag by 8 to 24 hours, a check every 24 hours and an email within an hour of the check, so allow about two days. Check your junk folder. This test does not exercise the forecast alert.
4. Set `budget_amount` back to your real value and apply again.

If the budget cannot be created on a new subscription, wait. It can take up to 48 hours before all Cost Management features work.

## Clean up

Run `terraform destroy`. It deletes the budget only. The resource group and the lab inside it stay.

## Before you use this design for real work

- **A budget is not a limit.** It sends emails and nothing more. The documentation describes an action group that can run automation when a threshold is met, in [Manage costs with budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/cost-management-budget-scenario), if you want something to act on an alert.
- **The budget counts everything in the resource group.** If you add the [monitoring lab](/terraform-labs/avd-monitoring-lab/), its Log Analytics workspace is in the same group, so its cost counts here too.
- **Pick the amount from real numbers.** The default of 50 is a placeholder. Use the Azure pricing calculator and the cost you actually see.
- **Use a separate budget when the amount changes.** A budget resets with the same amount each period, so create a separate budget when the amount will differ in future periods. If each of your environments has its own amount, give each its own budget.

## Sources

- [Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
- [Manage costs with budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/cost-management-budget-scenario)
- [azurerm_consumption_budget_resource_group](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/consumption_budget_resource_group)
