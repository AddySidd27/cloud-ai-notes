# Identity models (post 4): checked, no redesign

File: `src/img/avd/AVD-Post-04-Identity-Models-v2.png` is unchanged and still referenced by its post.

## Learn references
- [Azure Virtual Desktop prerequisites](https://learn.microsoft.com/en-us/azure/virtual-desktop/prerequisites)
- [Microsoft Entra joined session hosts in Azure Virtual Desktop](https://learn.microsoft.com/en-us/azure/virtual-desktop/azure-ad-joined-session-hosts)
- [What is Microsoft Entra Domain Services?](https://learn.microsoft.com/en-us/entra/identity/domain-services/overview)
- [Microsoft Entra hybrid joined devices](https://learn.microsoft.com/en-us/entra/identity/devices/concept-hybrid-join)

## Verification checklist
- [x] Entra joined session hosts need no line of sight to a domain controller or Entra Domain Services (azure-ad-joined-session-hosts).
- [x] Entra Domain Services domain controllers are fully managed by Microsoft; users synchronize one way from Entra ID (Domain Services overview).
- [x] Hybrid join means joined to on-premises AD and Entra ID (hybrid join page).
- [x] AVD prerequisites list Entra joined, AD DS joined and Entra Domain Services joined as supported; hybrid join is not supported with Entra Domain Services (checked earlier this session).

## Assumptions and design choices
- The title "Two choices" and the three-column layout are the author's.

## Unresolved questions for review
- No accuracy issue found. The banner says Entra ID authenticates access to the AVD service in every path; this matches the authentication documentation as read earlier, but wording could be re-confirmed. This is the author's check, not Microsoft verification or endorsement.

## Recheck, 18 October 2026
This diagram was not changed in the Learn recheck pass. Its earlier record stands, and it was not re-compared against a Learn picture in this pass.
