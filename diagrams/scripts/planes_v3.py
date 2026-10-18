#!/usr/bin/env python3
"""AVD post 8 (order 108): three planes. Own layout (the three-plane split is the author's framing). Official icons only."""
from common3 import *
NAME = "AVD-Post-08-Three-Planes-v3"
W, H = 1000, 800
d = D(W, H, "Management, control and data planes in Azure Virtual Desktop",
 "Original diagram with three horizontal bands. Management plane: you or your automation use Azure Resource Manager to create host pools, application groups and workspaces. If it fails, you cannot change settings and users are usually unaffected. Control plane: the Microsoft-run web service, broker service and gateway service, plus the resource directory and the geographical or regional database. If it fails, the feed or new connections fail. Data plane: the user device connects over RDP, over TCP through the gateway or over UDP with RDP Shortpath, to the session host, which uses profile storage and an identity service. If it fails, sessions are slow, freeze or drop.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 36, "Three planes (the author's framing) and what a problem in each affects", 20, True, "middle", INK)
def band(y, h, title, sub, fill, stroke):
    d.rect(20, y, 960, h, fill, stroke, 1.5, 8)
    d.text(36, y+26, title, 16, True, "start", INK); d.text(36, y+46, sub, 14, False, "start", INK)
def note(x, y, lines, col):
    d.text(x, y, lines[0], 14, True, "start", col)
    for i, l in enumerate(lines[1:]): d.text(x, y+20*(i+1), l, 14, False, "start", INK)
def arrow(x1, y1, x2, y2, col=GREYL): d.line(x1, y1, x2, y2, col, 3, None, True)
# Management plane
band(54, 176, "Management plane", "How you create and change AVD objects", "#fdf6ec", ORANGE)
tbox(d, 36, 118, 170, 80, ["You or your", "automation"], "#ffffff", ORANGE, 14, bold_first=True)
tbox(d, 256, 118, 190, 80, ["Azure Resource", "Manager"], "#ffffff", ORANGE, 14, bold_first=True)
tbox(d, 496, 118, 190, 80, ["Host pools, app", "groups, workspaces"], "#ffffff", ORANGE, 14, bold_first=True)
arrow(206, 158, 256, 158, ORANGE); arrow(446, 158, 496, 158, ORANGE)
note(716, 124, ["If it has a problem:", "you cannot change settings.", "Users are usually unaffected.", "(Author's view.)"], ORANGE)
# Control plane
band(246, 250, "Control plane", "The Microsoft-run services that connect users", "#e8f1fb", BLUE)
tbox(d, 36, 306, 150, 66, ["Web service"], "#ffffff", BLUE, 14, bold_first=True)
tbox(d, 226, 306, 150, 66, ["Broker service"], "#ffffff", BLUE, 14, bold_first=True)
tbox(d, 416, 306, 150, 66, ["Gateway service"], "#ffffff", BLUE, 14, bold_first=True)
tbox(d, 36, 416, 150, 66, ["Resource", "directory"], "#ffffff", BLUE, 14, bold_first=True)
tbox(d, 226, 416, 340, 66, ["Geographical or", "regional database"], "#ffffff", BLUE, 14, bold_first=True)
arrow(186, 339, 226, 339, BLUE); arrow(226, 339, 186, 339, BLUE)
d.line(416, 339, 376, 339, BLUE, 3, "3,4", True); d.line(376, 339, 416, 339, BLUE, 3, "3,4", True)
arrow(255, 372, 150, 416, BLUE); arrow(301, 372, 301, 416, BLUE); arrow(301, 416, 301, 372, BLUE)
note(596, 312, ["If it has a problem:", "the feed or new connections", "fail. Documented: a database", "failover briefly fails new", "connections, and a failed", "gateway instance drops the", "connections it relays."], BLUE)
# Data plane
band(512, 272, "Data plane", "The remote session itself", "#eef6ee", GREEN)
d.rect(36, 570, 150, 110, "#ffffff", GREEN, 1.2, 6)
d.icon(91, 576, 40, "dev"); d.text(111, 640, "User device", 14, True, "middle", INK); d.text(111, 659, "(client)", 14, False, "middle", INK)
d.rect(346, 570, 170, 110, "#ffffff", GREEN, 1.2, 6)
d.icon(411, 576, 40, "vm"); d.text(431, 640, "Session host", 14, True, "middle", INK); d.text(431, 659, "(your VM)", 14, False, "middle", INK)
arrow(186, 625, 346, 625, GREEN)
d.text(266, 586, "RDP over TCP via", 14, False, "middle", INK); d.text(266, 604, "the gateway, or UDP", 14, False, "middle", INK)
d.rect(246, 700, 180, 70, "#ffffff", GREEN, 1.2, 6)
d.icon(254, 712, 34, "files"); d.text(358, 730, "Azure Files", 14, True, "middle", INK); d.text(358, 750, "(profile storage)", 14, False, "middle", INK)
d.rect(476, 700, 190, 70, "#ffffff", GREEN, 1.2, 6)
d.icon(484, 712, 34, "entid"); d.text(590, 730, "Microsoft Entra ID", 14, True, "middle", INK); d.text(590, 750, "(or AD DS)", 14, False, "middle", INK)
arrow(380, 680, 380, 700, GREEN); arrow(500, 680, 500, 700, GREEN)
note(716, 580, ["If it has a problem:", "sessions are slow, freeze", "or drop. Sign-in is slow", "or fails. A temporary", "profile can appear.", "(Author's view.)"], GREEN)
finish3(d, NAME, "avd-post08", "Management, control and data planes")
