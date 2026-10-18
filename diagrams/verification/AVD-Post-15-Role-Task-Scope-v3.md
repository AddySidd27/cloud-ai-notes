# Task, role and scope (post 15)

Files: `AVD-Post-15-Role-Task-Scope-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/roles_v3.py`.
Type: Author decision aid or reference table, no icons (plain workflow).

Method and limits: every claim was checked by a separate reviewer who fetched the cited Microsoft Learn pages in October 2026 without seeing the author's notes. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Built-in roles for AVD](https://learn.microsoft.com/en-us/azure/virtual-desktop/rbac)
- [Entra joined session hosts](https://learn.microsoft.com/en-us/azure/virtual-desktop/azure-ad-joined-session-hosts)

## Verification checklist
- [x] Each of the nine task, role and extra-role pairs matches the RBAC page.
- [x] Virtual Machine User Login is not needed for host pools that use a session host configuration (added).

## Assumptions and design choices (not Learn requirements)
- Row order is the author's.

## Unresolved questions for review
- Portal host pool deployment also needs Application Group Contributor and Workspace Contributor, or Desktop Virtualization Contributor; not shown.
- Session Host Operator adding hosts outside the portal also depends on a valid registration token; not shown.

## Recheck against Learn's own diagrams, 18 October 2026
The cited pages were checked for diagrams. They contain no Learn diagram of this subject (text, tables or portal screenshots only), so this drawing is the author's original composition and no Learn layout was copied. Page text was last checked in October 2026. This is not Microsoft verification.
