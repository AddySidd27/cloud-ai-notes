# Client by device (post 12): checked, unchanged

Files: `AVD-Post-12-Client-By-Device` (.png, .svg, .drawio) in `src/img/avd/`.
Type: Author decision aid or reference table, no icons (plain workflow).

Method and limits: every claim was checked by a separate reviewer who fetched the cited Microsoft Learn pages in October 2026 without seeing the author's notes. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Connect with Windows App or Remote Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/users/connect-windows)
- [Prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)
- [Windows App overview](https://learn.microsoft.com/en-us/windows-app/overview)

## Verification checklist
- [x] MSI client unsupported in public cloud since March 27, 2026; Store app support ended September 2025.
- [x] macOS and iOS/iPadOS Remote Desktop clients replaced by Windows App.
- [x] RADC and mstsc.exe are not supported for AVD.
- [x] Meta Quest is a Windows App platform; one Learn page labels it preview.

## Assumptions and design choices (not Learn requirements)
- Existing image kept; it is labelled 'as the documentation reads at the time of checking'.

## Unresolved questions for review
- Date-sensitive: Learn gave Sept 28, 2026 support for Azure Government, 21Vianet and AVD Classic; that date has passed. The diagram is about public cloud. Re-check before each republish.

## Recheck, 18 October 2026
This diagram was not changed in the Learn recheck pass. Its earlier record stands, and it was not re-compared against a Learn picture in this pass.
