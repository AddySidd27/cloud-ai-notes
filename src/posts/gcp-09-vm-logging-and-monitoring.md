---
title: "Seeing What VMs Do: Ops Agent and Audit Logs"
layout: post.njk
permalink: /google-cloud/vm-logging-and-monitoring/
order: 409
part: 9
tags: gcp-lz
deck: "Prepare a VM for the Ops Agent, and find out who created or changed a VM with audit logs."
---

This article is for people who run virtual machines (VMs) in a Google Cloud landing zone. After reading it you can prepare a VM so the Ops Agent is authorized and can access the logging and monitoring APIs, name the two roles it needs, say what each kind of audit log records, and find out who created or changed a VM. You will also know what happens to some audit logs that are routed to a different project.

It does not cover dashboards or alerts, it does not walk through installing the agent, and it does not cover how to route audit logs from many projects.

Compute Engine VMs and their service accounts are covered in [Compute Engine in a Google Cloud Landing Zone: Where VMs Live](/google-cloud/compute-engine-in-a-landing-zone/). How to sign in to a VM is covered in [Reaching a Compute Engine VM: OS Login, IAM Roles and IAP](/google-cloud/reaching-a-vm-os-login-and-iap/). The folders and projects that hold logs are covered in [Google Cloud Organization, Folders and Projects](/google-cloud/organization-folders-and-projects/).

## Key terms

| Term | Meaning |
|---|---|
| Ops Agent | The primary agent for collecting telemetry from Compute Engine instances. You install it on a VM. |
| Telemetry | What the Ops Agent collects from a VM: logs, metrics and traces. |
| Trace | Data from applications instrumented with OpenTelemetry SDKs, collected as OpenTelemetry Protocol (OTLP) traces. You must configure the agent to collect traces from an instrumented application. |
| Cloud Logging | The service whose API address is `logging.googleapis.com`, which the running Ops Agent requires access to. |
| Logs Explorer | The tool you use to retrieve audit log entries. |
| Cloud Monitoring | The service whose API address is `monitoring.googleapis.com`, which the running Ops Agent requires access to. The agent must be authorized to send telemetry data to Monitoring. |
| Fluent Bit | The software the Ops Agent uses for logs. |
| OpenTelemetry Collector | The software the Ops Agent uses for metrics and traces. |
| Service account | A special kind of account that is typically used by an application or a workload, rather than a person. A VM can have one attached. |
| Service account key | A private key for a service account. It must be stored on the machine, and that storage can be compromised. |
| Application default credentials (ADC) | How Google Cloud authorizes the Ops Agent on a VM. ADC can use an attached service account or a service account key. |
| IAM principal | A user or a service account. IAM is Identity and Access Management. The IAM page lists them under View by principals, with their roles. |
| Logs Writer | A role the Ops Agent's service account needs. Shown as Logging > Logs Writer in the console. |
| Monitoring Metric Writer | A role the Ops Agent's service account needs. Shown as Monitoring > Monitoring Metric Writer in the console. |
| Access scopes | Assigned to a Compute Engine VM instance when you create it. The Ops Agent needs adequate ones. |
| Cloud Audit Logs | Logs written by Google Cloud services that record administrative activities and resource access. They answer "who did what, where, and when?" |
| Log bucket | A container that stores and organizes your logs data. For each billing account, project, folder and organization, Logging creates two: `_Required` and `_Default`. Each has a sink with a matching name. |
| Sink | Used to route log entries. Logging creates a sink with a matching name for each of the `_Required` and `_Default` buckets. |
| Admin Activity log | Audit log entries written by user-driven API calls or other actions that modify the configuration or metadata of resources. |
| System Event log | Audit log entries written by Google Cloud systems and managed service agents that modify the configuration of resources, not by direct user action. |
| Policy Denied log | Audit log entries written when a service denies access to a user or service account because of a security policy violation. |
| Data Access log | Audit log entries written by API calls that read the configuration or metadata of resources, and by user-driven calls that create, modify or read user-provided resource data. |

## What the Ops Agent does

