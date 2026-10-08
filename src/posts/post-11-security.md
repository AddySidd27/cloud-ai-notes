---
title: "Security"
slug: "security"
series: "Azure Landing Zone"
part: ""
post_number: 11
status: draft
preview_feature: false
fictional_case: false
learn_pages:
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/security"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/security-zero-trust"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/encryption-and-keys"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/defender-for-cloud/onboard-management-group"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/sentinel/overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/defender-for-cloud/just-in-time-access-overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/attestation/overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/event-grid/overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/key-vault/general/overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/azure/web-application-firewall/overview"
    checked_on: "2026-10-08"
  - url: "https://learn.microsoft.com/en-us/security/zero-trust/zero-trust-overview"
    checked_on: "2026-10-08"
repo_links:
  - "https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/security.md"
diagrams:
  - file: "../diagrams/post-11-security-design-area.svg"
    type: own-layout-official-icons
    based_on: "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/security (no diagram on that page; the Zero Trust page has a large architecture diagram that is not redrawn here)"
    icons: "Azure Public Service Icons V24 (Microsoft Defender for Cloud, Azure Sentinel, Log Analytics Workspaces, Key Vaults, Firewalls, Network Security Groups, DDoS Protection Plans, Web Application Firewall Policies, Entra Privileged Identity Management, Policy), unmodified"
    source: "../diagrams/post-11-security-design-area.drawio"
production_section_written_by_addy: true
layout: post.njk
permalink: "/azure-landing-zone/security/"
order: 11
deck: "The Security design area of an Azure landing zone sets up the tools for security operations and the controls for access. It lists what the platform team needs to decide: who gets security alerts, where logs are kept, how access is controlled, and how keys are managed, so every workload starts on the same baseline."
next_num: "13"
next_title: "Management and Monitoring"
tags: [alz]
---



## 1. The problem

In Post 7 you saw who can sign in and what they can change. In Post 8 you saw how to protect privileged access. In Post 10 you saw how networks are laid out. Each of those posts touched security, but none of them asked the wider question: what does the platform team put in place so that security works the same way for every workload?

Microsoft says security is a core consideration for all customers, in every environment, and that it should be considered throughout the process of designing and implementing a landing zone. Microsoft also says an organization must have visibility into what is happening inside everything it runs in the cloud, and that security monitoring and audit logging of Azure platform services is a key part of a scalable framework.

This post follows Microsoft's Security design area. Its stated goal is to understand security requirements and implement them consistently across all workloads in your cloud platform. Microsoft says the primary scope is security operations tooling and access control, and that this scope includes Zero Trust and advanced network security. The Cloud Adoption Framework (CAF) is Microsoft's guidance for adopting the cloud. To streamline the conversation, Microsoft says this design area does not address some disciplines of CAF's Secure methodology: security operations, asset protection and innovation security. Those build on your landing zone deployment. So here only the tools for security operations (alerts, logs, controls) are in scope. This series does not cover running security operations day to day, asset protection or innovation security.

## 2. Simple explanation

### Words you need first

Posts 1 to 10 defined these words: landing zone, workload, platform team, subscription, management group, Azure Policy, hub-and-spoke, Azure RBAC, service principal, managed identity, Microsoft Entra ID, multifactor authentication (MFA), Conditional Access, Privileged Identity Management (PIM), least privilege, just-in-time access (for roles), Zero Trust and its three principles, network security group (NSG), Azure Firewall, DDoS Protection, Log Analytics workspace, Microsoft Sentinel and Microsoft Defender for Cloud.

The words below are new, or are explained more fully here. Each is in plain words, based on Microsoft Learn. Where a row says "my plain words", the explanation is mine, not Microsoft's.

