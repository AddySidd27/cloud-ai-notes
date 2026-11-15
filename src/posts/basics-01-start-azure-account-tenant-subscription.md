---
title: "Start safely: Azure free account, tenant and subscription"
seoTitle: "Azure free account: tenant vs subscription, step by step"
layout: post.njk
permalink: "/azure-basics-labs/start-azure-account-tenant-subscription/"
order: 311
tags: [azure-basics-lab]
deck: "A free Azure account in a separate test tenant, with the tenant and subscription names read, the free-account limits understood and the Azure Virtual Desktop resource providers registered."
description: "Create a free Azure account in a test tenant, learn tenant vs subscription, know the $200 and 30-day limits, and register the resource providers AVD needs."
---

By the end you will have a free Azure account in a test tenant. You will be able to tell a tenant from a subscription, you will know what the free account does after 30 days, and you will have switched on (registered) the Azure services that Azure Virtual Desktop (AVD) needs later.

## What you need

- Nothing before this. It is the first lab in the series.
- A new email address that is only for testing. Do not use your work email.
- A phone that can receive a text message or a call, for identity verification.
- A credit or debit card. Virtual and prepaid cards are often refused, so use a normal card.
- About 40 minutes. Cost: nothing, if you stay inside the free account limits.
- Role: none to start with. You sign up, so the account is yours. If the **Register** button in step 5 is grayed out later, you do not have permission to register providers.

If you ever had an Azure subscription before, the free trial may not be available to you. Microsoft limits the free trial to people who are new to Azure. In that case a pay-as-you-go subscription is the other route, and you pay for what you use.

## Safety first

- Use a test tenant only. Never run these labs in your employer's tenant or any tenant you do not own.
- Before every change, read the tenant name and the subscription name on screen. This is the stop check, and you will repeat it as a habit.
- Azure asks for multifactor authentication (MFA) when you sign in to manage Azure. Do not try to turn it off. There is no exception, even for a test tenant.
- Your card is only charged if you upgrade to pay-as-you-go. Ignore any **Upgrade** banner in the portal.
- Register only the providers listed in this lab. Register a provider only when you are ready to use it, so do not register everything.

## What the lab builds

![Diagram: Subscription, tenant and resource providers.](/img/basics/start-azure-account-tenant-subscription.svg)

*Source: Microsoft Learn pages listed under Sources.*

## Steps in the Azure portal

### 1. Sign up for the free account

Two ideas first.

**Free account limits.**

- You get $200 of credit for the first 30 days. Credit you do not use in that time is lost.
- After 30 days, or when the credit runs out, your subscription and services are disabled until you upgrade to pay-as-you-go. Your card is not charged unless you upgrade.
- After you upgrade you still get some services free for 12 months, and you pay only for use beyond them.
- Before you upgrade, delete any resources you no longer need, so that you do not pay for them.

**Why a separate tenant.** A tenant is your own private directory of people and sign-in settings. Microsoft calls this service Microsoft Entra ID (the Microsoft sign-in service). Each tenant is separate from the others. The safe route is to sign up with a brand-new email that is not tied to any work tenant, in a private browser window so you are not signed in to anything else. Step 2 shows you the tenant name, so you can check what you got.

