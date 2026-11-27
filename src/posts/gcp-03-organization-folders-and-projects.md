---
title: "Google Cloud Organization, Folders and Projects"
layout: post.njk
permalink: /google-cloud/organization-folders-and-projects/
order: 403
part: 3
tags: gcp-lz
deck: "Draw your resource hierarchy, pick one of three designs with a two-question decision flow, and say what each folder and project in the enterprise foundations blueprint is for."
---

Every resource in Google Cloud sits inside a hierarchy. Policies and access are inherited down that hierarchy, so the shape you choose decides who can do what, and where. This article is for cloud administrators, architects and engineers who set up a Google Cloud foundation. After reading it you can draw a hierarchy, choose a design with a two-question decision flow, and explain the folders and projects in the enterprise foundations blueprint (defined in [What Is a Google Cloud Landing Zone](/google-cloud/what-is-a-google-cloud-landing-zone/)).

Terms such as landing zone, billing account, on-premises and Cloud Interconnect are explained in [What Is a Google Cloud Landing Zone](/google-cloud/what-is-a-google-cloud-landing-zone/). Accounts, roles and allow policies are explained in [Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). Organization policies are covered in [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/); this article only shows that they are inherited.

## Key terms

| Term | Meaning |
|---|---|
| Resource hierarchy | The parent-child structure of organizations, folders and projects. Every resource except the top one has exactly one parent. |
| Organization resource | The root node of the hierarchy. It represents an entity such as a company and is the parent of all folders and projects. |
| Folder | An optional grouping layer between the organization and projects. A folder can contain projects and other folders. |
| Project | The fundamental organizing entity. It contains the actual service resources, such as Compute Engine virtual machines and storage buckets. You need a project to use Google Cloud. |
| Project ID | A name you choose when you create the project. It is not the same as the display name. |
| Project number | A number Google Cloud assigns when you create the project. It is read-only. |
| Display name | The name of a project that appears in the user interface. It can be changed. It is not the same as the project ID. |
| Enterprise foundations blueprint | The Google Cloud blueprint whose example hierarchy this article describes. This article calls it "the blueprint". It is defined in [What Is a Google Cloud Landing Zone](/google-cloud/what-is-a-google-cloud-landing-zone/). |
| IAM | Identity and Access Management. See [Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). |
| Workload project | A project in which you create resources for applications. |
| Inheritance | Allow, deny and organization policies are inherited through the hierarchy. The effective policy for a resource results from the policies applied directly to it and the policies inherited from its ancestors. Organization policies can be superseded by policies defined at a lower level. Allow policies at lower levels are additive. How a lower-level organization policy combines with the inherited one depends on the kind of constraint; see [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/). |
| Allow policy | See [Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). Allow policies are inherited by descendants. |
| Deny policy | A policy that lets you restrict permissions at the project, folder and organization level. Deny policies are inherited through the hierarchy and are applied before allow policies. |
| Organization policy | You use organization policy constraints to set guidelines around the whole organization or significant parts of it and still allow for exceptions. Organization policies are inherited through the hierarchy. See [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/). |
| Role | See [Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). |
| Managed users | Members of the account domain. |
| Label | A project has a collection of labels that can be used for filtering projects. The blueprint uses them to record who owns a project and what it is for. |
| Bootstrap folder | The folder for the projects used to deploy the foundation components. |
| Common folder | The folder for projects whose resources are shared by all environments. |
| Host project | The project that hosts a Shared VPC network. The blueprint keeps host projects in its networking folder. See [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/). |

## The three levels

![An organization (example.com) at the top, with six folders below it: bootstrap, common, networking, production, nonproduction and development. An arrow runs from each folder to the projects it contains.](/img/google-cloud/google-cloud-organization-folders-projects.svg)

