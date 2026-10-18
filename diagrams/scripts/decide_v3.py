#!/usr/bin/env python3
"""AVD post 7 (order 107): decision aid, own layout. No Learn diagram of this decision exists."""
from common3 import *
NAME = "AVD-Post-07-Decision-Questions-v3"
W, H = 1000, 770
d = D(W, H, "Questions to ask when choosing a virtual desktop option",
 "Original decision aid. Four questions are asked from top to bottom. Question 1: do users need Windows desktops or apps that run centrally? If no, another approach may be simpler. Question 2: must the session hosts stay in your own datacenter? If yes, look at Azure Virtual Desktop Hybrid or Azure Virtual Desktop for Azure Local. Question 3: do you need a platform from Citrix or Omnissa? If yes, look at Citrix DaaS or Omnissa Horizon Cloud on Azure. Question 4: is one dedicated Cloud PC per user, run by Microsoft, enough? If yes, look at Windows 365. If no, look at Azure Virtual Desktop with shared multi-session hosts.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 38, "Questions to ask, in order", 20, True, "middle", INK)
d.text(250, 74, "Question", 15, True, "middle", GREYL); d.text(760, 74, "If the answer points here", 15, True, "middle", GREYL)
qs = [
 ("1", ["Do users need Windows desktops", "or apps that run centrally?"], "No", ["Another approach may be simpler,", "for example a managed laptop", "with the app installed"], RED),
 ("2", ["Must the session hosts stay", "in your own datacenter?"], "Yes", ["Azure Virtual Desktop Hybrid, or", "Azure Virtual Desktop for Azure Local", "(hosts on premises, service in Azure)"], PURPLE),
 ("3", ["Do you need a platform", "from Citrix or Omnissa?"], "Yes", ["Citrix DaaS, or Omnissa Horizon Cloud", "on Azure (not covered in this series)"], PURPLE),
 ("4", ["Is one dedicated Cloud PC per user,", "run by Microsoft, enough?"], "Yes", ["Windows 365", "(one Cloud PC per user, fixed", "monthly fee; network costs may apply)"], GREEN),
]
y0 = 92; step = 152
for i, (n, ql, ans, ol, col) in enumerate(qs):
    y = y0 + i*step
    d.rect(30, y, 440, 100, "#e8f1fb", BLUE, 1.5, 8)
    badge(d, 42, y+37, n, BLUE)
    for j, l in enumerate(ql): d.text(84, y+44+j*22, l, 15, False, "start", INK)
    d.line(470, y+50, 520, y+50, col, 3, None, True)
    d.text(495, y+38, ans, 14, True, "middle", col)
    d.rect(530, y, 440, 100, "#ffffff", col, 1.5, 8)
    top = y + 50 - (len(ol)-1)*11
    for j, l in enumerate(ol): d.text(750, top+j*22+5, l, 14, j == 0, "middle", INK)
    if i < 3:
        d.line(250, y+100, 250, y+step, GREYL, 3, None, True)
        d.text(262, y+100+34, "Otherwise, continue", 14, False, "start", GREYL)
# final
yf = y0 + 3*step + 100
d.line(250, yf, 250, yf+34, GREYL, 3, None, True)
d.text(262, yf+22, "No", 14, True, "start", GREYL)
d.rect(30, yf+36, 940, 58, "#eef6ee", GREEN, 1.5, 8)
d.text(500, yf+60, "Azure Virtual Desktop in Azure: pooled or personal hosts, your own images, autoscale", 15, True, "middle", INK)
d.text(500, yf+82, "You operate the images, session hosts, profiles and network; Microsoft operates the service.", 14, False, "middle", INK)
finish3(d, NAME, "avd-post07", "Questions to ask when choosing a virtual desktop option")
