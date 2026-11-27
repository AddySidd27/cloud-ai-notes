---
title: "Compute Engine in a Google Cloud Landing Zone: Where VMs Live"
layout: post.njk
permalink: /google-cloud/compute-engine-in-a-landing-zone/
order: 407
part: 7
tags: gcp-lz
deck: "Say which project, subnet, service account, firewall rules and organization policies a Compute Engine VM depends on, and check each one."
---

A virtual machine (VM) does not stand alone. It depends on several other parts of a landing zone: a project, a subnet, a service account, firewall rules and organization policies. If you are about to create VMs in a landing zone that already exists, this article shows what to look for in each place, so you can ask the right questions before you build. Each term is defined in the Key terms table.

It does not cover how people sign in to a VM. That is in [Reaching a Compute Engine VM: OS Login, IAM Roles and IAP](/google-cloud/reaching-a-vm-os-login-and-iap/). It assumes Shared VPC, which [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/) explains.

## Key terms

| Term | Meaning |
|---|---|
| IAM role | Explained in [Who Can Sign In to Google Cloud: Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). |
| Editor role | A basic role. Explained in [Who Can Sign In to Google Cloud: Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). |
| Organization and project | Explained in [Organization, Folders and Projects](/google-cloud/organization-folders-and-projects/). |
| Shared VPC | Allows an organization to connect resources from multiple projects to a common VPC network. |
| Shared VPC network | A network defined in a host project and made available as a centrally shared network. |
| Host project | A project that contains one or more Shared VPC networks. |
| Shared VPC Admin | Has the Compute Shared VPC Admin and Project IAM Admin roles. Enables a project as a host project and attaches service projects to it. |
| Service project | A project that a Shared VPC Admin has attached to a host project. It can use the host project's shared subnets. |
| Subnet | Explained in [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/). A VM gets its primary internal IPv4 address from its subnet. |
| Network User role | The role (`compute.networkUser`) that gives access to the whole host project or to selected subnets of its Shared VPC networks. |
| Service Project Admin | A principal (see [Who Can Sign In to Google Cloud: Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/)) that a Shared VPC Admin has granted the Network User role, so it can use the host project's shared subnets from a service project. It should have the Instance Admin (`compute.instanceAdmin`) role on the service project. |
| Security Admin role | The role (`compute.securityAdmin`) that a Shared VPC Admin grants on the host project. It manages firewall rules. |
| Firewall rule | Explained in [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/). For a Shared VPC network, firewall rules are created in the host project. |
| Service account | A special kind of account used by an application or compute workload, rather than a person. |
| Attached service account | The service account a VM runs as. Applications on the VM use it to authenticate. |
| Default Compute Engine service account | A service account that a project has when the Compute Engine API is enabled. |
| User-managed service account | A service account you create yourself. The default Compute Engine service account is also this kind. |
| Service agent | An account that Google Cloud creates and manages, and assigns to your project automatically. You cannot attach it to a VM. |
| Access scope | The legacy method of setting what a VM is authorized to do. A new VM gets a default set of access scopes. You set them on the VM. |
| `cloud-platform` scope | The full access scope. With it set, the IAM roles of the service account decide what the VM can do. |
| Application Default Credentials | A way for your code to authenticate with the attached service account. |
| Organization policy constraint | Explained in [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/). |
| Managed constraint | Explained in [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/). |
| OS Login | A way to control who can sign in to a Linux VM with IAM roles instead of SSH keys. Explained in [Reaching a Compute Engine VM: OS Login, IAM Roles and IAP](/google-cloud/reaching-a-vm-os-login-and-iap/). |

## A VM lives in a service project

In a Shared VPC setup, there are two kinds of project. The host project owns the network. A service project holds the workload. When you create a VM, you create it in a service project.

- A project cannot be a host project and a service project at the same time.
- Each service project can attach to only one host project.
- Shared VPC connects projects within the same organization.
- Billing for a resource that uses a Shared VPC network is attributed to the service project.
- Using a Shared VPC network is not mandatory. A service project can still use networks in its own project.

