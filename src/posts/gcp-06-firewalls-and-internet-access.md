---
title: "Google Cloud Firewalls and Internet Access"
layout: post.njk
permalink: /google-cloud/firewalls-and-internet-access/
order: 406
part: 6
tags: gcp-lz
deck: "Read a firewall rule, know which rule wins, and choose how VMs reach the internet and Google services without opening them to the world."
---

This article is for people who build or review the network of a Google Cloud landing zone. After reading it you can read a firewall rule, say which rule wins when two VPC firewall rules disagree, say where organization-wide rules live, and describe how the Google Cloud enterprise foundations blueprint gives apps and VMs outbound access, inbound access and access to Google services. The blueprint is a design for a Google Cloud foundation. It covers VPC networks, firewall policies and other networking resources (the terms are defined in Key terms below). A landing zone is explained in [What Is a Google Cloud Landing Zone](/google-cloud/what-is-a-google-cloud-landing-zone/).

The network itself (VPC networks, subnets and Shared VPC) is covered in [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/). Organization policy guardrails are in [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/). Who may create and change firewall rules in a Shared VPC setup is covered in the Shared VPC article and in [Compute Engine in a Landing Zone](/google-cloud/compute-engine-in-a-landing-zone/).

## Key terms

| Term | Meaning |
|---|---|
| VM, instance | A virtual machine in Google Cloud. This article says VM. |
| VPC network | A virtual network in Google Cloud. Every VPC network works as a distributed firewall: rules are defined for the network, but connections are allowed or denied for each instance. |
| VPC firewall rule | A rule that allows or denies connections to or from VMs in a VPC network. Enabled rules are always enforced, even if the instance has not started up. The blueprint calls these legacy VPC firewall rules. |
| Hierarchical firewall policy | A firewall policy enforced at the organization or folder level. The blueprint uses it for rules that apply across all environments. |
| Network firewall policy | A firewall policy for a VPC network. It can be global or regional. The blueprint gives each VPC network its own global network firewall policy. |
| Firewall policy | A firewall policy has rules. The kinds are hierarchical, regional system, global network and regional network firewall policies. Regional system firewall policies are evaluated right after hierarchical firewall policies, before VPC firewall rules. |
| Target | The instances a rule applies to. For a VPC firewall rule the default is all instances in the VPC network. You can also use a network tag or a service account. |
| Ingress, egress | Ingress is incoming traffic: packets entering a target. Egress is outgoing traffic: packets leaving a target. A VPC firewall rule applies to one of them, not both. |
| Priority | A whole number on a rule. For VPC firewall rules it is 0 to 65535 and the default is 1000. A lower number means a higher priority and is checked first. |
| Action | What a rule does: allow or deny. A VPC firewall rule has one action. |
| Service account | An identity associated with an instance. |
| Network tag | An arbitrary attribute added to an instance. Anyone who has permission to edit the instance can change its tags. |
| Firewall endpoint | Where a firewall policy rule can send traffic. A security profile there decides whether the packet is allowed or dropped. |
| Tag (with IAM controls) | A tag that is added to VM instances and that traffic is evaluated against. It has IAM controls, so you can define it centrally and delegate its use to other teams. The blueprint uses these and does not recommend legacy network tags. |
| Stateful | If a connection is allowed in one direction, the matching return traffic is allowed too. |
| Implied action | What Google Cloud does when no rule applies. It depends on the traffic direction and the target type. |
| Go to next | A firewall policy action. In a hierarchical firewall policy, evaluation continues with the hierarchical policy of a folder ancestor closer to the target, if there is one, and otherwise with the next step in the order. |
| 0.0.0.0/0 | The range that means any IPv4 address. |
| RFC 1918 ranges | The ranges 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16, as the blueprint table below lists them. |
| Cloud NAT | The service the blueprint recommends for outbound traffic from workloads to the internet, so that there are no unsolicited inbound connections. |
| Secure Web Proxy | A service the blueprint offers for more granular control: outbound traffic only to trusted web services. |
| Cloud Load Balancing, Google Cloud Armor | The blueprint recommends designing workloads with load balancing and Google Cloud Armor for inbound traffic from the internet. |
| Private Service Connect endpoint | An internal endpoint that the blueprint creates in each network to communicate with Google Cloud APIs. |
| Private Google Access | A feature the blueprint turns on in every subnet. Together with Private Service Connect endpoints, firewall policies and DNS records, it allows a private path to Google Cloud services. |
| vpc-sc API bundle | The API bundle the blueprint uses for the endpoint. It allows access to the Google Cloud services that the restricted VIP supports, and helps reduce exfiltration risk (data leaving your environment to places it should not go) by preventing access to Google APIs that are not related to Google Cloud. |

