---
title: "Windows 365 Enterprise: Reading an ANC Health Failure"
seoTitle: "Windows 365: Read an ANC Health Failure"
layout: post.njk
permalink: /windows-365/anc-troubleshooting/
order: 208
part: 9
tags: w365-series
deck: "A test of an Azure network connection (ANC) in an isolated network. It shows the health error I saw, what is still unknown, and how I removed the temporary Azure resources. I did not find a fix. The article shows how to investigate."
---

An Azure network connection (ANC) is an object in the Microsoft Intune admin center. It tells Windows 365 which subnet in your own Azure virtual network (VNet) a Cloud PC's network card should join. A Cloud PC is the Windows desktop that Windows 365 runs for a user. An ANC is worth testing when an application needs a customer-managed network path. I tested this separately from my working pilot. I created the ANC, and its health check showed an error. I do not know the cause, so I will not guess. The test ran over two days. The health check was on October 1, 2026, and the retry and cleanup were on October 4. For the join types and network options, see [Choose identity and network](/windows-365/identity-network/#words-to-know).

## My test setup

My lab had these parts:

- **Subscription and resource group:** a Visual Studio Enterprise Azure subscription and `rg-w365-anc-lab`.
- **VNet and subnet:** an isolated East US VNet, `vnet-w365-anc-eastus-lab`, with the private subnet `snet-cloudpcs`.
- **Outbound access:** a temporary NAT gateway (it gives a private subnet a way out to the internet) and a Standard public IP.
- **ANC:** `anc-w365-entra-eastus-lab`, using Microsoft Entra join (no Active Directory domain needed) and that subnet.

My working Enterprise Cloud PC stayed on its Microsoft-hosted network (a network that Microsoft runs for you). I did not move it. The [identity and network article](/windows-365/identity-network/#anc-path) tells the same story from the planning side. This article covers the investigation.

The diagram below shows the intended Entra join ANC path. It is an architecture drawing, not a screenshot of a working connection. Based on [Windows 365 network deployment options](https://learn.microsoft.com/en-us/windows-365/enterprise/windows-365-network-deployment-options). The [draw.io source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/source/03-entra-join-azure-network-connection.drawio) is editable.

![Intended Microsoft Entra join ANC network path](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/architecture/diagrams/exported/03-entra-join-azure-network-connection.png)

The October 1, 2026 health result showed an Error on the **Endpoint connectivity** check. The detail text in my record named `*.infra.windows365.microsoft.com` on port 443 (the `*` means any name that ends this way). That is what the check reported. It does not tell me whether DNS, a firewall, NAT or routing was the cause. A failed health check means this ANC does not work. My [lab status page](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) is kept up to date.

![Sanitized ANC health check list, identifiers removed, October 1, 2026: Endpoint connectivity shows Error, two checks show Warning, seven show Passed](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-03-2026-10-01-anc-health.jpg)

**What the screenshot shows:** it has one **Endpoint connectivity** row with status Error, two Warning rows (**Localization language package readiness** and **UDP connection check**) and seven Passed rows. The rows were checked at different times: the Error and Warnings at 3:52 PM and the Passed rows at 5:20 PM, as the [identity and network article](/windows-365/identity-network/#anc-path) also records. The endpoint pattern and port come from the check's **View details** text, not from the screenshot. Neither tells me whether DNS, a route, a firewall, a proxy or NAT was the root cause. In your own notes, write down what you saw and say the cause is unknown (judgement).

## How to investigate this case

1. In the Microsoft Intune admin center, go to **Devices > Windows 365 (under Provisioning) > Azure network connection** and select the ANC. Select **View details** on the failed check. Copy the exact check name, endpoint and timestamp into a private lab log.
2. Compare the VNet and subnet, the DNS server setting and the outbound path (the route your network allows to the internet) with Microsoft's [ANC overview](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections) and [network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network).
3. Check that the required names resolve. For this Entra join ANC, that means the public Microsoft endpoint names. The Active Directory domain DNS check applies to hybrid join only. Then check that port 443 is open. Learn's [endpoint connectivity checklist](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-azure-network-connection#endpoint-connectivity) says to:
   - use the Azure virtual network troubleshooting tools to confirm the VNet and subnet can reach the listed endpoints;
   - confirm the DNS server can resolve the external names;
   - confirm there is no proxy between the subnet and the internet;
   - confirm no firewall rule (physical, virtual or in Windows) blocks the traffic;
   - test from a VM on the same subnet.

   Learn also says to avoid TLS inspection (a firewall that opens encrypted traffic) on any VNet used for an ANC. Do not guess which one failed from the endpoint pattern alone.
4. Change one suspected cause at a time. Then select the ANC and select **Retry**. This needs the Intune Administrator or Windows 365 Administrator role. The full check can take up to 30 minutes, so wait until the status leaves **Running checks**. Save the old and new result with the time and the configuration change.
5. Assign the ANC to a test provisioning policy only when its status is **Checks successful**, or **Checks successful with warnings** after you have read each warning. While the status is **Running checks** or **Checks failed**, the ANC cannot be used. A policy for a pilot test user is described in [the provisioning article](/windows-365/provision/).
6. Before you change a working Cloud PC's assignment, write down how to undo it.

These steps are a suggested method. I did not complete them, and I never got a healthy result. After the October 4 retry, I removed the temporary NAT gateway and public IP. I kept the VNet, the subnet and the failed ANC. Check your Azure resources and billing before any new test.

Two facts from Learn matter for an idle lab ANC. An ANC that is unused for a period becomes **Inactive**, and its health checks pause until it is reactivated. You also cannot delete an ANC that a provisioning policy uses ([Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections)).

| Resource or test | Result |
| --- | --- |
| Entra join ANC | Created; status Checks failed (Endpoint connectivity Error, 2 Warnings, 7 Passed; see the [identity and network article](/windows-365/identity-network/#anc-path)) |
| Outbound endpoint check | Error on the required endpoint `*.infra.windows365.microsoft.com`, TCP port 443 |
| Temporary NAT gateway and public IP | Removed after the lab |
| Existing Microsoft-hosted Cloud PC | Kept in place; I did not move it |
| Fresh Cloud PC using this ANC | Not tested yet |

My [October 4 retry record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-03-2026-10-04-anc-egress-retry.md) has the retry notes and the cleanup. This article reports only the October 1 result. Do not rebuild a paid NAT gateway and public IP just to retake a screenshot. Have a test plan and a cleanup time first (judgement).

## What done looks like

A healthy ANC is the first checkpoint, not the last (judgement). After it you need a policy that uses it, a newly provisioned test Cloud PC, a successful user session, access to a private application (an internal app that has no public address) and a written cleanup. I have none of these yet. My ANC failed its health check and I have not tested it further.

Next: [turn the pilot into an operating service](/windows-365/operate-and-extend/).

### Microsoft Learn

- [Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections)
- [Azure network connection health checks](https://learn.microsoft.com/en-us/windows-365/enterprise/health-checks)
- [Troubleshoot Azure network connections](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-azure-network-connection)
- [Network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network)
