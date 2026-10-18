#!/usr/bin/env python3
"""AVD post 4: Azure Files with Microsoft Entra Kerberos, hybrid users. Original layout; official icons only."""
src = open("/home/claude/blog/tools/build_diagrams.py", encoding="utf-8").read().split("def cap(")[0]
exec(src)
exec(open("/home/claude/blog/tools/diag_helpers.py", encoding="utf-8").read())
import sys; sys.path.insert(0, ".")
from common3 import OUTD, render_png
NAME = "AVD-Post-04-Entra-Kerberos-v3"
ICONS.update({"files": "storage/10400-icon-service-Azure-Fileshares.svg",
              "vm": "compute/10021-icon-service-Virtual-Machine.svg",
              "dev": "intune/10332-icon-service-Devices.svg"})
W, H = 1000, 925
d = D(W, H, "Azure Files with Microsoft Entra Kerberos: hybrid users",
 "Not an official Microsoft diagram. Domain controllers in on-premises Active Directory synchronize identities to Microsoft Entra ID. Numbered setup steps: 1 enable Microsoft Entra Kerberos on the storage account, 2 assign a share-level role, 3 set folder and file permissions from a device with connectivity to AD DS, 4 enable cloud Kerberos ticket retrieval on the session hosts. At sign-in, lettered steps: A the session host retrieves a cloud Kerberos ticket from Microsoft Entra ID, B the session host uses Kerberos tickets from Microsoft Entra ID to access the share over SMB. A final note says to exclude the storage account's Entra app from MFA Conditional Access policies.", marker=True)
RED = "#b42318"; INK = "#1f2933"; BLUE = "#3b6fb6"; ORANGE = "#c2570c"; GREYL = "#5f6b7a"; GREEN = "#3c8d40"
def badge(x, y, t, col):
    d.rect(x, y, 26, 26, col, col, 1, 13); d.text(x+13, y+19, t, 14, True, "middle", "#ffffff")
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 38, "Azure Files with Microsoft Entra Kerberos: hybrid users", 20, True, "middle", INK)
# AD DS
d.rect(30, 100, 220, 110, "#f5f5f5", GREYL, 1.5, 8)
d.text(140, 148, "Domain controllers", 14, True, "middle", INK); d.text(140, 168, "(on-premises AD DS)", 14, False, "middle", INK)
# Entra ID
d.rect(380, 100, 200, 120, "#e8f1fb", BLUE, 1.5, 8)
d.icon(455, 108, 50, "entid"); d.text(480, 182, "Microsoft", 14, True, "middle", INK); d.text(480, 201, "Entra ID", 14, True, "middle", INK)
d.line(250, 155, 380, 155, GREYL, 2.5, "3 4", True)
d.text(315, 118, "Identity", 14, False, "middle", INK); d.text(315, 135, "sync", 14, False, "middle", INK)
# Azure Files
d.rect(730, 400, 240, 130, "#eef6ee", GREEN, 1.5, 8)
d.icon(830, 408, 44, "files"); d.text(850, 478, "Azure Files share", 14, True, "middle", INK); d.text(850, 497, "(storage account)", 14, False, "middle", INK)
badge(740, 410, "1", GREEN); badge(740, 442, "2", GREEN)
# Session hosts
d.rect(380, 400, 200, 130, "#ffffff", GREYL, 1.5, 8)
d.icon(460, 408, 40, "vm"); d.text(480, 474, "Session hosts", 14, True, "middle", INK); d.text(480, 493, "(hybrid users)", 14, False, "middle", INK); d.text(480, 512, "Entra joined or hybrid joined", 13, False, "middle", INK)
badge(390, 410, "4", BLUE)
# A and B
d.line(480, 400, 480, 220, ORANGE, 3, None, True)
badge(494, 290, "A", ORANGE); d.text(528, 303, "Gets a cloud Kerberos", 14, False, "start", INK); d.text(528, 321, "ticket at sign-in", 14, False, "start", INK)
d.line(580, 465, 730, 465, ORANGE, 3, None, True)
badge(595, 420, "B", ORANGE); d.text(594, 495, "Uses the tickets", 14, False, "start", INK); d.text(594, 512, "to reach the share", 14, False, "start", INK); d.text(594, 529, "over SMB", 14, False, "start", INK)
d.text(480, 560, "Session hosts need no line of sight to AD DS", 14, False, "middle", INK)
# ACL client
d.rect(30, 590, 220, 110, "#ffffff", GREYL, 1.5, 8)
d.icon(120, 596, 36, "dev"); d.text(140, 656, "Device used to set", 14, True, "middle", INK); d.text(140, 675, "folder permissions", 14, True, "middle", INK)
d.line(250, 645, 850, 645, BLUE, 3, None, False); d.line(850, 645, 850, 532, BLUE, 3, None, True)
badge(262, 604, "3", BLUE); d.text(298, 622, "Sets folder and file permissions (ACLs)", 14, False, "start", INK)
d.line(140, 590, 140, 212, GREYL, 2.5, "8 5", True)
d.text(152, 300, "Needs unimpeded network", 14, False, "start", INK); d.text(152, 318, "connectivity to AD DS", 14, False, "start", INK)
# steps panel
d.rect(20, 720, 960, 190, "#ffffff", GREYL, 1, 6)
d.text(36, 746, "Setup steps (once) and sign-in steps (each time)", 14, True, "start", INK)
rows = [("1", GREEN, "Enable Microsoft Entra Kerberos on the storage account and grant admin consent to the app it creates."),
        ("2", GREEN, "Assign a share-level Azure role to the synced user or group."),
        ("3", BLUE, "Set folder and file permissions (ACLs) from a device that can reach AD DS."),
        ("4", BLUE, "Turn on cloud Kerberos ticket retrieval on the session hosts (CloudKerberosTicketRetrievalEnabled)."),
        ("A", ORANGE, "At sign-in, the session host retrieves a cloud Kerberos ticket from Microsoft Entra ID."),
        ("B", ORANGE, "The session host uses Kerberos tickets from Microsoft Entra ID to access the share over SMB."),
        ("!", RED, "Exclude the storage account's Entra app from Conditional Access policies that require MFA for all apps.")]
for i, (n, c, t) in enumerate(rows):
    y = 760+i*20
    badge(36, y-6, n, c) if False else None
    d.text(40, y+14, n, 14, True, "start", c); d.text(64, y+14, t, 14, False, "start", INK)
check(d, "avd04")
svg = d.svg().replace('markerWidth="8" markerHeight="8"', 'markerWidth="4" markerHeight="4"')
open(OUTD+NAME+".svg", "w", encoding="utf-8").write(svg)
open(OUTD+NAME+".drawio", "w", encoding="utf-8").write(d.drawio("avd-post04-v3", "Entra Kerberos hybrid path v3"))
render_png(OUTD+NAME+".svg", OUTD+NAME+".png", d.w, d.h)
