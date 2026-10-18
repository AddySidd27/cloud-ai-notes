#!/usr/bin/env python3
"""PROPOSAL ONLY (scratch). Redesigned hybrid AVD diagram. Official Azure and Entra icons, unmodified (uniform scaling only).
Writes SVG + .drawio + PNG into this folder. Does not touch any repository."""
import os
src = open("/home/claude/blog/tools/build_diagrams.py", encoding="utf-8").read().split("def cap(")[0]
exec(src)
exec(open("/home/claude/blog/tools/diag_helpers.py", encoding="utf-8").read())
OUTD = "/home/claude/cloud-ai-notes-rewritten/src/img/avd/"
NAME = "AVD-Post-02-Hybrid-Architecture-v3"
ICONS.update({
 "avd": "other/00327-icon-service-Azure-Virtual-Desktop.svg",
 "hostpool": "compute/00328-icon-service-Host-Pools.svg",
 "mon": "monitor/00001-icon-service-Monitor.svg",
 "law": "monitor/00009-icon-service-Log-Analytics-Workspaces.svg",
 "entcon": "identity/02854-icon-service-Entra-Connect.svg",
 "subnet": "networking/02742-icon-service-Subnet.svg",
 "vm": "compute/10021-icon-service-Virtual-Machine.svg",
 "files": "storage/10400-icon-service-Azure-Fileshares.svg",
 "anf": "storage/10096-icon-service-Azure-NetApp-Files.svg",
 "dev": "intune/10332-icon-service-Devices.svg",
})
W, H = 1000, 1064
INK = "#1f2933"; BLUE = "#3b6fb6"; ORANGE = "#c2570c"; GREYL = "#5f6b7a"; PURPLE = "#6b4fa0"; GREEN = "#3c8d40"; TEAL = "#0f766e"
d = D(W, H, "Azure Virtual Desktop in a hybrid environment",
 "Not an official Microsoft diagram. At the top, the Microsoft-managed Azure Virtual Desktop service (control plane) with the web service, gateway service, broker service, resource directory and geographical or regional database, and Microsoft Entra ID. In an internet band, user devices running AVD clients sign in to Microsoft Entra ID and connect to the service over TLS. A customer Azure subscription holds a spoke virtual network with a session host subnet protected by a network security group and a host pool of session hosts running the AVD agent, a hub virtual network with a gateway subnet and an optional Azure Firewall subnet, VNet peering between hub and spoke, profile storage in Azure Files or Azure NetApp Files for FSLogix, and Azure Monitor with a Log Analytics workspace. The on-premises network holds Microsoft Entra Connect and domain controllers (AD DS). The hub gateway connects to the on-premises network by ExpressRoute or VPN. Session hosts connect outbound to the service (reverse connect). Microsoft Entra Connect synchronizes identities to Microsoft Entra ID.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 34, "Azure Virtual Desktop in a hybrid environment", 20, True, "middle", INK)
# control plane
d.rect(20, 50, 630, 155, "#e8f1fb", BLUE, 1.5, 8)
d.icon(32, 58, 30, "avd"); d.text(70, 80, "Azure Virtual Desktop service (control plane)", 15, True, "start", INK)
d.text(70, 98, "Managed by Microsoft", 13, False, "start", INK)
for i, lines in enumerate([["Web service"], ["Gateway", "service"], ["Broker", "service"], ["Resource", "directory"], ["Geographical or", "regional database"]]):
    tbox(d, 32+i*121, 116, 118, 76, lines, "#ffffff", BLUE, 13, bold_first=True)
# entra id
d.rect(680, 50, 300, 155, "#e8f1fb", BLUE, 1.5, 8)
d.icon(698, 92, 46, "entid"); d.text(756, 110, "Microsoft Entra ID", 15, True, "start", INK)
d.text(756, 134, "Authenticates users and", 13, False, "start", INK); d.text(756, 151, "issues the sign-in token", 13, False, "start", INK)
# internet band
d.rect(20, 212, 960, 134, "#f2f4f7", "#f2f4f7", 0, 4)
d.text(30, 336, "Internet", 15, True, "start", GREYL)
d.rect(700, 256, 180, 84, "#ffffff", GREYL, 1.2, 6); d.icon(775, 262, 30, "dev")
d.text(790, 312, "User devices", 14, True, "middle", INK); d.text(790, 329, "(AVD clients)", 13, False, "middle", INK)
# user sign in + connection
d.line(760, 256, 760, 207, BLUE, 3, None, True); d.text(752, 236, "Sign in", 13, False, "end", INK)
d.line(700, 300, 641, 300, BLUE, 3); d.line(641, 300, 641, 207, BLUE, 3, None, True)
d.text(490, 236, "Feed discovery and", 13, False, "start", INK); d.text(490, 253, "RDP connection (TLS)", 13, False, "start", INK)
# outbound reverse connect
# identity sync
# subscription
d.rect(20, 352, 575, 462, "#eef6ee", GREEN, 1.5, 8)
d.icon(300, 356, 22, "sub"); d.text(327, 373, "Azure subscription (simplified)", 14, True, "start", INK)
# spoke
d.rect(32, 392, 230, 256, "#ffffff", GREEN, 1.2, 6)
d.icon(40, 396, 20, "vnet"); d.text(65, 412, "Spoke virtual network", 14, True, "start", INK)
d.rect(42, 426, 210, 214, "#f7fbf7", GREEN, 1, 4)
d.icon(48, 431, 18, "subnet"); d.text(70, 445, "Session host subnet", 14, False, "start", INK)
d.rect(52, 458, 180, 118, "#ffffff", BLUE, 1.2, 4)
d.icon(58, 463, 22, "hostpool"); d.text(84, 479, "Host pool", 14, True, "start", INK)
d.icon(98, 490, 34, "vm"); d.icon(152, 490, 34, "vm")
d.text(142, 545, "Session hosts", 14, True, "middle", INK); d.text(142, 563, "(with the AVD agent)", 13, False, "middle", INK)
d.icon(52, 586, 24, "nsg"); d.text(82, 603, "Network security group", 13, False, "start", INK)
# hub
d.rect(336, 392, 247, 194, "#ffffff", GREEN, 1.2, 6)
d.icon(344, 396, 20, "vnet"); d.text(369, 412, "Hub virtual network", 14, True, "start", INK)
d.rect(346, 426, 227, 72, "#f7fbf7", GREEN, 1, 4)
d.icon(352, 430, 18, "subnet"); d.text(374, 444, "Gateway subnet", 14, False, "start", INK)
d.icon(358, 458, 32, "vng"); d.text(398, 474, "Virtual network gateway", 14, True, "start", INK); d.text(398, 491, "(ExpressRoute or VPN)", 13, False, "start", INK)
d.rect(346, 506, 227, 72, "#f7fbf7", GREEN, 1, 4)
d.icon(352, 510, 18, "subnet"); d.text(374, 524, "Azure Firewall subnet", 14, False, "start", INK)
d.icon(358, 536, 32, "fw"); d.text(398, 552, "Azure Firewall", 14, True, "start", INK); d.text(398, 569, "(optional)", 13, False, "start", INK)
# peering
d.line(262, 502, 336, 502, GREYL, 2.5)
d.text(299, 478, "VNet", 14, False, "middle", INK); d.text(299, 494, "peering", 14, False, "middle", INK)
# storage
d.rect(32, 690, 230, 100, "#ffffff", GREEN, 1.2, 6)
d.icon(72, 698, 34, "files"); d.icon(118, 698, 34, "anf")
d.text(147, 756, "Profile storage (FSLogix)", 14, True, "middle", INK); d.text(147, 775, "Azure Files or Azure NetApp Files", 14, False, "middle", INK)
d.line(147, 648, 147, 688, GREYL, 2.5, None, True); d.text(157, 674, "FSLogix profiles (SMB)", 13, False, "start", INK)
# monitoring
d.rect(336, 690, 247, 100, "#ffffff", GREEN, 1.2, 6)
d.icon(400, 698, 34, "mon"); d.icon(446, 698, 34, "law")
d.text(459, 756, "Azure Monitor", 14, True, "middle", INK); d.text(459, 775, "Log Analytics workspace", 14, False, "middle", INK)
d.line(252, 620, 460, 620, TEAL, 2.5); d.line(460, 620, 460, 688, TEAL, 2.5, None, True); d.text(470, 660, "Logs and metrics", 13, False, "start", INK)
# on-prem
d.rect(700, 352, 280, 330, "#f5f5f5", GREYL, 1.5, 8)
d.rect(850, 392, 120, 98, "#ffffff", GREYL, 1.2, 6); d.icon(895, 398, 30, "entcon")
d.text(910, 452, "Microsoft", 14, True, "middle", INK); d.text(910, 470, "Entra Connect", 14, True, "middle", INK)
d.rect(716, 520, 254, 70, "#ffffff", GREYL, 1.2, 6)
d.text(843, 550, "Domain controllers", 14, True, "middle", INK); d.text(843, 570, "(AD DS)", 13, False, "middle", INK)
d.text(840, 640, "On-premises network", 14, True, "middle", INK)
# arrows that must sit on top of the boxes they start from
d.line(232, 458, 232, 207, ORANGE, 3, None, True)
d.text(244, 236, "Session hosts connect", 13, False, "start", INK); d.text(244, 253, "outbound (reverse connect)", 13, False, "start", INK)
d.line(940, 392, 940, 207, GREYL, 2.5, "3 4", True); d.text(932, 226, "Identity", 13, False, "end", INK); d.text(932, 243, "synchronization", 13, False, "end", INK)
# private link
d.line(583, 462, 700, 462, PURPLE, 3, "8 5"); d.text(647, 436, "ExpressRoute", 14, False, "middle", INK); d.text(647, 452, "or VPN", 14, False, "middle", INK)
# notes
d.text(500, 842, "AD DS joined hosts need line of sight to domain controllers (here, via peering and the gateway); Entra joined hosts do not.", 14, False, "middle", INK)
d.text(500, 862, "If you use a firewall, allow the required AVD endpoints and do not use TLS inspection.", 14, False, "middle", INK)
# legend
d.rect(20, 882, 960, 172, "#ffffff", GREYL, 1, 6)
d.text(36, 908, "Legend", 14, True, "start", INK)
items = [(BLUE, None, True, "User sign in, and connection to the service over the internet"), (ORANGE, None, True, "Session host outbound connection to the service (reverse connect)"),
         (PURPLE, "8 5", False, "Private link between on-premises and Azure (ExpressRoute or VPN)"), (GREYL, None, True, "Private traffic inside Azure: peering and profile storage access"),
         (TEAL, None, True, "Logs and metrics sent to Azure Monitor"), (GREYL, "3 4", True, "Identity synchronization")]
for i, (c, da, ar, t) in enumerate(items):
    y = 932+i*20
    d.line(36, y-5, 96, y-5, c, 3, da, ar); d.text(108, y, t, 14, False, "start", INK)
check(d, "redesign")
svg = d.svg().replace('markerWidth="8" markerHeight="8"', 'markerWidth="4" markerHeight="4"')
open(OUTD+NAME+".svg", "w", encoding="utf-8").write(svg)
open(OUTD+NAME+".drawio", "w", encoding="utf-8").write(d.drawio("avd-post02-hybrid-v3", "Hybrid AVD architecture v3"))
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
    pg.goto("file://"+OUTD+NAME+".svg"); pg.screenshot(path=OUTD+NAME+".png", full_page=False); b.close()
print("written", NAME)
