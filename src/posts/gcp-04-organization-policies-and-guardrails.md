---
title: "Google Cloud Guardrails: Organization Policies and Security Decisions"
seoTitle: "Google Cloud Organization Policies and Guardrails"
layout: post.njk
permalink: /google-cloud/organization-policies-and-guardrails/
order: 404
part: 4
tags: gcp-lz
deck: "Explain what an organization policy constraint does, name the ones that matter for VMs and service accounts, and describe the seven security decisions for a landing zone."
---

Identity and Access Management (IAM) focuses on who. Organization policy focuses on what: it sets restrictions on specific resources to determine how they can be configured. In this article, a guardrail is such a restriction, set once and applied below it.

This article is for people who set up or review a Google Cloud foundation. You will learn what an organization policy and a constraint are (both are defined in the Key terms below), how a policy reaches folders and projects, which constraints matter for virtual machines (VMs) and service accounts (machine identities that you use to grant IAM roles to workloads), and the seven security decisions that a landing zone has to make.

It helps to know the resource hierarchy first: the organization is the top, folders sit below it, and projects sit in folders. See [Organization, Folders and Projects](/google-cloud/organization-folders-and-projects/). Firewall rules, another kind of network control, are in [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/).

## Key terms

| Term | Meaning |
|---|---|
| Organization Policy Service | The Google Cloud service that gives you centralized and programmatic control over your organization's Google Cloud resources. |
| Organization policy | A policy that configures a single constraint that restricts one or more Google Cloud services. It is set on an organization, a folder or a project. |
| Constraint | A particular type of restriction against a Google Cloud service or a list of Google Cloud services. |
| Legacy managed constraint | A legacy kind of constraint that managed constraints are designed to replace. A legacy managed constraint has a constraint type of list or boolean (boolean and list are defined two rows below). |
| Managed constraint | A constraint that Google manages. Managed constraints are designed to replace equivalent legacy managed constraints. |
| Boolean rule and list rule | A boolean rule can allow all values, deny all values, or set a constraint to enforced or not enforced. A list rule is a collection of allowed or denied values. |
| Enforced | A legacy managed constraint with a boolean rule is either enforced or not enforced. If the equivalent legacy managed constraint is boolean, the managed constraint can be enforced or not in the same way. For example, when `iam.managed.disableServiceAccountKeyCreation` is enforced, it blocks service account key creation. |
| Inheritance | All descendants of the resource that has the policy inherit it by default. Descendants include the folders, projects and service resources below it. |
| Active mode and dry-run mode | An organization policy enforces its constraint in active mode, in dry-run mode, or both. In dry-run mode, violations of the policy are audit-logged, but the violating actions are not denied. |
| Tag | Tags provide a way to conditionally enforce constraints based on whether a resource has a specific tag. |
| Google Cloud security baseline | Constraints that are enforced when the organization resource is first created. |
| Service account | Machine identities that you use to grant IAM roles to workloads. |
| Service account key | A persistent credential for a service account. |
| VPC Service Controls | A solution that defines a perimeter around sensitive resources that helps to restrict access from outside the perimeter. |
| Cloud Interconnect | A service that sets up a direct physical connection between Google Cloud and your data centers. |
| HA VPN | A way to connect private traffic between Google Cloud and your data centers. Its traffic is encrypted by default. |
| Log sink and audit logs | A centralized log sink collects audit logs from all projects. Most audit logs are stored in the Google Cloud project that produced them. |
| Security Command Center | A service that monitors the environment for insecure configurations and threats. |
| Cloud KMS and CMEK | Cloud Key Management Service (Cloud KMS) offers the ability to protect your data using customer-managed encryption keys (CMEK). |
| Access Transparency | Logs that record the actions taken by Google Cloud personnel in your environment. |

## What an organization policy does

IAM and organization policy answer different questions. IAM lets an administrator authorize who can take action on specific resources, based on permissions. Organization policy lets the administrator set restrictions on specific resources to determine how they can be configured. For example, when `compute.managed.vmExternalIpAccess` is enforced, it denies the creation or update of VM instances with IPv4 external IP addresses.

