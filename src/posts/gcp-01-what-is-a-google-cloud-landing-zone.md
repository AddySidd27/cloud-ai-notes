---
title: "What a Google Cloud Landing Zone Is and What Goes in It"
layout: post.njk
permalink: /google-cloud/what-is-a-google-cloud-landing-zone/
order: 401
part: 1
tags: gcp-lz
deck: "Explain what a Google Cloud landing zone is, name its four core elements, and say what to put in place before the first application."
---

Before a company runs real applications on Google Cloud, it needs a base to run them on: who can sign in, how resources are organized, how the network is laid out, and what rules protect it all. This base is called a landing zone. This article is for architects, engineers and managers who are new to Google Cloud. After reading it you can say what a landing zone is, name its four core elements, and say what must exist before the first application.

This article gives the overview only. Each core element has its own article later in the series, for example [identities, groups and roles](/google-cloud/identities-groups-and-roles/) and [organization, folders and projects](/google-cloud/organization-folders-and-projects/).

## Key terms

You do not need to memorize these. Terms from the four core elements are explained in the sections that follow the diagram.

| Term | Meaning |
|---|---|
| Landing zone | A modular and scalable configuration that lets an organization adopt Google Cloud. It is also called a cloud foundation. It is not a zone or a zonal resource, so it has nothing to do with a Google Cloud zone. |
| Infrastructure as Code (IaC) | IaC helps you make your deployment repeatable and modular. Terraform is an example. |
| Cloud Identity | A Cloud Identity account synchronizes with an on-premises identity provider and with IAM. |
| Enterprise foundations blueprint | The best practices that let you deploy a foundational set of resources in Google Cloud. It was formerly known as the security foundations blueprint. This article calls it "the blueprint". |
| Organization resource | The root node for managing resources in Google Cloud. You must create it before you deploy a landing zone. |
| Billing account | You must create one, either online or invoiced, before you deploy a landing zone. |
| Resource hierarchy | It consists of folders, projects and resources, under the organization. |
| IAM | Identity and Access Management. It provides granular access to Google Cloud resources. |
| Allow policy | Allow policies (formerly known as IAM policies) allow access to resources. All access permissions are denied by default until you apply allow policies directly to a resource, or the resource inherits them from a higher level. |
| Folder | In the blueprint, folders group projects based on their environment. |
| Project | In the blueprint, projects group individual resources based on their functionality and intended boundaries for access control. |
| Shared VPC | In the example landing zone, a Shared VPC network for each environment (production, development and testing) connects resources from multiple projects to the VPC network. |
| Organization policy | Organization policy constraints are configured to prevent various high-risk configurations. |

## What a landing zone is

A landing zone is a modular and scalable configuration that lets an organization adopt Google Cloud for its business needs. Another name for it is a cloud foundation. The word "zone" here has nothing to do with a Google Cloud zone: a landing zone is not a zone or a zonal resource.

A landing zone helps an enterprise deploy, use and scale Google Cloud more securely. It gives you:

- A foundation that is designed to be secure.
- The network for enterprise applications.
- The tools to govern how costs are distributed inside the company.

Because a landing zone is modular, the first version is often not the final one. Design it to grow as your use of Google Cloud grows. Some organizations might need more than one landing zone, for example for applications with their own scalability or compliance needs. Identities, billing and the organization resource can be shared between them.

Build the landing zone before you deploy your first enterprise application on Google Cloud. There is no single or standard implementation of a landing zone, so the design you build depends on your business needs.

## The four core elements

The diagram shows an example. The elements in it come from the example landing zone design, except Security Command Center and the folder, project and inheritance details, which come from the blueprint. The terms in the diagram are explained in the four sections below it. Your own design depends on your business context. The arrow from the identity provider shows synchronization. The arrows between organization, folders and projects show how the hierarchy nests. The other arrows show what comes before and after the landing zone. No arrow shows the order in which you build the four elements.

![Diagram of an example Google Cloud landing zone. An existing identity provider synchronizes with Cloud Identity. Before you start, create an organization resource and a billing account. The landing zone has four core elements: identity provisioning, resource hierarchy, network and security controls. A dashed band lists additional elements. The first application comes after the landing zone.](/img/google-cloud/google-cloud-landing-zone-elements.svg)

