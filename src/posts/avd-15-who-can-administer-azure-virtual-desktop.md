---
title: "Who Can Administer Azure Virtual Desktop: Roles, Scopes and Delegation"
seoTitle: "Who Can Administer AVD: Roles and Scopes"
layout: post.njk
permalink: "/azure-virtual-desktop/who-can-administer-azure-virtual-desktop/"
order: 115
part: 15
tags: [avd-series]
deck: "Use the built-in AVD roles to give each person only what they need, at the right scope, and avoid the common role mistakes."
description: "Give the right people the right access to Azure Virtual Desktop: the built-in roles, scopes, extra roles you need, a tiered delegation model and the Entra join exception."
---

Two bad habits are easy to fall into. The first is giving every administrator Contributor on the subscription because it is quick. The second is giving the help desk so little that every stuck session needs an engineer. AVD has its own built-in roles that avoid both, and they are less well known than the general Azure roles.

This article lists the roles, explains what each can and cannot do, shows which extra roles a task needs, and ends with a tiered delegation model.

## Key terms

| Term | Meaning |
|---|---|
| Azure RBAC | Azure role-based access control. You give a person or group a role at a scope. |
| Contributor | A general Azure role that can change everything in its scope. It cannot give other people access. |
| User Access Administrator | A general Azure role that can give other people access to resources. It is not an AVD role. |
| Host pool | A group of virtual machines that run the same desktop or apps. |
| Session host | A virtual machine in a host pool that users connect to. |
| Application group | The part of AVD that publishes a desktop or apps to users. You assign users here. |
| Workspace | The list of desktops and apps that a user sees in their client. |
| Microsoft Entra joined | A virtual machine that is joined to Microsoft Entra ID, not only to Active Directory. |
| Session host configuration | A way to create a host pool where AVD itself creates and updates the session hosts. See [Host pool, application group and workspace rules](/azure-virtual-desktop/host-pool-application-group-workspace-rules/). |
| Drain mode | A host setting that stops new sessions from starting on that session host. Existing sessions continue. |
| Service principal | The identity that an Azure service uses to act in your tenant. |
| Managed identity | An identity that Azure manages for a resource, so you need no password. |
| Start VM on Connect | A host pool setting that powers on a stopped session host when a user connects. |
| Autoscale | A scaling plan that starts and stops session hosts on a schedule. |
| Role | A named set of permissions. |
| Scope | The level where a role applies: management group, subscription, resource group or a single resource. |
| Least privilege | Giving only the permissions needed for the task. |
| Data action | An action a user takes while using a service, such as opening an application. |
| Session host operator | A person who works with session hosts, for example to put them in drain mode. |
| Registration token | A time-limited key that lets a new virtual machine join a host pool as a session host. |
| Resource provider | The Azure service that handles requests for a type of resource. For AVD it is `Microsoft.DesktopVirtualization`. |

## Two kinds of permission

AVD access has two sides, and they are easy to mix up.

- **Who can manage AVD.** These are Azure roles on the host pool, application group, workspace or the resource groups that hold them.
- **Who can use AVD.** This is the Desktop Virtualization User role on an application group, which lets a user open what it publishes. It is a data action, `useApplications`.

