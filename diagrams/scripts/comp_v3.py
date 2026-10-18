#!/usr/bin/env python3
"""AVD post 1: who manages what, following the stacked layout of components-and-responsibilities.png on the Learn page AVD service architecture and resilience."""
from common3 import *
NAME = "AVD-Post-01-Components-v3"
W, H = 1000, 520
d = D(W, H, "Who manages what in Azure Virtual Desktop",
 "Not an official Microsoft diagram. A stack of eight labelled boxes with two braces, following the layout of the Learn diagram. Microsoft-managed, six boxes: web service, broker service, gateway service, resource directory, geographical database and regional database. Customer-managed, two boxes: session hosts and user identities. The right side adds notes taken from the text of the same Learn page about what the customer manages for session hosts and user identities. The diagram shows no connections between components.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 38, "Who manages what in Azure Virtual Desktop", 20, True, "middle", INK)
d.text(500, 62, "Same two groups and eight components as the Learn diagram. No links are drawn between them.", 14, False, "middle", INK)
ms = ["Web service", "Broker service", "Gateway service", "Resource directory", "Geographical database", "Regional database"]
for i, t in enumerate(ms):
    tbox(d, 40, 90+i*50, 300, 42, [t], "#2e7a94", "#2e7a94", 14, bold_all=True, color="#ffffff")
cm = ["Session hosts", "User identities"]
for i, t in enumerate(cm):
    tbox(d, 40, 400+i*50, 300, 42, [t], "#d6eaf2", "#8cbfd3", 14, bold_all=True)
d.line(356, 92, 372, 92, "#2e7a94", 3); d.line(372, 92, 372, 382, "#2e7a94", 3); d.line(356, 382, 372, 382, "#2e7a94", 3)
d.line(372, 237, 392, 237, "#2e7a94", 3)
d.text(402, 243, "Microsoft-managed", 16, True, "start", INK)
d.line(356, 402, 372, 402, "#8cbfd3", 3); d.line(372, 402, 372, 492, "#8cbfd3", 3); d.line(356, 492, 372, 492, "#8cbfd3", 3)
d.line(372, 447, 392, 447, "#8cbfd3", 3)
d.text(402, 453, "Customer-managed", 16, True, "start", INK)
d.rect(600, 380, 380, 120, "#ffffff", GREYL, 1.2, 6)
d.text(612, 402, "From the text of the same page", 13, True, "start", INK)
for i, t in enumerate(["Session hosts: image and applications,", "network connectivity, resiliency, backup", "User identities: you manage, in Entra ID"]):
    d.text(612, 424+i*22, t, 13, False, "start", INK)
finish3(d, NAME, "avd-post01-comp", "AVD who manages what")
