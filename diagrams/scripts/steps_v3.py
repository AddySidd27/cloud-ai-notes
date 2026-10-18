#!/usr/bin/env python3
"""AVD post 10 (order 110): connection sequence with documented step numbers. Own layout, based on the numbered sequence in the network connectivity article."""
from common3 import *
NAME = "AVD-Post-10-Connection-Steps-v3"
W, H = 1000, 860
d = D(W, H, "The connection sequence, step by step",
 "Original diagram using the numbered steps of the client connection sequence. Steps 1 and 2: the client signs in to Microsoft Entra ID and gets a token. Steps 3 to 6: the client passes the token to the feed service and receives a signed connection configuration. Step 7: the client opens a TLS connection to a gateway through Azure Front Door. Step 8: the gateway asks the broker to orchestrate. Step 9: the broker uses the persistent channel to tell the session host. Steps 10 and 11: the session host opens an outbound connection to the same gateway, which relays traffic. Step 12: the RDP handshake starts. A dashed line shows the optional RDP Shortpath UDP path directly between client and session host. A panel lists where a connection stops for each group of steps.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 36, "A connection, step by step (numbers match the documented sequence)", 19, True, "middle", INK)
def pill(cx, cy, t, col):
    w = max(30, tw(t, 14, True)+16)
    d.rect(cx-w/2, cy-14, w, 28, col, col, 1, 14); d.text(cx, cy+5, t, 14, True, "middle", "#ffffff")
# Nodes
d.rect(30, 270, 180, 130, "#ffffff", GREEN, 1.6, 8)
d.icon(100, 278, 40, "dev"); d.text(120, 342, "User device", 14, True, "middle", INK); d.text(120, 362, "(Windows App)", 14, False, "middle", INK)
d.rect(330, 70, 190, 100, "#e8f1fb", BLUE, 1.6, 8)
d.icon(400, 76, 40, "entid"); d.text(425, 140, "Microsoft Entra ID", 14, True, "middle", INK)
d.rect(650, 70, 200, 100, "#e8f1fb", BLUE, 1.6, 8)
d.text(750, 100, "Feed subscription", 14, True, "middle", INK); d.text(750, 120, "service", 14, True, "middle", INK); d.text(750, 145, "(Microsoft-managed)", 13, False, "middle", INK)
d.rect(330, 270, 190, 130, "#e8f1fb", BLUE, 1.6, 8)
d.text(425, 318, "Gateway service", 14, True, "middle", INK); d.text(425, 340, "(entered through", 14, False, "middle", INK); d.text(425, 358, "Azure Front Door;", 14, False, "middle", INK); d.text(425, 376, "public cloud)", 14, False, "middle", INK)
d.rect(650, 270, 200, 130, "#e8f1fb", BLUE, 1.6, 8)
d.text(750, 340, "Broker service", 14, True, "middle", INK)
d.rect(650, 520, 200, 120, "#ffffff", GREEN, 1.6, 8)
d.icon(730, 526, 40, "vm"); d.text(750, 590, "Session host", 14, True, "middle", INK); d.text(750, 610, "(your VM)", 14, False, "middle", INK)
# Arrows
d.line(210, 285, 330, 125, ORANGE, 3, None, True); pill(262, 215, "1-2", ORANGE)
d.line(210, 300, 650, 125, ORANGE, 3, None, True); pill(600, 145, "3-6", ORANGE)
d.line(210, 335, 330, 335, ORANGE, 3, None, True); pill(270, 318, "7", ORANGE)
d.line(520, 335, 650, 335, BLUE, 3, None, True); pill(585, 318, "8", BLUE)
d.line(750, 400, 750, 520, BLUE, 3, "8 5", True); d.line(750, 520, 750, 400, BLUE, 3, "8 5", True); pill(750, 460, "9", BLUE)
d.text(766, 495, "persistent channel", 14, False, "start", INK); d.text(766, 513, "(opened by the agent)", 14, False, "start", INK)
d.line(650, 560, 480, 400, GREEN, 3, None, True); pill(565, 480, "10-11", GREEN)
pill(280, 445, "12", GREEN); d.text(306, 450, "RDP handshake starts", 14, False, "start", INK)
# shortpath dashed
d.line(120, 400, 120, 580, GREEN, 3, "10 6", False); d.line(120, 580, 650, 580, GREEN, 3, "10 6", True)
d.text(140, 610, "Optional: RDP Shortpath, direct UDP between", 14, False, "start", INK)
d.text(140, 630, "client and session host (dashed)", 14, False, "start", INK)
# panel
d.rect(24, 670, 952, 170, "#ffffff", GREYL, 1.2, 6)
d.text(40, 697, "Where a connection stops (the author's troubleshooting reading, not from Learn)", 15, True, "start", INK)
rows = [("1-2", "Cannot sign in: wrong account, Conditional Access or a blocked sign-in endpoint."),
        ("3-6", "Signed in but the feed is empty or wrong: assignment, workspace or group type."),
        ("7-9", "Desktop listed but no host starts: no available host, gateway or broker path."),
        ("10-11", "Long wait, then a generic error: host outbound access, proxy or TLS inspection."),
        ("After 12", "Opens, then drops, is slow or choppy: Windows sign-in, profile, network or TCP fallback.")]
for i, (k, t) in enumerate(rows):
    d.text(40, 724+i*22, k, 14, True, "start", ORANGE); d.text(120, 724+i*22, t, 14, False, "start", INK)
finish3(d, NAME, "avd-post10", "AVD connection sequence")