![Left: in a project, a VM runs the Ops Agent. The running agent requires access to Cloud Logging and Cloud Monitoring, shown outside the project box. The VM's attached service account, with the Logs Writer and Monitoring Metric Writer roles, supplies the credentials. Right: Cloud Audit Logs entries are stored in the _Required and _Default buckets. Admin Activity and System Event logs routed to a different project are stored there only if that project has its own log sink.](/img/google-cloud/google-cloud-vm-logging-and-monitoring.svg)

*Source: [Ops Agent overview](https://docs.cloud.google.com/monitoring/agent/ops-agent), [Authorize the Ops Agent](https://docs.cloud.google.com/monitoring/agent/ops-agent/authorization) and [Cloud Audit Logs overview](https://docs.cloud.google.com/logging/docs/audit).*

The left half of the figure is the Ops Agent. The right half is audit logs, which come later in this article.

The Ops Agent is the primary agent for collecting telemetry from your Compute Engine instances. It uses Fluent Bit for logs and the OpenTelemetry Collector for metrics and traces. You can install it on Compute Engine instances. It is not supported on Amazon EC2 instances or on-premises machines.

It collects some data with no configuration:

- Logs: standard system logs, such as `/var/log/syslog` and `/var/log/messages` on Linux and the Windows Event Log.
- Metrics: system metrics such as CPU, disk, memory, network and processes. Some are for Linux only and some for Windows only.

You can also configure it to collect file-based logs, journald (systemd) logs, and log and metric integrations for common third-party applications.

### What the VM requires access to

| When | The VM requires access to |
|---|---|
| Installing | `packages.cloud.google.com` and `dl.google.com` |
| Running | `oauth2.googleapis.com`, `monitoring.googleapis.com` and `logging.googleapis.com` |

The agent also uses TCP ports 20201 and 20202 inside the VM. They must be available on the VM. They do not need to be open to the outside.

The install addresses are DNS names that the VM must be able to reach. For how a VM gets internet access in a landing zone, see [Google Cloud Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/).

### Where not to install it

Do not try to install or configure the Ops Agent by hand on the VMs of some managed services. The list includes App Engine standard and flexible environment instances, Dataflow instances and Google Kubernetes Engine (GKE) node instances.

### Cost

If you install the Ops Agent, you might be charged for the metrics, logs or traces that it sends from the VM to Cloud Logging and Cloud Monitoring for your project.

## Giving the agent access

Google Cloud authorizes the Ops Agent on a VM by using application default credentials (ADC). An attached service account is recommended where possible, because a service account key requires local storage, and that storage can be compromised. The agent does not support `gcloud auth`.

Compute Engine instances are pre-authorized to run the agent. Old VMs, or VMs on which scopes have been modified, might not have adequate access scopes, so the steps below check them. The steps for a custom service account apply when you use one instead of the default service account.

For an attached service account, the steps are: check the VM's access scopes, give the service account the roles, attach it to the VM, and install the agent if it is not installed yet. Scopes are set on the VM, and roles are set on the service account in IAM. Both must be right.

| Role | Shown in the console as |
|---|---|
| Logs Writer | Logging > Logs Writer |
| Monitoring Metric Writer | Monitoring > Monitoring Metric Writer |

### Access scopes

New Compute Engine VMs have adequate access scopes for the Ops Agent, but old VMs or VMs whose scopes were changed might not. The VM has enough access if its default service account lists the `https://www.googleapis.com/auth/cloud-platform` scope. Otherwise it needs one scope from each pair:

- `logging.write` or `logging.admin`
- `monitoring.write` or `monitoring.admin`

To list the scopes, query the VM's metadata server (the source ADC uses to get credentials) for the default service account's scopes:

```
curl --silent --connect-timeout 1 -f -H "Metadata-Flavor: Google" \
  http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/scopes
```

To change scopes in the console, stop the VM, click Edit, and under Identity and API access choose Set access for each API. Set the entries named "Stackdriver Logging API" and "Stackdriver Monitoring API" to Write Only. Save, then start the VM. Scopes are introduced in [Compute Engine in a Google Cloud Landing Zone: Where VMs Live](/google-cloud/compute-engine-in-a-landing-zone/).

### A custom service account

These are the steps for a service account that you attach to the VM.

1. Create the service account. Select the project in which to create the service account. For a Compute Engine VM, choose the project in which you created the instance. Give the service account the Monitoring Metric Writer and Logs Writer roles. Grant your service account the least privileged IAM roles possible.
2. Attach the service account to the VM.
3. Install the agent if it is not installed yet.

To fix an existing account, open the IAM page, select your project, find the service account in the View by principals list, and review the Role column. To add a missing role, click Edit for the service account, click Add Another Role, and save.

## Audit logs: who did what

Google Cloud services write audit logs. There are four types.

| Type | What it records | On by default? |
|---|---|---|
| Admin Activity | Entries written by user-driven API calls or other actions that modify the configuration or metadata of resources. For example, when users create VM instances or change IAM permissions. | Always written. You cannot configure, exclude or disable it. |
| Data Access | Entries written by API calls that read the configuration or metadata of resources. It also records user-driven API calls that create, modify or read user-provided resource data. | Off, except for BigQuery. You must enable it, and it can add log charges. |
| System Event | Entries written by Google Cloud systems and managed service agents that modify the configuration of resources, not by direct user action. | Always written. You cannot configure, exclude or disable it. |
| Policy Denied | Entries written when a service denies access to a user or service account because of a security policy violation. | Generated by default. You cannot disable it, but you can use exclusion filters to prevent it from being stored in Cloud Logging. |

When a user creates a VM, that is an Admin Activity event, so it is always recorded.

### Log names

Each audit log has a name that includes the resource it belongs to. For a project:

- `projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Factivity` (Admin Activity)
- `projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fdata_access` (Data Access)
- `projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fsystem_event` (System Event)
- `projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fpolicy` (Policy Denied)

Folders, billing accounts and organizations use the same endings with `folders/FOLDER_ID`, `billingAccounts/BILLING_ACCOUNT_ID` and `organizations/ORGANIZATION_ID`.

### Who made the change

The caller's identity is in the `AuthenticationInfo` field of the audit log entry. Logging does not redact the caller's principal email address (a principal is a user or service account) for any access that succeeds or for any write operation. For a read that fails with "permission denied", the address might be redacted unless the caller is a service account.

The `callerIp` field records the caller's IP address. For calls between Google Cloud services on the internal production network it shows "private". For a VM without an external IP address it shows the VM's internal address if the VM is in the same organization or project as the resource, and "gce-internal-ip" if not.

### Who can read them

| To read | You need |
|---|---|
| Admin Activity, Policy Denied and System Event logs | Logs Viewer (`roles/logging.viewer`) on the project. It gives read access to these logs, but cannot show Data Access logs in the `_Default` bucket. |
| All logs in `_Required` and `_Default`, including Data Access in `_Default` | Private Logs Viewer (`roles/logging.privateLogViewer`). It includes Logs Viewer and adds access to all logs in those two buckets. |

## Where audit logs are stored and routed

Logging creates the `_Required` and `_Default` buckets and a sink with a matching name for each.

| Bucket | What it stores |
|---|---|
| `_Required` | Admin Activity and System Event logs. You cannot prevent them from being stored, and you cannot configure the sink for this bucket. They are stored in the `_Required` bucket of the project where they were generated. |
| `_Default` | Enabled Data Access logs and Policy Denied logs. To stop Data Access storage, disable those logs. To stop Policy Denied storage, exclude them by modifying the sink's filter. |

You can also route audit log entries to user-defined buckets at the project level, or to supported destinations outside Logging by using sinks.

One detail matters when you send logs to a different project. Admin Activity and System Event logs routed to another project do not pass through the destination project's `_Default` or `_Required` sink, so they are not stored there. To store them, create a log sink in the destination project.

Check how long Logging keeps log entries (the retention period) before you rely on old audit logs.

## Common mistakes

- Installing the Ops Agent by hand on a VM that belongs to a managed service from the "do not install" list, such as GKE nodes or App Engine.
- Forgetting that the service account needs both roles, Logs Writer and Monitoring Metric Writer.
- Not following the stop, edit, save, start steps when changing a VM's scopes.
- Expecting Data Access logs without enabling them. They are off for every service except BigQuery.
- Turning on Data Access logs everywhere without thinking about the extra log charges.
- Giving someone only Logs Viewer and expecting them to see Data Access logs.
- Routing audit logs to another project and expecting them to be stored there without a log sink in that project.
- Using `gcloud auth` credentials for the agent, or storing a service account key when an attached service account would do.

## How to check this in your own project

1. Check that the VM is a Compute Engine VM and not a managed-service VM from the "do not install" list.
2. Check access scopes. Run the metadata server command from the access scopes section. Either the list has the `cloud-platform` scope, or it has one logging scope and one monitoring scope from the pairs above.
3. Open the IAM page, select your project and find the VM's service account under View by principals. Confirm it has Logs Writer and Monitoring Metric Writer.
4. Install the agent if it is not installed yet, using Google's installation guides for the agent. Check that the VM has access to the addresses in the table above.
5. In Logs Explorer, select the project, folder or organization, and type `logName:"cloudaudit.googleapis.com"` in the query. To show the audit logs for one resource and log type, use the Query builder pane.
6. Open an entry from the VM and read the `AuthenticationInfo` field to see who made the change.
7. From the command line, read project audit logs with `gcloud logging read "logName : projects/PROJECT_ID/logs/cloudaudit.googleapis.com" --project=PROJECT_ID`. Add the `--freshness` flag to read logs that are more than 1 day old.
8. Check who has Logs Viewer and who has Private Logs Viewer.
9. Decide whether to enable Data Access logs. They are off by default except for BigQuery, and they can add log charges.

## How the series fits together

The articles in this series:

- [What a Google Cloud Landing Zone Is and What Goes in It](/google-cloud/what-is-a-google-cloud-landing-zone/) shows the parts and how they connect.
- [Who Can Sign In to Google Cloud: Identities, Groups and Roles](/google-cloud/identities-groups-and-roles/) covers who gets access.
- [Google Cloud Organization, Folders and Projects](/google-cloud/organization-folders-and-projects/) covers where resources live.
- [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/) covers organization policies and guardrails.
- [Google Cloud Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/) and [Google Cloud Firewalls and Internet Access](/google-cloud/firewalls-and-internet-access/) cover the network.
- [Compute Engine in a Google Cloud Landing Zone: Where VMs Live](/google-cloud/compute-engine-in-a-landing-zone/) and [Reaching a Compute Engine VM: OS Login, IAM Roles and IAP](/google-cloud/reaching-a-vm-os-login-and-iap/) cover the VMs and how to reach them.
- This article covers the logs and metrics a VM produces.

## Sources

- [Ops Agent overview](https://docs.cloud.google.com/monitoring/agent/ops-agent)
- [Authorize the Ops Agent](https://docs.cloud.google.com/monitoring/agent/ops-agent/authorization)
- [Cloud Audit Logs overview](https://docs.cloud.google.com/logging/docs/audit)
