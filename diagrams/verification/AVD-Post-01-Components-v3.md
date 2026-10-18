# Who manages what (post 1)

Files: `AVD-Post-01-Components-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/comp_v3.py`.
Type: Documented layout

Method and limits: Redrawn on 18 October 2026 from Learn's own picture, viewed in a browser, with the Learn text fetched the same day. Names, links and arrowheads follow the picture. Observations of Learn's pictures are in `learn-diagram-notes.md`. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Service architecture and resilience](https://learn.microsoft.com/en-us/azure/virtual-desktop/service-architecture-resilience), components-and-responsibilities.png

## Explanation
Eight boxes in two groups, as Learn draws them.

## Verification checklist (rechecked 18 October 2026 against Learn's own diagrams)
- [x] Microsoft-managed group: Web service, Broker service, Gateway service, Resource directory, Geographical database, Regional database (same order as the picture).
- [x] Customer-managed group: Session hosts, User identities.
- [x] No arrows, no Traffic Manager, no Front Door in the picture, so none drawn.
- [x] Side note on what the customer manages is from the page text, labelled as such.

## Assumptions and design choices (not Learn requirements)
- Colors and brace drawing are the author's.

## Unresolved questions for review
- None found for this diagram.
