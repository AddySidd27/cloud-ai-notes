# Azure Files with Microsoft Entra Kerberos, hybrid users (post 4)

Files: `AVD-Post-04-Entra-Kerberos-v3` (.png, .svg, .drawio) in `src/img/avd/`; generator `diagrams/scripts/kerb_v3.py`.
Type: Documented flow (author layout and simplification)

Method and limits: each item was checked against the text of the cited Microsoft Learn pages (fetched October 2026) and, where Learn publishes its diagram as SVG, against that SVG's text labels. Learn's pictures were later viewed in a browser on 18 October 2026, see the recheck section. This record is the author's check, not Microsoft verification or endorsement.

## Learn references
- [Enable Microsoft Entra Kerberos authentication for hybrid and cloud-only identities on Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-identity-auth-hybrid-identities-enable)
- [Azure Virtual Desktop prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)

## Explanation
Setup steps 1 to 4 and the sign-in flow A and B for hybrid users, with the Conditional Access exclusion called out.

## Verification checklist
- [x] Hybrid identities need AD DS synced to Entra ID (Entra Connect Sync or Cloud Sync).
- [x] Setting ACLs needs unimpeded network connectivity to AD DS.
- [x] Clients must be Entra joined or hybrid joined (not Entra Domain Services joined or AD-only).
- [x] CloudKerberosTicketRetrievalEnabled lets the client retrieve a cloud Kerberos ticket at sign-in.
- [x] Admin consent is needed for the app Entra Kerberos creates on the storage account.
- [x] Exclude the storage account's Entra app from Conditional Access policies that require MFA.

## Assumptions and design choices (not Learn requirements)
- Arrows A and B simplify the Kerberos exchange; Learn gives the text steps, not this diagram.
- The device that sets ACLs is shown separately because Learn says it needs AD DS connectivity.

## Unresolved questions for review
- The label for step 3 depends on the Learn wording about the ACL tool and device; confirm no further requirement (for example domain-joined) is needed in the drawing.

## Recheck against Learn's own diagrams, 18 October 2026
The cited pages' text and diagrams were rechecked. These pages have no Learn diagram of this subject, or the diagram is a screenshot, so this drawing is the author's original composition and no Learn layout was copied. See `learn-diagram-notes.md` and `LEARN-RECHECK.md`.
