---
title: "Who Can Sign In to Google Cloud: Identities, Groups and Roles"
seoTitle: "Google Cloud Identities, Groups and Roles"
layout: post.njk
permalink: /google-cloud/identities-groups-and-roles/
order: 402
part: 2
tags: gcp-lz
deck: "Choose how people get Google Cloud accounts, and give access to groups through roles instead of to individual people."
description: "Learn the three ways to bring user accounts into Google Cloud, why roles go to groups, which groups the blueprint configures, and how super admin accounts differ."
---

Before anyone builds a network or starts a virtual machine, you must decide who can sign in to Google Cloud and what each person can do. This article is for people who plan the first setup of Google Cloud for a company. After reading it you can pick one of three ways to bring user accounts in, explain why roles are given to groups, and list the groups that the example foundation configures.

The example foundation is the blueprint from the [overview article](/google-cloud/what-is-a-google-cloud-landing-zone/). This article covers the blueprint's authentication and authorization design. It does not cover how people log in to a virtual machine. That comes later in the series.

## Key terms

| Term | Meaning |
|---|---|
| Identity provider (IdP) | Google Cloud uses Google Sign-In to authenticate users. It is the same identity provider (IdP) that other Google services such as Gmail or Google Ads use. Active Directory, Microsoft Entra ID, ForgeRock, Okta and Ping Identity are examples of existing identity providers. |
| Google Workspace | A Google product where you can create user accounts directly. |
| Cloud Identity | The Google service that you use to manage identities for accessing Google Cloud services. You can create user accounts directly in it. If you already use Google Workspace, it uses the same console, administrative controls and user accounts as your Google Workspace account. |
| Managed account | An account that you manage in Cloud Identity or Google Workspace, so that you control the lifecycle and security of the account. |
| Consumer account | An account fully owned and managed by the person who created it. |
| Federation | Trust between two or more identity providers. Federation helps you ensure that your existing account management processes apply to Google Cloud and other Google services. |
| Workforce Identity Federation | A way to federate a Google Cloud organization directly with an external identity provider, without Cloud Identity or Google Workspace. |
| Google Cloud Directory Sync | The tool that Active Directory uses to provision identities to Cloud Identity in the blueprint's example. |
| 2-step verification | The blueprint recommends enforcing it for all user accounts. It helps mitigate threats such as phishing and social engineering. |
| Security key | Keys based on the phishing-resistant FIDO U2F (CTAP1) standards are one kind of phishing-resistant mechanism. The Titan Security Key is an example. |
| Super administrator (super admin) | A Cloud Identity account that authenticates directly to Cloud Identity, with a password. |
| Principal | An identity that has authenticated to Google Cloud. Principal types that represent people include Google Accounts and Google groups. |
| Permission | Determines what operations are allowed on a resource. |
| Role | A collection of permissions. You cannot grant permissions directly to a principal. You grant roles. |
| Allow policy | An object attached to a Google Cloud resource. |
| Basic role | A highly permissive role that gives broad access to Google Cloud services. Owner, Editor and Viewer are basic roles. |
| Predefined role | A role that is managed by a Google Cloud service. |
| IAM | Identity and Access Management. The Google Cloud tool that manages fine-grained authorization. |

## Where Google Cloud sign-in comes from

Google Cloud uses Google Sign-In to authenticate users. It is the same identity provider that Gmail and Google Ads use. Avoid letting employees use their private accounts to access Google Cloud. Onboard them to Cloud Identity or Google Workspace, so that you control the lifecycle and security of the accounts. These are managed accounts: accounts that you manage in Cloud Identity or Google Workspace.

You make two decisions: how user accounts get into Google, and what to do with consumer accounts your employees already have.

## Decision 1: Pick an identity architecture

There are three options. Check both columns, because each option has cases where it does not fit.

