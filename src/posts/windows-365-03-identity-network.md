---
title: "Windows 365 Enterprise: Choose Identity and Network"
layout: post.njk
permalink: /windows-365/identity-network/
order: 203
part: 3
tags: w365-series
deck: "Understand Microsoft Entra join, Microsoft-hosted networking and an Azure network connection before building a policy."
---

Make the identity and network decision before you create a provisioning policy. It determines which dependencies must work during provisioning and which team owns a failure. An Azure network connection (ANC) attaches the Cloud PC's network interface to your virtual network; Windows 365 still provisions the Cloud PC in a Microsoft-hosted subscription.

## Two decisions, not one

| Question | Simple first pilot | Use the other route when |
| --- | --- | --- |
| Device join | Microsoft Entra join | An application or management dependency requires hybrid join and you have healthy AD DS, DNS and line of sight. |
| Network | Microsoft-hosted network | A documented need requires customer VNet routing, private access, custom DNS or network controls. |

These choices are related but distinct. Microsoft Entra join can use an ANC. Hybrid join needs additional directory and network planning. See Microsoft's [deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options) and [identity guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/identity-authentication) for supported combinations and current requirements.

## Microsoft-hosted path

For the first exercise, choose Microsoft Entra join and a Microsoft-hosted network where it meets your requirements. Select the geography or region options offered by the current provisioning wizard. Test application reachability from the Cloud PC; do not infer that a private application works because the desktop opens. A working Cloud PC with this path can stay in place while you test an ANC separately.

## ANC path

Before creating an ANC, record the subscription, resource group, VNet, dedicated subnet, address capacity, DNS resolvers, routes, outbound connectivity and the people responsible for each. Check [ANC requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections) and [network endpoints](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network). The ANC health checks report whether the connection is ready for provisioning. A created object is not the same as a healthy connection.

My isolated East US Microsoft Entra join ANC lab used a VNet and private subnet. The health check later reported a failure for an outbound Windows 365 infrastructure endpoint pattern on TCP 443. The exact host and root cause remain unproven. I removed the temporary NAT gateway and Standard public IP after the test and did not move the working Microsoft-hosted Cloud PC. The [network use case](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/use-cases/UC-03-network-architecture.md) and [validation log](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) keep the procedure and observed result separate.

![Sanitized ANC health failure from the isolated lab](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-03-2026-10-01-anc-health.jpg)

The [editable architecture diagrams](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/architecture) accompany the Microsoft-hosted and ANC descriptions. Compare their paths with the linked Microsoft documentation before adapting them to your tenant.

## Decision checkpoint

Write one sentence explaining why the pilot needs an ANC. If you cannot identify an application, security or routing requirement, proceed with the Microsoft-hosted option. For ANC, require a healthy check, a dedicated pilot policy and a recovery plan before changing any production assignment.

Next: [choose an image and provision](/windows-365/provision/).

### Microsoft Learn

- [Windows 365 deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options)
- [Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections)
- [Network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network)
