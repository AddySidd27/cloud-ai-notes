---
title: "Reaching a Compute Engine VM: OS Login, IAM Roles and IAP"
layout: post.njk
permalink: /google-cloud/reaching-a-vm-os-login-and-iap/
order: 408
part: 8
tags: gcp-lz
deck: "Let an engineer sign in to a Linux VM through an IAM role instead of SSH keys that you create and manage individually, pick the right login role, and reach a VM that has no external IP address."
description: "Learn how OS Login, IAM roles and Identity-Aware Proxy TCP forwarding work together so engineers can reach Compute Engine VMs without managing SSH keys and without external IP addresses."
---

A new engineer needs to log in to a Linux virtual machine (VM) in Compute Engine, Google Cloud's service for VMs. Remote login to a VM uses SSH for Linux and RDP for Windows. You can manage SSH keys yourself, or you can give the engineer an IAM role. IAM is the Google Cloud system that controls who may do what, and a role is a set of permissions you grant to a person or group. This article is for people who run Compute Engine VMs and want to choose the second way. After reading it you can say what OS Login does, which role to grant for login with or without administrator rights, and what must be in place for a VM with no external IP address to be reachable.

The OS Login roles in this article are for Linux VMs. RDP appears only where the tunnel and the firewall rule are described.

To see where VMs sit in the wider design, read [Compute Engine in a Google Cloud Landing Zone: Where VMs Live](/google-cloud/compute-engine-in-a-landing-zone/). For the firewall side, read [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/).

## Key terms

| Term | Meaning |
|---|---|
| Service account | An account attached to a VM. A user who connects to the VM can use all of the IAM permissions granted to it. |
| OS Login | A way to manage SSH access to your instances using IAM, without having to create and manage individual SSH keys. It links your Linux user account to your Google identity. |
| Metadata-based SSH keys | SSH keys stored in project or instance metadata. Instances that use OS Login cannot use them. |
| Project metadata and instance metadata | The places where you set values such as `enable-oslogin`: project metadata applies to all VMs in the project, instance metadata to one VM. |
| POSIX account | The POSIX information that OS Login sets up for your Google account: a username, a user ID (UID), a group ID (GID) and a home directory. |
| Identity-Aware Proxy (IAP) | The Google Cloud service whose TCP forwarding feature lets you reach VMs that do not have external IP addresses. |
| IAP TCP forwarding | An encrypted tunnel over which you can forward SSH, RDP and other traffic to VMs, including VMs that have no external IP address or do not permit direct access over the internet. |
| Firewall rule | A rule that applies to the VMs you want to reach through IAP and allows ingress (incoming) traffic from the IAP IP range. Firewall rules and policies are explained in [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/). |

## What OS Login does

OS Login moves the question "who may log in to this VM?" out of SSH key files and into IAM. Key points:

- It is the recommended way to manage many users across multiple instances or projects, and the same Linux account information is used across all instances in the same project or organization.
- Google checks permissions for every login attempt, and permissions are updated automatically when an administrator changes IAM permissions.
- You can optionally require 2-step verification (2FA) for OS Login users.
- When OS Login is on, the instance fetches the SSH keys associated with the Linux user account from the OS Login service.

### Turn OS Login on

Set `enable-oslogin` to `TRUE` in project metadata (all VMs in the project) or instance metadata (one VM). When you create a VM with gcloud (the Google Cloud command-line tool), you can pass `--metadata enable-oslogin=TRUE`.

### Metadata-based SSH keys stop working

Instances that use OS Login cannot use metadata-based SSH keys. When you set OS Login metadata, Compute Engine deletes the VM's `authorized_keys` files and no longer accepts connections from SSH keys that are stored in project or instance metadata.

One exception is a local user account, an account that is not an OS Login user. You can configure an `authorized_keys` file to give access to a local user account even when OS Login is on. Local accounts and OS Login users must have different usernames and UIDs.

### The Linux account OS Login creates

