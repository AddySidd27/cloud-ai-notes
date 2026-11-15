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

By the end you will have a resource group called `rg-azb-core` that stays for the rest of this series, an action group that sends you email, and a monthly budget on your whole subscription with alerts at 50, 80 and 100 percent of actual cost plus one forecast alert. You will also create a practice resource group with tags and a virtual network in it, and delete it to see what a delete does.

## What you need

- An Azure subscription from [the free account lab](/azure-basics-labs/start-azure-account-tenant-subscription/), and the notes sheet from that lab. The Azure free account gives $200 of credit for 30 days.
- For the CLI part only: Cloud Shell from [the Cloud Shell lab](/azure-basics-labs/cloud-shell-and-azure-cli/). The portal part needs neither.
- A role that can create resources and budgets on the subscription. Microsoft says you need contributor permission to create and manage budgets.
- An email address you can read today.
- About 50 minutes. Cost: nothing. A virtual network is free, and Microsoft says there is no charge for using Azure Virtual Network. Action group emails are priced under Azure Monitor, so check [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/) if you want to be sure.

If your subscription is brand new, Microsoft says it can take up to 48 hours before you can use all Cost Management features. If the budget step fails, do the rest of the lab and come back to it.

If a step fails, select the bell icon at the top right of the portal. The notification shows the error text. Read it, and search for the exact text. The troubleshooting lab at the end of the series shows more places to look.

## Safety first

- Use a test tenant, not your employer's. Read the tenant and subscription name at the top of the portal before you change anything.
- Deleting a resource group deletes everything inside it and cannot be undone. In this lab you delete only `rg-azb-practice`. Read the name twice before you type it to confirm.
- A budget only sends emails. It does not stop or change anything that is running.
- Do not put secrets in tags. Microsoft says tags are stored as plain text and can show up in cost reports and exported templates.
- Azure already requires multifactor authentication (MFA) for Azure management work. If you are asked for it, that is expected.

## What the lab builds

![Diagram: Resource groups, tags, action group and budget.](/img/basics/resource-group-tags-budget.svg)

*Source: Microsoft Learn pages listed under Sources.*

## Steps in the Azure portal

### The resource group you will keep

A resource group is a container that holds related resources. A resource is anything you create in Azure, such as a virtual machine or a storage account. Put resources that share the same lifecycle in the same group, so you can deploy, update and delete them together. The group also has a region. That region is where the group's metadata is stored, and resources inside the group can be in other regions.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the subscription name.
2. Search for and open **Resource groups**, then select **Create**.
3. Set **Subscription** to your test subscription, **Resource group** to `rg-azb-core`, and **Region** to your region from the notes sheet (use the same one in every lab).
4. Select **Review + Create**, then **Create**. It takes a few seconds.
5. Select **Refresh** on the Resource groups page and open `rg-azb-core` to see it is empty.

Check: `rg-azb-core` is in the list and its Overview page opens.

### A practice group with tags, and a delete

A tag is a name and value pair that you attach to a resource group or a resource, such as `env = lab`. Tags help you find things and group costs. Three facts to know:

- Resources do not inherit the tags of their resource group. Tagging the group does not tag what is inside it.
- Tag names are not case sensitive, but tag values are.
- Do not put sensitive values in tags.

6. Select **Create** on the Resource groups page again.
7. Set **Resource group** to `rg-azb-practice` and use the same subscription and region.
8. Open the **Tags** tab, and add these three tags (use lowercase names to keep it simple):

   | Name | Value |
   |---|---|
   | env | lab |
   | owner | me |
   | series | azure-basics |

9. Select **Review + Create**, then **Create**.
10. Open `rg-azb-practice`. The tags show on the Overview page. You can add tags later with **Add tags** or **change** on that page, then **Save**.
11. Also tag `rg-azb-core` the same way (**env** = `core`, **owner** = `me`, **series** = `azure-basics`) so you see how to add tags to an existing group. Select **Save**.
12. Put something in the practice group. Search for **Virtual networks** and select **Create**. Set **Resource group** to `rg-azb-practice`, **Virtual network name** to `vnet-practice` and **Region** to your region. Leave Azure Bastion, Azure Firewall and DDoS protection off. Select **Review + create**, then **Create**.

Check: both groups show their tags on the Overview page, and `rg-azb-practice` contains `vnet-practice`.

Now delete the practice group, while the tags are fresh.

13. Go to **Resource groups** and open `rg-azb-practice`. Look at the list of resources: `vnet-practice` is inside.
14. Select **Delete resource group**.
15. Type the name `rg-azb-practice` to confirm, and confirm the delete.
16. Go back to the **Resource groups** list and select **Refresh**.

