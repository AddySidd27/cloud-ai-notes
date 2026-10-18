# Three authentications (post 13)

Files: `AVD-Post-13-Three-Authentications-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/auth3_v3.py`.
Type: Author decision aid or reference table, no icons (plain workflow).

Method and limits: every claim was checked by a separate reviewer who fetched the cited Microsoft Learn pages in October 2026 without seeing the author's notes. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Authentication in Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/authentication)
- [Configure single sign-on](https://learn.microsoft.com/en-us/azure/virtual-desktop/configure-single-sign-on)
- [Conditional Access and MFA](https://learn.microsoft.com/en-us/azure/virtual-desktop/set-up-mfa)

## Verification checklist
- [x] Entra authentication at subscribe, gateway connect and diagnostics, where Conditional Access applies.
- [x] With SSO the session host credential prompt is skipped; without it the client prompts every connection unless credentials are saved.
- [x] Smart card and Windows Hello for Business use Kerberos and need domain controller line of sight or a KDC proxy.
- [x] The five SSO tasks, in the documented order; enablerdsaadauth set to 1.
- [x] Hosts must be Entra joined or hybrid joined for SSO.

## Assumptions and design choices (not Learn requirements)
- Three-box framing is the author's. Changed: box 1 now notes that with SSO Conditional Access also applies at host sign-in through Windows Cloud Login.

## Unresolved questions for review
- None known.

## Recheck against Learn's own diagrams, 18 October 2026
The cited pages were checked for diagrams. They contain no Learn diagram of this subject (text, tables or portal screenshots only), so this drawing is the author's original composition and no Learn layout was copied. Page text was last checked in October 2026. This is not Microsoft verification.
