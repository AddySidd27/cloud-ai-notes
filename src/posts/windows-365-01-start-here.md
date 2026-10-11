---
title: "Windows 365 Enterprise: Start Here"
layout: post.njk
permalink: /windows-365/start-here/
order: 201
part: 1
tags: w365-series
deck: "A beginner's route from the first Cloud PC decision through deployment, management and daily operations, with clearly labelled lab evidence."
---

Windows 365 gives an assigned user a Cloud PC. The user connects from a supported device or browser, while the organization manages the Cloud PC with Microsoft Intune. This series follows one Enterprise pilot from planning to support. Each chapter tells you what to do in your own tenant, what to check, and which result in my lab is actually documented.

This project has an existing Enterprise Cloud PC observed as provisioned, Microsoft Entra joined, enrolled in Intune and accessible through a web session. It does not yet contain a continuous capture from a fresh license assignment through first sign-in. My separate Azure network connection (ANC) test failed a health check; I removed its temporary NAT gateway and public IP. A procedure below is not a claim that I completed that test.

## Words to know

| Term | Meaning |
| --- | --- |
| Cloud PC | The Windows desktop assigned to a user through Windows 365. |
| Provisioning policy | The Intune configuration that defines the Cloud PC's join type, network, image and assignment. |
| Microsoft-hosted network | The network option managed by Microsoft for the Cloud PC. It does not require your Azure subscription for Cloud PC networking. |
| Azure network connection (ANC) | A connection from the Cloud PC's network interface to your Azure virtual network. It needs subnet, DNS and outbound access planning. |
| Microsoft Entra join | The Cloud PC is joined to Microsoft Entra ID without an on-premises AD DS device join. |
| Intune | The management service used to deploy settings, apps, security policies and updates. |

## The route through the series

1. **Prepare:** confirm the Enterprise license, supporting requirements, administrator role, pilot user and a small assignment group. Write success criteria before touching a provisioning policy.
2. **Choose identity and network:** start with Microsoft Entra join and a Microsoft-hosted network for the first exercise. Introduce an ANC when a verified application requirement calls for customer-controlled routing, DNS or private connectivity.
3. **Choose the image:** begin with a gallery image unless the pilot application needs a custom image. Deliver applications through Intune where appropriate.
4. **Provision:** create and assign a Windows 365 Enterprise provisioning policy to the pilot group. Record its join type, network, image, region and group. Check the Cloud PC status and capture an actual error if provisioning fails.
5. **Connect:** ask the assigned user to open [windows365.microsoft.com](https://windows365.microsoft.com/), reach the desktop, disconnect and reconnect. Record the connection method and outcome.
6. **Verify the device:** compare the assigned user, join type, enrollment and last check-in in the Windows 365 and Intune views. A portal object alone is not proof of a working session.
7. **Manage:** test one configuration setting, one app and one update policy at a time. Compare the assignment result with the effective state inside the Cloud PC.
8. **Secure and support:** start Conditional Access in report-only mode, read sign-in logs, and preserve a recovery administrator. Test restart and reconnect before a disruptive lifecycle action.
9. **Test the ANC variant separately:** keep the working Microsoft-hosted Cloud PC in place. Use a dedicated pilot after ANC health is good; clean up temporary Azure resources when the test ends.
10. **Operate:** document support ownership, staged rollout, user changes, license checks, recovery steps and cost review.

The [engineering repository's complete learning journey](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/00-complete-learning-journey.md) has the full checklist, while its [validation status](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) separates observed results from procedures.

## My pilot evidence

This is the sanitized Enterprise license inventory I recorded on September 24, 2026. It shows a seat in inventory; it does not show a new assignment-to-provisioning sequence.

![Sanitized Windows 365 Enterprise license inventory](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-01-2026-09-24-license-inventory.jpg)

The later management checks include the Edge setting observed on the Cloud PC and Company Portal's installed application view. An installed view does not establish that a new Available app assignment or uninstall test succeeded.

![Observed Edge setting on Enterprise pilot](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-05-2026-09-24-edge-settings.jpg)

![Company Portal installed application view](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-07-2026-09-24-company-portal-installed.jpg)

The October 1 ANC health capture records a failed check. The endpoint pattern reported in that lab was `*.infra.windows365.microsoft.com:443`; the exact host and root cause are not established. This is useful troubleshooting evidence, not a successful customer-network deployment.

![Sanitized failed ANC health result](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-03-2026-10-01-anc-health.jpg)

## Architecture before portal clicks

Use the [editable draw.io diagrams and exports](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/architecture) to compare the Microsoft-hosted and ANC paths. A Cloud PC with ANC still runs in the Windows 365 service; its virtual network interface connects to the customer VNet. The ANC does not move the Cloud PC virtual machine into your Azure subscription. Hybrid join has additional AD DS and DNS dependencies, so it belongs in a separate lab.

## A repeatable evidence worksheet

For each action, record the date, pilot group, intended setting, assignment status, result inside the Cloud PC, and any delay or error. Remove user names, tenant identifiers, device IDs, addresses and secrets before publishing. Label a step **verified** only after you observe the result; label an untested walkthrough **procedure**; label a stopped test **blocked** with its error and cleanup.

For this project, [UC-01](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-01-tenant-readiness-and-pilot-design.md) covers readiness, [UC-03](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-03-network-architecture.md) explains the network choices, [UC-02](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-02-enterprise-provisioning.md) covers provisioning, and the [first Cloud PC lab](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/02-first-cloud-pc-lab.md) gives a focused exercise. The use-case IDs are topic identifiers, so read network and image decisions before provisioning even though their numbers are higher.

## What comes next

The following articles will unpack prerequisites, network and identity decisions, provisioning, connection, Intune management, security, lifecycle and support. Optional Boot, Switch and Offline experiences require their own current eligibility checks and supported devices. I will publish those as tested labs only when I can show the outcome.

### References

- Microsoft Learn: [Windows 365 Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements), [network deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options), [create a provisioning policy](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy), [Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections).
- [Windows 365 Enterprise engineering repository](https://github.com/AddySidd27/Windows365-enterprise-engineering) — original lab records, procedures, evidence and editable diagrams.
