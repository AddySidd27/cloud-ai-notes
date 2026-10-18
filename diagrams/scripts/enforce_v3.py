#!/usr/bin/env python3
"""AVD post 16 (order 116): where the controls sit on the connectivity path. Own layout; the documentation Private Link diagram is not reproduced."""
from common3 import *
NAME = "AVD-Post-16-Enforcement-Points-v3"
W, H = 1000, 810
d = D(W, H, "Where the network controls sit on the connectivity path",
 "Original drawing. At the top, the Microsoft-run Azure Virtual Desktop service reached on TCP 443 by name, with no IP address list to allow in place of names. On the left, a user device behind a firewall or proxy on the client network connects up to the service. On the right, a session host behind its subnet controls, which are network security group rules, a route table and a firewall or proxy, connects outbound to the service. At the bottom left, an optional Private Link panel lists the private endpoints and DNS zones. At the bottom right, a red panel says the Azure platform addresses 168.63.129.16 and 169.254.169.254 must not be proxied, intercepted or sent through VPN tunnels.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 38, "Where the controls sit", 20, True, "middle", INK)
# service
d.rect(300, 70, 400, 130, "#e8f1fb", BLUE, 1.8, 8)
d.text(500, 108, "Azure Virtual Desktop service (Microsoft-run)", 15, True, "middle", INK)
d.text(500, 134, "Feed, gateway and broker, reached by name", 14, False, "middle", INK)
d.text(500, 158, "on TCP 443. There is no IP list to use instead of names.", 14, False, "middle", INK)
d.text(500, 182, "Use FQDNs, the FQDN tag or the service tag.", 14, False, "middle", INK)
# client
d.rect(30, 310, 190, 130, "#ffffff", GREEN, 1.8, 8)
d.icon(95, 318, 40, "dev"); d.text(125, 392, "User device", 14, True, "middle", INK); d.text(125, 414, "(client app)", 14, False, "middle", INK)
d.rect(30, 230, 190, 60, "#fff7e8", ORANGE, 1.8, 8)
d.text(125, 256, "Client network:", 14, True, "middle", INK); d.text(125, 276, "firewall or proxy", 14, False, "middle", INK)
d.line(125, 310, 125, 290, GREYL, 3, None, False)
d.line(220, 250, 300, 170, ORANGE, 3, None, True)
# session host
d.rect(570, 280, 400, 230, "#ffffff", GREEN, 1.8, 8)
d.text(770, 306, "Session host subnet", 15, True, "middle", INK)
d.icon(675, 320, 40, "vm"); d.text(770, 382, "Session host (your VM)", 14, True, "middle", INK)
d.rect(590, 402, 360, 88, "#fff7e8", ORANGE, 1.5, 6)
d.text(770, 428, "Controls on the outbound path:", 14, True, "middle", INK)
d.text(770, 450, "network security group rules,", 14, False, "middle", INK)
d.text(770, 472, "route table, firewall or proxy", 14, False, "middle", INK)
d.line(770, 280, 650, 200, GREEN, 3, None, True)
d.text(790, 250, "outbound only", 14, False, "start", INK)
# private link
d.rect(30, 540, 500, 240, "#f1ecf7", PURPLE, 1.8, 8)
d.icon(168, 548, 28, "plink"); d.text(204, 568, "Optional: Private Link", 15, True, "start", PURPLE)
for i, l in enumerate(["Private endpoints in your network:", "- global: one for the whole deployment", "- feed: one per workspace", "- connection: one per host pool", "Private DNS zones:", "privatelink-global.wvd.microsoft.com", "privatelink.wvd.microsoft.com"]):
    d.text(50, 600+i*24, l, 14, i in (0, 4), "start", INK)
# platform addresses
d.rect(560, 540, 410, 240, "#fdf0ec", RED, 1.8, 8)
d.text(765, 568, "Azure platform addresses", 15, True, "middle", RED)
for i, l in enumerate(["169.254.169.254: instance metadata (IMDS)", "168.63.129.16: platform health, DNS, DHCP", "Must not be proxied, intercepted or", "sent through VPN tunnels. Blocking them", "causes provisioning and health problems."]):
    d.text(765, 606+i*26, l, 14, i == 0, "middle", INK)
finish3(d, NAME, "avd-post16", "Enforcement points")
