---
title: "Terraform Basics: Build a Resource Group and Network from Code"
seoTitle: "Terraform Basics on Azure: Plan, Apply, State and Destroy"
layout: post.njk
permalink: "/azure-basics-labs/terraform-basics/"
order: 320
tags: [azure-basics-lab]
deck: "Write a small Terraform project that builds a resource group, a virtual network, a subnet and a network security group, then plan, apply, change a tag and destroy it."
description: "Beginner Terraform lab for Azure: install Terraform on Windows, build a resource group, network, subnet and NSG, read the plan, then destroy it."
---

By the end you will have written a small Terraform project that builds a resource group called `rg-azb-tf`, a virtual network called `vnet-azb-tf` (10.20.0.0/16), one subnet and one network security group. You will read a plan, apply it, look at the state file, change a tag to see an in-place update, and destroy everything.

Copy each file exactly: a missing brace is the most common error. If `terraform validate` or `terraform plan` prints an error, read the first error line. It names the file and line to fix. If you need to search for it, add the word `azurerm`. Do not continue to `terraform apply` until both `validate` and `plan` end without errors.

**This lab uses a different order from the others.** Terraform is the main part, and the portal only shows you what Terraform built. That check makes sense only after `terraform apply`, so it sits in the middle of the Terraform section, not at the start. Sign-in comes first because Terraform needs it.

## What you need

- An Azure subscription from [the free account lab](/azure-basics-labs/start-azure-account-tenant-subscription/). The Azure free account gives $200 of credit for 30 days.
- A Windows PC. (On macOS or Linux the Terraform install differs. This lab covers Windows.)
- The Azure CLI on that PC, version 2.76 or newer, installed as in the part "Install Azure CLI on your own Windows PC" of [Azure Cloud Shell and Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) (macOS and Linux readers use the install page linked there). Cloud Shell is not used here. This is the lab where you run `az` in PowerShell on your own PC; the other labs run `az` in Bash in Cloud Shell.
- The notes sheet from [the free account lab](/azure-basics-labs/start-azure-account-tenant-subscription/), for your subscription ID and region.
- A role that can create resources in the subscription, such as Contributor.
- Do [Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/) and [Network security group](/azure-basics-labs/network-security-group/) first. This lab builds the same kinds of resources from code. It uses new names, so it does not clash with them.
- A text editor. Any editor works.
- About 90 minutes. The lab is built in two passes, so you can stop between them. Virtual networks and network security groups have no charge of their own, and this lab creates no VM. Destroy everything at the end anyway.

**Do the lab in this order:**

1. Sign in with the Azure CLI and copy your subscription ID.
2. Install Terraform and write the project files.
3. Pass 1: build only the resource group (init, validate, plan, apply).
4. Check it in the Azure portal.
5. Pass 2: add the network, subnet, network security group and the link between them (plan, apply). Check the portal again.
6. Look at the state, change a tag, plan and apply.
7. Destroy everything.

## Safety first

- Use a test tenant, not your employer's. Read the tenant and subscription name before you apply anything.
- Azure already requires multifactor authentication (MFA) for Azure management work, including create, update and delete from the CLI and from tools such as Terraform. Run `az login` with a user who has MFA registered. If you are asked for MFA at sign-in, that is expected.
- Use `az login` and nothing else. Do not use the device code option. Do not create a password or a client secret for Terraform. This lab stores no secrets.
- Read the plan before you apply it. `terraform apply` changes real resources. Before every apply, read the last line of the plan. If it says anything is destroyed that you did not expect, stop.
- Do not commit `terraform.tfstate` or your `terraform.tfvars` file to Git. The Terraform section explains why.
- Everything here lives in `rg-azb-tf` only. `rg-azb-core` and `rg-azb-lab` (with the resources from the virtual network and NSG labs) are not touched. Destroy deletes only what this project created.

## What the lab builds

![Diagram: Terraform builds a resource group, network, subnet and NSG.](/img/basics/terraform-basics.svg)

*Source: Microsoft Learn pages listed under Sources.*

## Steps with the Azure CLI

