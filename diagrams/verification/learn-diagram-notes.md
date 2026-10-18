# Learn diagram observations (viewed in browser pane, 2026-10-18)

## architecture/networking/architecture/hub-spoke  (_images/hub-spoke-network-topology-architecture.svg)
- Outer frame: Azure Virtual Network Manager.
- Hub VNet: Azure Bastion, Azure Firewall, VPN Gateway. Azure Monitor beside hub: dashed grey "Diagnostics" arrows from Bastion, Firewall, VPN Gateway to Monitor.
- Cross-premises network (2 VMs + gateway) <-> VPN Gateway (dotted double arrow). Vertical lines from hub to left.
- 2 Production spoke VNets (resource subnet with 3 VMs each): hub <-> each, double arrows "Virtual networks connected or peered through hub". Green dashed "Forced tunnel" from each production spoke to Azure Firewall.
- 2 Nonproduction spoke VNets: hub <-> each ("Connected virtual networks", double arrows). Between the 2 nonproduction spokes: double arrow "Peered or directly connected virtual networks".
- Production spokes: no spoke-to-spoke link drawn.

## virtual-desktop/network-connectivity  (media/azure-virtual-desktop-network-connections.svg)
- Components: Client, Session Host, Active Directory Domain Services, Public Internet cloud, box "Azure Virtual Desktop Infrastructure" holding RD Web, RD Gateway, RD Broker, Azure AD (outside, bottom).
- Reverse Connect Transport (TCP 443, thick blue): client side line from Internet to client (arrowhead at client) and Internet -> RD Gateway (arrow into gateway); RD Gateway -> Session Host (arrow into VM, labeled RDP data (TLS) / Reverse Connect Transport TCP 443).
- Feed subscription (TCP 443, red): client -> Internet -> RD Web (arrow into RD Web).
- Azure AD Authentication (TCP 443, purple): client -> Azure AD. Session host auth NOT drawn.
- RD Agent communication (TCP 443, green): Session Host -> RD Broker (arrow into broker).
- Internal service traffic (yellow dotted): RD Gateway <-> RD Broker bidirectional; dotted arrowheads into RD Web.
- AD connectivity (green dashed): Session Host -> AD DS (arrow into AD DS), label "Active Directory connectivity".
- Azure AD Connect sync (TCP 443, light green dashed): arrowhead at AD DS end (Learn drawing). Text of other pages: Entra Connect syncs AD DS -> Entra. Ambiguous: flag.
- Legend also has "Local Active Directory connectivity (various)" (grey dotted), not drawn.

## feed-discovery-different-geography.png (service-architecture-resilience) viewed 18 Oct 2026
- Region 1 box: Client <-> Web service <-> Resource directory (both arrows bidirectional).
- Client <-> Azure Traffic Manager: dashed, bidirectional, outside Region 1 box.
- Region 2 box: Resource directory has one blue line splitting into two arrowheads down to Geographical broker (in Geographical deployment scope) and Regional broker (in Regional deployment scope).
- Each broker <-> its own database (Geographical database, Regional database), bidirectional.
- No arrow from client to broker, no feed to session host drawn.

## rdp-connection.svg (service-architecture-resilience; path /azure/virtual-desktop/media/service-architecture-resilience/rdp-connection.svg) viewed 18 Oct 2026
- Left: Client <-> Azure Front Door (solid black, bidirectional).
- Front Door <-> Gateway service (black, TCP label, bidirectional) in Region 1 box.
- Gateway service <-> Broker service (dotted, bidirectional). Broker service <-> Session host (dotted, bidirectional).
- Gateway service <-> Session host: black TCP arrow bidirectional (over the top).
- Purple UDP: Client -> to a line running right; branches to "RDP Shortpath (managed networks)" icon box, to "RDP Shortpath (public networks)" icon, and arrow down to Session host. Session host UDP <-> both Shortpath icons (purple, arrowheads at managed-network icon and public-network icon).
- Shortpath boxes are drawn INSIDE the Region 1 box. No Entra, no web service, no TURN/STUN drawn.
- Text on the page says Front Door picks lowest-latency gateway; step list says Shortpath bypasses gateway.
- AMBIGUITY: the picture draws the client UDP line toward the Shortpath icons and also to the session host; it does not draw a direct client-host line labelled as such.