*Source: [Landing zone design in Google Cloud](https://docs.cloud.google.com/architecture/landing-zones), [Enterprise foundations blueprint](https://docs.cloud.google.com/architecture/security-foundations) and [Organization structure](https://docs.cloud.google.com/architecture/security-foundations/organization-structure).*

### Identity provisioning

In the blueprint, users and group membership are synchronized from your existing identity provider. In the example landing zone, a Cloud Identity account synchronizes with an on-premises identity provider and with IAM. IAM provides granular access to Google Cloud resources. In the blueprint, allow policies are applied to groups based on job function. All access is denied by default until an allow policy is applied directly to a resource or inherited from a higher level.

### Resource hierarchy

The root node for managing resources is the organization. Below it are folders and projects. In the blueprint, folders group projects by environment (for example production or development), and projects group individual resources based on their functionality and intended boundaries for access control. Resources lower in the hierarchy inherit policies such as IAM allow policies and organization policies.

### Network

The example landing zone uses a Shared VPC network for each environment (production, development and testing). A Shared VPC network connects resources from multiple projects to the VPC network. Multiple service projects are configured to use the Shared VPC networks. These service projects host your application resources. VPC firewall rules control connectivity to and from workloads in the Shared VPC networks. A Cloud NAT gateway allows outbound connections to the internet from resources in these networks. Cloud Interconnect connects on-premises applications and users. A Cloud DNS private zone hosts DNS records for your deployments in Google Cloud. In the blueprint, no outbound traffic to or inbound traffic from the public internet is permitted by default. The network has its own article: [network design with Shared VPC](/google-cloud/network-design-with-shared-vpc/).

### Security controls

Organization policy constraints prevent high-risk configurations. A VPC Service Controls perimeter isolates services and resources, which helps to mitigate the risk of data leaving to Google Cloud services outside the perimeter. The example landing zone design does not list Security Command Center. The blueprint uses it for threat detection and monitoring. The blueprint groups its controls in three types: policy controls (programmatic constraints), architecture controls (the configuration of resources) and detective controls (finding unusual or malicious behavior). Organization policies have their own article: [organization policies and guardrails](/google-cloud/organization-policies-and-guardrails/).

## The four core elements at a glance

| Core element | What it covers | Examples |
|---|---|---|
| Identity provisioning | Users and groups synchronized from your existing identity provider, and allow policies applied to groups | An existing identity provider, Cloud Identity, IAM |
| Resource hierarchy | The organization, folders and projects | Organization, folders, projects |
| Network | Connectivity for applications in Google Cloud | Shared VPC, service projects, firewall rules, Cloud NAT, Cloud Interconnect, Cloud DNS private zone |
| Security controls | Constraints, VPC Service Controls perimeters and threat detection | Organization policy, VPC Service Controls, Security Command Center |

## Other elements you can add

The four core elements come first. These elements can be added as your needs grow:

| Element | What it covers |
|---|---|
| Monitoring and logging | Log the relevant data, with dashboards that visualize the data and alerts that notify you of any actionable exceptions |
| Backup and disaster recovery | Plan how to back up and recover |
| Compliance | Follow the compliance frameworks that apply to your organization |
| Cost efficiency and control | Monitor and optimize the cost of applications in your landing zone |
| API management | Design a scalable solution for the APIs that you develop |
| Cluster management | Design Google Kubernetes Engine (GKE) clusters that follow best practices |

## What to do before the first application

1. Create an organization resource and a billing account.
2. Your stakeholders must reach a common understanding of the scope and the high-level decisions. Define the goals, set regular checkpoints, and agree on milestones with realistic timelines. Designing and deploying a landing zone can take multiple weeks, so project management is essential.
3. Build a team with people from several technical functions, such as security, identity, networks and operations. Identify a cloud practitioner who understands Google Cloud to lead the team.
4. Pick the first applications. Start with the ones that run most easily on Google Cloud, such as horizontally scaling multi-tier web applications.
5. Design with scalability and growth in mind. Your first iteration is often not your final version.
6. Describe the landing zone as code (IaC), for example with Terraform, and deploy infrastructure changes through an automated pipeline. This helps ensure that internal guidelines are followed and the right controls are in place.

These frameworks, guides and blueprints can help you follow best practices: Google Cloud Setup (a high-level guided flow to help you set up Google Cloud for scalable, production-ready, enterprise applications), the enterprise foundations blueprint, and the Google Cloud Well-Architected Framework (recommendations and best practices to help architects, developers, administrators and other cloud practitioners design and operate a cloud topology that is secure, efficient, resilient, high-performing and cost-effective).

The blueprint is for architects, security practitioners and platform engineering teams. You can use it to create a complete foundation based on best practices, or to review an existing environment on Google Cloud. Its deployable Terraform code is in the `terraform-example-foundation` GitHub repository.

## Common mistakes

- Deploying the first application before the landing zone exists.
- Treating the first version as the final one.
- Designing without scalability and growth in mind.
- Reading "landing zone" as a Google Cloud zone. It is a configuration, not a zone or a zonal resource.
- Planning without people from security, identity, networks or operations, or without a common understanding of the scope among stakeholders.
- Skipping the organization resource or the billing account. Create both before you deploy.

## How to check this in your own project

1. Confirm that your company has an organization resource in Google Cloud.
2. Confirm that a billing account exists, either online or invoiced.
3. For each core element, name one person or team responsible for it: identity provisioning, resource hierarchy, network and security controls.
4. Write down the scope, goals, checkpoints and milestones, and confirm them with your stakeholders.
5. List your first applications.
6. Decide whether you will build the landing zone from code (Terraform), and where the code will be stored.
7. If you already have an environment, read the blueprint pages to compare it with the blueprint before you decide what to copy.

## Sources

- [Landing zone design in Google Cloud](https://docs.cloud.google.com/architecture/landing-zones)
- [Enterprise foundations blueprint](https://docs.cloud.google.com/architecture/security-foundations)
- [Organization structure](https://docs.cloud.google.com/architecture/security-foundations/organization-structure)
