# The RDP connection (post 2, figure 3)

Files: `AVD-Post-02-RDP-Connection-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/rdp_v3.py`.
Type: Documented flow

Method and limits: Redrawn on 18 October 2026 from Learn's own picture, viewed in a browser, with the Learn text fetched the same day. Names, links and arrowheads follow the picture. Observations of Learn's pictures are in `learn-diagram-notes.md`. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Service architecture and resilience](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience), rdp-connection.svg
- [RDP Shortpath](https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-shortpath)

## Explanation
How the RDP connection is made, TCP through the gateway or UDP RDP Shortpath.

## Verification checklist (rechecked 18 October 2026 against Learn's own diagrams)
- [x] Client two-way Azure Front Door; Front Door two-way TCP to Gateway service.
- [x] Region 1 box holds Gateway service, Broker service, Session host, and both Shortpath boxes (managed, public).
- [x] Gateway to Broker and Broker to Session host are dotted and two-way.
- [x] Gateway two-way Session host over TCP.
- [x] UDP lines from the client to both Shortpath boxes and the session host, and from the session host to both Shortpath boxes.

## Assumptions and design choices (not Learn requirements)
- Box sizes and positions are the author's.

## Unresolved questions for review
- Learn's picture has no direct client-to-session-host line, while the text says Shortpath bypasses the gateway. Flagged, not resolved.
- Whether Front Door sits outside Region 1 by design or by drawing convenience is not stated.
