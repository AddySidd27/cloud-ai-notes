# Hub and spoke layouts (post 5)

Files: `AVD-Post-05-Hub-Spoke-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/hub_v3.py`.
Type: Five separate Learn layouts (A to C layouts, D and E hub-to-hub options)

Method and limits: Redrawn on 18 October 2026 from Learn's own picture, viewed in a browser, with the Learn text fetched the same day. Names, links and arrowheads follow the picture. Observations of Learn's pictures are in `learn-diagram-notes.md`. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Hub-spoke network topology in Azure](https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke), hub-spoke-network-topology-architecture.svg
- [Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology), hub-and-spoke-topology.png
- [AVD landing zone design guide](https://learn.microsoft.com/en-us/azure/architecture/landing-zones/azure-virtual-desktop/design-guide), virtual-desktop-accelerator-enterprise-landing-zone.svg
- Panels D and E, same page as B ([Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology)): D from hub-to-hub-er-or-peering.png (peering link only) and the text "When you need to connect two Azure regions, use global virtual network peering to connect the hub virtual networks in each region"; E from multiregion-hub-to-hub-er.png and the text on connecting hubs to the same ExpressRoute circuits for more than two regions, including the BGP and firewall-bypass note.
- [AVD network topology and connectivity](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/azure-virtual-desktop/eslz-network-topology-and-connectivity) (deprecated, removal 2026-10-30; not drawn)

## Explanation
Five panels, so the supported layouts are shown side by side and not merged. D and E are the two hub-to-hub options Learn gives; they are not combined.

## Verification checklist (rechecked 18 October 2026 against Learn's own diagrams)
- [x] Panel A: Bastion, Firewall, VPN Gateway in hub; Monitor diagnostics; 2 production and 2 nonproduction spokes two-way to hub; forced tunnel lines from production spokes to firewall; peered or directly connected link between the two nonproduction spokes; no link between production spokes.
- [x] Panel B: three spokes each peered to the hub; hub holds gateway and firewall; no spoke-to-spoke line.
- [x] Panel C: Hub region 1 and region N peered; identity VNets peered to their hubs; one AVD VNet peered to both hubs; no spoke-to-spoke line.
- [x] Panel D: two regions, three peered spokes per hub, hubs joined by two-way virtual network peering, gateway and firewall icons in each hub. The options picture also draws ExpressRoute circuits to a customer network; they are deliberately omitted from D (disclosed in the figure).
- [x] Panel E: three regions, three peered spokes per hub, no hub-to-hub peering, seven ExpressRoute links as drawn (Region 1 to circuits 1 and 2; Region 2 to circuits 1, 2 and 3; Region 3 to circuits 2 and 3), customer network bar, inbound text (connection weight or AS path prepending) and outbound text (local preference).
- [x] No peering was added or removed by the author.

## Assumptions and design choices (not Learn requirements)
- The earlier example address plan (10.40.0.0/21) was removed from the figure; it remains the author's text example in post 5.

## Unresolved questions for review
- Learn pages differ on spoke peering (panel A shows peered nonproduction spokes; the deprecated AVD page says AVD spokes are not peered). Both are shown as Learn presents them.
- Panel B ExpressRoute icon is unlabelled in Learn; not named beyond that. The same applies to the triangle icons in E.
- Learn's options picture (D source) draws peering and ExpressRoute together while its text and the multiregion picture treat them as options. D omits the circuits and says so; whether to read that picture as one combined design is left to the reader of the Learn page.
- In E the pairing of hubs to circuits was read from the picture at high zoom; the page text does not describe the pairing.
- Direction arrows on the inbound and outbound path text are drawn as text labels, not arrows.
- The Learn landing zone picture is large; only the connectivity and AVD landing zone regions were read closely.