| Option | What it means | Use it when | Avoid it when |
|---|---|---|---|
| 1. Google as the primary identity provider | You create user accounts directly in Cloud Identity or Google Workspace. | Identities already exist in Google Workspace; you have no existing identity provider; or you have one but want to start quickly with a small subset of users and federate identities later. | You have an existing identity provider that you want as the authoritative source for identities. |
| 2. Cloud Identity federated with an external identity provider | You link your existing identity provider to Cloud Identity. People sign in to Google Cloud and other Google services with their existing credentials. | You have an existing identity provider such as Active Directory, Microsoft Entra ID, ForgeRock, Okta or Ping Identity, and you want employees to use their existing credentials for Google Cloud and services such as Google Ads and Google Marketing Platform. | You have no existing identity provider. |
| 3. Workforce Identity Federation | You federate the Google Cloud organization directly with an external identity provider. This does not involve Cloud Identity or Google Workspace. | You do not want to federate with Cloud Identity, you have an existing identity provider, and the Google services you need support Workforce Identity Federation. | You have no existing identity provider, or your users need other Google services such as Google Workspace or Google Ads. |

The blueprint recommends option 2, because federation helps you ensure that your existing account management processes apply to Google Cloud and other Google services. If you have no identity provider, you can create accounts directly in Cloud Identity.

## How federation works in the blueprint

The diagram shows option 2, federation, using the blueprint's example. The example uses Microsoft Active Directory. Active Directory uses Google Cloud Directory Sync to provision identities to Cloud Identity. Users attempting to sign in to Google services are redirected to the external identity provider. No passwords are synchronized with Cloud Identity.

The blueprint has a table of setup guides: two for Active Directory (one for provisioning identities and one for sign-in), one for Microsoft Entra ID, and others for providers such as Ping and Okta.

![Active Directory provisions identities to Cloud Identity through Google Cloud Directory Sync. Sign-in is redirected to the identity provider. IAM roles are granted to the groups. Super admin accounts authenticate directly to Cloud Identity with a password.](/img/google-cloud/google-cloud-identities-groups-and-roles.png)

