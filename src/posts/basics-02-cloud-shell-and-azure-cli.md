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

By the end you will have run your first Azure commands in the browser, and you will know how to install the Azure CLI on a Windows PC and sign in. Every command in this lab only reads information, so nothing is created or changed.

## What you need

- [Start safely: Azure free account, tenant and subscription](/azure-basics-labs/start-azure-account-tenant-subscription/). You need a test tenant and a subscription you can sign in to, and the notes sheet you made at the end of step 5 there. That step also registered the Microsoft.CloudShell provider, which Cloud Shell needs.
- A modern browser. For the local install part, a Windows PC.
- Time: about 30 minutes.
- Cost: nothing. You use the option without a storage account.
- Role: any role that can sign in and read the subscription is enough. On your own free account you already have that.

## Safety first

- This lab uses Cloud Shell without a storage account (an "ephemeral" session). Files you save in it are deleted when the session ends, and nothing is billed. Cloud Shell can also keep your files in a storage account, which costs money. You do not need that in this series.
- Use a throwaway test tenant, never your employer's tenant. Before any change, read the tenant and subscription name that `az account show` prints.
- Only read commands in this lab: `show`, `list` and `--help`. No `create`, `update` or `delete`.
- Do not sign in with `az login --use-device-code`. Use the normal `az login`, which opens a browser.
- Azure already requires multifactor authentication (MFA) for Azure management. Do not plan around turning it off. There is no opt-out.

## What the lab builds

![Left to right: you sign in to the Azure portal and open Cloud Shell (Bash), which sends az commands to your test subscription. A gray, optional path below shows the Azure CLI on your own PC, signed in with az login, used for the Terraform lab.](/img/basics/cloud-shell-and-azure-cli.svg)

*Based on the pages listed under Sources. Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

No resources are deployed. You only connect and read.

## Steps in the Azure portal

Cloud Shell is a terminal that runs in your browser. Microsoft manages it, and it signs you in automatically. The Azure CLI is already installed in it.

