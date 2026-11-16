---
title: "Windows 365 Enterprise: Choose Identity and Network"
seoTitle: "Windows 365: Choose Identity and Network"
layout: post.njk
permalink: /windows-365/identity-network/
order: 203
part: 3
tags: w365-series
deck: "Understand Microsoft Entra join, Microsoft-hosted networking and an Azure network connection before building a policy."
---

Make the identity and network decision before you create a provisioning policy. A provisioning policy is the Intune setting that tells Windows 365 how to build a Cloud PC. The choice decides which dependencies must work during provisioning and which team owns a failure.

## Words to know

| Term | Meaning |
|---|---|
| Cloud PC | The Windows desktop that Windows 365 gives to a user. |
| Microsoft Entra join | The Cloud PC belongs to Microsoft Entra ID only (the cloud). It does not join an on-premises domain. |
| Hybrid join (Microsoft Entra hybrid join) | The Cloud PC joins your on-premises Active Directory domain and is also registered in Microsoft Entra ID. |
| AD DS | Active Directory Domain Services, your on-premises directory and its domain controllers. |
| Microsoft-hosted network | A network that Microsoft supplies and manages for the Cloud PC. You do not need an Azure subscription for it. |
| Azure network connection (ANC) | An object in Intune that points to a subnet in your own Azure virtual network. Windows 365 still creates the Cloud PC in a Microsoft-hosted subscription and attaches its network interface to your subnet. |
| VNet | Azure virtual network, a private network that you own in your Azure subscription. |
| DNS | The Domain Name System, which turns names into IP addresses. Hybrid join needs DNS that can resolve your AD DS domain. |
| FQDN | Fully qualified domain name, the full name of a domain or host, for example `corp.contoso.com`. |

## Two decisions, not one

| Question | Simple first pilot | Use the other route when |
|---|---|---|
| Device join | Microsoft Entra join | An application or management dependency requires hybrid join and you have healthy AD DS, working DNS and line of sight (a working network route) to a domain controller. |
| Network | Microsoft-hosted network | A specific need requires customer VNet routing, private access, custom DNS or network controls. |

These choices are related. Microsoft Entra join works with either network option, including an ANC. Hybrid join always needs an ANC, because the Microsoft-hosted network is not compatible with Microsoft Entra hybrid join ([Network deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options)).

Hybrid join also needs extra directory and network planning. See Microsoft's [deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options) and [identity guidance](https://learn.microsoft.com/en-us/windows-365/enterprise/identity-authentication) for supported combinations and current requirements.

## Microsoft-hosted path

For the first exercise, choose Microsoft Entra join and a Microsoft-hosted network where it meets your requirements. In the provisioning wizard, select a geography. For the region, Microsoft recommends **All default regions within the geography**, which gives the best resiliency and provisioning success ([Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)). Test that the Cloud PC can reach your applications. A desktop that opens does not mean a private application works. You can keep a working Microsoft-hosted Cloud PC and test an ANC with a different policy and a different test user.

## ANC path

Before creating an ANC, record the subscription, resource group, VNet, dedicated subnet, address capacity, DNS resolvers, routes, outbound connectivity and the people responsible for each. Check [ANC requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections) and [network endpoints](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network). The ANC health checks report whether the connection is ready for provisioning. Creating the ANC does not make it healthy.

The health checks work like this ([Azure network connection overview](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections)):

- The first health check runs after you create the ANC. Until it finishes and succeeds, you cannot assign the ANC to a provisioning policy.
- Checks run every one to six hours. A full check can take up to 30 minutes.
- To start a full check yourself, go to **Devices > Provision Cloud PCs > Azure network connection**, select the ANC and select **Retry**.
- To create or edit an ANC you need at least the Subscription Reader role on the Azure subscription that holds the VNet, and the Intune Administrator or Windows 365 Administrator role.

The health check can fail for an outbound endpoint that Windows 365 must reach. The required endpoints, such as `*.infra.windows365.microsoft.com` on port 443, are listed in the [network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network). For general causes and fixes, see [ANC health failures](/windows-365/anc-troubleshooting/).

## Editable network diagrams