Only two commands here. Terraform does the work, and the Azure CLI only gives it a sign-in. Run them in PowerShell on your Windows PC.

Sign in. A browser window opens. Use the same account as in the portal, and finish MFA if you are asked.

```powershell
az login
```

Show which subscription you are in. Terraform will use this subscription, so read the name.

```powershell
az account show --query "{name:name, id:id, tenant:tenantId}" -o table
```

Check: the name and tenant are your test ones. Copy the `id` value. It goes into `terraform.tfvars` later. If it is the wrong subscription, run `az account set --subscription "<id or name>"` and show it again. `az account set` and `az account show` are described in [Authenticate to Azure with a Microsoft account](https://learn.microsoft.com/en-us/azure/developer/terraform/authenticate/authenticate-to-azure-with-microsoft-account).

## Terraform

### Install Terraform on Windows

Terraform is a program that reads text files that describe cloud resources, and then builds, changes or deletes the resources to match. The files are written in a language called HCL, and they end in `.tf`.

The Windows install is also described in [Install Terraform on Windows with Azure PowerShell](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/get-started-windows-powershell). That page is older, so use HashiCorp's current download page instead.

1. Go to HashiCorp's install page, `https://developer.hashicorp.com/terraform/install`, and download the Windows package. Pick **Windows, AMD64**. It is right for almost all PCs.
2. Extract `terraform.exe` from the download to a folder you choose, for example `C:\terraform`.
3. Add that folder to your PATH. PATH is the list of folders Windows searches when you type a command. Press the Windows key, type `environment variables` and open **Edit the system environment variables**. Select **Environment Variables**. Under **User variables**, select **Path**, then **Edit**, **New**, type `C:\terraform`, and select **OK** three times.
4. Close all PowerShell windows and open a new one. Run `terraform -version`.

If you prefer, `winget` can do steps 1 to 3. Run `winget search terraform` and look for the package from HashiCorp. Its ID is usually `Hashicorp.Terraform`. Check the ID in the search result before you install.

Check: `terraform -version` prints a version number, and that version is 1.9.0 or newer. The code in this lab says `>= 1.9.0, < 2.0.0`. (The 4.x provider itself needs Terraform 1.0 or newer; this lab asks for more so that you start from a current release.) If PowerShell says that `terraform` is not recognized, the PATH entry is missing or the old PowerShell window is still open. Close all PowerShell windows, open a new one and try again. If it still fails, open the **Path** list again and check that the folder name is exactly right.

### How Terraform signs in to Azure

The azurerm provider is the plugin that lets Terraform talk to Azure. There are several ways to authenticate Terraform to Azure: a Microsoft account through the Azure CLI, a service principal, and a managed identity. This lab uses the first one. That is what you did with `az login`. The provider then uses that sign-in, so no password or secret is written in any file. The only thing you put in the code is the subscription ID, which says which subscription to work in. That ID is not a secret, but it is still yours, so it goes in `terraform.tfvars` and not in the committed code.

### The project files

Make an empty folder, for example `C:\azb\terraform-basics`, and open it in your editor. Create the files below in this one folder. Terraform reads every `.tf` file in the folder together, so the file names are only for your own tidiness. The project has `versions.tf`, `providers.tf`, `variables.tf`, `outputs.tf` and `main.tf`, plus two files for your values.

`versions.tf` says which Terraform version and which provider version to use. `~> 4.0` means any 4.x release of the provider. For a project you keep, pin a version you have checked on the Terraform Registry.

```hcl
terraform {
  required_version = ">= 1.9.0, < 2.0.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}
```

`providers.tf` configures the provider. The empty `features {}` block is required by azurerm, even when you set nothing in it. The subscription ID is needed for a plan or apply (it can come from this setting, an environment variable or the Azure CLI default), and not for `terraform validate`. This lab sets it in the code, so there is no guessing.

```hcl
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
```

`variables.tf` lists the values you can change. A variable is a named input. The ones without a default (`subscription_id` and `location`) must be given a value in `terraform.tfvars`.

```hcl
variable "subscription_id" {
  description = "ID of the Azure subscription to build in."
  type        = string
}

variable "location" {
  description = "Azure region. Use the same region as your other labs."
  type        = string
}

variable "tags" {
  description = "Tags put on the resource group, the virtual network and the network security group."
  type        = map(string)
  default = {
    env    = "lab"
    series = "azure-basics"
  }
}
```

`outputs.tf` prints values after an apply. For now it has one output. You add a second one in Pass 2.

```hcl
output "resource_group_name" {
  description = "Name of the resource group."
  value       = azurerm_resource_group.tf.name
}
```

`main.tf` holds the resources. In Pass 1 it holds only the resource group. Each block has a type (such as `azurerm_resource_group`), a local name (such as `tf`) and a body. A reference like `azurerm_resource_group.tf.name` reads a value from another block. That is how Terraform knows what to build first.

```hcl
resource "azurerm_resource_group" "tf" {
  name     = "rg-azb-tf"
  location = var.location
  tags     = var.tags
}
```

### Your values and the Git ignore file

Create `terraform.tfvars.example`. This one is safe to commit, because it holds only placeholders.

```hcl
subscription_id = "00000000-0000-0000-0000-000000000000"
location        = "eastus2" # example only. Use your own region.
```

In PowerShell, in the project folder, copy it:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Open `terraform.tfvars` and replace the zero ID with your subscription ID (from `az account show`) and `eastus2` with your own region, in the CLI spelling from your notes sheet. Use the same region as in your other labs.

Create `.gitignore`. If you will never put this folder in Git, you can skip this file. If you ever do, these lines keep your values and the state out of it.

```text
.terraform/
*.tfstate
*.tfstate.*
*.tfplan
*.tfvars
!terraform.tfvars.example
```

The `.terraform.lock.hcl` file that Terraform creates is not in this list on purpose. It records the exact provider version, and people usually commit it.

### Pass 1: format, initialize and validate

Run these in PowerShell, in the project folder.

```powershell
terraform fmt
terraform init
terraform validate
```

- `terraform fmt` tidies the spacing of your files. It prints the names of files it changed.
- `terraform init` downloads the azurerm provider into a hidden `.terraform` folder and creates the lock file. Run it once per folder, and again when you change provider versions.
- `terraform validate` checks that the code is well formed and that the arguments exist. It does not talk to Azure.

Check: `init` ends with a success message, and `validate` ends with a line saying the configuration is valid. If `validate` complains, it names the file and line.

### Pass 1: plan and apply

A plan is Terraform's preview. It compares your code with what exists and lists what it would do. Save it to a file so that apply does exactly this and nothing else.

```powershell
terraform plan -out main.tfplan
```

Read the symbols at the start of each line:

- `+` means Terraform will create this resource.
- `~` means Terraform will change this resource in place. It stays, and one or more values change.
- `-` means Terraform will destroy this resource.
- `-/+` means Terraform will destroy it and create it again. Some changes cannot be made in place.

Check: the plan lists one resource with `+`, and ends with a line like `Plan: 1 to add, 0 to change, 0 to destroy.` Values that Azure decides, such as the IDs, show as `(known after apply)`. Nothing exists in Azure yet.

```powershell
terraform apply main.tfplan
```

Because you give it the saved plan, it does not ask you to type `yes`. If you run `terraform apply` with no plan file, it makes a new plan and asks for `yes`.

If apply stops with an error that says you need to sign in with MFA, follow the part of the Cloud Shell and Azure CLI lab called "Azure asks for MFA when you change things" (`az logout`, then the `az login` command from the error), then run the apply again.

Check: it ends with a line like `Apply complete! Resources: 1 added, 0 changed, 0 destroyed.` and prints your output.

### Check in the Azure portal (after apply)

You create nothing in the portal in this lab. The portal is where you check what Terraform built. Come back here after Pass 2, and again after the tag change.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the tenant and subscription name.
2. Search for and open **Resource groups**. Open `rg-azb-tf`.
3. On the Overview page, look at the resource list and the tags.

Check: after Pass 1, `rg-azb-tf` exists and is empty. Its tags are `env = lab` and `series = azure-basics`. These are the defaults in `variables.tf`. Resources you create with Terraform look the same as ones you create by hand.

Now run `terraform plan` once more with no changes.

Check: the plan says `No changes. Your infrastructure matches the configuration.` That is the sign that code, state and Azure agree.

Check: you can stop here. If you stop, run `terraform destroy` (see Clean up) so nothing is left behind, and start Pass 2 later from the same folder.

### Pass 2: add the network, subnet and network security group

Now add the rest to `main.tf`. Add this below the resource group block. This is the point of Terraform: it compares the new code with what exists and only adds what is missing.

```hcl
resource "azurerm_virtual_network" "tf" {
  name                = "vnet-azb-tf"
  location            = azurerm_resource_group.tf.location
  resource_group_name = azurerm_resource_group.tf.name
  address_space       = ["10.20.0.0/16"]
  tags                = var.tags
}

resource "azurerm_subnet" "app" {
  name                 = "snet-azb-tf-app"
  resource_group_name  = azurerm_resource_group.tf.name
  virtual_network_name = azurerm_virtual_network.tf.name
  address_prefixes     = ["10.20.1.0/24"]
}

resource "azurerm_network_security_group" "app" {
  name                = "nsg-azb-tf-app"
  location            = azurerm_resource_group.tf.location
  resource_group_name = azurerm_resource_group.tf.name
  tags                = var.tags
}

resource "azurerm_subnet_network_security_group_association" "app" {
  subnet_id                 = azurerm_subnet.app.id
  network_security_group_id = azurerm_network_security_group.app.id
}
```

The network security group has no rules of your own. Azure adds its default rules to every network security group, and the NSG lab shows what they are. The last block joins the group to the subnet. It is a separate resource in Terraform. So four blocks give four new resources, and with the resource group that makes five.

Add a second output to `outputs.tf`, below the first one:

```hcl
output "subnet_id" {
  description = "Resource ID of the subnet."
  value       = azurerm_subnet.app.id
}
```

Run:

```powershell
terraform fmt
terraform validate
terraform plan -out main.tfplan
```

Check: the plan lists four resources with `+`, and ends with a line like `Plan: 4 to add, 0 to change, 0 to destroy.` The resource group is not in the list, because it already exists.

```powershell
terraform apply main.tfplan
```

Check: it ends with a line like `Apply complete! Resources: 4 added, 0 changed, 0 destroyed.` and prints your two outputs.

Now go back to the portal. Open `rg-azb-tf` and look at the resource list. You should see the virtual network `vnet-azb-tf` and the network security group `nsg-azb-tf-app`. The subnet is inside the virtual network, so it is not listed on its own. The link between the network security group and the subnet does not show as its own item either. Open `vnet-azb-tf`, then under **Settings** select **Subnets**.

Check: `rg-azb-tf` holds `vnet-azb-tf` and `nsg-azb-tf-app`. The subnet `snet-azb-tf-app` shows the address range 10.20.1.0/24 and `nsg-azb-tf-app` as its network security group. The tags are `env = lab` and `series = azure-basics`.

### Look at the state

Terraform keeps a record of what it built, in a file called `terraform.tfstate` in your folder. This is the state. Terraform reads it on every plan to match your code to the real resources. Without it, Terraform would not know that `rg-azb-tf` already exists.

```powershell
terraform state list
terraform show
```

`state list` prints one line for each resource Terraform manages. `show` prints a lot, so scroll to the top and check the resource names. You do not have to read it all. You can open `terraform.tfstate` in your editor too, but never edit it by hand.

Why you do not commit it: the state file is plain text, and it can hold values that are secret, such as passwords and keys, for resources that have them. This lab has none, but the habit matters. A state file also goes out of date the moment someone else changes the folder. Teams keep state in a shared remote place instead. That is beyond this lab.

### Change a tag and see an in-place update

Open `terraform.tfvars`. Add this block on a new line at the very end of the file, outside any quotes. It changes `env` from `lab` to `test` and adds one more tag, `owner`. Save the file.

```hcl
tags = {
  env    = "test"
  series = "azure-basics"
  owner  = "me"
}
```

Make a new plan. A plan file is tied to the state it was made from, so make a fresh one instead of reusing `main.tfplan`.

```powershell
terraform plan -out main.tfplan
```

Check: the plan shows `~` on the resource group, the virtual network and the network security group. Inside each one, a `~ tags` line shows `env` changing from `"lab"` to `"test"`, and `+ owner` appearing. The subnet and the association are not listed, because they have no tags. The last line reads like `Plan: 0 to add, 3 to change, 0 to destroy.` Nothing has `-/+`. A tag change updates the resource and does not rebuild it.

Apply it.

```powershell
terraform apply main.tfplan
```

Check: in the portal, the tags on `rg-azb-tf` now show `env = test` and `owner = me`. These are the values from `terraform.tfvars`.

You can learn something else from this without running it. If you changed the name of the virtual network, or its region, the plan would show `-/+`, because Azure does not allow that change on an existing resource. This is why you read the plan before you apply. A `-` or `-/+` on something you care about is the line to stop at.

Run `terraform plan` once more with no changes.

Check: the plan says `No changes. Your infrastructure matches the configuration.`

### Errors you may see

| What you see | What to do |
|---|---|
| `terraform` is not recognized | The PATH entry is missing or the old PowerShell window is still open. See "Install Terraform on Windows". |
| An error about a missing value for `subscription_id` or `location` | `terraform.tfvars` is missing, has another name, or is in another folder. It must be called exactly `terraform.tfvars` and sit next to the `.tf` files. |
| An error that says to run `az login`, or that it cannot build the account | Run `az login` again and `az account show`. Check that the subscription is the right one. |
| An error that asks for MFA, or mentions a claims challenge | `az logout`, then the `az login` command from the error. See the Cloud Shell lab, "Azure asks for MFA when you change things". |
| An error that names a resource provider that is not registered | Read the message and the provider name it gives, then register that provider as shown in the free account lab. |

## Check that it works

- `terraform validate` says the configuration is valid.
- Pass 1 ended with 1 added, and Pass 2 with 4 added.
- In the portal, `rg-azb-tf` holds `vnet-azb-tf` and `nsg-azb-tf-app`, and the subnet `snet-azb-tf-app` shows the network security group.
- After the tag change, the plan showed `~` and `3 to change`, and the portal shows the new tags.
- A plan with no code changes says `No changes`.

## The most common mistake

Changing resources in the portal while Terraform manages them. Terraform only knows what the state file says, and on the next plan it tries to put things back the way your code says. For example, if you add a tag to `rg-azb-tf` by hand and then run `terraform plan`, the plan shows a `~` to remove it. The rule: when Terraform builds a resource, change it only in the code.

The next most common mistake is committing `terraform.tfstate` or `terraform.tfvars` to Git. Use the `.gitignore` above before your first commit.

## Clean up

Destroy everything this project built.

```powershell
terraform destroy
```

Terraform shows a plan with `-` on all five resources and ends with a line like `Plan: 0 to add, 0 to change, 5 to destroy.` (If you stopped after Pass 1, it says 1.) Read it. Type `yes` only if every name starts with `rg-azb-tf`, `vnet-azb-tf`, `snet-azb-tf` or `nsg-azb-tf`.

Check: it ends with a line like `Destroy complete! Resources: 5 destroyed.` In the portal, `rg-azb-tf` is gone from the Resource groups list. Select **Refresh** if it is still shown.

**Keep these for later labs:**

- `rg-azb-core` and what is in it.
- `rg-azb-lab` and the resources from the virtual network and NSG labs. This lab did not touch them.
- The Terraform project folder, if you want to reuse the code. Delete `terraform.tfstate` and `main.tfplan` when you are done, or keep the folder out of Git.

Nothing in this lab is needed by the next lab.

## Try it yourself (optional)

Terraform is taught only in this lab, so the earlier labs point here. Each block below rebuilds something from the RBAC, virtual network or NSG labs in code. If `terraform validate` or `plan` reports an error, fix the file and line it names.

How to use them: make a new empty folder for each one. Copy `versions.tf`, `providers.tf`, `variables.tf` and `terraform.tfvars` from this lab into it, add the block as a new file, run `terraform init`, `terraform plan` and `terraform apply`, and read the plan first. The blocks read `rg-azb-lab` as an existing group (a `data` block reads something that already exists). Use Terraform instead of the portal or CLI steps, not on top of them. If the resource already exists from the earlier lab, delete it first, or Terraform reports that it already exists. Destroy each folder when you are done.

**The virtual network and subnet.** Create the resource group `rg-azb-lab` first (portal or CLI).

```hcl
data "azurerm_resource_group" "lab" {
  name = "rg-azb-lab"
}

resource "azurerm_virtual_network" "azb" {
  name                = "vnet-azb"
  address_space       = ["10.10.0.0/16"]
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
}

resource "azurerm_subnet" "vm" {
  name                 = "snet-vm"
  resource_group_name  = data.azurerm_resource_group.lab.name
  virtual_network_name = azurerm_virtual_network.azb.name
  address_prefixes     = ["10.10.1.0/24"]
}
```

The portal makes a private subnet. This block does not set the outbound setting. Tools that use an earlier API version keep the older default, which allows default outbound access. After apply, open the subnet in the portal and read **Default outbound access**. If you want the subnet private, look in the `azurerm_subnet` page of the provider documentation for an argument named `default_outbound_access_enabled`, and check its name and default there before you add it.

**The network security group on the subnet.** Get the subnet ID and put it in `terraform.tfvars` as `subnet_id = "..."`.

```powershell
az network vnet subnet show --resource-group rg-azb-lab --vnet-name vnet-azb --name snet-vm --query id -o tsv
```

```hcl
variable "subnet_id" {
  description = "Resource ID of snet-vm from the virtual network lab"
  type        = string
}

data "azurerm_resource_group" "lab" {
  name = "rg-azb-lab"
}

resource "azurerm_network_security_group" "vm" {
  name                = "nsg-azb-vm"
  location            = data.azurerm_resource_group.lab.location
  resource_group_name = data.azurerm_resource_group.lab.name
}

resource "azurerm_subnet_network_security_group_association" "vm" {
  subnet_id                 = var.subnet_id
  network_security_group_id = azurerm_network_security_group.vm.id
}
```

The plan must show two resources to add. This block has no RDP rule, because that rule was temporary. If you later run `terraform destroy` in this folder, it removes the NSG and detaches it from the subnet.

**The two role assignments.** Get the group's object ID with `az ad group show --group "TestUsers" --query id -o tsv` and put it in `terraform.tfvars` as `group_object_id = "..."`.

```hcl
variable "group_object_id" {
  description = "Object ID of the group TestUsers (from az ad group show)."
  type        = string
}

data "azurerm_subscription" "current" {}

data "azurerm_resource_group" "core" {
  name = "rg-azb-core"
}

resource "azurerm_role_assignment" "reader_sub" {
  scope                = data.azurerm_subscription.current.id
  role_definition_name = "Reader"
  principal_id         = var.group_object_id
  principal_type       = "Group"
}

resource "azurerm_role_assignment" "contributor_rg" {
  scope                = data.azurerm_resource_group.core.id
  role_definition_name = "Contributor"
  principal_id         = var.group_object_id
  principal_type       = "Group"
}
```

The plan must show two assignments to add and nothing else. `terraform destroy` in this folder removes both assignments, which is the clean-up for the RBAC lab.

## Where this is used in AVD

An Azure Virtual Desktop deployment is many resources that must match: host pool, session hosts, network and more. Terraform lets you build them from one folder of code, and rebuild them the same way again. The [Terraform AVD lab](/terraform-labs/avd-quick-lab/) uses the same commands you just practised: init, plan, apply and destroy.

## Next lab

[Your PC and Remote Desktop clients](/azure-basics-labs/your-pc-and-remote-desktop-clients/) gets your own computer ready to connect to a desktop in Azure.

## Sources

- [Install Terraform on Windows with Azure PowerShell](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/get-started-windows-powershell)
- [Authenticate Terraform to Azure](https://learn.microsoft.com/en-us/azure/developer/terraform/authenticate-to-azure)
- [azurerm provider documentation on the Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
