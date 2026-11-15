---
title: "Host Pools, Application Groups and Workspaces: The Rules That Connect Them"
seoTitle: "AVD Host Pools, App Groups and Workspaces"
layout: post.njk
permalink: "/azure-virtual-desktop/host-pool-application-group-workspace-rules/"
order: 109
part: 9
tags: [avd-series]
deck: "Learn how the AVD objects relate, which choices cannot be changed later and why a user sometimes sees nothing."
description: "Learn the rules that connect Azure Virtual Desktop host pools, application groups and workspaces, and how to find out why a user sees an empty feed."
---

A user opens Windows App (the Microsoft app users run to connect) and sees nothing. The session hosts are healthy and nothing is wrong with the network. The cause is often one of the rules that connect the four Azure Virtual Desktop (AVD) objects (host pool, session host, application group and workspace): a missing assignment, an application group that is not in a workspace, or a setting that hides what you published.

This article explains those objects and the rules between them, shows which choices cannot be changed after creation, and gives a short order of checks for an empty feed (the list of desktops and apps the client shows is empty). The [architecture article](/azure-virtual-desktop/azure-virtual-desktop-architecture/) introduced the objects. This one goes deeper into how they fit together.

## Key terms

| Term | Meaning |
|---|---|
| Host pool | A collection of Azure virtual machines that are registered to AVD as session hosts. All hosts in one pool should come from the same image (the saved copy of Windows and apps used to build a virtual machine). |
| Session host | A virtual machine in a host pool that runs the users' desktops or apps. |
| Pooled host pool | Users are load balanced (spread across hosts) to any session host in the pool. Several users can be on one host at the same time. |
| Personal host pool | Each session host is assigned to one user. |
| Application group | Controls access to a full desktop, or to a set of applications, from a single host pool. |
| Desktop application group | An application group that publishes the full Windows desktop. |
| RemoteApp application group | An application group that publishes individual applications you select. |
| Workspace | A logical grouping of application groups ([terminology](https://learn.microsoft.com/en-us/azure/virtual-desktop/terminology#workspaces)). Users see its application groups' resources in their client. |
| Assignment | Giving a user or group access to an application group. |
| Azure RBAC role | A set of permissions you give to a person or group at a scope. A scope is a resource, such as an application group. |
| Feed | The list of desktops and apps a user sees in the client. |
| Security group | A Microsoft Entra group used for permissions. A distribution group is a different kind of group, made for sending email to a list of people, and AVD does not support it. |
| Microsoft Entra tenant | Your organization's own instance of Microsoft Entra ID, which holds its users and groups. |
| Metadata | The information AVD stores about your objects, such as host pool, application group and workspace names. |
| Conditional Access | A Microsoft Entra feature that allows or blocks sign-ins based on conditions you set, such as user, app or device. |
| Windows App | The Microsoft app that users run to connect to AVD and Windows 365. |
| Cloud Solution Provider (CSP) | A Microsoft partner that sells and manages Azure subscriptions for customers. |
| Resource provider | The part of Azure that handles one kind of resource. AVD objects are handled by the Microsoft.DesktopVirtualization resource provider, which must be registered in the subscription. |
| Preferred application group type | A setting on pooled host pools that decides which type users see when they are assigned to both a desktop and a RemoteApp application group on that pool. |
| Deployment scope | A choice made at creation: Geographical or Regional. It decides where AVD stores an object's metadata. Geographical stores the metadata for a whole geography (the default). Regional stores it in one Azure region. |
| Management approach | A choice made at host pool creation: standard management, or session host configuration. With a session host configuration, AVD keeps the settings for the hosts and creates, updates and scales them for you. |

## The four objects in one picture

![A workspace at the top lists a desktop application group and two RemoteApp application groups. All three point to one pooled host pool that contains session hosts. Microsoft Entra ID users and user groups are assigned to the application groups. A panel lists four rules about how the objects relate.](/img/avd/AVD-Post-09-Object-Relationships-v3.png)

*How the four objects relate. Personal host pools and the session host configuration are left out. Source: [Azure Virtual Desktop terminology](https://learn.microsoft.com/en-us/azure/virtual-desktop/terminology).*

Each arrow points from the object that lists or uses something to the object it uses. The workspace lists application groups. Each application group publishes from one host pool. The host pool contains session hosts. Users are assigned to application groups, not to host pools and not to workspaces.

## The rules

These rules decide whether a design works.

| Rule | Detail |
|---|---|
| Application group to host pool | An application group can be assigned to a single host pool. You can assign several application groups to the same host pool. |
| Application group to workspace | An application group can be assigned to a single workspace. Each application group must be associated with a workspace for users to see what it publishes. |
| Desktop groups per pool | A host pool can have only one desktop application group. It can have many RemoteApp application groups. |
| Where each type works | Desktop application groups work with pooled or personal host pools. RemoteApp application groups work with pooled host pools only. |
| An application group needs a host pool | An application group cannot exist without one. |
| Users to groups | Users can be assigned to several application groups across several host pools. Users in several RemoteApp groups on one pool get the combined list of applications. |
| Same tenant | Users must be in the same Microsoft Entra tenant as their workspace, host pool and application group. Session host virtual machines can be in a different tenant if they are joined to the user's Active Directory (the on-premises Windows domain), or one that trusts it. |
| Same deployment scope | Regional and Geographical objects cannot be mixed. A regional host pool can only be in a regional workspace and can only contain regional application groups. |
| Same location | A host pool, its application groups and their workspace must all be in the same location. The FAQ says the application group's location "should" match its host pool's, to avoid moving data between locations. The service enforces it: creating an application group in a different location from its host pool fails with "ApplicationGroup must be in same location as associated HostPool". The workspace must also be in the same location as its application groups. |

The FAQ words the host pool rule as "should" and the workspace rule as "must". The [troubleshooting page for PowerShell](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-powershell) shows both are enforced when you create the objects. A consequence, which follows from the rule and is not stated in these words: a design that spans several locations needs more than one workspace, and users who need resources from several locations subscribe to more than one workspace.

## What can be changed later

Three choices are fixed when you create the object. A fourth, the preferred application group type, can change. Plan the fixed ones before the first deployment.

| Choice | Can it change later? |
|---|---|
| Host pool type (pooled or personal) | No ([Azure Virtual Desktop FAQ](https://learn.microsoft.com/en-us/azure/virtual-desktop/faq#can-i-change-from-pooled-to-personal-host-pools)). You cannot convert a pool. You can move registered virtual machines to a pool of the other type. |
| Management approach (standard or session host configuration) | No ([Host pool management approaches](https://learn.microsoft.com/en-us/azure/virtual-desktop/host-pool-management-approaches)). A pool created without a session host configuration cannot get one later. |
| Deployment scope (Geographical or Regional) | No ([service architecture and resilience](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience#deployment-scope)). Regional is offered only in regions that support it. |
| Preferred application group type | Yes. You must set it when you create the pool, and you can change it afterward. |

The management approach decides who looks after session hosts. With a session host configuration, AVD creates, updates and scales the hosts using the stored settings. It works with pooled host pools only, and you cannot create, update or scale hosts outside the service with tools built for standard management. With standard management you create and update the hosts yourself, and you decide how many exist (autoscale can still turn them on and off). This suits existing automation scripts. The article on [creating, updating and replacing session hosts](/azure-virtual-desktop/create-update-replace-session-hosts/) covers host management in depth.

Regional scope is offered only in some regions and was in preview at the time of writing. Check the [Regional host pools](https://learn.microsoft.com/en-us/azure/virtual-desktop/regional-host-pools) page for its current status before you choose it.

## Where assignment happens

AVD publishes an application group to users by assigning the Desktop Virtualization User role to the user or group, with the application group as the scope. The `New-AzRoleAssignment` PowerShell command (a cmdlet) does this. You can also do it in the portal ([Deploy Azure Virtual Desktop, Assign users to an application group](https://learn.microsoft.com/en-us/azure/virtual-desktop/deploy-azure-virtual-desktop#assign-users-to-an-application-group)).

The person who makes the assignment needs the User Access Administrator or Owner role (or any role that can create role assignments) on the application group. Creating host pools and other objects needs the Contributor role on the subscription or resource group.

Two points to remember.

- **Use security groups.** AVD does not support Microsoft Entra distribution groups. If a user is in the group only through a distribution list, they will see nothing.
- **Assignments belong to the tenant.** If a subscription moves from one Microsoft Entra tenant to another, the service loses track of the assignments, because they are tied to the old tenant. Assign the users to their application groups again.

## Desktop and RemoteApp on the same host pool

A pooled host pool can have both a desktop application group and RemoteApp application groups. That can give one user two sessions on the same pool: one for the desktop and one for an application. Microsoft warns that two sessions to the same host pool can overload session hosts, leave users stuck at sign-in, make connections fail, turn the remote session black and crash applications.

The **preferred application group type** setting reduces this. If a user is assigned to both types on one pool, the client shows only the preferred type.

| Application group types on the pool | The user is assigned to | Preferred type | The client shows |
|---|---|---|---|
| Desktop and RemoteApp | Both | Desktop | Desktop |
| Desktop and RemoteApp | Both | RemoteApp | RemoteApp applications |
| Desktop and RemoteApp | Both | Not set | Desktop |
| Desktop and RemoteApp | Desktop only | Either | Desktop |
| Desktop and RemoteApp | RemoteApp only | Either | RemoteApp applications |

Four details to know.

- The setting affects only users who are assigned to both types on the same pool. A user can still see a desktop from one pool and RemoteApp applications from another.
- In the Azure portal, the default is Desktop. The portal also creates a desktop application group named after the host pool with the suffix `-DAG`, for example `hp01-DAG`, whichever preferred type you choose. You can delete it afterward if you want only RemoteApp. These two portal behaviors do not happen when you create the pool with PowerShell or the Azure CLI.
- Older pools with no preferred type now show only the desktop to users assigned to both types. This enforcement is still rolling out to all Azure regions.
- The setting controls what the client shows, not what the service allows. The `ms-avd:connect` URI scheme (a link format that starts a connection directly) can still open both, and Microsoft does not recommend this.

As a recommendation: if the same users need both a full desktop and RemoteApp applications, consider separate host pools. It costs more virtual machines, but it removes the two-sessions problem instead of hiding it.

## Plan the objects for your design

- **Create a host pool for each group of users whose compute, image or security needs differ.** Do not create one just because a department asked. The [host pool planning article](/azure-virtual-desktop/plan-your-host-pools/) shows how to group users.
- **Create an application group for each distinct set of resources and each distinct audience.** Assign security groups to application groups so that adding a person is a group membership change.
- **Create a workspace for each audience and location that should see a set of application groups together.** Name them so users can tell them apart.
- **Write down the settings that cannot change** before the first host pool is created: pool type, management approach and deployment scope.

## When a user sees nothing

Start at the top and work down. The order is how quickly each check can be ruled out. [Troubleshoot Azure Virtual Desktop service connections](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-service-connection) covers the first three checks, the tenant move and Conditional Access. The workspace, scope, location and preferred type checks come from the rules above.

| Check | What it tells you |
|---|---|
| Is the user assigned to an application group, directly or through a group? | Confirm the assignment, for example with `Get-AzRoleAssignment -SignInName <userupn>`. That command lists only assignments made directly to the user. Add `-ExpandPrincipalGroups` to include assignments made to groups the user belongs to, which you need when you assign through groups. |
| Is the user signing in with the expected account? | A different account has a different assignment. In the web client, also rule out cached credentials. |
| Is the user's group a security group? | Distribution groups are not supported. |
| Is the application group in a workspace? | Each application group must be associated with a workspace for users to see it. |
| Is the workspace the same deployment scope and location as the application group? | Mixed scope is not allowed, and the service requires the same location. |
| Does the preferred application group type hide what you published? | A user assigned to both types sees only the preferred type. |
| Did the subscription move between tenants, or change owner? | After a tenant move, assign users again. For a subscription transferred by a Cloud Solution Provider, re-register the Microsoft.DesktopVirtualization resource provider. |
| Is a Conditional Access policy blocking an app? | In the web version of Windows App, the user needs access to both the AVD and Windows 365 apps in the Conditional Access policy. The Windows Cloud Login app matters when single sign-on (the user signs in once and is not asked again) is on. |

If the desktop appears but will not open, the object model is working and the problem is in the connection or the session host. The [failure article](/azure-virtual-desktop/how-azure-virtual-desktop-fails/) separates those cases, and the [connection article](/azure-virtual-desktop/follow-a-connection-step-by-step/) walks through a connection step by step.

## Common mistakes

- **Assigning users to a host pool.** The assignment belongs on the application group.
- **Building a host pool for each department.** Pools exist to group hosts with the same needs.
- **Deleting the `-DAG` application group without knowing why it exists.** That is fine for a RemoteApp-only pool. It surprises people who later want to publish a desktop.
- **Expecting one workspace to hold everything.** Location and deployment scope rules limit what one workspace can hold.
- **Assigning both desktop and RemoteApp groups on one pool without thinking about sessions.** The preferred type hides one of them, which may not be what you intended.
- **Choosing pool type, management approach or deployment scope casually.** None of these can be changed later.

## How to validate your object model

Run these checks before you add users.

1. For each application group, note its host pool and workspace, and confirm both are in the same location and deployment scope.
2. Assign a test user through a security group and sign in with Windows App. Confirm the expected resources appear and nothing extra.
3. Test a user who is in two groups, one for each application group type, on a pool with each setting of the preferred type. Confirm the client shows what the table says.
4. Remove the test user from the group and confirm the resources disappear after the client refreshes.

Next: [Follow a Connection Step by Step: Reverse Connect, RDP Shortpath and Where It Breaks](/azure-virtual-desktop/follow-a-connection-step-by-step/).

## Sources

- [Azure Virtual Desktop terminology](https://learn.microsoft.com/en-us/azure/virtual-desktop/terminology)
- [Regional host pools](https://learn.microsoft.com/en-us/azure/virtual-desktop/regional-host-pools)
- [Troubleshoot Azure Virtual Desktop service connections](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-desktop/troubleshoot-service-connection)