| Word | What it means |
|---|---|
| Cloud Adoption Framework (CAF) and Secure methodology | CAF is Microsoft's guidance for adopting the cloud. Its Secure methodology gives in-depth guidance on security processes and tools. |
| Greenfield and brownfield | Microsoft's headings for two starting points: a new (greenfield) cloud environment and an existing (brownfield) one. |
| Azure Monitor Logs | The part of Azure Monitor that stores log data in a Log Analytics workspace (Post 1), where you can query it. |
| VM | Short for virtual machine: a computer that runs in Azure. |
| Security operations | My plain words: watching for security problems and responding to them. In this design area only the tools for it are in scope. Running it day to day is not covered in this series. |
| SIEM and SOAR | SIEM means security information and event management: a tool that collects security data and finds threats. Microsoft calls Microsoft Sentinel a cloud-native SIEM solution. SOAR means security orchestration, automation and response: a tool that reacts to threats automatically. Microsoft describes the two as one combined solution for hybrid and multicloud environments (hybrid means on-premises plus cloud; multicloud means more than one cloud). In Sentinel, a playbook is a collection of remediation actions that can run on demand or automatically, when an automation rule triggers it. |
| Security alert | A real-time notice of an event that threatens your environment. In Microsoft Defender for Cloud, alerts are categorized and given severity levels, so you can plan the right response. |
| Activity log | My plain words: a record of operations on Azure resources. Learn recommends exporting Azure activity logs to Azure Monitor Logs for long-term retention. |
| Azure Event Grid | My plain words: a service that sends a short notice (an event) to other programs when something happens. Microsoft calls it a fully managed publish-subscribe service. |
| Attestation | A way to prove that software started correctly on a trusted computer. Azure Attestation is Microsoft's service for checking, from a distance, the security and integrity of a platform and of the binaries (programs) running inside it. |
| Trusted Launch and confidential VM | Trusted Launch is a setting for Azure VMs that Microsoft says helps prevent bootkit and rootkit infections (malware that loads before the operating system). A confidential VM is an Azure VM that offers OS disk encryption, with the disk encryption keys bound to the VM's TPM (Trusted Platform Module, my plain words: a security chip). |
| Boot chain | My plain words: the steps a VM goes through to start up. |
| Microsoft cloud security benchmark | A set of high-impact security recommendations to help secure most of the Azure services you use. Microsoft says its recommendations are general and are customized for each service in service recommendation articles. They are grouped into security controls, which are high-level requirements such as network security and data protection. |
| Perimeter | My plain words: the edge of what you protect. Microsoft says the perimeter has two parts: network security controls and Zero Trust access controls. The section below covers them under the headings "Advanced network security" and "Zero Trust access controls". |
| Network segmentation and micro-segmentation | Segmentation (my plain words) means splitting a network into separated parts. Microsoft says to plan to micro-segment individual workloads in their spoke virtual networks. Its example is to define traffic patterns and create fine-grained network security groups for each workload network. |
| Web Application Firewall (WAF) | A firewall that gives centralized protection for web applications against common exploits and vulnerabilities, such as SQL injection and cross-site scripting (two common attacks on websites). |
| HTTPS traffic inspection | My plain words: a firewall looking inside encrypted web traffic (HTTPS is the secure form of web traffic). Microsoft says the firewalls in the platform need to be capable of it for Zero Trust. |
| Blast radius | My plain words: how much can be damaged if one thing is compromised. Microsoft's "assume breach" principle says to minimize it. |
| Zero Trust pillar and deployment objective | A pillar is an area of Zero Trust, for example identity or networks. Each pillar has deployment objectives, which are specific goals that help an organization follow the Zero Trust principles. Microsoft says these goals go beyond technical configurations. |
| Endpoint | My plain words: a laptop, a desktop computer or a mobile device that a person uses. |
| Microsoft Intune | A Microsoft tool for managing devices (my plain words). Microsoft names it, with other device management solutions, as a way to meet endpoint goals. |
| Azure Virtual Desktop | An Azure service that delivers Windows desktops to users (my plain words). |
| Bicep and Terraform | Two tools for deploying Azure resources from code. Terraform was defined in Post 2. |
| BYOD and DLP | BYOD means bring your own device: a personal device used for work. DLP means data loss prevention. Microsoft says that to implement the endpoint objectives you can enforce DLP and access control for both corporate devices and enrolled personal devices. |
| Microsoft Defender for Cloud Apps | Microsoft's tool, named on the Zero Trust page, for managing access to applications. It has standardized policies to enforce your practices. |
| Microsoft Purview | Microsoft's tools for data governance (rules for how data is handled), protection and risk management. |
| Data classification and labeling | Sorting data by how sensitive it is, marking it with that label, and controlling who can access it. |
| Azure Key Vault | A service that stores and controls access to secrets (such as passwords and API keys), manages the encryption keys used to encrypt your data, and manages TLS/SSL certificates (files that prove a website is genuine and secure its traffic). |
| HSM | Hardware security module: a dedicated hardware device that protects encryption keys. Key Vault's Premium tier offers HSM-protected keys. |
| Microsoft-managed and customer-managed keys | My plain words: with Microsoft-managed keys, Azure looks after the encryption key. With customer-managed keys, you control the key. |
| Key rotation | My plain words: replacing a key or certificate with a new one on a routine. |
| Soft delete and purge policies | Key Vault settings that Microsoft recommends. My plain words: soft delete keeps a deleted key or secret recoverable for a set time, and purge protection stops it being permanently erased before that time ends. |
| Data plane | Post 7 defined control plane and data plane. For Key Vault, the data plane is working with the keys and secrets inside a vault. Azure RBAC can authorize it. |
| Just-in-time VM access | A Microsoft Defender for Cloud feature that locks down inbound traffic to a VM. It is different from just-in-time role activation in PIM (Post 8). |
| RDP and SSH | Remote sign-in ports for VMs (RDP for Windows, SSH for Linux). Attackers look for them when they are open. |
| Azure Storage and Azure SQL Database | Azure Storage holds data such as files and blobs. Azure SQL Database is a managed database service. |
| IP forwarding | A setting that lets a VM pass on network traffic that is not meant for itself. |