*Source: [Enterprise foundations blueprint: Organization structure](https://docs.cloud.google.com/architecture/blueprints/security-foundations/organization-structure).*

The hierarchy has three kinds of node. The organization is at the top. Folders are in the middle, and they are optional. Projects hold the service resources. In the figure, the organization is at the top and the six folders of the blueprint example are grouped below it. Each arrow from a folder to its projects means "contains". Folders can also contain other folders. The blueprint's example organization uses the domain example.com.

### Organization

An organization resource is not strictly required for all Google Cloud users, but folders need one, and some features of the resource hierarchy depend on it. Getting one works in three steps.

1. **What you need.** A Google Workspace or Cloud Identity account (see [Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/)). One such account can be associated with exactly one organization resource.
2. **What happens.** When a user of such an account creates a project, an organization resource is automatically provisioned for them.
3. **What it means.** Managed users, who are members of the account domain, must create projects within an organization.

The organization has an organization resource ID and a display name. The display name is generated from the primary domain name in Google Workspace or Cloud Identity.

A new organization starts with an initial allow policy that grants the Project Creator and Billing Account Creator roles to the entire domain. In plain terms, until you change that policy, everyone in the domain can create projects and billing accounts.

### Folders

Folders let you delegate administration rights. They work like sub-organizations inside the organization. IAM roles granted on a folder are inherited by all projects and folders in that folder. Because a folder can contain projects and other folders, each folder can include subfolders.

### Projects

A project sits under the organization or under a folder. A project can be at the top of its hierarchy only if a free trial or free tier user created it. A project has a project ID, a project number and a display name (see the key terms). The initial IAM policy of a new project grants the owner role to the person who created it.

## How the hierarchy affects other controls

| What you set | What happens below it |
|---|---|
| IAM roles on a folder | Inherited by all projects and folders in that folder. |
| Allow policies | Inherited by descendants. Allow policies at lower levels are additive. |
| Deny policies | Inherited through the hierarchy. Allow policies can be superseded by deny policies, which are applied before allow policies. |
| Organization policies | Inherited by descendants, but can be superseded by policies defined at a lower level. See [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/) for how the result depends on the kind of constraint. |
| Hierarchical firewall policies | Let you implement consistent firewall policies throughout the organization or in specific folders. Inheritance is implicit, which means that you can allow or deny traffic at any level or you can delegate the decision to a lower level. See [Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/). |
| Log aggregation | Cloud Logging includes aggregated sinks that you can use to aggregate logs at the folder or organization level (see [VM Logging and Monitoring](/google-cloud/vm-logging-and-monitoring/)). |
| Billing | Billing is not directly linked to the resource hierarchy, but assigned at the project level. To get aggregated information at the folder level, you can analyze your costs by project hierarchy using billing reports. |

Allow, deny and organization policies are inherited through the hierarchy, so a policy set on a folder applies to what is below it. What allow policies do is covered in [Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/). How a lower-level organization policy combines with an inherited one depends on the kind of constraint, and is covered in [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/).

## Choose a design

A hierarchy should match how your organization wants to work in the cloud. No single design fits every organization. Do not map your corporate structure straight onto the hierarchy. Start from three questions instead: who is responsible for cloud resources, what are your compliance needs, and do you expect events such as mergers, acquisitions or spin-offs.

### The three designs

| Design | Use it when |
|---|---|
| Option 1: application environments (for example development and QA, testing and production) | You have separate application environments with different policy and administration requirements. You have centralized security or audit requirements that a central security team must be able to enforce consistently on all production workloads and data. You need different IAM roles to access your resources in different environments. |
| Option 2: regions or subsidiaries (folders for each subsidiary or region) | Different regions or subsidiaries operate independently. They have different operational backbones, digital platform offerings and processes. Your business has different regulatory and compliance standards for regions or subsidiaries. |
| Option 3: accountability framework (folders for product modules and product teams) | You have clear ownership and accountability for each product. Your workloads are independent and do not share many common policies. Your processes and external developer platforms are offered as service or product offerings. |

Option 1 is not a good fit when you do not run multiple application environments, when you do not have varying application dependencies and business processes across environments, or when you have strong policy differences for different regions, teams or applications. Options 2 and 3 have no "not a good fit" list; use the conditions above.

What the folders look like in Options 2 and 3:

- **Option 2.** First level: Subsidiary 1, Subsidiary 2, Holding group and Bootstrap. Inside Holding group: APAC, EMEA, Americas and Shared infrastructure. Projects sit inside each folder.
- **Option 3.** First level: Ecommerce Modules, Logistics and Warehousing Modules, Reconciliation and Billing, and Bootstrap. Projects sit inside each folder.

### The decision flow

1. Do different subsidiaries, regional groups or business units have very different policy requirements? If yes, use Option 2. If no, go to question 2.
2. Do your workload or product teams require strong autonomy over their policies? For example, you do not have a central security team that determines policies for all workload or product teams. If yes, use Option 3. If no, use Option 1.

Most organizations choose a hybrid approach and select different designs at different levels of the hierarchy. Start with the design that has the biggest effect on policies and access.

## Three best practices

- **Use one organization node when you can.** This avoids management overhead. More than one makes sense to test major changes to your IAM levels or hierarchy, to experiment in a sandbox without the same organization policies, or when sub-companies are likely to be sold off or run separately.
- **Use one naming convention across the organization.** The enterprise foundations blueprint includes a sample convention you can adapt.
- **Keep bootstrapping and common services separate.**
  - Put the bootstrap folder right below the organization node.
  - Put the common-services folder right below the organization node when your top level is application environments, teams or applications are in the second layer, and shared services such as monitoring are common between environments.
  - Put the common-services folder lower, below the application folders, when services are shared between applications but you deploy a separate instance for each deployment environment.

## The blueprint's folders and projects

This is the structure the blueprint uses as its example. It has six folders.

| Folder | What it contains |
|---|---|
| `bootstrap` | The projects used to deploy foundation components. |
| `common` | Projects with resources shared by all environments. |
| `networking` | The networking resources shared by all environments. |
| `production` | Projects with production resources. |
| `nonproduction` | A copy of the production environment, so you can test workloads before you promote them to production. |
| `development` | The cloud resources used for development. |

The project names follow the folders. In the names below, `prj-b-` projects are in the bootstrap folder, `prj-c-` projects are in the common folder and `prj-net-` projects are in the networking folder. `{env}` stands for one of the environments: development (`d`), non-production (`n`) or production (`p`). Note that the folder is called `nonproduction` and the `environment` label value is `non-production`.

| Project | Folder | Purpose |
|---|---|---|
| `prj-b-cicd` | bootstrap | The deployment pipeline that builds the foundation components of the organization. |
| `prj-b-seed` | bootstrap | The Terraform state of your infrastructure and the Terraform service account that is required to run the pipeline. Terraform is an example of describing infrastructure as code; see [What Is a Google Cloud Landing Zone](/google-cloud/what-is-a-google-cloud-landing-zone/). |
| `prj-c-secrets` | common | The project that holds the blueprint's organization-level secrets. |
| `prj-c-logging` | common | The aggregated log sources for audit logs. |
| `prj-c-scc` | common | Resources to help configure Security Command Center alerting and other custom security monitoring. Security Command Center is described in [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/). |
| `prj-c-billing-export` | common | A BigQuery dataset with the organization's billing exports. |
| `prj-c-infra-pipeline` | common | An infrastructure pipeline for deploying resources such as virtual machines (VMs) and databases to be used by workloads. |
| `prj-c-kms` | common | Encryption keys for encrypting shared services within the common folder. |
| `prj-net-{env}-svpc` | networking | The host project for a Shared VPC network. |
| `prj-net-hub` | networking | The Shared VPC network used as a hub between the on-premises environment and Google Cloud spokes. This project is created in the hub-and-spoke topology only. Hub-and-spoke and other network designs are covered in [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/). |
| `prj-net-interconnect` | networking | The Cloud Interconnect connections that provide connectivity between your on-premises environment and Google Cloud. |
| `prj-{env}-{workload_name_or_id}` | each environment folder | Various workload projects in which you create resources for applications. |
| `prj-{env}-secrets` | each environment folder | The project that holds the blueprint's folder-level secrets. |
| `prj-{env}-kms` | each environment folder | Encryption keys for encrypting services within each environment folder. |

### Governance labels

The blueprint includes these labels for projects to record ownership and purpose.

| Label | Meaning |
|---|---|
| `application` | The human-readable name of the application or workload that is associated with the project. |
| `businesscode` | A short code that describes which business unit owns the project. `shared` marks common projects not tied to a business unit. |
| `billingcode` | A code that is used to provide chargeback information. |
| `primarycontact` | The username of the primary contact that is responsible for the project, without the domain suffix. |
| `secondarycontact` | The username of the secondary contact that is responsible for the project, without the domain suffix. |
| `environment` | The environment type, such as `bootstrap`, `common`, `production`, `non-production`, `development` or `network`. |
| `envcode` | A value that identifies the type of environment, shortened to `b`, `c`, `p`, `n`, `d` or `net`. |
| `vpc` | The ID of the network (a VPC network) that this project is expected to use. See [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/). |

## Common mistakes

- Copying the corporate org chart into folders instead of starting from responsibility, compliance and upcoming business events.
- Picking one design for every level instead of a hybrid when your needs differ by level.
- Creating several organization nodes without a reason such as testing IAM or hierarchy changes, experimenting in a sandbox, or sub-companies that are likely to be sold off.
- Treating the display name and the project ID as the same thing. The display name is the name shown in the interface and can be changed.
- Putting the bootstrap folder deep in the hierarchy instead of right below the organization.
- Copying the six blueprint folders as if they were required. They are one example design.

## How to check this in your own project

These steps are a planning exercise. They do not change anything in Google Cloud.

1. Write down who is responsible for cloud resources, your compliance needs and any planned mergers, acquisitions or spin-offs.
2. Answer the two decision-flow questions. Note the design they point to.
3. Check whether a hybrid fits better: a different design at a different level.
4. Sketch the hierarchy on paper: organization, folders, projects. Mark where bootstrap and common services go.
5. For each folder, list the roles and policies that should be inherited below it. For example, a group that should be able to view every project in the common folder gets that role on the common folder.
6. Compare your sketch with the blueprint's six folders and its project list. Note what you would keep or change.
7. Pick a naming convention and the labels you will put on every project.

## Sources

- [Decide a resource hierarchy for your Google Cloud landing zone](https://docs.cloud.google.com/architecture/landing-zones/decide-resource-hierarchy)
- [About resource hierarchy](https://docs.cloud.google.com/resource-manager/docs/overview)
- [Enterprise foundations blueprint: Organization structure](https://docs.cloud.google.com/architecture/blueprints/security-foundations/organization-structure)