1. Sign in to the [Azure portal](https://portal.azure.com/) with your test account. Complete the MFA prompt.
2. In the top bar, select the **Cloud Shell** icon (a small box with `>_`).
3. The first time, you are asked which shell to use. Select **Bash**.
4. In the **Getting started** pane, choose **No storage account required**. Select your subscription in the dropdown, then select **Apply**. Use this option for the whole series. The other option, **Mount storage account**, keeps your files but creates a billed storage account, and you do not need it here.
5. If Cloud Shell stops with an error about a resource provider, the **Microsoft.CloudShell** provider is not registered. A resource provider is the part of Azure behind one service. To fix it, search for **Subscriptions**, select your subscription, then under **Settings** select **Resource providers**. Search `cloudshell`, select **Microsoft.CloudShell**, and select **Register**. You do this once per subscription. If you registered the providers in the first lab, it is already done.

Check: a Cloud Shell pane opens in the portal with a Bash prompt, and it accepts typing.

## Steps with the Azure CLI

Azure CLI is a command-line tool for managing Azure. You type `az` to run it. Run these in the Cloud Shell Bash window you just opened.

Command blocks are Bash unless they say otherwise. Run them in Cloud Shell (Bash). They do not work in PowerShell on your PC. The only PowerShell blocks are the PC install part of this lab and the Terraform lab, and they are marked.

**The shape of a command.** Commands are organized as command groups, and each group is an area of an Azure service. A command is `az`, then the group, then often a subgroup, then the action, then parameters that start with `--`. Example: `az account show`. The group is `account`, the action is `show`.

**Command 1. Check the version.**

```bash
az version
```

Cloud Shell comes with the latest Azure CLI preinstalled.

**Command 2. See who and where you are.** Always check your subscription before you do anything else.

```bash
az account show
```

The output looks like this, with your own values:

```text
{
  "environmentName": "AzureCloud",
  "id": "<your subscription ID>",
  "isDefault": true,
  "name": "Azure subscription 1",
  "tenantId": "<your tenant ID>",
  ...
}
```

Compare `name`, `id` and `tenantId` with your notes sheet from the first lab. They must match your test subscription and test tenant. If they do not, stop. `isDefault: true` means this is the active subscription.

**Command 3. List the subscriptions you can use, as a table.**

```bash
az account list --output table
```

`--output table` prints a readable table instead of the default JSON. Other formats are `json`, `jsonc`, `tsv`, `yaml`, `yamlc` and `none`. Some fields, like `id`, `type` and `etag`, are not shown in table output.

**Command 4. Change the active subscription (only if you have more than one).**

```bash
az account set --subscription "YOUR-SUBSCRIPTION-NAME-OR-ID"
```

Replace the text in capitals and keep the quotes. Run `az account show` again to confirm. Cloud Shell remembers your subscription choice for later sessions in `/home/<user>/.azure/azureProfile.json`. Your files are not remembered.

**Command 5. List resource groups.** A resource group is a container for Azure resources. A new subscription may have none. Then the command prints nothing, or `[]`, and that is a correct result.

```bash
az group list --output table
```

**Command 6. Pick only the fields you want with `--query`.** `--query` runs a JMESPath query on the result, which is a small language for filtering JSON. This example returns only the tenant ID and the subscription ID. Later labs use the same shape:

```bash
az account show --query "{tenantId:tenantId, subscriptionId:id}"
```

Query names are case sensitive. Copy the quotes exactly, and type them in plain form, not as curly quotes.

**Command 7. Read help.**

```bash
az vm create --help
```

`--help` lists subgroups, parameters and examples. Reading help is safe: `az vm create --help` shows how the command works and does not create anything.

**Variables.** From the resource group lab on, command blocks start with lines such as `LOCATION=eastus2`. Cloud Shell forgets your variables after about 20 minutes without activity. If a command complains about an empty value, paste the variable block again.

Check: `az account show` shows your test subscription, `az account list --output table` prints a table, and `az group list --output table` prints a table or an empty result without an error.

### Install Azure CLI on your own Windows PC (optional until the Terraform lab)

Only the Terraform lab needs the CLI on your own PC. You can skip this part for now. These steps are for Windows. On macOS or Linux use the install page for your system: [Install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

1. Open PowerShell and run:

   ```powershell
   winget install --exact --id Microsoft.AzureCLI
   ```

   WinGet is available by default on Windows 11 and modern versions of Windows 10. If it is missing, Microsoft offers the MSI installer instead. For 64-bit Windows, download it from `https://aka.ms/installazurecliwindowsx64` and run it.
2. Close and reopen the terminal window. Microsoft says this is required.
3. Check the version. Use Azure CLI 2.76 or later, so that a missing-MFA error shows you the command to run.

   ```powershell
   az version
   ```

   To update later, run `az upgrade`.
4. Sign in the normal way:

   ```powershell
   az login
   ```

   If the CLI can open your default browser, it opens an Azure sign-in page. Sign in and complete MFA. Do not add `--use-device-code`. It is only meant for machines with no web browser.
5. Check where you landed:

   ```powershell
   az account show
   ```

Check: `az version` shows 2.76 or later, and `az account show` shows your test subscription after browser sign-in.

### Azure asks for MFA when you change things

Azure asks for MFA when you create, change or delete things with the CLI. Reading is fine. If a create command later fails with an error that asks for MFA, run `az logout`, then run the `az login` command that the error prints (it ends with `--claims-challenge`), and approve MFA in the browser. Use CLI 2.76 or later so the error shows that command.

## Terraform

No Terraform in this lab, because nothing is deployed. Terraform comes in [Terraform basics](/azure-basics-labs/terraform-basics/).

## Check that it works

- `az version` runs, in Cloud Shell and (if you installed it) on your PC.
- `az account show` names your test tenant's subscription and you can tell it apart from any other subscription.
- `az account list --output table` and `az group list --output table` give tables.
- `az vm create --help` prints help text.

## The most common mistake

Running commands against the wrong subscription. The Azure CLI uses whichever subscription is marked default. Run `az account show` first every time you open a new session, and fix it with `az account set --subscription` before you create anything in later labs.

A second one: pasting a Bash command into PowerShell, or a command whose quotes a web page or chat app changed to curly quotes. Type `bash` in Cloud Shell, or paste into a plain text file first to check.

A third one: copying a command from a web page and pasting it without reading it. Read what the action word is. `show`, `list` and `--help` only read. `create`, `update` and `delete` change things.

## Clean up

Nothing to delete, because no command in this lab created anything. Close the Cloud Shell pane. A session ends after 20 minutes without interactive activity.

Keep for later labs: your test tenant and subscription, and Cloud Shell access.

**Only if you chose Mount storage account.** Azure created a resource group with a storage account and an Azure Files share (a 5-GB file share), and regular storage costs apply. Do not delete that resource group, storage account or file share by accident. Deleting one that is mapped to Cloud Shell erases your `$HOME` directory disk image and the files in the share, and this cannot be undone. To stop using the share, run `clouddrive unmount` in Cloud Shell and confirm the prompts. That does not delete anything.

## Where this is used in AVD

In AVD work you will use `az` to check what is deployed in a subscription, and you will read the output the way you just did. Start with [Prepare your Azure environment for AVD](/azure-virtual-desktop/prepare-your-azure-environment/).

## Next lab

[Resource group, tags, budget and action group](/azure-basics-labs/resource-group-tags-budget/) uses what you learned here to create your first resource group and a cost alert.

## Sources

- [What is Azure Cloud Shell?](https://learn.microsoft.com/en-us/azure/cloud-shell/overview)
- [Get started with Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)
- [Install the Azure CLI on Windows](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows)