Each organization policy configures one constraint. You set it on the organization, a folder or a project. A policy can enforce its constraint in active mode, in dry-run mode, or both.

Many constraints have a default, and the table below lists it wherever one exists. For example, by default all VM instances are allowed to use external IP addresses.

## How a policy reaches folders and projects

All descendants of a resource inherit its organization policy by default. A policy on the organization therefore reaches every folder and project below it. This is why the folder design in [Organization, Folders and Projects](/google-cloud/organization-folders-and-projects/) matters: you set a rule once at the right level.

A folder or project can also set its own policy. That policy either overwrites the inheritance or inherits the parent's policy. What happens next depends on the kind of constraint:

- **Managed constraints:** policies inherited from a parent are not merged. The resource enforces the constraint as it was set on the parent resource, or overrides it with its own policy.
- **Legacy managed constraints:** policies are merged based on the rules of hierarchy evaluation.

So a policy set lower down can overwrite the inherited one, or, for legacy managed constraints, can be merged with it under the hierarchy-evaluation rules. Check the kind before predicting the result.

Two more facts help when you plan a rollout.

- The application of a new organization policy is usually not retroactive. Plan for resources that already exist.
- Tags provide a way to conditionally enforce constraints based on whether a resource has a specific tag.

## Constraints that matter for VMs and service accounts

This table is a selection of constraints. It is not a list of the constraints that any blueprint sets. The names are written without the `constraints/` prefix. Shared VPC is covered in [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/).

The Kind column shows whether a constraint is a managed constraint or a legacy managed constraint. Managed constraints are designed to replace equivalent legacy managed constraints. Each legacy managed constraint has a constraint type of list or boolean.

| Constraint | Kind | Description and default |
|---|---|---|
| `compute.managed.requireOsLogin` | Managed | When enforced, requires OS Login (sign-in to VMs controlled by IAM roles; see [Reaching a VM: OS Login, IAM Roles and IAP](/google-cloud/reaching-a-vm-os-login-and-iap/)) on all newly created projects. On new and existing projects, it prevents metadata updates that disable OS Login. |
| `compute.managed.vmExternalIpAccess` | Managed | Defines whether Compute Engine VM instances are allowed to use IPv4 external IP addresses. By default, all VM instances are allowed to use external IP addresses. If enforced, it denies the creation or update of VM instances with IPv4 external IP addresses. It does not restrict IPv6 external IP addresses. |
| `compute.managed.disableSerialPortAccess` | Managed | Prevents the `serial-port-enable` metadata key from being set to true for Compute Engine VMs. By default, serial port access can be enabled on a per-VM, per-zone, or per-project basis using this metadata key. Enforcing it does not affect existing VMs where `serial-port-enable` is already set to true. |
| `compute.managed.vmCanIpForward` | Managed | Defines whether Compute Engine VM instances can enable IP forwarding. By default, if no policy is specified, any VM can enable IP forwarding in any virtual network. If enforced, it denies the creation or update of VM instances with IP forwarding enabled. |
| `compute.requireShieldedVm` | Legacy managed | Boolean rule. When enforced, requires that all new Compute Engine VM instances use the Shielded VM options (hardened VM settings). Shielded VM features add verifiable integrity and exfiltration resistance to your VMs. By default, Shielded VM features do not need to be enabled. |
| `compute.skipDefaultNetworkCreation` | Legacy managed | Boolean rule. Skips the creation of the default network and related resources when a project is created. By default, a default network and supporting resources are created. |
| `compute.restrictSharedVpcHostProjects` | Legacy managed | A list rule for the set of Shared VPC host projects that projects at or below this resource can attach to. By default, a project can attach to any host project in the same organization. |
| `compute.restrictSharedVpcSubnetworks` | Legacy managed | A list rule for the set of Shared VPC subnetworks that eligible resources can use. By default, they can use any Shared VPC subnetwork. |
| `gcp.resourceLocations` | Legacy managed | A list rule for the locations where location-based Google Cloud resources can be created. By default, resources can be created in any location. |
| `iam.managed.disableServiceAccountKeyCreation` | Managed | When enforced, blocks service account key creation. |
| `iam.disableServiceAccountKeyCreation` | Legacy managed | Boolean rule. When enforced, disables the creation of service account external keys and Cloud Storage HMAC keys. By default, external keys can be created based on IAM roles and permissions. |
| `iam.automaticIamGrantsForDefaultServiceAccounts` | Legacy managed | Boolean rule. When enforced, stops the default App Engine and Compute Engine service accounts from being granted an IAM role automatically. By default, these service accounts automatically receive the Editor role when they are created. Roles are explained in [Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). The Editor role is a broad role that can change most resources. |

