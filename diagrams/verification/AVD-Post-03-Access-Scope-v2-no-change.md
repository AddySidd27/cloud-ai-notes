# Access scope (post 3): checked, no redesign

File: `src/img/avd/AVD-Post-03-Access-Scope-v2.png` is unchanged and still referenced by its post.

## Learn references
- [Understand scope for Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview)

## Verification checklist
- [x] Four scope levels: management group, subscription, resource group, resource (scope-overview, "Scope levels").
- [x] Parent-child nesting, each level more specific; lower levels inherit role permissions from higher levels.
- [x] Scope defined as the set of resources an assignment applies to (same wording as the diagram footer).
- [x] Resources shown (VM, virtual network, storage account) are marked as examples.

## Assumptions and design choices
- Layout and resource choice are the author's. Learn has its own diagram to compare.

## Unresolved questions for review
- No accuracy issue found. Restyling to the v3 look is optional and was not done. The existing image was checked against the page text only; Learn's PNG diagram was not viewed. This is the author's check, not Microsoft verification or endorsement.

## Recheck, 18 October 2026
This diagram was not changed in the Learn recheck pass. Its earlier record stands, and it was not re-compared against a Learn picture in this pass.
