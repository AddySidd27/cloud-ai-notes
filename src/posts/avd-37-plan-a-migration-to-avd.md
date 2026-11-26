---
title: "Plan a Migration to Azure Virtual Desktop from Another Platform"
layout: post.njk
permalink: "/azure-virtual-desktop/plan-a-migration-to-avd/"
order: 137
part: 37
tags: [avd-series]
deck: "Move users to Azure Virtual Desktop in waves, with an assessment first, a rollback plan before the first move and a clear way to handle profiles."
description: "A migration plan for moving virtual desktop users to Azure Virtual Desktop, based on Microsoft's general Azure migration guidance: assess, plan the waves, set a rollback plan and handle profiles."
---

A company already runs virtual desktops on another platform. Now it wants to move those users to Azure Virtual Desktop (AVD). Things that can go wrong include moving the wrong users first, missing an application that a team needs, losing profile data, or having no way back when a wave goes wrong.

Microsoft publishes no guide for moving from Citrix or Remote Desktop Services (RDS) to AVD. The steps below are Microsoft's general guidance for migrating workloads to Azure, applied to virtual desktop users. The profile advice comes from the FSLogix FAQ. This article does not convert one product's settings into another's. It covers the assessment, the plan and the AVD-specific preparation. Where a topic already has its own article in this series, this article links to it and does not repeat it.

Start with [Decide Whether Azure Virtual Desktop Fits](/azure-virtual-desktop/decide-whether-azure-virtual-desktop-fits/) if you have not yet confirmed that AVD is the right target.

## Key terms

| Term | Meaning |
|---|---|
| Source platform | The virtual desktop platform you run today and are moving away from. |
| Azure Virtual Desktop (AVD) | A desktop and app virtualization service that runs on Azure. It is the target in this article. |
| Workload | In this article, a group of users who use the same desktop or apps, together with those apps and what they depend on. The article also calls this a group. |
| Dependency | Something a workload needs in order to work, such as a database, an API, a sign-in service or a network connection. |
| Migration wave | A group of workloads that move together. |
| Baseline metrics | Measurements from the source platform taken before the move, such as CPU, memory, disk and network use. You compare against them after the move. |
| Right-sizing | Choosing Azure resources that match what the workload actually uses. |
| Remediation | A fix for an issue that would stop a workload from working in Azure. |
| Blocker | A compatibility issue that must be fixed before the move. |
| Risk register | A list of risks, with a plan to reduce each one, an owner and a timeline. |
| Azure landing zone | The prepared Azure environment that a migration plan assumes already exists. |
| Host pool | A collection of Azure virtual machines registered to AVD as session hosts. |
| Session host | A virtual machine in a host pool that runs the desktops or apps users connect to. |
| FSLogix profile container | A virtual hard disk (VHD or VHDX) file that holds the data of a user's Windows profile. |
| Known folder move | A OneDrive feature that moves or redirects the Windows Desktop, Documents, Pictures, Screenshots and Camera Roll folders to OneDrive. |
| Hybrid identity | A user account that is synced from an Active Directory. |
| Microsoft Entra joined | A device joined only to Microsoft Entra ID, not to on-premises Active Directory. |
| Hybrid Microsoft Entra joined | A device joined to on-premises Active Directory and registered with Microsoft Entra ID. |
| SID | A security identifier: a unique value that identifies an account in Windows. |
| Service level, recovery point and recovery time | Service level agreements (SLAs), recovery point objectives (RPOs) and recovery time objectives (RTOs) define the acceptable levels of availability and data loss. |
| Rollback | Reversing a change when it fails or creates risk. |
| Split-environment operation | A period when parts of the same workload run in the source environment and parts run in Azure. |
| Downtime migration | A move that needs a planned outage. |
| Near-zero downtime migration | A move that keeps the workload running during the transition, through continuous data replication. |
| Azure Migrate | A Microsoft tool for discovery and assessment of on-premises servers, databases and applications. |

## The plan on one page

![A source platform, on premises or in another cloud, feeds an assessment step. Five steps then run in order: plan migration, prepare workloads, execute migration, optimize in cloud, decommission source. A rollback plan is defined in the planning step, before the first move. The five steps lead to Azure Virtual Desktop.](/img/avd/avd-migration-plan.svg)

