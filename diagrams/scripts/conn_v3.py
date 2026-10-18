from common3 import *
NAME = "AVD-Post-05-Connections-v3"
W, H = 1000, 960
d = D(W, H, "Azure Virtual Desktop network connections, redrawn from Learn",
 "Not an official Microsoft diagram. It follows the Learn network connections diagram. A client, a session host and AD DS sit at the top. A public internet cloud sits at left. A box named Azure Virtual Desktop Infrastructure holds RD Web, RD Gateway and RD Broker, joined by internal service traffic. Microsoft Entra ID sits below the box. The client has a reverse connect transport line through the internet to RD Gateway, a feed subscription line through the internet to RD Web and an authentication line to Microsoft Entra ID. RD Gateway has a reverse connect line to the session host. The session host has an RD Agent communication line to RD Broker and an Active Directory connectivity line to AD DS. A Microsoft Entra Connect sync line joins Microsoft Entra ID and AD DS with its arrowhead at AD DS as Learn draws it. Session host authentication to Entra ID is not drawn in the Learn diagram.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 36, "Azure Virtual Desktop network connections", 20, True, "middle", INK)
d.text(500, 60, "Redrawn from the Learn diagram, using its names and arrowheads. Arrow ends are as Learn draws them.", 14, False, "middle", INK)
BLU="#1f8ad1"; RED_="#b42318"; PUR=PURPLE; GRN=GREEN; LG="#7bb27d"; YEL="#d4a017"
# nodes
d.rect(30, 100, 180, 120, "#ffffff", GREEN, 1.8, 8); d.icon(85, 110, 40, "dev"); d.text(120, 178, "Client", 14, True, "middle", INK)
d.rect(430, 100, 150, 120, "#ffffff", GREEN, 1.8, 8); d.icon(485, 110, 40, "vm"); d.text(505, 178, "Session host", 14, True, "middle", INK)
tbox(d, 820, 100, 150, 100, ["AD DS"], "#ffffff", ORANGE, 14, bold_all=True)
d.rect(30, 330, 140, 90, "#eaf2fb", GREYL, 1.8, 40); d.text(100, 380, "Public internet", 14, True, "middle", INK)
d.rect(330, 320, 450, 270, "#e8f1fb", BLUE, 1.8, 8)
d.text(555, 575, "Azure Virtual Desktop Infrastructure", 14, True, "middle", INK)
tbox(d, 490, 345, 130, 60, ["RD Web"], "#ffffff", BLUE, 14, bold_all=True)
tbox(d, 350, 465, 130, 60, ["RD Gateway"], "#ffffff", BLUE, 14, bold_all=True)
tbox(d, 640, 465, 130, 60, ["RD Broker"], "#ffffff", BLUE, 14, bold_all=True)
d.rect(330, 650, 230, 80, "#ffffff", PUR, 1.8, 8); d.icon(342, 670, 40, "entid"); d.text(392, 697, "Microsoft Entra ID", 14, True, "start", INK)
# blue reverse connect
d.line(60, 330, 60, 220, BLU, 4, None, True)
d.line(170, 400, 250, 400, BLU, 4); d.line(250, 400, 250, 495, BLU, 4); d.line(250, 495, 350, 495, BLU, 4, None, True)
d.line(390, 465, 390, 160, BLU, 4); d.line(390, 160, 430, 160, BLU, 4, None, True)
# red feed subscription
d.line(120, 220, 120, 330, RED_, 3, None, True)
d.line(170, 360, 490, 360, RED_, 3, None, True)
# purple auth
d.line(195, 220, 195, 690, PUR, 3); d.line(195, 690, 330, 690, PUR, 3, None, True)
# green RD agent
d.line(565, 220, 565, 290, GRN, 3); d.line(565, 290, 705, 290, GRN, 3); d.line(705, 290, 705, 465, GRN, 3, None, True)
# AD connectivity green dashed
d.line(580, 160, 820, 160, GRN, 2.5, "6,4", True)
d.text(700, 148, "Active Directory connectivity", 13, False, "middle", INK)
# internal service traffic (yellow dotted)
d.line(480, 495, 640, 495, YEL, 3, "3,4", True); d.line(640, 495, 480, 495, YEL, 3, "3,4", True)
d.line(440, 465, 520, 405, YEL, 3, "3,4", True); d.line(700, 465, 590, 405, YEL, 3, "3,4", True)
# sync
d.line(560, 690, 895, 690, LG, 3, "10,5"); d.line(895, 690, 895, 200, LG, 3, "10,5", True)
# legend
d.rect(30, 760, 940, 118, "#ffffff", GREYL, 1.2, 6)
leg = [(BLU, None, 4, "Reverse connect transport (TCP 443)"), (RED_, None, 3, "Feed subscription (TCP 443)"),
       (PUR, None, 3, "Microsoft Entra authentication (TCP 443)"), (GRN, None, 3, "RD Agent communication (TCP 443)"),
       (GRN, "6,4", 2.5, "Active Directory connectivity"), (LG, "10,5", 3, "Microsoft Entra Connect sync (TCP 443)"),
       (YEL, "3,4", 3, "Internal service traffic")]
for i, (c, da, sw, t) in enumerate(leg):
    col, row = i // 4, i % 4
    x = 48 + col*470; y = 784 + row*22
    d.line(x, y, x+40, y, c, sw, da); d.text(x+52, y+5, t, 13, False, "start", INK)
d.rect(30, 890, 940, 58, "#ffffff", ORANGE, 1.4, 6)
d.text(44, 912, "Flagged: Learn's arrowheads and the page text differ. The sync line has its arrowhead at AD DS here, as in Learn,", 13, False, "start", INK)
d.text(44, 932, "while Learn text describes Microsoft Entra Connect syncing from AD DS to Entra ID. Page text: both ends connect outward.", 13, False, "start", INK)
finish3(d, NAME, "avd-post05-conn-v3", "AVD network connections on Learn v3")