If your landing zone uses Shared VPC, find out which host project your workload project is attached to. If it is not attached, a Shared VPC Admin has to do that first.

## The VM takes its address from a shared subnet

When you create a VM, you choose a shared subnet from the host project. Two things follow.

- The VM's primary internal IPv4 address comes from that subnet.
- The VM must be in the same region as the subnet, even though the subnet and the VM are in different projects.

To use the subnet, the Service Project Admin needs the Network User role. It should have the Instance Admin role on the service project. A Shared VPC Admin grants it for the whole host project or for chosen subnets only; with subnet-level permission you can use only those subnets. The roles are listed in [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/).

A VM that already exists in a service project cannot be switched to a Shared VPC network. It has to be recreated. Plan this before you attach a project that already has VMs.

## Firewall rules apply to the VM

Traffic between VMs on internal addresses is subject to the applicable firewall rules. Firewall rules for the Shared VPC network are created in the host project, and Security Admins manage them. A Shared VPC Admin grants the Security Admin role on the host project. Firewall design is in [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/).

## The VM runs as a service account

A VM can have only one attached service account. You can attach the same service account to many VMs, and a change to that service account then affects all of them. You can attach a service account when you create the VM, or change it later. Code on the VM uses Application Default Credentials to authenticate with the attached service account.

### The default service account

A project that has the Compute Engine API enabled has a default Compute Engine service account. Its name looks like `PROJECT_NUMBER-compute@developer.gserviceaccount.com`. It is attached by default to VMs that you create with the Google Cloud CLI or the Google Cloud console. You can choose to attach no service account at all.

The default service account might automatically be granted the Editor role on your project. Disable that automatic grant by enforcing the `iam.automaticIamGrantsForDefaultServiceAccounts` organization policy constraint. Newer organizations have this constraint enforced by default, so check whether yours does.

### A dedicated service account for each workload

The default service account is also user-managed. To avoid giving an application more permission than it needs, create a new user-managed service account, grant it only the roles your application needs, and attach it to the VM.

### Roles and access scopes

Both the IAM roles of the service account and the access scopes of the VM must allow an action before the application on the VM can use a resource. A new VM is configured with a default set of access scopes. Access scopes are the legacy method. The best practice is to set the full `cloud-platform` access scope on the VM and then control access by granting IAM roles to the service account.

### Service agents are different

Service agents are created and managed by Google Cloud. You cannot attach a service agent to a VM.

## Organization policies that touch a VM

These three constraints affect where a VM can attach and which permissions its default service account gets. Other constraints affect a new VM or its project; they follow the table. The wider set of guardrails is in [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/).

| Constraint | What it does |
|---|---|
| `compute.restrictSharedVpcHostProjects` | Limits which host projects a project can attach to. |
| `compute.restrictSharedVpcSubnetworks` | Limits which Shared VPC subnets a service project can use. |
| `iam.automaticIamGrantsForDefaultServiceAccounts` | When enforced, stops the default Compute Engine service account from being granted the Editor role automatically. |

The two Shared VPC constraints apply to new attachments and new resources. Existing attachments, and existing VMs in a subnet that a policy now blocks, are not changed.

These constraints can affect a new VM or its project:

| Constraint | What it does |
|---|---|
| `compute.managed.vmExternalIpAccess` | Defines whether Compute Engine VM instances are allowed to use IPv4 external IP addresses. |
| `compute.managed.requireOsLogin` | When enforced, requires OS Login on all newly created projects. On new and existing projects, it prevents metadata updates that disable OS Login. |
| `compute.requireShieldedVm` | When enforced, requires that all new Compute Engine VM instances use the Shielded VM options (extra protection settings for a VM). Existing running instances continue to work as usual. |

If a new VM is refused, or an update that disables OS Login fails, check these along with the Shared VPC constraints.

## What a VM needs, in one view

