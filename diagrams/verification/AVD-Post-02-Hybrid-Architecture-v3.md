# Hybrid architecture (post 2, figure 1)

Files: `AVD-Post-02-Hybrid-Architecture-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/hybrid_v3.py`.
Type: Author overview built on documented components

Method and limits: each item was checked against the text of the cited Microsoft Learn pages (fetched October 2026) and, where Learn publishes its diagram as SVG, against that SVG's text labels. Learn's pictures were later viewed in a browser on 18 October 2026, see the recheck section. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Service architecture and resilience](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience)
- [Azure Architecture Center, virtual desktop architecture guidance](https://learn.microsoft.com/en-us/azure/architecture/virtual-desktop/virtual-desktop-get-started)
- [Understanding network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity)
- [Store FSLogix profile containers](https://learn.microsoft.com/en-us/azure/virtual-desktop/store-fslogix-profile)
- [Azure Virtual Desktop Insights](https://learn.microsoft.com/en-us/azure/virtual-desktop/insights)
- [Use Azure Firewall to protect AVD](https://learn.microsoft.com/en-us/azure/firewall/protect-azure-virtual-desktop)

## Explanation
One picture of a hybrid deployment: Microsoft-managed service, Entra ID, user devices, a customer subscription with spoke and hub, profile storage, monitoring, and an on-premises network with Entra Connect and AD DS.

## Verification checklist
- [x] Service components: web, gateway, broker, resource directory, geographical or regional database.
- [x] Session hosts connect outbound to the service (reverse connect).
- [x] Hub gateway reaches on-premises by ExpressRoute or VPN; peering joins spoke and hub.
- [x] FSLogix profile containers on Azure Files or Azure NetApp Files over SMB.
- [x] Monitoring through Azure Monitor and a Log Analytics workspace.
- [x] Entra Connect synchronizes identities to Entra ID.
- [x] No TLS inspection on firewall paths.

## Assumptions and design choices (not Learn requirements)
- The whole customer-side layout (hub, firewall, storage choice, monitoring) is one example.
- Icons are used only where Learn or the icon set has a product icon; AD DS has none and is a plain box.

## Unresolved questions for review
- Whether the identity sync arrow should show the Entra Connect to Entra ID direction only (as drawn) or note password hash sync as an option; not drawn to avoid inventing detail.

## Recheck against Learn's own diagrams, 18 October 2026
Original composition from six pages, not a reproduction of one Learn diagram. Learn's Azure Firewall for AVD picture (host pool VNet, central VNet with firewall, on-premises, internet, AVD service, RD clients) was viewed; it is consistent in spirit and not copied. Hub and spoke peering and the firewall are one example. Entra Connect sync direction follows the author's text; Learn's network connections picture has the sync arrowhead at AD DS, flagged in the Connections record.