On top of that, Microsoft Entra joined session hosts have a third permission, to sign in to the virtual machine. That is covered in [The Microsoft Entra join exception](#the-microsoft-entra-join-exception).

## The built-in roles

The table summarizes the AVD roles and what each does. For the full permission lists, see [Built-in Azure RBAC roles for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/rbac).

| Role | What it allows | Watch for |
|---|---|---|
| Desktop Virtualization Contributor | Manage all AVD resources, except user or group assignment. | It does not grant users access to compute resources. For assignments you also need User Access Administrator. |
| Desktop Virtualization Reader | View all AVD resources, no changes. | |
| Desktop Virtualization User | Use an application on a session host from an application group, as a non-administrative user. | Assign it on the application group. |
| Desktop Virtualization Host Pool Contributor | Manage all aspects of a host pool. | To create virtual machines you need Virtual Machine Contributor. To deploy from the portal you also need the Application Group Contributor and Workspace Contributor roles, or use Desktop Virtualization Contributor. |
| Desktop Virtualization Host Pool Reader | View a host pool. | |
| Desktop Virtualization Application Group Contributor | Manage an application group, except user or group assignment. | For assignment add User Access Administrator. |
| Desktop Virtualization Application Group Reader | View an application group. | |
| Desktop Virtualization Workspace Contributor | Manage workspaces. | To see applications in a related application group, add Application Group Reader. |
| Desktop Virtualization Workspace Reader | View a workspace. | |
| Desktop Virtualization User Session Operator | Send messages, disconnect sessions and sign users out. It cannot remove session hosts or change drain mode. It can see assignments but not change members. | Assign it to specific host pools. At resource group level it gives read permission on all host pools in the group. |
| Desktop Virtualization Session Host Operator | View and remove session hosts, and change drain mode. | It cannot add session hosts in the portal, because it has no write permission on host pool objects. Outside the portal it can add hosts if the registration token is valid and Virtual Machine Contributor is also assigned. |

Azure Virtual Desktop has no specific Owner role. You use the general Owner role for the service objects ([Built-in Azure RBAC roles for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/rbac)).

Three more roles exist for the service itself. They let the AVD resource provider act on virtual machines.

- Desktop Virtualization Power On Contributor: start.
- Desktop Virtualization Power On Off Contributor: start and stop.
- Desktop Virtualization Virtual Machine Contributor: create, delete, update, start and stop.

Do not confuse the last one with the general Azure Virtual Machine Contributor role in the table above.

You give these roles to the Azure Virtual Desktop service principal, not to people. For Start VM on Connect and power management autoscale, a managed identity on the host pool also works. For dynamic autoscale, use the service principal.

The page [Assign Azure RBAC roles or Microsoft Entra roles to the Azure Virtual Desktop service principals](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-principal-assign-roles) shows how. To assign them you need the `Microsoft.Authorization/roleAssignments/write` permission, which User Access Administrator and Owner include ([prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-principal-assign-roles#prerequisites)).

| Feature | Roles | Scope |
|---|---|---|
| Autoscale, power management | Power On Off Contributor ([Create and assign an autoscale scaling plan](https://learn.microsoft.com/en-us/azure/virtual-desktop/autoscale-create-assign-scaling-plan)) | Subscription. A lower scope stops autoscale from working properly. |
| Autoscale, dynamic | Power On Off Contributor and Desktop Virtualization Virtual Machine Contributor | Subscription. A lower scope stops autoscale from working properly. |
| Start VM on Connect | Power On Contributor ([Configure Start VM on Connect](https://learn.microsoft.com/en-us/azure/virtual-desktop/start-virtual-machine-connect)) | Subscription is recommended for several host pools. A lower scope is allowed if it contains the target session hosts. |

![A nine-row table with three columns: task, built-in role and scope or extra role. The tasks are sign users out, drain and remove session hosts, manage a host pool, publish apps, manage a workspace, manage all AVD resources, view only, use a desktop or app, and sign in to a Microsoft Entra joined virtual machine. The roles are User Session Operator, Session Host Operator, Host Pool Contributor, Application Group Contributor, Workspace Contributor, Desktop Virtualization Contributor, Desktop Virtualization Reader, Desktop Virtualization User and Virtual Machine User Login.](/img/avd/AVD-Post-15-Role-Task-Scope-v3.png)

*Read each row from left to right: the task, the role that fits it, then the scope or extra role you also need. Source: [Built-in Azure RBAC roles for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/rbac). The picture leaves out the reader roles for host pools, application groups and workspaces, the service roles, and the Start VM on Connect permission that can be given at a lower scope. Virtual Machine User Login is not needed for host pools that use a session host configuration.*

## Scope matters more than the role

The same role can be harmless or dangerous depending on where you assign it. You can assign each role at the scope you need, and some features have specific scope requirements. Follow these rules:

- **Assign at the lowest scope that works.** A help desk role on one host pool is safer than on a resource group.
- **Assign to groups, not people.** Membership then becomes a request process, not a role change.
- **Keep user access and admin access separate.** The Desktop Virtualization User role goes on the application group. Admin roles go on the objects or their resource groups.
- **Know the resource group side effect.** At resource group level, User Session Operator gives read permission on all host pools in it.

## A tiered delegation model

This is an example model to adapt.

| Tier | Who | Roles | Scope |
|---|---|---|---|
| 1 | Service desk | Desktop Virtualization User Session Operator | Each host pool they support |
| 2 | Operations | Desktop Virtualization Session Host Operator, plus Desktop Virtualization Reader | Host pools they run |
| 3 | AVD engineering | Host Pool Contributor, Application Group Contributor and Workspace Contributor, plus Virtual Machine Contributor where they create hosts | The AVD resource groups |
| 4 | Platform owner | Desktop Virtualization Contributor, plus User Access Administrator for assignments | The AVD resource groups, with a separate approval for assignments |

Why split assignment out: Desktop Virtualization Contributor and Application Group Contributor do not include user or group assignment. That separation is built in, so use it. User Access Administrator is a general Azure role, not an AVD one, so it can manage access to any resource in its scope. Keep its scope as narrow as you can. The person who publishes an application does not need to be the person who decides who can open it.

## Assigning roles

You can assign roles in the portal or with scripts. See [Assign Azure roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-steps) for the methods. The method does not change the permissions. Whatever the method, do these checks:

1. Assign to a security group, not an individual.
2. Pick the scope on the specific resource first. Move up only if it does not work.
3. Check the result afterwards. In the portal, open the Access control (IAM) page of the resource and look at the role assignments (see [List Azure role assignments using the Azure portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-list-portal)).

## The Microsoft Entra join exception

Users of Microsoft Entra joined session hosts need one more permission. Use these roles:

- Assign **Virtual Machine User Login** so users can sign in to the virtual machines.
- Assign **Virtual Machine Administrator Login** to administrators who need local administrator rights.
- You can assign these on the virtual machines, the resource group that holds them, or the subscription. The recommended way is to assign Virtual Machine User Login to the same group used for the application group, at resource group level, so it covers all hosts in the pool.
- For host pools that use a session host configuration, this extra role assignment is not required.

Expect a user without this role to be unable to sign in to the host even though the desktop appears in their client and the application group is assigned correctly. Confirm this in a test. For sign-in and MFA on Microsoft Entra joined hosts, see [How sign-in works](/azure-virtual-desktop/how-sign-in-works-three-authentications-and-sso/).

## Common mistakes

- **Giving the help desk Contributor.** Use User Session Operator on specific host pools.
- **Assigning User Session Operator at resource group level.** It gives read access to all host pools in the group.
- **Assigning users to the host pool or the workspace.** Users go on the application group.
- **Expecting Desktop Virtualization Contributor to assign users.** It does not. Add User Access Administrator.
- **Expecting Session Host Operator to add hosts in the portal.** It lacks write permission on host pool objects.
- **Forgetting Virtual Machine User Login on Microsoft Entra joined hosts in a host pool without a session host configuration.** Expect sign-in to fail.
- **Using individual accounts for role assignments.** Role reviews and leavers become harder.

## How to validate your delegation

These are recommended checks to run with test accounts, in a test environment.

1. Sign in as a Tier 1 test user. Confirm they can sign a user out and cannot drain a host or change a setting.
2. Sign in as a Tier 2 test user. Confirm they can drain and remove a host, and cannot add one in the portal.
3. Sign in as a Tier 3 test user. Confirm they can publish an application, and cannot assign users.
4. For a Microsoft Entra joined host pool without a session host configuration, remove Virtual Machine User Login from a test user and confirm sign-in fails. Add it back and confirm it works.
5. List the role assignments on each resource group and check that each one traces to a group and a reason.

Next: [Required Connectivity for Azure Virtual Desktop: Endpoints, Proxies, DNS and Private Link](/azure-virtual-desktop/required-connectivity-for-azure-virtual-desktop/).

## Sources

- [Built-in Azure RBAC roles for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/rbac)
- [Microsoft Entra joined session hosts](https://learn.microsoft.com/en-us/azure/virtual-desktop/azure-ad-joined-session-hosts)
- [Assign roles to the Azure Virtual Desktop service principals](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-principal-assign-roles)
