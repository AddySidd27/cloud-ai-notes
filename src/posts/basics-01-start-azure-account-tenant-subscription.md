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
By the end you will have a free Azure account in a test tenant. You will be able to tell a tenant from a subscription, you will know what the free account does after 30 days, and you will have registered the resource providers that Azure Virtual Desktop (AVD) uses.

I have not run these steps in a live tenant for this article. The steps follow Microsoft Learn.

## What you need

- No earlier lab. This is lab 1.
- A new email address that is only for testing. Do not use your work email.
- A phone that can receive a text message or a call, for identity verification.
- A credit or debit card. Microsoft says virtual and prepaid cards are not accepted.
- About 30 minutes. Cost: nothing, if you stay inside the free account limits.
- Role: none to start with. You sign up, so the account is yours. If the **Register** button in step 5 is greyed out later, you do not have permission to register providers.

If you ever had an Azure subscription before, the free trial may not be available to you. Microsoft limits the free trial to people who are new to Azure. In that case a pay-as-you-go subscription is the other route, and you pay for what you use.

## Safety first

- Use a test tenant only. Never run these labs in your employer's tenant or any tenant you do not own.
- Before every change, read the tenant name and the subscription name on screen. This is the stop check, and you will repeat it as a habit.
- Azure asks for multifactor authentication (MFA) when you sign in to manage Azure. Do not try to turn it off. For a test tenant too, Microsoft says there is no exception.
- Budgets only send alerts. They never stop anything. The free account itself stops services when the credit ends, but a budget does not.
- Register only the providers listed in this lab. Microsoft says to register a provider only when you are ready to use it, so do not register everything.

## What the lab builds

![A tenant box on the left that holds a subscription box. Inside the subscription are the registered resource providers, and a region label shows where resources will be placed.](/img/basics/start-azure-account-tenant-subscription.svg)