OS Login sets up POSIX account information for a Google identity when the person connects through the console or the gcloud CLI, or imports a public SSH key through the gcloud CLI or the OS Login API.

| Item | Value |
|---|---|
| Username | `USERNAME_DOMAIN_SUFFIX` format. Usernames cannot exceed 32 characters, and longer ones are truncated. |
| External user | A user from a different organization than the one that hosts the instances gets a username prefixed with `ext_`. |
| Service account | A username prefixed with `sa_`. |
| UID | A unique, randomly generated POSIX user ID. |
| GID | A POSIX group ID that matches the UID. |
| Home directory | The path to the user's home directory. |

### OS Login is not supported everywhere

OS Login is not supported on all instance configurations. OS Login is not supported with Windows Server and SQL Server, Fedora CoreOS, SLES 16, or OS Login profiles with a total size greater than 32 KiB. Check that your image supports it before you rely on it.

## The roles that matter

You can grant OS Login IAM roles at the instance, folder, organization or project level. If a user needs SSH access from the Google Cloud console or the Google Cloud CLI, grant the OS Login roles at the project level, or also grant a project-level role that contains the `compute.projects.get` permission. For folders and organizations, see [Google Cloud Organization, Folders and Projects](/google-cloud/organization-folders-and-projects/).

### Login roles

| Role | What it is for |
|---|---|
| `roles/compute.osLogin` | Grants login access without administrator access (`sudo`) to compute instances. |
| `roles/compute.osAdminLogin` | Grants login access with administrator access (`sudo`) to compute instances. |
| `roles/compute.osLoginExternalUser` | For users from a different organization than the VM they connect to. Grant it on the organization. An organization administrator must grant it. |

The first two roles are the choice that matters for login. They differ in one thing: whether the person gets administrator access on the VM (`sudo`). Choose by what the person needs to do on the VM.

### Other roles you need

| Role | Why it appears here |
|---|---|
| `roles/iap.tunnelResourceAccessor` (IAP-secured Tunnel User) | The role for TCP forwarding. It is not a login role. Grant it on the project or the instance. |
| `roles/iam.serviceAccountUser` (Service Account User) | Needed by all users if the VM has a service account. Grant it on the service account. |

The OS Login roles are the ones that grant login.

### The service account of the VM

This section covers only the login side. For how a VM gets its service account, see [Compute Engine in a Google Cloud Landing Zone: Where VMs Live](/google-cloud/compute-engine-in-a-landing-zone/).

When a user connects to a VM, that user can use all of the IAM permissions granted to the service account attached to the VM. So a login role on a VM is also, in effect, a grant of whatever that VM's service account can do. Keep this in mind when you choose which VMs get a service account with wide permissions.

If the VM has a service account, every user also needs `roles/iam.serviceAccountUser`, granted on that service account. The permission for SSH to a VM that uses a service account is `iam.serviceAccounts.actAs`.

## Reaching a VM that has no external IP address

IAP TCP forwarding lets people reach SSH and RDP on a VM without an external IP address. When you use IAP tunneling, the IAP proxies connect to the primary internal IPv4 address of the VM.

![gcloud compute ssh goes through Identity-Aware Proxy (Tunnel User role needed). A firewall rule allows tcp:22 from 35.235.240.0/20. The VM has OS Login on, and the person needs an OS Login role. No external IP needed.](/img/google-cloud/google-cloud-reaching-a-vm-os-login-and-iap.png)