## rdp-shortpath-managed-networks.png (rdp-shortpath page) viewed 18 Oct 2026
- Title "RDP Shortpath Network Connections". Legend: reverse connect (TCP 443), feed subscription (TCP 443), Entra auth (TCP 443), RD Agent communication (TCP 443), RDP Shortpath (UDP 3390) dotted navy, internal service traffic, Entra Connect Sync (TCP 443) dashed green, local AD connectivity (various).
- Client (VPN/ER icon) -> Shortpath UDP 3390 dashed line directly to Session Host (client to session host, arrowhead at session host). Session host -> AD DS "Active Directory connectivity" dashed green arrowhead at AD DS (session host is domain joined in this diagram).
- Reverse connect thick blue: client via Public Internet to RD Gateway; session host to RD Gateway. Feed subscription red: Public Internet to RD Web. Entra auth purple: client to Entra ID. RD Agent comm green: session host to RD Broker. RD Gateway, RD Web, RD Broker triangle of yellow dotted internal traffic inside "Azure Virtual Desktop Infrastructure" box. Entra Connect sync dashed green from Entra ID to AD DS (arrowhead at AD DS).

## rdp-shortpath-public-networks.svg viewed 18 Oct 2026
- Title "RDP Shortpath for public networks - network connections". Boxes: Client, Session host/Cloud PC, Microsoft Entra ID authentication (top, purple lines from client and from session host both to Entra), STUN access / TURN relay (UDP 3478) below between client and session host with bidirectional arrows to each, direct dotted RDP Shortpath (UDP 49152-65535) client <-> session host.
- Public internet cloud: client reverse connect to Gateway service (thick blue); feed subscription red to Web service; session host reverse connect to Gateway service; RD Data (TLS) dashed between session host and gateway. Session host RD Agent communication green to Broker service.
- "Microsoft-managed service infrastructure" box holds Web service, Gateway service, Broker service with yellow dotted internal traffic.
- Note this one shows session host authenticating to Entra ID too (purple line); managed-network version shows session host to AD DS.

## AVD landing zone design guide: virtual-desktop-accelerator-enterprise-landing-zone.svg (architecture/landing-zones/azure-virtual-desktop/design-guide) viewed 18 Oct 2026
- Connectivity subscription holds Hub virtual network region 1 and Hub virtual network region N. Each hub shows Azure DNS Private Resolver, VPN/ExpressRoute gateways, Azure Firewall (plus DDoS Protection, Azure DNS, ExpressRoute circuits, Firewall policies listed on left).
- "Virtual network peering" drawn between Hub region 1 and Hub region N.
- Identity subscription: Virtual network region 1 and region N (domain controllers / Entra Domain Services shown as OR); each peered ("Virtual network peering") to its hub.
- Virtual Desktop landing zone subscription: one "Virtual Desktop virtual network" with a personal subnet and a pooled subnet; TWO peering lines (hub region 1 and hub region N) go to this one VNet.
- Management plane box: Workspace, application groups, host pools (personal, pooled), Start VM on connect, scaling plan; storage (FSLogix, MSIX app attach), Key Vault in landing zone.
- Sandbox subscription separate. This is an enterprise-scale landing-zone example, a reference architecture for landing zone implementations, not a generic requirement.
- No spoke-to-spoke peering drawn between AVD and Identity VNets in the portion viewed.

## CAF traditional-azure-networking-topology: hub-and-spoke-topology.png viewed 18 Oct 2026
- Three spoke VNets (user icon boxes) at top, labelled band "Virtual network peering": one vertical line from EACH spoke down to the hub VNet. Hub box (Region 1) contains a gateway icon and an Azure Firewall icon. A line from the hub goes down to an on-premises/ExpressRoute-style triangle icon. No lines between spokes.
- Other images on that page NOT yet viewed: customer-managed-topology.svg, vnet-multiple-circuits.png, route-server-transitivity.png, hub-to-hub-er-or-peering.png, multiregion-hub-to-hub-er.png.

## components-and-responsibilities.png viewed 18 Oct 2026
- Stack of 8 boxes. Dark teal (Microsoft-managed brace): Web service, Broker service, Gateway service, Resource directory, Geographical database, Regional database. Light blue (Customer-managed brace): Session hosts, User identities. No arrows, no Traffic Manager or Front Door. Page text (not picture) lists session-host and identity responsibilities and says TM and Front Door direct users to entry points.