![An organization contains a host project and a service project, which a Shared VPC Admin attaches to the host project. The host project holds a Shared VPC network with a shared subnet, and the firewall rules. The service project holds a VM instance that gets its internal IP from the subnet, is subject to the firewall rules and runs as an attached service account. Three organization policy constraints that affect attachment and the default service account apply.](/img/google-cloud/google-cloud-compute-engine-in-a-landing-zone.svg)

*Source: [Shared VPC](https://docs.cloud.google.com/vpc/docs/shared-vpc) and [Service accounts](https://docs.cloud.google.com/compute/docs/access/service-accounts).*

| The VM needs | It comes from | Role or action involved |
|---|---|---|
| A project to live in | A service project attached to a host project | A Shared VPC Admin attaches the service project |
| An internal IP address | A shared subnet in the same region as the VM | The Service Project Admin needs the Network User role; a Shared VPC Admin grants it |
| Firewall rules that allow its traffic | Firewall rules of the Shared VPC network, created in the host project | Security Admins manage firewall rules |
| An identity | One attached service account | Recommended: create a user-managed service account and grant it only the roles the app needs |
| Permission from organization policies | Constraints that do not block the Shared VPC attachment or the subnet | Set on the organization, a folder or a project |

## Common mistakes

- Creating a VM in a service project and expecting to change its network afterwards. An existing VM cannot be switched to a Shared VPC network. Recreate it.
- Choosing a different region from the shared subnet. The VM must be in the subnet's region.
- Leaving the default Compute Engine service account attached and letting it keep the Editor role. Create a service account for the workload and give it only the roles it needs.
- Expecting to attach several service accounts. A VM has one.
- Trying to attach a service agent. You cannot.
- Granting roles to the service account but leaving access scopes that are too narrow. Both must allow the action. Set the `cloud-platform` scope and control access with roles.
- Looking for the firewall rules of a Shared VPC network in the service project. They are in the host project, and Security Admins manage them.
- Assuming a billing line for the VM appears in the host project. Billing is attributed to the service project.
- Expecting a new policy to change VMs or attachments that already exist. The two Shared VPC constraints apply to new ones.

## How to check this in your own project

1. Find the project the VM is in. Check that it is attached to a host project as a service project.
2. Find the subnet the VM uses. Check that it is a shared subnet from the host project, and that the VM is in the subnet's region.
3. Check that the VM's internal IP address is from that subnet's address range.
4. Check which service account is attached. If its name looks like `PROJECT_NUMBER-compute@developer.gserviceaccount.com`, it is the default service account.
5. Look at the roles of that service account on the project. If it has the Editor role, ask whether that was intended and whether the constraint in step 6 is enforced.
6. Check whether the `iam.automaticIamGrantsForDefaultServiceAccounts` constraint is enforced on your project, or ask whoever sets organization policies.
7. Check the access scopes on the VM. The recommended setting is `cloud-platform`. If the scopes are narrower, the VM can be blocked even when its service account has the role.
8. Look in the host project, or ask someone who has the Security Admin role there, which firewall rules apply to the VM's network.
9. If a Shared VPC subnet is refused for a new VM, ask whether `compute.restrictSharedVpcSubnetworks` or `compute.restrictSharedVpcHostProjects` is set, and whether the Service Project Admin has the Network User role on the subnet.
10. If a new VM is refused, check the constraints in the second table. Ask whether `compute.managed.vmExternalIpAccess`, `compute.managed.requireOsLogin` or `compute.requireShieldedVm` is set on the project.

For the next steps, see [Reaching a Compute Engine VM: OS Login, IAM Roles and IAP](/google-cloud/reaching-a-vm-os-login-and-iap/) and [Seeing What VMs Do: Ops Agent and Audit Logs](/google-cloud/vm-logging-and-monitoring/).

## Sources

- [Shared VPC](https://docs.cloud.google.com/vpc/docs/shared-vpc)
- [Service accounts (Compute Engine)](https://docs.cloud.google.com/compute/docs/access/service-accounts)
- [Organization policy constraints](https://docs.cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints)
