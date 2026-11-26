---
title: "Scale Azure Virtual Desktop with Scaling Plans: Schedules, Capacity and Cost"
seoTitle: "AVD Scaling Plans: Schedules, Capacity Threshold and Cost"
layout: post.njk
permalink: "/azure-virtual-desktop/scale-with-scaling-plans-schedules-capacity-and-cost/"
order: 133
part: 33
tags: [avd-series]
deck: "Build a scaling plan with the four daily phases, set the capacity threshold and minimum hosts, handle forced sign-out, and know what permission and tags it needs."
description: "How Azure Virtual Desktop autoscale works: scaling plan schedules, capacity threshold, force sign-out, Start VM on Connect, roles and the exclusion tag."
---

Session hosts cost money while they run. A scaling plan lets Azure Virtual Desktop (AVD) turn session hosts on and off on a schedule to optimize deployment costs.

This article is for admins who run an AVD host pool and want to set up autoscale, or who already did and need to understand why hosts start and stop the way they do. It covers pooled and personal host pools, the settings of each daily phase, how the capacity threshold decides when a host starts or stops, forced sign-out, Start VM on Connect, the permission autoscale needs, and the exclusion tag. It covers power management autoscaling, which turns hosts on and off. It is the method for a standard host pool, one without a session host configuration. Dynamic autoscaling, which also creates and deletes hosts, is mentioned at the end.

How to group users into host pools is in [Plan your host pools](/azure-virtual-desktop/plan-your-host-pools/). How session hosts are created and replaced is in [Create, update and replace session hosts](/azure-virtual-desktop/create-update-replace-session-hosts/). VM size choices are in [Choose session host VM sizes](/azure-virtual-desktop/choose-session-host-vm-sizes/). This article does not repeat them.

## Key terms

| Term | Meaning |
|---|---|
| Host pool | A group of session hosts that users connect to. |
| Session host | A virtual machine (VM) in a host pool that runs user sessions. |
| Pooled host pool | A host pool where users share session hosts. |
| Personal host pool | A host pool where each user has their own session host. |
| Autoscale | The AVD feature that scales session hosts up and down on a schedule. |
| Power management autoscaling | The scaling method that powers session hosts on and off. |
| Dynamic autoscaling | The scaling method that powers session hosts on and off and also creates and deletes them. |
| Scaling plan | An AVD object that holds the schedules for scaling session hosts in a host pool. You can assign one plan to several host pools. A host pool can have only one plan. |
| Schedule | Part of a scaling plan. It says when each phase of the day starts and which settings apply in each phase. A plan can have one or more schedules, for example one for weekdays and one for the weekend. |
| Ramp-up | The start of the day, when usage picks up. |
| Peak hours | The time of day when usage is expected to be highest. |
| Ramp-down | When usage tapers off. This is usually when you shut down VMs to save costs. |
| Off-peak hours | The time of day when usage is expected to be lowest. |
| Load balancing algorithm | How new user sessions are spread over session hosts. Breadth-first spreads new sessions across all available session hosts. Depth-first sends new sessions to the available session host with the most connections that has not reached its session limit. |
| Max session limit | The most user sessions one session host may hold. For pooled host pools you must set your own value for autoscale. Do not leave the default. |
| Available session host | A session host that is powered on and ready for user sessions. |
| Available host pool capacity | The max session limit multiplied by the number of available session hosts. With 2 available hosts and a limit of 5, the capacity is 10. |
| Used host pool capacity | The share of that capacity taken by sessions, as a percentage. 3 sessions on a capacity of 10 is 30%. Active and disconnected sessions both count. |
| Capacity threshold | The used-capacity percentage that triggers a scaling action. |
| Minimum percentage of hosts | The share of all session hosts that stay on in a phase. A fraction is rounded up to the next whole number. |
| Disconnected session | A session the user left without signing out. |
| Signed out (logged off) | The user ended the session, so it is no longer a disconnected session. |
| Drain mode | A host setting that stops new sessions from starting on that host. |
| Deallocate | Power a VM off so that it is stopped. This is what autoscale does to turn a host off. In this article "turn off" and "deallocate" mean the same. |
| Hibernate | An alternative to deallocate for personal hosts. It needs the hibernation feature turned on in the session hosts. |
| Exclusion tag | A tag name that you set on the scaling plan. Hosts that carry a tag with that name are left alone by autoscale. |
| Start VM on Connect | A host pool setting that powers on a session host when a user connects to it. |
| Service principal | The identity that AVD uses to manage the power state of your VMs. |
| Assignable scope | Where a role assignment applies. For the autoscale role it is the Azure subscription. |