*Source: [Associate or add an Azure subscription to your Microsoft Entra tenant](https://learn.microsoft.com/en-us/entra/fundamentals/how-subscriptions-associated-directory), [Azure resource providers and types](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types), [What are Azure regions?](https://learn.microsoft.com/en-us/azure/reliability/regions-overview). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

### 1. Sign up for the free account

Two ideas first.

**Free account limits.** You get $200 of credit for the first 30 days, in your billing currency. After that you can use only a limited amount of some services, free for 12 months. Credit you do not use in the 30 days is lost. The $200 does not cover third-party Marketplace purchases. When the credit runs out, or when 30 days pass, your subscription and services are disabled. To keep using Azure you must upgrade the account to pay-as-you-go. After you upgrade you still get the free services for 12 months, and you pay only for use beyond them. One warning from Microsoft: if you used resources that are not free, the subscription got disabled, and you then upgrade, those resources are enabled again and you are charged for them. So delete what you do not need before you upgrade.

**Why a separate tenant.** A tenant is your own copy of Microsoft Entra ID. It holds the users, groups and sign-in settings. Each tenant is separate from the others. Microsoft says the Entra "create a tenant" feature is for paid customers only, and that people with a free tenant or a trial subscription cannot create extra tenants there. Their advice for a new tenant is to sign up for a free account. So the safe route is simple: sign up with a brand-new email that is not tied to any work tenant, in a private browser window so you are not signed in to anything else. Learn says that when you activate a subscription, your identity is either tied to an organization's tenant or a new directory is created for it. Step 2 shows you the tenant name, so you can check what you got.

1. Open a private (InPrivate or incognito) browser window.
2. Go to the Azure free account page: [azure.microsoft.com/pricing/purchase-options/azure-account](https://azure.microsoft.com/pricing/purchase-options/azure-account). Find the button that starts the free account sign-up. Its label may change over time.
3. Sign in with your new test email, or create a Microsoft account for it. If the page shows a work or school address you know, stop and use a private window again.
4. Complete the four parts of sign-up: About you, identity verification by phone, identity verification by card, and the Agreement. Allow up to four minutes for the phone code. Internet phone numbers (VoIP) do not work. If you get no text message, try the **Call me** option. The card check may show a small temporary hold. Microsoft says it is removed within three to five days.
5. When sign-up ends, open the [Azure portal](https://portal.azure.com) and sign in.

### 2. Find the tenant name and ID (stop check, part 1)

A tenant is the directory that holds identities. Microsoft's own way to say it: the subscription is where Azure resources and role assignments are managed, and the tenant is the directory that holds the identities used to sign in.

1. In the Azure portal, search for **Microsoft Entra ID** and open it.
2. On the **Overview** page, look for the **Basic information** section. It shows the tenant name, the **Tenant ID** and the primary domain (a name ending in `.onmicrosoft.com`). Write the name and the ID in a text note. If a label looks different on your screen, use the next step.
3. In the left menu, select **Properties** and scroll down to **Tenant ID**. Check that it matches the one you wrote down.
4. Select the **Settings** icon in the top bar, then **Directories + subscriptions**. The **Current directory** is the tenant you are signed in to. If you ever have more than one directory, the **Switch** button changes it.

The tenant ID is sometimes called the directory ID. They are the same thing.

### 3. Find the subscription name and ID (stop check, part 2)

A subscription is where your resources live and where the bill goes. Every Azure resource belongs to one subscription. A subscription trusts exactly one tenant. One tenant can be trusted by many subscriptions. A subscription is not tied to a region.

1. In the portal, search for **Subscriptions** and open it.
2. Find the subscription that the sign-up created. Learn calls it the Free Trial subscription, but the name on your screen may differ. Write down its name and its **Subscription ID**. The list has a column for the ID.
3. Select the subscription name. On the page that opens, read the top section. Check that it is the subscription you expect.

If the list is empty, or you do not see the right one, you may be in a different directory. Switch directories (step 2.4).

**Make this a habit.** Before you start any lab and before any change, do both checks: the tenant name and ID under Microsoft Entra ID, and the subscription name on the Subscriptions page. If either one is not your test tenant, stop.

### 4. Know what a region is

A region is a set of datacenters in one area, joined by a fast network. When you create most resources, you pick a region. Pick one close to your users, because distance adds delay. For AVD, Microsoft says the round-trip time from the user to the region should be under 150 ms, and that the virtual network must be in the same region as the session host. The subscription itself is not in a region, but the resources inside it are.

For these labs, choose one region and use it every time. Check that it is on the region list in [Prerequisites for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites). That list shows where AVD can store host pool data. Session hosts can be in any region. The same page says West US 3 is not supported for automated host pools.

### 5. Register the resource providers

A resource provider is the part of Azure behind one service. For example, Microsoft.KeyVault is the provider behind Key Vault. Registering it sets up your subscription to use that service. Microsoft says to register a provider only when you are ready to use it, and that unneeded registrations can add apps you do not recognise to your tenant. When you create a resource in the portal, the portal usually registers the provider for you. I register them here so that later labs do not stop on a registration error. Some providers may already show **Registered**. That is fine, and you can skip those.

You need permission to register a provider (`*/register/action`). Learn says the Owner and Contributor roles include it.

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
   - Microsoft.CloudShell (needed to start Cloud Shell, used in Lab 2 and in the CLI part below)
5. Refresh the list. Wait until each one shows **Registered**. Registering can take a short while. It is fine if one still says **Registering** for a minute.

Check: the tenant name and ID are written down, the subscription name and ID are written down, you can say which one is the directory and which one holds the bill, and each provider above shows **Registered**.

## Steps with the Azure CLI

This part is optional. It does the same registration as step 5, by command. If you finished step 5, you can read it and move on. Lab 2 sets up Cloud Shell and the Azure CLI properly. Here you use Cloud Shell only to read your context and to register and check providers.

Cloud Shell needs the Microsoft.CloudShell provider from step 5 to be registered first. Open Cloud Shell with the icon in the top bar of the portal. If it asks which shell, choose **Bash**. In the **Getting started** pane, choose **No storage account required**, pick your subscription and select **Apply**. Do not use `az login --use-device-code`. Cloud Shell is already signed in for you.

Show the subscription and tenant that Cloud Shell is using:

```bash
az account show --query "{subscription:name, subscriptionId:id, tenantId:tenantId}" --output table
```

Compare the three values with your notes from steps 2 and 3. They must match. If they do not, stop and find out why before you go on.

Register the providers and check one of them:

```bash
for p in Microsoft.DesktopVirtualization Microsoft.Compute Microsoft.Network Microsoft.Storage Microsoft.KeyVault Microsoft.OperationalInsights Microsoft.Insights
do
  az provider register --namespace $p
done

az provider show --namespace Microsoft.DesktopVirtualization --query "{RegistrationState:registrationState}"
```

You can run `az provider register` again for a provider that is already registered. It does no harm. Registration can take a moment, so run the `show` command again if it says `Registering`. The other providers register the same way. Check them in the portal list from step 5.

Check: `az account show` prints your test subscription and tenant ID, and `az provider show` prints `Registered`.

## Terraform

No Terraform in this lab, because creating the account and the tenant is done by you in a browser, and the provider registration is a one-time click.

## Check that it works

- Microsoft Entra ID > Overview shows your test tenant name and ID.
- Subscriptions shows the subscription from your sign-up, and you can read its name and ID.
- Resource providers lists Microsoft.DesktopVirtualization and the others as **Registered**.
- You can say in one sentence each: what a tenant is, what a subscription is, what a region is.
- You can say what happens at 30 days: the subscription and services are disabled until you upgrade. Use an upgrade only when you want to pay for Azure.

## The most common mistake

Working in the wrong tenant. If you are also signed in to a work account, the portal may open the work directory, and everything you create lands there. Always read the tenant name and the subscription name first. Use a private browser window or a separate browser profile for the test account.

## Clean up

There is nothing to delete in this lab. Keep everything: the account, the tenant, the subscription and the registered providers. All later labs use them.

Do not delete the tenant while you still want to do the labs. If you later stop using the test tenant, Learn's way to remove it is to switch to that directory, open **Microsoft Entra ID**, and select **Delete directory** on the Overview page. Azure may refuse and tell you why. Follow what it says. Do this only for the test tenant, after you have read its name.

## Where this is used in AVD

AVD needs an Azure subscription with the Microsoft.DesktopVirtualization provider registered, and users who exist in Microsoft Entra ID. See [Prepare your Azure environment](/azure-virtual-desktop/prepare-your-azure-environment/).

## Next lab

[Lab 2: Cloud Shell and the Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) adds a working command line, so you can read and change things by command as well as by click.

## Sources

- [Avoid charges with your Azure free account](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/avoid-charges-free-account)
- [Create services included with Azure free account](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/create-free-services)
- [Reactivate a disabled Azure subscription](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/subscription-disabled)
- [Upgrade your Azure free account](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/upgrade-azure-subscription)
- [Troubleshoot issues when you sign up for a new account](https://learn.microsoft.com/en-us/azure/cost-management-billing/troubleshoot-subscription/troubleshoot-azure-sign-up)
- [Quickstart: Create a new tenant in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/fundamentals/create-new-tenant)
- [Associate or add an Azure subscription to your Microsoft Entra tenant](https://learn.microsoft.com/en-us/entra/fundamentals/how-subscriptions-associated-directory)
- [How to find your Microsoft Entra tenant ID](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-find-tenant)
- [Get subscription and tenant IDs in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-portal/get-subscription-tenant-id)
- [Manage Azure portal settings and preferences](https://learn.microsoft.com/en-us/azure/azure-portal/set-preferences)
- [Azure resource providers and types](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types)
- [Resource providers for Azure services](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-services-resource-providers)
- [What are Azure regions?](https://learn.microsoft.com/en-us/azure/reliability/regions-overview)
- [Prerequisites for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)
- [Get started with Azure Cloud Shell ephemeral sessions](https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/ephemeral)
- [Mandatory multifactor authentication for Azure and admin portals](https://learn.microsoft.com/en-us/entra/identity/authentication/concept-mandatory-multifactor-authentication)
- [az account](https://learn.microsoft.com/en-us/cli/azure/account)
- [Change directory tenants with your Azure subscriptions](https://learn.microsoft.com/en-us/azure/devtest/offer/how-to-change-directory-tenants-visual-studio-azure)
