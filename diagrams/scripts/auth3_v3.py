#!/usr/bin/env python3
"""AVD post 13 (order 113): three authentication phases and the single sign-on steps. Own layout; follows the three phases named in the authentication article."""
from common3 import *
NAME = "AVD-Post-13-Three-Authentications-v3"
W, H = 1000, 650
d = D(W, H, "The three authentications and the single sign-on steps",
 "Original drawing. Three boxes from left to right joined by arrows. First, cloud service authentication with Microsoft Entra ID, where the client subscribes to the feed, connects to the gateway and sends diagnostics, and where Conditional Access applies. Second, remote session authentication to the session host: with single sign-on the Microsoft Entra token is used, without it the user is prompted on every connection unless credentials are saved, and smart card and Windows Hello for Business use Kerberos and need a domain controller in view or a KDC proxy. Third, in-session authentication to apps and sites, with passwordless through WebAuthn redirection and smart cards through drivers and redirection. A panel below lists the five tasks to enable single sign-on.", marker=True)
d.rect(6, 6, W-12, H-12, "#ffffff", GREYL, 2, 8)
d.text(500, 38, "Three separate authentications on the way to a desktop", 20, True, "middle", INK)
boxes = [
 (30, "1", "Cloud service", BLUE, ["Microsoft Entra ID", "Happens when the client:", "- subscribes to the feed", "- connects to the gateway", "- sends diagnostics", "Conditional Access and MFA", "apply here. With SSO they also", "apply at host sign-in, through", "Windows Cloud Login."]),
 (355, "2", "Remote session", ORANGE, ["Sign-in to the session host", "With SSO: the Entra token is", "used, with no second prompt.", "Without SSO: a prompt on", "every connection, unless", "credentials are saved.", "Smart card and Windows Hello for", "Business use Kerberos; they need", "a domain controller in view, or", "a KDC proxy."]),
 (680, "3", "In-session", GREEN, ["Apps and sites in the desktop", "Passwordless: WebAuthn is", "redirected to the local PC.", "Smart card: drivers on the", "session host, plus smart", "card redirection."]),
]
for x, n, t, col, lines in boxes:
    d.rect(x, 70, 290, 328, "#ffffff", col, 1.8, 8)
    badge(d, x+14, 84, n, col)
    d.text(x+56, 106, t, 16, True, "start", INK)
    for j, l in enumerate(lines):
        d.text(x+16, 146+j*24, l, 14, j == 0, "start", INK)
d.line(320, 234, 355, 234, GREYL, 3, None, True)
d.line(645, 234, 680, 234, GREYL, 3, None, True)
d.rect(30, 412, 940, 214, "#eef6ee", GREEN, 1.5, 8)
d.text(50, 442, "To turn on single sign-on (the five documented tasks, in order)", 16, True, "start", INK)
steps = ["1.  Allow Microsoft Entra authentication for RDP (the Windows Cloud Login application).",
         "2.  Hide the consent prompt by listing session host device groups.",
         "3.  Create a Kerberos server object if Active Directory is part of the environment.",
         "4.  Review your Conditional Access policies.",
         "5.  Set the host pool: Microsoft Entra single sign-on, or enablerdsaadauth set to 1."]
for i, s in enumerate(steps): d.text(50, 474+i*27, s, 14, False, "start", INK)
d.text(50, 612, "Hosts must be Microsoft Entra joined or hybrid joined for this to work.", 14, True, "start", INK)
finish3(d, NAME, "avd-post13", "Three authentications")
