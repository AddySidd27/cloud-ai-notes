# Recheck against Learn's own diagrams, 18 October 2026

Instruction applied: Learn's diagram is the source of truth; no peering or connection decided independently; options shown separately; ambiguities flagged. This is the author's check, not Microsoft verification or endorsement.

| Diagram | Learn picture viewed | Result |
|---|---|---|
| Components (post 1) | components-and-responsibilities.png | Redrawn as Learn's stack; Traffic Manager and Front Door removed (not in picture) |
| Feed discovery (post 2) | feed-discovery-single-azure-region.png and different-geography | Redrawn to the picture; picture versus text difference flagged |
| RDP connection (post 2) | rdp-connection.svg | Redrawn with Region 1 box, Shortpath boxes, dotted two-way links; missing direct UDP line flagged |
| Hybrid (post 2) | Azure Firewall for AVD picture | Original composition, labelled as an example; not copied |
| Connections (post 5) | azure-virtual-desktop-network-connections.svg, both Shortpath pictures | Redrawn with Learn's names and arrowheads; sync direction flagged |
| Hub and spoke (post 5) | Architecture Center hub-spoke, CAF traditional, AVD landing zone, CAF hub-to-hub-er-or-peering.png and multiregion-hub-to-hub-er.png | Five separate panels; D hub-to-hub peering and E hub-to-hub ExpressRoute kept apart; no peering added |
| Topology (post 17) | CAF hub and spoke, CAF Virtual WAN | Redrawn; invented shared services box removed |
| Planes (post 8), Steps (post 10) | components interconnection picture | Control plane and step 9 arrows corrected to two-way and dotted |
| Enforcement (post 16) | Private Link with Shortpath picture | Original composition; not copied |
| Kerberos, Objects, Decision, OS, Three Authentications, Roles | none exist (text or screenshots only) | Original compositions |

Viewed since the table above (18 October 2026, later pass): the lower half of the landing zone picture and the baseline picture; CAF hub-to-hub peering (hub-to-hub-er-or-peering.png), multi-region ExpressRoute hub-to-hub (multiregion-hub-to-hub-er.png) and customer-managed topology pictures; Shortpath scenario 1 to 7 pictures (rdp-shortpath page). Details are in learn-diagram-notes.md. Private Link was viewed once. Not viewed: vnet-multiple-circuits.png and route-server-transitivity.png (not used by any diagram).
Learn's component interconnection picture was viewed but is not redrawn.


## Conflicts between Learn sources (not resolved; designs kept separate)

1. Spoke peering. Cloud Adoption Framework page "Azure Virtual Desktop network topology and connectivity design guidance" (cloud-adoption-framework/scenarios/azure-virtual-desktop/eslz-network-topology-and-connectivity, deprecated, removal date 30 October 2026) says in scenario 1 there is no virtual network peering between AVD spokes and all traffic goes through the hub. The Azure Architecture Center hub-spoke topology picture shows a connection between the two nonproduction spokes, labelled in our panel A as "Peered or directly connected". Panels A, B and C stay separate and none adds a spoke-to-spoke line that its own page does not draw.
2. Shortpath path drawing. rdp-connection.svg (AVD connection page) shows Shortpath as boxes inside Region 1 with no direct client to session host line. The rdp-shortpath page scenarios 4 and 6 and 7 draw direct UDP paths over VPN, STUN and TURN. Both are kept as drawn on their pages; the post diagram follows rdp-connection.svg and the text names the Shortpath page.
3. Scenario 6 on the rdp-shortpath page: the picture has no blocked-path symbols while its alt text says UDP is blocked on the direct VPN and direct public paths. Not redrawn; flagged.
4. Feed discovery: the single-region picture and the page text differ (flagged inside the diagram and its record).
5. Hub-to-hub: CAF shows two options (hubs peered; ExpressRoute only). The AVD landing zone picture draws hubs peered. Now drawn as separate panels D and E in the hub-spoke figure; the CAF options picture draws both peering and ExpressRoute together, so D omits the circuits and says so.
6. Landing zone picture: two hub peering lines land on one AVD VNet frame at the personal and pooled subnet rows. Peering is a virtual network level relationship, but we reproduce the picture and do not decide whether it means one or two networks.