## feed-discovery-single-azure-region.png viewed 18 Oct 2026
- Region 1 dashed box: Client <-> Web service <-> Resource directory (bidirectional). Client <-> Azure Traffic Manager dashed vertical, bidirectional. Below, two dashed boxes "Geographical deployment scope" and "Regional deployment scope" (NOT labelled with a region), each with its broker <-> database. Resource directory has one blue line splitting down to both brokers. Different-geography version is the same but second box labelled Region 2.
- PAGE TEXT vs PICTURE: text step 2 says the web service connects to the broker service which connects to resource directory and database. Picture draws web service <-> resource directory and resource directory -> brokers. FLAG: do not resolve.

## microsoft-managed-components-interconnection.png viewed 18 Oct 2026 (top half and middle)
- Two regional boxes (Region 1 top, second region mirrored below). Per region: Web service, Broker service, Gateway service, Session host, Geographical database "or" Regional database, Resource directory, RDP Shortpath (managed networks) and (public networks) icons in Region 1.
- Broker service <-> Web service (solid), Broker <-> Gateway service (dotted, bidirectional), Broker <-> Session host (dotted), Broker <-> database (solid bidirectional), Broker -> Resource directory (solid arrow).
- Client <-> Web service (solid black, left side); Client <-> Azure Front Door -> TCP line to Gateway service; Client <-> Traffic Manager dotted. Session host <-> Gateway service TCP (black). Purple UDP to Shortpath and session host.
- Green vertical lines between the two regions' geographical databases: "SQL region replication (where applicable)" and "SQL geo-replication".
- Here broker connects to resource directory, consistent with page text and unlike the feed-discovery pictures. FLAG as a Learn internal difference.

## Landing zone enterprise picture, lower half and right (viewed 18 Oct 2026, second pass)
- Virtual Desktop landing zone subscription: management plane (workspace, app groups, personal and pooled host pools, Start VM on connect, scaling plan with schedules), "Virtual Desktop virtual network" frame (grey) containing "Virtual Desktop subnet" with personal session host VMs, "Virtual Desktop subnet" with pooled session host VMs, "Private endpoints subnet", DDoS protection icon. Two Virtual network peering lines (one from hub region 1, one from hub region N) end on the left edge of this VNet frame, at the personal subnet row and the pooled subnet row. Reading: one VNet peered to both hubs. The picture does not say whether the two lines mean one VNet or one per subnet row (subnets are not peered; peering is VNet level). FLAG, not resolved here.
- Storage: MSIX app attach and FSLogix file shares in storage accounts, Key Vault (and Key Vault Zero Trust), dashed yellow link from the VNet to the storage boxes.
- Image template box; Virtual Desktop shared services subscription (Azure VM Image Builder, Automation account, Azure Compute Gallery, VM image definition), dashed link to image template.
- Sandbox subscription (Applications). Compliant VM templates box (VM SKU, access credentials, in-guest policies/DSC, backup policy, extensions, tagging).

## Landing zone baseline picture virtual-desktop-accelerator-baseline.svg (same design-guide page) viewed 18 Oct 2026
- Single region ("Region A"): Customer network box (AD DS server, "Microsoft Entra Connect/Cloud sync" server, Gateway), Internet, Non-corporate network; ExpressRoute circuit and Site-to-site VPN box.
- Connectivity subscription (Region A): hub VNet with Gateway, Azure Firewall/NVA, "DNS subnet" with Custom DNS server 1 and 2, DDoS Protection. Identity subscription (AD DS) and Management subscription at left. Virtual Desktop landing zone subscription with management plane and VNet, shared services landing zone with image resources, Microsoft 365 box, storage and Key Vault.
- Legend: Virtual network subnet; internal service component interaction; ExpressRoute or site-to-site VPN connection; Microsoft Entra Connect traffic (purple dashed); Private endpoint connection; "Virtual network to virtual network peering traffic" (green dash-dot); Virtual Desktop external traffic; internal traffic; scale unit module; Microsoft 365; pooled and personal host pools; AZ distribution; management plane relationship with session hosts.
- Entra Connect traffic purple dashed line runs from the Entra Connect/Cloud sync server to Microsoft Entra ID; arrowhead ends not distinguishable at the zoom used. Green dash-dot peering lines run from the hub down to the identity subscription network and the VD landing zone network.
- Page alt text for the enterprise picture: "Virtual network peering connects this subscription (connectivity) to other subscriptions."

