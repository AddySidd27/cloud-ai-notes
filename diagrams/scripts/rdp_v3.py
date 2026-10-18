from common3 import *
NAME = "AVD-Post-02-RDP-Connection-v3"
W, H = 1000, 640
d = D(W, H, "The RDP connection, redrawn from Learn",
 "Not an official Microsoft diagram. It follows the Learn RDP connection diagram. A client has a two-way link to Azure Front Door, and Azure Front Door has a two-way TCP link to the gateway service. Inside a box labelled Region 1 are the gateway service, the broker service and the session host, with dotted two-way links from gateway to broker and from broker to session host, and a two-way TCP link between the gateway service and the session host. Two RDP Shortpath boxes, one for managed networks and one for public networks, also sit inside Region 1. Purple UDP lines run from the client to both Shortpath boxes and to the session host, and from the session host to both Shortpath boxes.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 36, "The RDP connection: TCP through the gateway, and UDP RDP Shortpath", 20, True, "middle", INK)
UDP = "#7a3fa0"
d.rect(330, 80, 640, 470, "#f7f9fc", GREYL, 1.6, 8); d.text(650, 104, "Region 1", 14, True, "middle", INK)
tbox(d, 24, 270, 130, 90, ["", "Client"], "#ffffff", GREEN, 14, bold_all=True); d.icon(69, 282, 40, "dev")
tbox(d, 190, 255, 120, 110, ["", "Azure Front", "Door"], "#ffffff", BLUE, 14, bold_all=True); d.icon(230, 265, 40, "afd")
d.line(154, 315, 190, 315, INK, 2.5, None, True); d.line(190, 315, 154, 315, INK, 2.5, None, True)
tbox(d, 390, 430, 120, 80, ["Gateway","service"], "#ffffff", BLUE, 14, bold_all=True)
tbox(d, 560, 430, 130, 80, ["Broker service"], "#ffffff", BLUE, 14, bold_all=True)
d.rect(800, 430, 140, 80, "#ffffff", GREEN, 1.6, 8); d.icon(808, 440, 28, "vm"); d.text(870, 485, "Session host", 14, True, "middle", INK)
# front door <-> gateway (TCP)
d.line(310, 315, 330, 315, INK, 2.5); d.line(330, 315, 330, 470, INK, 2.5); d.line(330, 470, 390, 470, INK, 2.5, None, True); d.line(390, 470, 330, 470, INK, 2.5, None, True)
d.text(320, 390, "TCP", 13, True, "end", INK)
# gateway <-> broker, broker <-> host dotted
d.line(510, 470, 560, 470, INK, 2.5, "3,4", True); d.line(560, 470, 510, 470, INK, 2.5, "3,4", True)
d.line(690, 470, 800, 470, INK, 2.5, "3,4", True); d.line(800, 470, 690, 470, INK, 2.5, "3,4", True)
# gateway <-> session host TCP (over the top)
d.line(450, 430, 450, 395, INK, 2.5); d.line(450, 395, 870, 395, INK, 2.5); d.line(870, 395, 870, 430, INK, 2.5, None, True); d.line(450, 395, 450, 430, INK, 2.5, None, True)
d.text(640, 385, "TCP", 13, True, "middle", INK)
# shortpath boxes
d.rect(540, 130, 200, 80, "#ffffff", UDP, 1.6, 8); d.text(640, 165, "RDP Shortpath", 14, True, "middle", INK); d.text(640, 185, "managed networks", 13, False, "middle", INK)
d.rect(540, 255, 200, 80, "#ffffff", UDP, 1.6, 8); d.text(640, 290, "RDP Shortpath", 14, True, "middle", INK); d.text(640, 310, "public networks", 13, False, "middle", INK)
# UDP lines: client to both boxes and to session host
d.line(89, 270, 89, 170, UDP, 3); d.line(89, 170, 540, 170, UDP, 3, None, True)
d.line(440, 170, 440, 295, UDP, 3); d.line(440, 295, 540, 295, UDP, 3, None, True)
d.line(89, 170, 89, 270, UDP, 3, None, True)
d.text(110, 158, "UDP", 13, True, "start", UDP)
d.line(870, 430, 870, 232, UDP, 3); d.line(870, 232, 740, 170, UDP, 3, None, True); d.line(870, 232, 740, 295, UDP, 3, None, True)
d.line(870, 395, 870, 430, UDP, 3, None, True)
d.text(880, 330, "UDP", 13, True, "start", UDP)
d.rect(15, 565, 970, 62, "#ffffff", ORANGE, 1.4, 6)
d.text(28, 586, "Flagged: Learn draws the client UDP line toward the Shortpath boxes and the session host, with no direct client-to-host", 13, False, "start", INK)
d.text(28, 606, "line, while its text says Shortpath is a direct UDP transport that bypasses the gateway service. Not resolved here.", 13, False, "start", INK)
finish3(d, NAME, "avd-post02-rdp-v3", "AVD RDP connection on Learn v3")