*Source: [Plan your migration](https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/plan-migration) and [Assess your workloads for cloud migration](https://learn.microsoft.com/azure/cloud-adoption-framework/plan/assess-workloads-for-cloud-migration).*

The five numbered steps are the five steps of the general migration process. The assessment is covered in a separate guide that the plan builds on. The Azure landing zone must already exist, because it is a prerequisite of the migration plan. The AVD side of that is in [Prepare Your Azure Environment for Azure Virtual Desktop](/azure-virtual-desktop/prepare-your-azure-environment/), [Plan Azure Virtual Desktop Networking: Address Space, Subnets, DNS and Connectivity](/azure-virtual-desktop/plan-avd-networking/) and [Choose the Right Identity Model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/).

This article covers the assessment, step 1 in full and the AVD-specific preparation for step 2. It names steps 3 to 5 so the whole process is visible, but does not cover them.

The rest of this article takes these parts in order.

## Before step 1, part A: Assess users, apps and dependencies

An assessment gives you full visibility into every component, dependency and requirement before you move. Write down the following for each user group.

| What to record | What to include |
|---|---|
| Environment | Whether the group is production, test or development. |
| Applications | Every application the group uses, its vendor and its version. |
| Current machines | Current virtual machine sizes, operating system type and version, storage type and capacity, and any special hardware such as GPUs. |
| Baseline metrics | CPU, memory, disk reads and writes, network throughput, and peak concurrency or user load. Note the daily and weekly peaks. Add average response times for user transactions. |
| Licensing | The software licensing information for the operating system and the apps. It might make Azure Hybrid Benefit possible or require a license migration. |
| Security and identity | Service accounts, any hard-coded credentials, encryption methods and firewall rules. These must be repeated or changed in Azure. |
| Dependencies | What the apps talk to inside your organization, and outside it: SaaS platforms, partner APIs, on-premises systems and third-party services. |
| Compliance and service levels | Regulatory requirements for the data, and the agreed service level, recovery point and recovery time for the group (see Key terms). |

Three practical points about how to collect this.

- **Use tools, then check with people.** Assessment tools such as Azure Migrate automate discovery, but they might miss undocumented dependencies. Interview the application owners, or hold review sessions with them, to confirm and complete what the tool found.
- **Keep one shared record.** Put the inventory and dependency data in one place that the whole team can use, such as a spreadsheet or a diagram, and keep it up to date during the migration.
- **Check software vendors.** Confirm that each vendor's software works on Azure before the move. Use the vendor's documentation, a test environment or the vendor directly. Note any update, replacement or configuration change that is needed.

Then turn the findings into two lists.

1. **A remediation list.** Every compatibility issue and the fix it needs. Split it into blockers that must be fixed before the move and items that can be fixed after.
2. **A risk register.** Technical, operational and organizational risks, each with a way to reduce it, an owner and a timeline.

## Before step 1, part B: Size the new environment

The baseline metrics and machine details above are the inputs to sizing. They are used to right-size the Azure resources, and later to compare how the new environment performs against the old one.

How many users share a session host and which virtual machine size to choose are AVD decisions. They are covered in [Plan Your AVD Host Pools: Users, Applications, VM Sizing and Images](/azure-virtual-desktop/plan-your-host-pools/) and [Choose Session Host VM Sizes: Compute, GPU, Disks and Quota](/azure-virtual-desktop/choose-session-host-vm-sizes/). Bandwidth and latency between users and the Azure region are covered in [Plan Bandwidth, Latency and Quality of Service for Azure Virtual Desktop](/azure-virtual-desktop/plan-bandwidth-latency-and-quality-of-service/).

## Step 1: Plan the migration

This step holds most of the planning work: skills, waves, method, the data path, the overlap, the rollback plan and approval.

### Check your team's skills

Review your team's experience with Azure services, migration tools and the final switch to Azure. If the team lacks migration experience, bring in Microsoft or a Microsoft partner to check the strategy, recommend tools and set realistic timelines.

### Group users by dependency

Find the dependencies first. Then group users and apps by what they share: databases, APIs, sign-in services or network connections. Each group is the base of a migration wave. When you are not sure how tightly two things are linked, put them in the same group. You can separate them later.

| Type of dependency | What to do |
|---|---|
| Direct: needs immediate, low-latency communication | Move the connected parts together. |
| Indirect: occasional or non-critical contact | Move together, or in separate waves if the link tolerates delay or can run across both environments. |
| Business: linked through the organization or its management | Move related groups and their reporting systems together. |

### Decide the order of the waves

| Priority | Business value | Effort | What to do |
|---|---|---|---|
| High | High | Low | Quick wins. Move first. |
| Medium-high | High | High | Strategic. Plan carefully with enough resources. |
| Medium-low | Low | Low | Easy. Use them to fill gaps between larger moves. |
| Low | Low | High | Avoid or delay. |

Rules for the order:

- **Start with simpler groups.** Pick groups that are less complex and lower risk, with few integration points. This builds confidence and lets you test the process before harder groups.
- **Move non-production before production.** Development, staging and test environments let you test the whole process, including recovery, without affecting users. They also train the operations team.
- **Put critical groups later,** after the team has shown it can run the process. A business deadline can force an earlier date. If so, add safeguards and longer testing.
- **Add one or two complex groups to each early wave.** They show the problems you will meet with mission-critical groups.

For virtual desktops, a non-production group can be, for example, a test host pool with test users.

### Set the schedule

Give each wave a start and end date, with spare time for testing and fixing problems. Avoid critical business periods such as financial close, product launches and holiday seasons. Use a project tool to track dependencies and milestones.

### Choose the method for each group

| Method | Use it when | Trade-off |
|---|---|---|
| Downtime migration | The group can accept a planned outage, such as a test group or a group with a maintenance window. | Simpler and faster, but service stops. |
| Near-zero downtime migration | The group is critical or has strict service levels. | Little service disruption, but complex to set up and it needs testing. |

Write down the acceptable downtime for each group. Plan downtime moves for low-usage periods.

### Check the data path

If you copy data to Azure over the network, such as profile or file data, check which connection you have. The options are ExpressRoute, a VPN, Azure Data Box or the public internet.

- **ExpressRoute** is a private, dedicated connection to Azure. It is the first choice when you have it.
- **VPN** creates an encrypted tunnel over the internet to Azure. Use it when ExpressRoute is not available. It is typically slower than ExpressRoute.
- **Azure Data Box** is a physical device that Microsoft ships to you. You copy data onto it and ship it back. It does not use your network but takes the longest because of shipping.
- **Public internet** works everywhere but is the least secure. Use it only for data that is not sensitive.

### Address split-environment operations

During the move, some users or apps are on the source platform and some are on AVD. This is a split-environment operation.

- **Plan for what cannot move.** List components that must stay in the source environment for technical or regulatory reasons. Record why, how they connect to other systems and what data they share.
- **Keep the overlap short.** For parts that can move later, document their connections and data flows with the cloud systems. Set a timeline and plan for the risks. Consider delaying a move until more of its parts can move together.
- **Connect the environments reliably.** Use integration methods such as API gateways, message queues and data synchronization (copying data between the two sides) so the two sides work together until the rest has moved.

### Define the rollback plan before the first move

A rollback plan lets you reverse a change quickly when a deployment fails or creates risk. Set the criteria and the steps before any migration starts.

1. **Define a failed deployment** with business owners, workload owners and operations. Examples are failed health checks, poor performance, security issues and missed success measures. Add specific trigger conditions, such as limits on CPU use, response times or error rates.
2. **Automate the steps** where you can. For example, set up a pipeline that redeploys a prior version if health checks fail.
3. **Write rollback steps for each type of workload** and each way of deploying it. Attach the scripts, configuration snapshots and templates that you need.
4. **Test the rollback** by simulating a failure in a staging environment. Fix gaps in automation, permissions or dependencies. Check that the rollback returns the system to a stable, known-good state.
5. **Improve it after each wave.** Review what worked and what did not, and update the rules and scripts.

### Get approval

Before you run migrations, get formal approval from stakeholders. The plan should show the workload name, owner, importance, method, downtime window and business effect. Show the tested rollback steps with timeframes and success criteria. Check the schedule against business limits such as maintenance freezes and seasonal peaks. Get written approval for the plan and the rollback, and agree who has the authority to decide. Set measurable success criteria, such as performance benchmarks, functional checks and user acceptance, and schedule go or no-go reviews.

## Step 2: Prepare workloads

This part applies the step to AVD. It covers images, applications and profiles. Each has its own article in this series.

### Images and applications

Blockers on the remediation list from the assessment must be fixed before the move. Build the images and application delivery on the AVD side with the existing articles: [Build and Maintain a Golden Image](/azure-virtual-desktop/build-and-maintain-a-golden-image/), [Create, Update and Replace Session Hosts](/azure-virtual-desktop/create-update-replace-session-hosts/) and [Deliver Applications with RemoteApp and App Attach](/azure-virtual-desktop/deliver-applications-remoteapp-app-attach/).

### User profiles

Profiles need their own decision, because FSLogix does not provide a direct migration path from other roaming profile solutions. Two options follow from that.

- **Move user data separately.** Use OneDrive with known folder move, or similar cloud or network storage, so users have a place for their data outside the profile.
- **Copy for small cases.** The `frx` command-line utility can help copy local profiles into a new VHD or VHDX. It is meant for smaller use cases.

One more point matters if you already have profile containers. A container made for a hybrid-identity user on a hybrid Microsoft Entra joined session host cannot be reused when the same user signs in to a Microsoft Entra joined session host. The user's security identifier (SID) changes to a cloud-based SID, and the profile does not load correctly. So settle the join type of the session hosts before you create containers. The join choices are in [Choose the Right Identity Model for Azure Virtual Desktop](/azure-virtual-desktop/choose-the-right-identity-model/).

How profile containers work is in [How FSLogix Profile Containers Work](/azure-virtual-desktop/how-fslogix-profile-containers-work/). Choosing the storage and setting permissions is in [Choose Storage and Set Access for FSLogix Profile Containers](/azure-virtual-desktop/choose-storage-and-set-access-for-fslogix-profile-containers/).

## Steps 3 to 5

Step 3 is Execute migration, step 4 is Optimize in cloud and step 5 is Decommission source. This article does not cover them. The split-environment guidance in step 1 is the planning for the period when waves are moving.

## Common mistakes

- **Relying only on an assessment tool.** Tools can miss undocumented dependencies. Check with application owners.
- **Skipping baseline metrics.** Without them you cannot right-size, and you cannot tell later whether the new environment performs as well as the old one.
- **Expecting profiles to convert by themselves.** There is no direct FSLogix path from other roaming profile solutions. Plan the data move.
- **Moving hybrid-identity users from hybrid Microsoft Entra joined to Microsoft Entra joined session hosts after containers exist.** The cloud-based SID does not load the profile made before.
- **Writing the rollback plan during an incident.** Define it, test it and get it approved first.
- **Moving the most critical group first,** or moving only easy groups and never testing a complex one.
- **Scheduling a wave in a busy business period.**
- **Leaving the overlap open-ended.** Running across both environments for a long time adds risk.
- **Forgetting vendor and licensing checks.** Confirm that each vendor's software works on Azure and which licensing models apply.

## How to validate this in your environment

1. **Check the inventory.** Every user group has an owner, a list of apps, a dependency list and a group type (production, test or development). The application owners have confirmed the lists.
2. **Check the baseline.** For each group you have CPU, memory, disk, network, peak concurrency and any special hardware such as GPUs on record.
3. **Check the lists.** The remediation list marks blockers and later items. The risk register has an owner and a timeline for each risk.
4. **Check the order.** The first wave contains simple groups, non-production environments and one or two complex groups. No wave falls in a critical business period.
5. **Check profiles.** For a small set of test users, try the `frx` utility or a known folder move in a non-production setup. Confirm the user's data is where you expect it.
6. **Check rollback.** The definition of a failed deployment has thresholds. You have run the rollback in a staging environment and it returned the system to a known-good state.
7. **Check approval.** The plan and rollback have written approval, an agreed decision maker and go or no-go checkpoints.
8. **After each wave,** compare the results with the baseline and update the plan and the rollback steps. If the move causes problems, start with [Troubleshoot AVD: Turn On the Logs and Learn to Read Them](/azure-virtual-desktop/troubleshoot-avd-start-here/).

## Sources

- [Plan your migration](https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/plan-migration)
- [Assess your workloads for cloud migration](https://learn.microsoft.com/azure/cloud-adoption-framework/plan/assess-workloads-for-cloud-migration)
- [FSLogix FAQ](https://learn.microsoft.com/fslogix/overview-faq)
