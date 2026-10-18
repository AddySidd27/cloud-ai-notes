#!/usr/bin/env python3
"""AVD post 15 (order 115): task to role to scope map. Own layout (documentation has role tables, no diagram)."""
from common3 import *
NAME = "AVD-Post-15-Role-Task-Scope-v3"
W, H = 1000, 820
d = D(W, H, "Which built-in role fits which task, and where to assign it",
 "Original table-style drawing, nine rows with three columns: task, built-in role, and scope or extra role needed. Signing users out: Desktop Virtualization User Session Operator on specific host pools. Draining and removing session hosts: Session Host Operator, plus Virtual Machine Contributor to add hosts outside the portal. Managing a host pool: Host Pool Contributor, plus Virtual Machine Contributor to create virtual machines. Publishing apps: Application Group Contributor, plus User Access Administrator to assign users. Managing a workspace: Workspace Contributor, plus Application Group Reader to see apps. Managing everything in AVD: Desktop Virtualization Contributor, plus User Access Administrator for assignments. Viewing only: Desktop Virtualization Reader. Using a desktop or app: Desktop Virtualization User on the application group. Signing in to Microsoft Entra joined virtual machines: Virtual Machine User Login on the VMs, resource group or subscription.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 38, "Task, role and scope", 20, True, "middle", INK)
for x, t in [(40, "Task"), (350, "Built-in role"), (700, "Scope or extra role")]:
    d.text(x, 78, t, 15, True, "start", GREYL)
rows = [
 (["Sign users out, send messages"], ["Desktop Virtualization", "User Session Operator"], ["Assign on specific host pools"], ORANGE),
 (["Drain, view and remove", "session hosts"], ["Desktop Virtualization", "Session Host Operator"], ["Add VM Contributor to add", "hosts outside the portal"], ORANGE),
 (["Manage one host pool"], ["Desktop Virtualization", "Host Pool Contributor"], ["Add VM Contributor to", "create virtual machines"], BLUE),
 (["Publish apps, manage", "application groups"], ["Desktop Virtualization Application", "Group Contributor"], ["Add User Access Administrator", "to assign users"], BLUE),
 (["Manage a workspace"], ["Desktop Virtualization", "Workspace Contributor"], ["Add Application Group Reader", "to see the apps in it"], BLUE),
 (["Manage all AVD resources"], ["Desktop Virtualization", "Contributor"], ["Not user assignment. Add", "User Access Administrator."], PURPLE),
 (["View only"], ["Desktop Virtualization", "Reader"], ["Any scope you choose"], GREEN),
 (["Use a desktop or app"], ["Desktop Virtualization", "User"], ["On the application group"], GREEN),
 (["Sign in to a Microsoft", "Entra joined VM"], ["Virtual Machine", "User Login"], ["VMs, resource group or subscription.", "Not needed with session host config."], GREEN),
]
y0 = 92; step = 80
for i, (tk, ro, sc, col) in enumerate(rows):
    y = y0 + i*step
    d.rect(30, y, 290, 66, "#e8f1fb", BLUE, 1.5, 8)
    top = y + 33 - (len(tk)-1)*11
    for j, l in enumerate(tk): d.text(175, top+j*22+5, l, 14, False, "middle", INK)
    d.line(320, y+33, 340, y+33, GREYL, 3, None, True)
    d.rect(340, y, 330, 66, "#ffffff", col, 1.8, 8)
    top = y + 33 - (len(ro)-1)*11
    for j, l in enumerate(ro): d.text(505, top+j*22+5, l, 14, True, "middle", INK)
    d.line(670, y+33, 690, y+33, GREYL, 3, None, True)
    d.rect(690, y, 280, 66, "#ffffff", GREYL, 1.5, 8)
    top = y + 33 - (len(sc)-1)*11
    for j, l in enumerate(sc): d.text(830, top+j*22+5, l, 14, False, "middle", INK)
finish3(d, NAME, "avd-post15", "Role task scope")
