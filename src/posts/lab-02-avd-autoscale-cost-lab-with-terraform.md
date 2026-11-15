---
title: "AVD Autoscale Lab with Terraform: Weekday and Weekend Schedules and How to Measure the Saving"
seoTitle: "Azure Virtual Desktop Autoscale Terraform Lab: Scaling Plan and Cost"
layout: post.njk
permalink: "/terraform-labs/avd-autoscale-cost-lab/"
order: 302
tags: [terraform-lab]
deck: "A Terraform lab that adds a scaling plan to a pooled host pool, so session hosts power on and off by schedule. It covers how the schedule works, how to test it and how to measure the saving."
description: "A walk through a Terraform lab for Azure Virtual Desktop Autoscale: the scaling plan, the weekday and weekend schedule, the roles it needs, Start VM on Connect, how to test it and how to calculate the compute saving."
---

A session host that runs all day and all night costs money even when nobody is using it. Azure Virtual Desktop (AVD) has a built-in feature, Autoscale, that powers session hosts (the VMs that run users' desktops) on and off by schedule and by how many users are connected. This article walks through a Terraform lab that sets it up, and shows how to test it and how to measure what you save.

The code is in a public repository: [terraform-azure-avd-autoscaling-cost-optimization](https://github.com/AddySidd27/terraform-azure-avd-autoscaling-cost-optimization). It builds on the [AVD quick lab](/terraform-labs/avd-quick-lab/) and adds a scaling plan. The network, the storage, the FSLogix profiles and the Microsoft Entra join are the same as in that lab, so this article does not repeat them. Read the quick lab if you want those parts explained.

Below is what the code does, how Microsoft describes the features it uses, and a test plan.

One risk comes first. The documentation recommends Autoscale with VMs created by the AVD portal or Microsoft's templates. This lab builds its VMs directly with Terraform, so test that Autoscale really manages them.

## Before you start

- Quota for 8 vCPUs of the `Standard_Dv5` family in your region.
- A Microsoft Entra group and a test user, as in the quick lab.
- Permission to grant admin consent in your tenant.
- The Azure CLI, Git and Terraform 1.9 or newer.
- The lab costs money while it exists. Run `terraform destroy` when you finish (see "Run it").

## Key terms

| Term | Meaning |
|---|---|
| Host pool | A group of session hosts that users share. |
| Session host | A VM that runs users' desktops. |
| Pooled | A host pool where many users share the same hosts. |
| Resource group | An Azure container that holds related resources. |
| Tenant | Your organization's Microsoft Entra directory. |
| Role assignment | A rule that gives an identity a role, such as the right to power VMs on and off. |
| Tag | A name (and optional value) you attach to an Azure resource. |
| FSLogix | Software that keeps each user's profile on a file share, so it follows them to any host. |
| Terraform state | The file where Terraform records what it built. |
| Autoscale | The AVD feature that turns session hosts on and off by schedule and by load. It has two kinds. Power management starts and deallocates VMs you already have, and this lab uses it. |
| Scaling plan | The object that holds the schedules. You assign it to a host pool. A host pool can have only one scaling plan. |
| Deallocated | A VM that Azure has fully shut down and released the hardware for. Azure shows it as Stopped (deallocated). |
| Stopped | A VM that was shut down from inside Windows. Azure still holds the hardware, so it still charges for compute. |
| Phase | One part of the day in a schedule: ramp-up, peak, ramp-down or off-peak. |
| Ramp-up | The start of the day, when usage picks up. |
| Peak | The time of day when usage is highest. |
| Ramp-down | When usage drops. This is usually when VMs are shut down. |
| Off-peak | The time of day when usage is lowest. |
| Maximum session limit | The most sessions one session host accepts. |
| Capacity | The number of hosts that are on, multiplied by the maximum session limit. With 2 hosts on and a limit of 10, capacity is 20 sessions. |
| Capacity threshold | The share of capacity that triggers a scaling action. If used capacity goes above it, Autoscale starts another host. |
| Minimum percentage of hosts | The share of hosts that Autoscale keeps on in a phase. It rounds up to a whole host. |
| Drain mode | A host setting that stops new sessions from landing on it. Users already on it stay. |
| Force sign-out | A ramp-down setting that signs users out after a wait time, so Autoscale can shut a host down. |
| Exclusion tag | A tag you add to a VM so Autoscale leaves it alone. Autoscale does not start, stop or change drain mode on it. |
| Start VM on Connect | A host pool setting that starts a deallocated session host when a user connects. |
| Service principal | An identity that represents an Azure service inside your tenant. In this lab, Autoscale acts through the Azure Virtual Desktop service principal. The documentation also allows a managed identity. |
| Subscription scope | Scope is where a role applies. Subscription scope means everything in the subscription. |
| VM-hour | One VM running for one hour. It is the unit used in the cost calculation below. |
| Breadth First, Depth First | Load-balancing methods. Breadth First spreads new sessions across the hosts. Depth First fills one host up before it uses the next. |

## What is new compared with the quick lab

![The scaling plan is assigned to the host pool. The Azure Virtual Desktop service principal holds two roles on the subscription, Desktop Virtualization Power On Off Contributor and Desktop Virtualization Power On Contributor, so it can start and deallocate the two session hosts. A user who connects when all hosts are off starts one through Start VM on Connect. Below, the default schedule: on weekdays, ramp-up from 07:00, peak from 09:00, ramp-down from 18:00 and off-peak from 22:00. At weekends, ramp-up from 09:00, peak from 10:00, ramp-down from 14:00 and off-peak from 18:00.](/img/avd/AVD-Terraform-Autoscale-Lab.svg)

*Source: the lab's Terraform code, in the [terraform-azure-avd-autoscaling-cost-optimization](https://github.com/AddySidd27/terraform-azure-avd-autoscaling-cost-optimization) repository, and the page [Autoscale scaling plans and example scenarios](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scenarios). Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/). The scaling plan has no icon in that set, so it is a plain box.*

The lab keeps the same resources as the quick lab: one resource group, a pooled host pool with two Windows 11 multi-session session hosts, a virtual network, an NSG and an Azure Files share for FSLogix profiles. It adds three things and changes one default:

- **An `autoscale` module** (a folder of Terraform files) that creates the scaling plan and assigns it to the host pool.
- **Two role assignments at subscription scope** for the Azure Virtual Desktop service principal.
- **A new setting, `avd_service_principal_object_id`,** which you fill in before you deploy (see "The roles").
- **`start_vm_on_connect` is now `true` by default.** In the quick lab it is `false`.

The repository also has two new outputs (the scaling plan name and the configured schedule) and new guides for validation, cost and a seven-day test.

## How Autoscale decides

Before you read the schedule, you need the rules that Autoscale follows. These come from the page [Autoscale scaling plans and example scenarios](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scenarios).

**It starts a host when used capacity goes above the threshold.** Used capacity is sessions divided by capacity. For example, two hosts on with a limit of 5 sessions each give a capacity of 10. With a 30% threshold, 3 sessions are fine (30%), and the fourth session (40%) makes Autoscale start a third host.

**It stops a host only when it is safe to.** Autoscale stops a host only if the used capacity stays at or below the threshold afterwards, and only a host with no sessions, unless force sign-out is on during ramp-down. Pooled Autoscale does not stop hosts during ramp-up.

**In ramp-down it packs sessions onto fewer hosts.** Autoscale counts disconnected sessions too and assumes those users may come back at once, so it keeps enough hosts on for all of them.

**It overrides some host pool settings.** For a pooled host pool, Autoscale overwrites drain mode, and it ignores the load-balancing method in the host pool and uses the one in the schedule. So before you patch or repair a host, add the exclusion tag to it (see "Test it").

**It does not work with another scaling tool.** You cannot use Autoscale and another scaling tool, such as one built with Azure Automation, on the same host pool.

## The default schedule

The lab defines two schedules in `variables.tf`, one for weekdays and one for weekends. Every day of the week must appear in exactly one schedule, and the code checks this. Times are in the Windows time zone name you set in `autoscale_time_zone`, such as `Central Standard Time` (the default). Despite the name, that zone follows daylight saving time. A scaling plan runs only in its configured time zone.

| | Weekdays (Mon to Fri) | Weekends (Sat, Sun) |
|---|---|---|
| Ramp-up starts | 07:00 | 09:00 |
| Minimum hosts in ramp-up | 50% | 0% |
| Ramp-up capacity threshold | 60% | 75% |
| Peak starts | 09:00 | 10:00 |
| Ramp-down starts | 18:00 | 14:00 |
| Minimum hosts in ramp-down | 0% | 0% |
| Ramp-down capacity threshold | 50% | 75% |
| Off-peak starts | 22:00 | 18:00 |

Peak and off-peak have no threshold of their own. Peak takes the ramp-up threshold, and off-peak takes the ramp-down threshold.

The code sets the load-balancing method per phase: Breadth First in ramp-up and peak, and Depth First in ramp-down and off-peak. In ramp-down, Depth First packs sessions onto fewer hosts, so the empty hosts can be turned off.

These settings are the same on both schedules:

- **`ramp_down_force_logoff_users = false`.** The lab never forces anyone to sign out.
- **`ramp_down_stop_hosts_when = "ZeroSessions"`.** A host is stopped only when it has no sessions at all, active or disconnected. The other allowed value, `ZeroActiveSessions`, also stops a host that has only disconnected sessions.
- **`ramp_down_wait_time_minutes = 30`.** Autoscale waits this long before signing users out. It has no effect here, because force sign-out is off.

Because nobody is signed out by force, one forgotten disconnected session keeps a host on all night.

With two hosts, the weekday ramp-up minimum of 50% means one host is on from 07:00. The weekend minimum of 0% means both hosts can stay deallocated until someone connects.

This is a lab example, not a schedule to copy. Understand your usage patterns before you define a schedule, so look at your real usage before you pick times.

## What the code does

### The roles

In this lab, Autoscale and Start VM on Connect act through the Azure Virtual Desktop service principal (the documentation also allows a managed identity on the host pool), so the service principal needs two roles. The `autoscale` module assigns both at subscription scope:

| Role | Used for |
|---|---|
| Desktop Virtualization Power On Off Contributor | The scaling plan, to power hosts on and off |
| Desktop Virtualization Power On Contributor | Start VM on Connect |

Each of the two features needs its own role. For the scaling plan role, the scope must be the subscription, because a lower scope stops Autoscale from working properly. For Start VM on Connect, you can assign the role at a lower scope, as long as that scope contains the session host VMs.

The service principal is different in every tenant, so you look up its object ID and put it in `avd_service_principal_object_id`. The object ID identifies the service principal in your tenant. The application ID identifies the Azure Virtual Desktop app everywhere (`9cdead84-a844-4324-93f2-b2e6bb768d07`, from the documentation). Run `az login` first, then:

```powershell
az ad sp show --id 9cdead84-a844-4324-93f2-b2e6bb768d07 --query id --output tsv
```

Do not paste the application ID itself into the setting. If the command returns nothing, check that you are signed in to the right tenant. Older tenants may show the app as "Windows Virtual Desktop".

### The scaling plan

The scaling plan is one Terraform resource, `azurerm_virtual_desktop_scaling_plan`. It sets the time zone, the exclusion tag (`excludeFromScaling`), one `schedule` block per schedule, and the host pool it is assigned to, and it turns on the assignment. Terraform creates the two role assignments before the plan, because the plan needs those permissions.

The lab meets two prerequisites. The scaling plan must be in the same region as the host pool, and a pooled host pool needs a maximum session limit. The default limit is too high for Autoscale to use, so the lab sets 10.

### Start VM on Connect

With `start_vm_on_connect = true`, a connection starts one host when none is on. If that host fills up, the next connection starts another. It starts at most one VM every five minutes. Users who connect while a host is still starting may see "No resources available". They should wait a few minutes and try again. The schedule still decides when hosts are powered off.

Start VM on Connect can be configured only on an existing host pool, while this lab sets it when Terraform creates the pool. So after the apply, open the host pool, select Properties and check that Start VM on Connect says Yes. If it does not, set it there.

## Run it

The steps are the same as in the [quick lab](/terraform-labs/avd-quick-lab/). The differences are these:

1. **Permissions.** You need permission to create the lab resources, and a role that includes `Microsoft.Authorization/roleAssignments/write` on the subscription, such as Owner or User Access Administrator, for the two role assignments.
2. **Clone this repository** instead: `git clone https://github.com/AddySidd27/terraform-azure-avd-autoscaling-cost-optimization`.
3. **Values in `terraform.tfvars`.** Fill in the five values from the quick lab (`subscription_id`, `windows_image_version`, `admin_password`, `avd_user_group_object_id` and `storage_account_name`) and these extra ones: `avd_service_principal_object_id` (see above) and `autoscale_time_zone`. The list of valid Windows time-zone names comes from `Get-TimeZone -ListAvailable`. Change `autoscale_schedules` only if you want a different schedule. Keep the phase times in order: ramp-up, then peak, then ramp-down, then off-peak.
4. **Deploy.** Run `az login`, `terraform init`, `terraform plan -out main.tfplan` and `terraform apply main.tfplan`.
5. **Do all eight steps** in "Steps Terraform does not do" in the quick lab. This repository's `docs/post-deployment.md` has the same list.
6. **Check Start VM on Connect** (see above).

If a host is off during the manual steps, start it in the portal first, or deploy in a ramp-up or peak window. Run commands and `dsregcmd` do not work on a deallocated VM.

This repository has no `.gitignore` file. Do not commit `terraform.tfvars`, because it holds the VM password. When you finish, run `terraform destroy`. It also deletes every profile on the share.

## Test it

The repository has a validation guide and a seven-day test plan. This is the short version. Do steps 1 to 3 before the first scheduled phase.

1. **Check the plan.** In the Azure portal, open Azure Virtual Desktop, then Scaling plans. Open `avd-sp-avd-dev` and check that it is enabled, assigned to `avd-hp-avd-dev`, and has the right time zone and phase times.
2. **Check the roles.** On the subscription's Access control (IAM) page, search for the Azure Virtual Desktop enterprise application (it may be named Windows Virtual Desktop, so check the application ID). It should have both roles.
3. **Check the hosts.** Both session hosts should show Available in the host pool. Check their power state with `az vm get-instance-view --resource-group rg-avd-dev --name avdsh-01 --query "instanceView.statuses[?starts_with(code,'PowerState')].displayStatus" --output tsv` (and the same for `avdsh-02`).
4. **Test ramp-down.** Copy `autoscale_schedules` from `variables.tf` into `terraform.tfvars`. Move the ramp-down start of today's schedule (weekday or weekend) to 15 to 30 minutes from now, with off-peak later, and keep peak starting before ramp-down. Apply, sign out of every desktop (do not only disconnect), and watch the hosts. An unused host should go into drain mode and then be deallocated. Autoscale does not act at once, so allow time and check again after a while.
5. **Test that an active session is safe.** Before ramp-down starts, sign in one test user on one host. When ramp-down runs, the other host should be deallocated and the host with the session must stay on.
6. **Test Start VM on Connect.** When both hosts are deallocated, connect as a test user with a client, for example the web client from the quick lab. A host should start. The connection takes longer while the VM boots.
7. **Test the exclusion tag.** Add a tag named `excludeFromScaling` to one VM (the value can be empty). Run the ramp-down test again. The tagged host should stay on, and Autoscale should not start, stop or change drain mode on it. Remove the tag afterwards. If every host has the tag, Autoscale cannot manage any of them and users get "No resources available".
8. **Restore the schedule** and apply again.

The lab does not set up monitoring. The documentation has a page on [monitoring Autoscale operations with Insights](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-monitor-operations-insights) if you want the logs.

## Measure the saving

This lab does not give a dollar figure. VM, disk and storage prices depend on the region and your agreement, and they change. Count VM-hours instead (this uses a 30-day month with 22 weekdays and 8 weekend days), then price them with the [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/) or read the real cost in Azure Cost Management.

For two hosts that run all the time:

```text
2 hosts × 24 hours × 30 days = 1,440 VM-hours per month
```

Suppose, as an example, that the hosts average 12 running hours on weekdays and 4 on weekend days:

```text
Weekdays: 2 × 12 × 22 = 528 VM-hours
Weekends: 2 × 4 × 8   =  64 VM-hours
Scheduled total       = 592 VM-hours
Reduction: (1,440 − 592) ÷ 1,440 = 58.9%
```

This is a best case. When demand rises, Autoscale starts more hosts, so real VM-hours are higher and the saving is smaller. The 12 and 4 hours here are made up to show the arithmetic, not measured.

The saving covers compute only. The documentation's page on [VM states and billing](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing) says a deallocated VM does not incur compute charges, but its disks and networking still do. A VM that was only stopped from inside Windows still incurs compute charges, which is why the lab uses deallocation. The disks and the Azure Files share still cost money.

To check the real cost, run the lab once with the scaling plan removed or disabled for a few days, then once with it on. In Azure Cost Management, open Cost analysis, filter to the resource group `rg-avd-dev`, group by resource or meter, and compare the VM compute lines. Cost data can lag by up to a day. Report VM compute on its own line.

## Before you use this design for real work

The lab leaves out the same things as the quick lab (private access, controlled outbound traffic, monitoring, backup and image management). For Autoscale in particular:

- **Narrow the roles.** The lab assigns both roles at subscription scope, which the documentation requires for the scaling plan role. If your security rules need a narrower scope, only the Start VM on Connect role can move to the resource group. A subscription dedicated to AVD makes this simpler.
- **Keep the Terraform state in a protected location.** It holds secrets.

## Sources

- [Autoscale scaling plans and example scenarios](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scenarios)
- [Create and assign an autoscale scaling plan](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-create-assign-scaling-plan)
- [Assign Azure RBAC roles or Microsoft Entra roles to a service principal](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-principal-assign-roles)

