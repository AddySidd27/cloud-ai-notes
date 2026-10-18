# Three planes (post 8)

Files: `AVD-Post-08-Three-Planes-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/planes_v3.py`.
Type: Author framing built on documented components

Method and limits: each item was checked against the text of the cited Microsoft Learn pages (fetched October 2026) and, where Learn publishes its diagram as SVG, against that SVG's text labels. Learn's pictures were later viewed in a browser on 18 October 2026, see the recheck section. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Azure Virtual Desktop service architecture and resilience](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience)
- [Understanding Azure Virtual Desktop network connectivity](https://learn.microsoft.com/en-us/azure/virtual-desktop/network-connectivity)

## Explanation
The management, control and data planes are the author's framing for troubleshooting. Components inside them come from Learn.

## Verification checklist
- [x] Control plane contains web service, broker, gateway, resource directory and geographical or regional database.
- [x] Documented failure behavior: a database failover briefly fails new connections; a failed gateway instance drops the connections it relays.
- [x] Data plane: RDP over TCP through the gateway by default, or UDP with RDP Shortpath.

## Assumptions and design choices (not Learn requirements)
- The plane names and the 'if it has a problem' notes (other than the two documented behaviors) are the author's reasoning.
- Azure Files and Entra ID or AD DS on the data plane are examples of typical dependencies.

## Unresolved questions for review
- Learn has no diagram of this three-plane split; title says 'the author's framing' to avoid implying otherwise.

## Recheck against Learn's own diagrams, 18 October 2026
Control plane arrows were changed to match Learn's component interconnection picture: web service and broker two-way, gateway and broker dotted two-way, broker to resource directory, broker and database two-way. The three-plane framing and the data plane arrows are the author's, labelled as such.
