---
title: "Windows 365 Enterprise: An ANC Health Failure, Step by Step"
layout: post.njk
permalink: /windows-365/anc-troubleshooting/
order: 208
part: 8
tags: w365-series
deck: "A real isolated network test, the observed health error, what remains unknown and how the temporary Azure resources were cleaned up."
---

An Azure network connection is worth testing when an application requires a customer-managed network path. My separate lab reached a useful failure: the ANC object existed, but its health check did not pass. That result tells us more than a polished creation screenshot would, provided we do not invent the fix.

## The test boundary

The test used a Visual Studio Enterprise Azure subscription and `rg-w365-anc-lab`. An isolated East US VNet, `vnet-w365-anc-eastus-lab`, contained the private subnet `snet-cloudpcs`. A temporary NAT gateway and Standard public IP supplied outbound access during the test. The ANC, `anc-w365-entra-eastus-lab`, used Microsoft Entra join and that subnet. The existing working Enterprise Cloud PC stayed on its Microsoft-hosted network and was not moved.

The diagram below shows the intended Entra join ANC path. It is an architecture drawing, not a screenshot of a healthy connection. The [draw.io source](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/architecture/diagrams/source/03-entra-join-azure-network-connection.drawio) is editable.

![Intended Microsoft Entra join ANC network path](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/architecture/diagrams/exported/03-entra-join-azure-network-connection.png)

The October 1, 2026 health result failed a check involving `*.infra.windows365.microsoft.com:443`. That is the endpoint pattern in the observation, not a confirmed diagnosis of DNS, firewall, NAT or routing. A health failure blocks a credible claim of successful ANC provisioning. The [detailed lab record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/docs/live-validation-status.md) keeps the status current.

![Sanitized failed ANC health check](https://raw.githubusercontent.com/AddySidd27/Windows365-enterprise-engineering/main/evidence/UC-03-2026-10-01-anc-health.jpg)

**Reading the result:** the check did not pass. The screenshot identifies an endpoint pattern and port. It does not tell us whether DNS, a route, firewall, proxy or NAT was the root cause. Preserve that uncertainty in a troubleshooting write-up.

## How to investigate this case

1. Open the ANC health detail in Intune and copy the exact check name, endpoint and timestamp into a private lab log.
2. Compare the VNet/subnet, DNS server setting, effective route and outbound path with Microsoft's [ANC overview](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections) and [network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network).
3. Check whether the required name resolves and TCP 443 traffic can follow the approved egress path. Inspect DNS, network security rules, route tables, firewall or proxy policy and NAT association as applicable. Do not infer which one failed solely from the endpoint pattern.
4. Change one suspected cause at a time and run the ANC health **Retry** action. Save both the old and new result with time and configuration change.
5. Only after all relevant checks pass should a separate pilot policy and user test this ANC. Keep a restoration plan before changing a working Cloud PC's assignment.

The investigation steps are a procedure; I did not capture a successful retry. After this attempt, the temporary NAT gateway and public IP were removed, so do not assume paid egress infrastructure remains available. The isolated VNet/subnet and failed ANC record are distinct from the removed resources. Check current Azure resource and billing state before any new test.

| Resource or test | Recorded result |
| --- | --- |
| Entra join ANC | Created; health checks failed |
| Outbound endpoint check | Error observed for the documented infrastructure pattern on TCP 443 |
| Temporary NAT gateway and public IP | Removed after the lab |
| Existing Microsoft-hosted Cloud PC | Kept in place; no network move performed |
| Fresh Cloud PC using this ANC | Not provisioned or validated |

The [October 4 egress retry record](https://github.com/AddySidd27/Windows365-enterprise-engineering/blob/main/evidence/UC-03-2026-10-04-anc-egress-retry.md) gives the precise observations and cleanup. Do not rebuild paid Azure egress just to recreate a screenshot without a test plan and a cleanup time.

## What counts as completion

A healthy ANC is the first checkpoint, not the last. The later checkpoints are a policy that uses it, a newly provisioned test Cloud PC, a successful user session, expected private application access and documented cleanup. Until those results exist, label this as a diagnosed boundary and an open lab, not a working customer-network deployment.

Next: [turn the pilot into an operating service](/windows-365/operate-and-extend/).

### Microsoft Learn

- [Azure network connections](https://learn.microsoft.com/en-us/windows-365/enterprise/azure-network-connections)
- [Network requirements](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network)