### What the design area covers

Microsoft splits the Security design area into two parts: security operations and access control. It then adds a reference architecture and two linked pages, Zero Trust and encryption and keys. The table lists all five. This post follows that order, then adds the benchmark and Azure Attestation, and Microsoft's notes for new and existing environments.

| Part | The question it answers |
|---|---|
| Security operations | Who is told about problems, where are the logs, and how do you manage vulnerabilities and shared responsibility? |
| Access control | How do you protect the edge of your cloud, with network security and Zero Trust? |
| Zero Trust in the landing zone | Which Zero Trust area belongs to which landing zone design area? |
| Encryption and keys | Who manages keys, and how are they kept safe? |
| The reference architecture | What does Microsoft's landing zone deploy for security as examples? |

### Security operations tooling: what to decide

Microsoft lists these as design considerations, some of them phrased as questions. Only the tooling is in scope here.

| Topic | What to decide |
|---|---|
| Security alerts | Which teams need alerts, and whether groups of services need alerts routed to different teams. What your business needs for real-time monitoring and alerting. How alerts connect to a SIEM through Microsoft Defender for Cloud and Microsoft Sentinel. |
| Security logs | How long to keep audit data. Microsoft notes that Microsoft Entra ID P1 or P2 reports keep data for 30 days. Also how to archive logs for the long term, such as Azure activity logs, virtual machine logs and platform as a service (PaaS) logs. |
| Security controls | A baseline security setup for virtual machines through Azure in-guest VM policy, and how your security controls line up with governance guardrails. |
| Vulnerability management | Emergency patching for critical vulnerabilities, patching for virtual machines that are offline for long periods, and vulnerability assessment of virtual machines. |
| Shared responsibility | Where one team hands off to another when monitoring or responding to security events. Microsoft points to the Secure methodology for security operations. |
| Encryption and keys | Who needs access to keys, and who manages them. The encryption and keys section below covers this. |
| Attestation | Whether you will use Trusted Launch for your virtual machines and need proof of the integrity of the whole boot chain. Whether you want confidential disk encryption for confidential VMs. Whether your workloads need proof that they run inside a trusted environment. |

Microsoft's recommendations for security operations are:

- Use Microsoft Entra ID reporting to produce access control audit reports.
- Export Azure activity logs to Azure Monitor Logs for long-term retention. Export to Azure Storage for long-term storage beyond two years, if necessary.
- Enable Defender for Cloud standard for all subscriptions, and use Azure Policy to ensure compliance. ("Standard" is Microsoft's wording on this page. In Azure Policy definitions, Learn describes a subscription with a Defender plan enabled as "standard" and a disabled one as "free". Microsoft's newer Defender for Cloud overview talks about free Foundational CSPM capabilities and additional plans, so check which plans you need.)
- Watch the patching of the base operating system for drift, using Azure Monitor Logs and Defender for Cloud. Drift (my plain words) means a machine moving away from the baseline you set.
- Use Azure policies to deploy software settings through virtual machine extensions and to enforce a compliant baseline virtual machine configuration, and watch for security configuration drift with Azure Policy.
- Connect default resource settings to one central Azure Monitor Log Analytics workspace.
- Use a solution based on Azure Event Grid for real-time alerts that are driven by logs.
- Use Azure Attestation to prove the integrity of the whole boot chain of a virtual machine, the secure release of confidential disk encryption keys for a confidential VM, and the state of different workload trusted execution environments.

