# Independent review (October 2026)

**Scope notice (18 October 2026).** This review covers the earlier (v2) versions of the diagrams, before they were redrawn from Learn's own pictures. The v3 redraws were not independently reviewed. This covers all 16 redrawn diagrams, including the hub-to-hub peering and ExpressRoute panels (D and E) in the hub-and-spoke figure. The v3 diagrams, captions, alt text and the full-size diagram link were checked by the author only. See `LEARN-RECHECK.md` and `learn-diagram-notes.md`. Findings below that name Learn's PNG diagrams as unviewable, or describe the earlier hub-and-spoke example panel, are superseded by the v3 records.

A separate reviewer re-checked the 12 network and architecture diagrams, and a second reviewer the 11 decision and planning diagrams, against Microsoft Learn. Neither saw the author's notes. This is a check against Learn text and SVG labels, not Microsoft verification or endorsement. Learn's own PNG diagrams could not be viewed.

## Fixed after review
- Hybrid architecture: the client arrow ended under the resource directory; it now ends at the service frame. Subscription frame relabelled "Azure subscription (simplified)". Footnote now says Entra joined hosts need no line of sight to domain controllers.
- RDP connection: "closest region" changed to "lowest latency".
- Components: the Entra ID box now reads "User identities and access control" (in Microsoft Entra ID).
- Enforcement points: "no IP address list" replaced by "no IP list to use instead of names; use FQDNs, the FQDN tag or the service tag".
- Hub and spoke: "Azure DNS Private Resolver (optional)".
- Connections: footer now lists RDP Shortpath (UDP), Private Link and domain join ports as left out.
- Connection steps: "public cloud" added to the Front Door step; "opened by the agent" added to the persistent channel.
- Three planes: author's view tags on the two unsourced notes.
- Object relationships: assignment note now says each application group.
- Kerberos: added that session hosts need no line of sight to AD DS.
- Batch C: Azure Local join wording, Windows 365 network costs, personal hosts, Conditional Access at host sign-in, VM User Login not needed with a session host configuration.

## Not changed, for the owner's decision
- Hub and spoke: "spokes are not peered to each other" stays in the example panel. The CAF AVD scenario states it, but Learn marks that page for removal on 30 October 2026.
- Connections: the gateway and broker "internal service traffic" arrow is bidirectional, taken from Learn's SVG label; Learn text only says the gateway connects to the broker.
- Topology choice: "hub connections" arrows are one-way and the session host plus private endpoint subnet layout is an example; Learn states neither.
- Enforcement points: Private Link ports (TCP 1-65535 to the connection endpoint) are not drawn.
- Citrix DaaS and Omnissa Horizon Cloud (post 7), Compute Gallery replication and PerfMon (post 6) have no supporting Learn page found.
- Learn wording differs between pages ("web service" vs "feed subscription service").