There is a managed constraint and a legacy managed constraint for service account key creation. The legacy constraint, `constraints/iam.disableServiceAccountKeyCreation`, is the one that the first security decision below uses.

`iam.disableServiceAccountKeyCreation` and `iam.automaticIamGrantsForDefaultServiceAccounts` are automatically provisioned as part of the Google Cloud security baseline. Baseline constraints are enforced when the organization resource is first created, so some of these constraints may already be set. Ask the team that runs your organization.

## The seven security decisions

Each decision has a recommended option and alternatives. The guidance is for security specialists, CISOs (chief information security officers) and architects, and it assumes a central security or platform team enforces the controls. It focuses on enterprise-scale environments, so some strategies might be less relevant for small teams.

Option 1 is the recommended option for most use cases in all seven decisions.

| Decision | Option 1 (recommended) | Other options and when to avoid |
|---|---|---|
| 1. Limit persistent credentials for service accounts | Restrict service account keys with an organization policy constraint, so users cannot create or download them. Design a process for teams to request an exception when downloading a key is the only viable option. This constraint is part of the Google Cloud security baseline; see the note above. | Option 2: generate short-lived credentials with custom tooling or a third-party tool. Avoid option 1 when you already have tooling that generates short-lived API credentials. |
| 2. Mitigate data exfiltration through Google APIs (data exfiltrated by malicious insiders or compromised code, or exposed through a misconfigured IAM policy) | Configure VPC Service Controls broadly, with perimeters that restrict all supported APIs and exceptions for developer access. Avoid when your workloads need unrestricted internet access or use services that VPC Service Controls does not support. VPC Service Controls introduces complexity to your access model, so design it for your environment. | Option 2: configure it only for a subset of projects, such as those with sensitive data. Avoid when many projects could hold sensitive data. Option 3: do not configure it. Avoid when you have sensitive data in your Google Cloud environment. |
| 3. Monitor for insecure configurations and threats | Use Security Command Center, activated at the organization level. Avoid when your existing security tools can already do all three of these: fully address ephemeral or serverless cloud resources, monitor your cloud resources for insecure configurations, and identify threats at scale. | Option 2: use your existing security tools, alone or alongside Security Command Center. Avoid when your existing security operations center (SOC) does not have the skills or capacity to generate threat insights from the volume of cloud logs. Also avoid it because integrating multiple third-party tools with multiple Google Cloud services introduces more complexity than value. |
| 4. Collect logs in one place | Keep logs in Google Cloud with a centralized organization-wide log sink for audit logs. | Option 2: ingest audit logs directly into Google Security Operations (Google SecOps) if you use it as your security information and event management (SIEM) system, which you might combine with option 1. Option 3: export audit logs outside Google Cloud. Exporting can potentially be very expensive, so be selective about which logs you export. |
| 5. Encryption at rest | Accept Google Cloud default encryption at rest. Avoid when compliance requires you to manage your own keys. | Option 2: manage keys with Cloud KMS using CMEK. Customer-supplied encryption keys (CSEK) are not recommended. Option 3: tokenize data (replace sensitive values with placeholders) in the application before it is stored. This is not a control you can centrally enforce in the landing zone, and it adds cost, latency and complexity. |
| 6. Encryption in transit | Evaluate whether Google Cloud default encryption in transit is sufficient. | Option 2: add encryption for application traffic. It is not a control you can enforce centrally. Option 3: add encryption for on-premises connections. Traffic from your on-premises environment to Google Cloud over Cloud Interconnect is not encrypted in transit by default, so enable MACsec for Cloud Interconnect as part of your landing zone. MACsec encrypts the link between your network and Google. HA VPN traffic is encrypted by default. |
| 7. Cloud provider access | Enable Access Transparency logs. | Option 2: add Access Approval, a manual solution that requires your explicit approval before Customer Care and Google engineering access your content, and Key Access Justifications, which lets you set a policy on Cloud KMS keys to view, approve and deny key access requests. Avoid when approval delays would be unacceptable for high-availability workloads. |