## What a scaling plan is

A scaling plan defines the schedules for scaling the session hosts of a host pool. These rules apply:

- You can assign one scaling plan to one or more host pools of the same host pool type, pooled or personal. Its schedules apply to all of them.
- Each host pool can use only one scaling plan. If you assign one plan to several host pools, those host pools cannot be assigned to another plan.
- A plan is either pooled or personal.
- A plan works only in its configured time zone.
- The plan takes effect as soon as you enable it. Changes to a plan that is already assigned apply immediately.
- You cannot use autoscale and the Azure Automation and Azure Logic Apps scaling method on the same host pool. Use one or the other. Do not mix autoscale with other Microsoft or third-party scaling tools either. Turn those off for the host pools you assign.
- For best results, use autoscale with session hosts that you deployed with AVD Azure Resource Manager templates or first-party Microsoft tools.

When you create a plan you also choose a scaling method. Power management autoscaling powers hosts on and off. Use it for a host pool with standard management, which means a host pool without a session host configuration. The other method is dynamic autoscaling, described near the end.

![A scaling plan is assigned to one or more host pools of the same type. A pooled plan uses pooled schedules and a personal plan uses personal schedules. Autoscale turns the session host VMs on and off. A pooled schedule has ramp-up, peak, ramp-down and off-peak phases with load balancing, minimum hosts, capacity threshold and force logoff settings, and repeats on the days you select. A personal schedule has the same four phases with Start VM on Connect, disconnect and sign out actions. Related settings: the Power On Off Contributor role for the AVD service principal or a host pool managed identity at the subscription, the exclusion tag on session hosts, and Start VM on Connect on the host pool.](/img/avd/avd-scaling-plans.svg)

