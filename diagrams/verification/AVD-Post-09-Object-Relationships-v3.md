# Object relationships (post 9)

Files: `AVD-Post-09-Object-Relationships-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/objects_v3.py`.
Type: Documented relationships (author layout)

Method and limits: each item was checked against the text of the cited Microsoft Learn pages (fetched October 2026) and, where Learn publishes its diagram as SVG, against that SVG's text labels. Learn's pictures were later viewed in a browser on 18 October 2026, see the recheck section. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Azure Virtual Desktop terminology](https://learn.microsoft.com/en-us/azure/virtual-desktop/terminology)
- [Set up Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/environment-setup)

## Explanation
Workspace, application groups, host pool and session hosts, with the user and group assignment on the application group.

## Verification checklist
- [x] An application group belongs to one host pool and can be in one workspace.
- [x] A pooled host pool can have one desktop application group and several RemoteApp application groups.
- [x] RemoteApp application groups need a pooled host pool; desktop groups work with pooled or personal.
- [x] Objects in a workspace share the deployment scope and location.
- [x] Users or user groups are assigned on the application group (role: Desktop Virtualization User).

## Assumptions and design choices (not Learn requirements)
- 'Should share one image' for a pooled host pool is the author's guidance wording.

## Unresolved questions for review
- None known.

## Recheck against Learn's own diagrams, 18 October 2026
The cited pages' text and diagrams were rechecked. These pages have no Learn diagram of this subject, or the diagram is a screenshot, so this drawing is the author's original composition and no Learn layout was copied. See `learn-diagram-notes.md` and `LEARN-RECHECK.md`.