1. Open a private (InPrivate or incognito) browser window.
2. Go to the Azure free account page: [azure.microsoft.com/pricing/purchase-options/azure-account](https://azure.microsoft.com/pricing/purchase-options/azure-account). Find the button that starts the free account sign-up. Its label may change over time.
3. Sign in with a Microsoft account that is only for testing. If you have none, look for a link such as **Create one** on the sign-in page and make a new account. If the page shows a work or school address you know, stop and use a private window again.
4. Complete the sign-up pages: your details, identity verification by phone, identity verification by card, and the agreement. Allow a few minutes for the phone code. Internet phone numbers (such as Google Voice) are often refused, so use a normal mobile number. If you get no text message, try the call option. The card check may show a small temporary hold that goes away by itself.
5. When sign-up ends, open the [Azure portal](https://portal.azure.com) and sign in.

Expect a new tenant with a name you do not recognize from work, and a domain that ends in `.onmicrosoft.com`. If you see your employer's name, close the window and start again in a private window with a different email.

You can stop here and finish the rest tomorrow. Sign-up with phone and card checks often takes 20 minutes.

### 2. Find the tenant name and ID (stop check)

A tenant is the directory that holds identities. The subscription is where Azure resources and role assignments are managed, and the tenant is the directory that holds the identities used to sign in.

1. In the Azure portal, search for **Microsoft Entra ID** and open it.
2. On the **Overview** page, look for the **Basic information** section. It shows the tenant name, the **Tenant ID** and the primary domain (a name ending in `.onmicrosoft.com`). Write the name and the ID in a text note. If a label looks different on your screen, use the next step.
3. In the left menu, select **Properties** and scroll down to **Tenant ID**. Check that it matches the one you wrote down.
4. Select the **Settings** icon in the top bar, then **Directories + subscriptions**. The **Current directory** is the tenant you are signed in to. If you ever have more than one directory, the **Switch** button changes it.

The tenant ID is sometimes called the directory ID. They are the same thing.

### 3. Find the subscription name and ID (stop check)

A subscription is where your resources live and where the bill goes. Every Azure resource belongs to one subscription. A subscription trusts exactly one tenant. One tenant can be trusted by many subscriptions. A subscription is not tied to a region.

1. In the portal, search for **Subscriptions** and open it.
2. Find the subscription that the sign-up created. It may be called Free Trial or Azure subscription 1; the name on your screen may differ. Write down its name and its **Subscription ID**. The list has a column for the ID.
3. Select the subscription name. On the page that opens, read the top section. Check that it is the subscription you expect.

Check: your notes sheet (at the end of step 5) has a tenant name, tenant ID, subscription name and subscription ID, and the tenant ID matches the one on the Entra ID page. If the list is empty, or you do not see the right subscription, you may be in a different directory. Switch directories (step 2.4).

**Make this a habit.** Before you start any lab and before any change, do both checks: the tenant name and ID under Microsoft Entra ID, and the subscription name on the Subscriptions page. If either one is not your test tenant, stop.

### 4. Know what a region is

A region is a set of datacenters in one area, joined by a fast network. When you create most resources, you pick a region. Pick one close to your users, because distance adds delay. For AVD, the delay between the user and the region (round-trip time) should be under 150 milliseconds, and the virtual network must be in the same region as the session host. The subscription itself is not in a region, but the resources inside it are.

Pick the region closest to you that is on the region list in [Prerequisites for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites). That list shows where AVD can store its data. Write the region name on your notes sheet (step 5). Every later lab says "your region". That means this one.

The portal shows a region as, for example, East US 2. Commands use another spelling, `eastus2` (lower case, no spaces). Write both on your notes sheet. The CLI section below has a command that lists the spellings.

### 5. Register the resource providers

A resource provider is the part of Azure behind one service. For example, Microsoft.KeyVault is the provider behind Key Vault. Registering it sets up your subscription to use that service. Register a provider only when you are ready to use it, because unneeded registrations can add apps you do not recognize to your tenant. When you create a resource in the portal, the portal usually registers the provider for you. You register them here so that later labs do not stop on a registration error. Some providers may already show **Registered**. That is fine, and you can skip those.

You need permission to register a provider (`*/register/action`). The Owner and Contributor roles include it.

1. In the portal, open **Subscriptions** and select your subscription.
2. Under **Settings**, select **Resource providers**.
3. In the search box, type **Microsoft.DesktopVirtualization**. Select it and select **Register**.
4. Repeat for each of these, one at a time:
   - Microsoft.Compute (virtual machines)
   - Microsoft.Network (virtual networks, network security groups)
   - Microsoft.Storage (storage accounts and Azure Files)
   - Microsoft.KeyVault (Key Vault)
   - Microsoft.OperationalInsights (Log Analytics)
   - Microsoft.Insights (Azure Monitor)
   - Microsoft.CloudShell (needed to start Cloud Shell, used in the next lab and in the CLI part below)
5. Refresh the list. Wait until each one shows **Registered**. Registering can take a short while. It is fine if one still says **Registering** for a minute.

Check: you can say which one is the directory and which one holds the bill, and each provider above shows **Registered**.

### Your notes sheet

Copy this into a text note and fill it in. Every later lab asks for one of these lines.

```text
Tenant name:
Tenant domain (.onmicrosoft.com):
Tenant ID:
Subscription name:
Subscription ID:
Region name in the portal (for example East US 2):
Region name for commands (for example eastus2):
Sign-up date, and the date 30 days later:
```

## Steps with the Azure CLI

This part is optional. It does the same registration as step 5, by command. Use it or the clicks in step 5, not both. The next lab sets up Cloud Shell and the Azure CLI properly. Here you use Cloud Shell only to read your context and to register and check providers.

Cloud Shell needs the Microsoft.CloudShell provider from step 5 to be registered first. Select the Cloud Shell icon in the top bar of the portal (a small box with `>_`). If it asks which shell, choose **Bash**. In the **Getting started** pane, choose **No storage account required**, pick your subscription and select **Apply**. Do not use `az login --use-device-code`. Cloud Shell is already signed in for you.

Command blocks in this series are Bash unless they say otherwise. Run them in Cloud Shell (Bash), not in PowerShell.

Show the subscription and tenant that Cloud Shell is using:

```bash
az account show --query "{subscription:name, subscriptionId:id, tenantId:tenantId}" --output table
```

Compare the three values with your notes from steps 2 and 3. They must match. If they do not, stop and find out why before you go on.

Register the providers and check one of them:

```bash
for p in Microsoft.DesktopVirtualization Microsoft.Compute Microsoft.Network Microsoft.Storage Microsoft.KeyVault Microsoft.OperationalInsights Microsoft.Insights Microsoft.CloudShell
do
  az provider register --namespace $p
done

az provider show --namespace Microsoft.DesktopVirtualization --query "{RegistrationState:registrationState}"
```

You can run `az provider register` again for a provider that is already registered. It does no harm. Registration can take a moment, so run the `show` command again if it says `Registering`. The other providers register the same way. Check them in the portal list from step 5.

To see the command spelling of your region, run this and find your region in the list. Write both names on your notes sheet:

```bash
az account list-locations --query "[].{Name:displayName, CLI:name}" --output table
```

Check: `az account show` prints your test subscription and tenant ID, and `az provider show` prints `Registered`.

## Terraform

No Terraform in this lab, because creating the account and the tenant is done by you in a browser, and the provider registration is a one-time click.

## Check that it works

- Microsoft Entra ID > Overview shows your test tenant name and ID.
- Subscriptions shows the subscription from your sign-up, and you can read its name and ID.
- Resource providers lists Microsoft.DesktopVirtualization and the others as **Registered**.
- You can say in one sentence each: what a tenant is, what a subscription is, what a region is. Compare with this: a tenant is the directory of identities. A subscription is where resources live and the bill goes, and it trusts one tenant. A region is the place where resources are physically hosted.
- You can say what happens at 30 days: the subscription and services are disabled until you upgrade. Use an upgrade only when you want to pay for Azure. Your notes sheet has the date 30 days after sign-up.

## The most common mistake

Working in the wrong tenant. If you are also signed in to a work account, the portal may open the work directory, and everything you create lands there. Always read the tenant name and the subscription name first. Use a private browser window or a separate browser profile for the test account.

How to spot it: the organization name next to your profile picture at the top right is your employer's, or the Subscriptions list shows subscriptions you do not recognize. Close everything, open a private window and sign in again.

## Clean up

There is nothing to delete in this lab. Keep everything: the account, the tenant, the subscription and the registered providers. All later labs use them.

## Where this is used in AVD

If the Microsoft.DesktopVirtualization provider is not registered, creating an AVD host pool fails with a registration error. You have already done that step. AVD users also have to exist in the Microsoft Entra tenant you just read. See [Prepare your Azure environment](/azure-virtual-desktop/prepare-your-azure-environment/).

## Next lab

[Azure Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) adds a working command line, so you can read and change things by command as well as by click.

## Sources

- [Avoid charges with your Azure free account](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/avoid-charges-free-account)
- [Associate or add an Azure subscription to your Microsoft Entra tenant](https://learn.microsoft.com/en-us/entra/fundamentals/how-subscriptions-associated-directory)
- [Get subscription and tenant IDs in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-portal/get-subscription-tenant-id)
