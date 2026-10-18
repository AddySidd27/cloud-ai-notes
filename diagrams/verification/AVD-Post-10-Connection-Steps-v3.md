# Connection steps (post 10)

Files: `AVD-Post-10-Connection-Steps-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/steps_v3.py`.
Type: Documented sequence (author layout and troubleshooting panel)

Method and limits: each item was checked against the text of the cited Microsoft Learn pages (fetched October 2026) and, where Learn publishes its diagram as SVG, against that SVG's text labels. Learn's pictures were later viewed in a browser on 18 October 2026, see the recheck section. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Understanding Azure Virtual Desktop network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity)
- [Azure Virtual Desktop service architecture and resilience](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience)
- [RDP Shortpath](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-shortpath)

## Explanation
The numbers match the documented client connection sequence. The bottom panel is the author's troubleshooting reading.

## Verification checklist
- [x] Steps 1-2 Entra sign-in, 3-6 feed subscription, 7 gateway via Azure Front Door, 8 gateway to broker, 9 broker to session host agent (persistent channel), 10-11 session host connects to the same gateway, 12 RDP handshake.
- [x] RDP Shortpath is optional direct UDP between client and session host.
- [x] Step 10 is a TLS connection to the same gateway.

## Assumptions and design choices (not Learn requirements)
- Arrow directions follow who initiates each step as the page describes it.
- The 'where a connection stops' panel is explicitly marked as not from Learn.

## Unresolved questions for review
- Learn's step 2-3 wording and the resource directory definition differ on whether the web service uses the resource directory; the diagram avoids drawing it.

## Recheck against Learn's own diagrams, 18 October 2026
Step 9 channel changed to dotted two-way, matching Learn's picture of broker and session host. Numbered steps follow the page text. The optional Shortpath dashed client-to-host line follows the text; Learn's picture has no such direct line (flagged in the RDP record).
