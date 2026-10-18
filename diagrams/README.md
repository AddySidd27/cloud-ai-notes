# Diagram sources and verification

- `scripts/`: Python generators. Each writes the .svg, .drawio and .png into `src/img/avd/`. They import the shared helpers and the official Azure icon set from the author's local tool folder (`/home/claude/blog/tools`), which is not part of this repository.
- `verification/`: one record per diagram with Learn references, an explanation, a checklist, design-choice assumptions and unresolved questions.

Records are the author's check against Microsoft Learn text. They are not Microsoft verification or endorsement.


## Update 18 October 2026: Learn pictures as source of truth
Hub-Spoke, Connections, Components, Feed-Discovery, RDP-Connection and Topology-Choice were redrawn from Learn's own pictures; Planes and Steps arrows were corrected. See `verification/LEARN-RECHECK.md` and `verification/learn-diagram-notes.md`.
The hub-and-spoke figure also has two separate hub-to-hub panels, D for virtual network peering and E for ExpressRoute (Traditional Azure networking topology page). Article figures have a plain "Open full-size diagram" link. These changes and the v3 redraws have had an author check only, not an independent review (see `verification/INDEPENDENT-REVIEW.md`).
