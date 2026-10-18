# OS and license questions (post 11)

Files: `AVD-Post-11-OS-And-License-Choice-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/os_v3.py`.
Type: Author decision aid or reference table, no icons (plain workflow).

Method and limits: every claim was checked by a separate reviewer who fetched the cited Microsoft Learn pages in October 2026 without seeing the author's notes. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)
- [Licensing](https://learn.microsoft.com/en-us/azure/virtual-desktop/licensing)
- [Apply a Windows license](https://learn.microsoft.com/en-us/azure/virtual-desktop/apply-windows-license)
- [AVD Hybrid](https://learn.microsoft.com/en-us/azure/virtual-desktop/hybrid-overview)
- [Azure Local](https://learn.microsoft.com/en-us/azure/virtual-desktop/azure-stack-hci-overview)

## Verification checklist
- [x] Multi-session needs an eligible per-user license; Windows Server uses RDS CAL with Software Assurance or RDS user subscription licenses.
- [x] Per-user access pricing is not available for Windows Server.
- [x] Windows Server session hosts cannot be Entra joined and enrolled in Intune; use hybrid join and Group Policy.
- [x] AVD Hybrid does not support Windows multi-session.
- [x] Portal-created Windows client hosts get the license set; Windows Server hosts might get an incorrect license type.

## Assumptions and design choices (not Learn requirements)
- Row layout is the author's.

## Unresolved questions for review
- Azure Local join: the prerequisites page says AD DS only; the Azure Local page says the portal is limited to AD DS while PowerShell and other methods support native Entra join. The diagram uses the more detailed wording; confirm which is current.

## Recheck against Learn's own diagrams, 18 October 2026
The cited pages were checked for diagrams. They contain no Learn diagram of this subject (text, tables or portal screenshots only), so this drawing is the author's original composition and no Learn layout was copied. Page text was last checked in October 2026. This is not Microsoft verification.
