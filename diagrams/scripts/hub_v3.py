from common3 import *
ICONS.update({
 "bastion": "networking/02422-icon-service-Bastions.svg",
 "monitor": "monitor/00001-icon-service-Monitor.svg",
 "avnm": "other/02237-icon-service-Network-Managers.svg",
})
NAME = "AVD-Post-05-Hub-Spoke-v3"
W, H = 1000, 1792
d = D(W, H, "Hub and spoke layouts as drawn on Microsoft Learn pages, including two hub-to-hub options",
 "Not an official Microsoft diagram. Five separate panels, each redrawn from a Microsoft Learn page or picture, and not one combined design. Panel A follows the Azure Architecture Center hub-spoke network topology diagram: a hub virtual network with Azure Bastion, Azure Firewall and a VPN gateway, a cross-premises network connected to the gateway, Azure Monitor receiving diagnostics, two production spokes and two nonproduction spokes each connected to the hub, forced tunnel arrows from the production spokes to the firewall, and one connection between the two nonproduction spokes. Panel B follows the Cloud Adoption Framework traditional topology diagram: three spokes each peered to one hub that holds a gateway and a firewall. Panel C follows the Azure Virtual Desktop landing zone diagram: two regional hubs peered to each other, an identity virtual network per region peered to its hub, and one Azure Virtual Desktop virtual network peered to both hubs. No spoke-to-spoke peering is drawn in panels B and C, or between the production spokes in panel A. Panel D shows hub-to-hub connection by virtual network peering between two regional hubs, from the Cloud Adoption Framework traditional topology page. Panel E shows hub-to-hub connection through ExpressRoute circuits for three regions, with no hub-to-hub peering, from the same page. D and E are separate options and are not combined.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 34, "Hub and spoke layouts on Learn pages", 20, True, "middle", INK)
d.text(500, 58, "Separate sources. They are options and examples, not one design.", 14, False, "middle", INK)

# ---------- Panel A ----------
d.text(20, 92, "A. Azure Architecture Center: hub-spoke network topology", 15, True, "start", INK)
d.rect(205, 104, 780, 466, "#ffffff", GREYL, 1.4, 8)
d.icon(213, 109, 24, "avnm"); d.text(243, 127, "Azure Virtual Network Manager (outer frame in Learn)", 13, False, "start", INK)
d.rect(225, 140, 240, 325, "#e8f1fb", BLUE, 1.8, 8)
d.icon(231, 145, 24, "vnet"); d.text(262, 163, "Hub virtual network", 13, True, "start", INK)
for y, ic, t in [(180, "bastion", "Azure Bastion"), (265, "fw", "Azure Firewall"), (350, "vng", "VPN Gateway")]:
    d.rect(240, y, 210, 70, "#ffffff", BLUE, 1.2, 6)
    d.icon(250, y+19, 32, ic); d.text(292, y+42, t, 14, True, "start", INK)
d.rect(20, 180, 150, 240, "#ffffff", GREYL, 1.4, 8)
d.icon(75, 190, 40, "monitor"); d.text(95, 250, "Azure Monitor", 14, True, "middle", INK)
for i, t in enumerate(["Diagnostics", "from Bastion,", "Firewall and", "VPN Gateway"]):
    d.text(95, 290+i*20, t, 13, False, "middle", INK)
for y in (215, 300, 385):
    d.line(240, y, 170, y, GREYL, 2, "6,4", True)
d.rect(240, 495, 210, 60, "#ffffff", GREYL, 1.4, 8)
d.text(345, 522, "Cross-premises network", 14, True, "middle", INK)
d.text(345, 542, "VMs and a gateway", 13, False, "middle", INK)
d.line(345, 420, 345, 495, GREYL, 2.5, "3,3", True); d.line(345, 495, 345, 420, GREYL, 2.5, "3,3", True)
spokes = [("Production spoke 1", 150, "#eef6ee", GREEN), ("Production spoke 2", 235, "#eef6ee", GREEN),
          ("Nonproduction spoke 1", 320, "#fdf3e7", ORANGE), ("Nonproduction spoke 2", 430, "#fdf3e7", ORANGE)]
for t, y, f, s_ in spokes:
    d.rect(660, y, 315, 75, f, s_, 1.6, 8)
    d.icon(668, y+6, 26, "vnet"); d.text(700, y+25, t, 14, True, "start", INK)
    d.text(676, y+53, "Resource subnet with VMs", 13, False, "start", INK)
    yy = y+20
    d.line(465, yy, 660, yy, GREYL, 2.5, None, True); d.line(660, yy, 465, yy, GREYL, 2.5, None, True)
d.text(540, 150, "Connected or", 13, False, "middle", INK); d.text(540, 166, "peered through hub", 13, False, "middle", INK)
d.text(540, 316, "Connected", 13, False, "middle", INK); d.text(540, 332, "virtual networks", 13, False, "middle", INK)
for y in (205, 290):
    d.line(660, y, 632, y, GREEN, 2.5, "6,4", False)
d.line(632, 205, 632, 300, GREEN, 2.5, "6,4", False)
d.line(632, 300, 450, 300, GREEN, 2.5, "6,4", True)
d.text(540, 292, "Forced tunnel", 13, True, "middle", GREEN)
d.line(817, 395, 817, 430, GREYL, 2.5, None, True); d.line(817, 430, 817, 395, GREYL, 2.5, None, True)
d.text(827, 408, "Peered or", 13, False, "start", INK); d.text(827, 424, "directly connected", 13, False, "start", INK)

# ---------- Panel B ----------
d.text(20, 600, "B. Cloud Adoption Framework: traditional topology", 15, True, "start", INK)
d.rect(15, 612, 455, 330, "#ffffff", GREYL, 1.4, 8)
for i in range(3):
    x = 35 + i*140
    d.rect(x, 628, 120, 70, "#eef6ee", GREEN, 1.6, 8)
    d.icon(x+8, 636, 26, "vnet"); d.text(x+60, 682, "Spoke VNet", 13, True, "middle", INK)
    d.line(x+60, 698, x+60, 765, GREYL, 2.5, None, False)
d.rect(150, 722, 170, 22, "#ffffff", "#ffffff", 0, 0)
d.text(235, 738, "Virtual network peering", 14, True, "middle", INK)
d.rect(35, 765, 400, 100, "#e8f1fb", BLUE, 1.8, 8)
d.icon(41, 770, 24, "vnet"); d.text(72, 788, "Hub virtual network, Region 1", 13, True, "start", INK)
d.icon(145, 800, 36, "vng"); d.icon(275, 800, 36, "fw")
d.text(163, 856, "Gateway", 13, False, "middle", INK); d.text(293, 856, "Firewall", 13, False, "middle", INK)
d.line(235, 865, 235, 878, GREYL, 2.5, None, False)
d.icon(217, 878, 36, "er")
d.text(235, 930, "ExpressRoute icon, unlabelled in Learn", 13, False, "middle", INK)

# ---------- Panel C ----------
d.text(500, 600, "C. AVD landing zone design guide", 15, True, "start", INK)
d.rect(495, 612, 490, 330, "#ffffff", GREYL, 1.4, 8)
for y, r in ((660, "region 1"), (800, "region N")):
    d.rect(505, y, 105, 80, "#fdf3e7", ORANGE, 1.6, 8)
    d.text(557, y+35, "Identity VNet", 13, True, "middle", INK); d.text(557, y+55, r, 13, False, "middle", INK)
    d.rect(670, y, 115, 80, "#e8f1fb", BLUE, 1.8, 8)
    d.text(727, y+35, "Hub VNet", 13, True, "middle", INK); d.text(727, y+55, r, 13, False, "middle", INK)
    d.line(610, y+40, 670, y+40, GREYL, 2.5, None, False); d.text(640, y+32, "peering", 13, False, "middle", INK)
    d.line(785, y+40, 875, y+40, GREYL, 2.5, None, False); d.text(830, y+32, "peering", 13, False, "middle", INK)
d.line(727, 740, 727, 800, GREYL, 2.5, None, False); d.text(737, 774, "peering", 13, False, "start", INK)
d.rect(875, 660, 100, 220, "#eef6ee", GREEN, 1.6, 8)
d.icon(883, 668, 26, "vnet")
for i, t in enumerate(["AVD", "virtual", "network"]):
    d.text(925, 730+i*20, t, 13, True, "middle", INK)
for i, t in enumerate(["personal", "and pooled", "subnets"]):
    d.text(925, 800+i*18, t, 13, False, "middle", INK)
d.text(510, 912, "Hubs hold DNS Private Resolver, gateways and Azure Firewall in Learn.", 13, False, "start", INK)

# ---------- Panel D ----------
def region_block(x0, w, y, label, spw, gap, circuits=False):
    n = 3
    for k in range(n):
        sx = x0 + 2 + k*(spw+gap)
        d.rect(sx, y, spw, 52, "#eef6ee", GREEN, 1.6, 6)
        d.icon(sx+4, y+4, 22, "vnet"); d.text(sx+spw/2, y+44, "Spoke VNet", 13, True, "middle", INK)
        d.line(sx+spw/2, y+52, sx+spw/2, y+110, GREYL, 2.5, None, False)
    d.rect(x0+20, y+58, w-40, 24, "#ffffff", "#ffffff", 0, 0)
    d.text(x0+w/2, y+75, "Virtual network peering", 13, True, "middle", INK)
    d.rect(x0, y+110, w, 100, "#e8f1fb", BLUE, 1.8, 8)
    d.icon(x0+w/2-60, y+122, 32, "vng"); d.icon(x0+w/2+28, y+122, 32, "fw")
    d.text(x0+8, y+202, label, 13, True, "start", INK)

d.text(20, 1000, "D. Cloud Adoption Framework: hub-to-hub with virtual network peering", 15, True, "start", INK)
d.rect(15, 1012, 970, 292, "#ffffff", GREYL, 1.4, 8)
region_block(35, 320, 1030, "Hub VNet, Region 1", 95, 15)
region_block(645, 320, 1030, "Hub VNet, Region 2", 95, 15)
d.line(355, 1170, 645, 1170, GREYL, 2.5, None, True); d.line(645, 1170, 355, 1170, GREYL, 2.5, None, True)
d.text(500, 1158, "Virtual network peering", 13, True, "middle", INK)
d.text(500, 1192, "(global peering, hub to hub)", 13, False, "middle", INK)
d.text(30, 1262, "Learn text: to connect two Azure regions, use global virtual network peering between the regional hubs.", 13, False, "start", INK)
d.text(30, 1282, "The same Learn picture also draws ExpressRoute circuits to a customer network. They are left out here so this panel shows one option.", 13, False, "start", INK)

# ---------- Panel E ----------
d.text(20, 1330, "E. Cloud Adoption Framework: hub-to-hub through ExpressRoute (three regions)", 15, True, "start", INK)
d.rect(15, 1342, 970, 345, "#ffffff", GREYL, 1.4, 8)
xs = [35, 355, 675]
for k, x0 in enumerate(xs):
    region_block(x0, 290, 1358, "Hub VNet, Region %d" % (k+1), 88, 10)
cx = [x0+145 for x0 in xs]
hub_b = 1358+210
tri_top = 1600
for h, t in [(0,0),(0,1),(1,0),(1,1),(1,2),(2,1),(2,2)]:
    d.line(cx[h], hub_b, cx[t], tri_top, PURPLE, 2.2, None, False)
d.rect(35, 1650, 930, 8, "#cfd4da", "#cfd4da", 0, 0)
for c in cx:
    d.icon(c-14, tri_top, 28, "er")
    d.line(c, tri_top+28, c, 1650, GREYL, 2, None, False)
d.text(500, 1680, "Customer network", 13, True, "middle", INK)
d.text(30, 1680, "Inbound: connection weight or AS path prepending", 13, False, "start", INK)
d.text(970, 1680, "Outbound: local preference", 13, False, "end", INK)

# ---------- notes ----------
d.rect(15, 1704, 970, 74, "#ffffff", GREEN, 1.4, 6)
d.text(30, 1726, "Panels D and E are two separate options from the same Learn page, not one design. Learn says to use peering for two regions", 13, False, "start", INK)
d.text(30, 1746, "and to prefer shared ExpressRoute circuits for more than two. In E, hubs have no peering and spokes in other regions are reached by BGP routes.", 13, False, "start", INK)
d.text(30, 1766, "Each panel is only what its own Learn page draws. Virtual WAN is a separate topology. Check the cited pages before copying any panel.", 13, False, "start", INK)
finish3(d, NAME, "avd-post05-hub-v3", "AVD hub and spoke on Learn v3")
