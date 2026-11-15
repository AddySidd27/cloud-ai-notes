---
title: "Terraform Basics: Build a Resource Group and Network from Code"
seoTitle: "Terraform Basics on Azure: Plan, Apply, State and Destroy"
layout: post.njk
permalink: "/azure-basics-labs/terraform-basics/"
order: 320
tags: [azure-basics-lab]
deck: "Write a small Terraform project that builds a resource group, a virtual network, a subnet and a network security group, then plan, apply, change a tag and destroy it."
description: "A beginner Terraform lab for Azure: install Terraform on Windows, sign in with the Azure CLI, build a resource group, virtual network, subnet and NSG, read the plan, and destroy it."
---

By the end you will have written a small Terraform project that builds a resource group called `rg-azb-tf`, a virtual network called `vnet-azb-tf` (10.20.0.0/16), one subnet and one network security group. You will read a plan, apply it, look at the state file, change a tag to see an in-place update, and destroy everything.

I have not run these steps in a live tenant for this article. I have also not run `terraform validate` or `terraform plan` on this code. The install and sign-in steps follow Microsoft Learn (Microsoft's documentation site). The resource arguments are checked against the azurerm provider documentation for version 4.81.0. Run `terraform validate` first and read any error it gives.

Most labs in this series go portal first, then Azure CLI, then Terraform. This one is different. Terraform is the main part of this lab. The portal section only checks the result, and the CLI section only covers sign-in and the version check.

## What you need

- An Azure subscription from [Lab 1](/azure-basics-labs/start-azure-account-tenant-subscription/). The Azure free account gives $200 of credit for 30 days.
- The Azure CLI installed on your Windows PC, version 2.76 or newer. [Lab 2: Cloud Shell and the Azure CLI](/azure-basics-labs/cloud-shell-and-azure-cli/) shows the install. Cloud Shell is not used here.
- A role that can create resources in the subscription, such as Contributor.
- [Lab 8: Virtual network and subnet](/azure-basics-labs/virtual-network-subnet/) and [Lab 9: Network security group](/azure-basics-labs/network-security-group/) are useful, because here you build the same kinds of resources from code. This lab uses new names, so it does not clash with them.
- A text editor. Any editor works.
- About 45 minutes. Learn says there is no charge for using Azure Virtual Network, and this lab creates no VM. I found no price for a network security group on Learn. Destroy everything at the end anyway.

## Safety first

- Use a test tenant, not your employer's. Read the tenant and subscription name before you apply anything.
- Azure already requires multifactor authentication (MFA) for Azure management work, including create, update and delete from the CLI and from tools such as Terraform. If you are asked for it at sign-in, that is expected.
- Use `az login` and nothing else. Do not use the device code option. Do not create a password or a client secret for Terraform. This lab stores no secrets.
- Read the plan before you apply it. `terraform apply` changes real resources.
- Do not commit `terraform.tfstate` or your `terraform.tfvars` file to Git. The Terraform section explains why.
- Everything here lives in `rg-azb-tf` only. `rg-azb-core` and `rg-azb-lab` (with the resources from Labs 8 and 9) are not touched. Destroy deletes only what this project created.

## What the lab builds

![Terraform code in a local folder is read by the Terraform program on your PC, which signs in to Azure through the Azure CLI. Terraform builds the resource group rg-azb-tf. Inside it are the virtual network vnet-azb-tf with address space 10.20.0.0/16, a subnet inside the network, and a network security group joined to the subnet. Terraform also writes a local state file that records what it built.](/img/basics/terraform-basics.svg)

*Source: Learn pages [Quickstart: Install and configure Terraform](https://learn.microsoft.com/en-us/azure/developer/terraform/quickstart-configure), [Install Terraform on Windows with Azure PowerShell](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/get-started-windows-powershell) and [Authenticate Terraform to Azure](https://learn.microsoft.com/en-us/azure/developer/terraform/authenticate-to-azure). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/).*

## Steps in the Azure portal

You create nothing in the portal in this lab. The portal is where you check what Terraform built. Come back here after `terraform apply` in the Terraform section, and again after you change the tag and after you destroy.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the tenant and subscription name.
2. Search for and open **Resource groups**. Open `rg-azb-tf`.
3. On the Overview page, look at the resource list. You should see the virtual network `vnet-azb-tf` and the network security group `nsg-azb-tf-app`. The subnet is inside the virtual network, so it is not listed on its own.
4. Open `vnet-azb-tf`. Under **Settings**, select **Subnets**. You should see `snet-azb-tf-app` with the address range 10.20.1.0/24 and `nsg-azb-tf-app` as its network security group.
5. Back on the resource group, check the tags on the Overview page.

Check: all three resources are there, the subnet shows the network security group, and the tags match your `terraform.tfvars` file. Resources you create with Terraform look the same as ones you create by hand.

## Steps with the Azure CLI

Only three commands here. Terraform does the work, and the Azure CLI only gives it a sign-in. Run them in PowerShell on your Windows PC.

Sign in. A browser window opens. Use the same account as in the portal, and finish MFA if you are asked.

```powershell
az login
```

Show which subscription you are in. Terraform will use this subscription, so read the name.

```powershell
az account show --query "{name:name, id:id, tenant:tenantId}" -o table
```

Check: the name and tenant are your test ones. Copy the `id` value. It goes into `terraform.tfvars`. If it is the wrong subscription, run `az account set --subscription "<id or name>"` and show it again. Learn describes `az account set` and `az account show` on the page [Authenticate to Azure with a Microsoft account](https://learn.microsoft.com/en-us/azure/developer/terraform/authenticate/authenticate-to-azure-with-microsoft-account).

When Terraform is installed (next section), check it with:

```powershell
terraform -version
```

## Terraform

### Install Terraform on Windows

Terraform is a program that reads text files that describe cloud resources, and then builds, changes or deletes the resources to match. The files are written in a language called HCL, and they end in `.tf`.

Learn describes the Windows install in [Install Terraform on Windows with Azure PowerShell](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/get-started-windows-powershell). The steps are:

1. Download Terraform from the [Terraform downloads page](https://www.terraform.io/downloads.html), which is the link Learn gives. Pick the Windows package that fits your PC. Most PCs need the AMD64 one.
2. Extract the executable (`terraform.exe`) from the download to a folder you choose, for example `C:\terraform`.
3. Update your system's PATH environment variable to include that folder (Learn's wording: the directory that contains the executable). Close and reopen PowerShell so it picks up the change.
4. Run `terraform -version`.

Check: it prints a version number, and that version is 1.9.0 or newer. The code in this lab says `>= 1.9.0, < 2.0.0`. The Learn page says it was tested with Terraform 1.1.4, which is old, so use the current version from the download page, not the one in the Learn text.

### How Terraform signs in to Azure

The azurerm provider is the plugin that lets Terraform talk to Azure. Learn lists several ways to authenticate Terraform to Azure: a Microsoft account through the Azure CLI, a service principal, and a managed identity. This lab uses the first one. That is what you did with `az login`. The provider then uses that sign-in, so no password or secret is written in any file. The only thing you put in the code is the subscription ID, which says which subscription to work in. That ID is not a secret, but it is still yours, so it goes in `terraform.tfvars` and not in the committed code.

### The project folder

Make an empty folder, for example `C:\azb\terraform-basics`, and open it in your editor. Create the files below. All of them go in the same folder. Terraform reads every `.tf` file in the folder together, so the file names are only for your own tidiness.

`versions.tf` says which Terraform version and which provider version to use. Pinning the provider version means the code runs the same way next month.

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

`providers.tf` configures the provider. The empty `features {}` block is required by azurerm, even when you set nothing in it. The provider documentation says the subscription ID is needed for a plan or apply (it can come from this setting, an environment variable or the Azure CLI default), and not for `terraform validate`. This lab sets it in the code, so there is no guessing.

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
    env = "lab"
    lab = "10"
  }
}
```

`main.tf` holds the four resources. Each block has a type (such as `azurerm_resource_group`), a local name (such as `tf`) and a body. A reference like `azurerm_resource_group.tf.name` reads a value from another block. That is how Terraform knows to build the resource group first.

```hcl
resource "azurerm_resource_group" "tf" {
  name     = "rg-azb-tf"
  location = var.location
  tags     = var.tags
}

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

The network security group has no rules of your own. Azure adds its default rules to every network security group, and Lab 9 shows what they are. The last block joins the group to the subnet. It is a separate resource in Terraform.

`outputs.tf` prints values after an apply.

```hcl
output "resource_group_name" {
  description = "Name of the resource group."
  value       = azurerm_resource_group.tf.name
}

output "subnet_id" {
  description = "Resource ID of the subnet."
  value       = azurerm_subnet.app.id
}
```

### Your values and the Git ignore file

Create `terraform.tfvars.example`. This one is safe to commit, because it holds only placeholders.

```hcl
subscription_id = "00000000-0000-0000-0000-000000000000"
location        = "eastus2" # example only. Use your own region.
```

Copy it to a new file called `terraform.tfvars`, and put your own subscription ID (from `az account show`) and your own region in it. Use the same region as in your other labs.

Create `.gitignore`. If you ever put this folder in Git, these lines keep your values and the state out of it.

```text
.terraform/
*.tfstate
*.tfstate.*
*.tfplan
*.tfvars
!terraform.tfvars.example
```

The `.terraform.lock.hcl` file that Terraform creates is not in this list on purpose. It records the exact provider version, and people usually commit it.

### Format, initialise and validate

Run these in PowerShell, in the project folder.

```powershell
terraform fmt
terraform init
terraform validate
```

- `terraform fmt` tidies the spacing of your files. It prints the names of files it changed.
- `terraform init` downloads the azurerm provider into a hidden `.terraform` folder and creates the lock file. Run it once per folder, and again when you change provider versions.
- `terraform validate` checks that the code is well formed and that the arguments exist. It does not talk to Azure.

Check: `init` ends with a success message, and `validate` ends with a line saying the configuration is valid. I have not run these commands on this code. If `validate` complains, it names the file and line.

### Plan

A plan is Terraform's preview. It compares your code with what exists and lists what it would do. Save it to a file so that apply does exactly this and nothing else.

```powershell
terraform plan -out main.tfplan
```

Read the symbols at the start of each line:

- `+` means Terraform will create this resource.
- `~` means Terraform will change this resource in place. It stays, and one or more values change.
- `-` means Terraform will destroy this resource.
- `-/+` means Terraform will destroy it and create it again. Some changes cannot be made in place.

Check: the plan lists five resources with `+`, and ends with a line like `Plan: 5 to add, 0 to change, 0 to destroy.` Values that Azure decides, such as the IDs, show as `(known after apply)`. Nothing exists in Azure yet.

### Apply

```powershell
terraform apply main.tfplan
```

Because you give it the saved plan, it does not ask you to type `yes`. If you run `terraform apply` with no plan file, it makes a new plan and asks for `yes`.

Check: it ends with a line like `Apply complete! Resources: 5 added, 0 changed, 0 destroyed.` and prints your two outputs. Now go to the portal steps above and look at `rg-azb-tf`.

### Look at the state

Terraform keeps a record of what it built, in a file called `terraform.tfstate` in your folder. This is the state. Terraform reads it on every plan to match your code to the real resources. Without it, Terraform would not know that `rg-azb-tf` already exists.

```powershell
terraform state list
terraform show
```

`state list` prints one line for each resource Terraform manages. `show` prints every value of every resource, as Terraform last saw them. You can open `terraform.tfstate` in your editor too, but never edit it by hand.

Why you do not commit it: the state file is plain text, and it can hold values that are secret, such as passwords and keys, for resources that have them. This lab has none, but the habit matters. A state file also goes out of date the moment someone else changes the folder. Teams keep state in a shared remote place instead. That is beyond this lab.

### Change a tag and see an in-place update

Open `terraform.tfvars` and add a `tags` line at the end. Change `env` from `lab` to `test`, and add one more tag:

```hcl
tags = {
  env   = "test"
  lab   = "10"
  owner = "me"
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

Check: in the portal, the tags on `rg-azb-tf` now show `env = test` and `owner = me`.

You can learn something else from this without running it. If you changed the name of the virtual network, or its region, the plan would show `-/+`, because Azure does not allow that change on an existing resource. This is why you read the plan before you apply. A `-` or `-/+` on something you care about is the line to stop at.

Run `terraform plan` once more with no changes. The plan should say that there are no changes and that your infrastructure matches the configuration. That is the sign that code, state and Azure agree.

## Check that it works

- `terraform validate` says the configuration is valid.
- `terraform apply` ended with 5 added.
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

Terraform shows a plan with `-` on all five resources and ends with a line like `Plan: 0 to add, 0 to change, 5 to destroy.` Read it. Type `yes` only if every name starts with `rg-azb-tf`, `vnet-azb-tf`, `snet-azb-tf` or `nsg-azb-tf`.

Check: it ends with a line like `Destroy complete! Resources: 5 destroyed.` In the portal, `rg-azb-tf` is gone from the Resource groups list. Select **Refresh** if it is still shown.

**Keep these for later labs:**

- `rg-azb-core` and what is in it.
- `rg-azb-lab` and the resources from Labs 8 and 9. This lab did not touch them.
- The Terraform project folder, if you want to reuse the code. Delete `terraform.tfstate` and `main.tfplan` when you are done, or keep the folder out of Git.

Nothing in this lab is needed by Lab 11.

## Where this is used in AVD

An Azure Virtual Desktop deployment is many resources that must match: host pool, session hosts, network and more. Terraform lets you build them from one folder of code, and rebuild them the same way again. The [Terraform AVD lab](/terraform-labs/avd-quick-lab/) uses the same steps you just practised: init, plan, apply, and destroy.

## Next lab

[Lab 11: Your PC and Remote Desktop clients](/azure-basics-labs/your-pc-and-remote-desktop-clients/) gets your own computer ready to connect to a desktop in Azure.

## Sources

- [Quickstart: Install and configure Terraform](https://learn.microsoft.com/en-us/azure/developer/terraform/quickstart-configure)
- [Install Terraform on Windows with Azure PowerShell](https://learn.microsoft.com/en-us/azure/developer/terraform/get-started/get-started-windows-powershell)
- [Authenticate Terraform to Azure](https://learn.microsoft.com/en-us/azure/developer/terraform/authenticate-to-azure)
- [Authenticate to Azure with a Microsoft account](https://learn.microsoft.com/en-us/azure/developer/terraform/authenticate/authenticate-to-azure-with-microsoft-account)
- [az account](https://learn.microsoft.com/en-us/cli/azure/account)
- [azurerm provider documentation on the Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