*Source: [Authentication and authorization](https://docs.cloud.google.com/architecture/security-foundations/authentication-authorization).*

The blueprint recommends enforcing multi-factor authentication at your identity provider, with a phishing-resistant mechanism.

## Super admin accounts are different

Cloud Identity users with the super admin account authenticate directly to Cloud Identity, with a password, and bypass the sign-in settings of the organization. Other users are redirected to the identity provider. This is by design, so that a super admin can still access the Cloud Identity console if the sign-in setup with the identity provider is misconfigured or has an outage. It also means super admin accounts need extra protection. Always enforce 2-step verification with security keys for them.

## Decision 2: Deal with consumer accounts

Some users in your organization might already have a private Google account. Consumer accounts are not under your organization's control and might mix personal and corporate data. Consolidate them during onboarding. If you do not already use Google Workspace for all your user accounts, also block access to consumer accounts.

There are three ways to consolidate.

| Option | What it means | Use it when | Avoid it when |
|---|---|---|---|
| Migrate a relevant subset | Migrate only the consumer accounts relevant to your Google Cloud deployment. | The transfer tool for unmanaged user accounts shows many consumer accounts, but only some users will use Google Cloud, and you want to save time. | You have no consumer accounts in your domain, or you want all data from all consumer accounts consolidated before you use Google Cloud. |
| Migrate all accounts | Migrate all consumer accounts to managed accounts. | The transfer tool shows only a few consumer accounts, and you want to restrict consumer account use in your organization. | You want to save time. |
| Evict all accounts | You create a managed user identity with the same name without migrating the consumer account first. The owner of the consumer account keeps full control of it and its data. You do not transfer any of that data to your organization. | You want new managed accounts without transferring data from consumer accounts, you want to restrict available Google services, and you also want users to keep their data and keep using their consumer accounts. | Consumer accounts have been used for corporate purposes and might access corporate data. |

## Give roles to groups, not people

Access in Google Cloud works in three parts: a principal (who), a role (a set of permissions) and a resource (what). You grant a role to a principal on a resource. Roles on a container resource also apply to the resources inside it, because descendant resources inherit the allow policies of their ancestors. The [organization, folders and projects article](/google-cloud/organization-folders-and-projects/) covers that.

To manage roles at scale, assign users to groups based on their job functions, then grant IAM roles to those groups. Avoid granting roles to individual users. Add users to groups with the processes in your existing identity provider for group creation and membership. As you build your own workloads, you create more groups and grant roles to them.

Avoid basic roles (Owner, Editor, Viewer) and use predefined roles instead. Basic roles are overly permissive and a potential security risk.

## The groups the blueprint configures

The table shows the groups that the blueprint configures for viewing foundation resources, with example addresses such as `grp-gcp-org-admin@example.com`. You do not need to know the products in the roles column yet. The table only shows which role goes to which group. The billing, logging, secrets and KMS projects in the last column are projects that the blueprint names; projects are explained in the [organization, folders and projects article](/google-cloud/organization-folders-and-projects/). Group names and roles are copied from the blueprint, and a name does not always describe its role exactly. For example, `grp-gcp-kms-admin` has the Cloud KMS Viewer role.

| Group | What it is for | Roles | Where the role is granted |
|---|---|---|---|
| `grp-gcp-org-admin` | Highly privileged administrators who can grant IAM roles at the organization level. The privilege is not recommended for daily use. | Organization Administrator | Organization |
| `grp-gcp-billing-admin` | Highly privileged administrators who can modify the Cloud Billing account. The privilege is not recommended for daily use. | Billing Account Admin | Organization |
| `grp-gcp-billing-viewer` | The team that views and analyzes spending across all projects. | Billing Account Viewer; BigQuery User | Organization; billing project |
| `grp-gcp-audit-viewer` | The team that audits security-related logs. | Logs Viewer; BigQuery User | Logging project |
| `grp-gcp-security-reviewer` | The team that reviews cloud security. | Security Reviewer | Organization |
| `grp-gcp-network-viewer` | The team that views and maintains network configurations. | Compute Network Viewer | Organization |
| `grp-gcp-scc-admin` | The team that configures Security Command Center. | Security Center Admin Editor | Organization |
| `grp-gcp-secrets-admin` | The team that manages, stores and audits credentials and other secrets used by applications. | Secret Manager Admin | Secrets projects |
| `grp-gcp-kms-admin` | The team that enforces encryption key management to meet compliance requirements. | Cloud KMS Viewer | KMS projects |

## Settings the blueprint does not set for you

The blueprint's code does not automate the recommended Cloud Identity settings. You set them yourself, early. The blueprint's list includes:

- Enforce 2-step verification for all user accounts, with a phishing-resistant mechanism such as security keys.
- Require reauthentication every 16 hours with a security key for Google Cloud services.
- Share Cloud Identity audit logs with your Google Cloud environment.
- Make sure all user accounts are managed accounts.
- Disable account recovery for super admin accounts. It is off by default for new customers, and existing customers might have it on. Plan an internal process for a super admin to contact another super admin.
- Disable password reuse and monitor password strength for users who sign in to Cloud Identity with a password.
- Configure group sharing so that group owners cannot add external members. If you synchronize groups from your identity provider, these sharing settings do not apply to that synchronization, so check the controls in your identity provider.

## Common mistakes

- **Letting people use private accounts.** Use managed accounts.
- **Choosing federation when you have no identity provider.** Check the use and avoid columns in the table above.
- **Creating users directly in Google when your existing identity provider is the source for identities.** That is a case where option 1 does not fit.
- **Granting roles to individual users.** Grant them to groups instead.
- **Using Owner, Editor or Viewer.** Use predefined roles instead.
- **Treating super admins like normal users.** They authenticate directly to Cloud Identity with a password, so protect them with 2-step verification and security keys.
- **Assuming the blueprint's code configures Cloud Identity.** It does not. Check each recommended setting by hand.

## How to check this in your own project

1. Write down whether your company already has an identity provider. Use that answer and the table in Decision 1 to pick one of the three options.
2. List your super admin accounts. For each one, check that 2-step verification with a security key is enforced.
3. Find the consumer accounts that use your company's domain. Choose one of the three consolidation options.
4. List the groups that exist today and the roles each one has. Compare them with the table above. Mark any group that has Owner, Editor or Viewer.
5. Look at the allow policies on your organization and your projects. Check that roles are granted to groups and not to single users.
6. Check each setting in the previous section by hand. The blueprint's code does not do it for you.

Next: [Organization, Folders and Projects](/google-cloud/organization-folders-and-projects/).

## Sources

- [Decide how to onboard identities](https://docs.cloud.google.com/architecture/landing-zones/decide-how-to-onboard-identities)
- [Authentication and authorization](https://docs.cloud.google.com/architecture/security-foundations/authentication-authorization)
- [IAM overview](https://docs.cloud.google.com/iam/docs/overview)