### Access control: the two parts of the perimeter

Microsoft says modern security boundaries are more complex than those of a traditional datacenter, and that keeping users out of the protected network is no longer enough to control access. The perimeter has two parts.

**Advanced network security.** Microsoft links four pages, each with a one-line purpose:

| Topic | What Microsoft's page covers |
|---|---|
| Inbound and outbound internet connectivity | Recommended models for traffic to and from the public internet. |
| Landing zone network segmentation | Recommendations for secure internal segmentation within a landing zone. Microsoft says these drive network Zero Trust implementation. |
| Network encryption | Recommendations for encryption between on-premises and Azure, and across Azure regions. |
| Traffic inspection | Considerations and approaches for mirroring or tapping traffic within an Azure virtual network. |

**Zero Trust access controls.** For identity, Microsoft asks four questions. Which teams or people need access to services in the landing zone, and in what roles? Who authorizes the access requests? Who gets notified when privileged roles are activated? Who can see the audit history? Microsoft points to Privileged Identity Management for this (Post 8). It adds that Zero Trust can go beyond identity and access management, across pillars such as infrastructure, data and networking.

Microsoft's recommendations for access control are:

- Review each service you need against your requirements. If you want to bring your own keys, not every service may support it, so put a mitigation in place. Choose region pairs and disaster recovery regions that keep latency low.
- Make a security allowlist plan to assess services such as security configuration, monitoring and alerts, and then a plan to connect them to existing systems.
- Decide the incident response plan for Azure services before they move to production. (This is Microsoft's recommendation here. Running incident response day to day is not covered in this series.)
- Align your security requirements with the Azure platform roadmaps, to stay current with new security controls.
- Use a Zero Trust approach for access to the Azure platform where it is appropriate.

### Zero Trust in the landing zone

Microsoft describes Zero Trust as a security strategy built on three principles: verify explicitly (always authenticate and authorize based on all available data points), use least-privilege access (just-enough and just-in-time access, with adaptive risk-based policies) and assume breach (minimize the blast radius, segment access, look for threats and keep improving defenses). Microsoft's overview adds the simple idea behind it: never trust, always verify.

Microsoft says your landing zone is the foundation for your workloads, so it should be ready for Zero Trust. It also says not all Zero Trust objectives belong to a landing zone: many are for designing and releasing individual workloads. Its table maps each landing zone design area to the Zero Trust pillars:

| Landing zone design area | Zero Trust pillar |
|---|---|
| Azure billing and Microsoft Entra tenant | Identity |
| Identity and access management | Identity, applications, data |
| Resource organization | Identity |
| Governance | Visibility, automation and orchestration |
| Management | Endpoints, applications, data, infrastructure |
| Network topology and connectivity | Networks |
| Security | All pillars |
| Platform automation and DevOps | Visibility, automation and orchestration |

For each pillar, Microsoft then gives what the objectives are, what to consider and what to do:

| Pillar | What you can do, and what Microsoft notes about it | Considerations and recommendations on Microsoft's page |
|---|---|---|
| Identity | Identity federation, Conditional Access, identity governance and real-time data operations. Many of the controls are set in your Microsoft Entra tenant, and you must plan configuration requirements beyond the landing zone. | Plan how to manage identities in Microsoft Entra ID beyond Azure resources, for example federation, Conditional Access, and user, device, location or behavior information. Use separate subscriptions for identity resources such as domain controllers. Use managed identities where possible. |
| Endpoints | Register endpoints with cloud identity providers, enforce DLP and access control on corporate and BYOD devices, and monitor device risk. These apply to end-user devices, so you need solutions in Azure and outside it. | Plan endpoint management with Zero Trust practices in addition to the landing zone. If you have endpoints in Azure, such as Azure Virtual Desktop, you can enroll the client experience in Intune and apply Azure policies and controls to restrict access to the infrastructure. |
| Applications | Visibility into applications through APIs, policies to protect sensitive information, adaptive access controls and limiting shadow IT (my plain words: apps used without the organization's approval). These cover using applications, not securing their infrastructure. Landing zone practices do not give detailed controls for this, so it is set in each application's configuration. | Use Defender for Cloud Apps and its standardized policies. Plan how to onboard applications. Microsoft says not to trust applications your organization hosts any more than third-party applications. |
| Data | Classify and label data, enable access control and implement data loss protection. Microsoft says these need controls beyond Azure resources. | Use Microsoft Purview. Under subscription democratization, you can create access and network isolation for data resources and set up logging. The reference implementations include policies for logging and managing data resources. |
| Infrastructure | Monitor abnormal behavior in workloads, manage infrastructure identities, limit human access and segment resources. | Use the standard landing zone policies to block noncompliant deployments and enforce logging. Use PIM for just-in-time access to highly privileged roles. Use just-in-time VM access in Defender for Cloud to restrict access to virtual machines. Plan how to monitor and manage each workload. |
| Networks | Network segmentation, cloud-native filtering and least-access privilege. | Deploy firewalls capable of HTTPS inspection, and isolate identity and management network resources from the central hub. Plan micro-segmentation of each workload in its spoke virtual network. Microsoft links three Zero Trust deployment guides (Azure portal, Bicep and Terraform) and two further pages. |
| Visibility, automation and orchestration | Establish visibility, enable automation and keep improving. The reference implementations give policies for Azure logging, but other services need more integration. | Deploy Microsoft Sentinel as part of the landing zone. Plan to bring signals from Microsoft Entra ID and Microsoft 365 tools into your Sentinel workspace. Plan threat-hunting exercises and continual security improvement. |

One detail is worth keeping in mind. Just-in-time VM access in Defender for Cloud, which Microsoft's page describes as a Defender for Servers Plan 2 feature, protects machines from attackers who look for open management ports such as RDP or SSH. It locks down inbound traffic to the VM. When a request is approved, Defender for Cloud configures the network security groups and Azure Firewall to allow inbound traffic to the selected ports from the relevant IP address or range for the specified amount of time.

### Encryption and keys

Microsoft says encryption is a vital step toward data privacy, compliance and data residency in Azure. Its design considerations for Azure Key Vault include:

- Set subscription and scale limits as they apply to Key Vault. Key Vault has transaction limits for keys and secrets.
- A key vault is a security boundary, because permissions for keys, secrets and certificates are set at the vault level. Access policy assignments grant permissions to keys, secrets or certificates separately, but they do not support object-level permissions for a specific key, secret or certificate.
- Keep application-specific and workload-specific secrets apart from shared secrets where needed, to control access.
- Use Premium where HSM-protected keys are needed.
- Manage key rotation and secret expiration, and use Key Vault certificates to handle certificate procurement and signing, with alerts, notifications and automatic renewal.
- Set disaster recovery needs and replication and failover settings for keys, certificates and secrets.
- Monitor how keys, certificates and secrets are used, to detect unauthorized access.
- Delegate Key Vault creation and privileged access.
- Set your requirements for customer-managed keys, for example for Azure Storage encryption, whole-disk encryption for virtual machines, and encryption of data in transit and at rest.

Microsoft's recommendations are:

- Use a federated Key Vault model to avoid the transaction limits. My reading: several vaults, one per application or workload, not one central vault.
- Use Azure RBAC to authorize the data plane of Key Vault.
- Create vaults with soft delete and purge policies turned on.
- Follow least privilege: limit permission to permanently delete keys, secrets and certificates to specialized custom Microsoft Entra roles.
- Automate certificate renewal with public certificate authorities, and automate key and certificate rotation.
- Turn on the firewall and virtual network service endpoints on the vault to control access to it.
- Use the platform's central Azure Monitor Log Analytics workspace to audit key, certificate and secret use in each vault.
- Delegate vault creation and privileged access, and use Azure Policy to enforce a consistent, compliant configuration.
- Default to Microsoft-managed keys for the main encryption functions, and use customer-managed keys when required.
- Do not use centralized Key Vault instances for application keys or secrets, unless you use a Managed HSM instance (a Key Vault option with HSM-protected keys). Microsoft says several vaults reduce the blast radius, can improve performance, and are easier to manage when they match application or workload boundaries.
- Do not share Key Vault instances between applications, to avoid sharing secrets across environments.

### Microsoft cloud security benchmark and Azure Attestation

Microsoft covers two more items in this design area. The first is the Microsoft cloud security benchmark, whose recommendations are general and are customized for each service in service recommendation articles. The second is Azure Attestation, which Microsoft calls a tool to help you ensure the security and integrity of a platform and of the software that runs inside it.

### Examples of what the reference architecture includes

Microsoft says security is at the core of the Azure landing zone reference architecture, and that many tools and controls are deployed so organizations can reach a security baseline quickly. These are two separate lists, not pairs.

Tools included, as examples:

- Microsoft Defender for Cloud (standard or free tier)
- Microsoft Sentinel
- Azure DDoS Network Protection (optional; Post 10 calls it DDoS Protection)
- Azure Firewall
- Web Application Firewall (WAF)
- Privileged Identity Management (PIM)

Policies included for the Online and Corp (corporate-connected) landing zones (Post 9):

- Enforce secure access, such as HTTPS, to storage accounts
- Enforce auditing for Azure SQL Database
- Enforce encryption for Azure SQL Database
- Prevent IP forwarding
- Prevent inbound RDP from the internet
- Ensure subnets are associated with an NSG

### New and existing environments

For a new (greenfield) environment, Microsoft points to creating your initial subscriptions and to the Bicep deployment templates, which Microsoft says (for greenfield and brownfield) have proven-practice security guidance built in. For an existing (brownfield) environment, Microsoft suggests four services to bring the same principles to it:

- Microsoft Entra Connect cloud sync, for hybrid identity. With hybrid identity you can also enforce MFA and Microsoft Entra Password Protection.
- Conditional Access.
- Privileged Identity Management, with recurring access reviews.
- The recommendations, alerting and remediation of Defender for Cloud. A security team can connect it to Microsoft Sentinel when it needs a more robust, centrally managed hybrid and multicloud SIEM and SOAR solution.

## 3. Diagram

![Security in the landing zone. Left, security operations tooling: alerts (Defender for Cloud, Sentinel), logs, controls and patching, encryption and keys (Key Vault), and Azure Attestation. Middle, access control: network security controls and Zero Trust access controls, with the pillar names. Right, what the reference architecture includes: six tools and six policies. A footer notes what is out of scope.](/diagrams/post-11-security-design-area.svg)

*Simplified diagram, drawn by me with my own layout, because the Security page on Microsoft Learn has no diagram: [Design area: Security](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/security). Not an official Microsoft diagram. I show only the pillar names, and I left out the benchmark and the brownfield services. Icons are from the official [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/), unmodified.*

## 4. What I have seen in production

### Mistakes to check for first

Most of these are risks I worked out from Microsoft's recommendations, one line each. The next part says which ones I saw myself.

- **Alerts with no owner.** Microsoft asks which teams need alerts and whether some services need alerts routed to different teams.
- **Logs kept too short.** Microsoft notes Microsoft Entra ID P1 or P2 reports keep data for 30 days, and says to export activity logs for long-term retention.
- **Defender for Cloud left off some subscriptions.** Microsoft says to enable it for all subscriptions and use Azure Policy to ensure compliance.
- **Drift left unwatched.** Microsoft says to watch operating system patching and security configuration drift.
- **One central key vault for everything.** Microsoft says not to use centralized Key Vault instances for application keys or secrets, and not to share vaults between applications.
- **Deleted keys that can be lost for good.** Microsoft says to create vaults with soft delete and purge policies on, and to limit permanent deletion to specialized roles.
- **Keys and certificates that are never rotated, or that expire without warning.** Microsoft says to automate rotation and certificate renewal.
- **Zero Trust treated as an identity-only job.** Microsoft says Zero Trust can go beyond identity and access management, across pillars such as infrastructure, data and networking, and that many objectives are for individual workloads, not the landing zone.
- **Treating hosted applications as trusted.** Microsoft says not to trust applications your organization hosts any more than third-party applications.

### From my own projects

In my own projects, two of the points above were real problems:

- **Key Vault sprawl.** This was a real problem.
- **Logs and alerts.** This was a real problem.

I leave out project details.

## 5. Repo

- Security design area: the platform baseline and shared responsibility (my own short checklist): [security.md](https://github.com/AddySidd27/Azure_landing_zone/blob/main/docs/02-design-areas/security.md)

## 6. Sources

Microsoft Learn, checked October 2026: [Design area: Security](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/security) · [Incorporate Zero Trust practices in your landing zone](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/security-zero-trust) · [Encryption and key management in Azure](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/encryption-and-keys)

Where a sentence says "my plain words", it is my own explanation. Short definitions of Microsoft Sentinel, Defender for Cloud, Key Vault, Azure Attestation, Event Grid, Web Application Firewall and just-in-time VM access come from their own Learn overview pages, and the Zero Trust overview page gives "never trust, always verify". The Defender for Cloud "standard" and "free" wording comes from the Learn page on enabling Defender for Cloud on all subscriptions in a management group. The mistakes list and the repo checklist are mine too.