*Source: [Create and assign an autoscale scaling plan for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scaling-plan), [Autoscale scaling plans and example scenarios in Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scenarios) and [Configure Start VM on Connect](https://learn.microsoft.com/en-us/azure/virtual-desktop/start-virtual-machine-connect).*

## Before you create a plan

| Requirement | Detail |
|---|---|
| Region | The scaling plan configuration must be stored in the same Azure region as the host pool configuration. Your session hosts can be in any supported region. |
| Max session limit | For a pooled host pool, set a *MaxSessionLimit* of your own. Do not use the default value. |
| Permission to assign the role | You need the `Microsoft.Authorization/roleAssignments/write` permission on your subscriptions. The built-in roles **User Access Administrator** and **Owner** include it. |
| Power role | The **Desktop Virtualization Power On Off Contributor** role must be assigned to the AVD service principal (or to a managed identity assigned to your host pool), with your Azure subscription as the assignable scope. |
| PowerShell | If you use PowerShell, you need the Az.DesktopVirtualization module version 4.2.0 or later. |
| Hibernation | To use hibernation on personal hosts, turn on the hibernation feature on the session hosts. FSLogix and App Attach do not support hibernate. Do not turn it on if you use them in the personal host pool. |

### The role and its scope

Add each subscription that holds host pools and session hosts you want to scale as an assignable scope. This role lets AVD manage the power state of any session host in those subscriptions. It also lets the service act on host pools and hosts when there are no active user sessions.

Assign it at the subscription. If you assign it lower, such as at the resource group, host pool or VM, autoscale does not work properly.

Start VM on Connect uses a different role and has a different rule. See the Start VM on Connect section below.

## The four phases and their settings

Know your usage pattern before you set times. Then give each phase a start time. The start time of a phase is also the end time of the phase before it. A pooled plan works through the day like this:

| Phase | Can autoscale start hosts? | Can autoscale turn hosts off? |
|---|---|---|
| Ramp-up | Yes | No |
| Peak hours | Yes | Yes |
| Ramp-down | Yes | Yes. With force logoff on, it can also sign users out first. |
| Off-peak hours | Yes | Yes |

### Pooled host pools

In each phase, autoscale turns hosts off only if the used capacity then stays within the capacity threshold. Pooled autoscale does not turn hosts off during ramp-up. The values the portal fills in are suggested values for weekdays. Change them as needed.

| Phase | Settings you enter | Notes |
|---|---|---|
| Ramp-up | Start time, load balancing algorithm, minimum percentage of hosts, capacity threshold | Breadth-first is the recommended algorithm. It spreads users across existing hosts to keep access times fast. |
| Peak hours | Start time, load balancing algorithm | You cannot set the capacity threshold here. The ramp-up value carries over. You can pick breadth-first or depth-first. |
| Ramp-down | Start time, load balancing algorithm, minimum percentage of hosts, capacity threshold, force logoff of users | See the next sections for forced sign-out. |
| Off-peak hours | Start time, load balancing algorithm | You cannot set the capacity threshold here. The ramp-down value carries over. Depth-first is the recommended algorithm. It reduces the number of hosts gradually, based on the sessions on each VM. The example scenarios show the minimum percentage of hosts still keeping one host on in off-peak. |

Two more points about pooled plans:

- The load balancing choice in the schedule overrides the one in the host pool settings. Autoscale ignores the algorithm in the host pool and applies the one in the schedule.
- If a day is not selected in any schedule, the last off-peak settings carry over until the next ramp-up. With a single Monday to Friday schedule, the Friday off-peak settings stay in force until Monday's ramp-up.

### Personal host pools

In each phase you decide what happens to a personal host depending on its session state.

| Setting | What it does |
|---|---|
| Start time | When the phase starts. |
| Start VM on Connect | Turns the feature on or off during that phase. The host pool setting of the same name is separate, under **Properties**. |
| VMs to start (ramp-up only) | **Assigned VMs only** (personal desktops that have a user assigned at the start time), **Assigned and unassigned VMs** (all personal desktops in the host pool), or **Don't turn VMs on at start time**. |
| Disconnect settings | After a user session has been disconnected for a number of minutes (0 to 360), deallocate the VM, hibernate it, or do nothing. The user closed the session window without signing out. |
| Sign out settings | After a user has been logged off for a number of minutes (0 to 360), deallocate the VM, hibernate it, or do nothing. The user ended the session. |

If you choose not to start hosts during ramp-up, turn on Start VM on Connect. It is highly recommended in that case.

## How the capacity threshold works

The threshold decides when autoscale starts and stops pooled hosts. The worked examples below use the autoscale example scenarios.

**Turning hosts on.** Autoscale can start a host in any phase. It starts one when the used capacity is *greater than* the threshold. At or below the threshold it does nothing.

Example: ramp-up phase, 6 hosts in the pool, max session limit 5, threshold 30%, minimum percentage of hosts 30%.

1. Autoscale starts 2 hosts to meet the 30% minimum. 30% of 6 is 1.8, which rounds up to 2. Capacity is 2 x 5 = 10.
2. Three users sign in. Used capacity is 30%. This is not above the threshold, so no new host starts.
3. A fourth user signs in. Used capacity is 40%, above the threshold. Autoscale starts a third host. Capacity is now 15, and used capacity falls to about 27%.

**Turning hosts off.** Autoscale turns a host off only when all of this is true:

- Used capacity is below the capacity threshold.
- Turning a host off does not push the used capacity above the threshold.
- The host has no user sessions. The exception is the ramp-down phase with force logoff turned on.
- The phase is not ramp-up. Pooled autoscale does not turn hosts off in ramp-up, to avoid a poor user experience.

Autoscale picks a host with no sessions, puts it in drain mode, and turns it off.

Example: peak phase, 6 hosts, 5 of them available, max session limit 5, threshold 30%. Seven users are signed in, so used capacity is 28% of 25. Turning a host off would push it over the threshold, so nothing is turned off. Then two users sign out. Five users remain on the five available hosts, which is 20% of 25. Turning one host off would give a capacity of 20 and 25% used, which is under 30%, so autoscale picks a host with no sessions, puts it in drain mode and turns it off. Later four users remain on the four available hosts. Turning off another host would give about 27%, which is still under the threshold, but no host is empty, so nothing is turned off.

## Ramp-down, forced sign-out and session limits

Autoscale signs users out only if you turn on **force logoff** in the ramp-down phase. It never signs users out in other phases.

Without force logoff, you must choose when hosts stop: **VMs have no active or disconnected sessions** or **VMs have no active sessions**.

With force logoff, this is what autoscale does:

1. It picks the session host with the fewest user sessions, active and disconnected.
2. It puts that host in drain mode.
3. It sends the users on that host a notification that they will be signed out.
4. After the wait time, it signs out anyone still connected.
5. It then deallocates the VM.

In PowerShell, the wait time and the message are the `RampDownWaitTimeMinute` and `RampDownNotificationMessage` parameters.

The threshold and the minimum percentage of hosts still apply with or without force logoff. Autoscale shuts hosts down only if all existing sessions, active and disconnected, can fit on fewer hosts without going above the threshold.

The consolidation calculation is the same in both modes. Autoscale assumes that all disconnected users may reconnect at once. It works out how many hosts it must keep running:

Required hosts = total sessions (active + disconnected) / (max session limit x capacity threshold)

Use the threshold as a decimal, so 75% is 0.75.

Example: ramp-down phase with force logoff on, 6 hosts, 4 available, max session limit 5, threshold 75%, minimum percentage of hosts 10%, and 4 users with one on each host.

1. Capacity is 20 and used capacity is 20%. Autoscale can turn off two hosts without going over 75%.
2. Every host has a session, so autoscale forces the users on two hosts to sign out, then turns those two hosts off. Two hosts remain, capacity is 10, and two users are signed in (20%).
3. The two users sign back in. Used capacity is 40%, under 75%.
4. Turning off another host would leave a capacity of 5 for 4 users, which is 80%, above 75%. So autoscale does not.

In this example the 10% minimum of 6 hosts is 0.6, which rounds up to 1, so autoscale keeps at least one host available during ramp-down.

### Sign out disconnected sessions with a time limit policy

Disconnected sessions count toward used capacity. You can sign them out after a set time with the policy **Set time limit for disconnected sessions**. This lowers the used capacity. The policy applies in all phases.

- With Microsoft Intune: create a configuration profile for Windows 10 and later with the **Session Time Limits** profile type, then enable that setting and pick a time. You need the **Policy and Profile manager** built-in role and a group with the devices.
- With Group Policy: go to **Computer Configuration** > **Policies** > **Administrative Templates** > **Windows Components** > **Remote Desktop Services** > **Remote Desktop Session Host** > **Session Time Limits**, enable the setting and pick a time.

Restart the session hosts after the policy applies, so the setting takes effect.

## Start VM on Connect

Start VM on Connect lets users power on a session host when they connect. You turn it on per host pool. It is a host pool setting, separate from the scaling plan. It works for pooled and personal host pools, on Azure and Azure Local.

| Host pool type | What it starts |
|---|---|
| Personal | Only an existing session host VM that is already assigned, or can be assigned, to the user. |
| Pooled | A session host only when none is turned on. More VMs start only when the first VM reaches the session limit. |

Things to know:

- The connection takes longer when the host is deallocated, because the VM must start. Windows App and the Remote Desktop app tell the user that a VM is being powered on.
- In a pooled host pool it starts a VM at most every five minutes. Other users who connect in that time with no available resources get the error **No resources available**. They should wait a few minutes and try again.
- A direct connection to a powered-off VM by IP address or name does not start it.
- You can turn it on only for an existing host pool that is already tied to an application group and workspace. You cannot turn it on while creating the host pool.
- To configure it, you need the **Desktop Virtualization Host Pool Contributor** role. The names of the host pool, its session hosts and the resource group must contain only ANSI characters.
- To make it work, assign the **Desktop Virtualization Power On Contributor** role to the AVD service principal, or to a managed identity assigned to your host pool. The scope must contain the host pool and session host VMs. A subscription is recommended when you have several host pools or a subscription used only for AVD. A lower scope is allowed if it contains the target VMs. Do not confuse this role with the **Power On Off Contributor** role that autoscale needs. That one needs the subscription as its scope, because a lower scope stops autoscale from working properly.

Set it in the portal under **Host pools** > your host pool > **Properties**, then set **Start VM on connect** to **Yes** and **Save**. In PowerShell, use `Update-AzWvdHostPool` with `-StartVMOnConnect:$true`.

If a host does not power on, check the health of that VM first. You can also look at the AVD logs in Log Analytics. If you get an error message, read it closely and note the error name. AVD Insights can give suggestions for resolving issues.

## The exclusion tag

Set the exclusion tag name in the plan. When a VM has a tag with that name, autoscale does not turn it on, does not turn it off, and does not change its drain mode. This applies in all phases. The example tag name in the plan settings is `excludeFromScaling`.

Use it when you update hosts in a pooled host pool. For pooled host pools, autoscale overwrites drain mode, so a tag keeps it from undoing the drain mode you set for maintenance. How to update hosts is in [Create, update and replace session hosts](/azure-virtual-desktop/create-update-replace-session-hosts/). Autoscale matches on the tag name.

- Tagged hosts still count in the minimum percentage of hosts calculation.
- Do not put sensitive data such as user principal names in the tag.
- Be careful with how many hosts you tag. In this example, off-peak phase, the admin tagged five of six hosts. When a user signed in and used capacity went over the threshold, autoscale started nothing, because the only other hosts were tagged. Later the admin tagged the last untagged host too and turned it off. A user who tried to sign in then got **No resources available**. Removing the tag from two hosts let autoscale turn on just the one host needed for the minimum.

## Dynamic autoscaling in short

Dynamic autoscaling powers hosts on and off and also creates and deletes them. It is in preview, while power management autoscaling is generally available. It works only for pooled host pools with a session host configuration. It is available only in Azure, not Azure Government. It additionally needs the **Desktop Virtualization Virtual Machine Contributor** role on the service principal, at the subscription. Its schedule has these settings: the minimum host pool size is the number of session hosts that always stay in the pool, running or stopped. The maximum host pool size is the most running session hosts. The minimum percentage of active hosts is worked out from the minimum host pool size: 10% of a minimum size of 10 means one host is always available. It also needs access to the endpoint `wvdhpustgr0prod.blob.core.windows.net` to deploy the AVD Agent when it creates session hosts. Hosts that cannot reach it fail with `CustomerVmNoAccessToDeploymentPackageException`.

## Create and change a plan in the portal

1. In the Azure portal, search for *Azure Virtual Desktop*, select **Scaling Plans**, then **Create**.
2. On **Basics**, enter the subscription, resource group, scaling plan name (you can also add a friendly name that users see, and a description), location, time zone, host pool type and exclusion tag (the tag name for hosts you want autoscale to leave alone). For a pooled plan, choose **Power management autoscaling** as the method.
3. On **Schedules**, select **Add schedule**, name it, choose the days, and fill in each phase with the settings from the tables above.
4. On **Host pool assignments**, select the host pools. Select the check box next to each host pool you want to include. Clear all check boxes if you do not want to enable autoscale yet. You can assign only host pools that match the plan type.
5. On the **Tags** tab, add tags if you want them (name and value pairs). On **Review + create**, select **Create**.

To change a plan later, open it and use **Host pool assignments**, **Schedules** or **Properties**. You can change the friendly name, description, time zone and exclusion tag, plus the assignments and schedules. The host pools must be in the same region as the plan.

## Common mistakes

- Assigning the Power On Off Contributor role at a resource group or VM instead of the subscription. Autoscale then does not work properly.
- Leaving the max session limit at the default on a pooled host pool.
- Running autoscale together with another scaling tool on the same host pool.
- Expecting the host pool load balancing setting to apply. Autoscale uses the algorithm from the schedule.
- Looking for a capacity threshold field in the peak and off-peak tabs. It carries over from ramp-up and ramp-down.
- Expecting autoscale to turn off hosts that still hold disconnected sessions. Disconnected sessions count toward used capacity and block shutdown unless force logoff is on in ramp-down.
- Updating pooled hosts without the exclusion tag. Autoscale can overwrite drain mode.
- Skipping Start VM on Connect for personal hosts when ramp-up does not start them.
- Tagging every host with the exclusion tag, then seeing **No resources available**.
- Mixing up the Power On Contributor role (Start VM on Connect) and the Power On Off Contributor role (autoscale).

## How to validate this in your environment

1. In the Azure portal, open **Scaling plans**, open the plan and check **Host pool assignments**. Each host pool you expect is listed. The host pool type matches the plan type.
2. With Azure PowerShell, run `(Get-AzWvdScalingPlan -ResourceGroupName <rg> -Name <plan>).HostPoolReference | FL HostPoolArmPath,ScalingPlanEnabled` and check that `ScalingPlanEnabled` is true for each host pool. Sign in to Azure PowerShell first.
3. Open **Schedules** and read each phase. Check the start times against the plan time zone, and that the days cover the whole week or that you accept the carry-over.
4. On the host pool, check the max session limit is set to your own value (pooled).
5. Check that the AVD service principal has the **Desktop Virtualization Power On Off Contributor** role with the subscription as scope.
6. On the host pool **Properties**, check **Start VM on connect**.
7. At a time when you can test, compare the number of running hosts with the minimum percentage of hosts and the capacity threshold for the current phase, using the capacity threshold rules and the required-hosts formula above.
8. Test one tagged host. Check that autoscale leaves its power state and drain mode alone.

## Sources

- [Create and assign an autoscale scaling plan for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scaling-plan)
- [Autoscale scaling plans and example scenarios in Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-scenarios)
- [Configure Start VM on Connect](https://learn.microsoft.com/en-us/azure/virtual-desktop/start-virtual-machine-connect)
