# Apps and policies (post 14): checked, unchanged

Files: `AVD-Post-14-Apps-And-Policies` (.png, .svg, .drawio) in `src/img/avd/`.
Type: Author decision aid or reference table, no icons (plain workflow).

Method and limits: every claim was checked by a separate reviewer who fetched the cited Microsoft Learn pages in October 2026 without seeing the author's notes. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Conditional Access and MFA](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa)

## Verification checklist
- [x] AVD app covers subscribe, gateway and diagnostics; do not use 'Every time' on it.
- [x] Windows Cloud Login: same users and grant, frequency matches or exceeds policy 1, 'Every time' allowed.
- [x] Do not add the AVD Azure Resource Manager Provider app to any policy.
- [x] Do not block the Windows 365 app; it breaks AVD sign-in too.
- [x] Disable per-user MFA and use Conditional Access only.

## Assumptions and design choices (not Learn requirements)
- Existing image kept.

## Unresolved questions for review
- None known.

## Recheck, 18 October 2026
This diagram was not changed in the Learn recheck pass. Its earlier record stands, and it was not re-compared against a Learn picture in this pass.
