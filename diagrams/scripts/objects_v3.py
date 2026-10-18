#!/usr/bin/env python3
"""AVD post 9 (order 109): host pool, application group, workspace relationships. Own layout. Official icons only."""
from common3 import *
NAME = "AVD-Post-09-Object-Relationships-v3"
W, H = 1000, 820
d = D(W, H, "How host pools, application groups and workspaces relate",
 "Original diagram. A workspace at the top lists three application groups: one desktop application group and two RemoteApp application groups. Each application group belongs to exactly one host pool, and here all three belong to one pooled host pool, which contains session hosts. Users and groups from Microsoft Entra ID are assigned to the application groups through the Desktop Virtualization User role. A panel at the bottom lists the rules: an application group has one host pool and one workspace; a host pool has at most one desktop application group and several RemoteApp application groups; RemoteApp application groups need a pooled host pool; objects in a workspace share a deployment scope and location.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 36, "Relationships between the AVD objects", 20, True, "middle", INK)
# Users
d.rect(24, 230, 190, 150, "#f5f5f5", GREYL, 1.5, 8)
d.icon(97, 240, 44, "entid")
d.text(119, 306, "Microsoft Entra ID", 14, True, "middle", INK); d.text(119, 326, "users and user groups", 14, False, "middle", INK)
# workspace
d.rect(300, 70, 560, 90, "#fdf6ec", ORANGE, 1.8, 8)
d.text(580, 105, "Workspace", 17, True, "middle", INK)
d.text(580, 133, "What users see in their client: a list of application groups", 14, False, "middle", INK)
# app groups
ags = [(300, ["Desktop", "application group"]), (480, ["RemoteApp", "application group A"]), (660, ["RemoteApp", "application group B"])]
for x, ls in ags:
    tbox(d, x, 250, 170, 76, ls, "#e8f1fb", BLUE, 14, bold_first=True)
    d.line(x+85, 160, x+85, 250, ORANGE, 3, None, True)
d.text(398, 207, "listed in one workspace", 14, False, "start", ORANGE)
# assignment arrow
d.line(214, 288, 300, 288, PURPLE, 3, None, True)
d.text(257, 270, "Assigned", 14, True, "middle", PURPLE)
d.text(24, 405, "Assignment is on each application group,", 14, False, "start", INK)
d.text(24, 424, "not on the host pool. Role: Desktop", 14, False, "start", INK)
d.text(24, 443, "Virtualization User.", 14, False, "start", INK)
# host pool
d.rect(300, 400, 530, 84, "#eef6ee", GREEN, 1.8, 8)
d.text(565, 435, "Host pool (pooled)", 17, True, "middle", INK)
d.text(565, 462, "A collection of session hosts that should share one image", 14, False, "middle", INK)
for x, _ in ags:
    d.line(x+85, 326, x+85, 400, GREEN, 3, None, True)
d.text(397, 356, "one host pool per", 14, False, "start", GREEN); d.text(397, 375, "application group", 14, False, "start", GREEN)
# session hosts
for i in range(3):
    x = 380 + i*150
    d.icon(x+30, 520, 40, "vm"); d.text(x+50, 584, "Session host", 14, False, "middle", INK)
    d.line(x+50, 484, x+50, 518, GREEN, 3, None, True)
# rules panel
d.rect(24, 620, 952, 180, "#ffffff", GREYL, 1.2, 6)
d.text(40, 648, "Rules", 16, True, "start", INK)
rules = ["An application group belongs to one host pool and can be in one workspace.",
         "A pooled host pool has one desktop application group and can have several RemoteApp application groups.",
         "RemoteApp application groups need a pooled host pool. Desktop groups work with pooled or personal.",
         "A workspace only holds application groups with the same deployment scope and the same location."]
for i, r in enumerate(rules):
    badge(d, 40, 662+i*33, str(i+1), BLUE); d.text(76, 681+i*33, r, 14, False, "start", INK)
finish3(d, NAME, "avd-post09", "Host pool, application group and workspace relationships")