The [editable architecture diagrams](https://github.com/AddySidd27/Windows365-enterprise-engineering/tree/main/architecture) show the two network paths: the Microsoft-hosted network, and Microsoft Entra join with an ANC to a customer VNet. Compare them with the linked Microsoft documentation before you adapt them to your tenant.

## Hybrid join: a separate provisioning exercise

Microsoft describes hybrid join as the traditional approach, for organizations that still depend on on-premises Active Directory while they move to a cloud-native model. Use Microsoft Entra join for new deployments, and consider hybrid join only when a dependency cannot be met without it. If you need it, plan it as a separate exercise with these steps.

### 1. Prove the directory path first

Microsoft Entra hybrid join starts with a Windows Server Active Directory domain join. The device is then registered in Microsoft Entra ID through the organization's hybrid join configuration. A hybrid Cloud PC needs an Azure subscription and a VNet with line of sight to a domain controller. It also needs an ANC, because hybrid join does not work on a Microsoft-hosted network ([Network deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options), [Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)).

The assigned user must have a hybrid identity. Check the [Windows 365 identity matrix](https://learn.microsoft.com/en-us/windows-365/enterprise/identity-authentication) and [Enterprise requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements) before building anything.

In a test domain, document the domain's fully qualified domain name (FQDN), target organizational unit (OU), DNS servers, domain controller reachability, hybrid join configuration and the account delegated to join computers in that OU. Microsoft Entra Connect is the tool that copies directory objects to Microsoft Entra ID.

If the computer objects belong to specific OUs, configure those OUs to sync in Microsoft Entra Connect, and do not exclude the default device attributes ([Configure Microsoft Entra hybrid join](https://learn.microsoft.com/en-us/entra/identity/devices/how-to-hybrid-join)). Follow the [Microsoft Entra hybrid join configuration guide](https://learn.microsoft.com/en-us/entra/identity/devices/how-to-hybrid-join). Do not publish the join account password, domain controller addresses or tenant identifiers.

**Check:** From a test machine on the planned network, resolve the AD domain and reach a domain controller. Confirm that hybrid join and synchronization are configured for the same tenant. Typing a DNS server address into a form does not prove that names resolve or that the device registers.

### 2. Build the customer network deliberately

Plan a VNet and a subnet with enough available addresses for Cloud PCs, recovery and reprovisioning. Define your AD DS DNS servers as the custom DNS servers of the VNet so that the VNet can resolve your AD DS domain. Microsoft suggests at least two DNS servers. Also provide network access from the VNet to a domain controller.

The domain controller can be in Azure or on-premises over working connectivity. Also allow the required outbound endpoints for Windows 365, Intune, Microsoft Entra device registration and Azure Virtual Desktop session hosts. Use the current [Windows 365 network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network) instead of a port list from an old screenshot.

A hybrid ANC asks for the Azure network details and AD domain details, target OU and domain join credentials. The Cloud PC still runs in the Windows 365 service; its network interface is connected to the selected customer VNet. See the [ANC overview](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections). An Entra join ANC with no AD DS is not a hybrid ANC.

**Check:** Keep the working Microsoft-hosted policy and user assignment untouched. Create a separate hybrid ANC only when directory, DNS, routes, permissions and cost controls (a plan to delete test VNet resources when finished) are ready. Wait for a **Healthy** ANC check, which can take a while because a full check can last up to 30 minutes; inspect every failed check before selecting it in a provisioning policy. If a check fails, fix the cause and select **Retry** instead of assigning the ANC. Keep a recovery plan: a way to point users back to the working Microsoft-hosted policy.

### 3. Create a dedicated policy and assignment

In the Microsoft Intune admin center, go to **Devices > Provision Cloud PCs > Provisioning policies > Create policy**. On General, select **Hybrid Microsoft Entra join** and the healthy hybrid ANC. Choose the image, configuration and a dedicated pilot user group, then review the complete policy.

When you select **Create**, a hybrid policy can take up to 60 minutes to finish, depending on when Microsoft Entra Connect last synced ([Create provisioning policies](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy)). Microsoft's [current provisioning policy guide](https://learn.microsoft.com/en-us/windows-365/enterprise/create-provisioning-policy) requires an ANC for this join type. Use a licensed, eligible test user and avoid overlapping assignments that could affect the existing Cloud PC.

Record the policy name, join type, selected ANC, image and assigned group. Take screenshots of the wizard pages for your own records. A Review + create screenshot only shows the inputs you chose. It does not show that provisioning or sign-in worked.

### 4. Verify each outcome separately

| Checkpoint | What to record |
|---|---|
| ANC ready | Healthy status and date, with no unresolved failed checks |
| Provisioning | New pilot Cloud PC and its policy/status in **All Cloud PCs** |
| AD DS join | Computer object in the intended domain and OU |
| Hybrid registration | Device join state in Microsoft Entra ID and a device-side registration check |
| Management | Intune enrollment, primary user and last check-in |
| User experience | Successful first sign-in, disconnect/reconnect and required app reachability |

A **Provisioned** status in the portal does not show that the domain join, hybrid registration, Intune enrollment and user session all worked. If provisioning stops, record the exact stage and error. Start with DNS, domain controller path, join account permissions, OU and sync scope; then use [Microsoft's ANC troubleshooting guide](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-azure-network-connection).

Do not reprovision your only working Cloud PC for this test. ANC changes apply only to Cloud PCs provisioned after the change, and reprovisioning is a destructive action (the Cloud PC is rebuilt), according to the [ANC overview](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections).

## Decision checkpoint

Write one sentence explaining why the pilot needs an ANC. If you cannot identify an application, security or routing requirement, proceed with the Microsoft-hosted option. For ANC, require a healthy check, a dedicated pilot policy and a recovery plan (how to move users back to the Microsoft-hosted policy) before changing any production assignment.

Next: [Windows 365 Enterprise: Provision a Microsoft Entra Joined Cloud PC](/windows-365/provision/).

## Sources

- [Windows 365 deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options)
- [Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections)
- [Identity: Microsoft Entra join for Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-deployment-guidance-identity)