Check: `rg-azb-practice` is gone, and `vnet-practice` went with it. `rg-azb-core` is still there. This is the lesson: a delete takes everything inside the group. If it had held a virtual machine and a disk, they would have gone too. You can stop here and carry on later.

### An action group that sends email

An action group is a saved list of who to notify and what to run when an alert fires. Notification types include email, SMS, voice and push, and automated actions include webhooks, Azure Functions and Logic Apps. One action group can be used by many alert rules, so you create it once. You create it now so the alert in the Log Analytics lab can reuse it.

17. Search for and open **Monitor**. Select **Alerts**, then **Action groups**, then **Create**.
18. Under Project details, choose your subscription and the resource group `rg-azb-core`. Set **Region** to **Global**. A Global region means the service decides where the group is stored.
19. Under Instance details, set **Action group name** to `ag-azb-email` and **Display name** to `azb-email`.
20. Select **Next: Notifications**. Under **Notification type**, choose **Email/SMS message/Push/Voice**, tick **Email**, and type your email address. Name the notification `me` and select **OK**.
21. Select **Review + create**, then **Create**.
22. Open your mailbox. A new email address gets a one-time passcode (OTP) request, and you must verify it within 30 minutes of saving. Follow the link or enter the code. If it expires, open the action group and select **Resend**.
23. Optional: on the **Action groups** page, select `ag-azb-email`, then **Test**, pick a sample type and send a test.

Check: you got the confirmation email, the address is verified, and a test (if you ran it) shows **Success**. You can stop here.

### A monthly budget on your subscription

A budget is a spending limit for a scope and a time period. Here the scope is your whole subscription, so it sees the cost of every resource group in this series, not only `rg-azb-core`. `rg-azb-core` holds no billable resources, so a budget on that group alone would never alert. Three facts that decide how you read the alerts:

- **A budget only alerts.** When a threshold is passed, resources are not affected and consumption is not stopped.
- **The alerts are not instant.** Cost and usage data is typically available within 8 to 24 hours, and budgets are checked against it every 24 hours. When a threshold is met, emails normally go out within an hour of the check. So a new budget will not alert at once.
- **Alert types.** An *actual* alert fires on cost already spent. A *forecasted* alert fires when Azure expects the cost to pass the threshold by the end of the period. A budget can have up to five thresholds and five email addresses.

24. Search for **Subscriptions** and open your test subscription. In the left menu, select **Budgets** (it may sit under **Cost Management**), then **Add**. If **Budgets** does not open or **Add** fails on a new subscription, stop. It can take up to 48 hours after sign-up. Come back to this step tomorrow.
25. Check that the scope shown is your subscription. Leave filters empty.
26. Set the budget name to `budget-azb-core`. Set the reset period to **Monthly**. Set an expiration date in the future, for example two years from today. A budget resets only when you pick a future expiration date, and an expired budget is deleted. If the page also shows a start date, use the first day of the current month.
27. Set **Amount** to a small number that fits your credit, such as 10. Use the currency of your account.
28. Select **Next**. Add these alert conditions. Use the **Type** field to switch between Actual and Forecasted:

    | Type | % of budget |
    |---|---|
    | Actual | 50 |
    | Actual | 80 |
    | Actual | 100 |
    | Forecasted | 100 |

29. Enter your email address as the alert recipient. A budget needs at least one threshold and one email address.
30. Optional: in the alert recipients area, select **Manage action group** and choose `ag-azb-email`. Action groups work for subscription and resource group scopes. If you add it, the action group also runs when a threshold is met. If you cannot find the link, skip this step. The email in step 29 still works, and the action group is then not connected to the budget.
31. Select **Create**.

Add `azure-noreply@microsoft.com` to your approved senders, so budget emails do not land in junk.

Check: `budget-azb-core` is listed under **Budgets** on your subscription with the amount you set. Open it to see the four alert conditions. The spending bar may show nothing yet, because cost data arrives 8 to 24 hours late.

## Steps with the Azure CLI

The CLI covers the resource groups, tags and action group. Do either the portal steps for those sections or these commands, not both. The budget is portal only here: the `az consumption` budget commands set one alert, not the four in this lab.

Run these in Cloud Shell (Bash) from the Cloud Shell lab. Most CLI blocks in this series are Bash; the Terraform lab uses PowerShell. Check which subscription you are in first, then set the variables. Use the command spelling of your region from the notes sheet (no spaces, lower case, for example `eastus2`). Cloud Shell forgets your variables after about 20 minutes idle. If a command complains about an empty value, paste this block again.