## One picture

![Left: two example network firewall policy rules and the default check order. Right: Cloud NAT outbound, Cloud Load Balancing inbound, direct VM internet access not recommended, Private Service Connect with Private Google Access, hierarchical rules.](/img/google-cloud/google-cloud-firewalls-and-internet-access.svg)

*Source: [VPC firewall rules](https://docs.cloud.google.com/firewall/docs/firewalls), [Networking (enterprise foundations blueprint)](https://docs.cloud.google.com/architecture/blueprints/security-foundations/networking) and [Evaluation order for firewall policies and rules](https://docs.cloud.google.com/firewall/docs/firewall-policies-rule-eval-order).*

## What a firewall rule is made of

The blueprint calls VPC firewall rules legacy and recommends using only firewall policies and avoiding mixing them with legacy VPC firewall rules. VPC firewall rules are still evaluated along with firewall policies, so this section explains them.

A VPC firewall rule is defined for a network, but the connection is allowed or denied for each instance. Each rule has these parts:

| Part | What to know |
|---|---|
| Direction | Ingress or egress. If you give none, ingress is used. |
| Priority | 0 to 65535. The default is 1000. Several VPC firewall rules can share a priority. Rules in a firewall policy must each have a unique priority. |
| Action | Allow or deny. Only one per rule. |
| Enforcement | Enabled or disabled. A rule with no enforcement state set is automatically enabled. A disabled rule stays in place without being deleted. |
| Target | All instances in the network by default, or instances picked by network tag or service account. |
| Source (ingress) or destination (egress) | The default is any IPv4 address, 0.0.0.0/0. The default does not include IPv6 sources. One rule cannot mix IPv4 and IPv6 ranges. |
| Protocols and ports | For example tcp, udp, icmp. A port cannot be given on its own. Rules based on source ports are not supported. |
| Logging | An option that logs the connections that match the rule. |

A rule can target network tags or service accounts, but you cannot mix both in one rule. You can work with VPC firewall rules in the Google Cloud console, the gcloud CLI or the REST API.

## Which VPC firewall rule wins

For VPC firewall rules, the highest-priority rule that applies to a target for a type of traffic takes precedence. A lower number means a higher priority, so the lower number wins. It does not matter how specific the target is. A deny rule beats an allow rule only when both have the same priority. An allow rule with a higher priority can override a deny rule.

A worked example with two ingress rules: one denies all traffic from 0.0.0.0/0 at priority 1000, and one allows TCP port 80 from 0.0.0.0/0 to instances with the network tag webserver. If the allow rule has a number below 1000, TCP port 80 is allowed to the webserver instances. At 1000 or above, the deny rule applies.

Rules are stateful. When a connection is allowed, the return traffic is allowed too, and you cannot set a rule to deny the responses. When you change a rule, the change applies only to new connections. Existing connections continue.

In a firewall policy the check works differently. Rules are checked from highest to lowest priority and the first rule that applies to the target and matches the traffic is used. At most one rule matches in each policy.

### The example in the picture (a network firewall policy)

The blueprint shows two rules in a network firewall policy. They use tags that have IAM controls, not legacy network tags. Rule 1 is an egress rule. It denies outbound traffic from all sources at priority 65530. Rule 2 is an ingress rule. It allows traffic from instances tagged service=frontend to instances tagged service=backend at priority 999.

The traffic from instance-1 to instance-2 matches the tags that Rule 2 allows, so instance-2 can receive it. instance-3 does not receive the traffic from instance-1. The only rule in the policy that matches that traffic is Rule 1, which denies outbound traffic from all sources. Rule 2 is matched before Rule 1 is evaluated, based on the priority value.

## When no rule applies: the implied action

If nothing applies, Google Cloud uses an implied action. The implied action depends on the direction and the target.

| Traffic | Implied action |
|---|---|
| Ingress to a VM | Deny |
| Egress | Allow |

This is why, with only the defaults, a new VM with no allow rule does not receive incoming connections, but can still send traffic out unless a deny rule stops it. The blueprint adds a rule that denies egress to all other IP addresses, as described below.

### The default network

The default network starts with four ingress rules, all at priority 65534. They can be deleted or changed. Priority 65534 is a high number, so any rule you add with a lower number is checked first.

| Rule | Source | Allows |
|---|---|---|
| default-allow-internal | 10.128.0.0/9 | TCP, UDP and ICMP |
| default-allow-ssh | 0.0.0.0/0 | TCP port 22 |
| default-allow-rdp | 0.0.0.0/0 | TCP port 3389 |
| default-allow-icmp | 0.0.0.0/0 | icmp |

### Traffic that rules do not control

For VM instances, VPC firewall rules and hierarchical firewall policies do not apply to packets to and from the metadata server, or to packets that stay inside the VM. The metadata server is a local server that Google Cloud runs alongside each instance. It is at 169.254.169.254 (IPv4) and fd20:ce::254 (IPv6). It provides DHCP, DNS resolution, instance metadata and NTP.

### Traffic that is blocked by default

To help prevent spam, Google Cloud blocks egress packets sent to TCP destination port 25 (SMTP) of an external IP address by default. SMTP over TLS on port 465 or 587 is not part of that block. Google Cloud removes this block automatically when it determines that a project is low risk.

## Evaluation order

Hierarchical firewall policies are enforced at the organization or folder level. VPC firewall rules are evaluated together with firewall policies. This is the default order:

1. Hierarchical firewall policies. The organization policy first, then folders from the top down to the folder of the target's project.
2. Regional system firewall policies, evaluated right after hierarchical firewall policies.
3. VPC firewall rules.
4. Global network firewall policy.
5. Regional network firewall policies for the target's region and VPC.
6. The implied action.

Within a policy, Google Cloud ignores rules whose target or direction does not match, then checks the rest from highest to lowest priority and stops at the first match. A policy rule can allow, deny, go to next or, in hierarchical and global policies, send the traffic to a firewall endpoint, where a security profile decides whether the packet is allowed or dropped. Go to next continues with the hierarchical policy of a folder ancestor closer to the target, if there is one, and otherwise with the next step in the order. If no rule in a policy matches, go to next is applied. VPC firewall rules can only allow or deny. If two VPC firewall rules match, they have the same priority but different actions, and the deny rule is enforced.

The order is a setting of each VPC network. The setting is named networkFirewallPolicyEnforcementOrder. Its default value is AFTER_CLASSIC_FIREWALL, which gives the list above. The other value, BEFORE_CLASSIC_FIREWALL, puts the global and regional network firewall policies before the VPC firewall rules (steps 3, 4 and 5 become global network policies, regional network policies, then VPC firewall rules). You can change it with the gcloud compute networks update command and its --network-firewall-policy-enforcement-order flag.

## How the blueprint uses policies

The blueprint adds its own rule that denies egress to all other IP addresses, so its networks behave differently from the default described above. It uses one hierarchical firewall policy, applied to the production, non-production, development, bootstrap and common folders. Its rules are:

| Direction | Traffic | Action | Purpose |
|---|---|---|---|
| Ingress | 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12 (RFC 1918), all protocols | Go to next | Delegates the evaluation of inbound traffic from RFC 1918 to lower levels in the hierarchy |
| Egress | The same three ranges, all protocols | Go to next | Delegates the evaluation of outbound traffic to RFC 1918 to lower levels in the hierarchy |
| Ingress | 35.235.240.0/20, TCP ports 22 and 3389 | Allow | IAP for TCP forwarding (IAP is explained in [the article on reaching a VM](/google-cloud/reaching-a-vm-os-login-and-iap/)) |
| Egress | 35.190.247.13/32, TCP port 1688 | Allow | Windows server activation |
| Ingress | 130.211.0.0/22, 35.191.0.0/16, 209.85.152.0/22, 209.85.204.0/22, TCP ports 80 and 443 | Allow | Health checks for Cloud Load Balancing |

Each VPC network then gets its own global network firewall policy. It starts with a minimum set of rules that allow access to Google Cloud services: egress to the network's Private Service Connect endpoint on TCP port 443. The policy also denies egress to all other IP addresses. In the hub-and-spoke design, the policy also has a rule that allows outbound traffic from one spoke to another spoke (hub-and-spoke is explained in [Network Design with Shared VPC](/google-cloud/network-design-with-shared-vpc/)). The blueprint does not use legacy VPC firewall rules and recommends using only firewall policies. It uses tags with IAM controls, which can be defined centrally and delegated to other teams, and it does not recommend legacy network tags.

When you first deploy the blueprint, a VM in a VPC network can communicate with Google Cloud services, but not with other resources in the same VPC network. To allow that, you add rules to the network firewall policy, and use tags with IAM controls, that explicitly allow the VMs to communicate.

## Internet access

The blueprint does not allow inbound or outbound traffic between its VPC networks and the internet. For workloads that need it, it recommends the options below. Firewall rules are not the only control; see [Google Cloud Guardrails: Organization Policies and Security Decisions](/google-cloud/organization-policies-and-guardrails/) for the guardrails.

| Need | Recommended |
|---|---|
| Outbound to the internet | Cloud NAT, to allow outbound traffic without unsolicited inbound connections. For more granular control that allows outbound traffic to trusted web services only, Secure Web Proxy. |
| Inbound from the internet | Cloud Load Balancing with Google Cloud Armor. |
| Direct internet access to a VM | Not recommended. The blueprint does not recommend workloads that allow direct connectivity between the internet and a VM through an external IP address on the VM. |

### Reaching Google services

To let resources reach Google Cloud services, the blueprint recommends private connectivity instead of outbound internet traffic to public API endpoints. It configures Private Google Access on every subnet, creates internal endpoints with Private Service Connect to communicate with Google Cloud services, and configures firewall policies and DNS records to allow traffic to those endpoints. Used together, these controls allow a private path to Google Cloud services, without relying on internet outbound traffic or publicly advertised internet ranges.

Each network has an endpoint that uses the vpc-sc API bundle. DNS zones for googleapis.com, gcr.io and pkg.dev in each network map those names to the endpoint. The firewall policy allows TCP port 443 to the endpoint and denies other egress. The bundle allows access to the Google Cloud services supported by the restricted VIP, and helps mitigate exfiltration risk (data leaving your environment to places it should not go) by preventing access to other Google APIs not related to Google Cloud.

## Common mistakes

- Thinking the most specific VPC firewall rule wins. Only priority decides.
- Expecting a deny to beat an allow in VPC firewall rules. It does only at equal priority.
- Not knowing that the default network has default-allow-ssh and default-allow-rdp. They allow TCP ports 22 and 3389 from any IPv4 address (0.0.0.0/0), and they can be deleted or modified.
- Relying on network tags for control. Anyone who has permission to edit an instance can change its tags. Tags with IAM controls can be managed centrally.
- Mixing network tags and service accounts in one rule.
- Expecting a rule change to cut a connection that is already open.
- Mixing VPC firewall rules with firewall policies. The blueprint recommends using only firewall policies.
- Giving VMs direct internet connectivity instead of using Cloud NAT and load balancing.

## How to check this in your own project

1. List the VPC firewall rules of each network. You can use the Google Cloud console or the gcloud CLI. Listing needs the compute.firewalls.list permission, which the Compute Network Viewer role has. For each rule write down direction, priority, action, target and source or destination.
2. Check whether the default network rules exist and whether any rule allows TCP port 22 or 3389 from 0.0.0.0/0.
3. List the firewall policies on your organization and folders, and the network firewall policies on each network. For each VPC network, check its networkFirewallPolicyEnforcementOrder setting.
4. For a VM that must send traffic out, remember that egress is allowed unless a rule denies it. Look for a deny rule, such as a network firewall policy rule that denies egress to all other IP addresses, and for any allow rule with a higher priority that overrides it.
5. For each workload that talks to the internet, write down whether it goes through Cloud NAT, Cloud Load Balancing or has direct connectivity. Anything with direct connectivity needs a reason.
6. Check that Private Google Access is on for each subnet, as the blueprint configures it.
7. Turn on logging for rules you need to audit. Logging records the connections that match the rule.

## Sources

- [VPC firewall rules](https://docs.cloud.google.com/firewall/docs/firewalls)
- [Networking (enterprise foundations blueprint)](https://docs.cloud.google.com/architecture/blueprints/security-foundations/networking)
- [Evaluation order for firewall policies and rules](https://docs.cloud.google.com/firewall/docs/firewall-policies-rule-eval-order)
