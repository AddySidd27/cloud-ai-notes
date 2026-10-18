# Hub and spoke compared with Virtual WAN (post 17)

Files: `AVD-Post-17-Topology-Choice-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/topo_v3.py`.
Type: Two Learn pictures plus criteria

Method and limits: Redrawn on 18 October 2026 from Learn's own picture, viewed in a browser, with the Learn text fetched the same day. Names, links and arrowheads follow the picture. Observations of Learn's pictures are in `learn-diagram-notes.md`. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Traditional Azure networking topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/traditional-azure-networking-topology)
- [Virtual WAN network topology in an Azure landing zone](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/virtual-wan-network-topology), virtual-wan-topology.svg
- [Define an Azure network topology](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/define-an-azure-network-topology) (criteria boxes)

## Explanation
The two topologies as Learn draws them, with Learn's criteria for choosing.

## Verification checklist (rechecked 18 October 2026 against Learn's own diagrams)
- [x] Left panel matches the CAF hub-and-spoke picture.
- [x] Right panel: two virtual hubs with Azure Firewall and VPN/ExpressRoute gateways, VWAN band, DNS spoke with DNS Private Resolver per region, VWAN hub connection to a workload network per region, ExpressRoute circuits.
- [x] Removed the earlier 'shared services spoke with DNS servers' box, which is not in Learn's picture.
- [x] Criteria boxes follow the CAF text (checked earlier).

## Assumptions and design choices (not Learn requirements)
- Workload network stands in for the AVD spoke.

## Unresolved questions for review
- Link between the two virtual hubs is shown only as the VWAN band, as in the picture.
- Learn's Virtual WAN picture was read for the connectivity subscription and the first hub connections; the lower workload details were not read in full.
