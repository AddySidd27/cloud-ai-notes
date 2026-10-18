#!/usr/bin/env python3
"""AVD post 11 (order 111): OS and license decision aid, own layout (no documentation diagram exists)."""
from common3 import *
NAME = "AVD-Post-11-OS-And-License-Choice-v3"
W, H = 1000, 770
d = D(W, H, "Questions that decide the session host operating system and license",
 "Original decision aid with four questions from top to bottom. Question 1: do several users share one virtual machine? If yes, use Windows 11 Enterprise multi-session with an eligible per-user license, or Windows Server with an RDS client access license that has Software Assurance or RDS user subscription licenses. If no, use Windows 11 Enterprise single session. Question 2: are the users internal or external customers? Internal users need an eligible license. External commercial use needs per-user access pricing, which is not available for Windows Server. Question 3: will you manage hosts with Intune? Windows Server cannot be enrolled in Intune, so use hybrid join and Group Policy. Question 4: where do the hosts run? On Azure Local the hosts join Active Directory Domain Services only. In Azure Virtual Desktop Hybrid, multi-session is not supported. A final box says to apply the Windows license to the virtual machine and confirm activation.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 38, "Questions that decide the operating system and license", 20, True, "middle", INK)
d.text(250, 74, "Question", 15, True, "middle", GREYL); d.text(760, 74, "What the documentation says follows", 15, True, "middle", GREYL)
qs = [
 ("1", ["Do several users share", "one virtual machine?"], "Yes", ["Windows 11 Enterprise multi-session", "(per-user license), or Windows Server", "(RDS CAL with Software Assurance,", "or RDS user subscription licenses)"], BLUE),
 ("2", ["Are the users employees and", "contractors, or paying customers?"], "Paying", ["Paying customers: per-user access pricing,", "Windows client only, not Windows Server.", "Employees and contractors: an eligible license."], PURPLE),
 ("3", ["Will you manage the", "hosts with Intune?"], "Server", ["Windows Server cannot be enrolled", "in Intune. Use hybrid join and", "Group Policy instead."], ORANGE),
 ("4", ["Where will the", "hosts run?"], "Local", ["Azure Local: the portal joins hosts", "to AD DS only (PowerShell can Entra join).", "AVD Hybrid: no multi-session."], RED),
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
        d.text(262, y+100+34, "Then ask the next question", 14, False, "start", GREYL)
yf = y0 + 3*step + 100
d.line(250, yf, 250, yf+34, GREYL, 3, None, True)
d.rect(30, yf+36, 940, 58, "#eef6ee", GREEN, 1.5, 8)
d.text(500, yf+60, "Apply the Windows license to the VM and confirm the OS is activated", 15, True, "middle", INK)
d.text(500, yf+82, "Windows client hosts made in the portal get the license set; Windows Server hosts might get a wrong type.", 14, False, "middle", INK)
finish3(d, NAME, "avd-post11", "OS and license choice")
