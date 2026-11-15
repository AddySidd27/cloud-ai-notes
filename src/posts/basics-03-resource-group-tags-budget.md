---
title: "Resource Group, Tags, Budget and Action Group"
seoTitle: "Azure Resource Group, Tags and Budget Alert: Beginner Lab"
layout: post.njk
permalink: "/azure-basics-labs/resource-group-tags-budget/"
order: 313
tags: [azure-basics-lab]
deck: "Create the resource group you will keep for the whole series, practise with tags on a throwaway group, and set a monthly budget that emails you."
description: "Create a resource group and tags in Azure, set up an email action group and a monthly budget with 50, 80 and 100 percent alerts, then delete a practice group."
---

By the end you will have a resource group called `rg-azb-core` that stays for the rest of this series, an action group that sends you email, and a monthly budget on that group with alerts at 50, 80 and 100 percent of actual cost plus one forecast alert. You will also create a second, practice resource group with tags, and delete it to see what a delete does.

I have not run these steps in a live tenant for this article, and I have not run `terraform validate` on the Terraform block. Each step is checked against Microsoft Learn (Microsoft's documentation site).

## What you need

- An Azure subscription from [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/). The Azure free account gives $200 of credit for 30 days.
- For the CLI part only: Cloud Shell or the Azure CLI from [Lab 2](/azure-basics-labs/cloud-shell-and-azure-cli/). Azure CLI 2.76 or newer. The portal part needs neither.
- A role that can create resources and budgets on the subscription. Learn says you need contributor permission to create and manage budgets.
- An email address you can read today.
- About 30 minutes. Nothing in this lab runs or stores data. I did not find a Learn page that states the price of an action group email, so check [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/) if you want to be sure.

If your subscription is brand new, Learn says it can take up to 48 hours before you can use all Cost Management features. If the budget step fails, wait and try again.

## Safety first

- Use a test tenant, not your employer's. Read the tenant and subscription name at the top of the portal before you change anything.
- Deleting a resource group deletes everything inside it and cannot be undone. In this lab you delete only `rg-azb-practice`. Read the name twice before you type it to confirm.
- A budget only sends emails. It does not stop or change anything that is running.
- Do not put secrets in tags. Learn says tags are stored as plain text and can show up in cost reports and exported templates.
- Azure already requires multifactor authentication (MFA) for Azure management work. If you are asked for it, that is expected.

## What the lab builds

![Two resource groups in one subscription. rg-azb-core holds an action group named ag-azb-email and carries a monthly budget named budget-azb-core. The budget sends alerts at 50, 80 and 100 percent of actual cost and one forecast alert to the action group and to your email. A second group, rg-azb-practice, has the tags env, owner and lab and is deleted at the end.](/img/basics/resource-group-tags-budget.svg)

*Source: Learn pages [Manage resource groups in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal), [Use tags to organize your Azure resources](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources), [Action groups](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/action-groups) and [Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### Part 1: The resource group you will keep

A resource group is a container that holds related resources. A resource is anything you create in Azure, such as a virtual machine or a storage account. Learn says to put resources that share the same lifecycle in the same group, so you can deploy, update and delete them together. The group also has a region. Learn says that region is where the group's metadata is stored, and that resources inside the group can be in other regions.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the subscription name.
2. Search for and open **Resource groups**, then select **Create**.
3. Set **Subscription** to your test subscription, **Resource group** to `rg-azb-core`, and **Region** to the region closest to you.
4. Select **Review + Create**, then **Create**. It takes a few seconds.
5. Select **Refresh** on the Resource groups page and open `rg-azb-core` to see it is empty.

Check: `rg-azb-core` is in the list and its Overview page opens.

### Part 2: A practice group with tags

A tag is a name and value pair that you attach to a resource group or a resource, such as `env = lab`. Tags help you find things and group costs. Three facts from Learn:

- Resources do not inherit the tags of their resource group. Tagging the group does not tag what is inside it.
- Tag names are not case sensitive, but tag values are.
- Do not put sensitive values in tags.

6. Select **Create** on the Resource groups page again.
7. Set **Resource group** to `rg-azb-practice` and use the same subscription and region.
8. Open the **Tags** tab, and add these three tags (use lowercase names to keep it simple):

   | Name | Value |
   |---|---|
   | env | lab |
   | owner | your first name |
   | lab | 03 |

9. Select **Review + Create**, then **Create**.
10. Open `rg-azb-practice`. The tags show on the Overview page. Learn describes adding tags later with **Add tags** or **change** on that page, then **Save**.
11. Also tag `rg-azb-core` the same way (**env** = `core`, **owner**, **lab** = `03`) so you see how to add tags to an existing group. Select **Save**.

Check: both groups show their tags on the Overview page.

### Part 3: An action group that sends email

An action group is a saved list of who to notify and what to run when an alert fires. Learn says notification types include email, SMS, voice and push, and automated actions include webhooks, Azure Functions and Logic Apps. One action group can be used by many alert rules, so you create it once.

12. Search for and open **Monitor**. Select **Alerts**, then **Action groups**, then **Create**.
13. Under Project details, choose your subscription and the resource group `rg-azb-core`. Choose the region. Learn says a Global region means the service decides where the group is stored, and a Regional choice keeps it in one region. Global is fine here.
14. Under Instance details, set **Action group name** to `ag-azb-email` and **Display name** to `azb-email`.
15. Select **Next: Notifications**. Under **Notification type**, choose the email option. If the list reads **Email/SMS message/Push/Voice**, choose that and select **Email**. Enter your address and name the notification `me`. Select **OK**.
16. Select **Review + create**, then **Create**.
17. Open your mailbox. Learn says a new email address gets a one-time passcode (OTP) request, and that you must verify it within 30 minutes of saving. Follow the link or enter the code. If it expires, open the action group and select **Resend**.
18. Optional: on the **Action groups** page, select `ag-azb-email`, then **Test**, pick a sample type and send a test. Learn says test emails have "Test" in the subject.

Check: you got the confirmation email, and a test (if you ran it) shows **Success**.

### Part 4: A monthly budget on rg-azb-core

A budget is a spending limit for a scope and a time period, such as one resource group for one month. Three facts from Learn that decide how you read the alerts:

- **A budget only alerts.** When a threshold is passed, resources are not affected and consumption is not stopped.
- **The alerts are not instant.** Cost and usage data is typically available within 8 to 24 hours, and budgets are checked against it every 24 hours. When a threshold is met, emails normally go out within an hour of the check.
- **Alert types.** An *actual* alert fires on cost already spent. A *forecasted* alert fires when Azure expects the cost to pass the threshold by the end of the period. A budget can have up to five thresholds and five email addresses.

19. Open `rg-azb-core`. In its menu, select **Budgets** (Learn says it shows once you have opened a resource group), then **Add**.
20. Check that the scope shown is `rg-azb-core`. Leave filters empty.
21. Set the budget name to `budget-azb-core`. Set the reset period to **Monthly**. Set an expiration date in the future, for example two years from today. Learn says a budget resets only when you pick a future expiration date, and that an expired budget is deleted. If the page also shows a start date, use the first day of the current month.
22. Set **Amount** to a small number that fits your credit, such as 10. Use the currency of your account.
23. Select **Next**. Add these alert conditions. Use the **Type** field to switch between Actual and Forecasted:

    | Type | % of budget |
    |---|---|
    | Actual | 50 |
    | Actual | 80 |
    | Actual | 100 |
    | Forecasted | 100 |

24. Enter your email address as the alert recipient. Learn says a budget needs at least one threshold and one email address.
25. Learn says you can also call an action group from a budget, by selecting **Manage action group** while you create or edit it. Action groups work for subscription and resource group scopes. Look for that link on this page and pick `ag-azb-email`. If you cannot see how to pick an existing group, skip this step. The email in step 24 still works.
26. Select **Create**.

Add `azure-noreply@microsoft.com` to your approved senders, so budget emails do not land in junk.

Check: `budget-azb-core` is listed under **Budgets** on `rg-azb-core` with the amount you set. Open it to see the four alert conditions. The spending bar may show nothing yet, because cost data arrives 8 to 24 hours late.

### Part 5: Delete the practice group

27. Go to **Resource groups** and open `rg-azb-practice`.
28. Select **Delete resource group**.
29. Type the name `rg-azb-practice` to confirm, and confirm the delete.
30. Go back to the **Resource groups** list and select **Refresh**.

Check: `rg-azb-practice` is gone. `rg-azb-core` is still there. This is also the lesson: the practice group was empty, but if it had held a virtual machine, a disk and a network, all of them would have gone with it.

## Steps with the Azure CLI

Run these in Cloud Shell (Bash) from Lab 2. If you already did the portal steps, `rg-azb-core` exists, and creating it again with the same name only updates its tags. Check which subscription you are in first. Set the variables once, and replace the email with your own.

```bash
az account show --query "{name:name, tenant:tenantId}" -o table
LOCATION=eastus2           # use your own region
EMAIL=you@example.com      # replace with your own address
START=$(date +%Y-%m-01)    # first day of this month
END=$(date -d '+2 years' +%Y-%m-01)
```

Create the two resource groups, with tags on both. `--tags` takes space-separated `key=value` pairs.

```bash
az group create --name rg-azb-core --location $LOCATION --tags env=core owner=me lab=03
az group create --name rg-azb-practice --location $LOCATION --tags env=lab owner=me lab=03
```

Check: `az group list --tag lab=03 --query "[].name" -o tsv` lists both names.

Work with tags later. Learn says `az tag update` with `--operation Merge` adds tags to existing ones, `Replace` swaps the whole set, and `Delete` removes the ones you name. `az tag create` replaces all tags on the entity, so use it with care.

```bash
GROUP_ID=$(az group show --name rg-azb-practice --query id -o tsv)
az tag update --resource-id $GROUP_ID --operation Merge --tags cost-center=training
az tag list --resource-id $GROUP_ID
```

Create the action group with one email receiver. The format is `--action email NAME EMAIL_ADDRESS`.

```bash
az monitor action-group create \
  --name ag-azb-email \
  --resource-group rg-azb-core \
  --short-name azb-email \
  --action email me $EMAIL
```

Check: `az monitor action-group show --name ag-azb-email --resource-group rg-azb-core --query name -o tsv` prints the name. Then verify your email address with the one-time passcode message, as in the portal steps.

The budget has a CLI command, but Learn marks the whole `az consumption` command group as preview and under development, and the Learn tutorial warns that CLI commands might not support the latest version of the budget API. So the portal is the main path in this lab. For reference, the Learn tutorial shows this shape for a resource group budget with one actual-cost alert at 80 percent. Set the start date to the first day of the current month.

```bash
AG_ID=$(az monitor action-group show --name ag-azb-email --resource-group rg-azb-core --query id -o tsv)
az consumption budget create-with-rg \
  --budget-name budget-azb-core \
  --resource-group rg-azb-core \
  --amount 10 --category Cost --time-grain Monthly \
  --time-period "{\"start-date\":\"$START\",\"end-date\":\"$END\"}" \
  --notifications "{\"Key1\":{\"enabled\":\"true\",\"operator\":\"GreaterThanOrEqualTo\",\"contact-emails\":[\"$EMAIL\"],\"threshold\":80.0,\"contact-groups\":[\"$AG_ID\"]}}"
```

I did not find the CLI syntax for a forecast alert on Learn, so add the 50, 100 and forecast alerts in the portal by editing the budget, or use the Terraform lab linked below.

Delete the practice group. `--yes` skips the prompt, so leave it off the first time.

```bash
az group delete --name rg-azb-practice
az group exists --name rg-azb-practice
```

Check: the last command prints `false`.

## Terraform

Terraform describes the same resource group in a few lines. This block is not run for this article.

```hcl
resource "azurerm_resource_group" "core" {
  name     = "rg-azb-core"
  location = "eastus2"

  tags = {
    env   = "core"
    owner = "me"
    lab   = "03"
  }
}
```

The budget with the 50, 80, 100 and forecast alerts is covered in [Add a Cost Budget and Alerts to Your AVD Lab with Terraform](/terraform-labs/avd-budget-alert-lab/). That lab reads an existing resource group by name, so you can give it `rg-azb-core`. If you already made `budget-azb-core` in the portal, delete it first or use a different budget name there. Terraform itself is introduced in [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/).

## Check that it works

- `rg-azb-core` exists with tags, and `rg-azb-practice` does not.
- `ag-azb-email` exists in `rg-azb-core` and its email address is verified.
- `budget-azb-core` shows four alert conditions.
- To see a real budget email, you have to wait. With the data delay of 8 to 24 hours and a check every 24 hours, allow about two days before you expect a message, and only if your cost actually reaches a threshold. In an empty resource group nothing costs money, so no email is the normal result.

## The most common mistake

Thinking a budget protects you. It does not. It only sends emails, and the emails arrive after the cost data does, which can be a day or more later. A virtual machine left running over a weekend can cost more than you planned before the first alert arrives. The next most common mistake is deleting the wrong resource group, because the delete cannot be undone and takes everything inside it.

## Clean up

You already deleted `rg-azb-practice`. If you skipped that part, run:

```bash
az group delete --name rg-azb-practice
```

**Keep these for the later labs:**

- `rg-azb-core`
- `ag-azb-email`
- `budget-azb-core`

Later labs put their resources in `rg-azb-core`, so the budget watches their cost. To remove the budget later, open it under **Budgets** on `rg-azb-core` and delete it.

## Where this is used in AVD

An Azure Virtual Desktop deployment puts its host pool, session hosts and network in resource groups, and you plan those groups before you build. See [Prepare your Azure environment](/azure-virtual-desktop/prepare-your-azure-environment/) for how the groups, subscription and naming fit together. A budget on the resource group is the first safety net for a lab you may forget to stop.

## Next lab

[Lab 4: Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/) adds the people and groups that you will give access to `rg-azb-core`.

## Sources

- [Manage Azure resource groups by using the Azure portal](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal)
- [Manage Azure resource groups by using Azure CLI](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-cli)
- [Azure Resource Manager resource group and resource deletion](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/delete-resource-group)
- [Use tags to organize your Azure resources and management hierarchy](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources)
- [Apply tags with Azure portal](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources-portal)
- [Apply tags with Azure CLI](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources-cli)
- [Action groups](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/action-groups)
- [az monitor action-group](https://learn.microsoft.com/en-us/cli/azure/monitor/action-group)
- [Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
- [az consumption budget](https://learn.microsoft.com/en-us/cli/azure/consumption/budget)
- [az group](https://learn.microsoft.com/en-us/cli/azure/group)