## CAF traditional topology page, further pictures viewed 18 Oct 2026
- hub-to-hub-er-or-peering.png: Region 1 and Region 2, each with three spoke VNets peered ("Virtual network peering") to its regional hub (gateway + firewall icons). Hubs joined by "Virtual network peering" arrow (two-way). Both hubs also have ExpressRoute circuit links (crossing lines) to a "Customer network". Text on picture: "Use connection weight or AS path prepending to select inbound path", "Use local preference to select outbound path". Offers peering OR ExpressRoute for hub-to-hub.
- multiregion-hub-to-hub-er.png: Regions 1, 2, 3, each hub with three peered spokes; NO hub-to-hub peering drawn; ExpressRoute circuits cross-connect each hub to the customer network (hub to hub through ER). Same inbound/outbound path text.
- customer-managed-topology.svg (ALZ traditional topology): Connectivity subscription with "Hub virtual network region 1" and "Hub virtual network region N" (each: Azure DNS Private Resolver, VPN/ExpressRoute gateways, Azure Firewall), "Virtual network peering" between the two hubs, each hub peered to the workload landing zone VNet of its region (vNet region 1, vNet region N), ExpressRoute circuits and Firewall policies, DDoS Protection, Azure DNS in the subscription.
- Not viewed: vnet-multiple-circuits.png, route-server-transitivity.png (ExpressRoute and Route Server details, not used by any diagram).

## RDP Shortpath scenario pictures 1-7 (rdp-shortpath page, media/rdp-shortpath/rdp-shortpath-scenario-N.png) viewed 18 Oct 2026
- All use icons: Client device, Public network (Internet), VPN, ICE/STUN, ICE/TURN Relay, Session host, Azure Virtual Desktop Gateway (only in 7). Lines are colored (green, purple), no arrowheads.
- 1: Client - Public network - ICE/STUN - Session host (single green line).
- 2: Client - Public network, then two parallel branches to Session host: via ICE/STUN (purple) and via ICE/TURN Relay (green).
- 3: Client to ICE/STUN by two paths: Public network "200 ms" (purple) and VPN "80 ms" (green); ICE/STUN - Session host.
- 4: Two parallel client to Session host paths: public network with ICE/STUN (purple), and VPN (green) running straight to the session host (direct line, no STUN box on it).
- 5: Public network path (green) to ICE/STUN; VPN path (purple) with two red "no entry" symbols on it (client to VPN, VPN to ICE/STUN); ICE/STUN - Session host.
- 6: Client to Session host via public network with ICE/STUN (purple), public network with ICE/TURN relay (green), and VPN (purple); no blocked symbols drawn although alt text says UDP is blocked on the direct VPN and direct public paths.
- 7: Labels TCP and UDP. TCP (green): Client - Public network - Azure Virtual Desktop Gateway - Session host. UDP (purple): via ICE/STUN, via ICE/TURN relay, and via VPN, all to Session host.
- Relevance: Shortpath pictures draw direct client-to-session-host UDP paths (VPN in 4, 6, 7; STUN and TURN in 1-3, 6, 7). rdp-connection.svg draws Shortpath as icon boxes in Region 1, so my flagged "no direct client-host line" difference is a difference between two Learn pictures, not an error in either. Scenario 6 picture vs its alt text: blocked symbols absent in picture; flag.

## Re-viewed for panels D and E, 18 October 2026 (CAF traditional-azure-networking-topology)
- hub-to-hub-er-or-peering.png: Region 1 and Region 2 hubs (lock/gateway icon, firewall icon), three peered spokes each, "Virtual network peering" arrow between hubs, ExpressRoute triangles with crossing circuit lines to Customer network; texts "Use connection weight or AS path prepending to select inbound path" (down arrow) and "Use local preference to select outbound path" (up arrow).
- multiregion-hub-to-hub-er.png: Regions 1 to 3, same hub and spoke content, no hub-to-hub peering. Circuits read at zoom: Region 1 hub to triangles 1 and 2; Region 2 hub to 1, 2, 3; Region 3 hub to 2 and 3; each triangle has a vertical line to the Customer network bar. Same two texts.
