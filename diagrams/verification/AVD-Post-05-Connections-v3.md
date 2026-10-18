# Network connections (post 5)

Files: `AVD-Post-05-Connections-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/conn_v3.py`.
Type: Documented layout

Method and limits: Redrawn on 18 October 2026 from Learn's own picture, viewed in a browser, with the Learn text fetched the same day. Names, links and arrowheads follow the picture. Observations of Learn's pictures are in `learn-diagram-notes.md`. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Understanding Azure Virtual Desktop network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity), azure-virtual-desktop-network-connections.svg

## Explanation
Network connections between client, session host, the AVD infrastructure, Microsoft Entra ID and AD DS.

## Verification checklist (rechecked 18 October 2026 against Learn's own diagrams)
- [x] Names RD Web, RD Gateway and RD Broker inside Azure Virtual Desktop Infrastructure, as in the picture.
- [x] Legend entries match: reverse connect, feed subscription, Entra authentication, RD Agent communication, Active Directory connectivity, Entra Connect sync, internal service traffic.
- [x] Only the client authenticates to Entra ID in the picture; no session host authentication line drawn.
- [x] Sync line arrowhead at AD DS, as in the picture.
- [x] Learn's grey dotted local AD connectivity legend entry is not drawn, as in the picture's lines.

## Assumptions and design choices (not Learn requirements)
- Layout positions and colors are approximations of the picture.

## Unresolved questions for review
- Sync arrow direction: picture arrowhead at AD DS, other Learn text says AD DS to Entra ID. Flagged, not resolved.
- Reverse connect arrow ends: picture arrowheads versus text saying both ends connect outward. Flagged.
