---
title: "Azure Cloud Shell and Azure CLI: your first commands"
seoTitle: "Azure Cloud Shell and Azure CLI for beginners: first commands"
layout: post.njk
permalink: "/azure-basics-labs/cloud-shell-and-azure-cli/"
order: 312
tags: [azure-basics-lab]
deck: "You open Cloud Shell, run your first read-only Azure CLI commands, and know how to install the CLI on your own PC and sign in."
description: "Open Azure Cloud Shell, run az account show, az group list, --output table and --query, then install Azure CLI on Windows and sign in with az login."
---
By the end you will have run your first Azure commands in the browser, and you will know how to install the Azure CLI on a Windows PC and sign in. Every command in this lab only reads information. The only thing that can be created is the Cloud Shell storage account, and only if you choose that option.

I have not run these steps in a live tenant for this article. Each step is checked against Microsoft Learn.

## What you need

- Lab 1: [Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/). You need a test tenant and a subscription you can sign in to. Step 5 of Lab 1 registered the Microsoft.CloudShell provider, which Cloud Shell needs.
- A modern browser. For the local install part, a Windows PC.
- Time: about 30 minutes.
- Cost: running Cloud Shell itself is free. If you choose the option with a storage account, regular storage costs apply (see the first safety point). On the Azure free account you get $200 credit for 30 days, which is far more than this lab needs.
- Role: any role that can sign in and read the subscription is enough for the ephemeral option. For the storage account option, Learn says users need Contributor access or higher on the storage account. On your own free account you already have that.

## Safety first

- Cloud Shell can run with or without a storage account. Use of the machine that hosts Cloud Shell is free, but the file share that keeps your files sits in a storage account, and regular storage costs apply. Without a storage account (an "ephemeral" session) your files are deleted when the session ends.
- Use a throwaway test tenant, never your employer's tenant. Before any change, read the tenant and subscription name that `az account show` prints.
- Only read commands in this lab: `show`, `list`, `--help`, `find`. No `create`, `update` or `delete`.
- Do not sign in with `az login --use-device-code`. Use the normal `az login`, which opens a browser.
- Azure already requires multifactor authentication (MFA) for Azure management. Do not plan around turning it off. There is no opt-out.
- Use Azure CLI version 2.76 or later.

## What the lab builds

![Left to right: you in a browser open Azure Cloud Shell in the Azure portal, or you run the Azure CLI on your own Windows PC after az login. Both talk to Azure Resource Manager and your subscription, and Cloud Shell can optionally use a storage account with a file share.](/img/basics/cloud-shell-and-azure-cli.svg)