## How the pieces fit

The diagram combines the example security architecture and the log aggregation example with how an organization policy is inherited. A centralized log sink collects audit logs from all projects.

![Folders and projects inherit an organization policy. A perimeter surrounds sensitive resources, with exceptions for developer access. Two log sinks send audit logs to an Observability Analytics bucket and a Cloud Storage bucket. Security Command Center is activated at the organization level. Default encryption and Access Transparency logs are drawn inside the organization like the other controls.](/img/google-cloud/google-cloud-organization-policies-and-guardrails.svg)

*Sources: [Decide the security for your Google Cloud landing zone](https://docs.cloud.google.com/architecture/landing-zones/decide-security); [Introduction to the Organization Policy Service](https://docs.cloud.google.com/organization-policy/overview); [Organization policy constraints](https://docs.cloud.google.com/organization-policy/reference/org-policy-constraints).*

For log aggregation, one example is an Observability Analytics bucket (a log storage bucket that you can query) in a central project for administrator activity logs, and a Cloud Storage bucket for long-term retention of data access audit logs from projects with sensitive workloads. For what a VM itself writes to logs, see [Seeing What VMs Do](/google-cloud/vm-logging-and-monitoring/).

## Common mistakes

- **Setting a rule only on one project.** A policy on the organization or a folder reaches everything below it. A policy on one project applies to that project and its children.
- **Expecting a new policy to fix old resources.** The application of new organization policies is usually not retroactive.
- **Mixing up IAM and organization policy.** A role gives permission. A constraint limits what can be configured.
- **Assuming a folder policy combines with its parent for every constraint.** Managed constraints are not merged. Legacy managed constraints are merged under the rules of hierarchy evaluation.
- **Using a constraint name from memory.** Copy the exact name from the [reference](https://docs.cloud.google.com/organization-policy/reference/org-policy-constraints).
- **Turning on VPC Service Controls without an exception path.** It introduces complexity to your access model. Configure exceptions to the perimeter for developer access.
- **Blocking service account keys without an exception process.** Design a process for teams to request an exception when downloading a key is the only viable option.
- **Exporting every log outside Google Cloud.** Exporting can potentially be very expensive, so be selective about which logs you export.

## How to check this in your own project

You need access to a Google Cloud organization, or someone who runs it and can answer the questions below.

1. Open the [Organization policy constraints reference](https://docs.cloud.google.com/organization-policy/reference/org-policy-constraints) and find each constraint in the table above by its exact name. Read its kind, description and default.
2. For each constraint, write down your own choice: enforced at the organization, enforced at a folder, or not used. Write the reason next to it.
3. Ask the team that runs your organization which of these constraints are already set, and at which level. If your organization is new, some constraints may be part of the Google Cloud security baseline and already enforced.
4. Write one line for each of the seven decisions: the option you chose and who owns it.
5. For any decision where you chose an option other than option 1, write down the reason, using the "when to avoid" wording in the table where the table gives one.
6. Dry-run mode lets you monitor how a policy change would affect your workflows before it is enforced. Violations are audit-logged but not denied.

This article does not cover the steps for creating or testing organization policies.

## Sources

- [Decide the security for your Google Cloud landing zone](https://docs.cloud.google.com/architecture/landing-zones/decide-security)
- [Organization policy constraints](https://docs.cloud.google.com/organization-policy/reference/org-policy-constraints)
- [Introduction to the Organization Policy Service](https://docs.cloud.google.com/organization-policy/overview)
