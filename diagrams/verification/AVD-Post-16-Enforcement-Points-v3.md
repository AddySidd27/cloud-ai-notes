# Where the controls sit (post 16)

Files: `AVD-Post-16-Enforcement-Points-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/enforce_v3.py`.
Type: Documented requirements (author layout)

Method and limits: each item was checked against the text of the cited Microsoft Learn pages (fetched October 2026) and, where Learn publishes its diagram as SVG, against that SVG's text labels. Learn's pictures were later viewed in a browser on 18 October 2026, see the recheck section. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Required FQDNs and endpoints for Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/required-fqdn-endpoint)
- [Proxy server guidelines](https://learn.microsoft.com/en-us/azure/virtual-desktop/proxy-server-support)
- [Private Link with Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/private-link-overview)
- [Network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity)

## Explanation
Where firewalls, proxies, NSGs and route tables can interfere, plus the optional Private Link components and the two platform addresses.

## Verification checklist
- [x] Service is reached by name on TCP 443; use FQDNs, FQDN tags or service tags rather than IP lists.
- [x] Private Link: one global endpoint per deployment, one feed endpoint per workspace, one connection endpoint per host pool.
- [x] Private DNS zones privatelink-global.wvd.microsoft.com and privatelink.wvd.microsoft.com.
- [x] 169.254.169.254 (IMDS) and 168.63.129.16 must not be proxied or sent through VPN tunnels; blocking them causes provisioning and health problems (required FQDN page and platform address guidance).

## Assumptions and design choices (not Learn requirements)
- Placement of the NSG, route table and firewall on the host's outbound path is the usual layout, not a Learn diagram.

## Unresolved questions for review
- Confirm the wording of the proxy statement against the current required-FQDN page when published.

## Recheck against Learn's own diagrams, 18 October 2026
Original composition. Learn's Private Link with RDP Shortpath picture (client via public network or VPN, gateway, ICE/STUN, TURN relay, private endpoint, session host) was viewed; this diagram does not reproduce it. It makes no peering or gateway claims beyond the cited pages.