*Source: [Azure Cloud Shell overview](https://learn.microsoft.com/en-us/azure/cloud-shell/overview), [Get started with Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

No resources are deployed. You only connect and read.

## Steps in the Azure portal

Cloud Shell is a terminal that runs in your browser. Microsoft manages it, and it signs you in automatically. The Azure CLI is already installed in it.

1. Sign in to the [Azure portal](https://portal.azure.com/) with your test account. Complete the MFA prompt.
2. In the top navigation bar, select **Cloud Shell**.
3. The first time, you are asked which shell to use. Select **Bash**.
4. In the **Getting started** pane, choose one of two options.
   - **No storage account required**: an ephemeral session. This is the fastest. Files you save are deleted when the session ends. Select your subscription in the dropdown, then select **Apply**.
   - **Mount storage account**: your files stay between sessions. Select your subscription in the dropdown, then select **Apply**. In the **Mount storage account** pane, select **We will create a storage account for you**, then **Next**. Azure creates a new resource group and a storage account. Regular storage costs apply.
5. For this lab, either choice works. If you are unsure, choose **No storage account required**. You can switch later.
6. If Cloud Shell stops with an error about a resource provider, the **Microsoft.CloudShell** provider is not registered. A resource provider is the part of Azure behind one service. To fix it, search for **Subscriptions**, select your subscription, then under **Settings** select **Resource providers**. Search `cloudshell`, select **Microsoft.CloudShell**, and select **Register**. You do this once per subscription. If you did Lab 1, it is already done.

Check: a Cloud Shell pane opens in the portal with a Bash prompt, and it accepts typing.

## Steps with the Azure CLI

Azure CLI is a command-line tool for managing Azure. You type `az` to run it. Run these in the Cloud Shell Bash window you just opened.

**The shape of a command.** Commands are organised as command groups, and each group is an area of an Azure service. A command is `az`, then the group, then often a subgroup, then the action, then parameters that start with `--`. Example: `az account show`. The group is `account`, the action is `show`. For `az vm availability-set --help`, `vm` is the group and `availability-set` is a subgroup.

**1. Check the version.**

```bash
az version
```

Cloud Shell comes with the latest Azure CLI preinstalled. For your own PC, use 2.76 or later.

**2. See who and where you are.** Always check your subscription before you do anything else.

```bash
az account show
```

Read the `name` (the subscription) and `tenantId` fields. `isDefault: true` means this is the active subscription. Make sure it is your test subscription.

**3. List the subscriptions you can use, as a table.**

```bash
az account list --output table
```

`--output table` prints a readable table instead of the default JSON. Other formats are `json`, `jsonc`, `tsv`, `yaml`, `yamlc` and `none`. Some fields, like `id`, `type` and `etag`, are not shown in table output.

**4. Change the active subscription (only if you have more than one).**

```bash
az account set --subscription "<subscription name or ID>"
```

Run `az account show` again to confirm. Cloud Shell remembers your subscription for later sessions in `/home/<user>/.azure/azureProfile.json`.

**5. List resource groups.** A resource group is a container for Azure resources. A new subscription may have none, and then the table is empty.

```bash
az group list --output table
```

**6. Pick only the fields you want with `--query`.** `--query` runs a JMESPath query on the result, which is a small language for filtering JSON. These two examples show the shape:

```bash
az account show --query "{tenantId:tenantId, subscriptionid:id}"
az account list --query "[?isDefault].name"
```

The first returns only the tenant ID and subscription ID. The second returns only the name of the default subscription. Query names are case sensitive. Quote rules differ between shells, so copy these exactly in Cloud Shell Bash. On Windows PowerShell you may need different quotes.

**7. Find commands and read help.**

```bash
az find vm
az vm --help
az vm create --help
```

`az find` searches for command names. `--help` lists subgroups, parameters and examples. Reading help is safe: `az vm create --help` shows how the command works and does not create anything.

Check: `az account show` shows your test subscription, `az account list --output table` prints a table, and `az group list --output table` prints a table or an empty result without an error.

### Install Azure CLI on your own Windows PC

You do not need this to finish the lab, but you will want it later.

1. Open PowerShell and run:

   ```powershell
   winget install --exact --id Microsoft.AzureCLI
   ```

   WinGet is available by default on Windows 11 and modern versions of Windows 10. If it is missing, Learn offers the MSI installer instead. For 64-bit Windows, download it from `https://aka.ms/installazurecliwindowsx64` and run it.
2. Close and reopen the terminal window. Learn says this is required.
3. Check the version. You want 2.76 or later.

   ```powershell
   az version
   ```

   To update later, run `az upgrade`.
4. Sign in the normal way:

   ```powershell
   az login
   ```

   If the CLI can open your default browser, it opens an Azure sign-in page. Sign in and complete MFA. Do not add `--use-device-code`. Learn lists it only as the option when no web browser is available.
5. Check where you landed:

   ```powershell
   az account show
   ```

Check: `az version` shows 2.76 or later, and `az account show` shows your test subscription after browser sign-in.

### How mandatory MFA affects the CLI

Azure requires MFA for user accounts that sign in to Azure CLI, Azure PowerShell, the Azure mobile app, infrastructure-as-code tools and REST API endpoints to create, update or delete resources. Read operations do not need MFA. Enforcement started gradually on October 1, 2025. Test tenants are included, and there is no opt-out. Break glass accounts are included too.

What you see: if you signed in without MFA, you can still run read commands like the ones above. If you then try to create, update or delete something, the command returns an error that says you need to sign in with MFA. With Azure CLI 2.76.0 or later the error is more informative and prints an `az login` command with a `--claims-challenge` value. Run `az logout`, then run that exact command and complete MFA in the browser. Older versions (2.75.0 or earlier) show less helpful errors, which is why 2.76 or later is recommended. Service principals and managed identities are not affected, but they are for automation, not for you typing commands.

## Terraform

No Terraform in this lab, because nothing is deployed. Terraform comes in [Lab 10: Terraform basics](/azure-basics-labs/terraform-basics/).

## Check that it works

- `az version` runs, in Cloud Shell and (if you installed it) on your PC.
- `az account show` names your test tenant's subscription and you can tell it apart from any other subscription.
- `az account list --output table` and `az group list --output table` give tables.
- `az find vm` and `az vm --help` print help text.

## The most common mistake

Running commands against the wrong subscription. The Azure CLI uses whichever subscription is marked default. Run `az account show` first every time you open a new session, and fix it with `az account set --subscription` before you create anything in later labs.

A second one: copying a command from a web page and pasting it without reading it. Read what the action word is. `show`, `list` and `--help` only read. `create`, `update` and `delete` change things.

## Clean up

No commands in this lab created anything, so there is nothing to delete, except what the storage option may have made.

- If you chose **Mount storage account**, Azure created a resource group (Learn's example shows a name like `cloud-shell-storage-southcentralus`) with a storage account and an Azure Files share. Keep it if you plan to keep using Cloud Shell with saved files. It is a 5-GB file share, and regular storage costs apply.
- Do not delete the Cloud Shell resource group, storage account or file share by accident. Learn warns that deleting a resource group, storage account or file share that is mapped to Cloud Shell erases your `$HOME` directory disk image and the files in the share. This cannot be undone. The storage account is tagged `ms-resource-usage:azure-cloud-shell`, which helps you recognise it.
- To stop using the file share, run `clouddrive unmount` in Cloud Shell and confirm the prompts. This does not delete anything. The file share continues to exist until you delete it manually, and Cloud Shell asks you to set up storage again at the next session. Only delete the old share after you have copied out anything you need.
- To clear files, delete them from inside Cloud Shell. Learn says files in the `clouddrive` folder also show in the portal under Storage browser.
- Keep for later labs: your test tenant and subscription, and Azure CLI on your PC. Close Cloud Shell when you are done. A session times out after 20 minutes without interactive activity.

## Where this is used in AVD

Many AVD setup and check steps can be done with an Azure CLI command, so you will use what you practised here. Start with [Prepare your Azure environment for AVD](/azure-virtual-desktop/prepare-your-azure-environment/).

## Next lab

[Lab 3: Resource group, tags and budget](/azure-basics-labs/resource-group-tags-budget/) uses what you learned here to create your first resource group and a cost alert.

## Sources

- [What is Azure Cloud Shell?](https://learn.microsoft.com/en-us/azure/cloud-shell/overview)
- [Get started with Azure Cloud Shell ephemeral sessions](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/ephemeral)
- [Get started with Azure Cloud Shell using persistent storage](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/new-storage)
- [Persist files in Azure Cloud Shell](https://learn.microsoft.com/en-us/azure/cloud-shell/persisting-shell-storage)
- [Get started with Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)
- [Prepare your environment for the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-tutorial-1-prepare-environment)
- [Install the Azure CLI on Windows](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows)
- [Output formats for Azure CLI commands](https://learn.microsoft.com/en-us/cli/azure/format-output-azure-cli)
- [How to query Azure CLI command output using a JMESPath query](https://learn.microsoft.com/en-us/cli/azure/query-azure-cli)
- [Troubleshooting Azure CLI](https://learn.microsoft.com/en-us/cli/azure/use-azure-cli-successfully-troubleshooting)
- [Mandatory multifactor authentication for Azure and admin portals](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mandatory-multifactor-authentication)