*Source: [Use IAP for TCP forwarding](https://docs.cloud.google.com/iap/docs/using-tcp-forwarding), [About OS Login](https://docs.cloud.google.com/compute/docs/oslogin) and [Set up OS Login](https://docs.cloud.google.com/compute/docs/oslogin/set-up-oslogin).*

The arrows marked "request" show the path of the connection. The firewall rule is not a service in the path. It is drawn after IAP because it must allow traffic from IAP's range for the connection to reach the VM; the arrow marked "allowed by" shows that. The arrows marked "role needed" show a role that must be granted. Before you start, OS Login must be on for the VM (see Turn OS Login on above). Then two things must be in place, and after that you connect.

### 1. A firewall rule that lets IAP in

Check first whether your landing zone already has a rule that does this. Where firewall rules are kept is explained in [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/), and who manages them in [Compute Engine in a Google Cloud Landing Zone: Where VMs Live](/google-cloud/compute-engine-in-a-landing-zone/). If there is none, you need a rule that:

- applies to all VMs that you want to reach through IAP (in the console, set Target to "All instances in the network"),
- allows incoming (ingress) traffic from the IP range `35.235.240.0/20` (for IPv6 VMs, `2600:2d00:1:7::/64`), and
- allows connections to the ports you want to reach through IAP, for example port 22 for SSH and port 3389 for RDP. A port is the number after `tcp:` in a rule; it says which service on the VM the traffic is for.

The `35.235.240.0/20` range is the IAP range. It contains all the IP addresses that IAP uses for TCP forwarding. As a VPC firewall rule, an example is named `allow-ssh-ingress-from-iap` with `--direction=INGRESS`, `--action=allow`, `--rules=tcp:22` and `--source-ranges=35.235.240.0/20`.

The default rules `default-allow-ssh` and `default-allow-rdp` allow SSH and RDP from all IP addresses, not only from IAP. Consider disabling or deleting them if you want to prevent direct SSH or RDP access to your VMs.

### 2. The right roles for the person

| Need | Role | Where to grant it |
|---|---|---|
| Use the tunnel | IAP-secured Tunnel User (`roles/iap.tunnelResourceAccessor`) | On the project (all VMs in it) or on one specific VM, to a user or group |
| Log in to the VM | `roles/compute.osLogin` or `roles/compute.osAdminLogin` if the VM uses OS Login | Project or instance (also folder or organization). For console or gcloud SSH, grant at the project, or also grant a project-level role that contains `compute.projects.get` |
| Use a service account | `roles/iam.serviceAccountUser`, if the VM has a service account | On the service account |

The OS Login roles can go on the project or the instance. For console or gcloud SSH, grant them on the project, or also grant a project-level role that contains `compute.projects.get`. Grant Service Account User on the service account.

To grant the tunnel role on the whole project, use the IAM & Admin page in the Google Cloud console and select Add. To grant it for one VM, use Add principal on the SSH and TCP Resources tab of the IAP page in the console.

A user who has the Owner role on the project can use IAP for TCP forwarding.

The IAP page's table of roles also lists Compute Instance Admin (v1) (`roles/compute.instanceAdmin.v1`) for "SSH access". This article covers VMs that use OS Login, where the OS Login roles above give the login.

`gcloud compute ssh` needs the permissions `iap.tunnelInstances.accessViaIAP`, `compute.instances.get`, `compute.instances.list` and `compute.projects.get`. For VMs that do not use OS Login, it also needs `compute.instances.setMetadata`, `compute.projects.setCommonInstanceMetadata` and `compute.globalOperations.get`.

The person who connects needs the IAP-secured Tunnel User role from the table above.

Some roles are meant for the trusted administrators who set up TCP forwarding and related tasks. To set this up, ask your administrator to grant you the IAP Policy Admin (`roles/iap.policyAdmin`) role on your project. Custom roles or other predefined roles might also give the required permissions. If you work in a project that you created, you have the permissions you need to perform these setup tasks.

You can add a condition to the IAP role. A condition limits when the grant applies. For example, `destination.port == 22` limits the grant to port 22.

### 3. Connect with gcloud or the console

Run `gcloud compute ssh INSTANCE_NAME --zone=ZONE`.

| Situation | What gcloud does |
|---|---|
| The VM has no external IP address | Uses IAP TCP tunneling automatically. |
| The VM has an external IP address | Uses the external IP address, not IAP. |
| You add `--tunnel-through-iap` | Always uses IAP TCP tunneling. |
| You add `--internal-ip` | Never uses IAP. It connects directly to the internal IP of the VM. |

You can also use the SSH button in the Google Cloud console. For other TCP-based protocols, use `gcloud compute start-iap-tunnel`, which opens a local port and sends the traffic to the VM's port in an HTTPS stream.

### Limits of IAP TCP forwarding

- It is not meant for bulk transfer of data, and IAP can rate-limit users who abuse it.
- IAP disconnects sessions after one hour of inactivity. `gcloud compute start-iap-tunnel` tries to reconnect a tunnel that drops.

## Common mistakes

- **Expecting metadata-based SSH keys to still work.** Instances that use OS Login cannot use SSH keys stored in project or instance metadata. A local user account with an `authorized_keys` file is the exception.
- **Granting a login role and forgetting the service account.** A user who logs in can use all the IAM permissions of the service account attached to the VM.
- **Granting `roles/compute.osAdminLogin` when the person does not need administrator access.** The two roles differ by administrator access (`sudo`).
- **Granting an OS Login role only at the instance for a user who needs the console or gcloud.** Grant the roles at the project level for SSH from the console or the Google Cloud CLI.
- **Granting login and tunnel roles but not Service Account User.** If the VM has a service account, all users need `roles/iam.serviceAccountUser`, granted on the service account.
- **Granting a login role and forgetting the tunnel role.** On a VM with no external IP address, the person also needs `roles/iap.tunnelResourceAccessor`.
- **Leaving `default-allow-ssh` and `default-allow-rdp` in place** and then thinking SSH is only possible through IAP. Those rules allow SSH and RDP from all IP addresses.
- **Using only the IPv4 range for an IPv6 VM.** IPv6 VMs use `2600:2d00:1:7::/64`.
- **Using the tunnel to copy large files.** IAP TCP forwarding is not for bulk data transfer.
- **Forgetting `roles/compute.osLoginExternalUser` for users from a different organization than the VM.** Grant it on the organization; an organization administrator must do it.

## How to check this in your own project

1. Confirm OS Login is on: `enable-oslogin` is set to `TRUE` in instance metadata (the VM) or project metadata.
2. For each engineer or group, confirm that you granted `roles/compute.osLogin` or `roles/compute.osAdminLogin` (on the project or instance; on the project if they use the console or gcloud), `roles/iap.tunnelResourceAccessor` on the project or the VM, and, if the VM has a service account, `roles/iam.serviceAccountUser` on that service account.
3. Find the firewall rule (see [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/) for where rules are kept). Confirm that a rule allows ingress on `tcp:22` (and `tcp:3389` for RDP, if you use it) from `35.235.240.0/20`. Check whether `default-allow-ssh` and `default-allow-rdp` still exist.
4. As an engineer with `roles/compute.osLogin` and `roles/iap.tunnelResourceAccessor` (plus `roles/iam.serviceAccountUser` if the VM has a service account), run `gcloud compute ssh INSTANCE_NAME --zone=ZONE --tunnel-through-iap`. Check that login works. On the VM, try a command with `sudo`. If the role does what its description says, you do not get administrator access.
5. Repeat with a person who has `roles/compute.osAdminLogin`, `roles/iap.tunnelResourceAccessor` and, if needed, `roles/iam.serviceAccountUser`. On the VM, `sudo` is expected to work (administrator access).
6. On the VM, run `whoami`. The username is expected to follow the `USERNAME_DOMAIN_SUFFIX` format, or start with `ext_` for a user from a different organization than the VM.
7. Remove a role and try again. Google checks permissions for every login attempt, so the login should fail.
8. Review the service account attached to each VM. Everyone who can log in can use its permissions.

Next: [Seeing What VMs Do: Ops Agent and Audit Logs](/google-cloud/vm-logging-and-monitoring/).

## Sources

- [About OS Login](https://docs.cloud.google.com/compute/docs/oslogin)
- [Set up OS Login](https://docs.cloud.google.com/compute/docs/oslogin/set-up-oslogin)
- [Use IAP for TCP forwarding](https://docs.cloud.google.com/iap/docs/using-tcp-forwarding)
