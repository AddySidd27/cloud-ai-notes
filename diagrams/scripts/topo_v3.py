#!/usr/bin/env python3
"""AVD post 17 (order 117): hub and spoke versus Virtual WAN, with address checks. Own simplified layout (the documentation diagrams are full landing zone reference architectures)."""
from common3 import *
NAME = "AVD-Post-17-Topology-Choice-v3"
W, H = 1000, 805
d = D(W, H, "Hub and spoke compared with Virtual WAN for an AVD spoke",
 "Original simplified drawing. Left panel: traditional hub and spoke, a hub virtual network with shared services (firewall, gateway, Bastion, DNS resolver), joined by peering to a spoke virtual network that holds the AVD session host subnet. Right panel: Virtual WAN, a Microsoft-managed virtual hub with firewall and gateways, joined by hub connections to a shared services spoke for customer-run shared services such as DNS servers, and an AVD spoke. Three boxes below: when hub and spoke fits, when Virtual WAN fits (both from the Cloud Adoption Framework criteria), and address plan checks.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 38, "Two ways to connect an AVD spoke to the rest of the network", 20, True, "middle", INK)
# left panel: CAF traditional hub and spoke picture
d.rect(30, 66, 460, 450, "#ffffff", BLUE, 1.6, 8)
d.text(260, 94, "Traditional hub and spoke", 16, True, "middle", INK)
for i in range(3):
    x = 60 + i*135
    d.rect(x, 112, 120, 62, "#eef6ee", GREEN, 1.6, 8)
    d.icon(x+8, 118, 24, "vnet"); d.text(x+60, 160, "Spoke VNet", 13, True, "middle", INK)
    d.line(x+60, 174, x+60, 290, GREYL, 2.5)
d.rect(150, 224, 220, 24, "#ffffff", "#ffffff", 0, 0)
d.text(260, 242, "Virtual network peering", 14, True, "middle", INK)
d.rect(60, 290, 390, 110, "#e8f1fb", BLUE, 1.8, 8)
d.icon(66, 295, 24, "vnet"); d.text(96, 313, "Hub virtual network, Region 1", 13, True, "start", INK)
d.icon(150, 325, 36, "vng"); d.icon(300, 325, 36, "fw")
d.text(168, 385, "Gateway", 13, False, "middle", INK); d.text(318, 385, "Firewall", 13, False, "middle", INK)
d.line(255, 400, 255, 425, GREYL, 2.5)
d.icon(237, 425, 36, "er")
d.text(260, 480, "ExpressRoute icon, unlabelled in Learn", 13, False, "middle", INK)
d.text(260, 500, "No spoke-to-spoke link is drawn.", 13, False, "middle", INK)
# right panel: CAF Virtual WAN picture
d.rect(510, 66, 460, 450, "#ffffff", PURPLE, 1.6, 8)
d.text(740, 94, "Virtual WAN", 16, True, "middle", INK)
for y, r in ((120, "Region 1"), (380, "Region N")):
    d.rect(520, y, 100, 100, "#e8f1fb", BLUE, 1.5, 8)
    d.text(570, y+30, "DNS spoke", 13, True, "middle", INK); d.text(570, y+48, r, 13, True, "middle", INK)
    d.text(570, y+68, "DNS Private", 13, False, "middle", INK); d.text(570, y+86, "Resolver", 13, False, "middle", INK)
    d.line(620, y+50, 660, y+50, GREYL, 2.5)
    d.rect(660, y, 130, 100, "#f1ecf7", PURPLE, 1.5, 8)
    d.text(725, y+24, "Virtual hub", 13, True, "middle", INK); d.text(725, y+40, r, 13, True, "middle", INK)
    d.text(725, y+60, "Azure Firewall", 13, False, "middle", INK); d.text(725, y+76, "VPN/ExpressRoute", 13, False, "middle", INK); d.text(725, y+92, "gateways", 13, False, "middle", INK)
    d.line(790, y+50, 880, y+50, GREYL, 2.5)
    d.text(835, y+36, "VWAN hub", 13, False, "middle", INK); d.text(835, y+78, "connection", 13, False, "middle", INK)
    d.rect(880, y, 80, 100, "#eef6ee", GREEN, 1.6, 8)
    d.text(920, y+40, "Workload", 13, True, "middle", INK); d.text(920, y+58, "vNet", 13, True, "middle", INK); d.text(920, y+76, r, 13, True, "middle", INK)
d.rect(660, 220, 130, 160, "#c9b8e0", PURPLE, 1.5, 4)
d.icon(709, 230, 32, "vwan"); d.text(725, 290, "VWAN", 14, True, "middle", INK)
d.icon(531, 270, 32, "er"); d.text(570, 328, "ExpressRoute", 13, False, "middle", INK); d.text(570, 346, "circuits", 13, False, "middle", INK)
d.text(740, 500, "The VWAN band joins the two hubs.", 13, False, "middle", INK)
# bottom boxes
bx = [(30, "Hub and spoke fits when (CAF)", BLUE, ["- one or several regions, with", "  some traffic across regions", "- fewer than 30 IPsec site-to-", "  site tunnels per region", "- you want to control routing", "  yourself"]),
      (350, "Virtual WAN fits when (CAF)", PURPLE, ["- several regions that need", "  global connectivity", "- SD-WAN, or more than 30", "  branch sites", "- transitive routing between", "  VPN and ExpressRoute"]),
      (670, "Address plan checks", ORANGE, ["- No overlap across regions,", "  on premises and hubs", "- Azure keeps 5 addresses", "  in every subnet", "- A Virtual WAN hub range", "  cannot change after creation"])]
for x, t, col, ls in bx:
    d.rect(x, 545, 300, 235, "#ffffff", col, 1.8, 8)
    d.text(x+150, 575, t, 15, True, "middle", col)
    for i, l in enumerate(ls): d.text(x+(40 if l.startswith("  ") else 20), 612+i*27, l.strip() if l.startswith("  ") else l, 14, False, "start", INK)
finish3(d, NAME, "avd-post17", "Topology choice")
