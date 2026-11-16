---
title: "Windows 365 Enterprise: Reading an ANC Health Failure"
seoTitle: "Windows 365: Read an ANC Health Failure"
layout: post.njk
permalink: /windows-365/anc-troubleshooting/
order: 208
part: 9
tags: w365-series
deck: "How to read a failed Azure network connection health check and what to check first."
---

An Azure network connection (ANC) is an object in the Microsoft Intune admin center. It tells Windows 365 which subnet in your own Azure virtual network (VNet) a Cloud PC's network card should join. A Cloud PC is the Windows desktop that Windows 365 runs for a user. An ANC is worth using when an application needs a customer-managed network path. For the join types and network options, see [Choose identity and network](/windows-365/identity-network/#words-to-know).

## What an ANC needs

An ANC test needs these parts:

- **An Azure subscription and a resource group** for the network resources.
- **A VNet and a dedicated subnet** for the Cloud PCs.
- **Outbound access.** A private subnet needs a way out to the internet, for example a NAT gateway (it gives a private subnet outbound access through a public IP address) or a firewall route.
- **The ANC itself,** created with Microsoft Entra join (no Active Directory domain needed) or hybrid join, pointing at that subnet.

Keep your working Cloud PC on its Microsoft-hosted network (a network that Microsoft runs for you) and test the ANC with a separate user and policy. The [identity and network article](/windows-365/identity-network/#anc-path) covers the planning side. This article covers the investigation.

## Reading a failed check

The health check list shows one row per check, each with a status of Passed, Warning or Error. A typical failure is an Error on the **Endpoint connectivity** check. The detail text names the endpoint that Windows 365 could not reach, for example `*.infra.windows365.microsoft.com` on port 443 (the `*` means any name that ends this way). The list also shows when each check ran, and checks can run at different times.

The check tells you which endpoint failed, not why. DNS, a firewall, a proxy, NAT or routing could each be the cause. Do not guess from the endpoint name alone. Write down what you saw, and treat the cause as unknown until you have tested each possibility.

## How to investigate

1. In the Microsoft Intune admin center, go to **Devices > Provision Cloud PCs > Azure network connection** and select the ANC. Select **View details** on the failed check. Copy the exact check name, endpoint and timestamp into a private log.
2. Compare the VNet and subnet, the DNS server setting and the outbound path (the route your network allows to the internet) with the [ANC overview](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections) and the [network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network).
3. Check that the required names resolve. For an Entra join ANC, that means the public Microsoft endpoint names. The Active Directory domain DNS check applies to hybrid join only. Then check that port 443 is open. The [endpoint connectivity checklist](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-azure-network-connection#endpoint-connectivity) says to:
   - use the Azure virtual network troubleshooting tools to confirm the VNet and subnet can reach the listed endpoints;
   - confirm the DNS server can resolve the external names;
   - confirm there is no proxy between the subnet and the internet;
   - confirm no firewall rule (physical, virtual or in Windows) blocks the traffic;
   - test from a VM on the same subnet.

   Also avoid TLS inspection (a firewall that opens encrypted traffic) on any VNet used for an ANC.
4. Change one suspected cause at a time. Then select the ANC and select **Retry**. This needs the Intune Administrator or Windows 365 Administrator role. The full check can take up to 30 minutes, so wait until the status leaves **Running checks**. Save the old and new result with the time and the configuration change.
5. Assign the ANC to a test provisioning policy only when its status is **Checks successful**, or **Checks successful with warnings** after you have read each warning. While the status is **Running checks** or **Checks failed**, the ANC cannot be used. A policy for a pilot test user is described in [the provisioning article](/windows-365/provision/).
6. Before you change a working Cloud PC's assignment, write down how to undo it.

Two facts matter for an idle test ANC. An ANC that is unused for a period becomes **Inactive**, and its health checks pause until it is reactivated. You also cannot delete an ANC that a provisioning policy uses ([Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections)).

Remove temporary resources such as a NAT gateway and public IP address when the test ends, and check your Azure billing. Have a test plan and a cleanup time before you build paid resources.

## What done looks like

A healthy ANC is the first checkpoint, not the last. After it you need a policy that uses it, a newly provisioned test Cloud PC, a successful user session, access to a private application (an internal app that has no public address) and a written cleanup.

Next: [Windows 365 Enterprise: Operate, Roll Out and Extend](/windows-365/operate-and-extend/).

## Sources

- [Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections)
- [Troubleshoot Azure network connections](https://learn.microsoft.com/en-us/troubleshoot/windows-365/troubleshoot-azure-network-connection)
- [Network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network)