```bash
az account show --query "{name:name, tenant:tenantId}" --output table
LOCATION=eastus2           # replace with the command spelling of your region
EMAIL="<your-email-here>"  # replace the whole thing, keep the quotes
[ "$EMAIL" = "<your-email-here>" ] && echo "Set EMAIL first"
```

Create the two resource groups, with tags on both. `--tags` takes space-separated `key=value` pairs. Creating a group again with the same name and the same location only updates its tags. A different location is refused, because a resource group's location cannot be changed.

```bash
az group create --name rg-azb-core --location $LOCATION --tags env=core owner=me series=azure-basics
az group create --name rg-azb-practice --location $LOCATION --tags env=lab owner=me series=azure-basics
az network vnet create --resource-group rg-azb-practice --name vnet-practice --location $LOCATION
```

Check: `az group list --tag series=azure-basics --query "[].name" --output tsv` lists both names. (`--output` can be shortened to `-o`.)

Work with tags later. `az tag update` with `--operation Merge` adds tags to existing ones, `Replace` swaps the whole set, and `Delete` removes the ones you name. `az tag create` replaces all tags on the entity, so use it with care.

```bash
GROUP_ID=$(az group show --name rg-azb-practice --query id --output tsv)
az tag update --resource-id $GROUP_ID --operation Merge --tags cost-center=training
az tag list --resource-id $GROUP_ID
```

Delete the practice group. It asks `Are you sure (y/n)?`. Type `y` and press Enter. Run the second command after the first one finishes.

```bash
az group delete --name rg-azb-practice
az group exists --name rg-azb-practice
```

Check: the last command prints `false`.

Create the action group with one email receiver. The format is `--action email NAME EMAIL_ADDRESS`.

```bash
az monitor action-group create \
  --name ag-azb-email \
  --resource-group rg-azb-core \
  --short-name azb-email \
  --action email me $EMAIL
```

Check: `az monitor action-group show --name ag-azb-email --resource-group rg-azb-core --query name --output tsv` prints the name. Then verify your email address with the one-time passcode message, as in the portal steps. Then create the budget in the portal.

## Terraform

Terraform is a tool that builds Azure resources from text files. You meet it in [Terraform basics](/azure-basics-labs/terraform-basics/). Skip this section for now. It shows the resource group in a few lines.

```hcl
variable "location" {
  type        = string
  description = "Must match the region you used in the portal or CLI steps."
}

resource "azurerm_resource_group" "core" {
  name     = "rg-azb-core"
  location = var.location

  tags = {
    env    = "core"
    owner  = "me"
    series = "azure-basics"
  }
}
```

The lab [Add a Cost Budget and Alerts to Your AVD Lab with Terraform](/terraform-labs/avd-budget-alert-lab/) puts a budget on one existing resource group, not on the subscription. It is a separate exercise, and you do not need it for this series.

## Check that it works

- `rg-azb-core` exists with tags, and `rg-azb-practice` does not.
- `ag-azb-email` exists in `rg-azb-core` and its email address is verified.
- `budget-azb-core` exists on your subscription and shows four alert conditions.
- To see a real budget email, you have to wait. With the data delay of 8 to 24 hours and a check every 24 hours, allow about two days before you expect a message, and only if your cost actually reaches a threshold. If nothing costs money yet, no email is the normal result.

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
- `budget-azb-core` (on your subscription, so it sees the cost of every group)

`rg-azb-core` only holds the action group. The later labs put their resources in other groups: `rg-azb-lab` (created in [the virtual network lab](/azure-basics-labs/virtual-network-subnet/)), `rg-azb-tf` ([Terraform basics](/azure-basics-labs/terraform-basics/)) and `rg-azb-sandbox` ([the policy and locks lab](/azure-basics-labs/azure-policy-locks/)). The budget is on the subscription, so it watches all of them. To remove the budget later, open your subscription, select **Budgets**, open `budget-azb-core` and delete it.

## Where this is used in AVD

A host pool with session hosts bills every hour its virtual machines run. A subscription budget is your first alert when you forget one. The lab on [VM size, disk type and power states](/azure-basics-labs/vm-size-disk-stop-deallocate/) shows how stop and deallocate change the bill. For how resource groups fit a real AVD design, see [Prepare your Azure environment](/azure-virtual-desktop/prepare-your-azure-environment/).

## Next lab

[Microsoft Entra users, groups and break-glass accounts](/azure-basics-labs/entra-users-groups-break-glass/) adds the people and groups that you will give access to your resources in later labs.

## Sources

- [Manage Azure resource groups by using the Azure portal](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal)
- [Use tags to organize your Azure resources and management hierarchy](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources)
- [Tutorial: Create and manage budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
